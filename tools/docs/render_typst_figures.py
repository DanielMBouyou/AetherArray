"""Render the figures of the Typst edition of the master reference.

    python tools/docs/render_typst_figures.py

1. Copies the three analytical plots from docs/figures/ (made by
   tools/docs/master_reference_figures.py) into the Typst project.
2. Renders every figures/mermaid/*.mmd of the project to SVG with mermaid-cli, with
   HTML labels disabled so that the labels are plain SVG text that Typst can draw.

typst.app never runs Mermaid: the SVG files are committed next to their sources.

mermaid-cli is found as `mmdc` on PATH or through the MMDC environment variable. Labels
are set in Libertinus Serif, the body font that the Typst compiler embeds; install it
locally before rendering so that Chromium measures the label boxes with the same font.
A Puppeteer configuration (for example a Chromium path and --no-sandbox) can be passed
through the PUPPETEER_CONFIG environment variable.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECT = REPO / "docs" / "typst" / "aetherarray-master-reference"
ANALYTICAL = ["steering-n4.svg", "null-filling-n4.svg", "switched-line-dispersion.svg"]

CONFIG = {
    "theme": "neutral",
    "fontFamily": "Libertinus Serif",
    "htmlLabels": False,
    "flowchart": {"htmlLabels": False, "curve": "basis", "padding": 10},
    "themeVariables": {"fontFamily": "Libertinus Serif", "fontSize": "15px"},
    # Opaque edge label backgrounds, so that edges do not run through label text.
    "themeCSS": ".edgeLabel rect { opacity: 1 !important; fill: #ffffff !important; }",
}


def main() -> None:
    fig = PROJECT / "figures"
    fig.mkdir(parents=True, exist_ok=True)
    for name in ANALYTICAL:
        shutil.copyfile(REPO / "docs" / "figures" / name, fig / name)
    mdir = fig / "mermaid"
    cfg = mdir / "mermaid-config.json"
    cfg.write_text(json.dumps(CONFIG, indent=2) + "\n", encoding="utf-8")
    mmdc = os.environ.get("MMDC", "mmdc")
    for src in sorted(mdir.glob("*.mmd")):
        cmd = [mmdc, "-q", "-c", str(cfg), "-b", "white", "-i", str(src), "-o", str(src.with_suffix(".svg"))]
        if os.environ.get("PUPPETEER_CONFIG"):
            cmd[1:1] = ["-p", os.environ["PUPPETEER_CONFIG"]]
        subprocess.run(cmd, check=True)
        svg = src.with_suffix(".svg").read_text(encoding="utf-8")
        if "foreignObject" in svg:
            raise SystemExit(f"{src.name}: HTML labels present, Typst cannot draw them")
        print("rendered", src.with_suffix(".svg").relative_to(REPO))


if __name__ == "__main__":
    main()
