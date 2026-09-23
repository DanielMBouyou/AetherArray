# Layout constraints carried by the symbolic transmission lines

- Status: in progress, frequency frozen, physical lengths blocked on the stack-up
- Last reviewed: 2026-09-23

The schematic contains 30 `TLINE_SYMBOLIC` parts. They are not components to buy.
Each one is a piece of printed line whose **electrical** length is fixed by the
design and whose **physical** length cannot be computed until the board stack-up is
known. The working frequency was the other input and is now fixed. This file is the
contract between the two.

Each symbol carries the constraint in its own fields, so it travels with the part
rather than living only in prose:

| Field | Meaning |
| --- | --- |
| `EL_DEG` | electrical length in degrees at the working frequency |
| `Z0_OHM` | characteristic impedance the line must present |
| `LAYOUT` | one sentence saying what the line is for |

## 1. Converting an electrical length to a physical one

For a line of electrical length $\theta$ in degrees at frequency $f_0$:

```math
l = \frac{\theta}{360}\,\lambda_g,
\qquad
\lambda_g = \frac{c}{f_0\sqrt{\varepsilon_{\text{eff}}}}
```

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $l$ | physical length of the printed line | m |
| $\theta$ | electrical length required by the schematic field `EL_DEG` | degrees |
| $\lambda_g$ | guided wavelength in the chosen stack-up | m |
| $c$ | speed of light in vacuum | m/s |
| $f_0$ | working frequency, **fixed at 2.44 GHz by decision 0004** | Hz |
| $\varepsilon_{\text{eff}}$ | effective permittivity of the microstrip, from the stack-up and the trace width | dimensionless |

Worked example, to make the scale concrete and for no other purpose. On 1.6 mm FR4
with $\varepsilon_{\text{eff}} \approx 3.3$ at the now fixed $f_0 = 2.44$ GHz, the
guided wavelength would be about 68 mm, so a 45 degree section about 8.5 mm and a
180 degree section about 34 mm. **Those numbers remain an illustration, not a
specification.** The frequency is now fixed, but the permittivity is still assumed, and
the real lengths follow from the fabricated stack-up and are computed at layout.

## 2. The constraint is a difference, not a length

This is the single easiest thing to get wrong.

Each switched line bit has a reference arm, `EL_DEG` of 0, and a delay arm,
`EL_DEG` of 45, 90 or 180. **The reference arm is not zero length.** It is whatever
routing is needed to get from one switch to the other. What the design requires is:

```math
\theta_{\text{delay}} - \theta_{\text{reference}} = \theta_{\text{bit}}
```

measured between the same two reference planes, which are the RF ports of the two
switches forming that bit. A layout that makes the reference arm physically short and
the delay arm exactly $l$ long will be wrong by whatever the reference arm actually
measures.

## 3. Constraints, per structure

| Structure | Instances | Constraint |
| --- | --- | --- |
| Bit arms, 45 degrees | `TL101`, `TL102` and the same in each channel | delay arm exceeds reference arm by 45 degrees at $f_0$, both 50 ohm |
| Bit arms, 90 degrees | `TL103`, `TL104` and per channel | difference of 90 degrees at $f_0$, both 50 ohm |
| Bit arms, 180 degrees | `TL105`, `TL106` and per channel | difference of 180 degrees at $f_0$, both 50 ohm |
| Wilkinson arms | `TL901` to `TL906` | 90 degrees at $f_0$, **70.7 ohm**, paired with the 100 ohm isolation resistor of that stage |

## 4. Constraints across channels

The calibration work measures differences between channels, so systematic channel to
channel differences introduced by layout are indistinguishable from the defects under
study.

| Constraint | Reason |
| --- | --- |
| The four channels are laid out identically, not merely equivalently | any layout difference becomes a fixed error the calibration will faithfully measure and attribute to the hardware |
| The two arms of the divider at each Wilkinson stage are equal in length | an imbalance appears as a fixed amplitude and phase offset between element groups |
| Element port trace lengths from each channel output to its SMA are equal | otherwise the per element measurements carry an offset that the per element access was meant to remove |
| Line width is constant within a given impedance class | a width change is an impedance step, which is a reflection |

Equality here means to a tolerance still to be set. At 2.44 GHz roughly 1 mm of
microstrip is about 5 degrees, which sets the scale of what matters.

## 5. What is deliberately unresolved

> **Frozen on 2026-09-23 by decision 0004: $f_0 = 2.44$ GHz.** The analyser on the
> bench was observed to cover 9 kHz to 3 GHz with a complex S21 measurement, which is
> what the frequency was waiting on. The free space wavelength is therefore
> $\lambda_0 = 122.9$ mm.
>
> **The lengths in this file are still not computable, and the reason has changed.**
> They need the guided wavelength, which needs the stack-up: the substrate, its
> thickness and the resulting effective permittivity. The frequency is no longer the
> blocker. Nothing here may be computed until a stack-up is chosen.

| Item | Blocked on | Effect |
| --- | --- | --- |
| $\varepsilon_{\text{eff}}$ and the stack-up | choice of fabricator and material | every physical length, and the trace widths |
| Trace width for 50 ohm and 70.7 ohm | stack-up | layout |
| Matching tolerance between channels | a decision, not a measurement | layout acceptance |

None of these changes the schematic. That separation is the reason decision 0003 could
authorise capture while the frequency was still open, and it is why freezing the
frequency in decision 0004 changed no captured net.
