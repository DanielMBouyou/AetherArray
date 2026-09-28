# Rev A beamformer board, schematic

- Status: captured, electrical rule check clean, ready for review
- Last reviewed: 2026-09-28

This is the schematic for the board chosen in `decisions/0003-rev-a-rf-architecture.md`.
The layout hasn't started, and that decision doesn't allow it yet.

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

`rf-channel.kicad_sch` is one hierarchical sheet, used four times. There's no second
copy that could drift out of step, so the four channels match because of how the files
are built, not because somebody edited carefully. It's checked anyway: after
generation, the net layout of the four channels is compared, and it has to match.

## Reading the schematic

Here's the signal flow on the root sheet, drawn for transmit. The network is passive
and works the same both ways, so in receive the divider becomes a combiner and the
element ports become inputs.

```
J904 common port --- U900 path select --- 4-way Wilkinson --- CH0..CH3 --- J900..J903
                          |                                                 element ports
                     U901 AD8318
```

`U900` picks which measurement path sees the common node: the analyser on one side,
the on board detector on the other. That's the two path setup from section 5.3 of
`docs/architecture/rev-a-rf-architecture.md`.

Each channel has, in order: an enable switch, which either passes the signal on or
terminates the channel in 50 ohm, then three switched line bits in a row, of 45, 90
and 180 degrees. Seven switches per channel, 28 in total, plus `U900`.

Connections are made with labels instead of long drawn wires. Every pin gets a short
stub and a net name, so the netlist comes from the names, and no connection depends on
two lines happening to touch.

## Regenerating

```bash
python tools/generate-schematic.py
```

The generator is the real source. You can edit the schematic by hand in KiCad, but the
next run of the generator will overwrite it. So a change that should stick belongs in
the generator.

## Checks

```bash
kicad-cli sch erc --severity-all --exit-code-violations aetherarray-reva.kicad_sch
kicad-cli sch export bom --output bom/preliminary-bom.csv aetherarray-reva.kicad_sch
```

Current result: **0 violations**. See `erc/erc-notes.md`.

## What the bill of materials says

It's exported from the schematic, so it counts what's actually drawn.

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
| Header | 1 | interface to the controller. **Superseded by decision 0005**, see below |

**One difference from the architecture document.** Section 6 of
`docs/architecture/rev-a-rf-architecture.md` budgeted for 28 switches. Drawing the
schematic added one, `U900`, so the detector and the analyser don't both hang off the
common node all the time. Wiring both in permanently would load the path and split the
signal even when the detector isn't being used. It costs about 0.5 EUR and roughly
0.5 dB of loss in the common arm, and in return the two measurement paths are properly
exclusive.

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
| 5 V | controller, through `J905` | `U901` only, 68 mA typical |
| 3V3 | controller, through `J905` | 29 switches and 2 sensors, microamp parts |

The controller is the only power source. So its pins on `J905` are the design's power
outputs, and every other supply pin is an input. That's why the rule check passes
without a power flag anywhere.

## Superseded by decision 0005, re-capture required

This schematic was drawn before the controller changed, and **it doesn't match the
architecture any more**. The radio side is fine: the divider, the switched line chains,
the element ports and the detector are all unchanged, and so is the sixteen bit beam
state.

Here's what has to change when it's redrawn:

| Change | Reason |
| --- | --- |
| `J905` becomes a general controller interface, about 26 signal lines plus interleaved grounds, so a 2 by 20 rather than a 2 by 13 | `docs/architecture/control-architecture.md` section 7 |
| Two registered buffers appear between `J905` and the switch control inputs, clocked by a new `STROBE` line | electrical compatibility is undemonstrated, and the beam state must apply at one instant at the board |
| The two analogue return pins become a four wire serial converter interface | the fabric cannot sample an analogue voltage |
| A serial converter is added beside `U901` | keeps a 2.5 mV per 0.1 dB signal off the ribbon cable |

Until that's done, treat this schematic as the record of the radio design, and
`docs/architecture/control-architecture.md` as the record of the control design.

The redraw waits on EXP-005 Phase A. That experiment decides the last two rows, through
open item H3, and it can reopen decision 0005 through R9
(`experiments/EXP-005-repeatability-floor.md` section 10). Releasing the board also
waits on H1. The full gate for ordering is F1 to F5 in decision 0006.
