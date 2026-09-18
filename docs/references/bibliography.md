# Bibliography

- Status: in progress, first entries verified
- Last reviewed: 2026-09-17

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

[I6] Analog Devices. AD8318 data sheet, 1 MHz to 8 GHz logarithmic detector and
     controller.
     https://www.analog.com/media/en/technical-documentation/data-sheets/ad8318.pdf
     Retrieval timed out here, so no figure from it is quoted anywhere. Wanted for the
     logarithmic slope, the dynamic range for 1 dB conformance near 2.2 GHz, and the
     drift over temperature, which gate G2 depends on.
```

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
