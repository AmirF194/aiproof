# Per-Role Analysis (2026–2035)

All 36 roles, grouped by category. Each entry covers the four scoring axes plus salary range, key dynamics, and risks. Scoring methodology in [METHODOLOGY.md](METHODOLOGY.md). Raw data in [data/roles.csv](data/roles.csv).

**Reading the score**: 0–100, where higher = more durable over the 5–10 year window. Tiers: Fortress (85+), Safe (70–84), Stable (55–69), Exposed (40–54), At risk (<40).

---

## Master ranking

| Rank | Role | Category | Score | Tier |
| --- | --- | --- | --- | --- |
| 1 | Staff Engineer / Tech Lead | Engineering Leadership | 94 | Fortress |
| 2 | Security Engineer | Security | 92 | Fortress |
| 3 | AI Research Engineer | Data & AI | 89 | Fortress |
| 4 | ML Engineer | Data & AI | 87 | Fortress |
| 4 | MLOps Engineer | Data & AI | 87 | Fortress |
| 4 | Platform Engineer | Platform & Infrastructure | 87 | Fortress |
| 4 | Application Security Engineer | Security | 87 | Fortress |
| 4 | Cloud Security Engineer | Security | 87 | Fortress |
| 9 | Site Reliability Engineer | Platform & Infrastructure | 84 | Fortress |
| 9 | Offensive Security / Red Team | Security | 84 | Fortress |
| 11 | Engineering Manager | Engineering Leadership | 83 | Safe |
| 12 | Data Engineer | Data & AI | 82 | Safe |
| 13 | Systems / Low-level Engineer | Engineering | 81 | Safe |
| 14 | Technical Product Manager | Product & Design | 79 | Safe |
| 14 | Solutions Architect | Specialized & Emerging | 79 | Safe |
| 16 | Developer Experience Engineer | Specialized & Emerging | 75 | Safe |
| 17 | Embedded Engineer | Engineering | 74 | Safe |
| 18 | AI Application Engineer | Data & AI | 73 | Safe |
| 18 | Product Manager | Product & Design | 73 | Safe |
| 20 | Backend Engineer | Engineering | 72 | Safe |
| 20 | DevOps Engineer | Platform & Infrastructure | 72 | Safe |
| 22 | Cloud Engineer | Platform & Infrastructure | 67 | Stable |
| 22 | UX Designer / Researcher | Product & Design | 67 | Stable |
| 24 | Product Designer | Product & Design | 64 | Stable |
| 24 | SDET / Test Infrastructure | Quality & Testing | 64 | Stable |
| 26 | iOS Engineer | Engineering | 62 | Stable |
| 26 | Android Engineer | Engineering | 62 | Stable |
| 26 | Full-Stack Engineer | Engineering | 62 | Stable |
| 29 | Analytics Engineer | Data & AI | 57 | Exposed |
| 30 | Frontend Engineer | Engineering | 52 | Exposed |
| 30 | Data Scientist | Data & AI | 52 | Exposed |
| 32 | QA Automation | Quality & Testing | 40 | At risk |
| 32 | UI Designer | Product & Design | 40 | At risk |
| 34 | Data Analyst | Data & AI | 33 | At risk |
| 35 | Prompt Engineer | Specialized & Emerging | 27 | At risk |
| 36 | QA Manual | Quality & Testing | 20 | At risk |

---

## 1. Engineering Leadership

### Staff Engineer / Tech Lead — **94 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | Every org of 50+ engineers needs them; supply does not scale. |
| Automation Resistance | 9 | The role *is* judgment + cross-team coordination. AI cannot own this. |
| Skill Depth | 10 | 10–15 years to reach the bar. Compounds slowly, holds value. |
| Strategic Importance | 10 | Architectural decisions outlive the codebase. |

**Salary range**: $250K – $700K+ TC (US senior IC, public-company range).
**Key dynamics**: AI raises the value of senior IC work because it lowers the cost of mid-level work. Companies hire fewer mid-engineers and pay staff more. The "missing middle" hypothesis bears out in 2025 levels.fyi data — staff comp grew 11% YoY while mid-level grew 2%.
**Risks**: None within the window. Comp normalization possible after 2030 if AI displacement curves accelerate.

