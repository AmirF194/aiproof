# Methodology

The scoring rubric, axis definitions, weights, sources, and limitations behind the rankings in [README.md](README.md) and [REPORT.md](REPORT.md).

## Step 1 — Role identification

The 36 roles in [data/roles.csv](data/roles.csv) cover every distinct, salaried function found in modern software organizations of 50+ engineers. Roles are grouped into 8 categories:

| Category | Roles | Rationale |
| --- | --- | --- |
| Engineering Leadership | 2 | Tech Lead and EM tracks — they win or lose together. |
| Security | 4 | Distinct subdomains: general, AppSec, Cloud, Offensive. |
| Data & AI | 7 | Bimodal — splits sharply between builders and consumers. |
| Platform & Infrastructure | 4 | Platform/SRE/DevOps/Cloud are the dominant infra titles. |
| Engineering (core IC) | 6 | Backend, Frontend, Full-Stack, iOS, Android, Systems, Embedded. |
| Quality & Testing | 3 | Manual, Automation, SDET — three distinct curves. |
| Product & Design | 5 | TPM, PM, UX, Product Designer, UI Designer. |
| Specialized & Emerging | 3 | Solutions Architect, DX, Prompt Engineer. |

Roles are deliberately kept distinct even when titles overlap in industry use (e.g., Backend vs. Full-Stack, Cloud vs. DevOps vs. Platform). The point is to expose where the underlying work — not the title — is durable.

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

| Tier | Score | Meaning |
| --- | --- | --- |
| **Fortress** | 85–100 | Build a career here without hedging. Demand and automation resistance both strong. |
| **Safe** | 70–84 | Senior path is durable. Junior path is harder than it was in 2020. |
| **Stable** | 55–69 | Specialize within the role or get exposed. Generalist track is the soft spot. |
| **Exposed** | 40–54 | Plan an adjacent move within 2–3 years. Headcount compresses, salaries plateau. |
| **At risk** | <40 | Plan a transition. Headcount shrinks every year through 2030. |

## Sources

Inputs are directional, not survey-grade. The goal is a defensible frame, not a published index.

- **Salary**: Levels.fyi (2025 dataset), H1B LCA database (2024–25), Glassdoor, Otta, Hired.com.
- **Demand**: LinkedIn Workforce Reports (Q1–Q4 2025), Indeed Hiring Lab, BLS Occupational Outlook 2024–34, GitHub Octoverse 2025.
- **Automation impact**: McKinsey "The economic potential of generative AI" 2025 update, Gartner AI-impact estimates 2025, Stack Overflow Developer Survey 2025 AI section, GitHub Copilot productivity studies, Anthropic/Stripe published usage data, internal Cursor/Devin benchmarking.
- **Cluster trends**: Pragmatic Engineer 2026 industry report, State of DevOps 2025, State of AI 2025 (Benaich/Hogarth), CNCF surveys, ESG/Gartner cybersecurity spend forecasts.

No proprietary data is used. All cited sources are public or publicly summarized. The numerical scores are the author's calibrated estimates — the value of the rubric is its consistency across roles, not the precision of any individual score.

## Re-running the analysis

Raw scoring data is in [data/roles.csv](data/roles.csv) — every score and weight is exposed so you can re-weight if you disagree with the methodology. To reproduce charts after editing data:

```bash
python3 scripts/generate_charts.py
```

No third-party dependencies. Pure-Python SVG generation; runs in <1 second.

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
