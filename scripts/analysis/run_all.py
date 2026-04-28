"""Run the full analysis layer.

Order matters: compute_scores -> rank_roles -> tier_classification
-> trend_analysis. Each writes its own artifact under data/processed/.

Usage:
    python3 scripts/analysis/run_all.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compute_scores
import rank_roles
import tier_classification
import trend_analysis


def main() -> int:
    print("== Tech-Jobs analysis ==\n")
    n = compute_scores.compute()
    print(f"  score_components.csv     ({n} roles, no drift)")
    n = rank_roles.rank()
    print(f"  role_ranking.csv         ({n} roles)")
    nt, nc = tier_classification.classify()
    print(f"  tier_summary.csv         ({nt} tiers)")
    print(f"  category_summary.csv     ({nc} categories)")
    n = trend_analysis.analyze()
    print(f"  trend_buckets.csv        ({n} roles)")
    print("\nAnalysis complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
