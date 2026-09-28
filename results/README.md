# Results

This folder holds measurements that were actually taken. Not the ones we're hoping to
take.

## Layout

```
results/
  EXP-001-name/
    SOURCE.md        origin, date, operator, hardware, versions
    raw/             raw data, never modified
    processed/       derived data, regenerable by script
    figures/
    notes.md         what went wrong during the session
```

`raw/` is read only, by convention. If a raw measurement is wrong, we don't fix it. We
add a note and take the measurement again.

## Metadata rule

A measurement without its metadata is lost. `SOURCE.md` has to contain at least:

- date and time,
- the hardware used, with identifiers,
- software, bitstream or firmware versions,
- conditions (room temperature where it matters, supply, cabling),
- the calibration procedure and its date,
- anything odd that was noticed.

## Large file policy

This gets decided before the first serious measurement campaign.

| Option | Advantage | Drawback | Status |
| --- | --- | --- | --- |
| Everything in git | simple, self-contained | heavy repository, slow clone | to evaluate |
| Git LFS | integrated with GitHub | quota, friction for contributors | to evaluate |
| Data outside the repository, hashes inside | light repository | needs reliable external storage | to evaluate |
| Subsample in git, raw outside | compromise | risk of the two drifting apart | to evaluate |

Until then, files stay in the low megabytes, and compressible text formats win.

## Reproducibility

Every figure in the README or in a document has to be regenerable by a script in this
repository, from the data in `raw/`. A figure without a script is labelled as an
illustration.
