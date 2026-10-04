# AetherArray

A small antenna array you steer electronically. And mostly, a study of what happens
when you try to make it do what the theory says it should.

- Status: first board designed and its experiments specified; no hardware built yet
- Last reviewed: 2026-09-28

> **The short version.** AetherArray is four antennas working at 2.44 GHz. You steer
> the beam by switching short lengths of line in and out of each antenna's feed, so
> nothing moves. Steering isn't the hard part, though. Calibration is. Every real
> array points a little wrong, and this project asks two things: how few measurements
> does it take to fix that, and can an array that's been calibrated before use its own
> history to do it faster next time? Nothing is built yet. The first board is designed
> down to its schematic. The experiments that will judge it are written, with their
> pass or fail rules fixed before any data exists. And the first hardware is waiting
> on one short visit to a network analyser. This repository is the public lab notebook
> for all of it.

---

## The idea in one picture

An antenna array is a group of small antennas, each fed on its own. Change the phase
of the signal going to each one and you steer the beam. No motors.

```
   element 0      element 1      element 2      element 3
      |               |              |              |
    phase φ0       phase φ1       phase φ2       phase φ3
      |               |              |              |
      +---------------+--------------+--------------+
                          |
                    same source signal
```

If all the elements radiate in phase, the beam goes straight ahead. Shift the phases
step by step along the row and it tilts. That's how modern radars and phone base
station antennas work.

On paper it's simple. A real array never points exactly where you ask, though, and
that gap is what this whole project is about.

---

## The ideal model, and why it is wrong

Here's how theory describes a line of antennas:

```math
AF(\theta) = \sum_{n=0}^{N-1} a_n \, e^{\,j\left(n k d \sin\theta \,+\, \phi_n\right)}
```

Piece by piece:

- $N$ is how many elements there are.
- $a_n$ is the amplitude sent to element $n$. No unit.
- $\phi_n$ is the phase we give it, in radians. It's our control knob.
- $d$ is the gap between neighbouring elements, in metres.
- $k = 2\pi/\lambda$ is the wavenumber, in radians per metre. It turns a distance into
  a phase shift: one wavelength of travel turns the phase by $2\pi$.
- $\theta$ is the angle you look from, measured from the line straight out of the
  array.
- $n k d \sin\theta$ is the phase shift you get for free, because the wave from
  element $n$ travels a slightly different distance to reach you.
- $AF(\theta)$ is the total field in direction $\theta$: every element's
  contribution, added up.

What it means: contributions add when they arrive in phase, and cancel when they
arrive opposite. To point the beam at $\theta_0$, you pick:

```math
\phi_n = -\,n k d \sin\theta_0
```

So you cancel out, in advance, the phase shift the geometry would add.

Rough numbers for four elements, half a wavelength apart:

| Quantity | Approximate value | Meaning |
| --- | --- | --- |
| Beam width | about 25 degrees | with only four elements the beam is not narrow |
| Side lobe level | about -13 dB | there is still energy outside the main beam |
| Array gain | about 6 dB over a single element | doubling the element count adds 3 dB |

All of that assumes everything is perfect.

---

## Why nothing is perfect

This one calculation is enough to justify the whole project.

In ordinary coaxial cable, a signal travels at about 66 percent of the speed of
light. With that velocity factor, $v_f = 0.66$, the wavelength inside the cable at
$f = 2.44$ GHz is:

```math
\lambda_{\text{cable}} = \frac{v_f\, c}{f} = \frac{0.66 \times 3\cdot 10^{8}}{2.44\cdot 10^{9}}  \approx  81\ \text{mm}
```

So every millimetre of cable shifts the phase by:

```math
\frac{360^{\circ}}{\lambda_{\text{cable}}} = \frac{360^{\circ}}{81\ \text{mm}}  \approx  4.4^{\circ}\ \text{per millimetre}
```

**Make one cable a centimetre longer than another and you've added about 44 degrees
of phase error.** Cut your cables by hand and the pattern falls apart.

And cable length is just one source of error:

| Error source | Origin | Order of magnitude | Correctable? |
| --- | --- | --- | --- |
| Cable length | fabrication | tens of degrees | yes, by calibration |
| Component tolerance | manufacturing spread | a few degrees to a few dB | yes |
| Coupling between neighbouring elements | the antennas see each other | depends on spacing, often significant | partly |
| Thermal drift | temperature change | a few degrees | yes, if you recalibrate |
| Connectors | tightening, wear | a few degrees | yes, but variable |
| Environment | reflections off nearby objects | highly variable | no, you have to control the measurement site |

