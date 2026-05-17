"""Greenhouse public job-board crawler.

Greenhouse exposes a no-auth JSON endpoint per company:
    https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true

We iterate over a curated set of companies known to host their careers
page on Greenhouse, pull every active posting, and produce a normalised
CSV. This is real production data, refreshed on every run.

Output: data/raw/greenhouse_postings.csv
Columns: company, posting_id, title, location, remote, updated_at, url
"""
from __future__ import annotations

import csv
import json
import re

from _common import RAW, http_get

OUT = RAW / "greenhouse_postings.csv"

# Public Greenhouse boards across SaaS, infra, AI, fintech, and devtools.
# Easy to extend — every entry maps to https://boards.greenhouse.io/{slug}.
COMPANIES: tuple[str, ...] = (
    "airbnb", "stripe", "anthropic", "databricks", "snowflake", "coinbase",
    "discord", "doordash", "instacart", "robinhood", "figma", "asana",
    "twilio", "datadog", "elastic", "hashicorp", "gitlab", "vercel",
    "supabase", "neon", "modal", "weightsandbiases", "scale", "huggingface",
    "togetherai", "perplexity", "mistralai", "cohere", "writer", "groq",
)

REMOTE_PATTERN = re.compile(r"\b(remote|distributed|anywhere)\b", re.IGNORECASE)


def _fetch_board(slug: str) -> list[dict]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    raw = http_get(url, timeout=15.0)
    if raw is None:
        return []
    try:
        return json.loads(raw).get("jobs", [])
    except json.JSONDecodeError:
        return []


def collect() -> int:
    rows: list[dict] = []
    seen_companies = 0
    for slug in COMPANIES:
        jobs = _fetch_board(slug)
        if jobs:
            seen_companies += 1
        for j in jobs:
            loc = (j.get("location") or {}).get("name") or ""
            rows.append({
                "company": slug,
                "posting_id": j.get("id", ""),
                "title": j.get("title", "")[:200],
                "location": loc[:120],
                "remote": int(bool(REMOTE_PATTERN.search(loc))),
                "updated_at": j.get("updated_at", ""),
                "url": j.get("absolute_url", ""),
            })

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["company", "posting_id", "title", "location", "remote", "updated_at", "url"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"greenhouse_ats: wrote {n} postings to {OUT}")
