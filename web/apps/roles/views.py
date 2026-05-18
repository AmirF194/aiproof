from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from . import scoring
from .models import (
    TIER_BLURBS,
    TIER_COLORS,
    TIER_LABELS,
    TIER_ORDER,
    TREND_LABELS,
    Category,
    Role,
)

# label, db field expression for ordering. Sub-score sorts are descending.
SORT_FIELDS: dict[str, tuple[str, str]] = {
    "rank":        ("Rank (top first)",                "rank"),
    "score":       ("Overall score (high → low)",      "-score"),
    "score_asc":   ("Overall score (low → high)",      "score"),
    "role":        ("Role name (A → Z)",               "role"),
    "salary":      ("Salary (high → low)",             "-salary_high_usd"),
    "demand":      ("Demand (high → low)",             "-demand"),
    "automation_resistance":           ("Automation resistance (high → low)", "-automation_resistance"),
    "skill_depth":                     ("Skill depth (high → low)",           "-skill_depth"),
    "strategic_importance":            ("Strategic importance (high → low)",  "-strategic_importance"),
    "human_judgment_score":            ("Human judgment (high → low)",        "-human_judgment_score"),
    "stakeholder_interaction_score":   ("Stakeholder interaction (high → low)", "-stakeholder_interaction_score"),
    "ai_augmentation_potential_score": ("AI augmentation potential (high → low)", "-ai_augmentation_potential_score"),
    "regulatory_relevance_score":      ("Regulatory relevance (high → low)",  "-regulatory_relevance_score"),
    "confidence":  ("Confidence (high → low)",          "-confidence_score"),
}


def _filter_roles(request):
    qs = Role.objects.select_related("category", "metrics").all()

    q = request.GET.get("q", "").strip()
    tier = request.GET.get("tier", "").strip()
    category = request.GET.get("category", "").strip()
    trend = request.GET.get("trend", "").strip()
    seniority = request.GET.get("seniority", "").strip()
    family = request.GET.get("family", "").strip()
    sort = request.GET.get("sort", "rank").strip()

    if q:
        qs = qs.filter(Q(role__icontains=q) | Q(category__name__icontains=q) | Q(notes__icontains=q))
    if tier in TIER_ORDER:
        qs = qs.filter(tier=tier)
    if category:
        qs = qs.filter(category__slug=category)
    if trend in TREND_LABELS:
        qs = qs.filter(demand_trend=trend)
    if seniority in scoring.SENIORITY_ORDER:
        qs = qs.filter(seniority_level=seniority)
    if family:
        qs = qs.filter(role_family=family)

    order_field = SORT_FIELDS.get(sort, SORT_FIELDS["rank"])[1]
    qs = qs.order_by(order_field, "role")

    return qs, {
        "q": q,
        "tier": tier,
        "category": category,
        "trend": trend,
        "seniority": seniority,
        "family": family,
        "sort": sort,
    }


def _paginate(qs, request, per_page: int = 100):
    paginator = Paginator(qs, per_page)
    page_number = request.GET.get("page") or 1
    try:
        page = paginator.page(page_number)
    except Exception:  # InvalidPage / EmptyPage / PageNotAnInteger
        page = paginator.page(1)
    return page, paginator


def _family_options() -> list[str]:
    return list(
        Role.objects
        .exclude(role_family="")
        .values_list("role_family", flat=True)
        .order_by("role_family")
        .distinct()
    )


def _sort_options() -> list[dict]:
    return [{"key": k, "label": v[0]} for k, v in SORT_FIELDS.items()]


def ranking(request):
    qs, params = _filter_roles(request)
    page, paginator = _paginate(qs, request, per_page=100)
    categories = Category.objects.order_by("name")
    tiers = [
        {"key": k, "label": TIER_LABELS[k], "color": TIER_COLORS[k]}
        for k in TIER_ORDER
    ]
    trends = [{"key": k, "label": v} for k, v in TREND_LABELS.items()]
    return render(
        request,
        "roles/ranking.html",
        {
            "roles": page.object_list,
            "page": page,
            "paginator": paginator,
            "total": paginator.count,
            "categories": categories,
            "tiers": tiers,
            "trends": trends,
            "seniorities": scoring.SENIORITY_ORDER,
            "families": _family_options(),
            "sort_options": _sort_options(),
            "params": params,
            "page_title": "Full ranking — 1,000+ tech roles scored for AI resilience · AIProof",
            "page_description": "Browse the full AIProof ranking of 1,000+ tech roles. Filter by tier, category, trend, seniority, and role family. Sort by any of 8 score dimensions. Tick up to 4 to compare side-by-side.",
        },
    )


def ranking_table(request):
    """HTMX partial: just the table body + meta."""
    qs, params = _filter_roles(request)
    page, paginator = _paginate(qs, request, per_page=100)
    return render(
        request,
        "roles/_ranking_table.html",
        {
            "roles": page.object_list,
            "page": page,
            "paginator": paginator,
            "total": paginator.count,
            "params": params,
        },
    )


def _score_vector(r: Role) -> tuple[int, ...]:
    """8-dimensional score vector used for adjacent-role similarity."""
    return (
        r.demand or 0,
        r.automation_resistance or 0,
        r.skill_depth or 0,
        r.strategic_importance or 0,
        r.human_judgment_score or 0,
        r.stakeholder_interaction_score or 0,
        r.ai_augmentation_potential_score or 0,
        r.regulatory_relevance_score or 0,
    )


