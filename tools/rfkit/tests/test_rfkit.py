"""Tests on analytically constructed networks.

Every network here is built from a formula, so the expected answer is known
exactly. **None of it is physical evidence**, and the traces carry the
``synthetic`` source so they cannot be mistaken for measurements elsewhere.
"""
from __future__ import annotations

import numpy as np
import pytest

import rfkit
from rfkit.grid import NoCommonBand, OutOfBand


def flat_two_port(f, s21, s11=0.0):
    s = np.zeros((np.size(f), 2, 2), dtype=complex)
    s[:, 0, 0] = s11
    s[:, 1, 1] = s11
    s[:, 1, 0] = s21
    s[:, 0, 1] = s21
    return s


def trace(f, s21, s11=0.0):
    return rfkit.synthetic_trace(f, flat_two_port(f, s21, s11))


# ----------------------------------------------------------------- phase wrap
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (359.0, 1.0, -2.0),
        (1.0, 359.0, 2.0),
        (0.0, 0.0, 0.0),
        (10.0, 350.0, 20.0),
        (-179.0, 179.0, 2.0),
    ],
)
def test_phase_error_takes_the_short_way_round(a, b, expected):
    assert rfkit.phase_error_deg(a, b) == pytest.approx(expected, abs=1e-9)


def test_exactly_opposite_phases_land_on_the_documented_edge():
    """The range is half open, [-180, 180), so 180 degrees comes back as -180.

    Both name the same angle. The test asserts the magnitude, and exists so the
    convention is pinned rather than discovered by someone later.
    """
    assert abs(rfkit.phase_error_deg(90.0, -90.0)) == pytest.approx(180.0, abs=1e-9)
    assert rfkit.phase_error_deg(90.0, -90.0) == pytest.approx(-180.0, abs=1e-9)


def test_phase_error_never_exceeds_180():
    rng = np.random.default_rng(0)
    a = rng.uniform(-10_000, 10_000, 500)
    b = rng.uniform(-10_000, 10_000, 500)
    assert np.all(np.abs(rfkit.phase_error_deg(a, b)) <= 180.0 + 1e-9)


def test_wrap_is_idempotent():
    x = np.linspace(-1000, 1000, 101)
    once = rfkit.wrap_deg(x)
    assert np.allclose(once, rfkit.wrap_deg(once))


# ------------------------------------------------------------------- the grid
def test_common_band_is_the_intersection():
    a = trace(np.linspace(1e9, 3e9, 21), 0.5)
    b = trace(np.linspace(2e9, 4e9, 21), 0.5)
    band = rfkit.common_band([a, b])
    assert band.start_hz == pytest.approx(2e9)
    assert band.stop_hz == pytest.approx(3e9)


def test_disjoint_traces_refuse_to_compare():
    a = trace(np.linspace(1e9, 2e9, 11), 0.5)
    b = trace(np.linspace(3e9, 4e9, 11), 0.5)
    with pytest.raises(NoCommonBand):
        rfkit.common_band([a, b])


def test_grid_never_leaves_the_shared_band():
    a = trace(np.linspace(1e9, 3e9, 201), 0.5)
    b = trace(np.linspace(2e9, 4e9, 11), 0.5)
    _, grid = rfkit.align([a, b])
    assert grid[0] >= 2e9 - 1e-6
    assert grid[-1] <= 3e9 + 1e-6


def test_grid_takes_the_coarsest_input_not_the_finest():
    """Comparison must not invent resolution no input had."""
    a = trace(np.linspace(2e9, 3e9, 501), 0.5)
    b = trace(np.linspace(2e9, 3e9, 11), 0.5)
    _, grid = rfkit.align([a, b])
    assert grid.size == 11


def test_extrapolation_is_refused():
    a = trace(np.linspace(2e9, 3e9, 11), 0.5)
    with pytest.raises(OutOfBand):
        rfkit.extract_at(a, 1.0e9)
    with pytest.raises(OutOfBand):
        rfkit.extract_at(a, 4.0e9)


