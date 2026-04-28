"""Top-level orchestrator. Runs collection -> cleaning -> analysis -> charts.

Usage:
    python3 scripts/run_pipeline.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

STEPS = [
    ("collection", SCRIPTS / "data_collection" / "run_all.py"),
    ("cleaning",   SCRIPTS / "data_cleaning"   / "run_all.py"),
    ("analysis",   SCRIPTS / "analysis"        / "run_all.py"),
    ("charts",     SCRIPTS / "visualization"   / "generate_charts.py"),
    ("rasterize",  SCRIPTS / "visualization"   / "rasterize_charts.py"),
]


def main() -> int:
    for name, path in STEPS:
        print(f"\n==> {name}")
        rc = subprocess.call([sys.executable, str(path)])
        if rc != 0:
            print(f"!! {name} failed with exit code {rc}", file=sys.stderr)
            return rc
    print("\nPipeline complete. See data/processed/ and charts/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
