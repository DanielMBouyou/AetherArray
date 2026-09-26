# Repository conventions

This document sets out how the repository is organised and written. It is
deliberately short. If a rule gets in the way of real work, change it and record
why in `decisions/`.

## 1. Why this layout

The goal is that someone landing on the repository can answer one specific
question without reading everything else.

| Directory | Question it answers |
| --- | --- |
| `README.md` | What is this, and why is it interesting? |
| `docs/scope.md` | What is the problem, what is in scope, what is explicitly out? |
| `docs/uncertainties.md` | What is known, what is assumed, what still needs checking? |
| `research/` | What already exists, and what should we read? |
| `docs/architecture/` | Which architectures are possible, and how do we choose between them? |
| `docs/mathematics/` | How does the problem look when written down formally? |
| `benchmarks/` | How do we measure, and with which metrics? |
| `experiments/` | Which concrete experiments are planned, and in what order? |
| `docs/hardware/` | What hardware is needed, available, or missing? |
| `docs/runbooks/` | Which work needs school resources, and exactly how is each such task done? |
| `docs/verification/` | How do we know a result is correct? |
| `results/` | What did we actually measure? |
| `docs/references/` | Where are the sources and the vocabulary? |
| `decisions/` | What was decided, on what evidence, and when should we revisit it? |
| `hardware/` | The design files themselves: schematics, symbol libraries, generators |
| `tools/` | Checks and analysis code the repository runs on itself |

Two choices deserve a justification, because they depart from a flat list.

**`research/` sits at the top level, not inside `docs/`.** During this phase the
literature is not supporting documentation, it is the main work. Putting it on the
same level as `benchmarks/` and `experiments/` reflects its actual weight.

**`hardware/` sits at the top level, next to `docs/hardware/`, and the two are not
the same thing.** `docs/hardware/` is prose about what hardware is needed, available
or missing. `hardware/` holds machine readable design files that a tool opens.
Putting design files under `docs/` would make the documentation tree unreadable, and
putting the prose next to the design files would bury it. This directory was added on
2026-09-18, when decision 0003 authorised schematic capture; before that there were no
design files to hold.

**`tools/` holds code the repository runs on itself**, not code that is the subject
of study. `tools/check-docs.sh` checks these conventions, `tools/runbooks/` builds and checks
the school runbooks, and `tools/rfkit/` is the
shared radio frequency data layer described in `docs/architecture/rf-data-layer.md`.
Python dependencies are pinned in one file, `requirements.txt`, at the top level.
If a second package list ever appears, delete it: two lists that disagree are worse
than one that is out of date.

**`experiments/` (the plan) and `results/` (the measurements) are separate.** An
experiment plan is written once and rarely revised. Results accumulate, grow, and
are sometimes versioned differently (see `results/README.md`). Mixing the two
makes the git history unreadable.

**`docs/runbooks/` exists because some work can only happen at school**, where the
network analyser, the full HFSS licence and ADS are. Its `README.md` classifies every
action as `LOCAL`, `SCHOOL-SOFTWARE`, `SCHOOL-BENCH` or `EITHER`, and its `register.md`
lists them. Work runs where it is scientifically sufficient, not where the most
powerful tool is: HFSS Student is the default HFSS path within its documented limits,
ADS is optional, and Python with scikit-rf and `rfkit` never depends on a school
licence. **A school task cannot be marked ready without its runbook PDF**, built from
a Markdown source kept beside it by `tools/runbooks/build.py`, whose `--check` CI runs.
No PDF is kept without its source.

## 2. Document status

Every substantial document starts with a status block:

```
Status: draft | in progress | stable | superseded
Last reviewed: YYYY-MM-DD
```

A superseded document is not deleted. Keeping it records what we used to believe.

## 3. Confidence markers

Three markers are used throughout the repository, and they do not mean the same
thing:

- **[established]**: checked against a primary source (datasheet, measurement made
  here, official specification), and the source is cited.
- **[assumed]**: a reasonable working hypothesis, unverified, used to make
  progress. It must be possible to invalidate it.
- **[to verify]**: an open question, ideally with the method that would settle it.

Empty cells are not allowed in comparison tables. Write `to measure` or
`to verify` instead. A wrong number is worse than a missing one.

## 4. Naming

- Files and directories: lowercase, single hyphens, ASCII only.
- Decisions: `decisions/NNNN-short-title.md`, numbered continuously, never reused.
- Experiments: `EXP-NNN-short-title`.
- Results: `results/EXP-NNN/`, reusing the experiment identifier.
- Source notes: `research/notes/NNN-name.md`.

## 5. Mathematics, units and notation

**Mathematics is typeset, never drawn.** Every equation is written in LaTeX, which
GitHub renders with MathJax. Two forms are used, and only these two:

- a display equation goes in a fenced block tagged `math`, shown below,
- an inline expression goes between single dollar signs.

The fenced form is used rather than double dollar signs because Markdown processes
backslash escapes inside an ordinary paragraph, which quietly destroys commands such
as the thin space macros before the renderer ever sees them.

ASCII pseudo-formulas are not acceptable. Subscripts, superscripts, sums, fractions
and integrals are real notation:

```math
\eta = \frac{\Delta C}{T}
\qquad\text{not}\qquad
\texttt{eta = deltaC / T}
```

Code fences are for code, diagrams and file listings only. `tools/check-docs.sh`
flags the most common pseudo-formula habits.

- Every equation is followed by a sentence, or a small table, saying what each symbol
  means physically and in what unit. An equation without that counts as a
  documentation defect.
- SI units, explicit prefixes. Times in ns, us, ms.
- Logarithmic quantities always carry their reference: dBm, dBc, dB.
- Give a small numerical example whenever it makes the equation concrete.
- State whether a relation is exact or an approximation.

## 6. Writing style

- Short paragraphs. No superlatives. No promotional vocabulary.
- Write what was measured, not what we hope to measure.
- The em dash character is not used anywhere in this repository (it causes
  encoding and copy-paste problems between tools). Use commas, parentheses,
  colons or plain hyphens. `tools/check-docs.sh` enforces this.
- Numbers taken from vendor documentation are labelled as such. "30 ns claimed by
  the vendor" and "30 ns measured here" are not the same information.

## 7. Data

- No large binary files in git history until a storage policy is decided (see
  `results/README.md`).
- No data under a restrictive licence, no keys, no access tokens, no vendor
  documents covered by a confidentiality agreement.
- Every dataset present must sit next to a `SOURCE.md` giving its origin, licence
  and retrieval date.

## 8. Life cycle of a question

```
open question  ->  source note  ->  experiment  ->  result  ->  decision
   (docs/)         (research/)     (experiments/)  (results/)  (decisions/)
```

A decision that rests on no result must say so explicitly, and state what it is
based on instead (time constraint, budget, available hardware).

## 9. Relationship with the other projects

This repository stands alone: it can be read and used on its own. It belongs to a
set of five projects that share hardware and methods. Shareable pieces are listed
in `docs/shared-resources.md`. No code dependency on another repository is allowed
until a shared library has been formally decided.
