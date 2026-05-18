# AIProof — career-intelligence platform for the 2026–2035 AI shake-out

**Live site:** <https://aiproof.fastinfer.org/>

AIProof is a research project by **[FastInfer Inc.](https://fastinfer.org)** that ranks **1,000 technology roles** by their expected resilience to AI automation over **2026–2035**. Every role is scored across **8 dimensions** — four base (demand, automation resistance, skill depth, strategic importance) and four derived (human judgment, stakeholder interaction, AI augmentation potential, regulatory relevance). Live posting signals from 5 public job feeds refresh weekly.

The site presents the ranking, individual role profiles with score breakdowns, side-by-side comparisons, full methodology, source list, and limitations. The same data is available as downloadable CSVs.

## Quick links

- [Methodology](METHODOLOGY.md) — scoring rubric, weights, the 8 dimensions, confidence math
- [Insights](INSIGHTS.md) — deep research synthesis with cited claims
- [Report](REPORT.md) — top + bottom of the ranking, every category
- [PLAN.md](PLAN.md) — phased roadmap and execution log for the 2026 product overhaul
- Live: `/sources/`, `/limitations/`, `/data-policy/`, `/compare/`

---

## Running the web app locally

```bash
docker compose up -d --build
docker compose exec api python manage.py migrate
docker compose exec api python manage.py load_roles --wipe
docker compose exec worker python manage.py refresh_postings   # optional — pulls live data
```

Open <http://localhost:9012/>. Five containers run: API (gunicorn), Celery worker, Celery beat, Postgres, Redis.

### Dev loop

```bash
# Inside the api container
docker compose exec -w /app api ruff check .
docker compose exec -w /app api python -m pytest -q
docker compose exec api python manage.py validate_data
docker compose exec api python manage.py check
```

The same checks run in CI on every push and pull request (see [.github/workflows/deploy.yml](.github/workflows/deploy.yml)) — deploys are gated behind them.

### Refreshing the dataset

Live posting feeds are crawled weekly by Celery beat. To force a refresh manually:

```bash
docker compose exec worker python manage.py refresh_postings
```

That runs all 5 crawlers (HN Algolia, Greenhouse public boards, Lever public boards, The Muse, Remotive), aggregates the raw CSVs into per-role metrics, and updates `RoleMetric` rows. See [/data-policy/](https://aiproof.fastinfer.org/data-policy/) for the full feed list, cadence, and ethics.

### Re-deriving scores after a methodology change

```bash
# Edit web/apps/roles/scoring.py
docker compose exec api python manage.py load_roles --wipe    # re-derives every role
docker compose exec api python manage.py validate_data        # confirms formula integrity
docker compose exec -w /app api python -m pytest -q          # exercises every URL + the scoring formulas
```

Then commit and push — CI gates the deploy.

---

## Original data analysis (pre-web-app)

What follows is the original analytical project — the dataset, methodology, and per-role scoring that the web app surfaces. The numbers below were the starting calibration set; the web app extends them with 4 derived dimensions and live posting data.

> Scope: senior-IC framing, US/EU markets, USD total comp. Sources are directional — BLS 2024–34 projections, ISC2 2025 Cybersecurity Workforce Study, Stack Overflow Developer Survey 2025 (~49K respondents), Levels.fyi (April 2026), Gartner platform-engineering and AI-agent forecasts, McKinsey 2025 generative AI workforce study, Pragmatic Engineer 2026 industry report, Challenger / Gray & Christmas Q1 2026 layoff data. Full source list: [METHODOLOGY.md](METHODOLOGY.md). Deep research synthesis with citations per claim: [INSIGHTS.md](INSIGHTS.md).

---

## TL;DR — The five tiers

| Tier | Score | Roles | Verdict |
| --- | --- | --- | --- |
| **Fortress** | 83+ | 79 | Build a career here without hedging. |
| **Safe** | 70–82 | 315 | Senior path is durable. Junior path is harder than 2020. |
| **Stable** | 58–69 | 329 | Specialize or get exposed. Generalist track compresses. |
| **Exposed** | 41–57 | 223 | Plan an adjacent move within 2–3 years. |
| **At risk** | ≤40 | 54 | Plan a transition. Headcount shrinks every year. |

![Safety Score Ranking](charts/safety_score.svg)

Full per-role analysis in [REPORT.md](REPORT.md). Raw scoring data in [data/roles.csv](data/roles.csv).

---

## Top 10 safest roles (2026–2035)

| # | Role | Score | Why it ranks here |
| --- | --- | --- | --- |
| 1 | Chief AI Officer | 94 | New C-suite role; owns the model-strategy moat at every AI-first org. |
| 1 | Staff Engineer / Tech Lead | 94 | Owns judgment, architecture, and trade-offs — none of which AI replaces. |
| 1 | VP of AI / ML | 94 | Allocates GPU and headcount in the highest-leverage spend category. |
| 1 | Staff Security Engineer | 94 | Adversarial domain; attackers also use AI, so defenders are net-up. |
| 5 | Senior LLM Engineer | 92 | Owns the production foundation-model integration layer. |
| 5 | Security Engineer | 92 | Senior security IC remains the most-undersupplied IC role. |
| 5 | Senior Security Engineer | 92 | Same, with proven track record; comp band $160K–$400K. |
| 8 | CTO | 91 | Top-tier judgment role; AI augments rather than substitutes. |
| 8 | Principal Engineer | 91 | The IC ladder above Staff is the most durable career shape. |
| 8 | Senior Principal Engineer | 91 | Above-Principal IC tier scales to $1M+ TC at frontier labs. |
| 8 | Senior Staff Engineer | 91 | The "Staff that ships big architecture" tier; supply is glacial. |

For the full top-30, the bottom-20, and per-category top-and-bottom, see [REPORT.md](REPORT.md). The complete 1,000-row ranking is [data/processed/role_ranking.csv](data/processed/role_ranking.csv).

## Bottom 8 most-at-risk roles

| # | Role | Score | Why it ranks here |
| --- | --- | --- | --- |
| 988 | Data Analyst | 33 | LLM SQL + BI tools cover ~60% of operational analytics requests. |
| 991 | MicroStrategy Developer | 30 | Vendor-bound BI; tooling absorbed by modern semantic layers. |
| 991 | Game QA Tester | 30 | Routine play-through validation is highly automatable. |
| 991 | Desktop Support | 30 | Self-service portals + AI agents replace tier-1 work. |
| 994 | ColdFusion Maintainer | 29 | Legacy stack; shrinking maintainer pool with no replacement pipeline. |
| 994 | jQuery Maintainer | 29 | Pre-React JavaScript era; runway is "until the app is rewritten." |
| 998 | Prompt Engineer | 27 | A 2023 artifact; absorbed back into AI Application / ML Eng work. |
| 999 | Help Desk Tier 1 | 25 | Textbook AI-replacement case in corporate IT. |
| 1000 | QA Manual | 20 | Lowest-scored role in the dataset. Plan an exit, not a defense. |

---

## What the 2025–2026 data confirms

These are the load-bearing numbers behind the rankings. Citations and full synthesis in [INSIGHTS.md](INSIGHTS.md).

| Signal | Number | Source |
| --- | --- | --- |
| Software developer 10-yr employment growth | **+15%** (vs 3% all-occ avg) | BLS 2024–34 projections |
| Information security analyst 10-yr growth | **+32%** | BLS OOH |
| Global cybersecurity workforce gap | **4.8 million** unfilled | ISC2 2025 Workforce Study |
| Orgs reporting critical security skill shortage | **59%** (up from 44% in 2024) | ISC2 2025 |
| Large orgs with platform-engineering teams by 2026 | **80%** (from 45% in 2022) | Gartner |
| Enterprise apps with AI agents by end-2026 | **40%** (from <5% in 2025) | Gartner |
| Q1 2026 tech layoff announcements (US) | **52,050** (+40% YoY); **~48% AI-attributed** | Challenger, Gray & Christmas |
| Software dev employment, ages 22–25 | **−20%** vs late-2022 peak | Stanford / CPS analysis |
| Senior software engineer median comp | **+12–18% YoY** at surviving cos | Goldman Sachs (cited via KORE1) |
| Stack Overflow 2025: developers using AI | **84%** (51% daily); only **29%** trust output | Stack Overflow Developer Survey |
| ML Engineer median TC (Levels.fyi) | **$264K**; FAANG range **$265K–$450K** | Levels.fyi April 2026 |
| Agentic AI engineer comp | **$155K–$265K base, $400K+ TC top tier** | KORE1 / Acceler8 / Glassdoor |
| AI engineer base salary growth | **+9.2% (2025), +7% (2026)** ("Agentic Surge") | KORE1 |

The single sentence that captures all of this: **the senior tier is rising, the junior tier is being repriced, and the middle is being compressed**. Every score in this analysis assumes that bifurcation.

---

## Headline conclusions

**1. The safest roles cluster around three things: judgment, adversaries, and production.**
Staff engineers, security, and SREs all share the same property — they own outcomes that fail in messy, context-dependent ways. AI assists at every keystroke but cannot carry a pager. Roles that fail cleanly (a missing endpoint, a broken layout, a wrong chart) are the ones AI eats first.

**2. "AI risk" splits roles into three groups, not two.**

- **Multipliers** (one engineer doing 2–3×): Backend, Platform, ML, Security, Data Eng. AI raises throughput; headcount stays flat or grows.
- **Compressors** (1.5 engineers do the work of 3): Frontend, Full-Stack, QA Automation, Analytics Eng. Headcount drops 20–40% by 2030.
- **Replacements** (AI does most of the role): Manual QA, Data Analyst, UI Designer, Prompt Eng. Headcount drops 50%+.

**3. Security is the single most-undervalued category in this analysis.**
Every Security role lands in the top tier. Reason: AI-generated code multiplies attack surface while regulatory pressure (EU AI Act, SEC cyber-disclosure, sectoral rules) multiplies compliance demand. Five-year demand growth here is the strongest of any cluster.

**4. The "Data & AI" cluster is bimodal, not uniformly hot.**
ML Eng, MLOps, AI Research, Data Eng → Fortress.
Data Scientist, Analytics Eng → Exposed.
Data Analyst → At risk.
The split is whether the role *builds* AI systems or *consumes* them. Builders win the decade.

**5. Mid-level generalist tracks are the soft spot at every layer.**
"React dev," "full-stack TypeScript," "data scientist who runs notebooks," "QA who writes Selenium" — all the same shape, all compressing. The escape is depth: pick a domain (payments, search, ML infra), a cross-cutting skill (perf, a11y, security), or a platform (deep K8s, deep iOS, deep PostgreSQL).

**6. Leadership and senior IC tracks both win — for different reasons.**
Engineering Manager (83) and Staff Engineer (94) both score in the Fortress tier. AI compresses individual contributors but raises the value of people who allocate, mentor, and architect. The ladder gets steeper because the bottom rungs erode.

---

## Safe skill combinations (better than any single skill)

| Combination | Why it compounds |
| --- | --- |
| **Backend + AI / RAG / agents** | Most production AI work is integration. Backends with model literacy win. |
| **DevOps + Security** | Cloud security and infra security are converging into one role. |
| **Data Engineer + ML platforms** | Feature stores, training data pipelines, lakehouse → MLOps. |
| **Frontend + Design Systems / a11y** | The defensible part of frontend. Generalists compress; specialists hold. |
| **Mobile + Cross-platform native** | Deep KMP / Compose Multiplatform / SwiftUI internals stay rare. |
| **Product Manager + Technical depth** | TPM rate is rising while generalist PM stays flat. |
| **SRE + ML systems reliability** | "MLSRE" is a real and growing niche. ML inference uptime is hard. |

---

## How to use this

- **Choosing a first specialization** — go Security, Platform, or ML/Data Engineering. Highest safety, strongest 5-year demand, defensible skill depth.
- **Mid-career pivot from a Stable or Exposed tier** — the highest-leverage move is *adjacent*, not lateral. Frontend → Design Systems / DX. Data Scientist → ML Engineer. QA → SDET → Backend or AI Eval.
- **Mid-career pivot from At-risk** — give yourself 12–18 months and a structured study plan. The transitions that work: Manual QA → SDET → AI Eval; Data Analyst → Analytics Eng → Data Eng; UI Designer → Product Designer.
- **Hiring** — expect Security, ML, and Platform comp to keep climbing through 2028. Expect Manual QA budgets to compress 30–50% by 2030. Expect "AI Application Engineer" to be a hot title that consolidates back into "Backend Engineer who knows LLMs" by 2029.

---

## Charts

| File | What it shows |
| --- | --- |
| [charts/safety_score.svg](charts/safety_score.svg) | Top 50 + bottom 25 of the 1,000-role ranking, color-coded by tier (full ranking in `data/processed/role_ranking.csv`). |
| [charts/automation_risk.svg](charts/automation_risk.svg) | Demand vs. automation resistance — quadrant view of risk. |
| [charts/salary_range.svg](charts/salary_range.svg) | Senior-IC salary bands for the top, middle, and bottom of the ranking. |
| [charts/demand_growth.svg](charts/demand_growth.svg) | Average safety score and demand by category. |

Regenerate with `python3 scripts/run_pipeline.py` (no third-party dependencies). The chart step on its own: `python3 scripts/visualization/generate_charts.py`.

---

## Repository structure

```text
.
├── README.md           — this file (executive summary, conclusions)
├── REPORT.md           — top + bottom of the 1,000-role ranking and each category
├── INSIGHTS.md         — deep research synthesis with 2025–26 data, cited per claim
├── METHODOLOGY.md      — scoring rubric, weights, source list, limitations
├── data/
│   ├── roles.csv       — canonical scoring inputs (re-weight if you disagree)
│   ├── raw/            — source-of-truth datasets (real where possible, simulated where labeled)
│   │   ├── bls_projections_2024_2034.json
│   │   ├── isc2_workforce_2025.json
│   │   ├── levels_fyi_compensation_2026.json
│   │   ├── stackoverflow_developer_survey_2025.json
│   │   ├── gartner_forecasts_2025_2028.json
│   │   ├── layoffs_q1_2026.json
│   │   ├── wef_future_of_jobs_2025.json
│   │   ├── mckinsey_genai_workforce_2025.json
│   │   ├── github_octoverse_2025.json
│   │   ├── role_definitions.json
│   │   ├── linkedin_postings_simulated.csv
│   │   ├── indeed_postings_simulated.csv
│   │   ├── ai_mention_signals_simulated.csv
│   │   └── glassdoor_salary_simulated.csv
│   └── processed/      — pipeline outputs
│       ├── postings_timeseries.csv
│       ├── salary_per_role.csv
│       ├── role_metrics.csv
│       ├── role_signals.json
│       ├── score_components.csv
│       ├── role_ranking.csv
│       ├── tier_summary.csv
│       ├── category_summary.csv
│       └── trend_buckets.csv
├── scripts/
│   ├── run_pipeline.py — top-level orchestrator
│   ├── data_collection/   — load + refresh raw sources
│   ├── data_cleaning/     — normalize, merge, derive per-role metrics
│   ├── analysis/          — score, rank, tier, trend extraction
│   └── visualization/     — pure-Python SVG generators
├── charts/                — four SVG charts (regenerated by the pipeline)
└── docs/
    ├── role_taxonomy.md       — 36-role definitional taxonomy (predates the 1,000-role expansion)
    ├── career_paths.md        — entry points, pivots, skill combinations
    └── ai_impact_analysis.md  — Multipliers / Compressors / Replacements / Untouched
```

### Data lineage

`data/raw/*` (real + simulated, all labeled) → `scripts/data_cleaning/` → `data/processed/role_metrics.csv` + `role_signals.json` → `scripts/analysis/` → `data/processed/score_components.csv` + `role_ranking.csv` + `tier_summary.csv` + `trend_buckets.csv` → `scripts/visualization/generate_charts.py` → `charts/*.svg`.

`data/raw/` distinguishes real from simulated data via filenames and a `data_kind` field on every row/object. Real-source numbers (BLS, ISC2, Levels.fyi, Stack Overflow, Gartner, Q1 2026 layoffs, McKinsey, WEF, GitHub Octoverse) are cached snapshots audited against the URLs in [METHODOLOGY.md](METHODOLOGY.md). Simulated postings volumes and AI-mention rates are calibrated to the published signals and clearly marked.

### Reproduce

```bash
python3 scripts/run_pipeline.py
```

Pipeline runs in <5 seconds and uses `cairosvg` for the optional SVG→PNG rasterization step that feeds the LaTeX PDF; the score/chart generation has no third-party dependencies. The `compute_scores.py` step verifies all 1,000 published scores match the rubric to the integer (it raises if any drift is detected).

---

## Limitations

- **Geography:** US/EU bias. India, LATAM, SEA markets have different curves — Mobile, Frontend, and QA Automation hold up longer there.
- **Seniority:** Senior-IC framing. Junior-market dynamics are worse across the board because AI compresses the bottom of the ladder hardest.
- **Time horizon:** A 5–10 year window is long enough that a single foundation-model breakthrough or a regulatory clamp could re-rank these. Re-evaluate annually.
- **Industry:** Tech-product companies and FAANG-adjacent assumed. Heavily-regulated industries (defense, healthcare, finance) shift the rankings — Mobile and QA Manual hold longer there because of compliance overhead.

This is a frame for thinking, not a forecast. Use it to make decisions, not to predict markets.
