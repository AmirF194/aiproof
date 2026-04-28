# AI Impact Analysis

How AI is reshaping each role over the 2026–35 window. The frame: AI is not one effect — it splits roles into three groups (multipliers, compressors, replacements) and a fourth (untouched), and the group a role lands in determines its career safety.

The bucket assignments here are computed by [`scripts/analysis/trend_analysis.py`](../scripts/analysis/trend_analysis.py) from postings deltas and AI-mention deltas in the simulated postings dataset; the qualitative narratives are calibrated to public 2025–26 data (Stack Overflow Developer Survey 2025, ISC2 2025 Workforce Study, Gartner forecasts, Q1 2026 layoff data). Sources: [INSIGHTS.md](../INSIGHTS.md).

---

## TL;DR — The four groups

| Group | What AI does to the role | Headcount trajectory | Examples |
| --- | --- | --- | --- |
| **Multipliers** | One engineer does 2–3× the work of a 2022 engineer. Headcount **flat or up**. | flat / up | Backend (senior), Platform, ML Eng, Security, Data Eng |
| **Compressors** | 1.5 engineers do the work of 3. Headcount **down 20–40% by 2030**. | down 20–40% | Frontend, Full-Stack, generic Backend (CRUD), QA Automation, Analytics Eng |
| **Replacements** | AI does most of the role's work. Headcount **down 50%+**. | down 50%+ | Manual QA, Data Analyst, UI Designer, Prompt Eng |
| **Untouched** | AI augments at the margin but doesn't shape the role. | flat | Embedded, Systems / Low-level, Red Team |

This file walks through each group with the underlying mechanism, the data signals, and the role-by-role implications.

---

## 1. Multipliers — AI raises throughput, headcount holds or grows

### Mechanism

For roles whose value comes from **judgment, system design, ownership, and cross-team coordination**, AI removes the mechanical-but-necessary work (boilerplate, scaffolding, drafting, refactoring) and leaves more bandwidth for the high-leverage work that *only* a senior engineer can do.

