"""The fit/predict contract shared by every imputation method, and small numeric helpers.

Every method in the ladder is an `Imputer`:

    imp = LinearInterpolator().fit(panel)       # fit on the panel's trusted observations
    res = imp.predict()                         # fill every cell that is not an observation
    filled = panel.with_fill(res)               # new ProvenancePanel, filled cells flagged 'd'

`predict(where=...)` fills an arbitrary boolean mask (this is what the hold-out harness uses to
fill only the cells it deleted).  Results carry, when the method provides them, `lower`/`upper`
interval bounds and/or `draws` (multiple-imputation draws).  All methods are deterministic:
every method that draws random numbers takes an explicit seed.

A method fits only on cells with flag 'v' or 'm' by default (`use_flags=`); cells flagged 'd'
are derived and are never treated as observations.  The hold-out harness scores only 'v' cells
by default, so a result is never graded against a number we ourselves imputed.
"""
import copy

import numpy as np

from .panel import OBSERVED_FLAGS, ProvenancePanel


# ---------------------------------------------------------------- panel-level helpers
def interpolate_series(years, values, observed, transform='identity', extrapolate='hold'):
    """Fill one entity's series at the panel's year coordinates.

    Parameters
    ----------
    years : (T,) float array
    values : (T,) float array, NaN where not observed
    observed : (T,) bool array
    transform : 'identity' or 'log'
        'log' interpolates log(y); a segment whose endpoints are not both positive falls back to
        linear interpolation on that segment (documented, deterministic, never raises).
    extrapolate : 'hold' | 'none' | 'linear'
        'hold' (default) repeats the nearest observation beyond the observed span; 'none' leaves
        those cells NaN; 'linear' continues the end segment's (transformed) slope.

    Returns the filled array and the mask of cells that received a finite value.
    """
    x = np.asarray(years, dtype=float)
    y = np.asarray(values, dtype=float)
    obs = np.asarray(observed, bool) & np.isfinite(y)
    out = np.full(x.shape, np.nan)
    idx = np.flatnonzero(obs)
    if idx.size == 0:
        return out, np.zeros(x.shape, bool)
    xo, yo = x[idx], y[idx]
    if idx.size == 1:
        out[:] = yo[0]
        return out, np.isfinite(out)
    if transform not in ('identity', 'log'):
        raise ValueError(f"unknown transform {transform!r}; use 'identity' or 'log'")
    if extrapolate not in ('hold', 'none', 'linear'):
        raise ValueError(f"unknown extrapolate {extrapolate!r}; use 'hold', 'none' or 'linear'")
    if transform == 'log' and np.any(yo <= 0):
        # log interpolation is undefined for zero/negative endpoints; keep the series safe by
        # treating non-positive anchors as identity anchors segment by segment (see below).
        pass

    right = np.searchsorted(xo, x, side='left')       # first anchor with xo >= x
    left = right - 1
    inside = (right < xo.size) & (left >= 0)          # bracketed by two anchors
    if inside.any():
        xl, xr = xo[left[inside]], xo[right[inside]]
        yl, yr = yo[left[inside]], yo[right[inside]]
        t = (x[inside] - xl) / (xr - xl)
        if transform == 'log':
            ok = (yl > 0) & (yr > 0)
            zl, zr = np.log(np.where(ok, yl, 1.0)), np.log(np.where(ok, yr, 1.0))
            log_fill = np.exp(zl + t * (zr - zl))
            lin_fill = yl + t * (yr - yl)
            out[inside] = np.where(ok, log_fill, lin_fill)
        else:
            out[inside] = yl + t * (yr - yl)

    if extrapolate == 'hold':
        out[:left[0] + 1] = yo[0] if left[0] >= 0 else np.nan
        out[right[-1]:] = yo[-1]
    elif extrapolate == 'linear':
        t_left = np.arange(left[0] + 1) if left[0] >= 0 else np.array([], float)
        if t_left.size:
            if transform == 'log' and yo[0] > 0 and yo[1] > 0:
                slope = (np.log(yo[1]) - np.log(yo[0])) / (xo[1] - xo[0])
                out[:t_left.size] = np.exp(np.log(yo[0]) + slope * (x[:t_left.size] - xo[0]))
            else:
                slope = (yo[1] - yo[0]) / (xo[1] - xo[0])
                out[:t_left.size] = yo[0] + slope * (x[:t_left.size] - xo[0])
        n_right = xo.size - 1 - right[-1]
        if n_right > 0:
            n = xo.size
            if transform == 'log' and yo[-1] > 0 and yo[-2] > 0:
                slope = (np.log(yo[-1]) - np.log(yo[-2])) / (xo[-1] - xo[-2])
                out[right[-1]:] = np.exp(np.log(yo[-1]) + slope * (x[right[-1]:] - xo[-1]))
            else:
                slope = (yo[-1] - yo[-2]) / (xo[-1] - xo[-2])
                out[right[-1]:] = yo[-1] + slope * (x[right[-1]:] - xo[-1])
    return out, np.isfinite(out)


