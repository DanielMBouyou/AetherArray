#import "../template.typ": *

= Part III. What exactly is being built <part-iii-what-exactly-is-being-built>

=== III.1 The complete Rev A system

#aa-figure(num: "1", caption: [the Rev A system as specified on 2026-10-04. Sources: decision 0003, the schematic in
`hardware/rev-a/`, decision 0005 and `docs/architecture/control-architecture.md`. The ribbon,
the registered buffers and the converter are specified but not yet drawn in the schematic.])[
```text
 ANTENNA BOARD (2-layer FR-4, 1.6 mm)            BEAMFORMER BOARD (4-layer FR-4, JLC04161H-7628)
 patches not yet designed                       schematic captured (control section to re-capture)

 patch 0 -- SMA ==jumper 0==> J900 --[EN0]--[45]--[90]--[180]--+
 patch 1 -- SMA ==jumper 1==> J901 --[EN1]--[45]--[90]--[180]--+--[ 4-way Wilkinson, ]-- J904 common port
 patch 2 -- SMA ==jumper 2==> J902 --[EN2]--[45]--[90]--[180]--+  [ three stages,    ]        |
 patch 3 -- SMA ==jumper 3==> J903 --[EN3]--[45]--[90]--[180]--+  [ 70.7 ohm arms    ]   U900 path select
                                                                                       /            \
            every [ ] is one PE4259-63 SPDT, or a pair of them for a bit         analyser port      U901 AD8318
            EN: throw 1 -> phase chain, throw 2 -> 50 ohm termination            (complex S21)      log detector
                                                                                                         |
            MCP9808 0x18 beside the phase network, 0x19 beside the detector                       converter (H3)
                                                                                                         |
            ribbon cable, 2x20 planned: 16 beam state lines + STROBE + MON_SEL + SPI + I2C + 5 V + 3V3 + grounds
                                                                 |
 EXTERNAL DE1-SoC                                                v
   FPGA fabric: beam state register, sequencer, trigger, timestamp counter, SPI and I2C masters, record FIFO
   HPS (ARM processor): orchestration, storage, posterior update, choice of next measurement
                                                                 |
 PC (optional): training the drift prior, analysis, figures
```
]

=== III.2 Which way the signal goes

The schematic is drawn for transmit: a signal entering the common port $J 904$ is divided by the
Wilkinson network into four channels and leaves at the element ports $J 900$ to $J 903$
(`hardware/rev-a/README.md`). The RF path contains only switches, printed lines, resistors and
the Wilkinson network, no amplifier, so it is expected to behave identically in both directions
at the low power levels used *\[assumed\]*; that is what lets a transmit style characterisation
describe a receiving array. Reciprocity is not assumed for the AD8318, which is an active
detector placed only at the common port and used only as a receiver.

Four measurement configurations follow (`docs/architecture/rev-a-rf-architecture.md` section
5.3; `docs/hardware/measurement-bench.md` section 4):

#table(
  columns: (70pt, 6.2fr, 4.7fr, 2.7fr),
  table.header([Configuration], [Path], [What it gives], [Attended]),
  [conducted, per channel], [analyser between the common port and one element port, that channel enabled, the others terminated], [the complex transfer of one beamformer channel], [no handling once cabled; per channel isolation is electronic],
  [radiated receive], [analyser port 1 drives a probe antenna in the far field; the array receives; the common port goes to analyser port 2], [the complex response of the whole array, antennas and jumpers included, for any commanded state], [unattended once set up],
  [power only receive], [as above, but the common port switched by $U 900$ to the AD8318], [scalar received power for any commanded state, read by the controller], [unattended, without occupying the analyser],
  [element to element], [jumpers removed on a pair; analyser across two element connectors; other elements terminated], [the coupling between two antennas, toward $vb(S)_A$], [needs recabling],
)

The AP-S demonstrator (Part IX) would use the array in the third configuration, with ambient
commercial transmitters in place of the probe, and possibly a channel selective receiver in
place of the detector (section 47).

== 14\. Why two boards?

Decision 0003 made Rev A two boards; decision 0009 gave them two different constructions.

