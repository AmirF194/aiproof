#!/usr/bin/env python3
"""Generate the SVG charts under charts/ from data/roles.csv.

No third-party dependencies. Produces four charts:
  - charts/safety_score.svg     : full ranking, horizontal bars, color-coded by tier
  - charts/automation_risk.svg  : demand vs automation-resistance quadrant
  - charts/salary_range.svg     : senior-IC salary band for top + bottom roles
  - charts/demand_growth.svg    : category-average safety score
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DATA = REPO / "data" / "roles.csv"
OUT = REPO / "charts"

TIER_COLOR = {
    "fortress": "#1f7a3a",   # dark green
    "safe":     "#4caf50",   # green
    "stable":   "#f0a30a",   # amber
    "exposed":  "#e57321",   # orange
    "at_risk":  "#c62828",   # red
}

CATEGORY_ORDER = [
    "Engineering Leadership",
    "Security",
    "Data & AI",
    "Platform & Infrastructure",
    "Specialized & Emerging",
    "Engineering",
    "Product & Design",
    "Quality & Testing",
]


def load_rows():
    with DATA.open() as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("demand", "automation_resistance", "skill_depth",
                  "strategic_importance", "score",
                  "salary_low_usd", "salary_high_usd"):
            r[k] = int(r[k])
    return rows


def svg_open(width, height, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="-apple-system, Segoe UI, Roboto, sans-serif" '
        f'font-size="12" role="img" aria-label="{title}">\n'
        f'<rect width="100%" height="100%" fill="#ffffff"/>\n'
    )


def svg_close():
    return "</svg>\n"


def text(x, y, s, *, size=12, color="#222", weight="normal", anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{s}</text>\n')


def rect(x, y, w, h, fill, *, stroke=None, rx=0):
    s = f' stroke="{stroke}"' if stroke else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{s}{r}/>\n'


def line(x1, y1, x2, y2, stroke="#cccccc", width=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{width}"{d}/>\n')


def chart_safety_score(rows):
    rows = sorted(rows, key=lambda r: r["score"], reverse=True)
    n = len(rows)
    margin_l, margin_r, margin_t, margin_b = 230, 60, 80, 40
    bar_h = 18
    gap = 6
    plot_w = 600
    width = margin_l + plot_w + margin_r
    height = margin_t + n * (bar_h + gap) + margin_b

    out = [svg_open(width, height, "Career Safety Score by Role")]
    out.append(text(margin_l, 32, "Career Safety Score by Role  (2026–2035)",
                    size=18, weight="bold"))
    out.append(text(margin_l, 52,
                    "Higher = more durable.  Score = 0.30·Demand + 0.35·AutoResist + 0.15·SkillDepth + 0.20·StrategicImportance",
                    size=11, color="#555"))

    # x grid
    for v in (0, 25, 50, 75, 100):
        x = margin_l + plot_w * v / 100
        out.append(line(x, margin_t, x, height - margin_b, stroke="#eeeeee"))
        out.append(text(x, margin_t - 6, str(v), size=10, color="#888", anchor="middle"))

    # tier guide bands (subtle)
    tiers = [(85, 100, "#1f7a3a"), (70, 85, "#4caf50"),
             (55, 70, "#f0a30a"), (40, 55, "#e57321"), (0, 40, "#c62828")]
    for lo, hi, c in tiers:
        x1 = margin_l + plot_w * lo / 100
        x2 = margin_l + plot_w * hi / 100
        out.append(rect(x1, height - margin_b, x2 - x1, 4, c, rx=0))

    for i, r in enumerate(rows):
        y = margin_t + i * (bar_h + gap)
        w = plot_w * r["score"] / 100
        color = TIER_COLOR[r["verdict_tier"]]
        out.append(text(margin_l - 10, y + bar_h - 4, r["role"],
                        size=12, anchor="end"))
        out.append(rect(margin_l, y, w, bar_h, color, rx=2))
        out.append(text(margin_l + w + 6, y + bar_h - 4, str(r["score"]),
                        size=11, color="#333"))

    # legend
    legend_y = height - margin_b + 20
    legend_items = [
        ("Fortress (85+)", "#1f7a3a"),
        ("Safe (70–84)",   "#4caf50"),
        ("Stable (55–69)", "#f0a30a"),
        ("Exposed (40–54)","#e57321"),
        ("At risk (<40)",  "#c62828"),
    ]
    lx = margin_l
    for label, col in legend_items:
        out.append(rect(lx, legend_y - 10, 12, 12, col, rx=2))
        out.append(text(lx + 18, legend_y, label, size=11, color="#333"))
        lx += 130

    out.append(svg_close())
    (OUT / "safety_score.svg").write_text("".join(out))


def chart_automation_risk(rows):
    width, height = 880, 620
    margin_l, margin_r, margin_t, margin_b = 70, 30, 80, 60
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    out = [svg_open(width, height, "Demand vs Automation Resistance")]
    out.append(text(margin_l, 32,
                    "Demand vs Automation Resistance  (2026–2035)",
                    size=18, weight="bold"))
    out.append(text(margin_l, 52,
                    "Top-right = high demand AND hard to automate (the safest quadrant).",
                    size=11, color="#555"))

    # axes
    out.append(line(margin_l, margin_t, margin_l, height - margin_b, stroke="#333", width=1))
    out.append(line(margin_l, height - margin_b, width - margin_r, height - margin_b, stroke="#333", width=1))

    # mid lines
    mid_x = margin_l + plot_w * 5 / 10
    mid_y = margin_t + plot_h * (10 - 5) / 10
    out.append(line(mid_x, margin_t, mid_x, height - margin_b, stroke="#bbbbbb", dash="4 4"))
    out.append(line(margin_l, mid_y, width - margin_r, mid_y, stroke="#bbbbbb", dash="4 4"))

    # quadrant labels
    out.append(text(width - margin_r - 10, margin_t + 16, "Safest", size=14, color="#1f7a3a", weight="bold", anchor="end"))
    out.append(text(margin_l + 10, margin_t + 16, "Niche / specialist", size=14, color="#0277bd", weight="bold"))
    out.append(text(width - margin_r - 10, height - margin_b - 8, "High demand but exposed", size=14, color="#e57321", weight="bold", anchor="end"))
    out.append(text(margin_l + 10, height - margin_b - 8, "Most at risk", size=14, color="#c62828", weight="bold"))

    # axis ticks
    for v in range(0, 11, 2):
        x = margin_l + plot_w * v / 10
        out.append(line(x, height - margin_b, x, height - margin_b + 4, stroke="#333"))
        out.append(text(x, height - margin_b + 18, str(v), size=10, color="#444", anchor="middle"))
        y = margin_t + plot_h * (10 - v) / 10
        out.append(line(margin_l - 4, y, margin_l, y, stroke="#333"))
        out.append(text(margin_l - 8, y + 4, str(v), size=10, color="#444", anchor="end"))

    # axis titles
    out.append(text(margin_l + plot_w / 2, height - 14, "Automation Resistance  (10 = AI cannot replace)",
                    size=12, color="#333", anchor="middle"))
    out.append(f'<text x="{margin_l - 44}" y="{margin_t + plot_h / 2}" '
               f'font-size="12" fill="#333" '
               f'transform="rotate(-90 {margin_l - 44} {margin_t + plot_h / 2})" '
               f'text-anchor="middle">Market Demand  (10 = strongest)</text>\n')

    # plot points (jitter colliding ones)
    placed = []
    for r in rows:
        cx = margin_l + plot_w * r["automation_resistance"] / 10
        cy = margin_t + plot_h * (10 - r["demand"]) / 10
        # tiny jitter if collision
        jitter = 0
        for px, py in placed:
            if abs(px - cx) < 6 and abs(py - cy) < 6:
                jitter += 8
        cx += jitter
        placed.append((cx, cy))
        color = TIER_COLOR[r["verdict_tier"]]
        out.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{color}" '
                   f'fill-opacity="0.85" stroke="#ffffff" stroke-width="1.2"/>\n')
        # label only the most informative roles to avoid clutter
        notable = {
            "Staff Engineer / Tech Lead", "Security Engineer", "ML Engineer",
            "Platform Engineer", "AI Research Engineer", "AI Application Engineer",
            "Backend Engineer", "Frontend Engineer", "QA Manual",
            "Data Analyst", "Prompt Engineer", "Data Engineer",
            "Site Reliability Engineer", "Engineering Manager",
            "Systems / Low-level Engineer", "DevOps Engineer",
        }
        if r["role"] in notable:
            anchor = "start" if r["automation_resistance"] <= 7 else "end"
            dx = 9 if anchor == "start" else -9
            out.append(text(cx + dx, cy + 4, r["role"], size=10, color="#222", anchor=anchor))

    out.append(svg_close())
    (OUT / "automation_risk.svg").write_text("".join(out))


def chart_salary_range(rows):
    # representative slice: top 8 + middle 4 + bottom 6, in score order
    s = sorted(rows, key=lambda r: r["score"], reverse=True)
    sample = s[:8] + s[len(s)//2 - 2: len(s)//2 + 2] + s[-6:]
    sample = sorted(sample, key=lambda r: r["salary_high_usd"], reverse=True)

    margin_l, margin_r, margin_t, margin_b = 240, 100, 80, 40
    bar_h = 18
    gap = 8
    plot_w = 540
    width = margin_l + plot_w + margin_r
    height = margin_t + len(sample) * (bar_h + gap) + margin_b

    max_high = max(r["salary_high_usd"] for r in sample)
    # round up scale to nearest 100k
    scale_max = ((max_high // 100000) + 1) * 100000

    out = [svg_open(width, height, "Senior-IC Salary Range")]
    out.append(text(margin_l, 32, "Senior-IC Salary Range by Role  (USD, US market)",
                    size=18, weight="bold"))
    out.append(text(margin_l, 52,
                    "Bar = junior → senior total comp.  Frontier-lab outliers excluded.",
                    size=11, color="#555"))

    # x grid
    for v in range(0, scale_max + 1, 100000):
        x = margin_l + plot_w * v / scale_max
        out.append(line(x, margin_t, x, height - margin_b, stroke="#eeeeee"))
        out.append(text(x, margin_t - 6, f"${v//1000}K", size=10, color="#888", anchor="middle"))

    for i, r in enumerate(sample):
        y = margin_t + i * (bar_h + gap)
        x_lo = margin_l + plot_w * r["salary_low_usd"] / scale_max
        x_hi = margin_l + plot_w * r["salary_high_usd"] / scale_max
        color = TIER_COLOR[r["verdict_tier"]]
        out.append(text(margin_l - 10, y + bar_h - 4, r["role"],
                        size=12, anchor="end"))
        out.append(rect(x_lo, y + 3, x_hi - x_lo, bar_h - 6, color, rx=2))
        # endpoints
        out.append(f'<circle cx="{x_lo}" cy="{y + bar_h/2}" r="3" fill="#222"/>\n')
        out.append(f'<circle cx="{x_hi}" cy="{y + bar_h/2}" r="3" fill="#222"/>\n')
        label = f'${r["salary_low_usd"]//1000}K – ${r["salary_high_usd"]//1000}K'
        out.append(text(x_hi + 8, y + bar_h - 4, label, size=11, color="#333"))

    out.append(svg_close())
    (OUT / "salary_range.svg").write_text("".join(out))


def chart_demand_growth(rows):
    # Category-average safety score, plus median demand score
    cats = {}
    for r in rows:
        cats.setdefault(r["category"], []).append(r)

    items = []
    for cat in CATEGORY_ORDER:
        bucket = cats.get(cat, [])
        if not bucket:
            continue
        avg_score = sum(b["score"] for b in bucket) / len(bucket)
        avg_demand = sum(b["demand"] for b in bucket) / len(bucket)
        items.append((cat, avg_score, avg_demand, len(bucket)))

    items.sort(key=lambda x: x[1], reverse=True)

    margin_l, margin_r, margin_t, margin_b = 230, 100, 90, 50
    bar_h = 28
    gap = 14
    plot_w = 520
    width = margin_l + plot_w + margin_r
    height = margin_t + len(items) * (bar_h + gap) + margin_b

    out = [svg_open(width, height, "Category Averages")]
    out.append(text(margin_l, 32, "Average Safety Score by Job Category",
                    size=18, weight="bold"))
    out.append(text(margin_l, 52,
                    "Bar = avg safety score (0–100).  Dot = avg demand score (1–10, scaled).",
                    size=11, color="#555"))

    for v in (0, 25, 50, 75, 100):
        x = margin_l + plot_w * v / 100
        out.append(line(x, margin_t, x, height - margin_b, stroke="#eeeeee"))
        out.append(text(x, margin_t - 6, str(v), size=10, color="#888", anchor="middle"))

    for i, (cat, avg_s, avg_d, n) in enumerate(items):
        y = margin_t + i * (bar_h + gap)
        w = plot_w * avg_s / 100
        # tier color by avg score
        if avg_s >= 85: c = "#1f7a3a"
        elif avg_s >= 70: c = "#4caf50"
        elif avg_s >= 55: c = "#f0a30a"
        elif avg_s >= 40: c = "#e57321"
        else: c = "#c62828"
        out.append(text(margin_l - 10, y + bar_h - 8, f"{cat}  (n={n})",
                        size=12, anchor="end"))
        out.append(rect(margin_l, y, w, bar_h, c, rx=3))
        out.append(text(margin_l + w + 8, y + bar_h - 8,
                        f"{avg_s:.1f}", size=12, color="#333", weight="bold"))
        # demand dot
        dx = margin_l + plot_w * (avg_d * 10) / 100
        out.append(f'<circle cx="{dx}" cy="{y + bar_h + 4}" r="4" fill="#0277bd"/>\n')
        out.append(text(dx + 8, y + bar_h + 8,
                        f"demand {avg_d:.1f}/10", size=10, color="#0277bd"))

    out.append(svg_close())
    (OUT / "demand_growth.svg").write_text("".join(out))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    chart_safety_score(rows)
    chart_automation_risk(rows)
    chart_salary_range(rows)
    chart_demand_growth(rows)
    print(f"Wrote {len(list(OUT.glob('*.svg')))} charts to {OUT}")


if __name__ == "__main__":
    main()
