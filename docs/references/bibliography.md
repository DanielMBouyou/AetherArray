# Bibliography

- Status: in progress, first entries verified
- Last reviewed: 2026-09-21

`research/state-of-the-art.md` holds the leads and why they matter. This file holds
the exact reference once it has been checked.

## Rules

1. A reference enters here only after it has been found and verified (authors,
   title, venue, year). Until then it stays a lead in the state of the art
   document.
2. Each entry keeps a stable identifier (`A1`, `O2`, and so on) reused across the
   repository.
3. For online documents, record the consultation date and, where possible, a way to
   retrieve the exact version consulted.
4. Never copy a document under a restrictive licence into the repository. We record
   the reference, not the file.

## Format

```
[ID] Authors. Title. Venue, year. Link or identifier.
     Consulted YYYY-MM-DD. Note: research/notes/NNN-name.md
     One line on what this brings to the project.
```

## Verified entries

Bibliographic details checked on 2026-09-17. Verified here means author, title, venue
and year confirmed. It does not mean the full text has been read: where only the
abstract or a secondary summary was consulted, the entry says so, and no number from
that source is quoted elsewhere as established.

```
[A6] S. Mano, T. Katagi. A method for measuring amplitude and phase of each radiating
     element of a phased array antenna. Transactions of the IEICE, J65-B, 555-560,
     1982. English translation in Electronics and Communications in Japan, Part I,
     65(5), 1982, doi:10.1002/ecja.4410650508.
     Consulted 2026-09-17, abstract and secondary literature only. Note: not yet written.
     The rotating element field vector method, the project's power only baseline.

[A7] H. M. Aumann, A. J. Fenn, F. G. Willwerth. Phased array antenna calibration and
     pattern prediction using mutual coupling measurements. IEEE Transactions on
     Antennas and Propagation, 37(7), 844-850, 1989.
     Consulted 2026-09-17, abstract only. Note: not yet written.
     Calibration with no external probe. Its one stated restriction, the ability to
     transmit and receive with pairs of array elements, is the origin of requirement
     R1 in docs/hardware/rev-a-requirements.md.

[A12] A. Conca, D. Edidin, M. Hering, C. Vinzant. An algebraic characterization of
     injectivity in phase retrieval. Applied and Computational Harmonic Analysis,
     38(2), 346-356, 2015. Preprint arXiv:1312.0158.
     Consulted 2026-09-17, abstract and secondary summary only. Note: not yet written.
     Establishes that 4N-4 generic intensity measurements suffice to recover a vector
     in complex N space up to a global phase. Supplies the information bound used in
     docs/architecture/ml-calibration.md section 3.

[A13] B. Shahriari, K. Swersky, Z. Wang, R. P. Adams, N. de Freitas. Taking the human
     out of the loop: a review of Bayesian optimization. Proceedings of the IEEE,
     104(1), 148-175, 2016.
     Consulted 2026-09-17, bibliographic details only. Note: not yet written.
     Review reference for the pattern synthesis track. Note that this project uses
     Bayesian experimental design, not Bayesian optimisation, when the measurement
     count itself is the objective.

[A16] Z. Sarayloo, N. Masoumi, H. Shahi and others. A convolutional neural network
     approach for phased array calibration using power-only measurements. 2020 28th
     Iranian Conference on Electrical Engineering (ICEE), 1-6, 2020.
     Consulted 2026-09-17, abstract only. Note: not yet written.
     The nearest published form of the learned first calibration control, method M1.

[A18] S. D. Silverstein. Application of orthogonal codes to the calibration of active
     phased array antennas for communication satellites. IEEE Transactions on Signal
     Processing, 45(1), 206-218, 1997.
     Consulted 2026-09-17, abstract and secondary summary only. Note: not yet written.
     Orthogonal coding baseline B5. Measures every element simultaneously with the
     full array radiating, trading raw count for integration time and dynamic range.

[A19] S. S. Tambovskiy, G. Fodor, H. M. Tullberg. Antenna array calibration via
     Gaussian process models. arXiv:2301.06582, 2023. Presented at WSA and SCC 2023.
     Consulted 2026-09-17, abstract only. Note: not yet written.
     Precedent for a Gaussian process rather than a deep network when the measurement
     set is sparse, which matches this project's data budget.

[A20] S. Li, Y. Zhou, C. Zhang, L. Kong, K. Liu, Y. Xie, C. He. Phased array
     calibration based on rotating-element harmonic electric-field vector with time
     modulation. arXiv:2504.16107, 2025.
     Consulted 2026-09-17, preprint full text. Note: not yet written.
     Source for the statement that the classical rotating element method consumes K
     times N measurements, with K at least three.
```

