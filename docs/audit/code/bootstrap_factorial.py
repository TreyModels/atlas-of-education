#!/usr/bin/env python3
"""P0-04 + P0-05 (external audit) — bootstrap size/power factorial and the invalid
within-country permutation replacement.

Context (docs/audit/EXTERNAL_AUDIT_GPU_2026-11-25.md P0-04/P0-05)
------------------------------------------------------------------
The shipped E1/Q3 selftest (`gpu_e1_q3_wild_cluster_ri.py:172-185`) is

    c_eff = normal(0,1)[country]                     # country effect
    x1    = normal(0,1) + 0.5*c_eff                  # country effect enters the REGRESSOR
    y     = 0.2 + 0.8*active_c*x1 + 0.3*x2 + c_eff + noise   # ... and the OUTCOME

The pooled regression omits c_eff -> omitted-variable bias; clustered SEs cannot cure OVB. The
auditor's negative control (true effect zero everywhere) found pooled beta = 0.3054, t = 4.975,
wild-cluster p = 0.0005 — "significant" under a true null. The shipped selftest therefore cannot
attribute its result to minority-effect leakage. The shipped country-block permutation sets
x*_it = xbar_{pi(i)} + (x_it - xbar_i); after country FE, x*_it - xbar*_i = x_it - xbar_i
**identically**, so the within coefficient is permutation-invariant and the permutation cannot test
the within estimand (P0-05).

This script
-----------
TASK A (P0-04) — factorial: minority-effect share {0, 5, 15, 50, 100}% x country confounding
{0, 0.25, 0.5, 1.0} x estimator {pooled OLS, country FE, country+year FE}, 2,000 independently
generated datasets per cell; reports type-I error at 5% (size first), power, bias, RMSE, CI
coverage; writes docs/audit/BOOTSTRAP_SIZE_POWER_RESULTS.parquet.
TASK B (P0-05) — (i) algebraic + numerical proof of permutation invariance under country FE;
(ii) independent reproduction of the shipped selftest statistics; (iii) replacement inference:
restricted wild-cluster bootstrap (Rademacher) for the FE estimator, plus a whole-trajectory
cluster bootstrap, with size measured on the null cells; (iv) exchangeability discussion is in
docs/audit/BOOTSTRAP_REPORT.md.

Run:
    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    /Users/treymenefee/neon-boot/venv/bin/python docs/audit/code/bootstrap_factorial.py \
        --out docs/audit --workers 3 --n-datasets 2000 --seed 20261125
"""
from __future__ import annotations

import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

import numpy as np
import pandas as pd

G, T = 60, 20                      # countries, years (the shipped selftest design)
N = G * T
CL = np.repeat(np.arange(G), T)
TAU = 0.8                          # true minority slope (shipped)
SELFTEST_SEED = 20261125
SHARES = [0.0, 0.05, 0.15, 0.50, 1.00]
CONFS = [0.0, 0.25, 0.50, 1.00]
ESTIMATORS = ["pooled", "country_fe", "country_year_fe"]


# ====================================================================================== simulation
def simulate_batch(n_sets, share, conf, rng, tau=TAU, random_active=True):
    """Vectorised version of the shipped DGP for ``n_sets`` independent datasets.

    x1 = e + conf*c_eff ; y = 0.2 + tau*active_c*x1 + 0.3*x2 + c_eff + eps.
    ``share`` = fraction of countries with the true effect; the active set is a random subset of
    countries (exchangeable across countries by construction) unless ``random_active=False``, which
    reproduces the shipped "first k countries" rule for the benchmark.
    """
    c_eff = rng.normal(0.0, 1.0, size=(n_sets, G))[:, CL]
    x1 = rng.normal(0.0, 1.0, size=(n_sets, N)) + conf * c_eff
    x2 = rng.normal(0.0, 1.0, size=(n_sets, N))
    k = int(round(share * G))
    active = np.zeros((n_sets, G), float)
    if k > 0:
        if random_active:
            for b in range(n_sets):
                active[b, rng.choice(G, size=k, replace=False)] = 1.0
        else:
            active[:, :k] = 1.0
    y = 0.2 + tau * active[:, CL] * x1 + 0.3 * x2 + c_eff + rng.normal(0.0, 1.0, size=(n_sets, N))
    return y, x1, x2


