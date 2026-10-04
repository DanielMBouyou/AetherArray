#import "../template.typ": *

= Part I. Course and theory refresher <part-i-course-and-theory-refresher>

This part builds, from the beginning, every idea the rest of the document uses. Each section
follows the same pattern: the physical intuition, the mathematics, what it means for
AetherArray, how it will be simulated or measured, and what is known today. A reader who
already knows microwave engineering can skip to section 7; a reader who knows phased arrays
can skip to section 11.

== 1\. Electromagnetic waves

=== 1.1 Intuition

A radio wave is a travelling disturbance of two linked fields. The *electric field*
$vb(E)$, in volts per metre, pushes on charges; the *magnetic field* $vb(H)$, in
amperes per metre, is produced by moving charges and pushes on them in turn. A changing
$vb(E)$ produces $vb(H)$ and a changing $vb(H)$ produces $vb(E)$, which is why
the pair can sustain itself away from any source. Far from the antenna that launched it, the
wave is locally plane: $vb(E)$, $vb(H)$ and the direction of travel are mutually
perpendicular, and the direction of travel is given by the *propagation vector*
$vb(k)$, whose magnitude is the wavenumber.

=== 1.2 Frequency, wavelength, phase velocity

At a fixed point the field oscillates at the *frequency* $f$, in hertz. At a fixed instant
it repeats in space every *wavelength* $lambda$, in metres. The pattern moves at the
*phase velocity* $v_p$, so that one wavelength passes in one period:

$ lambda = frac(v_p, f) , wide v_p = frac(c, sqrt(epsilon_r mu_r)) , wide lambda_0 = frac(c, f) " in vacuum" $

#table(
  columns: (auto, 4.1fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$c$], [speed of light in vacuum, 299 792 458 m/s exactly], [m/s],
  [$epsilon_r$, $mu_r$], [relative permittivity and permeability of a uniform medium; $mu_r = 1$ for every material in this project], [dimensionless],
  [$lambda_0$], [free space wavelength], [m],
)

At the AetherArray working frequency, $f_0 = 2.44$ GHz (decision 0004):

$ lambda_0 = frac(299 thin 792 thin 458 space "m/s", 2.44 times 10^9 space "Hz") = 0.1229 space "m" = 122.9 space "mm" $

This is exact to the figures shown. Half of it, 61.4 mm, is the element spacing of the antenna
board, so the four element array is about 184 mm across its element centres.

In a uniform dielectric the wave is slower and the wavelength shorter by $sqrt(epsilon_r)$.
On a printed circuit board the wave travels partly in the board and partly in air (section 5),
so the relevant figure is the *guided wavelength* $lambda_g = lambda_0 \/ sqrt(epsilon_"eff")$,
with an effective permittivity between 1 and $epsilon_r$. Confusing $lambda_0$ with
$lambda_g$ is the classic error in switched line design: on the selected beamformer board the
analytical estimate is $lambda_g approx 68.8$ mm, barely more than half of $lambda_0$.

=== 1.3 Free space impedance

In a plane wave the ratio of the electric to the magnetic field strength is fixed by the
medium. In vacuum:

$ eta_0 = frac(abs(vb(E)), abs(vb(H))) = sqrt(frac(mu_0, epsilon_0)) approx 376.7 space Omega $

$mu_0$ and $epsilon_0$ are the permeability and permittivity of vacuum, in H/m and F/m.
$eta_0$ reappears in antenna formulas and in the closed form microstrip impedance of section 5.

=== 1.4 Phasors, and why complex numbers are used everywhere

A field oscillating at one frequency is completely described by two numbers: its amplitude and
its phase. Writing it as the real part of a rotating complex number,

$ E ( z , t ) = E_0 cos ( omega t - beta z + phi_0 ) = op("Re") lr(\{ underline(E) ( z ) thin e^(thin j omega t) \}) , wide underline(E) ( z ) = E_0 thin e^(thin j ( phi_0 - beta z )) $

#table(
  columns: (auto, 3.2fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$omega = 2 pi f$], [angular frequency], [rad/s],
  [$beta$], [phase constant, the phase accumulated per metre of travel], [rad/m],
  [$underline(E) ( z )$], [the *phasor*: a complex number holding amplitude $E_0$ and phase], [V/m],
  [$j$], [the imaginary unit, $j^2 = - 1$ (engineering notation)], [],
)

This document uses the engineering convention $e^(thin j omega t)$, in which a wave travelling
towards $+ z$ carries the factor $e^(- j beta z)$. Three things make phasors indispensable.

1. *Adding waves becomes adding vectors.* Two waves of the same frequency arriving at a point
   add as two arrows in the complex plane. Aligned, they reinforce; opposed, they cancel. A
   phased array is nothing more than this addition, done deliberately (section 7).
2. *A delay becomes a multiplication.* Travelling a distance $l$ multiplies the phasor by
   $e^(- j beta l)$: the magnitude is unchanged and the phase decreases by $beta l$.
3. *A time derivative becomes multiplication by $j omega$.* Differential equations in time
   become algebra, which is why every RF quantity in this project, S-parameters, the array
   state, channel gains, is complex.

=== 1.5 Phase and distance

The phase accumulated over a distance $z$ is

$ phi ( z ) = beta z , wide beta = frac(2 pi, lambda) $

so one wavelength of travel turns the phase by $2 pi$ radians, 360 degrees. In free space at
2.44 GHz, $beta_0 = 2 pi \/ lambda_0 = 51.1$ rad/m, which is 2.93 degrees per millimetre.

=== 1.6 From here to a switched line phase shifter

If a signal can be routed through either of two lines whose lengths differ by $Delta l$, the
two routes deliver it with a phase difference

$ Delta phi = beta thin Delta l = frac(2 pi, lambda_g) thin Delta l = frac(2 pi f sqrt(epsilon_"eff"), c) thin Delta l $

#table(
  columns: (auto, 3.2fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$Delta phi$], [phase difference between the long and the short route], [rad],
  [$Delta l$], [extra physical length of the long route], [m],
  [$lambda_g$], [guided wavelength in the printed line, not $lambda_0$], [m],
  [$epsilon_"eff"$], [effective permittivity of the microstrip, section 5], [dimensionless],
)

That is the whole principle of the AetherArray phase shifter (section 15). Three consequences
follow from the formula alone, and each one returns later.

- *The relevant wavelength is $lambda_g$.* With the analytical seed $lambda_g = 68.8$ mm,
  a 45 degree bit needs $Delta l = lambda_g \/ 8 approx 8.6$ mm, and one millimetre of printed
  line is about 5.2 degrees. Using $lambda_0$ instead would give lengths 1.8 times too long.
- *The phase is proportional to frequency.* A fixed $Delta l$ is a true time delay, not a
  fixed phase, so a 45 degree bit at 2.44 GHz is a slightly different angle at the band edges
  (section 8.5 and Figure 5b).
- *The phase is proportional to $sqrt(epsilon_"eff")$.* An error in the board's
  permittivity scales every switched length by the same fraction, so the longest state carries
  the largest error (section 59).

#aa-figure(num: "2", caption: [the phase line intuition. Phase grows linearly along a line; a switched line bit
selects between two lengths, and only their difference is the designed phase.])[
```text
   short route  :  in ---[ l_ref ]--------------------------- out     phase -beta*l_ref
   long route   :  in ---[ l_ref + delta_l ]----------------- out     phase -beta*(l_ref + delta_l)

   difference   :  delta_phi = beta * delta_l      (only the DIFFERENCE is designed)

   one guided wavelength lambda_g (about 69 mm on the beamformer board)
   |<----------------------------------------------------------->|
   0 deg              90 deg             180 deg            270 deg            360 deg
   |---------|---------|---------|---------|---------|---------|---------|---------|
            45                  135                  225                 315
```
]

=== 1.7 What is known and what is not

The free space quantities are exact consequences of $f_0$ *\[decided\]*. Every guided length
in this document is an *\[analytical\]* estimate that waits on SIM-001 for a full wave value,
and on board coupons for a measured one (sections 25 and 59).

