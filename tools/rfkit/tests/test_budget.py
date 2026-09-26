"""Tests of the error budget, and of the thresholds derived from it.

Every expected value is analytic or an exact array factor computation, and
every trace is ``synthetic``. The thresholds are tested against the derivation
that produced them, so a recorded value that drifts from its derivation fails
here rather than in a review.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

import rfkit
from rfkit import budget as b
from rfkit import thresholds as th

REPO = Path(__file__).resolve().parents[3]
F = np.linspace(2.39e9, 2.50e9, 56)   # covers band 57a with margin on both sides


def two_port(f, s21):
    s = np.zeros((np.size(f), 2, 2), dtype=complex)
    s[:, 1, 0] = s21
    s[:, 0, 1] = s21
    return rfkit.synthetic_trace(f, s)


def states(phases_deg, mags_db=None, f=F):
    """One synthetic trace per state, flat in frequency unless given as arrays."""
    out = {}
    for s, p in enumerate(phases_deg):
        m = 0.0 if mags_db is None else mags_db[s]
        out[s] = two_port(f, 10 ** (np.asarray(m) / 20.0) * np.exp(1j * np.deg2rad(p)))
    return out


# ------------------------------------------------------------- band and floor
def test_band_edge_offsets_are_computed_not_typed():
    lo, hi = b.band_edge_offsets()
    assert hi == pytest.approx(43.5 / 2440.0, rel=1e-12)
    assert round(hi * 100, 2) == 1.78
    assert lo == pytest.approx(-40.0 / 2440.0, rel=1e-12)


def test_quantisation_floor():
    sq = 45.0 / math.sqrt(12.0)
    assert b.quantisation_rms_deg() == pytest.approx(sq)
    assert b.pointing_std_from_independent_phase_deg(sq) == pytest.approx(
        sq / (math.pi * math.sqrt(5.0))
    )
    assert b.floor_gain_loss_db() == pytest.approx(
        10 / math.log(10) * math.radians(sq) ** 2 * 0.75
    )
    assert b.state_discrimination_ceiling_deg() == 22.5


# ------------------------------------------------------------- error structures
def test_finite_array_gain_matches_monte_carlo_and_the_limit_does_not():
    r = b.mean_monte_carlo(13.0, trials=1500)
    assert r.gain_loss_db_mean == pytest.approx(r.gain_loss_db_predicted, rel=0.08)
    large_array_limit = 10 / math.log(10) * math.radians(13.0) ** 2
    assert large_array_limit > 1.25 * r.gain_loss_db_mean


def test_independent_pointing_matches_monte_carlo():
    r = b.mean_monte_carlo(10.0, trials=1500)
    assert r.pointing_std_deg == pytest.approx(r.pointing_std_predicted_deg, rel=0.08)


def test_common_constant_phase_costs_nothing():
    r = b.monte_carlo(20.0, trials=200, correlated=True)
    assert r.pointing_std_deg == pytest.approx(0.0, abs=1e-6)
    assert r.gain_loss_db_mean == pytest.approx(0.0, abs=1e-9)
    assert r.gain_loss_db_predicted == 0.0


def test_amplitude_errors_alone_do_not_steer():
    rng = np.random.default_rng(7)
    for _ in range(20):
        amps = 1.0 + rng.normal(0.0, 0.2, 4)
        assert b.peak_direction_deg(amps, np.zeros(4)) == pytest.approx(0.0, abs=1e-6)


def test_proportional_error_vanishes_at_f0_and_steers_away_from_it():
    assert b.pointing_error_proportional_deg(30.0, 0.0) == pytest.approx(0.0, abs=1e-9)
    assert abs(b.pointing_error_proportional_deg(30.0, 0.0178)) > 0.05


def test_proportional_error_without_a_wrap_is_a_ramp():
    # Origin state 6 makes the 30 degree command 270, 180, 90, 0: no wrap, so a
    # scaling error is an exact ramp of -90 x per element.
    assert list(b.steering_command_deg(30.0, origin_state=6)) == [270.0, 180.0, 90.0, 0.0]
    x = 0.01
    slope = math.radians(-90.0 * x)
    predicted = -math.degrees(slope / (math.pi * math.cos(math.radians(30.0))))
    assert b.pointing_error_proportional_deg(30.0, x, origin_state=6) == pytest.approx(
        predicted, rel=0.03
    )


def test_the_worst_origin_is_at_least_as_bad_as_any_origin():
    worst, k = b.worst_proportional_pointing_deg(15.0, 0.0178)
    for origin in range(8):
        assert abs(b.pointing_error_proportional_deg(15.0, 0.0178, origin_state=origin)) <= worst
    assert 0 <= k < 8


def test_worst_pattern_factor_is_the_documented_ratio():
    ratio = b.worst_pattern_pointing_deg(1.0) / b.pointing_std_from_independent_phase_deg(1.0)
    assert ratio == pytest.approx(0.8 * math.sqrt(5.0))


def test_worst_pattern_bound_matches_the_exact_array_factor():
    t = 2.0
    exact = abs(b.peak_direction_deg(np.ones(4), np.array([-t, -t, t, t])))
    assert exact == pytest.approx(b.worst_pattern_pointing_deg(t), rel=0.02)


# ----------------------------------------------------------------- derivation
def test_thresholds_scale_with_the_square_root_of_eta():
    assert b.derive_phase_agreement_deg(0.4) == pytest.approx(2 * b.derive_phase_agreement_deg(0.1))


def test_the_phase_bound_cannot_consume_more_than_the_budget():
    with pytest.raises(ValueError):
        b.derive_amplitude_allowance_rel(0.1, 10.0)


def _derive(t):
    fn = getattr(b, t.derivation)
    eta = th.VARIANCE_FRACTION
    if t.derivation == "derive_phase_agreement_deg":
        return fn(eta)
    return fn(eta, th.get("s21_phase_diff_deg", th.HFSS_VS_ADS).value)


@pytest.mark.parametrize("t", th.provisional(), ids=lambda t: t.id)
def test_every_recorded_value_is_its_derivation_rounded_down(t):
    derived = _derive(t)
    assert t.value <= derived < t.value + 0.01
    assert t.status == th.PROVISIONAL
    assert (REPO / t.source).is_file()


def test_every_empty_threshold_says_why():
    for t in th.all_thresholds():
        if t.value is None:
            assert t.status in (th.STATUS_UNRESOLVED, th.NOT_A_LIMIT)
            assert len(t.note) > 40


def test_a_value_without_a_derivation_is_refused():
    with pytest.raises(ValueError):
        th.Threshold("x", th.DESIGN, 1.0, "dB", th.PROVISIONAL, th.ABSOLUTE,
                     "a note", source=th.DECISION)
    with pytest.raises(ValueError):
        th.Threshold("x", th.DESIGN, 1.0, "dB", th.STATUS_UNRESOLVED, th.ABSOLUTE, "a note")


def test_recorded_values_hold_jointly_at_every_worst_pattern():
    eta = th.VARIANCE_FRACTION
    t = th.get("s21_phase_diff_deg", th.HFSS_VS_ADS).value
    m = th.get("s21_mag_diff_db", th.HFSS_VS_ADS).value
    p = th.get("amplitude_imbalance_db", th.DESIGN).value
    floor_point = b.pointing_std_from_independent_phase_deg(b.quantisation_rms_deg())
    budget_gain = eta * b.floor_gain_loss_db()

    assert abs(b.peak_direction_deg(np.ones(4), np.array([-t, -t, t, t]))) <= (
        math.sqrt(eta) * floor_point
    )
    phase_patterns = ([-t, -t, t, t], [t, -t, -t, t], [t, -t, t, -t])
    signs = ([1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1])
    r = 10 ** (-p / 20.0)
    for ph in phase_patterns:
        for sg in signs:
            amp_m = 10 ** (m * np.array(sg) / 20.0)
            amp_p = np.where(np.array(sg) > 0, 1.0, r)
            assert b.gain_loss_db_exact(amp_m, ph) <= budget_gain
            assert b.gain_loss_db_exact(amp_p, ph) <= budget_gain


def test_band_edge_dispersion_stays_inside_the_budget_with_the_best_origin():
    sweep = b.proportional_sweep(th.VARIANCE_FRACTION, step_deg=3.0)
    assert sweep["best_origin"]["largest_fraction"] < 1.0


# ------------------------------------------------------------ comparison class
def test_comparison_class_comes_from_real_sources():
    assert th.comparison_class(["hfss", "ads"]) == th.HFSS_VS_ADS
    assert th.comparison_class(["ads", "vna"]) == th.SIMULATION_VS_VNA
    assert th.comparison_class(["vna", "hfss"]) == th.SIMULATION_VS_VNA
    assert th.comparison_class(["vna", "vna"]) is None
    assert th.comparison_class(["hfss", "hfss"]) is None
    assert th.comparison_class(["synthetic", "synthetic"]) is None


def test_only_a_synthetic_trace_may_be_told_its_class():
    assert th.comparison_class(["synthetic"], th.HFSS_VS_ADS) == th.HFSS_VS_ADS
    with pytest.raises(ValueError):
        th.comparison_class(["hfss", "vna"], th.HFSS_VS_ADS)
    with pytest.raises(ValueError):
        th.comparison_class(["synthetic"], "made_up")


# ----------------------------------------------------------- state comparison
NOMINAL = [0, 45, 90, 135, 180, 225, 270, 315]


def test_an_offset_common_to_every_state_is_absorbed():
    a = states([p + 10.0 for p in NOMINAL], [1.5] * 8)
    c = rfkit.compare_states(a, states(NOMINAL), comparison=th.HFSS_VS_ADS)
    assert c.phase_diff_deg_max == pytest.approx(0.0, abs=1e-9)
    assert c.mag_diff_db_max == pytest.approx(0.0, abs=1e-9)
    assert c.verdicts == {"s21_phase_diff_deg": "pass", "s21_mag_diff_db": "pass"}
    # while the plain difference of one state is large, and judged by nothing
    pair = rfkit.compare_pair(a[3], states(NOMINAL)[3], f0_hz=2.44e9, comparison=th.HFSS_VS_ADS)
    assert pair.s21_phase_diff_deg_max == pytest.approx(10.0, abs=1e-6)
    assert pair.verdicts["s21_phase_diff_deg"] == th.NOT_APPLICABLE
    assert pair.verdicts["s21_mag_diff_db"] == th.NOT_APPLICABLE


def test_a_state_dependent_error_is_caught_on_either_side_of_the_limit():
    limit = th.get("s21_phase_diff_deg", th.HFSS_VS_ADS).value
    for err, expected in ((limit - 0.05, "pass"), (limit + 0.05, "fail")):
        a = NOMINAL.copy()
        a[3] += err
        c = rfkit.compare_states(states(a), states(NOMINAL), comparison=th.HFSS_VS_ADS)
        assert c.per_state[3]["phase_deg_max"] == pytest.approx(err, abs=1e-9)
        assert c.verdicts["s21_phase_diff_deg"] == expected


def test_state_differences_are_taken_on_the_circle():
    a = states([179.0, -178.0])
    bb = states([-179.0, 178.0])
    c = rfkit.compare_states(a, bb, comparison=th.HFSS_VS_ADS)
    # reference differs by -2, state 1 by +4, so the state dependent part is 6
    assert c.phase_diff_deg_max == pytest.approx(6.0, abs=1e-9)


def test_a_state_dependent_magnitude_error_is_judged():
    mags = [0.0] * 8
    mags[5] = 0.5
    c = rfkit.compare_states(states(NOMINAL, mags), states(NOMINAL), comparison=th.HFSS_VS_ADS)
    assert c.mag_diff_db_max == pytest.approx(0.5, abs=1e-9)
    assert c.verdicts["s21_mag_diff_db"] == "fail"


def test_an_error_only_at_the_band_edge_is_not_missed():
    ramp = np.clip((F - 2.44e9) / (2.4835e9 - 2.44e9), 0.0, None) * 3.0
    a = {0: two_port(F, np.ones_like(F)), 1: two_port(F, np.exp(1j * np.deg2rad(45.0 + ramp)))}
    c = rfkit.compare_states(a, states([0.0, 45.0]), comparison=th.HFSS_VS_ADS)
    assert c.phase_diff_deg_at_f0 == pytest.approx(0.0, abs=1e-9)
    assert c.phase_diff_deg_max == pytest.approx(3.0, abs=1e-6)
    assert c.verdicts["s21_phase_diff_deg"] == "fail"


def test_a_band_not_covered_is_unresolved_not_extrapolated():
    f = np.linspace(2.41e9, 2.50e9, 31)
    c = rfkit.compare_states(states(NOMINAL, f=f), states(NOMINAL, f=f), comparison=th.HFSS_VS_ADS)
    assert not c.band_covered
    assert c.phase_diff_deg_max is None
    assert set(c.verdicts.values()) == {th.UNRESOLVED}
    assert c.phase_diff_deg_at_f0 == pytest.approx(0.0, abs=1e-9)


def test_synthetic_states_without_a_class_are_unresolved():
    c = rfkit.compare_states(states(NOMINAL), states(NOMINAL))
    assert c.comparison is None
    assert set(c.verdicts.values()) == {th.UNRESOLVED}


def test_state_sets_must_match():
    with pytest.raises(ValueError):
        rfkit.compare_states(states(NOMINAL[:3]), states(NOMINAL[:4]))


def test_simulation_against_analyser_stays_unresolved():
    c = rfkit.compare_states(states(NOMINAL), states(NOMINAL), comparison=th.SIMULATION_VS_VNA)
    assert set(c.verdicts.values()) == {th.UNRESOLVED}


# ---------------------------------------------------------------- array state
def _array_state(gains_db, phases_deg):
    traces = {
        n: two_port(F, 10 ** (g / 20.0) * np.exp(1j * np.deg2rad(p)))
        for n, (g, p) in enumerate(zip(gains_db, phases_deg))
    }
    return rfkit.state_from_channel_traces(traces, f0_hz=2.44e9)


def test_array_state_design_verdicts():
    ok = _array_state([0.0, 0.3, -0.4, 0.2], [0.0, 10.0, 170.0, -90.0])
    assert ok.verdicts()["amplitude_imbalance_db"] == "pass"
    assert ok.verdicts()["channel_phase_spread_deg"] == th.NOT_APPLICABLE
    assert _array_state([0.0, 1.0, 0.0, 0.0], [0.0] * 4).verdicts()["amplitude_imbalance_db"] == "fail"
    assert "verdicts" in ok.as_dict()


# ------------------------------------------------------------- reproducibility
def test_study_is_deterministic_and_says_what_it_is():
    text = b.study(trials=100)
    assert text == b.study(trials=100)
    assert "provisional" in text
    assert "1.72" not in text


def test_budget_command_writes_report_and_json(tmp_path):
    from rfkit.cli import main

    rc = main(["budget", "--trials", "100",
               "--json", str(tmp_path / "b.json"), "--report", str(tmp_path / "b.txt")])
    assert rc == 0
    d = json.loads((tmp_path / "b.json").read_text(encoding="utf-8"))
    ids = {t["id"]: t for t in d["recorded_thresholds"]}
    assert ids["s21_phase_diff_deg[hfss_vs_ads]"]["status"] == th.PROVISIONAL
    assert ids["channel_phase_spread_deg[design]"]["status"] == th.NOT_A_LIMIT
    assert d["criterion"]["variance_fraction"] == th.VARIANCE_FRACTION
    assert "decision 0007" in (tmp_path / "b.txt").read_text(encoding="utf-8")


def test_compare_states_command_runs_on_synthetic_files(tmp_path):
    from rfkit.cli import main

    args = []
    for label, tool in (("a", states(NOMINAL[:3])), ("b", states(NOMINAL[:3]))):
        args += [f"--{label}-source", "synthetic"]
        for s, t in tool.items():
            path = tmp_path / f"{label}{s}.s2p"
            t.network.write_touchstone(str(path.with_suffix("")), form="ri")
            args += [f"--{label}", f"{s}={path}"]
    rc = main(["compare-states", *args, "--json", str(tmp_path / "c.json")])
    assert rc == 0
    d = json.loads((tmp_path / "c.json").read_text(encoding="utf-8"))
    assert d["comparison"] is None
    assert set(d["verdicts"].values()) == {th.UNRESOLVED}