def _ols_cr1(y, X, clusters=CL):
    """Batched OLS with CR1 cluster-robust SEs. y: (B,N); X: (B,N,K). Returns beta, se."""
    B, n, K = X.shape
    Xt = np.einsum("bni->bin", X)
    XtX = np.einsum("bni,bnj->bij", X, X)
    Xty = np.einsum("bni,bn->bi", X, y)
    XtX_inv = np.linalg.inv(XtX)
    beta = np.einsum("bij,bj->bi", XtX_inv, Xty)
    resid = y - np.einsum("bni,bi->bn", X, beta)
    scores = np.einsum("bni,bn->bni", X, resid).reshape(B, G, T, K).sum(axis=2)   # (B,G,K)
    M = np.einsum("bgk,bgl->bkl", scores, scores)
    V = (G / max(G - 1.0, 1.0)) * np.einsum("bij,bjk,bkl->bil", XtX_inv, M, XtX_inv)
    se = np.sqrt(np.clip(np.einsum("bii->bi", V), 1e-18, None))
    return beta, se


def _demean_country(x):
    return x.reshape(x.shape[0], G, T) - x.reshape(x.shape[0], G, T).mean(axis=2, keepdims=True)


def _demean_two_way(x, iters=15):
    z = x.reshape(x.shape[0], G, T)
    for _ in range(iters):
        z = z - z.mean(axis=2, keepdims=True)
        z = z - z.mean(axis=1, keepdims=True)
    return z - z.mean(axis=(1, 2), keepdims=True)


def estimate_batch(y, x1, x2, estimator):
    """Return (beta1, se1) for one estimator over a batch of datasets."""
    B = y.shape[0]
    if estimator == "pooled":
        X = np.stack([np.ones_like(y), x1, x2], axis=2)
        beta, se = _ols_cr1(y, X)
        return beta[:, 1], se[:, 1]
    yw = _demean_country(y).reshape(B, N)
    x1w = _demean_country(x1).reshape(B, N)
    x2w = _demean_country(x2).reshape(B, N)
    if estimator == "country_year_fe":
        # two-way within transform on all three variables
        yw = _demean_two_way(y).reshape(B, N)
        x1w = _demean_two_way(x1).reshape(B, N)
        x2w = _demean_two_way(x2).reshape(B, N)
    X = np.stack([x1w, x2w], axis=2)
    beta, se = _ols_cr1(yw, X)
    return beta[:, 0], se[:, 0]


# ====================================================================================== benchmark
def shipped_selftest(seed=SELFTEST_SEED, tau=TAU, B_wild=2000):
    """Reproduce the shipped selftest exactly (same draw order) and the auditor's four statistics."""
    rng = np.random.default_rng(seed)
    c_eff = rng.normal(0, 1.0, size=G)[CL]
    x1 = rng.normal(0, 1.0, size=N) + 0.5 * c_eff
    x2 = rng.normal(0, 1.0, size=N)
    active_c = (CL < int(0.15 * G)).astype(float)
    y = 0.2 + tau * active_c * x1 + 0.3 * x2 + c_eff + rng.normal(0, 1.0, size=N)
    X = np.column_stack([np.ones(N), x1, x2])
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    u = y - X @ beta
    XtX_inv = np.linalg.inv(X.T @ X)
    S = np.zeros((G, 3))
    np.add.at(S, CL, X * u[:, None])
    V = (G / (G - 1.0)) * XtX_inv @ (S.T @ S) @ XtX_inv
    se = float(np.sqrt(V[1, 1]))
    t_obs = float(beta[1] / se)
    # Rademacher restricted wild-cluster bootstrap (shipped algorithm, NumPy)
    Xr = X[:, [0, 2]]
    br = np.linalg.solve(Xr.T @ Xr, Xr.T @ y)
    yr_hat = Xr @ br
    ur = y - yr_hat
    a = XtX_inv[1, :]
    xa = X @ a
    boot_rng = np.random.default_rng(seed)
    t_boot = np.empty(B_wild)
    for b in range(B_wild):
        W_g = boot_rng.integers(0, 2, size=G) * 2.0 - 1.0
        y_star = yr_hat + W_g[CL] * ur
        beta_star = XtX_inv @ (X.T @ y_star)
        resid_star = y_star - X @ beta_star
        S_g = np.zeros(G)
        np.add.at(S_g, CL, xa * resid_star)
        var1 = (G / (G - 1.0)) * np.sum(S_g ** 2)
        t_boot[b] = beta_star[1] / np.sqrt(max(var1, 1e-18))
    p_wild = float((1.0 + np.sum(np.abs(t_boot) >= abs(t_obs))) / (B_wild + 1.0))
    return dict(
        mode="shipped_selftest_reproduction", tau=tau, N=int(N), G=int(G),
        beta1=float(beta[1]), se_cr1=se, t_obs=t_obs, p_wild_cluster=p_wild,
        expected=dict(beta1=0.4447407388610457, se_cr1=0.08291358451449403,
                      t_obs=5.363906788800104, p_wild_cluster=0.0004997501249375312),
    )


