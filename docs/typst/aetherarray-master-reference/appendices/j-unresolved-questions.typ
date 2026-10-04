#import "../template.typ": *

== Appendix J. Unresolved questions, contradictions and stale documentation

Found while writing this document. None is resolved here; each needs its owner's decision or edit.

*Technical points where repository wording should be corrected.*

1. _The $4 N - 4$ bound is stated as necessary._ `docs/architecture/ml-calibration.md` section 3
   and decision 0002 say power only recovery "generically requires at least $4 N - 4$". The
   literature proves $4 N - 4$ sufficient for generic vectors; necessity is proved only for some
   dimensions; eleven suffice at $N = 4$ (section 11.5). The conclusion survives in substance; the
   argument should be restated (section 11.6), and uncertainty I16 extended.
2. _A faster classical power only baseline is missing._ The fast amplitude only method of Long and
   co-authors, about $2 N$ readings, is not in the baseline list B1 to B7 of
   `benchmarks/specification.md`; EXP-012 should include it, after verification.
3. _Decision 0002's second reopening condition was triggered and not written up._ G1 passed
   (decision 0004), and the condition asks for the first calibration comparison to be redone; the
   conclusion is unchanged and arguably strengthened, but the redone comparison is not recorded.
4. _The uniform array's first sidelobe at $N = 4$ is $- 11.3$ dB, not about $- 13$ dB._ The README
   table, `docs/mathematics/formulation.md` section 3 ("independent of N") and the EXP-001
   acceptance checklist ("first side lobe near -13 dB") use the large $N$ value; a correct EXP-001
   simulator would fail that check at $N = 4$.
5. _Common gain unobservability._ The repository says a common gain scaling leaves the sum port
   reading unchanged; strictly it changes absolute power, and is unobservable because it is
   confounded with the unknown probe path gain (section 11.4).
6. _"Degrades rather than failing silently"_ in `docs/mathematics/inverse-calibration.md` section 3
   holds only for a prior whose uncertainty is calibrated (section 39.2).
7. _The label reference plane is not fixed in one place_: conducted labels at element ports avoid
   enable switch leakage but exclude the antenna board; radiated per channel labels include
   everything but suffer leakage (section 16).
8. _No target for $M_"required"$_: no pointing, null depth or sensing target and no risk
   level $alpha$ are recorded (section 0.2).
9. _Patch bandwidth against band 57a_: the analytical patch bandwidth, about 26 MHz, is about a
   third of the 83.5 MHz band over which decisions 0007 and 0008 judge (section 6.4).
10. _The AP-S direction is not recorded_, and its receiver requirement, separating wanted from
    interfering sources, is not met by the AD8318 alone (section 47). Demonstration time
    calibration would have to be power only and over the air against a commercial source, since no
    analyser travels to the venue.
11. _`ansys-aedt-core` is not pinned_ in `requirements.txt`, so the SIM-001 environment is recorded
    only in session notes.
12. _Over the air calibration in a room is not a hardware calibration._ Found in the ISAC pass,
    version 0.2. The power forward model of `docs/mathematics/inverse-calibration.md` section 2 and
    the G4 test of decision 0008 assume a single far field probe at broadside. A demonstration
    calibration against an ambient transmitter at another angle, with multipath, estimates the
    product $h_n s_n$ of hardware and incident field (section 10bis.5). It would also trigger decision
    0008's reopening condition "the probe position of the bench changes from broadside". How the
    demonstrator calibrates, and what its calibration means, needs a decision before it is designed.
13. _One experiment's noise is the other's signal._ EXP-005 Phase B treats the effect of a person
    moving as part of the repeatability floor; in the sensing mode that effect is the signal. The floor
    used to judge drift must be measured in a controlled, unoccupied configuration, and the two uses
    of the same measurement kept apart.

*Stale or superseded text outside decision records.* Decision records are kept as written by
convention; these other documents could carry a supersession note.

#table(
  columns: (168pt, 7.1fr, 159pt),
  table.header([Document], [Stale statement], [Superseded by]),
  [`README.md`], ["104 tests"; "PyAEDT, planned, not used yet"; "Line lengths and antenna sizes wait for the board stack up"; the "Where it stands" table, last reviewed 2026-09-28], [160 tests at the baseline; the SIM-001 builder; decision 0009],
  [`README.md`, `docs/mathematics/formulation.md` section 3], [side lobe level about $- 13$ dB for four elements], [item 4 above],
  [`docs/scope.md`, last reviewed 2026-08-21], ["Smallest credible prototype: two elements ... going to four elements adds no new question"; Bayesian optimisation described as choosing maximally informative measurements], [decision 0002; `docs/architecture/ml-calibration.md` sections 4 and 8],
  [`docs/mathematics/formulation.md` section 7], [Bayesian optimisation as "the most defensible way to bring learning into this project"], [decision 0002],
  [`docs/architecture/ml-calibration.md` section 4 update; `docs/architecture/rev-a-rf-architecture.md` section 8 and 8.1; `docs/hardware/rev-a-requirements.md` section 6], [the pattern synthesis track scheduled or "worth running" because $Q^(N - 1) = 512$], [decision 0005; `ml-calibration.md` section 6, ML-D; `inverse-calibration.md` section 5],
  [`experiments/EXP-004-instrument-audit.md` status line], ["five of nine observations recorded"], [`results/EXP-004/README.md`: four complete, four partial, one not taken],
  [`ROADMAP.md`], ["Two element array built" as a phase 3 milestone], [decision 0002 makes four elements the smallest prototype for the learning track; two remain valid for the physics demonstration],
  [`docs/architecture/rev-a-rf-architecture.md` section 5.5], [converter resolution computed for 12 bits over 3.3 V], [decision 0005 and `control-architecture.md` section 4.1],
  [`experiments/EXP-005-repeatability-floor.md` section 7.3], [0.5 mV called "about one fortieth" of the detector's temperature figure], [$plus.minus 0.5$ dB is $plus.minus 12.5$ mV, so the ratio is nearer one twenty fifth of the half span; the rule itself is unaffected],
)

*Open questions carried by the repository*, in `docs/uncertainties.md`: I1 to I27, with I12 (drift
above the floor, gate G2) the most consequential, and I16, I18, I19, I24 to I27 directly relevant to
this document.
