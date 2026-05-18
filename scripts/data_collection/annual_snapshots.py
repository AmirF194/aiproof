"""Tier 5 — annual snapshot polling for the cited research sources.

For each annual source we cite, this crawler checks whether the publisher
has shipped a newer release than our cached snapshot. It does NOT auto-
download or auto-parse — instead it writes a status JSON noting which
sources have a fresher release upstream, so a human can review and pull
the new data deliberately.

This keeps the binding rule intact (no fabricated data, no auto-ingest
of unverified releases) while still giving us a continuous "is our
annual snapshot still current?" signal.

Output: data/raw/annual_snapshots_status.json
"""
from __future__ import annotations

import datetime as _dt
import json
import re

from _common import RAW, http_get

OUT = RAW / "annual_snapshots_status.json"

# Each source has:
#   - cache_year: the year of the snapshot currently on disk
#   - feed_url: a URL we can GET to detect a new release
#   - year_regex: pattern to extract the published year from the feed page
SOURCES: tuple[dict, ...] = (
    {
        "key": "stackoverflow_survey",
        "name": "Stack Overflow Developer Survey",
        "cache_year": 2025,
        "feed_url": "https://survey.stackoverflow.co/",
        "year_regex": r"(?:Survey|Results)\s+(\d{4})",
    },
    {
        "key": "github_octoverse",
        "name": "GitHub Octoverse",
        "cache_year": 2025,
        "feed_url": "https://octoverse.github.com/",
        "year_regex": r"Octoverse[^\d]*(\d{4})",
    },
    {
        "key": "isc2_workforce",
        "name": "ISC2 Cybersecurity Workforce Study",
        "cache_year": 2025,
        "feed_url": "https://www.isc2.org/research",
        "year_regex": r"Workforce Study[^\d]*(\d{4})",
    },
    {
        "key": "wef_future_of_jobs",
        "name": "WEF Future of Jobs Report",
        "cache_year": 2025,
        "feed_url": "https://www.weforum.org/reports/the-future-of-jobs-report-2025/",
        "year_regex": r"Future of Jobs[^\d]*(\d{4})",
    },
)


def _detect_upstream_year(feed_url: str, year_regex: str) -> int | None:
    raw = http_get(feed_url, timeout=20.0)
    if raw is None:
        return None
    match = re.search(year_regex, raw, re.IGNORECASE)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def collect() -> int:
    now = _dt.datetime.now(_dt.timezone.utc).isoformat()
    statuses: list[dict] = []
    for src in SOURCES:
        upstream = _detect_upstream_year(src["feed_url"], src["year_regex"])
        is_stale = upstream is not None and upstream > src["cache_year"]
        statuses.append({
            "key": src["key"],
            "name": src["name"],
            "cache_year": src["cache_year"],
            "upstream_year_detected": upstream,
            "newer_release_available": is_stale,
            "feed_url": src["feed_url"],
            "checked_at": now,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"sources": statuses, "generated_at": now}, indent=2))
    return len(statuses)


if __name__ == "__main__":
    n = collect()
    print(f"annual_snapshots: checked {n} sources, wrote {OUT}")
