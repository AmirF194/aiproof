"""The Muse public job-search API crawler.

Endpoint: https://www.themuse.com/api/public/jobs — no auth.
We paginate across software/data/AI categories, capturing every active
posting with location and a snippet for keyword matching downstream.

Output: data/raw/themuse_postings.csv
"""
from __future__ import annotations

import csv
import json
import re

from _common import RAW, http_get

OUT = RAW / "themuse_postings.csv"
ENDPOINT = "https://www.themuse.com/api/public/jobs"

CATEGORIES = (
    "Software Engineering",
    "Software Engineer",
    "Data Science",
    "Data and Analytics",
    "Engineering",
    "IT",
    "Product",
    "Design and UX",
    "Project Management",
    "Account Management",
)

HTML_TAG = re.compile(r"<[^>]+>")
AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops)\b",
    re.IGNORECASE,
)


def _fetch_page(category: str, page: int) -> list[dict]:
    url = f"{ENDPOINT}?category={category.replace(' ', '%20')}&page={page}"
    raw = http_get(url, timeout=15.0)
    if raw is None:
        return []
    try:
        return json.loads(raw).get("results", [])
    except json.JSONDecodeError:
        return []


def collect() -> int:
    seen: set[str] = set()
    rows: list[dict] = []
    for cat in CATEGORIES:
        for page in range(1, 6):  # ~100 jobs per category
            results = _fetch_page(cat, page)
            if not results:
                break
            for j in results:
                jid = str(j.get("id", ""))
                if jid in seen:
                    continue
                seen.add(jid)
                contents = HTML_TAG.sub(" ", j.get("contents") or "")[:600]
                locations = ", ".join(loc.get("name", "") for loc in (j.get("locations") or []))
                rows.append({
                    "posting_id": jid,
                    "title": (j.get("name") or "")[:200],
                    "company": (j.get("company") or {}).get("name", "")[:120],
                    "location": locations[:200],
                    "category": cat,
                    "remote": int("remote" in (locations or "").lower()),
                    "mentions_ai": int(bool(AI_PATTERN.search(j.get("name", "") + " " + contents))),
                    "url": (j.get("refs") or {}).get("landing_page", ""),
                })

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["posting_id", "title", "company", "location", "category", "remote", "mentions_ai", "url"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"themuse_api: wrote {n} postings to {OUT}")
