"""Reproducible command line entry points.

    cd tools
    python -m rfkit.cli compare --hfss a.s2p --ads b.s2p --vna c.s2p --f0 2.44e9
    python -m rfkit.cli state --channel 0=ch0.s2p --channel 1=ch1.s2p --f0 2.44e9
    python -m rfkit.cli example --out /tmp/rfkit-example

Every run writes machine readable JSON alongside the human readable report, and
the JSON carries the provenance of every input, so a figure in a document can be
traced back to the files it came from.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .compare import compare_all
from .io import load_touchstone
from .state import state_from_channel_traces


def _write(text: str, path: Path | None, label: str) -> None:
    if path is None:
        return
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {label}: {path}", file=sys.stderr)


def cmd_compare(args: argparse.Namespace) -> int:
    traces = []
    for source in ("hfss", "ads", "vna"):
        for path in getattr(args, source) or []:
            traces.append(load_touchstone(path, source=source))
    if len(traces) < 2:
        print("need at least two inputs to compare", file=sys.stderr)
        return 2

    report = compare_all(traces, f0_hz=args.f0, n_points=args.points)
    text = report.to_text()
    print(text)
    _write(text, args.report, "report")
    _write(json.dumps(report.as_dict(), indent=2) + "\n", args.json, "json")
    return 0


def cmd_state(args: argparse.Namespace) -> int:
    traces = {}
    for item in args.channel:
        if "=" not in item:
            print(f"--channel expects INDEX=PATH, got {item!r}", file=sys.stderr)
            return 2
        idx, path = item.split("=", 1)
        traces[int(idx)] = load_touchstone(path, source=args.source)

    state = state_from_channel_traces(traces, f0_hz=args.f0, reference=args.reference)
    text = state.summary()
    print(text)
    _write(text + "\n", args.report, "report")
    _write(json.dumps(state.as_dict(), indent=2) + "\n", args.json, "json")
    return 0


def cmd_example(args: argparse.Namespace) -> int:
    from .example import run_example

    run_example(Path(args.out))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rfkit", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("compare", help="compare traces from different tools")
    c.add_argument("--hfss", action="append", metavar="FILE")
    c.add_argument("--ads", action="append", metavar="FILE")
    c.add_argument("--vna", action="append", metavar="FILE")
    c.add_argument("--f0", type=float, default=None, help="frequency in Hz")
    c.add_argument("--points", type=int, default=None, help="force a uniform grid size")
    c.add_argument("--json", type=Path, default=None)
    c.add_argument("--report", type=Path, default=None)
    c.set_defaults(func=cmd_compare)

    s = sub.add_parser("state", help="build the array state from per channel traces")
    s.add_argument("--channel", action="append", required=True, metavar="INDEX=FILE")
    s.add_argument("--f0", type=float, required=True, help="frequency in Hz")
    s.add_argument("--reference", type=int, default=0)
    s.add_argument("--source", default="vna", help="hfss, ads, vna or synthetic")
    s.add_argument("--json", type=Path, default=None)
    s.add_argument("--report", type=Path, default=None)
    s.set_defaults(func=cmd_state)

    e = sub.add_parser("example", help="run the synthetic end to end example")
    e.add_argument("--out", type=Path, required=True)
    e.set_defaults(func=cmd_example)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
