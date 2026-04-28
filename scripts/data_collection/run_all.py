"""Run every data-collection module and print a summary.

This is the entry point you run after editing or refreshing the
``data/raw/`` snapshots. It validates every cached file is loadable and
reports the headline metric from each source.

Usage:
    python3 scripts/data_collection/run_all.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running as a script (no -m) by adding our directory to sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import bls_projections
import gartner_forecasts
import github_octoverse
import glassdoor_salaries
import isc2_workforce
import job_postings_simulated
import layoffs_tracker
import levels_fyi
import stackoverflow_survey
import ai_signals


def main() -> int:
    print("== Tech-Jobs data collection ==\n")

    bls = bls_projections.collect()
    print(f"[BLS]    {len(bls['occupations'])} occupations loaded")

    isc = isc2_workforce.collect()
    print(f"[ISC2]   global workforce gap {isc['global_workforce_gap']:,}; "
          f"{isc['orgs_reporting_critical_or_significant_skills_shortage_pct']}% orgs critical-shortage")

    levels = levels_fyi.collect()
    print(f"[Levels] ML Engineer median TC ${levels['ml_engineer']['median_tc_overall']:,}; "
          f"{len(levels['ml_engineer']['by_company'])} companies")

    so = stackoverflow_survey.collect()
    print(f"[SO]     {so['ai_use']['using_or_planning_to_use_ai_tools_pct']}% AI use, "
          f"{so['ai_use']['professional_developers_using_daily_pct']}% daily, "
          f"{so['ai_use']['trust_ai_output_pct']}% trust")

    gartner = gartner_forecasts.collect()
    print(f"[Gartner] {len(gartner['forecasts'])} forecasts")

    layoffs = layoffs_tracker.collect()
    print(f"[Layoffs] Q1 2026 {layoffs['tech_announced_us']:,} (+{layoffs['yoy_change_pct']}%, "
          f"~{layoffs['share_attributed_to_ai_pct']}% AI)")

    octo = github_octoverse.collect()
    print(f"[GitHub] {octo['developer_population']['total_developers_on_github_millions']}M devs")

    glass = glassdoor_salaries.collect()
    print(f"[Glassdoor] {len(glass)} salary rows")

    postings = job_postings_simulated.collect()
    print(f"[LinkedIn-sim] {len(postings['linkedin'])} rows  "
          f"[Indeed-sim] {len(postings['indeed'])} rows")

    ai = ai_signals.collect()
    print(f"[AI-mentions-sim] {len(ai)} rows")

    print("\nAll collectors loaded successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