== 2\. Transmission lines

=== 2.1 Why circuit intuition breaks down

Ordinary circuit theory assumes that a voltage applied at one end of a wire appears at the
other end instantly. That holds while the wire is short compared with a wavelength. A common
rule of thumb says lumped reasoning fails once a structure exceeds about a tenth of a
wavelength. On the beamformer board a tenth of $lambda_g$ is about 7 mm, shorter than many
of its traces, so at 2.44 GHz every trace, connector, switch package and antenna feed has to be
treated as a structure in which the voltage and the current vary along its length.

=== 2.2 The distributed model

A uniform line is modelled as a cascade of infinitesimal sections, each with series
resistance $R '$ and inductance $L '$ and shunt conductance $G '$ and capacitance $C '$, all per
unit length. Solving the resulting telegrapher's equations at one frequency gives voltage and
current waves travelling both ways:

$ V ( z ) = V^(+) e^(- gamma z) + V^(-) e^(gamma z) , wide I ( z ) = frac(V^(+) e^(- gamma z) - V^(-) e^(gamma z), Z_0) $

$ gamma = alpha + j beta = sqrt(( R ' + j omega L ' ) ( G ' + j omega C ' )) , wide Z_0 = sqrt(frac(R ' + j omega L ', G ' + j omega C ')) $

#table(
  columns: (1.0fr, 3.3fr, 1.1fr),
  table.header([Symbol], [Meaning], [Unit]),
  [$V^(+)$, $V^(-)$], [complex amplitudes of the forward and backward waves], [V],
  [$gamma$], [propagation constant], [1/m],
  [$alpha$], [attenuation constant: how fast the amplitude decays], [Np/m; multiply by 8.686 for dB/m],
  [$beta$], [phase constant, as in section 1], [rad/m],
  [$Z_0$], [characteristic impedance: the ratio $V \/ I$ for a single travelling wave], [ohm],
  [$R '$, $L '$, $G '$, $C '$], [line constants per unit length], [ohm/m, H/m, S/m, F/m],
)

For a low loss line, $Z_0 approx sqrt(L ' \/ C ')$ and $beta approx omega sqrt(L ' C ')$. Every RF
part of AetherArray is designed for $Z_0 = 50$ ohm, the impedance of the analyser, the SMA
connectors and the switches, except the Wilkinson arms at 70.7 ohm (section 15.6).

*Loss on the selected boards.* For the beamformer microstrip, the analytical model of
decision 0009 gives a conductor loss of about 4.5 dB/m and a dielectric loss of about
5.3 dB/m at 2.44 GHz, so about 9.8 dB/m in total *\[analytical\]*. The dielectric part follows
the standard quasi-static expression \[#link(<ref-B1>)[B1], chapter 3\]:

$ alpha_d approx frac(k_0 thin epsilon_r thin ( epsilon_"eff" - 1 ) thin tan delta, 2 sqrt(epsilon_"eff") thin ( epsilon_r - 1 )) $

$k_0 = 2 pi \/ lambda_0$, $tan delta$ is the loss tangent of the dielectric, and the result is
in Np/m. With $epsilon_r = 4.4$, $epsilon_"eff" = 3.19$ and $tan delta = 0.015$
it gives 0.61 Np/m, 5.3 dB/m, matching the generated table in section 59. This matters because
a longer phase state is also a lossier one: the 315 degree state carries about 60 mm more line
than the 0 degree state, so about 0.6 dB more loss (section 59).

=== 2.3 The reflection coefficient

When a line of impedance $Z_0$ ends in a load $Z_L$, the load forces its own ratio of voltage
to current. At the load, at $z = 0$, with $Gamma = V^(-) \/ V^(+)$:

$ V ( 0 ) = V^(+) ( 1 + Gamma ) , wide I ( 0 ) = frac(V^(+), Z_0) ( 1 - Gamma ) , wide Z_L = frac(V ( 0 ), I ( 0 )) = Z_0 thin frac(1 + Gamma, 1 - Gamma) $

and solving for $Gamma$:

$ Gamma = frac(Z_L - Z_0, Z_L + Z_0) $

$Gamma$ is complex and dimensionless. It is the fraction of the incident wave amplitude that
comes back, with the phase it comes back with. Four cases are worth knowing by heart.

#table(
  columns: (1.5fr, auto, 2.0fr, 4.7fr),
  table.header([Load], [$Gamma$], [What happens], [Where it appears in AetherArray]),
  [matched, $Z_L = Z_0$], [0], [all power absorbed, nothing reflected], [the 50 ohm terminations of the disabled channels; the analyser ports after calibration],
  [short circuit, $Z_L = 0$], [$- 1$], [total reflection, inverted], [a calibration standard; a via to ground],
  [open circuit, $Z_L arrow.r infinity$], [$+ 1$], [total reflection, same sign], [a calibration standard; the far end of a de-selected switched line arm],
  [mismatched, for example $Z_L = 75$ ohm], [0.2], [partial reflection], [a patch that resonates off frequency; a line etched too narrow],
)

Two derived quantities are used everywhere:

$ "RL" = - 20 log_10 abs(Gamma) space "dB" , wide "VSWR" = frac(1 + abs(Gamma), 1 - abs(Gamma)) , wide L_"mismatch" = - 10 log_10 lr(( 1 - abs(Gamma)^2 )) space "dB" $

#table(
  columns: (auto, 4.6fr, 2.0fr),
  table.header([Symbol], [Meaning], [Unit]),
  [RL], [return loss: how far below the incident wave the reflection is], [dB, positive for a passive load],
  [VSWR], [voltage standing wave ratio: ratio of the maximum to the minimum of the standing wave on the line], [dimensionless, 1 for a match],
  [$L_"mismatch"$], [power lost to reflection at that interface], [dB],
)

Example: $Gamma = 0.2$ gives a return loss of 14 dB, a VSWR of 1.5 and a mismatch loss of
0.18 dB, a figure `python -m rfkit.cli budget` also prints. "VSWR 2" in the patch bandwidth
estimates of section 22 means $abs(Gamma) = 1 \/ 3$, a return loss of 9.5 dB.

=== 2.4 Why every RF part is a transmission line structure

#table(
  columns: (1.5fr, 7.8fr),
  table.header([Part], [Why it is a transmission line problem]),
  [SMA connectors and the four jumpers], [coaxial lines with their own length and impedance; one centimetre of typical coaxial cable is about 44 degrees at 2.44 GHz (README worked example, velocity factor 0.66)],
  [PCB traces], [microstrip lines, section 5; their width sets $Z_0$ and their length sets phase],
  [PE4259-63 switches], [short lines with parasitic inductance and capacitance; their package is a discontinuity, and their off state is a finite isolation, not an open circuit],
  [switched line arms], [the designed phase elements themselves],
  [antenna feeds], [lines that transform the patch edge impedance to 50 ohm],
)

Every discontinuity reflects a little. Two discontinuities a distance apart create a small
standing wave between them, whose effect on the transmitted phase depends on frequency and,
in a switched line, on which arm is selected. That is one route by which a phase error
becomes *state dependent*, the kind calibration cannot absorb (section 11.4).

== 3\. S-parameters

=== 3.1 Waves rather than voltages

At microwave frequencies voltage and current are hard to measure directly, but incident and
reflected waves can be separated with directional couplers. S-parameters describe a network by
how it scatters waves. At each port $i$, referred to a reference impedance $Z_0$:

$ a_i = frac(V_i^(+), sqrt(Z_0)) , wide b_i = frac(V_i^(-), sqrt(Z_0)) $

$a_i$ is the wave going *into* port $i$ and $b_i$ the wave coming *out* of it, both in
$sqrt("W")$. With RMS phasors, $abs(a_i)^2$ is the incident power; with peak
phasors it is twice it. Only ratios are used below, so the convention cancels.

=== 3.2 The two port

$ mat(delim: "[", b_1; b_2) = mat(delim: "[", S_11, S_12; S_21, S_22) mat(delim: "[", a_1; a_2) $

