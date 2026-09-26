"""Build and check the school runbooks.

Every source is Markdown, ``docs/runbooks/SCH-NNN-name.md``, and builds to
``docs/runbooks/pdf/SCH-NNN-name.pdf``. The convention is ``docs/runbooks/README.md``.

    python tools/runbooks/build.py                    rebuild every PDF
    python tools/runbooks/build.py --check            fail on anything the convention forbids
    python tools/runbooks/build.py --check --png DIR  also write every page as an image

Deterministic: the same source and the same pinned libraries give the same bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib

matplotlib.use("Agg")
import fitz  # noqa: E402  PyMuPDF, for validation and page images
import mistune  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from reportlab import rl_config  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.pdfmetrics import stringWidth  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import (  # noqa: E402
    BaseDocTemplate, Frame, Image, KeepTogether, PageTemplate, Paragraph, Spacer, Table,
    TableStyle,
)

rl_config.invariant = 1

REPO = Path(__file__).resolve().parents[2]
RUNBOOKS = REPO / "docs" / "runbooks"
PDF_DIR = RUNBOOKS / "pdf"
REGISTER = RUNBOOKS / "register.md"
TEMPLATE = RUNBOOKS / "template.md"

REQUIRED_META = ("ID", "Class", "Status", "Experiment")
CLASSES = ("SCHOOL-SOFTWARE", "SCHOOL-BENCH")
STATUSES = ("NOT READY", "BLOCKED", "READY", "DONE")
SECTIONS = (
    "Why we are doing it", "The scientific question", "What must already be true",
    "What you need", "Expected duration", "Files to bring or open",
    "Files that must exist when you leave", "STOP / DO NOT CONTINUE", "Procedure",
    "Evidence to bring back", "Back at home",
)
BOXES = {
    "STOP / DO NOT CONTINUE": ("STOP / DO NOT CONTINUE", "#fdecea", "#c62828"),
    "Evidence to bring back": ("EVIDENCE TO BRING BACK", "#e8f0fb", "#1f4e9c"),
    "Back at home": ("BACK AT HOME", "#eaf5ea", "#2e7d32"),
}
ALERTS = {"NOTE": ("WHY", "#f3f3f3", "#707070"), "IMPORTANT": ("IMPORTANT", "#e8f0fb", "#1f4e9c"),
          "WARNING": ("WARNING", "#fff4e0", "#b26a00"), "CAUTION": ("STOP", "#fdecea", "#c62828")}
TBD = re.compile(r"\{\{TBD:\s*(?P<what>[^;{}]+);\s*source:\s*(?P<src>[^{}]+)\}\}")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
FRAME_W = PAGE_W - 2 * MARGIN


# ------------------------------------------------------------------ fonts
def _fonts() -> None:
    if "RB" in pdfmetrics.getRegisteredFontNames():
        return
    d = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    for name, file in (("RB", "DejaVuSans.ttf"), ("RB-Bold", "DejaVuSans-Bold.ttf"),
                       ("RB-Italic", "DejaVuSans-Oblique.ttf"),
                       ("RB-BoldItalic", "DejaVuSans-BoldOblique.ttf"),
                       ("RB-Mono", "DejaVuSansMono.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(d / file)))
    pdfmetrics.registerFontFamily("RB", normal="RB", bold="RB-Bold", italic="RB-Italic",
                                  boldItalic="RB-BoldItalic")


def _styles() -> dict:
    base = dict(fontName="RB", fontSize=10, leading=14, splitLongWords=1)
    return {
        "body": ParagraphStyle("body", spaceAfter=4, **base),
        "cell": ParagraphStyle("cell", **{**base, "fontSize": 9, "leading": 12}),
        "cellhead": ParagraphStyle("cellhead", **{**base, "fontName": "RB-Bold", "fontSize": 9, "leading": 12}),
        "title": ParagraphStyle("title", **{**base, "fontName": "RB-Bold", "fontSize": 18, "leading": 23}),
        "kicker": ParagraphStyle("kicker", **{**base, "fontSize": 9, "textColor": colors.HexColor("#666666")}),
        "h2": ParagraphStyle("h2", **{**base, "fontName": "RB-Bold", "fontSize": 13.5, "leading": 18,
                                      "textColor": colors.HexColor("#1f3a60"), "spaceBefore": 12,
                                      "spaceAfter": 5, "keepWithNext": 1}),
        "h3": ParagraphStyle("h3", **{**base, "fontName": "RB-Bold", "fontSize": 11, "leading": 15,
                                      "spaceBefore": 9, "spaceAfter": 3, "keepWithNext": 1}),
        "boxtitle": ParagraphStyle("boxtitle", **{**base, "fontName": "RB-Bold", "fontSize": 10.5}),
        "code": ParagraphStyle("code", **{**base, "fontName": "RB-Mono", "fontSize": 8.5, "leading": 11.5}),
        "item": ParagraphStyle("item", spaceAfter=2, **base),
    }


# ------------------------------------------------------------------- math
#: Standard LaTeX that GitHub renders, translated into what mathtext understands.
#: The sources stay standard; only the rendering is adapted.
TEX_ALIASES = (
    (r"\le ", r"\leq "), (r"\ge ", r"\geq "), (r"\dfrac", r"\frac"), (r"\tfrac", r"\frac"),
    (r"\operatorname", r"\mathrm"), (r"\text{", r"\mathrm{"),
)


def mathtext(tex: str) -> str:
    out = tex + " "
    for a, b in TEX_ALIASES:
        out = out.replace(a, b)
    out = re.sub(r"\\le(?![a-zA-Z])", r"\\leq", out)
    out = re.sub(r"\\ge(?![a-zA-Z])", r"\\geq", out)
    return out.strip()


class MathCache:
    """Renders LaTeX with matplotlib's mathtext into PNG files, once each."""

    def __init__(self, folder: Path):
        self.folder = folder
        self.count = 0

    def png(self, tex: str, size: float) -> tuple[str, float, float]:
        tex = mathtext(tex)
        key = hashlib.sha1(f"{size}|{tex}".encode()).hexdigest()[:16]
        path = self.folder / f"m{key}.png"
        dpi = 300
        if not path.exists():
            fig = Figure(figsize=(0.01, 0.01))
            fig.text(0, 0, f"${tex}$", fontsize=size)
            buf = io.BytesIO()
            fig.savefig(buf, dpi=dpi, format="png", bbox_inches="tight", pad_inches=0.02,
                        transparent=True, metadata={"Software": None})
            path.write_bytes(buf.getvalue())
        self.count += 1
        from PIL import Image as PILImage
        with PILImage.open(path) as im:
            w, h = im.size
        return str(path), w * 72.0 / dpi, h * 72.0 / dpi


