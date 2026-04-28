"""Reduce postings + AI-mention time-series to one row per role.

For each role, compute:
  - postings_2024_baseline (Jan 2024, LinkedIn-sim)
  - postings_2026_current (Jan 2026, LinkedIn-sim)
  - postings_yoy_pct           : (2026 / 2025-Jan - 1) * 100
  - postings_2yr_pct           : (2026 / 2024 - 1) * 100
  - ai_mention_pct_2026        : pct of postings mentioning AI/LLM
  - ai_mention_delta_pp        : 2024 -> 2026 change in pp
  - copilot_mention_pct_2026   : pct of postings mentioning Copilot/Cursor
  - trend_direction            : rising/stable/declining (rule-based)

Output: ``data/processed/role_metrics.csv``
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from _common import PROCESSED, RAW, read_csv, write_csv

LINKEDIN = RAW / "linkedin_postings_simulated.csv"
AI = RAW / "ai_mention_signals_simulated.csv"
OUT = PROCESSED / "role_metrics.csv"


def _by_role(rows: list[dict], value_key: str) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = defaultdict(dict)
    for r in rows:
        out[r["role"].strip()][r["month"].strip()] = int(r[value_key])
    return out


def _trend_label(p2024: int, p2026: int) -> str:
    if p2024 == 0:
        return "rising"
    pct = (p2026 - p2024) / p2024 * 100
    if pct >= 8:
        return "rising"
    if pct <= -8:
        return "declining"
    return "stable"


def compute() -> int:
    postings = _by_role(read_csv(LINKEDIN), "postings_count")
    ai_main = _by_role(read_csv(AI), "pct_postings_mentioning_ai_or_llm")
    ai_copilot = _by_role(read_csv(AI), "pct_postings_mentioning_copilot_or_cursor")

    rows = []
    for role, series in postings.items():
        p_2024 = series.get("2024-01", 0)
        p_2025 = series.get("2025-01", 0)
        p_2026 = series.get("2026-01", 0)
        ai_2024 = ai_main.get(role, {}).get("2024-01", 0)
        ai_2026 = ai_main.get(role, {}).get("2026-01", 0)
        cop_2026 = ai_copilot.get(role, {}).get("2026-01", 0)

        rows.append({
            "role": role,
            "postings_2024_baseline": p_2024,
            "postings_2025_jan": p_2025,
            "postings_2026_current": p_2026,
            "postings_yoy_pct": round((p_2026 - p_2025) / p_2025 * 100, 1) if p_2025 else "",
            "postings_2yr_pct": round((p_2026 - p_2024) / p_2024 * 100, 1) if p_2024 else "",
            "ai_mention_pct_2026": ai_2026,
            "ai_mention_delta_pp": ai_2026 - ai_2024,
            "copilot_mention_pct_2026": cop_2026,
            "trend_direction": _trend_label(p_2024, p_2026),
        })

    rows.sort(key=lambda r: r["role"])
    return write_csv(
        OUT, rows,
        [
            "role", "postings_2024_baseline", "postings_2025_jan", "postings_2026_current",
            "postings_yoy_pct", "postings_2yr_pct",
            "ai_mention_pct_2026", "ai_mention_delta_pp",
            "copilot_mention_pct_2026", "trend_direction",
        ],
    )


if __name__ == "__main__":
    n = compute()
    print(f"computed {n} role-metric rows -> {OUT}")
