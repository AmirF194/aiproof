#!/usr/bin/env python3
"""Rasterize charts/*.svg → charts/pdf/*.png for LaTeX inclusion.

Pure-Python via cairosvg. Output is fixed-width 1800px so the PDF includes
crisp graphics at letter-size. Aspect ratio is preserved per chart.
"""
from __future__ import annotations

from pathlib import Path

import cairosvg

REPO = Path(__file__).resolve().parent.parent.parent
SRC = REPO / "charts"
DST = REPO / "charts" / "pdf"
WIDTH = 1800


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for svg in sorted(SRC.glob("*.svg")):
        png = DST / (svg.stem + ".png")
        cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=WIDTH)
        print(f"  {svg.name} -> {png.relative_to(REPO)}")


if __name__ == "__main__":
    main()
