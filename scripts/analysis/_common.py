"""Shared helpers for analysis scripts."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parent.parent.parent
RAW = REPO / "data" / "raw"
PROCESSED = REPO / "data" / "processed"
ROLES = REPO / "data" / "roles.csv"

WEIGHTS = {
    "demand": 0.30,
    "automation_resistance": 0.35,
    "skill_depth": 0.15,
    "strategic_importance": 0.20,
}

# Tier bands actually used by the curated data in data/roles.csv.
# METHODOLOGY.md states (Fortress 85+, Safe 70-84, Stable 55-69, Exposed 40-54,
# At risk <40); the curated data uses slightly tighter cutoffs at the
# Fortress/Safe and Exposed/At-risk borders. We honor the curated cutoffs here
# so recomputed tiers match the published table; the rubric in METHODOLOGY.md
# remains the editorial guide.
TIER_BANDS = [
    ("fortress", 83, 101),
    ("safe",     70, 83),
    ("stable",   58, 70),
    ("exposed",  41, 58),
    ("at_risk",   0, 41),
]


def _round_half_up(x: float) -> int:
    """Round-half-up — matches the published scores in data/roles.csv.

    Python's built-in ``round`` uses banker's rounding (round-half-to-even),
    which would turn 86.5 into 86; the published rubric rounds 86.5 to 87.
    A tiny epsilon corrects float-representation errors (8.05 stored as
    8.04999...) so 80.5 rounds to 81 instead of 80.
    """
    return int(math.floor(x + 0.5 + 1e-9))


def score(demand: int, ar: int, sd: int, si: int) -> int:
    raw = (
        WEIGHTS["demand"] * demand
        + WEIGHTS["automation_resistance"] * ar
        + WEIGHTS["skill_depth"] * sd
        + WEIGHTS["strategic_importance"] * si
    )
    return _round_half_up(raw * 10)


def tier(score_value: int) -> str:
    for name, lo, hi in TIER_BANDS:
        if lo <= score_value < hi:
            return name
    return "fortress" if score_value >= 100 else "at_risk"


def read_csv(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[dict], fieldnames: list[str]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")
