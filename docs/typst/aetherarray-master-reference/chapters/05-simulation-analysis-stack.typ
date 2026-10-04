#import "../template.typ": *

= Part V. The simulation and analysis stack <part-v-the-simulation-and-analysis-stack>

Why several tools? Because each one answers a different question, and because agreement between
independent routes is the only evidence a model can offer before hardware exists.

#table(
  columns: (1.4fr, 3.4fr, 3.0fr, 3.6fr),
  table.header([Tool], [Question it answers], [Strength], [Blind spot]),
  [analytical models], [roughly what should happen, and how sensitive is it?], [instant, transparent, good for scaling and seeds], [geometry details, discontinuities, coupling],
  [HFSS], [what do Maxwell's equations give for this exact geometry?], [geometry aware, includes fringing, coupling and radiation], [only as good as the model's materials, ports and mesh; slow],
  [ADS, or scikit-rf circuit models], [what does an independent distributed circuit model give?], [fast, independent model form], [idealised discontinuities; needs component models],
  [the analyser], [what does the real board do?], [includes everything real], [only as good as its calibration and reference planes; needs hardware],
  [`rfkit`], [do these agree, by rules fixed in advance?], [one tested place for comparison rules and provenance], [judges only what it is given],
)

== 26\. Analytical calculations

Analytical models are closed form equations: the microstrip formulas of section 5, the patch
formulas of section 6, the array factor and its error statistics of sections 7 to 9.

#table(
  columns: (3.4fr, 2.5fr),
  table.header([Good for], [Bad for]),
  [sanity checks: is a 0.37 mm line plausible for 50 ohm on 0.21 mm of FR-4?], [switches and their packages],
  [initialisation: the width and length seeds of SIM-001], [bends, meanders and their self coupling],
  [scaling laws: how the 315 degree error grows with permittivity error], [connectors and launches],
  [quick sensitivity estimates: the tolerance tables of section 59], [discontinuities and their reflections],
  [error budgets: decision 0007's thresholds], [fringing in non uniform geometry],
  [], [mutual coupling between patches],
  [], [detailed loss including roughness and plating],
)

#caveat[
analytical seed $eq.not$ final geometry
]

In this repository, every analytical length or width is printed under the label INITIALISATION
ONLY or SANITY CHECK ONLY, and the stack-up validator refuses to store any geometry in the
canonical file (`hardware/rev-a/stackup/README.md` section 1).

== 27\. HFSS

=== 27.1 What it is

Ansys HFSS is a full wave, three dimensional, frequency domain electromagnetic solver based on the
finite element method. The model's volume is divided into small tetrahedra, the fields inside each
are approximated by simple functions, and Maxwell's equations become a large linear system solved
at each frequency. The result is the field everywhere in the model and the S-parameters at its
ports. It is driven by four kinds of input:

#table(
  columns: (auto, 6.5fr),
  table.header([Input], [Meaning in SIM-001]),
  [geometry], [substrate, trace, air box, ground; built by script from the canonical stack-up],
  [materials], [substrate permittivity and loss tangent, copper conductivity, from `reva-stackup-r1`],
  [boundaries], [outer faces perfect electric conductor; ground of finite conductivity],
  [ports], [one wave port at each end: a two dimensional eigenmode solve gives the port's mode, its impedance $Z_(p i)$ and its propagation constant],
)

=== 27.2 Adaptive meshing and convergence

HFSS solves at one frequency, estimates where the solution error is largest, refines the mesh
there, and solves again. The change in S-parameters between successive passes, $Delta S$, is
the convergence measure. SIM-001 requires $Delta S lt.eq 0.02$ on two consecutive passes, at most
20 passes, at a solution frequency of 2.44 GHz, then an interpolating sweep from 1 to 3 GHz in
5 MHz steps. Decision 0007 adds a requirement for any solve used in a simulator comparison: the
convergence criterion must be recorded, and for the verdict to concern models rather than mesh it
must satisfy $Delta S lt.eq abs(S_21) thin T$, with $T$ the phase threshold in radians, about
$0.04 thin abs(S_21)$.

=== 27.3 Why a colourful field plot is not evidence

A field plot shows that the solver produced a solution. It does not show that the solution is
right. A full wave result counts as evidence in this project only with:

