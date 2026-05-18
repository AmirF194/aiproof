"""Canada Job Bank crawler.

Public Government of Canada job-board. There's no documented JSON API, but
their robots.txt explicitly allows crawling with a 5-second delay, so we
parse the public HTML search pages.

We use the `searchstring=` keyword filter — the `fnoc=` NOC-code filter
turned out to ignore most filters when no other keyword is set.

Output: data/raw/canada_jobbank_postings.csv
"""
from __future__ import annotations

import csv
import re
import time
import urllib.parse

from _common import RAW, http_get

OUT = RAW / "canada_jobbank_postings.csv"

KEYWORDS: tuple[str, ...] = (
    "software engineer",
    "software developer",
    "data scientist",
    "machine learning",
    "cybersecurity",
    "information security",
    "cloud engineer",
    "devops",
    "data engineer",
    "site reliability",
    "full stack developer",
    "backend developer",
    "frontend developer",
)

CRAWL_DELAY_SECONDS = 5

# Each result is an <article id="article-NNN"> ... wrapping a <span class="noctitle">TITLE</span>.
_ARTICLE_RE = re.compile(
    r'<article id="article-(\d+)"[^>]*>\s*'
    r'<a href="(/jobsearch/jobposting/\d+[^"]*)"[^>]*class="resultJobItem"',
    re.DOTALL,
)
_TITLE_RE = re.compile(r'<span class="noctitle">\s*(.+?)\s*</span>', re.DOTALL)
_BUSINESS_RE = re.compile(r'<li class="business">\s*(.+?)\s*</li>', re.DOTALL)
_DATE_RE = re.compile(r'<li class="date">\s*(.+?)\s*</li>', re.DOTALL)
_LOCATION_RE = re.compile(
    r'<li class="location">\s*<span[^>]*>\s*</span>\s*<span[^>]*>Location</span>\s*(.+?)\s*</li>',
    re.DOTALL,
)
_HTML_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops|machine learning|artificial intelligence)\b",
    re.IGNORECASE,
)


def _clean(html: str) -> str:
    return _WS.sub(" ", _HTML_TAG.sub(" ", html or "")).strip()


def _parse_page(html: str, keyword: str) -> list[dict]:
    rows: list[dict] = []
    for match in _ARTICLE_RE.finditer(html):
        posting_id, href = match.groups()
        # Each <article>...</article> is sequential, so slice ahead to extract fields.
        end = html.find("</article>", match.end())
        block = html[match.end():end if end > 0 else match.end() + 2500]
        t = _TITLE_RE.search(block)
        b = _BUSINESS_RE.search(block)
        loc = _LOCATION_RE.search(block)
        d = _DATE_RE.search(block)
        title = _clean(t.group(1)) if t else ""
        if not title:
            continue
        rows.append({
            "posting_id": posting_id,
            "keyword": keyword,
            "title": title[:240],
            "employer": _clean(b.group(1)) if b else "",
            "location": _clean(loc.group(1)) if loc else "",
            "publication_date": _clean(d.group(1)) if d else "",
            "mentions_ai": int(bool(AI_PATTERN.search(title))),
            "url": (
                "https://www.jobbank.gc.ca"
                + re.sub(r";jsessionid=[^?&]+", "", href.split("?")[0])
            )[:280],
        })
    return rows


def _fetch_keyword(kw: str) -> list[dict]:
    qs = urllib.parse.urlencode({"searchstring": kw, "sort": "D", "page": 1})
    url = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?{qs}"
    html = http_get(url, timeout=30.0)
    if html is None:
        return []
    return _parse_page(html, kw)


def collect() -> int:
    seen: set[str] = set()
    rows: list[dict] = []
    for i, kw in enumerate(KEYWORDS):
        if i > 0:
            time.sleep(CRAWL_DELAY_SECONDS)
        for r in _fetch_keyword(kw):
            if r["posting_id"] in seen:
                continue
            seen.add(r["posting_id"])
            rows.append(r)

    if not rows:
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["posting_id", "keyword", "title", "employer", "location",
                        "publication_date", "mentions_ai", "url"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"canada_jobbank: wrote {n} postings to {OUT}")
