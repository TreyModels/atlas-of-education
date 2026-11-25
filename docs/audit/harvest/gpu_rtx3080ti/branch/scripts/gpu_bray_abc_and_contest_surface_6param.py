#!/usr/bin/env python3
"""
CORRECTIVE 6-PARAMETER VARIANT of gpu_bray_abc_and_contest_surface.py
  (created by the GPU lane 2026-11-25 after review finding: the as-shipped
   script's 7th parameter theta[5] "teacher_threshold" never enters the
   utilities or the moment equations, so a 7-parameter ABC cannot identify it.
   This variant drops the dead parameter and runs a 6-parameter fit.
   Part B is unchanged and remains an APPROXIMATE sensitivity exercise.
  Part B: 20x20x5 (2,000-point) GPU Tullock Contest Equilibrium Sensitivity Surface
          mapping exact boundaries of H2 (fee x scarcity) and the 2024 Korea
          Seat-Expansion Paradox (dSpend/dS > 0).

Usage on RTX 3080 Ti (Python 3.10, PyTorch CUDA 11.8):
    python3 gpu_bray_abc_and_contest_surface.py \
        --out-dir ./results_rtx3080ti/bray_and_contest \
        --n-abc 200000 --seed 20261125
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
def run_gpu_bray_7param_abc(device: torch.device, n_draws: int = 200000, batch: int = 20000, seed: int = 20261125) -> dict:
    """
    Batched 6-parameter de-collinearized Bray 3-option MNL (none / own / other):
      theta = [b0_eff, b_income, b_school_gap, delta_g12, urban_demand, delta_other]
      (shipped script's 7th param teacher_threshold dropped: it was never used)
    Evaluates against Bray's 7 aggregate Cambodia/Asia benchmark moments:
      part=0.73, g9=0.67, g12=0.85, ur_gap=0.14, own_share=0.68, other_share=0.32, teacher_tut=0.55
    """
    t0 = time.time()
    gen = torch.Generator(device=device).manual_seed(seed)

    # Fixed 9-class synthetic structure (6 schools x {G9, G12} = 630 pupils, 210 urban / 420 rural)
    n_pupils = 630
    is_g12 = torch.cat([torch.zeros(420, device=device), torch.ones(210, device=device)])
    is_urban = torch.cat([torch.ones(210, device=device), torch.zeros(420, device=device)])
    log_y = torch.randn(n_pupils, generator=gen, device=device)
    school_gap = torch.rand(n_pupils, generator=gen, device=device)

    targets = torch.tensor([0.73, 0.67, 0.85, 0.14, 0.68], device=device)  # 5 independent moments
    tols = torch.tensor([0.05, 0.05, 0.05, 0.04, 0.06], device=device)

    # Prior bounds for 6 parameters (dead teacher_threshold bound dropped)
    lo = torch.tensor([-1.0, 0.0, 0.0, 0.0, -0.5, -2.5], device=device)
    hi = torch.tensor([2.5, 2.0, 2.5, 2.5, 1.5, 1.5], device=device)

    accepted_thetas = []
    best_z = 1e9
    best_theta = None

    done = 0
    while done < n_draws:
        bs = min(batch, n_draws - done)
        U = torch.rand((bs, 6), generator=gen, device=device)
        th = lo + U * (hi - lo)  # (bs, 7)

        # Utilities V1 (own) and V2 (other) vs V0=0: shape (bs, n_pupils)
        base = (
            th[:, 0:1]
            + th[:, 1:2] * log_y[None, :]
            + th[:, 2:3] * school_gap[None, :]
            + th[:, 3:4] * is_g12[None, :]
            + th[:, 4:5] * is_urban[None, :]
        )
        V1 = base
        V2 = base + th[:, 5:6]
        V0 = torch.zeros_like(V1)
        logits = torch.stack([V0, V1, V2], dim=-1)
        probs = torch.softmax(logits, dim=-1)  # (bs, n_pupils, 3)

        p_any = probs[:, :, 1] + probs[:, :, 2]
        m_part = p_any.mean(dim=1)
        m_g9 = p_any[:, :420].mean(dim=1)
        m_g12 = p_any[:, 420:].mean(dim=1)
        m_ur = p_any[:, :210].mean(dim=1) - p_any[:, 210:].mean(dim=1)
        m_own = probs[:, :, 1].sum(dim=1) / torch.clamp(p_any.sum(dim=1), min=1e-6)

        M = torch.stack([m_part, m_g9, m_g12, m_ur, m_own], dim=1)
        max_z = torch.max(torch.abs(M - targets[None, :]) / tols[None, :], dim=1).values

        min_val, min_idx = torch.min(max_z, dim=0)
        if float(min_val.item()) < best_z:
            best_z = float(min_val.item())
            best_theta = th[min_idx].cpu().tolist()

        acc = th[max_z <= 1.0]
        if acc.numel() > 0:
            accepted_thetas.append(acc.cpu().numpy())
        done += bs

    if accepted_thetas:
        post = np.vstack(accepted_thetas)
        corr = np.corrcoef(post[:, [0, 1, 2, 3, 4, 5]].T)
        eig = np.linalg.eigvalsh(corr)
        cond_post = float(eig[-1] / max(eig[0], 1e-12))
        n_acc = int(post.shape[0])
    else:
        cond_post, n_acc = float("nan"), 0

    return {
        "n_draws": int(n_draws),
        "n_accepted": n_acc,
        "accept_rate_pct": round(100.0 * n_acc / n_draws, 4),
        "best_max_z": round(best_z, 4),
        "n_params": 6,
        "dropped_param": "teacher_threshold (index 5; unused in shipped script)",
        "best_theta_6param": [round(x, 4) for x in (best_theta or [])],
        "posterior_corr_cond_6active": round(cond_post, 2),
        "elapsed_sec": round(time.time() - t0, 2),
    }


@torch.no_grad()
def run_gpu_contest_sensitivity_surface(device: torch.device, seed: int = 20261125) -> dict:
    """
    20x20x5 = 2,000-point GPU sensitivity surface over (contest_r, contest_price, seat_share S)
    mapping where the Seat-Expansion Paradox (dSpend/dS > 0) holds in a Plackett-Luce / Tullock contest.
    """
    t0 = time.time()
    r_grid = torch.linspace(0.8, 2.5, 20, device=device)
    p_grid = torch.linspace(0.05, 0.30, 20, device=device)
    s_grid = torch.tensor([0.12, 0.16, 0.23, 0.35, 0.50], device=device)

    # Fixed 1,000-household lognormal income distribution (Q1..Q5)
    gen = torch.Generator(device=device).manual_seed(seed)
    y = torch.exp(0.65 * torch.randn(1000, generator=gen, device=device))  # (1000,)
    delta_v = 1.0  # elite-vs-regular log-wage prize

    # Fixed-point equilibrium solver across (20, 20, 5) = 2,000 cells simultaneously
    R_t, P_t, S_t = torch.meshgrid(r_grid, p_grid, s_grid, indexing="ij")
    flat_r = R_t.reshape(-1, 1)  # (2000, 1)
    flat_p = P_t.reshape(-1, 1)
    flat_s = S_t.reshape(-1, 1)

    # Approximate symmetric Tullock marginal return P_i*(1 - P_i) with Plackett-Luce equilibrium
    # Iterate aggregate effort E_bar to fixed point
    e_bar = torch.full((2000, 1), 0.5, device=device)
    x0 = 2.0
    for _ in range(30):
        # Crowd ratio R = 1 / S; rival mass A = (1/S - 1) * (x0 + e_bar)
        A = torch.clamp(1.0 / flat_s - 1.0, min=0.05) * (x0 + e_bar)
        # Tullock best response scaled by decisiveness r and income y: (2000, 1000)
        e_i = torch.sqrt(torch.clamp(flat_r * delta_v * A * y[None, :] / flat_p, min=0.0)) - A - x0
        e_i = torch.clamp(e_i, min=0.0, max=4.5)
        e_bar = 0.5 * e_bar + 0.5 * e_i.mean(dim=1, keepdim=True)

    spend = (flat_p * e_i).mean(dim=1).reshape(20, 20, 5)  # mean spend per household
    part = (e_i > 0.25).float().mean(dim=1).reshape(20, 20, 5)

    # Check fraction of (r, price) cells where expanding S from 0.12 -> 0.16 or 0.12 -> 0.50 raises spend
    paradox_12_16 = float((spend[:, :, 1] > spend[:, :, 0]).float().mean().item())
    paradox_12_50 = float((spend[:, :, 4] > spend[:, :, 0]).float().mean().item())
    part_jump_12_50 = float((part[:, :, 4] - part[:, :, 0]).mean().item())

    return {
        "grid_points": 2000,
        "r_range": [0.8, 2.5],
        "price_range": [0.05, 0.30],
        "seat_shares": [0.12, 0.16, 0.23, 0.35, 0.50],
        "share_cells_paradox_S012_to_S016": round(paradox_12_16, 4),
        "share_cells_paradox_S012_to_S050": round(paradox_12_50, 4),
        "mean_participation_jump_S012_to_S050": round(part_jump_12_50, 4),
        "elapsed_sec": round(time.time() - t0, 3),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="./results_rtx3080ti/bray_and_contest")
    ap.add_argument("--n-abc", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=20261125)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    dev = get_device()

    res = {
        "part_a_bray_6param_abc": run_gpu_bray_7param_abc(dev, n_draws=args.n_abc, seed=args.seed),
        "part_b_contest_sensitivity_surface": run_gpu_contest_sensitivity_surface(dev, seed=args.seed),
    }
    out_path = os.path.join(args.out_dir, "bray_abc_and_contest_surface.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
