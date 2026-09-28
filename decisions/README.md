# Decision log

This folder keeps the project's big technical decisions, one file each.

## Why

Six months from now, nobody will ask "what did we choose?". They'll ask "why did we
choose that, and is the reason still true?". A choice with no written reason gets
repeated out of habit, long after the situation that justified it has changed.

## What belongs here

A decision gets a file if at least one of these is true:

- it's expensive to undo (hardware bought, RTL architecture committed, data format
  frozen),
- it rules out a whole family of solutions,
- it rests on an assumption that could turn out to be wrong,
- someone competent could reasonably have chosen the opposite.

If a choice can be reversed in an hour, it doesn't need a file.

## Format

One file per decision: `NNNN-short-title.md`, starting at `0001`. Numbers only go up.
A cancelled decision isn't deleted. Its status becomes `superseded by NNNN`, and the
new file explains what changed.

Statuses: `proposed`, `accepted`, `rejected`, `superseded`, `on hold`.

The template is `0000-template.md`.

## One rule that matters during this phase

The project is still in its study phase, so most of the big questions shouldn't be
settled yet. A decision written too early, with no measurement behind it, is just an
intuition frozen and called a choice. If a decision really has to be made without
evidence (because of time or money), its evidence section says so plainly. It doesn't
invent a technical reason after the fact.
