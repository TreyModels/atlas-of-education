"""Imputation engine.

For one target series (country x year panel with gaps):
  1. regression on auxiliary long-run predictors plus a country-specific smooth trend (intercept, slope, curvature,
     shrunk toward zero by a ridge penalty chosen by cross-validation), global time spline;
  2. residuals follow a within-country exponential-decay (Gaussian-process) correlation, so a gap is filled
     close to its observed neighbours and reverts to the regression far from them;
  3. each imputation draws the regression coefficients from their (ridge) posterior and then the residuals of the
     missing cells conditional on the observed residuals of the same country.  The spread is multiplied by a
     calibration factor kappa found by validation.
Values are modelled on a log(1+y) scale (ratios and rates) or raw (gender parity) and clipped to the observed range.
"""
import numpy as np
from scipy.linalg import solve_triangular, cho_factor, cho_solve
from common import *

LOG_TARGETS = {"lsc", "sec", "ter", "prm_cmp"}
tt = ((YEARS - 1985) / 20.0)


def zcol(x):
    mu, sd = np.nanmean(x), np.nanstd(x)
    z = (x - mu) / (sd if sd > 0 else 1)
    return np.where(np.isfinite(z), z, 0.0), (~np.isfinite(x)).astype(float)


def build_cells(aux):
    """global predictor matrix for all NC*NY cells"""
    P = {}
    P["lninc"] = np.log(aux["lr_gdppc_log"]); P["fert"] = aux["lr_fertility"]; P["e0"] = aux["lr_life_exp"]
    P["lnu5"] = np.log(aux["lr_u5mr"]); P["urb"] = aux["lr_urban"]
    for k in aux:
        if k.startswith("x_"):
            P[k[2:]] = aux[k]
    cols, names = [], []
    for k, x in P.items():
        f = np.isfinite(x).mean()
        if f < 0.02:
            continue
        z, ind = zcol(x)
        cols.append(z.ravel()); names.append(k)
        if f < 0.99:
            cols.append(ind.ravel()); names.append(k + "_miss")
    # global time spline (piecewise linear, knots every ten years)
    t = YEARS - 1950.0
    T = np.tile(t[None, :], (NC, 1)).ravel() / 10.0
    cols.append(T); names.append("t")
    for kn in range(1960, 2021, 10):
        cols.append(np.maximum(T - (kn - 1950) / 10.0, 0)); names.append(f"t{kn}")
    G = np.column_stack(cols)
    ci = np.repeat(np.arange(NC), NY)
    tc = np.tile(tt, NC)
    oh = np.zeros((NC * NY, NC))
    oh[np.arange(NC * NY), ci] = 1
    X = np.hstack([np.ones((NC * NY, 1)), G, oh, oh * tc[:, None], oh * (tc ** 2)[:, None]])
    ng = 1 + G.shape[1]
    return X, ng, names


