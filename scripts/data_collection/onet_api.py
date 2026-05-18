"""O*NET Web Services crawler.

O*NET is the U.S. Department of Labor's authoritative occupational dataset:
skills, abilities, work activities, knowledge, and automation susceptibility
per occupation. Free after registration at https://services.onetcenter.org/.

Required environment variables (set in /opt/aiproof/.env on prod):
    ONET_USER   — username from the O*NET developer portal
    ONET_PASS   — paired password

We pull the same SOC codes the BLS crawler uses, and request the four
"work-context" and "skill" summaries that feed our human_judgment_score
and physical_world_dependency_score derivations.

Output: data/raw/onet_summaries.json — keyed by SOC code
"""
from __future__ import annotations

import base64
import json
import os

from _common import RAW, http_get

OUT = RAW / "onet_summaries.json"

TECH_SOC: tuple[str, ...] = (
    "15-1252.00",   # Software Developers
    "15-2051.00",   # Data Scientists
    "15-1212.00",   # Information Security Analysts
    "15-1241.00",   # Computer Network Architects
    "15-1245.00",   # Database Administrators
    "15-1244.00",   # Network & Systems Administrators
    "15-1211.00",   # Computer Systems Analysts
    "15-1254.00",   # Web Developers
    "15-1221.00",   # Computer & Information Research Scientists
    "17-2061.00",   # Computer Hardware Engineers
    "11-3021.00",   # Computer & Information Systems Managers
)


def _basic_auth(user: str, password: str) -> str:
    return "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()


def _fetch_occupation(soc: str, auth: str) -> dict | None:
    base = f"https://services.onetcenter.org/ws/online/occupations/{soc}/summary"
    raw = http_get(
        base,
        timeout=20.0,
        headers={
            "Authorization": auth,
            "Accept": "application/json",
        },
    )
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def collect() -> int:
    user = os.environ.get("ONET_USER", "").strip()
    password = os.environ.get("ONET_PASS", "").strip()
    if not (user and password):
        print("onet_api: ONET_USER / ONET_PASS not set — skipping.")
        return 0

    auth = _basic_auth(user, password)
    out: dict[str, dict] = {}
    for soc in TECH_SOC:
        data = _fetch_occupation(soc, auth)
        if data:
            out[soc] = data

    if not out:
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    return len(out)


if __name__ == "__main__":
    n = collect()
    print(f"onet_api: wrote {n} occupations to {OUT}")