# -------------------------------------------------------------- extraction
def test_extract_at_recovers_a_known_value():
    f = np.linspace(2.0e9, 3.0e9, 101)
    s21 = 0.5 * np.exp(1j * np.deg2rad(30.0))
    m = rfkit.extract_at(trace(f, s21), 2.44e9)
    assert m.s21_mag_db == pytest.approx(20 * np.log10(0.5), abs=1e-9)
    assert m.insertion_loss_db == pytest.approx(-20 * np.log10(0.5), abs=1e-9)
    assert m.s21_phase_deg == pytest.approx(30.0, abs=1e-9)


def test_extract_at_interpolates_between_points():
    f = np.array([2.0e9, 3.0e9])
    s = np.zeros((2, 2, 2), dtype=complex)
    s[:, 1, 0] = np.array([1.0 + 0j, 3.0 + 0j])
    t = rfkit.synthetic_trace(f, s)
    m = rfkit.extract_at(t, 2.5e9)
    assert m.s21.real == pytest.approx(2.0, abs=1e-9)


def test_return_loss_sign_convention():
    f = np.linspace(2e9, 3e9, 11)
    m = rfkit.extract_at(trace(f, 0.5, s11=0.1), 2.5e9)
    assert m.return_loss_db == pytest.approx(20.0, abs=1e-9)


def test_band_metrics_span_the_sweep():
    f = np.linspace(2e9, 3e9, 51)
    b = rfkit.extract_band(trace(f, 0.5))
    assert b.n_points == 51
    assert b.insertion_loss_db_mean == pytest.approx(-20 * np.log10(0.5), abs=1e-9)


# ------------------------------------------------------------- imbalance
def test_amplitude_imbalance():
    vals = [1.0, 10 ** (-1 / 20), 10 ** (-2 / 20), 1.0]
    assert rfkit.amplitude_imbalance_db(vals) == pytest.approx(2.0, abs=1e-9)


def test_phase_spread_is_computed_on_the_circle():
    """Channels clustered at the wrap point must not report a huge spread."""
    vals = [np.exp(1j * np.deg2rad(a)) for a in (179.0, -179.0, 180.0)]
    assert rfkit.phase_spread_deg(vals) < 5.0


# --------------------------------------------------------------- array state
def _channel_traces(gains_db, phases_deg, f=None):
    f = np.linspace(2.4e9, 2.5e9, 21) if f is None else f
    out = {}
    for n, (g, p) in enumerate(zip(gains_db, phases_deg)):
        s21 = 10 ** (g / 20.0) * np.exp(1j * np.deg2rad(p))
        out[n] = trace(f, s21)
    return out


def test_state_recovers_injected_gain_and_phase():
    gains = [-3.0, -2.6, -3.3, -2.1]
    phases = [17.0, 42.0, -23.0, 187.0]
    state = rfkit.state_from_channel_traces(_channel_traces(gains, phases), f0_hz=2.44e9)

    assert state.kind == "diagonal"
    assert state.n_channels == 4
    assert state.identifiable_count() == 6  # 2N - 2

    expected_gain = np.array(gains) - gains[0]
    expected_phase = rfkit.wrap_deg(np.array(phases) - phases[0])
    assert np.allclose(state.relative_gain_db(), expected_gain, atol=1e-9)
    assert np.allclose(state.relative_phase_deg(), expected_phase, atol=1e-9)


def test_state_relative_phase_wraps_the_short_way():
    """A channel at 187 degrees against a reference at 17 is 170, not -190."""
    state = rfkit.state_from_channel_traces(
        _channel_traces([0, 0], [17.0, 187.0]), f0_hz=2.44e9
    )
    assert state.relative_phase_deg()[1] == pytest.approx(170.0, abs=1e-9)


def test_state_preserves_raw_complex_values():
    state = rfkit.state_from_channel_traces(
        _channel_traces([-3.0, -6.0], [10.0, 20.0]), f0_hz=2.44e9
    )
    assert np.abs(state.diagonal[0]) == pytest.approx(10 ** (-3.0 / 20), abs=1e-9)
    assert state.diagonal[0] != state.relative()[0] * 0  # raw kept, not normalised away