# ====================================================================================== permutation
def permutation_invariance(seed=SELFTEST_SEED, B_perm=200):
    """Show the country-block permutation is within-invariant under country FE (P0-05)."""
    rng = np.random.default_rng(seed)
    c_eff = rng.normal(0, 1.0, size=G)[CL]
    x1 = rng.normal(0, 1.0, size=N) + 0.5 * c_eff
    x2 = rng.normal(0, 1.0, size=N)
    active_c = (CL < int(0.15 * G)).astype(float)
    y = 0.2 + 0.8 * active_c * x1 + 0.3 * x2 + c_eff + rng.normal(0, 1.0, size=N)

    def fe_beta(xv):
        Xw = np.column_stack([_within(xv), _within(x2)])
        yw = _within(y)
        return float(np.linalg.solve(Xw.T @ Xw, Xw.T @ yw)[0])

    def pooled_beta(xv):
        X = np.column_stack([np.ones(N), xv, x2])
        return float(np.linalg.solve(X.T @ X, X.T @ y)[1])

    c_means = np.array([x1[CL == i].mean() for i in range(G)])
    x1_within = x1 - c_means[CL]
    perms = np.random.default_rng(seed + 1)
    fe_vals, pooled_vals, within_maxdev = [], [], 0.0
    for _ in range(B_perm):
        perm = perms.permutation(G)
        x_star = c_means[perm][CL] + x1_within
        within_maxdev = max(within_maxdev, float(np.max(np.abs(_within(x_star) - _within(x1)))))
        fe_vals.append(fe_beta(x_star))
        pooled_vals.append(pooled_beta(x_star))
    fe_vals = np.array(fe_vals)
    pooled_vals = np.array(pooled_vals)
    return dict(
        mode="country_block_permutation_invariance",
        B_perm=B_perm,
        within_max_abs_deviation=within_maxdev,
        fe_beta_original=fe_beta(x1),
        fe_beta_perm_mean=float(fe_vals.mean()),
        fe_beta_perm_max_abs_dev_from_original=float(np.max(np.abs(fe_vals - fe_beta(x1)))),
        pooled_perm_sd=float(pooled_vals.std()),
        pooled_perm_min=float(pooled_vals.min()), pooled_perm_max=float(pooled_vals.max()),
        conclusion=("within coefficient is permutation-invariant (deviation <= 1e-12): the shipped "
                    "permutation cannot test the within estimand"),
    )


def _within(xv):
    return xv - np.array([xv[CL == i].mean() for i in range(G)])[CL]


