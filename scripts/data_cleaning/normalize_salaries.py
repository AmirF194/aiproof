"""Normalize the salary inputs into a single per-role record.

Reconciles Glassdoor-simulated bands with Levels.fyi anchor points (ML eng
specifically) and the existing data/roles.csv senior-IC ranges.

Output: ``data/processed/salary_per_role.csv``
"""
from __future__ import annotations

from _common import PROCESSED, RAW, read_csv, read_json, write_csv

GLASS = RAW / "glassdoor_salary_simulated.csv"
LEVELS = RAW / "levels_fyi_compensation_2026.json"
ROLES = Path(__file__).resolve().parent.parent.parent / "data" / "roles.csv" \
    if False else None  # placeholder to keep imports tidy

# Simpler: direct import of the canonical roles.csv path
from pathlib import Path
ROLES_CSV = Path(__file__).resolve().parent.parent.parent / "data" / "roles.csv"
OUT = PROCESSED / "salary_per_role.csv"


def normalize() -> int:
    glass = {r["role"]: r for r in read_csv(GLASS)}
    levels = read_json(LEVELS)
    roles = read_csv(ROLES_CSV)

    rows = []
    for r in roles:
        role = r["role"]
        g = glass.get(role, {})
        rows.append({
            "role": role,
            "category": r["category"],
            "tc_low_canonical_usd": int(r["salary_low_usd"]),
            "tc_high_canonical_usd": int(r["salary_high_usd"]),
            "tc_low_glassdoor_simulated_usd": int(g.get("total_comp_low_usd", 0)) or "",
            "tc_high_glassdoor_simulated_usd": int(g.get("total_comp_high_usd", 0)) or "",
            "base_low_glassdoor_simulated_usd": int(g.get("base_low_usd", 0)) or "",
            "base_high_glassdoor_simulated_usd": int(g.get("base_high_usd", 0)) or "",
            "sample_size_simulated": int(g.get("sample_size", 0)) or "",
            "levels_fyi_anchor_role": "ML Engineer" if role == "ML Engineer" else "",
            "levels_fyi_anchor_median_usd":
                levels["ml_engineer"]["median_tc_overall"] if role == "ML Engineer" else "",
        })

    return write_csv(
        OUT, rows,
        [
            "role", "category",
            "tc_low_canonical_usd", "tc_high_canonical_usd",
            "tc_low_glassdoor_simulated_usd", "tc_high_glassdoor_simulated_usd",
            "base_low_glassdoor_simulated_usd", "base_high_glassdoor_simulated_usd",
            "sample_size_simulated",
            "levels_fyi_anchor_role", "levels_fyi_anchor_median_usd",
        ],
    )


if __name__ == "__main__":
    n = normalize()
    print(f"normalized {n} salary rows -> {OUT}")
