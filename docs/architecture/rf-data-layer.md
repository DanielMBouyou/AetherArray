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
| **No invented thresholds.** A limit cites its document or every verdict is `unresolved` | `rfkit.thresholds` | a tool printing PASS against a number nobody decided |
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

## 4. Thresholds, and a gap this made visible

The comparison tool applies limits from `rfkit.thresholds`, and **every one of
them is currently empty**, so every verdict reads `unresolved`. That is not a
placeholder to be filled in quietly: it is a real gap the tool surfaces.

| Threshold needed | Currently |
| --- | --- |
| Agreement in S21 magnitude between solver, simulator and analyser | no value recorded anywhere |
| Agreement in S21 phase | no value recorded anywhere |
| Agreement in S11 magnitude | no value recorded anywhere |
| Acceptable amplitude imbalance across channels | measured quantity in the benchmark contract, no limit set |
| Acceptable phase spread across channels | no limit set |

EXP-011 plans to compare simulated coupling against measured coupling and fixes
no acceptance limit for that comparison. **Setting these belongs in a decision
record or in the benchmark specification, not in a tool.**

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
```

The example writes Touchstone files, a comparison report and an array state.
**Everything it produces is synthetic**, built from a formula in
`tools/rfkit/example.py`, and every trace carries `synthetic` in its provenance
so it cannot later be read as a measurement.
