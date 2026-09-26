# The RF data layer

- Status: implemented, no measured or simulated data yet
- Last reviewed: 2026-09-25

One library sits between every producer of S parameters and every consumer of
them. It is `scikit-rf`, wrapped by a small package in `tools/rfkit/`.

```
  HFSS  ---.
  ADS   ---+--> Touchstone --> skrf.Network --> rfkit --> comparison report
  VNA   ---'                                           --> array state H
                                                       --> dataset for inference
```

## 1. Why a shared layer rather than a script per task

The project compares three things that are easy to compare wrongly: a full wave
solve, a circuit simulation and a measurement. EXP-011 exists to put simulated
coupling next to measured coupling, and decision 0002 depends on per element
complex measurements becoming the labels that supervise the learned prior.

Each of those is a place where a quiet mistake would not announce itself.
Comparing two traces over a frequency range only one of them covers, or calling
the difference between 359 and 1 degrees 358 degrees, produces a plausible
number and a wrong conclusion. Putting those rules in one tested place is
cheaper than remembering them in each notebook.

## 2. What the layer guarantees

| Guarantee | Where it lives | What it prevents |
| --- | --- | --- |
| No trace without provenance: source, path, checksum, ports, reference impedance, sweep, calibration state | `rfkit.provenance`, `rfkit.io` | a number in a document that cannot be traced to a file |
| Comparison only over the shared band, **never extrapolated** | `rfkit.grid` | agreement manufactured by padding one sweep to another |
| The comparison grid is the **coarsest** contributing sweep unless overridden | `rfkit.grid.common_grid` | resolution invented that no input had |
| Phase differences taken on the circle | `rfkit.metrics.phase_error_deg` | 359 against 1 reported as 358 degrees |
| Phase spread across channels taken about the circular mean | `rfkit.metrics.phase_spread_deg` | a set clustered at the wrap point reporting a spurious 360 degrees |
| **No invented thresholds.** A limit is derived from its array level consequence and marked provisional, or every verdict against it is `unresolved` | `rfkit.thresholds`, `rfkit.budget`, decision 0007 | a tool printing PASS against a number nobody decided |
| S21 limits judged only on the state dependent difference, which the array state cannot absorb | `rfkit.compare.compare_states` | a constant offset, removed by any calibration, failing a comparison |
| No calibration claimed until standards exist | `rfkit.calibration` | raw data being consumed as corrected |
| Raw complex values preserved through to the array state | `rfkit.state` | a gauge choice destroying the measurement |
| Repeated measurements keep session, time and temperature | `rfkit.dataset` | statistics that flatten away what made them repeats |

## 3. The array state

`rfkit.state` turns per channel complex S21 into the state the inverse problem
infers, exactly as posed in `docs/mathematics/inverse-calibration.md`.

For Rev A the state is **diagonal**: one complex number per channel, giving
$2N-2$ identifiable real parameters after the unobservable common gain and
common phase are removed. The reference channel is explicit, and the raw complex
values are kept alongside the relative ones.

The **full coupling matrix is supported by the data structure** and is not the
default anywhere. `ArrayState.as_matrix()` embeds a diagonal state into the
matrix form, so code written for the extension works unchanged when a full state
arrives, and uncertainty I6 decides when that is needed.

## 4. Thresholds

Until 2026-09-25 every limit in `rfkit.thresholds` was empty and every verdict read
`unresolved`. **Decision 0007 now derives them** from what a discrepancy would do to
pointing, coherent gain and the error sidelobe floor, relative to what the three bit
quantisation of decision 0003 already costs, with one declared fraction $\eta = 0.10$.
The derivation is `rfkit.budget`, and `python -m rfkit.cli budget` prints it.

Thresholds are keyed by metric and by comparison class, because the uncertainty
sources differ:

| Metric | Design | HFSS against ADS | Simulation against analyser |
| --- | --- | --- | --- |
| S21 phase, state dependent part | | 2.29 deg, provisional | unresolved: needs the analyser uncertainty, EXP-004 O1 and O7 |
| S21 magnitude, state dependent part | | 0.40 dB, provisional | unresolved, same reason |
| S11 magnitude | | unresolved: no array level consequence in these units | unresolved |
| Amplitude imbalance across channels | 0.82 dB peak to peak, provisional | | |
| Phase spread across channels | **not a limit**: calibration removes it | | |

Three rules come with them. A plain difference between two traces is not judged
against the S21 limits, because part of it is common to every state and the array
state absorbs it; `compare_states` keeps only the state dependent part. A band the
traces do not both cover is `unresolved`, never extrapolated. And the values may change
only as decision 0007 section "How later data may, and may not, change these values"
allows, which was written before any data existed.

The coupling comparison of EXP-011 is **not** covered: the diagonal model the budget
rests on excludes coupling, and its acceptance belongs with gate G4. Since 2026-09-26
G4 has its own criterion, decision 0008, in `rfkit.coupling`: it ingests the antenna
board's `.s4p`, or assembles it from six two port measurements, and judges the
calibrated diagonal model against the coupled array on every steered beam.

## 5. Instrument control is deliberately outside

The workflow is analyser, then Touchstone file, then this package. No driver, no
session, no assumption about which analyser is on the bench, and a measurement
that is a file with a checksum.

`rfkit.instrument` holds the adapter boundary if automation is ever wanted. No
analysis module imports an instrument library, which is why all of them are
testable without hardware. Two things are recorded rather than assumed: no
native driver for the observed analyser has been identified, and the instrument
has never been connected to this computer, so its remote interface is unproven.

## 6. Deliberately future work

Recorded so the options are not rediscovered, and **none of these is a Rev A
requirement**: a TRL coupon on the board panel, IEEE P370 style de-embedding once
a fixture exists, time domain gating subject to EXP-004 observation O8, and
vector fitting if a rational model of a measured response is ever wanted.

## 7. Running it

```bash
python -m pip install -r requirements.txt
cd tools
python -m pytest rfkit/tests -q
python -m rfkit.cli example --out /tmp/rfkit-example
python -m rfkit.cli budget --json /tmp/budget.json --report /tmp/budget.txt
python -m rfkit.cli g4-chart
```

The example writes Touchstone files, a comparison report and an array state.
**Everything it produces is synthetic**, built from a formula in
`tools/rfkit/example.py`, and every trace carries `synthetic` in its provenance
so it cannot later be read as a measurement.