def test_reference_channel_is_unity_by_construction():
    state = rfkit.state_from_channel_traces(
        _channel_traces([-3.0, -6.0, -1.0], [10.0, 20.0, 30.0]), f0_hz=2.44e9, reference=2
    )
    assert state.relative_gain_db()[2] == pytest.approx(0.0, abs=1e-12)
    assert state.relative_phase_deg()[2] == pytest.approx(0.0, abs=1e-12)


def test_channels_must_be_contiguous_from_zero():
    ch = _channel_traces([0, 0], [0, 0])
    ch[5] = ch.pop(1)
    with pytest.raises(ValueError):
        rfkit.state_from_channel_traces(ch, f0_hz=2.44e9)


def test_full_matrix_is_supported_but_not_the_default():
    m = np.eye(4, dtype=complex) * 0.7
    m[0, 1] = 0.05
    full = rfkit.state_from_full_matrix(m, f0_hz=2.44e9)
    assert full.kind == "full"
    assert full.identifiable_count() == 2 * 4 * 4
    assert full.as_matrix()[0, 1] == pytest.approx(0.05)
    # the diagonal baseline embeds into the same matrix form
    diag = rfkit.state_from_channel_traces(_channel_traces([0] * 4, [0] * 4), f0_hz=2.44e9)
    assert diag.as_matrix().shape == (4, 4)
    assert diag.kind == "diagonal"


# ---------------------------------------------------------------- comparison
def test_identical_traces_compare_as_zero_difference():
    f = np.linspace(2.4e9, 2.5e9, 51)
    a, b = trace(f, 0.5), trace(f, 0.5)
    c = rfkit.compare_pair(a, b, f0_hz=2.44e9)
    assert c.s21_mag_diff_db_max == pytest.approx(0.0, abs=1e-9)
    assert c.s21_phase_diff_deg_max == pytest.approx(0.0, abs=1e-9)


def test_comparison_detects_a_known_offset():
    f = np.linspace(2.4e9, 2.5e9, 51)
    a = trace(f, 0.5 * np.exp(1j * np.deg2rad(10.0)))
    b = trace(f, 0.5 * 10 ** (-1.0 / 20) * np.exp(1j * np.deg2rad(4.0)))
    c = rfkit.compare_pair(a, b, f0_hz=2.44e9)
    assert c.s21_mag_diff_db_at_f0 == pytest.approx(1.0, abs=1e-6)
    assert c.s21_phase_diff_deg_at_f0 == pytest.approx(6.0, abs=1e-6)


def test_comparison_phase_difference_wraps():
    f = np.linspace(2.4e9, 2.5e9, 11)
    a = trace(f, np.exp(1j * np.deg2rad(179.0)))
    b = trace(f, np.exp(1j * np.deg2rad(-179.0)))
    c = rfkit.compare_pair(a, b, f0_hz=2.44e9)
    assert abs(c.s21_phase_diff_deg_at_f0) == pytest.approx(2.0, abs=1e-6)


def test_verdicts_without_a_comparison_class_are_unresolved():
    # Synthetic traces carry no comparison class unless told one, see test_budget.py.
    f = np.linspace(2.4e9, 2.5e9, 11)
    c = rfkit.compare_pair(trace(f, 0.5), trace(f, 0.4), f0_hz=2.44e9)
    assert set(c.verdicts.values()) == {"unresolved"}
    assert rfkit.unresolved_keys()  # and the gap is enumerable


# ------------------------------------------------------------------ dataset
def test_measurement_decodes_the_beam_state_word():
    # channel 2 enable and the 90 degree bit: bits 8 and 10
    word = (1 << 8) | (1 << 10)
    m = rfkit.Measurement(
        session="s", sequence_index=0, beam_state_word=word,
        observation=0.5 + 0j, observation_kind="complex_s21",
        provenance=rfkit.Provenance(source="synthetic"),
    )
    bits = m.channel_bits(2)
    assert bits["enable"] and bits["b90"]
    assert not bits["b45"] and not bits["b180"]
    assert not any(m.channel_bits(1).values())