# ---------------------------------------------------------------- parsing
@dataclass
class Source:
    path: Path
    text: str
    meta: dict
    title: str
    sections: list            # [(title, tokens)]
    preamble: list
    errors: list = field(default_factory=list)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()

    @property
    def rel(self) -> str:
        return self.path.relative_to(REPO).as_posix()


_md = mistune.create_markdown(renderer=None, plugins=["table", "math", "task_lists"])


def _plain(tokens) -> str:
    out = []
    for t in tokens or []:
        if "raw" in t and t["type"] in ("text", "codespan", "inline_math"):
            out.append(t["raw"])
        elif t["type"] in ("softbreak", "linebreak"):
            out.append(" ")
        elif "children" in t:
            out.append(_plain(t["children"]))
    return "".join(out)


def parse(path: Path) -> Source:
    text = path.read_text(encoding="utf-8")
    tokens = [t for t in _md(text) if t["type"] != "blank_line"]
    errors, meta, title = [], {}, ""
    if not tokens or tokens[0]["type"] != "heading" or tokens[0]["attrs"]["level"] != 1:
        errors.append("the first line must be the title heading")
    else:
        title = _plain(tokens[0]["children"])
        tokens = tokens[1:]
    if tokens and tokens[0]["type"] == "list":
        for item in tokens[0]["children"]:
            line = _plain(item["children"])
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        tokens = tokens[1:]
    for k in REQUIRED_META:
        if k not in meta:
            errors.append(f"missing status line: {k}")
    preamble, sections, current = [], [], None
    for t in tokens:
        if t["type"] == "heading" and t["attrs"]["level"] == 2:
            current = (_plain(t["children"]), [])
            sections.append(current)
        elif current is None:
            preamble.append(t)
        else:
            current[1].append(t)
    return Source(path, text, meta, title, sections, preamble, errors)


