"""O*NET Web Services crawler (V2 API).

O*NET is the U.S. Department of Labor's authoritative occupational dataset:
skills, abilities, work activities, knowledge, and tasks per occupation.
Free after registration at https://services.onetcenter.org/.

V2 auth: single API key in an `X-API-Key` header against
`https://api-v2.onetcenter.org/`. (The legacy `services.onetcenter.org/ws/`
host with HTTP Basic Auth is no longer accepted for new accounts.)

Required environment variable (set in /opt/aiproof/.env on prod):
    ONET_API_KEY   — API key from My Account page on services.onetcenter.org
                     (falls back to ONET_PASS for backward compat)

Output: data/raw/onet_summaries.json — keyed by SOC code
"""
from __future__ import annotations

import json
import os

from _common import RAW, http_get

OUT = RAW / "onet_summaries.json"
ENDPOINT = "https://api-v2.onetcenter.org/online/occupations/{soc}"

TECH_SOC: tuple[str, ...] = (
    "15-1252.00",   # Software Developers
    "15-2051.00",   # Data Scientists
    "15-1212.00",   # Information Security Analysts
    "15-1241.00",   # Computer Network Architects
    "15-1242.00",   # Database Administrators (was 15-1245 pre-2018 SOC)
    "15-1244.00",   # Network & Systems Administrators
    "15-1211.00",   # Computer Systems Analysts
    "15-1254.00",   # Web Developers
    "15-1221.00",   # Computer & Information Research Scientists
    "17-2061.00",   # Computer Hardware Engineers
    "11-3021.00",   # Computer & Information Systems Managers
)


def _fetch_occupation(soc: str, api_key: str) -> dict | None:
    raw = http_get(
        ENDPOINT.format(soc=soc),
        timeout=20.0,
        headers={
            "X-API-Key": api_key,
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
    api_key = (os.environ.get("ONET_API_KEY") or os.environ.get("ONET_PASS") or "").strip()
    if not api_key:
        print("onet_api: ONET_API_KEY not set — skipping.")
        return 0

    out: dict[str, dict] = {}
    for soc in TECH_SOC:
        data = _fetch_occupation(soc, api_key)
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
