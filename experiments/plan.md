# Experiment plan

- Status: in progress
- Last reviewed: 2026-08-21

As in the RF modelling project, the work runs on two tracks: a simulation track that
starts immediately, and a hardware track constrained by purchases and fabrication.

---

## Overview

| N | Track | Title | Unblocks | Effort | Status |
| --- | --- | --- | --- | --- | --- |
| 001 | simulation | Array simulator with injected defects | all of the simulation track | 1 week | to do |
| 002 | simulation | Compare calibration methods in simulation | main theoretical result | 2 weeks | to do |
| 003 | simulation | Sensitivity to noise and to measurement count | sizing the real campaigns | 1 week | to do |
| 004 | hardware | Instrument and environment audit | all of the hardware track | 2 days | to do |
| 005 | hardware | Repeatable power measurement trial | feasibility of any measurement | 2 days | to do |
| 006 | hardware | Two element array | first real system | 2 weeks | to do |
| 007 | hardware | Effect of a known cable error | demonstration of the problem | 1 day | to do |
| 008 | hardware | First real calibration | main practical result | 1 week | to do |
| 009 | hardware | Extend to four elements | resolution and coupling | 2 weeks | to do |
| 010 | hardware | How long a calibration stays valid | original angle | calendar time | to do |
| 011 | simulation | Electromagnetic simulation of the real geometry | physically grounded coupling model | 1 week | to do |

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

**Question**: what can we measure, and are the room reflections small enough?

**Method**: record every instrument model and its characteristics. Check whether the
network analyser offers time domain gating, since that would solve much of the echo
problem for free.

**Deliverable**: `docs/hardware/inventory-and-needs.md` filled in.

---

## EXP-005: repeatable power measurement

**Question**: can received power be measured repeatably in the available
environment?

**Method**: fixed setup, measurement repeated over several minutes, then after
moving an object in the room, then with somebody walking past.

**Criterion**: standard deviation of the repeated measurements. That number becomes
the uncertainty floor and decides whether pattern measurement is possible at all.

**Why it is a priority**: if the variation caused by the environment exceeds the
effect we want to measure, the strategy has to change immediately, before any
purchase.

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

## Later

EXP-008 to EXP-010 will be detailed once the earlier ones have run. EXP-010, on how
long a calibration lasts, needs little work but a lot of calendar time, so it can run
alongside the others.
