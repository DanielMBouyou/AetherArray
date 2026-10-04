#import "../template.typ": *

= Part XV. Literature and evidence <part-xv-literature-and-evidence>

=== XV.1 How the review was done, and its limits

On 2026-10-04 the references already in `docs/references/bibliography.md` were rechecked and a
wider search was made for work on phased array calibration, power only calibration, online and
over the air calibration, drift and temperature, Gaussian process and Bayesian calibration,
machine learning phase retrieval, experimental design, self calibration and ISAC receiving arrays.
*Every direct fetch from a publisher, IEEE Xplore, arXiv, DOI resolvers and bibliographic
databases was refused by the network policy of the environment.* Verification is therefore
*index level*: authors, titles, venues and abstract wording as they appear in search engine
results that index the publisher or preprint pages. No full text was read for this document. A
reference marked "index level" in the References may be cited for its existence and its stated
claim, and should be read in full before any number from it is used. Where a field could not be
confirmed, the References say so.

=== XV.2 What is already established

#table(
  columns: (2.8fr, 8.0fr, 5.9fr),
  table.header([Topic], [Established result], [Sources]),
  [power only calibration], [rotating element field vector: phase stepping of one element while total power is measured], [Mano and Katagi 1982 \[#link(<ref-A6>)[A6]\]; time modulated variant \[#link(<ref-A20>)[A20]\]],
  [self calibration through coupling], [adjacent element pairs transmit and receive; no external probe], [Aumann, Fenn and Willwerth 1989 \[#link(<ref-A7>)[A7]\]; in situ mutual coupling calibration tracking changes from an initial state on a 64 element panel \[#link(<ref-L18>)[L18]\]],
  [coded calibration], [all elements measured at once under orthogonal codes, with variance bounds], [Silverstein 1997 \[#link(<ref-A18>)[A18]\]],
  [fast multi element power only methods], [about $2 N$ power readings with three phase states], [Long and co-authors 2017 \[#link(<ref-L7>)[L7], #link(<ref-L8>)[L8]\]; Takahashi and co-authors 2008 \[#link(<ref-L9>)[L9]\]],
  [over the air calibration with complex signals], [calibration of a millimetre wave array in beam steering mode from measured complex signals], [Wang and co-authors 2021 \[#link(<ref-L10>)[L10]\]],
  [experimental comparison of methods], [REV, fast amplitude only and complex methods on one 4 by 8 array: REV and complex comparable, fast amplitude only less accurate], [Pan and co-authors 2023 \[#link(<ref-A22>)[A22]\]],
  [learned power only calibration], [networks trained on simulated data reduce power readings on a 64 element Ka band array; transfer learning reduces training data], [Xie and co-authors 2024 \[#link(<ref-A21>)[A21]\]; Sarayloo and co-authors 2020 \[#link(<ref-A16>)[A16]\]; Zhou and co-authors 2023 \[#link(<ref-L11>)[L11]\]],
  [amplitude only self calibration with learned phase retrieval], [on board peak detectors and a network for phase retrieval on a 2 by 4 array at 2.5 GHz, 5.3 degrees average rms phase error], [Wu, Syed, Ayling and Hajimiri, IMS 2025 \[#link(<ref-L13>)[L13]\]],
  [phase retrieval theory], [$4 N - 4$ generic measurements suffice; necessity only in some dimensions; 11 suffice at $N = 4$], [\[#link(<ref-A12>)[A12]\], \[#link(<ref-L1>)[L1]\], \[#link(<ref-L3>)[L3]\], \[#link(<ref-L4>)[L4]\], \[#link(<ref-L5>)[L5]\]; stable algorithms \[#link(<ref-L2>)[L2]\], \[#link(<ref-L39>)[L39]\]],
  [online reciprocity calibration in massive MIMO], [over the air and coupling based calibration at scale; calibration training spread over time], [\[#link(<ref-L14>)[L14]\], \[#link(<ref-L15>)[L15]\], \[#link(<ref-L16>)[L16]\], \[#link(<ref-L17>)[L17]\]],
  [drift and calibration stability], [multi day stability of a phased array feed with a calibration update scheme], [\[#link(<ref-L19>)[L19]\], authors not confirmed],
  [Gaussian process calibration from sparse data], [calibration posed as Bayesian function approximation from near field data], [Tambovskiy, Fodor and Tullberg 2023 \[#link(<ref-A19>)[A19]\]],
  [temporal priors with a physical forward model], [Kalman filtering of calibration terms; Gaussian process priors on antenna gain time series with learned temporal correlation; both in radio interferometry], [Tasse 2014 \[#link(<ref-L21>)[L21]\]; Arras and co-authors 2019 \[#link(<ref-L22>)[L22]\]; Kim and co-authors 2024 \[#link(<ref-L23>)[L23]\]; for antenna arrays, a 2025 preprint infers element errors jointly with channel parameters \[#link(<ref-L24>)[L24]\]],
  [Bayesian experimental design], [expected information gain as a design criterion; near optimal greedy selection for Gaussian processes], [\[#link(<ref-L28>)[L28]\], \[#link(<ref-L26>)[L26]\], \[#link(<ref-L27>)[L27]\], \[#link(<ref-L29>)[L29]\]],
  [ISAC and Wi-Fi sensing], [surveys of integrated sensing and communication; Wi-Fi passive radar; channel state information sensing; phased array processing on commodity Wi-Fi access points], [\[#link(<ref-L32>)[L32]\], \[#link(<ref-L33>)[L33]\], \[#link(<ref-L34>)[L34]\], \[#link(<ref-L35>)[L35]\]],
  [array calibration for ISAC], [hardware impairments learned end to end in ISAC; calibration of beam patterns for ISAC], [\[#link(<ref-L36>)[L36]\]; preprints \[#link(<ref-L37>)[L37]\], \[#link(<ref-L38>)[L38]\]],
)

=== XV.3 Where AetherArray is similar

- It uses REV, coupling based calibration and orthogonal coding as baselines, exactly as the
  literature defines them.
- Its sparse recalibration is a Bayesian estimation with an explicit forward model, as in the
  radio interferometry work \[#link(<ref-L21>)[L21], #link(<ref-L22>)[L22], #link(<ref-L23>)[L23]\].
- Its preference for Gaussian processes or linear Gaussian models on small data follows the
  precedent of \[#link(<ref-A19>)[A19]\].
- Its use of on board power detection resembles the amplitude only self calibration of \[#link(<ref-L13>)[L13]\],
  which is at almost the same frequency.

=== XV.4 Where it differs

- *The prior is temporal and learned from the array's own history*, not a population prior
  learned from simulated arrays \[#link(<ref-A21>)[A21], #link(<ref-L11>)[L11]\] and not a spatial or weight space model \[#link(<ref-A19>)[A19]\].
- *The forward model is a phased array's*, with a commanded discrete state per measurement, not
  a radio interferometer's sky model.
- *The figure of merit is the number of new physical measurements at equal accuracy*, against
  persistence, a non learned temporal baseline and a from scratch baseline at its own minimum.
- *Labels come from hardware*, by an expensive classical calibration run after the cheap one,
  rather than from a simulator.
- *The scale is deliberately small*, with exact enumeration of beam states, so that beam
  synthesis error is removed from the comparison.

=== XV.5 Claims that are not novel

Phased array calibration; power only calibration; REV; coupling based self calibration; orthogonal
coding; learned power only calibration; Gaussian process calibration; Kalman filtering of
calibration parameters; Bayesian experimental design; Wi-Fi sensing; ISAC as a concept; a
reconfigurable receiving array. Each has clear precedent above. The patent US 10,211,527 is close
prior art for recalibrating with a subset of excitation patterns on the grounds that drift since
the last calibration is limited, though deterministically and without a learned prior \[#link(<ref-L20>)[L20]\], index
level.

=== XV.6 What gap may remain

No paper found in this search combines a learned temporal prior over phased array calibration drift
with an explicit physical likelihood to reduce the number of recalibration measurements, measured
against non learned temporal baselines on real hardware. Nor was active, information based probe
selection for phased array recalibration found. The candidate contribution is therefore the
combination, and its experimental test on real hardware.

#caveat[
*Potential research differentiation; novelty not yet established.*
]

The search was index level, did not include a full IEEE Xplore keyword search, under-covered
paywalled conference proceedings (AP-S/URSI, EuCAP, IMS, radar conferences) and non English
journals, and did no citation chasing. Before any novelty is claimed, a systematic review is needed:
Xplore and Scholar searches on calibration drift with Kalman filtering, recalibration with a prior,
and Bayesian phased array calibration, and forward citation searches from \[#link(<ref-A19>)[A19]\], \[#link(<ref-L7>)[L7]\] and \[#link(<ref-L13>)[L13]\].
