#import "../template.typ": *

= Part VI. Simulation roadmap <part-vi-simulation-roadmap>

*Only SIM-001 exists in the repository.* The later stages below are a *\[proposed here\]*
sequence, assembled from the follow-up list of SIM-001, the decision 0007 simulator comparison,
EXP-011 and the school task register. Their numbers are suggestions; registering them, with
criteria written before data, is future work.

#aa-figure(num: "13", caption: [simulation roadmap. SIM-001 is registered; SIM-002 to SIM-008 are proposed numbering.])[
#image("../figures/mermaid/figure-13.svg", width: 100%)
]

Why sequential? Each stage needs the previous one's output as a trusted input. It is irrational to
optimise a full array before the transmission line model it is built from has been validated: an
error in $epsilon_"eff"$ would then be spread across every bit, every arm and every
coupling result, and could not be separated from them.

#small-table[
#table(
  columns: (49pt, 53pt, 4.9fr, 4.7fr, 6.4fr, 3.2fr, 46pt),
  table.header([Stage], [Input], [Model], [Expected output], [Pass or fail], [Unlocks], [Where]),
  [*SIM-001*, 50 ohm microstrip, registered], [canonical stack-up, seed width], [straight line, two lengths, three widths, wave ports], [$W_50$ by interpolation; $epsilon_"eff"$ and attenuation by two line extraction and by port solution], [converged at $Delta S lt.eq 0.02$ twice; $W_50$ inside the sweep; acceptable if at least twice the process minimum; other figures reported, not judged], [every printed length; gate F5], [`LOCAL`, HFSS Student],
  [SIM-002, Wilkinson line and real arm shapes, proposed], [$W_50$, $epsilon_"eff"$ from SIM-001], [70.7 ohm line; meandered 45, 90 and 180 degree arms with mitred bends], [differential phase of each arm as it will be routed, against the straight line value], [criterion to be registered; decision 0007's 2.29 degrees bounds the state dependent error a layout may introduce], [the arm geometry], [`LOCAL`, likely within Student limits],
  [SIM-003, one switched line bit, proposed], [SIM-002 arms; a switch model], [two SPDTs and two arms, switch as an S-parameter block if a model exists], [phase and loss of each state across band 57a; off arm resonance check], [decision 0007: HFSS against circuit model within 2.29 degrees and 0.40 dB on the state dependent part], [trust in the bit topology], [`EITHER`; full HFSS if over the mesh limit (SCH-010)],
  [SIM-004, full channel, proposed], [SIM-003], [enable switch and three bits in cascade, likely by cascading simulated blocks in `rfkit`], [all eight states: phase error against nominal, loss spread], [derived requirement: state dependent phase within 2.29 degrees of nominal at $f_0$; imbalance within 0.82 dB], [the channel design; amplitude imbalance against decision 0009's loss estimate], [`EITHER`],
  [SIM-005, divider, proposed], [$W_50$, 70.7 ohm width], [three stage Wilkinson with resistors, then $U 900$], [balance, output isolation, input match], [criterion to be registered], [the combiner], [`LOCAL`],
  [SIM-006, single patch, proposed], [antenna construction], [patch, feed, ground, radiation boundary], [resonance, $S_11$, bandwidth, efficiency, pattern], [criterion to be registered; resonance inside band 57a with margin for the permittivity bound], [the antenna geometry, uncertainty I27], [`LOCAL`, within Student limits \[assumed\]],
  [SIM-007, coupling, registered as EXP-011 Stage 1], [the four patch board], [four ports at the connector plane, embedded element patterns], [$vb(S)_A$ in `.s4p`, last two passes, patterns container], [*decision 0008*: PASS, FAIL, INTERMEDIATE or UNRESOLVED], [gate G4; the coupling matrix for EXP-013], [`EITHER`; SCH-004 on escalation],
  [SIM-008, system model, proposed], [SIM-004, SIM-005, SIM-007], [cascade of simulated blocks and the coupled forward model, not a full wave model of everything], [predicted per channel states, beams and nulls for all 512 states], [criterion to be registered], [the predictions that hardware validation (SCH-006) will test], [`LOCAL`],
)
]
