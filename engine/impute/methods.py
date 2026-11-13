"""The first four rungs of the imputation ladder, for country-year panels.

    1. LinearInterpolator    straight line between the nearest observed years
    2. LogLinearInterpolator straight line in log space (constant growth path)
    3. LogitSCurve           per-entity logit trend: an S-curve bounded to [lo, hi], for rates
    4. CohortBackcast        cohort-replacement model for attainment (Barro-Lee style)

Each is an `impute.base.Imputer`: fit(panel) / predict(where) -> ImputationResult.  None of them
draw random numbers; the deterministic characterisation is a feature, and the state-space and
multiple-imputation rungs (kalman.py, mi.py) are where uncertainty enters.
"""
import numpy as np
from scipy.special import expit

from .base import Imputer, ImputationResult, _ols_line, interpolate_series


# ---------------------------------------------------------------- 1. linear
class LinearInterpolator(Imputer):
    """Piecewise-linear interpolation between the nearest observed years in each entity.

    This is the workhorse and the baseline every other rung is scored against.  Interior cells
    are exact on a series that is exactly linear in the year coordinate (to floating point);
    beyond the observed span the default is to hold the nearest observation ('hold'), which is
    honest and never extrapolates a trend.  Use extrapolate='linear' for a continued end slope,
    or 'none' to leave the ends missing.
    """

    name = 'linear'

    def __init__(self, extrapolate='hold'):
        super().__init__()
        if extrapolate not in ('hold', 'none', 'linear'):
            raise ValueError("extrapolate must be 'hold', 'none' or 'linear'")
        self.extrapolate = extrapolate

    def _fit(self, panel):
        self._filled = np.full(self.shape, np.nan)
        for i in range(self.n_entities):
            row = np.where(self.obs[i], panel.values[i], np.nan)
            out, _ = interpolate_series(self.years, row, self.obs[i], 'identity', self.extrapolate)
            self._filled[i] = out

    def _predict(self, where):
        values = np.where(where, self._filled, np.nan)
        return ImputationResult(values, where, method=self.name)


# ---------------------------------------------------------------- 2. log-linear
class LogLinearInterpolator(LinearInterpolator):
    """Interpolate in log space: a constant proportional growth path between anchors.

    Exact on a series that is exponential in the year coordinate while both bracketing anchors are
    positive.  Segments with a non-positive endpoint fall back to linear interpolation on that
    segment (recorded in the class docstring, not silently).  Prediction stays positive on
    positive segments, which is what one wants for GDP, population and counts.
    """

    name = 'loglinear'

    def _fit(self, panel):
        self._filled = np.full(self.shape, np.nan)
        for i in range(self.n_entities):
            row = np.where(self.obs[i], panel.values[i], np.nan)
            out, _ = interpolate_series(self.years, row, self.obs[i], 'log', self.extrapolate)
            self._filled[i] = out


# ---------------------------------------------------------------- 3. logit S-curve
class LogitSCurve(Imputer):
    """Per-entity logit-linear trend, bounded to [lower, upper]; the rate/S-curve rung.

    For a bounded indicator (a percentage, a participation rate) a straight line can leave the
    admissible range and a log line cannot handle the ceilings.  This method maps the level onto
    the unit interval, p = (y - lo) / (hi - lo), takes z = logit(p), and fits an OLS trend
    z = a + b * year on the entity's observations.  The prediction is the inverse logit of the
    trend, so by construction `lower <= prediction <= upper` for every year, including outside the
    observed span.  The logistic S-curve is exactly a straight line in logit space, so an exactly
    logistic series is recovered exactly (up to the clipping epsilon used on observations at the
    bounds).

    The fit is a trend, not a local interpolation: it borrows the whole history of the entity,
    which is why the hold-out report shows it can beat linear interpolation on long gaps in
    smoothly saturating series but not necessarily on short gaps.
    """

    name = 'scurve'

    def __init__(self, lower=0.0, upper=100.0, clip=1e-4):
        super().__init__()
        if not np.isfinite(lower) or not np.isfinite(upper) or upper <= lower:
            raise ValueError('need finite bounds with upper > lower')
        if not 0 < clip < 0.5:
            raise ValueError('clip must be in (0, 0.5)')
        self.lower = float(lower)
        self.upper = float(upper)
        self.clip = float(clip)

    def _fit(self, panel):
        n = self.n_entities
        self._a = np.full(n, np.nan)
        self._b = np.full(n, np.nan)
        self._fallback = np.full(n, np.nan)
        self._x0 = float(np.mean(self.years))
        x_all = self.years - self._x0
        span = self.upper - self.lower
        for i in range(n):
            idx = np.flatnonzero(self.obs[i])
            if idx.size == 0:
                continue
            y = panel.values[i, idx]
            p = np.clip((y - self.lower) / span, self.clip, 1.0 - self.clip)
            z = np.log(p / (1.0 - p))
            a, b = _ols_line(x_all[idx], z)
            self._a[i], self._b[i] = a, b
            if idx.size == 1:
                self._fallback[i] = float(np.clip(y[0], self.lower, self.upper))

    def _predict(self, where):
        x = self.years - self._x0
        z = self._a[:, None] + self._b[:, None] * x[None, :]
        p = expit(z)                          # stable in (0, 1) even for huge |z|
        values = self.lower + (self.upper - self.lower) * p
        values = np.clip(values, self.lower, self.upper)
        single = np.isfinite(self._fallback)
        values[single] = self._fallback[single, None]
        values = np.where(where, values, np.nan)
        return ImputationResult(values, where, method=self.name)