### Engineering Manager — **83 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Steady. Span-of-control increasing as AI amplifies IC throughput. |
| Automation Resistance | 9 | People management is among the least automatable functions. |
| Skill Depth | 8 | Hard to develop; requires both technical and human judgment. |
| Strategic Importance | 9 | Allocation, hiring, retention — all critical and durable. |

**Salary range**: $160K – $400K TC.
**Key dynamics**: Span of control is rising — 2026 EMs commonly own 8–12 ICs vs. 6–8 in 2020 — because AI tooling makes ICs higher-leverage. Net effect on EM headcount is roughly flat: fewer EMs per IC, but more ICs in absolute terms. EMs who can do AI-aware planning (capacity, eval, model-cost forecasting) command a premium.
**Risks**: First-line EM at small companies is the exposed tier — companies skip the layer entirely or convert to "tech lead manager" hybrids.

---

## 2. Security

### Security Engineer (general) — **92 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | Cyber spend grows 12–14% YoY (Gartner 2025 forecast). |
| Automation Resistance | 9 | Adversarial domain; attackers also use AI, so defenders are net-up. |
| Skill Depth | 9 | Multi-year ramp; cross-cutting domain knowledge required. |
| Strategic Importance | 10 | Existential — a breach can end a company. |

**Salary range**: $130K – $350K TC.
**Key dynamics**: Three forces compound. (1) AI-generated code multiplies attack surface. (2) Regulatory pressure (EU AI Act enforcement 2026, SEC cyber-disclosure, PCI 4.0, sectoral rules) creates structural compliance demand. (3) Senior security talent is genuinely scarce — pipeline is narrow because security takes 5+ years to develop credibly. **The headcount-to-vacancy ratio in security is the worst of any tech category.**
**Risks**: Tooling consolidation (CNAPP, SIEM/SOAR convergence) can reduce demand for tool-specific operators. Defensible move: own a domain (cloud, app, identity) end-to-end, not a vendor.

### Application Security Engineer — **87 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | AI-generated code volume drives proportional review demand. |
| Automation Resistance | 8 | Threat modeling and root-cause review remain human-led. |
| Skill Depth | 9 | Code-level + protocol-level + adversarial mindset. |
| Strategic Importance | 9 | Shifts left into the SDLC; touches every team. |

**Salary range**: $130K – $360K TC.
**Key dynamics**: SAST/DAST tools improve, but their false-positive rates make human triage essential. AI-coding tools shift the bottleneck from "writing secure code" to "reviewing AI-written code at scale." AppSec engineers who own that review pipeline are critical-path.
**Risks**: SaaS AppSec platforms can squeeze in-house headcount at smaller companies.

### Cloud Security Engineer — **87 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | Cloud spend keeps growing; cloud blast radius keeps growing. |
| Automation Resistance | 8 | Misconfiguration analysis is partly automatable; response is not. |
| Skill Depth | 9 | AWS + Azure + GCP + IaC + identity is a wide surface. |
| Strategic Importance | 9 | Most breaches in 2024–25 traced to cloud misconfig. |

**Salary range**: $130K – $340K TC.
**Key dynamics**: Converging with cloud platform engineering at well-run companies. The bilingual role — "platform engineer who owns IAM and the security baseline" — is the highest-leverage shape.
**Risks**: CSPM tooling automation eats junior tier of this role faster than senior tier.

### Offensive Security / Red Team — **84 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Smaller market; high prestige; consultancy-heavy. |
| Automation Resistance | 9 | Genuinely creative work; AI helps with recon, not exploitation. |
| Skill Depth | 10 | Deepest skill ladder of any role on this list. |
| Strategic Importance | 8 | Demonstrates real risk to executives in a way audits don't. |

**Salary range**: $120K – $330K TC.
**Key dynamics**: AI-assisted attack tooling (autonomous recon, exploitation chains) raises the *bar* for human red-teamers but does not displace them — adversarial AI is a force multiplier the same way it is for defenders. Niche but durable.
**Risks**: Consultancy market is cyclical; in-house red teams cut first in downturns.

---

## 3. Data & AI