def validate(src: Source, template: bool = False) -> list:
    errors = list(src.errors)
    names = [s for s, _ in src.sections]
    positions = [names.index(s) if s in names else -1 for s in SECTIONS]
    for s, p in zip(SECTIONS, positions):
        if p < 0:
            errors.append(f"missing section: {s}")
    found = [p for p in positions if p >= 0]
    if found != sorted(found):
        errors.append("the required sections are out of order")
    proc = dict(src.sections).get("Procedure", [])
    steps = [_plain(t["children"]) for t in proc if t["type"] == "heading" and t["attrs"]["level"] == 3]
    numbers = [s.split(".", 1)[0] for s in steps]
    if numbers != [str(i) for i in range(1, 11)]:
        errors.append(f"the procedure must have steps 1 to 10 in order, found {numbers}")
    status = src.meta.get("Status", "")
    if not template:
        if not src.path.name.startswith(f"{src.meta.get('ID', '?')}-"):
            errors.append("the file name must start with the runbook ID")
        if src.meta.get("Class") not in CLASSES:
            errors.append(f"class must be one of {CLASSES}")
        if status not in STATUSES:
            errors.append(f"status must be one of {STATUSES}")
    loose = src.text.count("{{TBD") - len(TBD.findall(src.text))
    if loose:
        errors.append(f"{loose} placeholder(s) without the form {{{{TBD: what; source: decision}}}}")
    if status in ("READY", "DONE") and TBD.search(src.text):
        errors.append("a ready runbook cannot hold a placeholder")
    return errors


