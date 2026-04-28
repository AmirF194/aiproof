"""Cross-role trend extraction.

Joins the canonical scoring with the postings + AI-mention metrics in
``data/processed/role_metrics.csv`` to surface:

  - Roles with rising postings AND rising AI mentions (multipliers — AI
    raises throughput, headcount stays flat or grows)
  - Roles with falling postings AND rising AI mentions (compressors)
  - Roles with falling postings AND high AI-mention saturation (replacements)

Output: ``data/processed/trend_buckets.csv``
"""
from __future__ import annotations

from pathlib import Path

from _common import PROCESSED, ROLES, read_csv, write_csv


def classify_trend(postings_2yr_pct: float, ai_2026: int, ai_delta_pp: int) -> str:
    """Three-way bucket consistent with README's 'Multipliers / Compressors / Replacements'."""
    if postings_2yr_pct >= 5 and ai_delta_pp >= 15:
        return "multiplier"
    if postings_2yr_pct < -10 and ai_2026 >= 30:
        return "replacement"
    if postings_2yr_pct < 0 and ai_delta_pp >= 15:
        return "compressor"
    if postings_2yr_pct >= 5:
        return "growing"
    if postings_2yr_pct >= -5:
        return "stable"
    return "compressor"


def analyze() -> int:
    roles = {r["role"]: r for r in read_csv(ROLES)}
    metrics = {r["role"]: r for r in read_csv(PROCESSED / "role_metrics.csv")}

    rows = []
    for role, base in roles.items():
        m = metrics.get(role, {})
        p2yr = float(m.get("postings_2yr_pct", 0) or 0)
        ai_pct = int(m.get("ai_mention_pct_2026", 0) or 0)
        ai_delta = int(m.get("ai_mention_delta_pp", 0) or 0)
        bucket = classify_trend(p2yr, ai_pct, ai_delta)
        rows.append({
            "role": role,
            "category": base["category"],
            "score": int(base["score"]),
            "tier": base["verdict_tier"],
            "postings_2yr_pct": p2yr,
            "ai_mention_pct_2026": ai_pct,
            "ai_mention_delta_pp": ai_delta,
            "ai_impact_bucket": bucket,
        })

    rows.sort(key=lambda r: (r["ai_impact_bucket"], -r["score"]))
    return write_csv(
        PROCESSED / "trend_buckets.csv", rows,
        [
            "role", "category", "score", "tier",
            "postings_2yr_pct", "ai_mention_pct_2026", "ai_mention_delta_pp",
            "ai_impact_bucket",
        ],
    )


if __name__ == "__main__":
    n = analyze()
    print(f"classified {n} roles into trend buckets -> {PROCESSED / 'trend_buckets.csv'}")
