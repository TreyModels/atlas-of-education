"""Rung 5: a state-space (Kalman) smoother with uncertainty intervals, per country, pooled hyperparameters.

Model.  For each entity the level of the series is a local linear trend observed with noise:

    y(t)   = mu(t) + eps(t),        eps ~ N(0, R)                    observation
    mu(t+d)   = mu(t) + d * beta(t) + eta(t),   eta ~ N(0, q_level * d)
    beta(t+d) = beta(t) + zeta(t),             zeta ~ N(0, q_slope * d)

with d the year spacing of the panel.  Missings are simply skipped in the update step, so the
filter runs through gaps; the Rauch-Tung-Striebel (RTS) smoother then uses the observations on
BOTH sides of a gap.  The smoothed level at a missing year is the imputation; its standard error
is sqrt(P_smoothed[level] + R) -- state uncertainty plus the observation noise of the value being
imputed -- and the interval is the corresponding normal interval at `coverage` (default 90%).

Parameters.  (q_level, q_slope, R) are estimated by maximising the pooled prediction-error
log-likelihood over all entities with scipy's L-BFGS-B (deterministic), or supplied directly with
hyper=; the second case is the clean way to test interval calibration on simulated data.  The
series is standardised internally so the optimiser works on unit scale and the result is rescaled
back, which also makes the same defaults work for years-of-schooling (0-20) and GDP (1e2-1e5).

The implementation is batched over entities (all countries advance together), so a 150-country
panel costs only a handful of milliseconds per likelihood evaluation.
"""
import numpy as np
from scipy.optimize import minimize

from .base import Imputer, ImputationResult

# weakly informative initial state covariance in standardised units (the smoother forgets it)
_P0_LEVEL = 100.0
_P0_SLOPE = 10.0


