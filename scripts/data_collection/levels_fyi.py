"""Levels.fyi compensation snapshots.

Levels.fyi has no public API. Production scrapers must respect the site's
ToS and rate limits. This module reads the cached real snapshot we
maintain at ``data/raw/levels_fyi_compensation_2026.json`` and exposes it
to the pipeline.
"""
from __future__ import annotations

from _common import RAW, read_json

CACHE = RAW / "levels_fyi_compensation_2026.json"


def collect() -> dict:
    return read_json(CACHE)


if __name__ == "__main__":
    p = collect()
    ml = p["ml_engineer"]
    print(f"ML Engineer median TC: ${ml['median_tc_overall']:,}")
    for c in ml["by_company"][:5]:
        print(f"  {c['company']:<10}  ${c['median_tc']:>7,}")