Put them together and it adds up fast. A handy rule: if the phase errors are random,
with standard deviation $\sigma$ in radians, the average gain drops like this:

```math
\frac{G_{\text{real}}}{G_{\text{ideal}}}  \approx  e^{-\sigma^{2}}
```

With $\sigma = 30^{\circ} \approx 0.52$ rad, you lose about 1.2 dB. Worse, the side
lobes rise, and that usually hurts more than the lost gain. With only four elements
the real figure is a bit smaller, because part of the sum stays incoherent, and
`tools/rfkit/budget.py` uses the exact version.

In plain terms: an uncalibrated array works. It just works badly, and you can't
predict how badly.

---

## The realistic model

Instead of chasing each defect separately, you can put all of them into one complex
matrix:

```math
\mathbf{y} = \mathbf{H}\,\mathbf{x}
```

- $\mathbf{x} \in \mathbb{C}^{N}$ is what we command: one complex number per channel,
  meaning the amplitude and phase we ask for.
- $\mathbf{y} \in \mathbb{C}^{N}$ is what actually comes out of each element.
- $\mathbf{H} \in \mathbb{C}^{N \times N}$ holds everything else: each channel's gain
  and phase error on the diagonal, and the coupling between elements off it.

If $\mathbf{H}$ were the identity, the array would be perfect. It isn't.

Calibrating means measuring $\mathbf{H}$, then sending a corrected command:

```math
\mathbf{x}_{\text{corr}} = \mathbf{H}^{-1}\,\mathbf{x}_{\text{wanted}}
```

This is where it stops being tinkering and becomes applied maths. Measuring
$\mathbf{H}$ takes measurements, each one costs time, and the inversion can blow up if
the matrix is badly conditioned.

For the first board we model $\mathbf{H}$ as diagonal: one complex number per channel.
That leaves only $2N - 2 = 6$ unknowns, once you set aside the common gain and phase,
which nothing can see anyway. Is that good enough once the antennas start coupling to
each other? That's gate G4. The test that decides it was written before any coupling
was simulated or measured, in decision 0008.

---

## The real questions

1. **How many measurements does calibration take?** An array with $N$ channels has at
   least $N$ complex unknowns, and a lot more if you want the coupling too. Every
   measurement takes time and comes with noise.
2. **Can you calibrate without measuring phase?** Lots of simple setups only measure
   power. Getting phases back from power alone is a classic maths problem, and it
   isn't easy.
3. **Is a classical method enough?** Least squares, regularisation, direct inversion.
   They're old, proven and cheap, and you need to know how far they go before trying
   anything fancier.
4. **Can a learned method cut the number of measurements?** Not on a first
   calibration, as it turns out. With four elements, the classical methods already sit
   at the information limit for power only measurement, so there's nothing left to
   save. What survives is a narrower question, and a more interesting one: **once the
   array has been calibrated before, can a prior learned from its own drift history
   recalibrate it with fewer measurements than starting from scratch?**
5. **How long does a calibration stay valid?** People rarely look at this. It's easy
   to measure, directly useful, and it's now the question the learning track depends
   on.

The order isn't an accident. The project doesn't start with machine learning. It
starts with what already works, then looks for where that stops being enough. Question
4 came out of exactly that: the obvious claim about learning didn't survive a simple
counting argument, and the one that replaced it is sharper. The reasoning is in
`docs/architecture/ml-calibration.md`, and the choice is recorded in
`decisions/0002-learning-as-a-drift-prior.md`. Learning only ever enters as a prior
inside a physical inverse problem. It never becomes a black box that predicts a
command: `docs/mathematics/inverse-calibration.md`.

---

## The first board, in plain words

The first board, Rev A, comes from decisions 0003, 0004 and 0005. It's really two
boards, joined by four short cables.

```
 antenna board                         beamforming board
 --------------                        --------------------------------------------
 patch 0 --SMA==jumper==SMA-- enable --- 3 phase bits --+
 patch 1 --SMA==jumper==SMA-- enable --- 3 phase bits --+-- 4-way   -- path  -- analyser
 patch 2 --SMA==jumper==SMA-- enable --- 3 phase bits --+   divider    select    or on board
 patch 3 --SMA==jumper==SMA-- enable --- 3 phase bits --+                        detector
                                              |
                                  16 control lines, ribbon cable
                                              |
                                   DE1-SoC board, FPGA and processor
```

