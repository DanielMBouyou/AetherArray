// Layout of the AetherArray master technical reference.
//
// A restrained technical report: A4, serif body, numbered pages, running header with
// the current part, figure captions, repeated table headers. Section numbers are part
// of the heading text (they come from the canonical Markdown), so Typst heading
// numbering is off. Figure numbers are likewise given explicitly (1 to 20, plus 5b,
// 7a and 7b), because the text refers to them by those numbers.
//
// Only fonts embedded in the Typst compiler are used (Libertinus Serif, New Computer
// Modern Math, DejaVu Sans Mono), so the output is the same on typst.app and locally.

#import "metadata.typ": meta

// -- colours ----------------------------------------------------------------------
#let ink = rgb("#1b1f24")
#let accent = rgb("#1f3a5f")
#let muted = rgb("#5b6773")
#let hairline = rgb("#b8c0c8")
#let shade = rgb("#f2f4f6")
#let note-fill = rgb("#f7f4ec")
#let note-rule = rgb("#a8873a")

// -- maths helpers used by the chapters --------------------------------------------
// LaTeX \mathbf and \mathsf are upright; Typst bold() and sans() keep italics.
#let vb(x) = math.bold(math.upright(x))
#let sf(x) = math.sans(math.upright(x))

// -- blocks used by the chapters ---------------------------------------------------

// A Markdown blockquote of the canonical document: caveats and key statements.
#let caveat(body) = block(
  width: 100%,
  fill: note-fill,
  stroke: (left: 2pt + note-rule),
  inset: (left: 10pt, right: 8pt, y: 7pt),
  breakable: true,
  body,
)

// A thematic break inside a part.
#let rule() = align(center, line(length: 40%, stroke: 0.5pt + hairline))

// A numbered figure. `num` is the figure number as printed in the text, a string.
#let aa-figure(num: none, caption: none, body) = figure(
  body,
  caption: caption,
  kind: image,
  supplement: [Figure],
  numbering: _ => num,
)

// A diagram without a caption or number, as in the canonical document.
#let diagram(body) = block(width: 100%, breakable: false, align(center, body))

// Tables with six to eight columns: smaller type.
#let small-table(body) = {
  show table: set text(size: 7.4pt)
  body
}

// Tables with nine or more columns: smaller type on a landscape page of their own.
#let landscape-table(body) = page(flipped: true, {
  show table: set text(size: 8.2pt)
  body
})

// The reference list, rendered from bibliography.yml. The printed entry text is kept
// exactly; the evidence field of the data file restates it and is not printed again.
#let reference-list(bib) = {
  for g in bib.groups {
    heading(level: 3, g.title)
    for e in g.entries {
      for id in e.ids [#metadata(id)#label("ref-" + id)]
      block(spacing: 0.75em, par(hanging-indent: 1.6em, justify: false)[
        #e.label #eval(e.text, mode: "markup", scope: (vb: vb, sf: sf))
      ])
    }
  }
}

// -- title page --------------------------------------------------------------------
#let title-page(m) = page(header: none, footer: none, margin: (x: 25mm, top: 45mm, bottom: 30mm), {
  set par(justify: false)
  text(size: 34pt, weight: "bold", fill: accent, m.title)
  v(6mm)
  text(size: 15pt, fill: ink, m.subtitle)
  v(14mm)
  line(length: 100%, stroke: 1pt + accent)
  v(6mm)
  text(size: 20pt, fill: ink, m.doc-type)
  v(4mm)
  text(size: 12pt)[Version #m.version]
  linebreak()
  text(size: 12pt, m.date-text)
  v(1fr)
  set text(size: 9pt, fill: muted)
  grid(
    columns: (auto, 1fr),
    column-gutter: 4mm,
    row-gutter: 2.2mm,
    [Repository revision:], raw(m.revision),
    [Typst source compiled from:], [`main.typ`, converted from #raw(m.source)],
  )
})

// -- table of contents ---------------------------------------------------------------
#let front-outline() = {
  set page(numbering: "i")
  counter(page).update(1)
  show outline.entry.where(level: 1): it => {
    v(5pt, weak: true)
    strong(it)
  }
  outline(title: [Contents], depth: 2, indent: auto)
  pagebreak(weak: true)
  outline(title: [List of figures], target: figure.where(kind: image))
}

