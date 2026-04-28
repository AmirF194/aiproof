"""Stack Overflow Developer Survey loader.

The 2025 survey is publicly downloadable as a CSV. This module exposes the
real headline numbers via the cached snapshot. To process the full
respondent CSV, place it at data/raw/stackoverflow_2025_full.csv and use
the helper below.
"""
from __future__ import annotations

import csv
from pathlib import Path

from _common import RAW, read_json

CACHE = RAW / "stackoverflow_developer_survey_2025.json"
FULL_CSV = RAW / "stackoverflow_2025_full.csv"


def collect() -> dict:
    return read_json(CACHE)


def aggregate_full_csv() -> dict | None:
    """Aggregate the full SO survey CSV if present. Returns None if missing."""
    if not FULL_CSV.exists():
        return None
    counts: dict[str, int] = {"total": 0, "uses_ai_daily": 0, "trusts_ai": 0}
    with FULL_CSV.open() as f:
        for row in csv.DictReader(f):
            counts["total"] += 1
            if row.get("AISelect", "").startswith("Yes"):
                counts["uses_ai_daily"] += 1
            if row.get("AITrust", "") in ("Highly trust", "Somewhat trust"):
                counts["trusts_ai"] += 1
    return counts


if __name__ == "__main__":
    p = collect()
    ai = p["ai_use"]
    print(f"SO 2025 AI use: {ai['using_or_planning_to_use_ai_tools_pct']}% "
          f"(daily {ai['professional_developers_using_daily_pct']}%, "
          f"trust {ai['trust_ai_output_pct']}%)")
