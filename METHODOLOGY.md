# Methodology

The scoring rubric, axis definitions, weights, sources, and limitations behind the rankings in [README.md](README.md) and [REPORT.md](REPORT.md).

## Step 1 — Role identification

The original frame covered 36 broad functions found in modern software organizations of 50+ engineers. The current dataset expands that to **1,000 distinct, posting-real roles** — every entry corresponds to a job title that appears as its own listing on Indeed, LinkedIn, or Levels.fyi today (2026). Roles are grouped into the same 8 categories:

| Category | Roles | Rationale |
| --- | --- | --- |
| Engineering (core IC) | 405 | Backend / frontend / mobile / systems / game / graphics / robotics — fragments hardest because language and framework are primary hiring filters. |
| Data & AI | 178 | Bimodal — splits sharply between builders (ML / LLM / agent / data eng) and consumers (analysts, BI, prompt). |
| Platform & Infrastructure | 121 | Platform / SRE / DevOps / cloud / database / network / IT operations as one stack. |
| Specialized & Emerging | 100 | Sales eng, DevRel, TPM, RPA, SaaS-vendor specialists, integration platforms. |
| Security | 75 | AppSec, cloud, offensive, IR, GRC, IAM, crypto, AI-safety adjacent. |
| Product & Design | 48 | PM ladder × discipline (TPM, AI PM, growth, platform); design ladder + design eng. |
| Engineering Leadership | 45 | C-suite, VP, director, EM ladder, IC ladder (Staff → Distinguished → Fellow). |
| Quality & Testing | 28 | Manual, automation, SDET, perf, security QA, test architect. |

### How distinctness is decided

To reach 1,000 without padding, four legitimate dimensions of distinctness are used. A row earns a place only when it would post as its own job listing — not as a filter on a more generic posting:

1. **Function** (~250 base) — Backend Engineer vs SRE vs Compiler Engineer vs ML Engineer.
2. **Seniority**, when the comp band shifts >50% — Junior / Mid / Senior / Staff / Principal for IC; Manager / Senior / Group / Director / VP / C-suite for management.
3. **Stack or framework**, when it is the primary hiring filter — Solidity Developer, Salesforce Developer, COBOL Developer, SAP ABAP Developer, Java Spring vs FastAPI vs Rails.
4. **Vertical**, when domain knowledge dominates — HFT Engineer, Bioinformatics Engineer, Automotive Security Engineer, HL7/FHIR Integration Engineer.

Roles are deliberately kept distinct even when titles overlap in industry use (e.g., Backend vs. Full-Stack, Cloud vs. DevOps vs. Platform). The point is to expose where the underlying work — not the title — is durable. Duplicates with the *same* underlying work but different vendors (e.g., Salesforce Developer vs Apex Developer) are kept only when the hiring market treats them as separate filters.

The full role list is generated from a single source of truth, [scripts/data_collection/generate_roles.py](scripts/data_collection/generate_roles.py), which emits [data/roles.csv](data/roles.csv) deterministically. Edit the script (not the CSV) to add, remove, or rescore roles — the cleaning step verifies that scores and tiers match the methodology and fails the build on drift.

## Step 2 — Per-role evaluation criteria

For every role, six dimensions are assessed before scoring:

1. **Market demand (current + 5-year trend)** — job postings on LinkedIn, Indeed, hired.com; Levels.fyi reqs; BLS occupational outlook (2024–34); McKinsey/Gartner cluster forecasts.
2. **Salary range (junior to senior)** — Levels.fyi median + 90th percentile; H1B disclosures (LCA database); Glassdoor and Otta ranges. US senior-IC focus.
3. **Risk of automation** — qualitative, calibrated against 2024–26 capability data: GitHub Copilot impact studies, Anthropic/Stripe internal usage data, Cursor/Devin capability benchmarks, McKinsey 2025 generative-AI workforce study.
4. **Skill complexity / barrier to entry** — bootcamp-to-senior ramp time, prerequisite credentials, cross-disciplinary requirements.
5. **Dependency on human judgment vs. repetitive tasks** — used directly in calibrating automation resistance.
6. **Long-term stability (5–10 years)** — indirectly captured by the four scoring axes.

