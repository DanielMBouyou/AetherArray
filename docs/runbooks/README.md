# School runbooks

- Status: in force since 2026-09-26
- Last reviewed: 2026-09-26

Some of this project's work can only happen at school, where the network analyser, the
full HFSS licence and ADS are. This directory makes that distinction permanent, and
gives every school task a procedure that can be opened at the machine days later and
followed without reconstructing the project. The register of every current task is
`register.md`.

## 1. Where work runs

| Class | Meaning |
| --- | --- |
| `LOCAL` | runs on our own machines: Python, `rfkit`, scikit-rf, KiCad, HFSS Student within its limits, and the boards we own |
| `SCHOOL-SOFTWARE` | needs a licence only the school has: full HFSS, or ADS |
| `SCHOOL-BENCH` | needs the school laboratory's instruments, the network analyser first of all |
| `EITHER` | runs locally, and moves to school only when a stated local limit is exceeded or when it is simply convenient |

Four rules decide the class.

1. **Work runs where it is scientifically sufficient, not where the most powerful tool
   is.** A task moves to school only for a reason that can be written down: an
   instrument, or a limit that a local tool cannot meet.
2. **HFSS Student is the default HFSS path.** For release 2025 R1 the manufacturer
   documents, bibliography V7: 64,000 elements for a 3D volume mesh, 8,000 for a 3D
   surface mesh and 2,000 triangles in 2D; DXF and STEP import only; local solves only,
   on at most four cores; no SBR+, no mesh assemblies, no circuit model generation from
   S parameters and no geometry export. **A model escalates to the full licence only if
   its converged mesh needs more than the volume limit, or it needs a listed feature.**
   Converged means what the experiment using it says, for EXP-011 the last two adaptive
   passes giving the same verdict. Record the installed Student release; if it is not
   2025 R1, read its limits again before relying on these.
3. **ADS is optional.** It is a valuable independent circuit model, and the simulator
   comparison of decision 0007 is written for it, but nothing in the repository needs it
   to be reproduced. The portable circuit route is scikit-rf's transmission line media.
   `rfkit` has no source label for a scikit-rf circuit model yet; comparing one against
   HFSS under decision 0007 needs that label, and a decision on which limits apply.
4. **Python, scikit-rf and `rfkit` are the analysis layer everywhere, and never depend
   on a school licence.** A school task produces files. The analysis happens at home.

## 2. Runbooks

Every `SCHOOL-SOFTWARE` and `SCHOOL-BENCH` task has one runbook: an editable Markdown
source here, `SCH-NNN-short-name.md`, and a PDF generated from it, `pdf/SCH-NNN-short-name.pdf`.
One runbook per executable task, never one manual for everything. **No PDF exists
without its source, and no PDF is edited by hand**: the PDF carries the SHA-256 of the
source it was built from, in its footer and in its metadata, and the check below refuses
a PDF whose source has changed since.

A runbook starts from `template.md` and keeps its headings in order. The first page
answers what the task is, why it is done, what question it answers, what must already be
true, what is needed, how long it takes, and which files to bring and to leave with.
Then comes a `STOP / DO NOT CONTINUE` box, a procedure in ten numbered steps, from
opening the application to the final checklist before leaving, an `EVIDENCE TO BRING
BACK` list, and a `BACK AT HOME` section naming the exact command or repository task that
consumes the data.

**A value not yet decided is never invented.** It is written as a placeholder naming
the decision that will fix it, `{{TBD: what; source: which decision}}`, and the PDF shows
it highlighted. A runbook containing a placeholder cannot be ready.

## 3. Readiness

| Status | Meaning |
| --- | --- |
| `NOT READY` | no runbook yet, because something the procedure needs is undefined; the register names what is missing |
| `BLOCKED` | the runbook is written and its PDF built, but a prerequisite gate is still open |
| `READY` | the PDF is built from the current source and validated, it holds no placeholder, and no prerequisite gate is open |
| `DONE` | executed, and its results recorded under `results/` |

**A school task cannot be `READY` without its PDF.** The check below fails if the
register says otherwise, and CI runs it. A procedure is never written for a solver model
or a test that is not yet defined: that task stays `NOT READY`.

## 4. Building and checking

```
python -m pip install -r requirements.txt
python tools/runbooks/build.py
python tools/runbooks/build.py --check
python tools/runbooks/build.py --check --png some/folder
```

The first rebuilds every PDF from its source. The second is what CI runs. It fails when
a runbook drops or reorders a required heading, when a ready runbook still holds a
placeholder, when a PDF is missing, built from an older source, or different in content
from a fresh build, when any text or image falls outside the printable area of a page,
when a page lacks its page number, and when the register and the runbooks disagree. The
third also writes every page as an image, for looking at before a visit.

## 5. Adding a runbook

1. Give the task an identifier in `register.md`, with its class, status `NOT READY`, its
   prerequisite gates and what is missing.
2. When nothing it needs is undefined, copy `template.md` to `SCH-NNN-short-name.md` and
   write it.
3. Build it, look at the pages, and set its status to `BLOCKED` or `READY` in both the
   runbook and the register.
