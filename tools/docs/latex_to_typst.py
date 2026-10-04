"""Translate the LaTeX (KaTeX) mathematics of the master reference into Typst math.

Only the subset of LaTeX that docs/aetherarray-master-reference.md actually uses is
supported. Anything else raises LatexError, so a new construct is noticed rather than
silently mistranslated. Used by tools/docs/md_to_typst.py.

Typst conventions relied on:
  - tokens are separated by spaces, so adjacent letters never merge into an identifier
    and no accidental function call or shorthand (such as <= or ->) can form;
  - inside a function call (frac, sqrt, lr, ...) commas, semicolons and colons are
    escaped, because there they would separate arguments;
  - vb() and sf() are helpers defined in template.typ for upright bold and upright
    sans serif letters, the LaTeX meaning of \\mathbf and \\mathsf.
"""
from __future__ import annotations

import re

TOKEN = re.compile(r"\\[A-Za-z]+|\\.|[{}^_&]|\s+|[A-Za-z]|[0-9]+(?:\.[0-9]+)?|.", re.S)


class LatexError(ValueError):
    pass


GREEK = {
    "alpha": "alpha", "beta": "beta", "gamma": "gamma", "delta": "delta",
    "epsilon": "epsilon.alt", "varepsilon": "epsilon", "zeta": "zeta", "eta": "eta",
    "theta": "theta", "vartheta": "theta.alt", "iota": "iota", "kappa": "kappa",
    "lambda": "lambda", "mu": "mu", "nu": "nu", "xi": "xi", "pi": "pi", "rho": "rho",
    "sigma": "sigma", "tau": "tau", "upsilon": "upsilon", "phi": "phi.alt",
    "varphi": "phi", "chi": "chi", "psi": "psi", "omega": "omega",
    "Gamma": "Gamma", "Delta": "Delta", "Theta": "Theta", "Lambda": "Lambda",
    "Xi": "Xi", "Pi": "Pi", "Sigma": "Sigma", "Phi": "Phi", "Psi": "Psi", "Omega": "Omega",
}

SYMBOLS = {
    "approx": "approx", "pm": "plus.minus", "mp": "minus.plus", "leq": "lt.eq",
    "le": "lt.eq", "geq": "gt.eq", "ge": "gt.eq", "neq": "eq.not", "ne": "eq.not",
    "times": "times", "in": "in", "mid": "divides", "propto": "prop", "cdot": "dot.op",
    "circ": "compose", "dots": "dots.h", "ldots": "dots.h", "cdots": "dots.c",
    "star": "star", "to": "arrow.r", "rightarrow": "arrow.r",
    "longrightarrow": "arrow.r.long", "infty": "infinity", "ll": "lt.double",
    "gg": "gt.double", "ell": "ell", "imath": "dotless.i", "partial": "partial",
    "sum": "sum", "prod": "product", "sin": "sin", "cos": "cos", "tan": "tan",
    "log": "log", "ln": "ln", "arg": "arg", "max": "max", "min": "min", "exp": "exp",
    "Pr": 'op("Pr")', "top": "top", "sim": "tilde.op", "equiv": "equiv",
    "{": "\\{", "}": "\\}", "_": "\\_", "%": "\\%", "&": "\\&", "#": "\\#",
}

SPACES = {",": "thin", ":": "med", ";": "thick", " ": "space", "quad": "quad", "qquad": "wide"}
DROPPED = {"!", "textstyle", "displaystyle"}

ACCENTS = {"tilde": "tilde", "hat": "hat", "bar": "macron", "underline": "underline",
           "overline": "overline", "vec": "arrow", "dot": "dot"}
FONTS = {"mathbf": "vb", "boldsymbol": "bold", "mathsf": "sf", "mathbb": "bb",
         "mathcal": "cal", "mathrm": "upright"}