# -------------------------------------------------------------- rendering
class Renderer:
    def __init__(self, math: MathCache):
        self.st = _styles()
        self.math = math

    # inline -----------------------------------------------------------
    def inline(self, tokens, size=10.0) -> str:
        out = []
        for t in tokens or []:
            kind = t["type"]
            if kind == "text":
                out.append(self._text(t["raw"]))
            elif kind == "strong":
                out.append(f"<b>{self.inline(t['children'], size)}</b>")
            elif kind == "emphasis":
                out.append(f"<i>{self.inline(t['children'], size)}</i>")
            elif kind == "codespan":
                out.append(f'<font face="RB-Mono" size="{size - 1:g}" backColor="#eeeeee">'
                           f"{escape(t['raw'])}</font>")
            elif kind == "inline_math":
                path, w, h = self.math.png(t["raw"], size)
                out.append(f'<img src="{path}" width="{w:.2f}" height="{h:.2f}" valign="middle"/>')
            elif kind == "link":
                out.append(self.inline(t["children"], size))
            elif kind in ("softbreak",):
                out.append(" ")
            elif kind == "linebreak":
                out.append("<br/>")
            elif "children" in t:
                out.append(self.inline(t["children"], size))
            elif "raw" in t:
                out.append(self._text(t["raw"]))
        return "".join(out)

    def _text(self, raw: str) -> str:
        s = escape(raw)
        return TBD.sub(lambda m: ('<font backColor="#ffe08a"><b>TO BE DECIDED:</b> '
                                  f'{m["what"].strip()} <i>(source: {m["src"].strip()})</i></font>'), s)

    # blocks -----------------------------------------------------------
    def blocks(self, tokens, width=FRAME_W) -> list:
        out = []
        for t in tokens:
            out.extend(self.block(t, width))
        return out

    def block(self, t, width) -> list:
        kind = t["type"]
        if kind == "paragraph" or kind == "block_text":
            return [Paragraph(self.inline(t.get("children")), self.st["body"])]
        if kind == "heading":
            style = self.st["h3"] if t["attrs"]["level"] >= 3 else self.st["h2"]
            return [Paragraph(self.inline(t["children"]), style)]
        if kind == "list":
            return self.list_(t, width)
        if kind == "table":
            return [self.table(t, width), Spacer(1, 5)]
        if kind == "block_code":
            info = (t.get("attrs") or {}).get("info", "")
            if info == "math":
                path, w, h = self.math.png(t["raw"].strip(), 12)
                if w > width:
                    w, h = width, h * width / w
                return [Spacer(1, 3), Image(path, width=w, height=h, hAlign="CENTER"), Spacer(1, 5)]
            return [self.code(t["raw"], width)]
        if kind == "block_quote":
            return self.alert(t, width)
        if kind == "thematic_break":
            return [Spacer(1, 6)]
        return []

    def list_(self, t, width, depth=0) -> list:
        ordered = t["attrs"].get("ordered", False)
        n = t["attrs"].get("start", 1) or 1
        rows = []
        for item in t["children"]:
            if item["type"] == "task_list_item":
                mark = chr(0x2611) if item["attrs"].get("checked") else chr(0x2610)
            elif ordered:
                mark = f"{n}."
            else:
                mark = chr(0x2022)
            n += 1
            inner = []
            for c in item["children"]:
                if c["type"] == "list":
                    inner.extend(self.list_(c, width - 16, depth + 1))
                else:
                    inner.extend(self.block(c, width - 16))
            rows.append([Paragraph(mark, self.st["item"]), inner])
        tbl = Table(rows, colWidths=[16, width - 16], hAlign="LEFT")
        tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                 ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                                 ("TOPPADDING", (0, 0), (-1, -1), 1),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
        return [tbl, Spacer(1, 3)]

    @staticmethod
    def _unbreakable(tokens) -> float:
        """Width of the longest run a line cannot break inside, in points."""
        widest = 0.0
        for t in tokens or []:
            if t["type"] == "codespan":
                for w in t["raw"].split():
                    widest = max(widest, stringWidth(w, "RB-Mono", 8))
            elif t["type"] == "text":
                for w in t["raw"].split():
                    widest = max(widest, stringWidth(w, "RB", 9))
            elif "children" in t:
                widest = max(widest, Renderer._unbreakable(t["children"]))
        return widest

    def table(self, t, width) -> Table:
        head = t["children"][0]["children"]
        body = [r["children"] for r in t["children"][1]["children"]] if len(t["children"]) > 1 else []
        n_col = len(head)
        grid = [head] + body
        texts = [[_plain(c["children"]) for c in row] for row in grid]
        # An empty cell is space to write in by hand, so it counts as a wide one.
        natural = [max(min(len(row[j]) if j < len(row) and row[j].strip() else 40, 70)
                       for row in texts[1:] or texts) + 4 for j in range(n_col)]
        natural = [max(n, len(texts[0][j]) + 4) for j, n in enumerate(natural)]
        widths = [max(width * w / sum(natural), 0.12 * width) for w in natural]
        widths = [w * width / sum(widths) for w in widths]
        # Every column is at least as wide as its longest path or word, so nothing is
        # split in the middle; the slack of the other columns pays for it.
        mins = [max(self._unbreakable(row[j]["children"]) if j < len(row) else 0 for row in grid) + 13
                for j in range(n_col)]
        widths = [max(w, m) for w, m in zip(widths, mins)]
        excess = sum(widths) - width
        if excess > 0:
            slack = [w - m for w, m in zip(widths, mins)]
            if sum(slack) >= excess:
                widths = [w - excess * s / sum(slack) for w, s in zip(widths, slack)]
            else:
                widths = [w * width / sum(widths) for w in widths]
        rows = [[Paragraph(self.inline(c["children"], 9), self.st["cellhead"]) for c in head]]
        heights = [None]
        for r in body:
            cells = [Paragraph(self.inline(c["children"], 9), self.st["cell"]) for c in r]
            cells += [Paragraph("", self.st["cell"])] * (n_col - len(cells))
            rows.append(cells)
            # A row with an empty cell is a form to fill by hand: give it room to write.
            heights.append(30 if any(not _plain(c["children"]).strip() for c in r) else None)
        tbl = Table(rows, colWidths=widths, rowHeights=heights, repeatRows=1, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9edf2")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c0cc")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return tbl

    def code(self, raw: str, width) -> Table:
        lines = raw.rstrip("\n").split("\n")
        # Only the indentation is made unbreakable, so long commands wrap between words.
        body = "<br/>".join(
            chr(0xA0) * (len(line) - len(line.lstrip(" "))) + escape(line.lstrip(" ")) for line in lines)
        p = Paragraph(body, self.st["code"])
        tbl = Table([[p]], colWidths=[width])
        tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f4f4")),
                                 ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
        return tbl

    def alert(self, t, width) -> list:
        children = list(t["children"])
        label = None
        if children and children[0]["type"] == "paragraph":
            first = children[0]["children"]
            head = _plain(first[:2]) if first else ""
            m = re.match(r"\[!(\w+)\]", head)
            if m and m.group(1).upper() in ALERTS:
                label = m.group(1).upper()
                rest = first[2:]
                while rest and rest[0]["type"] == "softbreak":
                    rest = rest[1:]
                children[0] = {**children[0], "children": rest}
        title, bg, border = ALERTS.get(label, ("", "#f3f3f3", "#707070"))
        return [self.box(title, children, bg, border, width)]

    def box(self, title, tokens, bg, border, width) -> Table:
        inner = width - 16
        rows = []
        if title:
            rows.append([Paragraph(f'<font color="{border}">{title}</font>', self.st["boxtitle"])])
        for f in self.blocks(tokens, inner):
            rows.append([f])
        tbl = Table(rows, colWidths=[width])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
            ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor(border)),
            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, 0), 6), ("BOTTOMPADDING", (0, -1), (-1, -1), 6),
        ]))
        return tbl

    # document ---------------------------------------------------------
    def story(self, src: Source) -> list:
        st = self.st
        name = src.title.split(":", 1)[1].strip() if ":" in src.title else src.title
        story = [Paragraph("AetherArray, school runbook", st["kicker"]),
                 Paragraph(escape(name), st["title"]), Spacer(1, 6)]
        rows = [["Task", escape(name)]]
        for k in ("ID", "Class", "Status", "Experiment", "Decisions", "Last reviewed"):
            if k in src.meta:
                rows.append([k, escape(src.meta[k])])
        rows.append(["Source", f'<font face="RB-Mono" size="8">{escape(src.rel)}</font>'])
        rows.append(["Source SHA-256", f'<font face="RB-Mono" size="8">{src.sha256}</font>'])
        tbl = Table([[Paragraph(f"<b>{a}</b>", st["cell"]), Paragraph(b, st["cell"])] for a, b in rows],
                    colWidths=[0.24 * FRAME_W, 0.76 * FRAME_W], hAlign="LEFT")
        tbl.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c0cc")),
                                 ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e9edf2")),
                                 ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        story += [tbl, Spacer(1, 8)]
        story += self.blocks(src.preamble)
        for title, tokens in src.sections:
            if title in BOXES:
                label, bg, border = BOXES[title]
                story.append(Spacer(1, 8))
                story.append(self.box(label, tokens, bg, border, FRAME_W))
            else:
                story.append(Paragraph(escape(title), st["h2"]))
                story += self.blocks(tokens)
        return story


