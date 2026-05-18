"""Aggregate the 5 live posting feeds into per-role metrics.

Reads:
  data/raw/hn_who_is_hiring.csv
  data/raw/greenhouse_postings.csv
  data/raw/lever_postings.csv
  data/raw/themuse_postings.csv
  data/raw/remotive_postings.csv

Joins against data/roles.csv (the 1000-role roster) by case-insensitive
word-boundary match of the role name against each posting's title (or
HN snippet). Longest role name wins when multiple roles match.

Writes:
  data/processed/role_postings_live.csv
    role_slug, postings_total, postings_recent_30d,
    postings_yoy_pct, ai_mention_pct, remote_pct, sources_n, sample_titles

Stdlib only — no pandas dep.
"""
from __future__ import annotations

import csv
import datetime as _dt
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent.parent
RAW = REPO / "data" / "raw"
PROCESSED = REPO / "data" / "processed"
ROLES_CSV = REPO / "data" / "roles.csv"
OUT = PROCESSED / "role_postings_live.csv"


def read_csv(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[dict], fieldnames: list[str]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)

AI_PATTERN = re.compile(
    r"\b(ai|ml|llm|gpt|claude|gemini|copilot|cursor|rag|agent|fine-?tun|mlops|machine learning|artificial intelligence)\b",
    re.IGNORECASE,
)
REMOTE_PATTERN = re.compile(r"\b(remote|wfh|anywhere|distributed)\b", re.IGNORECASE)

NOW = _dt.datetime.now(_dt.timezone.utc)
RECENT_CUTOFF = NOW - _dt.timedelta(days=30)
YEAR_AGO = NOW - _dt.timedelta(days=365)


def _slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9\s/-]+", "", s.lower())
    s = re.sub(r"\s+", "-", s.strip())
    return s.replace("/", "-")[:220].strip("-")


# Acronym <-> expansion synonyms applied bidirectionally to every role name.
# Each entry is (short, long). When a role name contains `short`, we also
# emit a variant with `long` substituted, and vice-versa. Order matters:
# longer forms first so substitutions are stable.
_SYNONYMS: list[tuple[str, str]] = [
    ("Machine Learning", "ML"),
    ("Artificial Intelligence", "AI"),
    ("Site Reliability Engineer", "SRE"),
    ("Database Administrator", "DBA"),
    ("Product Manager", "PM"),
    ("Technical Program Manager", "TPM"),
    ("Quality Assurance", "QA"),
    ("Information Security", "InfoSec"),
    ("User Experience", "UX"),
    ("User Interface", "UI"),
    ("Natural Language Processing", "NLP"),
    ("Computer Vision", "CV"),
]


_ROLE_NOUN_SWAPS: list[tuple[str, str]] = [
    ("Engineer", "Developer"),
    ("Engineer", "Programmer"),
    ("Developer", "Programmer"),
    ("Front-end", "Frontend"),
    ("Back-end", "Backend"),
]


def _expand_synonyms(name: str) -> list[str]:
    """Return a list of variants of `name` with synonyms applied.

    Two passes:
      1. Acronym/expansion dictionary (ML ↔ Machine Learning etc.) applied in
         both directions.
      2. Common role-noun swaps (Engineer/Developer/Programmer, Front-end/Frontend).

    Avoids stripping seniority prefixes — that risks over-attribution between
    Senior/Mid/Staff variants of the same base role.
    """
    out: set[str] = {name}
    # Pass 1: acronym dictionary
    for long, short in _SYNONYMS:
        long_re = re.compile(rf"\b{re.escape(long)}\b", re.IGNORECASE)
        short_re = re.compile(rf"\b{re.escape(short)}\b", re.IGNORECASE)
        for v in list(out):
            if long_re.search(v):
                out.add(long_re.sub(short, v))
            if short_re.search(v):
                out.add(short_re.sub(long, v))
    # Pass 2: role-noun swaps — applied symmetrically
    for a, b in _ROLE_NOUN_SWAPS:
        a_re = re.compile(rf"\b{re.escape(a)}\b", re.IGNORECASE)
        b_re = re.compile(rf"\b{re.escape(b)}\b", re.IGNORECASE)
        for v in list(out):
            if a_re.search(v):
                out.add(a_re.sub(b, v))
            if b_re.search(v):
                out.add(b_re.sub(a, v))
    return list(out)


