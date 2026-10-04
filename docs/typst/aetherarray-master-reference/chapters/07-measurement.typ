#import "../template.typ": *

= Part VII. Measurement and experimental method <part-vii-measurement-and-experimental-method>

== 34\. Evidence hierarchy

The repository uses several vocabularies for evidence, each introduced where it was needed.
Together they form one discipline: never let a weaker kind of evidence be read as a stronger one.

#table(
  columns: (56pt, 3.8fr, 4.8fr, 4.0fr),
  table.header([Vocabulary], [Classes], [Where defined], [What it prevents]),
  [confidence markers], [`[established]`, `[assumed]`, `[to verify]`], [`CONVENTIONS.md` section 3], [an assumption hardening into a fact by repetition],
  [instrument evidence], [`[observed]` with a date, `[inventory]`, `[vendor]`, `[listing]`], [`docs/hardware/measurement-bench.md` section 1], [a measurement plan built on an instrument nobody has seen],
  [material values], [`guaranteed`, `typical`, `nominal`, `assumed`, `unbounded`], [decision 0009; the canonical stack-up], [a typical value used as a tolerance; a guessed tolerance given a number],
  [thresholds], [`provisional-theory-derived`, `unresolved`, `not-a-limit`], [decision 0007; `rfkit.thresholds`], [a tool printing PASS against a number nobody derived],
  [data provenance], [source label on every trace, including `synthetic`], [`rfkit.provenance`], [synthetic test data read later as a measurement],
  [task readiness], [`NOT READY`, `BLOCKED`, `READY`, `DONE`], [`docs/runbooks/README.md`], [a school task attempted without a procedure],
  [experiment state], [planned, running, to do; results cells `to measure`], [`experiments/`, `results/`], [an empty cell being filled with a plausible number],
)

Read as a hierarchy of strength, for a question of fact about this project's hardware:

```text
 strongest   measured on project hardware, calibrated, repeated          none yet
             observed directly on the bench, dated                       the analyser's capabilities, 2026-09-20
             simulated on the actual geometry, converged, checked        none yet
             vendor documentation for the exact part or model            PE4259, AD8318, MCP9808, DE1-SoC, laminates
             analytical computation from documented inputs               seeds, budgets, sensitivity tables
             listing or secondary source                                 ZVL calibration methods, dynamic range
             inference or engineering judgement, labelled                local converter precaution, keep-out margin
 weakest     unverified                                                  data rates of an unattended rig
```

The ordering depends on the question. Decision 0004 made the point explicitly: for "can this
instrument reach 2.44 GHz and measure a complex $S_21$", a bench observation is stronger than a
datasheet, because a datasheet describes a model family and the observation describes the unit in
the room. For "how accurately does it measure", the datasheet of the identified model and a
calibration are what count.

== 35\. EXP-004: the analyser audit

=== 35.1 What has to be known

#table(
  columns: (auto, 1.8fr, 2.5fr, 4.3fr),
  table.header([Observation], [What it is], [Reading on 2026-09-20], [What it decides now]),
  [O1], [manufacturer, model, serial], [Rohde and Schwarz ZVL; *exact model and serial not read*], [provenance and every accuracy figure; the one reading that could still reopen the frequency, if the model were specified below 2.44 GHz],
  [O2], [maximum frequency], [3 GHz, pass], [the frequency; closed],
  [O3], [minimum frequency], [9 kHz, pass], [headroom; closed],
  [O4], [transmission measurement], [$S_21$ available, pass], [gate G1; closed],
  [O5], [complex formats], [available, pass], [gate G1; closed],
  [O6], [source power], [capability up to 0 dBm; *level to be used not recorded*], [a procedure parameter],
  [O7], [calibration kit and connectors], [N female ports; *no kit, no adapter confirmed*], [calibrated validation of any board; the most consequential gap],
  [O8], [time domain option], [*not taken*], [the echo strategy for EXP-005; not a gate],
  [O9], [remote interface], [USB present; *enumeration not verified*], [automation for EXP-014; not a gate],
)

