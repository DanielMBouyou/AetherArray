# Initial backlog

- Status: mirrored into GitHub issues
- Last reviewed: 2026-08-21

## Simulation track, start immediately

| # | Title | Type | Note |
| --- | --- | --- | --- |
| 1 | Implement the array factor and check it against the theoretical cases | experiment | foundation of the whole track |
| 2 | Add defect, coupling and noise injection | experiment | lets us know the truth |
| 3 | Reproduce the statistical effect of phase errors | experiment | validates the simulator against theory |
| 4 | Implement channel by channel calibration | experiment | the basic method |
| 5 | Implement the phase rotation method | experiment | needs only power measurements |
| 6 | Implement regularised inversion | experiment | the complete method |
| 7 | Compare the methods with measurements counted | experiment | main theoretical result |
| 8 | Study noise sensitivity | experiment | sizes the real campaigns |
| 9 | Simulate the planned geometry electromagnetically | experiment | replaces an invented coupling model with a physical one |

## Hardware track, blocking

| # | Title | Type | Note |
| --- | --- | --- | --- |
| 10 | Audit the available instruments | study | gates everything |
| 11 | Check whether the analyser offers time domain gating | study | could solve the echo problem for free |
| 12 | Characterise the environment reflections | experiment | decides the measurement strategy |
| 13 | Measure the repeatability of a power measurement | experiment | the uncertainty floor |
| 14 | Decide the kind of wave, radio frequency or acoustic | decision | depends on 12 and 13 |
| 15 | Decide the working frequency | decision | depends on 10 and 14 |

## Design

| # | Title | Type | Note |
| --- | --- | --- | --- |
| 16 | Compare the beamforming architectures | study | analogue, digital, switched line |
| 17 | Find and cost the phase shifting components | study | cost per channel |
| 18 | Decide the architecture | decision | determines the role of the FPGA |
| 19 | Design the antennas | study | reproducibility between elements matters more than individual performance |
| 20 | Build a two element array | experiment | first real system |
| 21 | Design an angular positioner | study | also useful to the RF modelling project |
| 22 | Group the board order with the RF modelling project | decision | shares the fixed setup cost |

## Measurement and validation

| # | Title | Type | Note |
| --- | --- | --- | --- |
| 23 | Measure the effect of a known cable error | experiment | the most legible demonstration in the project |
| 24 | Measure the uncalibrated pattern | experiment | the control case |
| 25 | Apply a first real calibration | experiment | main result |
| 26 | Measure coupling between elements | experiment | confirms or refutes the diagonal matrix assumption |
| 27 | Compare simulated coupling against measured coupling | experiment | a distinctive deliverable |
| 28 | Measure how long a calibration stays valid | experiment | needs calendar time, start early |

## Advanced methods

| # | Title | Type | Note |
| --- | --- | --- | --- |
| 29 | Study Bayesian optimisation | study | reducing the measurement count |
| 30 | Apply it and measure the real gain | experiment | comparison at an equal measurement budget |
| 31 | Decide whether a learned method is pursued | decision | depends on 30 |

## Infrastructure

| # | Title | Type | Note |
| --- | --- | --- | --- |
| 32 | Automate acquisition and archiving | study | shared with the RF modelling project |
| 33 | Decide the repository licence | decision | code, measurements and board files differ |
| 34 | Organise sharing the network analyser with the RF modelling project | decision | single resource |