def _page_decorator(src: Source, total: int):
    name = src.title

    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("RB", 8)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(MARGIN, PAGE_H - 13 * mm, name[:95])
        canvas.setStrokeColor(colors.HexColor("#b8c0cc"))
        canvas.line(MARGIN, PAGE_H - 14.5 * mm, PAGE_W - MARGIN, PAGE_H - 14.5 * mm)
        canvas.line(MARGIN, 14 * mm, PAGE_W - MARGIN, 14 * mm)
        canvas.drawString(MARGIN, 10 * mm, f"{src.rel}   sha256 {src.sha256[:16]}")
        canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"page {doc.page} of {total}")
        canvas.restoreState()

    return draw


def render(src: Source, out: Path, workdir: Path) -> int:
    """Two passes: the first counts the pages, the second prints page X of Y."""
    _fonts()
    math = MathCache(workdir)
    total = 0
    for _ in range(2):
        doc = BaseDocTemplate(
            str(out), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
            topMargin=20 * mm, bottomMargin=18 * mm, invariant=1,
            title=src.title, author="AetherArray", subject=f"{src.meta.get('ID', '')} school runbook",
            creator="tools/runbooks/build.py", keywords=f"source={src.rel}; sha256={src.sha256}",
        )
        frame = Frame(MARGIN, 18 * mm, FRAME_W, PAGE_H - 38 * mm, id="body",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        doc.addPageTemplates([PageTemplate(id="page", frames=[frame],
                                           onPage=_page_decorator(src, max(total, 1)))])
        doc.build(Renderer(math).story(src))
        total = doc.page
    return total


# ------------------------------------------------------------- validation
def layout_errors(pdf: Path, n_math: int | None = None) -> list:
    errors = []
    doc = fitz.open(pdf)
    n = doc.page_count
    lo_x, hi_x = MARGIN - 1.5, PAGE_W - MARGIN + 1.5
    lo_y, hi_y = 8 * mm, PAGE_H - 8 * mm
    for i, page in enumerate(doc, start=1):
        text = page.get_text()
        if f"page {i} of {n}" not in text:
            errors.append(f"{pdf.name} page {i}: no page number")
        for x0, y0, x1, y1, word, *_ in page.get_text("words"):
            if x0 < lo_x or x1 > hi_x or y0 < lo_y or y1 > hi_y:
                errors.append(f"{pdf.name} page {i}: text outside the printable area: {word!r}")
                break
        for info in page.get_image_info():
            x0, y0, x1, y1 = info["bbox"]
            if x0 < lo_x or x1 > hi_x or y0 < lo_y or y1 > hi_y:
                errors.append(f"{pdf.name} page {i}: an image is clipped or outside the page")
    return errors


def pdf_source_hash(pdf: Path) -> str | None:
    m = re.search(r"sha256=([0-9a-f]{64})", fitz.open(pdf).metadata.get("keywords") or "")
    return m.group(1) if m else None


def pdf_text(pdf: Path) -> list:
    return [p.get_text() for p in fitz.open(pdf)]


def register_rows() -> list:
    text = REGISTER.read_text(encoding="utf-8")
    part = text.split("## 2. School tasks", 1)
    if len(part) < 2:
        return []
    rows = []
    for line in part[1].splitlines():
        if not line.startswith("| SCH-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(dict(zip(("id", "task", "class", "status", "runbook", "gates", "missing"), cells)))
    return rows


def sources() -> list:
    return sorted(RUNBOOKS.glob("SCH-*.md"))


def check(png_dir: Path | None) -> int:
    errors = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # The template must itself satisfy the format it imposes.
        tsrc = parse(TEMPLATE)
        errors += [f"template: {e}" for e in validate(tsrc, template=True)]
        render(tsrc, tmp / "template.pdf", tmp)
        errors += layout_errors(tmp / "template.pdf")

        by_id = {}
        for path in sources():
            src = parse(path)
            by_id[src.meta.get("ID")] = src
            errors += [f"{path.name}: {e}" for e in validate(src)]
            fresh = tmp / (path.stem + ".pdf")
            render(src, fresh, tmp)
            committed = PDF_DIR / (path.stem + ".pdf")
            if not committed.exists():
                errors.append(f"{path.name}: no PDF; run tools/runbooks/build.py")
                continue
            if pdf_source_hash(committed) != src.sha256:
                errors.append(f"{committed.name}: built from an older source; rebuild")
            if pdf_text(committed) != pdf_text(fresh):
                errors.append(f"{committed.name}: content differs from a fresh build; rebuild")
            errors += layout_errors(committed)
            same = committed.read_bytes() == fresh.read_bytes()
            print(f"{committed.name}: {fitz.open(committed).page_count} pages, "
                  f"{'byte identical to' if same else 'same content as'} a fresh build")
            if png_dir:
                png_dir.mkdir(parents=True, exist_ok=True)
                for i, page in enumerate(fitz.open(committed), start=1):
                    page.get_pixmap(dpi=110).save(str(png_dir / f"{path.stem}-p{i}.png"))

        for stale in PDF_DIR.glob("*.pdf") if PDF_DIR.exists() else []:
            if not (RUNBOOKS / (stale.stem + ".md")).exists():
                errors.append(f"{stale.name}: a PDF without a source")

        rows = register_rows()
        if not rows:
            errors.append("register: no school task table found")
        seen = set()
        for r in rows:
            rid = r["id"]
            seen.add(rid)
            if r["class"] not in CLASSES:
                errors.append(f"register {rid}: class {r['class']!r}")
            if r["status"] not in STATUSES:
                errors.append(f"register {rid}: status {r['status']!r}")
            src = by_id.get(rid)
            if r["status"] in ("BLOCKED", "READY", "DONE"):
                if src is None:
                    errors.append(f"register {rid}: {r['status']} without a runbook source")
                elif src.meta.get("Status") != r["status"]:
                    errors.append(f"register {rid}: status {r['status']} but the runbook says "
                                  f"{src.meta.get('Status')}")
                elif not (PDF_DIR / (src.path.stem + ".pdf")).exists():
                    errors.append(f"register {rid}: {r['status']} without its PDF")
            if r["status"] == "READY" and r["gates"] != "none open":
                errors.append(f"register {rid}: READY while gates are open: {r['gates']}")
            if r["status"] == "NOT READY" and (not r["missing"] or r["missing"] == "nothing"):
                errors.append(f"register {rid}: NOT READY must say what is missing")
        for rid in by_id:
            if rid not in seen:
                errors.append(f"register: runbook {rid} is not listed")

    for e in errors:
        print("FAIL:", e)
    if not errors:
        print("Runbook checks passed.")
    return 1 if errors else 0


def build() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    status = 0
    with tempfile.TemporaryDirectory() as tmp:
        for path in sources():
            src = parse(path)
            errs = validate(src)
            if errs:
                status = 1
                for e in errs:
                    print(f"FAIL: {path.name}: {e}")
                continue
            out = PDF_DIR / (path.stem + ".pdf")
            pages = render(src, out, Path(tmp))
            print(f"built {out.relative_to(REPO).as_posix()}, {pages} pages")
    return status


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--check", action="store_true")
    p.add_argument("--png", type=Path, default=None)
    a = p.parse_args(argv)
    return check(a.png) if a.check else build()


if __name__ == "__main__":
    raise SystemExit(main())
