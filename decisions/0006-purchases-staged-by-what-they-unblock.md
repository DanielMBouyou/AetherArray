# 0006. Purchases are staged by what they unblock

- Status: accepted
- Date: 2026-09-25
- Scope: every hardware purchase for this project, and the ordering rule previously stated in decision 0003, `docs/hardware/rev-a-requirements.md`, `docs/architecture/rev-a-rf-architecture.md`, `docs/architecture/ml-calibration.md` and `docs/uncertainties.md`

## Question

When may this project buy hardware, given that part of the evidence meant to gate every
purchase can only be produced with hardware that is not owned?

## Context

The ordering rule is written in five places, in slightly different words:

| Where | Wording |
| --- | --- |
| `decisions/0003-rev-a-rf-architecture.md`, consequences | nothing is ordered until EXP-004 and EXP-005 have run |
| `docs/hardware/rev-a-requirements.md` section 7 | nothing should be ordered before G1 and G2 are answered, and both are answerable with instruments already owned |
| `docs/architecture/ml-calibration.md` section 9 | G2 costs nothing to answer, and is answered with instruments already owned, before any purchase |
| `docs/uncertainties.md`, commentary on I12 | the answer costs nothing but bench time with instruments already owned |
| `docs/architecture/rev-a-rf-architecture.md` section 6 | nothing is ordered before section 7 clears |

Its intent is sound and is kept. The learning track rests on gate G2, and hardware that
exists only for that track should not be bought while G2 could still show that the
track does not exist. `docs/hardware/rev-a-requirements.md` section 7 names the
requirements concerned: R1, R3, R4 and R8.

Two of its premises no longer hold.

1. **G2 is not answerable with instruments already owned.** EXP-005 Phase B, the
   repeatability floor of received power, needs a detector, antennas and
   interconnect, none of which is owned (`experiments/EXP-005-repeatability-floor.md`
   section 9). Observation O7 has confirmed no calibration kit, no adapter and no
   cable (`results/EXP-004/README.md`).
2. **Half of G2 cannot precede fabrication under any rule.** G2 is settled by "EXP-005
   then EXP-010", and EXP-010 asks how long a calibration of the array stays valid,
   which is a property of the built array. The same holds for E6 in
   `docs/architecture/rev-a-rf-architecture.md` section 7.3, switch state
   repeatability, which needs fitted switches.

Read literally, the rule is therefore circular:

```
no purchase -> no Phase B -> no repeatability floor -> no G2 -> no purchase
```

One level down it forbids the Rev A order permanently, because the drift half of G2
needs the board the rule withholds.

A third fact decides how much this matters. Of the four requirements G2 is meant to
protect, R1 and R4 are not retrofittable and R3 only partly
(`docs/hardware/rev-a-requirements.md` section 2). A rule that waits for G2 before
fitting them guarantees that G2 is answered on a board that cannot use the answer.

## Options considered

### Option A: keep the rule as written

Nothing is bought until G2 is answered. Since G2 cannot be answered without buying,
nothing is ever bought, and the project remains a simulation study by default rather
than by decision.

### Option B: drop the gate and order Rev A now

Removes the stall at once, and throws away what the gates protect. EXP-005 Phase A
decides two of the four rows of the pending schematic re-capture through open item H3,
and can reopen decision 0005 through R9. Observation O1 is the one reading that can
still reopen the frequency, decision 0004. Open item H1 blocks board release on its
own. Ordering now would be ordering a schematic already known to be out of date.

### Option C: stage purchases by class, each gated only by what it depends on

Every purchase belongs to one of four classes. Each class waits for the evidence it
actually depends on, and no purchase waits on a question that the purchase itself is
needed to answer. The drift half of G2 moves after fabrication, where it can be
answered, and gates the learning track rather than the order.

### Option D: answer the drift half of G2 before fabrication, on a proxy

Measure the drift of cables and a sample switch before any board exists, keeping G2
whole ahead of the order. It does not answer the question. The drift G2 concerns
belongs to the board, its switches, lines and connectors and their thermal behaviour,
which is exactly what a proxy lacks, and a sample switch needs a fixture board, which is
itself a fabrication.

## Comparison

| Criterion | A, as written | B, order now | C, staged | D, proxy |
| --- | --- | --- | --- | --- |
| Terminates | no | yes | yes | yes |
| Rev A order waits for the evidence that can exist before it | no order is ever placed | no | yes | yes |
| Answers the drift half of G2 | never | after fabrication | after fabrication | on the wrong object |
| Money at risk if G2 later fails | none, nothing is bought | the whole board, on an outdated schematic | the G2 only features, bounded below | as C, plus the proxy fixture |
| Reversibility | total, and nothing is learnt | poor | good, since class 2 items stay useful whatever the gates return | good |

