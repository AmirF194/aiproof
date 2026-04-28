# Per-Role Analysis (2026–2035)

The full **1,000-role** dataset, scored on demand, automation resistance, skill depth, and strategic importance. Methodology in [METHODOLOGY.md](METHODOLOGY.md). Raw inputs in [data/roles.csv](data/roles.csv). Computed outputs (rankings, tier summaries, category averages) in [data/processed/](data/processed/). Deep research synthesis with citations in [INSIGHTS.md](INSIGHTS.md).

**Reading the score:** 0–100, where higher = more durable over the 5–10 year window.

| Tier | Score | Verdict |
| --- | --- | --- |
| Fortress | 83+ | Build a career here without hedging. |
| Safe | 70–82 | Senior path is durable. Junior path is harder than 2020. |
| Stable | 58–69 | Specialize within the role or get exposed. |
| Exposed | 41–57 | Plan an adjacent move within 2–3 years. |
| At risk | ≤40 | Plan a transition. Headcount shrinks every year. |

**Distribution across the 1,000 roles:** Fortress 79 · Safe 315 · Stable 329 · Exposed 223 · At risk 54.

This file enumerates the **top of the ranking, the bottom, and the top + bottom of each category**. The full per-role table — all 1,000 rows — is [data/processed/role_ranking.csv](data/processed/role_ranking.csv).

---

## Master ranking — Top 30

| Rank | Role | Category | Score |
| --- | --- | --- | --- |
| 1 | Chief AI Officer | Engineering Leadership | 94 |
| 1 | Staff Engineer / Tech Lead | Engineering Leadership | 94 |
| 1 | VP of AI / ML | Engineering Leadership | 94 |
| 1 | Staff Security Engineer | Security | 94 |
| 5 | Senior LLM Engineer | Data & AI | 92 |
| 5 | Security Engineer | Security | 92 |
| 5 | Senior Security Engineer | Security | 92 |
| 8 | CTO | Engineering Leadership | 91 |
| 8 | Principal Engineer | Engineering Leadership | 91 |
| 8 | Senior Principal Engineer | Engineering Leadership | 91 |
| 8 | Senior Staff Engineer | Engineering Leadership | 91 |
| 12 | Chief Information Security Officer | Engineering Leadership | 90 |
| 12 | VP of Engineering | Engineering Leadership | 90 |
| 12 | VP of Security | Engineering Leadership | 90 |
| 15 | AI Research Engineer | Data & AI | 89 |
| 15 | AI Safety / Alignment Researcher | Data & AI | 89 |
| 15 | Foundation Model Engineer | Data & AI | 89 |
| 15 | LLM Research Scientist | Data & AI | 89 |
| 15 | Senior AI Research Engineer | Data & AI | 89 |
| 15 | Staff ML Engineer | Data & AI | 89 |
| 15 | CUDA Engineer | Engineering | 89 |
| 22 | Chief Architect | Engineering Leadership | 88 |
| 22 | VP of Infrastructure | Engineering Leadership | 88 |
| 22 | VP of Platform | Engineering Leadership | 88 |
| 25 | AI Infrastructure Engineer | Data & AI | 87 |
| 25 | LLM Engineer | Data & AI | 87 |
| 25 | ML Engineer | Data & AI | 87 |
| 25 | MLOps Engineer | Data & AI | 87 |
| 25 | Senior ML Engineer | Data & AI | 87 |
| 25 | SVP of Engineering | Engineering Leadership | 87 |

**What the top reveals:** four clusters dominate the Fortress band — (1) the IC-staff and IC-principal track, (2) the AI/ML build path (LLM, foundation-model, ML systems, AI safety), (3) the security track at every seniority, (4) C-suite and VP roles whose work AI cannot meaningfully automate. Notice that **CUDA Engineer** lands in the top 21 — an ostensibly "low-level" role that sits at the structural bottleneck of every frontier-AI training run.

---

## Bottom 20 — most at-risk

