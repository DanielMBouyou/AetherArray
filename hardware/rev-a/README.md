# Rev A beamformer board, schematic

- Status: captured, electrical rule check clean, ready for review
- Last reviewed: 2026-09-18

The schematic for the board selected in `decisions/0003-rev-a-rf-architecture.md`.
Layout has not started and is not authorised by that decision.

## Files

| File | Role |
| --- | --- |
| `aetherarray-reva.kicad_pro` | project |
| `aetherarray-reva.kicad_sch` | root sheet: common port, divider, detector, telemetry, control interface |
| `rf-channel.kicad_sch` | one RF channel, instantiated four times |
| `aetherarray.kicad_sym` | project symbol library for the parts with a chosen part number |
| `tools/generate-schematic.py` | the generator that produces every file above |
| `bom/preliminary-bom.csv` | bill of materials exported from the captured schematic |
| `erc/erc-report.txt` | electrical rule check output |
| `erc/erc-notes.md` | what the check covers, and what is deliberately left open |
| `layout-constraints.md` | the constraints the symbolic delay sections impose on layout |

## The four channels are identical by construction

`rf-channel.kicad_sch` is a single hierarchical sheet instantiated four times. There
is no second copy to drift out of step, and the identity is a property of the file
structure rather than of anyone's care in editing. It is checked as well: the net
topology signature of the four channels is compared after generation and must match.

## Reading the schematic

Signal flow on the root sheet, drawn for transmit. The network is passive and
reciprocal, so in receive the divider is a combiner and the element ports are inputs.

```
J904 common port --- U900 path select --- 4-way Wilkinson --- CH0..CH3 --- J900..J903
                          |                                                 element ports
                     U901 AD8318
```

`U900` selects which measurement path sees the common node: the analyser on one
throw, the on board detector on the other. That is the two path arrangement in
section 5.3 of `docs/architecture/rev-a-rf-architecture.md`.

Each channel contains, in order: an enable switch that either passes the signal on or
terminates the channel in 50 ohm, then three cascaded switched line bits of 45, 90 and
180 degrees. Seven switches per channel, 28 in total, plus `U900`.

Connectivity is expressed with labels rather than long drawn nets. Every pin carries a
short stub and a net name, so the netlist is read from the names and no net depends on
two lines happening to touch.

## Regenerating

```bash
python tools/generate-schematic.py
```

The generator is the source of truth. Editing the schematic by hand in the editor
works, but the next run of the generator will overwrite it, so a change that should
persist belongs in the generator.

## Checks

```bash
kicad-cli sch erc --severity-all --exit-code-violations aetherarray-reva.kicad_sch
kicad-cli sch export bom --output bom/preliminary-bom.csv aetherarray-reva.kicad_sch
```

Current result: **0 violations**. See `erc/erc-notes.md`.

## What the bill of materials says

Exported from the schematic, so it counts what is actually drawn.

| Part | Quantity | Note |
| --- | --- | --- |
| PE4259-63 | 29 | 28 in the four channels, 1 for the measurement path select |
| AD8318ACPZ | 1 | logarithmic detector |
| MCP9808T-E/MS | 2 | requirement R4 telemetry, addresses 0x18 and 0x19 |
| 100 nF | 35 | one bypass per switch, plus supply and filter duties |
| 100 pF | 2 | detector input coupling |
| 1 nF, 220 pF | 1 each | supply decoupling and loop filter |
| 50 ohm | 4 | channel terminations |
| 100 ohm | 3 | Wilkinson isolation |
| 18k, 1k, 4k7 | 1, 2, 2 | temperature compensation, converter series, I2C pull ups |
| Symbolic transmission lines | 30 | 24 in the channels, 6 in the divider; these are layout, not purchases |
| SMA | 5 | four element ports and the common port |
| Header | 1 | interface to the Nucleo |

**Delta against the architecture document.** Section 6 of
`docs/architecture/rev-a-rf-architecture.md` costed 28 fitted switches. Capture added
one, `U900`, so that the detector and the analyser do not both sit on the common node
permanently. Hard wiring both would load the path and split the signal whether or not
the detector was in use. The cost is about 0.5 EUR and roughly 0.5 dB of insertion
loss in the common arm, and the two measurement paths become properly exclusive.

## Interfaces

| Interface | Detail |
| --- | --- |
| RF common | `J904`, one SMA |
| RF element ports | `J900` to `J903`, one SMA each, satisfying R1 and R2 |
| Control and power | `J905`, 26 pins: 17 control lines, 2 converter returns, I2C, 5 V, 3V3 and three grounds |
| Test points | `TP101` and `TP102` per channel on the chain input and output, and `TP900` to `TP904` on the detector output, the die temperature output and the three rails |

## Power

| Rail | Source | Load |
| --- | --- | --- |
| 5 V | Nucleo, through `J905` | `U901` only, 68 mA typical |
| 3V3 | Nucleo, through `J905` | 29 switches and 2 sensors, microamp parts |

The Nucleo is the only source, so its pins on `J905` are the power outputs of the
design and every other supply pin is an input. That is what makes the rule check pass
without a power flag anywhere.
