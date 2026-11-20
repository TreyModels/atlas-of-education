#!/usr/bin/env python
"""SIMULATED cluster 5 — geo fragmentation toy simulation. Stipulated parameters only.

No observed data is read. Nothing here is calibrated, evidence, or a historical test.
All outputs are labelled SIMULATED.
"""
import csv, hashlib, json, os, sys
from datetime import datetime, timezone

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, "results")
os.makedirs(RES, exist_ok=True)

# ---- FROZEN stipulated parameters (do not change) ----
R, DMAX, D0, T = 0.08, 1.10, 0.10, 80
CROSS = 0.50
CAP = 2.0
CEIL_LO, CEIL_HI = 0.35, 1.00
BIND_CEIL = 0.40
BASE_SEED = 20261120
N_SEEDS = 200
K_GRID = [1, 2, 4, 8, 16, 32]
F_GRID = [0.0, 0.25, 0.50, 0.75, 1.0]
K15 = 8
CLUSTER = "5_geo_fragmentation_sim"
NOTE = "SIMULATED — stipulated toy, not evidence"

# RNG call pattern (documented in RUN_MANIFEST.json):
#   Per (experiment, seed_index i): rng = numpy.random.Generator(numpy.random.PCG64(BASE_SEED + 1000000*experiment_block + i))
#   block 1 = X13/X14, block 2 = X15.
#   X13/X14: ceilings = rng.uniform(CEIL_LO, CEIL_HI, size=K_MAX) once per seed;
#            cell K uses the FIRST K of that vector (paired across K).
#   X15:     ceilings = rng.uniform(CEIL_LO, CEIL_HI, size=K15) once per seed;
#            binding set = first round(f*K15) entries after rng.permutation(K15)
#            (permutation call made once per seed, same seed stream).
# Demand path is deterministic and seed-independent.
K_MAX = max(K_GRID)
BLOCK_X13, BLOCK_X15 = 1, 2

def demand_path():
    d = np.empty(T + 1)
    d[0] = D0
    for t in range(T):
        d[t + 1] = d[t] * R * (1.0 - d[t] / DMAX)
    return d

D = demand_path()

def crossing(ceils):
    """ceils: array of ceilings (cap_k = CAP, non-binding). Returns crossing t or None."""
    a = np.array([np.minimum(d, np.minimum(CAP, ceils)).mean() for d in D])
    idx = np.nonzero(a >= CROSS)[0]
    return int(idx[0]) if idx.size else None

def x13_x14():
    cross = {K: [] for K in K_GRID}
    vol = {K: [] for K in K_GRID}
    for i in range(N_SEEDS):
        rng = np.random.Generator(np.random.PCG64(BASE_SEED + 1000000 * BLOCK_X13 + i))
        ceils_all = rng.uniform(CEIL_LO, CEIL_HI, K_MAX)
        for K in K_GRID:
            c = crossing(ceils_all[:K])
            cross[K].append(c)
            Tend = c if c is not None else T
            a = np.array([np.minimum(d, np.minimum(CAP, ceils_all[:K])).mean() for d in D])
            diffs = np.diff(a[: Tend + 1])
            vol[K].append(float(np.std(diffs, ddof=1)) if len(diffs) > 1 else 0.0)
    return cross, vol

def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    # average ranks for ties
    def avg_ranks(v):
        sv = np.sort(np.unique(v[~np.isnan(v)]))
        r = np.full_like(v, np.nan, dtype=float)
        for u in sv:
            m = v == u
            idx = np.nonzero(m)[0]
            r[m] = (idx.min() + idx.max() + 1) / 2.0
        return r
    rx, ry = avg_ranks(x), avg_ranks(y)
    rx, ry = rx - rx.mean(), ry - ry.mean()
    den = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / den) if den > 0 else float("nan")

def boot_ci(vals, stat, nb=1000, seed=BASE_SEED + 77):
    vals = np.array(vals, dtype=float)
    rng = np.random.Generator(np.random.PCG64(seed))
    n = len(vals)
    stats = []
    for _ in range(nb):
        s = vals[rng.integers(0, n, n)]
        stats.append(stat(s))
    stats = np.array(stats, float)
    return float(np.nanpercentile(stats, 2.5)), float(np.nanpercentile(stats, 97.5))

def q(vals, p):
    v = np.array([x for x in vals if x is not None], float)
    return float(np.percentile(v, p)) if v.size else float("nan")

def pct_cens(vals):
    return 100.0 * sum(1 for x in vals if x is None) / len(vals)

def med_of(vals):
    v = np.array([x for x in vals if x is not None], float)
    return float(np.median(v)) if v.size else float("nan")