## Evidence

No experimental evidence. The decision rests on the dependency structure of documents
already in this repository, each cited where it is used: `experiments/EXP-005-repeatability-floor.md`
sections 7 to 10, `results/EXP-004/README.md`, decisions 0002 to 0005,
`docs/hardware/rev-a-requirements.md` sections 2 and 7,
`docs/architecture/rev-a-rf-architecture.md` section 7,
`docs/architecture/control-architecture.md` section 8 and
`docs/hardware/measurement-bench.md` section 4.

## Decision

Purchases are staged in four classes. **A purchase is allowed once every gate it
depends on is closed, and it never waits on a question it is needed to answer.** Rev A
fabrication waits on every question that can be answered before fabrication, and on
none that needs the fabricated array.

### The four classes

| Class | What it covers | Gate |
| --- | --- | --- |
| 1, zero purchase | EXP-004 outstanding observations, O1 and O6 to O9; EXP-005 Phase A, conditions C1 to C5, on owned hardware; the analyser only reconnection floor of EXP-005 section 9, if O7 finds a cable or a through connection; the whole simulation track | none |
| 2, measurement enabling | the smallest set that lets EXP-005 Phase B run: interconnect sized by O7; a pair of antennas for 2.44 GHz, unless an owned probe antenna is confirmed; a detector of the type decision 0003 selected, in a form usable before the board exists, with its supply | per item, in the dependency graph below. **Each item must remain useful whatever the gate it answers returns**: interconnect and antennas are needed to validate any board, and a separate detector is the independent reference for the detector on the board |
| 3, Rev A design and fabrication | the board, every part fitted to it, and its connectors | the pre-fabrication gate, F1 to F5 below |
| 4, optional upgrades | the angular positioner, absorbers, a dedicated source that frees the analyser, and anything whose absence costs convenience or pattern measurement rather than a gate | a named experiment that needs it |

The usefulness condition on class 2 is what stops it being a side door into class 3. An
item that an unfavourable gate result would waste belongs to class 3, and waits with it.

### What Phase A must establish before a Phase B purchase

| Purchase | What Phase A must have established | Why |
| --- | --- | --- |
| The detector | C1 executed, with preconditions V1 to V4 of EXP-005 section 7.2 all holding and recorded in `results/EXP-005/` | the detector is read through the acquisition path that C1 qualifies. V1 shows the codes dither, so averaging recovers resolution below one converter step of 1.0 mV, which is 0.04 dB at the detector slope. V2 bounds the within state spread of the local path. A detector bought before that is known could only be tested by debugging two unknowns at once |
| Interconnect and antennas | nothing | they are used with the analyser, not with the acquisition path. Their gates are O7, which says what is missing, and O1, because antennas are specific to the band and O1 is the one reading that can still reopen decision 0004 |

No Phase B purchase waits on C2 to C5, or on the outcomes for R9 and H3. Those decide
the control path and the re-capture. Phase B can read the detector over the local path,
which is the path C1 qualifies.

### The Phase B dependency graph

EXP-005 section 9 lists a radio frequency source among the Phase B needs. The observed
analyser already serves as that source, the role `docs/hardware/measurement-bench.md`
section 4 assigns it for detector validation, so a source is not a purchase. The
analyser also measures received power through its own receiver, so the fixed geometry
rows can run before any detector exists. The detector adds the route the unattended
runs of EXP-014 depend on.

| Phase B measurement | Needs | Already present | Class 2 item, and its gate |
| --- | --- | --- | --- |
| PB1, repeated received power at a fixed geometry, analyser route | analyser as source and receiver, interconnect, two antennas | the analyser, `[observed]` | interconnect after O7; antennas after O1, and after O7 if their connectors need adapting |
| PB2, effect of a person or an object moving | as PB1 | as PB1 | as PB1 |
| PB3, reconnection repeatability at radio frequency | analyser, and one cable or a through connection | the analyser | none if O7 finds a cable, otherwise interconnect after O7 |
| PB4, floor of the detector path, E5 | analyser as a stepped source, interconnect, detector and its supply, a converter | the analyser, the DE1-SoC converter | the detector after C1 with V1 to V4; interconnect as above |

