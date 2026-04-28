# Which Tech Jobs Are Safe? A 2026–2035 Market Analysis

A structured comparison of **36 roles** across modern software organizations, scored on demand, automation resistance, skill depth, and strategic importance. Designed for real career decisions — choosing a first specialization, mid-career pivots, hiring planning.

> Scope: senior-IC framing, US/EU markets, USD total comp. Sources are directional — BLS 2024–34 projections, ISC2 2025 Cybersecurity Workforce Study, Stack Overflow Developer Survey 2025 (~49K respondents), Levels.fyi (April 2026), Gartner platform-engineering and AI-agent forecasts, McKinsey 2025 generative AI workforce study, Pragmatic Engineer 2026 industry report, Challenger / Gray & Christmas Q1 2026 layoff data. Full source list: [METHODOLOGY.md](METHODOLOGY.md). Deep research synthesis with citations per claim: [INSIGHTS.md](INSIGHTS.md).

---

## TL;DR — The five tiers

| Tier | Score | Verdict | Examples |
| --- | --- | --- | --- |
| **Fortress** | 85–100 | Build a career here without hedging. | Staff Engineer, Security, ML Engineer, Platform |
| **Safe** | 70–84 | Senior path is durable. Junior path is harder than 2020. | Backend, Data Engineer, DevOps, TPM, Solutions Arch |
| **Stable** | 55–69 | Specialize or get exposed. Generalist track compresses. | Mobile, Full-Stack, Product Designer, SDET |
| **Exposed** | 40–54 | Plan an adjacent move within 2–3 years. | Frontend, Data Scientist, Analytics Engineer |
| **At risk** | <40 | Plan a transition. Headcount shrinks every year. | QA Manual, Data Analyst, UI Designer, Prompt Eng. |

![Safety Score Ranking](charts/safety_score.svg)

Full per-role analysis in [REPORT.md](REPORT.md). Raw scoring data in [data/roles.csv](data/roles.csv).

---

## Top 10 safest roles (2026–2035)

| # | Role | Score | Why it ranks here |
| --- | --- | --- | --- |
| 1 | Staff Engineer / Tech Lead | 94 | Owns judgment, architecture, and trade-offs — none of which AI replaces. |
| 2 | Security Engineer | 92 | Adversarial domain; attackers also use AI, so defenders are net-up. |
| 3 | AI Research Engineer | 89 | Frontier work is a tiny, well-paid moat. Comp may compress; demand won't. |
| 4 | ML Engineer | 87 | Builds the systems everyone else integrates. Critical-path role. |
| 4 | MLOps Engineer | 87 | Production AI fails without these people. Demand is structural. |
| 4 | Platform Engineer | 87 | Internal platforms scale orgs; AI helps build them, not own them. |
| 4 | Application Security Engineer | 87 | AI-generated code creates *more* AppSec work, not less. |
| 4 | Cloud Security Engineer | 87 | Cloud spend keeps growing; cloud blast radius keeps growing. |
| 9 | Site Reliability Engineer | 84 | Production reliability is a 3 a.m. problem AI can't own end-to-end. |
| 9 | Offensive Security / Red Team | 84 | Highest-skill subdomain in security; small but growing. |

## Bottom 5 most-at-risk roles

| # | Role | Score | Why it ranks here |
| --- | --- | --- | --- |
| 32 | QA Automation | 40 | Self-healing E2E + AI test generation eat the middle of this market. |
| 32 | UI Designer | 40 | Visual-only design work is the most AI-exposed creative task. |
| 34 | Data Analyst | 33 | LLMs do SQL + chart generation. Headcount compression is mechanical. |
| 35 | Prompt Engineer | 27 | A 2023 artifact. Better models reduce, not raise, prompt sensitivity. |
| 36 | QA Manual | 20 | Textbook AI-replacement case. Plan an exit, not a defense. |

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
| [charts/safety_score.svg](charts/safety_score.svg) | Full ranking of all 36 roles, color-coded by tier. |
| [charts/automation_risk.svg](charts/automation_risk.svg) | Demand vs. automation resistance — quadrant view of risk. |
| [charts/salary_range.svg](charts/salary_range.svg) | Senior-IC salary bands for the top, middle, and bottom of the ranking. |
| [charts/demand_growth.svg](charts/demand_growth.svg) | Average safety score and demand by category. |

Regenerate with `python3 scripts/run_pipeline.py` (no third-party dependencies). The chart step on its own: `python3 scripts/visualization/generate_charts.py`.

---

## Repository structure

```text
.
├── README.md           — this file (executive summary, conclusions)
├── REPORT.md           — per-role analysis, all 36 roles, grouped by category
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
    ├── role_taxonomy.md       — 36 roles, definitions, primary skills
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

No third-party dependencies. Pipeline runs in <2 seconds. The `compute_scores.py` step verifies all 36 published scores match the rubric to the integer (it raises if any drift is detected).

---

## Limitations

- **Geography:** US/EU bias. India, LATAM, SEA markets have different curves — Mobile, Frontend, and QA Automation hold up longer there.
- **Seniority:** Senior-IC framing. Junior-market dynamics are worse across the board because AI compresses the bottom of the ladder hardest.
- **Time horizon:** A 5–10 year window is long enough that a single foundation-model breakthrough or a regulatory clamp could re-rank these. Re-evaluate annually.
- **Industry:** Tech-product companies and FAANG-adjacent assumed. Heavily-regulated industries (defense, healthcare, finance) shift the rankings — Mobile and QA Manual hold longer there because of compliance overhead.

This is a frame for thinking, not a forecast. Use it to make decisions, not to predict markets.
