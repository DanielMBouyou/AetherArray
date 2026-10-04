#import "../template.typ": *

= Part II. The engineering problem <part-ii-the-engineering-problem>

=== II.1 From one array to many channels

Phased arrays are used in radar, satellite terminals, cellular base stations and test systems,
and the larger ones have hundreds or thousands of channels. Every channel carries its own gain
error, its own phase error, its own temperature dependence and its own share of manufacturing
variation, and the elements couple to their neighbours. The array only does what its designer
intended once those errors have been measured and compensated: once it has been calibrated.

Calibration costs something every time it is done:

#table(
  columns: (1.5fr, 4.7fr),
  table.header([Cost], [Why]),
  [measurement time], [each state must be applied, settled and read, with enough integration to beat the noise],
  [RF hardware], [probes, couplers, reference channels, switching for calibration paths],
  [downtime], [an array being calibrated is usually not doing its job],
  [test complexity], [positioners, chambers, fixtures, procedures, operators],
  [energy], [transmitting calibration signals, running instruments],
  [computation], [small compared with the rest; the measurements dominate (`benchmarks/metrics.md`)],
)

A first calibration, done once at the factory or in a chamber, may be expensive and still
acceptable. Repeated recalibration in the field is different: its cost recurs for the life of
the array, and the array drifts in between.

=== II.2 Recalibration has structure

The array state does not jump arbitrarily from one calibration to the next. Between $t - 1$ and
$t$, the same switches, lines and connectors are present, at a temperature that has changed by
a few degrees, after a time that is known. Much of the change is plausibly smooth, correlated
across channels, and related to measurable covariates such as temperature and elapsed time.
That is the hypothesis that makes a learned prior worth testing:

$ p_theta lr(( vb(H)_t divides vb(H)_(t - 1) \, vb(H)_(t - 2) \, dots.h \, T_t \, Delta t )) quad "instead of" quad p lr(( vb(H)_t )) " uninformative" $

#table(
  columns: (auto, 3.4fr),
  table.header([Symbol], [Meaning]),
  [$p_theta$], [a probability model with parameters $theta$ learned from the array's own history],
  [$vb(H)_(t - 1) , vb(H)_(t - 2) , dots.h$], [earlier calibrated states],
  [$T_t$], [temperatures logged with the session],
  [$Delta t$], [time elapsed since the last calibration],
)

If the hypothesis holds, a recalibration starts from a good guess with a known uncertainty, and
only the dimensions that the history cannot predict have to be measured afresh.

#aa-figure(num: "8", caption: [the calibration model. The commanded word becomes nominal weights; the array state
turns them into realised weights; measurements of the realised weights, with the history, give
an estimate of the state, from which the best reachable command is selected.])[
#image("../figures/mermaid/figure-08.svg", width: 100%)
]

=== II.3 Initial calibration and recalibration are different problems

#table(
  columns: (1.8fr, 4.0fr, 4.3fr),
  table.header([], [Initial calibration], [Recalibration]),
  [prior information about $vb(H)_t$], [none beyond the physical model and population statistics], [the previous calibration, the elapsed time, the temperature history],
  [minimum new readings], [at least $2 N - 2$ for any method; several more for power only uniqueness (section 11.6)], [can be fewer than $2 N - 2$ for a target accuracy, if the prior pins most dimensions],
  [where learning could help], [little room at $N = 4$; labels only in simulation], [the subject of the project: labels from hardware, attributable savings],
  [repository specification], [ML-A, EXP-013, a *control*], [ML-B, EXP-015, the *central claim*],
)

AetherArray's machine learning claim applies to the second column. The first column is kept as
a control that shows the learning machinery works at all (decision 0002, point 2).

== 13\. Why this matters at scale, and why a four element array can still be useful

=== 13.1 What a four element array offers

#table(
  columns: (1.5fr, 5.3fr),
  table.header([Property], [Why it matters for this research]),
  [real RF hardware], [the drift, tolerances, connectors and switch nonidealities are physical, not modelled],
  [a known number of channels], [identifiability and counts are exact and small],
  [repeatable state control], [every beam state is an exact 16 bit code word applied on one clock edge],
  [observable drift], [temperature is logged beside the phase network and the detector],
  [ground truth], [the analyser measures each channel's complex transfer, electronically isolated, with no cable handling],
  [cheap experiments], [a few tens of euro of parts; unattended runs],
  [complete enumeration], [512 relative states: every beam can be evaluated exactly],
)

=== 13.2 What it does not offer

#caveat[
*A physical validation at $N = 4$ is not a proof of behaviour at $N = 128$.*
]

A four element array cannot show how coupling behaves between the centre and the edge of a
large aperture, how thermal gradients across a large board correlate channel errors, how an
active transmit and receive module with amplifiers drifts, or how measurement counts behave
when the identifiable dimension is 254 instead of 6.

=== 13.3 The intended scaling study

The scaling study is *\[proposed here\]*; the repository does not contain it. Its logic would be:

1. measure on Rev A the statistics that a simulator needs and cannot invent: phase drift and
   amplitude drift distributions, their temporal correlation, their dependence on temperature,
   the measurement noise, and the coupling structure from EXP-011;
2. parameterise an array simulator with those distributions, labelled as measured on four
   channels;
3. simulate recalibration with and without a learned prior at $N = 4 , 8 , 16 , 32 , 64 , 128$, with
   the same baselines as on hardware;
4. check the $N = 4$ simulation against the $N = 4$ hardware result before believing the
   larger ones.

How the counts scale with $N$, for a diagonal state, *\[analytical\]*:

#table(
  columns: (auto, 1.8fr, 1.1fr, 1.1fr, 1.5fr),
  table.header([$N$], [identifiable parameters $2 N - 2$], [complex route, one channel at a time], [REV minimum $3 N$], [generic injective power only count $4 N - 4$, sufficient]),
  [4], [6], [4], [12], [12 (11 known to suffice)],
  [8], [14], [8], [24], [28],
  [16], [30], [16], [48], [60],
  [32], [62], [32], [96], [124],
  [64], [126], [64], [192], [252],
  [128], [254], [128], [384], [508],
)

For $N > 4$, REV needs fewer readings than the generic sufficient count $4 N - 4$, and at large $N$
it falls below any injective count, since known lower bounds grow as about $4 N$ \[#link(<ref-L5>)[L5]\]. That is
possible only because REV relies on structure and on prior assumptions (section 11.5). The room for prior
information grows with $N$, which is why the repository expects adaptive methods to gain more at
larger $N$ (`docs/architecture/ml-calibration.md` section 5, M4).

#aa-figure(num: "18", caption: [four physical channels and a simulated scaling study. The simulated part is a
proposal; EXP-001, the array simulator it needs, has not been built.])[
#image("../figures/mermaid/figure-18.svg", width: 100%)
]

*Limits of the extrapolation, stated in advance.*

- Large arrays use different hardware: integrated beamformer chips, active modules with
  amplifiers, digital or hybrid architectures. Their drift mechanisms differ from those of a
  passive switched line board.
- Thermal and coupling topology change with size: gradients, edge effects and correlated errors
  across subarrays have no analogue at four elements.
- Full wave simulation does not scale with the study. HFSS Student is limited to 64 000 volume
  mesh elements \[#link(<ref-V23>)[V23]\], and even the full licence cannot model a 128 channel array repeatedly; a
  scaling study would use idealised coupling models, such as the Toeplitz model already in
  `rfkit.coupling`, or periodic unit cell analysis, and say so.
- Measured statistics from one board are a sample of one board.