#table(
  columns: (60pt, 13.2fr),
  table.header([Reason], [Explanation]),
  [per element access, requirements R1 and R2], [every element has its own connector, so each element can be measured alone, the coupling between any two can be measured, and the mutual coupling calibration method B6 \[#link(<ref-A7>)[A7]\] remains possible. An integrated splitter would close all three permanently (`docs/hardware/rev-a-requirements.md` section 3)],
  [substrate physics], [the switched lines need a thin dielectric and an inner ground; the patches need a thick one. A factor of about seven in patch bandwidth and five in efficiency separates them (section 6.4)],
  [control routing], [the beamformer needs an inner plane so the beam state lines of decision 0005 can cross under RF lines without cutting the RF ground],
  [replaceable antennas], [the beamformer board survives a change of antenna geometry, of frequency or of element type; a missed patch resonance costs an antenna board, not the whole system],
  [fabrication risk], [decision 0009 expects a second antenna board order may be needed; the expensive, dense board is not affected],
  [native experiments], [the four jumpers make the known cable error experiment EXP-007 and the reconnection sensitivity metric natural rather than contrived],
)

The price is real: eight connectors and four cables add loss and add drift sources. That drift
is inside what EXP-010 measures; it is at least observable rather than hidden
(`docs/architecture/rev-a-rf-architecture.md` section 5.2).

== 15\. Beamformer channels

=== 15.1 What each channel contains

#table(
  columns: (auto, 3.3fr, 2.6fr),
  table.header([Stage], [Parts], [Function]),
  [enable], [one PE4259-63: throw 1 to the phase chain, throw 2 to a 50 ohm termination], [pass the channel, or terminate it so it can be excluded electronically],
  [45 degree bit], [two PE4259-63 and two printed arms], [select the reference or the delay arm],
  [90 degree bit], [two PE4259-63 and two printed arms], [as above],
  [180 degree bit], [two PE4259-63 and two printed arms], [as above],
)

Seven switches per channel, 28 for four channels, plus $U 900$, the path selector at the common
node, added during capture: 29 PE4259-63 in all (`hardware/rev-a/README.md`). One control line
drives both switches of a bit, so the channel takes four control lines and the array sixteen.

=== 15.2 The switched line principle

#aa-figure(num: "5", caption: [one switched line bit. Two single pole double throw (SPDT) switches route the signal
through one of two printed arms; the difference of their electrical lengths is the bit.])[
```text
                       reference arm  (electrical length theta_ref)
                  +----------------------------------------+
    in -- RFC [SPDT A]                                  [SPDT B] RFC -- out
                  +---------- delay arm ---------------------+
                       (electrical length theta_ref + theta_bit)

    control = 0 : both SPDTs select the reference arm   ->  phase  -theta_ref
    control = 1 : both SPDTs select the delay arm       ->  phase  -theta_ref - theta_bit

    designed quantity:  theta_delay - theta_ref = theta_bit = 45, 90 or 180 degrees at f0,
    measured between the RF ports of SPDT A and SPDT B (layout-constraints.md section 2)
```
]

An SPDT switch connects its common port (RFC) to one of two throws. Two of them, facing each
other, select one of two paths. The phase difference between the paths is $beta thin Delta l$
(section 1.6). Three bits in cascade give the eight states of section 8.

=== 15.3 What the realised phase depends on

The analytical difference lengths of decision 0009 are 8.6, 17.2 and 34.4 mm for the 45, 90 and
180 degree bits on the beamformer construction *\[analytical, INITIALISATION ONLY\]*. They are
seeds, not layout values, because the realised phase difference depends on more than a straight
line length:

#table(
  columns: (2.1fr, 7.3fr),
  table.header([Factor], [Effect]),
  [effective permittivity], [sets $lambda_g$; known a priori only to an assumed $plus.minus 0.2$ on $epsilon_r$ (section 59)],
  [frequency], [a fixed length is a time delay; 5.6 degrees on the 315 degree state at the upper band edge (section 8.5)],
  [bends and meanders], [a 34 mm arm will not be straight; corners and closely spaced meander turns change the effective length and couple to themselves],
  [discontinuities], [pads, width steps and the transition into each switch add reactance that differs between arms if their routing differs],
  [switch package and parasitics], [each SPDT adds its own insertion phase and loss; if its two throws differ, that difference enters the bit],
  [launch and reference planes], [the bit is defined between the switch RF ports, not between connectors],
  [line width], [changes $Z_0$ and $epsilon_"eff"$ together; a width tolerance of $plus.minus 20$ per cent is guaranteed by the fabricator \[V11\]],
  [loss], [the longer arm is lossier, so each bit also changes amplitude: the state dependent loss of section 59],
)

