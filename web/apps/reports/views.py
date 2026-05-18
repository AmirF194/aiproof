from django.shortcuts import render

from .services import render_doc

_PAGE_DESCRIPTIONS = {
    "report": "AIProof per-role analysis — the full 1,000-role dataset with deep insights, tier interpretations, and category breakdowns.",
    "insights": "Deep insights behind the AIProof ranking — labour-market data, cybersecurity workforce, AI adoption signals, and compensation benchmarks.",
    "methodology": "How AIProof scores 1,000 tech roles across 8 dimensions. Full formulas, weights, tier cutoffs, confidence math, and narrative templates.",
}


def _render_md(request, key: str, template: str, page_label: str):
    doc = render_doc(key)
    return render(
        request,
        template,
        {
            "doc": doc,
            "page_label": page_label,
            "page_title": f"{doc.title or page_label} — AIProof",
            "page_description": _PAGE_DESCRIPTIONS.get(key, ""),
        },
    )


def report(request):
    return _render_md(request, "report", "reports/page.html", "Per-Role Analysis")


def insights(request):
    return _render_md(request, "insights", "reports/page.html", "Deep Insights")


def methodology(request):
    return _render_md(request, "methodology", "reports/page.html", "Methodology")
