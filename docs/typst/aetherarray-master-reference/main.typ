// AetherArray master technical reference, Typst edition. Entry point.
// Compile: typst compile main.typ AetherArray_Master_Reference_v0.2.pdf

#import "template.typ": *
#import "metadata.typ": meta

#show: aa-report.with(meta)

#title-page(meta)
#front-outline()
#body-start()

// Front matter of the canonical document: status, how to use it, contents overview.
#include "chapters/front-matter.typ"

// Parts 0 to XXI.
#include "chapters/00-overview.typ"
#include "chapters/01-course-theory.typ"
#include "chapters/02-engineering-problem.typ"
#include "chapters/03-hardware.typ"
#include "chapters/04-stackup-rf-design.typ"
#include "chapters/05-simulation-analysis-stack.typ"
#include "chapters/06-simulation-roadmap.typ"
#include "chapters/07-measurement.typ"
#include "chapters/08-machine-learning.typ"
#include "chapters/09-aps-isac-demonstrator.typ"
#include "chapters/10-project-status.typ"
#include "chapters/11-validation.typ"
#include "chapters/12-software-tools.typ"
#include "chapters/13-data-flow.typ"
#include "chapters/14-why-useful.typ"
#include "chapters/15-literature-evidence.typ"
#include "chapters/16-ieee-strategy.typ"
#include "chapters/17-risk-register.typ"
#include "chapters/18-roadmap.typ"
#include "chapters/19-glossary.typ"
#include "chapters/20-is-and-is-not.typ"
#include "chapters/21-synthesis.typ"

// Appendices A to L.
#include "appendices/00-appendices.typ"
#include "appendices/a-parameters.typ"
#include "appendices/b-stackup.typ"
#include "appendices/c-acceptance-budget.typ"
#include "appendices/d-open-hardware-items.typ"
#include "appendices/e-simulations.typ"
#include "appendices/f-experiments.typ"
#include "appendices/g-decisions.typ"
#include "appendices/h-tools.typ"
#include "appendices/i-aps-checklist.typ"
#include "appendices/j-unresolved-questions.typ"
#include "appendices/k-notation.typ"
#include "appendices/l-where-to-find.typ"

// References (rendered from bibliography.yml) and the self review.
#include "backmatter/references.typ"
#include "backmatter/review.typ"
