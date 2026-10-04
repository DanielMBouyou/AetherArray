"""Figures for docs/aetherarray-master-reference.md.

Every figure here is an ANALYTICAL ILLUSTRATION: the ideal array factor of a
uniform linear array of isotropic elements, with no coupling, no element
pattern and no measured or simulated data of any kind. They exist so that the
reference document can show textbook behaviour with the parameters decisions
0003 and 0004 fixed (four elements, half wavelength spacing, three phase bits,
2.44 GHz, band 57a). None of them is a simulation of Rev A and none of them is
a result. The one random figure uses a fixed seed and says so in its caption.

Deliberately absent: any angle pair study for the communication mode. That is
the N = 4 feasibility gate described in the document, and its acceptance rule
has to be written before it is run.

Run from the repository root:

    python tools/docs/master_reference_figures.py

It rewrites docs/figures/*.svg deterministically.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
from rfkit import budget as b  # noqa: E402

OUT = REPO / "docs" / "figures"
N = b.N_DEFAULT
D_OVER_LAMBDA = b.D_OVER_LAMBDA_DEFAULT
STEP_DEG = b.quantisation_step_deg(b.PHASE_BITS_DEFAULT)
SEED = 20261004
LABEL = "analytical illustration: ideal isotropic elements, array factor only, no coupling"

plt.rcParams.update({
    "svg.hashsalt": "aetherarray-master-reference",
    "font.size": 9,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 100,
})


def _db(af: np.ndarray, floor_db: float = -120.0) -> np.ndarray:
    """Power relative to the ideal peak N^2, clipped at the plot floor.

    The clip is done in the data, not only by the axes, so that renderers that
    ignore SVG clip paths draw the same picture.
    """
    p = np.abs(af) ** 2
    return np.maximum(10.0 * np.log10(np.maximum(p / (N ** 2), 1e-12)), floor_db)


def _steer(theta0_deg: float) -> np.ndarray:
    """Continuous steering phases, phi_n = -n k d sin(theta0), in degrees."""
    kd_deg = 360.0 * D_OVER_LAMBDA
    return -np.arange(N) * kd_deg * math.sin(math.radians(theta0_deg))


def _quantise(phases_deg: np.ndarray) -> np.ndarray:
    return np.round(np.asarray(phases_deg) / STEP_DEG) * STEP_DEG


def _save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)


def fig_steering() -> dict:
    """Broadside, 30 degrees (exact on the 45 degree grid) and 15 degrees (rounded)."""
    theta = np.linspace(-90.0, 90.0, 3601)
    amps = np.ones(N)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    cases = [
        ("broadside, all phases 0", np.zeros(N), "-"),
        ("30 deg: progressive -90 deg, exact on the 3-bit grid", _quantise(_steer(30.0)), "-"),
        ("15 deg requested, continuous phases", _steer(15.0), "--"),
        ("15 deg requested, phases rounded to 45 deg steps", _quantise(_steer(15.0)), ":"),
    ]
    info = {}
    for label, ph, ls in cases:
        ax.plot(theta, _db(b.array_factor(theta, amps, ph, D_OVER_LAMBDA), -40.0), ls, lw=1.3, label=label)
    info["pointing_15_rounded_deg"] = b.peak_direction_deg(amps, _quantise(_steer(15.0)), D_OVER_LAMBDA)
    info["phases_15_rounded_deg"] = _quantise(_steer(15.0)).tolist()
    ax.set_xlim(-90, 90)
    ax.set_ylim(-40, 2)
    ax.set_xlabel("angle from broadside, theta (deg)")
    ax.set_ylabel("|AF|^2 relative to N^2 (dB)")
    ax.set_title("N = 4, d = lambda/2: steering with 3-bit phase states", fontsize=9)
    ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2)
    fig.text(0.01, 0.01, LABEL, fontsize=6, style="italic")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    _save(fig, "steering-n4.svg")
    return info


def fig_null_filling() -> dict:
    """A broadside null at 30 degrees, and how independent phase errors fill it."""
    rng = np.random.default_rng(SEED)
    theta = np.linspace(-90.0, 90.0, 3601)
    amps = np.ones(N)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    sigma_demo = 10.0
    for _ in range(25):
        err = rng.normal(0.0, sigma_demo, N)
        ax1.plot(theta, _db(b.array_factor(theta, amps, err, D_OVER_LAMBDA), -50.0), color="0.6", lw=0.5)
    ax1.plot(theta, _db(b.array_factor(theta, amps, np.zeros(N), D_OVER_LAMBDA), -50.0), "k", lw=1.5,
             label="no error")
    floor = 10 * math.log10(math.radians(sigma_demo) ** 2 / N)
    ax1.axhline(floor, color="C3", ls="--", lw=1.0, label=f"sigma^2/N floor, {floor:.1f} dB")
    ax1.axvline(30.0, color="C0", ls=":", lw=0.8)
    ax1.set_xlim(-90, 90)
    ax1.set_ylim(-50, 2)
    ax1.set_xlabel("theta (deg)")
    ax1.set_ylabel("|AF|^2 / N^2 (dB)")
    ax1.set_title(f"25 draws, independent phase error {sigma_demo:g} deg rms", fontsize=8)
    ax1.legend(fontsize=7, loc="lower left")

    sigmas = np.array([1, 2, 3, 5, 7, 10, 13, 15, 20, 25, 30], dtype=float)
    mc = []
    for s in sigmas:
        err = rng.normal(0.0, s, (20000, N))
        w = np.exp(1j * np.radians(err))
        v = np.exp(1j * np.arange(N) * 2 * math.pi * D_OVER_LAMBDA * math.sin(math.radians(30.0)))
        mc.append(10 * math.log10(np.mean(np.abs(w @ v) ** 2) / N ** 2))
    s_fine = np.linspace(0.5, 30, 200)
    ax2.plot(s_fine, 10 * np.log10(np.radians(s_fine) ** 2 / N), "C3--", lw=1.0,
             label="small error formula, sigma^2/N")
    ax2.plot(sigmas, mc, "ko", ms=3.5, label="Monte Carlo mean, 20000 draws")
    q = b.quantisation_rms_deg(b.PHASE_BITS_DEFAULT)
    ax2.axvline(q, color="C2", ls=":", lw=1.0, label=f"3-bit rounding rms, {q:.2f} deg")
    ax2.set_xlabel("independent phase error, rms (deg)")
    ax2.set_ylabel("mean power at the 30 deg null, rel. peak (dB)")
    ax2.set_title("Null depth is limited by residual error", fontsize=8)
    ax2.legend(fontsize=7, loc="lower right")
    fig.text(0.01, 0.01, LABEL + f"; random draws from seed {SEED}", fontsize=6, style="italic")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    _save(fig, "null-filling-n4.svg")
    return {"floor_10deg_db": floor, "mc": dict(zip(sigmas.tolist(), mc))}


def fig_dispersion() -> dict:
    """Intrinsic dispersion of a fixed switched line: phase error against frequency."""
    f = np.linspace(b.BAND_START_HZ, b.BAND_STOP_HZ, 200)
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    out = {}
    for bit in (45, 90, 180, 315):
        err = bit * (f / b.F0_HZ - 1.0)
        ax.plot(f / 1e9, err, lw=1.2, label=f"{bit} deg state")
        out[bit] = (float(err[0]), float(err[-1]))
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("frequency (GHz), band 57a")
    ax.set_ylabel("phase error vs nominal (deg)")
    ax.set_title("A fixed line length is a true delay: its phase scales with f", fontsize=9)
    ax.legend(fontsize=7)
    fig.text(0.01, 0.01, "analytical illustration: ideal non-dispersive line, phase = nominal x f / f0",
             fontsize=6, style="italic")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    _save(fig, "switched-line-dispersion.svg")
    return out


def main() -> None:
    info = {"steering": fig_steering(), "null": fig_null_filling(), "dispersion": fig_dispersion()}
    for k, v in info.items():
        print(k, v)


if __name__ == "__main__":
    main()
