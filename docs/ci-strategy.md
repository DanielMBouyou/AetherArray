# Continuous integration strategy

- Status: target defined
- Last reviewed: 2026-08-21

## Where we are

Only the documentation check is active.

## Target

| Stage | Trigger | What is checked | Status |
| --- | --- | --- | --- |
| 1 | documentation | conventions, structure, language | active |
| 2 | simulator | the theoretical reference cases are reproduced | planned |
| 3 | calibration methods | with no noise, the injected defects are recovered exactly | planned |
| 4 | comparison | a reduced set of draws reproduces the same conclusions | planned |
| 5 | figure scripts | every figure regenerates without error | planned |

Stages 2 and 3 are the most useful: they check the scientific core of the project in
seconds.

## Point of attention

The methods being compared are stochastic: they depend on random draws. In
continuous integration the seeds have to be fixed, otherwise tests fail occasionally
for no reason, which destroys trust in the pipeline.

Variable seed campaigns have their place, but launched deliberately, with the seeds
recorded in the results.

## What stays manual

- Every physical measurement.
- Control of the measurement environment.
- Electromagnetic simulation runs, which are long and need a licensed tool.
- Interpreting the gaps between simulation and measurement.
