# rfkit

- Status: implemented and tested against synthetic traces only
- Last reviewed: 2026-09-28

The shared RF data layer. The why is in `docs/architecture/rf-data-layer.md`. This file
is the how.

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

You give each file's source on the command line. It's never guessed from the path.
The comparison only happens over the band all the inputs share, and asking for a
frequency outside it is an error, not an extrapolation.

This compares plain differences, so its S21 verdicts say `not applicable`. Here's why:
part of a plain difference is the same in every state, and the array state absorbs it.
To judge against the S21 limits, compare the same channel in every state instead:

```bash
cd tools
python -m rfkit.cli compare-states \
    --a-source hfss --a 0=../results/rf/raw/hfss/state0.s2p --a 3=../results/rf/raw/hfss/state3.s2p \
    --b-source ads  --b 0=../results/rf/raw/ads/state0.s2p  --b 3=../results/rf/raw/ads/state3.s2p \
    --reference-state 0 \
    --json ../results/rf/processed/states.json
```

It's judged over the whole of band 57a, both edges and $f_0$. If the files don't cover
the band, it says `unresolved`.

## The error budget and the thresholds

```bash
cd tools
python -m rfkit.cli budget --json ../results/rf/processed/budget.json
```

This prints the sensitivity study, and how every provisional threshold is derived,
decision 0007. All the random seeds are fixed, so two runs print exactly the same text.

## Gate G4, coupling

```bash
cd tools
python -m rfkit.cli g4 --antenna final.s4p --source hfss \
    --previous-pass previous.s4p --patterns patterns.npz --json g4.json
python -m rfkit.cli g4-chart
```

The first command applies decision 0008 to one antenna matrix. What each stage has to
supply is in `experiments/EXP-011-coupling-model-adequacy.md`. The second prints G4
against **synthetic** nearest neighbour coupling, which isn't a prediction of any real
array.

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

Each channel trace is that channel measured on its own. On Rev A, that means one
channel enabled and the others terminated.

## Worked example, synthetic

```bash
cd tools && python -m rfkit.cli example --out /tmp/rfkit-example
```

**Every number it produces is synthetic**, and every trace carries `synthetic` as its
source.

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
| `coupling` | gate G4: the coupled forward model, the diagonal model it is judged against, and the rules of decision 0008 |
| `state` | per channel S21 to the array state, diagonal now, full supported |
| `dataset` | repeated measurements with metadata, and the inference record |
| `calibration` | interfaces that refuse until standards exist |
| `instrument` | the adapter boundary, deliberately empty of drivers |

## Two rules worth repeating

**Nothing makes up a threshold.** A value only exists if `rfkit.budget` derives it and
decision 0007 adopted it, and the tests fail if the two ever disagree. If a verdict
says `unresolved`, it's because a term the limit needs is still unknown, and the note
on that threshold says which one.

**Nothing pretends to be calibrated.** `apply_calibration` raises an error. No
calibration kit, adapters or fixture have been confirmed to exist yet, and that's
EXP-004 reading O7.
