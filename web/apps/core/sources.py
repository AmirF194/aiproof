"""Registry of every data source the aiproof ranking is built on.

Each entry is what's needed to cite it: a name, URL, the kind of access
(public API / public scrape / paid / manual), the licence/terms summary,
what it feeds in the pipeline, and the date of last refresh.

Kept as a hand-curated list rather than a model — sources change once or
twice a year, and reviewing diffs in version control is the audit trail.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    key: str
    name: str
    url: str
    access: str   # api | public_scrape | annual_report | manual | paid_excerpt
    licence: str
    feeds: tuple[str, ...]
    last_fetched: str  # ISO date or "rolling"
    notes: str = ""


SOURCES: tuple[Source, ...] = (
    Source(
        key="bls_oep",
        name="U.S. Bureau of Labor Statistics — Occupational Employment Projections (2024–2034)",
        url="https://www.bls.gov/emp/tables.htm",
        access="api",
        licence="Public domain (US federal work)",
        feeds=("demand", "salary baseline"),
        last_fetched="rolling",
        notes="Free public API; SOC-code projections for every tech occupation we map roles into.",
    ),
    Source(
        key="onet",
        name="O*NET — Occupational Information Network",
        url="https://www.onetonline.org/",
        access="api",
        licence="CC BY 4.0 (US Department of Labor)",
        feeds=("skill depth", "task automation"),
        last_fetched="rolling",
        notes="Skill, task, and ability ratings per SOC code; primary input to the skill_depth axis.",
    ),
    Source(
        key="hn_who_is_hiring",
        name="Hacker News — Who's Hiring (Algolia search API)",
        url="https://hn.algolia.com/api",
        access="api",
        licence="Public, no key required",
        feeds=("demand trend", "AI mention rate", "role-name signal"),
        last_fetched="rolling",
        notes="Monthly 'Ask HN: Who is hiring?' threads — high-signal engineering-job corpus.",
    ),
    Source(
        key="greenhouse_ats",
        name="Greenhouse public job-board JSON",
        url="https://developers.greenhouse.io/job-board.html",
        access="api",
        licence="Public per company",
        feeds=("posting volume", "salary mention", "remote split"),
        last_fetched="rolling",
        notes="No-auth endpoint at /v1/boards/{company}/jobs; pulls from hundreds of companies.",
    ),
    Source(
        key="lever_ats",
        name="Lever public postings API",
        url="https://github.com/lever/postings-api",
        access="api",
        licence="Public per company",
        feeds=("posting volume", "salary mention"),
        last_fetched="rolling",
        notes="No-auth endpoint at /v0/postings/{company}; complements Greenhouse coverage.",
    ),
    Source(
        key="so_survey",
        name="Stack Overflow Developer Survey",
        url="https://survey.stackoverflow.co/",
        access="annual_report",
        licence="ODbL (data) / CC BY 4.0 (text)",
        feeds=("compensation", "tooling adoption", "AI-tool use"),
        last_fetched="2025-07",
        notes="Annual CSV release; we ingest the raw responses and aggregate per role.",
    ),
    Source(
        key="github_octoverse",
        name="GitHub Octoverse",
        url="https://octoverse.github.com/",
        access="annual_report",
        licence="GitHub — fair-use citation",
        feeds=("language trend", "AI-tool adoption"),
        last_fetched="2025-10",
        notes="Annual published numbers on language usage, Copilot adoption, repo growth.",
    ),
    Source(
        key="bls_oews",
        name="BLS OEWS — Occupational Employment & Wage Statistics",
        url="https://www.bls.gov/oes/",
        access="api",
        licence="Public domain (US federal work)",
        feeds=("salary band", "headcount"),
        last_fetched="rolling",
        notes="Wage percentiles by SOC; anchors the salary_range field for every role.",
    ),
    Source(
        key="isc2_workforce",
        name="ISC2 Cybersecurity Workforce Study",
        url="https://www.isc2.org/research",
        access="annual_report",
        licence="ISC2 — fair-use citation",
        feeds=("security demand", "skills gap"),
        last_fetched="2025-12",
        notes="Annual published top-line numbers; gated PDF for the detailed tables.",
    ),
    Source(
        key="layoffs_fyi",
        name="layoffs.fyi tech-layoff tracker",
        url="https://layoffs.fyi/",
        access="public_scrape",
        licence="Site-published, attribution",
        feeds=("trend direction", "category risk"),
        last_fetched="2026-04",
        notes="Aggregated layoff events by company and role family; client-side rendered so we cache snapshots.",
    ),
    Source(
        key="levels_fyi",
        name="Levels.fyi compensation snapshots",
        url="https://www.levels.fyi/",
        access="manual",
        licence="Site-published, attribution",
        feeds=("senior IC compensation"),
        last_fetched="2026-02",
        notes="No public API; we maintain a manual snapshot of headline bands for senior+ ICs.",
    ),
    Source(
        key="gartner_press",
        name="Gartner press-release forecasts (platform eng, AI agents, code-assist)",
        url="https://www.gartner.com/en/newsroom",
        access="paid_excerpt",
        licence="Gartner — public press content under fair-use",
        feeds=("category trend", "strategic importance"),
        last_fetched="2025-11",
        notes="Detailed reports are paid; we cite only the public headline numbers.",
    ),
)


def get_source(key: str) -> Source | None:
    return next((s for s in SOURCES if s.key == key), None)
