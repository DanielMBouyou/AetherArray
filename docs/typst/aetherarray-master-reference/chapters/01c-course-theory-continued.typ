#import "../template.typ": *

== 11\. Calibration

=== 11.1 What calibration means here

The controller commands channel $i$ with a nominal complex weight $x_i$, set by the enable bit
and the three phase bits. The hardware applies something else:

$ x_i thick arrow.r.long thick h_i thin x_i , wide h_i = g_i thin e^(thin j thin delta phi.alt_i) , wide vb(H)_t = op("diag") ( h_1 , dots.h , h_N ) $

#table(
  columns: (auto, 3.3fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$x_i$], [nominal weight: $e_i e^(j phi.alt_i)$, enable bit $e_i$ times the nominal state phase], [dimensionless],
  [$h_i$], [complex error of channel $i$], [dimensionless],
  [$g_i$], [gain error of channel $i$, realised amplitude relative to nominal], [dimensionless],
  [$delta phi.alt_i$], [phase error of channel $i$], [rad],
  [$vb(H)_t$], [the diagonal array state at time $t$], [],
)

Calibration estimates $vb(H)_t$ and uses it. With phase only control, the correction
cannot be $vb(H)^(- 1) vb(x)$ as in a textbook; it is the selection, among the
reachable states, of the one whose realised weights $hat(vb(H))_t vb(x)$ best serve
the criterion. Gain errors are estimated and not corrected (decision 0003, section 4).

=== 11.2 Kinds of error

#table(
  columns: (3.4fr, 6.2fr, 3.6fr),
  table.header([Error], [Example], [Absorbed by a diagonal state?]),
  [common gain and phase, the same on every channel and every state], [probe antenna gain, cable to the analyser, distance], [yes, and unobservable anyway: it does not change the beam shape],
  [per channel, independent of the commanded state], [different jumper lengths, connector differences, switch to switch insertion loss variation], [*yes*: this is exactly what one complex number per channel holds],
  [per channel, dependent on the commanded state], [a 45 degree bit that is really 47 degrees; a long state lossier than a short one; reflections between discontinuities that change with the selected arm], [*no*],
  [common to all channels, proportional to the state phase], [a permittivity error or a frequency offset scaling every line length by the same fraction], [*no*: it depends on the state, so it steers the beam (decision 0007)],
  [coupling between channels], [section 10], [only if it does not depend on the state],
)

*Why state dependent errors are the dangerous ones.* A state independent error is a constant
per channel; one calibration measures it and every beam benefits. A state dependent error is
different for each of the eight states of each channel, so it reaches every calibrated beam
differently, and the diagonal model cannot represent it. It can only be bounded by design, which
is why decision 0007 derives a requirement on the hardware's own state dependent phase error,
2.29 degrees at $f_0$, and an amplitude imbalance allowance of 0.82 dB peak to peak, or modelled
explicitly per state, at the cost of 32 complex unknowns instead of 4.

=== 11.3 What a full calibration is

A *full calibration* estimates all identifiable parameters of the chosen model from scratch,
without using any previous estimate. On Rev A it can be done two ways.

#table(
  columns: (43pt, 6.3fr, 1.9fr, 3.9fr),
  table.header([Route], [Procedure], [Measurements], [Needs]),
  [complex, per channel], [enable one channel, terminate the other three, measure $S_21$ from the common port, repeat for each channel], [$N = 4$ complex readings], [the analyser; per channel isolation, which Rev A provides electronically],
  [power only, REV], [for each channel, step its phase through at least three states while the others stay fixed, and read the total power], [$3 N = 12$ power readings at the minimum], [a power reading at the sum port and one fixed probe (section 11.5)],
)

The complex route is the "expensive label" of the learning track: it gives every channel's
complex transfer directly, and Rev A obtains it without touching a cable
(`docs/architecture/rev-a-rf-architecture.md` section 5.3).

=== 11.4 Identifiability: what can be known at all

Of the $2 N$ real numbers in $vb(H)_t$, two cannot be determined from the array output. A
common phase rotation of every $h_i$ is confounded with the phase of the probe path, and a
common scaling of every $g_i$ is confounded with the gain of the probe path, the probe antenna,
the distance and the cables, which are not known to the required precision. Neither changes the
beam shape. With one channel taken as reference, the identifiable set is

$ d = 2 N - 2 $

real parameters, $N - 1$ relative gains and $N - 1$ relative phases: *six at $N = 4$*. Since a
scalar reading provides one real number, six readings is the absolute floor for any method
that starts with no information about the state, whatever the algorithm.

=== 11.5 Why power only measurement is harder

A power reading is quadratic in the unknowns:

