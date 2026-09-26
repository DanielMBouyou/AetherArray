# rfkit

- Status: implemented and tested against synthetic traces only
- Last reviewed: 2026-09-25, error budget and provisional thresholds added

The shared RF data layer. Architecture and rationale in
`docs/architecture/rf-data-layer.md`; this file is how to run it.

## Install and test

```bash
python -m pip install -r requirements.txt
cd tools
python -m pytest rfkit/tests -q
```

## Compare traces from different tools

```bash
cd tools
python -m rfkit.cli compare \
    --hfss ../results/rf/raw/hfss/thing.s2p \
    --ads  ../results/rf/raw/ads/thing.s2p \
    --vna  ../results/rf/raw/vna/thing.s2p \
    --f0 2.44e9 \
    --json ../results/rf/processed/comparison.json \
    --report ../results/rf/processed/comparison.txt
```

The source of each file is given on the command line and never inferred from its
path. Comparison happens on the band all inputs share; a frequency outside it is
an error, not an extrapolation.

This compares plain differences, and its S21 verdicts read `not applicable`: part of
a plain difference is common to every state, and the array state absorbs it. To judge
against the S21 limits, compare the same channel in every state:

```bash
cd tools
python -m rfkit.cli compare-states \
    --a-source hfss --a 0=../results/rf/raw/hfss/state0.s2p --a 3=../results/rf/raw/hfss/state3.s2p \
    --b-source ads  --b 0=../results/rf/raw/ads/state0.s2p  --b 3=../results/rf/raw/ads/state3.s2p \
    --reference-state 0 \
    --json ../results/rf/processed/states.json
```

It is judged over all of band 57a, both edges and $f_0$, and reads `unresolved` if the
files do not cover the band.

## The error budget and the thresholds

```bash
cd tools
python -m rfkit.cli budget --json ../results/rf/processed/budget.json
```

Prints the sensitivity study and the derivation of every provisional threshold,
decision 0007. Every seed is fixed, so two runs print the same text.

## Build the array state

```bash
cd tools
python -m rfkit.cli state \
    --channel 0=../results/rf/raw/vna/ch0.s2p \
    --channel 1=../results/rf/raw/vna/ch1.s2p \
    --channel 2=../results/rf/raw/vna/ch2.s2p \
    --channel 3=../results/rf/raw/vna/ch3.s2p \
    --f0 2.44e9 --reference 0 \
    --json ../results/rf/processed/state.json
```

Each channel trace is that channel measured alone, which on Rev A means one
channel enabled and the others terminated.

## Worked example, synthetic

```bash
cd tools && python -m rfkit.cli example --out /tmp/rfkit-example
```

**Every number it produces is synthetic** and every trace carries `synthetic` as
its source.

## Modules

| Module | Holds |
| --- | --- |
| `provenance` | where a trace came from, and its checksum |
| `io` | Touchstone loading, and synthetic construction for tests |
| `grid` | shared band, common grid, refusal to extrapolate |
| `metrics` | extraction at a point and over a band, phase on the circle |
| `budget` | from an RF error to its array level consequence, and the derivation of every threshold |
| `thresholds` | limits by metric and comparison class, each provisional, unresolved or not a limit |
| `compare` | pairwise agreement, and state by state agreement on what calibration cannot absorb |
| `state` | per channel S21 to the array state, diagonal now, full supported |
| `dataset` | repeated measurements with metadata, and the inference record |
| `calibration` | interfaces that refuse until standards exist |
| `instrument` | the adapter boundary, deliberately empty of drivers |

## Two rules worth repeating

**Nothing invents a threshold.** A value exists only if `rfkit.budget` derives it
and decision 0007 adopted it, and the tests fail if the two part company. If a
verdict reads `unresolved`, a term the limit needs is unknown, and the note on the
threshold names it.

**Nothing claims a calibration.** `apply_calibration` raises. No kit, adapters
or fixture have been confirmed to exist, which is EXP-004 observation O7.