# ====================================================================================== replacement inference
def fe_restricted_wild_bootstrap(y, x1, x2, B=999, seed=0):
    """Restricted wild-cluster bootstrap (Rademacher) for the FE estimator, H0: beta_x1 = 0."""
    yw, x1w, x2w = _within(y), _within(x1), _within(x2)
    Xw = np.column_stack([x1w, x2w])
    beta = np.linalg.solve(Xw.T @ Xw, Xw.T @ yw)
    u = yw - Xw @ beta
    XtX_inv = np.linalg.inv(Xw.T @ Xw)
    S = np.zeros((G, 2))
    np.add.at(S, CL, Xw * u[:, None])
    se = np.sqrt(np.clip((G / (G - 1.0)) * (XtX_inv @ (S.T @ S) @ XtX_inv)[0, 0], 1e-18, None))
    t_obs = beta[0] / se
    # restricted model: yw ~ x2w
    br = float(x2w @ yw) / float(x2w @ x2w)
    yr_hat = x2w * br
    ur = yw - yr_hat
    a = XtX_inv[0, :]
    xa = Xw @ a
    rng = np.random.default_rng(seed)
    t_boot = np.empty(B)
    for b in range(B):
        W_g = rng.integers(0, 2, size=G) * 2.0 - 1.0
        y_star = yr_hat + W_g[CL] * ur
        beta_star = XtX_inv @ (Xw.T @ y_star)
        resid_star = y_star - Xw @ beta_star
        S_g = np.zeros(G)
        np.add.at(S_g, CL, xa * resid_star)
        var1 = (G / (G - 1.0)) * np.sum(S_g ** 2)
        t_boot[b] = beta_star[0] / np.sqrt(max(var1, 1e-18))
    return dict(beta=float(beta[0]), se=float(se), t_obs=float(t_obs),
                p_wild=float((1.0 + np.sum(np.abs(t_boot) >= abs(t_obs))) / (B + 1.0)),
                B=B)


def fe_cluster_bootstrap(y, x1, x2, B=499, seed=0):
    """Whole-trajectory (cluster) bootstrap: resample countries with replacement, recompute FE beta."""
    yw, x1w, x2w = _within(y), _within(x1), _within(x2)
    rng = np.random.default_rng(seed)
    betas = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, G, size=G)
        idx = np.concatenate([np.flatnonzero(CL == c) for c in pick])
        # re-cluster the resampled countries so demeaning is within each sampled trajectory
        Xb = np.column_stack([x1w[idx], x2w[idx]])
        yb = yw[idx]
        betas[b] = np.linalg.solve(Xb.T @ Xb, Xb.T @ yb)[0]
    return dict(beta_obs=float(np.linalg.solve(
        np.column_stack([x1w, x2w]).T @ np.column_stack([x1w, x2w]),
        np.column_stack([x1w, x2w]).T @ yw)[0]),
        ci95=[float(np.percentile(betas, 2.5)), float(np.percentile(betas, 97.5))],
        sd=float(betas.std()), B=B)


