"""SmartRecruiters public postings crawler.

SmartRecruiters exposes a no-auth JSON endpoint per company:
    https://api.smartrecruiters.com/v1/companies/{id}/postings

Paginated; default page size 10, max 100. Coverage skews enterprise —
Bosch, Visa, NielsenIQ already deliver thousands of postings.

Output: data/raw/smartrecruiters_postings.csv
"""
from __future__ import annotations

import csv
import json
import re

from _common import RAW, http_get

OUT = RAW / "smartrecruiters_postings.csv"

# Companies confirmed live via probe — extend by checking jobs.smartrecruiters.com/{Slug}.
COMPANIES: tuple[str, ...] = (
    "BoschGroup",          # 4,500+ postings — global enterprise
    "Visa",
    "NielsenIQ",
)

PAGE_SIZE = 100
MAX_PAGES_PER_COMPANY = 50    # 50 * 100 = 5,000 row cap per company

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops)\b",
    re.IGNORECASE,
)


def _fetch_page(slug: str, offset: int) -> dict:
    url = (
        f"https://api.smartrecruiters.com/v1/companies/{slug}/postings"
        f"?offset={offset}&limit={PAGE_SIZE}"
    )
    raw = http_get(url, timeout=20.0)
    if raw is None:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def collect() -> int:
    rows: list[dict] = []
    for slug in COMPANIES:
        offset = 0
        for _ in range(MAX_PAGES_PER_COMPANY):
            page = _fetch_page(slug, offset)
            items = page.get("content", [])
            if not items:
                break
            for j in items:
                loc = j.get("location", {}) or {}
                department = (j.get("department") or {}).get("label") or ""
                industry = (j.get("industry") or {}).get("label") or ""
                title = j.get("name", "") or ""
                rows.append({
                    "company": slug,
                    "posting_id": j.get("id", ""),
                    "title": title[:200],
                    "department": department[:120],
                    "industry": industry[:120],
                    "city": (loc.get("city") or "")[:80],
                    "country": (loc.get("country") or "")[:40],
                    "remote": int(bool(loc.get("remote", False))),
                    "mentions_ai": int(bool(AI_PATTERN.search(title))),
                    "release_date": (j.get("releasedDate") or "")[:25],
                    "url": j.get("ref", ""),
                })
            offset += PAGE_SIZE
            if offset >= page.get("totalFound", 0):
                break

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "company", "posting_id", "title", "department", "industry",
                "city", "country", "remote", "mentions_ai", "release_date", "url",
            ],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"smartrecruiters_ats: wrote {n} postings to {OUT}")
