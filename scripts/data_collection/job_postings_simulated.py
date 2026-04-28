"""Job-postings dataset (LinkedIn + Indeed) — simulated.

LinkedIn's Talent Insights and Indeed's hiring data require contracted
access. Live scraping is contested and rate-limited. For the analysis we
maintain a calibrated simulated dataset under
``data/raw/linkedin_postings_simulated.csv`` and
``data/raw/indeed_postings_simulated.csv``.

Calibration anchors:
  - Frontend share <20% of total IT postings and falling (TheFrontendCo)
  - Senior PM postings +87% YoY (Lenny's)
  - Data analyst postings declining; AI Application Engineer rising
  - Per-role 2024-01 baseline cross-checked against public BLS OEWS counts
    where the SOC code maps cleanly.

The ``simulated`` flag is preserved on every row.
"""
from __future__ import annotations

import csv
from pathlib import Path

from _common import RAW

LINKEDIN = RAW / "linkedin_postings_simulated.csv"
INDEED = RAW / "indeed_postings_simulated.csv"


def _read(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def collect_linkedin() -> list[dict]:
    return _read(LINKEDIN)


def collect_indeed() -> list[dict]:
    return _read(INDEED)


def collect() -> dict:
    return {"linkedin": collect_linkedin(), "indeed": collect_indeed()}


if __name__ == "__main__":
    li = collect_linkedin()
    ind = collect_indeed()
    print(f"LinkedIn rows: {len(li)} ({len({r['role'] for r in li})} roles)")
    print(f"Indeed   rows: {len(ind)} ({len({r['role'] for r in ind})} roles)")
