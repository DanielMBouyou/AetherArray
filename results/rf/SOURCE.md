# Source record for results/rf

- Status: no data yet
- Last reviewed: 2026-09-25

`CONVENTIONS.md` section 7 requires a source record beside every dataset. This
is that record, and it is empty because the directory is empty.

## Datasets

| Dataset | Date | Origin | Hardware and identifiers | Software versions | Conditions | Calibration | Anomalies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none yet | not applicable | not applicable | not applicable | not applicable | not applicable | not applicable | not applicable |

## What must be filled in for each dataset added

- Date and time.
- Origin: electromagnetic solver, circuit simulator or analyser, with the exact
  tool and version.
- Hardware with identifiers, for a measurement: which analyser, which cables,
  which board.
- Conditions: ambient temperature, supply, cabling, source power actually used.
- Calibration procedure and its date. **At the time of writing no calibration
  has been performed and none can be**: no kit or adapters have been confirmed
  to exist, which is EXP-004 observation O7. Traces loaded by the analysis
  package carry `calibration="none"` until that changes.
- Anything anomalous noticed during the session.

A dataset that arrives without these is not admitted here.