$ y_k = lr(| sum_(n = 1)^N w_n ( vb(x)_k ) thin h_n |)^2 + epsilon.alt_k $

so recovering $vb(h)$ means recovering a complex vector from magnitudes alone, up to a
global phase: *phase retrieval*. The classical rotating element field vector method (REV) of
Mano and Katagi \[#link(<ref-A6>)[A6]\] sidesteps it channel by channel. Stepping the phase $phi$ of channel
$n$ while the others, summing to $S$, stay fixed gives

$ P ( phi ) = abs(S)^2 + abs(y_n)^2 + 2 thin abs(S) thin abs(y_n) cos lr(( psi_n + phi - arg S )) $

a sinusoid with three unknowns, hence at least three phase states per channel and $3 N$
readings in total (`docs/mathematics/formulation.md` section 6; \[#link(<ref-A20>)[A20]\] for the count). Note a
direct consequence of the formula: the offset and the amplitude of the sinusoid are symmetric
in $abs(S)$ and $abs(y_n)$, so the two magnitudes can be swapped without
changing $P ( phi )$. The method needs a further assumption, such as $abs(y_n) < abs(S)$, or a further measurement, to choose between them.

*What the phase retrieval literature actually establishes.* This point needs care, because the
repository states it more strongly than the literature supports.

#table(
  columns: (3.6fr, 3.9fr, 1.8fr),
  table.header([Result], [Status], [Source]),
  [$4 N - 4$ generic intensity measurements suffice to determine any vector in $bb(C)^N$ up to global phase], [proved: a sufficient count for generic measurement vectors], [Conca, Edidin, Hering, Vinzant 2015 \[#link(<ref-A12>)[A12]\]],
  [$4 N - 4$ is also necessary], [proved only for dimensions $N = 2^k + 1$; conjectured in general], [\[#link(<ref-A12>)[A12]\]; \[#link(<ref-L3>)[L3]\]],
  [at $N = 4$, eleven measurements can be injective], [an explicit frame of 11 vectors in $bb(C)^4$ with a certificate], [Vinzant 2015 \[#link(<ref-L4>)[L4]\]],
  [lower bound at $N = 4$], [10 or 11 from a general bound; a 2026 preprint claims exactly 11], [\[#link(<ref-L5>)[L5]\]; \[#link(<ref-L6>)[L6]\], unreviewed],
)

All four are verified at index level only (Part XV). Three corrections follow for the
repository's argument, which `docs/architecture/ml-calibration.md` section 3 and decision 0002
state as "recovering a complex vector from intensity measurements alone generically requires at
least $4 N - 4$":

1. $4 N - 4$ is a *sufficient* count for generic vectors, not a proven lower bound at $N = 4$,
   where 11 can suffice.
2. These results concern *generic* measurement vectors. The Rev A probe vectors are
   structured, unit modulus and restricted to 45 degree phases; whether a given set of them is
   injective has to be checked for that set. Uncertainty I16 already records this as open.
3. Injectivity is uniqueness for *every* possible state. A method that uses prior information,
   for example that the errors are small, or that one magnitude exceeds another, can need fewer
   readings. REV itself relies on such an assumption, and the fast amplitude only method of Long
   and co-authors reports about $2 N$ readings with three phase states \[#link(<ref-L7>)[L7]\], although an
   experimental comparison found it less accurate than REV \[#link(<ref-A22>)[A22]\].

=== 11.6 What remains of the "no headroom" argument

#table(
  columns: (2.5fr, 1.2fr, 2.4fr),
  table.header([Count at $N = 4$], [Readings], [Nature]),
  [identifiable parameters, the absolute floor], [6], [necessary for any method starting from nothing],
  [complex route, one channel at a time], [4 complex, 8 real numbers], [what the analyser path needs],
  [fast amplitude only method \[#link(<ref-L7>)[L7]\]], [about 8, to verify], [structured, with prior assumptions],
  [generic injective power only set], [11 to 12], [uniqueness for every state],
  [REV at its minimum of three states], [12], [structured, with one assumption],
)

The honest conclusion is narrower than the repository's wording and survives intact in
substance. On first calibration at $N = 4$, the best classical routes already sit within a few
readings of the floor of six, and going below the injective count requires prior information
about the state. A learned first calibration estimator trained on simulated arrays is a way of
supplying population prior information; at this scale it has little room to save
measurements, its labels exist only in simulation, and any saving it showed would be hard to
separate from the choice of baseline. *So $N = 4$ provides no honest argument that machine
learning reduces first calibration measurement counts, and the project does not make that
claim.* The prior information worth using is the array's own history, which exists only for
recalibration. That is decision 0002, and this document recommends restating its counting
argument in these terms (Appendix J).

The complex route strengthens the conclusion: since gate G1 passed (decision 0004), the analyser
can measure each channel's complex transfer in $N$ readings, which is already close to the
floor. Decision 0002's second reopening condition, "if EXP-004 finds that phase can be measured
directly, ... the comparison in section 3 of the architecture document is redone", was
triggered by that result; decision 0004 records that decision 0002 does not reopen, which is
correct in substance, but the comparison itself has not been redone in writing.

== 12\. Drift

=== 12.1 What drift is

An array calibrated at time $t$ is described by $vb(H)_t$. Later it is described by a
different state:

$ vb(H)_(t + Delta t) eq.not vb(H)_t $

The calibration made at $t$ then describes hardware that no longer exists. How long a
calibration stays valid, the question of EXP-010, is unmeasured in this project and, by the
repository's reading of the literature, rarely measured outside climate chambers
(`research/state-of-the-art.md` section 4).

=== 12.2 Possible sources, and what is known about each

None of the sources below has been measured on AetherArray, because no AetherArray hardware
exists. The table classifies each by the evidence for its relevance here.

#table(
  columns: (1.8fr, 4.4fr, 6.4fr),
  table.header([Source], [Mechanism], [Classification]),
  [temperature of the beamformer board], [permittivity, copper dimensions and switch characteristics change with temperature], [*plausible*; no temperature coefficient for the selected laminate is recorded],
  [temperature of the detector], [the AD8318 output drifts with temperature, $plus.minus 0.5$ dB over its full range \[#link(<ref-V6>)[V6]\]], [*documented by the vendor* as a range figure; no per degree slope is given, so the slope near room temperature is *unresolved* (I13)],
  [switch state repeatability], [a switch returning to a state may not return to exactly the same transfer], [*unresolved* and important: if not below the measurement floor, the drift experiment measures the switches (decision 0003; E6)],
  [connector and cable movement], [mating a connector or flexing a cable changes phase], [*plausible*, and modelled as a *jump*, not drift: every session records a connector handling flag (I14)],
  [supply variation], [switch and detector behaviour with supply voltage], [*plausible*],
  [analyser drift after calibration], [the instrument's own error terms move with time and temperature], [*plausible*; uncertainty not yet characterised (O1, O7)],
  [ageing], [slow material and contact changes], [*plausible*, on time scales beyond the planned experiments],
  [environment], [people and objects near a radiated measurement], [*not hardware drift*, but it changes radiated readings and can be mistaken for drift; EXP-005 Phase B measures it],
)

One mechanism deserves emphasis because it connects drift to the limits of the diagonal model.
If the board's permittivity changes uniformly with temperature, every switched length changes
phase in proportion to its electrical length. That is a common proportional error: it depends
on the commanded state, so a diagonal state cannot absorb it and it steers the beam (decision
0007). Temperature drift may therefore be partly state dependent. Whether it is large enough to
matter is unknown *\[to verify\]*; the board temperature sensor of requirement R4, beside the
phase network, is what will make it visible.

=== 12.3 What drift does

#table(
  columns: (1.2fr, 3.5fr, 4.6fr),
  table.header([Affected quantity], [How drift enters], [Sensitivity]),
  [beam pointing], [the component of the phase drift that is linear in element index], [about 0.14 degrees of pointing per degree of independent phase error at broadside (from section 8.2)],
  [gain], [the variance of the phase and amplitude drift], [small: 0.1 dB for 10 degrees rms],
  [null depth], [the variance of the drift, section 9.4], [large: a few degrees of drift move a null by several dB],
  [sensing features], [any change of the receive patterns used as features], [a hardware change looks like an environmental one (section 48)],
)

#aa-figure(num: "9", caption: [conceptual drift of one channel's relative phase after a calibration. Not data; no
drift has been measured.])[
```text
 state H_t                      calibration valid           calibration stale
 (one channel, relative phase)
     ^
     |                            .-~~-.                      .~~~~~.
     |   cal    .--~~--.      .-~        ~-._      _.-~~-.-~~        ~~-.
     |----*---~         ~~--~                ~~~~~                      ~~--   true state
     |    |<---- |error| small ---->|<------- |error| grows ------------>|
     |  t_cal                     recalibrate?                         recalibrate
     +-----------------------------------------------------------------------> time
```
]

Gate G2 asks whether drift over a few hours is larger than the measurement's own repeatability.
If it is not, there is nothing for a drift prior to learn, the learning track is abandoned, and
decision 0002 is superseded rather than reinterpreted (decision 0002, conditions for reopening).
