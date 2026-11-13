"""Rung 6: Amelia-style multiple imputation across countries, by transparent chained equations.

When one country's cell is missing, the rest of the panel still says something about it: other
countries tell us about the common year (a world recession, a survey round), and the country's
own neighbours tell us about its persistent deviation from the world.  This rung combines both in
a documented, auditable approximation of the Amelia multiple-imputation workflow.

Model.  Work with the country's deviation from the world that year,

    z(i,t) = y(i,t) - year_mean(-i,t),

where year_mean(-i,t) is the mean of the OTHER countries' trusted observations in year t (so the
year effect can never be contaminated by the value being imputed).  Then a pooled regression

    z(i,t) = a + b1 z(i,t-1) + b2 z(i,t-2) + c * own_dev_mean(i) + e

is fitted over the trusted observations; lags use the current completed panel, so chained
equations propagate information into the gaps.  own_dev_mean(i) is the country's average deviation
over its trusted years and carries its persistent level.

Chained equations.  Start from linear interpolation per country; fit; refill every non-observed
cell in year order (so a filled lag informs the next year); repeat `iterations` times (default 3).
This is chained equations on a single variable with lagged and cross-sectional structure -- the
same pattern Amelia implements for one variable, without Amelia's EM start or its full joint
posterior.  It is deliberately transparent: every coefficient is inspectable.

Multiple draws and pooling.  For m = 1..M:
    sigma2_m ~ scaled inverse chi-square(dof),
    beta_m   ~ N(beta_hat, sigma2_m (X'X)^-1),
    refill in year order with    y = year_mean(-i,t) + x beta_m + N(0, sigma2_m).
M = 20 draws by default, with an explicit seed, so the whole rung is deterministic.  Rubin's rule
with the between-draw variance gives the point estimate and interval:
    point = mean of the M draws,
    T     = (1 + 1/M) * Var(draws, ddof=1),
    interval = point +/- z sqrt(T).
The draws carry both parameter and residual uncertainty; the (1 + 1/M) factor corrects for finite M.
Coverage is only as honest as the model: with a misspecified regression the intervals can be too
narrow.  That is a documented limitation of this rung, reported by the hold-out harness rather
than hidden.

In the hold-out report this rung is not expected to beat univariate interpolation on point error
for every series; its job is to borrow cross-country structure and to carry multiple draws and
Rubin intervals rather than a single number.
"""
import numpy as np

from .base import Imputer, ImputationResult, interpolate_series

_N_FEATURES = 4    # const, z lag 1, z lag 2, the country's own mean deviation