### AI Research Engineer — **89 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 8 | Concentrated at frontier labs + a few hyperscalers. |
| Automation Resistance | 9 | Frontier research is what *creates* the AI tools. |
| Skill Depth | 10 | PhD-equivalent ramp; publication track expected. |
| Strategic Importance | 9 | Owns the org's model-quality moat. |

**Salary range**: $180K – $700K+ TC. Frontier-lab packages exceed $1M for top researchers.
**Key dynamics**: The research/applied split is hardening. Pretraining is a winner-take-most subdomain — only OpenAI, Anthropic, Google DeepMind, Meta, xAI, and 3–5 Chinese labs hire at scale. Outside the frontier, "research engineer" titles increasingly mean applied evaluation and adaptation work.
**Risks**: Comp normalization 2028–2030 if the frontier saturates. Demand will hold; magnitude won't.

### ML Engineer — **87 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | Every product company building AI features needs them. |
| Automation Resistance | 8 | AI tools accelerate this role; they don't replace it. |
| Skill Depth | 9 | ML systems + production infra + research literacy. |
| Strategic Importance | 9 | Owns the model side of the product. |

**Salary range**: $140K – $400K TC.
**Key dynamics**: The applied-ML track has 10× the headcount of the research track and is where most career safety lives. The growth subniche through 2030: **agent systems engineering** — building reliable, evaluable, observable LLM-based agents in production.
**Risks**: Foundation-model commoditization could collapse demand for in-house training. Most ML jobs by 2030 will be *integration*, not training.

### MLOps Engineer — **87 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | Production AI fails without these people. |
| Automation Resistance | 8 | Deep tooling, monitoring, evaluation infrastructure. |
| Skill Depth | 9 | DevOps + ML systems + data engineering convergence. |
| Strategic Importance | 9 | The reliability layer for every AI feature shipped. |

**Salary range**: $130K – $340K TC.
**Key dynamics**: The role is converging with platform engineering at companies where AI is core product. Eval infrastructure (golden datasets, regression suites, cost/latency dashboards) is the rising subniche. By 2028, "ML platform engineer" overtakes "MLOps engineer" as the dominant title.
**Risks**: Managed platforms (Databricks, Vertex AI, SageMaker) eat the lower tier. Defensible move: own the eval and observability layer.

### Data Engineer — **82 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | Every AI initiative starts and ends with data. |
| Automation Resistance | 7 | Pipelines have integration complexity AI struggles with. |
| Skill Depth | 8 | SQL + distributed systems + lakehouse + streaming. |
| Strategic Importance | 9 | Data infrastructure is the foundation of every analytics + ML system. |

**Salary range**: $110K – $310K TC.
**Key dynamics**: dbt-native and Iceberg-native pipelines are the dominant 2026 stack. The growth subniche: **AI-data engineering** — building training data pipelines, embedding stores, retrieval indices. This is data engineering with ML literacy attached, and pays 25–30% over generic data eng.
**Risks**: Fully-managed platforms (Snowflake, Databricks, ClickHouse Cloud) compress the bottom of the market.

### AI Application Engineer — **73 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 10 | Fastest-growing job category in 2025–26. |
| Automation Resistance | 5 | Integration work is exactly what AI tools do well. |
| Skill Depth | 6 | Lower barrier than ML eng; mostly orchestration + prompting + RAG. |
| Strategic Importance | 8 | Owns user-facing AI features. |

**Salary range**: $120K – $320K TC.
**Key dynamics**: This title is having a moment but will consolidate. By 2029, the work is "Backend Engineer who knows LLMs" — the same way "JavaScript Engineer" became "Frontend Engineer" became "Full-Stack." The role is real; the title is transient.
**Risks**: Lowest skill barrier of any Safe-tier role. Vulnerable to commoditization. The career-safe move: pair AI Application work with deeper backend or ML systems skills.

### Data Scientist — **52 (Exposed)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 5 | Headcount declining since 2023 peak; LinkedIn postings down ~30%. |
| Automation Resistance | 4 | Notebook-style EDA + modeling is highly LLM-automatable. |
| Skill Depth | 7 | Still real — stats + ML + business judgment. |
| Strategic Importance | 6 | Diluted by ML eng absorbing production work and analytics eng absorbing dashboards. |

