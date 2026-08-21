# NNNN. Short decision title

- Status: proposed | accepted | rejected | superseded by NNNN | on hold
- Date: YYYY-MM-DD
- Scope: which subsystem this affects

## Question

State the question in a form that admits more than one defensible answer. If there
is only one possible answer, this is not a decision, it is a constraint: document
it somewhere else.

## Context

What is true at the time of the decision: hardware constraints, time available,
skills, dependencies on choices already made.

## Options considered

### Option A
What it does, what it buys, what it costs.

### Option B
Same.

### Option C, or "decide nothing yet"
"Wait until we have measured" is a legitimate option. List it when it is
reasonable.

## Comparison

| Criterion | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Expected performance | to measure | to measure | to measure |
| Implementation effort | | | |
| Hardware cost | | | |
| Reproducibility by a third party | | | |
| Main risk | | | |
| Reversibility | | | |

## Evidence

List it precisely, and say what kind of evidence each item is:

- measurement made here: link to `results/EXP-NNN`
- simulation result: name the tool and its version
- external source: full reference
- unverified technical opinion: say so

If this section is empty, write it down in plain words: "no experimental
evidence, decision based on X".

## Decision

What is decided, in one or two sentences, with no ambiguity.

## Consequences

- What this makes possible.
- What this makes harder or impossible.
- Work it creates (code to write, hardware to buy, skills to acquire).

## Known limitations

What the decision does not solve, and the cases where it is probably wrong.

## Conditions for reopening

Write observable triggers, not a vague date. For example: "if measured latency
exceeds X", "if DSP utilisation exceeds Y", "if component Z becomes unavailable".
