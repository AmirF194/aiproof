# AIProof — Crawler & Data-Gathering Plan

Reliable, legal, extensive coverage of the global tech labour market — feeding [aiproof.fastinfer.org](https://aiproof.fastinfer.org/) with real, refreshable posting + market signals.

This document is the durable plan. [PLAN.md](PLAN.md) tracks the broader product roadmap; this file tracks **only data gathering**. When a new source is shipped, tick it here and add its entry to [web/apps/core/sources.py](web/apps/core/sources.py).

---

## 1. Binding constraints

These are not optional. They map to the user-set rules already published on [`/data-policy/`](https://aiproof.fastinfer.org/data-policy/).

1. **No paywalled / login-gated / robots-disallowed scraping.** Means LinkedIn, Indeed (direct), Glassdoor (direct), ZipRecruiter are off-limits.
2. **Identifiable User-Agent.** Every crawler sends `aiproof-research/1.0 (+https://aiproof.fastinfer.org)`.
3. **Respect rate limits.** Each crawler has a per-source delay; we honour `Retry-After` headers.
4. **No fabricated data.** When a source fails, we preserve the prior snapshot and log the failure — we never substitute synthetic numbers.
5. **Public archive.** Every raw response is persisted to `data/raw/{source}_{date}.csv`/`json` so claims are auditable.
6. **License-aware.** Each source's redistribution terms are recorded in `apps.core.sources.SOURCES`. We never expose raw fields from a source whose licence forbids it.

---

## 2. Current state (baseline)

5 live API crawlers, refreshing weekly via Celery beat → ~7,543 postings/run, **153 of 1,000 roles** matched.

| # | Source | Endpoint | Cos covered | Rows / run |
|---|---|---|---|---|
| 1 | Hacker News "Who is Hiring" | `hn.algolia.com/api/v1` | 12 months of threads | 2,742 |
| 2 | Greenhouse public boards | `boards-api.greenhouse.io/v1/boards/{co}/jobs` | ~30 | 3,587 |
| 3 | Lever public boards | `api.lever.co/v0/postings/{co}` | ~8 | 696 |
| 4 | The Muse | `themuse.com/api/public/jobs` | aggregator | 500 |
| 5 | Remotive | `remotive.com/api/remote-jobs` | aggregator | 18 |

Cached snapshots (cited but not refreshed automatically): BLS OEP, Stack Overflow Survey, GitHub Octoverse, ISC2 Workforce, layoffs.fyi, Levels.fyi, Gartner press.

---

## 3. Why the current set is not enough

- **153 / 1,000 role match rate** = 84.7% of the catalogue has zero live signal.
- The unmatched roles are mostly: (a) C-suite / Director-of-X — filled via recruiters, (b) niche specialties whose exact title rarely appears, (c) regions our crawled companies don't post to (no Canadian, no European data).
- **Geographic blind spot**: zero Indeed.ca, JobBank.gc.ca, EURES, Reed UK data. The site claims "global" tech labour-market signal but is functionally US-centric.
- **YoY signal**: only HN exposes posting dates → YoY % is null on ~85% of role pages.
- **Compensation signal**: Levels.fyi is a manual snapshot, not live.

Goal: lift coverage to **≥ 500 / 1,000 roles** with non-null live data and **≥ 50,000 postings / week** crawled, with at least 3 non-US data sources.

---

## 4. Source taxonomy

Five tiers, ranked by ease + legality:

### Tier 1 — Free, no auth, JSON-shaped public endpoints ✅ ship first

These are the easiest wins. Each adds a crawler module ~80 lines of code, no API key.

| Source | Endpoint pattern | Coverage |
|---|---|---|
| **Workable** | `apply.workable.com/api/v3/accounts/{slug}/jobs` | 200+ companies |
| **SmartRecruiters** | `api.smartrecruiters.com/v1/companies/{id}/postings` | 100+ companies |
| **Recruitee** | `{slug}.recruitee.com/api/offers` | 50+ companies |
| **Ashby** | `api.ashbyhq.com/posting-api/job-board/{slug}` | 80+ companies (AI/devtools heavy) |
| **Personio** | `{slug}.jobs.personio.com/search.json` | 50+ companies (Europe-focused) |
| **Teamtailor** | `api.teamtailor.com/v1/jobs` (per-company) | 30+ companies |
| **BambooHR** | `{slug}.bamboohr.com/jobs/embed2.php?type=json` | 60+ companies (SMB) |
| **Jobvite** | `app.jobvite.com/CompanyJobs/SearchJobs.aspx?c={id}&format=json` | varies |
| **WeWorkRemotely RSS** | `weworkremotely.com/categories/*.rss` | aggregator, remote-only |
| **Working Nomads RSS** | `workingnomads.com/jobsrss` | aggregator |
| **Remote.co RSS** | `remote.co/feed/` | aggregator |
| **JustRemote** | `justremote.co/api/jobs` | aggregator |
| **Greenhouse expansion** | (existing crawler) | **30 → 300 companies** (10× existing endpoint, zero new infra) |
| **Lever expansion** | (existing crawler) | **8 → 50 companies** |

**Estimated lift**: +40,000 postings/week, +200 roles with live data.

### Tier 2 — Free, requires email-only registration ✅ ship second

Single one-time setup, keys in `.env` on prod.

| Source | What you get | Rate limit | Geographic |
|---|---|---|---|
| **Adzuna API** | Aggregated Indeed/Reed/CV-Library across 16 countries (US, UK, CA, AU, DE, FR, IN, NL, PL, IT, ES, RU, ZA, MX, BR, SG) | 250 calls/day free | Global |
| **USAJobs Search API** | Federal job postings | Generous (10k/day with key) | US |
| **BLS Public Data API** | Live time-series for occupational employment & wages by SOC code | 500 queries/day with free key, 25/day without | US |
| **O\*NET Web Services API** | Skills, tasks, abilities per SOC code — the canonical source for skill-depth + automation-task analysis | Generous, free account | US (international SOC mappings exist) |
| **Reed.co.uk API** | UK job postings | 1,000 calls/day free | UK |

**Estimated lift**: +30,000 postings/week, +150 roles, **first non-US data**.

### Tier 3 — Legal Indeed/LinkedIn aggregator proxies via RapidAPI 💳 ship third

These cost money beyond a small free tier but legally aggregate data from sources we can't crawl directly.

| Source | Coverage | Cost |
|---|---|---|
| **JSearch (RapidAPI)** | Aggregates Indeed, LinkedIn, Glassdoor, Google Jobs, ZipRecruiter — legally, via RapidAPI's pipeline | Free tier 200 reqs/month; $30/mo for 10k reqs |
| **Active Jobs DB (RapidAPI)** | Half-million-row global jobs dataset, refreshed daily | $20/mo |
| **Job Posting Feed (RapidAPI)** | LinkedIn job feed legally relayed | $40/mo |

**Estimated lift**: Closes the Indeed/LinkedIn gap legally. +50,000 postings/week if budget allows. The way to credibly say "we cover Indeed" without scraping it.

### Tier 4 — Government open data 🇨🇦🇪🇺 ship in parallel with Tier 2

Public datasets, no rate limit, free, comprehensive.

| Source | Format | Refresh |
|---|---|---|
| **Government of Canada Job Bank — Open Data** | Bulk CSV via Open Government Portal (`open.canada.ca`) | Monthly |
| **EURES (EU)** | REST API for cross-EU job postings | Live |
| **CompTIA Cyberseek (US)** | Cyber-workforce demand map | Quarterly |
| **OECD Skills for Jobs** | Skills shortage by country | Annual CSV |

**Estimated lift**: Direct answer to "do we have Indeed.ca?" — Job Bank covers the same labour-market intent for Canada with cleaner, license-clean data.

### Tier 5 — Annual / cyclic snapshots — automated download ✅ keep maintained

Already cited; the automation upgrade is to fetch + diff + alert when a new release ships.

| Source | When |
|---|---|
| Stack Overflow Developer Survey CSV | Each summer (July) |
| GitHub Octoverse JSON / HTML | Each autumn (October) |
| ISC2 Workforce Study top-line | Each December |
| BLS OEP / OEWS publication | Every 2 years |
| WEF Future of Jobs | Annual (May) |
| McKinsey GenAI Workforce | Annual |

---

## 5. Infrastructure required

Before adding 20+ new crawlers, the shared infrastructure needs to harden.

### 5.1 Rate-limiter

Single shared per-source token-bucket. `apps/core/crawl/ratelimit.py`:

```python
class RateLimiter:
    def __init__(self, calls_per_minute: int, burst: int = 1): ...
    def acquire(self) -> None: ...   # blocks if needed
```

Per-source config in `data/crawl_config.yml`:

```yaml
greenhouse: { calls_per_minute: 60 }
lever:      { calls_per_minute: 30 }
themuse:    { calls_per_minute: 30 }
adzuna:     { calls_per_minute: 5,  daily_cap: 250 }
jsearch:    { calls_per_minute: 1,  monthly_cap: 200 }
```

### 5.2 Retry + circuit breaker

Standard pattern: 3 retries with exponential back-off, then circuit-break for 1 hour. Failures are logged structurally (source, status, retry count) so we can build an alert dashboard.

### 5.3 Storage & dedup

Replace per-source CSVs with a single `RawPosting` Django model:

```python
class RawPosting(models.Model):
    source = models.CharField(max_length=40, db_index=True)
    posting_id = models.CharField(max_length=120)            # source-native ID
    company = models.CharField(max_length=200, db_index=True)
    title = models.CharField(max_length=300, db_index=True)
    location = models.CharField(max_length=200)
    posted_at = models.DateTimeField(null=True, db_index=True)
    url = models.URLField()
    snippet = models.TextField()                              # for ai-mention regex
    fingerprint = models.CharField(max_length=64, db_index=True)  # sha256(company|title|location)
    seen_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source", "posting_id"], name="uniq_source_posting"),
        ]
        indexes = [models.Index(fields=["fingerprint", "source"])]
```

Dedup logic:
- Same `(source, posting_id)` → update `last_seen_at`, don't insert (job still live)
- Cross-source dedup by `fingerprint` → first-seen wins, others tagged as `cross_source_duplicate`

### 5.4 Scheduling tiers

Different sources have different cadences:

| Cadence | Sources | Why |
|---|---|---|
| **Daily** | Adzuna, JSearch (with budget) | High-quota aggregators; daily refresh keeps the YoY series fine-grained |
| **Weekly** | All Tier 1 + Workable, SmartRecruiters, etc. | Companies update their boards weekly; HN posts monthly |
| **Monthly** | Canada Job Bank Open Data, OECD | Their refresh cycle |
| **On publish** | Annual reports | Detected by polling the publisher's blog/RSS |

Celery beat config grows from 1 task to ~5 staggered tasks (offset by hours to spread load).

### 5.5 Observability

- Each crawler emits a metric: `{source, rows_fetched, errors, duration_ms}`
- A new `/admin/crawl/` page (staff-only) shows last-run-status per source
- Slack/email alert when a source returns 0 rows three runs in a row (= broken, not just slow)

### 5.6 robots.txt compliance

Add a one-time check at crawler startup: fetch `{site}/robots.txt`, verify our User-Agent isn't disallowed for the path. If disallowed: skip the source, log a warning, no scrape.

---

## 6. Implementation phases

Map to PLAN.md naming convention (Phase 10A, 10B, …). Each phase ships independently, CI-gated, deployable on its own.

### Phase 10A — Infrastructure   `[ ]`   est. 1 day

- `apps/core/crawl/` package: `ratelimit.py`, `retry.py`, `fingerprint.py`
- `RawPosting` model + migration
- Replace 5 existing crawlers' CSV writers with `RawPosting.objects.bulk_create(..., update_conflicts=True)`
- Migrate `aggregate_live_postings.py` to read from `RawPosting` instead of CSVs
- Backwards-compat: still write the CSVs (used by /data/role_postings_live.csv download)

**Coverage delta:** 0 (foundation only)

### Phase 10B — ATS expansion (Tier 1)   `[ ]`   est. 2 days

Add 8 new crawlers, all no-auth public endpoints, all following the same pattern as `greenhouse_ats.py`:

- `workable_ats.py` — 50 confirmed Workable boards (probe + curated list)
- `smartrecruiters_ats.py` — 30 confirmed boards
- `recruitee_ats.py` — 25 boards
- `ashby_ats.py` — 40 boards (AI/devtools heavy)
- `personio_ats.py` — 25 boards (Europe-focused)
- `bamboohr_ats.py` — 30 boards
- `weworkremotely_rss.py` — full RSS parse
- `workingnomads_rss.py` — full RSS parse

Plus expand existing:
- Greenhouse: 30 → 300 companies (probe `boards.greenhouse.io` directory)
- Lever: 8 → 50 companies (manual curation)

**Coverage delta:** +40,000 postings/week, ~+200 matched roles. **Single biggest lift.**

### Phase 10C — Free-tier public APIs (Tier 2)   `[ ]`   est. 1 day

Requires 4 keys in `.env`:
- `ADZUNA_APP_ID`, `ADZUNA_API_KEY` — register at developer.adzuna.com
- `USAJOBS_EMAIL` — register at developer.usajobs.gov
- `BLS_API_KEY` — register at data.bls.gov
- `ONET_USER`, `ONET_PASS` — register at services.onetcenter.org

Crawlers:
- `adzuna_api.py` — 16 countries, paginated; per-country quota 250/day
- `usajobs_api.py` — keyword search across federal listings
- `bls_oep_api.py` — replace cached snapshot with live calls per SOC code
- `bls_oews_api.py` — wage data per SOC code
- `onet_api.py` — skills/tasks/abilities per role (feeds skill-depth scoring)

**Coverage delta:** +30,000 postings/week (mostly Adzuna), first non-US data, real BLS time-series for YoY.

### Phase 10D — Government open data (Tier 4)   `[ ]`   est. half day

- `canada_jobbank.py` — download monthly CSV from open.canada.ca/data
- `eures_api.py` — EU REST API
- `oecd_skills.py` — annual CSV

**Coverage delta:** Canada coverage answers the "Indeed.ca" question directly. EU coverage adds Germany/France/Netherlands signal.

### Phase 10E — Legal Indeed/LinkedIn aggregators (Tier 3)   `[ ]`   est. half day + budget decision

Skip until budget is approved. When approved:

- `jsearch_rapidapi.py` — daily refresh, aggregates Indeed/LinkedIn/Glassdoor legally
- `active_jobs_db_rapidapi.py` — bulk dataset, weekly refresh

**Cost:** $30–100/month depending on tier.
**Coverage delta:** Closes the Indeed gap. Lets us legitimately claim "Indeed-aggregated data" on the methodology page.

### Phase 10F — Annual snapshot automation   `[ ]`   est. half day

- Polling job that watches publisher feeds (SO Survey, Octoverse, ISC2) and alerts when a new release ships
- Automated CSV/PDF download with checksum + signature verification (where available)

**Coverage delta:** 0 (refresh quality only)

### Phase 10G — Observability + alerts   `[ ]`   est. half day

- `/admin/crawl/` dashboard
- Slack alert on 3-consecutive-failures per source
- Daily summary email of crawl health

---

## 7. Coverage forecast

| Phase | Live sources | Postings / week | Roles matched | Geography |
|---|---|---|---|---|
| Today | 5 | 7,543 | 153 / 1,000 | US-centric |
| After 10A+10B | 13 | ~47,000 | ~350 / 1,000 | US-centric |
| After 10C | 18 | ~77,000 | ~450 / 1,000 | + UK, EU, global Adzuna |
| After 10D | 21 | ~85,000 | ~480 / 1,000 | + Canada, EU |
| After 10E (with budget) | 23 | ~135,000 | ~600 / 1,000 | + Indeed/LinkedIn legal proxy |

These are estimates. The non-linear bit is matched-role count, which depends on synonym map evolution as much as source count.

---

## 8. Open decisions needed from product

Before kicking off Phase 10:

1. **Adzuna API key?** Free tier needs an email + organisation name. OK to register as FastInfer Inc., or use a personal email?
2. **RapidAPI / JSearch budget?** Tier 10E is the only paid item. $30–100/month decision.
3. **O\*NET account?** Single registration; do we use it for skill-depth scoring re-derivation (sizeable methodology change) or only for citation?
4. **Order of execution?** Default suggestion is 10A → 10B → 10C → 10D → 10F → 10G, then 10E if budget approves. Open to re-ordering.
5. **Storage growth.** RawPosting at ~135,000 rows/week × 52 weeks × 5 years = ~35M rows. Postgres handles that fine but `data/raw/*.csv` mounts won't be backed up to a separate bucket by default. Add S3/B2 backup as 10H?

---

## 9. What this plan deliberately does NOT include

- **Direct LinkedIn scraping** — TOS violation, hiQ-precedent legal risk
- **Direct Indeed.com / Indeed.ca scraping** — TOS + bot detection
- **Direct Glassdoor scraping** — login-gated, bot-detected
- **Aggregated Reddit / Twitter sentiment** — noisy signal, ethical concerns about user-content reuse
- **Headless-browser scraping (Puppeteer/Playwright)** — too easy to slide into TOS-violation territory; we stick to public APIs and RSS

Anyone proposing one of these for AIProof should be redirected back to this document.

---

## 10. Execution log

Update when each phase ships.

| Phase | Started | Shipped | Commit | Notes |
| --- | --- | --- | --- | --- |
| 10A — Infrastructure | — | — | — | — |
| 10B — ATS expansion | — | — | — | — |
| 10C — Free-tier APIs | — | — | — | — |
| 10D — Gov open data | — | — | — | — |
| 10E — RapidAPI aggregators | — | — | — | — |
| 10F — Annual snapshot automation | — | — | — | — |
| 10G — Observability | — | — | — | — |
