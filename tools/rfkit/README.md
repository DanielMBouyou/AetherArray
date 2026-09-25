# rfkit

- Status: implemented and tested against synthetic traces only
- Last reviewed: 2026-09-25

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
| `thresholds` | limits with their sources, or `unresolved` |
| `compare` | pairwise agreement, machine and human readable |
| `state` | per channel S21 to the array state, diagonal now, full supported |
| `dataset` | repeated measurements with metadata, and the inference record |
| `calibration` | interfaces that refuse until standards exist |
| `instrument` | the adapter boundary, deliberately empty of drivers |

## Two rules worth repeating

**Nothing invents a threshold.** If a verdict reads `unresolved`, the limit has
not been decided anywhere in the repository, and deciding it belongs in a
decision record.

**Nothing claims a calibration.** `apply_calibration` raises. No kit, adapters
or fixture have been confirmed to exist, which is EXP-004 observation O7.