# ---------------------------------------------------------------- 4. cohort back-casting
class CohortBackcast(Imputer):
    """Cohort-replacement model for attainment (mean years of schooling of the adult population).

    The idea.  Adult mean schooling S barely moves with anything that happens to adults; it moves
    by cohort replacement.  Let E(t) be the schooling of the cohort that turns adult at t and let
    L be the average length of adult life over which cohorts are replaced.  The discrete
    replacement identity used here is

        S(t + d) = (1 - a_d) * S(t) + a_d * E,      a_d = 1 - (1 - 1/L)^d      (1)

    with d the spacing between panel years (1 for annual data, 5 for Barro-Lee waves).  Inverting
    (1) between adjacent observed years recovers the entering cohort, placed at the geometric-time
    centre of the interval (the constant-E equivalent of the pair):

        E = (S(t + d) - r^d * S(t)) / (1 - r^d),    r = 1 - 1/L                (2)

    Fit: recover E from every pair of adjacent observed years (2), placing it at the
    geometric-time centre of the pair, then interpolate E linearly in time between those nodes and
    hold it at the ends.
    Predict: integrate (1) forward from the last observed year before a gap and backward by
    inverting (1) from the first observed year after it, and blend the two by the distance to the
    anchors.  Years before the first observation are back-cast by inverting (1) with E held at its
    earliest recovered value; years after the last are projected forward the same way.

    The recovered E(t) series is itself the useful object -- each node is a cohort's attainment
    derived from the observed aggregate means on either side of it, i.e. from the earlier and
    later cohorts in the panel -- and cohort_attainment() exposes it.  predict() then integrates
    the cohort series back into the adult mean, which is what fills a gap or back-casts earlier
    years while respecting that adults already in the population keep their schooling.

    This is a documented approximation of a cohort-accounting model on aggregate attainment data:
    the repo's Barro-Lee file carries the adult mean only, not attainment by age cohort, so the
    cohort structure enters through the replacement horizon L.  L=40 is the Barro-Lee round number
    for the length of adult working life; pass replacement_years= to vary it.

    An exactly cohort-generated series (1) with linear E(t) is recovered to floating point.
    """

    name = 'cohort'

    def __init__(self, replacement_years=40.0, max_pair_years=None):
        super().__init__()
        if not np.isfinite(replacement_years) or replacement_years <= 1.0:
            raise ValueError('replacement_years must be finite and > 1')
        if max_pair_years is not None and (not np.isfinite(max_pair_years) or max_pair_years <= 0):
            raise ValueError('max_pair_years must be None or a positive number of years')
        self.replacement_years = float(replacement_years)
        # Every pair of adjacent observed nodes recovers one cohort level E.  A pair spanning a
        # gap is still informative: its constant-E equivalent is the cohort level at the weighted
        # centre of the interval, so it anchors E inside the gap.  Set max_pair_years=w to ignore
        # pairs spanning more than w years (e.g. w=5 keeps only unbroken Barro-Lee waves).
        self.max_pair_years = np.inf if max_pair_years is None else float(max_pair_years)

    # -- fit ----------------------------------------------------------------
    def _fit(self, panel):
        n, T = self.shape
        self._filled = np.full((n, T), np.nan)
        self._nodes = [None] * n
        years = self.years
        L = self.replacement_years
        max_pair = self.max_pair_years
        for i in range(n):
            obs = np.flatnonzero(self.obs[i])
            if obs.size == 0:
                continue
            # only trusted observations enter the cohort identity; derived ('d') cells are not
            # anchors even if they carry a number
            s = np.where(self.obs[i], panel.values[i], np.nan)
            if obs.size == 1:
                e_years = np.array([years[obs[0]]])
                e_vals = np.array([s[obs[0]]])
            else:
                # Recover the entering cohort E on each pair of adjacent observed nodes.  Over a
                # step of d years with E held constant, the replacement identity gives
                #     S(t+d) = r^d S(t) + (1 - r^d) E,        r = 1 - 1/L,
                # so E = (S(t+d) - r^d S(t)) / (1 - r^d).  That constant-E equivalent sits at the
                # geometric-time centre of the interval (_centre_offset), where the node is placed;
                # with a linear E(t) this makes the interpolation below exact.  Pairing across a gap
                # (large d) therefore still yields the cohort level near the middle of the gap,
                # which is the best an aggregate series can say from the two ends.
                e_years, e_vals = [], []
                for a, b in zip(obs[:-1], obs[1:]):
                    d = years[b] - years[a]
                    if d > max_pair:
                        continue        # optional: ignore pairs spanning more than max_pair years
                    share = 1.0 - (1.0 - 1.0 / L) ** d
                    centre = CohortBackcast._centre_offset(d, L)
                    e_years.append(years[a] + centre)
                    e_vals.append((s[b] - (1.0 - share) * s[a]) / share)   # equation (2)
                if not e_years:         # no unbroken adjacent pair: hold E at the latest value
                    e_years = [float(years[obs[-1]])]
                    e_vals = [float(s[obs[-1]])]
                e_years = np.asarray(e_years)
                e_vals = np.asarray(e_vals)
            self._nodes[i] = (np.asarray(e_years, float), np.asarray(e_vals, float))
            self._filled[i] = self._fill_entity(years, s, obs, e_years, e_vals, L)

    def cohort_attainment(self):
        """The entering-cohort attainment series recovered from the aggregate data.

        Returns {entity: (node_years, attainment)} where node j is the schooling of the cohort
        entering adult life at node_years[j], recovered from the change between the two adjacent
        observed aggregate means (equation 2) and placed at the geometric centre of that pair.
        This is the "derive a cohort's attainment from the observed (older and younger) cohorts"
        step made explicit; predict() integrates it back into the adult mean.
        """
        if not self._fitted:
            raise RuntimeError('cohort: call fit() first')
        return {e: (self._nodes[i][0].copy(), self._nodes[i][1].copy())
                for i, e in enumerate(self.entities) if self._nodes[i] is not None}

    # -- the disaggregated cohort recursion ---------------------------------
    @staticmethod
    def _centre_offset(d, L):
        """Where in an interval of d years the constant-E equivalent of E(t) sits, in years after
        the left node.  For a linear E(t) this is exactly the year whose E reproduces the change:
        the weights are w_k=(1-r) r^(d-k), so the offset is their time centre (1 for d=1, ~3.06 for
        d=5 at L=40).  Used both to place the recovered nodes and to evaluate the E inside a step.
        """
        r = 1.0 - 1.0 / L
        k = np.arange(1.0, d + 1.0)
        w = (1.0 - r) * r ** (d - k)
        return float(np.dot(k, w) / np.sum(w))

    @staticmethod
    def _e_at(x, e_years, e_vals):
        """Entering-cohort attainment at year x: linear in time between recovered nodes, held at ends."""
        return np.interp(x, e_years, e_vals)

    @classmethod
    def _fill_entity(cls, years, s, obs, e_years, e_vals, L):
        T = len(years)
        out = np.full(T, np.nan)
        out[obs] = s[obs]
        first, last = int(obs[0]), int(obs[-1])
        forward = np.full(T, np.nan)
        backward = np.full(T, np.nan)
        e = lambda x: cls._e_at(x, e_years, e_vals)

        # forward = integrate equation (1) from the last observation at or before each cell
        state = s[first]
        forward[first] = state
        for t in range(first + 1, T):
            if np.isfinite(s[t]):
                state = s[t]
                forward[t] = state
                continue
            d = years[t] - years[t - 1]
            a = 1.0 - (1.0 - 1.0 / L) ** d
            state = (1.0 - a) * state + a * e(years[t - 1] + cls._centre_offset(d, L))
            forward[t] = state

        # backward = invert equation (1), anchored on the next observation to the right
        backward[last] = s[last]
        state = s[last]
        for t in range(last - 1, -1, -1):
            if np.isfinite(s[t]):
                state = s[t]
                backward[t] = state
                continue
            d = years[t + 1] - years[t]
            a = min(1.0 - (1.0 - 1.0 / L) ** d, 1.0 - 1e-9)
            state = (state - a * e(years[t] + cls._centre_offset(d, L))) / (1.0 - a)
            backward[t] = state

        # blend: between two observed anchors weight by the distance in years to each; outside the
        # observed span use the one-sided (back-cast / projection) recursion.
        anchors = obs
        for t in np.flatnonzero(~np.isfinite(out)):
            j = np.searchsorted(anchors, t)
            if j == 0:                       # before the first observation: back-cast only
                out[t] = backward[t]
            elif j == anchors.size:          # after the last: project only
                out[t] = forward[t]
            else:
                left, right = anchors[j - 1], anchors[j]
                w = (years[t] - years[left]) / (years[right] - years[left]) if years[right] > years[left] else 0.5
                out[t] = (1.0 - w) * forward[t] + w * backward[t]
        return out

    def _predict(self, where):
        values = np.where(where, self._filled, np.nan)
        return ImputationResult(values, where, method=self.name)
