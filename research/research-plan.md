# Research plan

- Status: in progress
- Last reviewed: 2026-08-21

## Principle

Two parallel tracks. The simulation track starts immediately and produces the
theoretical result. The hardware track, slower, produces the real validation.

## Lot 1: fundamentals and simulator (simulation track)

| Task | Deliverable | Stopping criterion |
| --- | --- | --- |
| Read the array fundamentals | notes A1 and A2 | we can write the equations without error |
| Implement and check the array factor | tested simulator | beam width and side lobes matching theory |
| Add defects, coupling and noise | complete simulator | defects known, so estimation error measurable |
| Study the statistical effect of errors | note A9 | we can predict the gain loss before measuring |
| Simulate the real geometry electromagnetically | coupling matrix | the coupling model comes from physics, not invention |

## Lot 2: calibration methods (simulation track)

| Task | Deliverable | Stopping criterion |
| --- | --- | --- |
| Study phase rotation calibration | note A6 | method understood and implemented |
| Study calibration through coupling | note A7 | we know whether it applies at our scale |
| Implement the classical methods | tested code | correct results in simulation |
| Study regularisation and conditioning | note A11 | we can diagnose an unstable inversion |
| Compare the methods in simulation | EXP-002 | quality against measurement count curves |

## Lot 3: measurement environment (hardware track, blocking)

| Task | Deliverable | Stopping criterion |
| --- | --- | --- |
| Audit the instruments | inventory filled in | we know what we can measure |
| Check for time domain gating | note | we know how to handle echoes |
| Characterise the environment reflections | EXP-005 | uncertainty floor quantified |
| Decide the measurement strategy | decision record | argued choice |

## Lot 4: array design

| Task | Deliverable | Stopping criterion |
| --- | --- | --- |
| Compare the architectures | `docs/architecture/options.md` completed | four costed options |
| Decide the kind of wave and the frequency | decision record | justified by the measurement means |
| Study the available phase shifting components | comparison with prices | cost per channel known |
| Design a two element array | schematic and layout | first realisable system |

## Lot 5: measurement and validation

| Task | Deliverable | Stopping criterion |
| --- | --- | --- |
| Measure the effect of a known cable error | EXP-007 | calculation and measurement agree |
| Calibrate the real array | EXP-008 | measured improvement in the pattern |
| Extend to four elements | EXP-009 | coupling observable |
| Measure how long a calibration lasts | EXP-010 | degradation against time curve |
| Compare simulated and measured coupling | analysis note | gap quantified and discussed |

## Lot 6: advanced methods

Conditional on the lot 2 results.

| Task | Deliverable | Stopping criterion |
| --- | --- | --- |
| Study Bayesian optimisation | note A13 | method understood |
| Apply it to reducing the measurement count | results | quantified gain, or none |
| Study drift prediction | note | feasibility assessed |

## Skills to acquire

| Skill | Target level | How | Verified by |
| --- | --- | --- | --- |
| Antenna array theory | able to predict a pattern | reference texts | simulator matching theory |
| Pattern measurement | able to measure cleanly | practice and a written protocol | repeatable measurement |
| Inverse problems and regularisation | able to diagnose an unstable inversion | literature, simulation | condition number computed and interpreted |
| Derivative free optimisation | able to choose and tune a method | literature, trials | honest comparison against a reference |
| Printed antenna design | able to design and simulate | available tools | measured matching agreeing with simulation |
| Electromagnetic simulation and scripting | able to model and sweep a structure | tool documentation | simulated coupling compared against measurement |
| Bench automation | able to drive and archive | shared with the RF modelling project | automated campaign |

## Stopping criterion for the study phase

1. The simulator exists and is checked.
2. The classical methods are compared in simulation.
3. The measurement environment is characterised, with a quantified uncertainty
   floor.
4. The array architecture is chosen and justified.
