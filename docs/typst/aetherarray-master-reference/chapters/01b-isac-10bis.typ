#import "../template.typ": *

== 10bis. Integrated sensing and communication (ISAC)

This section is numbered 10bis so that the numbering of everything after it is unchanged. It
teaches the concept once; Part VIII applies it to the learning track and Part IX to the contest.

=== 10bis.1 What ISAC means

*ISAC stands for integrated sensing and communication.* It names the family of radio systems in
which communication and sensing share resources that used to be separate: spectrum, waveform,
transmitter, antenna aperture, RF front end, processing, or simply the same electromagnetic field
\[#link(<ref-L32>)[L32]\]. Communication tries to deliver information from a transmitter to a receiver through the
propagation channel. Sensing tries to infer something about the propagation channel itself: where
reflectors are, whether something moved, whether a person is present. Both functions observe the
same field; they ask opposite questions of it. For communication the environment is a nuisance to
be equalised or rejected; for sensing it is the signal.

ISAC is therefore not "Wi-Fi used as radar". That is one example among several, and not the one
most of the literature is about.

=== 10bis.2 Three architectural families

#table(
  columns: (69pt, 4.9fr, 7.1fr, 4.1fr),
  table.header([Family], [What is shared], [Typical form], [AetherArray]),
  [*A. Joint waveform, joint transmitter*], [the transmitted waveform is designed for both data and sensing], [OFDM signals whose echoes are processed for range and Doppler while carrying data \[#link(<ref-L42>)[L42]\]; automotive and 6G joint waveform design \[#link(<ref-L32>)[L32]\]], [*not implemented*; Rev A has no transmitter of its own],
  [*B. Shared RF hardware and spatial aperture*], [the same antenna array, RF chain and spatial processing serve both functions], [an array that alternates or combines communication beams and sensing beams], [*yes, proposed*: one four element reconfigurable receiving array for both],
  [*C. Opportunistic, passive sensing*], [the field of an existing transmitter, whose waveform the sensing receiver did not design], [passive bistatic radar with broadcast or Wi-Fi illuminators \[#link(<ref-L33>)[L33], #link(<ref-L43>)[L43]\]; Wi-Fi sensing from channel measurements \[#link(<ref-L34>)[L34]\]], [*yes, proposed*: commercial Wi-Fi or Bluetooth sources as illuminators],
)

The proposed AetherArray demonstrator belongs to *B and C together*: a receive only array whose
aperture and RF chain are shared between communication oriented interference rejection and
opportunistic sensing, lit by transmitters it does not control. It does nothing in family A.

A reconfigurable array is valuable in family B for a simple reason: spatial selectivity helps both
functions. Communication wants gain towards the wanted source and nulls towards interferers;
sensing wants to look at the environment from several spatial viewpoints. An array that can be
switched between patterns on one clock edge serves both with the same hardware, and the same
calibration determines how good both are.

=== 10bis.3 Illuminators of opportunity

An *illuminator of opportunity* is a transmitter that exists for its own purpose, a Wi-Fi access
point, a Bluetooth beacon, a phone in hotspot mode, whose field a separate receiver exploits for
sensing. Nothing is transmitted for the sensing function.

#aa-figure(num: "20", caption: [an illuminator of opportunity. The array receives the direct path and every scattered
path; a person changes some of them.])[
```text
     COTS transmitter (Wi-Fi AP, BLE beacon, hotspot phone)
            |
            +-------- direct path ------------------------------\
            |                                                     \
            +--> person or object --> scattered / reflected path --> AetherArray (receive only)
            |                                                     /
            +--> walls, floor, furniture --> other multipath ----/
                       person in a path: shadowing; edges: diffraction; motion: time variation
```
]

The field at the array is a sum over propagation paths. For a narrowband signal at one frequency,
the complex signal at element $n$ is approximately

$ s_n ( t ) = sum_ell alpha_ell ( t ) thin e^(thin j n k d sin theta_ell ( t )) thin c ( t ) + nu_n ( t ) $

#table(
  columns: (auto, 4.0fr),
  table.header([Symbol], [Meaning]),
  [$ell$], [propagation path: direct, single reflection, multiple reflection, diffraction],
  [$alpha_ell ( t )$], [complex amplitude of path $ell$: path loss, reflection coefficient, delay phase],
  [$theta_ell ( t )$], [arrival direction of path $ell$],
  [$c ( t )$], [the transmitter's own signal, unknown and bursty for Wi-Fi or Bluetooth],
  [$nu_n ( t )$], [noise and other sources],
)

The physical mechanisms a person or an object changes:

#table(
  columns: (1.5fr, 5.7fr),
  table.header([Mechanism], [Effect on the paths]),
  [reflection and scattering], [adds a path or changes its amplitude and direction],
  [shadowing], [attenuates a path that crosses the body, often the direct path],
  [diffraction], [redistributes field around edges, including the body's],
  [multipath change], [changes the relative phases of paths, so their sum fluctuates],
  [motion], [makes $alpha_ell ( t )$ and $theta_ell ( t )$ vary in time; a moving reflector shifts phase by $2 pi$ per wavelength of path length change, 123 mm at 2.44 GHz],
)

The narrowband model ignores delay spread across a Wi-Fi channel's bandwidth; that is acceptable
for a power based receiver and is an approximation, stated as such.

#table(
  columns: (2.2fr, 8.6fr),
  table.header([Advantages], [Limitations, and what they imply for experiments]),
  [low cost: no transmitter to build], [the waveform is not controlled: power, timing and channel are the transmitter's; experiments must record them or use ratio features],
  [spectrum reuse: no extra emission], [traffic and power vary: a Wi-Fi AP's activity depends on its users; idle periods give few readings],
  [commercial compatibility, as the AP-S rules require], [synchronisation is limited: the receiver does not know when bursts arrive unless it decodes them],
  [receive only hardware], [multipath depends on geometry: results are specific to a room and a placement; the transmitter and array positions must be recorded and repeated],
  [educational clarity], [repeatability is hard: people near the setup, including the operator, change the field; EXP-005 Phase B measures exactly this],
  [], [sensing performance depends on where the transmitter is: a person who blocks no strong path is nearly invisible],
)

=== 10bis.4 One field, two problems

Write the combiner output for commanded state $vb(x)$ as $r ( t ) = vb(u)^(sf(T)) vb(s) ( t )$,
with realised weights $vb(u) = vb(H)_t thin vb(w) ( vb(x) )$: the nominal weights of the
state, passed through the array state of section 0.3. Its mean power is

$ P ( vb(x) , t ) = bb(E) lr([ abs(r ( t ))^2 ]) = vb(u)^(sf(T)) thin vb(R) ( t ) thin vb(u)^(*) , wide vb(R) ( t ) = bb(E) lr([ vb(s) ( t ) thin vb(s) ( t )^(sf(H)) ]) $

#table(
  columns: (auto, 4.7fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$vb(s) ( t )$], [element signals, the field sampled by the four antennas], [$sqrt("W")$, complex],
  [$vb(R) ( t )$], [spatial covariance of the received field: $4 times 4$, Hermitian; it is set by the sources and the environment], [W],
  [$vb(u)$], [realised complex weights of the commanded state], [dimensionless],
)

The expectation is over the transmitter's signal and the noise, over an averaging time short
compared with environmental change.

*Communication* asks which state best serves a wanted transmitter against an interferer. With
both sources present, $vb(R) = vb(R)_D + vb(R)_I + vb(R)_nu$, and the desired and
interfering powers are $P_D ( vb(x) ) = vb(u)^(sf(T)) vb(R)_D vb(u)^(*)$ and
$P_I ( vb(x) ) = vb(u)^(sf(T)) vb(R)_I vb(u)^(*)$. In free space with one path each,
these reduce to the $P_D$ and $P_I$ of section 9.2; indoors each source contributes several paths,
and a null placed on an interferer's direct path does not null its reflections. The objective
$J ( vb(x) ) = P_D ( vb(x) ) - lambda P_I ( vb(x) )$, or a signal to interference ratio, is
meaningful only when the receiver can separate the two powers, by channel, time or transmitter
identity (section 47). Beam steering, interference suppression and null placement are then a choice
among the reachable states, $8^(N - 1) = 512$ relative configurations, or 820 with the enable bits, and
the choice is an exact enumeration against the estimated array state (section 8.3). *ISAC creates no
reason to use machine learning for beam synthesis*; section 38 explains why once, and nothing in this
section changes it.

*Sensing* asks whether, and how, the environment changed. Cycling through $K$ receive states gives a
vector

$ vb(p) ( t ) = lr([ P ( vb(x)_1 \, t ) \, dots.h \, P ( vb(x)_K \, t ) ])^(sf(T)) , wide P ( vb(x)_k , t ) = vb(u)_k^(sf(T)) thin vb(R) ( t ) thin vb(u)_k^(*) $

Each pattern weights the paths differently: a beam towards the door sees a reflection from the door
strongly, a pattern with a null towards the transmitter suppresses the direct path and leaves the
scattered field visible. A person who adds, removes or moves a path changes $vb(R) ( t )$, and the
change appears in the components of $vb(p)$ whose patterns look that way.

*Why several patterns carry more information than one received signal strength.* Each power is a
linear function of the entries of $vb(R) ( t )$, because $vb(u)^(sf(T)) vb(R) vb(u)^(*) = sum_(m , n) u_m R_(m n) u_n^(*)$. A Hermitian $4 times 4$ matrix has 16 real parameters. A single
omnidirectional element measures one of them, a diagonal entry: the total power, which says almost
nothing about where the field comes from. $K$ well chosen patterns measure up to 16 independent
combinations, including the cross terms $R_(m n)$ that hold the relative phases between elements and
therefore the arrival directions. The pattern diverse power vector is a sketch of the spatial
covariance obtained without coherent receivers per channel. This is a statement about what can in
principle be observed; which patterns are informative in a given room, and whether 16 are needed, is
an experimental question.

=== 10bis.5 The calibration problem both functions share

The measurement does not depend on the environment alone. In the notation of this document,

$ y_t = G lr(( cal(E)_t \, vb(H)_t \, vb(x)_t )) + epsilon.alt_t $

where $cal(E)_t$ is the state of the environment and the sources, $vb(H)_t$ the array state,
$vb(x)_t$ the commanded state and $epsilon.alt_t$ the measurement noise. For power readings, section
10bis.4 makes $G$ explicit, and with the diagonal array state of Rev A something sharper follows.
Substituting $vb(u)_k = vb(H)_t vb(w)_k$:

$ P ( vb(x)_k , t ) = vb(w)_k^(sf(T)) thin tilde(vb(R)) ( t ) thin vb(w)_k^(*) , wide tilde(vb(R)) ( t ) = vb(H)_t thin vb(R) ( t ) thin vb(H)_t^(sf(H)) , wide tilde(R)_(m n) = h_m ( t ) thin R_(m n) ( t ) thin h_n^(*) ( t ) $

*The measurements depend on the environment and on the hardware only through their product
$tilde(vb(R))$.* A phase drift $delta phi.alt_m$ on channel $m$ rotates every cross term
$tilde(R)_(m n)$ by $delta phi.alt_m$, which is exactly what a change of arrival direction does. A gain
drift on channel $m$ scales its row and column, which is what a change in a path's strength does. From
the sensing data alone, hardware drift and environmental change are not separable:

#caveat[
*A measured change is not necessarily an environmental change.*
]

#table(
  columns: (1.8fr, 5.2fr),
  table.header([Source of a change in $vb(p) ( t )$], [Examples]),
  [environment, the signal], [a person enters, an object moves, a reflector shifts, shadowing or multipath changes],
  [hardware, the confound], [amplitude drift, phase drift, temperature, switch path variation, detector and acquisition drift],
)

