"""Convert docs/aetherarray-master-reference.md into the Typst project.

Source policy:
  - docs/aetherarray-master-reference.md is the canonical scientific and content source;
  - docs/typst/aetherarray-master-reference/ is the editable publication and layout
    edition generated from it;
  - content and scientific corrections are normally made in the Markdown and then
    propagated to Typst; hand edits of the Typst files are meant mainly for layout and
    publication work.

    python tools/docs/md_to_typst.py              # create missing files, keep existing ones
    python tools/docs/md_to_typst.py --generated  # rewrite generated/ only
    python tools/docs/md_to_typst.py --force      # overwrite hand-editable files as well

Hand-editable files are the prose under chapters/, appendices/ and backmatter/,
bibliography.yml and figures/mermaid/*.mmd. Without --force an existing one is never
touched. With --force every one that would change is listed in a warning on standard
error before anything is written: review or back up that diff first, because hand
edits are lost. The generated/ files (stack-up tables that rfkit generates) are always
rewritten and must not be edited by hand. After changing a stack-up table, run
`python -m rfkit.cli stackup --write-docs` from tools/ and then this script with
--generated.

No scientific content is added, removed or reworded: text, equations, tables, caveats
and captions are carried over as they are. The only editorial additions are Typst
structure (labels, figure wrappers, includes) and the title page in template.typ.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from latex_to_typst import convert as latex  # noqa: E402

REPO = HERE.parents[1]
SRC = REPO / "docs" / "aetherarray-master-reference.md"
OUT = REPO / "docs" / "typst" / "aetherarray-master-reference"

GEN_NOTE = ("// GENERATED FILE, do not edit by hand.\n"
            "// Source: docs/aetherarray-master-reference.md, block `stackup:begin {name}`, itself\n"
            "// generated from hardware/rev-a/stackup/reva-stackup.json by\n"
            "// `python -m rfkit.cli stackup --write-docs` (run from tools/).\n"
            "// Regenerate with: python tools/docs/md_to_typst.py --generated\n")

PART_FILES = {
    "Part 0.": "00-overview", "Part I.": "01-course-theory", "Part II.": "02-engineering-problem",
    "Part III.": "03-hardware", "Part IV.": "04-stackup-rf-design",
    "Part V.": "05-simulation-analysis-stack", "Part VI.": "06-simulation-roadmap",
    "Part VII.": "07-measurement", "Part VIII.": "08-machine-learning",
    "Part IX.": "09-aps-isac-demonstrator", "Part X.": "10-project-status",
    "Part XI.": "11-validation", "Part XII.": "12-software-tools", "Part XIII.": "13-data-flow",
    "Part XIV.": "14-why-useful", "Part XV.": "15-literature-evidence",
    "Part XVI.": "16-ieee-strategy", "Part XVII.": "17-risk-register", "Part XVIII.": "18-roadmap",
    "Part XIX.": "19-glossary", "Part XX.": "20-is-and-is-not", "Part XXI.": "21-synthesis",
}
APPENDIX_FILES = {
    "A": "a-parameters", "B": "b-stackup", "C": "c-acceptance-budget", "D": "d-open-hardware-items",
    "E": "e-simulations", "F": "f-experiments", "G": "g-decisions", "H": "h-tools",
    "I": "i-aps-checklist", "J": "j-unresolved-questions", "K": "k-notation", "L": "l-where-to-find",
}
# Diagrams that are tall rather than wide get a narrower box so they fit one page.
FIGURE_WIDTH = {"7a": "78%", "5b": "78%"}

CITE_ID = r"[ABLPTVR]\d+[a-z]?"


# ---------------------------------------------------------------------------------
# Block parser
# ---------------------------------------------------------------------------------
LIST_RE = re.compile(r"^([-*+]|\d+\.) (.*)$")


def parse_blocks(lines: list[str]) -> list[tuple]:
    blocks: list[tuple] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        m = re.match(r"^```(\w*)\s*$", line)
        if m:
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            blocks.append(("fence", m.group(1), "\n".join(lines[i + 1:j])))
            i = j + 1
            continue
        if s.startswith("<!--"):
            blocks.append(("comment", s))
            i += 1
            continue
        m = re.match(r"^(#{1,6}) (.*)$", line)
        if m:
            blocks.append(("heading", len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if s == "---":
            blocks.append(("hr",))
            i += 1
            continue
        if line.startswith(">"):
            j = i
            inner = []
            while j < n and lines[j].startswith(">"):
                inner.append(re.sub(r"^> ?", "", lines[j]))
                j += 1
            blocks.append(("quote", parse_blocks(inner)))
            i = j
            continue
        if line.startswith("|"):
            j = i
            while j < n and lines[j].startswith("|"):
                j += 1
            blocks.append(("table", lines[i:j]))
            i = j
            continue
        if LIST_RE.match(line):
            items = []
            j = i
            while j < n:
                m = LIST_RE.match(lines[j])
                if m:
                    items.append([m.group(1), [m.group(2)]])
                    j += 1
                    continue
                if lines[j].startswith(" ") and lines[j].strip():
                    items[-1][1].append(lines[j].strip())
                    j += 1
                    continue
                if not lines[j].strip() and j + 1 < n and LIST_RE.match(lines[j + 1]):
                    j += 1
                    continue
                break
            blocks.append(("list", [(mk, "\n".join(t)) for mk, t in items]))
            i = j
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", s)
        if m:
            blocks.append(("image", m.group(1), m.group(2)))
            i += 1
            continue
        j = i
        para = []
        while j < n and lines[j].strip():
            l = lines[j]
            if j > i and (l.startswith(("```", "#", ">", "|", "<!--")) or LIST_RE.match(l)):
                break
            para.append(l.strip())
            j += 1
        blocks.append(("para", "\n".join(para)))
        i = j
    return blocks


# ---------------------------------------------------------------------------------
# Inline conversion
# ---------------------------------------------------------------------------------
MATH_RE = re.compile(r"(?<![\\\w$])\$(?=\S)((?:[^$\\]|\\.)+?)(?<=\S)\$(?![\w$])", re.S)


def slug(text: str) -> str:
    t = re.sub(r"[`*$\\]", "", text.lower())
    t = re.sub(r"[^\w\- ]", "", t)
    return t.strip().replace(" ", "-")


class Ctx:
    def __init__(self, refids: set[str], labels: set[str]):
        self.refids = refids
        self.labels = labels


def escape_text(t: str) -> str:
    out = []
    for k, ch in enumerate(t):
        prev = t[k - 1] if k else ""
        nxt = t[k + 1] if k + 1 < len(t) else ""
        if ch in "\\#$@<[]_~`":
            out.append("\\" + ch)
        elif ch == "/" and nxt in "/*":
            out.append("\\/")
        elif ch == "-" and prev == "-":
            out.append("\\-")
        elif ch == "?" and prev == "-":
            out.append("\\?")
        else:
            out.append(ch)
    return "".join(out)


def cite_group(inner: str, ctx: Ctx) -> str | None:
    parts = re.split(r"(, | to )", inner)
    if not re.fullmatch(CITE_ID, parts[0]):
        return None
    out = []
    for p in parts:
        if re.fullmatch(CITE_ID, p) and p in ctx.refids:
            out.append(f"#link(<ref-{p}>)[{p}]")
        else:
            out.append(escape_text(p))
    return "\\[" + "".join(out) + "\\]"


def inline(text: str, ctx: Ctx) -> str:
    ph: list[str] = []

    def keep(s: str) -> str:
        ph.append(s)
        return f"\x00{len(ph) - 1}\x00"

    # code spans, then mathematics, then links and citations
    text = re.sub(r"`([^`]+)`", lambda m: keep("`" + m.group(1) + "`"), text)
    text = MATH_RE.sub(lambda m: keep("$" + latex(m.group(1).replace("\n", " ")) + "$"), text)
    text = re.sub(r"https?://[^\s)\]>]+[^\s)\]>.,;:]",
                  lambda m: keep(f'#link("{m.group(0)}")'), text)

    def link(m):
        target, label_text = m.group(2), m.group(1)
        assert target.startswith("#"), target
        ctx.labels.add(target[1:])
        return keep(f"#link(<{target[1:]}>)[{inline(label_text, ctx)}]")

    text = re.sub(r"\[([^\]]+)\]\((#[^)]+)\)", link, text)

    def cite(m):
        r = cite_group(m.group(1), ctx)
        return keep(r) if r else m.group(0)

    text = re.sub(r"\[([^\]]+)\]", cite, text)
    text = escape_text(text)

    def strong(m):
        return emph_markup(m, "*", "strong")

    def emph(m):
        return emph_markup(m, "_", "emph")

    text = re.sub(r"\*\*(.+?)\*\*", strong, text, flags=re.S)
    text = re.sub(r"(?<![*\w])\*(?=\S)(.+?)(?<=\S)\*(?![*\w])", emph, text, flags=re.S)
    text = text.replace("*", "\\*").replace("\x01", "*")
    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: ph[int(m.group(1))], text)
    return text


def emph_markup(m, delim: str, func: str) -> str:
    s = m.string
    before = s[m.start() - 1] if m.start() else " "
    after = s[m.end()] if m.end() < len(s) else " "
    body = m.group(1)
    if before.isalnum() or after.isalnum():
        return f"#{func}[{body}]"
    d = "\x01" if delim == "*" else "_"
    return f"{d}{body}{d}"


LINE_START = re.compile(r"^(\d+\.|[-+=/])(\s|$)")


def protect_line_starts(t: str) -> str:
    def fix(line: str) -> str:
        m = LINE_START.match(line)
        if not m:
            return line
        if m.group(1).endswith("."):
            return m.group(1)[:-1] + "\\." + line[len(m.group(1)):]
        return "\\" + line
    return "\n".join(fix(l) for l in t.split("\n"))


# ---------------------------------------------------------------------------------
# Block emission
# ---------------------------------------------------------------------------------
def split_row(line: str) -> list[str]:
    cells, cur, in_code, in_math = [], "", False, False
    body = line.strip()[1:-1] if line.strip().endswith("|") else line.strip()[1:]
    k = 0
    while k < len(body):
        ch = body[k]
        if ch == "\\" and k + 1 < len(body) and body[k + 1] == "|":
            cur += "|"
            k += 2
            continue
        if ch == "`":
            in_code = not in_code
        elif ch == "$" and not in_code and (in_math or not (k and (body[k - 1].isalnum() or body[k - 1] == "\\"))):
            in_math = not in_math
        if ch == "|" and not in_code and not in_math:
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
        k += 1
    cells.append(cur.strip())
    return cells


def visible_len(cell: str) -> int:
    c = re.sub(r"\$[^$]*\$", "xxxx", cell)
    c = re.sub(r"[*`]", "", c)
    return len(c)


def column_widths(header: list[str], body: list[list[str]]) -> list[str]:
    """Typst column widths: fr shares by content, never narrower than the longest word.

    The width estimates assume the type sizes set in template.typ: 8.6 pt on a 170 mm
    text width, 7.4 pt from six columns, 8.2 pt on a 257 mm landscape text width from
    nine columns.
    """
    ncol = len(header)
    size = 8.6 if ncol < 6 else (8.2 if ncol >= 9 else 7.4)
    avail = (729.0 if ncol >= 9 else 481.0) - 2.0
    cw = 0.5 * size
    inset = 8.5

    def words(cell: str) -> list[str]:
        return re.sub(r"\$[^$]*\$", "xxxx", cell).replace("`", "").replace("*", "").split() or [""]

    natural, minimum, weight = [], [], []
    for c in range(ncol):
        cells = [header[c]] + [r[c] for r in body]
        lens = [visible_len(x) for x in cells]
        longest_word = max([1.1 * len(w) for w in words(header[c])] +
                           [len(w) for r in body for w in words(r[c])])
        natural.append(max(lens) * cw + inset)
        minimum.append(min(longest_word * cw + inset, 0.35 * avail))
        weight.append(max(0.6 * sum(lens) / len(lens) + 0.15 * max(lens), 1.4 * longest_word, 10))
    fixed: dict[int, float] = {c: natural[c] for c in range(ncol) if max(visible_len(x) for x in [header[c]] + [r[c] for r in body]) <= 14}
    while True:
        free = [c for c in range(ncol) if c not in fixed]
        if not free:
            break
        rest = avail - sum(fixed.values())
        total = sum(weight[c] for c in free)
        short = [c for c in free if rest * weight[c] / total < minimum[c]]
        if not short:
            break
        for c in short:
            fixed[c] = minimum[c]
    if sum(fixed.values()) > avail:
        # Even the minimum widths do not fit: share the width in proportion to them.
        return [f"{(fixed.get(c) or minimum[c]) / 10:.1f}fr" for c in range(ncol)]
    out = []
    for c in range(ncol):
        if c in fixed:
            out.append("auto" if fixed[c] == natural[c] else f"{fixed[c]:.0f}pt")
        else:
            out.append(f"{round(weight[c] / 10, 1)}fr")
    return out


def emit_table(rows: list[str], ctx: Ctx) -> str:
    header = split_row(rows[0])
    body = [split_row(r) for r in rows[2:]]
    ncol = len(header)
    for r in body:
        assert len(r) == ncol, (header, r)
    cols = column_widths(header, body)
    lines = ["#table(", f"  columns: ({', '.join(cols)}{',' if ncol == 1 else ''}),",
             "  table.header(" + ", ".join(f"[{protect_line_starts(inline(h, ctx))}]" for h in header) + "),"]
    for r in body:
        lines.append("  " + ", ".join(f"[{protect_line_starts(inline(x, ctx))}]" for x in r) + ",")
    lines.append(")")
    t = "\n".join(lines)
    if ncol >= 9:
        return f"#landscape-table[\n{t}\n]"
    if ncol >= 6:
        return f"#small-table[\n{t}\n]"
    return t


def emit_list(items, ctx: Ctx) -> str:
    out = []
    for mk, text in items:
        marker = "-" if mk in "-*+" else mk
        box = ""
        m = re.match(r"^\[( |x)\] (.*)$", text, re.S)
        if m:
            box = "#sym.ballot " if m.group(1) == " " else "#sym.ballot.check "
            text = m.group(2)
        body = protect_line_starts(inline(text, ctx))
        pad = " " * (len(marker) + 1)
        body = body.replace("\n", "\n" + pad)
        out.append(f"{marker} {box}{body}")
    return "\n".join(out)


class Emitter:
    def __init__(self, ctx: Ctx, figdir: Path | None):
        self.ctx = ctx
        self.figdir = figdir
        self.mermaid: list[tuple[str, str]] = []
        self.generated: dict[str, str] = {}
        self.last_heading = "start"

    def heading(self, level: int, text: str, labels: set[str]) -> str:
        s = slug(text)
        body = protect_line_starts(inline(text, self.ctx))
        lab = f" <{s}>" if (level == 1 or s in labels) else ""
        return "=" * level + " " + body + lab

    def figure(self, num: str, caption: str, body: str) -> str:
        return f'#aa-figure(num: "{num}", caption: [{caption}])[\n{body}\n]'

    def blocks(self, blocks: list[tuple], labels: set[str], relroot: str) -> str:
        out: list[str] = []
        k = 0
        while k < len(blocks):
            b = blocks[k]
            nxt = blocks[k + 1] if k + 1 < len(blocks) else None
            cap = None
            if b[0] in ("fence", "image") and nxt and nxt[0] == "para" and \
                    re.match(r"^\*Figure \w+:", nxt[1]) and not (b[0] == "fence" and b[1] == "math"):
                m = re.match(r"^\*Figure (\w+): (.*)\*$", nxt[1], re.S)
                assert m, nxt[1][:80]
                cap = (m.group(1), protect_line_starts(inline(m.group(2), self.ctx)))
            kind = b[0]
            if kind == "heading":
                self.last_heading = slug(b[2])
                out.append(self.heading(b[1], b[2], labels))
            elif kind == "para":
                out.append(protect_line_starts(inline(b[1], self.ctx)))
            elif kind == "list":
                out.append(emit_list(b[1], self.ctx))
            elif kind == "table":
                out.append(emit_table(b[1], self.ctx))
            elif kind == "quote":
                inner = self.blocks(b[1], labels, relroot)
                out.append(f"#caveat[\n{inner}\n]")
            elif kind == "hr":
                if nxt is None or (nxt[0] == "heading" and nxt[1] == 1):
                    pass
                else:
                    out.append("#rule()")
            elif kind == "comment":
                m = re.match(r"<!-- stackup:begin (\w+) -->", b[1])
                if m:
                    name = m.group(1)
                    j = k + 1
                    while not (blocks[j][0] == "comment" and f"stackup:end {name}" in blocks[j][1]):
                        j += 1
                    inner = self.blocks(blocks[k + 1:j], labels, "..")
                    self.generated[name] = inner
                    out.append(f'#include "{relroot}/generated/stackup-{name}.typ"')
                    k = j + 1
                    continue
                raise ValueError(b[1])
            elif kind == "fence":
                lang, content = b[1], b[2]
                if lang == "math":
                    out.append("$ " + latex(content) + " $")
                elif lang == "mermaid":
                    if cap:
                        digits = re.match(r"\d+", cap[0]).group(0)
                        name = "figure-%02d%s" % (int(digits), cap[0][len(digits):])
                    else:
                        name = "diagram-" + self.last_heading
                    self.mermaid.append((name, content))
                    w = FIGURE_WIDTH.get(cap[0] if cap else name, "100%")
                    img = f'#image("{relroot}/figures/mermaid/{name}.svg", width: {w})'
                    out.append(self.figure(cap[0], cap[1], img) if cap else f"#diagram[\n{img}\n]")
                elif lang == "text":
                    raw = "```text\n" + content + "\n```"
                    out.append(self.figure(cap[0], cap[1], raw) if cap else raw)
                else:
                    raise ValueError(lang)
            elif kind == "image":
                assert cap
                w = FIGURE_WIDTH.get(cap[0], "100%")
                img = f'#image("{relroot}/{b[2]}", width: {w}, alt: "{b[1]}")'
                out.append(self.figure(cap[0], cap[1], img))
            if cap:
                k += 2
            else:
                k += 1
        return "\n\n".join(out)


# ---------------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------------
GROUP_KEYS = {
    "Textbooks": ("textbooks", "index-level"),
    "Repository": ("repository", "repository-record"),
    "Literature": ("literature", "index-level"),
    "IEEE contest": ("ieee-pages", "snippet-only"),
}


def evidence_of(text: str, default: str) -> str:
    if re.search(r"located but not (verified|retrievable)", text):
        return "unverified"
    if "Full text" in text:
        return "full"
    for word, label in (("Abstract", "abstract"), ("Bibliographic", "bibliographic")):
        if re.search(rf"\b{word}\b", text):
            return label
    if re.search(r"\b[Ii]ndex level\b", text):
        return "index-level"
    return default


def parse_references(blocks: list[tuple], ctx: Ctx):
    groups, intro = [], []
    cur = None
    for b in blocks:
        if b[0] == "heading" and b[1] == 3:
            key = next(v for k, v in GROUP_KEYS.items() if b[2].startswith(k))
            cur = {"key": key[0], "title": b[2], "default": key[1], "entries": []}
            groups.append(cur)
        elif b[0] == "list" and cur:
            for _, text in b[1]:
                text = text.replace("\n", " ")
                m = re.match(rf"^((?:\[{CITE_ID}\](?:, | to )?)+:?) (.*)$", text, re.S)
                assert m, text
                ids = re.findall(rf"\[({CITE_ID})\]", m.group(1))
                e = {"id": ids[0], "ids": ids, "label": m.group(1), "group": cur["key"],
                     "evidence": evidence_of(m.group(2), cur["default"]),
                     "markdown": m.group(2), "typst": inline(m.group(2), ctx)}
                if "preprint" in m.group(2):
                    e["preprint"] = True
                cur["entries"].append(e)
        elif cur is None and b[0] == "para":
            intro.append(b[1])
    return intro, groups


def yaml_bibliography(groups) -> str:
    q = lambda s: json.dumps(s, ensure_ascii=False)  # noqa: E731, JSON strings are YAML
    out = [
        "# Bibliography of the AetherArray master technical reference, version 0.2.",
        "#",
        "# Extracted by tools/docs/md_to_typst.py from the References section of",
        "# docs/aetherarray-master-reference.md. backmatter/references.typ renders it.",
        "#",
        "# Fields:",
        "#   label     the identifier text exactly as printed, for example \"[B1]\"",
        "#   group     section of the reference list",
        "#   evidence  the verification level that the entry text or its group heading states:",
        "#             full, abstract, bibliographic, index-level, snippet-only, unverified,",
        "#             or repository-record (details are in docs/references/bibliography.md).",
        "#             It restates the printed entry and is never stronger than it.",
        "#   preprint  present and true when the entry says it is a preprint",
        "#   text      the entry as printed, in Typst markup; the printed text is authoritative",
        "#   source    the same entry in the Markdown of the canonical document",
        "",
        "groups:",
    ]
    for g in groups:
        out += [f"  - key: {g['key']}", f"    title: {q(g['title'])}",
                f"    default-evidence: {g['default']}", "    entries:"]
        for e in g["entries"]:
            out += [f"      - id: {e['id']}",
                    f"        ids: [{', '.join(e['ids'])}]",
                    f"        label: {q(e['label'])}",
                    f"        evidence: {e['evidence']}"]
            if e.get("preprint"):
                out.append("        preprint: true")
            out += [f"        text: {q(e['typst'])}", f"        source: {q(e['markdown'])}"]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------------
HEADER = '#import "{rel}/template.typ": *\n\n'


def split_sections(blocks):
    """Top level sections, keyed by output file."""
    files: list[tuple[str, list]] = []
    cur_name, cur = "chapters/front-matter", []
    for b in blocks:
        if b[0] == "heading" and b[1] == 1 and cur and b[2] != "AetherArray: master technical reference":
            files.append((cur_name, cur))
            t = b[2]
            if t.startswith("Part "):
                key = t.split(" ")[0] + " " + t.split(" ")[1]
                cur_name = "chapters/" + PART_FILES[key]
            elif t == "Appendices":
                cur_name = "appendices/00-appendices"
            elif t == "References":
                cur_name = "backmatter/references"
            elif t.startswith("Review"):
                cur_name = "backmatter/review"
            else:
                raise ValueError(t)
            cur = []
        if b[0] == "heading" and b[1] == 2 and b[2].startswith("Appendix "):
            files.append((cur_name, cur))
            cur_name, cur = "appendices/" + APPENDIX_FILES[b[2].split(" ")[1].rstrip(".")], []
        if b[0] == "heading" and b[1] == 2 and b[2].startswith("10bis."):
            files.append((cur_name, cur))
            cur_name, cur = "chapters/01b-isac-10bis", []
        if b[0] == "heading" and b[1] == 2 and b[2].startswith("11. ") and cur_name.endswith("10bis"):
            files.append((cur_name, cur))
            cur_name, cur = "chapters/01c-course-theory-continued", []
        cur.append(b)
    files.append((cur_name, cur))
    return files


def write_editable(files: dict[Path, str], force: bool) -> list[Path]:
    """Write hand-editable files: new ones always, changed ones only with force."""
    changed = [p for p, t in files.items() if p.exists() and p.read_text(encoding="utf-8") != t]
    if changed and force:
        print("WARNING: --force overwrites these hand-editable files, and any hand edits in "
              "them are lost. Review or back up the diff first (git diff, git stash).",
              file=sys.stderr)
        for p in changed:
            print(f"  overwriting {p.relative_to(REPO)}", file=sys.stderr)
    written = []
    for p, t in files.items():
        if p.exists() and p.read_text(encoding="utf-8") == t:
            continue
        if p in changed and not force:
            print(f"kept, differs from the Markdown (use --force to overwrite): {p.relative_to(REPO)}")
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8")
        written.append(p)
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--generated", action="store_true", help="rewrite generated/ only")
    ap.add_argument("--force", action="store_true",
                    help="overwrite hand-editable files (lists them in a warning first)")
    args = ap.parse_args()

    md = SRC.read_text(encoding="utf-8").split("\n")
    blocks = parse_blocks(md)

    # identifiers that have an entry in the reference list
    refids = set()
    in_refs = False
    for b in blocks:
        if b[0] == "heading" and b[1] == 1:
            in_refs = b[2] == "References"
        if in_refs and b[0] == "list":
            for _, t in b[1]:
                refids.update(re.findall(rf"\[({CITE_ID})\]", t.split("]")[0] + "]"))
                m = re.match(rf"^((?:\[{CITE_ID}\](?:, | to )?)+)", t)
                if m:
                    refids.update(re.findall(CITE_ID, m.group(1)))
    # internal link targets, gathered in a dry run
    ctx = Ctx(refids, set())
    sections = split_sections(blocks)
    for _, bl in sections:
        Emitter(ctx, None).blocks(bl, set(), "..")
    labels = set(ctx.labels)

    em = Emitter(ctx, OUT / "figures")
    editable: dict[Path, str] = {}
    for name, bl in sections:
        if name == "backmatter/references":
            heading = bl[0]
            intro, groups = parse_references(bl[1:], ctx)
            editable[OUT / "bibliography.yml"] = yaml_bibliography(groups)
            body = (em.heading(heading[1], heading[2], labels) + "\n\n" +
                    "\n\n".join(protect_line_starts(inline(p, ctx)) for p in intro) + "\n\n" +
                    '#let bib = yaml("../bibliography.yml")\n\n#reference-list(bib)')
        else:
            body = em.blocks(bl, labels, "..")
        if name == "chapters/01-course-theory":
            body += '\n\n#include "01b-isac-10bis.typ"\n\n#include "01c-course-theory-continued.typ"'
        text = HEADER.format(rel="..") + body + "\n"
        editable[OUT / f"{name}.typ"] = text

    gdir = OUT / "generated"
    gdir.mkdir(parents=True, exist_ok=True)
    for name, inner in em.generated.items():
        (gdir / f"stackup-{name}.typ").write_text(
            GEN_NOTE.format(name=name) + "\n" + HEADER.format(rel="..") + inner + "\n", encoding="utf-8")
    for name, content in em.mermaid:
        editable[OUT / "figures" / "mermaid" / f"{name}.mmd"] = content + "\n"
    written = [] if args.generated else write_editable(editable, args.force)
    print(f"{len(written)} hand-editable files written, {len(em.generated)} generated tables, "
          f"{len(em.mermaid)} mermaid sources, {len(refids)} reference identifiers")
    print("files:", " ".join(n for n, _ in sections))


if __name__ == "__main__":
    main()
