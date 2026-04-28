# Role Taxonomy

Canonical list of the 36 roles scored in this analysis, grouped by category, with a one-line definition and the primary skills that define each role.

The full machine-readable version is in [data/raw/role_definitions.json](../data/raw/role_definitions.json). For per-role scoring rationale, see [REPORT.md](../REPORT.md). For the rubric and weights, see [METHODOLOGY.md](../METHODOLOGY.md).

---

## How roles were chosen

1. Cover every distinct, salaried function in modern software organizations of 50+ engineers.
2. Distinct titles only when the *underlying work* differs. "Backend Engineer" and "Full-Stack Engineer" both write Python, but the work shapes diverge enough to score separately. "ML Engineer" and "ML Ops Engineer" overlap heavily but have separate maturity curves.
3. Cross-referenced with the BLS Standard Occupational Classification, O*NET, and the LinkedIn Skills Graph so the taxonomy maps cleanly to public datasets where possible.
4. Roles whose entire shape is a 2024-onward AI-driven artifact (Prompt Engineer, AI Application Engineer) are kept in the list because they're real categories in 2026 hiring, even when the analysis predicts consolidation.

---

## 1. Engineering Leadership (2 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **Staff Engineer / Tech Lead** | Senior IC who owns architecture, cross-team trade-offs, and mentorship without direct reports. | system design, code review at scale, technical strategy, cross-team coordination |
| **Engineering Manager** | First/second-line people manager; owns hiring, allocation, performance, team-level delivery. | people management, hiring, 1:1s, capacity planning |

---

## 2. Security (4 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **Security Engineer** | Generalist IC: detection, IR, vuln management, threat modeling. | threat modeling, IR, vuln mgmt, SIEM/SOAR |
| **Application Security Engineer** | Embedded with engineering teams to secure code, libraries, APIs, third-party integrations. | SAST/DAST, secure code review, threat modeling |
| **Cloud Security Engineer** | IAM, network policy, CSPM, workload identity, secrets management — usually paired with platform eng. | AWS/Azure/GCP IAM, IaC security, CSPM |
| **Offensive Security / Red Team** | Adversarial testers — pentest, red-team ops, exploit development. | pentesting, exploit dev, social engineering, C2 |

---

## 3. Data & AI (7 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **AI Research Engineer** | Frontier-lab role: pretraining, alignment, evaluation, novel architectures. PhD-equivalent ramp. | deep learning, PyTorch/JAX, distributed training |
| **ML Engineer** | Builds production ML systems: training pipelines, feature eng, serving, eval. | Python, PyTorch, ML systems, MLOps fundamentals |
| **MLOps Engineer** | Reliability + infrastructure for ML in prod: training infra, feature stores, eval pipelines, monitoring. | Kubernetes, training infra, observability, eval frameworks |
| **Data Engineer** | Pipelines, warehouses, lakehouses — the foundation for analytics + ML. | SQL, Spark, Iceberg/Delta, dbt, streaming |
| **AI Application Engineer** | Integrates LLMs and foundation models into product surfaces. RAG, agents, evals. | LLM integration, RAG, agents, evals |
| **Data Scientist** | Statistics, experimentation, exploratory analysis. Bifurcating into causal specialists + notebook generalists. | stats, experimentation, Python/R, causal inference |
| **Analytics Engineer** | Owns the semantic / modeling layer between raw data and analyst consumers. dbt-native. | SQL, dbt, data modeling, warehouse internals |
| **Data Analyst** | Operational analytics: dashboards, ad-hoc queries, business analysis. | SQL, BI tools, spreadsheets, stakeholder comm |

---

## 4. Platform & Infrastructure (4 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **Platform Engineer** | Builds the internal developer platform: golden paths, IDPs, infra abstractions, self-service tooling. | Kubernetes, IaC, API design, DX |
| **Site Reliability Engineer** | Production reliability: SLOs, on-call, capacity, observability, IR. | distributed-systems debugging, SLO/SLI, on-call |
| **DevOps Engineer** | CI/CD, deployment automation, IaC. Title bifurcating into platform vs SRE. | CI/CD, Terraform, scripting, container orchestration |
| **Cloud Engineer** | Cloud-platform-specific: AWS/Azure/GCP architecture, FinOps, multi-cloud cost. | AWS/Azure/GCP, IaC, cost optimization, networking |

---

