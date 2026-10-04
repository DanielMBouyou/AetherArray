#import "../template.typ": *

= Part 0. Executive overview <part-0-executive-overview>

== 0.1 What is AetherArray?

AetherArray is a four channel, 2.44 GHz, phase only, switched line phased array research
platform, designed so that the drift of a real RF array can be observed and so that
recalibration with fewer new physical measurements can be tested against conventional
recalibration. Its first hardware revision, Rev A, is two printed circuit boards: a passive
board of four microstrip patch antennas, and a beamformer board joined to it by four coaxial
jumpers. On the beamformer board each channel has an enable switch that either passes the
signal or terminates the channel in 50 ohm, followed by three switched line phase bits of 45,
90 and 180 degrees built from PE4259-63 RF switches; the four channels meet in a four way
Wilkinson network whose common port is switched either to a vector network analyser or to an
on board AD8318 logarithmic power detector, and two MCP9808 sensors log temperature. An
external Terasic DE1-SoC drives the sixteen beam state lines: its FPGA applies each state on a
single clock edge, holds the control lines still while the detector is sampled and timestamps
everything from one clock, and its processor stores the records and runs the inference. The
design flow goes from analytical seeds through full wave simulation in Ansys HFSS, scripted
with PyAEDT, optionally through a circuit model in Keysight ADS or scikit-rf, to measurement on
a Rohde and Schwarz ZVL analyser, with every result exchanged as a Touchstone file and read by
`rfkit`, the project's library on top of scikit-rf. Calibration is posed as a Bayesian inverse
problem: an explicit physical forward model supplies the likelihood, and a prior learned from
the array's own drift history is meant to make recalibration cheaper. A competition facing
demonstrator for integrated sensing and communication would use the calibrated array as a
reconfigurable receiver that steers towards a wanted commercial transmitter, suppresses an
interfering one, and senses changes in a room lit by ambient Wi-Fi or Bluetooth signals: a
shared aperture, opportunistic form of ISAC, defined and bounded in section 10bis.

Sources: decisions 0003, 0004, 0005 and 0009; `docs/architecture/rev-a-rf-architecture.md`;
`docs/architecture/control-architecture.md`; `docs/mathematics/inverse-calibration.md`;
`docs/architecture/rf-data-layer.md`. The demonstrator is *\[proposed here\]*, from the project
owner's brief of 2026-10-04; the repository records no decision about it (section 45).

Three things are easily confused, and this document keeps them apart throughout.

#table(
  columns: (60pt, 5.0fr, 163pt, 4.5fr),
  table.header([], [What it is], [Where it is recorded], [State on 2026-10-04]),
  [*The physical platform*], [the two Rev A boards, the controller, the analyser and the software around them], [decisions 0003, 0005, 0009; `hardware/rev-a/`], [designed, schematic captured; control section needs re-capture; nothing fabricated],
  [*The scientific question*], [whether a learned prior over drift reduces the new measurements needed to recalibrate], [decision 0002; `docs/architecture/ml-calibration.md`; EXP-015], [formalised; gated by G2, which needs the built array],
  [*The AP-S demonstrator*], [an ISAC receiver built on the platform, to show what calibration is worth], [not in the repository], [proposed; contest rules confirmed only through search excerpts],
)

== 0.2 The central scientific question

#caveat[
Can a prior learned from the temporal drift of a specific RF array reduce the number of
*new* physical measurements needed to recover that array's state, while reaching the same
final calibration accuracy, and therefore the same RF performance, as a conventional
recalibration from scratch?
]

This is decision 0002, point 1, written in the vocabulary of this document. In the repository
it appears as experiment EXP-015 and specification ML-B in
`docs/architecture/ml-calibration.md` section 6.

The figure of merit is a count, not an accuracy:

$ M_"required"( "method" ) = min lr(\{ k thick colon thick op("Pr") lr(( Delta ( vb(H)_t ) lt.eq delta thin mid(|) thin y_(1 colon k) \, vb(x)_(1 colon k) \, cal(D) )) gt.eq 1 - alpha \}) $

#table(
  columns: (auto, 6.7fr, 1.8fr),
  table.header([Symbol], [Meaning], [Unit]),
  [$k$], [number of *new* physical measurements taken in this recalibration session], [count],
  [$vb(H)_t$], [the true array state, unknown; the probability is taken over its posterior after the $k$ measurements], [complex, dimensionless],
  [$Delta ( vb(H)_t )$], [the error the beam chosen from the current estimate would have if the true state were $vb(H)_t$: pointing error in the repository; null depth or a sensing figure in the demonstrator], [deg, or dB],
  [$delta$], [the target value of $Delta$], [as $Delta$],
  [$alpha$], [accepted risk of missing the target], [dimensionless],
  [$y_(1 : k)$, $vb(x)_(1 : k)$], [the readings and the commanded beam states that produced them], [V or complex; 16 bit words],
  [$cal(D)$], [the array's history: earlier calibrations, times, temperatures], [data],
)

