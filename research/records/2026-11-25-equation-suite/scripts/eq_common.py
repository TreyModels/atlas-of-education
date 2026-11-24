"""Shared helpers for the 2026-11-25 Master Equation Inventory suite.

SIMULATION-only helpers. numpy + stdlib only (no scipy). Every script labels its own data tier and
makes no causal claim. Estimators are deliberately small, auditable implementations: OLS with HC1 or
cluster-robust SEs, logit/probit by Newton, Tobit by EM, two-part models, BH/BY, and a projected-gradient
synthetic-control weight solver.
"""
import argparse, hashlib, json, math, os
from datetime import datetime, timezone

import numpy as np

_ERF = np.vectorize(math.erf)


def rng(seed):
    return np.random.default_rng(int(seed))


def norm_cdf(x):
    return 0.5 * (1.0 + _ERF(np.asarray(x, float) / math.sqrt(2.0)))


def norm_pdf(x):
    return np.exp(-0.5 * np.asarray(x, float) ** 2) / math.sqrt(2.0 * math.pi)


def ols(y, X, cluster=None):
    """OLS with HC1 (default) or cluster-robust SEs. Returns dict of lists/scalars."""
    y = np.asarray(y, float).reshape(-1)
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ (X.T @ y)
    e = y - X @ b
    n, p = X.shape
    if cluster is not None:
        cl = np.asarray(cluster)
        groups = np.unique(cl)
        S = np.zeros((p, p))
        for g in groups:
            m = cl == g
            s = X[m].T @ e[m]
            S += np.outer(s, s)
        G = len(groups)
        cov = XtX_inv @ S @ XtX_inv * (G / max(G - 1, 1)) * ((n - 1) / max(n - p, 1))
    else:
        S = X.T @ (X * (e ** 2)[:, None])
        cov = XtX_inv @ S @ XtX_inv * (n / max(n - p, 1))
    se = np.sqrt(np.maximum(np.diag(cov), 0.0))
    ss = float(np.sum((y - y.mean()) ** 2))
    tt = [float(b[i] / se[i]) if se[i] > 0 else float("inf") for i in range(p)]
    return {"b": b.tolist(), "se": se.tolist(), "t": tt, "n": int(n),
            "r2": float(1.0 - np.sum(e ** 2) / ss) if ss > 0 else 0.0}


def logit(y, X, iters=60, ridge=1e-8):
    y = np.asarray(y, float).reshape(-1)
    X = np.asarray(X, float)
    b = np.zeros(X.shape[1])
    b[0] = math.log((y.mean() + 1e-6) / (1 - y.mean() + 1e-6))
    for _ in range(iters):
        z = np.clip(X @ b, -30, 30)
        p = 1.0 / (1.0 + np.exp(-z))
        w = np.maximum(p * (1 - p), 1e-12)
        H = X.T @ (X * w[:, None]) + ridge * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    z = np.clip(X @ b, -30, 30)
    p = 1.0 / (1.0 + np.exp(-z))
    w = np.maximum(p * (1 - p), 1e-12)
    H = X.T @ (X * w[:, None]) + ridge * np.eye(X.shape[1])
    se = np.sqrt(np.maximum(np.diag(np.linalg.pinv(H)), 0.0))
    return {"b": b.tolist(), "se": se.tolist(), "n": int(len(y))}


def probit(y, X, iters=60, ridge=1e-8):
    y = np.asarray(y, float).reshape(-1)
    X = np.asarray(X, float)
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        z = np.clip(X @ b, -6.5, 6.5)
        p = np.clip(norm_cdf(z), 1e-12, 1.0 - 1e-12)
        ph = norm_pdf(z)
        w = np.maximum(ph ** 2 / (p * (1.0 - p)), 1e-12)
        score = X.T @ ((ph / (p * (1.0 - p))) * (y - p))
        H = X.T @ (X * w[:, None]) + ridge * np.eye(X.shape[1])
        step = np.linalg.solve(H, score)
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    z = np.clip(X @ b, -6.5, 6.5)
    p = np.clip(norm_cdf(z), 1e-12, 1.0 - 1e-12)
    ph = norm_pdf(z)
    w = np.maximum(ph ** 2 / (p * (1.0 - p)), 1e-12)
    H = X.T @ (X * w[:, None]) + ridge * np.eye(X.shape[1])
    se = np.sqrt(np.maximum(np.diag(np.linalg.pinv(H)), 0.0))
    return {"b": b.tolist(), "se": se.tolist(), "n": int(len(y))}


