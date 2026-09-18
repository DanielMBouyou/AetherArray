# Benchmark specification

- Status: draft, to be frozen before the first comparison
- Last reviewed: 2026-08-21

`methodology.md` explains the intent. This document is the contract.

---

## 1. System boundary

The array under test runs from the **input of the feed network** to the radiating
elements. Everything upstream, meaning the source and the cables to the bench, is
characterised separately and either calibrated out or reported.

For conducted measurements the boundary is the calibration reference plane, stated
explicitly. For radiated measurements the boundary includes the elements and the
environment, and the environment is described alongside the result.

## 2. Inputs

| Property | Specification |
| --- | --- |
| Commands | complex amplitude and phase per channel, quantised if the hardware quantises |
| Requested steering angles | a fixed list, at minimum broadside, 15, 30 and 45 degrees |
| Defect draws, in simulation | at least 20 independent draws per configuration |
| Noise level, in simulation | swept over at least three levels |
| Determinism | fixed seeds, recorded |

## 3. Outputs

The measured or simulated pattern, the achieved pointing direction, the gain, the
side lobe level, and the number of measurements consumed.

## 4. Baselines

| Baseline | Definition | Role |
| --- | --- | --- |
| B0, ideal | perfect array, no defects | what theory promises |
| B1, uncalibrated | real defects, theoretical commands applied | **the control, and what everything is judged against** |
| B2, channel by channel | each channel measured separately | the basic method |
| B3, phase rotation | power only measurements, run at its minimum of three phase states | the classical method needing no phase measurement |
| B4, regularised inversion | full matrix estimation | the complete method |
| B5, orthogonal coding | every element measured at once under orthogonal codes | the strongest measurement count baseline |
| B6, mutual coupling | element pairs measured against each other | the only method needing no external probe, and conditional on per element access |
| B7, information bound | $2N-2$ identifiable parameters, $4N-4$ generic power only measurements | not a method, the floor every count is quoted against |

B3 is run at three phase states because that is its own minimum. Running it at eight
or sixteen and reporting the difference as somebody else's gain would be a result
about the baseline, not about the method.

B1 is the most important row and the cheapest to obtain. Without it there is no way
to say what calibration is worth.

## 5. Primary metric

Pointing error and side lobe level, both plotted against the **number of physical
measurements consumed**.

Not a single number: one curve per method, since the interesting question is what
you get for a given measurement budget.

## 6. Secondary metrics

Gain, beam width, deviation from the target pattern, estimation error in simulation,
condition number, calibration time, and validity after several hours.

## 7. Measurement method

As set out in `methodology.md`, with a reference measurement at the start and the end
of every session, and the repeatability quantified in EXP-005 acting as the
significance threshold.

## 8. Repetitions and reporting

| Item | Requirement |
| --- | --- |
| Defect draws in simulation | at least 20 |
| Repeats on the real array | at least 3 sessions for any published conclusion |
| Reporting | curves with spread bands, never single numbers |
| Uncertainty | measured, and drawn on the figures |

## 9. Failure criteria

Reported as failed, not quietly dropped, if:

- the start and end reference measurements differ by more than the stated
  uncertainty,
- the environment changed during the campaign,
- a method is compared without its measurement count,
- the simulation coupling model was not stated.

## 10. Reproducibility requirements

The repository must contain the simulator with its seeds, the calibration
implementations, the measurement scripts, the array geometry, the tool versions, and
the plotting script for every published figure.

## 11. The one figure that would summarise the project

Pointing error against number of physical measurements, one curve per calibration
method, with the uncalibrated case as a horizontal line near the top and the ideal
simulation as a horizontal line near the bottom.

Everything the project is about sits in that plot: how far from ideal you start, how
fast each method closes the gap, and how many measurements that costs. The vertical
gap between the two horizontal lines is the value of calibration itself. The
horizontal distance between curves is the value of a better method.

It does not exist yet, and no placeholder version will be produced.

## 12. Biggest threats to the validity of this benchmark

| Threat | Effect | Mitigation |
| --- | --- | --- |
| Room reflections dominating | echoes look like lobes and everything is wrong | environment characterised first, time gating if available, conducted measurement as fallback |
| Invented coupling model in simulation | conclusions do not transfer to the real array | coupling taken from full wave simulation of the real geometry, then checked against measurement |
| Single defect draw | results vary enormously between draws | at least 20 draws |
| Not counting measurements | an expensive method looks free | measurement count mandatory in every row |
| Operator present during measurement | a human body changes the pattern measurably | protocol requires distance |
| Comparing calibrated and uncalibrated across sessions | drift confounded with improvement | both measured in the same session, with reference checks |