The two can be told apart only with information from outside the sensing data: an independent
measurement of $vb(H)_t$ (a calibration), or prior knowledge of how each evolves. Their time
scales help: people move in seconds, thermal drift takes minutes to hours. They do not settle it, since
a moved piece of furniture is a slow environmental change. First order, the confound is visible in the
differential of the same expression:

$ delta P_k approx underbrace(vb(u)_k^(sf(T)) thin delta vb(R) thin vb(u)_k^(*), "environment") thick + thick underbrace(2 thin op("Re") lr(\{ lr(( delta vb(H)_t vb(w)_k ))^(sf(T)) vb(R) thin vb(u)_k^(*) \}), "hardware") $

Both terms land in the same $K$ numbers.

The consequence for each function:

```text
 COMM :  H_t drifts --> realised weights wrong --> beam off, null filled --> desired / interferer
                                                                               discrimination worse
 SENSE:  H_t drifts --> spatial signature p(t) changes --> a change detector reports an event
                                                           that is hardware drift, not the room
```

This is the bridge between the three threads of the project. Calibration research estimates
$vb(H)_t$. The learning track tries to estimate it with fewer new measurements by using its
history. ISAC is where an error in $vb(H)_t$ becomes a wrong communication beam and a false
sensing event.

*A consequence for calibration in a room.* An over the air calibration against an ambient source
estimates, per channel, the product of the hardware term and the incident field at that element,
$h_n s_n$, not $h_n$ alone. In free space with a single path from a known direction, the field term is
known and can be divided out; indoors it contains multipath that the calibration absorbs, and that
changes when the room changes. A calibration done that way is a channel calibration, useful for the
communication mode in that room, but it is not the hardware state the drift prior is about. Hardware
labels for the learning track therefore come from the conducted route or a controlled probe
(sections 11.3 and 16), and any calibration done at a demonstration has to say which of the two it is.

