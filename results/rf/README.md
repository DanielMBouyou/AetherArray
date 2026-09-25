# RF measurement and simulation data

- Status: layout defined, no data yet
- Last reviewed: 2026-09-25

S parameter data from every source, in one place, under the repository's
existing `raw` and `processed` split from `results/README.md`.

**This directory is empty of data.** No electromagnetic solve, no circuit
simulation and no analyser sweep has been performed. The layout exists so the
first one has somewhere correct to go.

## Layout

```
results/rf/
  SOURCE.md          origin, date, operator, versions, per the repository rule
  raw/               never modified once written
    hfss/            electromagnetic solver exports, .sNp
    ads/             circuit simulator exports, .sNp
    vna/             analyser sweeps, .sNp
  processed/         regenerable from raw plus configuration, never hand edited
```

`raw/vna/` is what other documents call the analyser raw path. The three source
directories are separate because a trace's origin decides how it is read: the
loader takes the source as an argument and does not guess it from a path.

## Rules

| Rule | Why |
| --- | --- |
| **Neither `raw/` nor `processed/` is tracked by git** | the repository already ignores `results/**/raw/` and `results/**/processed/`, and `CONVENTIONS.md` section 7 holds data out of history until a storage policy is decided. Both directories are created on demand and live on disk, not in the repository |
| This file and `SOURCE.md` **are** tracked | the metadata survives in git even though the data does not, which is the point of the rule |
| `raw/` is write once | `results/README.md`: a wrong raw measurement is not corrected, it is annotated and retaken |
| `processed/` is reproducible from `raw/` plus a recorded command | a figure that cannot be regenerated from tracked instructions plus untracked data is not reproducible |
| Solver working files stay out entirely | `.gitignore` excludes them by extension as well |

**Consequence worth stating.** A clean clone gives you this file, `SOURCE.md` and
the tooling, and no data at all. That is intended. Recreate the directories with

```bash
mkdir -p results/rf/raw/{hfss,ads,vna} results/rf/processed
```

and populate them from wherever the data is kept.

## Regenerating processed outputs

```bash
cd tools
python -m rfkit.cli compare \
    --hfss ../results/rf/raw/hfss/example.s2p \
    --ads  ../results/rf/raw/ads/example.s2p \
    --vna  ../results/rf/raw/vna/example.s2p \
    --f0 2.44e9 \
    --json ../results/rf/processed/comparison.json \
    --report ../results/rf/processed/comparison.txt
```

The working frequency is fixed at 2.44 GHz by decision 0004. The tool refuses to
evaluate at a frequency outside the range the inputs share, rather than
extrapolating to reach it.
