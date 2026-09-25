# Experiment plan

- Status: in progress
- Last reviewed: 2026-09-25

As in the RF modelling project, the work runs on two tracks: a simulation track that
starts immediately, and a hardware track constrained by purchases and fabrication.

---

## Overview

| N | Track | Title | Unblocks | Effort | Status |
| --- | --- | --- | --- | --- | --- |
| 001 | simulation | Array simulator with injected defects | all of the simulation track | 1 week | to do |
| 002 | simulation | Compare calibration methods in simulation | main theoretical result | 2 weeks | to do |
| 003 | simulation | Sensitivity to noise and to measurement count | sizing the real campaigns | 1 week | to do |
| 004 | hardware | Instrument and environment audit | all of the hardware track, and the working frequency | 30 minutes at the bench | **running**, see `EXP-004-instrument-audit.md` |
| 005 | hardware | Repeatability floor, and whether the control path disturbs it | R9 and H3, therefore re-capture and purchase | Phase A about 2 days | **planned**, see `EXP-005-repeatability-floor.md` |
| 006 | hardware | Two element array | first real system | 2 weeks | to do |
| 007 | hardware | Effect of a known cable error | demonstration of the problem | 1 day | to do |
| 008 | hardware | First real calibration | main practical result | 1 week | to do |
| 009 | hardware | Extend to four elements | resolution and coupling | 2 weeks | to do |
| 010 | hardware | How long a calibration stays valid | original angle | calendar time | to do |
| 011 | simulation | Electromagnetic simulation of the real geometry | physically grounded coupling model | 1 week | to do |
| 012 | simulation | Measurement count bound against the classical baselines | sizing every later claim | 3 days | to do |
| 013 | simulation | Learned estimator for first calibration, as a control | ML-A, the learned control | 1 week | to do |
| 014 | hardware | Unattended recalibration rig and its logging schema | ML-B, the drift dataset | 1 week then calendar time | to do |
| 015 | hardware | Learned drift prior against from scratch recalibration | **the project's central claim** | 2 weeks after 014 | to do |

Experiments 012 to 015 come from `docs/architecture/ml-calibration.md` and decision
0002. They are the learning track, and 015 is the one the project's research question
actually names.

---

## EXP-001: array simulator

**Question**: do we have a virtual bench where the defects are known exactly?

**Method**: implement the array factor, inject randomly drawn gain and phase errors,
add adjustable coupling and measurement noise.

**Checks before trusting it**: with no defects and no noise the pattern must match
theory exactly.

- [ ] Beam width matching the classical formula
- [ ] First side lobe near -13 dB with uniform amplitudes
- [ ] Requested broadside pointing gives a maximum exactly at zero
- [ ] Requested 30 degree pointing gives a maximum at 30 degrees
- [ ] Spacing beyond half a wavelength produces a grating lobe at the predicted
      position

These checks are quick to write and catch almost every implementation error.

---

## EXP-002: comparison in simulation

**Question**: which calibration method gives the best quality for a given number of
measurements?

**Method**: apply each method to the same virtual array, with the same defects and
the same noise, counting the measurements consumed. Repeat over many defect draws.

**Deliverable**: quality against measurement count, one curve per method. This is
the central result of the simulation track, and it needs no hardware.

---

## EXP-004: instrument and environment audit

Expanded into its own document on 2026-09-19, because it now carries the working
frequency decision: **`experiments/EXP-004-instrument-audit.md`**.

**Question**: what can we measure, and which working frequency should Rev A use?

**Method**: nine numbered observations at the front panel, each with an expected value
written beforehand, then every reading checked against the datasheet of whatever model
observation O1 returns.

**State**: the local evidence phase is complete and found nothing, which is recorded in
`results/EXP-004/`. The analysis that does not need the bench has been done, so the
visit is a lookup: observation O2, the analyser upper frequency, decides whether
$f_0 = 2.44$ GHz can be used. There is no second radio frequency to fall back on,
because every licence exempt band below it is duty cycle limited.

**Deliverable**: `results/EXP-004/` filled in, then decision 0004 fixing the frequency,
then the physical line lengths in `hardware/rev-a/layout-constraints.md`.

---

## EXP-005: the repeatability floor, and whether the control path disturbs it

Expanded into its own document on 2026-09-25, because it now decides two Rev A
requirements before re-capture or purchase: **`experiments/EXP-005-repeatability-floor.md`**.

**Question, Phase A**: does digital traffic on the control cable produce error that is
correlated with the commanded beam state, does the proposed quiet window remove it, and
does carrying the analogue signal down the cable cost anything against converting it
locally?

**Question, Phase B**: can received power be measured repeatably in the available
environment? This is the original question and it is gated on a detector, a source,
antennas and cables, none of which is owned. Those purchases are staged by decision
0006, and the Rev A order waits on this phase as its gate F3.

**Why Phase A runs now**: it needs no detector. The detector is only a source of a slow
voltage, and a stable direct source substitutes for it, with the advantage that its true
value is known to be constant. The local converter path is a **second DE1-SoC**, of
which three are owned, so both paths use the same converter and the only difference is
the cable.

**What it decides**: requirement R9 and open item H3, both adopted in decision 0005 as
precautions rather than findings. The decision rules are quantitative and were fixed
before any measurement.

**Why it is a priority**: two of the things a schematic re-capture would draw are
exactly what this experiment decides.

---

## EXP-007: demonstration of the problem

**Question**: what is the measurable effect of a known cable length error?

**Method**: two element array, measure the pattern, replace one cable with a
slightly longer one of known length, measure again.

**Hypothesis, written before the measurement**: the introduced phase shift is about
4.4 degrees per millimetre at 2.4 GHz in cable of typical velocity factor. The beam
direction should move by an amount calculable from that.

