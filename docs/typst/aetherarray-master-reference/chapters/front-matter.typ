#import "../template.typ": *

= AetherArray: master technical reference <aetherarray-master-technical-reference>

- Status: draft, first issue, for review by the project owner
- Last reviewed: 2026-10-04
- Document version: 0.2: second pass making integrated sensing and communication (ISAC) a
  first class technical concept, section 10bis; first issue was version 0.1 at commit `de61a40`
- Repository baseline: `main@33086b9395f57f4056a3205e7e8174d50defd500`, committed 2026-10-04,
  "Add SIM-001 analysis tooling". This is one commit newer than `e772a25`, the baseline named
  in the request for this document, so the newer commit is the one described.
- Canonical stack-up: `reva-stackup-r1:6363d8ab0f2b`, decision 0009
- Test suite at this baseline: 160 tests collected and passing, `cd tools && python -m pytest
  rfkit/tests -q`, Python 3.12 with `requirements.txt`. This count is a snapshot of 2026-10-04,
  not a property of the project; rerun the command for the current figure.
- How this document was produced: written from the repository contents at the baseline above,
  with external literature and the IEEE contest rules researched on 2026-10-04; the ISAC pass of
  version 0.2 found no newer repository evidence, and the official IEEE and publisher sites were
  still unreachable from this environment, so no citation could be upgraded to a primary read. It records no
  new decision and changes no existing one. Where it proposes something, it says so.

#caveat[
*The one paragraph to read if you read nothing else.* AetherArray is a four element,
2.44 GHz, phase only phased array that has been *designed but not built*. Its purpose is
scientific rather than commercial: to measure, on real hardware, whether the history of how
an RF array drifts can be used to recalibrate it with fewer new physical measurements than
calibrating it from scratch. The architecture, the working frequency, the controller, the
printed circuit board stack-up and the acceptance rules for the first simulations are all
decided and recorded. No board has been fabricated, no full wave simulation has produced a
result, no drift has been measured and no learning model exists. The 2027 IEEE AP-S Student
Design Contest, whose theme is reconfigurable receiving antennas for integrated sensing and
communication, is the intended external test of the idea; that ambition is described here
but is not yet recorded in any decision of the repository.
]

#rule()

== How to use this document

=== Who it is for

#table(
  columns: (2.3fr, 2.8fr, 1.8fr, 1.1fr),
  table.header([Reader], [Start with], [Then read], [You can skip]),
  [RF or microwave professor], [Part 0, Part III, Part IV, Part XI], [Part V, Part VI, Part X], [Part I sections 1 to 4],
  [Antenna professor], [Part 0, sections 6, 7, 9, 10, 10bis, Part IX], [sections 22, 58, Part VI], [sections 17 to 20],
  [Signal processing or machine learning professor], [Part 0, sections 10bis, 11 and 12, Part VIII], [Part II, Part XV, section 57], [Part IV],
  [IEEE AP-S or MTT-S mentor, competition jury], [Part 0, section 10bis, Part IX, Part X, Part XXI], [Part VIII section 44, Part XVII], [Part I],
  [Student joining the project], [Part I in full, then Part 0 again], [Part III, Part V, Appendix L], [nothing],
  [Hardware or RF recruiter], [Part 0, Part X, Part XII], [Part III, Part V], [Part XV],
)

=== How claims are labelled

The repository has several vocabularies for evidence, each in the place it was needed. This
document uses all of them and never mixes them up. They are explained in section 34; a short
version is here so the labels make sense from the first page.

#table(
  columns: (1.9fr, 6.5fr),
  table.header([Label], [Meaning in this document]),
  [*\[observed\]*], [somebody stood in front of the instrument or hardware and read it; date given],
  [*\[documented\]*, written *\[inventory\]* where the repository uses that word], [listed in an inventory or an older record; present state unknown],
  [*\[listing\]*], [stated only by a distributor or aggregator, not by the manufacturer],
  [*\[vendor\]*], [stated by a manufacturer for a part or model family, not measured here],
  [*\[analytical\]*], [computed from a closed form model or a repository script; not a simulation of the real geometry and not a measurement],
  [*\[simulated\]*], [produced by a full wave or circuit solver on a modelled geometry. *No such result exists yet*],
  [*\[measured\]*], [produced by an instrument on project hardware. *No such result exists yet*],
  [*\[synthetic\]*], [generated from a formula to test software; never evidence about hardware],
  [*\[decided\]*], [fixed by an accepted decision record in `decisions/`],
  [*\[planned\]*], [specified in the repository but not done],
  [*\[proposed here\]*], [suggested by this document; not in the repository; needs a decision before it counts],
  [*\[assumed\]*], [a working hypothesis, stated so it can be invalidated],
  [*\[to verify\]*], [an open question, with the method that would settle it where known],
  [*\[snippet only\]*], [an external fact read only through search engine excerpts of the official page, because the page itself could not be opened from this environment],
)

Internal facts are cited by repository path or identifier, for example decision 0007,
`experiments/EXP-005-repeatability-floor.md`, or uncertainty I24 in `docs/uncertainties.md`.
External sources are cited by bracketed identifiers listed in the References at the end. The
identifiers that already exist in `docs/references/bibliography.md` (A6, V8, T1 and so on) are
reused unchanged.

