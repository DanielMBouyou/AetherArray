"""Error budget: from an RF parameter error to an array level consequence.

Everything here is analytic or Monte Carlo on the array factor. It needs no
hardware, no measured data and no solver, so it can be rerun by anyone and
checked line by line.

The array it describes is the one decisions 0003 and 0004 fixed: four elements,
half wavelength spacing, three phase bits of 45, 90 and 180 degrees, 2.44 GHz,
operated in band 57a, 2400 to 2483.5 MHz.

Conventions and assumptions, stated once:

- Uniform linear array, isotropic elements, uniform amplitude taper.
- Steering to broadside unless a scan angle is given. The benchmark steering
  set is broadside, 15, 30 and 45 degrees, ``benchmarks/specification.md``.
- Small error approximations are used where marked, and every one of them is
  checked against the Monte Carlo or the exact array factor in :func:`study`.

Three error structures, which do not cost the same:

- **independent** per channel errors steer the beam through their component
  that is linear in element index, and cost coherent gain;
- a **common constant** phase, the same on every channel and every state,
  costs nothing: it is one of the two quantities the diagonal state cannot
  observe, ``docs/mathematics/inverse-calibration.md``;
- a **common proportional** error, an electrical length scaled by the same
  fraction everywhere, as a frequency offset or a permittivity error produces,
  is correlated across channels but **depends on the commanded state**, so it
  steers the beam. It is the worst of the three to mistake for the second.

The derivation of the provisional acceptance thresholds lives in the
``derive_*`` functions. The values are recorded, with their status and source,
in :mod:`rfkit.thresholds`; decision 0007 holds the reasoning. Nothing in this
module sets a threshold by itself.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

N_DEFAULT = 4
D_OVER_LAMBDA_DEFAULT = 0.5
PHASE_BITS_DEFAULT = 3

#: Decision 0004 and bibliography entry R1, band 57a.
F0_HZ = 2.44e9
BAND_START_HZ = 2400.0e6
BAND_STOP_HZ = 2483.5e6

#: ``benchmarks/specification.md`` section 2, the minimum steering set.
STEERING_ANGLES_DEG = (0.0, 15.0, 30.0, 45.0)

DB_PER_NEPER_POWER = 10.0 / math.log(10.0)  # 4.3429, converts a variance to dB


def band_edge_offsets(
    f0_hz: float = F0_HZ, start_hz: float = BAND_START_HZ, stop_hz: float = BAND_STOP_HZ
) -> tuple[float, float]:
    """Fractional offsets of the band edges from ``f0``, lower then upper.

    About -1.64 and +1.78 per cent for band 57a around 2.44 GHz. Computed rather
    than typed, because an earlier draft of this module typed 1.72.
    """
    return (start_hz - f0_hz) / f0_hz, (stop_hz - f0_hz) / f0_hz


# --------------------------------------------------------------------- basics
def beamwidth_deg(n: int = N_DEFAULT, d_over_lambda: float = D_OVER_LAMBDA_DEFAULT) -> float:
    """Half power beam width at broadside, from ``docs/mathematics/formulation.md``.

    ``0.886 * lambda / (N d)`` in radians, converted to degrees.
    """
    return math.degrees(0.886 / (n * d_over_lambda))


def quantisation_step_deg(bits: int = PHASE_BITS_DEFAULT) -> float:
    """Phase step of a uniform phase shifter with ``bits`` bits."""
    return 360.0 / (2 ** bits)


def quantisation_rms_deg(bits: int = PHASE_BITS_DEFAULT) -> float:
    """RMS residual of rounding a phase to the nearest step.

    A uniform error over one step of width ``q`` has standard deviation
    ``q / sqrt(12)``. This is the floor the hardware cannot beat, whatever the
    calibration does, so it anchors every phase budget below it.
    """
    return quantisation_step_deg(bits) / math.sqrt(12.0)


# ------------------------------------------------------- phase to pointing
def slope_index_variance(n: int = N_DEFAULT) -> float:
    """``sum (i - mean)^2`` over element indices, the denominator of a slope fit."""
    idx = np.arange(n, dtype=float)
    return float(np.sum((idx - idx.mean()) ** 2))


def pointing_from_phase_slope_deg(
    slope_deg: float,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    theta0_deg: float = 0.0,
) -> float:
    """Beam shift caused by a linear phase ramp across the array.

    The beam points where the total phase is stationary in element index. With
    a commanded steering phase and an added ramp of ``slope`` radians per
    element, that gives

        sin(theta) = sin(theta0) - slope / (k d)

    with ``k d = 2 pi (d / lambda)``. This is exact, not a small error
    approximation; only the conversion back to an angle is linearised when the
    shift is small.
    """
    kd = 2.0 * math.pi * d_over_lambda
    s = math.sin(math.radians(theta0_deg)) - math.radians(slope_deg) / kd
    if abs(s) > 1.0:
        return float("nan")  # beam has been steered off the visible region
    return math.degrees(math.asin(s)) - theta0_deg


def pointing_std_from_independent_phase_deg(
    sigma_phi_deg: float,
    n: int = N_DEFAULT,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
) -> float:
    """Pointing error standard deviation from independent per channel phase errors.

    Only the component of the error that is **linear in element index** steers
    the beam. Fitting a slope to ``n`` independent errors of standard deviation
    ``sigma`` gives a slope whose standard deviation is
    ``sigma / sqrt(sum (i - mean)^2)``, and the slope maps to an angle through
    :func:`pointing_from_phase_slope_deg`.

    For four elements at half wavelength spacing this reduces to
    ``sigma_phi / (pi * sqrt(5))``, about ``sigma_phi / 7.02``.
    """
    sigma_slope_deg = sigma_phi_deg / math.sqrt(slope_index_variance(n))
    kd = 2.0 * math.pi * d_over_lambda
    return math.degrees(math.radians(sigma_slope_deg) / kd)


def pointing_from_common_mode_phase_deg(sigma_phi_deg: float) -> float:
    """Pointing error from a phase error common to every channel: exactly zero.

    A phase added equally to all elements multiplies the array factor by a
    constant. It moves no beam, and it is one of the two quantities the
    identifiability count in the inverse calibration document calls
    unobservable. Kept as a function so the asymmetry between correlated and
    independent errors is explicit rather than implied.
    """
    return 0.0


# ------------------------------------------------------------- errors to gain
def gain_loss_db_from_phase(sigma_phi_deg: float, n: int = N_DEFAULT) -> float:
    """Mean coherent gain lost to independent Gaussian phase errors, for ``n`` elements.

    ``docs/mathematics/formulation.md`` section 4 gives ``E[G]/G0 = exp(-sigma^2)``,
    which is the **large array limit**. For finite ``n`` the incoherent part of
    the sum survives:

        E[G]/G0 = exp(-sigma^2) + (1 - exp(-sigma^2)) / n

    At four elements the limit overstates the loss by about a third, 0.223 dB
    against 0.166 dB at the quantisation floor, and the Monte Carlo in
    :func:`study` agrees with the finite form. To first order both are
    ``(1 - 1/n) sigma^2``, so the loss is proportional to the error variance.
    """
    s2 = math.radians(sigma_phi_deg) ** 2
    coherent = math.exp(-s2)
    return -10.0 * math.log10(coherent + (1.0 - coherent) / n)


def gain_loss_db_from_amplitude(sigma_rel: float, n: int = N_DEFAULT) -> float:
    """Mean coherent gain lost to independent amplitude errors, ``sigma_rel`` relative.

    For ``a_i = 1 + delta_i`` the normalised array gain is
    ``|sum a|^2 / (n sum a^2)``, whose mean is ``(1 + sigma^2/n) / (1 + sigma^2)``,
    to first order ``1 - (1 - 1/n) sigma^2``. Amplitude errors cost gain at the
    same rate per unit variance as phase errors in radians, which is why the
    two share one variance budget in :func:`derive_magnitude_agreement_db`.
    """
    s2 = sigma_rel ** 2
    return -10.0 * math.log10((1.0 + s2 / n) / (1.0 + s2))


def gain_loss_db_exact(amps, phases_deg) -> float:
    """Exact coherent gain lost by one deterministic set of weights, in dB.

    ``|sum a exp(j phi)|^2 / (n sum a^2)`` against its ideal value of one. No
    approximation, so it is what the threshold tests check against.
    """
    a = np.asarray(amps, dtype=float)
    w = a * np.exp(1j * np.radians(np.asarray(phases_deg, dtype=float)))
    return float(-10.0 * np.log10(np.abs(w.sum()) ** 2 / (a.size * np.sum(a ** 2))))


def relative_from_db_spread(spread_db: float) -> float:
    """Relative amplitude standard deviation implied by a peak to peak dB spread.

    Assumes the channel gains are spread roughly uniformly over the range, so
    ``sigma_dB = spread / sqrt(12)``, then converts to a relative amplitude with
    ``d(a)/a = ln(10)/20 * dB``.
    """
    sigma_db = spread_db / math.sqrt(12.0)
    return (math.log(10.0) / 20.0) * sigma_db


def sidelobe_rise_db(sigma_phi_deg: float, sigma_rel_amp: float, n: int = N_DEFAULT) -> float:
    """Average error induced sidelobe level relative to the peak, in dB.

    The standard small error result for a uniform array is that random errors
    scatter a fraction ``(sigma_a^2 + sigma_phi^2) / N`` of the power into an
    average sidelobe floor. Returned as a negative number of dB below the peak.
    """
    var = sigma_rel_amp ** 2 + math.radians(sigma_phi_deg) ** 2
    if var <= 0:
        return -math.inf
    return 10.0 * math.log10(var / n)


# ------------------------------------------------------------- array factor
def array_factor(
    theta_deg: np.ndarray,
    amps: np.ndarray,
    phases_deg: np.ndarray,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
) -> np.ndarray:
    """Complex array factor of a uniform linear array."""
    n = len(amps)
    idx = np.arange(n)[:, None]
    kd = 2.0 * math.pi * d_over_lambda
    theta = np.radians(np.asarray(theta_deg, dtype=float))[None, :]
    ph = np.radians(np.asarray(phases_deg, dtype=float))[:, None]
    return np.sum(np.asarray(amps, dtype=float)[:, None] * np.exp(1j * (idx * kd * np.sin(theta) + ph)), axis=0)


def _peak_on_grid(grid: np.ndarray, amps, phases_deg, d_over_lambda) -> tuple:
    mag = np.abs(array_factor(grid, amps, phases_deg, d_over_lambda))
    k = int(np.argmax(mag))
    return k, mag


def peak_direction_deg(
    amps: np.ndarray,
    phases_deg: np.ndarray,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    span_deg: float = 40.0,
    coarse_points: int = 801,
    fine_points: int = 401,
) -> float:
    """Direction of the pattern maximum.

    Coarse search, then a refined search around the coarse peak, then a
    parabolic interpolation on the refined samples. Two stages rather than one
    dense grid: it is both cheaper and more accurate, since the final step size
    is far smaller than any single grid that would fit comfortably in memory.
    """
    coarse = np.linspace(-span_deg, span_deg, coarse_points)
    k, _ = _peak_on_grid(coarse, amps, phases_deg, d_over_lambda)
    half = (coarse[1] - coarse[0]) * 1.5
    fine = np.linspace(coarse[k] - half, coarse[k] + half, fine_points)
    j, mag = _peak_on_grid(fine, amps, phases_deg, d_over_lambda)
    if 0 < j < len(fine) - 1:
        y0, y1, y2 = mag[j - 1], mag[j], mag[j + 1]
        denom = y0 - 2 * y1 + y2
        if denom != 0:
            return float(fine[j] - 0.5 * (fine[1] - fine[0]) * (y2 - y0) / denom)
    return float(fine[j])


# ---------------------------------------------------------------- Monte Carlo
@dataclass(frozen=True)
class TrialResult:
    sigma_phi_deg: float
    sigma_amp_rel: float
    pointing_std_deg: float
    pointing_std_predicted_deg: float
    gain_loss_db_mean: float
    gain_loss_db_predicted: float
    trials: int


def monte_carlo(
    sigma_phi_deg: float,
    sigma_amp_rel: float = 0.0,
    n: int = N_DEFAULT,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    trials: int = 4000,
    seed: int = 20260925,
    correlated: bool = False,
) -> TrialResult:
    """Empirical pointing spread and gain loss, against the analytic prediction.

    ``correlated`` applies one common phase error to every channel instead of
    independent ones, which is the case that should produce no pointing error at
    all.
    """
    rng = np.random.default_rng(seed)
    ideal = np.abs(array_factor(np.array([0.0]), np.ones(n), np.zeros(n), d_over_lambda))[0] ** 2

    peaks = np.empty(trials)
    gains = np.empty(trials)
    for t in range(trials):
        if correlated:
            ph = np.full(n, rng.normal(0.0, sigma_phi_deg))
        else:
            ph = rng.normal(0.0, sigma_phi_deg, n)
        amps = 1.0 + rng.normal(0.0, sigma_amp_rel, n) if sigma_amp_rel > 0 else np.ones(n)
        peaks[t] = peak_direction_deg(amps, ph, d_over_lambda)
        gains[t] = np.abs(array_factor(np.array([0.0]), amps, ph, d_over_lambda))[0] ** 2

    predicted_point = (
        0.0 if correlated
        else pointing_std_from_independent_phase_deg(sigma_phi_deg, n, d_over_lambda)
    )
    # A phase common to every channel costs no gain at all, so the correlated
    # case predicts zero for the phase term, not the independent value.
    predicted_gain = (0.0 if correlated else gain_loss_db_from_phase(sigma_phi_deg, n)) + (
        gain_loss_db_from_amplitude(sigma_amp_rel, n) if sigma_amp_rel > 0 else 0.0
    )
    return TrialResult(
        sigma_phi_deg=sigma_phi_deg,
        sigma_amp_rel=sigma_amp_rel,
        pointing_std_deg=float(np.std(peaks)),
        pointing_std_predicted_deg=float(predicted_point),
        gain_loss_db_mean=float(-10 * np.log10(np.mean(gains) / ideal)),
        gain_loss_db_predicted=float(predicted_gain),
        trials=trials,
    )


def band_edge_phase_error_deg(bit_deg: float, fractional_offset: float) -> float:
    """Phase error of a switched line bit at a frequency offset from f0.

    A switched line section is a fixed **length**, so its electrical length
    scales with frequency: a bit designed for ``bit_deg`` at f0 gives
    ``bit_deg * (1 + x)`` at a fractional offset ``x``. The error is therefore
    ``bit_deg * x``, largest for the largest bit.

    This is intrinsic to the phase shifter chosen in decision 0003 and is not a
    modelling error. Two tools modelling the same lines should both reproduce
    it, so an agreement comparison judges their **difference** across the band,
    and the intrinsic term itself is a design property, assessed in
    :func:`worst_proportional_pointing_deg`.
    """
    return bit_deg * fractional_offset


# ------------------------------------------- correlated, state dependent errors
def steering_command_deg(
    theta0_deg: float,
    n: int = N_DEFAULT,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    bits: int = PHASE_BITS_DEFAULT,
    origin_state: int = 0,
) -> np.ndarray:
    """Quantised phase command for steering to ``theta0``, wrapped into [0, 360).

    The ideal phase is ``-i k d sin(theta0)`` on element ``i``, the sign that
    points :func:`array_factor` at ``theta0``. ``origin_state`` adds a common
    offset of that many steps. That changes nothing about the ideal beam, since
    a common phase is unobservable, but it changes **which states** the channels
    use, and so what a state dependent error does to the beam.
    """
    step = quantisation_step_deg(bits)
    ideal = -np.arange(n) * 360.0 * d_over_lambda * math.sin(math.radians(theta0_deg))
    ideal = ideal + origin_state * step
    return np.mod(np.round(ideal / step) * step, 360.0)


def _peak_abs_deg(phases_deg: np.ndarray, d_over_lambda: float) -> float:
    """Pattern maximum searched over the whole scan range, not only near broadside."""
    return peak_direction_deg(
        np.ones(len(phases_deg)), phases_deg, d_over_lambda,
        span_deg=80.0, coarse_points=3201, fine_points=801,
    )


def pointing_error_proportional_deg(
    theta0_deg: float,
    fractional_error: float,
    n: int = N_DEFAULT,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    bits: int = PHASE_BITS_DEFAULT,
    origin_state: int = 0,
) -> float:
    """Beam shift caused by scaling every realised state phase by ``1 + x``.

    A switched line bit is a fixed length, so a frequency offset, or a common
    error in effective permittivity, multiplies every bit's phase by the same
    factor. A channel commanded to the wrapped state phase ``q`` realises
    ``(1 + x) q``. The error is correlated across channels and yet not common
    mode: it depends on the state, and the wrap turns it into a sawtooth rather
    than a clean ramp. Exact, on the array factor, and measured against the same
    quantised command without the error, so quantisation itself is not counted.
    """
    q = steering_command_deg(theta0_deg, n, d_over_lambda, bits, origin_state)
    return _peak_abs_deg(q * (1.0 + fractional_error), d_over_lambda) - _peak_abs_deg(
        q, d_over_lambda
    )


def worst_proportional_pointing_deg(
    theta0_deg: float,
    fractional_error: float,
    n: int = N_DEFAULT,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    bits: int = PHASE_BITS_DEFAULT,
) -> tuple[float, int]:
    """Largest :func:`pointing_error_proportional_deg` over every common origin.

    Returns the magnitude and the origin state that produced it. The origin is
    a free choice of whoever writes the steering table, so the budget has to
    hold for the worst one, not for a convenient one.
    """
    results = [
        (abs(pointing_error_proportional_deg(theta0_deg, fractional_error, n,
                                             d_over_lambda, bits, k)), k)
        for k in range(2 ** bits)
    ]
    return max(results)


def proportional_sweep(
    eta: float,
    max_deg: float = 45.0,
    step_deg: float = 0.5,
    n: int = N_DEFAULT,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    bits: int = PHASE_BITS_DEFAULT,
) -> dict:
    """Band edge dispersion over a dense steering sweep, for the worst and best origin.

    The benchmark angles are a minimum, not the only angles the array will use,
    so a statement about them alone would be a statement about four points.
    Returns the largest fraction of the pointing budget used, and where, first
    when the command origin is the worst of the eight and then when it is chosen
    per angle to be the best.
    """
    lo, hi = band_edge_offsets()
    floor = pointing_std_from_independent_phase_deg(quantisation_rms_deg(bits), n, d_over_lambda)
    worst, best, over = (0.0, 0.0), (0.0, 0.0), []
    for th0 in np.arange(0.0, max_deg + 1e-9, step_deg):
        budget = math.sqrt(eta) * floor / math.cos(math.radians(th0))
        per_origin = [
            max(abs(pointing_error_proportional_deg(th0, lo, n, d_over_lambda, bits, k)),
                abs(pointing_error_proportional_deg(th0, hi, n, d_over_lambda, bits, k))) / budget
            for k in range(2 ** bits)
        ]
        if max(per_origin) > worst[0]:
            worst = (max(per_origin), float(th0))
        if min(per_origin) > best[0]:
            best = (min(per_origin), float(th0))
        if max(per_origin) > 1.0:
            over.append(float(th0))
    return {
        "step_deg": step_deg,
        "max_deg": max_deg,
        "worst_origin": {"largest_fraction": worst[0], "at_deg": worst[1],
                         "angles_over_budget_deg": over},
        "best_origin": {"largest_fraction": best[0], "at_deg": best[1]},
    }


def worst_pattern_pointing_deg(
    bound_deg: float,
    n: int = N_DEFAULT,
    d_over_lambda: float = D_OVER_LAMBDA_DEFAULT,
    theta0_deg: float = 0.0,
) -> float:
    """Largest beam shift any per channel error pattern bounded by ``bound`` can cause.

    First order. The shift follows the least squares slope of the errors across
    the aperture, ``sum (i - mean) e_i / sum (i - mean)^2``, so the worst pattern
    puts ``-bound`` on one half of the array and ``+bound`` on the other:

        slope = bound * sum |i - mean| / sum (i - mean)^2

    That is 0.8 bound per element at four elements, against ``sigma / sqrt(5)``
    for an independent error of the same rms: a ratio of 1.79, which is the
    price of not knowing the structure of an error.
    """
    idx = np.arange(n) - (n - 1) / 2.0
    slope_deg = bound_deg * float(np.sum(np.abs(idx)) / np.sum(idx ** 2))
    kd = 2.0 * math.pi * d_over_lambda
    return math.degrees(math.radians(slope_deg) / (kd * math.cos(math.radians(theta0_deg))))


# ----------------------------------------------------------------- derivations
def state_discrimination_ceiling_deg(bits: int = PHASE_BITS_DEFAULT) -> float:
    """Half a phase step, 22.5 degrees for three bits.

    A per state error beyond it makes a state realise a phase nearer its
    neighbour than its own nominal value, so the eight states no longer come out
    in order. A hard ceiling on any state error, far above the provisional
    thresholds, and independent of any policy choice.
    """
    return quantisation_step_deg(bits) / 2.0


def floor_variance_rad2(bits: int = PHASE_BITS_DEFAULT, n: int = N_DEFAULT) -> float:
    """Expected variance of the quantisation error about the channel mean, in rad^2.

    ``(q^2 / 12) (1 - 1/n)``. This is the part of the floor that costs coherent
    gain and raises the error sidelobe floor; the part common to every channel
    costs nothing.
    """
    return math.radians(quantisation_rms_deg(bits)) ** 2 * (1.0 - 1.0 / n)


def floor_gain_loss_db(bits: int = PHASE_BITS_DEFAULT, n: int = N_DEFAULT) -> float:
    """Coherent gain the quantisation floor costs, first order: 0.167 dB for Rev A."""
    return DB_PER_NEPER_POWER * floor_variance_rad2(bits, n)


def derive_phase_agreement_deg(
    eta: float, bits: int = PHASE_BITS_DEFAULT, n: int = N_DEFAULT
) -> float:
    """Largest state dependent phase discrepancy the pointing criterion admits.

    Criterion: the shift caused by the worst pattern bounded by ``T``, squared,
    is at most ``eta`` times the pointing variance of the quantisation floor.
    Both scale with ``1 / cos(theta0)``, so the bound holds at every steering
    angle:

        T = sqrt(eta) sigma_q sqrt(sum (i - mean)^2) / sum |i - mean|

    which is ``sqrt(eta) sigma_q sqrt(5) / 4`` at four elements. Pointing, not
    gain, is the binding criterion for phase.
    """
    if not eta > 0:
        raise ValueError("eta must be positive")
    idx = np.arange(n) - (n - 1) / 2.0
    return float(
        math.sqrt(eta) * quantisation_rms_deg(bits)
        * math.sqrt(np.sum(idx ** 2)) / np.sum(np.abs(idx))
    )


def derive_amplitude_allowance_rel(
    eta: float, phase_bound_deg: float, bits: int = PHASE_BITS_DEFAULT, n: int = N_DEFAULT
) -> float:
    """Relative amplitude deviation left once the phase bound has taken its share.

    Coherent gain and the error sidelobe floor both follow the variance about
    the channel mean of phase in radians plus relative amplitude, and the worst
    pattern bounded by ``b`` has variance ``b^2``. So the joint criterion is

        m^2 = eta * floor_variance - phase_bound_rad^2

    Amplitude does not steer the beam at first order, so pointing takes no
    share of it.
    """
    left = eta * floor_variance_rad2(bits, n) - math.radians(phase_bound_deg) ** 2
    if left <= 0:
        raise ValueError("the phase bound already uses the whole gain budget")
    return math.sqrt(left)


def derive_magnitude_agreement_db(
    eta: float, phase_bound_deg: float, bits: int = PHASE_BITS_DEFAULT, n: int = N_DEFAULT
) -> float:
    """State dependent S21 magnitude discrepancy that fits the remaining budget, in dB.

    ``20 log10(1 + m)``. The upward excursion is the larger in linear terms, so
    converting with it is the conservative direction.
    """
    return 20.0 * math.log10(1.0 + derive_amplitude_allowance_rel(eta, phase_bound_deg, bits, n))


def derive_amplitude_imbalance_db(
    eta: float, phase_bound_deg: float, bits: int = PHASE_BITS_DEFAULT, n: int = N_DEFAULT
) -> float:
    """Largest peak to peak channel magnitude spread that fits the remaining budget.

    For a spread ``P``, the arrangement with the largest variance puts half the
    channels at each extreme, a relative deviation of ``(1 - r) / (1 + r)`` about
    their mean with ``r = 10^(-P/20)``. Setting that to ``m`` gives

        P = 20 log10((1 + m) / (1 - m))

    A bound on any arrangement, not on a typical one.
    """
    m = derive_amplitude_allowance_rel(eta, phase_bound_deg, bits, n)
    return 20.0 * math.log10((1.0 + m) / (1.0 - m))


def derived_values(eta: float, phase_bound_deg: float | None = None) -> dict:
    """Every derived number for one ``eta``, from one place.

    ``phase_bound_deg`` is the phase threshold as **recorded**, which may be the
    derived value rounded down; the amplitude allowances are computed from it,
    so that the recorded pair is jointly admissible rather than each alone.
    """
    t = derive_phase_agreement_deg(eta)
    tb = t if phase_bound_deg is None else phase_bound_deg
    return {
        "eta": eta,
        "phase_agreement_deg": t,
        "magnitude_agreement_db": derive_magnitude_agreement_db(eta, tb),
        "amplitude_imbalance_db": derive_amplitude_imbalance_db(eta, tb),
    }


def mean_monte_carlo(sigma_phi_deg, seeds=(1, 2, 3, 4), **kw) -> TrialResult:
    """Average :func:`monte_carlo` over several seeds.

    A single seed gives one sample of an estimate whose own scatter is a few per
    cent, and running several sigmas from one seed produces correlated rows that
    look like a systematic bias when they are not. Averaging seeds removes that
    trap.
    """
    runs = [monte_carlo(sigma_phi_deg, seed=s, **kw) for s in seeds]
    return TrialResult(
        sigma_phi_deg=sigma_phi_deg,
        sigma_amp_rel=runs[0].sigma_amp_rel,
        pointing_std_deg=float(np.mean([r.pointing_std_deg for r in runs])),
        pointing_std_predicted_deg=runs[0].pointing_std_predicted_deg,
        gain_loss_db_mean=float(np.mean([r.gain_loss_db_mean for r in runs])),
        gain_loss_db_predicted=runs[0].gain_loss_db_predicted,
        trials=sum(r.trials for r in runs),
    )



def _recorded_thresholds():
    from . import thresholds as th

    return th


def study(trials: int = 2000, eta: float | None = None) -> str:
    """The sensitivity study and the threshold derivation, as a printable report.

    Run with ``python -m rfkit.cli budget``. Deterministic: every seed is fixed,
    so two runs with the same arguments print the same text.
    """
    th = _recorded_thresholds()
    eta = th.VARIANCE_FRACTION if eta is None else eta
    n, dl = N_DEFAULT, D_OVER_LAMBDA_DEFAULT
    sq = quantisation_rms_deg()
    floor_point = pointing_std_from_independent_phase_deg(sq, n, dl)
    lo, hi = band_edge_offsets()
    out = [
        "AetherArray error budget, four elements, half wavelength spacing",
        "=" * 64,
        "",
        f"beam width at broadside          : {beamwidth_deg(n, dl):.2f} deg",
        f"phase step, {PHASE_BITS_DEFAULT} bits              : {quantisation_step_deg():.1f} deg",
        f"quantisation RMS residual        : {sq:.2f} deg",
        f"pointing error from quantisation : {floor_point:.3f} deg rms at broadside",
        f"gain loss from quantisation      : {floor_gain_loss_db():.3f} dB, four elements",
        f"error sidelobe floor             : {sidelobe_rise_db(sq, 0.0, n):.1f} dB rel peak",
        "",
        "These lines are the floor Rev A cannot beat: they follow from the three",
        "bit phase shifter fixed by decision 0003, whatever the calibration",
        "achieves. The provisional thresholds derived at the end of this report",
        "are expressed relative to them, and nothing above them is a threshold.",
        "",
        "independent per channel phase error",
        "-----------------------------------",
        "  sigma_phi   pointing std      predicted    gain loss   predicted",
        "    (deg)        (deg)            (deg)        (dB)        (dB)",
    ]
    for s in (1.0, 2.0, 5.0, 10.0, 13.0, 20.0):
        r = mean_monte_carlo(s, sigma_amp_rel=0.0, n=n, d_over_lambda=dl, trials=trials)
        out.append(
            f"   {r.sigma_phi_deg:6.1f}      {r.pointing_std_deg:8.3f}      "
            f"{r.pointing_std_predicted_deg:8.3f}    {r.gain_loss_db_mean:8.3f}    "
            f"{r.gain_loss_db_predicted:8.3f}"
        )
    out += [
        "",
        "  Each row averages four independent seeds. The gain prediction is the",
        "  finite array form; the large array limit exp(-sigma^2) would overstate",
        "  the loss by about a third at four elements.",
        "",
        "common mode phase error, same on every channel and every state",
        "--------------------------------------------------------------",
        "  sigma_phi   pointing std   (predicted exactly zero)",
    ]
    for s in (5.0, 20.0):
        r = monte_carlo(s, 0.0, n, dl, trials=max(200, trials // 4), correlated=True)
        out.append(f"   {r.sigma_phi_deg:6.1f}      {r.pointing_std_deg:10.6f}")
    out += [
        "",
        "  A phase common to all channels and all states steers nothing. It is the",
        "  unobservable common phase of the diagonal state.",
        "",
        "common proportional error, every state phase scaled by 1 + x",
        "------------------------------------------------------------",
        "  Correlated across channels, yet state dependent, so it steers. x is a",
        "  frequency offset or a common permittivity error. Worst over the eight",
        f"  possible command origins, against the pointing budget sqrt(eta) times",
        f"  the floor, eta = {eta:g}.",
        "",
        "  steering   x = %+.2f%%    x = %+.2f%%    budget    used" % (lo * 100, hi * 100),
        "    (deg)       (deg)         (deg)       (deg)",
    ]
    for th0 in STEERING_ANGLES_DEG:
        w_lo, _ = worst_proportional_pointing_deg(th0, lo, n, dl)
        w_hi, _ = worst_proportional_pointing_deg(th0, hi, n, dl)
        bud = math.sqrt(eta) * floor_point / math.cos(math.radians(th0))
        out.append(
            f"   {th0:6.1f}     {w_lo:8.3f}      {w_hi:8.3f}     {bud:7.3f}   "
            f"{max(w_lo, w_hi) / bud:5.0%}"
        )
    sweep = proportional_sweep(eta)
    w, bst = sweep["worst_origin"], sweep["best_origin"]
    out += [
        "",
        "  At f0 the term is zero by construction. At the band edges, over a sweep",
        f"  of 0 to {sweep['max_deg']:g} deg in {sweep['step_deg']:g} deg steps:",
        f"    worst command origin : up to {w['largest_fraction']:.0%} of the budget, at "
        f"{w['at_deg']:g} deg;",
        f"                           over it at {len(w['angles_over_budget_deg'])} of the "
        f"{int(sweep['max_deg'] / sweep['step_deg']) + 1} angles",
        f"    best command origin  : up to {bst['largest_fraction']:.0%}, at {bst['at_deg']:g} deg",
        "  The origin is a free choice, since a common phase is unobservable, so a",
        "  steering table that picks it per angle keeps band edge operation inside",
        "  the budget. One that does not can exceed it between the benchmark angles.",
        "",
        "amplitude imbalance, peak to peak in dB",
        "---------------------------------------",
        "  spread    sigma_rel   gain loss   error sidelobe floor",
        "   (dB)                   (dB)           (dB rel peak)",
    ]
    for spread in (0.5, 1.0, 2.0, 4.0):
        sr = relative_from_db_spread(spread)
        out.append(
            f"  {spread:6.1f}     {sr:7.4f}    {gain_loss_db_from_amplitude(sr, n):8.4f}    "
            f"{sidelobe_rise_db(0.0, sr, n):10.1f}"
        )
    out += [
        "",
        "  Amplitude error costs gain at the same rate per unit variance as phase",
        "  in radians, and does not steer the beam at first order. Phase only",
        "  control cannot correct it, so it stays in the calibrated beam.",
        "",
        "return loss and mismatch loss",
        "-----------------------------",
        "  return loss   reflected power   mismatch loss",
        "     (dB)           (fraction)         (dB)",
    ]
    for rl in (6.0, 10.0, 14.0, 20.0):
        g2 = 10 ** (-rl / 10.0)
        out.append(f"  {rl:9.1f}     {g2:12.4f}     {-10 * math.log10(1 - g2):10.3f}")
    out += [
        "",
        "  This maps a matching requirement onto a power budget. It sets none: no",
        "  return loss requirement is recorded in this repository, and between",
        "  50 ohm ports the S21 comparison already carries the effect of mismatch.",
        "",
        "in band behaviour of the switched line bits",
        "-------------------------------------------",
        "  A switched line section is a fixed length, so its phase scales with",
        "  frequency. About 2.44 GHz the fractional offset is %+.2f per cent at the"
        % (lo * 100),
        "  lower edge of band 57a and %+.2f per cent at the upper edge." % (hi * 100),
        "",
        "   bit      error at lower edge   error at upper edge",
        "  (deg)           (deg)                 (deg)",
    ]
    for bit in (45.0, 90.0, 180.0, 315.0):
        out.append(
            f"  {bit:6.0f}          {band_edge_phase_error_deg(bit, lo):8.2f}"
            f"              {band_edge_phase_error_deg(bit, hi):8.2f}"
        )
    out += [
        "",
        "  The last row is state 7, all three bits. Both simulators should",
        "  reproduce this term, so an agreement comparison judges their difference",
        "  across the band, not the term itself.",
        "",
        "the price of an unknown structure",
        "---------------------------------",
        f"  worst pattern, bound 1 deg     : {worst_pattern_pointing_deg(1.0, n, dl):.4f} deg of pointing",
        f"  independent, rms 1 deg         : {pointing_std_from_independent_phase_deg(1.0, n, dl):.4f} deg of pointing",
        f"  ratio                          : "
        f"{worst_pattern_pointing_deg(1.0, n, dl) / pointing_std_from_independent_phase_deg(1.0, n, dl):.2f}",
        "",
        "  A comparison of two traces cannot know the steering pattern its",
        "  discrepancy will meet, so the thresholds below bound the worst one.",
        "",
    ]
    out += _derivation_section(eta, th, n, dl)
    return "\n".join(out) + "\n"


def _derivation_section(eta, th, n, dl) -> list[str]:
    sq = quantisation_rms_deg()
    floor_point = pointing_std_from_independent_phase_deg(sq, n, dl)
    t_rec = th.get("s21_phase_diff_deg", th.HFSS_VS_ADS).value
    m_rec = th.get("s21_mag_diff_db", th.HFSS_VS_ADS).value
    p_rec = th.get("amplitude_imbalance_db", th.DESIGN).value
    out = [
        "provisional thresholds, decision 0007",
        "-------------------------------------",
        f"  variance fraction eta            : {eta:g}, a declared policy, not a measurement",
        f"  pointing budget                  : {math.sqrt(eta) * floor_point:.4f} deg at broadside",
        f"  gain budget                      : {eta * floor_gain_loss_db():.4f} dB",
        f"  state discrimination ceiling     : {state_discrimination_ceiling_deg():.1f} deg, hard",
        "",
        "   eta     phase agreement   magnitude agreement   amplitude imbalance",
        "             (deg)               (dB)                 (dB p-p)",
    ]
    for e in (0.05, 0.10, 0.20):
        d = derived_values(e)
        out.append(
            f"  {e:5.2f}      {d['phase_agreement_deg']:8.3f}          "
            f"{d['magnitude_agreement_db']:8.3f}             {d['amplitude_imbalance_db']:8.3f}"
        )
    out += [
        "",
        "  recorded in rfkit.thresholds, rounded down, each with its status:",
    ]
    for t in th.all_thresholds():
        val = "no value" if t.value is None else f"{t.value:g} {t.unit}"
        out.append(f"    {t.key:<26} {t.comparison:<18} {val:<12} {t.status}")
    # Exact check of the recorded values at their worst admissible patterns.
    ph = np.array([-t_rec, -t_rec, t_rec, t_rec])
    shift = abs(_peak_abs_deg(ph, dl))
    amp = 10 ** (np.array([m_rec, -m_rec, m_rec, -m_rec]) / 20.0)
    loss = gain_loss_db_exact(amp, [t_rec, -t_rec, -t_rec, t_rec])
    r = 10 ** (-p_rec / 20.0)
    loss_p = gain_loss_db_exact([1.0, 1.0, r, r], [t_rec, -t_rec, -t_rec, t_rec])
    out += [
        "",
        "  exact check at the recorded values, worst admissible patterns:",
        f"    pointing, phase pattern -T -T +T +T   : {shift:.4f} deg"
        f"  against {math.sqrt(eta) * floor_point:.4f}",
        f"    gain, phase and magnitude together    : {loss:.5f} dB"
        f"  against {eta * floor_gain_loss_db():.5f}",
        f"    gain, phase and imbalance together    : {loss_p:.5f} dB"
        f"  against {eta * floor_gain_loss_db():.5f}",
        "",
        "  Values are provisional-theory-derived. Decision 0007 fixes, before any",
        "  real HFSS, ADS or analyser data exist, the only ways they may change.",
    ]
    return out


def summary(eta: float | None = None) -> dict:
    """Machine readable version of the derivation, without the Monte Carlo.

    Cheap and deterministic, so the command line tool writes it alongside the
    report and a figure can be traced back to the numbers here.
    """
    th = _recorded_thresholds()
    eta = th.VARIANCE_FRACTION if eta is None else eta
    n, dl = N_DEFAULT, D_OVER_LAMBDA_DEFAULT
    sq = quantisation_rms_deg()
    lo, hi = band_edge_offsets()
    floor_point = pointing_std_from_independent_phase_deg(sq, n, dl)
    proportional = []
    for th0 in STEERING_ANGLES_DEG:
        w_lo, k_lo = worst_proportional_pointing_deg(th0, lo, n, dl)
        w_hi, k_hi = worst_proportional_pointing_deg(th0, hi, n, dl)
        proportional.append({
            "steering_deg": th0,
            "lower_edge": {"offset": lo, "pointing_deg": w_lo, "origin_state": k_lo},
            "upper_edge": {"offset": hi, "pointing_deg": w_hi, "origin_state": k_hi},
            "budget_deg": math.sqrt(eta) * floor_point / math.cos(math.radians(th0)),
        })
    return {
        "array": {"n": n, "d_over_lambda": dl, "bits": PHASE_BITS_DEFAULT,
                  "f0_hz": F0_HZ, "band_hz": [BAND_START_HZ, BAND_STOP_HZ],
                  "band_edge_offsets": [lo, hi]},
        "floor": {"quantisation_rms_deg": sq, "pointing_std_deg": floor_point,
                  "gain_loss_db": floor_gain_loss_db(),
                  "state_discrimination_ceiling_deg": state_discrimination_ceiling_deg()},
        "criterion": {"variance_fraction": eta,
                      "pointing_budget_deg": math.sqrt(eta) * floor_point,
                      "gain_budget_db": eta * floor_gain_loss_db()},
        "derived": derived_values(eta),
        "proportional_error": proportional,
        "proportional_sweep": proportional_sweep(eta),
        "recorded_thresholds": [t.as_dict() for t in th.all_thresholds()],
    }
