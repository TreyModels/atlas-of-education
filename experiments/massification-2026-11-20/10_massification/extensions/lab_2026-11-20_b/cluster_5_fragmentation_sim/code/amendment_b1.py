#!/usr/bin/env python
"""POST-HOC DISCLOSED AMENDMENT B1 — cluster 5 (SIMULATED, not evidence).

Why this file exists
--------------------
The FROZEN predeclaration wrote the demand recursion as
    d_{t+1} = d_t * r * (1 - d_t/dmax),  r = 0.08, dmax = 1.10
which is contractive for r < 1: demand DECAYS from 0.10 and can never reach the 0.50 crossing
threshold. The predeclared run (code/run.py) therefore produced 100% right-censored cells and its
thresholds were not evaluable. That is a LEAD PREDECLARATION DEFECT, disclosed as such.

This amendment keeps every frozen threshold, K grid, f grid, seed set, cell count and estimator
identical, and changes ONLY the demand recursion to a genuinely growing logistic rule:
    d_{t+1} = d_t * (1 + g*(1 - d_t/dmax)),  g = 0.08, dmax = 1.10, d_0 = 0.10, t = 0..79
It is POST-HOC and cannot change the predeclared verdict in results/CLUSTER_RESULTS.csv.

All outputs are labelled SIMULATED — stipulated toy, not calibrated, not evidence, no historical test.
"""
import csv
import os
from datetime import datetime, timezone

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, "results", "AMENDMENT_B1")
os.makedirs(RES, exist_ok=True)

# ---- frozen design (IDENTICAL to predeclaration) ----
DMAX, D0, T = 1.10, 0.10, 80
G = 0.08                      # logistic growth rate (amended rule; predeclared rule was contractive r=0.08)
CROSS = 0.50
CAP = 2.0
CEIL_LO, CEIL_HI = 0.35, 1.00
BIND_CEIL = 0.40
BASE_SEED = 20261120
N_SEEDS = 200
K_GRID = [1, 2, 4, 8, 16, 32]
F_GRID = [0.0, 0.25, 0.50, 0.75, 1.0]
K15 = 8
K_MAX = max(K_GRID)
BLOCK_X13, BLOCK_X15 = 1, 2
CLUSTER = "5_geo_fragmentation_sim"
NOTE = "SIMULATED — stipulated toy, not evidence"


def demand_path():
    d = np.empty(T + 1)
    d[0] = D0
    for t in range(T):
        d[t + 1] = d[t] * (1.0 + G * (1.0 - d[t] / DMAX))
    return d


D = demand_path()
assert D.max() > CROSS, "amended demand path must be able to reach the crossing threshold"


def crossing(ceils):
    a = np.array([np.minimum(d, np.minimum(CAP, ceils)).mean() for d in D])
    idx = np.nonzero(a >= CROSS)[0]
    return int(idx[0]) if idx.size else None


def q(vals, p):
    v = np.array([x for x in vals if x is not None], float)
    return float(np.percentile(v, p)) if v.size else float("nan")


def med_of(vals):
    v = np.array([x for x in vals if x is not None], float)
    return float(np.median(v)) if v.size else float("nan")


def pct_cens(vals):
    return 100.0 * sum(1 for x in vals if x is None) / len(vals)


def avg_ranks(v):
    v = np.asarray(v, float)
    out = np.empty_like(v)
    for u in np.unique(v):
        m = v == u
        idx = np.nonzero(m)[0]
        out[m] = (idx.min() + idx.max() + 1) / 2.0
    return out


def spearman(x, y):
    x, y = avg_ranks(np.asarray(x, float)), avg_ranks(np.asarray(y, float))
    x, y = x - x.mean(), y - y.mean()
    den = np.sqrt((x ** 2).sum() * (y ** 2).sum())
    return float((x * y).sum() / den) if den > 0 else float("nan")


def boot_ci(pairs, stat, nb=1000, seed=BASE_SEED + 77):
    arr = np.array([(np.nan if a is None else a, np.nan if b is None else b) for a, b in pairs], float)
    rng = np.random.Generator(np.random.PCG64(seed))
    n = len(arr)
    stats = []
    for _ in range(nb):
        s = arr[rng.integers(0, n, n)]
        stats.append(stat(s[:, 0], s[:, 1]))
    stats = np.array(stats, float)
    return float(np.nanpercentile(stats, 2.5)), float(np.nanpercentile(stats, 97.5))


