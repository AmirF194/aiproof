"""GitHub Octoverse loader (2025).

GitHub publishes the Octoverse report annually. The headline numbers we
use are cached at ``data/raw/github_octoverse_2025.json``.
"""
from __future__ import annotations

from _common import RAW, read_json

CACHE = RAW / "github_octoverse_2025.json"


def collect() -> dict:
    return read_json(CACHE)


if __name__ == "__main__":
    p = collect()
    pop = p["developer_population"]
    print(f"GitHub developers: {pop['total_developers_on_github_millions']}M "
          f"(+{pop['yoy_growth_pct']}% YoY)")
    for lang in p["language_trends_2025"][:5]:
        print(f"  #{lang['rank']} {lang['language']:<12} {lang['change_yoy']}")