class Model:
    def __init__(self, target, y, X, ng, lo, hi, minobs=3, rng_seed=0):
        self.target, self.X, self.ng = target, X, ng
        self.log = target in LOG_TARGETS
        self.lo, self.hi = lo, hi
        self.y = y
        yt = np.log1p(y) if self.log else y.copy()
        self.yt = yt
        cnt = np.isfinite(y).sum(1)
        self.use = cnt >= minobs
        m = np.isfinite(yt) & self.use[:, None]
        self.oidx = np.flatnonzero(m.ravel())
        Xo = X[self.oidx]; yo = yt.ravel()[self.oidx]
        self.Xo, self.yo = Xo, yo
        self.XtX = Xo.T @ Xo; self.Xty = Xo.T @ yo
        self.choose_lambda(np.random.default_rng(rng_seed))
        self.fit(self.lam)

    def pen(self, lam):
        p = np.full(self.X.shape[1], 1e-4)
        ng = self.ng
        p[ng:ng + NC] = lam; p[ng + NC:ng + 2 * NC] = lam; p[ng + 2 * NC:] = 5 * lam
        return p

    def fit(self, lam):
        A = self.XtX + np.diag(self.pen(lam))
        self.cf = cho_factor(A, lower=True)
        self.L = self.cf[0]
        self.beta = cho_solve(self.cf, self.Xty)
        res = self.yo - self.Xo @ self.beta
        edf = np.einsum("ij,ji->", self.Xo, cho_solve(self.cf, self.Xo.T)) if len(self.yo) < 9000 else len(self.yo) * 0.1
        self.sigma = float(np.sqrt((res ** 2).sum() / max(len(res) - edf, 10)))
        # residual panel for GP
        mu = (self.X @ self.beta).reshape(NC, NY)
        R = self.yt - mu
        self.mu = mu
        # lag-1 residual correlation
        a, b = R[:, :-1].ravel(), R[:, 1:].ravel()
        ok = np.isfinite(a) & np.isfinite(b) & np.repeat(self.use, NY - 1)
        rho = np.corrcoef(a[ok], b[ok])[0, 1] if ok.sum() > 30 else 0.5
        rho = min(max(rho, 0.2), 0.97)
        self.tau = -1 / np.log(rho)
        self.sig_r = float(np.nanstd(R[np.repeat(self.use, NY).reshape(NC, NY) & np.isfinite(R)]))
        self.sig_r *= np.sqrt(len(res) / max(len(res) - edf, 10))
        self.prep_gp()

    def choose_lambda(self, rng):
        n = len(self.yo)
        fold = rng.integers(0, 5, n)
        best = None
        for lam in (0.3, 1.0, 3.0, 10.0):
            sse = 0.0
            for f in range(5):
                tr, te = fold != f, fold == f
                A = self.Xo[tr].T @ self.Xo[tr] + np.diag(self.pen(lam))
                b = np.linalg.solve(A, self.Xo[tr].T @ self.yo[tr])
                sse += ((self.yo[te] - self.Xo[te] @ b) ** 2).sum()
            if best is None or sse < best[0]:
                best = (sse, lam)
        self.lam = best[1]

    def prep_gp(self):
        self.gp = {}
        s2 = self.sig_r ** 2
        for i in np.flatnonzero(self.use):
            O = np.flatnonzero(np.isfinite(self.yt[i])); U = np.flatnonzero(~np.isfinite(self.yt[i]))
            if len(U) == 0:
                continue
            K = lambda a, b: s2 * np.exp(-np.abs(a[:, None] - b[None, :]) / self.tau)
            KOO = K(O, O) + 1e-4 * s2 * np.eye(len(O))
            KUO = K(U, O)
            W = np.linalg.solve(KOO, KUO.T).T
            C = K(U, U) - W @ KUO.T + 1e-8 * s2 * np.eye(len(U))
            Lc = np.linalg.cholesky(C)
            self.gp[i] = (O, U, W, Lc)

    def draw(self, M, kappa, rng, dist=None):
        """returns (M, NC, NY) draws in original units; NaN for countries that are not modelled"""
        out = np.full((M, NC, NY), np.nan)
        p = self.X.shape[1]
        for m in range(M):
            z = rng.standard_normal(p)
            beta = self.beta + kappa * self.sigma * solve_triangular(self.L.T, z, lower=False)
            mu = (self.X @ beta).reshape(NC, NY)
            v = np.full((NC, NY), np.nan)
            for i, (O, U, W, Lc) in self.gp.items():
                e = self.yt[i, O] - mu[i, O]
                v[i, O] = self.yt[i, O]
                v[i, U] = mu[i, U] + W @ e + kappa * (Lc @ rng.standard_normal(len(U)))
            if self.log:
                v = np.expm1(v)
            out[m] = np.clip(v, self.lo, self.hi)
        return out


def horizon(y):
    """distance (years) from every cell to the nearest observed cell of the same country"""
    h = np.full(y.shape, 999.0)
    for i in range(y.shape[0]):
        O = np.flatnonzero(np.isfinite(y[i]))
        if len(O):
            h[i] = np.abs(np.arange(y.shape[1])[:, None] - O[None, :]).min(1)
    return h
