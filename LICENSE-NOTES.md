# Licence analysis, no decision yet

- Status: to settle before the repository is presented as reusable
- Last reviewed: 2026-08-21

There is deliberately no `LICENSE` file. Picking one out of habit is a technical
decision dressed up as a formality.

**Important**: a public repository with no licence is not "open". With no licence,
default copyright applies and nobody may reuse the content. That is acceptable
during a research phase, and it is not acceptable indefinitely for a repository
meant to be read and possibly reused.

## 1. What the repository contains

The content is not homogeneous, so a single licence is not obviously the right
answer.

| Nature | Present today | Planned | Suitable licence family |
| --- | --- | --- | --- |
| Documentation, analysis, figures | yes | yes | Creative Commons |
| Software (scripts, reference model, analysis) | no | yes | permissive or copyleft software licence |
| Antenna and board design files | no | likely | dedicated hardware licence, see below |
| Simulation files | no | yes | careful with vendor supplied device models |
| Measurement data produced here | no | yes | data licence or public domain |
| Third party data | no | no, by policy | not applicable, we do not redistribute it |

## 2. Candidates

| Licence | Type | Allows | Requires | Relevance here |
| --- | --- | --- | --- | --- |
| MIT | permissive | anything, including closed commercial use | attribution | simple, but silent on patents |
| BSD 2 or 3 clause | permissive | same | attribution | equivalent to MIT in practice |
| Apache 2.0 | permissive | same | attribution, notice of changes, patent grant | interesting for hardware, where patents genuinely exist |
| MPL 2.0 | file level copyleft | broad use | modified files stay open | rarely used for hardware |
| GPL 3.0 | strong copyleft | broad use | derivative works stay GPL | discourages industrial reuse, rarely a fit for RTL |
| CERN OHL, P, W and S variants | hardware | designed for hardware designs | from permissive to strong copyleft | written for exactly this case |
| Solderpad | hardware | Apache 2.0 adapted to hardware | attribution, patents | used by several RISC-V projects |
| CC BY 4.0 | documentation | reuse with attribution | attribution | fits text and figures |
| CC0 | public domain | anything | nothing | fits measurement data |

## 3. What will actually decide

The licences of the external blocks we reuse. Three cases:

| Case | Consequence |
| --- | --- |
| Only original code | free choice |
| Permissively licensed blocks reused | free choice, with attribution and header retention |
| Strong copyleft block reused | the project licence is largely determined |

So the licence decision follows the architecture decision. Every external block
under consideration has its licence recorded in its note in `research/notes/`, and
that list is what will decide.

## 4. The board design question

A printed circuit board design is not software. Licences written for open hardware
exist precisely for this kind of object, in several variants ranging from permissive
to strongly reciprocal for derived work.

Open question: apply a software licence for simplicity, or a hardware licence for
accuracy? To be settled with an argument.

## 5. Device models and simulation files

Specific to the radio frequency projects, and easy to forget: device models supplied
by component vendors, and electromagnetic simulation project files that embed vendor
libraries, usually come with their own terms of use, and redistributing them is
generally not allowed.

Repository rule:

- no vendor supplied device model is redistributed,
- we reference the part and where to obtain its model,
- simulation files in the repository must either open without those models, or state
  clearly what is missing.

The same caution applies to measurement data provided by third parties, including
public datasets: their terms of use are read and recorded in the corresponding
source note.

## 6. Starting proposal, not validated

To be confirmed by a decision record:

- documentation and figures: Creative Commons attribution,
- scripts and reference model: Apache 2.0, for the patent grant,
- board design files: to decide, a dedicated hardware licence is likely,
- measurement data produced here: public domain or simple attribution.

One `LICENSE` file per content type is possible and common. It requires a clear
statement at the top of the README to avoid ambiguity.

## 7. Checklist before declaring the repository reusable

- [ ] No third party data redistributed without permission.
- [ ] No vendor documentation copied into the repository.
- [ ] No keys, tokens or personal addresses.
- [ ] No vendor supplied device model redistributed.
- [ ] Terms of use of every third party dataset checked and recorded.
- [ ] Chosen licence file present.
- [ ] README states clearly which licence applies to what.
