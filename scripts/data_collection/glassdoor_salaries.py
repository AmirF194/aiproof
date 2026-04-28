"""Glassdoor salary aggregator (simulated, calibrated to Levels.fyi/Glassdoor public bands).

Glassdoor scraping is gated by login + bot detection. We maintain a
calibrated simulated dataset under
``data/raw/glassdoor_salary_simulated.csv``. Bands are consistent with
Levels.fyi senior-IC ranges and KORE1 / Acceler8 published guides cited in
INSIGHTS.md.
"""
from __future__ import annotations

import csv

from _common import RAW

CSV_PATH = RAW / "glassdoor_salary_simulated.csv"


def collect() -> list[dict]:
    with CSV_PATH.open() as f:
        return list(csv.DictReader(f))


if __name__ == "__main__":
    rows = collect()
    print(f"{len(rows)} salary rows.  Top 5 by max TC:")
    rows_sorted = sorted(rows, key=lambda r: int(r["total_comp_high_usd"]), reverse=True)
    for r in rows_sorted[:5]:
        print(f"  {r['role']:<35}  ${int(r['total_comp_low_usd']):>7,}-${int(r['total_comp_high_usd']):>7,}")
