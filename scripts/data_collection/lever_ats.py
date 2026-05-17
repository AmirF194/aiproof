"""Lever public postings crawler.

Lever exposes a no-auth JSON endpoint per company:
    https://api.lever.co/v0/postings/{company}

Complements the Greenhouse crawler — many companies use Lever for ATS.

Output: data/raw/lever_postings.csv
Columns: company, posting_id, title, location, team, commitment, updated_at, url
"""
from __future__ import annotations

import csv
import json

from _common import RAW, http_get

OUT = RAW / "lever_postings.csv"

# Public Lever boards — probed live and confirmed serving postings.
# Add slugs by visiting https://jobs.lever.co/{slug} in a browser.
COMPANIES: tuple[str, ...] = (
    "spotify", "palantir", "mistral", "contentsquare",
    "metabase", "prismic", "jumpcloud", "everbridge",
)


def _fetch_board(slug: str) -> list[dict]:
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    raw = http_get(url, timeout=15.0)
    if raw is None:
        return []
    try:
        data = json.loads(raw)
        # Lever returns a list at top level
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def collect() -> int:
    rows: list[dict] = []
    for slug in COMPANIES:
        for j in _fetch_board(slug):
            cats = j.get("categories") or {}
            rows.append({
                "company": slug,
                "posting_id": j.get("id", ""),
                "title": (j.get("text") or "")[:200],
                "location": (cats.get("location") or "")[:120],
                "team": (cats.get("team") or "")[:120],
                "commitment": (cats.get("commitment") or "")[:60],
                "updated_at": j.get("createdAt", ""),
                "url": j.get("hostedUrl", ""),
            })

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["company", "posting_id", "title", "location", "team", "commitment", "updated_at", "url"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"lever_ats: wrote {n} postings to {OUT}")
