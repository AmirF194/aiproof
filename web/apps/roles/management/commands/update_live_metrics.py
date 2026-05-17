"""Load data/processed/role_postings_live.csv into RoleMetric rows.

Sets the postings_2026_current, postings_yoy_pct, ai_mention_pct_2026,
and copilot_mention_pct_2026 fields from the freshly aggregated live
posting data. Roles with no live matches are left untouched (their
calibrated values from the static pipeline remain).

Run:
    python manage.py update_live_metrics
"""
from __future__ import annotations

import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.roles.models import Role, RoleMetric


class Command(BaseCommand):
    help = "Update RoleMetric from data/processed/role_postings_live.csv."

    def handle(self, *args, **options):
        csv_path = Path(settings.PROCESSED_DIR) / "role_postings_live.csv"
        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"missing input: {csv_path}"))
            return

        # Build slug → Role lookup once.
        roles_by_slug = {r.slug: r for r in Role.objects.all()}
        roles_by_name = {r.role.lower(): r for r in roles_by_slug.values()}

        updated = 0
        skipped = 0
        with csv_path.open() as f:
            for row in csv.DictReader(f):
                role = roles_by_slug.get(row["role_slug"])
                if role is None:
                    # Fall back to a name match — aggregator slugifier may differ
                    # from Django's slugify in edge cases.
                    role = (
                        roles_by_name.get(row["role_name"].lower())
                        or roles_by_slug.get(slugify(row["role_name"]))
                    )
                if role is None:
                    skipped += 1
                    continue

                postings = int(row["postings_total"] or 0)
                yoy = row.get("postings_yoy_pct") or ""
                ai_pct = float(row["ai_mention_pct"] or 0) or None
                metric, _ = RoleMetric.objects.get_or_create(role=role)
                metric.postings_2026_current = postings
                if yoy not in ("", None):
                    metric.postings_yoy_pct = float(yoy)
                metric.ai_mention_pct_2026 = ai_pct
                metric.save()
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"update_live_metrics: {updated} updated, {skipped} unmatched")
        )
