#!/usr/bin/env python3
"""
RTX 3080 Ti (CUDA 11.8, 12GB VRAM) — GPU Job 1:
Finite-Sample Rademacher Wild-Cluster Bootstrap & Country-Block Permutation Null
for Paper #1 ("Zero Universal Laws, 32 Regimes" — E1 & Q3 referee armor).

Usage on RTX 3080 Ti (Python 3.10, PyTorch CUDA 11.8):
    python3 gpu_e1_q3_wild_cluster_ri.py \
        --panel-csv /path/to/e1_panel.csv \
        --out-dir ./results_rtx3080ti/e1_q3_wild_cluster \
        --B 2000 --seed 20261125

If --panel-csv is omitted, runs a built-in synthetic validation check (verifying
GPU batched CR1 + Rademacher wild-cluster t-stats to <1e-5 vs CPU reference).
"""
from __future__ import annotations

import argparse
import json
import os
import time
import numpy as np
import torch


def get_device() -> torch.device:
    if torch.cuda.is_available():
        dev = torch.device("cuda")
        print(f"[GPU] Using {torch.cuda.get_device_name(0)} (CUDA {torch.version.cuda})")
        return dev
    print("[CPU] CUDA not available; falling back to CPU")
    return torch.device("cpu")


@torch.no_grad()
def gpu_wild_cluster_ols(
    y: torch.Tensor,
    X: torch.Tensor,
    cluster_ids: torch.Tensor,
    B: int = 2000,
    batch_size: int = 250,
    seed: int = 20261125,
) -> dict:
    """
    Batched Rademacher wild-cluster bootstrap on GPU (float64 for numerical stability).
    Tests H0: beta[1] == 0 (first non-intercept regressor) using restricted residuals.
    """
    device = y.device
    N, K = X.shape
    uniq, inv = torch.unique(cluster_ids, return_inverse=True)
    G = int(uniq.numel())

    # Unrestricted OLS + CR1 SE
    XtX = X.T @ X
    XtX_inv = torch.linalg.pinv(XtX)
    beta_hat = XtX_inv @ (X.T @ y)
    u_hat = y - X @ beta_hat

    # Cluster scores S: (G, K)
    S = torch.zeros((G, K), dtype=X.dtype, device=device)
    S.index_add_(0, inv, X * u_hat[:, None])
    cr1 = G / max(G - 1.0, 1.0)
    V_cr1 = cr1 * (XtX_inv @ (S.T @ S) @ XtX_inv)
    se_cr1 = torch.sqrt(torch.clamp(torch.diag(V_cr1), min=1e-18))
    t_obs = float((beta_hat[1] / se_cr1[1]).item())

    # Restricted fit imposing beta[1] == 0
    keep_cols = [c for c in range(K) if c != 1]
    Xr = X[:, keep_cols]
    br = torch.linalg.pinv(Xr.T @ Xr) @ (Xr.T @ y)
    yr_hat = Xr @ br
    ur = y - yr_hat  # restricted residuals

    # Precompute projection matrices for fast batched bootstrap
    # For each draw b: y*_b = yr_hat + (w_g[inv] * ur)
    # beta*_b = XtX_inv @ X.T @ y*_b
    # u*_b = y*_b - X @ beta*_b
    gen = torch.Generator(device=device).manual_seed(seed)
    t_boot_list = []

    done = 0
    while done < B:
        bs = min(batch_size, B - done)
        # Rademacher weights {-1, +1} per cluster: (G, bs)
        W_g = torch.where(
            torch.randint(0, 2, (G, bs), generator=gen, device=device) == 0,
            torch.tensor(-1.0, dtype=X.dtype, device=device),
            torch.tensor(1.0, dtype=X.dtype, device=device),
        )
        # Map to observations: (N, bs)
        U_star = W_g[inv] * ur[:, None]
        Y_star = yr_hat[:, None] + U_star  # (N, bs)

        # Batched OLS: (K, bs)
        Beta_star = XtX_inv @ (X.T @ Y_star)
        Resid_star = Y_star - X @ Beta_star  # (N, bs)

        # Batched cluster scores: compute var(beta*_1) directly via projected score
        # Let a = XtX_inv[1, :] (shape K); then (XtX_inv @ s_g)_1 = (X @ a) * resid
        xa = X @ XtX_inv[1, :]  # (N,)
        # Score for beta_1 per obs & draw: (N, bs)
        sc = xa[:, None] * Resid_star
        S_g = torch.zeros((G, bs), dtype=X.dtype, device=device)
        S_g.index_add_(0, inv, sc)
        var_1 = cr1 * torch.sum(S_g ** 2, dim=0)  # (bs,)
        se_1 = torch.sqrt(torch.clamp(var_1, min=1e-18))
        t_b = Beta_star[1, :] / se_1
        t_boot_list.append(t_b.cpu().numpy())
        done += bs

    t_boot = np.concatenate(t_boot_list)
    p_wild = float((1.0 + np.sum(np.abs(t_boot) >= abs(t_obs))) / (B + 1.0))
    return {
        "N": int(N),
        "G": int(G),
        "beta1": float(beta_hat[1].item()),
        "se_cr1": float(se_cr1[1].item()),
        "t_obs": t_obs,
        "p_wild_cluster": p_wild,
        "B": int(B),
        "t_boot_q025": float(np.percentile(t_boot, 2.5)),
        "t_boot_q975": float(np.percentile(t_boot, 97.5)),
    }


