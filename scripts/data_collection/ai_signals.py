"""AI-mention signals across job postings (simulated, calibrated).

Reads ``data/raw/ai_mention_signals_simulated.csv`` — the share of postings
mentioning AI/LLM and AI coding tools (Copilot/Cursor) per role per month.

These series anchor the ``automation_resistance`` axis: where AI mention
rate climbs *and* posting volume falls, the work is being absorbed by AI;
where mention rate climbs *and* posting volume holds or grows, the role is
becoming AI-augmented (the multiplier pattern).
"""
from __future__ import annotations

import csv
from pathlib import Path

from _common import RAW

CSV_PATH = RAW / "ai_mention_signals_simulated.csv"


def collect() -> list[dict]:
    with CSV_PATH.open() as f:
        return list(csv.DictReader(f))


if __name__ == "__main__":
    rows = collect()
    by_role: dict[str, list[dict]] = {}
    for r in rows:
        by_role.setdefault(r["role"], []).append(r)
    print(f"{len(rows)} rows over {len(by_role)} roles")
    # show 5 fastest-growing AI mention rates 2024-01 -> 2026-01
    deltas = []
    for role, vals in by_role.items():
        if len(vals) < 2:
            continue
        first = int(vals[0]["pct_postings_mentioning_ai_or_llm"])
        last = int(vals[-1]["pct_postings_mentioning_ai_or_llm"])
        deltas.append((last - first, role))
    deltas.sort(reverse=True)
    print("Top 5 AI-mention growth (2024 -> 2026):")
    for d, r in deltas[:5]:
        print(f"  +{d:>3} pp  {r}")