#aa-figure(num: "3", caption: [a two port and its scattering parameters. "Matched" means terminated in the
reference impedance, so that no wave returns into that port.])[
```text
            a1 -->  +-----------------+  <-- a2
   port 1           |                 |           port 2
            b1 <--  |   S11     S12   |  --> b2
                    |   S21     S22   |
                    +-----------------+
       reference plane 1          reference plane 2

   S11 = b1/a1 with a2 = 0  : reflection at port 1, port 2 matched
   S21 = b2/a1 with a2 = 0  : transmission from port 1 to port 2
   S12 = b1/a2 with a1 = 0  : transmission from port 2 to port 1
   S22 = b2/a2 with a1 = 0  : reflection at port 2, port 1 matched
```
]

Each $S_(i j)$ is a complex number at each frequency. For a *reciprocal* network, one with no
amplifier, ferrite or nonreciprocal material, $S_21 = S_12$. For a *lossless* network
the matrix is unitary. The RF signal path of Rev A, switches, lines and Wilkinson network,
contains no amplifier, so it is expected to be reciprocal at the small signal levels used
*\[assumed\]*; reciprocity is checkable in measurement, and decision 0008 already uses the
measured asymmetry $S_(i j) - S_(j i)$ as a floor on measurement uncertainty.

=== 3.3 Magnitude, decibels, phase

$ abs(S_21)_"dB" = 20 log_10 abs(S_21) , wide "IL" = - 20 log_10 abs(S_21) , wide phi_21 = arg S_21 $

#table(
  columns: (auto, 3.0fr, auto),
  table.header([Quantity], [Meaning], [Unit]),
  [$abs(S_21)_"dB"$], [transmission magnitude in decibels, negative for a passive network], [dB],
  [IL], [insertion loss, positive for a passive network], [dB],
  [$phi_21$], [transmission phase], [deg or rad],
)

The factor is 20, not 10, because $S$ is an amplitude ratio and power goes as its square.
*Conventions matter.* The equality of insertion loss with $- 20 log_10 abs(S_21)$
holds when the source and load are both the reference impedance; with a mismatched source or
load the power actually delivered differs. Return loss is defined as $- 20 log_10 abs(S_11)$, positive; some instruments and papers instead plot $S_11$ in dB, negative, and
call it return loss. This document always states which.

For a matched, lossless line of length $l$, $S_21 = e^(- j beta l)$: unit magnitude and a
phase of $- beta l$. The phase decreases with length and with frequency, and is reported
*wrapped* into an interval of 360 degrees by instruments. Comparing phases therefore needs
care: 359 degrees and 1 degree differ by 2 degrees, not 358, which is why `rfkit` takes every
phase difference on the circle (section 31). Unwrapping along frequency recovers a continuous
curve, whose slope is the group delay $tau_g = - thin upright(d) phi_21 \/ upright(d) omega$.

=== 3.4 What AetherArray needs from S-parameters

#table(
  columns: (1.8fr, 4.0fr, 2.5fr),
  table.header([Need], [Quantity], [Where]),
  [validating the microstrip model], [$S_21$ of two line lengths, giving $gamma$ and so $epsilon_"eff"$ and $alpha$], [SIM-001; coupons C1 and C2],
  [the phase of each switched line bit], [$arg S_21$ in the long state minus the short state, between the switch reference planes], [SIM-003 and SIM-004 proposed; SCH-006],
  [state dependent loss], [$abs(S_21)$ of each of the eight states], [decision 0007 imbalance limit; decision 0009 loss estimate],
  [splitter and combiner behaviour], [balance of the four arms, isolation between outputs, input match], [SIM-005 proposed; SCH-006],
  [antenna matching], [$S_11$ of each element port], [SIM-006 proposed; I27],
  [coupling], [the full $4 times 4$ matrix $vb(S)_A$ of the antenna board], [EXP-011, decision 0008],
  [the per channel array state], [$S_21$ from the common port through one enabled channel], [`rfkit.state`, section 11],
)

*Why the phase of $S_21$ is the heart of the phase bits.* A bit is correct when the
difference of transmission phase between its two states is the designed 45, 90 or 180 degrees
at $f_0$, measured between the same two planes. The absolute phase of either arm does not
matter; the difference does (`hardware/rev-a/layout-constraints.md` section 2). A layout that
makes the reference arm short and the delay arm "45 degrees long" is wrong by whatever the
reference arm actually measures.

== 4\. The vector network analyser

=== 4.1 What it measures

A vector network analyser (VNA) contains a swept source and two or more receivers. Directional
couplers or bridges at each port separate the incident wave from the reflected one, and the
receivers measure *ratios* of waves, for example $b_2 \/ a_1$, in both magnitude and phase. That
is what "vector" means: the instrument measures complex ratios, not only powers. A scalar
analyser or a power detector measures magnitude only; it cannot tell a 45 degree bit from a
315 degree one.

=== 4.2 Why a raw reading is not yet a measurement

The instrument's internal paths are not perfect. Its couplers leak (finite directivity), its
ports are not exactly 50 ohm (source and load match), its receivers have frequency dependent
gain and phase (tracking), and the cables and adapters between the instrument and the device
add their own length, loss and reflections. A raw reading of "$S_21$" is the device plus all
of that. *Calibration* removes it: known standards are measured, an error model is solved
from them, and later readings are corrected. For a two port, the familiar procedures connect a
short, an open and a matched load at each port and a through between them (called SOLT, or
TOSM by Rohde and Schwarz), or use lines of known relation instead (TRL). The planes at which
the standards were connected become the *reference planes*: corrected S-parameters describe
the device between those planes and nothing else.

*De-embedding* goes one step further. If the device sits inside a fixture, for example SMA
launches on a board, the fixture can be characterised separately and mathematically removed,
so that the result refers to planes inside the board. Coupon C3 of decision 0009, two launches
back to back, exists for exactly this (section 25).

*Uncertainty* never reaches zero. Residual calibration errors, connector repeatability,
cable movement after calibration, instrument drift and noise all remain. They are combined
into an expanded uncertainty, written $U$ in decisions 0007 and 0008, for each S-parameter at
each frequency.

=== 4.3 Why "the VNA says $S_21 = X$" means nothing on its own

Consider a jumper 10 cm longer than intended. In coaxial cable with a velocity factor of
0.66, the guided wavelength at 2.44 GHz is about 81 mm, so 10 cm adds about 440 degrees of
phase. An uncalibrated reading, or a reading calibrated at the wrong plane, can therefore be
wrong by more than a full turn while looking perfectly plausible. A reading is meaningful
only together with: the reference planes, the calibration method and kit used, the date and
the conditions of that calibration, the intermediate frequency bandwidth and averaging, the
source power, and an uncertainty estimate. The `rfkit` provenance record exists to carry
those facts with every file (section 31).

=== 4.4 The AetherArray analyser, today

The analyser is the subject of experiment EXP-004. Three different capabilities have to be
kept apart.

#table(
  columns: (3.1fr, 11.7fr, 155pt),
  table.header([Capability], [Status], [Evidence]),
  [*The instrument exists and can reach the band*], [*\[observed\]* 2026-09-20: a Rohde and Schwarz ZVL, 9 kHz to 3 GHz, 50 ohm, N female ports, S21 available, complex and phase formats available, source up to 0 dBm, USB present], [`results/EXP-004/README.md` result 2],
  [*A calibrated measurement at the board's SMA plane is possible*], [*unknown.* No calibration kit and no adapter has been confirmed (observation O7). The kits named in the laboratory inventory are 3.5 mm kits belonging to a different instrument whose own presence is unconfirmed], [`docs/hardware/measurement-bench.md` section 6; uncertainty I19],
  [*Measurements can be automated*], [*unknown.* USB is present on the instrument, but nothing has ever enumerated on the project computer (O9); no driver has been identified, and `rfkit.instrument` is deliberately empty of drivers], [`results/EXP-004/README.md` result 1; `docs/architecture/rf-data-layer.md` section 5],
)