Of these six, four feed directly into the score (below). Salary and judgment-vs-repetition are inputs to the qualitative analysis but are not separate axes — salary is reported alongside the score, and judgment-vs-repetition is folded into automation resistance.

## Step 3 — The Career Safety Score

Each role is scored 1–10 on four axes, then weighted and normalized to 0–100.

| Axis | What it measures | Weight |
| --- | --- | --- |
| **Demand** | 5–10 year trajectory of job-posting volume + organizational headcount. 10 = strongly rising, 5 = flat, 1 = collapsing. | 30% |
| **Automation Resistance** | Inverse of AI displacement risk. 10 = AI augments and the work is deeply human; 1 = AI replaces wholesale. | 35% |
| **Skill Depth** | Time and effort to reach senior. 10 = decade of compounding; 1 = months. Higher depth = higher moat. | 15% |
| **Strategic Importance** | How mission-critical the role is to org outcomes. 10 = company-defining; 1 = operationally necessary, organizationally peripheral. | 20% |

**Why these weights:**

- **Automation resistance carries the most weight (35%)** because it dominates the 5–10 year window. A high-demand role that AI fully automates is not safe.
- **Demand is second (30%)** because it sets the absolute floor on opportunity. Even an automation-resistant role with no demand is a dead end.
- **Strategic importance (20%)** captures whether the role survives cost-cutting cycles. Roles tied to revenue or risk survive recessions; roles tied to "nice-to-have" output do not.
- **Skill depth (15%)** is the smallest weight because depth is a *moat*, not a *driver* — it amplifies the other three but doesn't substitute for them.

### The formula

```text
score_raw = 0.30·Demand + 0.35·AutoResist + 0.15·SkillDepth + 0.20·StrategicImportance
score_100 = round(score_raw × 10)
```

### Worked example: Platform Engineer