**Salary range**: $100K – $250K TC.
**Key dynamics**: The role is being squeezed from two sides: ML engineers absorb the modeling work that goes to production, and analytics engineers + LLMs absorb the exploratory analysis. The surviving niche is **causal inference and experimentation specialists** at companies with mature A/B testing infrastructure (Meta, Netflix, DoorDash, Airbnb).
**Risks**: Generic "data scientist" headcount compresses 30–40% by 2030. Plan a move to ML eng or specialized causal/experimentation.

### Analytics Engineer — **57 (Stable, low end)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Stable; dbt ecosystem maturity holds the role. |
| Automation Resistance | 5 | LLMs write SQL well; modeling layer still needs a human owner. |
| Skill Depth | 6 | SQL + dbt + warehouse-internals + business semantics. |
| Strategic Importance | 6 | Owns the semantic layer between raw data and analyst consumers. |

**Salary range**: $90K – $220K TC.
**Key dynamics**: The role exists because BI tools didn't solve the modeling layer. Semantic-layer products (Cube, dbt Semantic Layer, Looker) plus LLM SQL generation are eating the bottom of this work. Senior analytics engineers who own the entire warehouse architecture survive; mid-level "SQL writer" tier compresses.
**Risks**: Convergence with data engineering (likely) or absorption into a generic "platform data engineer" role (also likely) — either way, the title may not last the decade.

### Data Analyst — **33 (At risk)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 4 | Declining fast; LLM SQL + BI tools cover the work. |
| Automation Resistance | 2 | The textbook AI-replacement case in the data category. |
| Skill Depth | 4 | Low barrier; mostly SQL + a BI tool + business sense. |
| Strategic Importance | 4 | Critical to operations but increasingly self-service. |

**Salary range**: $65K – $160K TC.
**Key dynamics**: Self-service BI + LLM-powered NL-to-SQL has reached "good enough" for ~60% of operational analytics requests. Headcount compression is mechanical, not theoretical.
**Recommended transitions**: Data analyst → analytics engineer (most natural; ~6 months); analytics engineer → data engineer (~12 months). The whole ladder moves up one rung.

---

## 4. Platform & Infrastructure

### Platform Engineer — **87 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 9 | Internal-platform investment is the dominant 2026 infra trend. |
| Automation Resistance | 8 | Builds the abstractions; AI helps build them, not own them. |
| Skill Depth | 9 | Cross-cutting: K8s + IaC + IDPs + DX + security baseline. |
| Strategic Importance | 9 | Platform velocity = engineering org velocity. |

**Salary range**: $130K – $360K TC.
**Key dynamics**: "DevOps engineer" as a title is fading; "platform engineer" and "SRE" are absorbing the work. Internal Developer Platforms (Backstage-derived, Port, custom) are now standard at every 200+ engineer org. The growth subniche: **AI platform engineer** — building golden paths for AI-feature delivery, eval pipelines, model serving, prompt-management infra.
**Risks**: Managed IDPs (Humanitec, Port, Cortex) compress the build-it-yourself tier.

### Site Reliability Engineer — **84 (Fortress)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 8 | Strong; uptime expectations rising as AI features get critical. |
| Automation Resistance | 8 | AI helps with RCA; it can't carry a pager. |
| Skill Depth | 9 | Distributed systems debugging, capacity, observability, on-call. |
| Strategic Importance | 9 | Production reliability is the customer-facing commitment. |

