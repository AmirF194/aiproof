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

    return render(
        request,
        "core/home.html",
        {
            "tiers": tiers,
            "top_10": top_10,
            "bottom_10": bottom_10,
            "total": total,
            "categories": categories,
        },
    )


def about(request):
    return render(request, "core/about.html")


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
        {"groups": grouped, "n_sources": len(SOURCES)},
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
