"""Gate G4: whether the diagonal array state survives coupling between elements.

Decision 0008 holds the reasoning and ``experiments/EXP-011-coupling-model-adequacy.md``
the protocol. Everything here was written before any coupling data existed.

Two mechanisms, kept apart because they are measured apart:

- **antenna port mutual coupling**, the off diagonal of the antenna board's
  scattering matrix ``S_A`` at the element connectors, where the jumpers join
  the two boards. It is radiative, and the geometry sets it;
- **beamformer path crosstalk**, a property of the beamforming board. Its reverse
  part, the match of each output and the isolation between outputs, acts
  through ``S_Bo`` together with ``S_A``. Its forward part, one channel's
  transfer depending on another channel's state, is a state dependent diagonal
  error, judged under decision 0007 and not here.

The coupled forward model, for the waves ``t(s)`` the beamformer delivers into
matched loads in commanded state ``s``:

    a(s)    = (I - S_Bo(s) S_A)^-1 t(s)     waves actually incident on the antennas
    e(s)    = (I - S_A) a(s)                 radiating currents
    E(u, s) = v(u)^T e(s)                    far field, v_m(u) = exp(j m k d u)

The second line is the canonical minimum scattering approximation: an antenna
radiates according to its port current, the difference of incident and reflected
waves. It is not exact for patches, which is why a simulation verdict needs the
embedded element patterns as well, see :class:`EmbeddedPatterns`.

The diagonal model a calibration fits keeps one state independent complex factor
per channel and nothing off the diagonal:

    E_d(u, s) = v(u)^T diag(h) M0(s) t(s),   M0 = the diagonal of the model with S_A and S_Bo diagonal

``M0`` keeps the diagonal mismatch terms, so that with no coupling ``h = 1`` and the
two models coincide exactly: whatever is left over is due to coupling alone.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from . import budget as b
from . import thresholds as th
from .grid import Band, OutOfBand
from .io import RfTrace

PASS = "pass"
FAIL = "fail"
INTERMEDIATE = "intermediate"
UNRESOLVED = "unresolved"

SIMULATION = "simulation"
MEASUREMENT = "measurement"

N = b.N_DEFAULT
Q = 2 ** b.PHASE_BITS_DEFAULT
STEP_DEG = b.quantisation_step_deg()


# --------------------------------------------------------------------- data
def _interp_along_f(f: np.ndarray, arr: np.ndarray, freqs: np.ndarray) -> np.ndarray:
    """Complex linear interpolation along axis 0, refusing to extrapolate."""
    f = np.asarray(f, dtype=float)
    freqs = np.asarray(freqs, dtype=float)
    if freqs.min() < f[0] or freqs.max() > f[-1]:
        raise OutOfBand(
            f"requested {freqs.min() / 1e9:.6g} to {freqs.max() / 1e9:.6g} GHz, data covers "
            f"{f[0] / 1e9:.6g} to {f[-1] / 1e9:.6g} GHz; extrapolation is refused"
        )
    flat = arr.reshape(arr.shape[0], -1)
    out = np.empty((freqs.size, flat.shape[1]), dtype=complex)
    for k in range(flat.shape[1]):
        out[:, k] = np.interp(freqs, f, flat[:, k].real) + 1j * np.interp(freqs, f, flat[:, k].imag)
    return out.reshape((freqs.size,) + arr.shape[1:])


@dataclass(frozen=True)
class CouplingData:
    """The antenna board's scattering matrix at the element connectors."""

    f_hz: np.ndarray
    s: np.ndarray
    source: str
    provenance: list = field(default_factory=list)
    note: str = ""

    def __post_init__(self) -> None:
        s = np.asarray(self.s)
        if s.ndim != 3 or s.shape[1] != s.shape[2]:
            raise ValueError("s must have shape (frequencies, ports, ports)")
        if s.shape[0] != np.asarray(self.f_hz).size:
            raise ValueError("one matrix per frequency point")
        if s.shape[1] != N:
            raise ValueError(f"Rev A has {N} element ports, got {s.shape[1]}")

    def at(self, freqs) -> np.ndarray:
        return _interp_along_f(self.f_hz, np.asarray(self.s, dtype=complex), freqs)


def coupling_from_trace(trace: RfTrace, note: str = "") -> CouplingData:
    """From one N port Touchstone trace, a ``.s4p`` for Rev A."""
    return CouplingData(
        f_hz=trace.f, s=np.asarray(trace.network.s, dtype=complex),
        source=trace.provenance.source, provenance=[trace.provenance.as_dict()], note=note,
    )