| Rank | Role | Category | Score |
| --- | --- | --- | --- |
| 979 | Selenium Engineer | Quality & Testing | 35 |
| 979 | No-code Developer / Maker | Specialized & Emerging | 35 |
| 983 | Sigma / ThoughtSpot Developer | Data & AI | 34 |
| 983 | Alpine.js Engineer | Engineering | 34 |
| 983 | KaiOS Engineer | Engineering | 34 |
| 983 | PowerBuilder Maintainer | Engineering | 34 |
| 983 | Visual Basic / VB.NET Maintainer | Engineering | 34 |
| 988 | Data Analyst | Data & AI | 33 |
| 989 | Pardot Developer | Specialized & Emerging | 32 |
| 990 | QA Manual Lead | Quality & Testing | 31 |
| 991 | MicroStrategy Developer | Data & AI | 30 |
| 991 | Game QA Tester | Engineering | 30 |
| 991 | Desktop Support | Platform & Infrastructure | 30 |
| 994 | Domo Developer | Data & AI | 29 |
| 994 | Mode Analytics Developer | Data & AI | 29 |
| 994 | ColdFusion Maintainer | Engineering | 29 |
| 994 | jQuery Maintainer | Engineering | 29 |
| 998 | Prompt Engineer | Data & AI | 27 |
| 999 | Help Desk Tier 1 | Platform & Infrastructure | 25 |
| 1000 | QA Manual | Quality & Testing | 20 |

**What the bottom reveals:** three patterns repeat — (1) **legacy stacks** with shrinking maintainer pools (ColdFusion, PowerBuilder, VB.NET, jQuery, Alpine.js, KaiOS) — these survive but the runway is short; (2) **vendor-bound BI / no-code tools** (MicroStrategy, Domo, Mode, Sigma, Pardot, no-code maker) — the work is real but the tooling is being eaten by LLM SQL and modern semantic layers; (3) **routine tier-1 / manual roles** (Help Desk, Manual QA, Desktop Support, Game QA Tester) — the textbook AI-replacement category.

The single role whose collapse is fastest in this dataset: **Prompt Engineer** at 27 — a 2023 artifact already absorbed back into AI Application / ML Engineer work.

---

## 1. Engineering Leadership (45 roles)

Top of category leans **C-suite and IC-track** — the two paths AI cannot meaningfully automate.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 94 | Fortress | Chief AI Officer |
| 94 | Fortress | Staff Engineer / Tech Lead |
| 94 | Fortress | VP of AI / ML |
| 91 | Fortress | CTO |
| 91 | Fortress | Principal Engineer |
| 91 | Fortress | Senior Principal Engineer |
| 91 | Fortress | Senior Staff Engineer |
| 90 | Fortress | Chief Information Security Officer |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 64 | Stable | Head of Frontend |
| 63 | Stable | Engineering Operations Manager |
| 58 | Stable | Head of QA |

**Cluster read:** the IC ladder above Staff (Principal, Senior Principal, Distinguished, Fellow) is the most durable career shape in the dataset — comp scales to $1M+ and AI assists rather than substitutes. The "Head of QA" position falling to the bottom of the leadership category mirrors the Quality & Testing collapse below.

---

## 2. Security (75 roles)

The single category where **every senior role lands Fortress or Safe** — supply gap is structural, not cyclical.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 94 | Fortress | Staff Security Engineer |
| 92 | Fortress | Security Engineer |
| 92 | Fortress | Senior Security Engineer |
| 87 | Fortress | AI / ML Security Engineer |
| 87 | Fortress | AI Red Team Engineer |
| 87 | Fortress | Application Security Engineer |
| 87 | Fortress | Cloud Security Engineer |
| 87 | Fortress | Security Architect |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 59 | Stable | Wireless Pentester |
| 55 | Exposed | SOC Analyst (Tier 2) |
| 45 | Exposed | SOC Analyst (Tier 1) |

**Cluster read:** the new Fortress-tier additions are the AI-adjacent security functions — **AI/ML Security Engineer** and **AI Red Team Engineer** both land at 87, on par with AppSec and Cloud Security. The bottom of the cluster is **Tier-1 SOC analysts**, the single security role being meaningfully automated by SIEM-native LLMs and SOAR playbooks. Every seniority above Tier-2 SOC remains durable.

---

## 3. Data & AI (178 roles)