## Vendor documentation, checked 2026-09-18

Manufacturer product pages and distributor listings consulted for decision 0003.
Part status, stock and unit price are quoted as read on that date and are re-checked
before any order. Figures marked to verify were not obtainable from a machine
readable datasheet here.

```
[V1] pSemi. PE4259, UltraCMOS SPDT RF switch, 10 MHz to 3000 MHz.
     MPN as ordered: PE4259-63. SC-70-6. 0.35 dB insertion loss, 30 dB isolation,
     1.8 V to 3.3 V, integrated CMOS control logic.
     Status active and recommended for new designs. 0.84 USD at one unit, 0.601 at
     ten, 0.475 at one hundred, more than 300000 units in distributor stock.
     Consulted 2026-09-18, product page and distributor listing.
     The part the Rev A phase chain and channel enable are built from.
     To verify: insertion loss and state to state repeatability at 2.4 GHz.

[V2] pSemi. PE44820, UltraCMOS 8-bit RF digital phase shifter.
     MPN as ordered: PE44820B-X. 32 lead 5 mm QFN. 358.6 degrees in 1.4 degree steps.
     Nominal band 1.7 GHz to 2.2 GHz, extended narrowband operation 1.1 GHz to 3.0 GHz.
     Status active, 328 units in distributor stock, 13.09 USD at one unit.
     Consulted 2026-09-18. The datasheet is an image based file and was not machine
     readable here, so no insertion loss figure is quoted.
     Evaluated and rejected for Rev A on budget and on band edge, decision 0003.

[V3] pSemi. PE4302 is discontinued. PE4312 is the pin compatible successor, a 6-bit
     digital step attenuator, 1 MHz to 4 GHz, 31.5 dB in 0.5 dB steps, parallel and
     serial control, single 3 V supply.
     Consulted 2026-09-18.
     Named as the amplitude control provision in decision 0003. Recorded chiefly
     because PE4302 is still widely quoted and is no longer orderable.

[V4] Analog Devices. ADL5390, RF and IF vector multiplier, 20 MHz to 2400 MHz.
     Continuous 360 degree phase and amplitude control from two analogue voltages,
     output amplitude from about +5 dB to below -30 dB, requires quadrature inputs.
     Consulted 2026-09-18, product page.
     The only compared option offering amplitude control. Rejected for Rev A because
     2.4 GHz is its specified upper limit.

[V5] Microchip. MCP9808, I2C digital temperature sensor.
     About 0.25 degrees Celsius typical accuracy over -40 to +125 degrees Celsius,
     0.0625 degree resolution, 8 pin MSOP or DFN.
     Consulted 2026-09-18.
     Requirement R4 telemetry. TMP117 is the higher accuracy alternative at higher
     cost, and 0.25 degrees is ample for separating array drift from detector drift.

[V6] Analog Devices. AD8318, 1 MHz to 8 GHz, 70 dB logarithmic detector and
     controller. Data sheet revision E.
     https://www.analog.com/media/en/technical-documentation/data-sheets/AD8318.pdf
     Accurate logarithmic conformance from 1 MHz to 6 GHz with useful operation to
     8 GHz; plus or minus 1 dB over a 55 dB range below 5.8 GHz; nominal slope minus
     25 mV per dB; stability over temperature plus or minus 0.5 dB; single 5 V supply,
     about 68 mA typical.
     Consulted 2026-09-18. Direct retrieval of the file failed repeatedly in this
     environment; the figures above were read from the revision E document through a
     search index and each one was cross checked against an independently supplied
     value before being recorded.
     Requirement R3. These figures close item E7 of the Rev A architecture and are
     turned into schematic requirements in section 5.5 of that document.
```

