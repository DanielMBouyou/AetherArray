# Decision log

This directory records the structural technical decisions of the project.

## Why

In six months the question will not be "what did we choose". It will be "why did
we choose that, and does the reason still hold". A choice with no recorded
justification ends up being repeated out of habit, long after the context has
changed.

## What belongs here

A decision goes in if at least one of these is true:

- it is expensive to undo (hardware bought, RTL architecture committed, data
  format frozen),
- it rules out a family of solutions,
- it rests on an assumption that could turn out to be wrong,
- someone competent could reasonably make the opposite call.

A choice that can be reversed in an hour does not need a record.

## Format

One file per decision: `NNNN-short-title.md`, starting at `0001`. Numbers never go
backwards. A cancelled decision is not deleted: its status becomes
`superseded by NNNN`, and the new record explains what changed.

Statuses: `proposed`, `accepted`, `rejected`, `superseded`, `on hold`.

The template is in `0000-template.md`.

## One rule that matters during this phase

The project is in its study phase. Most of the big questions should not be settled
yet. A decision record written too early, with no measurement behind it, is a way
of freezing an intuition and calling it a choice. If a decision has to be made
without evidence (schedule or budget pressure), the evidence section must say so
rather than invent a technical justification.
