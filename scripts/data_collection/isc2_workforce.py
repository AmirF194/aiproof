"""ISC2 Cybersecurity Workforce Study loader (2025 edition).

ISC2 publishes the executive summary publicly each December. The detailed
PDF is gated behind a download form; we maintain a cached snapshot of the
top-line numbers used by the analysis.
"""
from __future__ import annotations

from _common import RAW, read_json

CACHE = RAW / "isc2_workforce_2025.json"


def collect() -> dict:
    return read_json(CACHE)


if __name__ == "__main__":
    p = collect()
    print(f"ISC2 2025 — global gap {p['global_workforce_gap']:,}, "
          f"US gap est. {p['us_workforce_gap_estimate']:,}, "
          f"orgs reporting critical-or-significant skill shortage "
          f"{p['orgs_reporting_critical_or_significant_skills_shortage_pct']}% "
          f"(up from {p['orgs_reporting_critical_or_significant_skills_shortage_pct_2024']}%)")
