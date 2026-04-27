# Per-Role Analysis (2026–2035)

Each role is evaluated on five dimensions: market demand, salary range, automation risk, skill complexity, and long-term stability. Scores feed into [SCORING.md](SCORING.md).

---

## 1. AI/ML Engineer

| Dimension          | Assessment                                                                 |
|--------------------|---------------------------------------------------------------------------|
| Market demand      | Highest of any role on this list. ~30% YoY growth in postings through 2027, plateau forecast 2029+. |
| Salary range (USD) | $180K – $450K total comp (senior IC, US). $700K+ at frontier labs.        |
| Automation risk    | Lowest. AI tools accelerate this role — they don't replace it.            |
| Skill complexity   | Highest. ML systems + production infra + research literacy.               |
| 5–10 yr stability  | Very strong. Risk is comp compression after 2030 as supply catches up.    |

**Key dynamics**
- Two sub-tracks are diverging: **applied ML / MLOps** (productionizing models, evals, RAG, agents) and **research / pretraining** (frontier labs only). Applied has 10× the headcount and is the safer bet.
- Compensation is currently distorted by frontier-lab bidding. Expect normalization 2028–2030 but still 1.5–2× backend baseline.
- Skill half-life is short — the stack you learn in 2026 will be partially obsolete by 2029. Continuous learning is the cost of admission.

**Risks**
- Foundation-model commoditization could collapse demand for in-house model training. Most AI/ML jobs by 2030 will be *integration*, not training.
- Regulatory drag (EU AI Act enforcement, sectoral rules in healthcare/finance) could slow hiring in regulated industries.

---

## 2. DevOps / Platform Engineer

| Dimension          | Assessment                                                                 |
|--------------------|---------------------------------------------------------------------------|
| Market demand      | Strong. Renaming to "platform engineering" and "SRE" continues; total headcount grows. |
| Salary range (USD) | $150K – $320K total comp (senior IC, US).                                  |
| Automation risk    | Low. AI accelerates IaC and incident triage but cannot own production.    |
| Skill complexity   | High. Distributed systems, networking, security, cost engineering.        |
| 5–10 yr stability  | Strong. Cloud spend keeps growing; someone has to own it.                 |

**Key dynamics**
- "DevOps engineer" as a title is fading; "platform engineer" and "SRE" are absorbing the work. Same job, better leverage.
- AI-driven ops (autoremediation, AI-assisted RCA) is the growth subniche. Engineers who own that integration are the most valuable.
- Kubernetes literacy remains table-stakes. Cost optimization (FinOps) is a fast-rising adjacent skill.

**Risks**
- Managed platforms (Vercel, Railway, Cloudflare Workers, fully-managed K8s) keep eating the bottom of the market. Junior DevOps roles compress.
- Heavy on-call burden continues to push talent toward adjacent roles.

---

## 3. Backend Engineer

| Dimension          | Assessment                                                                 |
|--------------------|---------------------------------------------------------------------------|
| Market demand      | Steady. Largest absolute headcount of any role here; growth is moderate.  |
| Salary range (USD) | $140K – $280K total comp (senior IC, US).                                  |
| Automation risk    | Moderate. AI drafts code well; system design and ownership remain human.  |
| Skill complexity   | Moderate-to-high. Varies wildly by domain (CRUD vs. distributed systems). |
| 5–10 yr stability  | Strong at senior level. Junior backend market is the most compressed.     |

**Key dynamics**
- The role bifurcates: **systems backend** (databases, distributed systems, latency-sensitive infra) is safe and well-paid; **CRUD backend** (REST endpoints, glue code) is heavily AI-augmentable and will see headcount compression.
- Senior backend engineers who can do system design + own a service end-to-end stay in high demand. The ladder gets steeper because the bottom rungs erode.
- Languages don't matter much for safety — domain depth does. Payments, search, real-time, ML infra: all defensible niches.

**Risks**
- Junior hiring contracts hard. Path-to-senior takes longer because AI tools do the easy work that used to be junior training ground.
- Offshore + AI compounds: the same code that gets generated also gets reviewed cheaper.

---

## 4. Mobile Developer (iOS/Android)

| Dimension          | Assessment                                                                 |
|--------------------|---------------------------------------------------------------------------|
| Market demand      | Stable but flat. Per-app headcount declining; total headcount roughly flat. |
| Salary range (USD) | $135K – $260K total comp (senior IC, US).                                  |
| Automation risk    | Moderate. UI generation is a real threat; platform-native depth is not.   |
| Skill complexity   | Moderate. Higher for native (Swift/Kotlin); lower for cross-platform.     |
| 5–10 yr stability  | OK, with pressure. Native specialists hold value; generalists compress.   |