DELIMS = {"(": "(", ")": ")", "[": "[", "]": "]", "\\{": "{", "\\}": "}", "|": "|",
          "\\lvert": "|", "\\rvert": "|", "\\vert": "|", "\\lVert": "‖", "\\rVert": "‖",
          "\\|": "‖", ".": ""}

PLAIN_ESCAPE = {"/": "\\/", '"': '\\"', "$": "\\$", "#": "\\#", "@": "\\@", "\\": "\\\\",
                "~": "space", "`": "\\`", "'": "'"}
ARG_ESCAPE = {",": "\\,", ";": "\\;", ":": "colon"}

SIMPLE_ATOM = re.compile(r'^(?:[A-Za-z]|[0-9]+(?:\.[0-9]+)?|"[^"]*"|[A-Za-z]+(?:\.[a-z]+)*)$')


class Parser:
    def __init__(self, src: str):
        self.toks = [t for t in TOKEN.findall(src)]
        self.i = 0

    # -- token helpers -------------------------------------------------------------
    def peek(self, skip_ws: bool = True):
        j = self.i
        while skip_ws and j < len(self.toks) and self.toks[j].isspace():
            j += 1
        return self.toks[j] if j < len(self.toks) else None

    def next(self, skip_ws: bool = True):
        while skip_ws and self.i < len(self.toks) and self.toks[self.i].isspace():
            self.i += 1
        if self.i >= len(self.toks):
            raise LatexError("unexpected end of formula")
        t = self.toks[self.i]
        self.i += 1
        return t

    def raw_group(self) -> str:
        """The verbatim text of a {...} group, for \\text and \\operatorname."""
        if self.next() != "{":
            raise LatexError("expected {")
        depth, out = 1, []
        while True:
            t = self.next(skip_ws=False)
            if t == "{":
                depth += 1
            elif t == "}":
                depth -= 1
                if depth == 0:
                    return "".join(out)
            out.append(t)

    # -- grammar -------------------------------------------------------------------
    def arg(self, in_arg: bool) -> list[str]:
        """One argument: a {group} or a single token with its own arguments."""
        t = self.peek()
        if t == "{":
            self.next()
            return self.seq(in_arg, stop={"}"}, consume_stop=True)
        return self.atom(in_arg)

    def seq(self, in_arg: bool, stop: set, consume_stop: bool = False) -> list[str]:
        out: list[str] = []
        while True:
            t = self.peek()
            if t is None:
                if stop - {None}:
                    raise LatexError(f"missing {stop}")
                return out
            if t in stop:
                if consume_stop:
                    self.next()
                return out
            if t in ("^", "_"):
                self.next()
                sub = self.arg(in_arg)
                if t == "^" and sub == ["compose"]:
                    sub = ["degree"]
                if sub == ["degree"]:
                    out.append("degree")
                    continue
                body = " ".join(sub)
                if not out:
                    out.append('""')
                if len(sub) == 1 and SIMPLE_ATOM.match(sub[0]):
                    out[-1] += t + body
                else:
                    out[-1] += f"{t}({body})"
                continue
            out.extend(self.atom(in_arg))

    def atom(self, in_arg: bool) -> list[str]:
        t = self.next()
        if t == "{":
            return self.seq(in_arg, stop={"}"}, consume_stop=True)
        if t.startswith("\\") and len(t) > 1:
            return self.command(t[1:], in_arg)
        if in_arg and t in ARG_ESCAPE:
            return [ARG_ESCAPE[t]]
        if t in PLAIN_ESCAPE:
            return [PLAIN_ESCAPE[t]]
        if t == "&":
            raise LatexError("& outside a matrix")
        return [t]

    def command(self, name: str, in_arg: bool) -> list[str]:
        if name in GREEK:
            return [GREEK[name]]
        if name in SYMBOLS:
            return [SYMBOLS[name]]
        if name in SPACES:
            return [SPACES[name]]
        if name in DROPPED:
            return []
        if name in ("frac", "tfrac", "dfrac"):
            a = " ".join(self.arg(True))
            b = " ".join(self.arg(True))
            return [f"frac({a}, {b})"]
        if name == "binom":
            a = " ".join(self.arg(True))
            b = " ".join(self.arg(True))
            return [f"binom({a}, {b})"]
        if name == "sqrt":
            return [f"sqrt({' '.join(self.arg(True))})"]
        if name == "text":
            txt = self.raw_group().replace("\\_", "_").replace("\\%", "%").replace("\\&", "&")
            txt = txt.replace("\\", "\\\\").replace('"', '\\"')
            return [f'"{txt}"']
        if name == "operatorname":
            return [f'op("{self.raw_group()}")']
        if name in FONTS:
            inner = self.arg(True)
            body = " ".join(inner)
            letters = re.fullmatch(r"(?:[A-Za-z] )+[A-Za-z]", body)
            if letters:
                body = '"' + body.replace(" ", "") + '"'
            return [f"{FONTS[name]}({body})"]
        if name in ACCENTS:
            return [f"{ACCENTS[name]}({' '.join(self.arg(True))})"]
        if name == "underbrace":
            body = " ".join(self.arg(True))
            if self.peek() == "_":
                self.next()
                lab = " ".join(self.arg(True))
                return [f"underbrace({body}, {lab})"]
            return [f"underbrace({body})"]
        if name == "left":
            return [self.left()]
        if name == "middle":
            d = self.delim()
            return [f"mid({d})"]
        if name == "lvert":
            inner = self.seq(True, stop={"\\rvert"}, consume_stop=True)
            return [f"abs({' '.join(inner)})"]
        if name == "lVert":
            inner = self.seq(True, stop={"\\rVert"}, consume_stop=True)
            return [f"norm({' '.join(inner)})"]
        if name == "begin":
            env = self.raw_group()
            if env != "bmatrix":
                raise LatexError(f"environment {env}")
            return [self.matrix()]
        if name == "\\":
            return ["\\"]
        raise LatexError(f"unsupported command \\{name}")

    def delim(self) -> str:
        t = self.next()
        if t not in DELIMS:
            raise LatexError(f"bad delimiter {t}")
        d = DELIMS[t]
        return {"{": "\\{", "}": "\\}"}.get(d, d)

    def left(self) -> str:
        ld = self.delim()
        inner = self.seq(True, stop={"\\right"}, consume_stop=True)
        rd = self.delim()
        body = " ".join(inner)
        return f"lr({ld} {body} {rd})".replace("(  ", "( ").replace("  )", " )")

    def matrix(self) -> str:
        rows, row, cell = [], [], []
        while True:
            t = self.peek()
            if t is None:
                raise LatexError("unterminated matrix")
            if t == "\\end":
                self.next()
                self.raw_group()
                row.append(" ".join(cell))
                rows.append(row)
                break
            if t == "&":
                self.next()
                row.append(" ".join(cell))
                cell = []
                continue
            if t == "\\\\":
                self.next()
                row.append(" ".join(cell))
                rows.append(row)
                row, cell = [], []
                continue
            cell.extend(self.seq(True, stop={"&", "\\\\", "\\end"}))
        body = "; ".join(", ".join(c.strip() for c in r) for r in rows)
        return f'mat(delim: "[", {body})'


def convert(src: str) -> str:
    p = Parser(src)
    out = p.seq(False, stop={None})
    if p.peek() is not None:
        raise LatexError(f"trailing token {p.peek()}")
    s = re.sub(r"\s+", " ", " ".join(out)).strip()
    # Typst keeps the space between a text string and a parenthesis: "SIR" (w) would
    # print a gap that \text{SIR}(\mathbf{w}) does not have.
    return re.sub(r'(?<!\\)"\s+\(', '"(', s)


if __name__ == "__main__":
    import sys
    print(convert(sys.argv[1]))