=== 10bis.6 Where the learning contribution sits

Part VIII defines the method; this paragraph only places it. The diagonal state
$vb(H)_t = op("diag") ( h_i ( t ) )$ with $h_i ( t ) = g_i ( t ) thin e^(thin j thin delta phi.alt_i ( t ))$ is
unchanged, and so is the Bayesian structure:

$ p lr(( vb(H)_t divides y \, vb(x) \, cal(D) )) thick prop thick p lr(( y divides vb(H)_t \, vb(x) )) thin p_theta lr(( vb(H)_t divides cal(D) )) $

with the learned temporal prior $p_theta$, the physical likelihood $p ( y divides vb(H)_t , vb(x) )$,
and the posterior as the corrected estimate after sparse new measurements. Its purpose in an ISAC
system is not "learning produces a beam command". It is:

```text
 drift history --> better prior on H_t now --> fewer new calibration measurements
               --> calibrated spatial response restored sooner --> COMM and SENSE more reliable
```

$M_"required"$, the number of new physical measurements needed to recover a target (section
0.2), has two system level forms here. *Communication:* at equal recovered desired to interferer
performance, $M_"sparse" < M_"full"$ would support the research claim. *Sensing:* at
equal stability or detection performance, the same inequality could support it too, but only once the
sensing metric is defined before the experiment, for example the false alarm rate of a change detector
during periods with no environmental change. No such result exists.