## Instrument sources, checked 2026-09-20

Capability references for `docs/hardware/measurement-bench.md`. A capability here says
what a model family can do. It says nothing about whether that instrument is present.

```
[T1] Rohde and Schwarz. R&S ZVL vector network analyser, family reference. The unit on
     the bench has not been identified to a variant; the 3 GHz member is the one whose
     published range matches the observation.
     9 kHz to 3 GHz, 2 ports, N connectors. Source power range -50 dBm to 0 dBm.
     Calibration: full one port (OSM), full two port (TOSM), and one path two port.
     Dynamic range up to 123 dB. Remote control over 100BaseT, GPIB optional (B10).
     Capability figures above: distributor and aggregator listings, not manufacturer
     documentation. The manufacturer datasheet is a scanned image and could not be
     read here, and the manufacturer product page is now a discontinued product stub
     carrying no option list. Retrieval attempted 2026-09-20 and 2026-09-21.

[T1a] Rohde and Schwarz. R&S ZVL option designations, confirmed 2026-09-21 against the
     manufacturer's own option listing and manual catalogue for the family:
     K1 spectrum analysis, K2 distance to fault, K3 time domain analysis.
     K1 is corroborated independently by the existence of a manufacturer document
     titled "R&S ZVL-K1 Operating Manual", which describes the spectrum analyser mode.
     Operating manual catalogue entry:
     https://www.rohde-schwarz.com/us/manual/rs-zvl-operating-manual_78701-28770.html
     Family option listing: rohde-schwarz.com, product page zvl-options_63490-9014.
     Limit on this source: the live product pages render as discontinued product
     stubs, so the confirmation rests on the manufacturer's option listing and manual
     catalogue rather than on a datasheet PDF, which remains unreadable here.
     **This establishes what each designation means. It establishes nothing about
     which options are installed on the unit on the bench.** That is observation O8,
     which records the instrument's own option list verbatim.
     Supersedes the earlier entry in this file, which recorded these designations as
     unconfirmed and not to be relied on.

[T2] Keysight, formerly Agilent. N9923A FieldFox handheld RF vector network analyser,
     2 MHz to 4 GHz, 6 GHz variant available. S11 and S21 in the base unit; four
     S-parameter measurement is option dependent. **Option 122 is full two port
     S-parameters**, confirmed 2026-09-21 against the manufacturer's own options page
     and technical overview for this model: it adds S22 and S12 to the base S11 and
     S21, and provides full two port calibration.
     https://www.keysight.com/us/en/options/N9923A/fieldfox-a-handheld-rf-vector-network-analyzer-4-ghz-6-ghz.html
     Technical overview 5990-5087, keysight.com asset 7018-02396.
     The same manufacturer source gives more than 100 dB of dynamic range for vector
     measurement, from four independent receivers. The 90 dB figure for four parameter
     measurement remains a secondary listing. Built in quick calibration
     in addition to SOLT. Discontinued, still supported.
     Consulted 2026-09-20, re-checked 2026-09-21.
     Supersedes the earlier entry, which recorded option 122 as not established.
     The intended independent cross check, conditional on presence and on option 122
     being installed.

[T3] Keysight, formerly Hewlett Packard. 8714C economy network analyser, 300 kHz to
     3 GHz. Output power up to +16 dBm. Dynamic range above 100 dB in narrowband
     mode. Obsolete.
     Consulted 2026-09-20. Second cross check, conditional on presence. The +16 dBm
     output is above the radiated ceiling this project must respect and has to be set
     deliberately if ever used for a radiated measurement.

[T4] Keysight, formerly Agilent. N9000A CXA signal analyser, 9 kHz to 26.5 GHz
     depending on model, absolute amplitude accuracy 0.5 dB. Obsolete.
     Consulted 2026-09-20. Absolute power reference for AD8318 validation,
     conditional on presence.

[T5] Keysight, formerly Hewlett Packard. 8562A portable spectrum analyser,
     **9 kHz to 22 GHz**. Obsolete.
     https://www.keysight.com/us/en/support/8562A/9-khz-22-ghz-spectrum-analyzer.html
     Consulted 2026-09-20, corrected 2026-09-21. Second spectrum instrument,
     conditional on presence.
     Correction: the earlier entry gave 1 kHz as the lower limit, taken from a
     secondary listing. The manufacturer's own product title gives 9 kHz. Nothing in
     the measurement plan depended on the difference, since this instrument is
     `[inventory]` and every use of it is conditional.
```

