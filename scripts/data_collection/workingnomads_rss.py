"""Working Nomads public job-feed crawler.

Working Nomads aggregates remote postings. They expose a public JSON
endpoint at /api/exposed_jobs/ — no auth required, returns the current
listing snapshot with company, category, tags, location, pub_date.

(The older /jobsrss RSS URL referenced on their site is dead — Working
Nomads moved their public feed to JSON. We use the JSON.)

Output: data/raw/workingnomads_postings.csv
"""
from __future__ import annotations

import csv
import json
import re

from _common import RAW, http_get

OUT = RAW / "workingnomads_postings.csv"
URL = "https://www.workingnomads.com/api/exposed_jobs/"

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops|machine learning|artificial intelligence)\b",
    re.IGNORECASE,
)
HTML_TAG = re.compile(r"<[^>]+>")


def collect() -> int:
    raw = http_get(URL, timeout=30.0)
    if raw is None:
        return 0
    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    if not isinstance(items, list):
        return 0

    rows: list[dict] = []
    for j in items:
        title = j.get("title", "") or ""
        desc = HTML_TAG.sub(" ", j.get("description", "") or "")
        desc = re.sub(r"\s+", " ", desc).strip()
        tags = j.get("tags") or []
        rows.append({
            "title": title[:240],
            "company": (j.get("company_name") or "")[:120],
            "category": (j.get("category_name") or "")[:80],
            "tags": "|".join(tags) if isinstance(tags, list) else str(tags)[:200],
            "location": (j.get("location") or "")[:120],
            "publication_date": (j.get("pub_date") or "")[:31],
            "snippet": desc[:400],
            "mentions_ai": int(bool(AI_PATTERN.search(title + " " + desc))),
            "url": (j.get("url") or "")[:280],
        })

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["title", "company", "category", "tags", "location", "publication_date", "snippet", "mentions_ai", "url"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"workingnomads_rss: wrote {n} postings to {OUT}")
