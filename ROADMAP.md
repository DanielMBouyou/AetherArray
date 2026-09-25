# Roadmap

- Status: proposal, revised after each phase
- Last reviewed: 2026-09-25

## Phase 0: theory and simulator

- [ ] Fundamentals read, equations written correctly
- [ ] Array simulator implemented and checked against the theoretical cases
- [ ] Defects, coupling and noise injectable
- [ ] Statistical effect of errors reproduced in simulation
- [ ] Electromagnetic simulation of the planned geometry, giving a physical coupling model

**Exit**: we have a virtual bench where the truth is known.

## Phase 1: calibration methods in simulation

- [ ] Classical methods implemented
- [ ] Comparison with measurements counted
- [ ] Noise sensitivity characterised
- [ ] Quality against measurement count curves produced

**Exit**: the theoretical result of the project exists, with no hardware.

## Phase 2: measurement environment

- [ ] Instruments audited
- [ ] Environment reflections characterised
- [ ] Measurement repeatability quantified
- [ ] Measurement strategy decided
- [x] Radio frequency or acoustic route decided: radio frequency for the first board,
      decisions 0003 and 0004, before the environment was characterised

**Exit**: we know whether and how a pattern can be measured.

## Phase 3: first real array

- [x] Architecture and frequency chosen: decisions 0003 and 0004
- [ ] Two element array built
- [ ] Effect of a known cable error measured, and matching the calculation
- [ ] Uncalibrated pattern measured

**Exit**: the demonstration of the problem exists, with measurements behind it.

## Phase 4: real calibration

- [ ] First calibration method applied to the real array
- [ ] Improvement measured on the pattern
- [ ] Several methods compared, measurements counted
- [ ] Confrontation with the phase 1 predictions

**Exit**: the project's main result.

## Phase 5: extension and robustness

- [ ] Four element array
- [ ] Coupling measured and compared against the simulated coupling
- [ ] How long a calibration stays valid, measured
- [ ] Thermal sensitivity assessed

## Phase 6: advanced methods

Conditional.

- [ ] Bayesian optimisation applied to reducing the measurement count
- [ ] Quantified gain, or a documented absence of gain
- [ ] Drift prediction studied

## Early exit points

| Stop after | What is still publishable |
| --- | --- |
| Phase 1 | a rigorous comparison of calibration methods in simulation, with a physically grounded coupling model |
| Phase 3 | a measured demonstration of the gap between theory and reality |
| Phase 4 | the complete result of the project |

## The structural decision to take early

The kind of array, radio frequency or acoustic, has to be settled at the end of
phase 2, based on what the measurement environment genuinely allows. That choice
changes the cost, the schedule and how the project is presented, but not its
scientific content.

**Settled for the first board on 2026-09-23**, earlier than planned. Decision 0003 chose
the switched line radio frequency architecture, and decision 0004 fixed 2.44 GHz once
the analyser was observed to cover it. The environment has still not been
characterised. That risk now sits with EXP-005 Phase B, and if reflections dominate,
the documented response is conducted measurement or the acoustic route,
`docs/uncertainties.md` section 2.
