# Bibliography

- Status: in progress, first entries verified
- Last reviewed: 2026-10-03

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

Bibliographic details checked on 2026-09-26, for gate G4 and decision 0008.

```
[A23] W. K. Kahn, H. Kurss. Minimum-scattering antennas. IEEE Transactions on Antennas
     and Propagation, 13(5), 671-675, 1965. doi:10.1109/TAP.1965.1138529.
     Consulted 2026-09-26, bibliographic details and abstract only.
     Defines the canonical minimum scattering antenna, invisible when its terminals are
     open circuited, so that it radiates according to its port current. The
     approximation behind the coupled forward model of decision 0008.

[A24] W. Wasylkiwskyj, W. K. Kahn. Theory of mutual coupling among minimum-scattering
     antennas. IEEE Transactions on Antennas and Propagation, 18(2), 204-216, 1970.
     doi:10.1109/TAP.1970.1139649.
     Consulted 2026-09-26, bibliographic details and abstract only.
     Expresses the mutual coupling of such antennas through their radiation patterns
     alone. The reason an S parameter matrix can stand in for the embedded element
     patterns, and the reason the simulation stage checks that it does.
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

[V7] Ansys. HFSS Student Limitations. Ansys Electromagnetics Suite 2025 R1 help,
     ansyshelp.ansys.com, Electronics v251, HFSS, Getting Started.
     Consulted 2026-09-26, manufacturer documentation, full page.
     3D volume mesh 64,000 elements, 3D surface 8,000, 2D 2,000 triangles; DXF and
     STEP import only; local solve only; HPC limited to 4 cores; SBR+, mesh
     assemblies, circuit model generation from S parameters, geometry export,
     optiSLang, Workbench, beta features and Linux not supported. No port limit is
     stated. Sets the escalation rule of docs/runbooks/README.md; another release
     must be checked again.
```

## Fabrication, laminate and simulator sources, checked 2026-10-03

Consulted for decision 0009, the Rev A stack-up. Fabricator pages carry no revision
unless one is shown; prices and lead times are as published on that date and are
re-checked before any order. No instant quote could be obtained from any fabricator,
because every quote page needs a browser. Values in `hardware/rev-a/stackup/*.json`
cite these identifiers.

