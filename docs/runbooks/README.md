# School runbooks

- Status: in force since 2026-09-26
- Last reviewed: 2026-10-03

Some of this project's work can only happen at school, because that's where the
network analyser, the full HFSS licence and ADS are. This folder makes that split
permanent. It also gives every school task a procedure you can open at the machine,
days later, and follow without having to piece the project back together. The list of
every current task is `register.md`.

## 1. Where work runs

| Class | Meaning |
| --- | --- |
| `LOCAL` | runs on our own machines: Python, `rfkit`, scikit-rf, KiCad, HFSS Student within its limits, and the boards we own |
| `SCHOOL-SOFTWARE` | needs a licence only the school has: full HFSS, or ADS |
| `SCHOOL-BENCH` | needs the school laboratory's instruments, the network analyser first of all |
| `EITHER` | runs locally, and moves to school only when a stated local limit is exceeded or when it is simply convenient |

Four rules decide which class a task gets.

1. **Work runs where it's scientifically good enough, not where the biggest tool is.**
   A task only moves to school for a reason you can write down: an instrument, or a
   limit a home tool can't meet.
2. **HFSS Student is the default way to use HFSS.** For release 2025 R1, the
   manufacturer documents these limits, bibliography V7: 64,000 elements for a 3D
   volume mesh, 8,000 for a 3D surface mesh, and 2,000 triangles in 2D; DXF and STEP
   import only; local solves only, on at most four cores; no SBR+, no mesh assemblies,
   no circuit model generation from S parameters, and no geometry export. **A model
   only goes to the full licence if its converged mesh needs more than the volume
   limit, or if it needs one of the listed features.** "Converged" means whatever the
   experiment using the model says it means. For EXP-011, that's the last two adaptive
   passes giving the same verdict. Write down which Student release is installed. If
   it isn't 2025 R1, read its limits again before trusting these. **Recorded on
   2026-10-03:** the installed release is 2025 R2, and its limits, read that day, are the
   same, with optiSLang and LSDSO both unsupported, bibliography V23.
3. **ADS is optional.** It's a useful independent circuit model, and the simulator
   comparison in decision 0007 is written for it, but nothing in the repository needs it
   to be reproduced. The portable circuit route is scikit-rf's transmission line
   models. `rfkit` doesn't have a source label for a scikit-rf circuit model yet.
   Comparing one against HFSS under decision 0007 needs that label, plus a decision on
   which limits apply.
4. **Python, scikit-rf and `rfkit` are the analysis layer everywhere, and never depend
   on a school licence.** A school task produces files. The analysis happens at home.

## 2. Runbooks

Every `SCHOOL-SOFTWARE` and `SCHOOL-BENCH` task gets one runbook: a Markdown source
here, `SCH-NNN-short-name.md`, and a PDF built from it, `pdf/SCH-NNN-short-name.pdf`.
One runbook per task you can actually do, never one giant manual. **There's no PDF
without its source, and nobody edits a PDF by hand.** Each PDF carries the SHA-256 of
the source it was built from, in its footer and in its metadata. The check below
refuses any PDF whose source has changed since.

A runbook starts from `template.md` and keeps its headings in order. The first page
says what the task is, why it's done, what question it answers, what has to be true
already, what you need, how long it takes, and which files to bring and to leave with.
After that comes a `STOP / DO NOT CONTINUE` box, then a procedure in ten numbered
steps, from opening the software to the checklist before you leave, then an `EVIDENCE
TO BRING BACK` list, and finally a `BACK AT HOME` section with the exact command or
repository task that uses the data.

**A value that isn't decided yet is never made up.** It's written as a placeholder that
names the decision that will fix it, `{{TBD: what; source: which decision}}`, and the
PDF shows it highlighted. A runbook with a placeholder in it can't be ready.

## 3. Readiness

| Status | Meaning |
| --- | --- |
| `NOT READY` | no runbook yet, because something the procedure needs is undefined; the register names what is missing |
| `BLOCKED` | the runbook is written and its PDF built, but a prerequisite gate is still open |
| `READY` | the PDF is built from the current source and validated, it holds no placeholder, and no prerequisite gate is open |
| `DONE` | executed, and its results recorded under `results/` |

**A school task can't be `READY` without its PDF.** The check below fails if the
register says otherwise, and CI runs it. Nobody writes a procedure for a solver model
or a test that isn't defined yet. That task stays `NOT READY`.

## 4. Building and checking

```
python -m pip install -r requirements.txt
python tools/runbooks/build.py
python tools/runbooks/build.py --check
python tools/runbooks/build.py --check --png some/folder
```

The first command rebuilds every PDF from its source. The second is what CI runs. It
fails if a runbook drops a required heading or puts them out of order, if a ready
runbook still has a placeholder, if a PDF is missing, built from an older source or
different in content from a fresh build, if any text or image sits outside the
printable area of a page, if a page has no page number, or if the register and the
runbooks disagree. The third also saves every page as an image, so you can look at
them before a visit.

## 5. Adding a runbook

1. Give the task an identifier in `register.md`, with its class, status `NOT READY`,
   its prerequisite gates, and what's missing.
2. When nothing it needs is undefined any more, copy `template.md` to
   `SCH-NNN-short-name.md` and write it.
3. Build it, look at the pages, and set its status to `BLOCKED` or `READY`, both in the
   runbook and in the register.
