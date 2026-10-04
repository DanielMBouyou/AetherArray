"""Tests of the canonical stack-up, its validation, and what is derived from it.

The canonical file is decision 0009's. These tests check the rules it has to
keep: every number with a unit, a status and a source; nominal values and
tolerances never mixed; no RF geometry frozen; and every derived width or
length labelled as the seed or estimate it is. Seeds are checked for
determinism and dimensional sanity, not against a "right" answer, which is
SIM-001's job.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import re
from pathlib import Path

import numpy as np
import pytest

import rfkit
from rfkit import stackup as su
from rfkit.provenance import Provenance, stackup_mismatch

REPO = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="module")
def st():
    return su.load()


@pytest.fixture()
def raw():
    return json.loads(su.CANONICAL_PATH.read_text(encoding="utf-8"))


def problems_after(raw, mutate):
    mutate(raw)
    return su.validate(raw)


# ----------------------------------------------------------------- the file itself
def test_canonical_file_is_valid_and_fingerprinted(st):
    assert su.validate(st.raw) == []
    assert re.fullmatch(r"reva-stackup-r\d+:[0-9a-f]{12}", st.fingerprint)
    assert st.raw["status"] == "selected"
    assert set(st.constructions) == {"beamformer", "antenna"}


def test_candidates_file_is_valid_and_never_selected():
    cand = su.load_candidates()
    assert cand.raw["status"] == "evidence"
    assert not set(cand.constructions) & {"beamformer", "antenna"}


def test_every_source_is_in_the_bibliography(st):
    bib = (REPO / "docs" / "references" / "bibliography.md").read_text(encoding="utf-8")
    for doc in (st, su.load_candidates()):
        for sid, s in doc.raw["sources"].items():
            if s["kind"] == "repository":
                assert (REPO / s["url"]).exists(), sid
            else:
                assert f"[{sid}]" in bib, f"{sid} is cited but not in the bibliography"


def test_frequency_is_not_duplicated_in_the_stackup(raw):
    text = json.dumps(raw)
    assert "2.44e9" not in text and "2440000000" not in text


# ----------------------------------------------------------------- validation rules
def test_missing_unit_status_or_source_is_rejected(raw):
    q = raw["constructions"]["beamformer"]["layers"][1]["thickness"]
    for key in ("unit", "status", "source"):
        r = copy.deepcopy(raw)
        del r["constructions"]["beamformer"]["layers"][1]["thickness"][key]
        assert su.validate(r), key
    assert q["unit"] == "mm"


def test_units_must_be_explicit_and_known(raw):
    p = problems_after(raw, lambda r: r["materials"]["fr4_prepreg_7628"]["permittivity"]
                       .update(unit="mils"))
    assert any("unit" in x for x in p)


def test_status_vocabulary_is_closed(raw):
    p = problems_after(raw, lambda r: r["materials"]["copper"]["conductivity"]
                       .update(status="probably"))
    assert any("status" in x for x in p)


def test_unknown_source_is_rejected(raw):
    p = problems_after(raw, lambda r: r["materials"]["copper"]["conductivity"]
                       .update(source="V999"))
    assert any("source" in x for x in p)


def test_a_tolerance_inside_a_nominal_value_is_rejected(raw):
    p = problems_after(raw, lambda r: r["materials"]["fr4_prepreg_7628"]["permittivity"]
                       .update(plus=0.2, minus=0.2))
    assert any("tolerances go in the tolerances block" in x for x in p)


def test_a_bound_carries_no_distribution(raw):
    p = problems_after(raw, lambda r: r["tolerances"]["beamformer"]["etched_width"]
                       .update(sigma=0.05))
    assert any("no distribution" in x for x in p)


def test_an_unbounded_tolerance_carries_no_number(raw):
    def mutate(r):
        r["tolerances"]["antenna"]["rf_copper_thickness"]["plus"] = 0.01
    assert any("unbounded" in x for x in problems_after(raw, mutate))


def test_every_construction_reserves_all_four_tolerances(st, raw):
    for key in st.constructions:
        assert set(st.tolerances[key]) == set(su.TOLERANCE_PARAMETERS)
    p = problems_after(raw, lambda r: r["tolerances"]["beamformer"].pop("etched_width"))
    assert any("reserved parameter missing" in x for x in p)


def test_rf_reference_must_be_the_adjacent_plane(raw):
    p = problems_after(raw, lambda r: r["constructions"]["beamformer"]["rf_line"]
                       .update(reference_layer="L3"))
    assert any("next copper layer" in x for x in p)


@pytest.mark.parametrize("key", ["w50_seed", "trace_width", "patch_length", "element_spacing",
                                 "feed_inset", "line_length"])
def test_rf_geometry_cannot_be_frozen_in_the_stackup(raw, key):
    p = problems_after(raw, lambda r: r["constructions"]["antenna"].update(
        {key: {"value": 1.0, "unit": "mm", "status": "assumed", "source": "D0009"}}))
    assert any("may not be frozen" in x for x in p)


def test_simulation_model_choices_carry_provenance(raw):
    p = problems_after(raw, lambda r: r["simulation_model"]["copper_roughness"].pop("source"))
    assert any("simulation_model.copper_roughness" in x for x in p)


def test_load_raises_on_an_invalid_file(tmp_path, raw):
    raw["constructions"]["beamformer"]["layers"][0]["thickness"]["unit"] = "oz"
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(su.StackupError):
        su.load(path)


def test_nominal_and_tolerance_are_kept_apart(st):
    """No bound appears in a construction, and every bound names a model input."""
    text = json.dumps(st.raw["constructions"])
    assert '"plus"' not in text and '"minus"' not in text
    for bounds in st.tolerances.values():
        for b in bounds.values():
            assert b.parameter in {"h", "er", "t", "w"}
            assert b.bounded or (b.minus is None and b.plus is None)


# ----------------------------------------------------------------- the seed
def test_seed_is_deterministic_and_labelled(st):
    a, b = su.seed(st, "beamformer"), su.seed(st, "beamformer")
    assert a == b
    assert "INITIALISATION ONLY" in a["label"] and "not the final width" in a["label"]


@pytest.mark.parametrize("key", ["beamformer", "antenna"])
def test_seed_is_dimensionally_sane(st, key):
    c = st.construction(key)
    s = su.seed(st, key)
    w, h = s["w_seed_m"], c.h.si
    line = su.line(h, c.er.value, w, c.t.si, tand=c.tand.value, sigma=c.sigma.si)
    assert line.z0_ohm == pytest.approx(50.0, abs=0.01)
    assert 1.0 < s["eeff"] < c.er.value
    assert s["lambda_g_m"] < s["lambda0_m"]
    assert s["lambda0_m"] == pytest.approx(299_792_458.0 / 2.44e9)
    assert 0.5 < w / h < 5.0                       # a 50 ohm microstrip, not a stripline
    assert abs(s["w_seed_vs_closed_form"]) < 0.10  # zero thickness synthesis, independent
    # The closed form ignores copper thickness; at t/h near 0.17 on the
    # beamformer that alone lowers the effective permittivity by about 3.5 per cent.
    assert abs(s["eeff"] / s["eeff_closed_form"] - 1) < 0.05
    L = s["length_for_deg_m"]
    assert L["90"] == pytest.approx(2 * L["45"]) and L["315"] == pytest.approx(7 * L["45"])


def test_thicker_copper_and_wider_lines_lower_the_impedance():
    base = su.line(0.2e-3, 4.4, 0.37e-3, 35e-6)
    assert su.line(0.2e-3, 4.4, 0.40e-3, 35e-6).z0_ohm < base.z0_ohm
    assert su.line(0.2e-3, 4.4, 0.37e-3, 45e-6).z0_ohm < base.z0_ohm
    assert su.line(0.22e-3, 4.4, 0.37e-3, 35e-6).z0_ohm > base.z0_ohm


def test_closed_form_width_reproduces_pozar_example():
    """Pozar, Microwave Engineering, example 3.7: 50 ohm on 0.127 cm, er 2.20."""
    assert su.closed_form_width(50.0, 2.20, 1.27e-3) == pytest.approx(3.89e-3, rel=0.01)


# ----------------------------------------------------------------- sensitivity
def test_phase_error_formula_is_exact_for_a_uniform_line():
    assert su.phase_error_deg(180.0, 3.2, 3.2) == 0.0
    assert su.phase_error_deg(180.0, 3.2, 3.2 * 1.02) == pytest.approx(180 * (math.sqrt(1.02) - 1))


def test_first_order_sensitivity_agrees_with_the_line_model(st):
    c = st.construction("beamformer")
    s = su.seed(st, "beamformer")
    w = s["w_seed_m"]
    d_er = 0.2
    exact = su.phase_error_deg(
        315.0, s["eeff"],
        su.line(c.h.si, c.er.value + d_er, w, c.t.si, tand=c.tand.value).eeff)
    approx = su.first_order_phase_error_deg(315.0, c.er.value, c.h.si, w, d_er)
    assert approx == pytest.approx(exact, rel=0.10)


def test_sensitivity_signs_and_structure(st):
    r = su.sensitivity(st, "beamformer")
    er = r["one_at_a_time"]["rf_dielectric_permittivity"]
    assert er["high"]["phase_error_deg"]["315"] > 0 > er["low"]["phase_error_deg"]["315"]
    hh = r["one_at_a_time"]["rf_dielectric_thickness"]
    assert hh["high"]["z0_ohm"] > 50 > hh["low"]["z0_ohm"]
    worst = r["worst_corner_phase_error_deg"]
    assert worst["315"] >= max(abs(v["high"]["phase_error_deg"]["315"])
                               for v in r["one_at_a_time"].values())
    assert worst["315"] == pytest.approx(7 * worst["45"], rel=1e-9)


def test_unbounded_tolerances_are_reported_not_computed(st):
    r = su.sensitivity(st, "antenna")
    assert "rf_copper_thickness" in r["unbounded"]
    assert "rf_copper_thickness" not in r["one_at_a_time"]
    with pytest.raises(su.StackupError):
        st.tolerances["antenna"]["rf_copper_thickness"].interval(35e-6)


def test_loss_spread_grows_with_the_roughness_bound(st):
    smooth = su.state_loss_spread_db(st, "beamformer", 1.0)
    rough = su.state_loss_spread_db(st, "beamformer", 2.0)
    assert 0 < smooth < rough < 2 * smooth


def test_patch_figures_are_sanity_checks_only(st):
    ant, bf = su.patch_sanity(st, "antenna"), su.patch_sanity(st, "beamformer")
    assert "SANITY CHECK ONLY" in ant["label"]
    lam0 = ant["lambda0_m"]
    assert 0.2 * lam0 < ant["l_patch_m"] < 0.5 * lam0
    assert ant["l_patch_m"] < ant["w_patch_m"] < 0.5 * lam0
    assert ant["fractional_bandwidth_vswr2"] > 5 * bf["fractional_bandwidth_vswr2"]
    assert ant["radiation_efficiency"] > 3 * bf["radiation_efficiency"]
    lo, hi = ant["resonance_shift_for_dk_bounds"]
    assert lo < 0 < hi


# ----------------------------------------------------------------- SIM-001
def test_sim001_parameters_come_from_the_canonical_file(st):
    p = su.sim001_parameters(st)
    c = st.construction("beamformer")
    v = p["variables_mm"]
    assert p["stackup"] == st.fingerprint
    assert v["sub_h"] == pytest.approx(c.h.si * 1e3)
    assert v["cu_t"] == pytest.approx(c.t.si * 1e3)
    assert v["w_seed"] == pytest.approx(su.seed(st, "beamformer")["w_seed_m"] * 1e3, abs=1e-4)
    assert p["materials"]["substrate"]["permittivity"] == c.er.value
    assert v["l_long"] > v["l_short"] and v["port_h"] > v["sub_h"] and v["port_w"] > v["w_seed"]
    assert p["width_sweep_mm"][0] < v["w_seed"] < p["width_sweep_mm"][-1]


def test_sim_export_metadata_is_checked(st):
    assert len(su.check_sim_export({}, st)) >= len(su.SIM_EXPORT_FIELDS)
    meta = {k: None for k in su.SIM_EXPORT_FIELDS}
    meta.update(stackup=st.fingerprint, port_impedance_ohm=50.0)
    assert su.check_sim_export(meta, st) == []
    meta["stackup"] = "reva-stackup-r0:000000000000"
    assert any("not the canonical" in x for x in su.check_sim_export(meta, st))


def test_hfss_builder_plan_needs_no_aedt_and_reads_the_canonical_file(st):
    path = REPO / "tools" / "sim" / "sim001_hfss.py"
    spec = importlib.util.spec_from_file_location("sim001_hfss", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pl = mod.plan(st)
    v = pl["parameters"]["variables_mm"]
    assert len(pl["designs"]) == 6
    for d in pl["designs"]:
        assert d["substrate"]["sizes"][2] == pytest.approx(v["sub_h"])
        assert d["trace"]["origin"][2] == pytest.approx(v["sub_h"])
        for port in d["ports"]:
            (x0, y0, z0), (x1, y1, z1) = port["integration_line"]
            assert z0 == 0.0 and z1 == pytest.approx(v["sub_h"]) and y0 == y1 == port["y"]


def _builder():
    path = REPO / "tools" / "sim" / "sim001_hfss.py"
    spec = importlib.util.spec_from_file_location("sim001_hfss", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_port_size_check_plan_scales_only_port_and_box(st):
    """Protocol step 6: seed width, both lengths, port and box enlarged by half."""
    mod = _builder()
    base = {d["name"]: d for d in mod.plan(st)["designs"]}
    big = mod.plan(st, port_scale=1.5, seed_only=True)["designs"]
    assert len(big) == 2
    for d in big:
        ref = base[d["name"].replace("_ps1p5", "")]
        assert d["name"].endswith("_ps1p5")
        assert d["w_mm"] == ref["w_mm"] == su.sim001_parameters(st)["variables_mm"]["w_seed"]
        assert d["trace"] == ref["trace"]
        assert d["substrate"]["sizes"][0] == pytest.approx(1.5 * ref["substrate"]["sizes"][0])
        assert d["air"]["sizes"][2] + d["trace"]["origin"][2] == pytest.approx(1.5 * ref["port_h_mm"])


def test_builder_refuses_to_build_twice_into_one_project(st, tmp_path):
    mod = _builder()
    (tmp_path / "sim001.aedt").write_text("", encoding="utf-8")
    with pytest.raises(FileExistsError):
        mod.build(tmp_path, student=True, solve=False, st=st)


def test_failure_cleanup_touches_only_servers_started_by_the_run():
    import time
    assert _builder().stop_servers_started_after(time.time() + 3600) == []


# ----------------------------------------------------------------- traceability
def test_stackup_fingerprint_travels_with_a_trace(tmp_path, st):
    f = np.linspace(2.3e9, 2.6e9, 31)
    s = np.zeros((f.size, 2, 2), dtype=complex)
    s[:, 1, 0] = s[:, 0, 1] = np.exp(-1j * f / 1e9)
    trace = rfkit.synthetic_trace(f, s)
    path = tmp_path / "line.s2p"
    trace.network.write_touchstone(str(path))
    loaded = rfkit.load_touchstone(path, source="hfss", stackup=st.fingerprint)
    assert loaded.provenance.stackup == st.fingerprint
    assert loaded.with_network(loaded.network, "copy").provenance.stackup == st.fingerprint
    assert loaded.provenance.as_dict()["stackup"] == st.fingerprint


def test_comparison_warns_when_stackups_differ():
    a = Provenance(source="hfss", stackup="reva-stackup-r1:aaaaaaaaaaaa")
    b = Provenance(source="vna", stackup="reva-stackup-r2:bbbbbbbbbbbb")
    c = Provenance(source="synthetic")
    assert stackup_mismatch([a, b]) is not None
    assert stackup_mismatch([a, a.as_dict(), c]) is None


# ----------------------------------------------------------------- documentation
def test_generated_tables_in_the_documentation_are_current(st):
    stale = su.check_docs(st, su.load_candidates())
    assert stale == [], f"run: cd tools && python -m rfkit.cli stackup --write-docs ({stale})"


def test_every_generated_block_is_known():
    for rel in su.GENERATED_DOCS:
        text = (REPO / rel).read_text(encoding="utf-8")
        names = re.findall(r"<!-- stackup:begin (\S+) -->", text)
        assert names, rel
        assert set(names) <= set(su.SECTIONS), rel
