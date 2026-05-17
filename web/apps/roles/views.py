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
    qs = Role.objects.select_related("category").all()

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


def role_detail(request, slug):
    role = get_object_or_404(
        Role.objects.select_related("category"), slug=slug
    )
    peers = (
        Role.objects.filter(category=role.category)
        .exclude(pk=role.pk)
        .order_by("-score")[:8]
    )
    return render(
        request,
        "roles/detail.html",
        {
            "role": role,
            "peers": peers,
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
