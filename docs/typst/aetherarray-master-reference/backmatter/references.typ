#import "../template.typ": *

= References <references>

Verification levels: *full* means the source was read for the repository's bibliography as
recorded there; *abstract* means abstract only, as recorded there; *index level* means
bibliographic details and abstract wording seen in search engine results on 2026-10-04, with no
full text read; *snippet only* means the official page itself could not be opened. Identifiers
beginning A, V, T and R are those of `docs/references/bibliography.md`, whose entries give full
details and consultation dates.

#let bib = yaml("../bibliography.yml")

#reference-list(bib)
