"""Remotive public remote-jobs API crawler.

Endpoint: https://remotive.com/api/remote-jobs — no auth, returns all
active remote postings across software, data, design, devops.

Output: data/raw/remotive_postings.csv
"""
from __future__ import annotations

import csv
import json
import re

from _common import RAW, http_get

OUT = RAW / "remotive_postings.csv"
ENDPOINT = "https://remotive.com/api/remote-jobs"

CATEGORIES = (
    "software-dev",
    "data",
    "devops",
    "design",
    "product",
    "qa",
    "all-others",
)

HTML_TAG = re.compile(r"<[^>]+>")
AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops)\b",
    re.IGNORECASE,
)


def _fetch_category(slug: str) -> list[dict]:
    raw = http_get(f"{ENDPOINT}?category={slug}", timeout=15.0)
    if raw is None:
        return []
    try:
        return json.loads(raw).get("jobs", [])
    except json.JSONDecodeError:
        return []


def collect() -> int:
    seen: set[str] = set()
    rows: list[dict] = []
    for slug in CATEGORIES:
        for j in _fetch_category(slug):
            jid = str(j.get("id", ""))
            if jid in seen:
                continue
            seen.add(jid)
            desc = HTML_TAG.sub(" ", j.get("description") or "")[:800]
            rows.append({
                "posting_id": jid,
                "title": (j.get("title") or "")[:200],
                "company": (j.get("company_name") or "")[:120],
                "location": (j.get("candidate_required_location") or "")[:120],
                "category": slug,
                "salary": (j.get("salary") or "")[:80],
                "publication_date": (j.get("publication_date") or "")[:25],
                "mentions_ai": int(bool(AI_PATTERN.search(j.get("title", "") + " " + desc))),
                "url": j.get("url", ""),
            })

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["posting_id", "title", "company", "location", "category", "salary", "publication_date", "mentions_ai", "url"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"remotive_api: wrote {n} postings to {OUT}")
