"""Hacker News 'Ask HN: Who is hiring?' crawler via the public Algolia API.

Algolia exposes a free, no-auth search endpoint at https://hn.algolia.com/api/v1/.
We pull the monthly 'Who is hiring?' threads (whoishiring user) and aggregate
top-level comments — each is a single job posting — into a dated CSV.

Output: data/raw/hn_who_is_hiring.csv
Columns: month, posting_id, snippet, has_remote, mentions_ai

This is real, live data: no simulation. Falls back gracefully if offline.
"""
from __future__ import annotations

import csv
import datetime as _dt
import json
import re

from _common import RAW, http_get

OUT = RAW / "hn_who_is_hiring.csv"
ALGOLIA = "https://hn.algolia.com/api/v1"

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops)\b",
    re.IGNORECASE,
)
REMOTE_PATTERN = re.compile(r"\b(remote|wfh|work from home)\b", re.IGNORECASE)
HTML_TAG = re.compile(r"<[^>]+>")


def _thread_ids(limit: int = 12) -> list[tuple[str, int]]:
    """Return [(YYYY-MM, story_id)] for the most recent `limit` whoishiring threads."""
    url = (
        f"{ALGOLIA}/search_by_date?"
        f"tags=story,author_whoishiring&query=who%20is%20hiring&hitsPerPage={limit}"
    )
    raw = http_get(url, timeout=15.0)
    if raw is None:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    out: list[tuple[str, int]] = []
    for hit in data.get("hits", []):
        title = hit.get("title", "") or ""
        if "who is hiring" not in title.lower():
            continue
        created = hit.get("created_at", "")
        try:
            month = _dt.datetime.fromisoformat(created.replace("Z", "+00:00")).strftime("%Y-%m")
        except ValueError:
            continue
        out.append((month, hit["objectID"]))
    return out


def _thread_comments(story_id: int) -> list[dict]:
    """Top-level comments on a HN story via Algolia."""
    url = (
        f"{ALGOLIA}/search?tags=comment,story_{story_id}"
        f"&hitsPerPage=1000"
    )
    raw = http_get(url, timeout=20.0)
    if raw is None:
        return []
    try:
        return json.loads(raw).get("hits", [])
    except json.JSONDecodeError:
        return []


def collect() -> int:
    rows: list[dict] = []
    for month, sid in _thread_ids(limit=12):
        for c in _thread_comments(sid):
            text = HTML_TAG.sub(" ", c.get("comment_text") or "")
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) < 60:  # skip noise
                continue
            rows.append({
                "month": month,
                "posting_id": c.get("objectID", ""),
                "snippet": text[:240],
                "has_remote": int(bool(REMOTE_PATTERN.search(text))),
                "mentions_ai": int(bool(AI_PATTERN.search(text))),
            })

    if not rows:
        return 0  # offline — leave existing cache intact

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["month", "posting_id", "snippet", "has_remote", "mentions_ai"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n = collect()
    print(f"hn_who_is_hiring: wrote {n} postings to {OUT}")