class KalmanSmoother(Imputer):
    """Local-linear-trend smoother with observation-noise predictive intervals."""

    name = 'kalman'
    provides_intervals = True

    def __init__(self, coverage=0.90, fit_hyper=True, hyper=None, maxiter=80):
        super().__init__()
        if not 0.0 < coverage < 1.0:
            raise ValueError('coverage must be in (0, 1)')
        if hyper is not None:
            hyper = tuple(float(x) for x in hyper)
            if len(hyper) != 3 or not all(np.isfinite(hyper)) or min(hyper) <= 0:
                raise ValueError('hyper must be (q_level, q_slope, R) with all entries > 0')
        self.coverage = float(coverage)
        self.fit_hyper = bool(fit_hyper) and hyper is None
        self._hyper = hyper
        self.maxiter = int(maxiter)
        self.hyper_ = None
        self.loglik_ = None

    # ------------------------------------------------------------ fit
    def _fit(self, panel):
        Y = np.where(self.obs, panel.values, np.nan)
        finite = np.isfinite(Y)
        if not finite.any():
            raise ValueError('KalmanSmoother needs at least one observation')
        spread = float(np.nanstd(Y))
        self._scale = spread if np.isfinite(spread) and spread > 0 else 1.0
        Ys = Y / self._scale

        if self._hyper is not None:
            q_std = np.array(self._hyper) / (self._scale ** 2)
        elif self.fit_hyper:
            q_std = self._estimate_hyper(Ys)
        else:
            # documented fallback heuristic when fit_hyper=False and no hyper given
            v = float(np.nanvar(Ys)) or 1.0
            q_std = np.array([0.01 * v, 1e-5 * v, 0.1 * v])

        a_s, P_s, self.loglik_ = self._rts(Ys, q_std)
        R_std = q_std[2]
        mu = a_s[:, :, 0].T                       # (T, n) -> (n, T), the panel orientation
        var_value = P_s[:, :, 0, 0].T + R_std
        # a country with no trusted observation is not informed by this rung: leave it missing
        # rather than report the arbitrary initial state
        self._has_obs = finite.any(axis=1)
        mu = np.where(self._has_obs[:, None], mu, np.nan)
        var_value = np.where(self._has_obs[:, None], var_value, np.nan)
        self._values = mu * self._scale
        self._var = np.maximum(var_value, 1e-12) * (self._scale ** 2)
        self.hyper_ = dict(q_level=float(q_std[0] * self._scale ** 2),
                           q_slope=float(q_std[1] * self._scale ** 2),
                           obs_var=float(R_std * self._scale ** 2))
        from scipy.stats import norm
        self._z = float(norm.ppf(0.5 + 0.5 * self.coverage))

    def _estimate_hyper(self, Ys):
        v = float(np.nanvar(Ys))
        v = v if np.isfinite(v) and v > 0 else 1.0
        x0 = np.log(np.array([0.01 * v, 1e-5 * v, 0.1 * v]))
        res = minimize(lambda z: -self._loglik(Ys, np.exp(z)), x0, method='L-BFGS-B',
                       bounds=[(-20.0, 5.0)] * 3, options={'maxiter': self.maxiter})
        z = res.x if np.all(np.isfinite(res.x)) else x0
        return np.exp(z)

    # ------------------------------------------------------------ batched filter / smoother
    def _loglik(self, Ys, q):
        try:
            return self._filter(Ys, q)[4]
        except (FloatingPointError, np.linalg.LinAlgError):
            return -np.inf

    def _filter(self, Y, q):
        """Batched Kalman filter.  Returns (a_pred, P_pred, a_filt, P_filt, loglik)."""
        n, T = Y.shape
        q_level, q_slope, R = (float(x) for x in q)
        if not (q_level > 0 and q_slope > 0 and R > 0):
            raise FloatingPointError('non-positive variance')

        a_pred = np.empty((T, n, 2))
        P_pred = np.empty((T, n, 2, 2))
        a_filt = np.empty((T, n, 2))
        P_filt = np.empty((T, n, 2, 2))
        valid = np.isfinite(Y)
        has = valid.any(axis=1)
        first = np.argmax(valid, axis=1)

        a = np.zeros((n, 2))
        a[:, 0] = np.where(has, Y[np.arange(n), first], 0.0)
        P = np.zeros((n, 2, 2))
        P[:, 0, 0] = _P0_LEVEL
        P[:, 1, 1] = _P0_SLOPE
        ll = 0.0
        dt = np.diff(self.years) if T > 1 else np.array([])

        for t in range(T):
            if t > 0:
                h = float(dt[t - 1])
                Tm = np.array([[1.0, h], [0.0, 1.0]])
                a = a @ Tm.T
                P = Tm @ P @ Tm.T
                P = P + np.diag([q_level * h, q_slope * h])
            a_pred[t] = a
            P_pred[t] = P
            y = Y[:, t]
            mask = np.isfinite(y)
            v = np.where(mask, y - a[:, 0], 0.0)
            F = P[:, 0, 0] + R
            K = (P[:, 0, :] / F[:, None]) * mask[:, None]
            a = a + K * v[:, None]
            P = P - K[:, :, None] * P[:, None, 0, :]
            P = 0.5 * (P + P.transpose(0, 2, 1))            # keep it exactly symmetric
            a_filt[t] = a
            P_filt[t] = P
            ll += -0.5 * float(np.sum(np.where(mask, np.log(2.0 * np.pi * F) + v * v / F, 0.0)))
        return a_pred, P_pred, a_filt, P_filt, ll

    def _rts(self, Y, q):
        """Batched RTS smoother.  Returns (a_smooth (T,n,2), P_smooth (T,n,2,2), loglik)."""
        n, T = Y.shape
        a_pred, P_pred, a_filt, P_filt, ll = self._filter(Y, q)
        a_s = a_filt.copy()
        P_s = P_filt.copy()
        dt = np.diff(self.years) if T > 1 else np.array([])
        for t in range(T - 2, -1, -1):
            h = float(dt[t])
            Tm = np.array([[1.0, h], [0.0, 1.0]])
            Pn = P_pred[t + 1]
            A = P_filt[t] @ Tm.T                                   # P_f[t] T'
            J = np.linalg.solve(Pn, A.transpose(0, 2, 1)).transpose(0, 2, 1)   # A inv(Pn)
            a_s[t] = a_filt[t] + (J @ (a_s[t + 1] - a_pred[t + 1])[:, :, None])[:, :, 0]
            P_s[t] = P_filt[t] + J @ (P_s[t + 1] - Pn) @ J.transpose(0, 2, 1)
            P_s[t] = 0.5 * (P_s[t] + P_s[t].transpose(0, 2, 1))
        return a_s, P_s, ll

    # ------------------------------------------------------------ predict
    def _predict(self, where):
        values = np.where(where, self._values, np.nan)
        se = np.sqrt(self._var)
        lower = np.where(where, self._values - self._z * se, np.nan)
        upper = np.where(where, self._values + self._z * se, np.nan)
        return ImputationResult(values, where, method=self.name,
                                lower=lower, upper=upper, nominal=self.coverage)