class AmeliaMI(Imputer):
    """Chained-equations multiple imputation with a cross-country year factor and Rubin pooling."""

    name = 'amelia'
    provides_intervals = True
    provides_draws = True

    def __init__(self, draws=20, iterations=3, coverage=0.90, seed=0, ridge=1e-8):
        super().__init__()
        if int(draws) < 2:
            raise ValueError('draws must be >= 2 for a between-draw variance')
        if int(iterations) < 0:
            raise ValueError('iterations must be >= 0')
        if not 0.0 < coverage < 1.0:
            raise ValueError('coverage must be in (0, 1)')
        self.draws_n = int(draws)
        self.iterations = int(iterations)
        self.coverage = float(coverage)
        self.seed = int(seed)
        self.ridge = float(ridge)

    # ------------------------------------------------------------ fit
    def _fit(self, panel):
        n, T = self.shape
        Yobs = np.where(self.obs, panel.values, np.nan)
        finite = np.isfinite(Yobs)
        if not finite.any():
            raise ValueError('AmeliaMI needs at least one observation')
        self._global_mean = float(np.nanmean(Yobs))
        self._Yobs = Yobs
        self._year_mean = self._year_cross_means(Yobs, self._global_mean)
        # own mean deviation, from trusted years only; fall back to the world (zero deviation)
        dev = np.where(finite, Yobs - self._year_mean, np.nan)
        own_dev = np.nanmean(dev, axis=1)
        self._own_dev = np.where(np.isfinite(own_dev), own_dev, 0.0)

        Y = self._initial_fill()
        for _ in range(self.iterations):
            beta, sigma2, xtx_inv, dof = self._estimate(Y)
            Y = self._fill_point(Y, beta)
        self._chained_fill = Y
        self._beta, self._sigma2, self._xtx_inv, self._dof = self._estimate(Y)
        self._draws = self._multiple_draws(Y)

        draws = self._draws
        M = draws.shape[0]
        mean = draws.mean(axis=0)
        between = draws.var(axis=0, ddof=1)
        self._values = np.where(self.obs, Yobs, mean)
        self._var = np.maximum((1.0 + 1.0 / M) * between, 1e-12)
        from scipy.stats import norm
        self._z = float(norm.ppf(0.5 + 0.5 * self.coverage))

    # ------------------------------------------------------------ cross-section
    def _year_cross_means(self, Yobs, fallback):
        """Mean of the other countries' trusted observations in each year, (n, T)."""
        finite = np.isfinite(Yobs)
        count = finite.sum(axis=0)                              # (T,)
        total = np.nansum(Yobs, axis=0)                         # (T,)
        denom = count[None, :] - finite.astype(int)             # others available for each cell
        numer = total[None, :] - np.where(finite, Yobs, 0.0)
        with np.errstate(invalid='ignore', divide='ignore'):
            ym = numer / np.maximum(denom, 1)
        return np.asarray(np.where(denom >= 1, ym, fallback), dtype=float)

    def _initial_fill(self):
        """Linear interpolation per entity, held at the ends; the entity/global mean if no anchor."""
        Y = np.full(self.shape, np.nan)
        for i in range(self.n_entities):
            out, _ = interpolate_series(self.years, self._Yobs[i], self.obs[i], 'identity', 'hold')
            fallback = self._global_mean + self._own_dev[i]
            Y[i] = np.where(np.isfinite(out), out, fallback)
        Y = np.where(self.obs, self._Yobs, Y)
        return Y

    def _features(self, Y, t):
        """(n, 4) design row for year index t, in deviation-from-year-mean space."""
        n = self.n_entities
        x = np.empty((n, _N_FEATURES))
        x[:, 0] = 1.0
        if t >= 1:
            x[:, 1] = Y[:, t - 1] - self._year_mean[:, t - 1]
        else:
            x[:, 1] = self._own_dev
        if t >= 2:
            x[:, 2] = Y[:, t - 2] - self._year_mean[:, t - 2]
        else:
            x[:, 2] = self._own_dev
        x[:, 3] = self._own_dev
        return x

    def _design(self, Y):
        X = np.empty((self.n_entities, self.n_years, _N_FEATURES))
        for t in range(self.n_years):
            X[:, t, :] = self._features(Y, t)
        return X

    def _estimate(self, Y):
        """Pooled OLS of the deviation z on lagged deviations and the own mean deviation."""
        X = self._design(Y)
        Xtr = X[self.obs]
        Yobs = self._Yobs
        ztr = (Yobs - self._year_mean)[self.obs]
        beta, *_ = np.linalg.lstsq(Xtr, ztr, rcond=None)
        resid = ztr - Xtr @ beta
        dof = max(1, int(Xtr.shape[0]) - _N_FEATURES)
        sigma2 = float(resid @ resid) / dof
        xtx_inv = np.linalg.pinv(Xtr.T @ Xtr)
        return beta, sigma2, xtx_inv, dof

    def _fill_point(self, Y, beta):
        """Fill every non-observed cell with year_mean + x beta, in year order."""
        Y = Y.copy()
        for t in range(self.n_years):
            missing = ~self.obs[:, t]
            if not missing.any():
                continue
            Xt = self._features(Y, t)
            Y[missing, t] = self._year_mean[missing, t] + (Xt @ beta)[missing]
        return Y

    def _multiple_draws(self, Y0):
        """M completed panels drawn from the fitted regression's posterior predictive."""
        rng = np.random.default_rng(self.seed)
        M = self.draws_n
        n, T = self.shape
        beta, sigma2, xtx_inv, dof = self._beta, self._sigma2, self._xtx_inv, self._dof
        draws = np.empty((M, n, T))
        for m in range(M):
            sigma2_m = sigma2 * dof / rng.chisquare(dof)        # scaled inverse chi-square
            cov = sigma2_m * xtx_inv
            try:
                A = np.linalg.cholesky(cov + self.ridge * np.eye(_N_FEATURES))
            except np.linalg.LinAlgError:                       # pragma: no cover - xtx_inv is PSD
                w, V = np.linalg.eigh(cov)
                A = V @ np.diag(np.sqrt(np.maximum(w, self.ridge)))
            beta_m = beta + A @ rng.standard_normal(_N_FEATURES)
            sigma_m = float(np.sqrt(max(sigma2_m, 1e-300)))
            Y = Y0.copy()
            for t in range(T):
                missing = ~self.obs[:, t]
                if not missing.any():
                    continue
                Xt = self._features(Y, t)
                z = Xt @ beta_m + sigma_m * rng.standard_normal(n)
                Y[missing, t] = (self._year_mean[:, t] + z)[missing]
            draws[m] = Y
        return draws

    # ------------------------------------------------------------ predict
    def _predict(self, where):
        values = np.where(where, self._values, np.nan)
        draws = np.where(where[None, :, :], self._draws, np.nan)
        se = np.sqrt(self._var)
        lower = np.where(where, self._values - self._z * se, np.nan)
        upper = np.where(where, self._values + self._z * se, np.nan)
        return ImputationResult(values, where, method=self.name, lower=lower, upper=upper,
                                draws=draws, nominal=self.coverage)
