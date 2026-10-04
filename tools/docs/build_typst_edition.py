"""Build the Typst edition of the master reference: PDF, project ZIP, and the ZIP test.

    python tools/docs/build_typst_edition.py [--typst PATH]

1. Compiles docs/typst/aetherarray-master-reference/main.typ to
   docs/build/AetherArray_Master_Reference_v0.2.pdf.
2. Packs the project folder into docs/build/AetherArray_Master_Reference_v0.2_Typst.zip,
   with fixed timestamps so that the same sources give the same archive.
3. Extracts the ZIP into a temporary directory, compiles main.typ there, and checks that
   the page count matches: the archive is self-contained.

It does not convert the Markdown or render diagrams; see md_to_typst.py and
render_typst_figures.py for those.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECT = REPO / "docs" / "typst" / "aetherarray-master-reference"
BUILD = REPO / "docs" / "build"
PDF = BUILD / "AetherArray_Master_Reference_v0.2.pdf"
ZIP = BUILD / "AetherArray_Master_Reference_v0.2_Typst.zip"
SKIP = {".pdf"}


def pages(pdf: Path) -> int:
    """Page count from the /Count of the page tree root, the largest one in the file."""
    counts = re.findall(rb"/Count\s+(\d+)", pdf.read_bytes())
    return max(int(c) for c in counts)


def compile_project(typst: str, root: Path, out: Path) -> None:
    subprocess.run([typst, "compile", "--root", str(root), str(root / "main.typ"), str(out)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--typst", default="typst", help="path to the typst compiler")
    args = ap.parse_args()

    BUILD.mkdir(parents=True, exist_ok=True)
    compile_project(args.typst, PROJECT, PDF)
    n = pages(PDF)

    files = sorted(p for p in PROJECT.rglob("*") if p.is_file() and p.suffix not in SKIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            info = zipfile.ZipInfo(str(Path(PROJECT.name) / p.relative_to(PROJECT)), (2026, 10, 4, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes())

    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(tmp)
        root = Path(tmp) / PROJECT.name
        out = Path(tmp) / "recompiled.pdf"
        compile_project(args.typst, root, out)
        m = pages(out)
    if m != n:
        raise SystemExit(f"extracted ZIP compiled to {m} pages, the project to {n}")
    print(f"{PDF.relative_to(REPO)}: {n} pages, {PDF.stat().st_size} bytes")
    print(f"{ZIP.relative_to(REPO)}: {len(files)} files, {ZIP.stat().st_size} bytes")
    print(f"extracted ZIP recompiled independently: {m} pages")


if __name__ == "__main__":
    main()
