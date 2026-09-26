"""rfkit: the shared RF data layer for AetherArray.

One path from every source of S parameters into one set of objects:

    HFSS  ---.
    ADS   ---+--> Touchstone --> skrf.Network --> RfTrace --> metrics, comparison,
    VNA   ---'                                               array state, dataset

Design rules, each of which exists because of something in the repository:

- A trace without provenance is not accepted. ``results/README.md`` says a
  measurement without metadata is lost.
- Traces are compared only over the frequency range they share, and never
  extrapolated. See ``rfkit.grid``.
- Phase differences are taken on the circle, so 359 against 1 is 2 degrees.
  See ``rfkit.metrics.phase_error_deg``.
- No threshold is invented. A limit is derived from its array level
  consequence in ``rfkit.budget``, recorded with its source and marked
  provisional, or it has no value and every verdict against it reads
  ``unresolved``. See ``rfkit.thresholds`` and decision 0007.
- No calibration is claimed until standards exist. See ``rfkit.calibration``.
- Raw values are preserved. Processed outputs are regenerable from raw plus
  configuration, which is the ``results/`` convention.

Run the tests with::

    cd tools && python -m pytest rfkit/tests -q
"""
from __future__ import annotations

from .calibration import CalibrationNotAvailable, CalibrationPlan, apply_calibration, deembed
from .compare import (
    ComparisonReport,
    PairComparison,
    StateComparison,
    compare_all,
    compare_pair,
    compare_states,
)
from .dataset import Measurement, MeasurementSet, read_dataset, write_dataset
from .grid import Band, NoCommonBand, OutOfBand, align, common_band, common_grid
from .io import RfTrace, load_directory, load_touchstone, synthetic_trace
from .metrics import (
    amplitude_imbalance_db,
    extract_at,
    extract_band,
    mag_db,
    phase_error_deg,
    phase_spread_deg,
    unwrapped_phase_deg,
    wrap_deg,
)
from .provenance import Provenance, dump_provenance
from .state import ArrayState, state_from_channel_traces, state_from_full_matrix
from .thresholds import THRESHOLDS, Threshold, unresolved_keys

__version__ = "0.1.0"

__all__ = [
    "ArrayState", "Band", "CalibrationNotAvailable", "CalibrationPlan",
    "ComparisonReport", "Measurement", "MeasurementSet", "NoCommonBand",
    "OutOfBand", "PairComparison", "Provenance", "RfTrace", "StateComparison",
    "THRESHOLDS", "Threshold", "align", "amplitude_imbalance_db", "apply_calibration",
    "common_band", "common_grid", "compare_all", "compare_pair", "compare_states", "deembed",
    "dump_provenance", "extract_at", "extract_band", "load_directory",
    "load_touchstone", "mag_db", "phase_error_deg", "phase_spread_deg",
    "read_dataset", "state_from_channel_traces", "state_from_full_matrix",
    "synthetic_trace", "unresolved_keys", "unwrapped_phase_deg", "wrap_deg",
    "write_dataset", "__version__",
]
