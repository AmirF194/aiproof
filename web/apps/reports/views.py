from django.shortcuts import render

from .services import render_doc


def _render_md(request, key: str, template: str, page_label: str):
    doc = render_doc(key)
    return render(
        request,
        template,
        {
            "doc": doc,
            "page_label": page_label,
        },
    )


def report(request):
    return _render_md(request, "report", "reports/page.html", "Per-Role Analysis")


def insights(request):
    return _render_md(request, "insights", "reports/page.html", "Deep Insights")


def methodology(request):
    return _render_md(request, "methodology", "reports/page.html", "Methodology")