The category with the **widest internal spread** (89 down to 27) and the most role explosion in the 1,000-row expansion. Build vs. consume splits cleanly along the score axis.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 92 | Fortress | Senior LLM Engineer |
| 89 | Fortress | AI Research Engineer |
| 89 | Fortress | AI Safety / Alignment Researcher |
| 89 | Fortress | Foundation Model Engineer |
| 89 | Fortress | LLM Research Scientist |
| 89 | Fortress | Senior AI Research Engineer |
| 89 | Fortress | Staff ML Engineer |
| 87 | Fortress | AI Infrastructure Engineer |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 29 | At risk | Domo Developer |
| 29 | At risk | Mode Analytics Developer |
| 27 | At risk | Prompt Engineer |

**Cluster read:** the new title proliferation (LLM Engineer, Foundation Model Engineer, AI Agent Engineer, AI Safety Researcher, RLHF Engineer, Multimodal AI Engineer, Vector Search Engineer) all lands Fortress or high-Safe — the agentic surge is structural, not a bubble. The bottom of the category is **legacy BI tooling** (Domo, Mode, Sigma, MicroStrategy) plus the **Prompt Engineer** title, which has effectively died out as a standalone role since 2024.

---

## 4. Platform & Infrastructure (121 roles)

Includes corporate IT (sysadmin, help desk, M365 admin) — the bottom of this category captures what AI displaces hardest in the broader IT job market, even though "platform engineer" itself is Fortress-tier.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 87 | Fortress | Platform Engineer |
| 86 | Fortress | Staff Platform Engineer |
| 86 | Fortress | Staff SRE |
| 84 | Fortress | Internal Developer Platform (IDP) Engineer |
| 84 | Fortress | Senior Platform Engineer |
| 84 | Fortress | Senior SRE |
| 84 | Fortress | Site Reliability Engineer |
| 82 | Safe | Kubernetes / Container Platform Engineer |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 35 | At risk | Help Desk Tier 2 |
| 30 | At risk | Desktop Support |
| 25 | At risk | Help Desk Tier 1 |

**Cluster read:** **Internal Developer Platform Engineer** rises into the Fortress band because Backstage-style platforms are now standard at every 200+ engineer org. The bottom of the cluster is **corporate IT** — the help desk and desktop support tier is being absorbed by AI-augmented self-service portals. Cloud/DevOps mid-tier holds Stable but is rebranding into Platform.

---

## 5. Engineering — core IC (405 roles)

The largest category, with the widest stack/seniority fragmentation. Backend-systems and AI-adjacent engineering hold; framework-specific frontend and legacy-stack maintenance compress.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 89 | Fortress | CUDA Engineer |
| 86 | Fortress | Autonomous Vehicle Software Engineer |
| 86 | Fortress | Distributed Systems Engineer |
| 86 | Fortress | GPU Engineer |
| 86 | Fortress | Self-Driving Perception Engineer |
| 86 | Fortress | Self-Driving Planning Engineer |
| 86 | Fortress | Triton (GPU) Kernel Engineer |
| 83 | Fortress | Principal Backend Engineer |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 30 | At risk | Game QA Tester |
| 29 | At risk | ColdFusion Maintainer |
| 29 | At risk | jQuery Maintainer |

**Cluster read:** the top of the engineering category is now dominated by **GPU + autonomy** roles — CUDA Engineer, Triton Kernel Engineer, GPU Engineer, Self-Driving Perception/Planning. These were largely absent from the 36-role frame. Mid-tier general backend (Senior Backend, Senior Full-Stack) holds Safe; framework-specific frontend (React, Vue, Angular as standalone titles) drops into Stable. The legacy-maintenance bottom is the longest tail in the dataset — every COBOL, RPG, ColdFusion, PowerBuilder, jQuery, and Alpine.js role lands At-risk or Exposed.

---

## 6. Specialized & Emerging (100 roles)

