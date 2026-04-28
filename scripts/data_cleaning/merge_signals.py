"""Merge per-role metrics + canonical scores into one signal payload.

This is the single artifact downstream analysis (compute_scores.py,
trend_analysis.py) reads. It joins:
  - data/roles.csv             — canonical scoring inputs
  - data/processed/role_metrics.csv — derived from postings + AI mentions
  - data/processed/salary_per_role.csv — normalized comp

Output: ``data/processed/role_signals.json`` (per-role nested object)
"""
from __future__ import annotations

import json
from pathlib import Path

from _common import PROCESSED, read_csv, write_json

REPO = Path(__file__).resolve().parent.parent.parent
ROLES = REPO / "data" / "roles.csv"
METRICS = PROCESSED / "role_metrics.csv"
SAL = PROCESSED / "salary_per_role.csv"
OUT = PROCESSED / "role_signals.json"


def merge() -> int:
    roles = {r["role"]: r for r in read_csv(ROLES)}
    metrics = {r["role"]: r for r in read_csv(METRICS)}
    salaries = {r["role"]: r for r in read_csv(SAL)}

    payload = {"generated_at": "pipeline-output", "roles": []}
    for role, base in roles.items():
        m = metrics.get(role, {})
        s = salaries.get(role, {})
        payload["roles"].append({
            "role": role,
            "category": base["category"],
            "score_inputs": {
                "demand": int(base["demand"]),
                "automation_resistance": int(base["automation_resistance"]),
                "skill_depth": int(base["skill_depth"]),
                "strategic_importance": int(base["strategic_importance"]),
            },
            "score": int(base["score"]),
            "tier": base["verdict_tier"],
            "salary": {
                "tc_low_usd": int(base["salary_low_usd"]),
                "tc_high_usd": int(base["salary_high_usd"]),
                "base_low_glassdoor_simulated_usd": s.get("base_low_glassdoor_simulated_usd", ""),
                "base_high_glassdoor_simulated_usd": s.get("base_high_glassdoor_simulated_usd", ""),
                "sample_size_simulated": s.get("sample_size_simulated", ""),
            },
            "metrics": {
                "postings_2024_baseline": int(m.get("postings_2024_baseline", 0) or 0),
                "postings_2026_current": int(m.get("postings_2026_current", 0) or 0),
                "postings_yoy_pct": float(m.get("postings_yoy_pct", 0) or 0),
                "postings_2yr_pct": float(m.get("postings_2yr_pct", 0) or 0),
                "ai_mention_pct_2026": int(m.get("ai_mention_pct_2026", 0) or 0),
                "ai_mention_delta_pp": int(m.get("ai_mention_delta_pp", 0) or 0),
                "copilot_mention_pct_2026": int(m.get("copilot_mention_pct_2026", 0) or 0),
            },
            "trend_direction": m.get("trend_direction", base.get("demand_trend", "stable")),
        })

    payload["roles"].sort(key=lambda r: r["score"], reverse=True)
    write_json(OUT, payload)
    return len(payload["roles"])


if __name__ == "__main__":
    n = merge()
    print(f"merged {n} role signals -> {OUT}")