=== Numbers that can go stale

Every table in this document that sits between `stackup:begin` and `stackup:end` markers is
*generated* from `hardware/rev-a/stackup/reva-stackup.json` by
`python -m rfkit.cli stackup --write-docs`, and the test suite fails if one of them no longer
matches the canonical file. Numbers quoted in prose are copied from those tables or from the
decision records, and are dated by the baseline above. If a prose number and a generated table
disagree, the generated table is right.

=== Figures

Figure 19, in section 10bis.7, is the signature figure: one aperture, two ISAC functions, one
calibration layer. Diagrams are written as Mermaid or as text inside code fences, so that they live in the
repository as source. GitHub renders Mermaid directly; a PDF conversion needs a Mermaid filter.
The three plotted figures in `docs/figures/` are produced by
`python tools/docs/master_reference_figures.py`. All three are *\[analytical\]* illustrations of
the ideal array factor: no coupling, no element pattern, no simulated or measured data.

#rule()

== Contents

- #link(<part-0-executive-overview>)[Part 0. Executive overview]
- #link(<part-i-course-and-theory-refresher>)[Part I. Course and theory refresher]: 1 Electromagnetic waves; 2 Transmission lines; 3 S-parameters; 4 The vector network analyser; 5 Microstrip; 6 Antennas; 7 Phased arrays; 8 Quantised phase shifting; 9 Null steering and interference rejection; 10 Mutual coupling; 10bis Integrated sensing and communication (ISAC); 11 Calibration; 12 Drift
- #link(<part-ii-the-engineering-problem>)[Part II. The engineering problem]: 13 Why this matters at scale
- #link(<part-iii-what-exactly-is-being-built>)[Part III. What exactly is being built]: 14 Why two boards; 15 Beamformer channels; 16 Enable and terminate; 17 The RF detector; 18 Temperature sensors; 19 The DE1-SoC; 20 Grounding and the digital to RF interface
- #link(<part-iv-pcb-stack-up-and-rf-physical-design>)[Part IV. PCB stack-up and RF physical design]: 21 Beamformer stack-up; 22 Antenna stack-up; 23 Why not a Rogers laminate; 24 Solder mask and roughness; 25 Coupons
- #link(<part-v-the-simulation-and-analysis-stack>)[Part V. The simulation and analysis stack]: 26 Analytical calculations; 27 HFSS; 28 ADS; 29 PyAEDT; 30 Touchstone; 31 scikit-rf and rfkit; 32 Python; 33 Git, CI and reproducibility
- #link(<part-vi-simulation-roadmap>)[Part VI. Simulation roadmap]
- #link(<part-vii-measurement-and-experimental-method>)[Part VII. Measurement and experimental method]: 34 Evidence hierarchy; 35 EXP-004; 36 EXP-005; 37 The future drift experiment
- #link(<part-viii-machine-learning>)[Part VIII. Machine learning]: 38 What it does not do; 39 What it does; 40 Candidate models; 41 Training data; 42 Baselines; 43 Active measurement selection; 44 Why it matters in the ISAC demonstrator
- #link(<part-ix-the-ieee-ap-s-2027-isac-demonstrator>)[Part IX. The IEEE AP-S 2027 ISAC demonstrator]: 45 Official challenge; 46 Why AetherArray fits; 47 Communication mode; 48 Sensing mode; 49 Why four elements may be enough; 50 The N = 4 feasibility gate; 51 Dual polarisation; 52 Demonstration sequence
- #link(<part-x-current-project-status>)[Part X. Current project status]: 53 Decision history; 54 What exists physically; 55 What exists in software; 56 What has not happened yet
- #link(<part-xi-validation-philosophy>)[Part XI. Validation philosophy]: 57 Acceptance budgets; 58 Coupling gate G4; 59 Stack-up sensitivity
- #link(<part-xii-software-and-tool-table>)[Part XII. Software and tool table]
- #link(<part-xiii-complete-data-flow>)[Part XIII. Complete data flow]: 60 Design; 61 Measurement; 62 Learning; 63 Demonstrator
- #link(<part-xiv-why-this-project-is-useful>)[Part XIV. Why this project is useful]: 64 to 68
- #link(<part-xv-literature-and-evidence>)[Part XV. Literature and evidence]
- #link(<part-xvi-ieee-strategy>)[Part XVI. IEEE strategy]: 69 MTT-S; 70 AP-S; 71 AP-S 2027 ambition; 72 What would be meaningful on a CV
- #link(<part-xvii-risk-register>)[Part XVII. Risk register]
- #link(<part-xviii-roadmap>)[Part XVIII. Roadmap]
- #link(<part-xix-glossary>)[Part XIX. Glossary]
- #link(<part-xx-what-the-project-is-and-is-not>)[Part XX. What the project is and is not]
- #link(<part-xxi-one-page-synthesis>)[Part XXI. One page synthesis]
- #link(<appendices>)[Appendices]: A parameters; B stack-up; C acceptance budget; D open hardware items; E simulations; F experiments; G decisions; H tools; I AP-S checklist; J unresolved questions; K notation; L where to find things
- #link(<references>)[References]
- #link(<review-from-five-reader-perspectives>)[Review from five reader perspectives]