Two further hazards are specific to switched lines with finite isolation. They are standard
engineering concerns, not repository findings, and both must be checked in simulation
*\[to verify, SIM-003 proposed\]*.

- *Reflections between discontinuities.* Small mismatches at both ends of an arm create a
  standing wave whose effect on the transmitted phase depends on the arm's length, so it differs
  between states: a state dependent error by construction.
- *Resonance of the de-selected arm.* The arm that is not selected is a line held between two
  switch throws in their off state, close to an open circuit at both ends and weakly coupled to
  the through path by the switch's off state isolation. A line open at both ends resonates when
  its electrical length approaches a multiple of half a guided wavelength. The delay arm of the
  180 degree bit is at least half a guided wavelength long, so depending on the reference arm
  length it may sit near such a resonance, producing a sharp, state dependent loss and phase
  excursion in the band. The usual remedies are choosing the reference length to keep both arms
  away from resonance, or splitting the bit.

=== 15.4 The PE4259-63

#table(
  columns: (1.7fr, 3.8fr, 2.3fr),
  table.header([Property], [Value], [Evidence]),
  [function], [SPDT RF switch with integrated CMOS control logic], [*\[vendor\]* V1],
  [frequency range], [10 MHz to 3000 MHz], [*\[vendor\]* V1],
  [insertion loss], [0.35 dB typical at 1000 MHz, 0.5 dB at 2000 MHz], [*\[vendor\]*, typical spot values; nothing at 2.44 GHz],
  [isolation], [30 dB typical at 1000 MHz, 20 dB at 2000 MHz], [*\[vendor\]*, typical; no guaranteed minimum at any frequency (I18)],
  [supply], [1.8 V to 3.3 V], [*\[vendor\]*],
  [package], [SC-70-6, 0.65 mm lead pitch], [*\[vendor\]*],
  [availability], [active, more than 300 000 units in distributor stock, 0.84 USD at one unit, read 2026-09-18], [*\[vendor\]* listing],
  [control thresholds], [*not read*: the datasheet is a scanned image], [open item H1],
  [control polarity], [the single pin truth table, which level selects which throw, *not read*], [firmware inversion constant, decision 0005],
)

The datasheet is a scanned image that could not be read by machine; isolation at 2.44 GHz, the
logic input thresholds and the truth table need a person with the file open
(`experiments/EXP-004-instrument-audit.md`, follow-up).

=== 15.5 Open hardware items H1 to H5

#table(
  columns: (64pt, 3.6fr, 5.1fr, 8.6fr),
  table.header([Item], [Question], [Why it matters], [Closes when]),
  [*H1* logic level compatibility], [does the switch read the buffer's output levels correctly?], [*blocks board release*. A common rail buffer prevents overvoltage but does not prove the switch sees a valid high and low], [the PE4259 input thresholds at the board supply and the selected buffer's guaranteed output levels are recorded with margin; fallback: a level translator specified against a named standard plus a bench measurement of the threshold on a sample (SCH-011)],
  [H2 expansion header supply], [can the DE1-SoC header source about 70 mA at 5 V?], [the detector is 68 of the 69 mA the board draws], [the header current limit is read; otherwise a separate supply, which enlarges H5],
  [H3 converter part], [which converter digitises the detector on the RF board, if any?], [decision 0005 placed it there as a precaution], [EXP-005 Phase A decides whether it stays, then a part is chosen],
  [H4 buffer part], [which registered buffer latches the sixteen lines?], [needed for H1 and for setup and hold times], [a part is selected],
  [H5 ground strategy], [how are the two boards' grounds joined?], [a ribbon between a digital board and a receive chain is a loop], [a decision before layout; EXP-005 condition C5 informs it],
)