**Key dynamics**
- Cross-platform (Flutter, React Native, Kotlin Multiplatform, Compose Multiplatform) keeps gaining share. By 2030, expect ~60% of new mobile work to be cross-platform.
- Native-only roles consolidate at large consumer companies (Meta, Google, Uber, banks). Mid-market mobile teams shrink.
- Apple's Swift+SwiftUI maturity and Google's KMP push are squeezing the middle: either you're deep on platform internals, or you're using a cross-platform framework.

**Risks**
- AI design-to-code tools (Vercel v0-style for mobile) compress UI work.
- App-store consolidation and the rise of mobile web / PWAs nibble at native demand for content-heavy apps.

---

## 5. Frontend Engineer

| Dimension          | Assessment                                                                 |
|--------------------|---------------------------------------------------------------------------|
| Market demand      | Compressing. Total postings down ~15% from 2024 peak; senior demand stable. |
| Salary range (USD) | $120K – $230K total comp (senior IC, US).                                  |
| Automation risk    | High. Component scaffolding, layout, and styling are AI-native tasks.     |
| Skill complexity   | Moderate. Easy entry, hard mastery (perf, a11y, design systems).          |
| 5–10 yr stability  | Mixed. Specialists thrive; generalist "React dev" role is the soft spot.  |

**Key dynamics**
- AI tooling (v0, Cursor, Copilot) reliably produces working components from prompts. The work that compresses is exactly the work that defined "frontend developer" 2018–2024.
- The roles that survive and grow: **design-system engineers**, **accessibility specialists**, **performance engineers**, **DX/tooling engineers**. These require taste, deep platform knowledge, or cross-cutting concerns AI can't synthesize.
- Full-stack TypeScript ("Next.js engineer") is the dominant survivor of the generalist track — frontend skills + backend literacy travel further than either alone.

**Risks**
- The bottom of the ladder collapses fastest here. Bootcamp-to-junior-frontend is no longer a reliable path.
- Design-tool encroachment (Figma → code, Framer, Builder.io) accelerates.

---

## 6. QA Engineer (manual + automation)

| Dimension          | Assessment                                                                 |
|--------------------|---------------------------------------------------------------------------|
| Market demand      | Declining for manual; flat-to-up for SDET / automation.                   |
| Salary range (USD) | $80K – $180K total comp (senior IC, US). Wide variance.                   |
| Automation risk    | Highest of any role here. Manual QA is the textbook AI-replacement case.  |
| Skill complexity   | Low to moderate. SDET requires real engineering; manual QA does not.      |
| 5–10 yr stability  | Weak overall. SDET path is OK; manual QA is a shrinking field.            |

**Key dynamics**
- LLM-based test generation, visual-regression AI, and self-healing E2E frameworks are mature enough to replace meaningful portions of manual QA work by 2027.
- SDET (Software Development Engineer in Test) survives and converges with backend engineering. The skills overlap so much that "QA" as a separate org is fading at well-run companies.
- A genuinely growing niche: **AI evaluation engineers** — building eval harnesses, red-teaming models, benchmarking. This is QA reborn for the AI era and pays like ML-adjacent work.

**Risks**
- Offshore QA centers, which absorbed much of the work in the 2010s, are the first to be AI-displaced.
- Career mobility out of pure QA is harder than out of any other role here. Plan the transition early.

**Recommended transitions out of QA**
1. SDET → backend engineer (most natural; ~12 months of focused study)
2. QA → AI evaluation engineer (best upside; requires Python + ML literacy)
3. QA → DevOps / release engineering (good fit for QA-leaning automation people)

---

## Cross-cutting patterns

- **Automation pressure is bottom-up.** Junior and routine work compresses fastest in every role. The senior end is largely safe — for now.
- **Specialization beats breadth in 2026–2030.** The "full-stack generalist" identity that worked in 2018 is the most exposed shape today. Pick a moat: a domain (payments, ML infra, real-time), a skill (perf, a11y, security), or a platform (deep iOS, deep K8s).
- **Stability tracks distance from the UI.** The further from the screen, the more durable the role: AI/ML infra > backend systems > DevOps > backend CRUD > mobile > frontend > QA.
- **AI literacy is now a baseline skill in every role.** By 2027, "doesn't use AI tools effectively" will be a hiring red flag in all six roles.