The exact model and serial number, observation O1, have not been read; the identification as a
ZVL3 is inferred from behaviour. Which options are installed, observation O8, is unknown,
including whether the time domain option is present. Option designations are known from
manufacturer sources: K1 spectrum analysis, K2 distance to fault, K3 time domain analysis
\[#link(<ref-T1a>)[T1a]\]. The family is described in distributor listings as supporting one port (OSM), full two
port (TOSM) and one path two port calibration \[#link(<ref-T1>)[T1]\], a *\[listing\]* claim that the bench has
not confirmed. Runbook SCH-001, status READY, is the 30 minute bench visit that finishes O1 and
O6 to O9 (`docs/runbooks/SCH-001-exp004-analyser-audit.md`).

The practical blocker is therefore not frequency coverage but the connector chain: the
analyser has N female ports, the boards have SMA connectors, and nothing confirmed joins them
at a calibrated plane. A chain that would work, if its parts exist, is an N male to 3.5 mm
adapter followed by a 3.5 mm calibration at the adapter output, which is mechanically
compatible with SMA. It is a proposal in the repository, not a plan.

== 5\. Microstrip

=== 5.1 Geometry

#aa-figure(num: "4", caption: [microstrip cross-section. The dimensions are the canonical values of
`reva-stackup-r1`; the widths are analytical seeds, not layout values.])[
```text
                 W
              <------>
              +======+              copper trace, thickness t      (L1)
   air        |      |   air
  ------------+------+------------------------------------------- top of dielectric
                                                  dielectric, relative permittivity er
     h        field lines run trace -> ground, partly through air, partly through the board
  ---------------------------------------------------------------- 
  ################################################################ ground plane            (L2)

  Beamformer board (decision 0009): h = 0.2104 mm of 7628 prepreg, er nominal 4.4,
  t = 0.035 mm, seed width for 50 ohm about 0.37 mm.
  Antenna board: h about 1.53 mm of two layer FR-4, er nominal 4.5, seed width about 2.8 mm.
```
]

A microstrip is a copper strip of width $W$ and thickness $t$ on a dielectric layer of height
$h$ and relative permittivity $epsilon_r$, above a continuous ground plane. The signal
travels as a wave guided between the strip and the ground.

=== 5.2 Why the effective permittivity lies between 1 and $epsilon_r$

Below the strip the electric field runs through the dielectric; at the edges it fringes up
into the air and comes back down. The wave therefore sees a mixture, and behaves as if it were
in a uniform medium of *effective permittivity*

$ 1 < epsilon_"eff" < epsilon_r , wide epsilon_"eff" approx frac(epsilon_r + 1, 2) + frac(epsilon_r - 1, 2) thin F , wide F = lr(( 1 + frac(12 h, W) ))^(- 1 \/ 2) $

#table(
  columns: (auto, 4.0fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$epsilon_"eff"$], [effective permittivity of the quasi-TEM wave], [dimensionless],
  [$F$], [filling factor: the share of the field beyond the uniform half that sits in the dielectric], [dimensionless],
  [$h$, $W$], [dielectric height and strip width], [m],
)