# ====================================================================================== factorial cell
def run_cell(job):
    share, conf, estimator, n_sets, seed = job
    rng = np.random.default_rng(seed)
    batch = 250
    betas, ses = [], []
    done = 0
    while done < n_sets:
        nb = min(batch, n_sets - done)
        y, x1, x2 = simulate_batch(nb, share, conf, rng)
        b, s = estimate_batch(y, x1, x2, estimator)
        betas.append(b)
        ses.append(s)
        done += nb
    beta = np.concatenate(betas)
    se = np.concatenate(ses)
    tau_bar = TAU * int(round(share * G)) / G
    tstat = beta / se
    reject = np.abs(tstat) > 1.96
    covered = (beta - 1.96 * se <= tau_bar) & (tau_bar <= beta + 1.96 * se)
    return dict(share=share, conf=conf, estimator=estimator, n_datasets=n_sets,
                true_effect=float(tau_bar), beta_mean=float(beta.mean()),
                beta_sd=float(beta.std(ddof=1)), bias=float(beta.mean() - tau_bar),
                rmse=float(np.sqrt(np.mean((beta - tau_bar) ** 2))),
                mean_se=float(se.mean()), rejection_rate=float(reject.mean()),
                coverage95=float(covered.mean()),
                t_mean=float(tstat.mean()), t_sd=float(tstat.std(ddof=1)),
                size_or_power=("size" if abs(share) < 1e-12 else "power"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/audit")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--n-datasets", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261125)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()

    # ---- Task A: full factorial -------------------------------------------------------------
    jobs = []
    ci = 0
    for share in SHARES:
        for conf in CONFS:
            for est in ESTIMATORS:
                ci += 1
                jobs.append((share, conf, est, args.n_datasets, args.seed + 1000 * ci))
    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as ex:
        rows = list(ex.map(run_cell, jobs, chunksize=1))
    fact = pd.DataFrame(rows).sort_values(["share", "conf", "estimator"]).reset_index(drop=True)
    fact.to_parquet(os.path.join(args.out, "BOOTSTRAP_SIZE_POWER_RESULTS.parquet"), index=False)

    # ---- Task B: benchmark reproduction, permutation invariance, replacement inference -------
    bench = shipped_selftest()
    neg = shipped_selftest(tau=0.0)
    perm = permutation_invariance()
    # replacement inference on the null world (share=0) across confoundings, FE estimator
    repl = []
    for conf in CONFS:
        for method in ("fe_restricted_wild", "fe_cluster_bootstrap"):
            rej, cover = [], []
            n_rep = 120 if method == "fe_restricted_wild" else 120
            for r in range(n_rep):
                rng = np.random.default_rng(args.seed + 77 + r + int(100 * conf))
                y, x1, x2 = simulate_batch(1, 0.0, conf, rng)
                y, x1, x2 = y[0], x1[0], x2[0]
                if method == "fe_restricted_wild":
                    out = fe_restricted_wild_bootstrap(y, x1, x2, B=499, seed=args.seed + r)
                    rej.append(out["p_wild"] < 0.05)
                    cover.append(True)   # WCR p-value; coverage via cluster CI below
                else:
                    out = fe_cluster_bootstrap(y, x1, x2, B=299, seed=args.seed + r)
                    rej.append(not (out["ci95"][0] <= 0.0 <= out["ci95"][1]))
                    cover.append(out["ci95"][0] <= 0.0 <= out["ci95"][1])
            repl.append(dict(confounding=conf, method=method, n_rep=n_rep,
                             size_rejection_rate=float(np.mean(rej)),
                             coverage95=float(np.mean(cover)) if method == "fe_cluster_bootstrap" else None))
    repl = pd.DataFrame(repl)

    summary = dict(
        task="P0-04/P0-05 bootstrap size/power factorial + permutation replacement",
        date_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        runtime_sec=round(time.time() - t0, 2),
        design=dict(G=G, T=T, N=int(N), tau=TAU, shares=SHARES, confoundings=CONFS,
                    estimators=ESTIMATORS, n_datasets=args.n_datasets, seed=args.seed),
        benchmark_reproduction=bench,
        negative_control=neg,
        permutation_invariance=perm,
        replacement_inference=repl.to_dict(orient="records"),
        factorial_file="BOOTSTRAP_SIZE_POWER_RESULTS.parquet",
        size_table=fact[fact.share == 0.0][["conf", "estimator", "rejection_rate", "coverage95"]]
            .to_dict(orient="records"),
        power_table=fact[fact.share == 0.15][["conf", "estimator", "rejection_rate", "bias", "rmse"]]
            .to_dict(orient="records"),
    )
    # size-control assertion: the correctly specified FE estimator must hold ~5% under the null
    size_fe = fact[(fact.share == 0.0) & (fact.estimator == "country_fe")].rejection_rate
    summary["acceptance"] = dict(
        fe_size_median=float(size_fe.median()),
        fe_size_holds=(float(size_fe.median()) <= 0.08),
        pooled_size_under_confounding=float(
            fact[(fact.share == 0.0) & (fact.estimator == "pooled") & (fact.conf == 1.0)]
            .rejection_rate.mean()),
        permutation_within_deviation=perm["within_max_abs_deviation"],
        permutation_invariant=bool(perm["within_max_abs_deviation"] <= 1e-12),
        benchmark_matches=(abs(bench["beta1"] - bench["expected"]["beta1"]) < 1e-9
                           and abs(bench["se_cr1"] - bench["expected"]["se_cr1"]) < 1e-9
                           and abs(bench["t_obs"] - bench["expected"]["t_obs"]) < 1e-9),
    )
    with open(os.path.join(args.out, "boostrap_factorial_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=float)
    print(json.dumps({k: summary[k] for k in ("runtime_sec", "acceptance")}, indent=2))


if __name__ == "__main__":
    main()