def _adjacent_roles(role: Role, n: int = 3) -> list[Role]:
    """Closest n roles to `role` by Euclidean distance over the 8-axis score vector.

    Restricted to the same category (so adjacents are realistic career neighbours,
    not just numerically similar). Fall back to the wider catalogue if the category
    has fewer than n+1 roles.
    """
    candidates = (
        Role.objects.select_related("category")
        .filter(category=role.category)
        .exclude(pk=role.pk)
    )
    if candidates.count() < n:
        candidates = (
            Role.objects.select_related("category")
            .exclude(pk=role.pk)
        )
    target = _score_vector(role)

    def dist_sq(other: Role) -> int:
        ov = _score_vector(other)
        return sum((a - b) ** 2 for a, b in zip(target, ov, strict=True))

    return sorted(candidates, key=dist_sq)[:n]


def role_detail(request, slug):
    role = get_object_or_404(
        Role.objects.select_related("category", "metrics"), slug=slug
    )
    adjacent = _adjacent_roles(role, n=3)
    peers = (
        Role.objects.filter(category=role.category)
        .exclude(pk=role.pk)
        .order_by("-score")[:6]
    )

    # Score breakdown: ordered list of (label, value, color_hex) for the chart.
    breakdown = [
        ("Market demand",                  role.demand,                              "#0ea5e9"),
        ("Automation resistance",          role.automation_resistance,               "#10b981"),
        ("Skill depth",                    role.skill_depth,                         "#8b5cf6"),
        ("Strategic importance",           role.strategic_importance,                "#f59e0b"),
        ("Human judgment",                 role.human_judgment_score or 0,           "#06b6d4"),
        ("Stakeholder interaction",        role.stakeholder_interaction_score or 0,  "#ec4899"),
        ("AI augmentation potential",      role.ai_augmentation_potential_score or 0,"#f97316"),
        ("Regulatory relevance",           role.regulatory_relevance_score or 0,     "#6366f1"),
    ]

    # Deterministic role enrichment — selected by (role_family, category, seniority);
    # see scoring.py and METHODOLOGY.md#role-enrichment.
    family = role.role_family or ""
    category_name = role.category.name
    seniority = role.seniority_level or "Mid"
    enrichment = {
        "overview":          scoring.role_overview(family, category_name, seniority),
        "responsibilities":  scoring.role_responsibilities(family, category_name),
        "tools":             scoring.role_typical_tools(family, category_name),
        "day_to_day":        scoring.role_day_to_day(family, category_name),
        "ai_impact":         scoring.role_ai_impact(family, category_name),
    }

    page_title = (
        f"{role.role} — AI-proof score {role.score}/100 ({role.tier_label}) · AIProof"
    )
    notes_excerpt = (role.notes or "").strip()
    if len(notes_excerpt) > 140:
        notes_excerpt = notes_excerpt[:137].rstrip() + "..."
    page_description = (
        f"{role.role}: AI-proof score {role.score}/100, "
        f"{role.tier_label.lower()} tier. {notes_excerpt} "
        f"Full 8-dimension breakdown, live posting signals, and adjacent roles."
    ).strip()

    return render(
        request,
        "roles/detail.html",
        {
            "role": role,
            "adjacent": adjacent,
            "peers": peers,
            "breakdown": breakdown,
            "enrichment": enrichment,
            "tier_blurb": TIER_BLURBS.get(role.tier, ""),
            "page_title": page_title,
            "page_description": page_description,
        },
    )


def category_index(request):
    categories = Category.objects.order_by("-avg_score")
    return render(
        request,
        "roles/categories.html",
        {
            "categories": categories,
            "page_title": "Categories — 8 role families ranked for AI resilience · AIProof",
            "page_description": "Eight categories spanning software, AI, data, security, platform, product, design, and quality testing — ranked by average AI-proof score across the 1,000+ role dataset.",
        },
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    roles = category.roles.order_by("-score", "role")
    return render(
        request,
        "roles/category_detail.html",
        {
            "category": category,
            "roles": roles,
            "page_title": f"{category.name} — AI-proof ranking of {category.n_roles} roles · AIProof",
            "page_description": f"{category.n_roles} {category.name} roles ranked for AI resilience. Average score {category.avg_score or 0:.1f}/100. Browse top-scoring roles and dive into individual profiles.",
        },
    )


def tier_detail(request, tier):
    if tier not in TIER_ORDER:
        raise Http404
    roles = (
        Role.objects.select_related("category")
        .filter(tier=tier)
        .order_by("-score", "role")
    )
    tier_label = TIER_LABELS[tier]
    blurb = TIER_BLURBS[tier]
    return render(
        request,
        "roles/tier_detail.html",
        {
            "tier_key": tier,
            "tier_label": tier_label,
            "tier_blurb": blurb,
            "tier_color": TIER_COLORS[tier],
            "roles": roles,
            "page_title": f"{tier_label} tier — {len(roles)} AI-resilient tech roles · AIProof",
            "page_description": f"{tier_label} tier: {blurb} {len(roles)} roles in this tier.",
        },
    )
