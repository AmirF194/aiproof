"""Refresh all live posting feeds from public APIs.

Invokes the three real crawlers — HN Algolia, Greenhouse public boards,
Lever public boards — and writes normalised CSVs into data/raw/.

Run:
    python manage.py refresh_postings

Designed to be invoked from cron (weekly) on the production host.
Network failures are tolerated per-source: existing cache is preserved
when a fetch returns zero rows.
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


CRAWLERS = (
    "hn_who_is_hiring",
    "greenhouse_ats",
    "lever_ats",
)


class Command(BaseCommand):
    help = "Refresh live posting feeds (HN Who's Hiring, Greenhouse, Lever)."

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