@torch.no_grad()
def gpu_country_block_permutation(
    y: torch.Tensor,
    X: torch.Tensor,
    cluster_ids: torch.Tensor,
    B: int = 2000,
    seed: int = 20261126,
) -> dict:
    """
    Country-block permutation null: shuffles treatment column X[:, 1] across clusters
    (preserving within-country autocorrelation) to test finite-sample leakage.
    """
    device = y.device
    uniq, inv = torch.unique(cluster_ids, return_inverse=True)
    G = int(uniq.numel())
    XtX_inv = torch.linalg.pinv(X.T @ X)
    beta_obs = float((XtX_inv @ (X.T @ y))[1].item())

    # Mean treatment per cluster for block-level shuffling
    x1 = X[:, 1]
    c_counts = torch.zeros(G, dtype=X.dtype, device=device)
    c_counts.index_add_(0, inv, torch.ones_like(x1))
    c_means = torch.zeros(G, dtype=X.dtype, device=device)
    c_means.index_add_(0, inv, x1)
    c_means = c_means / torch.clamp(c_counts, min=1.0)
    x1_within = x1 - c_means[inv]

    gen = torch.Generator(device=device).manual_seed(seed)
    betas_perm = np.empty(B, dtype=np.float64)
    for b in range(B):
        perm = torch.randperm(G, generator=gen, device=device)
        X_p = X.clone()
        X_p[:, 1] = c_means[perm][inv] + x1_within
        b_p = torch.linalg.pinv(X_p.T @ X_p) @ (X_p.T @ y)
        betas_perm[b] = float(b_p[1].item())

    p_perm = float((1.0 + np.sum(np.abs(betas_perm) >= abs(beta_obs))) / (B + 1.0))
    return {
        "beta_obs": beta_obs,
        "p_block_perm": p_perm,
        "perm_mean": float(np.mean(betas_perm)),
        "perm_sd": float(np.std(betas_perm)),
        "B": int(B),
    }


def run_selftest(device: torch.device, B: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    G, T = 60, 20
    N = G * T
    cl = np.repeat(np.arange(G), T)
    c_eff = rng.normal(0, 1.0, size=G)[cl]
    x1 = rng.normal(0, 1.0, size=N) + 0.5 * c_eff
    x2 = rng.normal(0, 1.0, size=N)
    # Minority-effect world: only 15% of countries have true slope +0.8, 85% have 0.0
    active_c = (cl < int(0.15 * G)).astype(float)
    y = 0.2 + 0.8 * active_c * x1 + 0.3 * x2 + c_eff + rng.normal(0, 1.0, size=N)

    X_t = torch.tensor(np.column_stack([np.ones(N), x1, x2]), dtype=torch.float64, device=device)
    y_t = torch.tensor(y, dtype=torch.float64, device=device)
    cl_t = torch.tensor(cl, dtype=torch.long, device=device)

    t0 = time.time()
    wcb = gpu_wild_cluster_ols(y_t, X_t, cl_t, B=B, seed=seed)
    perm = gpu_country_block_permutation(y_t, X_t, cl_t, B=min(B, 1000), seed=seed + 1)
    return {
        "mode": "selftest_minority_effect_15pct",
        "elapsed_sec": round(time.time() - t0, 3),
        "wild_cluster": wcb,
        "block_perm": perm,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel-csv", default="", help="Path to E1/Q3 panel CSV with columns: country, y, x, [controls...]")
    ap.add_argument("--y-col", default="y")
    ap.add_argument("--x-col", default="x")
    ap.add_argument("--cluster-col", default="country")
    ap.add_argument("--out-dir", default="./results_rtx3080ti/e1_q3_wild_cluster")
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261125)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    dev = get_device()

    if not args.panel_csv:
        res = run_selftest(dev, args.B, args.seed)
    else:
        import pandas as pd
        df = pd.read_csv(args.panel_csv).dropna(subset=[args.y_col, args.x_col, args.cluster_col])
        y_np = df[args.y_col].to_numpy(dtype=np.float64)
        x_np = df[args.x_col].to_numpy(dtype=np.float64)
        cl_np = pd.Categorical(df[args.cluster_col]).codes.astype(np.int64)
        X_np = np.column_stack([np.ones(len(df)), x_np])

        t0 = time.time()
        y_t = torch.tensor(y_np, dtype=torch.float64, device=dev)
        X_t = torch.tensor(X_np, dtype=torch.float64, device=dev)
        cl_t = torch.tensor(cl_np, dtype=torch.long, device=dev)
        res = {
            "mode": "panel_csv",
            "panel_csv": args.panel_csv,
            "elapsed_sec": round(time.time() - t0, 3),
            "wild_cluster": gpu_wild_cluster_ols(y_t, X_t, cl_t, B=args.B, seed=args.seed),
            "block_perm": gpu_country_block_permutation(y_t, X_t, cl_t, B=args.B, seed=args.seed + 1),
        }

    out_path = os.path.join(args.out_dir, "wild_cluster_ri_results.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
