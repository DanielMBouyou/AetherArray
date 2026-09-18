# Electrical rule check, result and open items

- Status: clean, 0 violations
- Last reviewed: 2026-09-18

## Result

```
kicad-cli sch erc --severity-all --exit-code-violations aetherarray-reva.kicad_sch
0 violations, exit code 0
```

Run with `--severity-all`, so errors, warnings and exclusions are all reported. No
rule severity was lowered and no violation was excluded to reach this: the project
file carries an empty exclusion list. Output in `erc-report.txt`.

## What the check caught while the schematic was being built

Recorded because each one was a real defect, not a false alarm, and because the count
shows the check is doing work.

| Defect | How it appeared | Fix |
| --- | --- | --- |
| Component origins off the 1.27 mm connection grid | 296 off grid endpoint warnings | every placement snapped to the grid |
| Hierarchical sheet pin sides inverted, so no sheet pin connected | 24 unconnected pin errors and 24 dangling wire warnings | left edge pins are angle 180, right edge angle 0 |
| Control inputs fed from a connector of passive pins | 16 undriven input errors | a real interface symbol whose pins are outputs, inputs and power outputs by function |
| Two power flags on rails already driven | power output conflicts | flags removed; the Nucleo interface is the only source |
| Four channel sheets placed over the root components | every net merged into two | sheets moved to a clear band |
| Detector filter capacitors sharing a grid cell with the divider isolation resistors | 3V3 shorted to ground, `ADC_DET` shorted to `CH2_RF` | capacitors moved to a free row |

The last two were shorts that a visual review would very likely have missed, because
the labels involved sat exactly on top of one another.

## Deliberately unresolved, and why none of it blocks review

These are open by decision, not by oversight. None is suppressed in the tool; each is
simply not something the rule check can or should settle.

| Item | Why it is open | When it closes |
| --- | --- | --- |
| No footprints assigned | footprint choice belongs with layout, which decision 0003 does not authorise | at layout |
| Transmission line physical lengths | they depend on $f_0$ and the stack-up, see `layout-constraints.md` | after EXP-004 and the stack-up choice |
| PE4259 control polarity | the vendor pin table is captured, but the single-pin truth table, which level selects RF1, was not obtainable here | before firmware; it affects no net in this schematic |
| Loop filter value, `C906` at 220 pF | the response depends on the measurement bandwidth wanted, which the first measurements will set | at bring-up |
| Temperature compensation resistor, `R903` at 18k | the correct value depends on the band finally chosen | after EXP-004 |
| Antenna board not captured | Rev A is two boards and only the beamformer is in scope here | when the array geometry is designed |
| Exposed pad of `U901` | it is internally tied to `CMIP` and must be soldered to ground; that is a footprint property, so it cannot be expressed in a schematic | at layout |

## A note on what a clean check does not mean

The rule check proves the netlist is consistent with itself: no shorted rails, no
undriven inputs, no floating pins, everything on grid. It proves nothing about whether
the design works. Insertion loss through seven cascaded switches, the isolation
between channels, the behaviour of the reflective switch terminations and the
detector's dynamic range against the real signal level are all open questions that
belong to simulation and to bring-up, not to a rule check.