Stack Overflow Developer Survey 2025 (≈49K respondents):
- **84%** of developers use or plan to use AI tools (up from 76% in 2024)
- **51%** of professional developers use them daily
- **Only 29%** trust AI output (down from ≈40% in 2024)
- Productivity uplift: **+40–55% code per sprint** at comparable quality (Vucense / Tom's Hardware aggregate)

That means the 2022 work of 15 engineers can be done by 10 engineers in 2026 — but the 10 engineers who survive are the ones who own outcomes the AI can't carry.

### Roles in this group

| Role | Score | What AI multiplies | What stays human |
| --- | --- | --- | --- |
| Staff Engineer / Tech Lead | 94 | Code review at scale, RFC drafts, architecture sketches | Trade-off decisions, cross-team alignment, mentorship |
| Engineering Manager | 83 | 1:1 prep, performance writeups, planning docs | Hiring decisions, retention, conflict resolution |
| Security Engineer | 92 | Triage, log correlation, IR drafts | Threat modeling judgment, incident command, regulatory negotiation |
| AppSec Engineer | 87 | SAST/DAST triage, code review at scale | Threat modeling, vulnerability prioritization |
| Cloud Security Engineer | 87 | CSPM finding triage, IaC linting | Cross-cloud architecture decisions, IAM design |
| ML Engineer | 87 | Boilerplate, eval-script generation, refactoring | Model architecture, training-data decisions, eval design |
| MLOps Engineer | 87 | Pipeline scaffolding, infra IaC | Eval framework design, on-call ownership |
| Platform Engineer | 87 | Scaffolding for IDP modules, docs generation | API design, abstraction trade-offs, internal product taste |
| SRE | 84 | RCA drafting, dashboard generation, runbook updates | Pager ownership, capacity decisions, postmortem judgment |
| Data Engineer | 82 | dbt model drafting, SQL generation | Data modeling decisions, SLA-bearing pipeline ownership |
| Backend Engineer (senior, systems-track) | 72 | API scaffolding, refactoring, docs | System design, distributed-systems ownership |

### Why this group wins

- The **adversarial** subset (Security) wins extra hard because attackers also have AI. Defenders are net-up: the work expands at least as fast as AI helps.
- The **on-call** subset (SRE, MLOps, Platform) wins because AI assists at incident response but cannot own a pager.
- The **judgment** subset (Staff Eng, EM) wins because the work *is* judgment.

---

## 2. Compressors — 1.5 engineers do the work of 3

### Mechanism

For roles whose work is **mid-tier generalist** — assembling components, writing CRUD endpoints, building dashboards, scripting tests — AI tools produce 60–80% of the artifact and a human reviews it. The throughput gain is real, but the human time spent per artifact drops by ~40%, which compresses headcount proportionally.

The compression *isn't fired engineers in 2026*. It's that the 30 mid-level openings the company would have posted in 2024 become 18 openings in 2027. The team grows slower than it would have.

Q1 2026 layoff data (Challenger, Gray & Christmas):
- **52,050** US tech layoffs announced (+40% YoY)
- **~48% AI-attributed**
- **31% of cuts** in software engineering, biased toward "mid-tier generalist" titles

### Roles in this group

| Role | Score | What AI compresses | What survives |
| --- | --- | --- | --- |
| Backend Engineer (CRUD-heavy) | 72 | API scaffolding, glue code, internal tools | Distributed-systems work, payments, search, real-time |
| Full-Stack Engineer | 62 | Component + API scaffolding | Specialists ("full-stack with deep auth," "with deep search") |
| Frontend Engineer | 52 | Component assembly from designs, layout, styling | Design Systems, a11y, performance, DX |
| QA Automation | 40 | Selenium/Cypress/Playwright script writing | SDET, AI-eval QA |
| Analytics Engineer | 57 | SQL writing, simple dbt models | Senior analytics eng who own warehouse architecture |
| Cloud Engineer | 67 | IaC scaffolding, vendor-cert work | FinOps, multi-cloud cost engineering, security-paired |
| iOS / Android Engineer | 62 | UI scaffolding from design | Cross-platform internals, native performance, system-level |
| Product Designer | 64 | Visual exploration, mockup variants | Design Engineer (codes own components), interaction design |
| UX Designer (the design half) | 67 (bundled) | IA, wireframes | UX Researcher half (study design, synthesis) |

### Where the compressed roles end up

The Stable / Exposed mid-tier doesn't *disappear* — it consolidates upward. Engineers in this group either:

1. **Become specialists.** Pick a domain (payments, search, real-time, ML systems), a cross-cutting skill (perf, a11y, security), or a platform (deep K8s, deep iOS, deep Postgres internals). The "specialist" version of the same title scores 1–2 tiers higher.
2. **Become senior at scale.** AI raises the value of senior IC work because it lowers the cost of mid-level work. The path to senior is *longer* than 2020 (less time on training-ground tasks AI absorbs) but the senior tier is where the comp lives.
3. **Move to a Multiplier role.** Backend → ML systems. Frontend → DX. SDET → backend. Cloud → Platform.

The trap: stay generalist, hope for the best. The 2027 hiring market does not reward this.

---

## 3. Replacements — AI does most of the role's work

### Mechanism

For roles where the work is **highly structured, schema-bound, and AI-native**, current 2026 model capability is good enough to deliver 60–80% of typical requests with no human review and the rest with light human review.

These roles do not vanish overnight. They shrink mechanically: the **headcount per company drops 50%+ by 2030**, the surviving roles concentrate at companies where the failure cost is high (regulated industries, enterprise contracts), and entry-level postings collapse first.

### Roles in this group

| Role | Score | What AI replaces | What residual demand looks like |
| --- | --- | --- | --- |
| QA Manual | 20 | Test plan execution, bug reproduction, regression sweeps | Senior compliance / safety QA at regulated companies (banks, healthcare, defense) |
| Data Analyst | 33 | Ad-hoc SQL, dashboard generation, business-question answering | Senior analyst at orgs without analytics-eng coverage; specialty roles in growth, finance |
| UI Designer | 40 | Visual exploration, mockup variants, color/type/layout | Senior designers in animation/motion/interaction prototyping |
| Prompt Engineer | 27 | Prompt tuning, eval scripting | Effectively zero — title is gone at any company running frontier models |

### Cautionary case studies

- A financial firm replaced a 12-person QA team with an AI test pipeline to save $1.2M and **lost $6M in orders** when an AI agent hallucinated a discount code that zeroed out the catalog (QA Financial). *Implication: the cost of QA failure rises with AI-generated code, which keeps senior QA + AI-eval roles defensible even as manual QA collapses.*
- Tesla *grew* QA from **260 to 390 staff (2020 → 2025)** but the composition shifted to AI-testing specialists and safety-validation engineers, not manual testers.
- Stack Overflow 2025: **45%** of developers cite "debugging AI-generated code" as a top frustration — which is exactly the work surviving QA / AI-eval roles will own.

---

## 4. Untouched — AI doesn't shape the role much

### Mechanism

A small group of roles works on **systems AI cannot reason about reliably**: kernels, compilers, distributed-systems internals, hardware-software interfaces, novel exploitation chains. AI helps with auxiliary tasks (docs, glue code) but doesn't compress the core work.

### Roles in this group

| Role | Score | Why AI underperforms here |
| --- | --- | --- |
| Systems / Low-level Engineer | 81 | Reasoning about memory, concurrency, IRQs, lock-free data structures requires correctness arguments AI hallucinates. |
| Embedded Engineer | 74 | Hardware-software interfaces (DMA, peripherals, RTOS schedulers) need physical-system grounding. |
| Offensive Security / Red Team | 84 | Genuinely creative adversarial work; AI helps with recon, not exploitation chains. |
| AI Research Engineer | 89 | Frontier work *creates* the AI tools; can't be replaced by them. |

These roles are also small. The downside: smaller absolute headcount, fewer adjacent moves available if the specific niche shrinks (e.g., a particular hyperscaler de-emphasizes a chip family).

---

## 5. The bifurcation thesis

The single hardest fact to reconcile in the 2025–26 labor market:

- **BLS** projects **+15% software developer growth** through 2034 (5× the all-occupations average).
- **Q1 2026 layoffs** are up **40% YoY**, with ~48% AI-attributed.

Both are true. The reconciliation:

| Tier | Direction | Source signals |
| --- | --- | --- |
| **Senior** | rising | Goldman Sachs (cited via KORE1): senior software engineer comp +12–18% YoY at surviving cos. ISC2: 59% of orgs with critical security skill shortages, up from 44%. |
| **Junior** | repricing | Stanford / CPS: software developer employment for ages 22–25 down −20% from late-2022 peak. UK tech-grad roles −46% in 2024, −53% projected through 2026. |
| **Mid-tier generalist** | compressing | AI tooling produces +40–55% more code per sprint. Most layoffs target the mid-tier, not the senior IC, not the (already-not-being-hired) junior. |

Every score in this analysis assumes the bifurcation. The **At-risk and Exposed tiers are mostly mid-tier generalist roles**; the **Fortress tier is mostly judgment/adversary/production** work.

---

## 6. The skills floor that's now everywhere

By **2027**, "doesn't use AI tools effectively" will be a hiring red flag in essentially every role on this list — including PM, Designer, and Researcher. This is not a differentiator; it is **table stakes**.

McKinsey 2025 generative-AI workforce study: demand for AI fluency in job postings has grown **~7× in two years**. **71% of business leaders** say they prefer a less-experienced candidate with strong AI skills over a more-experienced one without.

What "AI fluency" means in 2026, by role:

| Role | What "AI-fluent" means |
| --- | --- |
| Backend / Frontend / Full-Stack | Daily Copilot/Cursor/Claude Code use; can review AI-generated code at speed |
| Platform / SRE / DevOps | Comfortable with AI-generated IaC; uses AI for RCA/runbooks |
| Security | Knows how attackers use AI; uses AI for triage at scale |
| ML / MLOps | Uses LLMs for eval generation, data labeling, training-data synthesis |
| Data / Analytics | Uses LLMs for SQL drafting, schema documentation, ad-hoc Q&A |
| Product Manager | Uses LLMs for spec drafting, customer-research synthesis, roadmap iteration |
| Designer | Uses AI design tools (v0, Galileo, Uizard) for exploration |
| Researcher | Uses LLMs for synthesis, transcript coding, literature review |

Roles that *don't* require AI fluency in 2026:
- Some QA Manual / Data Analyst / Prompt Eng roles where the entire workflow is being replaced by AI rather than amplified.

---

## 7. What the bucket-assignment script outputs

[`scripts/analysis/trend_analysis.py`](../scripts/analysis/trend_analysis.py) writes [`data/processed/trend_buckets.csv`](../data/processed/trend_buckets.csv) — the machine-readable bucket assignments for all 36 roles, derived from postings deltas and AI-mention deltas in the simulated dataset. The narrative buckets in this file (Multiplier / Compressor / Replacement / Untouched) are the editorial layer; the CSV is the data layer.

To regenerate after editing inputs:

```bash
python3 scripts/run_pipeline.py
```

The thresholds in `classify_trend()` are intentionally simple (postings 2-yr change + AI mention delta in pp) so the rule is auditable. They are not the only legitimate cut — re-weight in the script if you disagree.

---

## 8. The single sentence

> The senior tier is rising, the junior tier is being repriced, and the middle is being compressed. Every score in this analysis assumes that bifurcation.
