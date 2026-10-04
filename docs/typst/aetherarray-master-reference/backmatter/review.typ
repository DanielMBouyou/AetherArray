#import "../template.typ": *

= Review from five reader perspectives <review-from-five-reader-perspectives>

A self review, written so that the weak sections are named rather than hidden.

#table(
  columns: (47pt, 11.3fr, 11.6fr),
  table.header([Reader], [Can they get what they need?], [Where the document is weak]),
  [first year RF student], [Part I builds from fields to S-parameters, microstrip, antennas and arrays, with a worked number in every section], [Part I is dense; some sections, especially 10 and 11, assume comfort with complex matrices; there are no exercises],
  [RF professor], [equations are standard and sourced; conventions stated; every project number traced to a decision or a generated table; switched line hazards named], [no simulated or measured RF result exists to examine; switch behaviour at 2.44 GHz rests on typical spot values; the off arm resonance and leakage analyses are qualitative; the textbook citations are index level],
  [ML professor], [the learned object, likelihood and prior are separated; baselines include a non learned temporal model; temporal splits, leakage and prior calibration are addressed], [no data exist, so the model class, the data rate and the drift magnitude are all unknown; the target $delta$ and risk $alpha$ are undefined; the power only likelihood needs approximations not yet specified],
  [AP-S jury], [Part IX states the official requirements separately from the response, shows why nulls make calibration visible, and names the receiver gap and the schedule risk], [contest facts are snippet level; no feasibility numbers, sensing data or receiver choice exist; the team and mentor are not recorded; schedule is the dominant risk],
  [hardware recruiter], [real skills are visible and attributable: stack-up selection from fabricator data, error budgeting, pre-registered experiments, a scripted schematic, PyAEDT tooling, a tested RF library, FPGA timing design], [nothing has been fabricated, assembled, brought up or measured; gateware and layout skills are specified, not yet demonstrated],
)

*The ISAC pass, read from five angles (version 0.2).*

#table(
  columns: (52pt, 3.8fr, 11.9fr),
  table.header([Reader], [Question], [Answer, and remaining weakness]),
  [RF professor], [does the ISAC explanation have electromagnetic meaning?], [yes: the field is a sum of paths, the array samples it, every power is a quadratic form of the spatial covariance (10bis.3, 10bis.4); weakness: narrowband model, no delay spread, no measured multipath],
  [signal processing professor], [is the sensing formulation defensible?], [the observability statement and the confound $tilde(vb(R)) = vb(H) vb(R) vb(H)^(sf(H))$ are exact for the diagonal model; weakness: no detector, no false alarm model, no data, bursty sources not modelled],
  [ML professor], [is learning solving a genuine temporal inference problem?], [yes: estimating a slowly drifting hidden state from sparse measurements, with a physical likelihood; the ISAC setting adds the attribution problem of 10bis.5 but no new reason for a learned beamformer],
  [AP-S reviewer], [is the contest implementation linked to the official problem?], [section 46 traces every official requirement to a physical function, an implementation and a metric; weakness: snippet level rules, no receiver choice, no feasibility numbers],
  [skeptical engineer], [does every claim map to evidence or a labelled future experiment?], [section 10bis.8 lists each ISAC claim with its status and the experiment that would establish it; none is established today],
)

*Sections where current evidence is insufficient, by design of this document:* 6.4 and 22 (antenna
performance), 15.3 (switch behaviour), 17 (detector chain performance), 37 (drift protocol), 40 to 43
(learning), 10bis.4 to 10bis.6 and 45 to 52 (ISAC and the demonstrator), and every row of Part X that reads NOT STARTED.
