"""WeWorkRemotely RSS crawler.

WeWorkRemotely publishes per-category RSS feeds that are public, no-auth,
and include the full job description in CDATA blocks.

Endpoints:
  https://weworkremotely.com/categories/remote-programming-jobs.rss
  https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss
  https://weworkremotely.com/categories/remote-design-jobs.rss
  ...

Output: data/raw/weworkremotely_postings.csv
"""
from __future__ import annotations

import csv
import re
from xml.etree import ElementTree as ET

from _common import RAW, http_get

OUT = RAW / "weworkremotely_postings.csv"

CATEGORIES: tuple[str, ...] = (
    "remote-programming-jobs",
    "remote-devops-sysadmin-jobs",
    "remote-design-jobs",
    "remote-product-jobs",
    "remote-back-end-programming-jobs",
    "remote-front-end-programming-jobs",
    "remote-full-stack-programming-jobs",
    "remote-marketing-jobs",
    "remote-customer-support-jobs",
    "remote-management-and-finance-jobs",
)

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops|machine learning|artificial intelligence)\b",
    re.IGNORECASE,
)
HTML_TAG = re.compile(r"<[^>]+>")


def _fetch_category(slug: str) -> list[dict]:
    url = f"https://weworkremotely.com/categories/{slug}.rss"
    raw = http_get(url, timeout=20.0)
    if raw is None:
        return []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []
    items: list[dict] = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        # "Company: Title" or "Headline | Company"; we keep raw and split downstream.
        link = (item.findtext("link") or "").strip()
        pubdate = (item.findtext("pubDate") or "").strip()
        desc_raw = (item.findtext("description") or "")
        desc = HTML_TAG.sub(" ", desc_raw)
        desc = re.sub(r"\s+", " ", desc).strip()
        items.append({
            "category": slug,
            "title": title[:240],
            "publication_date": pubdate[:31],
            "snippet": desc[:400],
            "mentions_ai": int(bool(AI_PATTERN.search(title + " " + desc))),
            "url": link[:280],
        })
    return items


def collect() -> int:
    seen: set[str] = set()
    rows: list[dict] = []
    for cat in CATEGORIES:
        for item in _fetch_category(cat):
            if item["url"] in seen:
                continue
            seen.add(item["url"])
            rows.append(item)

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["category", "title", "publication_date", "snippet", "mentions_ai", "url"],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"weworkremotely_rss: wrote {n} postings to {OUT}")