This is the quasi-static closed form used in Pozar \[#link(<ref-B1>)[B1], equation 3.195\] and quoted in decision

0009. Because some field is always in air, the wave is not purely TEM; it is called

quasi-TEM, and its $epsilon_"eff"$ rises slowly with frequency (dispersion), which
the Kirschning and Jansen model captures \[#link(<ref-B9>)[B9]\].

=== 5.3 How $W \/ h$ sets the impedance

A wider strip has more capacitance to ground per unit length and so a lower $Z_0$. For
$W \/ h gt.eq 1$ the zero thickness closed form is \[#link(<ref-B1>)[B1]\]

$ Z_0 approx frac(eta_0, sqrt(epsilon_"eff") thin lr([ W \/ h + 1.393 + 0.667 ln lr(( W \/ h + 1.444 )) ])) $

The essential point is that $Z_0$ depends on the *ratio* $W \/ h$ and on $epsilon_r$, not on
$W$ alone. For FR-4 near $epsilon_r = 4.4$, 50 ohm needs $W \/ h$ of roughly 1.8 to 2.
Therefore:

- on the beamformer board, $h = 0.2104$ mm, so a 50 ohm line is about 0.37 mm wide;
- on a two layer 1.6 mm board, $h approx 1.53$ mm, so a 50 ohm line is about 2.8 mm wide.

The SC-70-6 package of the PE4259-63 has a lead pitch of 0.65 mm. A 2.8 mm line is more than
four times that, so every one of the 87 switch RF pins (29 switches, three RF pins each) would
need a taper; a 0.37 mm line matches the pads. This single ratio is why the beamformer is not
built on the antenna board's laminate (decision 0009, option A2).

*A worked check.* With $W = 0.372$ mm and $h = 0.2104$ mm, $W \/ h = 1.77$, $F = 0.358$ and the
closed form gives $epsilon_"eff" approx 3.31$ and $Z_0 approx 52.6$ ohm at zero
thickness. The scikit-rf `MLine` model, which includes the 35 um copper thickness and
dispersion, gives $epsilon_"eff" = 3.19$ at $f_0$ and 50 ohm at that width; its
zero thickness synthesis gives 0.402 mm. Two respectable analytical models differ by about four
per cent in $epsilon_"eff"$ and eight per cent in width. That disagreement is
precisely why the analytical width is called a seed.

=== 5.4 Why $W_"seed"$ is only an initialisation

`rfkit.stackup.seed` computes the width for which the scikit-rf line model gives 50 ohm on
the nominal stack-up. Decision 0009 labels it *INITIALISATION ONLY*: $W_"seed" eq.not W_50$.
SIM-001 sweeps the width at 0.9, 1.0 and 1.1 times the seed in HFSS and interpolates the width
at which the port impedance is 50 ohm; it never extrapolates
(`experiments/SIM-001-microstrip-50-ohm.md`, decision criterion 2). And even $W_50$ from
HFSS is a model of nominal materials: the board as fabricated is characterised later on its
coupons.

=== 5.5 Material uncertainty, one effect at a time

#table(
  columns: (64pt, 5.6fr, 5.6fr, 2.3fr),
  table.header([Effect], [Mechanism], [What it does here], [Status]),
  [nominal $epsilon_r$], [the fabricator's impedance calculator uses 4.4 for 7628 prepreg, with no frequency or test method stated], [sets $epsilon_"eff"$, hence every guided length], [*\[vendor\]* nominal, V8],
  [uncertainty of $epsilon_r$], [published FR-4 values span roughly 4.2 to 4.6; the laminate brand is not guaranteed per order], [a bound of $plus.minus 0.2$ is adopted; it moves the 315 degree state by about 6.3 degrees], [*\[assumed\]* bound, decision 0009],
  [manufacturing variation], [prepreg thickness, etched width, copper thickness], [impedance from about 41 to 61 ohm at the worst corner of all bounds; up to 11.6 degrees on the 315 degree state], [*\[analytical\]*, generated table in section 59],
  [glass weave], [7628 is a coarse glass cloth; a 0.37 mm line can sit over glass bundles or resin gaps], [different channels may see different local permittivity; *the one material effect a coupon cannot calibrate away*], [*unquantified*, uncertainty I25],
  [copper roughness], [the foil's surface roughness, a few micrometres, exceeds the 1.34 um skin depth at 2.44 GHz], [raises conductor loss, up to about double in the Hammerstad and Jensen model, and raises apparent permittivity], [*bounded*, not modelled; section 24],
  [solder mask], [a thin dielectric coating of uncertain thickness over the line], [would add channel dependent phase], [*removed*: mask opened over RF copper; section 24],
  [conductor loss], [finite copper conductivity, skin effect, ENIG nickel on exposed copper], [about 4.5 dB/m on the beamformer line, smooth copper], [*\[analytical\]*],
  [dielectric loss], [$tan delta = 0.015$, a laminate vendor typical value at 1 GHz], [about 5.3 dB/m; does not depend on width], [*\[vendor\]* typical, V12],
)

The skin depth is $delta_s = sqrt(2 \/ ( omega mu_0 sigma )) = 1.34$ um for copper at 2.44 GHz, with
$sigma = 5.8 times 10^7$ S/m; the 15.2 um inner copper of the ground plane is about eleven
skin depths thick, so it behaves as a good conductor.

== 6\. Antennas

=== 6.1 Radiation in a few lines

An antenna turns a guided wave into a free wave. Time varying currents on a conductor radiate:
far from the antenna, at distances large compared with both the wavelength and the antenna,
the field falls as $1 \/ r$, is transverse to the direction of travel, and its angular shape no
longer depends on distance. That angular shape is the *radiation pattern*. The boundary of
that *far field* region is conventionally taken at $R = 2 D^2 \/ lambda$ for an antenna of
largest dimension $D$; for the four element array, $D approx 0.18$ m and $R approx 0.55$ m
(decision 0004).

=== 6.2 The figures used to describe an antenna

#table(
  columns: (1.7fr, 4.8fr, 2.0fr),
  table.header([Quantity], [Definition], [Unit]),
  [directivity $D ( theta , phi.alt )$], [radiation intensity in a direction divided by its average over all directions], [dimensionless, or dBi],
  [radiation efficiency $e_r$], [radiated power divided by accepted power; the rest is lost in conductor and dielectric], [dimensionless],
  [gain $G$], [$G = e_r D$], [dBi],
  [realised gain], [$G thin ( 1 - abs(Gamma)^2 )$: includes the mismatch at the feed], [dBi],
  [polarisation], [the direction in which $vb(E)$ oscillates; a simple patch is linearly polarised], [],
  [E-plane, H-plane], [the two principal cuts of the pattern: containing $vb(E)$, and containing $vb(H)$], [],
  [half power beamwidth], [angle between the two directions where the pattern is 3 dB below its maximum], [deg],
  [sidelobes], [secondary maxima of the pattern; their level is quoted relative to the main lobe], [dB],
  [impedance match], [how close the feed impedance is to 50 ohm, through $Gamma$], [],
)

By reciprocity, an antenna has the same pattern, gain and impedance when receiving as when
transmitting. That is why a receiving array can be characterised by transmitting through it
with a passive network, and why the AP-S demonstrator, which must receive (section 45), can be
designed with transmit language.

=== 6.3 The microstrip patch

A patch is a rectangle of copper on a grounded dielectric. Between the patch and the ground it
behaves like a leaky resonant cavity: the fundamental mode has a standing wave along the patch
length $L$, and the fields fringing at the two radiating edges add in phase broadside to the
board. Resonance occurs approximately when $L$ is half a wavelength in the dielectric,
slightly shortened by fringing. The transmission line model in Balanis \[#link(<ref-B2>)[B2]\] gives seeds:

$ W_p = frac(c, 2 f_0) sqrt(frac(2, epsilon_r + 1)) , wide L_p approx frac(c, 2 f_0 sqrt(epsilon_("eff" \, p))) - 2 thin Delta L $

#table(
  columns: (auto, 3.3fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$W_p$, $L_p$], [patch width and resonant length], [m],
  [$epsilon_("eff" , p)$], [effective permittivity of a microstrip as wide as the patch], [dimensionless],
  [$Delta L$], [fringing extension at each radiating edge, a fraction of $h$], [m],
)

On the antenna construction this gives $W_p approx 37.0$ mm and $L_p approx 28.6$ mm
*\[analytical, sanity check only\]* (generated table, section 22).

What controls the rest:

- *Substrate thickness $h$.* Bandwidth grows roughly in proportion to $h \/ lambda$, and so does
  the share of power radiated rather than dissipated. A thin substrate stores a lot of energy
  for little radiation: a high quality factor, a narrow bandwidth and a low efficiency.
- *Permittivity $epsilon_r$.* A higher $epsilon_r$ makes the patch smaller but its
  bandwidth narrower, and makes the resonance sensitive to permittivity error.
- *Feed position.* The input impedance varies from a few hundred ohm at the edge to near
  zero at the centre; an inset feed or a quarter wave transformer brings it to 50 ohm.
- *Loss.* On FR-4 with $tan delta approx 0.015$, dielectric loss takes a large share of
  the accepted power.

=== 6.4 Why the antenna board and the beamformer board use different stack-ups

Decision 0009 applied the same patch sanity check to every candidate construction.

#table(
  columns: (2.0fr, auto, 1.6fr, 1.5fr),
  table.header([Construction], [$h$], [Patch bandwidth, VSWR 2], [Radiation efficiency]),
  [beamformer, 4 layer FR-4, patch over L2], [0.21 mm], [about 0.14 per cent], [about 9 per cent],
  [antenna, 2 layer FR-4], [1.53 mm], [about 1.05 per cent], [about 48 per cent],
)

*\[analytical\]* estimates, generated in section 22. The thin prepreg that makes the beamformer
lines narrow enough for the switch pads would make a patch with almost no bandwidth and an
efficiency near ten per cent; the thick core that suits a patch makes 2.8 mm lines that do not
fit the switches and leaves no inner plane for control routing. The two boards need
substrates an order of magnitude apart, so they are two boards with two constructions from
one fabricator and one laminate class.

Two consequences of the antenna estimate deserve attention, both *\[analytical\]* and both
recorded in decision 0009 or derivable from it.

- *The bandwidth is narrower than the band.* About 1.05 per cent of 2.44 GHz is about
  26 MHz, while band 57a is 83.5 MHz wide. If the estimate holds, a single patch is matched to
  VSWR 2 over roughly a third of the band. This does not contradict any decision, but every
  judgement made "at every point in band 57a" (decisions 0007 and 0008) will see the antenna
  mismatch change across the band. SIM-006 must report it.
- *The first board may miss the band.* The permittivity bound alone moves the resonance by
  $- 1.06$ to $+ 3.38$ per cent, which is more than the bandwidth. Decision 0009 says a second
  antenna board order should be expected.

=== 6.5 The antenna design workflow

#diagram[
#image("../figures/mermaid/diagram-65-the-antenna-design-workflow.svg", width: 100%)
]

Nothing in the repository designs the patch yet; its length, width, feed and spacing remain
free parameters for HFSS (decision 0009). The analytical equations above say only that a patch
is physically sensible on the chosen construction.

== 7\. Phased arrays

=== 7.1 Intuition

Several antennas fed with the same signal radiate waves that add at every point in space. In
some directions the waves arrive in step and reinforce; in others they arrive out of step and
cancel. Delaying the signal to each element by a controlled amount moves the direction in
which they reinforce. That is a phased array: a beam steered by phase, with nothing moving.
The standard references for what follows are Balanis \[#link(<ref-B2>)[B2]\], Mailloux \[#link(<ref-B3>)[B3]\] and Hansen \[#link(<ref-B4>)[B4]\].

=== 7.2 Geometry and the array factor

#aa-figure(num: "6", caption: [four element uniform linear array, element 0 at the origin, spacing $d$.])[
```text
                       wavefront arriving from direction theta
                    \        \        \        \
                     \        \        \        \
                      \  d sin(theta)  \        \
                       \ |<-->| \        \        \
     element:      0 ---o--------o--------o--------o---   x
                        |<--d--->|
                     origin    n = 1    n = 2    n = 3        theta measured from broadside (the normal)
```
]

Take $N$ identical elements on a line, spaced by $d$, element 0 at the origin, and a distant
point in the direction $theta$ measured from the array normal (broadside). The path from
element $n$ is shorter than the path from element 0 by $n d sin theta$, which is a phase
advance of $n k d sin theta$ with $k = 2 pi \/ lambda_0$. If element $n$ is fed with amplitude
$a_n$ and phase $phi.alt_n$, the field in direction $theta$ is proportional to

$ A F ( theta ) = sum_(n = 0)^(N - 1) a_n thin e^(thin j lr(( n k d sin theta + phi.alt_n ))) $

#table(
  columns: (auto, 3.2fr, 2.0fr),
  table.header([Symbol], [Meaning], [Unit]),
  [$A F ( theta )$], [array factor: the coherent sum of the element contributions], [dimensionless, complex],
  [$a_n$, $phi.alt_n$], [amplitude and phase applied to element $n$: the command], [dimensionless, rad],
  [$k = 2 pi \/ lambda_0$], [free space wavenumber, 51.1 rad/m at 2.44 GHz], [rad/m],
  [$d$], [element spacing, $lambda_0 \/ 2 = 61.4$ mm for Rev A], [m],
  [$theta$], [observation angle from broadside], [rad],
)

