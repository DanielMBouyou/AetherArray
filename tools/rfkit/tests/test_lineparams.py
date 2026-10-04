"""Tests of the two line propagation constant extraction.

Every network here is analytic: a line of known propagation constant and a
characteristic impedance other than the 50 ohm reference, inside asymmetric
launch error boxes. The extraction has to return the propagation constant
whatever the launches are, which is the property SIM-001 and the coupons of
SCH-012 rely on.
"""
from __future__ import annotations

import numpy as np
import pytest
import skrf
from scipy.constants import c as C0
from skrf.media import DefinedGammaZ0

import rfkit
from rfkit.lineparams import (
    LineExtractionError,
    attenuation_db_per_m,
    eeff_from_gamma,
    s_to_t,
    two_line_gamma,
)

F = np.linspace(1e9, 3e9, 401)
EEFF = 3.2 - 0.05j            # complex: a lossy dielectric
ALPHA_C = 0.5                 # Np/m of conductor loss, added on top


def gamma_true(f):
    return 1j * 2 * np.pi * f / C0 * np.sqrt(EEFF) + ALPHA_C


def pair(z0_line=46.0, l_short=10e-3, l_long=27.2e-3):
    freq = skrf.Frequency.from_f(F, unit="hz")
    line = DefinedGammaZ0(frequency=freq, z0_port=50.0, z0=z0_line, gamma=gamma_true(F))
    ref = DefinedGammaZ0(frequency=freq, z0=50.0, gamma=1j * 2 * np.pi * F / C0)
    launch_a = ref.inductor(0.3e-9) ** ref.shunt_capacitor(0.15e-12)
    launch_b = ref.shunt_capacitor(0.2e-12) ** ref.inductor(0.25e-9)
    def trace(length):
        net = launch_a ** line.line(length, unit="m") ** launch_b
        return rfkit.synthetic_trace(F, net.s)
    return trace(l_short), trace(l_long), l_long - l_short


def test_cascade_matrix_of_a_thru_is_identity():
    s = np.zeros((3, 2, 2), dtype=complex)
    s[:, 0, 1] = s[:, 1, 0] = 1.0
    assert np.allclose(s_to_t(s), np.eye(2))


def test_two_line_recovers_the_propagation_constant_through_launches():
    short, long, dl = pair()
    f, g = two_line_gamma(short, long, dl)
    assert np.allclose(g, gamma_true(f), rtol=1e-9)
    assert np.allclose(eeff_from_gamma(f, g).real,
                       eeff_from_gamma(f, gamma_true(f)).real, rtol=1e-9)
    assert np.all(attenuation_db_per_m(g) > 0)


def test_independent_of_line_impedance():
    for z in (35.0, 50.0, 70.7):
        short, long, dl = pair(z0_line=z)
        f, g = two_line_gamma(short, long, dl)
        assert np.allclose(g, gamma_true(f), rtol=1e-9), z


def test_lossless_eeff_is_beta_squared():
    f = np.array([2.44e9])
    beta = 2 * np.pi * f / C0 * np.sqrt(3.2)
    assert eeff_from_gamma(f, 1j * beta).real == pytest.approx(3.2)


def test_refuses_mismatched_grids_and_bad_lengths():
    short, long, dl = pair()
    other = rfkit.synthetic_trace(F[:-1], np.asarray(long.network.s)[:-1])
    with pytest.raises(LineExtractionError):
        two_line_gamma(short, other, dl)
    with pytest.raises(LineExtractionError):
        two_line_gamma(short, long, 0.0)


def test_refuses_a_length_difference_beyond_half_a_wavelength():
    short, long, _ = pair(l_long=10e-3 + 60e-3)   # 60 mm is past half a wavelength at 3 GHz
    with pytest.raises(LineExtractionError):
        two_line_gamma(short, long, 60e-3)
