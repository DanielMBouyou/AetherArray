# Hardware design files

- Status: in progress, Rev A schematic captured
- Last reviewed: 2026-10-03

The electronic design files live here. The reasoning behind them is in `docs/`, and
the choices that constrain them are in `decisions/`.

| Directory | Contents |
| --- | --- |
| `rev-a/` | The first beamformer board: schematic, project symbol library, generator, bill of materials and electrical rule check output |
| `rev-a/stackup/` | The canonical stack-up of both Rev A boards, decision 0009, and the candidates it was compared with |

## Why this is separate from `docs/hardware/`

`docs/hardware/` answers "what hardware do we need, have, or lack?", in normal
sentences. This folder holds files a tool opens. Mix the two and the documentation gets
hard to read and the design files get hard to find.

## What is not here

- No board layout. Decision 0003 only authorises the schematic.
- No antenna board. Rev A is two boards, and only the beamformer board is drawn so far.
  The antenna board is a separate design. The frequency it needs is settled, 2.44 GHz
  by decision 0004, and the stack-up is chosen by decision 0009, so what
  its geometry waits on now is the patch design itself.
- No footprints assigned. Footprints get chosen along with the layout.