This is the convention of `README.md`, `docs/mathematics/formulation.md` and
`rfkit.budget.array_factor`, and every formula below uses it. By reciprocity the same
expression describes reception: a plane wave arriving from $theta$ and combined with weights
$a_n e^(j phi.alt_n)$ produces an output proportional to $A F ( theta )$.

*Element pattern and total pattern.* Real elements are not isotropic. If all elements had
the same pattern $f ( theta )$, the total field would factor as $E ( theta ) = f ( theta ) thin A F ( theta )$,
the principle of pattern multiplication. With coupling, each element radiates differently
inside the array, and the correct description uses one *embedded element pattern* $g_n ( theta )$
per element: $E ( theta ) = sum_n g_n ( theta ) thin a_n e^(j phi.alt_n)$. Decision 0008 uses exactly this
form for the simulation stage of gate G4 (section 10).

=== 7.3 Steering

With uniform amplitudes, $A F$ is largest when every term has the same phase in the wanted
direction $theta_0$. That requires $n k d sin theta_0 + phi.alt_n$ to be the same for all $n$,
so

$ phi.alt_n = - thin n thin k d sin theta_0 , wide Delta phi.alt = phi.alt_(n + 1) - phi.alt_n = - thin k d sin theta_0 $

$Delta phi.alt$ is the progressive phase between neighbours, in rad. With $d = lambda_0 \/ 2$,
$k d = pi$, so $Delta phi.alt = - 180 degree sin theta_0$: steering to 30 degrees needs
$- 90$ degrees per element, steering to 15 degrees needs $- 46.6$ degrees. Substituting into the
array factor with $a_n = 1$ and summing the geometric series gives the classical closed form

$ abs(A F ( theta )) = lr(| frac(sin ( N psi \/ 2 ), sin ( psi \/ 2 )) |) , wide psi = k d lr(( sin theta - sin theta_0 )) $

which is exact. Its maximum, $N$, occurs at $psi = 0$, that is $theta = theta_0$: the
*coherent addition* of $N$ unit contributions. The array output power in that direction is
$N^2$ times one element's, while the noise from independent sources adds only as $N$, which is
why the array gain over one element is $10 log_10 N$, 6.0 dB for four isotropic elements at
half wavelength spacing.

=== 7.4 Nulls, beamwidth, sidelobes and grating lobes

- *Nulls.* $abs(A F) = 0$ when $N psi \/ 2$ is a nonzero multiple of $pi$ but $psi \/ 2$ is
  not: $psi = 2 pi m \/ N$. At broadside, $N = 4$ and $d = lambda_0 \/ 2$, the nulls fall at
  $sin theta = plus.minus 0.5$ and $plus.minus 1$: $plus.minus 30$ and $plus.minus 90$ degrees. Section 9 uses the null at
  30 degrees.
- *Beamwidth.* The half power beamwidth at broadside is approximately
  $0.886 thin lambda_0 \/ ( N d )$ radians, 25.4 degrees for Rev A, and it widens roughly as
  $1 \/ cos theta_0$ when the beam is steered.
- *Sidelobes.* With uniform amplitudes the first sidelobe is $- 11.3$ dB for $N = 4$; the
  often quoted $- 13.2$ dB is the limit for large $N$ ($- 12.8$ dB at $N = 8$, $- 13.15$ dB at
  $N = 16$) *\[analytical\]*. Lowering sidelobes needs an amplitude taper, which Rev A cannot
  apply (decision 0003, section 4 of the architecture document).
- *Grating lobes.* $A F$ repeats whenever $psi$ advances by $2 pi$. A second full strength
  lobe, a grating lobe, appears in visible space unless

$ frac(d, lambda) < frac(1, 1 + abs(sin theta_0)) $

which for steering anywhere up to 90 degrees gives $d lt.eq lambda \/ 2$. That is why half a
wavelength is the usual spacing. Rev A's spacing is half a wavelength at 2.44 GHz; at the
upper band edge it is 0.509 wavelengths, still far from a grating lobe for the benchmark
steering angles up to 45 degrees.

- *Aperture.* The array spans $3 d = 1.5 lambda_0 = 184$ mm between element centres.

#aa-figure(num: "7a", caption: [array factor of four isotropic elements at half wavelength spacing, broadside,
steered to 30 degrees with an exact progressive phase of $- 90$ degrees, and steered to 15
degrees with continuous phases and with phases rounded to the 45 degree grid. The rounded 15
degree command points at 14.48 degrees. *\[analytical\]* illustration, generated by
`tools/docs/master_reference_figures.py`.])[
#image("../figures/steering-n4.svg", width: 78%, alt: "Steering a four element array with 3-bit phase states")
]

=== 7.5 What four elements can and cannot do

#table(
  columns: (5.8fr, 3.8fr),
  table.header([Can], [Cannot]),
  [steer a 25 degree wide beam over roughly $plus.minus 45$ degrees], [form a narrow beam or resolve sources closer than about a beamwidth],
  [place up to $N - 1 = 3$ nulls with full complex weights; fewer, and less precisely, with phase only quantised control], [reject many interferers at once],
  [show, cleanly, every effect of phase error, quantisation, coupling and drift on pointing, gain and null depth], [demonstrate the gain, sidelobe performance or scaling behaviour of a large array],
  [be enumerated exhaustively: every reachable beam state can be evaluated], [serve as a production antenna],
)

Four elements is a small array, and this document does not present it otherwise. Its value is
that it is an *instrumented* array: every element has its own connector, every channel can be
isolated electronically, every state is an exact code word, temperature is logged, and the
number of states is small enough to evaluate completely. Those are properties of a research
platform, not of a product.

== 8\. Quantised phase shifting

=== 8.1 The eight states

Each Rev A channel has three switched line bits of 45, 90 and 180 degrees (decision 0003).
With bit values $b_45 , b_90 , b_180 in \{ 0 , 1 \}$, the nominal phase of the channel is

$ phi.alt = 45 degree lr(( b_45 + 2 thin b_90 + 4 thin b_180 )) in \{ 0 degree , 45 degree , 90 degree , dots.h , 315 degree \} $

so eight states, 45 degrees apart. State 7, all three bits set, is the 315 degree state with
the most extra line. The phase is "nominal" because the realised phase of each state differs
from it; the forward model of `docs/mathematics/inverse-calibration.md` section 2 uses nominal
phases on purpose and lets the array state absorb what it can of the difference.

=== 8.2 Quantisation error and its floor

To command an arbitrary phase, the controller picks the nearest state; the effect of this rounding
on array patterns is a classical subject \[#link(<ref-B7>)[B7]\]. If the wanted phases
are spread uniformly, the rounding error is uniform on $plus.minus 22.5$ degrees, and its standard
deviation is

$ sigma_q = frac(Delta, sqrt(12)) = frac(45 degree, sqrt(12)) = 12.99 degree $

$Delta$ is the step, 45 degrees; $sqrt(12)$ is the standard deviation of a uniform
distribution of unit width. Decision 0007 propagates this floor to the array, with the
finite array formulas implemented in `rfkit.budget` and checked by Monte Carlo
*\[analytical\]*:

#table(
  columns: (2.3fr, 1.2fr, 1.8fr),
  table.header([Consequence of the 3-bit floor], [Value], [Formula]),
  [pointing standard deviation at broadside], [1.85 degrees], [$sigma_theta = sigma_q \/ lr(( k d cos theta_0 sqrt(sum_i ( i - macron(dotless.i) )^2) ))$, with $sum_i ( i - macron(dotless.i) )^2 = 5$ for four elements],
  [coherent gain loss], [0.167 dB], [$G \/ G_0 = e^(- sigma^2) + ( 1 - e^(- sigma^2) ) \/ N$],
  [error sidelobe floor], [$- 18.9$ dB relative to the peak], [$10 log_10 ( sigma^2 \/ N )$],
  [worst case error on one channel], [22.5 degrees], [half a step; beyond it states come out of order],
)