**Criterion**: agreement between the predicted and measured shift.

**Why this experiment matters**: it is the most legible demonstration in the
project, and it validates the measurement bench at the same time. If the measured
shift matches the calculation, you know the whole setup works and that you are
measuring what you think you are.

---

## EXP-011: electromagnetic simulation of the real geometry

**Question**: what coupling does the planned array actually have?

**Method**: model the intended geometry in the full wave simulator, extract the
coupling matrix, and feed it into the array simulator in place of an invented one.

**Why it matters**: it replaces a guessed coupling model with a physically grounded
one. Later, comparing simulated coupling against coupling measured on the fabricated
array is a result in itself, and it is something most projects at this scale cannot
produce.

---

## EXP-012: where the measurement count bound actually sits

**Question**: how many physical measurements do the classical baselines need, and how
close is that to the information bound, at the element count we are likely to build?

**Method**: in the simulator, run the element by element, rotating element field
vector and orthogonal coding baselines on identical defect draws, at four and eight
elements, counting measurements. Compare against the identifiable parameter count of
$2N-2$ and against the generic power only bound of $4N-4$.

**Deliverable**: the table in `docs/architecture/ml-calibration.md` section 2,
replaced by measured numbers rather than formulas.

**Why it comes first**: every later claim about a learned method saving measurements
is meaningless until this curve exists. Running it before any learned method also
removes the temptation to pick a flattering baseline afterwards.

---

## EXP-013: learned estimator for first calibration, as a control

**Question**: does a supervised estimator trained on simulated arrays beat the
rotating element field vector method at its own minimum of three phase states?

**Method**: specification ML-A in `docs/architecture/ml-calibration.md` section 6.
Train on simulator draws whose coupling comes from EXP-011 and whose noise level comes
from EXP-005.

**Hypothesis, written before the run**: it will not beat the baseline on measurement
count at four elements, because the baseline is already at the bound. It may beat it
on accuracy at a fixed count under noise.

**Mandatory negative test**: train at one error magnitude and one coupling model, test
at another, and report the degradation. A method that only works inside its training
distribution is reported as such.

**Why it is a control and not a contribution**: this is a smaller scale reproduction
of published work, A16 and A21. Its role is to show that the learned machinery works
at all before anything is claimed from it.

---

## EXP-014: unattended recalibration rig

**Question**: can the array calibrate itself repeatedly, with no operator, for weeks?

**Method**: the fabric of an external DE1-SoC executes the beam state sequence, applies
each state at one instant through the registered buffer on the board, holds the control
lines static through the sample window, triggers the converter after an exact settling
delay and timestamps both from one clock. The processor on the same device drains the
records to disk. Decision 0005 and `docs/architecture/control-architecture.md`.
Requirements R3, R4, R5, R8 and R9 in `docs/hardware/rev-a-requirements.md`.

**Criterion**: the rig completes a full classical calibration unattended, repeatedly,
and the session to session spread is at or below the EXP-005 repeatability floor.

**Deliverable**: the dataset. Not a result, a dataset, and it is the input to EXP-015.

**The record schema is fixed, not discovered.** Every measurement writes the fields in
`docs/architecture/control-architecture.md` section 6: session identifier, sequence
index, commanded and read back beam state words, strobe and conversion timestamps, the
settling delay applied, raw converter counts, the converter reference and channel, the
two board temperatures and the detector die temperature, the gateware and software
versions, the connector handling flag, and the analyser state if one was used.

Three of those are easy to omit and expensive to lose. **Raw counts** must be kept
because the noise model is estimated from them and scaling first discards what that
needs. **The read back word** must be kept because it separates a control fault from a
physical effect. **The version fields** must be kept because a timing change between
sessions is otherwise invisible in the data.

**Why the logging schema is part of the experiment**: a drift dataset cannot be
reconstructed afterwards. A session logged without its temperature is a session lost,
and a session logged under a schema that changed mid-campaign is worse, because it
looks usable.

---

## EXP-015: learned drift prior against from scratch recalibration

**Question**: does a prior learned from the array's own history return pointing error
below target using fewer physical measurements than calibrating from scratch?

This is the project's central claim, stated as an experiment.

**Method**: specification ML-B in `docs/architecture/ml-calibration.md` section 6,
posed formally in `docs/mathematics/inverse-calibration.md`. On each held out session,
recalibrate from the prior using $P$ measurements, then run a full classical
calibration immediately afterwards to supply the label.

The prior is the learned part and enters only as $p(\mathbf{H}_t \mid \mathcal{D})$.
The likelihood stays explicit physics, so a wrong prior costs measurements rather than
giving a wrong answer quietly. Each fresh measurement is chosen by expected information
gain over the reachable beam states, which is an enumeration at this array size, not a
search.

**Controls**: recalibrating from scratch, and applying the previous calibration
unchanged.

**Criterion**: the smallest $P$ that returns pointing error below target, compared
against the $4N-4$ the same array needs from scratch. Reported as a curve with spread
bands over sessions, never as a single number.

**Failure is declared, not explained away, if**: the required $P$ is not below the
from scratch count on held out sessions, or if gate G2 has already shown that drift
sits under the repeatability floor.

**Prerequisite**: EXP-005 and EXP-010 must first show that drift over hours is
measurable at all. If it is not, this experiment does not run and decision 0002 is
superseded.

---

## Later

EXP-008 and EXP-009 will be detailed once the earlier ones have run. EXP-010, on how
long a calibration lasts, needs little work but a lot of calendar time, so it can run
alongside the others. It has been promoted: it now gates EXP-014 and EXP-015, and
therefore the learning track as a whole.
