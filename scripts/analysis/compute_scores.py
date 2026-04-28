"""Recompute the Career Safety Score for every role from the four axes.

This script is the single canonical implementation of the rubric. It:
  1. reads data/roles.csv
  2. recomputes score = round((0.30·D + 0.35·AR + 0.15·SD + 0.20·SI) * 10)
  3. assigns tier from the score band
  4. writes data/processed/score_components.csv and verifies the published
     scores in data/roles.csv match (raises if any drift)

Run after editing the four-axis values in data/roles.csv.
"""
from __future__ import annotations

from pathlib import Path

from _common import PROCESSED, ROLES, read_csv, score, tier, write_csv

OUT = PROCESSED / "score_components.csv"


def compute(strict: bool = True) -> int:
    rows_in = read_csv(ROLES)
    rows_out = []
    drift = []

    for r in rows_in:
        d = int(r["demand"])
        ar = int(r["automation_resistance"])
        sd = int(r["skill_depth"])
        si = int(r["strategic_importance"])
        s = score(d, ar, sd, si)
        t = tier(s)

        published_score = int(r["score"])
        published_tier = r["verdict_tier"]
        if s != published_score or t != published_tier:
            drift.append((r["role"], published_score, s, published_tier, t))

        rows_out.append({
            "role": r["role"],
            "category": r["category"],
            "demand": d,
            "automation_resistance": ar,
            "skill_depth": sd,
            "strategic_importance": si,
            "weighted_demand":   round(0.30 * d, 4),
            "weighted_ar":       round(0.35 * ar, 4),
            "weighted_sd":       round(0.15 * sd, 4),
            "weighted_si":       round(0.20 * si, 4),
            "score_recomputed": s,
            "tier_recomputed": t,
            "score_published": published_score,
            "tier_published": published_tier,
            "drift": "yes" if (s != published_score or t != published_tier) else "no",
        })

    rows_out.sort(key=lambda x: x["score_recomputed"], reverse=True)
    write_csv(
        OUT, rows_out,
        [
            "role", "category",
            "demand", "automation_resistance", "skill_depth", "strategic_importance",
            "weighted_demand", "weighted_ar", "weighted_sd", "weighted_si",
            "score_recomputed", "tier_recomputed",
            "score_published", "tier_published",
            "drift",
        ],
    )

    if drift and strict:
        msg = "\n".join(
            f"  {role}: published score={ps} recomputed={rs}  "
            f"published_tier={pt} recomputed={rt}"
            for role, ps, rs, pt, rt in drift
        )
        raise SystemExit(
            f"score drift detected — published vs recomputed mismatch in {len(drift)} roles:\n{msg}"
        )

    return len(rows_out)


if __name__ == "__main__":
    n = compute()
    print(f"recomputed {n} role scores -> {OUT}  (no drift)")