The large array approximation $e^(- sigma^2)$, the classical tolerance result \[#link(<ref-B6>)[B6]\], overstates the
gain loss at four elements by about a third, 0.223 against 0.167 dB; decision 0007 corrected an earlier draft that used it.
*These numbers are the floor no calibration can beat*, because they come from the bit count,
not from any error. Decision 0007 anchors every acceptance threshold to them (section 57).

The rounding is deterministic for a given steering angle; $sigma_q$ is its average over
angles. Some angles need no rounding at all. With $d = lambda_0 \/ 2$ the progressive phase
$Delta phi.alt = - m times 45 degree$ is exactly reachable when $sin theta_0 = m \/ 4$: at 0,
14.48, 30, 48.59 and 90 degrees. A request for 15 degrees rounds to the 14.48 degree command,
an error of 0.52 degrees (Figure 7a).

=== 8.3 Only relative phase matters

Adding the same phase $c$ to every channel multiplies $A F$ by $e^(j c)$, which changes neither
its magnitude nor the direction of its maximum. *The far field beam shape depends only on
relative phases.* Two consequences:

1. The common phase is unobservable from the beam and can be fixed by convention, for example
   by taking channel 0 as the reference (requirement R7).
2. The number of distinct beam shapes is the number of relative phase configurations. With
   one channel as reference and eight states on each of the other three,

$ abs(cal(X)) = 8^(thin N - 1) = 8^3 = 512 $

The 16 bit beam state word has 65 536 values, but most of them are redundant: they differ by a
common phase, or by the phase bits of a channel that is disabled. Counting the enable bits as a
binary amplitude, the distinct relative configurations are $sum_(k = 1)^4 binom(4, k) 8^(k - 1) = 512 + 256 + 48 + 4 = 820$ *\[analytical\]*: all four channels on, three on, two on, one on.

*This small number is central to Part VIII.* With an estimate of the array state, every one
of the 512 (or 820) configurations can be evaluated in software in a fraction of a second, so
the best beam for any criterion is found exactly, by enumeration. There is nothing for a
learned beamformer to do (section 38).

=== 8.4 Why the common phase is not quite free off $f_0$

The eight command "origins", adding $0 , 45 , dots.h , 315$ degrees to every channel, give the same
beam at $f_0$. Away from $f_0$ they do not, because a switched line's phase scales with
frequency (section 8.5): adding a common offset changes which bits are set and therefore how
much line each channel carries. Decision 0007 found that a steering table which picks the
origin per angle keeps band edge operation within the pointing budget, while the worst origin
exceeds it at 22 of 91 angles between 0 and 45 degrees, by up to 22 per cent
*\[analytical\]*. This constrains whoever writes the steering table; no `rfkit` metric
enforces it.

=== 8.5 Dispersion of a switched line

A fixed length of line is a time delay, so its phase grows in proportion to frequency:
$phi.alt ( f ) = phi.alt_"nominal" thin f \/ f_0$ for an ideal non dispersive line. Band 57a spans
$- 1.64$ to $+ 1.78$ per cent about 2.44 GHz, so the 315 degree state is $- 5.2$ degrees off at
2.400 GHz and $+ 5.6$ degrees off at 2.4835 GHz, before any fabrication error
*\[analytical\]*. Both simulators must reproduce this term; it is intrinsic, and only their
disagreement about it is judged (decision 0007).

#aa-figure(num: "5b", caption: [phase error against frequency of the 45, 90, 180 and 315 degree states of an ideal
switched line, relative to their nominal value at 2.44 GHz. *\[analytical\]*.])[
#image("../figures/switched-line-dispersion.svg", width: 78%, alt: "Intrinsic dispersion of the switched line states across band 57a")
]

== 9\. Null steering and interference rejection

=== 9.1 Three different goals

#table(
  columns: (1.7fr, 2.7fr, 3.5fr),
  table.header([Goal], [What is optimised], [When it is the right goal]),
  [steer the main beam], [response in one direction $theta_D$], [one source, no interference],
  [place a null], [response in one direction $theta_I$ driven to zero], [one interferer to suppress, the wanted direction loosely constrained],
  [maximise a signal to interference metric], [the ratio of wanted to unwanted response], [both matter at once: the AP-S communication mode],
)

=== 9.2 Formulation

Write the steering vector for direction $theta$ as $vb(a) ( theta )$ with entries
$a_n ( theta ) = e^(- j n k d sin theta)$, and the realised weights as $vb(w)$, whose entry
$w_n$ is the complex amplitude applied to element $n$ (written $a_n e^(j phi.alt_n)$ in section 7,
where $a_n$ was an amplitude, not a steering vector entry), so that $vb(a) ( theta )^(sf(H)) vb(w) = A F ( theta )$ in the
convention of section 7. For a wanted source at $theta_D$ and an interferer at $theta_I$:

$ P_D ( vb(w) ) = lr(| vb(a)_D^(sf(H)) vb(w) |)^2 , wide P_I ( vb(w) ) = lr(| vb(a)_I^(sf(H)) vb(w) |)^2 , wide J ( vb(w) ) = P_D ( vb(w) ) - lambda thin P_I ( vb(w) ) $

or, with source powers $S_D$ and $S_I$ received by an isotropic element and receiver noise
power $sigma_n^2$ referred to one channel,

$ "SIR"( vb(w) ) = frac(S_D thin P_D ( vb(w) ), S_I thin P_I ( vb(w) )) , wide "SINR"( vb(w) ) = frac(S_D thin P_D ( vb(w) ), S_I thin P_I ( vb(w) ) + sigma_n^2 norm(vb(w))^2) $

#table(
  columns: (auto, 3.3fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$vb(a)_D$, $vb(a)_I$], [steering vectors towards the wanted and the interfering source], [dimensionless],
  [$P_D$, $P_I$], [array power response towards each], [dimensionless],
  [$lambda$], [trade-off weight of the scalar objective, not a wavelength here], [dimensionless],
  [$S_D$, $S_I$], [received powers of the two sources at one element], [W],
  [$sigma_n^2$], [noise power per channel], [W],
)

