"""Registry of every data source the aiproof ranking is built on.

Each entry is what's needed to cite it: a name, URL, the kind of access
(public API / public scrape / annual report / manual snapshot / paid),
the licence/terms summary, what it feeds in the pipeline, and the date
of last refresh.

Honesty rules for this file (binding):
  - `access="api"` only if a live crawler exists in scripts/data_collection/
    AND that crawler is wired into apps.core.management.commands.refresh_postings.
  - `last_fetched="rolling"` only on entries with a live weekly Celery beat
    refresh. Everything else uses an ISO date matching the snapshot.
  - No entry without a corresponding script or cached file on disk.
  - No simulated data appears on /sources/ (LinkedIn / Indeed / Glassdoor
    simulations stay in scripts/data_collection/*_simulated.py for the
    legacy static pipeline; they are NOT cited on the public site).

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
    # ---------- LIVE crawlers (Celery beat, weekly) ----------
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
        notes="No-auth endpoint at /v1/boards/{company}/jobs; we currently pull ~30 companies.",
    ),
    Source(
        key="lever_ats",
        name="Lever public postings API",
        url="https://github.com/lever/postings-api",
        access="api",
        licence="Public per company",
        feeds=("posting volume", "salary mention"),
        last_fetched="rolling",
        notes="No-auth endpoint at /v0/postings/{company}; ~8 companies confirmed live.",
    ),
    Source(
        key="themuse_api",
        name="The Muse public jobs API",
        url="https://www.themuse.com/developers/api/v2",
        access="api",
        licence="Public, no key required",
        feeds=("posting volume", "AI mention rate", "remote split"),
        last_fetched="rolling",
        notes="No-auth endpoint at /api/public/jobs; paginated by category.",
    ),
    Source(
        key="remotive_api",
        name="Remotive remote-jobs API",
        url="https://remotive.com/api/remote-jobs",
        access="api",
        licence="Public, no key required",
        feeds=("posting volume", "AI mention rate"),
        last_fetched="rolling",
        notes="No-auth endpoint listing every active remote posting on Remotive.",
    ),
    Source(
        key="ashby_ats",
        name="Ashby public job-board API",
        url="https://developers.ashbyhq.com/reference/get_posting-api-job-board-job-board-name",
        access="api",
        licence="Public per company",
        feeds=("posting volume", "AI mention rate"),
        last_fetched="rolling",
        notes="No-auth endpoint at /posting-api/job-board/{company}; AI-lab heavy (OpenAI, Cohere, Anthropic, Mistral, ElevenLabs).",
    ),
    Source(
        key="smartrecruiters_ats",
        name="SmartRecruiters public postings API",
        url="https://developers.smartrecruiters.com/docs/get-list-of-postings",
        access="api",
        licence="Public per company",
        feeds=("posting volume", "AI mention rate", "global coverage"),
        last_fetched="rolling",
        notes="No-auth endpoint at /v1/companies/{slug}/postings; enterprise-heavy (Bosch, Visa, NielsenIQ); 5k+ postings per run.",
    ),
    Source(
        key="weworkremotely_rss",
        name="WeWorkRemotely category RSS feeds",
        url="https://weworkremotely.com/",
        access="api",
        licence="Public RSS, attribution",
        feeds=("remote posting volume", "AI mention rate"),
        last_fetched="rolling",
        notes="Public RSS per category — programming, devops, design, product, full-stack, back-end, front-end.",
    ),
    Source(
        key="workingnomads_api",
        name="Working Nomads public jobs API",
        url="https://www.workingnomads.com/",
        access="api",
        licence="Public, attribution",
        feeds=("remote posting volume",),
        last_fetched="rolling",
        notes="Public JSON endpoint at /api/exposed_jobs/ listing the current remote-jobs snapshot.",
    ),
    Source(
        key="canada_jobbank",
        name="Government of Canada — Job Bank",
        url="https://www.jobbank.gc.ca/",
        access="public_scrape",
        licence="Open Government Licence — Canada",
        feeds=("Canadian posting volume", "geographic coverage"),
        last_fetched="rolling",
        notes="Public HTML pages; robots.txt explicitly allows crawling with a 5-second delay which we honour. Covers Canada's full labour market.",
    ),
    Source(
        key="bls_oews_api",
        name="BLS OEWS — live Public Data API",
        url="https://www.bls.gov/developers/",
        access="api",
        licence="Public domain (US federal work)",
        feeds=("salary baseline", "headcount", "occupation time-series"),
        last_fetched="rolling",
        notes="Live calls to the BLS Public Data API for SOC-code time-series. No key needed for ≤ 25 queries/day; BLS_API_KEY env var lifts to 500/day.",
    ),
    Source(
        key="annual_snapshots_poller",
        name="Annual research-report freshness poller",
        url="https://aiproof.fastinfer.org/sources/",
        access="api",
        licence="Aggregates public publisher pages",
        feeds=("snapshot-staleness signal",),
        last_fetched="rolling",
        notes="Polls Stack Overflow Survey, GitHub Octoverse, ISC2, and WEF Future of Jobs publisher pages weekly to detect when a newer release ships. Does not auto-ingest — flags for human review.",
    ),
    Source(
        key="usajobs_api",
        name="USAJobs.gov Search API (US Federal)",
        url="https://developer.usajobs.gov/",
        access="api",
        licence="Public domain (US federal work)",
        feeds=("US federal posting volume",),
        last_fetched="rolling",
        notes="Free API after one-time email registration; runs when USAJOBS_API_KEY env var is set.",
    ),
    Source(
        key="adzuna_api",
        name="Adzuna global job-search API",
        url="https://developer.adzuna.com/",
        access="api",
        licence="Adzuna API ToS (attribution required)",
        feeds=("16-country posting volume", "salary", "AI mention rate"),
        last_fetched="rolling",
        notes="250 calls/day free. Aggregates Indeed/Reed/CV-Library legally across 16 countries — runs when ADZUNA_APP_ID and ADZUNA_API_KEY env vars are set.",
    ),
    Source(
        key="reed_uk_api",
        name="Reed.co.uk Job Search API",
        url="https://www.reed.co.uk/developers/jobseeker",
        access="api",
        licence="Reed Developer ToS (attribution required)",
        feeds=("UK posting volume", "salary"),
        last_fetched="rolling",
        notes="1,000 calls/day free; runs when REED_API_KEY env var is set.",
    ),
    Source(
        key="onet_api",
        name="O*NET Web Services API (US DOL)",
        url="https://services.onetcenter.org/",
        access="api",
        licence="CC BY 4.0 (US Department of Labor)",
        feeds=("skill depth", "task automation susceptibility"),
        last_fetched="rolling",
        notes="Skills, work-activities, and abilities per SOC code — feeds the skill_depth + human_judgment scoring. Runs when ONET_USER and ONET_PASS env vars are set.",
    ),

    # ---------- CACHED snapshots (annual / manual, cited in methodology) ----------
    Source(
        key="bls_oep",
        name="U.S. Bureau of Labor Statistics — Occupational Employment Projections (2024–2034)",
        url="https://www.bls.gov/emp/tables.htm",
        access="annual_report",
        licence="Public domain (US federal work)",
        feeds=("demand baseline",),
        last_fetched="2024-09",
        notes="BLS-published projections, cached at data/raw/bls_projections_2024_2034.json. Used by the original calibration; no live API call today. A live BLS Public Data API crawler is on the Phase 10 roadmap.",
    ),
    Source(
        key="so_survey",
        name="Stack Overflow Developer Survey",
        url="https://survey.stackoverflow.co/",
        access="annual_report",
        licence="ODbL (data) / CC BY 4.0 (text)",
        feeds=("compensation reference", "tooling adoption", "AI-tool use"),
        last_fetched="2025-07",
        notes="Annual CSV release; cached snapshot used in the methodology + insights pages.",
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
        access="manual",
        licence="Site-published, attribution",
        feeds=("trend direction", "category risk"),
        last_fetched="2026-04",
        notes="Aggregated layoff events by company and role family; the site is client-side rendered so we maintain a manual snapshot rather than scrape.",
    ),
    Source(
        key="levels_fyi",
        name="Levels.fyi compensation snapshots",
        url="https://www.levels.fyi/",
        access="manual",
        licence="Site-published, attribution",
        feeds=("senior IC compensation",),
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
