# RF measurement and simulation data

- Status: layout defined, no data yet
- Last reviewed: 2026-09-28

S parameter data from every source goes here, using the same `raw` and `processed`
split as `results/README.md`.

**There's no data in here yet.** No electromagnetic solve, no circuit simulation and no
analyser sweep has been done. The layout exists so the first one has a proper place to
land.

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
folders are kept apart because where a trace comes from decides how it's read: the
loader takes the source as an argument, and it never guesses it from the path.

## Rules

| Rule | Why |
| --- | --- |
| **Neither `raw/` nor `processed/` is tracked by git** | the repository already ignores `results/**/raw/` and `results/**/processed/`, and `CONVENTIONS.md` section 7 keeps data out of history until a storage policy is decided. Both folders get created when needed and live on disk, not in the repository |
| This file and `SOURCE.md` **are** tracked | the metadata survives in git even though the data doesn't, which is the whole point of the rule |
| `raw/` is write once | `results/README.md`: a wrong raw measurement isn't corrected, it's annotated and retaken |
| `processed/` is reproducible from `raw/` plus a recorded command | a figure you can't regenerate from tracked instructions and untracked data isn't reproducible |
| Solver working files stay out entirely | `.gitignore` excludes them by extension as well |

**Worth saying out loud.** A fresh clone gives you this file, `SOURCE.md` and the
tools. No data at all. That's on purpose. Recreate the folders with

```bash
mkdir -p results/rf/raw/{hfss,ads,vna} results/rf/processed
```

and fill them from wherever the data is kept.

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

The working frequency is fixed at 2.44 GHz by decision 0004. The tool won't evaluate
at a frequency outside the range the inputs share. It refuses, rather than
extrapolating to get there.
