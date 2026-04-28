"""Produce the canonical role ranking.

Output: ``data/processed/role_ranking.csv`` — sorted by score desc, ties
sharing the same rank number (matches the table in REPORT.md).
"""
from __future__ import annotations

from _common import PROCESSED, ROLES, read_csv, write_csv

OUT = PROCESSED / "role_ranking.csv"


def rank() -> int:
    rows = read_csv(ROLES)
    rows.sort(key=lambda r: int(r["score"]), reverse=True)

    out = []
    last_score = None
    last_rank = 0
    for i, r in enumerate(rows, start=1):
        s = int(r["score"])
        if s != last_score:
            last_rank = i
            last_score = s
        out.append({
            "rank": last_rank,
            "role": r["role"],
            "category": r["category"],
            "score": s,
            "tier": r["verdict_tier"],
            "demand_trend": r["demand_trend"],
        })

    return write_csv(
        OUT, out,
        ["rank", "role", "category", "score", "tier", "demand_trend"],
    )


if __name__ == "__main__":
    n = rank()
    print(f"ranked {n} roles -> {OUT}")