def main():
    # ---------------- X13 + X14 ----------------
    cross, vol = x13_x14()
    x13_rows, seed_rows = [], []
    for K in K_GRID:
        x13_rows.append(dict(K=K, median=q(cross[K], 50), q25=q(cross[K], 25),
                             q75=q(cross[K], 75), pct_censored=round(pct_cens(cross[K]), 1),
                             n_seeds=N_SEEDS))
        for i, c in enumerate(cross[K]):
            seed_rows.append(dict(K=K, seed_index=i, crossing_year=">80" if c is None else c,
                                  censored=1 if c is None else 0))
    delta = med_of(cross[32]) - med_of(cross[1])
    se_delta_lo, se_delta_hi = boot_ci(
        list(zip(cross[1], cross[32])),
        lambda s: (np.median([b for a, b in s if b is not None]) if True else np.nan)
                  - (np.median([a for a, b in s if a is not None])),
    )
    se_delta = (se_delta_hi - se_delta_lo) / (2 * 1.96) if np.isfinite(se_delta_hi) else float("nan")

    # X14 volatility ratio: ratio of medians across seeds
    v1, v32 = np.array(vol[1]), np.array(vol[32])
    V = float(np.median(v1) / np.median(v32))
    v_lo, v_hi = boot_ci(
        list(zip(vol[1], vol[32])),
        lambda s: (np.median([b for a, b in s])) / (np.median([a for a, b in s])),
    )
    se_V = (v_hi - v_lo) / (2 * 1.96)

    x14_rows = [dict(K=K, median_volatility=med_of(vol[K]),
                     q25_volatility=q(vol[K], 25), q75_volatility=q(vol[K], 75),
                     pct_censored=round(pct_cens(cross[K]), 1), n_seeds=N_SEEDS)
                for K in K_GRID]

    def x13_verdict(d):
        if d >= 3: return "SIMULATED-THRESHOLD-MET"
        if d >= 1: return "PARTIAL"
        return "SIMULATED-THRESHOLD-MISSED"
    def x14_verdict(v):
        if v >= 1.5: return "SIMULATED-THRESHOLD-MET"
        if v >= 1.1: return "PARTIAL"
        return "SIMULATED-THRESHOLD-MISSED"

    # ---------------- X15 ----------------
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
    x15_rows = []
    for f in F_GRID:
        x15_rows.append(dict(f=f, median=q(cross15[f], 50), q25=q(cross15[f], 25),
                             q75=q(cross15[f], 75), pct_censored=round(pct_cens(cross15[f]), 1),
                             n_seeds=N_SEEDS))
    # Right-censored medians are NOT imputed: cells whose median is NaN (all >80)
    # are excluded from Spearman; the exclusions are recorded in the note.
    f_fin = [f for f in F_GRID if np.isfinite(med_of(cross15[f]))]
    rho = spearman(f_fin, [med_of(cross15[f]) for f in f_fin]) if len(f_fin) >= 3 else float("nan")
    rho_excluded = [f for f in F_GRID if f not in f_fin]
    d10_0 = med_of(cross15[1.0]) - med_of(cross15[0.0])
    if np.isfinite(rho) and rho >= 0.90 and np.isfinite(d10_0) and d10_0 >= 2:
        v15 = "SIMULATED-THRESHOLD-MET"
    elif np.isfinite(rho) and rho >= 0.90:
        v15 = "PARTIAL"
    else:
        v15 = "SIMULATED-THRESHOLD-MISSED"
    d_005 = med_of(cross15[0.50]) - med_of(cross15[0.0])
    d_051 = med_of(cross15[1.0]) - med_of(cross15[0.50])
    first_half_bigger = d_005 > d_051

    # ---------------- write CSVs ----------------
    def write_csv(name, rows, cols):
        p = os.path.join(RES, name)
        with open(p, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        return p

    write_csv("X13_split_delay.csv", x13_rows,
              ["K", "median", "q25", "q75", "pct_censored", "n_seeds"])
    write_csv("X13_seed_detail.csv", seed_rows, ["K", "seed_index", "crossing_year", "censored"])
    write_csv("X14_smoothing.csv", x14_rows,
              ["K", "median_volatility", "q25_volatility", "q75_volatility", "pct_censored", "n_seeds"])
    write_csv("X15_heterogeneity_dose.csv", x15_rows,
              ["f", "median", "q25", "q75", "pct_censored", "n_seeds"])

    summary = [
        dict(experiment="X13", cluster=CLUSTER,
             question="Does splitting the system into more markets delay the ceiling crossing?",
             estimand="Delta = median crossing year (K=32) - median crossing year (K=1)",
             estimate=f"{delta:.4f}", se=f"{se_delta:.4f}",
             ci_low=f"{se_delta_lo:.4f}", ci_high=f"{se_delta_hi:.4f}", n=N_SEEDS,
             clusters=";".join(str(K) for K in K_GRID),
             threshold="Delta >= 3 years -> SIMULATED-THRESHOLD-MET; 1 <= Delta < 3 -> PARTIAL; |Delta| < 1 -> SIMULATED-THRESHOLD-MISSED",
             verdict=x13_verdict(delta), label="simulated",
             note=NOTE + "; stipulated demand recursion with r=0.08 (<1) is contractive: d_t decays monotonically from 0.10 and d_t < 0.50 for all t, so every cell is fully right-censored (>80) and the median crossing year is undefined (not imputed)"),
        dict(experiment="X14", cluster=CLUSTER,
             question="Does splitting smooth the approach (lower volatility of annual participation changes)?",
             estimand="V = median volatility (K=1) / median volatility (K=32); window t=0..crossing year (or t=79 if censored)",
             estimate=f"{V:.4f}", se=f"{se_V:.4f}", ci_low=f"{v_lo:.4f}", ci_high=f"{v_hi:.4f}",
             n=N_SEEDS, clusters=";".join(str(K) for K in K_GRID),
             threshold="V >= 1.5 -> SIMULATED-THRESHOLD-MET (SMOOTHER); 1.1 <= V < 1.5 -> PARTIAL; V < 1.1 -> SIMULATED-THRESHOLD-MISSED",
             verdict=x14_verdict(V), label="simulated",
             note=NOTE + "; no ceiling binds below the decaying stipulated demand path, so aggregate participation equals d_t in every cell and volatility is identical across K (V=1 by construction of the stipulated parameters)"),
        dict(experiment="X15", cluster=CLUSTER,
             question="Heterogeneity dose: do more binding-below-demand markets delay the crossing?",
             estimand="Spearman rho(crossing year, f) over f in {0,0.25,0.5,0.75,1.0}; plus median delay f=0 -> f=1.0",
             estimate=f"{rho:.4f}", se="", ci_low="", ci_high="", n=N_SEEDS,
             clusters=";".join(str(f) for f in F_GRID),
             threshold="rho >= 0.90 AND delay(f=0->1.0) >= 2 years -> SIMULATED-THRESHOLD-MET; rho >= 0.90 with smaller delay -> PARTIAL; rho < 0.90 -> SIMULATED-THRESHOLD-MISSED",
             verdict=v15, label="simulated",
             note=(NOTE + f"; delay(f=0->0.5)={d_005}, delay(f=0.5->1.0)={d_051}, first_half_bigger={first_half_bigger}"
                   + (f"; Spearman excludes all-censored cells f={rho_excluded} (median >80, not imputed)" if rho_excluded else ""))),
    ]
    write_csv("CLUSTER_RESULTS.csv", summary,
              ["experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low",
               "ci_high", "n", "clusters", "threshold", "verdict", "label", "note"])

    # ---------------- manifest ----------------
    def sha(p):
        with open(p, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    code_paths = [os.path.join(BASE, "code", "run.py")]
    manifest = {
        "cluster": CLUSTER,
        "status": "SIMULATED — stipulated parameters; not calibrated; not evidence",
        "parameter_vector": {
            "R": R, "DMAX": DMAX, "D0": D0, "T": T, "crossing_threshold": CROSS,
            "cap_k": CAP, "ceil_uniform": [CEIL_LO, CEIL_HI], "binding_ceil_X15": BIND_CEIL,
            "base_seed": BASE_SEED, "K_grid_X13_X14": K_GRID, "K_X15": K15,
            "f_grid_X15": F_GRID,
            "X14_window": "annual changes Delta A_t for t=1..T*, T* = crossing year, or t=79 if right-censored; SD (ddof=1) of those changes",
            "demand_path_note": "Stipulated recursion d_{t+1}=d_t*r*(1-d_t/dmax) with r=0.08 (<1) is contractive: d_t decays monotonically from 0.10 and stays below 0.50 for all t, so no crossing can occur under the frozen parameters; all cells are fully right-censored (>80) and censored medians are reported as undefined, never imputed.",
        },
        "rng": {
            "generator": "numpy.random.Generator(numpy.random.PCG64(seed))",
            "seed_formula": "seed = 20261120 + 1000000*block + seed_index; block 1 = X13/X14, block 2 = X15",
            "call_pattern": ("Per seed one uniform draw of size K_MAX=32 for X13/X14 "
                             "(cell K uses first K entries -> paired across K); for X15 one uniform draw "
                             "of size 8 plus one rng.permutation(8) per seed to choose binding markets."),
            "bootstrap": "X13/X14 bootstrap CI: PCG64(20261120+77), 1000 resamples",
        },
        "seeds_per_cell": N_SEEDS,
        "code": [{"path": "code/run.py", "sha256": sha(code_paths[0])}],
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reproducibility": "Deterministic: fixed seeds, fixed demand path, no observed data read. Re-running code/run.py must reproduce results CSVs byte-identically.",
    }
    with open(os.path.join(BASE, "RUN_MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)

    print("X13 Delta =", round(delta, 4), "verdict:", x13_verdict(delta))
    print("X14 V =", round(V, 4), "verdict:", x14_verdict(V))
    print("X15 rho =", round(rho, 4), "delay f0->f1 =", round(d10_0, 4),
          "verdict:", v15, "| first-half-delay-bigger:", first_half_bigger)
    print("DONE")

if __name__ == "__main__":
    main()
