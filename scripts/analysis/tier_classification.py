"""Aggregate roles by tier and category.

Output:
  - ``data/processed/tier_summary.csv`` — # roles, avg score, avg demand
    by tier
  - ``data/processed/category_summary.csv`` — same, by category
"""
from __future__ import annotations

from collections import defaultdict

from _common import PROCESSED, ROLES, read_csv, write_csv

TIERS = ["fortress", "safe", "stable", "exposed", "at_risk"]
CATS = [
    "Engineering Leadership", "Security", "Data & AI",
    "Platform & Infrastructure", "Engineering",
    "Quality & Testing", "Product & Design", "Specialized & Emerging",
]


def _summarize(rows: list[dict], key: str, order: list[str]) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[r[key]].append(r)
    out = []
    for k in order:
        bucket = buckets.get(k, [])
        if not bucket:
            continue
        out.append({
            key: k,
            "n_roles": len(bucket),
            "avg_score": round(sum(int(b["score"]) for b in bucket) / len(bucket), 1),
            "avg_demand": round(sum(int(b["demand"]) for b in bucket) / len(bucket), 2),
            "avg_automation_resistance": round(sum(int(b["automation_resistance"]) for b in bucket) / len(bucket), 2),
            "avg_skill_depth": round(sum(int(b["skill_depth"]) for b in bucket) / len(bucket), 2),
            "avg_strategic_importance": round(sum(int(b["strategic_importance"]) for b in bucket) / len(bucket), 2),
        })
    return out


def classify() -> tuple[int, int]:
    rows = read_csv(ROLES)
    tier_rows = _summarize(rows, "verdict_tier", TIERS)
    cat_rows = _summarize(rows, "category", CATS)
    n_tiers = write_csv(
        PROCESSED / "tier_summary.csv",
        tier_rows,
        ["verdict_tier", "n_roles", "avg_score", "avg_demand",
         "avg_automation_resistance", "avg_skill_depth", "avg_strategic_importance"],
    )
    n_cats = write_csv(
        PROCESSED / "category_summary.csv",
        cat_rows,
        ["category", "n_roles", "avg_score", "avg_demand",
         "avg_automation_resistance", "avg_skill_depth", "avg_strategic_importance"],
    )
    return n_tiers, n_cats


if __name__ == "__main__":
    nt, nc = classify()
    print(f"tier_summary.csv ({nt} tiers)  category_summary.csv ({nc} categories)")