Source: `results/EXP-004/README.md`, result 2: four observations complete, four partial, one not
taken. Runbook SCH-001 is READY and finishes them in about 30 minutes at the bench. Result 1 is
a negative result worth recording: no local evidence on the project computer identifies any
instrument, because none has ever been plugged into it.

=== 35.2 Why the frequency could be fixed before the model was identified

Decision 0004 fixed $f_0 = 2.44$ GHz on 2026-09-23 from the bench observation alone, and recorded
why the earlier logic, which held the frequency open until the exact model was read, was wrong.
Two questions had been merged: whether the instrument can do something, which an observation
answers best, and how well it does it, which needs the datasheet and a calibration. Only the
first gates design; the second gates validation.

The regulatory side was settled from the primary source \[#link(<ref-R1>)[R1]\]: band 57a, 2400 to 2483.5 MHz,
allows 10 mW equivalent isotropic radiated power with no duty cycle restriction, which is what a
swept measurement needs; every sub-band between 863 and 870 MHz requires a duty cycle limit or a
spectrum access technique. With a 2 dBi probe, the observed 0 dBm source ceiling keeps the
radiated level about 8 dB below the limit, so compliance is guaranteed by the instrument rather
than by the operator. The national table of frequency allocations, which may be more restrictive
than the European instrument, has not been checked; it is a `LOCAL` lookup in the register.

== 36\. EXP-005: the repeatability floor, and whether the control path disturbs it

=== 36.1 Three things called noise

#table(
  columns: (1.8fr, 3.6fr, 6.4fr),
  table.header([Quantity], [What it is], [What it does to calibration]),
  [ordinary measurement noise], [random scatter from sample to sample], [sets the floor; averaging reduces it],
  [environmental drift], [slow movement of the mean with temperature, time, handling], [slow enough to track; the subject of EXP-010],
  [*state correlated error*], [a shift of the reading that depends on *which beam state was commanded*], [*does not look like noise*. It looks like a property of the array, so the calibration absorbs it faithfully and reports a hardware coefficient that does not exist],
)

The third is why the quiet window (requirement R9) and the local converter (open item H3) exist,
and both were adopted in decision 0005 as precautions. EXP-005 decides them by measurement.

=== 36.2 Phase A, executable now

Phase A needs no detector. It concerns the acquisition path, and a stable direct voltage stands in
for the detector's output with the advantage that its true value is constant, so any state
correlated change is unambiguously the path.

#table(
  columns: (auto, 9.8fr),
  table.header([Element], [Specification]),
  [apparatus], [two owned DE1-SoC boards: board 1 drives a ribbon and converts the far path, board 2 converts a local path with a short lead. Same converter type on both, so the only difference is the cable],
  [source S1], [0.4 V to 2.2 V, near 1.2 V; stable to 0.2 mV over about 60 s; 100 ohm or less source impedance; not a DE1-SoC rail],
  [conditions], [C1 static; C2 lines toggling during conversion; C3 the quiet window; C4 the temperature bus only; C5, optional, quiet window plus a ground strap],
  [beam state set], [16 words: eight single bit patterns, then eight from a fixed seed written into the protocol],
  [interleaving], [conditions interleaved in every cycle, never blocked, so slow drift cancels in the contrasts],
  [counts], [1000 samples per state per condition per cycle, 16 states, 20 cycles; a settling sweep from 1 us to 10 ms; at least 5 ribbon replugs; at least 3 sessions on different days],
)

The state correlated error is the part of the between state spread that within state noise does
not explain:

$ e_"state" = sqrt(max lr(( 0 \, thick sigma_"between"^2 - frac(sigma_"within"^2, m) ))) $

#table(
  columns: (auto, 2.3fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$sigma_"between"$], [standard deviation of the per state means], [mV],
  [$sigma_"within"$], [pooled standard deviation inside a state], [mV],
  [$m$], [samples per state, 1000], [count],
)

Subtracting $sigma_"within"^2 \/ m$ matters: with finite samples the per state means scatter
even when nothing depends on the state, and reporting that scatter as an effect would manufacture
one.

=== 36.3 The threshold, and what kind of number it is

