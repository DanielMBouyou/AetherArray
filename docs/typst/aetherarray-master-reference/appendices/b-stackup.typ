#import "../template.typ": *

== Appendix B. Stack-up

The canonical definition is `hardware/rev-a/stackup/reva-stackup.json`, identifier
`reva-stackup-r1`, fingerprint `reva-stackup-r1:6363d8ab0f2b` at the baseline. Its generated
tables appear in this document in section 21 (construction and tolerances), section 22 (patch
sanity check), section 23 (comparison with the candidates), section 59 (sensitivity, pointing and
loss) and Appendix A (seeds and SIM-001 inputs). The alternatives compared are in
`hardware/rev-a/stackup/candidates.json`. How each tool reads the file is in
`hardware/rev-a/stackup/README.md` section 6. To regenerate every table:
`cd tools && python -m rfkit.cli stackup --write-docs`.
