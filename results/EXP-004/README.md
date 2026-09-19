# EXP-004 results

- Status: partial, local evidence phase complete, bench observations outstanding
- Last reviewed: 2026-09-19

Plan and decision rule in `experiments/EXP-004-instrument-audit.md`.

## Result 1, 2026-09-19: no local evidence identifies the instruments

A negative result, recorded so that the search is not repeated. Every avenue that
could have identified the network analyser without walking to the bench was tried and
none carried information.

| Avenue | Method | Outcome |
| --- | --- | --- |
| Consolidated private inventory | read the instrument section | every field marked entirely unknown |
| Instrument and driver software | enumerate installed programs for the known vendor and interface names | none installed |
| Instrument control library | check whether the standard instrument control package is importable | absent |
| Historic USB attachment | read the operating system device enumeration records for the vendor identifiers of the mainstream instrument makers | no such vendor identifier has ever been enumerated on this machine |
| Instrument class devices | search the same records for the standard instrument class driver | none |
| Saved measurements | search the user profile for Touchstone files | none, other than the sample files shipped inside a library |

### What this rules out

The analyser has never been connected to this computer. That is consistent with the
inventory, and it means the remote interface, observation O9, is unproven as well as
the rest.

### What it does not rule out

An instrument that exists, works, and has simply never been plugged in. Nothing here
is evidence about the instrument itself, only about its absence from this machine.

### Consequence

The bench visit is unavoidable. It is also now short: the analysis in the experiment
document reduces the frequency decision to one reading, observation O2.

## Result 2: the bench observations

Not yet made. The table below is the form to fill in. Expected values are in the
experiment document so that a surprise is visible while standing at the instrument.

| N | Observation | Reading | Date | Matches expectation |
| --- | --- | --- | --- | --- |
| O1 | Manufacturer, model, serial | to measure | | |
| O2 | Maximum sweep frequency | to measure | | |
| O3 | Minimum sweep frequency | to measure | | |
| O4 | Transmission measurement available | to measure | | |
| O5 | Complex format available | to measure | | |
| O6 | Source power range | to measure | | |
| O7 | Calibration kit and connector type | to measure | | |
| O8 | Time domain or gating present | to measure | | |
| O9 | Remote interface enumerates | to measure | | |

No cell in this table is filled from a catalogue, a memory or a guess. A reading that
was not taken stays as `to measure`.
