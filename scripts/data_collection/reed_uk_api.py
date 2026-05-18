"""Reed.co.uk API crawler.

UK-focused job aggregator. Free 1,000 calls/day after registration at
www.reed.co.uk/developers/jobseeker.

Required environment variables (set in /opt/aiproof/.env on prod):
    REED_API_KEY   — API key from Reed developer portal

Output: data/raw/reed_uk_postings.csv
"""
from __future__ import annotations

import base64
import csv
import json
import os
import re
import urllib.parse

from _common import RAW, http_get

OUT = RAW / "reed_uk_postings.csv"

KEYWORDS: tuple[str, ...] = (
    "software engineer",
    "data scientist",
    "machine learning",
    "cybersecurity",
    "devops",
    "cloud engineer",
)
RESULTS_PER_KEYWORD = 100   # Reed cap is 100 per request

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops|machine learning|artificial intelligence)\b",
    re.IGNORECASE,
)


def _fetch(keyword: str, api_key: str) -> list[dict]:
    qs = urllib.parse.urlencode({
        "keywords": keyword,
        "resultsToTake": RESULTS_PER_KEYWORD,
    })
    url = f"https://www.reed.co.uk/api/1.0/search?{qs}"
    # Reed uses HTTP Basic with the key as the username and an empty password.
    auth = base64.b64encode(f"{api_key}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "User-Agent": "aiproof-research (contact@fastinfer.org)",
    }
    raw = http_get(url, timeout=20.0, headers=headers)
    if raw is None:
        return []
    try:
        return json.loads(raw).get("results", [])
    except json.JSONDecodeError:
        return []


def collect() -> int:
    api_key = os.environ.get("REED_API_KEY", "").strip()
    if not api_key:
        print("reed_uk_api: REED_API_KEY not set — skipping.")
        return 0

    seen: set[str] = set()
    rows: list[dict] = []
    for kw in KEYWORDS:
        for j in _fetch(kw, api_key):
            pid = str(j.get("jobId", ""))
            if pid in seen:
                continue
            seen.add(pid)
            title = j.get("jobTitle", "") or ""
            desc = j.get("jobDescription", "") or ""
            rows.append({
                "posting_id": pid,
                "title": title[:200],
                "company": (j.get("employerName") or "")[:120],
                "location": (j.get("locationName") or "")[:120],
                "salary_min": j.get("minimumSalary") or "",
                "salary_max": j.get("maximumSalary") or "",
                "publication_date": (j.get("date") or "")[:25],
                "mentions_ai": int(bool(AI_PATTERN.search(title + " " + desc[:500]))),
                "url": (j.get("jobUrl") or "")[:280],
                "keyword": kw,
            })

    if not rows:
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["posting_id", "title", "company", "location", "salary_min",
                        "salary_max", "publication_date", "mentions_ai", "url", "keyword"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"reed_uk_api: wrote {n} postings to {OUT}")