def assemble_from_two_ports(pairs: dict, n_ports: int = N) -> tuple[CouplingData, float]:
    """Build the N port matrix from two port measurements, and check it.

    ``pairs`` maps ``(i, j)``, zero based with ``i < j``, to the two port trace
    measured with analyser port 1 on element ``i`` and port 2 on element ``j``,
    every other element port terminated in a matched load. Transmission terms
    come from their own pair. Each reflection is measured in ``n - 1`` pairs:
    they are averaged, and the largest disagreement is returned as a
    consistency figure that an assembly keeping only the last reading hides.
    """
    expected = {(i, j) for i in range(n_ports) for j in range(i + 1, n_ports)}
    if set(pairs) != expected:
        raise ValueError(f"need every pair {sorted(expected)}, got {sorted(pairs)}")
    traces = list(pairs.values())
    f = traces[0].f
    for t in traces:
        if t.n_ports != 2 or t.f.size != f.size or not np.allclose(t.f, f):
            raise ValueError("every pair must be a two port on one frequency grid")
    s = np.zeros((f.size, n_ports, n_ports), dtype=complex)
    refl = {i: [] for i in range(n_ports)}
    for (i, j), t in pairs.items():
        s[:, j, i] = t.s(2, 1)
        s[:, i, j] = t.s(1, 2)
        refl[i].append(t.s(1, 1))
        refl[j].append(t.s(2, 2))
    spread = 0.0
    for i, readings in refl.items():
        stack = np.array(readings)
        s[:, i, i] = stack.mean(axis=0)
        spread = max(spread, float(np.max(np.abs(stack - stack.mean(axis=0)))))
    sources = {t.provenance.source for t in traces}
    if len(sources) != 1:
        raise ValueError(f"pairs from more than one source: {sorted(sources)}")
    data = CouplingData(f_hz=f, s=s, source=sources.pop(),
                        provenance=[t.provenance.as_dict() for t in traces],
                        note="assembled from two port pairs")
    return data, spread


@dataclass(frozen=True)
class Beamformer:
    """The beamforming board's reverse path, seen from its outputs.

    ``output_match[f, n, k]`` is the reflection at output ``n`` with channel ``n``
    in state ``k``; ``isolation[f, n, m]`` the transmission from output ``m`` to
    output ``n`` with the common port terminated, taken as state independent.
    Either may be ``None``, meaning ideal.
    """

    f_hz: np.ndarray
    output_match: np.ndarray | None = None
    isolation: np.ndarray | None = None

    def at(self, freqs):
        g = None if self.output_match is None else _interp_along_f(self.f_hz, self.output_match, freqs)
        x = None if self.isolation is None else _interp_along_f(self.f_hz, self.isolation, freqs)
        return g, x


@dataclass(frozen=True)
class EmbeddedPatterns:
    """Embedded element patterns from the full wave solver.

    ``g[f, n, i]`` is the complex far field, in one polarisation and in the plane
    containing the array axis, at ``theta_deg[i]`` for a unit incident wave on port
    ``n`` with every other port matched. Sampled no coarser than one degree.
    """

    f_hz: np.ndarray
    theta_deg: np.ndarray
    g: np.ndarray

    def __post_init__(self) -> None:
        if np.max(np.diff(self.theta_deg)) > 1.0 + 1e-9:
            raise ValueError("embedded patterns must be sampled at one degree or finer")


# ------------------------------------------------------------ descriptors
def descriptors(s: np.ndarray) -> dict:
    """What a raw coupling number says, which is not the G4 verdict.

    ``s`` has shape ``(frequencies, N, N)``. The row aggregate is the coherent
    worst case: every coupling term into one element adding in phase.
    """
    s = np.asarray(s, dtype=complex)
    eye = np.eye(s.shape[1], dtype=bool)
    off = np.where(eye, 0.0, np.abs(s))
    adjacent = np.array([np.abs(s[:, i, i + 1]) for i in range(s.shape[1] - 1)])
    row = off.sum(axis=2)
    sv = np.linalg.svd(s, compute_uv=False)
    return {
        "max_offdiag_db": _db(off.max()),
        "max_adjacent_db": _db(adjacent.max()),
        "max_row_aggregate": float(row.max()),
        "max_row_aggregate_db": _db(row.max()),
        "reciprocity_defect": float(np.abs(s - np.swapaxes(s, 1, 2)).max()),
        "max_singular_value": float(sv.max()),
        "max_reflection_db": _db(np.abs(np.diagonal(s, axis1=1, axis2=2)).max()),
    }


def _db(x: float) -> float:
    return float(20.0 * math.log10(x)) if x > 0 else -math.inf


def screen_limit(eta: float) -> float:
    """The single number below which coupling cannot fail the unfitted comparison.

    If every channel's coupled current differs from its own diagonal term by at
    most ``rho``, its phase error is at most ``asin(rho)`` and its amplitude error
    at most ``rho``. Decision 0007's worst pattern bound then passes pointing when
    ``asin(rho) <= T``, and the joint gain criterion is looser, so the limit is
    ``sin(T)``: about 0.040 at ``eta = 0.10``, an aggregate of -28 dB.
    """
    return math.sin(math.radians(b.derive_phase_agreement_deg(eta)))


