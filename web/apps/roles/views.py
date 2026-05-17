from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import (
    Category,
    Role,
    TIER_BLURBS,
    TIER_COLORS,
    TIER_LABELS,
    TIER_ORDER,
    TREND_LABELS,
)


SORT_FIELDS = {
    "score": "-score",
    "score_asc": "score",
    "role": "role",
    "rank": "rank",
    "salary": "-salary_high_usd",
}


def _filter_roles(request):
    qs = Role.objects.select_related("category", "metrics").all()

    q = request.GET.get("q", "").strip()
    tier = request.GET.get("tier", "").strip()
    category = request.GET.get("category", "").strip()
    trend = request.GET.get("trend", "").strip()
    sort = request.GET.get("sort", "rank").strip()

    if q:
        qs = qs.filter(Q(role__icontains=q) | Q(category__name__icontains=q))
    if tier in TIER_ORDER:
        qs = qs.filter(tier=tier)
    if category:
        qs = qs.filter(category__slug=category)
    if trend in TREND_LABELS:
        qs = qs.filter(demand_trend=trend)

    order = SORT_FIELDS.get(sort, "rank")
    qs = qs.order_by(order, "role")

    return qs, {
        "q": q,
        "tier": tier,
        "category": category,
        "trend": trend,
        "sort": sort,
    }


def ranking(request):
    qs, params = _filter_roles(request)
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
            "roles": qs[:200],
            "total": qs.count(),
            "categories": categories,
            "tiers": tiers,
            "trends": trends,
            "params": params,
        },
    )


def ranking_table(request):
    """HTMX partial: just the table body + meta."""
    qs, params = _filter_roles(request)
    return render(
        request,
        "roles/_ranking_table.html",
        {
            "roles": qs[:200],
            "total": qs.count(),
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
        return sum((a - b) ** 2 for a, b in zip(target, ov))

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

    return render(
        request,
        "roles/detail.html",
        {
            "role": role,
            "adjacent": adjacent,
            "peers": peers,
            "breakdown": breakdown,
            "tier_blurb": TIER_BLURBS.get(role.tier, ""),
        },
    )


def category_index(request):
    categories = Category.objects.order_by("-avg_score")
    return render(
        request,
        "roles/categories.html",
        {"categories": categories},
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    roles = category.roles.order_by("-score", "role")
    return render(
        request,
        "roles/category_detail.html",
        {"category": category, "roles": roles},
    )


def tier_detail(request, tier):
    if tier not in TIER_ORDER:
        raise Http404
    roles = (
        Role.objects.select_related("category")
        .filter(tier=tier)
        .order_by("-score", "role")
    )
    return render(
        request,
        "roles/tier_detail.html",
        {
            "tier_key": tier,
            "tier_label": TIER_LABELS[tier],
            "tier_blurb": TIER_BLURBS[tier],
            "tier_color": TIER_COLORS[tier],
            "roles": roles,
        },
    )