```
[V8]  JLCPCB. Controlled Impedance PCB Layer Stackup. https://jlcpcb.com/impedance
      Consulted 2026-10-03, no date shown. Fabricator documentation.
      Published 4 layer 1.6 mm stack-ups. JLC04161H-7628: 7628 prepreg 0.2104 mm,
      core 1.065 mm, outer copper 0.035 mm, inner 0.0152 mm. Prepreg permittivity
      7628 4.4, 3313 4.1, 1080 3.91, 2116 4.16; core 4.6; no frequency stated.
      Solder mask in the calculator: 1.2 mil over substrate, 0.6 mil over trace,
      permittivity 3.8. "The PCB will be strictly produced in accordance with the
      following stackup." Impedance control at no extra charge.

[V9]  JLCPCB. User Guide to the JLCPCB Impedance Calculator.
      https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator
      Consulted 2026-10-03, last updated 2026-09-16. Fabricator documentation.
      Calculations for 4 to 8 layers assume Nan Ya NP-155F core; resin content 7628
      49 %, 3313 57 %, 1080 67 %, 2116 54 %; NP-155F cores above 0.70 mm 4.43,
      which conflicts with the 4.6 of V8. Outer copper 1.6 mil in the calculator,
      against 0.035 mm on V8. "For reference only".

[V10] JLCPCB. Multi-Layer PCB Standard Laminated Structures.
      https://jlcpcb.com/help/article/multi-layer-pcb-standard-laminated-structures
      Consulted 2026-10-03, last updated 2026-09-09. Fabricator documentation.
      Stack-up copper is finished copper; permittivity values are deduced, not the
      supplier's raw data; free impedance testing with a tolerance of 20 %.

[V11] JLCPCB. PCB Manufacturing and Assembly Capabilities.
      https://jlcpcb.com/capabilities/pcb-capabilities
      Consulted 2026-10-03, no date shown. Fabricator documentation.
      Impedance control on 4 layers and more, tolerance 10 %; board thickness
      tolerance 10 % at 1.0 mm and above; track width tolerance 20 %; minimum
      trace and space 0.09 mm multilayer and 0.10 mm two layer at 1 oz; via
      0.15 mm hole, 0.25 mm pad; annular ring 0.15 mm minimum; finishes HASL,
      ENIG, OSP; solder mask at least 10 um, permittivity 3.8; FR-4 two layer
      permittivity 4.5, no frequency; laminates "from suppliers including Nan Ya,
      KB, Shengyi"; maximum board 670 x 600 mm two layer, 663 x 593 mm four layer.

[V12] Nan Ya Plastics. NP-155F data sheet.
      https://cclqc.npc.com.tw/cclfile/pdt/Datasheet_NP-155F_1761637097200.pdf
      Consulted 2026-10-03, issued 2008-03-01, new 2025-10-27. Laminate vendor.
      IPC-TM-650 2.5.5.9, at 1 GHz: 0.062 inch laminate permittivity 4.2 to 4.4,
      loss tangent 0.014 to 0.016; 0.020 inch laminate 3.9 to 4.1 and 0.012 to
      0.014. "Data shown are nominal values for reference only." Nothing at
      2.44 GHz.

[V13] JLCPCB. Surface finish. https://jlcpcb.com/help/article/jlcpcb-surface-finish
      Consulted 2026-10-03, last updated 2026-09-09. Fabricator documentation.
      ENIG nickel about 3 to 6 um.

[V14] JLCPCB. UL certification. https://jlcpcb.com/help/article/ul-certification
      Consulted 2026-10-03, last updated 2026-09-09. Fabricator documentation.
      Laminates by UL class: two layer NP-140F, KB-6164, S1141 or S1000H;
      multilayer NP-140F, NP-155F, KB-6164, S1141, KB-6165, S1000H or S1000-2M.
      So no single brand is guaranteed for an order.

[V15] Kingboard, issued by Matrix USA. KB6167F data sheet, Rev 20200616, as
      hosted by OSH Park.
      https://docs.oshpark.com/resources/two-layer-substrate-Kingboard-KB6167F.pdf
      Consulted 2026-10-03. Laminate vendor. 7628 x 8 construction, permittivity
      4.6 at 2 GHz, loss tangent 0.014. One edge of the FR-4 permittivity bounds.

[V16] JLCPCB. PCB fabrication services and production time.
      https://jlcpcb.com/help/article/pcb-fabrication-services-and-production-time
      Consulted 2026-10-03, last updated 2026-09-09. Fabricator documentation.
      Up to 100 x 100 mm, 1.6 mm: two layer 5 pieces 24 hours; four layer 5
      pieces 2 to 5 days.

[V17] Rogers Corporation. RO4000 Series High Frequency Circuit Materials, data
      sheet RO4003C and RO4350B. PUB 92-004, revised 080322.
      https://www.rogerscorp.com/-/media/project/rogerscorp/documents/advanced-electronics-solutions/english/data-sheets/ro4000-laminates-ro4003c-and-ro4350b---data-sheet.pdf
      Consulted 2026-10-03. Laminate vendor.
      Process permittivity, IPC-TM-650 2.5.5.5 clamped stripline at 10 GHz:
      RO4003C 3.38 +/- 0.05, RO4350B 3.48 +/- 0.05. Design permittivity,
      differential phase length method, 8 to 40 GHz: 3.55 and 3.66. Loss tangent
      at 2.5 GHz: 0.0021 and 0.0031. Thickness tolerances: 0.020 inch +/- 0.0015,
      0.060 inch +/- 0.004. Chart 2 reads higher than the design value near
      2.5 GHz for 20 mil standard foil, read from an image, about 3.75 for RO4350B.

[V18] Rogers Corporation. Copper Foils for High Frequency Circuit Materials.
      PUB 92-243.
      https://www.rogerscorp.com/-/media/project/rogerscorp/documents/advanced-electronics-solutions/english/properties---detailed-characteristics/copper-foils-for-high-frequency-circuit-materials.pdf
      Consulted 2026-10-03. Laminate vendor.
      Typical Sq, dielectric side, standard electrodeposited foil on RO4000:
      1 oz 3.2 um, 1/2 oz 2.8 um; LoPro 0.9 um. Rough foil raises the apparent
      permittivity, which the Hall and Huray model does not account for. The only
      roughness data found for any candidate; none for FR-4 at the fabricators.

[V19] JLCPCB. High Frequency PCB. https://jlcpcb.com/pcb-fabrication/high-frequency-pcb
      Consulted 2026-10-03, no date shown; and the launch article of 2023-03-09,
      https://jlcpcb.com/blog/112-rogers-pcb-ptfe-pcb-high-frequency-pcb-is-available-on-jlcpcb
      Fabricator documentation. RO4350B two layer only, cores 0.51, 0.76 and
      1.52 mm, finished 0.6, 0.9 and 1.65 mm, 1 oz, ENIG, 4 to 5 days, "starting
      at just $47"; in 2023, 99.5 USD for 5 pieces within 10 x 10 cm. No RO4003C,
      no hybrid, no stated impedance control.

[V20] OSH Park. Four Layer service. https://docs.oshpark.com/services/four-layer/
      Consulted 2026-10-03, page dated 28-JAN-2026. Fabricator documentation.
      FR408HR; L1 to L2 2113 prepreg 7.87 mil +/- 0.797 mil; L1 copper 1.7 mil;
      permittivity 3.61 at 1 GHz; ENIG; 5 mil trace and space; 10 USD per square
      inch for three copies; ships in 9 to 14 days. A FR408HR shortage notice was
      posted on 2026-07-21,
      https://docs.oshpark.com/troubleshooting/mixed-material-4-layer-stackup/

[V21] Isola. FR408HR Dk and Df tables, Revision G, 2026-01-05.
      https://www.isola-group.com/wp-content/uploads/data-sheets/fr408hr-laminate-and-prepreg__Dk_Df_Tables.pdf
      Consulted 2026-10-03. Laminate vendor. 2113 prepreg, 57.5 % resin: 3.61 and
      0.0090 at 2 GHz; 2116 at 55 %: 3.66. All FR408HR glass is spread weave.

[V22] Eurocircuits. RF pool service. https://www.eurocircuits.com/services/rf-pool/
      Consulted 2026-10-03, no date shown. Fabricator documentation.
      RO4350B pooled from one piece, two layer 0.25 and 0.50 mm, four layer
      1.00 mm with FR-4 prepreg; 5 working days. Build-up and price only in the
      online configurator, so not evaluated.

[V23] Ansys. HFSS Student Limitations. Ansys Electromagnetics Suite 2025 R2 help,
      https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/HFSS/Content/GettingStarted/HFSSStudentLimitations.htm
      Consulted 2026-10-03, manufacturer documentation. The same limits as V7,
      and also "optiSLang and LSDSO not supported", which the 2025 R1 page states
      too and V7 omitted. The release installed here is 2025 R2. Touchstone and
      port solution export are not mentioned either way.

[V24] AISLER. 4 layer 1.6 mm stack-up, staff page on the vendor's documentation
      site. https://community.aisler.net/t/4-layers-1-6mm-35-m-stackup/5457
      Consulted 2026-10-03, edited 2026-05-12. Fabricator documentation.
      Prepreg permittivity "4.0 - 4.3", no frequency, no laminate named, impedance
      "only provide a basic orientation". Screened out: no named laminate.

[V25] PCBWay. High frequency PCB page and quick order form.
      https://www.pcbway.com/pcb_prototype/What_is_High_Frequency__HF__PCB_.html
      Consulted 2026-10-03, no date shown. Fabricator documentation.
      RO4003C and RO4350B offered, 7 to 10 days; no price obtained, no minimum
      quantity or impedance statement found. Screened out on missing evidence.
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
