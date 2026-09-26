"""Tests of the G4 coupling adequacy machinery, on synthetic matrices only.

Every matrix here is built from a formula and carries the ``synthetic`` source.
**None of it is a simulation or a measurement of any array**, and nothing here
anticipates what EXP-011 will find.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

import rfkit
from rfkit import coupling as c
from rfkit import thresholds as th

REPO = Path(__file__).resolve().parents[3]
F = np.array([2.39e9, 2.50e9])
SMALL = th.G4Protocol(steering_deg=tuple(float(a) for a in range(-45, 46, 15)), guard_draws=4)


def nn(db, phase_deg=0.0, reflection=0.1, second=()):
    k = 10 ** (db / 20.0) * np.exp(1j * math.radians(phase_deg))
    return c.toeplitz_coupling(F, reflection, (k,) + tuple(second))


def patterns_from(data, step=1.0):
    """Embedded patterns synthesised from the minimum scattering model itself."""
    fp = np.array([2.40e9, 2.44e9, 2.4835e9])
    theta = np.arange(-90.0, 90.0 + 1e-9, step)
    s = data.at(fp)
    g = np.empty((fp.size, 4, theta.size), dtype=complex)
    for i, fq in enumerate(fp):
        kd = math.pi * fq / 2.44e9
        v = np.exp(1j * kd * np.outer(np.sin(np.radians(theta)), np.arange(4)))
        g[i] = (v @ (np.eye(4) - s[i])).T
    return c.EmbeddedPatterns(f_hz=fp, theta_deg=theta, g=g)


def ideal_beamformer(match=0.0):
    gam = np.full((F.size, 4, 8), match, dtype=complex)
    return c.Beamformer(f_hz=F, output_match=gam)


# --------------------------------------------------------------- the states
def test_the_judged_states_cover_every_angle_and_origin():
    th0, origin, states = c.steering_states(th.G4)
    assert len(th0) == 91 * 8
    assert set(th.G4.steering_deg) >= {0.0, 15.0, 30.0, 45.0, -45.0}
    assert states.min() >= 0 and states.max() <= 7
    assert c.calibration_states().shape == (29, 4)


# ------------------------------------------------------------ isolation
def test_no_coupling_means_no_error_at_all():
    e = c.evaluate(c.toeplitz_coupling(F, 0.1), protocol=SMALL)
    assert e.pass_broadside_calibration and e.pass_best_diagonal
    assert e.worst_broadside["pointing_fraction_of_budget"] < 1e-9
    assert e.worst_broadside["gain_fraction_of_budget"] < 1e-9


def test_a_mismatched_beamformer_without_coupling_is_not_charged_to_coupling():
    gam = np.zeros((F.size, 4, 8), dtype=complex)
    gam[:, :, :] = 0.3 * np.exp(1j * np.radians(np.arange(8) * 40.0))
    e = c.evaluate(c.toeplitz_coupling(F, 0.2), beamformer=c.Beamformer(F, gam), protocol=SMALL)
    assert e.worst_broadside["pointing_fraction_of_budget"] < 1e-9


def test_a_known_coupling_matrix_reproduces_the_array_exactly():
    d = nn(-15.0, 40.0, second=(10 ** (-25 / 20),))
    e = c.evaluate(d, model=d, protocol=SMALL)
    assert e.worst_broadside["pointing_fraction_of_budget"] < 1e-9
    assert e.worst_broadside["gain_fraction_of_budget"] < 1e-9


def test_state_independent_coupling_leaves_no_calibration_residual():
    # The residual cannot reveal coupling: a probe calibration fits it exactly.
    e = c.evaluate(nn(-15.0, 30.0), protocol=SMALL)
    assert e.calibration_residual_max < 1e-12
    assert not e.pass_broadside_calibration


def test_state_dependent_coupling_does_leave_a_residual():
    gam = np.zeros((F.size, 4, 8), dtype=complex)
    gam[:, :, :] = 0.2 * np.exp(1j * np.radians(np.arange(8) * 40.0))
    e = c.evaluate(nn(-20.0, 30.0), beamformer=c.Beamformer(F, gam), protocol=SMALL)
    assert e.calibration_residual_max > 1e-3


# ------------------------------------------------- one number is not enough
def test_the_same_coupling_magnitude_at_another_phase_gives_another_answer():
    in_phase, quadrature = nn(-25.0, 0.0, 0.0), nn(-25.0, 90.0, 0.0)
    assert in_phase.s[0, 0, 1] != quadrature.s[0, 0, 1]
    a, q = c.evaluate(in_phase, protocol=SMALL), c.evaluate(quadrature, protocol=SMALL)
    assert a.descriptors["max_offdiag_db"] == pytest.approx(q.descriptors["max_offdiag_db"])
    ratio_a = a.worst_broadside["pointing_fraction_of_budget"]
    ratio_q = q.worst_broadside["pointing_fraction_of_budget"]
    assert ratio_a > 2.0 * ratio_q


def test_the_screen_is_sufficient_for_the_unfitted_comparison():
    assert c.screen_limit(0.1) == pytest.approx(math.sin(math.radians(2.2963966)), rel=1e-6)
    e = c.evaluate(nn(-40.0, 30.0), protocol=SMALL)
    assert e.screen["passes"]
    assert e.unfitted["pointing_fraction_of_budget"] <= 1.0
    assert e.unfitted["max_phase_error_deg"] <= math.degrees(math.asin(e.screen["rho_max"])) + 1e-9


def test_the_screen_is_conservative():
    e = c.evaluate(nn(-30.0, 0.0), protocol=SMALL)
    assert not e.screen["passes"]
    assert e.pass_broadside_calibration


def test_strong_coupling_fails_even_the_best_diagonal():
    e = c.evaluate(nn(-15.0, 0.0), protocol=SMALL)
    assert not e.pass_best_diagonal


# ----------------------------------------------------------- descriptors
def test_descriptors_see_asymmetry_and_aggregate():
    s = np.array(nn(-20.0).s)
    s[:, 0, 1] *= 1.2
    d = c.descriptors(s)
    assert d["reciprocity_defect"] > 0
    assert d["max_row_aggregate"] == pytest.approx(2 * 10 ** (-20 / 20), rel=1e-9)


# ------------------------------------------------------------ the two routes
def test_embedded_patterns_built_from_the_model_agree_with_it():
    for d in (nn(-40.0, 20.0), nn(-15.0, 20.0)):
        cms = c.evaluate(d, protocol=SMALL)
        emb = c.evaluate(d, patterns=patterns_from(d), protocol=SMALL)
        assert emb.pass_broadside_calibration == cms.pass_broadside_calibration
        assert emb.pass_best_diagonal == cms.pass_best_diagonal


def test_embedded_route_has_no_error_without_coupling_on_any_grid():
    d = c.toeplitz_coupling(F, 0.1)
    for step in (1.0, 0.5):
        e = c.evaluate(d, patterns=patterns_from(d, step), protocol=SMALL)
        assert e.worst_broadside["pointing_fraction_of_budget"] < 1e-9


def test_patterns_coarser_than_a_degree_are_refused():
    with pytest.raises(ValueError):
        c.EmbeddedPatterns(f_hz=np.array([2.44e9]), theta_deg=np.arange(-90, 91, 2.0),
                           g=np.zeros((1, 4, 91), dtype=complex))


# ------------------------------------------------------------------ verdict
def _sim(d, **kw):
    return c.run_g4(d, stage=c.SIMULATION, previous_pass=d, patterns=patterns_from(d),
                    protocol=SMALL, **kw)


def test_weak_coupling_passes_in_simulation():
    r = _sim(nn(-40.0, 20.0))
    assert r.verdict == c.PASS
    assert r.validity["routes_agree"]


def test_strong_coupling_fails_in_simulation():
    assert _sim(nn(-15.0, 20.0)).verdict == c.FAIL


def test_a_simulation_needs_two_passes_and_the_patterns():
    d = nn(-40.0)
    assert c.run_g4(d, stage=c.SIMULATION, protocol=SMALL).verdict == c.UNRESOLVED
    r = c.run_g4(d, stage=c.SIMULATION, previous_pass=d, protocol=SMALL)
    assert r.verdict == c.INTERMEDIATE


def test_a_mesh_that_changes_the_outcome_is_intermediate():
    weak, strong = nn(-40.0), nn(-15.0)
    r = c.run_g4(weak, stage=c.SIMULATION, previous_pass=strong,
                 patterns=patterns_from(weak), protocol=SMALL)
    assert r.verdict == c.INTERMEDIATE


def test_a_measurement_needs_uncertainty_beamformer_and_stage_one():
    d = nn(-40.0)
    assert c.run_g4(d, stage=c.MEASUREMENT, protocol=SMALL).verdict == c.UNRESOLVED
    assert c.run_g4(d, stage=c.MEASUREMENT, u_abs=1e-3, protocol=SMALL).verdict == c.UNRESOLVED
    r = c.run_g4(d, stage=c.MEASUREMENT, u_abs=1e-3, beamformer=ideal_beamformer(), protocol=SMALL)
    assert r.verdict == c.INTERMEDIATE
    r = c.run_g4(d, stage=c.MEASUREMENT, u_abs=1e-3, beamformer=ideal_beamformer(),
                 stage1_routes_agreed=True, protocol=SMALL)
    assert r.verdict == c.PASS
    assert r.validity["u_effective"] >= 1e-3


def test_an_uncertainty_that_straddles_the_budget_is_intermediate():
    d = nn(-27.0, 180.0, 0.0)
    r = c.run_g4(d, stage=c.MEASUREMENT, u_abs=0.02, beamformer=ideal_beamformer(),
                 stage1_routes_agreed=True, protocol=SMALL)
    assert r.verdict == c.INTERMEDIATE
    assert any("uncertainty" in x for x in r.reasons)


def test_the_reciprocity_defect_sets_a_floor_under_the_uncertainty():
    d = nn(-40.0)
    s = np.array(d.s)
    s[:, 0, 1] += 0.004
    asym = c.CouplingData(F, s, "synthetic")
    r = c.run_g4(asym, stage=c.MEASUREMENT, u_abs=1e-4, beamformer=ideal_beamformer(),
                 stage1_routes_agreed=True, protocol=SMALL)
    assert r.validity["u_effective"] == pytest.approx(0.002, rel=1e-6)


def test_a_band_not_covered_is_unresolved():
    d = c.toeplitz_coupling(np.array([2.41e9, 2.50e9]), 0.1, (0.01,))
    assert c.run_g4(d, stage=c.SIMULATION, previous_pass=d, protocol=SMALL).verdict == c.UNRESOLVED


def test_a_matrix_that_is_not_passive_is_unresolved():
    s = np.array(c.toeplitz_coupling(F, 0.95, (0.3,)).s)
    d = c.CouplingData(F, s, "synthetic")
    assert c.descriptors(s)["max_singular_value"] > 1.0
    r = c.run_g4(d, stage=c.SIMULATION, previous_pass=d, protocol=SMALL)
    assert r.verdict == c.UNRESOLVED


def test_a_residual_above_the_floor_demotes_a_pass():
    gam = np.zeros((F.size, 4, 8), dtype=complex)
    gam[:, :, :] = 0.05 * np.exp(1j * np.radians(np.arange(8) * 40.0))
    d = nn(-40.0, 20.0)
    r = c.run_g4(d, stage=c.MEASUREMENT, u_abs=1e-4, beamformer=c.Beamformer(F, gam),
                 stage1_routes_agreed=True, repeatability_floor=1e-9, protocol=SMALL)
    assert r.verdict == c.INTERMEDIATE


# ----------------------------------------------------------------- stages
def test_stage_follows_the_source():
    assert c.stage_for("hfss") == c.SIMULATION
    assert c.stage_for("vna") == c.MEASUREMENT
    with pytest.raises(ValueError):
        c.stage_for("ads")
    with pytest.raises(ValueError):
        c.stage_for("synthetic")
    with pytest.raises(ValueError):
        c.stage_for("hfss", c.MEASUREMENT)


# ------------------------------------------------------------------ guard
def test_guard_matrices_are_fixed_by_seed_and_reciprocal():
    d = nn(-25.0)
    g1, g2 = c.guard_matrices(d, 0.01, SMALL), c.guard_matrices(d, 0.01, SMALL)
    assert len(g1) == SMALL.guard_draws + 1
    for a, bb in zip(g1, g2):
        assert np.array_equal(a.s, bb.s)
    ds = np.array(g1[1].s)[0] - np.array(d.s)[0]
    assert np.allclose(ds, ds.T)
    assert np.allclose(np.abs(ds), 0.01)


# ------------------------------------------------------------------ ingest
def _write_s4p(d, path):
    tr = rfkit.synthetic_trace(d.f_hz, np.array(d.s))
    tr.network.write_touchstone(str(path.with_suffix("")), form="ri")
    return path


def test_a_four_port_touchstone_round_trips(tmp_path):
    d = nn(-20.0, 33.0)
    back = c.coupling_from_trace(rfkit.load_touchstone(_write_s4p(d, tmp_path / "a.s4p"),
                                                       source="synthetic"))
    assert np.allclose(back.s, d.s)
    assert back.source == "synthetic"


def test_two_port_pairs_assemble_into_the_matrix():
    d = nn(-20.0, 33.0, second=(10 ** (-30 / 20),))
    s = np.array(d.s)
    pairs = {}
    for i in range(4):
        for j in range(i + 1, 4):
            sub = s[:, [i, j]][:, :, [i, j]]
            pairs[(i, j)] = rfkit.synthetic_trace(F, sub)
    back, spread = c.assemble_from_two_ports(pairs)
    assert np.allclose(back.s, s)
    assert spread == pytest.approx(0.0, abs=1e-12)
    del pairs[(0, 1)]
    with pytest.raises(ValueError):
        c.assemble_from_two_ports(pairs)


# -------------------------------------------------------------------- cli
def test_g4_command_on_synthetic_files(tmp_path):
    from rfkit.cli import main

    # The command runs the full protocol; two frequency points keep it quick.
    d = nn(-40.0, 20.0)
    path = _write_s4p(d, tmp_path / "ant.s4p")
    pat = patterns_from(d)
    np.savez(tmp_path / "pat.npz", f_hz=pat.f_hz, theta_deg=pat.theta_deg, g=pat.g)
    rc = main(["g4", "--antenna", str(path), "--source", "synthetic", "--stage", "simulation",
               "--previous-pass", str(path), "--patterns", str(tmp_path / "pat.npz"),
               "--json", str(tmp_path / "g4.json")])
    assert rc == 0
    out = json.loads((tmp_path / "g4.json").read_text(encoding="utf-8"))
    assert out["stage"] == "simulation"
    assert out["verdict"] in (c.PASS, c.INTERMEDIATE, c.FAIL, c.UNRESOLVED)


def test_the_protocol_is_recorded_in_a_decision():
    assert (REPO / th.G4_DECISION).is_file()
    assert th.COUPLING_VARIANCE_FRACTION == th.VARIANCE_FRACTION