def _ols_line(x, y):
    """Least-squares line y = a + b x, returned as (a, b).  Deterministic, no exceptions."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size == 0:
        return float('nan'), float('nan')
    if x.size == 1 or np.ptp(x) == 0:
        return float(y.mean()), 0.0
    xm, ym = x.mean(), y.mean()
    b = float(np.sum((x - xm) * (y - ym)) / np.sum((x - xm) ** 2))
    return float(ym - b * xm), b


# ---------------------------------------------------------------- result object
class ImputationResult:
    """The output of `Imputer.predict`: values only at the requested cells, plus optional intervals.

    Attributes
    ----------
    values : (n_entities, n_years) float
        Finite only where a cell was filled (the requested `where` mask); NaN elsewhere.
    where : (n_entities, n_years) bool
        Cells that were requested.
    method : str
        Name of the method that produced the values (stored on derived cells in panel history).
    lower, upper : arrays or None
        Interval bounds for the methods that provide intervals.
    draws : (M, n_entities, n_years) float or None
        Multiple-imputation draws for the methods that provide them.
    nominal : float or None
        Nominal coverage of [lower, upper], e.g. 0.90.
    """

    __slots__ = ('values', 'where', 'method', 'lower', 'upper', 'draws', 'nominal')

    def __init__(self, values, where, method='', lower=None, upper=None, draws=None, nominal=None):
        values = np.asarray(values, dtype=float)
        where = np.asarray(where, bool)
        if values.shape != where.shape:
            raise ValueError(f'values shape {values.shape} != where shape {where.shape}')
        if np.isinf(values).any():
            raise ValueError('imputed values must be finite or NaN, not +/-inf')
        self.values = values
        self.where = where
        self.method = str(method)
        self.lower = None if lower is None else np.asarray(lower, dtype=float)
        self.upper = None if upper is None else np.asarray(upper, dtype=float)
        if self.lower is not None or self.upper is not None:
            if self.lower is None or self.upper is None:
                raise ValueError('provide both lower and upper, or neither')
            if self.lower.shape != values.shape or self.upper.shape != values.shape:
                raise ValueError('interval bounds must match the values shape')
        self.draws = None if draws is None else np.asarray(draws, dtype=float)
        if self.draws is not None and (self.draws.ndim != 3 or self.draws.shape[1:] != values.shape):
            raise ValueError('draws must have shape (M, n_entities, n_years)')
        self.nominal = None if nominal is None else float(nominal)

    @property
    def filled(self):
        """Mask of cells that actually received a finite value."""
        return self.where & np.isfinite(self.values)

    @property
    def n_filled(self):
        return int(self.filled.sum())

    @property
    def has_intervals(self):
        return self.lower is not None

    def coverage(self, truth):
        """Share of finite truth values inside [lower, upper], over filled cells.

        Returns NaN for methods without intervals.  This is the number the hold-out harness
        compares with `nominal`.
        """
        if self.lower is None:
            return float('nan')
        truth = np.asarray(truth, dtype=float)
        m = self.filled & np.isfinite(truth)
        if not m.any():
            return float('nan')
        return float(np.mean((self.lower[m] <= truth[m]) & (truth[m] <= self.upper[m])))

    def width(self):
        """Mean interval width over filled cells, or NaN without intervals."""
        if self.lower is None:
            return float('nan')
        m = self.filled
        return float(np.mean(self.upper[m] - self.lower[m])) if m.any() else float('nan')

    def __repr__(self):
        extra = ''
        if self.lower is not None:
            extra += f', {100 * self.nominal:.0f}% intervals' if self.nominal is not None else ', intervals'
        if self.draws is not None:
            extra += f', {self.draws.shape[0]} draws'
        return f'ImputationResult({self.method}: {self.n_filled} filled{extra})'


# ---------------------------------------------------------------- the imputer base class
class Imputer:
    """Base class for the imputation ladder.  Subclasses implement `_predict(where)`."""

    name = 'imputer'
    provides_intervals = False
    provides_draws = False

    def __init__(self):
        self._fitted = False
        self.entities = None
        self.years = None
        self.shape = None
        self.use_flags = OBSERVED_FLAGS
        self.obs = None                     # trusted observation mask (fit data)

    # -- fit / predict -------------------------------------------------------
    def fit(self, panel, use_flags=OBSERVED_FLAGS):
        """Store the panel geometry and its trusted observations.  Returns self."""
        if not isinstance(panel, ProvenancePanel):
            raise TypeError(f'fit expects a ProvenancePanel, got {type(panel).__name__}')
        self.entities = list(panel.entities)
        self.years = panel.years.copy()
        self.shape = panel.shape
        self.use_flags = ProvenancePanel._check_flags(use_flags)
        self.obs = panel.observed(self.use_flags)
        self._fitted = True
        self._fit(panel)
        return self

    def _fit(self, panel):
        """Hook for subclasses after the bookkeeping is done."""

    def fit_predict(self, panel, where=None, use_flags=OBSERVED_FLAGS):
        return self.fit(panel, use_flags).predict(where)

    def predict(self, where=None):
        """Fill the cells selected by `where` (default: every non-observation cell)."""
        if not self._fitted:
            raise RuntimeError(f'{self.name}: call fit() before predict()')
        where = self._check_where(where)
        return self._predict(where)

    def _check_where(self, where):
        if where is None:
            return ~self.obs
        where = np.asarray(where, bool)
        if where.shape != self.shape:
            raise ValueError(f'where shape {where.shape} != panel shape {self.shape}')
        return where

    def _predict(self, where):
        raise NotImplementedError

    # -- utilities -----------------------------------------------------------
    def clone(self):
        """An unfitted copy with the same configuration (the harness refits per replicate)."""
        return copy.deepcopy(self)

    def _empty_result(self, where, values=None, **kw):
        if values is None:
            values = np.full(self.shape, np.nan)
        return ImputationResult(values, where, method=self.name, **kw)


# ---------------------------------------------------------------- module-level convenience
def impute_panel(panel, imputer, use_flags=OBSERVED_FLAGS, where=None, overwrite=False, clone=True):
    """Fit `imputer` on `panel` and return a new panel with the non-observed cells filled as 'd'."""
    imp = imputer.clone() if clone else imputer
    res = imp.fit(panel, use_flags=use_flags).predict(where)
    return panel.with_fill(res, overwrite=overwrite)


def method_names():
    """Names of the full ladder, in the order the docs describe it."""
    from .methods import CohortBackcast, LinearInterpolator, LogLinearInterpolator, LogitSCurve
    from .kalman import KalmanSmoother
    from .mi import AmeliaMI
    return [LinearInterpolator.name, LogLinearInterpolator.name, LogitSCurve.name,
            CohortBackcast.name, KalmanSmoother.name, AmeliaMI.name]


def make_imputer(name, **kw):
    """Construct a method from its ladder name (used by the report and by the harness)."""
    from .methods import CohortBackcast, LinearInterpolator, LogLinearInterpolator, LogitSCurve
    from .kalman import KalmanSmoother
    from .mi import AmeliaMI
    registry = {
        LinearInterpolator.name: LinearInterpolator,
        LogLinearInterpolator.name: LogLinearInterpolator,
        LogitSCurve.name: LogitSCurve,
        CohortBackcast.name: CohortBackcast,
        KalmanSmoother.name: KalmanSmoother,
        AmeliaMI.name: AmeliaMI,
    }
    if name not in registry:
        raise KeyError(f'unknown imputation method {name!r}; known: {sorted(registry)}')
    return registry[name](**kw)