The decision threshold is *0.5 mV, 0.02 dB at the detector slope*. It is a design judgement, not
a law of physics: it is one fifth of a 0.1 dB drift signal, so an acquisition path contributing
less than this cannot dominate what the drift experiment tries to see, and it is small against the
detector's own $plus.minus 0.5$ dB temperature figure. Its validity rests on the drift signal being of
order 0.1 dB, which is itself unmeasured.

Rules, fixed before any measurement (EXP-005 section 7), after four validity preconditions V1 to V4
(codes dither; within state spread of the local path at most 2 mV; source drift within a cycle at
most 0.5 mV; the two paths agree at rest within 3 mV):

#table(
  columns: (2.0fr, 12.5fr),
  table.header([Question], [Outcomes]),
  [R9, the quiet window, on the far path], [demote if C2 shows at most 0.5 mV; keep provisionally between 0.5 and 1.0 mV; keep, justified, if C2 exceeds 1.0 mV and C3 is at most 0.5 mV; *escalate*, reopening decision 0005, if C3 exceeds 0.5 mV whatever C2 shows],
  [H3, the local converter, in C3], [demote if the far path's within state spread is at most 1.2 times the local one, its state correlated error at most 0.5 mV, and its reconnection shift within 0.5 mV of the local one; keep, justified, if the spread exceeds twice the local one or the error exceeds 1.0 mV; otherwise keep provisionally],
  [C4, the temperature bus], [above 0.5 mV makes scheduling sensor reads outside the window mandatory],
  [C5, the ground strap], [a difference from C3 above 0.5 mV upgrades H5 to a measured requirement],
)

=== 36.4 Status

*Not executed.* Condition C1 has not been run; every result cell reads `to measure`. Item B1,
the analogue input header and the circuit in front of the converter, is advanced but not closed;
item B2, the converter example to use, is not chosen; the harness is not built
(`results/EXP-005/README.md`). Phase B, the original question of whether received power can be
measured repeatably in the room, needs a detector, antennas and interconnect, none owned, and its
decision rules for both routes have not been written; it is gate F3 of decision 0006.

== 37\. The future drift experiment

The learning track needs data that only a fabricated array can produce: the drift of its own
switches, lines, connectors and antennas over time. Three planned experiments supply it.

#table(
  columns: (auto, 3.9fr, 8.9fr),
  table.header([Experiment], [Question], [State of its protocol]),
  [EXP-010], [how long does a calibration stay valid?], [not detailed; "little work but a lot of calendar time"; gates EXP-014 and EXP-015 (`experiments/plan.md`)],
  [EXP-014], [can the array calibrate itself repeatedly, unattended, for weeks?], [method and record schema fixed; criterion: a full classical calibration completes unattended, repeatedly, with session to session spread at or below the EXP-005 floor],
  [EXP-015], [does a learned prior recalibrate with fewer measurements than from scratch?], [specification ML-B; failure declared if the required count is not below the from scratch count on held out sessions, or if G2 has failed],
)

The record schema of `docs/architecture/control-architecture.md` section 6 is the contract for
that data. Every measurement writes: session identifier; sequence index; commanded and read back
beam state words; strobe and conversion timestamps from one clock; the settling delay applied; raw
converter counts; the converter reference and channel; the phase network, detector and die
temperatures; gateware and software versions; the connector handling flag; and the analyser state
when it was used. A field not captured is absent, not defaulted. Three are easy to omit and
expensive to lose: raw counts, from which the noise model is estimated; the read back word; and
the version fields, without which a timing change between sessions is invisible.

What the repository does not yet fix, and this document does not invent: the duration of a
campaign, the schedule of full calibrations against cheap ones, whether temperature is varied
deliberately or left to the room, the label's reference plane (section 16), and the session rate.
The rate of about 100 labelled recalibration pairs per week is an *unverified estimate* from an
assumed ten minute cycle (decision 0002).

#aa-figure(num: "14", caption: [measurement roadmap and its gates, from `docs/runbooks/register.md`, decision 0006 and
`experiments/plan.md`.])[
#image("../figures/mermaid/figure-14.svg", width: 100%)
]