**Why two boards?** Each antenna gets its own connector. That means we can measure
every element on its own, measure the coupling between any two, and use the one
calibration method that needs no outside probe at all: it transmits on one element
and listens on another. Put everything on one board and all three of those doors
close for good.

**How the beam gets steered.** Each channel has three switched line phase bits: 45, 90
and 180 degrees. In each bit, a pair of small RF switches, PE4259, picks either a short
path or a longer one. Three bits give eight phase states, 45 degrees apart. That leaves
a rounding error of about 13 degrees rms per channel, and no calibration can remove it.
It's the yardstick every other error in the project gets measured against. Two bits
would've been cheaper, but they'd have damaged the very baseline the measurement counts
are compared with. There's no amplitude control. Phase only.

**How you measure one channel alone.** A seventh switch in each channel either lets the
signal through or terminates it. So any single channel can be measured while the others
are switched off electronically, and nobody has to touch a cable. That's twenty nine
switches in total.

**How the board measures itself.** The four channels meet in a divider. A path selector
connects that common port either to the network analyser, which measures phase, or to
a detector on the board, an AD8318, which only measures power but can run on its own
for days. Two temperature sensors, MCP9808, and the detector's own die temperature are
logged too, because drift with temperature is exactly what the learning track studies.

**What drives it.** An external DE1-SoC board, which has an FPGA and an ARM processor
on it. The FPGA sets all sixteen switch lines on the same clock edge, holds them still
while the detector is sampled, and timestamps everything from one clock. The processor
stores the data and runs the inference. A microcontroller could steer the beam fine.
The problem is that switching lines right next to the receiver would add an error that
follows the commanded state, and that error looks exactly like a calibration
coefficient. EXP-005 checks whether that worry is real.

**Why 2.44 GHz?** It's the only licence free band at this size that lets you transmit
continuously: 2400 to 2483.5 MHz, at 10 mW. And the analyser goes up to 3 GHz. The
lower bands limit how often you're allowed to transmit, which a swept measurement
can't respect. That's decision 0004.

**Where it stands.** The schematic is drawn in KiCad by a script, so the four channels
are identical by construction, and it passes its electrical rule check. It still has to
be redrawn for the DE1-SoC controller. Line lengths and antenna sizes wait for the
board stack up. Nothing has been ordered, and decision 0006 says what each purchase is
waiting for.

---

## The tools, and what each one is for

| Tool | What it does in this project | Where it runs |
| --- | --- | --- |
| **Ansys HFSS**, full wave electromagnetic solver | simulates the antenna board: the coupling between the four patches as a 4 port S parameter matrix, and each element's embedded radiation pattern. That's what gate G4 judges, EXP-011. Later, the switched line section, as a check on the circuit model | **HFSS Student at home**, as long as the converged mesh stays under its documented limit of 64,000 volume elements; the full licence at school only for a model that goes over |
| **PyAEDT** | scripting HFSS, for geometry sweeps | planned, not used yet |
| **Keysight ADS**, circuit simulator | a separate model of the switched line channel and the divider, to cross check HFSS under decision 0007 | at school only, and **optional**: nothing in the repository needs it to be reproduced |
| **scikit-rf** | reads every S parameter file, from any tool, as a Touchstone network, and has transmission line models, so a circuit model can be built at home too | everywhere |
| **rfkit**, this repository's own layer on top of scikit-rf | turns those files into answers: it compares only over the band two tools share, takes phase differences around the circle, compares state by state, builds the array state $\mathbf{H}$, works out the error budget and its thresholds, and runs the G4 coupling test | everywhere, 104 tests, `tools/rfkit/` |
| **Network analyser**, a Rohde and Schwarz ZVL | every real RF measurement: 9 kHz to 3 GHz, phase and magnitude, and it exports Touchstone files | the school lab |
| **KiCad** | the schematic, generated by `hardware/rev-a/tools/generate-schematic.py` | at home |
| **DE1-SoC with Quartus** | the controller, and the acquisition test of EXP-005 | at home |
| **Python, NumPy, matplotlib, reportlab** | analysis, figures, and the PDF runbooks | everywhere |

Every measurement and every simulation gets to the analysis the same way:

```
  HFSS   ---.
  ADS    ---+--> Touchstone file --> scikit-rf --> rfkit --> comparison report
  analyser -'                                           --> array state H
                                                        --> G4 verdict on coupling
                                                        --> dataset for inference
```

