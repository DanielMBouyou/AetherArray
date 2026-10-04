#import "../template.typ": *

= Part XIV. Why this project is useful <part-xiv-why-this-project-is-useful>

== 64\. Educational usefulness

AetherArray puts, in one object small enough to understand completely, most of what an RF
engineer has to learn: electromagnetic waves and transmission lines, microwave circuits and
S-parameters, antenna design, phased array theory, PCB stack-up and fabrication tolerance, digital
control and FPGA timing, metrology and calibration, signal processing, estimation and Bayesian
inference, and the software discipline of reproducible work. Each topic appears because the
project needs it, not because a syllabus lists it, and each has a concrete number attached: 8.6 mm
for 45 degrees, 2.29 degrees for an acceptance limit, 0.5 mV for a state correlated error. Every
decision is written down with its alternatives, so a student can see not only what was chosen but
why the obvious alternative was not.

== 65\. Research usefulness

The useful scientific object is not a four element antenna; it is a *controlled physical
platform* on which these questions can be studied with ground truth:

- how calibration accuracy trades against the number of physical measurements;
- how a real, cheap RF array drifts with time and temperature, outside a climate chamber;
- how an inverse problem with an explicit forward model behaves on real hardware, power only and
  complex;
- how measurement design, choosing what to measure next, changes the count;
- whether a learned prior, kept inside a physical inverse problem, earns its place.

== 66\. Industrial relevance, without overclaiming

The same problems appear, at much larger scale and with different hardware, in wireless devices,
cellular base stations, satellite terminals, radar, RF production test and adaptive antennas:
channels drift, calibration costs time and equipment, and arrays are recalibrated in the field.
AetherArray is *not* equivalent to any production system. Industrial arrays use integrated
beamformers, active modules with amplifiers, thermal management, factory calibration in chambers
and proprietary built in calibration paths, at hundreds or thousands of channels. What carries over
is method: the separation of state estimation from beam synthesis, the counting of measurements,
pre-registered acceptance rules, and a candid account of which errors calibration can and cannot
absorb.

== 67\. Why not simulate everything?

Because a simulator reproduces what it was told (decision 0001, known limitations). Real hardware
contains manufacturing tolerances, a laminate from an unspecified brand, glass weave under a
0.37 mm line, connector repeatability, thermal drift, switch nonidealities, measurement noise and
coupling paths nobody modelled. The questions this project asks, how a real array drifts and
whether its history helps recalibrate it, have no answer inside a simulator, because the drift
statistics are exactly what a simulator would have to be given. The physical Rev A exists to supply
them.

== 68\. Why not measure everything every time?

Because the cost of measurement is the problem being studied. On four channels a full calibration
is a dozen readings; on hundreds of channels, repeated in the field, measurement count and
calibration time become expensive in downtime, equipment and energy. If a learned prior can restore
the same accuracy with fewer new measurements, that saving recurs at every recalibration for the
life of the array. Whether it can, on real hardware, is the experiment.