=== 10bis.7 Why this is ISAC, and in what narrow sense

The proposed system is, precisely:

#caveat[
*a reconfigurable receiving array sharing the same spatial RF aperture and hardware between
communication oriented interference rejection and opportunistic environmental sensing.*
]

The two functions share the antenna array, the phase reconfigurable RF chain, the calibration, the
measurement infrastructure, the deterministic control and the spatial patterns. The illuminator stays
external and commercial. That is a legitimate member of families B and C, and a deliberately narrow
one. AetherArray is *not* a 5G or 6G ISAC base station, not a joint waveform design system, not a
monostatic radar, not a range and Doppler radar (a power detector measures neither delay nor
frequency shift), and not a centimetre level localisation system. Calling it any of those would be
semantic inflation.

#aa-figure(num: "19", caption: [the signature figure. One RF aperture, two ISAC functions, one calibration layer beneath
both, and the learned prior as a way to restore that layer with fewer new measurements.])[
#image("../figures/mermaid/figure-19.svg", width: 100%)
]

=== 10bis.8 ISAC claims and their evidence

#table(
  columns: (3.5fr, 60pt, 60pt, 4.1fr, 6.2fr),
  table.header([Claim], [Type], [Current status], [Evidence today], [What would establish it]),
  [the array can steer a receive response], [theoretical, simulation], [*analytical only*], [array factor, sections 7 and 8; no simulation of the real geometry, no hardware], [an HFSS model of the array (EXP-011, SIM-008) and a measured pattern change between states (EXP-007 to EXP-009)],
  [the array can suppress an interferer while keeping the wanted link], [system level], [*not established*], [the ideal theory of section 9; the N = 4 feasibility gate is not written or run], [the gate (section 50), then a physical desired and interferer experiment with a source separating receiver],
  [pattern diverse power vectors contain sensing information], [plausible, literature supported in other forms], [*not demonstrated on AetherArray*], [the observability argument of 10bis.4; Wi-Fi sensing literature with different receivers \[#link(<ref-L34>)[L34]\]], [a repeated, controlled sensing experiment with a pre-registered task and error rate],
  [hardware drift degrades sensing stability], [physical hypothesis], [*unmeasured*], [the confound $tilde(vb(R)) = vb(H) vb(R) vb(H)^(sf(H))$ of 10bis.5; no drift has been measured], [repeated sensing with a static room, calibrated against uncalibrated, over a drift period],
  [drift degrades null depth], [physical hypothesis, analytical], [*unmeasured*], [$sigma^2 \/ N$, section 9.4], [a measured null over time, with temperature logged],
  [a learned prior reduces new recalibration measurements], [research hypothesis], [*unproven; gated by G2*], [none; nothing built], [a held out temporal experiment against baselines A to D, section 42],
  [the system qualifies as ISAC in families B and C], [definitional], [*true by design, narrow*], [10bis.7], [not an empirical claim; it holds if both modes run on the shared aperture],
)