# ----------------------------------------------------------------- states
def steering_states(protocol: th.G4Protocol) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Every commanded state the verdict is judged on: angle, origin, state vector."""
    th0, origin, states = [], [], []
    for a in protocol.steering_deg:
        for k in range(protocol.origins):
            q = b.steering_command_deg(a, origin_state=k)
            th0.append(a)
            origin.append(k)
            states.append(np.round(q / STEP_DEG).astype(int) % Q)
    return np.array(th0, dtype=float), np.array(origin), np.array(states)


def calibration_states(n: int = N) -> np.ndarray:
    """The rotation family: all channels at state 0, then each channel through the others."""
    rows = [np.zeros(n, dtype=int)]
    for i in range(n):
        for k in range(1, Q):
            r = np.zeros(n, dtype=int)
            r[i] = k
            rows.append(r)
    return np.array(rows)


def _weights(states: np.ndarray) -> np.ndarray:
    return np.exp(1j * np.radians(states * STEP_DEG))


def _v(theta_deg, kd: float) -> np.ndarray:
    return np.exp(1j * kd * np.outer(np.sin(np.radians(np.atleast_1d(theta_deg))), np.arange(N)))


# -------------------------------------------------------------- operators
def _operators(s_a, states, gamma, iso, s_model):
    """Per state operators, each of shape (S, N, N).

    ``m_inc`` maps the beamformer's waves to the waves incident on the antennas,
    ``m_true`` to the radiating currents of the minimum scattering model, and
    ``m_model`` to the currents the model assumes: diagonal, keeping only the
    diagonal mismatch terms, unless a known coupling matrix is supplied.
    """
    eye = np.eye(N)
    n_s = len(states)
    g = np.zeros((n_s, N), dtype=complex)
    if gamma is not None:
        g = gamma[np.arange(N)[None, :], states]
    iso0 = np.zeros((N, N), dtype=complex) if iso is None else np.where(np.eye(N, dtype=bool), 0, iso)
    sbo = np.broadcast_to(iso0, (n_s, N, N)).copy()
    sbo[:, np.arange(N), np.arange(N)] = g
    m_inc = np.linalg.inv(eye[None] - sbo @ s_a[None])
    m_true = (eye - s_a)[None] @ m_inc
    if s_model is None:
        sd = np.diag(s_a)[None, :]
        m_model = np.zeros_like(m_true)
        m_model[:, np.arange(N), np.arange(N)] = (1 - sd) / (1 - g * sd)
    else:
        m_model = (eye - s_model)[None] @ np.linalg.inv(eye[None] - sbo @ s_model[None])
    return m_inc, m_true, m_model


# ------------------------------------------------------------------ beams
def _peaks(theta: np.ndarray, fields: np.ndarray) -> np.ndarray:
    """Beam maximum per column, parabolic interpolation on the grid."""
    mag = np.abs(fields)
    k = np.argmax(mag, axis=0)
    k = np.clip(k, 1, theta.size - 2)
    cols = np.arange(mag.shape[1])
    y0, y1, y2 = mag[k - 1, cols], mag[k, cols], mag[k + 1, cols]
    den = y0 - 2 * y1 + y2
    step = theta[1] - theta[0]
    off = np.where(den != 0, 0.5 * (y0 - y2) / np.where(den != 0, den, 1.0), 0.0)
    return theta[k] + step * off


def _psl_db(fields: np.ndarray) -> np.ndarray:
    """Peak sidelobe level relative to the beam maximum, per column.

    The main lobe runs from the nearest local minimum on each side of the
    maximum; everything beyond is sidelobe. Vectorised over columns.
    """
    mag = np.abs(fields)
    n_g, n_s = mag.shape
    p = np.argmax(mag, axis=0)
    lm = np.zeros_like(mag, dtype=bool)
    lm[1:-1] = (mag[1:-1] <= mag[:-2]) & (mag[1:-1] <= mag[2:])
    idx = np.arange(n_g)[:, None]
    last = np.maximum.accumulate(np.where(lm, idx, -1), axis=0)
    nxt = np.flip(np.minimum.accumulate(np.flip(np.where(lm, idx, n_g), axis=0), axis=0), axis=0)
    cols = np.arange(n_s)
    left = last[np.maximum(p - 1, 0), cols]
    right = nxt[np.minimum(p + 1, n_g - 1), cols]
    lobe = (idx > left[None, :]) & (idx < right[None, :])
    side = np.where(lobe, 0.0, mag).max(axis=0)
    peak = mag[p, cols]
    return np.where(side > 0, 20 * np.log10(np.where(side > 0, side, 1.0) / peak), -np.inf)


def _gain_loss_rows(w: np.ndarray) -> np.ndarray:
    """Exact coherence loss of each row of relative weights, as in decision 0007."""
    return -10 * np.log10(np.abs(w.sum(axis=1)) ** 2 / (w.shape[1] * np.sum(np.abs(w) ** 2, axis=1)))


# ------------------------------------------------------------- evaluation
@dataclass
class G4Evaluation:
    """The G4 metrics for one coupling matrix, before any verdict rule is applied."""

    freqs_hz: list
    band_covered: bool
    route: str
    pass_broadside_calibration: bool | None
    pass_best_diagonal: bool | None
    worst_broadside: dict = field(default_factory=dict)
    worst_best_diagonal: dict = field(default_factory=dict)
    unfitted: dict = field(default_factory=dict)
    screen: dict = field(default_factory=dict)
    recovered_state: dict = field(default_factory=dict)
    calibration_residual_max: float | None = None
    sidelobe_increase_db_max: float | None = None
    descriptors: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return dict(self.__dict__)


def _worst(ratio_p, ratio_g, th0, origin, fz):
    i_p, i_g = int(np.argmax(ratio_p)), int(np.argmax(ratio_g))
    return {
        "pointing_fraction_of_budget": float(ratio_p[i_p]),
        "pointing_at": {"f_hz": float(fz[i_p]), "steering_deg": float(th0[i_p]), "origin": int(origin[i_p])},
        "gain_fraction_of_budget": float(ratio_g[i_g]),
        "gain_at": {"f_hz": float(fz[i_g]), "steering_deg": float(th0[i_g]), "origin": int(origin[i_g])},
    }


def _interp_rows(theta, values, ang):
    """Complex linear interpolation of the columns of ``values`` at angles ``ang``."""
    ang = np.atleast_1d(ang)
    return np.array([[np.interp(a, theta, values[:, n].real) + 1j * np.interp(a, theta, values[:, n].imag)
                      for n in range(values.shape[1])] for a in ang])


def evaluate(
    data: CouplingData,
    beamformer: Beamformer | None = None,
    model: CouplingData | None = None,
    patterns: EmbeddedPatterns | None = None,
    protocol: th.G4Protocol = th.G4,
    eta: float | None = None,
    band: Band | None = None,
) -> G4Evaluation:
    """Every G4 metric for one antenna matrix.

    The true far field is built from port patterns: ``V (I - S_A)`` under the
    minimum scattering approximation, or the solver's embedded element patterns.
    Either way the field for state ``s`` is ``P(theta) a(s)``.

    The diagonal model is given the array's **average embedded element pattern**
    ``f(theta)``, which EXP-011 supplies, needs no calibration and adds no
    unknown. Without it, the part of every element's scan dependence that is
    common to all of them would be charged to coupling. Both beams are judged on
    one grid, so neither carries an interpolation the other does not.

    Errors are compared as equivalent element currents, the least squares
    excitation of ``f(theta) v(theta)`` that reproduces the field, so decision
    0007's error model applies unchanged: pointing from the exact beams,
    coherence loss from the relative current errors.

    Two diagonal models are judged. The **broadside calibration** fits ``h`` to
    complex probe readings at the protocol's probe direction over the rotation
    family, which is what the bench can do. The **best diagonal** is the least
    squares state independent ``h`` for the currents over exactly the states
    judged, which is as much as a diagonal fit could extract.

    ``model`` replaces the diagonal model with a known coupling matrix, the first
    promotion decision 0008 names if G4 fails. It is judged on the minimum
    scattering route, where it is exact when the matrix is right.
    """
    eta = th.COUPLING_VARIANCE_FRACTION if eta is None else eta
    band = band or Band(*th.OPERATING_BAND_HZ)
    f0 = th.OPERATING_F0_HZ
    if model is not None and patterns is not None:
        raise ValueError("the known coupling model is judged on the minimum scattering route")
    route = "embedded patterns" if patterns is not None else "minimum scattering"
    d = descriptors(np.asarray(data.s))

    if patterns is not None:
        freqs = np.asarray(patterns.f_hz, dtype=float)
        covered = bool(np.all((freqs >= data.f_hz[0]) & (freqs <= data.f_hz[-1])))
    else:
        covered = bool(data.f_hz[0] <= band.start_hz and data.f_hz[-1] >= band.stop_hz)
        inside = data.f_hz[(data.f_hz >= band.start_hz) & (data.f_hz <= band.stop_hz)]
        freqs = np.unique(np.concatenate([inside, [band.start_hz, band.stop_hz, f0]]))
    if not covered:
        return G4Evaluation(freqs_hz=[], band_covered=False, route=route,
                            pass_broadside_calibration=None, pass_best_diagonal=None,
                            descriptors=d)

    s_all = data.at(freqs)
    s_mod = None if model is None else model.at(freqs)
    gam, iso = (None, None) if beamformer is None else beamformer.at(freqs)

    th0, origin, st_steer = steering_states(protocol)
    st_cal = calibration_states()
    t_steer, t_cal = _weights(st_steer), _weights(st_cal)
    probes = np.unique(np.concatenate([[protocol.probe_deg], th0]))

    floor_point = b.pointing_std_from_independent_phase_deg(b.quantisation_rms_deg())
    budget_p = math.sqrt(eta) * floor_point / np.cos(np.radians(th0))
    budget_g = eta * b.floor_gain_loss_db()

    rp_bs, rg_bs, rp_best, rg_best, fz = [], [], [], [], []
    unf_phase, unf_amp, unf_rp, rho_max, resid, psl_inc = 0.0, 0.0, 0.0, 0.0, 0.0, -np.inf
    h_db, h_deg, h_dir = 0.0, 0.0, 0.0
    cms_grid = np.arange(-protocol.theta_span_deg, protocol.theta_span_deg + 1e-9,
                         protocol.theta_step_deg)

    for fi, f in enumerate(freqs):
        kd = 2 * math.pi * b.D_OVER_LAMBDA_DEFAULT * f / f0
        s_a = s_all[fi]
        sd = np.diag(s_a)
        g_f = None if gam is None else gam[fi]
        x_f = None if iso is None else iso[fi]
        m_mod_f = None if s_mod is None else s_mod[fi]
        inc_s, mt_s, mm_s = _operators(s_a, st_steer, g_f, x_f, m_mod_f)
        inc_c, _, mm_c = _operators(s_a, st_cal, g_f, x_f, m_mod_f)
        a_steer = np.einsum("snm,sm->sn", inc_s, t_steer)
        a_cal = np.einsum("snm,sm->sn", inc_c, t_cal)

        if patterns is None:
            grid = cms_grid
            vg = _v(grid, kd)
            ports = vg @ (np.eye(N) - s_a)                      # (G, N)
        else:
            grid = np.asarray(patterns.theta_deg, dtype=float)
            vg = _v(grid, kd)
            ports = np.asarray(patterns.g[fi], dtype=complex).T

        fields_true = ports @ a_steer.T
        if model is None:
            fhat = np.mean(ports / (vg * (1 - sd)[None, :]), axis=1)
            basis = np.linalg.pinv(fhat[:, None] * vg)          # (N, G)
            e_true = (basis @ fields_true).T
        else:
            fhat = np.ones(grid.size, dtype=complex)
            e_true = np.einsum("snm,sm->sn", mt_s, t_steer)

        def probe(ang, grid=grid, ports=ports, fhat=fhat, a_cal=a_cal):
            p_row = _interp_rows(grid, ports, ang)[0]
            f_row = np.interp(ang, grid, fhat.real) + 1j * np.interp(ang, grid, fhat.imag)
            return p_row @ a_cal.T, f_row

        def model_currents(h, mm=mm_s, t=t_steer):
            if model is None:
                return h[None, :] * np.einsum("snm,sm->sn", mm, t)
            return np.einsum("snm,sm->sn", mm, h[None, :] * t)

        def probe_fit(ang, kd=kd, probe=probe):
            y, f_row = probe(ang)
            vp = _v(ang, kd)[0]
            if model is None:
                a_mat = f_row * vp[None, :] * np.einsum("snm,sm->sn", mm_c, t_cal)
            else:
                a_mat = np.einsum("n,snm->sm", vp, mm_c) * t_cal
            h, *_ = np.linalg.lstsq(a_mat, y, rcond=None)
            return h, float(np.linalg.norm(y - a_mat @ h) / np.linalg.norm(y))

        def judge(h, grid=grid, vg=vg, fhat=fhat, e_true=e_true, fields_true=fields_true,
                  model_currents=model_currents):
            e_mod = model_currents(h)
            fields_mod = fhat[:, None] * (vg @ e_mod.T)
            dp = _peaks(grid, fields_true) - _peaks(grid, fields_mod)
            return dp, _gain_loss_rows(e_true / e_mod), fields_mod

        # Broadside probe calibration over the rotation family, as the bench does it.
        h_bs, r_bs = probe_fit(protocol.probe_deg)
        resid = max(resid, r_bs)
        dp, loss, fields_mod = judge(h_bs)
        rp_bs.append(np.abs(dp) / budget_p)
        rg_bs.append(loss / budget_g)
        psl_inc = max(psl_inc, float(np.max(_psl_db(fields_true) - _psl_db(fields_mod))))
        h_db = max(h_db, float(np.max(np.abs(20 * np.log10(np.abs(h_bs))))))
        h_deg = max(h_deg, float(np.max(np.abs(np.degrees(np.angle(h_bs))))))
        for a in probes:
            h_a, _ = probe_fit(a)
            h_dir = max(h_dir, float(np.max(np.abs(h_a / h_bs - 1))))

        # The best state independent diagonal, fitted to the currents themselves.
        if model is None:
            base = np.einsum("snm,sm->sn", mm_s, t_steer)
            h_best = np.sum(np.conj(base) * e_true, axis=0) / np.sum(np.abs(base) ** 2, axis=0)
        else:
            blocks = mm_s * t_steer[:, None, :]
            h_best, *_ = np.linalg.lstsq(blocks.reshape(-1, N), e_true.reshape(-1), rcond=None)
        dp_b, loss_b, _ = judge(h_best)
        rp_best.append(np.abs(dp_b) / budget_p)
        rg_best.append(loss_b / budget_g)
        fz.append(np.full(len(th0), f))

        # The unfitted comparison, H_full against diag(H_full), and its screen.
        # Always on the minimum scattering currents: it describes S_A, not a route.
        vg_c = _v(cms_grid, kd)
        diag_t = np.einsum("snn->sn", mt_s) * t_steer
        e_cms = np.einsum("snm,sm->sn", mt_s, t_steer)
        eps_u = e_cms / diag_t - 1
        unf_phase = max(unf_phase, float(np.max(np.abs(np.degrees(np.angle(1 + eps_u))))))
        unf_amp = max(unf_amp, float(np.max(np.abs(20 * np.log10(np.abs(1 + eps_u))))))
        unf_rp = max(unf_rp, float(np.max(
            np.abs(_peaks(cms_grid, vg_c @ e_cms.T) - _peaks(cms_grid, vg_c @ diag_t.T)) / budget_p)))
        off = np.abs(mt_s * t_steer[:, None, :])
        diag_mag = np.abs(diag_t)
        rho = (off.sum(axis=2) - diag_mag) / diag_mag
        rho_max = max(rho_max, float(rho.max()))

    rp_bs, rg_bs = np.concatenate(rp_bs), np.concatenate(rg_bs)
    rp_best, rg_best = np.concatenate(rp_best), np.concatenate(rg_best)
    fz = np.concatenate(fz)
    th_all = np.tile(th0, len(freqs))
    or_all = np.tile(origin, len(freqs))
    return G4Evaluation(
        freqs_hz=[float(x) for x in freqs],
        band_covered=True,
        route=route,
        pass_broadside_calibration=bool(np.all(rp_bs <= 1) and np.all(rg_bs <= 1)),
        pass_best_diagonal=bool(np.all(rp_best <= 1) and np.all(rg_best <= 1)),
        worst_broadside=_worst(rp_bs, rg_bs, th_all, or_all, fz),
        worst_best_diagonal=_worst(rp_best, rg_best, th_all, or_all, fz),
        unfitted={"max_phase_error_deg": unf_phase, "max_amplitude_error_db": unf_amp,
                  "pointing_fraction_of_budget": unf_rp},
        screen={"rho_max": rho_max, "limit": screen_limit(eta), "passes": rho_max <= screen_limit(eta)},
        recovered_state={"max_gain_bias_db": h_db, "max_phase_bias_deg": h_deg,
                         "max_change_with_probe_direction": h_dir},
        calibration_residual_max=resid,
        sidelobe_increase_db_max=psl_inc,
        descriptors=d,
    )


# ----------------------------------------------------------------- guard
def guard_matrices(data: CouplingData, u_abs: float, protocol: th.G4Protocol = th.G4) -> list:
    """The matrices a measured verdict must hold for, fixed by seed before any data.

    One with every coupling magnitude inflated by ``u_abs`` at its own phase, then
    ``protocol.guard_draws`` reciprocal perturbations of magnitude ``u_abs`` at
    random phases, the same across the band, as a calibration error would be.
    """
    s = np.asarray(data.s, dtype=complex)
    eye = np.eye(N, dtype=bool)
    mags = np.abs(s)
    inflated = np.where(eye, s, np.where(mags > 0, s / np.where(mags > 0, mags, 1) * (mags + u_abs), u_abs))
    out = [CouplingData(data.f_hz, inflated, data.source, data.provenance, "guard: inflated")]
    rng = np.random.default_rng(protocol.guard_seed)
    for k in range(protocol.guard_draws):
        ph = rng.uniform(0, 2 * np.pi, (N, N))
        ph = np.triu(ph) + np.triu(ph, 1).T
        ds = u_abs * np.exp(1j * ph)
        out.append(CouplingData(data.f_hz, s + ds[None], data.source, data.provenance, f"guard: draw {k}"))
    return out


# ---------------------------------------------------------------- verdict
@dataclass
class G4Report:
    stage: str
    verdict: str
    reasons: list
    nominal: G4Evaluation
    others: list
    validity: dict
    eta: float

    def as_dict(self) -> dict:
        return {
            "stage": self.stage, "verdict": self.verdict, "reasons": self.reasons,
            "eta": self.eta, "validity": self.validity,
            "nominal": self.nominal.as_dict(),
            "others": [
                {"note": n, "pass_broadside_calibration": e.pass_broadside_calibration,
                 "pass_best_diagonal": e.pass_best_diagonal}
                for n, e in self.others
            ],
        }

    def to_text(self) -> str:
        e = self.nominal
        lines = ["AetherArray gate G4, coupling model adequacy", "=" * 44, ""]
        lines.append(f"stage        : {self.stage}")
        lines.append(f"route        : {e.route}")
        lines.append(f"VERDICT      : {self.verdict.upper()}")
        for r in self.reasons:
            lines.append(f"  - {r}")
        lines += ["", "descriptive, not the verdict", "-" * 28]
        for k, v in e.descriptors.items():
            lines.append(f"  {k:<26}: {v:.4g}")
        if e.band_covered:
            lines += ["", "propagated through the array, fraction of the budget used", "-" * 57]
            for label, w in (("broadside calibration", e.worst_broadside),
                             ("best diagonal, fitted to the currents", e.worst_best_diagonal)):
                lines.append(f"  {label}:")
                lines.append(f"    pointing {w['pointing_fraction_of_budget']:.3f} at {w['pointing_at']}")
                lines.append(f"    gain     {w['gain_fraction_of_budget']:.3f} at {w['gain_at']}")
            lines.append(f"  unfitted, H_full against diag(H_full): {e.unfitted}")
            lines.append(f"  single number screen: {e.screen}")
            lines.append(f"  recovered state bias: {e.recovered_state}")
            lines.append(f"  calibration residual, largest: {e.calibration_residual_max:.4g}")
            lines.append(f"  peak sidelobe increase, largest: {e.sidelobe_increase_db_max:.3f} dB")
        lines += ["", f"validity: {self.validity}"]
        for note, o in self.others:
            lines.append(f"  {note}: broadside {o.pass_broadside_calibration}, "
                         f"best diagonal {o.pass_best_diagonal}")
        return "\n".join(lines) + "\n"


def stage_for(source: str, explicit: str | None = None) -> str:
    """Solver data is a simulation stage, analyser data a measurement stage."""
    inferred = {"hfss": SIMULATION, "vna": MEASUREMENT}.get(source)
    if source == "synthetic":
        if explicit not in (SIMULATION, MEASUREMENT):
            raise ValueError("synthetic data must be told which stage it stands in for")
        return explicit
    if inferred is None:
        raise ValueError(f"coupling data from {source!r} has no G4 stage; the circuit "
                         "simulator does not model radiative coupling")
    if explicit is not None and explicit != inferred:
        raise ValueError(f"{source} data is a {inferred} stage, not {explicit}")
    return inferred


def run_g4(
    data: CouplingData,
    stage: str | None = None,
    previous_pass: CouplingData | None = None,
    u_abs: float | None = None,
    beamformer: Beamformer | None = None,
    patterns: EmbeddedPatterns | None = None,
    repeatability_floor: float | None = None,
    stage1_routes_agreed: bool | None = None,
    protocol: th.G4Protocol = th.G4,
    eta: float | None = None,
) -> G4Report:
    """Apply the rules of decision 0008, in the order it fixes them.

    Simulation stage: the last two adaptive passes, and the embedded element
    patterns. Measurement stage: the analyser uncertainty, the beamformer's
    reverse path, and whether Stage 1 found the two far field routes in
    agreement. Anything missing leaves the verdict unresolved or intermediate,
    never a pass.
    """
    eta = th.COUPLING_VARIANCE_FRACTION if eta is None else eta
    stage = stage_for(data.source, stage)
    nominal = evaluate(data, beamformer=beamformer, protocol=protocol, eta=eta)
    reasons, others = [], []
    d = nominal.descriptors
    validity = {"band_covered": nominal.band_covered, "reciprocity_defect": d["reciprocity_defect"],
                "max_singular_value": d["max_singular_value"]}

    def unresolved(why):
        reasons.append(why)
        return G4Report(stage, UNRESOLVED, reasons, nominal, others, validity, eta)

    if not nominal.band_covered:
        return unresolved("the data do not cover band 57a; nothing is extrapolated")

    if stage == SIMULATION:
        if previous_pass is None:
            return unresolved("a simulation verdict needs the last two adaptive passes")
        prev = evaluate(previous_pass, beamformer=beamformer, protocol=protocol, eta=eta)
        others.append(("previous adaptive pass", prev))
        tol = float(np.max(np.abs(previous_pass.at(nominal.freqs_hz) - data.at(nominal.freqs_hz))))
        validity["mesh_change"] = tol
    else:
        if u_abs is None:
            return unresolved("a measured verdict needs the analyser uncertainty, EXP-004 O1 and O7")
        if beamformer is None:
            return unresolved("a measured verdict needs the beamformer output match and isolation")
        u_eff = max(u_abs, d["reciprocity_defect"] / 2)
        validity["u_effective"] = u_eff
        tol = u_eff
        for g in guard_matrices(data, u_eff, protocol):
            others.append((g.note, evaluate(g, beamformer=beamformer, protocol=protocol, eta=eta)))

    if d["max_singular_value"] > 1 + tol + 1e-9:
        return unresolved(f"the matrix is not passive within {tol:.3g}: the data are not physical")

    # Stability: the same outcome across the mesh passes, or across every guard matrix.
    evals = [nominal] + [o for _, o in others]
    stable = (len({e.pass_broadside_calibration for e in evals}) == 1
              and len({e.pass_best_diagonal for e in evals}) == 1)
    governing = nominal

    if stage == SIMULATION:
        checked = patterns is not None
        if not checked:
            reasons.append("embedded element patterns not supplied: the minimum scattering "
                           "approximation is unchecked, so the verdict cannot pass beyond intermediate")
        else:
            emb = evaluate(data, beamformer=beamformer, patterns=patterns, protocol=protocol, eta=eta)
            others.append(("embedded patterns", emb))
            validity["routes_agree"] = (
                emb.pass_broadside_calibration == nominal.pass_broadside_calibration
                and emb.pass_best_diagonal == nominal.pass_best_diagonal)
            if not validity["routes_agree"]:
                reasons.append("minimum scattering and embedded patterns disagree: the embedded "
                               "route governs here, and the measured stage is capped at intermediate")
                governing = emb
    else:
        checked = stage1_routes_agreed is True
        if stage1_routes_agreed is None:
            reasons.append("Stage 1's comparison of the two routes is not supplied")
        elif stage1_routes_agreed is False:
            reasons.append("Stage 1 found minimum scattering inadequate for this array, so a "
                           "measured verdict, which rests on it, stays intermediate")

    if not stable:
        reasons.append("the outcome changes within the uncertainty or across mesh passes")
    if checked and stable and not governing.pass_best_diagonal:
        verdict = FAIL
        reasons.append("even the best state independent diagonal, fitted to the currents over "
                       "the judged states, leaves a beam outside the budget")
    elif checked and stable and governing.pass_broadside_calibration:
        verdict = PASS
        reasons.append("a broadside calibration of the diagonal model keeps every judged "
                       "beam inside the budget")
    else:
        verdict = INTERMEDIATE
        if not governing.pass_broadside_calibration and governing.pass_best_diagonal:
            reasons.append("a diagonal model could hold, but a broadside probe calibration does "
                           "not find it: the calibration, not the model class, falls short")

    if repeatability_floor is None:
        reasons.append("calibration residual not yet compared with the EXP-005 Phase B floor")
    elif (nominal.calibration_residual_max or 0) > repeatability_floor and verdict == PASS:
        verdict = INTERMEDIATE
        reasons.append("the calibration residual exceeds the repeatability floor: the diagonal "
                       "likelihood is misspecified at the noise level")
    return G4Report(stage, verdict, reasons, nominal, others, validity, eta)


# ---------------------------------------------------------------- synthetic
def toeplitz_coupling(
    f_hz: np.ndarray,
    reflection: complex = 0.0,
    neighbours: tuple = (),
    n: int = N,
) -> CouplingData:
    """A **synthetic** uniform array matrix: ``neighbours[k]`` couples elements ``k + 1`` apart.

    Reciprocal and identical for every element, which a real array is not: edge
    elements differ. For tests and for the pre data sensitivity study only, and
    marked ``synthetic`` so it cannot be read as a simulation or a measurement.
    """
    s = np.zeros((n, n), dtype=complex)
    np.fill_diagonal(s, reflection)
    for k, c in enumerate(neighbours, start=1):
        for i in range(n - k):
            s[i, i + k] = s[i + k, i] = c
    f_hz = np.asarray(f_hz, dtype=float)
    return CouplingData(f_hz=f_hz, s=np.broadcast_to(s, (f_hz.size, n, n)).copy(),
                        source="synthetic", note="synthetic Toeplitz coupling")


def synthetic_chart(
    magnitudes_db=(-40.0, -35.0, -30.0, -27.0, -25.0, -22.0, -20.0),
    phases_deg=tuple(range(0, 360, 45)),
    reflection: complex = 0.0,
    protocol: th.G4Protocol = th.G4,
) -> list:
    """G4 against nearest neighbour coupling, on **synthetic** uniform matrices.

    Not a prediction of EXP-011. A matched, uniform, nearest neighbour array is an
    idealisation: the real matrix has edge effects, longer range terms, reflections
    and a frequency dependence. What the chart shows holds for any array: the
    outcome depends on the phase of the coupling as well as its magnitude, and the
    single number screen is conservative.
    """
    f = np.array([th.OPERATING_BAND_HZ[0] - 1e6, th.OPERATING_BAND_HZ[1] + 1e6])
    rows = []
    for m in magnitudes_db:
        for p in phases_deg:
            k = 10 ** (m / 20.0) * np.exp(1j * math.radians(p))
            e = evaluate(toeplitz_coupling(f, reflection, (k,)), protocol=protocol)
            rows.append({
                "coupling_db": m, "phase_deg": p,
                "broadside_pointing": e.worst_broadside["pointing_fraction_of_budget"],
                "broadside_gain": e.worst_broadside["gain_fraction_of_budget"],
                "best_pointing": e.worst_best_diagonal["pointing_fraction_of_budget"],
                "best_gain": e.worst_best_diagonal["gain_fraction_of_budget"],
                "outcome": PASS if e.pass_broadside_calibration
                else (FAIL if not e.pass_best_diagonal else INTERMEDIATE),
                "screen_passes": e.screen["passes"],
            })
    return rows


def load_beamformer_npz(path) -> Beamformer:
    """Arrays ``f_hz``, and ``output_match`` and or ``isolation``, as the protocol defines them."""
    z = np.load(path)
    return Beamformer(f_hz=z["f_hz"], output_match=z["output_match"] if "output_match" in z else None,
                      isolation=z["isolation"] if "isolation" in z else None)


def load_patterns_npz(path) -> EmbeddedPatterns:
    """Arrays ``f_hz``, ``theta_deg`` and complex ``g`` of shape (frequencies, ports, angles)."""
    z = np.load(path)
    return EmbeddedPatterns(f_hz=z["f_hz"], theta_deg=z["theta_deg"], g=z["g"])
