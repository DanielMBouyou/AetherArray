# Hardware design files

- Status: in progress, Rev A schematic captured
- Last reviewed: 2026-09-18

Electronic design files live here. The reasoning that produced them lives in
`docs/`, and the choices that constrain them live in `decisions/`.

| Directory | Contents |
| --- | --- |
| `rev-a/` | The first beamformer board: schematic, project symbol library, generator, bill of materials and electrical rule check output |

## Why this is separate from `docs/hardware/`

`docs/hardware/` answers "what hardware is needed, available or missing", in prose.
This directory holds machine readable design files that a tool opens. Mixing the two
would make the documentation tree unreadable and the design files hard to find.

## What is not here

- No board layout. Decision 0003 authorises schematic capture only.
- No antenna board. Rev A is two boards, and only the beamformer board is captured.
  The antenna board is a separate design whose geometry waits on the working
  frequency.
- No footprints assigned. Footprint choice belongs with layout.
