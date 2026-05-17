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


# Local-file link targets that should become real site URLs, with friendly
# replacement text when the author wrote the bare filename as the link text
# (which our source markdown often does).
_LINK_REWRITES = {
    "REPORT.md": ("/report/", "Report"),
    "INSIGHTS.md": ("/report/insights/", "Insights"),
    "METHODOLOGY.md": ("/report/methodology/", "Methodology"),
    "README.md": ("/", "Overview"),
    "data/roles.csv": ("/data/roles.csv", "roles.csv (download)"),
    "data/processed/role_ranking.csv": ("/data/role_ranking.csv", "role_ranking.csv (download)"),
    "data/processed/": ("/sources/", "data sources"),
    "data/processed": ("/sources/", "data sources"),
    "docs/role_directory.md": ("/sources/", "role directory"),
}

_ANCHOR_RE = re.compile(r'<a\b([^>]*?)\bhref="([^"]+)"([^>]*)>(.*?)</a>', re.DOTALL)


def _rewrite_internal_links(html: str) -> str:
    def _sub(m: re.Match) -> str:
        pre, href, post, text = m.group(1), m.group(2), m.group(3), m.group(4)
        # Preserve fragments (#section) when remapping a known target.
        base, _, frag = href.partition("#")
        if base in _LINK_REWRITES:
            new_href, label = _LINK_REWRITES[base]
            if frag:
                new_href = f"{new_href}#{frag}"
            # Replace the visible text when the author used the raw path as the label.
            if text.strip() == href or text.strip() == base:
                text = label
            return f'<a{pre}href="{new_href}"{post}>{text}</a>'
        return m.group(0)

    return _ANCHOR_RE.sub(_sub, html)


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
