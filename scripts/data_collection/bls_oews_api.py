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

import datetime as _dt
import json
import os
import urllib.request

from _common import RAW

OUT = RAW / "bls_oews_live.json"
ENDPOINT = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# OEWS series IDs: OEUN + area(7) + industry(6) + occupation(6) + datatype(2)
# Area 0000000 = national. Industry 000000 = all. Datatype:
#   01 = Employment count
#   04 = Annual mean wage
#   13 = Annual median wage
# BLS publishes the May-YYYY reference snapshot the following spring, so the
# most recent year available is current_year-1; we ask for a 2-year window
# to also catch the prior reference if the current one is mid-release.
DATATYPES: tuple[str, ...] = ("01", "04", "13")
TECH_SOC_CODES: dict[str, str] = {
    "Software Developers":                "151252",
    "Data Scientists":                    "152051",
    "Information Security Analysts":      "151212",
    "Computer Network Architects":        "151241",
    "Database Administrators":            "151242",
    "Network and Computer Systems Administrators": "151244",
    "Computer Systems Analysts":          "151211",
    "Web Developers":                     "151254",
    "Computer Programmers":               "151251",
    "Computer and Information Research Scientists": "151221",
    "Computer Hardware Engineers":        "172061",
    "Computer and Information Systems Managers": "113021",
}


def _series_id(soc: str, datatype: str) -> str:
    return f"OEUN0000000000000{soc}{datatype}"


def collect() -> int:
    series_ids = [_series_id(soc, dt) for soc in TECH_SOC_CODES.values() for dt in DATATYPES]
    current_year = _dt.datetime.now(_dt.timezone.utc).year
    payload: dict = {
        "seriesid": series_ids,
        "startyear": str(current_year - 2),
        "endyear": str(current_year),
    }
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
    datatype_lookup = {"01": "employment", "04": "annual_mean_wage", "13": "annual_median_wage"}
    out: list[dict] = []
    data_points = 0
    for s in series:
        sid = s.get("seriesID", "")
        soc_code = sid[-8:-2] if len(sid) >= 8 else ""
        datatype = sid[-2:] if len(sid) >= 2 else ""
        rows = s.get("data", []) or []
        if not rows:
            continue
        data_points += len(rows)
        out.append({
            "series_id": sid,
            "occupation": soc_lookup.get(soc_code, sid),
            "soc_code": soc_code,
            "metric": datatype_lookup.get(datatype, datatype),
            "data": rows,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"fetched_at": response.get("message", []), "series": out}, indent=2))
    return data_points


if __name__ == "__main__":
    n = collect()
    print(f"bls_oews_api: wrote {n} data points to {OUT}")
