#import "../template.typ": *

= Part XXI. One page synthesis <part-xxi-one-page-synthesis>

*1. What are we building?* A four element, 2.44 GHz phased array with three bit switched line
phase control: a passive antenna board, a beamformer board with 29 RF switches, a Wilkinson
combiner, an analyser port and an on board power detector, driven by an external DE1-SoC whose FPGA
applies beam states deterministically. It is designed, its schematic is captured, and nothing is
built.

*2. What scientific question are we asking?* Whether a prior learned from the array's own drift
history lets it be recalibrated with fewer new physical measurements than calibrating from scratch,
at the same final accuracy. The figure of merit is $M_"required"$, a count of measurements.

*3. Why four elements?* Because four is the smallest array where the learning question has room
(two elements leave two parameters), because every state can be enumerated, and because it fits
the budget. It is a research instrument, not a demonstration of scale; scaling to larger arrays
would be studied in simulation, parameterised by what four channels measure.

*4. Why an FPGA?* Not to form beams, which an analogue array does without one, but to make the
measurement deterministic: all sixteen lines on one clock edge, a fixed settling delay, control
lines silent while sampling, one clock for every timestamp. A state correlated error would
otherwise imitate a calibration coefficient.

*5. Why HFSS, ADS and a VNA?* Because each catches errors the others cannot: HFSS solves the real
geometry, a circuit model provides an independent model form, and the analyser measures reality at
calibrated planes. Their agreement, judged by rules fixed before the data, is the evidence.

*6. Why machine learning?* Only for what physics cannot supply: the temporal structure of this
array's drift. The likelihood stays physical; beam selection stays exact. At $N = 4$, learning cannot
honestly reduce first calibration counts, so the claim is restricted to recalibration.

*7. What does the AP-S demonstrator add?* A narrow but genuine form of ISAC, one receive aperture
shared between interference rejection and opportunistic sensing (section 10bis), in which
calibration's value is visible to anyone:
a null on an interferer that fills when the hardware drifts and returns when the array is
recalibrated, with the measurement count shown, plus sensing that is only trustworthy on calibrated
hardware. It tests the idea in public; it does not change the research question.

*8. What has actually been completed?* Nine decisions; the stack-up; the schematic of the RF design;
the acceptance budget and the coupling test, both written before any data; the RF data layer and its
160 tests on synthetic data; the SIM-001 model builder and analysis; one school runbook; the frequency
fixed from a bench observation. No simulation result, no hardware, no measurement, no model.

*9. What is the immediate next task?* In parallel: open AEDT Student once by hand and run SIM-001;
make the SCH-001 bench visit; run condition C1 of EXP-005; read the PE4259 datasheet by hand; build
the array simulator EXP-001; and, if the contest is pursued, read the official call in full and
record a decision.

*10. What result would make AetherArray scientifically successful?* A measured curve, over held out
sessions on real hardware, showing that the learned prior reaches the same final accuracy as a full
recalibration with measurably fewer new measurements than both the from scratch baseline and the non
learned temporal baseline; or, equally valuable, a clean demonstration that it does not, with the
reason. Along the way: a measured drift and calibration lifetime for a low cost array outside a
climate chamber, and simulated against measured coupling, both of which the literature rarely
reports.
