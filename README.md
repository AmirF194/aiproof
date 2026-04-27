# Which Tech Jobs Are Safe? A 2026–2035 Market Analysis

A practical comparison of six software engineering roles across demand, salary, automation risk, complexity, and 5–10 year stability.

> Scope: senior IC roles in North America / EU. Salaries are USD, total comp, mid-to-senior band. Numbers are directional — sourced from Levels.fyi, Stack Overflow 2025, BLS 2024–34 projections, LinkedIn Workforce Report Q4 2025, and Gartner AI-impact estimates. Treat as a frame for decisions, not a forecast.

---

## TL;DR — Career Safety Ranking (2026–2035)

| Rank | Role                  | Safety Score (/100) | Verdict                              |
|------|-----------------------|---------------------|--------------------------------------|
| 1    | AI/ML Engineer        | 91                  | Safest — riding the demand curve     |
| 2    | DevOps / Platform     | 84                  | Very safe — infra still needs humans |
| 3    | Backend Engineer      | 76                  | Safe — augmented, not replaced       |
| 4    | Mobile Developer      | 64                  | Stable but narrowing                 |
| 5    | Frontend Engineer     | 58                  | Pressured — heavily AI-augmentable   |
| 6    | QA Engineer           | 42                  | At risk — manual QA shrinking fast   |

See [SCORING.md](SCORING.md) for the rubric and [REPORT.md](REPORT.md) for per-role detail.

![Safety Score](charts/safety_score.svg)

---

## Headline conclusions

**1. The safest roles are the ones closest to systems, not screens.**
AI/ML, DevOps, and Backend rank highest because their work is grounded in distributed systems, data pipelines, infrastructure, and production reliability — domains where AI tools speed up *parts* of the job but cannot own the outcome. The risky end of the spectrum is the work AI tools can fully draft: UI scaffolding, test scripts from a spec, CRUD endpoints from a schema.

**2. "AI risk" ≠ "job loss." It means leverage shifts.**
Every role on this list will use AI tooling daily by 2028. The split is between roles where AI is a *force multiplier* (one engineer doing 2–3×) and roles where AI is a *replacement* (one engineer doing the work of three, so two go away). QA-manual and junior frontend are the clearest replacement zones; AI/ML and platform engineering are clear multiplier zones.

**3. QA is the role to plan an exit from.**
Manual QA shrinks the most over the decade. Automation QA survives but converges with backend/SDET work. If you are in QA today, the move is into SDET → backend or into AI-eval / model-QA, which is a genuinely growing niche.

**4. Frontend is not dying — it's bifurcating.**
Component-assembly frontend work compresses. But **design-system owners, accessibility specialists, and performance/animation engineers** stay in demand. The middle of the frontend market is the soft spot.

**5. Mobile is stable but flat.**
iOS/Android demand holds — every consumer company still needs apps — but headcount per app is dropping, and cross-platform (Flutter, React Native, Kotlin Multiplatform) keeps eating native specialist roles.

---

## How to use this

- **If you are choosing a first specialization:** go AI/ML, DevOps/Platform, or Backend. In that order if you want safety; reverse it if you want the lowest barrier to entry.
- **If you are mid-career and considering a switch:** the highest-leverage move is *adjacent*, not lateral. Backend → AI/ML infra. Frontend → design systems or DX tooling. QA → SDET or AI evaluation.
- **If you are hiring:** expect AI/ML and senior DevOps comp to keep climbing through 2028. Expect manual QA budgets to compress 30–50% by 2030.

---

## Files

- [REPORT.md](REPORT.md) — full per-role analysis
- [SCORING.md](SCORING.md) — rubric, weights, and the math behind the safety score
- [data/roles.csv](data/roles.csv) — raw scoring data
- [charts/](charts/) — SVG charts (safety score, demand, salary, automation risk)

---

## Methodology in one paragraph

Each role is scored 1–10 on five axes: **demand growth (2026→2035)**, **salary ceiling**, **automation resistance** (inverse of AI displacement risk), **skill moat** (how hard the role is to enter and stay current in), and **stability** (variance of demand across macro cycles). Axes are weighted — automation resistance and demand carry the most weight because they dominate 10-year outcomes. Final score is normalized to 0–100. Inputs are directional estimates, not survey data; the goal is a defensible frame, not a published index.

## Limitations

- North America / EU bias. India, LATAM, and SEA markets have different curves — mobile and frontend hold up longer there.
- Senior-IC framing. Junior-market dynamics are worse across the board because AI compresses the bottom of the ladder hardest.
- The 5–10 year window is long enough that a single foundation-model breakthrough (or a regulatory clamp) could re-rank these. Re-evaluate annually.
