"""Reproducible command line entry points.

    cd tools
    python -m rfkit.cli compare --hfss a.s2p --ads b.s2p --vna c.s2p --f0 2.44e9
    python -m rfkit.cli compare-states --a-source hfss --a 0=s0.s2p --a 1=s1.s2p \
        --b-source ads --b 0=t0.s2p --b 1=t1.s2p
    python -m rfkit.cli state --channel 0=ch0.s2p --channel 1=ch1.s2p --f0 2.44e9
    python -m rfkit.cli budget --json budget.json --report budget.txt
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

from .compare import compare_all, compare_states
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


def _state_map(items, source: str) -> dict:
    out = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"expected STATE=PATH, got {item!r}")
        idx, path = item.split("=", 1)
        out[int(idx)] = load_touchstone(path, source=source)
    return out


def cmd_compare_states(args: argparse.Namespace) -> int:
    a = _state_map(args.a, args.a_source)
    b = _state_map(args.b, args.b_source)
    result = compare_states(a, b, reference_state=args.reference_state,
                            f0_hz=args.f0, n_points=args.points)
    text = result.to_text()
    print(text)
    _write(text, args.report, "report")
    _write(json.dumps(result.as_dict(), indent=2) + "\n", args.json, "json")
    return 0


def cmd_g4(args: argparse.Namespace) -> int:
    from . import coupling as c

    data = c.coupling_from_trace(load_touchstone(args.antenna, source=args.source))
    prev = None
    if args.previous_pass:
        prev = c.coupling_from_trace(load_touchstone(args.previous_pass, source=args.source))
    agreed = {"yes": True, "no": False, None: None}[args.stage1_routes_agreed]
    report = c.run_g4(
        data, stage=args.stage, previous_pass=prev, u_abs=args.uncertainty,
        beamformer=c.load_beamformer_npz(args.beamformer) if args.beamformer else None,
        patterns=c.load_patterns_npz(args.patterns) if args.patterns else None,
        repeatability_floor=args.repeatability_floor, stage1_routes_agreed=agreed,
    )
    text = report.to_text()
    print(text)
    _write(text, args.report, "report")
    _write(json.dumps(report.as_dict(), indent=2, default=float) + "\n", args.json, "json")
    return 0


def cmd_g4_chart(args: argparse.Namespace) -> int:
    from . import coupling as c

    rows = c.synthetic_chart()
    lines = ["G4 against nearest neighbour coupling, SYNTHETIC uniform matrices",
             "  dB   phase  broadside p/g   best p/g   outcome   screen"]
    for r in rows:
        lines.append(f"  {r['coupling_db']:5.0f} {r['phase_deg']:5.0f}   "
                     f"{r['broadside_pointing']:5.2f}/{r['broadside_gain']:5.2f}   "
                     f"{r['best_pointing']:5.2f}/{r['best_gain']:5.2f}   {r['outcome']:<12} "
                     f"{'pass' if r['screen_passes'] else 'no'}")
    text = "\n".join(lines) + "\n"
    print(text)
    _write(text, args.report, "report")
    _write(json.dumps(rows, indent=2) + "\n", args.json, "json")
    return 0


def cmd_budget(args: argparse.Namespace) -> int:
    from . import budget

    text = budget.study(trials=args.trials)
    print(text)
    _write(text, args.report, "report")
    _write(json.dumps(budget.summary(), indent=2) + "\n", args.json, "json")
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

    cs = sub.add_parser(
        "compare-states",
        help="compare two tools state by state, on the state dependent difference",
    )
    cs.add_argument("--a-source", required=True, help="hfss, ads or vna")
    cs.add_argument("--a", action="append", required=True, metavar="STATE=FILE")
    cs.add_argument("--b-source", required=True, help="hfss, ads or vna")
    cs.add_argument("--b", action="append", required=True, metavar="STATE=FILE")
    cs.add_argument("--reference-state", type=int, default=0)
    cs.add_argument("--f0", type=float, default=2.44e9, help="frequency in Hz")
    cs.add_argument("--points", type=int, default=None, help="force a uniform grid size")
    cs.add_argument("--json", type=Path, default=None)
    cs.add_argument("--report", type=Path, default=None)
    cs.set_defaults(func=cmd_compare_states)

    g4 = sub.add_parser("g4", help="gate G4: is the diagonal state adequate under coupling")
    g4.add_argument("--antenna", required=True, metavar="FILE.s4p",
                    help="the antenna board at the element connectors")
    g4.add_argument("--source", required=True, help="hfss, vna or synthetic")
    g4.add_argument("--stage", default=None, choices=("simulation", "measurement"),
                    help="only for synthetic data; otherwise inferred from the source")
    g4.add_argument("--previous-pass", default=None, metavar="FILE.s4p",
                    help="simulation: the previous adaptive pass")
    g4.add_argument("--patterns", default=None, metavar="FILE.npz",
                    help="simulation: embedded element patterns, f_hz, theta_deg, g")
    g4.add_argument("--uncertainty", type=float, default=None,
                    help="measurement: expanded uncertainty of each S term, linear")
    g4.add_argument("--beamformer", default=None, metavar="FILE.npz",
                    help="measurement: f_hz, output_match, isolation")
    g4.add_argument("--stage1-routes-agreed", default=None, choices=("yes", "no"))
    g4.add_argument("--repeatability-floor", type=float, default=None,
                    help="relative floor from EXP-005 Phase B, once it exists")
    g4.add_argument("--json", type=Path, default=None)
    g4.add_argument("--report", type=Path, default=None)
    g4.set_defaults(func=cmd_g4)

    gc = sub.add_parser("g4-chart", help="G4 against synthetic nearest neighbour coupling")
    gc.add_argument("--json", type=Path, default=None)
    gc.add_argument("--report", type=Path, default=None)
    gc.set_defaults(func=cmd_g4_chart)

    bu = sub.add_parser("budget", help="the error budget study and threshold derivation")
    bu.add_argument("--trials", type=int, default=2000,
                    help="Monte Carlo trials per seed, the seeds are fixed")
    bu.add_argument("--json", type=Path, default=None)
    bu.add_argument("--report", type=Path, default=None)
    bu.set_defaults(func=cmd_budget)

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
