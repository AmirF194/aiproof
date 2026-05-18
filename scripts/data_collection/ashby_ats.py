"""Ashby public job-board crawler.

Ashby exposes a no-auth JSON endpoint per company:
    https://api.ashbyhq.com/posting-api/job-board/{slug}

Strong AI / devtools company coverage — OpenAI, Anthropic, Cohere,
Mistral, ElevenLabs, Runway, etc.

Output: data/raw/ashby_postings.csv
"""
from __future__ import annotations

import csv
import json
import re

from _common import RAW, http_get

OUT = RAW / "ashby_postings.csv"

# Companies confirmed live via probe — extend by checking jobs.ashbyhq.com/{slug}.
COMPANIES: tuple[str, ...] = (
    # AI / ML labs
    "openai", "cohere", "mistral", "anthropic", "elevenlabs",
    "runway-ml", "factory", "cognition", "gradient",
    # Developer tools
    "ramp", "deel", "notion", "posthog", "supabase", "replit",
    "warp", "mux", "cribl", "plaid", "vanta",
)

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops)\b",
    re.IGNORECASE,
)
REMOTE_PATTERN = re.compile(r"\b(remote|distributed|anywhere|wfh)\b", re.IGNORECASE)


def _fetch_board(slug: str) -> list[dict]:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    raw = http_get(url, timeout=15.0)
    if raw is None:
        return []
    try:
        return json.loads(raw).get("jobs", [])
    except json.JSONDecodeError:
        return []


def collect() -> int:
    rows: list[dict] = []
    for slug in COMPANIES:
        for j in _fetch_board(slug):
            loc = j.get("locationName") or ""
            title = j.get("title") or ""
            text = title + " " + (j.get("descriptionPlain") or "")[:600]
            rows.append({
                "company": slug,
                "posting_id": j.get("id", ""),
                "title": title[:200],
                "department": (j.get("departmentName") or "")[:120],
                "team": (j.get("teamName") or "")[:120],
                "location": loc[:120],
                "remote": int(bool(REMOTE_PATTERN.search(loc) or j.get("isRemote"))),
                "mentions_ai": int(bool(AI_PATTERN.search(text))),
                "employment_type": (j.get("employmentType") or "")[:40],
                "updated_at": j.get("updatedAt", ""),
                "url": j.get("jobUrl", ""),
            })

    if not rows:
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "company", "posting_id", "title", "department", "team",
                "location", "remote", "mentions_ai", "employment_type",
                "updated_at", "url",
            ],
        )
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"ashby_ats: wrote {n} postings to {OUT}")