**Home and school.** The analyser, the full HFSS licence and ADS are all at school. So
every task in the repository is tagged `LOCAL`, `SCHOOL-SOFTWARE`, `SCHOOL-BENCH` or
`EITHER`. Work stays at home whenever that's good enough scientifically. It only moves
to school for an instrument, or for a limit a home tool can't meet. Every school task
gets a step by step PDF, built from a Markdown file and checked automatically, so you
can follow it at the machine days later without having to remember the whole project.
They're all listed in `docs/runbooks/register.md`, and the first one that's ready is
`docs/runbooks/pdf/SCH-001-exp004-analyser-audit.pdf`.

---

## How the work is organised

**Simulation before hardware.** Anything a formula or a simulator can answer gets
answered that way first. In a simulation you know the defects exactly, so you can
check whether a method really works. Decision 0001.

**Rules written before the data.** When an experiment decides something, its rule is
committed before a single number exists, and the commit is the timestamp. The
acquisition test of EXP-005, the thresholds of decision 0007 and the coupling test of
decision 0008 were all done this way. If a rule turns out to be unusable, that's
recorded as a failure and the experiment is redone. It's never adjusted to fit a
result.

**Nothing made up.** A threshold either comes from a derivation you can rerun, or it
says "unresolved" and names what's missing. An unverified figure is marked as
unverified. A value that isn't decided yet is written as a placeholder that names the
decision that will fix it.

**Decisions so far.**

| Decision | What it settles |
| --- | --- |
| 0001 | simulator before hardware |
| 0002 | learning enters as a prior over drift, not as a shortcut to first calibration |
| 0003 | the Rev A architecture: two boards, four elements, three bit switched lines, phase only |
| 0004 | the working frequency, 2.44 GHz |
| 0005 | an external DE1-SoC as the controller |
| 0006 | purchases staged by what they unblock, so that none waits on a question it is needed to answer |
| 0007 | provisional acceptance thresholds, derived from the three bit rounding floor |
| 0008 | gate G4, the test of whether coupling can be left out of the calibration model |

**Gates still open.** G2 asks whether drift over a few hours is bigger than the
measurement's own repeatability, and it decides whether the learning track exists at
all. G4 has its test and is waiting for coupling data. The budget gate gets settled at
order time.

---

## Where it stands

| Done | In progress | Waiting |
| --- | --- | --- |
| architecture, frequency and controller decided | the analyser audit, EXP-004: four of nine readings complete, four partial, one not taken; one visit finishes it, runbook SCH-001 | the purchases, which wait on that visit |
| schematic captured, rule check clean | the acquisition test, EXP-005 Phase A, ready to run at home | the repeatability floor, EXP-005 Phase B, which needs antennas and a detector |
| RF data layer, error budget and coupling test, tested | | the antenna geometry, and with it EXP-011 |
| school runbook system and register | | fabrication, after the pre-fabrication gate of decision 0006 |

---

## The difficulty not to underestimate: measuring

To measure a radiation pattern properly, you have to stand far enough away that the
wave has become flat. The usual minimum distance is:

```math
R > \frac{2 D^{2}}{\lambda}
```

where $D$ is the biggest dimension of the array and $\lambda$ is the wavelength.

For four elements at 2.44 GHz, half a wavelength apart, that's 61.5 mm between them,
so $D \approx 0.18$ m and $\lambda = 0.123$ m:

```math
R > \frac{2 \times 0.18^{2}}{0.123}  \approx  0.55\ \text{m}
```

Under a metre. It fits on a table. But in a normal room the signal bounces off walls,
the floor, furniture and whoever's doing the measuring. Those echoes add to the direct
signal and can shift it by several decibels, which is about the size of what we're
trying to measure.

That's the real obstacle, and the design works around it:

| Route | Principle | Where it stands |
| --- | --- | --- |
| Conducted measurement, channel by channel | measure each channel through a cable at its connector | the backbone: the labels the learning track needs are conducted end to end |
| Coupling measured between element pairs | transmit on one element, receive on another | possible because every element has its own connector |
| Careful free space measurement | distance, differential measurements, absorbers | for the radiated experiments; its quality is what EXP-005 Phase B measures |
| Time domain gating on the analyser | separate the direct path from later echoes | depends on the installed options, reading O8 of EXP-004 |
| An acoustic array | the same mathematics at 40 kHz, with a microphone | not chosen for the first board; kept as the documented response if room reflections prove to dominate |