def test_beam_state_word_must_be_16_bit():
    with pytest.raises(ValueError):
        rfkit.Measurement(
            session="s", sequence_index=0, beam_state_word=1 << 16,
            observation=0.0, observation_kind="power_dbm",
            provenance=rfkit.Provenance(source="synthetic"),
        )


def test_measurement_set_keeps_metadata_and_gives_statistics():
    f = np.linspace(2.4e9, 2.5e9, 11)
    ms = rfkit.MeasurementSet()
    for i, g in enumerate([-3.00, -3.02, -2.98]):
        ms.add(
            trace(f, 10 ** (g / 20)),
            rfkit.Measurement(
                session=f"sess{i}", sequence_index=i, beam_state_word=0,
                observation=0.0, observation_kind="power_dbm",
                provenance=rfkit.Provenance(source="synthetic"),
                temperature_phase_c=21.0 + i,
            ),
        )
    summary = ms.repeatability_summary()
    assert summary["n_repeats"] == 3
    assert summary["sessions"] == ["sess0", "sess1", "sess2"]
    assert summary["temperatures_phase_c"] == [21.0, 22.0, 23.0]
    assert summary["s21_mag_std_db_max"] == pytest.approx(0.02, abs=5e-3)


def test_measurement_set_refuses_mismatched_grids():
    ms = rfkit.MeasurementSet()
    ms.add(trace(np.linspace(2.4e9, 2.5e9, 11), 0.5))
    ms.add(trace(np.linspace(2.4e9, 2.5e9, 21), 0.5))
    with pytest.raises(ValueError):
        ms.network_set()


def test_dataset_round_trip(tmp_path):
    rec = rfkit.Measurement(
        session="s1", sequence_index=3, beam_state_word=0x1234,
        observation=complex(0.5, -0.25), observation_kind="complex_s21",
        provenance=rfkit.Provenance(source="vna"),
        temperature_detector_c=22.5, uncertainty=0.01, uncertainty_kind="stddev_db",
    )
    path = tmp_path / "d.jsonl"
    rfkit.write_dataset([rec], path)
    back = rfkit.read_dataset(path)
    assert back[0]["beam_state_word"] == 0x1234
    assert back[0]["observation"]["imag"] == pytest.approx(-0.25)
    assert back[0]["provenance"]["source"] == "vna"


# --------------------------------------------------------------- calibration
def test_calibration_refuses_rather_than_pretending():
    f = np.linspace(2.4e9, 2.5e9, 11)
    with pytest.raises(rfkit.CalibrationNotAvailable):
        rfkit.apply_calibration(trace(f, 0.5))


def test_loaded_traces_are_marked_uncalibrated():
    f = np.linspace(2.4e9, 2.5e9, 11)
    assert trace(f, 0.5).provenance.calibration == "none"


# ------------------------------------------------------------------ io guard
def test_source_must_be_known():
    with pytest.raises(ValueError):
        rfkit.Provenance(source="wishful")


def test_round_trip_through_touchstone(tmp_path):
    f = np.linspace(2.4e9, 2.5e9, 11)
    t = trace(f, 0.5 * np.exp(1j * np.deg2rad(33.0)))
    path = tmp_path / "x.s2p"
    t.network.write_touchstone(str(path.with_suffix("")), form="ri")
    back = rfkit.load_touchstone(path, source="vna")
    assert back.provenance.source == "vna"
    assert back.provenance.sha256
    m = rfkit.extract_at(back, 2.44e9)
    assert m.s21_phase_deg == pytest.approx(33.0, abs=1e-6)


# --------------------------------------------------------------- the example
def test_example_runs_end_to_end(tmp_path):
    from rfkit.example import run_example

    result = run_example(tmp_path / "ex")
    assert (tmp_path / "ex" / "processed" / "comparison.json").exists()
    assert (tmp_path / "ex" / "processed" / "array_state.json").exists()
    assert result["state"].n_channels == 4
    for p in result["state"].provenance:
        assert p.source in ("synthetic", "vna")
