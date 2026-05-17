from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import markdown
from django.conf import settings
from django.utils.text import slugify


MD_EXTENSIONS = [
    "extra",
    "tables",
    "fenced_code",
    "toc",
    "sane_lists",
    "pymdownx.superfences",
    "pymdownx.tilde",
    "pymdownx.tasklist",
    "pymdownx.magiclink",
    "pymdownx.smartsymbols",
]


@dataclass
class TocEntry:
    level: int
    title: str
    slug: str


@dataclass
class RenderedDoc:
    html: str
    toc: list[TocEntry]
    title: str
    raw_md: str


HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.MULTILINE)


def _extract_toc(md_text: str) -> list[TocEntry]:
    toc: list[TocEntry] = []
    seen: dict[str, int] = {}
    for match in HEADING_RE.finditer(md_text):
        level = len(match.group(1))
        title = match.group(2).strip()
        slug_base = slugify(title) or "section"
        slug = slug_base
        if slug in seen:
            seen[slug] += 1
            slug = f"{slug_base}-{seen[slug_base]}"
        else:
            seen[slug] = 1
        toc.append(TocEntry(level=level, title=title, slug=slug))
    return toc


def _extract_title(md_text: str) -> str:
    for match in HEADING_RE.finditer(md_text):
        if len(match.group(1)) == 1:
            return match.group(2).strip()
    return ""


def _rewrite_chart_refs(html: str) -> str:
    # Charts in source markdown reference `charts/foo.svg`; map to /static/charts/foo.svg.
    return html.replace('src="charts/', 'src="/static/charts/').replace(
        "src='charts/", "src='/static/charts/"
    )


def _rewrite_internal_links(html: str) -> str:
    return (
        html.replace('href="REPORT.md', 'href="/report/')
        .replace('href="INSIGHTS.md', 'href="/report/insights/')
        .replace('href="METHODOLOGY.md', 'href="/report/methodology/')
        .replace('href="README.md', 'href="/')
        .replace('href="data/processed/role_ranking.csv', 'href="/roles/')
        .replace('href="data/roles.csv', 'href="/roles/')
    )


@lru_cache(maxsize=8)
def _render_cached(path_str: str, mtime: float) -> RenderedDoc:
    path = Path(path_str)
    raw = path.read_text(encoding="utf-8")
    title = _extract_title(raw)
    toc = _extract_toc(raw)
    md = markdown.Markdown(extensions=MD_EXTENSIONS, output_format="html5")
    html = md.convert(raw)
    html = _rewrite_chart_refs(html)
    html = _rewrite_internal_links(html)
    return RenderedDoc(html=html, toc=toc, title=title, raw_md=raw)


def render_doc(key: str) -> RenderedDoc:
    path: Path = settings.REPORT_MD_FILES[key]
    return _render_cached(str(path), path.stat().st_mtime)