Source: `docs/architecture/control-architecture.md` section 8. All five are open on 2026-10-04,
and gate F4 of decision 0006 requires H1 to H4 closed and H5 decided before fabrication.

=== 15.6 The Wilkinson network and the path selector

The four channels meet in a four way Wilkinson network built from three two way stages, each
with two quarter wave arms of 70.7 ohm and a 100 ohm isolation resistor
(`hardware/rev-a/layout-constraints.md` section 3). An ideal Wilkinson stage is matched at all
ports and isolates its two outputs from each other, which keeps the channels from loading one
another. Its seed arm width on the beamformer construction is 0.182 mm *\[analytical\]*, about
twice the 0.09 mm process minimum; an optional coupon C4 checks the etch of that narrowest line.
The common node then passes through $U 900$, which connects it either to the analyser connector
or to the detector, so that neither loads the other; it adds about 0.5 dB to the common arm
*\[estimate\]*.

== 16\. Enable and terminate

Each channel's enable switch either passes the signal into the phase chain or connects the
element port to a 50 ohm termination. That single switch is what makes several experiments
possible without touching a cable.

#table(
  columns: (1.7fr, 6.0fr),
  table.header([Use], [How the enable switch provides it]),
  [isolate one channel], [enable one, terminate three, measure; the per channel label of the learning track is obtained electronically],
  [labels for supervised learning], [the expensive full calibration that supervises the cheap one can run unattended],
  [element by element baseline B2], [the classical method of measuring each channel alone],
  [fault finding], [a dead or misbehaving channel shows up in a single measurement],
  [coupling measurements], [terminated neighbours present a defined 50 ohm load, as EXP-011 requires],
  [binary amplitude], [subsets of channels can be switched on, which adds 308 relative configurations to the 512 (section 8.3)],
)

Two limits must be stated. First, switching channels off is not amplitude control: it cannot
taper the aperture or lower sidelobes in any designed way, and Rev A makes no claim to amplitude
beamforming (decision 0003). Second, a terminated channel is not perfectly silent. Its signal
leaks into the chain through the enable switch's isolation, about 20 dB typical at 2 GHz \[#link(<ref-V1>)[V1]\],
with no value obtained at 2.44 GHz. When one channel is measured at the common port with the
other three terminated, their leakage adds to it; EXP-004 gives the residual as $sqrt(3) dot.op 10^(- I \/ 20)$ for random relative phases and $3 dot.op 10^(- I \/ 20)$ when the three add coherently, for
isolation $I$ in dB *\[analytical\]*:

#table(
  columns: (auto, 1.4fr, 1.4fr, auto, 1.4fr),
  table.header([Isolation $I$], [Residual, random phases], [Amplitude error], [Phase error], [Residual, coherent worst case]),
  [20 dB], [$- 15.2$ dB], [17 per cent], [10 degrees], [$- 10.5$ dB],
  [25 dB], [$- 20.2$ dB], [10 per cent], [6 degrees], [$- 15.5$ dB],
  [30 dB], [$- 25.2$ dB], [5 per cent], [3 degrees], [$- 20.5$ dB],
)

This degrades per channel measurements *taken at the common port*, the B2 baseline. It does
not degrade a conducted measurement between the common port and the enabled channel's own
element port, because the other channels' signals do not reach that port. It does not affect REV
either, which never switches channels off. Which reference plane the learning labels use is
therefore a real design choice; the repository leans on the conducted route but does not fix it
in one place (Appendix J).

== 17\. The RF detector

=== 17.1 What a logarithmic detector does

The AD8318 converts RF power at its input into a DC voltage proportional to the power in
decibels. Over its accurate range:

$ V_"out" approx s lr(( P_"dBm" - P_"icpt" )) , wide s approx - 25 space "mV/dB" $

#table(
  columns: (auto, 3.8fr, auto),
  table.header([Symbol], [Meaning], [Unit]),
  [$V_"out"$], [detector output voltage, about 0.4 V to 2.2 V over the usable range], [V],
  [$s$], [logarithmic slope, nominally $- 25$ mV/dB, negative: more power gives less voltage], [V/dB],
  [$P_"dBm"$], [input power], [dBm],
  [$P_"icpt"$], [intercept, a constant of the part and of the frequency], [dBm],
)

