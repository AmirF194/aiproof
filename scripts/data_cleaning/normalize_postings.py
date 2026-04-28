"""Normalize LinkedIn + Indeed simulated postings into a single time-series.

Output: ``data/processed/postings_timeseries.csv``
Columns: role, month, source, postings_count, data_kind
"""
from __future__ import annotations

from pathlib import Path

from _common import PROCESSED, RAW, read_csv, write_csv

LINKEDIN = RAW / "linkedin_postings_simulated.csv"
INDEED = RAW / "indeed_postings_simulated.csv"
OUT = PROCESSED / "postings_timeseries.csv"


def normalize() -> int:
    rows = []
    for src, path in (("linkedin", LINKEDIN), ("indeed", INDEED)):
        for r in read_csv(path):
            rows.append({
                "role": r["role"].strip(),
                "month": r["month"].strip(),
                "source": src,
                "postings_count": int(r["postings_count"]),
                "data_kind": r["data_kind"].strip(),
            })
    rows.sort(key=lambda r: (r["role"], r["month"], r["source"]))
    return write_csv(
        OUT, rows,
        ["role", "month", "source", "postings_count", "data_kind"],
    )


if __name__ == "__main__":
    n = normalize()
    print(f"normalized {n} rows -> {OUT}")