#table(
  columns: (2.1fr, 6.3fr),
  table.header([Requirement], [What it rules out]),
  [convergence recorded: passes, final $Delta S$, element count], [a solution still changing with the mesh],
  [port check], [a wave port too small that couples to the walls; SIM-001 reruns with ports enlarged by half],
  [boundary check], [a shield or radiation boundary too close],
  [material provenance], [values typed by hand or from the wrong board; every model reads the canonical file],
  [frequency coverage], [conclusions drawn from one frequency; verdicts are judged across band 57a],
  [reproducibility], [a result nobody can regenerate; the builder, its inputs and the exported files are versioned],
  [an independent check], [agreement with a model of different form: the closed form, the two line extraction and the port solution are three readings in SIM-001],
)

=== 27.4 HFSS Student and full HFSS

Work runs where it is scientifically sufficient, not where the biggest tool is
(`docs/runbooks/README.md` rule 2). HFSS Student, installed locally as release 2025 R2, is the
default. Its documented limits \[#link(<ref-V23>)[V23]\]: 64 000 elements in a three dimensional volume mesh, 8 000 in
a three dimensional surface mesh, 2 000 triangles in two dimensions; DXF and STEP import only;
local solves only, on at most four cores; no SBR+, mesh assemblies, circuit model generation from
S-parameters, geometry export, optiSLang, LSDSO, Workbench, beta features or Linux. No port limit is
stated, and whether Touchstone export with port impedance comments is supported is not documented
either way, which SIM-001 step 5 checks. A model moves to the full licence at school only if its
converged mesh needs more than the volume limit, or a listed feature; a straight 50 ohm line
should need far less, so exceeding the limit there would first be treated as a modelling fault.

=== 27.5 Uses in AetherArray

#table(
  columns: (4.1fr, 2.4fr),
  table.header([Use], [Status]),
  [50 ohm microstrip on the beamformer construction], [SIM-001, READY; execution blocked],
  [phase sections, meanders and the Wilkinson arms], [proposed, Part VI],
  [switch discontinuities, if a package model can be built], [proposed; no PE4259 model source identified],
  [the four way divider], [proposed],
  [single patch, then the four element antenna board: coupling $vb(S)_A$ and embedded element patterns], [EXP-011 Stage 1, criterion fixed; geometry not designed],
)

*No HFSS solve has produced a result.* The first execution of the SIM-001 builder against AEDT
Student, on 2026-10-03, failed inside the first PyAEDT call: the AEDT server process started but
never opened its scripting connection, and no geometry was created. A second probe with no builder
code failed the same way. The session notes point, without confirmation, to AEDT Student never
having completed an interactive first launch on that account; the remedy recorded is to open it
once by hand and rerun step 2 unchanged (`results/SIM-001/notes.md`).

== 28\. ADS

Keysight ADS (Advanced Design System) is a circuit and system simulator for RF and microwave
design. Instead of meshing a geometry, it connects models: ideal and physical transmission line
elements, such as a microstrip line model of a given width and length on a given substrate;
S-parameter blocks imported from Touchstone files, for example a component vendor's switch model;
lumped elements; and network analysis around them. It is fast and its model form is independent of
HFSS's: a line in ADS is a closed form distributed model, not a solved field.

That independence is what makes it useful. If ADS and HFSS agree on the state dependent phase of a
switched line channel, the agreement is evidence about the design; if they disagree, the
disagreement locates a modelling error, often a discontinuity or a coupling path one model omits.
The intended chain is

```text
   analytical seed  -->  ADS or scikit-rf circuit model  -->  HFSS full wave  -->  VNA on the board
        (rfkit.stackup)       (independent model form)         (geometry aware)     (reality)
```

with each step compared to the previous by `rfkit`. Decision 0007 fixed the acceptance limits for
the HFSS against ADS comparison before any data: 2.29 degrees on the state dependent part of the
$S_21$ phase difference and 0.40 dB on the state dependent part of its magnitude, judged at every
grid point of band 57a and at $f_0$, with the convergence condition of section 27.2 (section 57).

ADS is at school only and optional: nothing in the repository needs it to be reproduced. The
portable circuit route is scikit-rf's transmission line media. Two gaps are recorded: `rfkit` has
no source label yet for a scikit-rf circuit model, which a decision 0007 comparison would need,
and no source has been identified for a PE4259 model usable in ADS (SCH-009). *No ADS result
exists.*

== 29\. PyAEDT

PyAEDT, packaged as `ansys-aedt-core`, is a Python interface to Ansys Electronics Desktop, which
hosts HFSS. AetherArray uses it so that solver models are built by script rather than by hand.

