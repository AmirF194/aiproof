# Deep Insights: What 2025–2026 Data Actually Shows

This file is the research layer behind [README.md](README.md) and [REPORT.md](REPORT.md). Every number here is sourced. Use it to pressure-test the scores in [data/roles.csv](data/roles.csv) (1,000 roles across 8 categories — see [REPORT.md](REPORT.md) for the per-category top-and-bottom; full ranking in [data/processed/role_ranking.csv](data/processed/role_ranking.csv)).

The headline: **the labor market for software has already split into three economies — and the split is wider than the public narrative suggests.** This file walks through the evidence cluster by cluster. The structural findings hold across the expanded 1,000-role dataset; the title-level fragmentation just makes the bifurcation more visible (the Fortress band is 79 of 1,000 roles, the At-risk tail is 54).

---

## 1. The aggregate picture is not the story. The split is.

Two facts have to be held at the same time:

- **BLS (2024–34 projections, published Sept 2025)**: software developer / QA / tester employment grows **+15%** over the decade — *five times the all-occupations average* — with ~129,200 openings per year. Information security analysts grow **+32%**. ([BLS OOH — Software Developers](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm), [BLS Employment Projections 2024–34](https://www.bls.gov/news.release/pdf/ecopro.pdf))
- **Q1 2026 layoffs**: ~78,000–90,000 tech jobs cut globally; **Challenger, Gray & Christmas** logged 52,050 tech-sector announcements, **+40% vs Q1 2025**. ~48% of cuts cite AI as a primary driver. ([Tom's Hardware](https://www.tomshardware.com/tech-industry/tech-industry-lays-off-nearly-80-000-employees-in-the-first-quarter-of-2026-almost-50-percent-of-affected-positions-cut-due-to-ai), [KORE1](https://www.kore1.com/tech-layoffs-2026/))

These are not contradictions. They describe a market where **demand for the senior tier is rising while the junior tier is being repriced and the middle is being compressed**. The BLS aggregate hides the bifurcation. Every score in this analysis assumes the bifurcation, not the headline.

The clearest single statistic supporting the split: **employment for software developers aged 22–25 has fallen ~20% from the late-2022 peak** (Stanford / SF Standard analysis of CPS data), while **senior software engineer comp is +12–18% YoY** at surviving companies (Goldman Sachs comp analysis cited by KORE1). ([SF Standard](https://sfstandard.com/2026/02/19/ai-writes-code-now-s-left-software-engineers/), [KORE1](https://www.kore1.com/tech-layoffs-2026/))

---

## 2. AI coding tools: the throughput multiplier that compresses the middle

The Stack Overflow 2025 Developer Survey (published Dec 2025, ~49,000 respondents) is the cleanest dataset on developer AI use:

- **84%** are using or planning to use AI tools (up from 76% in 2024)
- **51%** of professional developers use them daily
- **Only 29%** trust AI output (down from ~40% in 2024)
- **45%** cite "debugging AI-generated code is time-consuming" as a key frustration

([Stack Overflow Survey 2025 — AI section](https://survey.stackoverflow.co/2025/ai), [Stack Overflow blog summary](https://stackoverflow.blog/2025/12/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/))

Productivity numbers triangulate to a consistent estimate: developers using AI tools produce **40–55% more code per sprint** at comparable quality (multiple sources, summarized in the Vucense / Tom's Hardware coverage). That implies **a 10-engineer team with AI matches the 2022 output of a 15-engineer team without it**.

This is the mechanical basis for the "compressors" in the README:

| Role | Why it compresses | Source signal |
| --- | --- | --- |
| Frontend Engineer | UI scaffolding is the most AI-native task; postings down sharply | Frontend share of postings now <20%, dropping; "largest decline among engineering roles" |
| Full-Stack Engineer | Most generalist shape, most exposed to throughput multiplier | 72% of tech leaders plan to *reduce* entry-level dev hiring (early-2025 survey) |
| QA Automation | Self-healing E2E + AI test gen mature enough | Multiple confirmed displacement cases |
| Junior backend (CRUD) | AI does the easy work that used to train juniors | 22–25 yo developer employment –20% |

Sources: [SF Standard](https://sfstandard.com/2026/02/19/ai-writes-code-now-s-left-software-engineers/), [The Front-End Company stats](https://www.thefrontendcompany.com/posts/frontend-development-statistics), [Pragmatic Engineer 2026](https://newsletter.pragmaticengineer.com/p/the-impact-of-ai-on-software-engineers-2026), [Markaicode coverage of 500-leader survey](https://markaicode.com/ai-vs-developers-coding-jobs-2026/).

---

## 3. Security: the single most-undervalued category

The ISC2 2025 Cybersecurity Workforce Study (published Dec 2025) is the canonical dataset:

- Global cybersecurity workforce gap: **4.8 million** unfilled positions (US share: ~700,000)
- **59% of organizations report critical or significant skills shortages** in their security teams — *up from 44% in 2024*. This is one of the largest YoY skill-gap moves in any tech category.
- AI/ML is now the **#1 cited skill need** in security (41%), with cloud security at **#2 (30%)**
- **88%** of organizations had at least one significant cybersecurity consequence from skills shortages; 69% had more than one
- BLS projects **+32% growth** for information security analysts 2024–34

([ISC2 2025 Workforce Study](https://www.isc2.org/Insights/2025/12/2025-ISC2-Cybersecurity-Workforce-Study), [BLS OOH — Information Security](https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm), [DeepStrike](https://deepstrike.io/blog/cybersecurity-skills-gap), [Programs.com](https://programs.com/resources/cybersecurity-talent-shortage-stats/))

**Why this matters for the score**: security is the *only* cluster in this analysis where the demand-vs-supply gap *widened* from 2024 to 2025. The scoring puts every security role in the top quartile (84–92), which the data more than supports.

The two intra-security dynamics worth pulling out:

- **AI-augmented attackers** are pushing AppSec and detection-engineering work *up*, not down. The shifted bottleneck is "review AI-written code at scale," and AppSec engineers own that pipeline.
- **Cloud security is the single fastest-growing security subniche**, driven by the ISC2 finding that cloud is the #2 skill gap and by sustained cloud-spend growth. The bilingual "platform engineer who owns IAM" is the highest-leverage shape.

---

## 4. Data & AI: the cluster is bimodal, and the gap is widening

Two roles with the word "data" in the title now sit on opposite tiers:

- **Data Engineer (82)**: senior freelance rates rose from $105/hr (2020) to $165/hr (Q1 2026); **lakehouse specialists (Iceberg / Hudi / Delta) command +$60/hr premium**; SQL, ETL, Snowflake, dbt all up double-digit percentage points YoY in postings ([Second Talent rate card](https://www.secondtalent.com/resources/freelance-data-engineer-hourly-rate-us/), [Data Engineering Jobs 2026 trends](https://dataengineeringjobs.co.uk/career-advice/data-engineering-hiring-trends-2026-what-to-watch-out-for-for-job-seekers-recruiters-))
- **Data Analyst (33)**: BI + LLM SQL covers ~60% of operational requests; postings declining; entry-tier first to compress

Inside ML, Levels.fyi (April 2026) shows the tier structure clearly:

| Company | Median TC (ML Engineer) |
| --- | --- |
| LinkedIn | $450K |
| Meta | $430K |
| Apple | $335K |
| Google | $290K |
| Nvidia | $267K |
| Amazon | $265K |
| **Levels.fyi median across companies** | **$264K** |

([Levels.fyi — ML Engineer](https://www.levels.fyi/t/software-engineer/title/machine-learning-engineer), [Meta](https://www.levels.fyi/companies/meta/salaries/software-engineer/title/machine-learning-engineer), [Google](https://www.levels.fyi/companies/google/salaries/software-engineer/title/machine-learning-engineer))

The *fastest-growing* AI subcategory is **agentic AI / agent systems engineering**:

- Acceler8 / KORE1 / Glassdoor triangulate to **$155K–$265K base, $400K+ TC for top performers, $500K+ at frontier labs**
- AI engineer base salaries **+9.2% in 2025** (the "Agentic Surge"), **+7% in 2026**
- Gartner forecast: **40% of enterprise applications will include task-specific AI agents by end of 2026** (up from <5% in 2025)
- Some senior agentic roles command **+30–50% premium** over generic backend

([KORE1 hiring guide](https://www.kore1.com/hire-agentic-ai-engineers-2026/), [Acceler8](https://www.acceler8talent.com/resources/blog/ai-engineer--salary---market-rates-2025-2026/), [Glassdoor](https://www.glassdoor.com/Salaries/agentic-ai-engineer-salary-SRCH_KO0,19.htm))

This is a leading indicator that the "AI Application Engineer (73)" tier could rise toward Fortress short-term — but the long-term consolidation thesis (this title becomes "backend engineer who knows LLMs" by ~2029) holds, which is why the score does not over-correct.

The **Data Scientist (52)** verdict is the most data-driven downgrade. Job-postings analysis shows hiring *for senior data scientists* still growing while *junior data-science postings have collapsed*; the "DS" bucket is being absorbed up (into ML Eng) and down (into LLM-augmented analytics). The defensible niche is causal inference and experimentation at companies with mature A/B platforms. ([Interview Query](https://www.interviewquery.com/p/data-science-job-market-disappearing), [Towards Data Science](https://towardsdatascience.com/is-the-ai-and-data-job-market-dead/))

---

## 5. Platform / SRE / DevOps: the structural infra winner

Gartner's platform-engineering forecast is the single most cited number in the 2025–26 infra discourse:

- **80% of large software engineering organizations will have platform engineering teams by 2026** — up from **45% in 2022**. ([Gartner — Platform Engineering](https://www.gartner.com/en/infrastructure-and-it-operations-leaders/topics/platform-engineering), [DEV Community summary](https://dev.to/meena_nukala/platform-engineering-in-2026-the-numbers-behind-the-boom-and-why-its-transforming-devops-381l))
- **55% of organizations have already adopted platform engineering** as of 2025
- **92% of CIOs are planning AI integrations into their platforms**
- Gartner projects **90% of enterprise software engineers will use AI code assistants by 2028** (up from <14% in early 2024)

The implication for scoring: Platform Engineer (87) is the cluster's anchor; SRE (84) and DevOps (72) are the two halves of the "operate vs build" split. The DevOps title is in slow decline as work bifurcates — engineers with the title still earn well but the rebrand path is short.

**FinOps engineer** is the rising sub-niche the original analysis only mentioned in passing. 2026 data:

- Average TC ~$128K (US); senior tiers $175K+ at hyperscalers
- AI cost management is the **single most-desired FinOps skill set** across orgs of all sizes
- Industry-wide finding: **30–50% of GPU resources are wasted through over-provisioning** — a rate that creates direct pressure to staff this function

([State of FinOps 2026](https://data.finops.org/), [KORE1 cloud salary guide](https://www.kore1.com/cloud-engineer-salary-guide-2026/), [ZipRecruiter](https://www.ziprecruiter.com/Salaries/Cloud-Finops-Salary))

If the rubric were re-run with FinOps as a separate role, it would land in the high-Safe / low-Fortress range (78–82) because demand is rising fast but skill depth is moderate.

---

## 6. The "megamanager" effect and why EM still scores Fortress

Fortune (April 2026) reports **Meta's applied-AI engineering division running a 50:1 IC-to-manager ratio** — roughly double the historical functional limit. The pattern is broader: Pragmatic Engineer's 2026 industry report and DX's Q1 2026 study both find **rising span of control across most engineering orgs as AI absorbs administrative load**.

([Fortune — Megamanager era](https://fortune.com/2026/04/07/megamanager-era-how-many-direct-reports-ai-middle-management/), [Organimi — Span of Control 2026](https://www.organimi.com/span-of-control-in-2026/), [Pragmatic Engineer 2026](https://newsletter.pragmaticengineer.com/p/the-impact-of-ai-on-software-engineers-2026))

This is the mechanism behind the EM (83) score: **fewer managers per IC, but more ICs in absolute terms — so EM headcount is roughly flat while the role becomes higher-leverage**. The risk note in REPORT.md is real: first-line EM at small companies is the exposed tier.

The consequence for career planning: a Staff Engineer (94) and an EM (83) are the two durable senior tracks, but the *shape* of EM work is changing — coaching and mentorship are the first casualties of high-span-of-control orgs, which inverts the role from "people developer" to "throughput optimizer."

---

## 7. Frontend, Mobile, QA: the three compressors with different curves

**Frontend.** The clearest displacement evidence in the dataset:

- Frontend's share of all IT postings has dropped from ~20% to <20% and is *still falling* ([TheFrontendCompany](https://www.thefrontendcompany.com/posts/frontend-development-statistics))
- 72% of tech leaders surveyed early-2025 plan to *reduce* entry-level developer hiring; **64% are increasing AI tooling investment** — frontend is the single most-affected role
- "Vibe coding" tools (v0, Bolt, Lovable, Replit) reliably produce production-ready React from prompts

The defensible escapes (design systems, a11y, performance, DX) are validated by data — but they require taste or platform depth that AI cannot synthesize.

**Mobile.** Less compressed than the README's score suggests in absolute terms, *but* with two twists:

- **Hybrid native + cross-platform is now the dominant org pattern**: performance-critical features stay native, shared logic moves to Flutter / RN / KMP. Engineers who can do both command premium comp.
- Stack Overflow 2024 data: Flutter is the most-used cross-platform framework at 46% adoption (vs RN 35%); **150,000+ apps on Flutter**.
- Senior Flutter / RN compensation: **$135K–$180K** (Flutter) and **$125K–$160K** (RN) — close to native-iOS senior bands.

Implication: the score (62 for both iOS and Android) holds, but the *signal* is "specialize in cross-platform internals" more than "go deeper into native-only."

**QA.** The displacement story is real but more nuanced than the headlines suggest:

- WEF Future of Jobs 2025: **41% of employers plan workforce reductions** specifically citing AI automation. Manual QA is in this bucket.
- Tesla counterexample: QA team **grew from 260 to 390** between 2020 and 2025 — but the *composition shifted* from manual testers toward AI-testing specialists, safety validation engineers, and adversarial testers.
- Gartner originally projected 80% of testing automated by 2025; the **revised projection is 60–70% of routine testing automated by 2030**, with **demand for skilled QA professionals up 25%** because software complexity is rising.

([WEF Future of Jobs 2025 cited via TestRigor](https://testrigor.com/blog/will-ai-replace-testers/), [QA Financial — bank case study](https://qa-financial.com/ai-replaces-qa-team-and-triggers-6m-loss-do-banks-risk-losing-judgement/))

The bank case study is worth flagging: a financial firm replaced a 12-person QA team with AI to save $1.2M and **lost $6M in orders** because an AI agent hallucinated a discount code that zeroed out the catalog. The implication is structural, not anecdotal: as AI generates more code, the *cost of QA failure* rises, which keeps senior-tier QA / AI-eval roles defensible even as manual QA collapses.

The clear winning transition: Manual QA → SDET → Backend or AI Eval. The losing path: stay in manual.

---

## 8. Product, Design, and the "AI fluency" floor

Product management hiring tells a counterintuitive story:

- **+53.6% above the 2023 bottom** in PM postings; total open PM roles ~6,000+ globally
- **AI PM hiring doubled in 2025** to ~12,000 new roles
- Senior PM postings up **+87% YoY**
- McKinsey: demand for AI fluency in job postings has grown **~7×** in two years, mostly in management and business roles
- **71% of business leaders** would prefer a less-experienced candidate with strong AI skills over a more-experienced candidate without them

([Lenny's Newsletter — State of PM Job Market](https://www.lennysnewsletter.com/p/state-of-the-product-job-market-in), [Aakash Gupta — AI PM Salaries](https://www.news.aakashg.com/p/the-state-of-ai-product-management), [Product School — AI PM guide](https://productschool.com/blog/artificial-intelligence/guide-ai-product-manager))

This validates the PM (73) and TPM (79) scores and surfaces the actual differentiator: **AI fluency is now the floor across PM, design, and senior IC roles**. By 2027, "doesn't use AI tools effectively" will be a hiring red flag in essentially every role on this list. This is not a differentiator — it is table stakes.

**Design.** Nielsen Norman Group's State of UX 2026:

- 82% of design leaders say need for designers has stayed the same or increased; ~10–25% growth in many orgs
- **UX research is the highest-demand niche** in the design category — synthesis and interpretation are slowest to automate
- Junior UX roles are the most exposed: **500–800 applicants per posting** in some cases

UI Designer (40) and Product Designer (64) hold their tier. The 1,000-role expansion split out **Senior UX Researcher** (Safe, 75) and **Quantitative UX Researcher** (Safe, 71) as separate rows — both confirm that synthesis-and-interpretation work is where the design discipline holds value as visual production gets eaten.

([NN/g — State of UX 2026](https://www.nngroup.com/articles/state-of-ux-2026/), [UX Design Institute](https://www.uxdesigninstitute.com/blog/the-ux-job-market-in-2026-2/))

---

## 9. Prompt Engineer: the one role that has effectively disappeared

The clearest disappearance signal in the dataset:

- Indeed search volume for "prompt engineer" peaked at **144 per million** in April 2023; **plateaued at 20–30 per million** through 2025–26
- "By early 2026, the Prompt Engineer as a standalone job title is effectively gone at any company running frontier models" ([SolidAITech](https://www.solidaitech.com/2026/04/prompt-engineer-job-dead-ai-careers.html), [Fortune coverage](https://fortune.com/2025/05/07/prompt-engineering-200k-six-figure-role-now-obsolete-thanks-to-ai/))
- Automated Prompt Engineering frameworks (DSPy, etc.) are now standard infrastructure

The score (27) captures this. The skill is real and absorbed into AI Application Engineer / ML Eng work — the *job title* is not durable.

---

## 10. What to update in the rubric for 2027

If this analysis is re-run in early 2027, the most likely score moves on the author's view:

| Role | Current | Probable 2027 | Reason |
| --- | --- | --- | --- |
| AI Application Engineer | 73 | 75–78 | Agentic AI is structural, not a fad — but the title may be on its way to consolidating |
| Frontend Engineer | 52 | 45–48 | Postings trajectory plus tooling maturity both point down |
| Data Analyst | 33 | 25–30 | LLM-NL-to-SQL eats the role faster than the rubric assumed |
| FinOps Engineer (split out) | n/a | 78–82 | Currently absorbed into Cloud Engineer; warrants its own row |
| UX Researcher (split out) | 67 | 75–78 | Rising; design researcher path is uniquely defensible |
| Engineering Manager | 83 | 80–82 | Megamanager pattern reduces total EM headcount even as role value rises |
| AI Research Engineer | 89 | 85–88 | Comp normalization possible if frontier saturates |

These are *projections of how the data is moving*, not predictions. Re-score yearly; if any axis moves more than 2 points for any role, publish a delta.

---

## How to read this file

- The numbers in the role tables ([data/roles.csv](data/roles.csv)) are the author's calibrated estimates based on the data above. The full 1,000-role roster is generated by [scripts/data_collection/generate_roles.py](scripts/data_collection/generate_roles.py).
- The *value* of this analysis is the **rubric consistency**, not the precision of any individual score. If you disagree with a specific score, edit the generator and re-run the pipeline (`python3 scripts/run_pipeline.py`) — the cleaning step verifies that the published tier matches the rubric.
- The data dates fast. The most decay-prone numbers in this file are the layoff totals (Q1 2026), the Indeed search rates, and any specific salary band. The *structural* findings (skill-gap directions, span-of-control trends, BLS 10-year projections, the bifurcation pattern) decay much more slowly.

If a single foundation-model breakthrough or a major regulatory event reshuffles the picture, the structure of this rubric is designed to be re-run, not enshrined.
