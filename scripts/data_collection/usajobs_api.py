"""USAJobs.gov Search API crawler.

US Federal Government's public job-search API. Free to use after one-time
free registration at developer.usajobs.gov which gives an Authorization-Key.

Required environment variables (set in /opt/aiproof/.env on prod):
    USAJOBS_API_KEY   — the Authorization-Key from developer.usajobs.gov
    USAJOBS_EMAIL     — contact email included in the User-Agent (optional;
                         defaults to contact@fastinfer.org)

We crawl across a curated set of keyword queries that cover the tech roles
in our roster (software, data, security, AI, cloud, devops).

Output: data/raw/usajobs_postings.csv
"""
from __future__ import annotations

import csv
import json
import os
import re
import urllib.parse
import urllib.request

from _common import RAW

OUT = RAW / "usajobs_postings.csv"
DEFAULT_EMAIL = "contact@fastinfer.org"
KEYWORDS: tuple[str, ...] = (
    "software engineer",
    "data scientist",
    "cybersecurity",
    "artificial intelligence",
    "cloud engineer",
    "devops",
    "machine learning",
    "information security",
    "data engineer",
    "site reliability",
)

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops|machine learning|artificial intelligence)\b",
    re.IGNORECASE,
)


def _fetch(keyword: str, page: int, api_key: str, email: str) -> list[dict]:
    qs = urllib.parse.urlencode({
        "Keyword": keyword,
        "Page": page,
        "ResultsPerPage": 100,
    })
    url = f"https://data.usajobs.gov/api/Search?{qs}"
    req = urllib.request.Request(url, headers={
        "User-Agent": f"aiproof-research ({email})",
        "Host": "data.usajobs.gov",
        "Authorization-Key": api_key,
    })
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:  # noqa: BLE001
        return []
    return data.get("SearchResult", {}).get("SearchResultItems", []) or []


def collect() -> int:
    api_key = os.environ.get("USAJOBS_API_KEY", "").strip()
    if not api_key:
        # Honest, non-fabricating fallback: leave existing cache untouched.
        print("usajobs_api: USAJOBS_API_KEY not set — skipping (set it in .env to enable).")
        return 0
    email = os.environ.get("USAJOBS_EMAIL", DEFAULT_EMAIL).strip() or DEFAULT_EMAIL

    seen: set[str] = set()
    rows: list[dict] = []
    for kw in KEYWORDS:
        for page in range(1, 4):  # cap at 3 pages = 300 results per keyword
            items = _fetch(kw, page, api_key, email)
            if not items:
                break
            for it in items:
                d = it.get("MatchedObjectDescriptor", {}) or {}
                pid = d.get("PositionID") or ""
                if pid in seen:
                    continue
                seen.add(pid)
                title = d.get("PositionTitle", "") or ""
                locs = d.get("PositionLocationDisplay", "") or ""
                org = d.get("OrganizationName", "") or ""
                qualifications = (d.get("QualificationSummary") or "")[:600]
                rows.append({
                    "posting_id": pid,
                    "title": title[:200],
                    "organization": org[:120],
                    "location": locs[:200],
                    "department": (d.get("DepartmentName") or "")[:120],
                    "publication_date": (d.get("PublicationStartDate") or "")[:25],
                    "close_date": (d.get("ApplicationCloseDate") or "")[:25],
                    "mentions_ai": int(bool(AI_PATTERN.search(title + " " + qualifications))),
                    "url": d.get("PositionURI", "")[:280],
                    "keyword": kw,
                })
            if len(items) < 100:
                break

    if not rows:
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["posting_id", "title", "organization", "location", "department",
                        "publication_date", "close_date", "mentions_ai", "url", "keyword"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"usajobs_api: wrote {n} postings to {OUT}")