---

## What the project will compare

| Configuration | What it represents |
| --- | --- |
| Ideal simulation | what theory predicts |
| Real system, uncalibrated | what you get for free |
| Classical calibration | inversion, least squares, regularisation |
| Rotating element field vector, at its own minimum | the power only baseline, not padded to flatter a rival |
| Orthogonal coding | all elements measured at once, the strongest count baseline |
| Mutual coupling | calibration with no external probe, which the per element connectors allow |
| Adaptive measurement selection | choosing each measurement for information gain |
| Learned drift prior | recalibrating from history rather than from nothing |

For each one: pointing error, gain, side lobe level, beam width, how many measurements
it needs, how long calibration takes, and how stable it stays over time. Every count
is also compared with the information limit, so a method gets judged by what's
possible, not just by what its rivals managed.

---

## What already exists, briefly

| Source | What you find there | What you do not |
| --- | --- | --- |
| Academic | array theory, mutual coupling, calibration methods including power only ones, inverse problems | how many physical measurements each method actually needs, compared |
| Industry | fully documented educational kits, beamforming integrated circuits, application notes | how long a calibration stays valid outside a climate chamber |
| Open source | S parameter processing, Bayesian optimisation, amateur projects that document their failures | a cross validation between a radio frequency array and an acoustic one |

The details are in `research/state-of-the-art.md`, and the checked references are in
`docs/references/bibliography.md`.

## How the project will be evaluated

What we count isn't computer time. It's the **number of physical measurements**. A
measurement means moving something, waiting for it to settle, and taking a noisy
reading. The maths afterwards takes milliseconds.

| Criterion | Threshold |
| --- | --- |
| Number of measurements consumed by the method | mandatory next to any calibration result |
| Validation in simulation, where the injected defects are known | mandatory, it is the only place correctness is checkable |
| Measurement repeatability quantified | mandatory, it sets the significance threshold |
| Repetition over several defect draws | mandatory, one draw concludes nothing |
| Measurement conditions and environment recorded | mandatory, room echoes look like lobes |
| Simulated against measured labelling | mandatory |

The reference is the uncalibrated array. It's what tells you how much calibration
actually buys you.

---

## Running what exists

All of this runs on a normal computer. No licence, no instrument.

```bash
python -m pip install -r requirements.txt

cd tools
python -m pytest rfkit/tests -q                 # the RF data layer, on synthetic data
python -m rfkit.cli example --out /tmp/rfkit     # a worked example, synthetic and labelled so
python -m rfkit.cli budget                       # the error budget and how each threshold is derived
python -m rfkit.cli g4-chart                     # the coupling test on synthetic matrices
cd ..

bash tools/check-docs.sh                         # the documentation conventions
python tools/runbooks/build.py --check           # the school runbooks and their PDFs
```

Nothing these commands print is a measurement of a real array. Every trace they use is
marked `synthetic`.

Regenerating the schematic, `python hardware/rev-a/tools/generate-schematic.py`, also
needs KiCad 10. It's free and open source, and the generator reads its stock symbol
libraries. Right now it expects them where the Windows installer puts them by default.

## How to read this repository

| You want to | Go to |
| --- | --- |
| everything in one long reference, from first principles to current status | `docs/aetherarray-master-reference.md` |
| the scope and the questions | `docs/scope.md` |
| the equations, explained | `docs/mathematics/formulation.md` and `docs/mathematics/inverse-calibration.md` |
| why the first board looks the way it does | `docs/architecture/rev-a-rf-architecture.md` and `decisions/0003-rev-a-rf-architecture.md` |
| where learning fits, and where it does not | `docs/architecture/ml-calibration.md` |
| the schematic | `hardware/rev-a/` |
| the RF data layer and its tools | `docs/architecture/rf-data-layer.md` and `tools/rfkit/` |
| the experiments, their rules and their results | `experiments/plan.md` and `results/` |
| every decision, and what would reopen it | `decisions/` |
| what is known, assumed and still to verify | `docs/uncertainties.md` |
| the instruments, and what runs where | `docs/hardware/measurement-bench.md` and `docs/runbooks/` |
| how the documents are written | `CONVENTIONS.md` |

## Licence

Not decided yet. The repository has code, will have measurements, and already has
board design files. The analysis is in `LICENSE-NOTES.md`.
