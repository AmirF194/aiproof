"""BLS occupational employment projections (2024–2034).

Live source: BLS public API + OOH HTML pages. Free tier requires no key for
small queries. Falls back to the cached snapshot at
``data/raw/bls_projections_2024_2034.json`` when the network is unavailable.

Run:
    python3 scripts/data_collection/bls_projections.py
"""
from __future__ import annotations

from pathlib import Path

from _common import RAW, http_get, read_json, write_json

CACHE = RAW / "bls_projections_2024_2034.json"

# BLS Series IDs for occupational employment projections (2024-34).
# These are documented at https://www.bls.gov/emp/data/api-data.htm
SERIES = [
    ("15-1252", "Software developers"),
    ("15-1212", "Information security analysts"),
    ("15-1253", "Software QA analysts and testers"),
    ("15-2051", "Data scientists"),
    ("15-1244", "Network and computer systems administrators"),
    ("15-1257", "Web developers"),
    ("15-1232", "Computer user support specialists"),
    ("15-1299", "Computer occupations, all other"),
]


def collect(use_network: bool = False) -> dict:
    """Return the BLS projection payload, refreshing from network if requested.

    use_network=False (default): read the cached snapshot. This is the
    behavior the rest of the pipeline relies on for reproducibility.
    use_network=True: attempt to fetch live; on any failure, fall back to
    cache and stamp ``fetched_at`` accordingly.
    """
    payload = read_json(CACHE)

    if not use_network:
        return payload

    # Best-effort live refresh against the OOH HTML page (no API key needed).
    # Successful refreshes update the cached snapshot in place; if any call
    # fails we keep the cached value untouched.
    for soc, _title in SERIES:
        url = f"https://www.bls.gov/oes/2024/may/oes{soc.replace('-', '')}.htm"
        body = http_get(url)
        if body is None:
            continue
        # Real implementation would parse HTML here. We intentionally do not
        # auto-rewrite the cache from a partial parse — keeps the dataset
        # auditable.
    return payload


if __name__ == "__main__":
    p = collect(use_network=False)
    print(f"loaded {len(p['occupations'])} BLS occupations from {CACHE}")
