"""Schema + integrity checks for the role dataset.

Run:
    python manage.py validate_data

Exits non-zero on the first failure so it can gate CI and the deploy hook.
"""
from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from apps.roles import scoring
from apps.roles.models import TIER_ORDER, Category, Role, RoleMetric


class Command(BaseCommand):
    help = "Validate the role dataset for schema + scoring integrity."

    def handle(self, *args, **options):
        problems: list[str] = []

        # --- Cardinality ---
        # The original roster was exactly 1,000 hand-scored roles. We allow growth
        # via deterministic additions (e.g. umbrella titles whose scores are the
        # average of comparable specialized rows) but guard against silent loss.
        n_roles = Role.objects.count()
        if n_roles < 1000:
            problems.append(f"Expected at least 1,000 roles; have {n_roles}.")
        n_categories = Category.objects.count()
        if n_categories != 8:
            problems.append(f"Expected exactly 8 categories; have {n_categories}.")

        # --- Bounds on every score field ---
        bounded = [
            ("demand", 0, 10),
            ("automation_resistance", 0, 10),
            ("skill_depth", 0, 10),
            ("strategic_importance", 0, 10),
            ("human_judgment_score", 0, 10),
            ("stakeholder_interaction_score", 0, 10),
            ("physical_world_dependency_score", 0, 10),
            ("ai_augmentation_potential_score", 0, 10),
            ("regulatory_relevance_score", 0, 10),
            ("score", 0, 100),
            ("confidence_score", 0, 100),
        ]
        for field, lo, hi in bounded:
            out_of_range = Role.objects.filter(**{f"{field}__lt": lo}).count() + \
                           Role.objects.filter(**{f"{field}__gt": hi}).count()
            if out_of_range:
                problems.append(f"{out_of_range} roles have {field} outside [{lo}, {hi}].")

        # --- Tier validity ---
        bad_tier = Role.objects.exclude(tier__in=TIER_ORDER).count()
        if bad_tier:
            problems.append(f"{bad_tier} roles have an unknown tier value.")

        # --- Required string fields ---
        empty_slug = Role.objects.filter(slug="").count()
        if empty_slug:
            problems.append(f"{empty_slug} roles have an empty slug.")
        no_seniority = Role.objects.filter(seniority_level="").count()
        if no_seniority:
            problems.append(f"{no_seniority} roles have an empty seniority_level.")
        no_family = Role.objects.filter(role_family="").count()
        if no_family:
            problems.append(f"{no_family} roles have an empty role_family.")
        no_notes = Role.objects.filter(notes="").count()
        if no_notes:
            problems.append(
                f"{no_notes} roles have an empty notes field (expected 0 since "
                "docs/role_directory.md covers every role)."
            )

        # --- Scoring formula spot-check: re-derive HJ and AAP for a sample
        # and verify they match what's stored in the DB. ---
        sample = list(Role.objects.order_by("?")[:25])
        mismatches: list[str] = []
        for r in sample:
            expected_hj = scoring.human_judgment_score(r.automation_resistance, r.skill_depth)
            if expected_hj != (r.human_judgment_score or 0):
                mismatches.append(
                    f"{r.role}: human_judgment_score stored={r.human_judgment_score} expected={expected_hj}"
                )
            expected_aap = scoring.ai_augmentation_potential_score(r.automation_resistance, r.skill_depth)
            if expected_aap != (r.ai_augmentation_potential_score or 0):
                mismatches.append(
                    f"{r.role}: ai_augmentation_potential_score stored={r.ai_augmentation_potential_score} expected={expected_aap}"
                )
        if mismatches:
            problems.append(
                "Score formulas drifted from apps.roles.scoring — re-run load_roles. Examples:\n  - "
                + "\n  - ".join(mismatches[:5])
            )

        # --- Metrics sanity (only when present) ---
        bad_metric = RoleMetric.objects.filter(postings_2026_current__lt=0).count()
        if bad_metric:
            problems.append(f"{bad_metric} RoleMetric rows have negative postings.")

        # --- Final ---
        if problems:
            self.stderr.write(self.style.ERROR("validate_data: FAIL"))
            for p in problems:
                self.stderr.write(self.style.ERROR(f"  - {p}"))
            raise CommandError(f"{len(problems)} integrity problem(s) found.")

        self.stdout.write(
            self.style.SUCCESS(
                f"validate_data: OK — {n_roles} roles, {n_categories} categories, all bounds + formulas check out."
            )
        )
