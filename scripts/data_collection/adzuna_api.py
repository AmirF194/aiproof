"""Adzuna API crawler.

Adzuna aggregates job postings from Indeed, Reed, CV-Library, and others
across 16 countries. Free tier: 250 calls/day after free registration at
developer.adzuna.com.

Required environment variables (set in /opt/aiproof/.env on prod):
    ADZUNA_APP_ID    — application ID
    ADZUNA_API_KEY   — paired API key

We sweep multiple countries and a curated set of tech keywords. Pagination
is bounded so we stay well inside the 250-call daily quota.

Output: data/raw/adzuna_postings.csv
"""
from __future__ import annotations

import csv
import json
import os
import re
import urllib.parse

from _common import RAW, http_get

OUT = RAW / "adzuna_postings.csv"

# 16-country coverage. Two-letter ISO. UK is "gb".
COUNTRIES: tuple[str, ...] = (
    "us", "gb", "ca", "au", "de", "fr", "nl", "in",
    "pl", "it", "es", "ru", "za", "mx", "br", "sg",
)
KEYWORDS: tuple[str, ...] = (
    "software engineer",
    "data scientist",
    "machine learning",
    "cybersecurity",
    "devops engineer",
    "cloud engineer",
)
PAGES_PER_KEYWORD = 2          # 50 results × 2 pages × 6 keywords × 16 countries
                               # = 192 calls (per crawl), well under 250/day cap
RESULTS_PER_PAGE = 50

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops|machine learning|artificial intelligence)\b",
    re.IGNORECASE,
)


def _fetch(country: str, keyword: str, page: int, app_id: str, app_key: str) -> list[dict]:
    qs = urllib.parse.urlencode({
        "app_id": app_id,
        "app_key": app_key,
        "what": keyword,
        "results_per_page": RESULTS_PER_PAGE,
        "content-type": "application/json",
    })
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}?{qs}"
    raw = http_get(url, timeout=20.0)
    if raw is None:
        return []
    try:
        return json.loads(raw).get("results", [])
    except json.JSONDecodeError:
        return []


def collect() -> int:
    app_id = os.environ.get("ADZUNA_APP_ID", "").strip()
    app_key = os.environ.get("ADZUNA_API_KEY", "").strip()
    if not (app_id and app_key):
        print("adzuna_api: ADZUNA_APP_ID / ADZUNA_API_KEY not set — skipping.")
        return 0

    seen: set[str] = set()
    rows: list[dict] = []
    for country in COUNTRIES:
        for kw in KEYWORDS:
            for page in range(1, PAGES_PER_KEYWORD + 1):
                items = _fetch(country, kw, page, app_id, app_key)
                if not items:
                    break
                for j in items:
                    pid = str(j.get("id", ""))
                    if pid in seen:
                        continue
                    seen.add(pid)
                    loc = (j.get("location") or {}).get("display_name") or ""
                    cat = (j.get("category") or {}).get("label") or ""
                    title = j.get("title", "") or ""
                    desc = (j.get("description") or "")[:500]
                    rows.append({
                        "posting_id": pid,
                        "country": country,
                        "title": title[:200],
                        "company": (j.get("company") or {}).get("display_name", "")[:120],
                        "location": loc[:200],
                        "category": cat[:80],
                        "salary_min": j.get("salary_min") or "",
                        "salary_max": j.get("salary_max") or "",
                        "publication_date": (j.get("created") or "")[:25],
                        "mentions_ai": int(bool(AI_PATTERN.search(title + " " + desc))),
                        "url": (j.get("redirect_url") or "")[:280],
                        "keyword": kw,
                    })

    if not rows:
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["posting_id", "country", "title", "company", "location",
                        "category", "salary_min", "salary_max", "publication_date",
                        "mentions_ai", "url", "keyword"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"adzuna_api: wrote {n} postings to {OUT}")