## 5. Engineering — core IC (6 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **Systems / Low-level Engineer** | Kernel, compiler, distributed-systems internals, ML systems, database engines. | C/C++/Rust, OS, perf eng, distributed-systems theory |
| **Embedded Engineer** | IoT, automotive, robotics, defense, edge AI. | C/C++, RTOS, hardware interfaces, low-level debugging |
| **Backend Engineer** | Server-side: APIs, services, databases, business logic. | language depth, API design, database modeling, system design |
| **Frontend Engineer** | Browser-side: components, state, routing, performance, a11y. | TS, React/Vue/Svelte, CSS, browser perf |
| **Full-Stack Engineer** | Spans frontend + backend. Most generalist engineering shape. | TS end-to-end, API design, DB basics, deployment |
| **iOS Engineer** | Native iOS in Swift/SwiftUI. | Swift, SwiftUI/UIKit, iOS architecture, App Store ops |
| **Android Engineer** | Native Android in Kotlin/Compose. | Kotlin, Jetpack Compose, Android architecture, Play Store ops |

---

## 6. Quality & Testing (3 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **SDET / Test Infrastructure** | Test frameworks, CI test infra, prod-like test envs. Converging with backend/platform eng. | test-framework design, CI/CD, IaC, API testing |
| **QA Automation** | Selenium/Cypress/Playwright. Compressing fastest of any engineering-adjacent role. | Selenium/Cypress/Playwright, scripting, test design |
| **QA Manual** | Hand-driven test execution against test plans. | test case design, exploratory testing, domain knowledge |

---

## 7. Product & Design (5 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **Technical Product Manager** | PM for technically-deep products: dev tools, AI features, infra, platforms. | technical depth, spec writing, API/data product design |
| **Product Manager** | Discovery, prioritization, requirements, roadmap. | customer research, prioritization, narrative writing |
| **UX Designer / Researcher** | Bundle of two roles (UX design + UX research). Splitting into separate tracks. | research methodology, synthesis, IA, interaction design |
| **Product Designer** | End-to-end: visual + interaction + systems thinking. | Figma, design systems, interaction design, FE literacy |
| **UI Designer** | Visual interface: layout, typography, color, component visuals. | Figma, visual design, typography, design systems |

---

## 8. Specialized & Emerging (3 roles)

| Role | One-line definition | Primary skills |
| --- | --- | --- |
| **Solutions Architect** | Customer-facing technical role at vendors / consultancies. Owns the deal-side narrative. | vendor product depth, customer-facing comm, POCs, pre-sales |
| **Developer Experience (DX) Engineer** | Builds SDK, CLI, docs, IDP, onboarding for developer-facing products. | API design, technical writing, tooling, product taste |
| **Prompt Engineer** | Standalone title focused on prompt design + tuning. Largely a 2023 artifact; absorbed into AI App / ML Eng work in 2025–26. | prompt design, evals, LLM literacy |

---

## Roles deliberately not separated

- **AI Engineer** vs. **ML Engineer** — "AI Engineer" is currently a marketing variant of either ML Engineer or AI Application Engineer depending on company. Tracking both creates double-count.
- **DevSecOps** — This is "DevOps engineer who knows security" or "Security engineer who knows DevOps" depending on team. Counted in either Security or DevOps based on the work, not the title.
- **FinOps Engineer** — Currently absorbed into Cloud Engineer. INSIGHTS.md flags it as a candidate to split out in the 2027 re-score.
- **MLOps** vs. **ML Platform** — Same role, different titles. MLOps is still the more common posting term in 2026; consolidating into "ML Platform Engineer" is the 2027–28 trajectory.
- **Design Engineer** — Counted under Product Designer with a "design engineer" sub-niche call-out in REPORT.md. Will likely split out by 2027.
- **AI Eval Engineer** — Currently absorbed into MLOps + AI Application Engineer; rising fast and may split out in 2027.

## Roles deliberately included even with predicted consolidation

- **Prompt Engineer** — kept because the title still appears on real job postings in 2026 (~160/month per simulated LinkedIn series), even though the analysis predicts the standalone title is gone by 2027.
- **AI Application Engineer** — kept because the title is the *fastest-growing* category in 2025–26 hiring, even though the long-term consolidation is into "Backend Engineer who knows LLMs."
- **Full-Stack Engineer** — kept despite generalist compression because the title is still the most common shape at sub-200-engineer companies in 2026.
- **DevOps Engineer** — kept despite slow decline because the title is still the most common infra-engineer shape outside FAANG.

---

## Where the taxonomy will likely change next

Forecast for the 2027 re-score (preview from the closing sections of [INSIGHTS.md](../INSIGHTS.md#10-what-to-update-in-the-rubric-for-2027)):

1. **Split UX Designer / Researcher into two rows.** Researcher half scores ~75; designer half scores ~60. The current bundled score of 67 hides a real gap.
2. **Add FinOps Engineer.** Demand-rising fast; currently inside Cloud Engineer.
3. **Add AI Eval Engineer.** Currently absorbed into MLOps + AI App; emerging as a distinct track.
4. **Possibly retire Prompt Engineer.** If 2026 postings continue toward zero, the row stops being informative.
5. **Possibly retire Cloud Engineer as a standalone.** Convergence into Platform + Cloud Security may complete by 2028.
