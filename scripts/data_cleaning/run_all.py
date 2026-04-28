"""Run every cleaning step in order.

Usage:
    python3 scripts/data_cleaning/run_all.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compute_role_metrics
import merge_signals
import normalize_postings
import normalize_salaries


def main() -> int:
    print("== Tech-Jobs data cleaning ==\n")
    n = normalize_postings.normalize()
    print(f"  postings_timeseries.csv     ({n} rows)")
    n = normalize_salaries.normalize()
    print(f"  salary_per_role.csv         ({n} rows)")
    n = compute_role_metrics.compute()
    print(f"  role_metrics.csv            ({n} rows)")
    n = merge_signals.merge()
    print(f"  role_signals.json           ({n} roles)")
    print("\nClean complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
