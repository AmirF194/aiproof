"""Shared helpers for data-collection scripts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent.parent
RAW = REPO / "data" / "raw"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def http_get(
    url: str,
    timeout: float = 10.0,
    headers: dict[str, str] | None = None,
) -> str | None:
    """Best-effort HTTP fetch using only the stdlib. Returns None on failure.

    Returns None when the network is unavailable, the host blocks the UA, or
    the request times out — pipelines downstream must fall back to cache.

    Caller-supplied `headers` override the defaults; the default User-Agent
    identifies us as aiproof-research with a contact URL.
    """
    default_headers = {
        "User-Agent": "aiproof-research/1.0 (+https://aiproof.fastinfer.org)",
    }
    if headers:
        default_headers.update(headers)
    try:
        import urllib.request
        req = urllib.request.Request(url, headers=default_headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None
