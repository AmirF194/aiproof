"""Gartner forecasts loader (platform engineering, AI agents, AI code-assist).

Gartner research is paid, but headline numbers from their press releases and
public web pages are aggregated here. Cached snapshot lives at
``data/raw/gartner_forecasts_2025_2028.json``.
"""
from __future__ import annotations

from _common import RAW, read_json

CACHE = RAW / "gartner_forecasts_2025_2028.json"


def collect() -> dict:
    return read_json(CACHE)


if __name__ == "__main__":
    p = collect()
    for f in p["forecasts"]:
        print(f"- {f['topic']}: {f['metric']}")