#table(
  columns: (2.2fr, 8.6fr),
  table.header([Benefit], [How SIM-001 realises it]),
  [reproducibility], [the builder `tools/sim/sim001_hfss.py` is versioned; rerunning it rebuilds the same six designs],
  [parameterisation], [widths of 0.9, 1.0 and 1.1 times the seed, two lengths, port size as variables],
  [no manual transcription], [substrate thickness, permittivity, loss tangent and copper come from `rfkit.stackup.sim001_parameters`, which reads the canonical file],
  [sweep automation], [the solve, the sweep and the exports are scripted],
  [export provenance], [each design writes a renormalised `.s2p`, a `-portdata.s2p` referred to the port impedance, and a JSON sidecar with the stack-up fingerprint and convergence fields, checked by `rfkit.stackup.check_sim_export`],
  [versioning], [the builder, the analysis script and the canonical file are all in git],
)

The rule that generated geometry must consume the canonical configuration, never copied constants,
is enforced by construction: the builder has no numeric material value of its own, and
`python sim/sim001_hfss.py --dry-run` prints the complete geometry from the canonical file
without AEDT, a step the CI runs. The builder also refuses to add designs to an existing project,
stops the AEDT servers it started if it fails, and offers `--student`, `--graphical`,
`--port-scale` and `--seed-only` for the protocol's steps. The analysis script
`tools/sim/sim001_analyse.py` applies the committed SIM-001 criterion; it has been tested on an
emulated run only. `ansys-aedt-core` 1.1.0 is recorded in the SIM-001 protocol but is not in
`requirements.txt`, because no CI job runs AEDT.

== 30\. Touchstone

A Touchstone file, extension `.sNp` for an $N$ port, is a plain text table of network parameters
against frequency; `.s2p` is a two port, `.s4p` a four port such as the antenna board's coupling
matrix. A minimal two port file looks like this:

```text
! AetherArray example, synthetic: not a measurement
# GHz S RI R 50
! freq    re(S11)  im(S11)  re(S21)  im(S21)  re(S12)  im(S12)  re(S22)  im(S22)
2.400     0.010    -0.020   0.700    -0.650   0.700    -0.650   0.012    -0.018
2.440     0.011    -0.019   0.640    -0.710   0.640    -0.710   0.013    -0.017
```

The option line, starting with `#`, gives the frequency unit, the parameter type, the number
format (RI for real and imaginary, MA for magnitude and angle, DB for decibels and angle) and the
reference impedance. Lines starting with `!` are comments; HFSS uses them to carry the port
impedance and propagation constant, which SIM-001 reads. For two port files the column order is
S11, S21, S12, S22, an exception to the row order used for larger files.

#table(
  columns: (2.2fr, 6.1fr),
  table.header([Limitation], [Consequence]),
  [metadata is free text in comments], [calibration state, reference planes, stack-up and instrument settings are not standardised; `rfkit` carries them in a provenance record beside the file],
  [one reference impedance per file in version 1], [port renormalisation must be explicit],
  [no uncertainty], [the analyser's expanded uncertainty must travel separately],
)

Touchstone is the bridge of the project: whatever produced the S-parameters, the analysis reads
the same kind of file.

#aa-figure(num: "12", caption: [one data path for every source of S-parameters.])[
#image("../figures/mermaid/figure-12.svg", width: 100%)
]

== 31\. scikit-rf and rfkit

*scikit-rf* is an open source Python library for RF and microwave engineering. Its `Network`
object holds S-parameters against frequency and reads and writes Touchstone; it also provides
transmission line media such as the `MLine` microstrip model used for the stack-up seeds,
calibration algorithms, de-embedding, time domain transforms and vector fitting. It is pinned at
version 1.12.0 in `requirements.txt`.

*rfkit* is the project's layer on top of it, in `tools/rfkit/`. It encodes, once and with tests,
the rules that would otherwise have to be remembered in every analysis notebook.

