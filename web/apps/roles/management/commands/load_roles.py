import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from apps.roles import scoring
from apps.roles.models import Category, Role, RoleMetric, TierSummary


def _int(value: str) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def _float(value: str) -> float | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Load the 1,000 roles (and processed signals) from /data into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            type=Path,
            default=settings.DATA_DIR,
            help="Path to the data directory (default: repo /data).",
        )
        parser.add_argument(
            "--wipe",
            action="store_true",
            help="Delete all Roles, Categories, RoleMetrics before loading.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        data_dir: Path = opts["data_dir"]
        roles_csv = data_dir / "roles.csv"
        processed = data_dir / "processed"
        ranking_csv = processed / "role_ranking.csv"
        metrics_csv = processed / "role_metrics.csv"
        category_csv = processed / "category_summary.csv"
        tier_csv = processed / "tier_summary.csv"

        if not roles_csv.exists():
            raise CommandError(f"roles.csv not found at {roles_csv}")

        if opts["wipe"]:
            self.stdout.write("Wiping existing role data...")
            RoleMetric.objects.all().delete()
            Role.objects.all().delete()
            Category.objects.all().delete()
            TierSummary.objects.all().delete()

        categories = self._load_categories(roles_csv, category_csv)
        ranks = self._load_ranks(ranking_csv)
        descriptions = self._load_descriptions(data_dir)
        n_roles = self._load_roles(roles_csv, categories, ranks, descriptions)
        if metrics_csv.exists():
            n_metrics = self._load_metrics(metrics_csv)
        else:
            n_metrics = 0
        if tier_csv.exists():
            self._load_tiers(tier_csv)

        # After metrics are loaded, refresh confidence to account for live data + calibration.
        self._recompute_confidence()

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {n_roles} roles across {len(categories)} categories "
                f"({n_metrics} with extended metrics)."
            )
        )

    def _load_categories(
        self,
        roles_csv: Path,
        category_csv: Path,
    ) -> dict[str, Category]:
        names: set[str] = set()
        with roles_csv.open(newline="") as fh:
            for row in csv.DictReader(fh):
                names.add(row["category"])

        summaries: dict[str, dict] = {}
        if category_csv.exists():
            with category_csv.open(newline="") as fh:
                for row in csv.DictReader(fh):
                    summaries[row["category"]] = row

        categories: dict[str, Category] = {}
        for name in sorted(names):
            slug = slugify(name)[:140]
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": slug},
            )
            if not cat.slug:
                cat.slug = slug
            summary = summaries.get(name, {})
            cat.n_roles = _int(summary.get("n_roles", "")) or 0
            cat.avg_score = _float(summary.get("avg_score", "")) or 0
            cat.avg_demand = _float(summary.get("avg_demand", "")) or 0
            cat.avg_automation_resistance = (
                _float(summary.get("avg_automation_resistance", "")) or 0
            )
            cat.avg_skill_depth = _float(summary.get("avg_skill_depth", "")) or 0
            cat.avg_strategic_importance = (
                _float(summary.get("avg_strategic_importance", "")) or 0
            )
            cat.save()
            categories[name] = cat
        return categories

    def _load_descriptions(self, data_dir: Path) -> dict[str, str]:
        """Parse docs/role_directory.md → {role_name: one-line description}."""
        import re
        candidates = [
            data_dir.parent / "docs" / "role_directory.md",
            Path("/") / "docs" / "role_directory.md",
        ]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            return {}
        line_re = re.compile(r"^\s*-\s+\*\*(.+?)\*\*\s*[—\-]\s*(.+?)\s*$")
        out: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            m = line_re.match(line)
            if m:
                out[m.group(1).strip()] = m.group(2).strip()
        return out

    def _load_ranks(self, ranking_csv: Path) -> dict[tuple[str, str], int]:
        ranks: dict[tuple[str, str], int] = {}
        if not ranking_csv.exists():
            return ranks
        with ranking_csv.open(newline="") as fh:
            for row in csv.DictReader(fh):
                rank = _int(row["rank"]) or 0
                ranks[(row["role"], row["category"])] = rank
        return ranks

    def _load_roles(
        self,
        roles_csv: Path,
        categories: dict[str, Category],
        ranks: dict[tuple[str, str], int],
        descriptions: dict[str, str],
    ) -> int:
        n = 0
        with roles_csv.open(newline="") as fh:
            for row in csv.DictReader(fh):
                name = row["role"].strip()
                category = categories[row["category"]]
                category_name = category.name
                tier = (row.get("verdict_tier") or "").strip().lower().replace(
                    " ", "_"
                ).replace("-", "_")
                if tier == "atrisk":
                    tier = "at_risk"

                demand = _int(row["demand"]) or 0
                ar = _int(row["automation_resistance"]) or 0
                sd = _int(row["skill_depth"]) or 0
                si = _int(row["strategic_importance"]) or 0

                # --- Derived dimensions (deterministic; see apps.roles.scoring)
                seniority = scoring.parse_seniority(name)
                family = scoring.derive_role_family(name, category_name)
                hj = scoring.human_judgment_score(ar, sd)
                stake = scoring.stakeholder_interaction_score(demand, si, category_name, seniority)
                phys = scoring.physical_world_dependency_score(name, category_name)
                augment = scoring.ai_augmentation_potential_score(ar, sd)
                regul = scoring.regulatory_relevance_score(si, category_name)
                description = descriptions.get(name, "")

                # Confidence depends on data coverage; recomputed below in
                # _recompute_confidence_and_narratives after metrics are loaded.
                placeholder_conf = scoring.confidence_score(
                    scoring.ConfidenceInputs(
                        has_live_postings=False,
                        is_calibrated=False,
                        has_salary_band=bool(_int(row.get("salary_low_usd", ""))),
                        has_description=bool(description),
                    )
                )

                axis_scores = {
                    "demand": demand,
                    "automation_resistance": ar,
                    "skill_depth": sd,
                    "strategic_importance": si,
                    "human_judgment": hj,
                    "stakeholder_interaction": stake,
                }

                Role.objects.update_or_create(
                    role=name,
                    category=category,
                    defaults={
                        "demand": demand,
                        "automation_resistance": ar,
                        "skill_depth": sd,
                        "strategic_importance": si,
                        "score": _int(row["score"]) or 0,
                        "tier": tier or "stable",
                        "demand_trend": (row.get("demand_trend") or "flat")
                        .strip()
                        .lower(),
                        "salary_low_usd": _int(row.get("salary_low_usd", "")),
                        "salary_high_usd": _int(row.get("salary_high_usd", "")),
                        "rank": ranks.get((name, row["category"]), 0),
                        "notes": description,
                        "seniority_level": seniority,
                        "role_family": family,
                        "human_judgment_score": hj,
                        "stakeholder_interaction_score": stake,
                        "physical_world_dependency_score": phys,
                        "ai_augmentation_potential_score": augment,
                        "regulatory_relevance_score": regul,
                        "confidence_score": placeholder_conf,
                        "why_ai_resistant": scoring.why_ai_resistant(axis_scores),
                        "why_ai_exposed": scoring.why_ai_exposed(axis_scores),
                    },
                )
                n += 1
        return n

    def _recompute_confidence(self) -> None:
        """Final pass: now that metrics + descriptions are loaded, refresh confidence."""
        roles = Role.objects.select_related("metrics").all()
        for r in roles:
            metrics = getattr(r, "metrics", None)
            has_live = bool(metrics and (metrics.postings_2026_current or 0) > 0)
            # Calibrated = role appears in the original hand-scored 36 (proxy: postings_2024_baseline set).
            is_calibrated = bool(metrics and metrics.postings_2024_baseline)
            r.confidence_score = scoring.confidence_score(
                scoring.ConfidenceInputs(
                    has_live_postings=has_live,
                    is_calibrated=is_calibrated,
                    has_salary_band=bool(r.salary_low_usd),
                    has_description=bool(r.notes),
                )
            )
            r.save(update_fields=["confidence_score"])

    def _load_metrics(self, metrics_csv: Path) -> int:
        n = 0
        with metrics_csv.open(newline="") as fh:
            for row in csv.DictReader(fh):
                try:
                    role = Role.objects.get(role=row["role"])
                except Role.DoesNotExist:
                    continue
                except Role.MultipleObjectsReturned:
                    role = Role.objects.filter(role=row["role"]).first()
                    if role is None:
                        continue
                RoleMetric.objects.update_or_create(
                    role=role,
                    defaults={
                        "postings_2024_baseline": _int(row.get("postings_2024_baseline", "")),
                        "postings_2025_jan": _int(row.get("postings_2025_jan", "")),
                        "postings_2026_current": _int(row.get("postings_2026_current", "")),
                        "postings_yoy_pct": _float(row.get("postings_yoy_pct", "")),
                        "postings_2yr_pct": _float(row.get("postings_2yr_pct", "")),
                        "ai_mention_pct_2026": _float(row.get("ai_mention_pct_2026", "")),
                        "ai_mention_delta_pp": _float(row.get("ai_mention_delta_pp", "")),
                        "copilot_mention_pct_2026": _float(row.get("copilot_mention_pct_2026", "")),
                        "trend_direction": (row.get("trend_direction") or "").strip(),
                    },
                )
                n += 1
        return n

    def _load_tiers(self, tier_csv: Path) -> None:
        with tier_csv.open(newline="") as fh:
            for row in csv.DictReader(fh):
                tier = (row["verdict_tier"] or "").strip().lower().replace(
                    " ", "_"
                ).replace("-", "_")
                if tier == "atrisk":
                    tier = "at_risk"
                TierSummary.objects.update_or_create(
                    tier=tier,
                    defaults={
                        "n_roles": _int(row.get("n_roles", "")) or 0,
                        "avg_score": _float(row.get("avg_score", "")) or 0,
                        "avg_demand": _float(row.get("avg_demand", "")) or 0,
                        "avg_automation_resistance": _float(
                            row.get("avg_automation_resistance", "")
                        )
                        or 0,
                        "avg_skill_depth": _float(row.get("avg_skill_depth", "")) or 0,
                        "avg_strategic_importance": _float(
                            row.get("avg_strategic_importance", "")
                        )
                        or 0,
                    },
                )
