"""Propagation constant of a uniform line from two lengths, and what follows from it.

The two line method. Two lines that differ only in length, measured or
simulated between the same reference planes, have cascade matrices
``T_i = X L(l_i) Y`` with the same error boxes ``X`` and ``Y``: the launches,
or a port whose reference impedance is not the line's own. Then

    M = T_long T_short^-1 = X diag(exp(-g dl), exp(+g dl)) X^-1

so the eigenvalues of ``M`` are ``exp(-g dl)`` and ``exp(+g dl)`` whatever the
error boxes are, and the propagation constant ``g`` follows from either one.
The same function serves a solver's two lines, SIM-001, and a board's coupons
C1 and C2, SCH-012, which is why it lives in the shared data layer.

Two numerical limits, both enforced rather than assumed. The branch is fixed at
the first frequency point, where the phase difference must be below half a turn,
and then followed by continuity. And wherever the phase difference comes close
to a multiple of half a turn, the two eigenvalues merge and which one is which
cannot be told: the function refuses there, when the sine of the phase
difference falls below ``DEGENERACY_SIN``. SIM-001 sizes the difference at a
quarter guided wavelength at f0, about 37 to 111 degrees over 1 to 3 GHz.
"""
from __future__ import annotations

import numpy as np
from scipy.constants import c as C0

from .io import RfTrace

NP_TO_DB = 20.0 / np.log(10.0)

#: A numerical conditioning limit, not an acceptance criterion: within about
#: 5.7 degrees of a multiple of 180 degrees the two eigenvalues are too close to
#: tell apart reliably.
DEGENERACY_SIN = 0.1


class LineExtractionError(ValueError):
    """The two traces cannot give a propagation constant."""


def s_to_t(s: np.ndarray) -> np.ndarray:
    """Cascade matrices of two port S matrices, shape (points, 2, 2).

    Convention: ``[b1, a1] = T [a2, b2]``, so cascades multiply left to right.
    """
    s11, s12, s21, s22 = s[:, 0, 0], s[:, 0, 1], s[:, 1, 0], s[:, 1, 1]
    if np.any(np.abs(s21) < 1e-12):
        raise LineExtractionError("S21 vanishes, the line does not transmit")
    t = np.empty_like(s)
    t[:, 0, 0] = -(s11 * s22 - s12 * s21) / s21
    t[:, 0, 1] = s11 / s21
    t[:, 1, 0] = -s22 / s21
    t[:, 1, 1] = 1.0 / s21
    return t


def two_line_gamma(short: RfTrace, long: RfTrace, delta_l_m: float) -> tuple[np.ndarray, np.ndarray]:
    """Frequency and complex propagation constant, in 1/m, from two line lengths.

    Both traces must share their frequency grid exactly: interpolating S
    parameters before an eigenvalue extraction would hide the very errors this
    method is meant to expose.
    """
    if delta_l_m <= 0:
        raise LineExtractionError("the long line must be longer")
    if short.n_ports != 2 or long.n_ports != 2:
        raise LineExtractionError("two port traces only")
    f = short.f
    if f.shape != long.f.shape or not np.allclose(f, long.f, rtol=0, atol=1e-3):
        raise LineExtractionError("the two traces do not share a frequency grid")
    t_s = s_to_t(np.asarray(short.network.s))
    t_l = s_to_t(np.asarray(long.network.s))
    m = t_l @ np.linalg.inv(t_s)
    eig = np.linalg.eigvals(m)
    # exp(-g dl) lags in phase. At the first point, where the phase difference
    # is below half a turn, it is the eigenvalue below the real axis; after
    # that, the one closest to the previous choice.
    lam = np.empty(len(f), dtype=complex)
    first = eig[0]
    lam[0] = first[0] if first[0].imag < first[1].imag else first[1]
    for k in range(1, len(f)):
        a, b = eig[k]
        lam[k] = a if abs(a - lam[k - 1]) <= abs(b - lam[k - 1]) else b
    phase = np.unwrap(-np.angle(lam))
    if phase[0] <= 0 or phase[0] >= np.pi:
        raise LineExtractionError("the phase difference at the first point is not within half a turn")
    if np.any(np.abs(np.diff(phase)) > np.pi / 2):
        raise LineExtractionError("phase step above a quarter turn between points; grid too coarse")
    if np.any(np.abs(np.sin(phase)) < DEGENERACY_SIN):
        raise LineExtractionError("the phase difference passes a multiple of half a turn, where "
                                  "the two eigenvalues merge; use a shorter length difference")
    alpha = -np.log(np.abs(lam)) / delta_l_m
    beta = phase / delta_l_m
    return f, alpha + 1j * beta


def eeff_from_gamma(f_hz: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    """Complex effective permittivity of a quasi-TEM line, ``-(g c / (2 pi f))^2``.

    Exact for a TEM line; for microstrip it is the usual definition of the
    effective permittivity from the propagation constant. The real part is what
    a phase length uses.
    """
    return -(gamma * C0 / (2 * np.pi * np.asarray(f_hz))) ** 2


def attenuation_db_per_m(gamma: np.ndarray) -> np.ndarray:
    """Attenuation of a line in dB per metre, from its propagation constant."""
    return np.real(gamma) * NP_TO_DB