#table(
  columns: (1.5fr, 10.1fr),
  table.header([Module], [What it does, as implemented on 2026-10-04]),
  [`provenance`, `io`], [every trace carries its source, path, checksum, ports, reference impedance, sweep, calibration state and stack-up fingerprint; synthetic traces are labelled `synthetic`],
  [`grid`], [finds the band shared by all traces and the coarsest common grid; refuses to extrapolate, raising an error instead],
  [`metrics`], [values at a frequency and over a band; magnitude in dB; phase unwrapping; phase differences on the circle, so 359 and 1 degrees differ by 2; phase spread about the circular mean; amplitude imbalance],
  [`compare`], [pairwise comparison, whose $S_21$ verdicts read "not applicable", and `compare_states`, which keeps only the state dependent part and judges it against decision 0007 over band 57a],
  [`budget`, `thresholds`], [the error budget and the derivation of every threshold; values rounded down, tests fail if a recorded value is not its derivation],
  [`coupling`], [gate G4: the coupled forward model, the diagonal model, the rules of decision 0008, the guard matrices, the synthetic chart],
  [`state`], [per channel $S_21$ to the diagonal array state, reference channel explicit, raw complex values kept; the full matrix form supported by the data structure],
  [`dataset`], [repeated measurements with session, time and temperature, and the inference record],
  [`calibration`], [interfaces that refuse to run until calibration standards exist; `apply_calibration` raises an error by design],
  [`instrument`], [the adapter boundary for automation, deliberately without drivers],
  [`stackup`], [loading and validating the canonical stack-up; seeds, sensitivity, loss and patch checks; SIM-001 inputs and export checks; the generated documentation tables],
  [`lineparams`], [the two line extraction of section 25],
)

Command line entry points: `compare`, `compare-states`, `state`, `budget`, `g4`, `g4-chart`,
`example` and `stackup` (`tools/rfkit/README.md`).

Why a project specific layer is worth its cost: the comparisons this project makes, HFSS against
ADS against the analyser, are easy to make wrongly in ways that produce plausible numbers.
Comparing over a band only one trace covers, calling 359 against 1 degree a 358 degree error,
judging a constant offset that calibration removes as a failure, or printing PASS against a
threshold nobody derived: each is prevented by one tested function rather than by vigilance.
*Status: 160 tests pass at the baseline, all on synthetic or analytically constructed data. No
simulated or measured file has yet been processed.*

== 32\. Python

Python is the working language of everything that is not gateware or schematic: experiment
orchestration, analysis, plotting, simulation scripting, optimisation, the probabilistic inference
to come, tests and the runbook builder.

#table(
  columns: (2.5fr, 2.0fr, 2.7fr),
  table.header([Package], [Role], [Status]),
  [NumPy 2.4.6, SciPy 1.17.1], [numerical arrays, root finding, statistics], [pinned in `requirements.txt`],
  [scikit-rf 1.12.0], [the RF data layer], [pinned],
  [pytest 9.1.1], [the test suite], [pinned],
  [matplotlib 3.10.9], [figures, and equations in the runbook PDFs], [pinned],
  [mistune, reportlab, pillow, pymupdf], [the school runbook PDFs], [pinned],
  [ansys-aedt-core 1.1.0], [the SIM-001 builder], [recorded in SIM-001, not pinned, not run in CI],
  [scikit-learn, PyTorch, a Gaussian process or Kalman filter library], [the learning track], [*not chosen and not dependencies*; the model class is to be chosen on data (section 40)],
)

The pins date from 2026-09-25 with Python 3.12, and the CI uses Python 3.12. The repository rule is
that there is one package list; a second would be deleted.

== 33\. Git, CI and reproducibility

RF research benefits from software engineering discipline for a plain reason: the evidence chain
from a material value to a verdict passes through many files and several tools, and any step done
by hand is a step where a number can be retyped wrongly, a threshold moved after the data, or a
synthetic trace mistaken for a measurement.

#table(
  columns: (2.2fr, 8.3fr),
  table.header([Practice], [In this repository]),
  [version control], [every document, decision, script and design file is in git; the commit is the timestamp],
  [decision records], [nine accepted decisions, each with options, evidence, known limitations and conditions for reopening; superseded text is kept, not deleted],
  [canonical configuration], [one stack-up file read by every tool; numbers never retyped],
  [generated documentation], [tables between markers regenerated from the canonical file; tests fail on drift],
  [pre-registration], [decision rules committed before data: EXP-005 section 7, decision 0007, decision 0008, the SIM-001 criterion],
  [tests], [`rfkit` test suite, 160 tests at the baseline],
  [continuous integration], [three workflows: documentation conventions (`tools/check-docs.sh`); RF tests, worked example, budget derivation, stack-up table check and the SIM-001 dry run; runbook build and check],
  [runbooks], [every school task gets a step by step PDF built from Markdown, with the source's checksum in the PDF; a task cannot be READY without it],
)

The test count is quoted with its date because it changes; the command in the front matter
recomputes it.
