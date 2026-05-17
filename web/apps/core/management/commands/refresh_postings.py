"""Refresh all live posting feeds, aggregate to per-role metrics, push to DB.

Pipeline (Celery beat fires this weekly):
  1. Run 5 live crawlers (HN, Greenhouse, Lever, The Muse, Remotive)
       → writes raw CSVs to data/raw/
  2. Aggregate raw postings against the 1,000-role roster
       → writes data/processed/role_postings_live.csv
  3. update_live_metrics
       → updates RoleMetric rows in the database

Network failures are tolerated per-source: existing cache is preserved
when a fetch returns zero rows.
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


CRAWLERS = (
    "hn_who_is_hiring",
    "greenhouse_ats",
    "lever_ats",
    "themuse_api",
    "remotive_api",
)


class Command(BaseCommand):
    help = "Crawl live posting feeds, aggregate to roles, update DB metrics."

    def handle(self, *args, **options):
        scripts_dir = Path(settings.REPO_DIR) / "scripts" / "data_collection"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))

        results: list[tuple[str, int, float]] = []
        for name in CRAWLERS:
            t0 = time.monotonic()
            try:
                mod = importlib.import_module(name)
                # Each crawler exposes a `collect()` returning row count.
                count = int(mod.collect())
            except Exception as exc:  # noqa: BLE001
                self.stderr.write(self.style.ERROR(f"{name}: {exc!r}"))
                count = -1
            dur = time.monotonic() - t0
            results.append((name, count, dur))

        total = 0
        for name, count, dur in results:
            if count < 0:
                self.stdout.write(self.style.ERROR(f"  {name:24s}  FAILED  ({dur:.1f}s)"))
            else:
                total += count
                self.stdout.write(f"  {name:24s}  {count:>6d} rows  ({dur:.1f}s)")
        self.stdout.write(self.style.SUCCESS(f"refresh_postings: {total} total rows across {len(CRAWLERS)} sources"))

        # Aggregate raw → per-role metrics, then push into the database.
        clean_dir = Path(settings.REPO_DIR) / "scripts" / "data_cleaning"
        if str(clean_dir) not in sys.path:
            sys.path.insert(0, str(clean_dir))
        try:
            agg = importlib.import_module("aggregate_live_postings")
            n_roles = int(agg.aggregate())
            self.stdout.write(f"  aggregate_live_postings   {n_roles:>6d} roles matched")
        except Exception as exc:  # noqa: BLE001
            self.stderr.write(self.style.ERROR(f"aggregate_live_postings failed: {exc!r}"))
            return

        call_command("update_live_metrics")
