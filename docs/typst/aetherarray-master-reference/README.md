# AetherArray master technical reference, Typst edition

- Status: Typst edition of version 0.2 of `docs/aetherarray-master-reference.md`, converted at
  repository revision `415cb685a34be02bb3de3a589be7b1a02ccbae80`
- Entry point: `main.typ`
- Compiler: Typst 0.15.1 (any 0.15.x should work)

> **Warning. Do not run the forced Markdown-to-Typst regeneration over hand-edited Typst
> content without first reviewing/backing up the diff.** `python tools/docs/md_to_typst.py
> --force` rewrites the chapter, appendix and back matter files, `bibliography.yml` and the
> Mermaid sources from the Markdown. It lists every file it is about to overwrite in a warning,
> then overwrites it, and any hand edit in those files is lost.

## Source policy

- `docs/aetherarray-master-reference.md` is the canonical scientific and content source.
- This folder is the editable publication and layout edition, generated from that Markdown.
- Content and scientific corrections are normally made in the Markdown first, then propagated
  to Typst (see "Propagating a Markdown change" below).
- Hand edits of the Typst files are meant mainly for layout and publication work: the
  template, page breaks, figure sizes, table widths.

This folder is a self-contained Typst project. It holds the full text of the master technical
reference, Parts 0 to XXI with section 10bis, the appendices A to L, the references and the
five-reader review. Equations are native Typst mathematics, tables are Typst tables and
diagrams are SVG files. Nothing in it needs Mermaid, Python or a network connection to compile.

## Opening it in typst.app

1. Download the ZIP `AetherArray_Master_Reference_v0.2_Typst.zip`, or zip this folder.
2. In typst.app, create an empty project, then use "Upload files" and drop the whole content of
   the ZIP, keeping the folder structure (`chapters/`, `appendices/`, `backmatter/`,
   `figures/`, `generated/`).
3. Make `main.typ` the main file (file menu, "Set as main file") if typst.app did not pick it.

The template uses only fonts that ship with the Typst compiler (Libertinus Serif, New Computer
Modern Math, DejaVu Sans Mono), so typst.app and a local compiler give the same pages.

## Compiling locally

```sh
typst compile main.typ AetherArray_Master_Reference_v0.2.pdf
```

Run it from this folder. `typst watch main.typ` recompiles on every save.

## Where things are

| Path | Content |
| --- | --- |
| `main.typ` | entry point: loads the template and metadata, includes every part in order |
| `template.typ` | page layout, headings, tables, figure captions, title page, contents |
| `metadata.typ` | title, version, date, repository revision, PDF properties |
| `chapters/front-matter.typ` | document status, how to use the document, contents overview |
| `chapters/00-overview.typ` to `chapters/21-synthesis.typ` | Parts 0 to XXI, one file per part |
| `chapters/01b-isac-10bis.typ` | section 10bis, integrated sensing and communication, kept in its own file |
| `chapters/01c-course-theory-continued.typ` | sections 11 and 12, the end of Part I |
| `appendices/` | the Appendices heading and one file per appendix, A to L |
| `backmatter/references.typ` | the reference list, rendered from `bibliography.yml` |
| `backmatter/review.typ` | review from five reader perspectives |
| `bibliography.yml` | every reference entry, with its identifier, group and evidence level |
| `figures/*.svg` | the three analytical plots (steering, null filling, switched line dispersion) |
| `figures/mermaid/*.mmd` | Mermaid sources of the 14 diagrams |
| `figures/mermaid/*.svg` | the same diagrams pre-rendered for Typst |
| `generated/stackup-*.typ` | the nine stack-up tables generated from the canonical stack-up file |

Helpers defined in `template.typ` and used in the chapters:

- `caveat[...]`: a boxed statement, used for every blockquote of the canonical document;
- `aa-figure(num: "7a", caption: [...])[...]`: a figure with the number printed in the text;
- `diagram[...]`: an uncaptioned diagram;
- `small-table[...]` and `landscape-table[...]`: wide tables in smaller type, or on a
  landscape page of their own;
- `vb(x)` and `sf(x)` in mathematics: upright bold and upright sans serif letters, the
  meaning of `\mathbf` and `\mathsf` in the canonical document.

Section numbers are part of the heading text and figure numbers are given explicitly, as in the
canonical document, because the text refers to them by those numbers.

## Editing

The files in `chapters/`, `appendices/` and `backmatter/` are ordinary Typst and can be
edited by hand, mainly for layout and publication work (see the source policy above).

### Propagating a Markdown change

1. Edit `docs/aetherarray-master-reference.md`.
2. From the repository root, run `python tools/docs/md_to_typst.py`. Without `--force` it only
   creates missing files and reports every existing file that now differs from the Markdown;
   it overwrites nothing.
3. Bring the change into those Typst files by hand, or, after reviewing and backing up the
   diff (`git diff`, `git stash`), run it again with `--force`, which warns before overwriting.
4. Rebuild with `python tools/docs/build_typst_edition.py`.

Three kinds of file are generated and should not be edited by hand:

- `generated/stackup-*.typ`, from `hardware/rev-a/stackup/reva-stackup.json`. From the
  repository root, run `cd tools && python -m rfkit.cli stackup --write-docs`, then
  `python tools/docs/md_to_typst.py --generated`;
- `figures/mermaid/*.svg`. Edit the `.mmd` file next to it, then run
  `python tools/docs/render_typst_figures.py` (it needs mermaid-cli);
- `figures/steering-n4.svg`, `figures/null-filling-n4.svg` and
  `figures/switched-line-dispersion.svg`. Run `python tools/docs/master_reference_figures.py`,
  then `python tools/docs/render_typst_figures.py`, which copies them here.

`bibliography.yml` was extracted from the reference list. Its `evidence` field restates the
verification level that the printed entry or its group heading gives (full, abstract,
bibliographic, index-level, snippet-only, unverified or repository-record). It is never
stronger than the printed entry. If you edit an entry, keep its `text` and its `evidence`
consistent.

## How this edition was made

`tools/docs/md_to_typst.py` converted the Markdown, with `tools/docs/latex_to_typst.py` for
the mathematics. It carries the text, equations, tables, caveats and captions over without
rewording them. The title page, the automatic table of contents and the list of figures are the
only additions.

## Building the PDF and the ZIP

From the repository root:

```sh
python tools/docs/build_typst_edition.py --typst /path/to/typst
```

It writes `docs/build/AetherArray_Master_Reference_v0.2.pdf` and
`docs/build/AetherArray_Master_Reference_v0.2_Typst.zip`, then extracts the ZIP into a
temporary folder and compiles `main.typ` there to prove that the archive is self-contained and
importable into typst.app as is. `docs/build/` is ignored by git: both files are reproducible
from the sources.