This is the stopping rule of `docs/mathematics/inverse-calibration.md` section 3.1. A
"measurement" here means one commanded beam state, applied, settled and read once, with a
fixed integration time per reading. Fixing the integration time matters: without it, a
method could appear to need fewer measurements simply by averaging each one longer.

Why a count, and not "how accurately does the model predict the drift"? Because the scarce
resource is physical. A measurement means applying a state, waiting for it to settle and taking
a noisy reading, at the analyser or through the detector; the computation afterwards takes
milliseconds (`benchmarks/metrics.md` section 3). A drift model can predict well and still save
nothing, if the measurements needed to confirm its prediction are as many as those needed to
estimate the state without it. $M_"required"$ measures the saving directly, and it is
falsifiable: if the history carries no information, the method and the from scratch baseline
need the same $k$.

*Two parameters of this definition are not yet fixed.* No numeric pointing target $delta$
exists anywhere in the repository; decision 0007 says so explicitly and refuses to invent one.
And no value of $alpha$ is recorded. Both must be written down, with their reasoning, before
EXP-015 runs. For the demonstrator, $Delta$ would more naturally be a null depth or a signal to
interference ratio, and the same rule applies: the target is fixed before the data.

== 0.3 Why the project exists: the commanded beam is not the real beam

A beamformer is commanded with a vector of complex weights, one per channel. What the hardware
actually applies is different, and the difference changes with time:

$ vb(w)_"real"( t ) = vb(H)_t thin vb(w)_"cmd" $

#table(
  columns: (auto, 4.6fr),
  table.header([Symbol], [Meaning]),
  [$vb(w)_"cmd" in bb(C)^N$], [the weights the controller asks for: amplitude and phase per channel],
  [$vb(w)_"real"( t ) in bb(C)^N$], [the weights the RF hardware really applies at time $t$],
  [$vb(H)_t in bb(C)^(N times N)$], [the array state: per channel gain and phase errors on the diagonal, coupling between channels off it],
  [$N$], [number of channels, 4 for Rev A],
)

The repository writes the same relation as $vb(y) = vb(H) vb(x)$
(`docs/mathematics/formulation.md` section 5). $vb(H)_t$ collects many physical effects:
different cable and trace lengths, component tolerances, switch path differences, printed
circuit board permittivity varying from place to place and from one order to the next, the
coupling of each antenna to its neighbours, and slow changes with temperature, time and
handling. If $vb(H)_t$ were the identity, the array would do exactly what theory says. It
never is.

The consequences are visible and practical:

- the main beam points in the wrong direction;
- the gain in the wanted direction falls;
- the nulls, the directions of near total cancellation used to reject interference, fill in;
- the sidelobes rise;
- a pattern used as a sensing signature changes even though the environment did not;
- a calibration done yesterday becomes wrong today, because $vb(H)_t$ has moved.

Calibration means estimating $vb(H)_t$ and correcting the command. Each estimate costs
measurements, and since $vb(H)_t$ drifts, the cost recurs. That recurring cost is the
object of the research.

== 0.4 Three layers

#diagram[
#image("../figures/mermaid/diagram-04-three-layers.svg", width: 100%)
]

*Layer 1* is hardware and measurement: what exists to be calibrated and how it is observed.
*Layer 2* is the research: the array state, the inverse problem, the temporal prior and the
measurement count. *Layer 3* is a demonstration: it uses the calibrated array for adaptive
reception and sensing, and it makes the value of calibration visible as a null that fills in
when the hardware drifts and comes back when the array is recalibrated. Layer 3 is a way of
showing layer 2, and it must not redefine it. In particular, the demonstrator does not turn the
project into "machine learning beamforming": beam synthesis on Rev A is an exact enumeration
(section 38), and the learned component stays a prior over drift. Figure 19 in section 10bis.7
shows the same structure from the ISAC side: one aperture, two functions, one calibration layer.

== 0.5 Where the project stands, in one paragraph

Nine decisions are accepted (Appendix G). The Rev A beamformer schematic is captured in KiCad
by a generator script and passes its electrical rule check, but its control interface must be
re-captured for the DE1-SoC controller. The stack-up is chosen. The first full wave
simulation, SIM-001, a 50 ohm microstrip line, is fully specified and its model builder and
analysis script exist, but its first execution on 2026-10-03 failed before any geometry was
created, because AEDT Student opened no scripting session; *no solver result exists*. The
analyser audit, EXP-004, has fixed the working frequency from direct bench observation but
still lacks the exact instrument model, the calibration kit and the option list. The
acquisition experiment EXP-005 Phase A is ready to run on owned hardware and has not been run.
Nothing has been purchased or fabricated. No gateware exists. The `rfkit` library and its 160
tests run on synthetic data only. The learning track is formalised and entirely unimplemented,
and it depends on gate G2, whether drift exceeds the measurement floor, which can only be
answered on the built array. Part X gives the full status matrix with evidence.