The vendor specifies 1 MHz to 8 GHz, $plus.minus 1$ dB conformance over a 55 dB range below 5.8 GHz,
$plus.minus 0.5$ dB stability over temperature across its full range, and a single 5 V supply at about
68 mA \[#link(<ref-V6>)[V6]\] *\[vendor\]*. A 0.1 dB change of received power is a 2.5 mV change of output.

=== 17.2 What it cannot do

- *It measures power only.* It returns no phase, so through the detector the array state must
  be inferred from power readings: the phase retrieval problem of section 11.5.
- *It is broadband.* It responds to all power in its range of frequencies. It cannot by itself
  separate a wanted transmitter from an interfering one in the same band, which matters for the
  AP-S communication mode (section 47).
- *Its constants are not known to the needed accuracy.* The slope and intercept vary from unit
  to unit and with frequency and temperature, so the detector must be characterised against the
  analyser used as a stepped source (`docs/hardware/measurement-bench.md` section 4). Its
  temperature drift is corrected empirically against the MCP9808 beside it, which is why that
  sensor is mandatory (requirement R4).

=== 17.3 Why a converter is needed, and where it goes

The FPGA fabric is digital; it cannot sample an analogue voltage. Every analogue quantity
reaches it through an analogue to digital converter (ADC).

#table(
  columns: (2.0fr, 4.6fr, 8.9fr),
  table.header([Option], [Description], [Status]),
  [local converter on the RF board], [a serial ADC beside the detector, read by the fabric over four lines], [*decided as a precaution*, decision 0005 point 2; part not selected (H3); requirement stated as at least 14 effective bits over a 2 V span, so one step is below 0.01 dB],
  [DE1-SoC on board converter, LTC2308], [eight channels, 12 bit, up to 500 ksps, 0 V to 4.096 V input range at the header \[#link(<ref-T6>)[T6]\]], [*kept as an independent path*; it samples a different chain from a different ground reference, so a disagreement between the two paths is informative],
)

The case for the local converter is cost asymmetry, not a demonstrated failure: carrying a
signal where 0.1 dB is 2.5 mV along a ribbon beside sixteen switching lines could pick up
interference *correlated with the commanded state*, which would imitate a calibration
coefficient (section 36). Fitting the converter costs a few euro; omitting it and being wrong
costs a board revision. EXP-005 Phase A turns the argument into a measurement.

An unresolved detail: the LTC2308 has a 2.5 V internal reference, yet the header range is
quoted as 0 V to 4.096 V, which implies some circuit in front of the converter, a divider or an
external reference. Which it is matters for the source impedance the converter sees, and is
item B1 of EXP-005, not yet closed (`results/EXP-005/README.md`, preparation P3).

=== 17.4 Resolution, averaging and dither

A 12 bit converter over 4.096 V has a step of

$ "LSB" = frac(4.096 space "V", 2^12) = 1.0 space "mV" , wide frac(1.0 space "mV", 25 space "mV/dB") = 0.04 space "dB" $

One step is larger than the 0.02 dB effect EXP-005 looks for. Averaging $m$ readings reduces
random noise by $sqrt(m)$, but only if the noise moves the reading across at least one step.
If the input sits still between two codes, every reading returns the same code, and averaging
recovers nothing: the error is a fixed rounding, not noise. That is why EXP-005 has a validity
precondition, V1, that the raw codes of a burst show at least two adjacent distinct values, and
why dither, deliberately added noise, would be required otherwise.

== 18\. Temperature sensors

Two MCP9808 digital sensors sit on the beamformer board: one at I2C address 0x18 beside the
phase network, one at 0x19 beside the detector. The vendor gives about 0.25 degrees Celsius
typical accuracy and 0.0625 degree resolution \[#link(<ref-V5>)[V5]\] *\[vendor\]*. The AD8318 also provides an
analogue die temperature output, read by a converter channel, as a third, independent
temperature.

Nothing in the repository says temperature causes a known correction to the array state; no
coefficient has been measured. Temperature is logged because it is useful in four ways:

#table(
  columns: (1.7fr, 4.0fr),
  table.header([Use], [Why]),
  [covariate], [a drift prior can condition on it: $p ( vb(H)_t divides vb(H)_(t - 1) , T_t , Delta t , dots.h )$],
  [experimental context], [a session is interpretable only with its conditions],
  [potential predictor], [if drift tracks temperature, the prior will learn it; if not, that is a finding],
  [diagnostic], [separates array drift, near 0x18, from detector drift, near 0x19],
)

A temperature reading is taken with every measurement record, not on a separate schedule, and
outside the quiet window of section 19, because an I2C transaction is switching activity on two
more lines of the same cable (`docs/architecture/control-architecture.md` sections 4.2 and 5.1).
Whether temperature enters the first prior model, or only later, is a modelling choice to be
made on data, not now.

== 19\. The DE1-SoC

=== 19.1 What it is

The Terasic DE1-SoC is a development board built around an Intel Cyclone V system on chip. One
chip contains two very different computers:

#table(
  columns: (auto, 7.2fr, 4.9fr),
  table.header([Part], [What it is], [What it is good at]),
  [*FPGA fabric*], [a field programmable gate array: a large array of logic cells and wiring configured into custom digital circuits, which run in parallel on a clock], [deterministic timing: an operation takes exactly the same number of clock cycles every time],
  [*HPS*], [the hard processor system: an ARM processor running ordinary software], [storage, networking, files, floating point computation, everything without a hard deadline],
  [*GPIO*], [two 40 pin expansion headers, 36 user pins each, connected directly to the FPGA at 3.3 V with protection diodes \[#link(<ref-T6>)[T6]\]], [sixteen beam state lines and the rest of the interface],
  [*ADC*], [the LTC2308, reached from the fabric over a four wire serial interface \[#link(<ref-T6>)[T6]\]], [the independent detector path of section 17],
)

Three DE1-SoC boards are owned (`docs/hardware/inventory-and-needs.md`); one is enough for Rev
A, and EXP-005 Phase A uses two.

=== 19.2 Why not a microcontroller alone

Decision 0003 originally specified an STM32G0 microcontroller. Decision 0005 replaced it, and
the reason is the measurement, not the beamforming: an analogue array needs no programmable
logic to form a beam.

#table(
  columns: (3.5fr, 2.3fr, 1.8fr),
  table.header([Requirement of the drift experiment], [Microcontroller], [FPGA fabric]),
  [identical delay between applying a state and sampling, every time], [subject to interrupts and host traffic: it jitters], [an exact number of clock cycles],
  [all sixteen lines change at one instant], [ports written in sequence], [one clock edge],
  [trigger and timestamp from one clock], [usually two clocks], [one free running counter],
  [control lines provably static while sampling], [by convention], [by construction, in the sequencer],
  [unattended sequencing without the host], [limited], [native],
)

Each microcontroller weakness enters the data as scatter correlated with the measurement
sequence, the one kind of error this project cannot tolerate (section 36). The costs are also
recorded: gateware is new work, the board is external so the interface crosses a cable, and the
schematic must be re-captured. If EXP-005 shows the floor is set by the environment rather than
by control timing, decision 0005 allows a fallback to the simpler route for the control path
alone, without touching the RF design.

=== 19.3 The partition

#aa-figure(num: "11", caption: [hardware and software partition. Everything with a deadline is in the fabric;
everything probabilistic is above it (`docs/architecture/control-architecture.md` section 2).])[
#image("../figures/mermaid/figure-11.svg", width: 100%)
]

*Why learning does not run in the FPGA.* Nothing about inference has a hard deadline: a
posterior update over six parameters, or an enumeration of 512 states, takes milliseconds on
the processor, between measurements that take far longer. Putting floating point inference in
fabric would add design effort and risk for no timing benefit. The fabric owns no floating point,
no inference and no storage, by design.

=== 19.4 One measurement, step by step

```text
 time  --->
 HPS / sequencer   load word k+1 into register
 16 data lines     ======X====================================================X==== (static)
 STROBE                   _|^|_                                                         rising edge latches
 RF board buffer          outputs change on STROBE edge, all 16 at once
 settling interval        |<------ N_settle clock cycles, counted at the controller ------>|
 TRIGGER                                                                      _|^|_
 conversion(s)                                                                 [c1][c2]..[cm]
 timestamp                taken at STROBE edge ............................... and at TRIGGER edge
 quiet window             |<========= no control line change, no I2C traffic ===========>|
 I2C temperature read                                                                       [read]
 record                   word, read-back word, both timestamps, settling, raw counts, T, versions
```

_Timing of one sequencer entry (`docs/architecture/control-architecture.md` section 5.1). The
settling interval is counted from the strobe at the controller, so cable and buffer delay lie
inside it on purpose. The value of $N_"settle"$ is set by the settling sweep of EXP-005._

The quiet window, from the strobe edge to the end of the last conversion, forbids any control
line change and any I2C traffic. The I2C clause matters as much as the control line clause,
because an I2C transaction is switching on two more lines of the same cable.

=== 19.5 The 16 bit beam state word

$ b = 4 c + f , wide c in \{ 0 , 1 , 2 , 3 \} , wide f in \{ 0 , 1 , 2 , 3 \} $

Bit $b$ of the word carries field $f$ of channel $c$, with $f$ meaning enable, 45, 90 and 180
in that order. Bits 0 to 3 are channel 0, bits 12 to 15 channel 3. Logical polarity is defined:
a one enables the channel or selects the delay arm. Electrical polarity is not: it depends on
the unread PE4259 truth table and becomes one inversion constant per field in gateware. The
monitor path select $"MON_SEL"$ is a seventeenth line, deliberately outside the word.

=== 19.6 What the read-back proves, and walk one bit bring-up

Each record carries a read-back word. With an ordinary registered buffer, the only word that
can be read is the controller's own output register. That detects a sequencer or software
fault. It does *not* detect a broken conductor, a bad connector contact or an unpowered or
failed buffer: the controller would read back exactly what it intended while the switches never
received it. Detecting those would need sixteen return lines, which the interface does not
carry. Instead, bring-up walks a single bit through all sixteen positions and watches the RF
response change as expected: each bit should toggle exactly one channel's enable or one bit's
phase, and nothing else (`docs/architecture/control-architecture.md` section 5.2).

=== 19.7 What exists

No gateware exists. Quartus 17.1 is installed on the project computer, and no programmer has
ever been attached to it (`results/EXP-005/README.md`, P2). The beam state register, sequencer,
trigger, timestamp counter, serial masters and record FIFO are specified only.

== 20\. Grounding and the digital to RF interface

Connecting an FPGA board by ribbon cable to a board carrying a 2.44 GHz receive chain creates
several coupled problems.

#table(
  columns: (1.3fr, 5.7fr, 4.5fr),
  table.header([Problem], [Mechanism], [Why it matters here]),
  [return currents], [each switching line's current returns through the cable's ground conductors], [with too few or badly placed grounds, return currents share paths with the analogue signal],
  [common impedance], [a shared ground conductor has impedance, so one circuit's current shifts another circuit's reference], [the detector's 2.5 mV per 0.1 dB is easily disturbed],
  [digital noise], [fast edges contain energy far above the clock frequency], [it can couple into the detector input or the analogue lines],
  [ground loops], [the DE1-SoC, the RF board, the analyser and a PC each have a ground; joined at several points they form loops], [loop currents from other equipment add slowly varying offsets],
  [EMI], [the ribbon is an antenna for both the digital edges and the RF], [radiated pickup in the receive chain],
)

The specific danger is not noise in general, which averaging reduces, but noise that depends on
the commanded state, which averaging does not remove and which a calibration absorbs as if it
were a property of the array. The mitigations decided so far are partial: interleaved grounds
in the 2 by 20 connector, a registered buffer at the board edge that restores edges and removes
skew, the quiet window, an unbroken L2 ground beneath every RF trace with digital routing on L3
and L4 (decision 0009), and the converter beside the detector.

*H5, the ground strategy between the two boards, is open.* If the header cannot supply the
board (H2), the board takes its own supply and the question grows. EXP-005 condition C5, a
ground strap between the boards, is designed to show whether the grounding arrangement is a live
variable; if C5 differs from C3 by more than 0.5 mV, H5 becomes a measured requirement rather
than a layout question (`experiments/EXP-005-repeatability-floor.md` section 7.6). No final
ground strategy is claimed here.