```
[T6] Terasic. DE1-SoC user manual, Cyclone V SoC development board.
     Two 40 pin expansion headers, 36 user pins each connected directly to the
     Cyclone V device, at 3.3 V with protection diodes, plus DC 5 V, DC 3.3 V and two
     grounds per header.
     On board converter: LTC2308, eight channel, 12 bit, up to 500 ksps, analogue input
     range 0 V to 4.096 V, reached from the fabric over a four wire serial interface at
     3.3 V.
     Consulted 2026-09-23, manufacturer user manual.
     The Rev A controller, decision 0005. Source of the 3.3 V expansion header level
     that makes the buffer on the radio frequency board necessary, and of the onboard
     converter retained as an independent cross check.
     Not obtained: the current limit of the header supply rails, which is an open item.
```

## Regulatory sources, checked 2026-09-19

```
[R1] European Commission. Commission Implementing Decision (EU) 2022/180 of 8 February
     2022 amending Decision 2006/771/EC as regards the update of harmonised technical
     conditions in the area of radio spectrum use for short-range devices. Annex,
     non-specific short range devices.
     https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022D0180
     Consulted 2026-09-19, annex rows read directly.
     Source of the band table in experiments/EXP-004-instrument-audit.md. Band 57a,
     2400 to 2483.5 MHz, 10 mW e.i.r.p., carries no duty cycle restriction, which is
     what permits a continuous carrier for radiated measurement. Every sub-band between
     863 and 870 MHz requires a mitigation technique or a duty cycle of at most 10 per
     cent, which is what eliminates that band for this work.
     Limit: this is the European harmonisation instrument. The national table of
     allocations may be more restrictive and has not been checked.
```

## Located but not yet verified

These have an identifier but lack confirmed authorship, or were not retrievable here.
They stay out of the verified list until that is fixed.

```
[A21] A power-only fast calibration method for phased array using convolution neural
     network. IEEE Xplore document 10660493, 2024. Authors not yet confirmed.
     Validated on a 64 element Ka band array. The 2024 development of A16, and the
     closest published claim of measurement count reduction by a learned method.

[A22] Phased array antenna calibration method: experimental validation and comparison.
     Electronics, 12(3), 489, 2023, doi:10.3390/electronics12030489.
     Retrieval refused here. Wanted for its measured comparison of calibration
     methods, which would be a direct cross check on the counts in section 2 of
     docs/architecture/ml-calibration.md.

[I1] Analog Devices. CN0566 circuit note, ADALM-PHASER phased array exploration
     platform. An eight element receive array near 10.25 GHz, using ADAR1000
     beamformers with a software defined radio and a single board computer. Per
     channel phase and gain resolution figures are to verify against the ADAR1000
     datasheet. This is the documented educational kit named as lead I1 in the state
     of the art.

```

`[I6]`, the AD8318 data sheet, has been resolved and moved to the verified vendor list
as `[V6]`.

## Where to look

| Source | Use | Caveat |
| --- | --- | --- |
| Open access paper repositories | find accessible versions | check it is the final version |
| Digital libraries of the professional societies | exact published reference | sometimes paywalled |
| Conference sites for antennas and propagation, microwave theory and signal processing | full proceedings | usually the best entry point |
| Vendor documentation | exact technical data | watch for superseded versions |
| Public code repositories | real implementations | check the licence before reusing anything |

## Internal references

| Document | Content |
| --- | --- |
| `research/state-of-the-art.md` | leads and reading priorities |
| `research/notes/` | one note per source read |
| `docs/references/glossary.md` | vocabulary |
