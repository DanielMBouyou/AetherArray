# Results

This directory holds measurements that were actually taken, not measurements we
hope to take.

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

`raw/` is read-only by convention. If a raw measurement is wrong, we do not fix
it: we add a note and take the measurement again.

## Metadata rule

A measurement without metadata is lost. `SOURCE.md` must contain at least:

- date and time,
- hardware used, with identifiers,
- software, bitstream or firmware versions,
- conditions (ambient temperature where relevant, supply, cabling),
- calibration procedure and its date,
- anything anomalous that was noticed.

## Large file policy

To be decided before the first serious measurement campaign.

| Option | Advantage | Drawback | Status |
| --- | --- | --- | --- |
| Everything in git | simple, self-contained | heavy repository, slow clone | to evaluate |
| Git LFS | integrated with GitHub | quota, friction for contributors | to evaluate |
| Data outside the repository, hashes inside | light repository | needs reliable external storage | to evaluate |
| Subsample in git, raw outside | compromise | risk of the two drifting apart | to evaluate |

Until this is decided, files stay in the low megabytes and compressible text
formats are preferred.

## Reproducibility

Every figure published in the README or in a document must be regenerable by a
script in this repository, from the data in `raw/`. A figure with no associated
script is labelled as illustrative.
