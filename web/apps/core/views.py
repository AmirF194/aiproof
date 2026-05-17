from pathlib import Path

from django.conf import settings
from django.db.models import Avg, Count
from django.http import FileResponse, Http404
from django.shortcuts import render

from apps.roles.models import Category, Role, TIER_ORDER, TIER_LABELS, TIER_BLURBS

from .sources import SOURCES


# Allowlist of CSVs that the public can download from the processed data dir.
_DOWNLOADABLE = {
    "role_ranking.csv": "processed",
    "category_summary.csv": "processed",
    "tier_summary.csv": "processed",
    "role_postings_live.csv": "processed",
    "roles.csv": "root",
}


def home(request):
    from django.db.models import Max, Sum

    from apps.roles.models import RoleMetric
    from .sources import SOURCES

    tier_rows = (
        Role.objects.values("tier")
        .annotate(n=Count("id"), avg_score=Avg("score"))
        .order_by()
    )
    tier_map = {row["tier"]: row for row in tier_rows}
    tiers = [
        {
            "key": key,
            "label": TIER_LABELS[key],
            "blurb": TIER_BLURBS[key],
            "n": tier_map.get(key, {}).get("n", 0),
            "avg_score": tier_map.get(key, {}).get("avg_score") or 0,
        }
        for key in TIER_ORDER
    ]

    top_10 = Role.objects.order_by("-score", "role")[:10]
    bottom_10 = Role.objects.order_by("score", "role")[:10]

    total = Role.objects.count()
    categories = Category.objects.order_by("name")

    # --- Hero stats strip ---
    live_postings_total = (
        RoleMetric.objects.aggregate(s=Sum("postings_2026_current"))["s"] or 0
    )
    n_live_roles = RoleMetric.objects.filter(postings_2026_current__gt=0).count()
    last_updated = Role.objects.aggregate(m=Max("last_updated"))["m"]

    # --- Role-family aggregates ---
    family_rows = (
        Role.objects
        .exclude(role_family="")
        .values("role_family")
        .annotate(n=Count("id"), avg_score=Avg("score"))
        .order_by("-n")[:8]
    )
    role_families = list(family_rows)

    # --- Source feed grid ---
    featured_sources = [s for s in SOURCES if s.access == "api"][:8]

    return render(
        request,
        "core/home.html",
        {
            "tiers": tiers,
            "top_10": top_10,
            "bottom_10": bottom_10,
            "total": total,
            "categories": categories,
            "live_postings_total": live_postings_total,
            "n_live_roles": n_live_roles,
            "n_dimensions": 8,
            "last_updated": last_updated,
            "role_families": role_families,
            "featured_sources": featured_sources,
            "page_title": "AIProof — career-intelligence platform · 1,000 tech roles scored for AI resilience",
            "page_description": "AIProof is a career-intelligence platform by FastInfer that ranks 1,000 technology roles by their expected resilience to AI automation over 2026–2035. Eight scoring dimensions, weekly-refreshed live posting signals, full methodology and limitations published.",
        },
    )


def about(request):
    return render(
        request,
        "core/about.html",
        {
            "page_title": "About — AIProof career-intelligence platform · FastInfer",
            "page_description": "AIProof is FastInfer's open analytical framework for tech-career durability under AI automation. 1,000 roles, 8 score dimensions, weekly live data, transparent methodology.",
        },
    )


ACCESS_LABELS = {
    "api": "Public API",
    "public_scrape": "Public scrape",
    "annual_report": "Annual report",
    "manual": "Manual snapshot",
    "paid_excerpt": "Paid (public excerpt only)",
}


def sources(request):
    grouped: dict[str, list] = {}
    for s in SOURCES:
        grouped.setdefault(ACCESS_LABELS.get(s.access, s.access), []).append(s)
    return render(
        request,
        "core/sources.html",
        {
            "groups": grouped,
            "n_sources": len(SOURCES),
            "page_title": f"Sources & citations — {len(SOURCES)} feeds behind AIProof",
            "page_description": "BLS, O*NET, Hacker News, Greenhouse, Lever, The Muse, Remotive, Stack Overflow Survey, GitHub Octoverse, ISC2, Levels.fyi, layoffs.fyi — every source AIProof crawls, with URLs, licences, and last-fetched dates.",
        },
    )


COMPARE_AXES: list[tuple[str, str, str]] = [
    ("demand",                          "Market demand",              "#0ea5e9"),
    ("automation_resistance",           "Automation resistance",      "#10b981"),
    ("skill_depth",                     "Skill depth",                "#8b5cf6"),
    ("strategic_importance",            "Strategic importance",       "#f59e0b"),
    ("human_judgment_score",            "Human judgment",             "#06b6d4"),
    ("stakeholder_interaction_score",   "Stakeholder interaction",    "#ec4899"),
    ("ai_augmentation_potential_score", "AI augmentation potential",  "#f97316"),
    ("regulatory_relevance_score",      "Regulatory relevance",       "#6366f1"),
]


def compare(request):
    """Side-by-side comparison of 2–4 roles."""
    raw = request.GET.get("roles", "").strip()
    slugs = [s.strip() for s in raw.split(",") if s.strip()][:4]

    roles = list(
        Role.objects
        .select_related("category", "metrics")
        .filter(slug__in=slugs)
    )
    # Preserve user's ordering from the query string.
    roles.sort(key=lambda r: slugs.index(r.slug))

    rows = []
    for axis_attr, label, color in COMPARE_AXES:
        values = [getattr(r, axis_attr) or 0 for r in roles]
        rows.append({
            "label": label,
            "color": color,
            "values": values,
            "best": max(values) if values else 0,
        })

    titles = ", ".join(r.role for r in roles) if roles else "roles"
    return render(
        request,
        "core/compare.html",
        {
            "roles": roles,
            "rows": rows,
            "slugs_csv": ",".join(slugs),
            "n_valid": len(roles),
            "n_requested": len(slugs),
            "page_title": f"Compare {titles} — AIProof side-by-side career profiles",
            "page_description": "Compare 2–4 tech roles side-by-side on AI-proof score, 8 sub-dimensions, tier, salary, and live posting signals.",
        },
    )


def limitations(request):
    return render(
        request,
        "core/limitations.html",
        {
            "page_title": "Limitations — what AIProof is and isn't · AIProof",
            "page_description": "AIProof scores are calibrated estimates, not forecasts. Read the seven limitations — measurement vs. estimate, labour-market drift, AI capability drift, title noise, geographic and seniority bias, and what the score is not.",
        },
    )


def data_policy(request):
    return render(
        request,
        "core/data_policy.html",
        {
            "page_title": "Data policy — refresh cadence, ethics, takedowns · AIProof",
            "page_description": "What AIProof collects, where it comes from, how often it refreshes, crawler ethics, takedown process, CC BY 4.0 licence.",
        },
    )


def data_download(request, filename: str):
    """Stream a curated CSV from data/{processed,raw}/ as an attachment."""
    location = _DOWNLOADABLE.get(filename)
    if location is None:
        raise Http404
    if location == "processed":
        path = Path(settings.PROCESSED_DIR) / filename
    elif location == "root":
        path = Path(settings.DATA_DIR) / filename
    else:
        raise Http404
    if not path.is_file():
        raise Http404
    return FileResponse(path.open("rb"), as_attachment=True, filename=filename)