```
gate                      class 2 item          Phase B measurement
----                      ------------          -------------------
O7 recorded  -----------> interconnect  ------> PB3, and needed by every other row
O1 and O7 recorded -----> antenna pair  ------> PB1, PB2
C1 with V1 to V4 -------> detector      ------> PB4, which is E5

the analyser, observed on the bench, needs no purchase and is source and receiver in every row
```

### The pre-fabrication gate, class 3

Class 3 clears when all five hold. Each is answerable before fabrication.

| | Condition | Where the requirement comes from |
| --- | --- | --- |
| F1 | EXP-004 closed: all nine observations recorded, O1 read from the label and checked against the data sheet of that model, and O7 recorded with a calibration chain to the board's SMA plane settled from owned or class 2 items | decision 0004, conditions for reopening |
| F2 | EXP-005 Phase A complete, with the R9 and H3 outcomes applied. An escalation of R9 reopens decision 0005, and F2 does not clear until it is re-decided | EXP-005 sections 7.4, 7.5 and 10 |
| F3 | EXP-005 Phase B complete on both routes, the analyser route for uncertainties I1 and I3 and the detector route for E5, each judged by a rule written before its data | EXP-005 section 9; `docs/architecture/rev-a-rf-architecture.md` section 7.3 |
| F4 | the schematic re-captured to decision 0005, open items H1 to H4 closed, and H5 decided | `hardware/rev-a/README.md`; `docs/architecture/control-architecture.md` section 8 |
| F5 | the stack-up chosen, and the line lengths derived from it | `hardware/rev-a/layout-constraints.md`; decision 0004 |

**Not in the gate**, because each needs the fabricated array: the drift half of G2,
which is EXP-010; switch state repeatability, E6; and the control polarity of the
PE4259, which is a firmware question. These gate EXP-014, EXP-015 and the learning
track, as decision 0002 already requires, rather than the order.

F3 is where the original intent survives. The half of G2 that can exist before
fabrication, the floor against which drift will later be judged, is measured first,
and R3, the one G2 dependent requirement that is only partly retrofittable, is judged
on it through E5.

### Where G2 now sits

G2 is unchanged as a question. Its two halves are answered at different times: the
floor before fabrication, in F3, and drift above the floor after it, in EXP-010.
Decision 0002 remains conditional on the second half, exactly as before.

## Consequences

- Class 1 work can start at once: C1, and O1 and O7 at the next bench visit.
- The first purchase becomes possible as soon as O1 and O7 are recorded, and the
  detector as soon as C1 holds V1 to V4. No purchase waits on its own result any more.
- The Rev A order has a finite, checkable gate, F1 to F5.
- **The Rev A order is placed before G2 is fully known, deliberately.** What is at risk
  if the drift half of G2 later fails is bounded, with the figures in
  `docs/hardware/rev-a-requirements.md` section 2: R1 at about 6 EUR, which serves the
  classical baselines B2 and B6 regardless; R4 at about 2 EUR; R8 in gateware at no part
  cost; and R3, which F3 will already have tested.
- Interconnect bought under class 2 is the shared connector and cable set that
  `docs/hardware/bom-proposal.md` already accounts once across the laboratory.
- Superseded in place, with the original wording kept: the five sentences in the
  context table.
- Work created: a decision rule for each Phase B route, written and committed before
  any Phase B data exist.

## Known limitations

- **The Phase B decision rules do not exist yet**, and this record does not set them.
  Phase B can run without them but cannot close, so F3, and class 3 with it, stays
  gated until they are written. No value for them is derivable from current evidence.
- The graph assumes the analyser can act as the Phase B source for the length of a
  session. Where it is kept, and on what terms it is available, has not been recorded.
  If it cannot, a dedicated source moves from class 4 to class 2.
- Whether an antenna usable as the probe is already owned is unverified, as it is in
  `docs/architecture/rev-a-rf-architecture.md` section 6.1.
- The class 2 list names functions, not parts. Selection and prices are left to the
  purchase itself.

## Conditions for reopening

- If O1 reopens decision 0004, the antenna purchase and class 3 are suspended until the
  frequency is settled again.
- If O7 shows that no calibrated reference plane is achievable even with class 2
  interconnect, the conducted only fallback of decision 0004 becomes relevant, and the
  antenna purchase is reconsidered.
- If R9 escalates in EXP-005 condition C3, F2 cannot clear until decision 0005 is
  re-decided.
- If the analyser cannot serve as the Phase B source, a dedicated source is reclassified
  to class 2.
- If a way appears to measure the board's own drift before fabrication, the drift half
  of G2 moves back into F3.