def tobit_em(y, X, iters=400):
    """Left-censored-at-zero Tobit by EM. SEs are the OLS-on-completed-data approximation; disclosed."""
    y = np.asarray(y, float).reshape(-1)
    X = np.asarray(X, float)
    pos = y > 0
    b = np.linalg.lstsq(X[pos], y[pos], rcond=None)[0]
    sigma = max(float(np.std(y[pos] - X[pos] @ b)), 1e-6)
    ystar = y.copy()
    for _ in range(iters):
        b_old, sigma_old = b, sigma
        z = X @ b
        a = -z / sigma
        safe_a = np.where(a < -6.0, -6.0, a)
        tail_a = np.where(a < -6.0, a, -6.0)
        lam = np.where(
            a < -6.0,
            -tail_a - 1.0 / tail_a + 2.0 / (tail_a ** 3),
            norm_pdf(safe_a) / np.maximum(norm_cdf(safe_a), 1e-300),
        )
        ystar = np.where(pos, y, z - sigma * lam)
        var_cond = np.where(pos, 0.0, (sigma ** 2) * np.maximum(1.0 - a * lam - lam ** 2, 0.0))
        b = np.linalg.lstsq(X, ystar, rcond=None)[0]
        sigma = max(float(np.sqrt(np.mean((ystar - X @ b) ** 2 + var_cond))), 1e-6)
        if max(float(np.max(np.abs(b - b_old))), abs(sigma - sigma_old)) < 1e-9:
            break
    cov = max(float(sigma ** 2), 1e-8) * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.maximum(np.diag(cov), 0.0))
    return {"b": b.tolist(), "se": se.tolist(), "sigma": float(sigma), "n": int(len(y))}


def bh(p, alpha=0.05):
    p = np.sort(np.asarray(p, float))
    k = np.arange(1, len(p) + 1)
    ok = p <= k * alpha / len(p)
    return int(k[ok].max()) if ok.any() else 0


def by(p, alpha=0.05):
    p = np.sort(np.asarray(p, float))
    m = len(p)
    H = sum(1.0 / i for i in range(1, m + 1))
    k = np.arange(1, m + 1)
    ok = p <= k * alpha / (m * H)
    return int(k[ok].max()) if ok.any() else 0


def synthetic_control_weights(y1_pre, y0_pre, ridge=1e-6, iters=4000, lr=0.05):
    """Projected-gradient simplex weights for a synthetic control (approximate; disclosed)."""
    y1_pre = np.asarray(y1_pre, float)
    y0_pre = np.asarray(y0_pre, float)
    J = y0_pre.shape[1]
    w = np.ones(J) / J
    for _ in range(iters):
        r = y1_pre - y0_pre @ w
        g = -2.0 * (y0_pre.T @ r) / len(y1_pre) + 2.0 * ridge * w
        w = w - lr * g
        w = np.maximum(w, 0.0)
        s = w.sum()
        w = w / s if s > 0 else np.ones(J) / J
    return w


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_result(outdir, name, obj):
    os.makedirs(outdir, exist_ok=True)
    obj = dict(obj)
    obj.setdefault("generated_utc", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    p = os.path.join(outdir, name + ".json")
    with open(p, "w") as f:
        json.dump(obj, f, indent=1)
    return p


def save_csv(outdir, name, header, rows):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, name + ".csv")
    with open(p, "w") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    return p


def smoke_parser(description):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--smoke", action="store_true", help="fewer seeds/reps; same code path")
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--seed", type=int, default=20261125)
    return ap.parse_args()