The SINR form is the textbook one for a receiver with independent channel noise \[#link(<ref-B5>)[B5]\]. In Rev A
the channels are combined passively before any receiver, so the noise is added after the
combiner and the simpler SIR is the meaningful figure; which of the two applies depends on the
receiver chosen for the demonstrator, which is not chosen (section 47).

With unconstrained complex weights the best null keeping the wanted response is the
projection of $vb(a)_D$ orthogonal to $vb(a)_I$,
$vb(w) prop lr(( vb(I) - vb(a)_I vb(a)_I^(sf(H)) \/ N )) vb(a)_D$,
which puts an exact null on $theta_I$ at the cost of some gain towards $theta_D$. Rev A
cannot apply it: it has no amplitude control and only eight phases per channel. Its reachable
set is the 512 relative configurations (820 with the enable bits), so the problem becomes

$ vb(x)^star = arg max_(vb(x) in cal(X)) thick J lr(( hat(vb(H))_t vb(w)_"nominal"( vb(x) ) )) $

an exact enumeration once the array state estimate $hat(vb(H))_t$ exists
(`docs/mathematics/inverse-calibration.md` section 5).

=== 9.3 Degrees of freedom at $N = 4$

Four channels give three relative complex weights. With full complex control they can place
three nulls, or one null and keep a well formed main beam. With phase only control, the
amplitudes are fixed and only the three relative phases remain; with three bits each of those
takes eight values. Some pairs of wanted and interfering directions will be well served by
some state, others will not, and an interferer close to the wanted direction, within about a
beamwidth, cannot be rejected without losing the wanted signal too. Which angle pairs are
achievable, and how robustly, is exactly the question of the N = 4 feasibility gate proposed
in section 50; it has deliberately not been computed for this document, because its
acceptance rule has to be fixed first.

=== 9.4 Why nulls are a sensitive meter of calibration error

A main beam is forgiving: the 13 degree quantisation floor costs only 0.17 dB of gain. A null
is the opposite. It exists because four contributions cancel, and any residual error leaves
an uncancelled remainder. For small independent errors of standard deviation $sigma$, in
radians of phase or in relative amplitude, the expected power left in a null, relative to the
beam peak, is

$ frac(bb(E) lr([ abs(A F ( theta_"null" ))^2 ]), N^2) approx frac(sigma^2, N) $

an approximation valid for $sigma lt.double 1$ rad, which the Monte Carlo of Figure 7b confirms. Its
consequences, at $N = 4$ *\[analytical\]*:

#table(
  columns: (1.2fr, 1.5fr),
  table.header([Residual error, rms], [Expected null power relative to the beam peak]),
  [1 degree], [$- 41$ dB],
  [2 degrees], [$- 35$ dB],
  [5 degrees], [$- 27$ dB],
  [10 degrees], [$- 21$ dB],
  [13 degrees, the 3-bit floor], [$- 19$ dB],
)

The same mechanism is the "error sidelobe floor" of decision 0007. Phase quantisation,
amplitude imbalance, coupling and drift all add to $sigma^2$, and any of them fills the null.
A drift of a few degrees, almost invisible in the main beam, moves a null by several decibels.
*That is why the demonstrator proposed in Part IX shows calibration through nulls rather
than through the main beam.* Two cautions apply: the formula describes the average over
random errors, not a particular deterministic null chosen by enumeration, which can be deeper
or shallower; and a measured null depth is also limited by the measurement's own noise floor
and by multipath in the room.

#aa-figure(num: "7b", caption: [left, the broadside pattern with its null at 30 degrees, and 25 patterns with
independent phase errors of 10 degrees rms; right, the mean power at the 30 degree null against
the rms phase error, Monte Carlo and the small error formula. *\[analytical\]* illustration
with random draws from a fixed seed; it is not data.])[
#image("../figures/null-filling-n4.svg", width: 100%, alt: "Null filling by random phase errors")
]

== 10\. Mutual coupling

=== 10.1 Two mechanisms

*Antenna mutual coupling* is radiative: part of the wave radiated or received by one patch
is picked up by its neighbours, so each element's current depends on what the others are
doing. It is described by the antenna board's $4 times 4$ scattering matrix $vb(S)_A$,
measured at the four element connectors; its off diagonal terms are the coupling. Its practical
signatures are an *active reflection coefficient* that changes with the steering state and
*embedded element patterns* that differ from the isolated element pattern and from one
another.

*RF path coupling* happens in the beamformer: imperfect isolation between channels and
reflections at the beamformer outputs. Decision 0008 splits it into a reverse part, which acts
together with $vb(S)_A$ through waves reflected by the antennas, and forward crosstalk, a
channel's transfer changing with a neighbour's state, which it treats as a state dependent
diagonal error judged under decision 0007.

Rev A's two board split makes these separable: each board can be characterised on its own at
the element connector plane (decision 0008, context).

=== 10.2 Why a diagonal array state is an approximation

$ vb(H) = vb(D) + vb(C) $

$vb(D)$ is diagonal: one complex gain per channel. $vb(C)$ is the cross channel part:
coupling. The Rev A calibration model keeps only $vb(D)$. That model is exact only if
coupling is negligible or if it does not depend on the commanded state. In general it does,
because the contribution of element $m$ to element $n$ carries the relative phase of their
commands.

Decision 0008 writes the coupled forward model explicitly. For the waves $vb(t) ( s )$ the
beamformer delivers into matched loads in state $s$:

$ vb(a) ( s ) = lr(( vb(I) - vb(S)_(B o) ( s ) thin vb(S)_A ))^(- 1) vb(t) ( s ) , wide vb(e) ( s ) = lr(( vb(I) - vb(S)_A )) vb(a) ( s ) , wide E ( u , s ) = vb(v) ( u )^(sf(T)) thin vb(e) ( s ) $

#table(
  columns: (auto, 4.4fr),
  table.header([Symbol], [Meaning]),
  [$vb(S)_(B o) ( s )$], [beamformer reverse path: output reflections on the diagonal, output to output isolation off it],
  [$vb(a) ( s )$], [waves actually incident on the antennas],
  [$vb(e) ( s )$], [radiating currents, in the canonical minimum scattering approximation \[#link(<ref-A23>)[A23], #link(<ref-A24>)[A24]\]],
  [$v_m ( u ) = e^(thin j m k d u)$, $u = sin theta$], [far field phase of element $m$],
)

The middle equation is an approximation exact for no real patch, so the simulation stage of G4
also uses the solver's embedded element patterns, with no approximation.

=== 10.3 Gate G4: a test of the model, not a limit on coupling

Decision 0008 records four findings, obtained from the model on synthetic matrices before any
data, which shaped the test.

1. *A calibration residual cannot detect coupling.* When coupling does not depend on the
   state, a probe calibration at one direction fits the diagonal model exactly. The error
   appears only when the beam is steered away from where the calibration looked.
2. *A single raw coupling number cannot decide.* On a synthetic uniform array with nearest
   neighbour coupling of $- 25$ dB, the pointing error of the broadside calibration ranges from
   0.38 to 1.27 of the budget as the *phase* of the coupling varies. Same $abs(S_(i j))$,
   opposite verdicts.
3. *A single number can guarantee something narrower.* A screen, a bound on the relative size
   of the coupled currents, guarantees a pass when it is below 0.040 (about $- 28$ dB aggregate,
   $- 34$ dB per neighbour), but it rejects arrays that full propagation passes by several dB.
   It is reported and never decides.
4. *Coupling is structured.* It is reciprocal, close to Toeplitz and deterministic; treating it
   as independent random terms would be the wrong model.

The test that follows judges what matters, the calibrated beam. At every frequency in band 57a,
for steering angles from $- 45$ to $+ 45$ degrees in one degree steps and all eight command
origins, the beam of the calibrated diagonal model is compared with the coupled beam, against a
budget of $eta_c = 0.10$ of the quantisation floor's error variance, allocated separately from
decision 0007's:

$ delta theta^2 lt.eq eta_c thin sigma_(theta , q)^2 ( theta_0 ) , wide L lr(( 1 + bold(epsilon.alt) )) lt.eq eta_c thin L_q $

$delta theta$ is the difference of the two beam maxima, $sigma_(theta , q) ( theta_0 )$ the
quantisation pointing spread at that steering angle, $L$ the coherence loss caused by the
relative current error $bold(epsilon.alt)$, and $L_q = 0.167$ dB the floor's. The outcome
is PASS, FAIL, INTERMEDIATE or UNRESOLVED by rules fixed before any data (section 58). On the
synthetic nearest neighbour chart printed by `python -m rfkit.cli g4-chart`, full propagation
passes at every coupling phase down to $- 27$ dB and fails at some phases at $- 25$ dB
*\[synthetic\]*; this is an idealisation and not a prediction of EXP-011.

*The full coupling model is an extension, not the default.* If G4 fails, the first promotion
freezes a measured coupling matrix in the forward model, which keeps the unknowns at $2 N - 2$
provided the coupling does not drift. Only if that also fails are coupling terms estimated,
raising the unknowns to order $2 N^2$, 32 at $N = 4$, and reopening every measurement count in
the repository (decision 0008, "What follows from each outcome"). No coupling has been
simulated or measured; the antenna geometry it needs is not designed.

#include "01b-isac-10bis.typ"

#include "01c-course-theory-continued.typ"