def _matcher(role_names: list[str]) -> list[tuple[re.Pattern, str]]:
    """Build word-boundary regexes per role, longest first.

    Each role expands to its canonical name plus any synonym variants
    (e.g. "Senior Machine Learning Engineer" → also "Senior ML Engineer").
    Longest-pattern-wins per posting ensures specific titles outrank generic
    abbreviations. Roles shorter than 10 chars are dropped to avoid spurious
    matches on titles like "Engineer".
    """
    seen: set[str] = set()
    rows: list[tuple[str, str]] = []  # (pattern_string, canonical_role_name)
    for name in role_names:
        clean = name.strip()
        if len(clean) < 10:
            continue
        for variant in _expand_synonyms(clean):
            if len(variant) < 10:
                continue
            key = variant.lower()
            if key in seen:
                continue
            seen.add(key)
            rows.append((variant, clean))

    rows.sort(key=lambda r: -len(r[0]))
    return [(re.compile(rf"\b{re.escape(v)}\b", re.IGNORECASE), canonical) for v, canonical in rows]


def _match_role(text: str, matchers: list[tuple[re.Pattern, str]]) -> str | None:
    if not text:
        return None
    for pat, role_name in matchers:
        if pat.search(text):
            return role_name
    return None


def _parse_dt(value: str) -> _dt.datetime | None:
    if not value:
        return None
    value = value.strip()
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%d/%m/%Y",
    ):
        try:
            return _dt.datetime.strptime(value, fmt).replace(tzinfo=_dt.timezone.utc)
        except ValueError:
            continue
    try:
        parsed = _dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=_dt.timezone.utc)
    return parsed


def _iter_postings():
    """Yield (text, dt_or_none, mentions_ai_or_None, mentions_remote_or_None, source)."""
    hn = RAW / "hn_who_is_hiring.csv"
    if hn.exists():
        for row in read_csv(hn):
            month = row.get("month", "")
            try:
                dt = _dt.datetime.strptime(month + "-01", "%Y-%m-%d").replace(tzinfo=_dt.timezone.utc) if month else None
            except ValueError:
                dt = None
            yield (
                row.get("snippet", ""),
                dt,
                bool(int(row.get("mentions_ai", "0") or 0)),
                bool(int(row.get("has_remote", "0") or 0)),
                "hn",
            )

    gh = RAW / "greenhouse_postings.csv"
    if gh.exists():
        for row in read_csv(gh):
            text = row.get("title", "")
            dt = _parse_dt(row.get("updated_at", ""))
            yield (
                text,
                dt,
                bool(AI_PATTERN.search(text)),
                bool(int(row.get("remote", "0") or 0)) or bool(REMOTE_PATTERN.search(row.get("location", ""))),
                "greenhouse",
            )

    lv = RAW / "lever_postings.csv"
    if lv.exists():
        for row in read_csv(lv):
            text = row.get("title", "")
            yield (
                text,
                None,
                bool(AI_PATTERN.search(text)),
                bool(REMOTE_PATTERN.search(row.get("location", ""))),
                "lever",
            )

    mu = RAW / "themuse_postings.csv"
    if mu.exists():
        for row in read_csv(mu):
            text = row.get("title", "")
            yield (
                text,
                None,
                bool(int(row.get("mentions_ai", "0") or 0)),
                bool(int(row.get("remote", "0") or 0)),
                "themuse",
            )

    rv = RAW / "remotive_postings.csv"
    if rv.exists():
        for row in read_csv(rv):
            text = row.get("title", "")
            dt = _parse_dt(row.get("publication_date", ""))
            yield (
                text,
                dt,
                bool(int(row.get("mentions_ai", "0") or 0)),
                True,  # remotive is all-remote by definition
                "remotive",
            )

    # --- Tier 1 additions ---
    ashby = RAW / "ashby_postings.csv"
    if ashby.exists():
        for row in read_csv(ashby):
            text = row.get("title", "")
            dt = _parse_dt(row.get("updated_at", ""))
            yield (
                text,
                dt,
                bool(int(row.get("mentions_ai", "0") or 0)),
                bool(int(row.get("remote", "0") or 0)),
                "ashby",
            )

    sr = RAW / "smartrecruiters_postings.csv"
    if sr.exists():
        for row in read_csv(sr):
            text = row.get("title", "")
            dt = _parse_dt(row.get("release_date", ""))
            yield (
                text,
                dt,
                bool(int(row.get("mentions_ai", "0") or 0)),
                bool(int(row.get("remote", "0") or 0)),
                "smartrecruiters",
            )

    wwr = RAW / "weworkremotely_postings.csv"
    if wwr.exists():
        for row in read_csv(wwr):
            text = row.get("title", "")
            yield (
                text,
                None,
                bool(int(row.get("mentions_ai", "0") or 0)),
                True,  # WWR is remote-only by definition
                "weworkremotely",
            )

    wn = RAW / "workingnomads_postings.csv"
    if wn.exists():
        for row in read_csv(wn):
            text = row.get("title", "")
            dt = _parse_dt(row.get("publication_date", ""))
            yield (text, dt, bool(int(row.get("mentions_ai", "0") or 0)), True, "workingnomads")

    # --- Tier 4 — Canada Job Bank ---
    cjb = RAW / "canada_jobbank_postings.csv"
    if cjb.exists():
        for row in read_csv(cjb):
            text = row.get("title", "")
            yield (
                text,
                None,
                bool(int(row.get("mentions_ai", "0") or 0)),
                False,
                "canada_jobbank",
            )

    # --- Tier 2 — only produce rows when the key-gated CSVs are present ---
    for path, source in (
        (RAW / "adzuna_postings.csv", "adzuna"),
        (RAW / "usajobs_postings.csv", "usajobs"),
        (RAW / "reed_uk_postings.csv", "reed_uk"),
    ):
        if path.exists():
            for row in read_csv(path):
                text = row.get("title", "")
                dt = _parse_dt(row.get("publication_date", ""))
                yield (
                    text,
                    dt,
                    bool(int(row.get("mentions_ai", "0") or 0)),
                    bool(int(row.get("remote", "0") or 0)),
                    source,
                )


