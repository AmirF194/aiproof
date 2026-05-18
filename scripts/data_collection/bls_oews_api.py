"""BLS Occupational Employment & Wage Statistics — live API crawler.

US Bureau of Labor Statistics Public Data API v2. Free; works without a key
for up to 25 queries/day, or 500/day after free registration at
https://data.bls.gov/registrationEngine/.

We pull OEWS series for the core tech occupations our roster maps into.
SOC code → series ID mapping is in TECH_SOC_CODES.

Required environment variables (optional):
    BLS_API_KEY   — registered API key (lifts daily quota to 500)

Output: data/raw/bls_oews_live.json — series-keyed median wage + employment counts
"""
from __future__ import annotations

import json
import os
import urllib.request

from _common import RAW

OUT = RAW / "bls_oews_live.json"
ENDPOINT = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# OEWS series IDs follow the form: OEUN <area> <industry> <occupation> <datatype>
# Area 0000000 = national, Industry 000000 = all, Datatype 04 = annual median wage.
TECH_SOC_CODES: dict[str, str] = {
    "Software Developers":                "151252",
    "Data Scientists":                    "152051",
    "Information Security Analysts":      "151212",
    "Computer Network Architects":        "151241",
    "Database Administrators":            "151245",
    "Network and Computer Systems Administrators": "151244",
    "Computer Systems Analysts":          "151211",
    "Web Developers":                     "151254",
    "Computer Programmers":               "151251",
    "Computer and Information Research Scientists": "151221",
    "Computer Hardware Engineers":        "172061",
    "Computer and Information Systems Managers": "113021",
}


def _series_id(soc: str, datatype: str = "04") -> str:
    # OEUN + areacode (7 digits: 0000000 = US) + industry (6 digits: 000000) + soc (6 digits) + datatype (2 digits)
    return f"OEUN0000000000000{soc}{datatype}"


def collect() -> int:
    series_ids = [_series_id(code) for code in TECH_SOC_CODES.values()]
    payload: dict = {"seriesid": series_ids, "startyear": "2023", "endyear": "2024"}
    api_key = os.environ.get("BLS_API_KEY", "").strip()
    if api_key:
        payload["registrationkey"] = api_key

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "aiproof-research/1.0 (+https://aiproof.fastinfer.org)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            response = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as exc:  # noqa: BLE001
        print(f"bls_oews_api: request failed ({exc}) — leaving cache untouched.")
        return 0

    if response.get("status") != "REQUEST_SUCCEEDED":
        print(f"bls_oews_api: API returned status={response.get('status')} — leaving cache untouched.")
        return 0

    series = response.get("Results", {}).get("series", []) or []
    if not series:
        return 0

    soc_lookup = {v: k for k, v in TECH_SOC_CODES.items()}
    out: list[dict] = []
    for s in series:
        sid = s.get("seriesID", "")
        soc_code = sid[-8:-2] if len(sid) >= 8 else ""
        out.append({
            "series_id": sid,
            "occupation": soc_lookup.get(soc_code, sid),
            "soc_code": soc_code,
            "data": s.get("data", []),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"fetched_at": response.get("message", []), "series": out}, indent=2))
    return len(out)


if __name__ == "__main__":
    n = collect()
    print(f"bls_oews_api: wrote {n} series to {OUT}")
