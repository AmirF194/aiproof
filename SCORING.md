# Career Safety Scoring System

A simple, weighted rubric. Designed to be defensible and easy to re-run as conditions change.

## The five axes

Each role is scored 1–10 on:

| Axis                    | What it measures                                                                  | Weight |
|-------------------------|-----------------------------------------------------------------------------------|--------|
| Demand growth           | Projected change in role demand 2026 → 2035 (BLS + LinkedIn + private trackers).  | 25%    |
| Automation resistance   | Inverse of AI-displacement risk. 10 = AI augments; 1 = AI replaces.               | 30%    |
| Salary ceiling          | Senior-IC total comp ceiling, normalized.                                         | 15%    |
| Skill moat              | How hard the role is to enter and stay current in. Higher moat = more durable.    | 15%    |
| Cyclical stability      | Demand variance across macro cycles. 10 = recession-resistant.                    | 15%    |

**Why these weights**: automation resistance carries the most weight because it dominates the 10-year window — a high-demand role that AI fully automates is not safe. Demand is second because it sets the absolute floor on opportunity. Salary, moat, and cyclical stability are smaller but real.

Final score = `Σ (axis_score × weight) × 10`, normalized to a 0–100 range.

## The scores

| Role              | Demand | Auto-Resist | Salary | Moat | Cyclical | **Total /100** |
|-------------------|:------:|:-----------:|:------:|:----:|:--------:|:--------------:|
| AI/ML Engineer    | 10     | 10          | 10     | 9    | 6        | **91**         |
| DevOps / Platform | 8      | 9           | 8      | 8    | 9        | **84**         |
| Backend Engineer  | 7      | 7           | 7      | 7    | 9        | **76**         |
| Mobile Developer  | 6      | 6           | 7      | 7    | 7        | **64**         |
| Frontend Engineer | 6      | 4           | 6      | 6    | 7        | **58**         |
| QA Engineer       | 4      | 3           | 4      | 4    | 6        | **42**         |

Worked example (DevOps / Platform):
`(8×0.25) + (9×0.30) + (8×0.15) + (8×0.15) + (9×0.15) = 2.00 + 2.70 + 1.20 + 1.20 + 1.35 = 8.45 → 84`

Raw data is in [data/roles.csv](data/roles.csv) so you can re-weight if you disagree.

## How to interpret the score

- **85–100**: Safest tier. Build a career here without hedging.
- **70–84**: Safe at senior level. Junior path is harder than it used to be.
- **55–69**: Stable but specialize. Generalists in this band are exposed.
- **< 55**: Plan a transition. Not "doomed," but the wind is against you.

## What this score is *not*

- Not a salary predictor. Comp is one input.
- Not a fit assessment. The safest career you hate is still a bad career.
- Not a forecast. It's a frame for thinking about defensibility — the underlying data shifts annually.

Re-score yearly. If a single axis moves more than 2 points for any role, re-publish.