- Demand = 9 (strongest 2026 infra-hiring trend)
- Automation Resistance = 8 (AI assists but doesn't own internal platforms)
- Skill Depth = 9 (cross-cutting K8s + IaC + IDP + DX + security baseline)
- Strategic Importance = 9 (platform velocity = engineering velocity)

```text
0.30·9 + 0.35·8 + 0.15·9 + 0.20·9
= 2.70 + 2.80 + 1.35 + 1.80
= 8.65
× 10 = 87
```

→ **Fortress tier.**

## Step 4 — Ranking

Roles are ranked by total score, descending. Ties are common (multiple roles at 87, multiple at 62) and are reported as tied — they reflect genuine equivalence on this rubric, not measurement noise.

## Step 5 — Tier interpretation

The tier cutoffs are calibrated to the curated `data/roles.csv` distribution and live in [scripts/analysis/_common.py](scripts/analysis/_common.py) — the cleaning step recomputes scores from the four axes and verifies tier assignments match.

| Tier | Score | Meaning |
| --- | --- | --- |
| **Fortress** | 83–100 | Build a career here without hedging. Demand and automation resistance both strong. |
| **Safe** | 70–82 | Senior path is durable. Junior path is harder than it was in 2020. |
| **Stable** | 58–69 | Specialize within the role or get exposed. Generalist track is the soft spot. |
| **Exposed** | 41–57 | Plan an adjacent move within 2–3 years. Headcount compresses, salaries plateau. |
| **At risk** | ≤40 | Plan a transition. Headcount shrinks every year through 2030. |

Across the 1,000-role dataset the tiers fall: Fortress 79, Safe 315, Stable 329, Exposed 223, At risk 54. The Stable + Exposed bands together hold 55% of all software/AI job titles — the "specialize or compress" middle is where most career decisions actually sit.

## Sources

Inputs are directional, not survey-grade. The goal is a defensible frame, not a published index. Every URL below was verified during the April 2026 research pass; for a per-claim citation map, see [INSIGHTS.md](INSIGHTS.md).

### Government / official statistics

- [BLS Occupational Outlook Handbook — Software Developers, QA Analysts, Testers](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm) (2024–34: +15%, ~129,200 openings/yr)
- [BLS Employment Projections 2024–34 release](https://www.bls.gov/news.release/pdf/ecopro.pdf)
- [BLS Industry & Occupational Projections Overview 2024–34](https://www.bls.gov/opub/mlr/2026/article/industry-and-occupational-employment-projections-overview.htm)
- BLS Information Security Analysts (cited via OOH; +32% 2024–34)

### Cybersecurity workforce

- [ISC2 2025 Cybersecurity Workforce Study](https://www.isc2.org/Insights/2025/12/2025-ISC2-Cybersecurity-Workforce-Study) (4.8M global gap; 59% critical skill shortage; AI/ML #1 skill gap)
- [DeepStrike — Cybersecurity Skills Gap analysis](https://deepstrike.io/blog/cybersecurity-skills-gap)
- [Programs.com — Cybersecurity workforce stats](https://programs.com/resources/cybersecurity-talent-shortage-stats/)

### Developer survey / AI adoption

- [Stack Overflow 2025 Developer Survey — AI section](https://survey.stackoverflow.co/2025/ai) (84% AI use; 51% daily; 29% trust)
- [Stack Overflow blog — 2025 results summary](https://stackoverflow.blog/2025/12/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/)
- [Stack Overflow — AI vs Gen Z (junior dev impact)](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/)

### Compensation

- [Levels.fyi — ML Engineer compensation](https://www.levels.fyi/t/software-engineer/title/machine-learning-engineer) (median $264K; FAANG breakdown)
- [Levels.fyi — ML/AI Software Engineer focus](https://www.levels.fyi/t/software-engineer/focus/ml-ai)
- [Acceler8 Talent — AI Engineer Salary 2025–2026](https://www.acceler8talent.com/resources/blog/ai-engineer--salary---market-rates-2025-2026/)
- [KORE1 — AI Engineer Salary Guide 2026](https://www.kore1.com/ai-engineer-salary-guide/)
- [KORE1 — ML Engineer Salary Guide 2026](https://www.kore1.com/ml-engineer-salary-guide/)
- [KORE1 — Cloud Engineer Salary Guide 2026](https://www.kore1.com/cloud-engineer-salary-guide-2026/)
- [Second Talent — Freelance Data Engineer rate card 2026](https://www.secondtalent.com/resources/freelance-data-engineer-hourly-rate-us/)
- [Glassdoor — Agentic AI Engineer salary](https://www.glassdoor.com/Salaries/agentic-ai-engineer-salary-SRCH_KO0,19.htm)

### Layoffs & hiring

- [Tom's Hardware — Q1 2026 tech layoffs analysis](https://www.tomshardware.com/tech-industry/tech-industry-lays-off-nearly-80-000-employees-in-the-first-quarter-of-2026-almost-50-percent-of-affected-positions-cut-due-to-ai)
- [KORE1 — Tech Layoffs 2026: Where Displaced Talent Is Going](https://www.kore1.com/tech-layoffs-2026/)
- [SF Standard — AI writes the code now (Stanford CPS analysis)](https://sfstandard.com/2026/02/19/ai-writes-code-now-s-left-software-engineers/)
- [Vucense — Q1 2026 layoffs / AI displacement](https://vucense.com/ai-intelligence/industry-business/tech-layoffs-q1-2026-ai-displacement-80000/)
- [Rezi — The Crisis of Entry-Level Labor](https://www.rezi.ai/posts/entry-level-jobs-and-ai-2026-report)

### Industry analyst forecasts

- [Gartner — Platform Engineering page](https://www.gartner.com/en/infrastructure-and-it-operations-leaders/topics/platform-engineering) (80% by 2026)
- [Pragmatic Engineer 2026 industry report](https://newsletter.pragmaticengineer.com/p/the-impact-of-ai-on-software-engineers-2026)
- [DEV Community — Platform Engineering 2026 numbers](https://dev.to/meena_nukala/platform-engineering-in-2026-the-numbers-behind-the-boom-and-why-its-transforming-devops-381l)
- [Platform Engineering — Becomes Mandatory](https://platformengineering.com/features/platform-engineering-becomes-mandatory-the-new-devops-standard/)

### Cluster-specific

- [Lenny's Newsletter — State of the Product Job Market](https://www.lennysnewsletter.com/p/state-of-the-product-job-market-in)
- [Aakash Gupta — State of AI Product Management (12K+ AI PM roles)](https://www.news.aakashg.com/p/the-state-of-ai-product-management)
- [NN/g — State of UX 2026](https://www.nngroup.com/articles/state-of-ux-2026/)
- [UX Design Institute — UX Job Market 2026](https://www.uxdesigninstitute.com/blog/the-ux-job-market-in-2026-2/)
- [Interview Query — Data Science Job Market](https://www.interviewquery.com/p/data-science-job-market-disappearing)
- [State of FinOps 2026](https://data.finops.org/)
- [Fortune — The Megamanager Era](https://fortune.com/2026/04/07/megamanager-era-how-many-direct-reports-ai-middle-management/)
- [Organimi — Span of Control 2026](https://www.organimi.com/span-of-control-in-2026/)
- [Fortune — Prompt Engineering Obsolete (May 2025)](https://fortune.com/2025/05/07/prompt-engineering-200k-six-figure-role-now-obsolete-thanks-to-ai/)
- [SolidAITech — Prompt Engineer Job Dead 2026](https://www.solidaitech.com/2026/04/prompt-engineer-job-dead-ai-careers.html)
- [QA Financial — AI replaces QA team and triggers $6M loss](https://qa-financial.com/ai-replaces-qa-team-and-triggers-6m-loss-do-banks-risk-losing-judgement/)
- [Robert Half — 2026 Technology Job Market](https://www.roberthalf.com/us/en/insights/research/data-reveals-which-technology-roles-are-in-highest-demand)

No proprietary data is used. All cited sources are public or publicly summarized. The numerical scores are the author's calibrated estimates — the value of the rubric is its consistency across roles, not the precision of any individual score.

## Re-running the analysis

Raw scoring data lives in [data/roles.csv](data/roles.csv), but it is generated — edit [scripts/data_collection/generate_roles.py](scripts/data_collection/generate_roles.py) and re-run the pipeline:

```bash
python3 scripts/data_collection/generate_roles.py   # rebuild data/roles.csv
python3 scripts/run_pipeline.py                     # collection → cleaning → analysis → charts → rasterize
```

The cleaning step recomputes every score from the four axes and fails the build if tiers drift from the published table. Charts are pure-Python SVG; rasterization to PNG (for the LaTeX PDF) uses `cairosvg`. The pipeline runs in under 5 seconds end-to-end with no other third-party dependencies.

## Limitations and caveats

1. **Geography**: US/EU bias. Mobile, Frontend, and QA Automation hold up longer in India, LATAM, and SEA markets than these scores suggest.
2. **Seniority**: Senior-IC framing throughout. Junior dynamics are worse than the scores indicate — AI compresses the bottom of every ladder hardest.
3. **Industry**: Tech-product / FAANG-adjacent assumed. Defense, healthcare, and finance shift the rankings — Mobile and QA Manual hold longer in regulated industries because of compliance overhead and slower technology adoption.
4. **Time horizon**: A 5–10 year window is long enough that a single foundation-model breakthrough or regulatory clamp could re-rank the list. Re-evaluate annually.
5. **Title vs. work**: Titles are noisy. "AI Engineer" can mean four different jobs depending on the company. The analysis tries to score the *underlying work*, but in some cases the title is the only handle available.
6. **Measurement asymmetry**: Some axes (demand, salary) have public data. Others (automation resistance, strategic importance) are calibrated qualitative estimates. Treat them as informed opinion, not measurement.

## What the score is *not*

- **Not a salary predictor.** Compensation is correlated with score but not determined by it. Specific employers, geographies, and timing matter more.
- **Not a fit assessment.** The safest career you hate is still a bad career.
- **Not a forecast.** It is a frame for thinking about defensibility — the underlying data shifts every year, and the rubric is designed to be re-run, not enshrined.

## When to re-score

Re-score yearly. If a single axis moves by more than 2 points for any role between annual reviews, publish a delta. The most likely 2027 movers (in the author's view): AI Application Engineer (Demand → 8 from 10 as the title consolidates), Frontend Engineer (Demand → 5 from 6 if the trajectory holds), Security (no movement expected; Fortress tier is structural).
