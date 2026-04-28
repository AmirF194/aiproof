"""Tech layoffs tracker (Q1 2026 snapshot).

Aggregates Challenger, Gray & Christmas + layoffs.fyi-style summaries.
Live scraping of layoffs.fyi requires a browser context (the site uses
client-side rendering) — out of scope for this stdlib pipeline. Cached
snapshot at ``data/raw/layoffs_q1_2026.json``.
"""
from __future__ import annotations

from _common import RAW, read_json

CACHE = RAW / "layoffs_q1_2026.json"


def collect() -> dict:
    return read_json(CACHE)


if __name__ == "__main__":
    p = collect()
    print(f"Q1 2026 tech layoffs (US): {p['tech_announced_us']:,} "
          f"(+{p['yoy_change_pct']}% YoY, ~{p['share_attributed_to_ai_pct']}% AI-attributed)")
    for fn in p["function_breakdown"][:5]:
        print(f"  {fn['function']:<48}  {fn['share_pct']}%")