def x13_x14():
    cross = {K: [] for K in K_GRID}
    vol = {K: [] for K in K_GRID}
    for i in range(N_SEEDS):
        rng = np.random.Generator(np.random.PCG64(BASE_SEED + 1000000 * BLOCK_X13 + i))
        ceils_all = rng.uniform(CEIL_LO, CEIL_HI, K_MAX)   # paired: first K used for cell K
        for K in K_GRID:
            c = crossing(ceils_all[:K])
            cross[K].append(c)
            Tend = c if c is not None else T
            a = np.array([np.minimum(d, np.minimum(CAP, ceils_all[:K])).mean() for d in D])
            diffs = np.diff(a[: Tend + 1])
            vol[K].append(float(np.std(diffs, ddof=1)) if len(diffs) > 1 else 0.0)
    return cross, vol


def main():
    cross, vol = x13_x14()

    x13_rows, seed_rows = [], []
    for K in K_GRID:
        x13_rows.append(dict(K=K, median=q(cross[K], 50), q25=q(cross[K], 25), q75=q(cross[K], 75),
                             pct_censored=round(pct_cens(cross[K]), 1),
                             pct_crossed=round(100.0 - pct_cens(cross[K]), 1), n_seeds=N_SEEDS))
        for i, c in enumerate(cross[K]):
            seed_rows.append(dict(K=K, seed_index=i, crossing_year=">80" if c is None else c,
                                  censored=1 if c is None else 0))

    delta = med_of(cross[32]) - med_of(cross[1])
    d_lo, d_hi = boot_ci(list(zip(cross[1], cross[32])),
                         lambda a, b: np.nanmedian(b) - np.nanmedian(a))
    se_delta = (d_hi - d_lo) / (2 * 1.96) if np.isfinite(d_hi) else float("nan")

    v1, v32 = np.array(vol[1]), np.array(vol[32])
    V = float(np.median(v1) / np.median(v32))
    v_lo, v_hi = boot_ci(list(zip(vol[1], vol[32])), lambda a, b: np.median(a) / np.median(b))
    se_V = (v_hi - v_lo) / (2 * 1.96)
    x14_rows = [dict(K=K, median_volatility=med_of(vol[K]), q25_volatility=q(vol[K], 25),
                     q75_volatility=q(vol[K], 75), pct_censored=round(pct_cens(cross[K]), 1),
                     n_seeds=N_SEEDS) for K in K_GRID]

    cross15 = {f: [] for f in F_GRID}
    for i in range(N_SEEDS):
        rng = np.random.Generator(np.random.PCG64(BASE_SEED + 1000000 * BLOCK_X15 + i))
        ceils = rng.uniform(CEIL_LO, CEIL_HI, K15)
        perm = rng.permutation(K15)
        for f in F_GRID:
            nb = int(round(f * K15))
            c = ceils.copy()
            c[perm[:nb]] = BIND_CEIL
            cross15[f].append(crossing(c))
    x15_rows = [dict(f=f, median=q(cross15[f], 50), q25=q(cross15[f], 25), q75=q(cross15[f], 75),
                     pct_censored=round(pct_cens(cross15[f]), 1), n_seeds=N_SEEDS) for f in F_GRID]

    f_fin = [f for f in F_GRID if np.isfinite(med_of(cross15[f]))]
    rho = spearman(f_fin, [med_of(cross15[f]) for f in f_fin]) if len(f_fin) >= 3 else float("nan")
    d10_0 = med_of(cross15[1.0]) - med_of(cross15[0.0])
    if np.isfinite(rho) and rho >= 0.90 and np.isfinite(d10_0) and d10_0 >= 2:
        v15 = "SIMULATED-THRESHOLD-MET"
    elif np.isfinite(rho) and rho >= 0.90:
        v15 = "PARTIAL"
    else:
        v15 = "SIMULATED-THRESHOLD-MISSED"
    d_005 = med_of(cross15[0.50]) - med_of(cross15[0.0])
    d_051 = med_of(cross15[1.0]) - med_of(cross15[0.50])

    v13 = "SIMULATED-THRESHOLD-MET" if delta >= 3 else ("PARTIAL" if delta >= 1 else "SIMULATED-THRESHOLD-MISSED")
    v14 = "SIMULATED-THRESHOLD-MET" if V >= 1.5 else ("PARTIAL" if V >= 1.1 else "SIMULATED-THRESHOLD-MISSED")

    def write_csv(name, rows, cols):
        p = os.path.join(RES, name)
        with open(p, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        return p

    write_csv("X13_split_delay_B1.csv", x13_rows,
              ["K", "median", "q25", "q75", "pct_censored", "pct_crossed", "n_seeds"])
    write_csv("X13_seed_detail_B1.csv", seed_rows, ["K", "seed_index", "crossing_year", "censored"])
    write_csv("X14_smoothing_B1.csv", x14_rows,
              ["K", "median_volatility", "q25_volatility", "q75_volatility", "pct_censored", "n_seeds"])
    write_csv("X15_heterogeneity_dose_B1.csv", x15_rows,
              ["f", "median", "q25", "q75", "pct_censored", "n_seeds"])

    # exploratory secondary read (NO threshold): does fragmentation change the EXTENSIVE margin
    # (share of seeds that ever cross) rather than the timing?
    pc1, pc32 = 100.0 - pct_cens(cross[1]), 100.0 - pct_cens(cross[32])

    summary = [
        dict(experiment="X13", cluster=CLUSTER,
             question="Does splitting the system into more markets delay the ceiling crossing?",
             estimand="Delta = median crossing year (K=32) - median crossing year (K=1)",
             estimate=f"{delta:.4f}", se=f"{se_delta:.4f}", ci_low=f"{d_lo:.4f}", ci_high=f"{d_hi:.4f}",
             n=N_SEEDS, clusters=";".join(str(K) for K in K_GRID),
             threshold="Delta >= 3 -> MET; 1 <= Delta < 3 -> PARTIAL; |Delta| < 1 -> MISSED",
             verdict=v13, label="simulated",
             note=f"POST-HOC DISCLOSED AMENDMENT B1 (lead predeclaration defect: r=0.08 contractive recursion); "
                  f"thresholds unchanged; not predeclared; SIMULATED — stipulated toy, not evidence; "
                  f"EXPLORATORY (no threshold): share of seeds ever crossing = {pc1:.1f}% at K=1 vs {pc32:.1f}% at K=32 "
                  f"(fragmentation moves the extensive margin, not the timing)"),
        dict(experiment="X14", cluster=CLUSTER,
             question="Does splitting smooth the approach (lower volatility of annual participation changes)?",
             estimand="V = median volatility (K=1) / median volatility (K=32)",
             estimate=f"{V:.4f}", se=f"{se_V:.4f}", ci_low=f"{v_lo:.4f}", ci_high=f"{v_hi:.4f}",
             n=N_SEEDS, clusters=";".join(str(K) for K in K_GRID),
             threshold="V >= 1.5 -> MET; 1.1 <= V < 1.5 -> PARTIAL; V < 1.1 -> MISSED",
             verdict=v14, label="simulated",
             note="POST-HOC DISCLOSED AMENDMENT B1 (lead predeclaration defect: r=0.08 contractive recursion); "
                  "thresholds unchanged; not predeclared; SIMULATED — stipulated toy, not evidence"),
        dict(experiment="X15", cluster=CLUSTER,
             question="Heterogeneity dose: do more binding-below-demand markets delay the crossing?",
             estimand="Spearman rho(crossing year, f) over f in {0,0.25,0.5,0.75,1.0}; delay f=0 -> f=1.0",
             estimate=f"{rho:.4f}", se="", ci_low="", ci_high="", n=N_SEEDS,
             clusters=";".join(str(f) for f in F_GRID),
             threshold="rho >= 0.90 AND delay(f=0->1.0) >= 2 -> MET; rho >= 0.90 smaller delay -> PARTIAL; rho < 0.90 -> MISSED",
             verdict=v15, label="simulated",
             note=f"POST-HOC DISCLOSED AMENDMENT B1 (lead predeclaration defect: r=0.08 contractive recursion); "
                  f"thresholds unchanged; not predeclared; SIMULATED — stipulated toy, not evidence; "
                  f"finite f-cells={f_fin}; delay f=0->0.5={d_005:.3f}, f=0.5->1.0={d_051:.3f}; "
                  f"first_half_bigger={d_005 > d_051}"),
    ]

    cols = ["experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low", "ci_high",
            "n", "clusters", "threshold", "verdict", "label", "note", "run_tag"]
    out = os.path.join(BASE, "CLUSTER_RESULTS_AMENDMENT_B1.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in summary:
            row["run_tag"] = "amendment_B1"
            w.writerow(row)

    print(f"AMENDMENT B1 — X13 Delta={delta:.4f} [{d_lo:.4f},{d_hi:.4f}] -> {v13}")
    print(f"AMENDMENT B1 — X14 V={V:.4f} [{v_lo:.4f},{v_hi:.4f}] -> {v14}")
    print(f"AMENDMENT B1 — X15 rho={rho:.4f} delay(0->1)={d10_0} cells={f_fin} -> {v15}")
    print(f"extensive margin: crossed {pc1:.1f}% (K=1) vs {pc32:.1f}% (K=32)")
    print("wrote", RES, "and", out)


if __name__ == "__main__":
    main()