Sales engineering, DevRel, technical program management, integration platforms, vendor specialists. Comparatively flat distribution — most roles land Stable.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 84 | Fortress | Senior Forward Deployed Engineer |
| 84 | Fortress | Senior TPM |
| 83 | Fortress | Technical Program Manager |
| 81 | Safe | Principal TPM |
| 80 | Safe | Forward Deployed Engineer |
| 79 | Safe | Senior Solutions Architect |
| 79 | Safe | Solutions Architect |
| 77 | Safe | Senior Sales Engineer |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 37 | At risk | Zendesk Developer |
| 35 | At risk | No-code Developer / Maker |
| 32 | At risk | Pardot Developer |

**Cluster read:** **Forward Deployed Engineer** — the category that barely existed in the 36-role frame — now anchors the top with two Fortress-tier entries. AI-product companies hire FDEs aggressively because customer-specific agent integration is the most defensible work in the AI app layer. The bottom is **vendor-bound implementer roles** (Zendesk, Pardot, no-code makers) that depend on specific SaaS tools whose feature surface is being absorbed by general-purpose AI platforms.

---

## 7. Product & Design (48 roles)

Senior PM and AI PM hold; UI Designer / Marketing Designer / generic Visual Designer compress.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 83 | Fortress | Senior Technical PM |
| 81 | Safe | Principal Product Manager |
| 80 | Safe | Group Product Manager |
| 80 | Safe | Platform Product Manager |
| 79 | Safe | Technical Product Manager |
| 78 | Safe | Senior Product Manager |
| 74 | Safe | Senior Design Engineer |
| 73 | Safe | API Product Manager |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 44 | Exposed | Visual Designer |
| 40 | At risk | UI Designer |
| 37 | At risk | Marketing Designer |

**Cluster read:** **Senior Technical PM** is the highest-scored product role at 83 — the bilingual PM ↔ engineer track survives best. **Design Engineer** and **Senior Design Engineer** carry the design discipline forward as a Safe-tier specialty; pure-visual roles (UI, Marketing, Visual) are the most AI-exposed creative work in the dataset.

---

## 8. Quality & Testing (28 roles)

Smallest category and the only one with **no Fortress entries**. SDET and security QA hold Safe; everything else compresses.

**Top 8**

| Score | Tier | Role |
| --- | --- | --- |
| 72 | Safe | Security QA Engineer |
| 72 | Safe | Test Architect |
| 69 | Stable | Performance / Load Test Engineer |
| 69 | Stable | Staff SDET |
| 67 | Stable | Senior SDET |
| 65 | Stable | Quality Engineering Director |
| 64 | Stable | SDET / Test Infrastructure |
| 64 | Stable | Stress Test Engineer |

**Bottom 3 in category**

| Score | Tier | Role |
| --- | --- | --- |
| 35 | At risk | Selenium Engineer |
| 31 | At risk | QA Manual Lead |
| 20 | At risk | QA Manual |

**Cluster read:** the only QA roles that survive are **adversarial / safety / performance** specialists — Security QA, Test Architect, Performance Engineer. The "person who writes Selenium scripts" tier collapses fully (Selenium Engineer at 35). The transition path Manual QA → SDET → Backend or AI Eval remains the cleanest exit from the bottom.

---

## How to use this report

- **Choosing a first specialization** — pick from the per-category top 8s above. Security, Platform/SRE, ML/AI builders, and the IC ladder are the highest-confidence Fortress paths.
- **Mid-career pivot from Stable / Exposed** — move *adjacent*, not lateral. Frontend → Design Systems → Design Engineer. Data Scientist → Senior Data Scientist or ML Engineer. QA → SDET → AI Eval.
- **Mid-career pivot from At-risk** — give yourself 12–18 months and a structured study plan. The transitions that work: Manual QA → SDET → AI Eval; Data Analyst → Analytics Eng → Data Eng; UI Designer → Product Designer → Design Engineer; legacy maintainer (COBOL/ColdFusion) → modernization engineer.
- **Hiring** — expect Security, ML/AI infrastructure, and Platform comp to keep climbing through 2028. Expect the bottom 200 roles in this dataset to compress 30–50% by 2030. Expect "AI Application Engineer" and "AI Agent Engineer" to consolidate back into "Backend Engineer who knows LLMs" by ~2029.

The full ranking — every one of the 1,000 roles — is in [data/processed/role_ranking.csv](data/processed/role_ranking.csv).