// Starts the arabic page numbering of the body.
#let body-start() = {
  pagebreak(weak: true)
  set page(numbering: "1")
  counter(page).update(1)
}

// -- the report ------------------------------------------------------------------------
#let aa-report(m, body) = {
  set document(
    title: m.pdf-title,
    author: m.pdf-author,
    description: m.pdf-subject,
    keywords: m.pdf-keywords,
    date: m.date,
  )
  set text(font: "Libertinus Serif", size: 10pt, fill: ink, lang: "en", region: "gb")
  set par(justify: true, leading: 0.62em, spacing: 0.95em)
  show math.equation: set text(font: "New Computer Modern Math")
  show raw: set text(font: "DejaVu Sans Mono")
  show raw.where(block: false): set text(size: 0.86em)
  show link: set text(fill: accent)

  set page(
    paper: "a4",
    margin: (x: 20mm, top: 24mm, bottom: 22mm),
    numbering: "1",
    header: context {
      let pg = here().page()
      let starts = query(heading.where(level: 1)).filter(h => h.location().page() == pg)
      if pg == 1 or starts.len() > 0 { return }
      let before = query(heading.where(level: 1).before(here()))
      set text(size: 8pt, fill: muted)
      grid(
        columns: (1fr, auto),
        meta.short-title,
        if before.len() > 0 { before.last().body },
      )
      v(-5pt)
      line(length: 100%, stroke: 0.4pt + hairline)
    },
    footer: context {
      if here().page() == 1 { return }
      set text(size: 8.5pt, fill: muted)
      align(center, counter(page).display())
    },
  )

  // Headings: numbers are in the text, so no automatic numbering.
  set heading(numbering: none)
  show heading: set text(fill: accent)
  show heading: set par(justify: false)
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(4mm)
    block(below: 9mm, {
      text(size: 21pt, weight: "bold", it.body)
      v(1mm)
      line(length: 100%, stroke: 0.8pt + accent)
    })
  }
  show heading.where(level: 2): set text(size: 13.5pt)
  show heading.where(level: 2): set block(above: 1.7em, below: 0.9em)
  show heading.where(level: 3): set text(size: 11.2pt)
  show heading.where(level: 3): set block(above: 1.4em, below: 0.75em)
  show heading.where(level: 4): set text(size: 10.2pt, style: "italic")

  // Code and ASCII diagrams: never wrapped, the type shrinks so the longest line fits.
  show raw.where(block: true): it => layout(size => {
    let n = calc.max(1, ..it.text.split("\n").map(l => l.clusters().len()))
    // Inside a figure the available width can be reported as unbounded: cap it at the
    // text width of a portrait page.
    let avail = calc.min(size.width.to-absolute(), 170mm) - 14pt
    let s = calc.min(8.4pt, avail / (0.625 * n))  // 0.602 em advance, plus slack
    set text(size: s)
    set par(justify: false)
    block(width: 100%, fill: shade, inset: 7pt, radius: 1.5pt, it)
  })

  // Display equations wider than the text are scaled down rather than overflowing.
  show math.equation.where(block: true): it => layout(size => {
    let w = measure(it).width
    if w > size.width {
      scale(size.width / w * 100%, reflow: true, it)
    } else { it }
  })

  // Tables: hairlines, repeated header row, compact type.
  set table(
    stroke: (x, y) => (
      top: if y == 0 { 0.8pt + ink } else if y == 1 { 0.6pt + ink } else { 0pt },
      bottom: 0.3pt + hairline,
    ),
    inset: (x: 4pt, y: 3.6pt),
    align: left + top,
    fill: (x, y) => if y > 0 and calc.even(y) { shade },
  )
  show table: set text(size: 8.6pt)
  show table: set par(justify: false, leading: 0.5em)
  show table.cell.where(y: 0): set text(weight: "bold")
  show table: it => block(width: 100%, above: 1.1em, below: 1.1em, it)

  // Figures and captions.
  show figure: set block(breakable: false, above: 1.4em, below: 1.4em)
  set figure.caption(separator: [: ])
  show figure.caption: it => {
    set text(size: 8.8pt)
    set par(justify: false)
    block(width: 100%, align(left, [*#it.supplement #context it.counter.display(it.numbering)*#it.separator#it.body]))
  }

  set list(indent: 0.6em, body-indent: 0.5em, spacing: 0.7em)
  set enum(indent: 0.6em, body-indent: 0.5em, spacing: 0.7em)

  body
}