def aggregate() -> int:
    if not ROLES_CSV.exists():
        return 0

    role_rows = read_csv(ROLES_CSV)
    role_names = [r["role"] for r in role_rows]
    matchers = _matcher(role_names)

    counts: dict[str, int] = defaultdict(int)
    recent: dict[str, int] = defaultdict(int)
    past: dict[str, int] = defaultdict(int)
    ai_hits: dict[str, int] = defaultdict(int)
    remote_hits: dict[str, int] = defaultdict(int)
    sources: dict[str, set[str]] = defaultdict(set)
    samples: dict[str, list[str]] = defaultdict(list)

    total_postings = 0
    matched_postings = 0
    for text, dt, has_ai, has_remote, src in _iter_postings():
        total_postings += 1
        role = _match_role(text, matchers)
        if not role:
            continue
        matched_postings += 1
        counts[role] += 1
        sources[role].add(src)
        if has_ai:
            ai_hits[role] += 1
        if has_remote:
            remote_hits[role] += 1
        if dt and dt >= RECENT_CUTOFF:
            recent[role] += 1
        if dt and YEAR_AGO <= dt < (NOW - _dt.timedelta(days=300)):
            past[role] += 1
        if len(samples[role]) < 3 and text:
            samples[role].append(text[:120])

    rows: list[dict] = []
    for r in role_rows:
        name = r["role"]
        n = counts.get(name, 0)
        if n == 0:
            continue
        yoy = None
        if past.get(name, 0) > 0:
            yoy = round(((recent.get(name, 0) + 1) / (past.get(name, 0) + 1) - 1) * 100, 1)
        rows.append({
            "role_slug": _slugify(name),
            "role_name": name,
            "postings_total": n,
            "postings_recent_30d": recent.get(name, 0),
            "postings_yoy_pct": yoy if yoy is not None else "",
            "ai_mention_pct": round(ai_hits.get(name, 0) / n * 100, 1),
            "remote_pct": round(remote_hits.get(name, 0) / n * 100, 1),
            "sources_n": len(sources[name]),
            "sample_titles": " | ".join(samples[name]),
        })

    rows.sort(key=lambda r: -r["postings_total"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUT,
        rows,
        fieldnames=[
            "role_slug", "role_name", "postings_total", "postings_recent_30d",
            "postings_yoy_pct", "ai_mention_pct", "remote_pct",
            "sources_n", "sample_titles",
        ],
    )
    return len(rows)


def collect() -> int:
    """Pipeline-compatible entry point matching the data_collection signature."""
    return aggregate()


if __name__ == "__main__":
    n = aggregate()
    print(f"aggregate_live_postings: {n} roles with live postings → {OUT}")
