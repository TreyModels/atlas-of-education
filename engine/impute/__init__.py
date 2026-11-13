"""engine.impute -- the Atlas imputation system.

A provenance-carrying country-year panel and a ladder of imputation methods, with a hold-out
harness that scores them by method and gap length.

Provenance (panel.py)
    ProvenancePanel    values + per-cell flags: 'v' verified, 'm' memory, 'd' derived, '' missing
    from_long          build a panel from {entity, year, value, flag} records
    Methods fit on ('v', 'm') by default; derived 'd' values are never treated as observations.

The ladder (fit(panel) / predict(where) -> ImputationResult)
    1. LinearInterpolator      straight line between nearest observed years          (methods.py)
    2. LogLinearInterpolator   constant proportional-growth path                    (methods.py)
    3. LogitSCurve             per-entity logit trend bounded to [lo, hi], for rates (methods.py)
    4. CohortBackcast          cohort-replacement identity for attainment            (methods.py)
    5. KalmanSmoother          local linear trend, RTS smoother, predictive intervals (kalman.py)
    6. AmeliaMI                chained equations across countries, M draws, Rubin pooling (mi.py)

Scoring (harness.py)
    holdout(panel, methods=..., gap_lengths=(1,2,3,5,10)) deletes observed cells in blocks,
    refits every method on the damaged panel, and returns a HoldoutReport with MAE/RMSE/bias by
    method x gap length plus interval coverage.

Real data (data.py, pandas only at the loading boundary)
    load_pwt, load_attainment, load_barro_lee, load_ilostat, load_learning_scores.

Run the B11-style validation report with:   python -m engine.impute
"""
from .base import (Imputer, ImputationResult, impute_panel, interpolate_series, make_imputer,
                   method_names)
from .harness import DEFAULT_GAP_LENGTHS, HoldoutReport, damage, holdout, make_deletions
from .kalman import KalmanSmoother
from .methods import CohortBackcast, LinearInterpolator, LogLinearInterpolator, LogitSCurve
from .mi import AmeliaMI
from .panel import (DERIVED, MEMORY, MISSING, OBSERVED_FLAGS, TRUSTED, VERIFIED, ProvenancePanel,
                    from_long)

__version__ = '1.0'

__all__ = [
    # provenance
    'ProvenancePanel', 'from_long', 'VERIFIED', 'MEMORY', 'DERIVED', 'MISSING',
    'OBSERVED_FLAGS', 'TRUSTED',
    # api
    'Imputer', 'ImputationResult', 'impute_panel', 'interpolate_series', 'make_imputer',
    'method_names',
    # ladder
    'LinearInterpolator', 'LogLinearInterpolator', 'LogitSCurve', 'CohortBackcast',
    'KalmanSmoother', 'AmeliaMI',
    # scoring
    'holdout', 'make_deletions', 'damage', 'HoldoutReport', 'DEFAULT_GAP_LENGTHS',
    '__version__',
]
