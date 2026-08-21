# State of the art: phased arrays and calibration

- Status: structured draft, most reading still to do
- Last reviewed: 2026-08-21

References recorded from memory, to be confirmed on first reading.

---

## 1. Academic

### 1.1 Array fundamentals

| Ref | Lead | Priority | Question | State |
| --- | --- | --- | --- | --- |
| A1 | Standard reference text on antenna theory | 1 | array factor, patterns, gain, vocabulary | to find |
| A2 | Standard reference text on phased array antennas | 1 | real architectures, practical constraints | to find |
| A3 | Work on mutual coupling and the embedded element pattern | 1 | what invalidates the ideal model | to find |
| A4 | Work on active impedance | 2 | why matching changes as you steer | to find |
| A5 | Amplitude tapering to reduce side lobes | 2 | the beam width against side lobe trade-off | to find |

### 1.2 Calibration

| Ref | Lead | Priority | Question | State |
| --- | --- | --- | --- | --- |
| A6 | Phase rotation calibration, using power measurements only | 1 | the project's central method, cheap in hardware | to find |
| A7 | Calibration exploiting coupling between neighbouring elements | 1 | calibration with no external measurement, very elegant | to find |
| A8 | Near field calibration | 2 | accurate, but needs mechanical scanning | to find |
| A9 | Work on manufacturing errors and their statistical effect on the pattern | 1 | quantitatively justifies calibration | to find |
| A10 | Effect of phase quantisation | 2 | relevant if discrete step phase shifters are used | to find |

A7 deserves particular attention: some methods use coupling between neighbouring
elements, normally treated as a defect, as an internal measurement mechanism. The
array then calibrates itself, with no external instrument. If that works at our
scale it would change the project entirely by removing the need for a pattern
measurement bench.

### 1.3 Inverse problems and optimisation

| Ref | Lead | Priority | Question | State |
| --- | --- | --- | --- | --- |
| A11 | Regularisation of ill posed inverse problems | 1 | stability of the inversion | to find |
| A12 | Phase retrieval from intensity measurements | 2 | the power only case | to find |
| A13 | Bayesian optimisation and Gaussian processes | 1 | reducing the number of physical measurements | to find |
| A14 | Evolution strategies for derivative free optimisation | 2 | a robust reference method | to find |
| A15 | Pattern synthesis by optimisation | 2 | reaching a target pattern | to find |

### 1.4 Learning applied to arrays

| Ref | Lead | Priority | Question | State |
| --- | --- | --- | --- | --- |
| A16 | Work applying learning to array calibration | 1 | has somebody already answered our question? | to find |
| A17 | Drift prediction and predictive maintenance of RF systems | 2 | an original and measurable angle | to find |

---

## 2. Industry

| Ref | Lead | What we want | State |
| --- | --- | --- | --- |
| I1 | Educational phased array kits with full documentation | a real architecture described in detail, for free | to find |
| I2 | Datasheets of integrated beamforming circuits | what exists, at what price, with what performance | to find |
| I3 | Datasheets of commanded phase shifters and attenuators | candidate components | to find |
| I4 | Application notes on array calibration | proven protocols | to find |
| I5 | Documentation of coherent multi channel software radios | option for the digital route | to find |

I1 is probably the highest return source in the project. Some manufacturers publish
complete educational kits with schematics, code and detailed explanations. Even
without buying the kit, the documentation alone is worth the reading time.

---

## 3. Open source

| Ref | Lead | Role | State |
| --- | --- | --- | --- |
| O1 | S parameter processing library | measurement and analysis | available locally, shared with the RF modelling project |
| O2 | Instrument control library | automation | to evaluate, shared |
| O3 | Bayesian optimisation libraries | candidate method | to evaluate |
| O4 | Free electromagnetic simulators | cross check against the proprietary simulation | to evaluate |
| O5 | Open array simulation code | calculation reference | to evaluate |
| O6 | Amateur phased array projects | concrete experience reports | to evaluate |
| O7 | Board design tools | printed antennas | available |

O6 is useful in a different way from the others: amateur projects often document
their failures, which academic literature never does. That is precisely the most
useful information when starting out.

O4 is worth a note. A proprietary full wave simulator is available here, which is a
real advantage, but having a free one alongside it lets us check that a simulated
result is not an artefact of one particular tool.

---

## 4. What the literature probably does not cover

1. A quantified comparison of the **number of physical measurements** needed by
   several calibration methods, on the same real array.
2. How long a calibration stays valid under ordinary conditions, meaning without a
   climate chamber.
3. An assessment of what a low cost setup can genuinely measure, with stated
   uncertainties.
4. A cross validation between an acoustic array and a radio frequency array, showing
   that the same calibration algorithms work on both.
5. A comparison between simulated coupling, from a full wave model, and coupling
   measured on the fabricated array.

Point 4 would be an original and rather enjoyable contribution, and it is within
reach. Point 5 became realistic because a full wave simulator is available.

---

## 5. Reading priorities

| Order | What | Why now |
| --- | --- | --- |
| 1 | A6, phase rotation calibration | the central method, undemanding in hardware |
| 2 | A7, calibration through coupling | could remove the need for a measurement bench |
| 3 | I1, documented educational kits | a free reference architecture |
| 4 | A9, statistical effect of errors | quantitatively justifies the whole project |
| 5 | A1 and A2, fundamentals | so we do not write nonsense |
| 6 | A13, Bayesian optimisation | only once the classical reference is established |

## 6. Tracking

Every source read produces a note in `research/notes/`.