**Salary range**: $130K – $350K TC.
**Key dynamics**: AI-assisted RCA tooling (Honeycomb's MCP integrations, Datadog Bits AI, OpenTelemetry-native AI summarizers) accelerates incident response — but the on-call ownership stays human. The growth subniche: **MLSRE / AI inference reliability** — uptime and tail-latency for LLM-backed services, which fail in genuinely new ways.
**Risks**: Heavy on-call burden continues to push talent toward platform engineering.

### DevOps Engineer — **72 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Holding; absorbed by platform/SRE retitling. |
| Automation Resistance | 7 | IaC and CI/CD are AI-augmentable but not replaceable. |
| Skill Depth | 7 | Wide; depth varies by stack and scale. |
| Strategic Importance | 8 | Touches every release. |

**Salary range**: $100K – $290K TC.
**Key dynamics**: Generic "DevOps engineer" title is in slow decline as work bifurcates into "platform engineer" (build) and "SRE" (operate). Engineers with the title still command strong comp; the rebrand path is short and natural.
**Risks**: Junior DevOps roles compress hardest. Bootcamp-to-DevOps is a tougher path than it was in 2020.

### Cloud Engineer — **67 (Stable)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Stable but commoditizing. |
| Automation Resistance | 6 | Cloud configurations are AI-assistable. |
| Skill Depth | 7 | One-cloud depth + IaC. |
| Strategic Importance | 7 | Critical to cost + reliability but operationally narrow. |

**Salary range**: $95K – $270K TC.
**Key dynamics**: Pure "cloud engineer" titles are converging into platform/SRE/security roles. The defensible specialization is **FinOps + multi-cloud cost engineering** — a fast-rising and durable niche where cloud spend optimization is a board-level concern.
**Risks**: Vendor-specific cloud certifications (AWS, Azure, GCP) without underlying systems depth lose value fastest.

---

## 5. Engineering (core IC)

### Systems / Low-level Engineer — **81 (Safe, top end)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Smaller market but very specialized; hyperscalers + chip cos + databases. |
| Automation Resistance | 9 | Kernel, compiler, distributed-systems internals — AI cannot reason about these reliably. |
| Skill Depth | 10 | The deepest skill ladder in IC engineering. |
| Strategic Importance | 8 | Performance + correctness work has direct revenue impact. |

**Salary range**: $110K – $350K TC. Hyperscaler comp can exceed $500K.
**Key dynamics**: The AI inference stack (CUDA kernels, vLLM/SGLang internals, custom silicon backends) is the new growth area for systems engineers. Companies are paying systems-engineering rates for ML systems work, which has transferred a generation of skills into a new domain. Database internals (FoundationDB-derivatives, distributed OLTP, vector indexes) is the other growth area.
**Risks**: Smaller absolute headcount means individual job loss is more impactful — fewer adjacent moves available.

### Embedded Engineer — **74 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | IoT, automotive, robotics, defense. |
| Automation Resistance | 8 | Hardware-software interfaces stay human-led. |
| Skill Depth | 9 | C/C++ + RTOS + hardware literacy. |
| Strategic Importance | 7 | Mission-critical in the industries that need it. |

**Salary range**: $90K – $230K TC.
**Key dynamics**: Demand is driven by adjacent industries (EV, robotics, drones, edge AI) more than software companies. AI-on-device (NPUs, on-device LLMs) is the rising subniche.
**Risks**: Geographic concentration — demand pools in specific industries and regions, not broadly distributed.

### Backend Engineer — **72 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 8 | Largest absolute headcount of any role on this list. |
| Automation Resistance | 6 | AI drafts code well; system design and ownership remain human. |
| Skill Depth | 7 | Varies wildly — CRUD vs. distributed systems is two different careers. |
| Strategic Importance | 8 | Touches every product surface. |

**Salary range**: $90K – $280K TC.
**Key dynamics**: Bifurcates into **systems backend** (databases, distributed systems, latency-sensitive, payments, search) — safe and well-paid — and **CRUD backend** (REST endpoints, glue code, internal tools) — heavily AI-augmentable. Senior systems backend engineers who can do system design end-to-end stay in high demand.
**Risks**: Junior hiring contracts hard. Path-to-senior takes longer because AI does the easy work that used to be junior training ground. The "no junior backend roles" complaint in 2026 is real and structural.

### iOS Engineer — **62 (Stable)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Stable but flat. Per-app headcount declining. |
| Automation Resistance | 6 | Platform-native depth resists; UI scaffolding doesn't. |
| Skill Depth | 7 | Swift + SwiftUI + UIKit + Apple-platform depth. |
| Strategic Importance | 6 | Every consumer-facing company needs them; mid-market mobile teams shrinking. |

**Salary range**: $95K – $260K TC.
**Key dynamics**: Apple's SwiftUI maturity and the AI-design-to-code wave (Vercel v0-style for mobile) compress the middle. Native-only iOS roles consolidate at large consumer companies. Cross-platform (Flutter, React Native, KMP) keeps gaining share.
**Risks**: Mid-market teams adopt cross-platform; native specialists concentrate at Meta, Google, Uber, banks.

### Android Engineer — **62 (Stable)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Slightly weaker than iOS in US; stronger in emerging markets. |
| Automation Resistance | 6 | Same logic as iOS. |
| Skill Depth | 7 | Kotlin + Compose + Android-platform depth. |
| Strategic Importance | 6 | Same as iOS. |

**Salary range**: $90K – $250K TC.
**Key dynamics**: Compose Multiplatform + Kotlin Multiplatform are credible cross-platform stories, which threaten and protect Android specialists in different ways. Senior Android engineers who can do KMP work travel further than either side alone.
**Risks**: Same as iOS, plus regional consolidation.

### Full-Stack Engineer — **62 (Stable)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Strong title; weakening shape. |
| Automation Resistance | 5 | Generalist work is exactly what AI tools cover. |
| Skill Depth | 6 | Breadth over depth. |
| Strategic Importance | 7 | Productive at startups; less differentiated at scale. |

**Salary range**: $90K – $260K TC.
**Key dynamics**: "Full-stack TypeScript engineer" (Next.js + Node + Postgres) is the dominant 2026 generalist shape. AI tooling makes this engineer productive — and also makes one of them as productive as 2.5 of them in 2022. The career-safe move is to back the title with a depth: "full-stack with deep auth/identity," "full-stack with deep search/retrieval," "full-stack with deep payments." Generalists get compressed; specialists labeled "full-stack" do not.
**Risks**: Most exposed of the engineering generalist titles.

### Frontend Engineer — **52 (Exposed)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Compressing. Total postings down ~15% from 2024 peak. |
| Automation Resistance | 4 | Component scaffolding, layout, and styling are AI-native tasks. |
| Skill Depth | 5 | Easy entry; hard mastery. |
| Strategic Importance | 6 | UX matters — but UX-from-mockup is increasingly automated. |

**Salary range**: $80K – $230K TC.
**Key dynamics**: AI tooling (v0, Cursor, Lovable, Bolt) reliably produces working components from prompts. The work that compresses is exactly the work that defined "frontend developer" 2018–2024 — component assembly from designs. The roles that survive: **design-system engineers**, **accessibility specialists**, **performance engineers**, **DX/tooling engineers**. These require taste, deep platform knowledge, or cross-cutting concerns AI can't synthesize.
**Risks**: The bottom of the ladder collapses fastest here. Bootcamp-to-junior-frontend is no longer a reliable path.
**Recommended transitions out**: Frontend → Design Systems engineer; Frontend → DX engineer; Frontend → Full-Stack with backend depth.

---

## 6. Quality & Testing

### SDET / Test Infrastructure — **64 (Stable)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Holding; absorbing automation work from QA. |
| Automation Resistance | 6 | Test infrastructure has real engineering depth. |
| Skill Depth | 7 | CI/CD + test frameworks + production-like envs. |
| Strategic Importance | 7 | Velocity-critical at scale. |

**Salary range**: $100K – $230K TC.
**Key dynamics**: SDET converges with backend engineering and platform engineering. The skills overlap so much that "QA org" as a separate function is fading at well-run companies. Senior SDETs frequently cross over to backend or platform roles.
**Risks**: At smaller orgs, test-infra is increasingly absorbed by platform teams; standalone SDET roles rare below ~150 engineers.

### QA Automation — **40 (At risk, high end)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 4 | Declining; AI test-gen + self-healing E2E erodes the role. |
| Automation Resistance | 3 | Automating tests is what AI does well. |
| Skill Depth | 5 | Selenium, Cypress, Playwright + scripting. |
| Strategic Importance | 5 | Coverage matters; ownership rarely lives here. |

**Salary range**: $70K – $170K TC.
**Key dynamics**: Self-healing E2E frameworks (Mabl, Testim, AI-augmented Playwright) and LLM-based test generation from spec are mature enough to replace most of this role's work by 2027. The escape: convert to SDET (engineering depth) or AI Eval (model-QA — a real growing field).

### QA Manual — **20 (At risk)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 2 | Shrinking the most of any role on this list. |
| Automation Resistance | 1 | Textbook AI-replacement case. |
| Skill Depth | 3 | Low barrier. |
| Strategic Importance | 3 | Necessary; not differentiating. |

**Salary range**: $50K – $130K TC.
**Key dynamics**: Offshore QA centers (which absorbed much of this work in the 2010s) are the first to be AI-displaced. Career mobility *out* of pure manual QA is harder than out of any other role on this list.
**Recommended transitions** (in priority order):

1. SDET → backend engineer (most natural; 12 months of focused study)
2. AI Evaluation engineer (best upside; requires Python + ML literacy)
3. DevOps / release engineering (good fit for QA-leaning automation people)

Plan the move now, not later. The decline curve is exponential.

---

## 7. Product & Design

### Technical Product Manager — **79 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Rising as products get more technical (AI features, dev tools, infra). |
| Automation Resistance | 8 | Spec writing partly automatable; cross-team negotiation isn't. |
| Skill Depth | 8 | Both technical and product judgment required. |
| Strategic Importance | 9 | Owns critical-path decisions. |

**Salary range**: $130K – $340K TC.
**Key dynamics**: TPM growth outpaces generalist PM growth as more products are technically deep (developer tools, AI features, platforms, infra). TPMs with AI/ML literacy are the highest-comp tier. The role is becoming the IC equivalent of an engineering manager — owns scope but not direct reports.
**Risks**: Title inflation — many "TPM" roles at non-tech companies are PM-with-extra-meetings, not the real shape.

### Product Manager — **73 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Steady. Smaller orgs cutting layers but PM count holds. |
| Automation Resistance | 7 | Stakeholder management + judgment is AI-resistant. |
| Skill Depth | 6 | Wide; the moat is taste, not technique. |
| Strategic Importance | 9 | Defines what gets built. |

**Salary range**: $110K – $310K TC.
**Key dynamics**: Heavy AI augmentation in PM workflow (eval, customer research synthesis, doc-writing) — but the role itself is durable because the work is fundamentally about navigating ambiguity and people. Junior PM roles are the most exposed; senior PM is fortress-tier.
**Risks**: At smaller companies, PM is collapsing into "engineer-PM" hybrids (the ICPM model), which can compress headcount.

### UX Designer / Researcher — **67 (Stable)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Stable. Research roles holding better than visual roles. |
| Automation Resistance | 7 | Customer research and synthesis are slow to automate. |
| Skill Depth | 7 | Real craft + research methodology. |
| Strategic Importance | 7 | Mature orgs invest; immature orgs cut. |

**Salary range**: $85K – $220K TC.
**Key dynamics**: UX research is genuinely defensible — synthesis + interpretation + study design require human judgment. UX *design* (wireframes, IA) is more AI-augmentable. The split is widening into "UX researcher" and "Product designer" with a shrinking middle.
**Risks**: Boom-bust cycles in design hiring; UX roles get cut first in downturns.

### Product Designer — **64 (Stable)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 6 | Stable; converging with senior frontend at AI-native companies. |
| Automation Resistance | 6 | AI design-to-code raises the bar but doesn't eliminate the role. |
| Skill Depth | 7 | Visual + interaction + systems thinking. |
| Strategic Importance | 7 | Owns the user-facing surface. |

**Salary range**: $95K – $250K TC.
**Key dynamics**: "Design engineer" — designers who code their own components in design systems — is the rising shape. The product designer who can ship working code beats the one who ships only Figma files.
**Risks**: The visual-only end of product design is the soft spot.

### UI Designer — **40 (At risk)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 4 | Declining. Visual-only roles compressing fastest in design. |
| Automation Resistance | 3 | The most AI-exposed creative task. |
| Skill Depth | 5 | Visual craft + tool fluency. |
| Strategic Importance | 5 | Visual quality matters; ownership rarely lives in pure-UI. |

**Salary range**: $75K – $190K TC.
**Key dynamics**: Mid-journey, Stable Diffusion variants, and AI design tools (Galileo, Uizard, Vercel v0) cover the low-to-mid end of UI work. The defensible niche: UI specialists who own animation, motion, and interaction prototyping at the depth Figma + AI tools can't replicate.
**Recommended transitions**: UI Designer → Product Designer (most natural) → Design Engineer (requires code skills; high upside).

---

## 8. Specialized & Emerging

### Solutions Architect — **79 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Steady at enterprise software vendors and consultancies. |
| Automation Resistance | 8 | Customer-facing technical judgment is hard to automate. |
| Skill Depth | 9 | Cross-product technical depth + customer skills. |
| Strategic Importance | 8 | Owns the deal-side technical narrative. |

**Salary range**: $140K – $340K TC. OTE-heavy at vendors.
**Key dynamics**: AI tools accelerate POC building, which makes good solutions architects 2× more productive. The role itself is durable because it's customer-facing technical work — AI assists, doesn't replace, the human-relationship layer.
**Risks**: Vendor consolidation can shrink the role at specific companies; the function is durable but employer-specific.

### Developer Experience (DX) Engineer — **75 (Safe)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 7 | Rising. Every developer-facing company invests here. |
| Automation Resistance | 8 | Taste-driven work; AI assists but can't own it. |
| Skill Depth | 8 | Tooling + writing + product sense. |
| Strategic Importance | 7 | Critical to adoption at developer-tools companies. |

**Salary range**: $120K – $300K TC.
**Key dynamics**: At developer-tools companies (Vercel, Stripe, Anthropic, Linear, Supabase), DX is core product. At product companies, DX work is internal — building the IDP, the docs, the SDK. Both flavors are durable. The growth subniche: **DX for AI tools** — onboarding, evaluation, and adoption flows for AI products, which requires very specific taste.
**Risks**: Title is fuzzy; can be miscast as "tech writer who codes" at companies that don't take DX seriously.

### Prompt Engineer — **27 (At risk)**

| Axis | Score | Note |
| --- | --- | --- |
| Demand | 3 | Hot in 2023; quietly declining since. |
| Automation Resistance | 2 | Better models reduce prompt sensitivity, eliminating the role. |
| Skill Depth | 3 | Genuinely shallow as a standalone skill. |
| Strategic Importance | 3 | Real but absorbed into AI Application Engineer / ML Eng work. |

**Salary range**: $80K – $180K TC.
**Key dynamics**: The role was always a transitional artifact of model immaturity. As models become more robust to prompt phrasing, the value of prompt-only specialists collapses. Prompt-engineering *skills* are real; the *job title* is not durable.
**Recommended transitions**: Prompt Engineer → AI Application Engineer (natural; requires backend literacy) → ML Engineer (longer ramp; requires ML systems knowledge).

---

## Cross-cutting patterns

- **Automation pressure is bottom-up.** Junior and routine work compresses fastest in every category. The senior end is largely safe — for now. The 2026 hiring market reflects this: senior comp climbing, junior reqs scarce.
- **Specialization beats breadth in 2026–2030.** The "full-stack generalist" identity that worked in 2018 is the most exposed shape today. Pick a moat: a domain (payments, ML infra, real-time, search), a cross-cutting skill (perf, a11y, security), or a platform (deep iOS, deep K8s, deep Postgres internals).
- **Stability tracks distance from the UI.** The further from the screen, the more durable the role: Security ≈ ML systems ≈ Platform > Backend systems > DevOps > Backend CRUD > Mobile > Frontend > QA Manual.
- **AI literacy is now baseline in every role.** By 2027, "doesn't use AI tools effectively" will be a hiring red flag in all 36 roles on this list — including PM and Designer. This is not a differentiator; it is table stakes.
- **Adversarial domains are the hidden winners.** Security stands out because the threat side also gets AI. Anywhere the work involves an opponent (security, fraud, abuse, anti-cheat, market making), AI escalates both sides — and humans stay in the loop.
- **Title inflation will obscure the real ranking.** Expect "AI Engineer" and "AI Product Manager" titles to appear on 2× as many job postings by 2028 without the underlying role changing. Look at the work, not the title.
