#import "../template.typ": *

= Part IX. The IEEE AP-S 2027 ISAC demonstrator <part-ix-the-ieee-ap-s-2027-isac-demonstrator>

#caveat[
*Status of everything in this part.* The repository contains no decision, experiment or
document about the AP-S Student Design Contest or about integrated sensing and communication.
The demonstrator is *\[proposed here\]*, from the project owner's brief. The contest facts below
were researched on 2026-10-04 from official IEEE pages, but the environment this document was
written in could not open them: its network policy refused connections to `ieeeaps.org` and
`2027.apsursi.org`. Every contest fact is therefore *\[snippet only\]*: read in search engine
excerpts of the official pages, consistent across many independent queries, and *not yet
checked against the full call*. Quoted wording is near verbatim as indexed. Before the proposal
is written, the official call \[#link(<ref-P2>)[P2]\] must be read in full and this part corrected against it.
]

== 45\. The official challenge

=== 45.1 What the 2027 contest asks for

#table(
  columns: (64pt, 14.5fr, auto),
  table.header([Item], [Official requirement, as indexed], [Source]),
  [edition and title], [the 18th IEEE AP-S Student Design Contest; topic "Reconfigurable Receiving Antennas for Integrated Sensing and Communications (ISAC)"], [\[#link(<ref-P1>)[P1]\], \[#link(<ref-P2>)[P2]\]],
  [challenge], ["design a dual-mode, reconfigurable receiving antenna system for ISAC that utilizes unmodified, commercial off-the-shelf (COTS) transmitters, such as Wi-Fi routers or Bluetooth beacons, as ambient signal sources, propose a setup to demonstrate its utility, and provide educational material to explain it"], [\[#link(<ref-P1>)[P1]\]],
  [receive only], ["the student-designed hardware must operate as a receiver"], [\[#link(<ref-P1>)[P1]\]],
  [two modes], ["The antenna system must dynamically switch between sensing and communication modes"], [\[#link(<ref-P1>)[P1]\]],
  [sensing mode], [ambient signals as "illuminators of opportunity"; with "a basic signal-processing backend, the antenna must optimize its characteristics to detect or track environmental changes, such as human movement or object positioning"], [\[#link(<ref-P1>)[P1]\]],
  [communication mode], ["establishing a robust data link with a specified COTS TX"; the system "must dynamically direct its main beam toward the desired TX while simultaneously placing pattern nulls or utilizing polarization mismatch to suppress strong, direct-path interference from other ambient communication sources"], [\[#link(<ref-P1>)[P1]\]],
  [transmitters], [unmodified COTS transmitters of the team's choice, single or multiple; Wi-Fi routers or Bluetooth beacons certified for use in Japan, and smartphones in standard hotspot mode, are given as acceptable], [\[#link(<ref-P1>)[P1]\]],
  [display], ["Performance metrics/results must be displayed in real time, with easy visualization"], [\[#link(<ref-P1>)[P1]\]],
  [education], [the theory explained "in simple terms for non-engineers", and "step-by-step instructions" to replicate the system], [\[#link(<ref-P1>)[P1]\]],
  [cost], ["The total production cost for the entire system must be less than US\$1,500"; university licensed or free software may be used; other commercial software counts in the budget], [\[#link(<ref-P1>)[P1]\]],
  [team], [2 to 5 students, at least half undergraduates by the end of May 2027; no student or mentor in more than one team], [\[#link(<ref-P1>)[P1]\]],
  [mentor], [one professional mentor who is an IEEE AP-S member; a mentor letter agreeing to supervise and to advance initial costs if necessary; the work done primarily by the students], [\[#link(<ref-P1>)[P1]\]],
  [proposal], [preliminary design due 31 December 2026 (GMT-10): a PDF of at most four pages in 12 point Times New Roman, with the demonstration setup and the quantities to be measured or post-processed, the antenna system to be built, a bill of materials up to US\$1,500, and the mentor letter], [\[#link(<ref-P1>)[P1]\]],
  [selection and funding], [six semi-finalist teams selected by 22 January 2027, each receiving US\$1,500 to build and test; stipends of up to US\$10,000 per team to attend the symposium, on submission of final materials and visa letters], [\[#link(<ref-P1>)[P1]\]],
  [final materials], [due 24 May 2027: a video of at most 10 minutes; replication instructions of at most 5 pages; a final report of at most 5 pages in the IEEE Transactions on Antennas and Propagation format, including simulation and measurement results], [\[#link(<ref-P1>)[P1]\]],
  [judging], [preliminary: likelihood of achieving the design goal and specifications, creativity, quality of the written materials. Final: achieved performance, creativity, system functionality, educational value, quality of final materials and of the on-site demonstration], [\[#link(<ref-P1>)[P1]\]],
  [prizes], [1st, 2nd and 3rd: certificates and US\$1,500, US\$750 and US\$250], [\[#link(<ref-P1>)[P1]\]],
  [symposium], [2027 IEEE International Symposium on Antennas and Propagation and JNC-USNC-URSI Radio Science Meeting, Kyoto International Conference Center, Kyoto, Japan, 20 to 25 June 2027], [\[#link(<ref-P3>)[P3]\]],
)

*Not found in any excerpt, and therefore unknown:* a mandated frequency band; any rule on
software defined radios, commercial receiver modules or commercial antennas; judging weights; a
proposal template; whether student IEEE membership is required; a contest contact. One search
summary gave "travel awards up to US\$1,500", which conflicts with the official domain excerpts;
it appears to confuse the build funds with the stipend.

=== 45.2 Requirement and response, kept apart

#table(
  columns: (2.5fr, 12.6fr),
  table.header([Official requirement], [Our design response, *\[proposed here\]*]),
  [a reconfigurable *receiving* antenna system], [Rev A in its receive configuration: a passive switched line network, no transmitter of our own in the demonstration],
  [COTS transmitters as ambient sources], [2.4 GHz Wi-Fi routers, Bluetooth beacons or a hotspot phone; band 57a is the band they use, which the 2.44 GHz choice of decision 0004 happens to fit],
  [communication mode with beam and nulls, or polarisation], [beam towards the wanted transmitter and a null on the interferer, chosen by exact enumeration of the reachable states against the calibrated array state; polarisation is a gated option (section 51)],
  [sensing mode], [pattern diversity: a set of receive patterns cycled by the FPGA, their received powers as features],
  [real time display], [a dashboard on the HPS or a PC: per state powers, estimated pattern, null depth, sensing state, measurement count],
  [educational material], [the course of Part I is the raw material; the 16 bit word, the enumeration and the drift experiment are easy to show],
  [cost below US\$1,500], [the Rev A bill of materials was estimated at about 62 EUR before decision 0005 added a converter and buffers, and has not been re-costed; the controller and any receiver come on top; the whole system must be costed, including the DE1-SoC if the rules count owned equipment (to verify)],
)

== 46\. Why AetherArray fits, and what is missing

Each official requirement is traced to the physical function it asks for (section 10bis), to how
AetherArray would provide it, to a metric, and to the evidence that exists and that is missing.

#small-table[
#table(
  columns: (2.9fr, 3.2fr, 5.0fr, 3.4fr, 57pt, 3.4fr),
  table.header([Official requirement], [Physical function], [AetherArray implementation], [Measurable metric], [Current evidence], [Missing evidence]),
  [reconfigurable receiving antenna system], [spatially selective reception, section 7], [4 elements, 3-bit phase, enable per channel, 512 relative states; receive only, passive chain], [pattern change between commanded states], [analytical; schematic captured; not built], [patch design, re-capture, fabrication, a measured pattern],
  [communication: main beam to the wanted TX], [coherent gain towards \$	heta\_D\$, sections 7.3 and 10bis.4], [exact enumeration against the estimated array state], [$P_D$ against the ideal steered value], [analytical], [EXP-007 to EXP-009; a source separating receiver],
  [communication: nulls or polarisation against interference], [suppression of $P_I$ with the link kept, sections 9 and 10bis.4], [null placement by enumeration; polarisation gated (section 51)], [$P_I$ suppression; SIR or packet success, if the receiver separates sources], [ideal theory only], [N = 4 feasibility gate (section 50); a measured desired and interferer experiment],
  [sensing with ambient illuminators], [inference on the multipath field, sections 10bis.3 and 10bis.4], [pattern diverse power vector $vb(p) ( t )$ over $K$ states], [detection or false alarm rate of a pre-registered task], [observability argument only], [protocol, classifier, controlled repeated experiment],
  [dynamic switching between modes], [shared aperture, family B], [the FPGA applies any state on one clock edge], [switching time, recorded], [specified; no gateware], [gateware and HPS software],
  [real time metrics], [a live estimate of the field and the array], [record stream and inference on the HPS], [dashboard latency], [specified], [the dashboard],
  [(not an official requirement) robustness to drift], [the shared calibration layer, section 10bis.5], [Part VIII: full recalibration, and the learned prior as research extension], [null depth or sensing false alarms before and after recalibration; $M_(e x t r e q u i r e d)$], [formalised only], [EXP-005 to EXP-015],
  [educational material and replication], [explanation and reproducibility], [public repository, runbooks, generated documentation, Part I], [an outsider replicates], [strong for documentation], [the contest's replication guide],
  [total cost below US\$1,500], [], [about 62 EUR of parts estimated before decision 0005's additions, plus controller and receiver], [itemised bill of materials], [estimated, not re-costed, no quote], [full system costing],
)
]

The fit is genuine in three respects: a receiving, reconfigurable array is exactly what Rev A is;
the 2.4 GHz band is where the allowed commercial transmitters operate; and the communication
mode's demand for nulls is exactly where calibration error becomes visible. It is incomplete in
one structural respect, the receiver behind the array (section 47), and in schedule.

== 47\. Communication mode

#aa-figure(num: "15", caption: [the proposed communication mode. The receiver behind the sum port is not chosen.])[
```text
          desired COTS TX (e.g. Wi-Fi router, a known channel)
                     \
                      \   theta_D
                       \
                  +-----------------------+         sum port         +--------------------------+
                  |  AetherArray RX       |------------------------->| receiver: TO BE CHOSEN   |
                  |  4 patches, 512 states|                          | power per source, link   |
                  +-----------------------+                          +--------------------------+
                       /                                                        |
                      /   theta_I                                       DE1-SoC: state, timing, records
                     /                                                          |
          interfering COTS TX (e.g. second router or beacon)              dashboard: P_D, P_I, SIR,
                                                                          pattern, null depth
```
]

*Objective.* Keep a strong response towards the wanted transmitter while suppressing the
interferer: maximise $J$ or the signal to interference ratio of section 9.2 over the reachable
states.

*Procedure, as proposed.*

1. Estimate the array state $hat(vb(H))_t$ (Part VIII). If the wanted transmitter is used as the
   calibration source over the air, what is estimated is the product of hardware and incident field,
   $h_n s_n$, a channel calibration valid in that room (section 10bis.5); it equals the hardware state
   only for a dominant direct path from a known direction, or when the hardware state comes from a
   conducted reference.
2. Estimate or know $theta_D$ and $theta_I$.
3. Enumerate all 512 relative states, or 820 with the enable bits, computing $P_D$ and $P_I$ from
   $hat(vb(H))_t$ and an element pattern model; choose the best.
4. Apply it on one clock edge; measure the outcome; display it.

*The receiver is the open architectural question.* The AD8318 at the sum port measures total
power across its whole frequency range. When the wanted and the interfering transmitters are both
active in the 2.4 GHz band, it reports their sum and cannot attribute power to either; and ambient
Wi-Fi and Bluetooth signals are bursts, not continuous carriers, so a sampled detector sees a
fluctuating input. A signal to interference metric therefore needs a measurement that can tell the
sources apart:

#table(
  columns: (2.9fr, 4.8fr, 8.0fr),
  table.header([Option], [How it separates the sources], [Cost and risk]),
  [AD8318 alone], [only if the sources occupy different times or different channels behind a filter], [not controllable with unmodified commercial transmitters; filtering per channel is impractical],
  [software defined radio at the sum port], [channelisation, packet timing or identity per source], [cost against the US\$1,500 cap; software effort; whether a commercial receiver is acceptable under the receive only rule is not stated in the excerpts],
  [commercial Wi-Fi or Bluetooth receiver module fed from the sum port], [reports received signal strength and packet statistics per transmitter identity], [cheap and directly measures the "robust data link"; same rule question; reported RSSI is coarse and its accuracy uncharacterised],
)

None is chosen, and this document does not choose one. Whatever is chosen also changes the
measurement model of Part VIII: a per source power reading is still a power reading, so the power
only likelihood applies, but its noise and its time cost differ from the detector's. Whether
ambient signals at demonstration distances reach the useful range of any of these receivers after
the chain loss is *\[to verify\]* by a link budget.

*Null visualisation.* The dashboard can show the measured $P_D$ and $P_I$ for the chosen state,
the estimated pattern with its null, and, over time, the null depth on the interferer. That last
plot is what makes drift and recalibration visible (section 52).

== 48\. Sensing mode

#aa-figure(num: "16", caption: [the proposed sensing mode.])[
```text
        COTS Wi-Fi router (illuminator of opportunity)
              |   \
              |    \  reflections off people and objects (multipath)
         direct     \
          path       \__ person moving in zone L / C / R __
              |                                            \
              v                                             v
        +---------------------------------------------------------+
        |  AetherArray cycles K receive patterns w_1 ... w_K      |
        |  feature vector p(t) = [P_1(t), ..., P_K(t)]            |
        +---------------------------------------------------------+
                                   |
                     simple classifier: empty / present, moving / static, left / centre / right
```
]

The physics is in section 10bis: the illuminator and its paths in 10bis.3, the pattern diverse
vector $vb(p) ( t )$ and why it carries more than one received signal strength in 10bis.4, and the
confound with hardware drift in 10bis.5. What this section adds is the demonstration design. A few
beams pointing in different directions and a few patterns nulled towards the transmitter, so that
the scattered field is not swamped by the direct path, would form the $K$ states. Calibration is what
lets a change in $vb(p)$ be attributed to the room.

Candidate tasks, in increasing difficulty: room empty or occupied; a person moving or still; a
person in the left, centre or right zone. *The simplest reproducible task is preferable* to an
ambitious unreliable one, for reasons specific to a contest: the venue's multipath differs from
the laboratory's, visitors stand around the booth, ambient traffic varies, and a judge will believe
a binary detection that works every time before a localisation that works sometimes. Ratio
features such as $P_k \/ sum_j P_j$ would cancel variations of the transmitter's own power, a
*\[proposed here\]* design choice. The classifier should be as simple as the task allows, a
threshold or a nearest centroid, with its error rate reported on data recorded on a different day
from its training data.

No sensing protocol, classifier or data exists in the repository.

== 49\. Why four elements may be enough

A four element array is not impressive by element count, and nothing in this document claims
otherwise. Its value for the contest comes from properties a larger array would make harder to
obtain:

#table(
  columns: (2.2fr, 4.3fr),
  table.header([Property], [Why it serves the demonstrator]),
  [controllable states], [16 bits, applied on one clock edge],
  [exact enumeration], [the best state for any criterion is known, not approximated],
  [full characterisation], [every channel measurable alone, the coupling matrix measurable pair by pair],
  [drift experiments], [temperature logged, unattended runs, labels from hardware],
  [calibration], [6 parameters: identifiable, small, explainable to non-engineers],
  [measured null degradation and recovery], [the visible demonstration of what calibration is worth],
)

Why not move to eight elements automatically:

#table(
  columns: (2.0fr, 3.4fr),
  table.header([Grows with $N = 8$], [From $N = 4$]),
  [switches], [28 channel switches become 56],
  [divider], [a fourth Wilkinson stage, with its loss and area],
  [control], [32 beam state lines, against 36 user pins on one DE1-SoC header],
  [calibration dimensionality], [6 identifiable parameters become 14],
  [measurement burden], [REV at its minimum, 12 readings become 24],
  [board size], [an antenna board about twice as long],
  [cost and schedule], [more parts, more layout, more bring-up, inside a contest deadline],
)

Enumeration itself would survive: $8^7$, about 2.1 million relative states, is still a few seconds
of arithmetic against an estimated model, so even at $N = 8$ model based beam synthesis would not
need a learned beamformer. What would not survive is the schedule. The rule this document proposes
is the one the brief states: *N = 4 remains the architecture unless a deterministic feasibility
study, with criteria written first, shows that a predefined AP-S requirement cannot be met.*

== 50\. The N = 4 feasibility gate

*\[proposed here\]*, not run. Its design follows the repository's practice of writing the rule
before the data.

1. *Write the requirement first.* From the contest needs, fix what the communication mode must
   achieve, for example a minimum interferer suppression with at most a stated loss towards the
   wanted transmitter, over a stated set of angle pairs $( theta_D , theta_I )$ with a minimum
   separation, and a stated robustness to phase and amplitude error. The numbers are not proposed
   here, because choosing them is the decision.
2. *Enumerate.* For every pair on the grid, evaluate all 512 relative states, and the 820 with
   enable bits, with the ideal model; record the best achievable wanted gain, interferer
   suppression and objective.
3. *Perturb.* Repeat with the quantisation inherent in the states, with random phase and
   amplitude errors at decision 0007's levels, and at plausible drift levels; record how the best
   state degrades and how often the choice changes.
4. *Map.* Plot the coverage over $( theta_D , theta_I )$.
5. *Decide.* Retain $N = 4$ unless the predefined requirement fails over the predefined scenario
   set; if it fails, reopen the element count by a new decision, with the gate's results as
   evidence.

```text
   theta_I (deg)
     +45 | . . . . . . . x x x
         | . . . . . . x x x .
         | . . . . . x x x . .        x : interferer within about a beamwidth of the wanted
       0 | . . . . x x x . . .            direction; cannot be suppressed without losing the link
         | . . . x x x . . . .        . : feasibility to be computed by the gate
         | . . x x x . . . . .
     -45 | . x x x . . . . . .
         +----------------------
          -45        0       +45   theta_D (deg)
```

_Conceptual angle pair coverage map. Only the diagonal band follows from first principles; nothing
else has been computed, deliberately, so that the gate's criteria can be fixed before its results
are seen._

== 51\. The dual polarisation option

The official text allows interference to be suppressed by "polarization mismatch" as well as by
nulls. A dual polarised element, two orthogonal feeds per patch with switching between them, would
add:

#table(
  columns: (2.4fr, 5.7fr),
  table.header([Benefit], [Explanation]),
  [polarisation reconfigurability], [the receive polarisation becomes a control],
  [interference rejection], [an interferer arriving in a different polarisation from the wanted signal can be rejected without spending spatial degrees of freedom],
  [richer sensing signatures], [scattering by people changes polarisation, which adds features],
)

And would cost:

#table(
  columns: (1.5fr, 5.8fr),
  table.header([Cost], [Explanation]),
  [RF switching], [a second set of feeds per element, more switches, more loss],
  [antenna complexity], [two feeds per patch, cross polar isolation to design and verify],
  [isolation], [the two polarisations must not leak into each other],
  [routing], [more lines on the antenna board, more connectors or a switch on the antenna board, which conflicts with the passive antenna board of decision 0003],
  [calibration], [a polarisation dimension in the array state],
  [simulation], [larger HFSS models, possibly beyond the Student limit],
)

Decision 0008 already notes that one polarisation and one plane are judged, and cross polar
behaviour is not. *Dual polarisation is therefore a gated option, not current architecture.* It
would need its own feasibility evidence and a decision that supersedes parts of decision 0003.

== 52\. Demonstration sequence

#aa-figure(num: "17", caption: [drift, degrade, recalibrate. A narrative, not a measured sequence.])[
#image("../figures/mermaid/figure-17.svg", width: 100%)
]

#table(
  columns: (auto, 4.0fr, 4.2fr),
  table.header([Step], [What the audience sees], [Honesty condition]),
  [1], [the calibrated array: estimated pattern, per state powers], [the calibration's own measurement count is shown],
  [2], [the wanted link held while the interferer is suppressed], [the receiver used to separate the sources is named],
  [3], [drift], [an induced drift is announced as induced; a handling event is not called drift],
  [4], [the null filling in, the metric falling], [levels are whatever is measured on the day],
  [5], [a full recalibration and its count], [the full method at its own minimum, not padded],
  [6], [a sparse recalibration with the learned prior and its smaller count, if the research supports it], [if the prior does not help, the demonstration says so; the comparison is the result],
  [7], [sensing on the calibrated array], [the task's error rate is stated],
)

*The demonstration must stand without the learning extension.* Steps 1 to 5 and 7 use only the
classical calibration and the exact enumeration; step 6 is the research overlay. If the learned prior
is not ready, or does not help, the demonstration still shows an ISAC receiver, its dependence on
calibration, and a full recalibration restoring it. The calibration overlay is

```text
 drift --> COMM and SENSE degrade --> full recalibration baseline (count M_full)
                                 \--> learned prior sparse recalibration (count M_sparse), research
```

and each recalibration shown must say whether it estimated the hardware state or a room dependent
channel (section 10bis.5).

The exact implementation will evolve. No value in this sequence is known today.
