#!/usr/bin/env python3
"""Corrected small experiment (task-23) -- SELF-CONTAINED driver.

PRE-REGISTRATION (committed BEFORE this code and before any run):
    research/records/2026-11-24-synthetic-matrix-v2/PRE_REGISTRATION_corrected.md
    at commit 77d6f23 (blob 618f4d1c..., sha256 eab63120...).

This driver implements that declared grid exactly and fixes the Codex audit findings
(messages d4b70c8e / reply c456fbb8; CORR.md on the synthetic branches):

  M1  all six declared specifications S1..S6 are implemented (the audited v2b driver ran 3);
  M2  the s=0 zero-signal world is one of the five matrix worlds;
  M3  S2 and S5 use TRUE 5-year windows (Delta_5 on t-5); only S1/S4 use 10-year windows;
  M4  ten independent country blocks: fresh country parameter draws for every block;
  M5  cluster-robust CIs over countries (CR1 sandwich inside each independent block;
      cross-block inference from the 10 independent block replicates, paired, t df=9);
      no binomial-over-cells uncertainty anywhere;
  M6  seeds, grid, code hashes and every departure are recorded in the run manifest;
This file implements the MATRIX CORE of the pre-registration.  The corrected Phase B
birth-history layer (B2-B5 fixes: WOMEN=4000, within-mother B1 with explicit
denominators, feature-specific admissibility gates, independent s=0 draws per label) is a
separate self-contained driver, run_corrected_phaseb.py, executed after this matrix run is
committed (Lead sequencing; the matrix run must not wait on Phase B).

Decision (pre-declared, no tuning): effect sizes + TOST equivalence with margin
|delta slope| <= 0.05 (equivalence only if the 90% CI of the difference lies wholly
inside +-0.05) and out-of-block predictive discrimination. "Non-significant" alone is
NOT equivalence.

SIMULATION only. Not evidence. No causal language. Old exploratory outputs are untouched.

Usage:
    python run_corrected.py            # full declared run -> results/
    python run_corrected.py --smoke    # 2-block code-path smoke -> results_smoke/
"""
import os

os.environ.update({
    "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1", "REDESIGN_BACKEND": "numpy",
})

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import platform
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import model  # noqa: E402  (kernel layer copied unmodified from the matrix record)

# ----------------------------------------------------------------------------------
# DECLARED GRID (copy of the pre-registered design; frozen before the run)
# ----------------------------------------------------------------------------------
SEED = 20261124
PREREG_COMMIT = "77d6f23"
PREREG_PATH = "research/records/2026-11-24-synthetic-matrix-v2/PRE_REGISTRATION_corrected.md"
PREREG_SHA256 = "eab6312045b6db8ef28eb8693deaf1edb9cb1ad3d15f9b08fe92541074791fb0"

# Five matrix worlds: the four literature parameterisations plus the s=0 zero-signal
# world.  "s0" is run with s=0 (theta = THETA0, NULL_FIXED), i.e. the same declared
# null construction model.py documents.
WORLDS = ("P", "S", "C", "R", "s0")
LIT_WORLDS = ("P", "S", "C", "R")
SPECS = ("S1", "S2", "S3", "S4", "S5", "S6")
SPEC_DEF = {
    "S1": "10y differences + decade FE",
    "S2": "TRUE 5y windows (Delta_5) + bin FE",
    "S3": "levels + country FE + year FE",
    "S4": "10y differences + income control",
    "S5": "TRUE 5y windows (Delta_5) + region-style control + bin FE",
    "S6": "first differences (Delta_1) + year FE",
}
DOSES = (0.0, 0.05)          # measurement-error dose ladder: 0x, 1x (sigma=0.05); 2x dropped as declared
LINKS = ("cl", "sw", "wo", "hw", "tut", "learn", "inc")
LINK_DEF = {
    "cl": "child employment (states 1,2: study+work, visible work)",
    "sw": "study + work (state 1)",
    "wo": "visible work (state 2)",
    "hw": "hidden work (state 3)",
    "tut": "tutoring",
    "learn": "learning",
    "inc": "household income",
}
MARGIN = 0.05                # pre-registered TOST margin in absolute slope units
T90_9 = 1.8331129326536335   # Student t 0.95 quantile, df = 9 (10 independent blocks)
T95_9 = 2.2621571628540993   # Student t 0.975 quantile, df = 9

# Country-type table declared by the v2 pre-registration (8 rows).  The corrected
# pre-registration says "full sample + 4 declared types" without enumerating them:
# DECLARED HERE, BEFORE THE RUN, as the first four rows of that table
# (16 countries per type, 64 countries total).
TYPES_V2 = (
    (0.45, 0.18, -0.10, 0.95, 0.10, 0.25, 0.12, 0.75),
    (0.65, 0.25, 0.10, 1.05, 0.20, 0.35, 0.20, 0.85),
    (0.35, 0.15, -0.20, 0.90, 0.05, 0.20, 0.08, 0.70),
    (0.75, 0.30, 0.20, 1.10, 0.30, 0.45, 0.30, 0.95),
    (0.55, 0.22, 0.00, 1.00, 0.15, 0.30, 0.15, 0.80),
    (0.50, 0.20, 0.05, 1.02, 0.10, 0.40, 0.25, 0.90),
    (0.60, 0.28, -0.05, 1.08, 0.25, 0.28, 0.10, 0.75),
    (0.40, 0.16, 0.15, 0.92, 0.08, 0.22, 0.05, 0.65),
)
TYPES4 = TYPES_V2[:4]
RANGES = dict(sigma_y=(0.25, 0.95), sigma_a=(0.08, 0.45), mu_y=(-0.4, 0.5), mu_a=(0.7, 1.5),
              w_child=(0.02, 0.5), shadow_cost=(0.1, 0.7), f_pub_pre=(0.0, 0.45),
              y_sub0=(0.55, 1.25))
NUIS_HASH_NOTE = "fresh nuisance draws per block from default_rng(SEED+1000+block); block sha256 recorded"

def full_config(workers):
    return dict(N=10_000, NC=64, NTYPES=4, YEARS=25, NBLOCKS=10,
                workers=workers, mode="full")


def smoke_config(workers):
    # 2-seed smoke: every code path at reduced scale; NOT a result.
    return dict(N=1_000, NC=8, NTYPES=4, YEARS=25, NBLOCKS=2,
                workers=min(workers, 4), mode="smoke")


# ----------------------------------------------------------------------------------
# utilities
# ----------------------------------------------------------------------------------
def json_safe(o):
    if isinstance(o, dict):
        return {str(k): json_safe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [json_safe(v) for v in o]
    if isinstance(o, np.ndarray):
        return json_safe(o.tolist())
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return None if (math.isnan(v) or math.isinf(v)) else v
    if isinstance(o, (np.integer, int)):
        return int(o)
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    return o


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_obj(obj):
    return hashlib.sha256(json.dumps(json_safe(obj), sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(msg):
    print(msg, flush=True)


# ----------------------------------------------------------------------------------
# matrix: country blocks, kernel series, specifications, cluster-robust fits
# ----------------------------------------------------------------------------------
def block_nuisance(b, cfg):
    """Fresh independent country parameter draws for block b (no reuse across blocks)."""
    cpt = cfg["NC"] // cfg["NTYPES"]
    rng = np.random.default_rng(SEED + 1000 + b)
    out = []
    for c in range(cfg["NC"]):
        base = dict(zip(RANGES, TYPES4[c // cpt]))
        out.append({k: float(np.clip(base[k] + rng.normal(0, 0.05), *RANGES[k])) for k in RANGES})
    return out


def nuisance_block_hash(nuis):
    arr = np.array([[nuis[c][k] for k in RANGES] for c in range(len(nuis))], dtype=np.float64)
    return hashlib.sha256(arr.tobytes()).hexdigest()


def unit_seed(b, c):
    """Kernel seed for (block, country); unique per country-block, shared across worlds so
    that worlds differ only in their declared parameterisation (paired design)."""
    return 20270101 + 100000 * b + 100 * c


def link_series(res):
    st = res["state"]
    return {
        "cl": np.isin(st, (1, 2)).mean(axis=1).astype(np.float64),
        "sw": (st == 1).mean(axis=1).astype(np.float64),
        "wo": (st == 2).mean(axis=1).astype(np.float64),
        "hw": (st == 3).mean(axis=1).astype(np.float64),
        "tut": res["tutor"].mean(axis=1).astype(np.float64),
        "learn": res["learn"].mean(axis=1).astype(np.float64),
        "inc": res["y_hh"].mean(axis=1).astype(np.float64),
        "ger": (st <= 1).mean(axis=1).astype(np.float64),
    }


def measured_series(clean, b, wi, cfg):
    """Dose 1x: independent lognormal sigma=0.05 measurement error on every link series and
    on the GER treatment series, per country-block world (declared in the pre-registration)."""
    rng = np.random.default_rng([SEED, 11, b, wi])
    out = {}
    for c in range(cfg["NC"]):
        out[c] = {}
        for L in LINKS + ("ger",):
            v = clean[c][L]
            out[c][L] = (v * np.exp(rng.normal(0.0, 0.05, size=v.shape))).astype(np.float64)
    return out


def groupings_list(nc, cpt):
    g = [("full", tuple(range(nc)))]
    for t in range(nc // cpt):
        g.append((f"type{t}", tuple(range(t * cpt, (t + 1) * cpt))))
    return g


def rows_for_spec(spec, countries, years, cpt):
    """Row layout for a specification.  Returns dict with the differencing window and the
    fixed-effect categorical columns.  S2/S5 use a genuine 5-year window; S3 is levels;
    S6 is a one-year first difference."""
    c = np.asarray(countries, dtype=np.int64)
    nc = len(c)
    if spec in ("S1", "S4"):
        tw = np.arange(10, years)
        nrow = len(tw)
        cidx = np.repeat(c, nrow)
        t1 = np.tile(tw, nc)
        t0 = t1 - 10
        return dict(spec=spec, kind="diff", c=cidx, t0=t0, t1=t1, nrow=nrow,
                    fe_vals={"decade": 1 + (t1 >= 15).astype(np.int64) + (t1 >= 20).astype(np.int64)},
                    fe_keys=["decade"])
    if spec in ("S2", "S5"):
        tw = np.arange(5, years)
        nrow = len(tw)
        cidx = np.repeat(c, nrow)
        t1 = np.tile(tw, nc)
        t0 = t1 - 5                     # TRUE 5-year window
        fe = {"bin": 1 + (t1 - 5) // 5}
        if spec == "S5":
            fe["region"] = cidx // cpt  # region-style control (declared country types)
        return dict(spec=spec, kind="diff", c=cidx, t0=t0, t1=t1, nrow=nrow,
                    fe_vals=fe, fe_keys=list(fe))
    if spec == "S3":
        t = np.arange(0, years)
        nrow = len(t)
        cidx = np.repeat(c, nrow)
        t1 = np.tile(t, nc)
        return dict(spec=spec, kind="level", c=cidx, t0=t1, t1=t1, nrow=nrow,
                    fe_vals={"country": cidx, "year": t1}, fe_keys=["country", "year"])
    if spec == "S6":
        t = np.arange(1, years)
        nrow = len(t)
        cidx = np.repeat(c, nrow)
        t1 = np.tile(t, nc)
        t0 = t1 - 1
        return dict(spec=spec, kind="diff", c=cidx, t0=t0, t1=t1, nrow=nrow,
                    fe_vals={"year": t1}, fe_keys=["year"])
    raise ValueError(spec)


def _dummy_cols(vals):
    """Dummy columns dropping the first observed level (keeps the intercept)."""
    levels = np.unique(vals)
    return [(vals == lev).astype(np.float64) for lev in levels[1:]]


def build_design(rows, gmat, incmat):
    c, t1, t0 = rows["c"], rows["t1"], rows["t0"]
    if rows["kind"] == "diff":
        x = gmat[t1, c] - gmat[t0, c]
    else:
        x = gmat[t1, c]
    cols = [np.ones(len(c), dtype=np.float64), x]
    if rows["spec"] == "S4":
        cols.append(incmat[t1, c] - incmat[t0, c])   # income control (declared)
    for key in rows["fe_keys"]:
        cols.extend(_dummy_cols(rows["fe_vals"][key]))
    return np.column_stack(cols)


def build_design_per_country(rows, gmat, incmat):
    """Same transform for one country; no country/region dummies (they are absorbed)."""
    c, t1, t0 = rows["c"], rows["t1"], rows["t0"]
    if rows["kind"] == "diff":
        x = gmat[t1, c] - gmat[t0, c]
    else:
        x = gmat[t1, c]
    cols = [np.ones(len(c), dtype=np.float64), x]
    if rows["spec"] == "S4":
        cols.append(incmat[t1, c] - incmat[t0, c])
    for key in rows["fe_keys"]:
        if key in ("country", "region"):
            continue
        cols.extend(_dummy_cols(rows["fe_vals"][key]))
    return np.column_stack(cols)


def build_Y(rows, Lmat):
    c, t1, t0 = rows["c"], rows["t1"], rows["t0"]
    if rows["kind"] == "diff":
        return np.column_stack([Lmat[L][t1, c] - Lmat[L][t0, c] for L in LINKS])
    return np.column_stack([Lmat[L][t1, c] for L in LINKS])


def fit_batch(Y, X, starts, n_clusters):
    """Cluster-robust (CR1) OLS, batched over outcome links.

    Returns (beta, se) for the first regressor (the GER coefficient, column 1).
    Clusters are countries; rows are contiguous by country (starts gives the offsets).
    """
    n, k = X.shape
    if n <= k or n_clusters < 2:
        return None, None
    XtX = X.T @ X
    try:
        XtXi = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        XtXi = np.linalg.pinv(XtX)
    B = XtXi @ (X.T @ Y)                  # k x L
    E = Y - X @ B                         # n x L
    S = np.add.reduceat(X[:, :, None] * E[:, None, :], starts, axis=0)   # G x k x L
    v = XtXi[1]                           # variance of coefficient 1 only
    proj = np.einsum("k,gkL->gL", v, S)   # G x L
    meat11 = np.einsum("gL,gL->L", proj, proj)
    scale = (n_clusters / (n_clusters - 1.0)) * ((n - 1.0) / (n - k))
    se = np.sqrt(np.maximum(meat11 * scale, 0.0))
    return B[1], se


def fit_slope_per_country(Y, X):
    """Plain OLS slope for one country (variance not needed for classification features)."""
    XtX = X.T @ X
    try:
        XtXi = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        XtXi = np.linalg.pinv(XtX)
    return (XtXi @ (X.T @ Y))[1]


FEATURE_SPECS = ("S1", "S2", "S4")   # country-level slope identified (see departures log)


def block_task(args):
    """One independent country block: kernel runs for all 5 worlds, 2 doses, all specs,
    all groupings, and country-level slopes for the predictive-discrimination layer."""
    b, cfg = args
    nc, T, N = cfg["NC"], cfg["YEARS"], cfg["N"]
    cpt = nc // cfg["NTYPES"]
    t0w = time.time()
    nuis = block_nuisance(b, cfg)
    group_list = groupings_list(nc, cpt)
    nw = len(WORLDS)

    cell_beta, cell_se = {}, {}
    feat_beta = {}
    for spec in SPECS:
        for dose in DOSES:
            for gname, countries in group_list:
                for L in LINKS:
                    cell_beta[(spec, dose, gname, L)] = np.full(nw, np.nan)
                    cell_se[(spec, dose, gname, L)] = np.full(nw, np.nan)
    for spec in FEATURE_SPECS:
        for dose in DOSES:
            for L in LINKS:
                for c in range(nc):
                    feat_beta[(spec, dose, L, c)] = np.full(nw, np.nan)

    for wi, w in enumerate(WORLDS):
        s = 0 if w == "s0" else 1
        world_arg = "P" if s == 0 else w
        clean = {}
        for c in range(nc):
            res = model.run_unit(world_arg, s, unit_seed(b, c), n=N, years=T, **nuis[c])
            clean[c] = link_series(res)
        noisy = measured_series(clean, b, wi, cfg)
        for dose in DOSES:
            S = clean if dose == 0.0 else noisy
            Lmat = {L: np.column_stack([S[c][L] for c in range(nc)]) for L in LINKS}
            gmat = np.column_stack([S[c]["ger"] for c in range(nc)])
            incmat = Lmat["inc"]
            for spec in SPECS:
                for gname, countries in group_list:
                    rows = rows_for_spec(spec, countries, T, cpt)
                    X = build_design(rows, gmat, incmat)
                    Y = build_Y(rows, Lmat)
                    starts = np.arange(0, len(rows["c"]), rows["nrow"])
                    beta, se = fit_batch(Y, X, starts, len(countries))
                    if beta is None:
                        continue
                    for li, L in enumerate(LINKS):
                        if spec == "S4" and L == "inc":
                            cell_beta[(spec, dose, gname, L)][wi] = np.nan
                            continue
                        cell_beta[(spec, dose, gname, L)][wi] = beta[li]
                        cell_se[(spec, dose, gname, L)][wi] = se[li]
            for spec in FEATURE_SPECS:
                for c in range(nc):
                    rows = rows_for_spec(spec, (c,), T, cpt)
                    X = build_design_per_country(rows, gmat, incmat)
                    Y = build_Y(rows, Lmat)
                    beta = fit_slope_per_country(Y, X)
                    for li, L in enumerate(LINKS):
                        if spec == "S4" and L == "inc":
                            continue
                        feat_beta[(spec, dose, L, c)][wi] = beta[li]
        log(f"  block {b}: world {w} done ({time.time()-t0w:.1f}s)")
    return {"block": b, "cells_beta": cell_beta, "cells_se": cell_se,
            "feats": feat_beta, "nuis_sha256": nuisance_block_hash(nuis),
            "wall_s": round(time.time() - t0w, 2)}


# ----------------------------------------------------------------------------------
# matrix aggregation: effect sizes, TOST, bootstrap over independent blocks
# ----------------------------------------------------------------------------------
def _t_ci(mean, se, q):
    return mean - q * se, mean + q * se


def pairwise_matrix(block_results, cfg):
    blocks = sorted(block_results, key=lambda r: r["block"])
    n_blocks = len(blocks)
    world_pairs = [(i, j) for i in range(len(WORLDS)) for j in range(i + 1, len(WORLDS))]
    cells = []
    D_rows, meta = [], []
    for spec in SPECS:
        for dose in DOSES:
            for gname, _ in groupings_list(cfg["NC"], cfg["NC"] // cfg["NTYPES"]):
                for L in LINKS:
                    if spec == "S4" and L == "inc":
                        continue   # declared not-applicable: control would be the outcome
                    key = (spec, dose, gname, L)
                    betas = np.array([r["cells_beta"][key] for r in blocks], dtype=np.float64)
                    ses = np.array([r["cells_se"][key] for r in blocks], dtype=np.float64)
                    if np.any(np.isnan(betas)):
                        cells.append({"spec": spec, "dose": dose, "grouping": gname, "link": L,
                                      "status": "fit_failed", "n_blocks_ok": int(np.sum(~np.isnan(betas[:, 0]))) })
                        continue
                    wsum = {}
                    for wi, w in enumerate(WORLDS):
                        m = float(np.mean(betas[:, wi]))
                        se_b = float(np.std(betas[:, wi], ddof=1) / math.sqrt(n_blocks))
                        lo90, hi90 = _t_ci(m, se_b, T90_9)
                        lo95, hi95 = _t_ci(m, se_b, T95_9)
                        se_cr = float(np.median(ses[:, wi]))
                        wsum[w] = {"beta": m, "se_between_block": se_b, "se_within_block_cr_median": se_cr,
                                   "ci90": [lo90, hi90], "ci95": [lo95, hi95],
                                   "block_betas": betas[:, wi].tolist(), "block_ses_cr": ses[:, wi].tolist()}
                    pairs = {}
                    for i, j in world_pairs:
                        d = betas[:, i] - betas[:, j]
                        delta = float(np.mean(d))
                        se_d = float(np.std(d, ddof=1) / math.sqrt(n_blocks))
                        lo90, hi90 = _t_ci(delta, se_d, T90_9)
                        lo95, hi95 = _t_ci(delta, se_d, T95_9)
                        pairs[f"{WORLDS[i]}-{WORLDS[j]}"] = {
                            "delta": delta, "se": se_d, "ci90": [lo90, hi90], "ci95": [lo95, hi95],
                            "tost_equivalent_90": bool(lo90 >= -MARGIN and hi90 <= MARGIN),
                            "statistically_distinct_95": bool(lo95 > 0 or hi95 < 0),
                        }
                        D_rows.append(d)
                        meta.append((spec, L, dose, f"{WORLDS[i]}-{WORLDS[j]}", gname))
                    cells.append({"spec": spec, "dose": dose, "grouping": gname, "link": L,
                                  "status": "ok", "n_blocks": n_blocks,
                                  "worlds": wsum, "pairs": pairs})
    return cells, np.asarray(D_rows, dtype=np.float64), meta


def _share(flags):
    return float(np.mean(flags)) if len(flags) else None


def _boot_shares(D, meta, rng, R=400):
    """Block bootstrap (resample the 10 independent blocks with replacement) for the share
    of pairwise contrasts that are TOST-equivalent / statistically distinct."""
    n, B = D.shape
    idx = rng.integers(0, B, size=(R, B))
    means = (D @ idx.T) / B
    D2 = D * D
    ms = (D2 @ idx.T) / B
    var = (ms - means * means) * (B / (B - 1.0))
    se = np.sqrt(np.maximum(var, 0.0) / B)
    equiv = (means - T90_9 * se >= -MARGIN) & (means + T90_9 * se <= MARGIN)
    distinct = ((means - T95_9 * se) > 0) | ((means + T95_9 * se) < 0)
    return equiv, distinct


def _pct(v, lo=2.5, hi=97.5):
    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]


def summarise_matrix(block_results, cfg):
    cells, D, meta = pairwise_matrix(block_results, cfg)
    rng = np.random.default_rng([SEED, 909])
    equiv, distinct = _boot_shares(D, meta, rng)
    full = {}
    for ci, cell in enumerate(cells):
        if cell["status"] != "ok":
            continue
        for pname, p in cell["pairs"].items():
            full.setdefault((cell["spec"], cell["link"], cell["dose"], pname, cell["grouping"]), p)
    d_list = [r for r in D]
    absd = np.abs(np.asarray(d_list))
    groups = {
        "spec": (np.array([m[0] for m in meta]), SPECS),
        "link": (np.array([m[1] for m in meta]), LINKS),
        "dose": (np.array([m[2] for m in meta]), DOSES),
        "pair": (np.array([m[3] for m in meta]), [f"{WORLDS[i]}-{WORLDS[j]}"
                                                  for i in range(len(WORLDS)) for j in range(i + 1, len(WORLDS))]),
        "grouping": (np.array([m[4] for m in meta]),
                     [g for g, _ in groupings_list(cfg["NC"], cfg["NC"] // cfg["NTYPES"])]),
    }
    breakdown = {}
    for gname, (labels, order) in groups.items():
        bd = {}
        for lab in order:
            msk = labels == str(lab)
            if not msk.any():
                continue
            bd[str(lab)] = {
                "n_pairwise_contrasts": int(msk.sum()),
                "share_tost_equivalent": _share(equiv[msk].mean(axis=0)),
                "share_tost_equivalent_ci95": _pct(equiv[msk].mean(axis=0)),
                "share_distinct_95": _share(distinct[msk].mean(axis=0)),
                "share_distinct_95_ci95": _pct(distinct[msk].mean(axis=0)),
                "median_abs_delta": float(np.median(absd[msk])),
            }
        breakdown[gname] = bd
    summary = {
        "n_design_cells": len(cells),
        "n_cells_ok": int(sum(1 for c in cells if c["status"] == "ok")),
        "n_cells_fit_failed": int(sum(1 for c in cells if c["status"] != "ok")),
        "n_pairwise_contrasts": int(len(absd)),
        "share_tost_equivalent_90": _share(equiv.mean(axis=0)),
        "share_tost_equivalent_90_ci95": _pct(equiv.mean(axis=0)),
        "share_statistically_distinct_95": _share(distinct.mean(axis=0)),
        "share_statistically_distinct_95_ci95": _pct(distinct.mean(axis=0)),
        "share_inconclusive": _share((~equiv & ~distinct).mean(axis=0)),
        "abs_delta": {"median": float(np.median(absd)), "iqr": [float(np.percentile(absd, 25)),
                                                               float(np.percentile(absd, 75))],
                      "p90": float(np.percentile(absd, 90)), "max": float(np.max(absd)),
                      "share_gt_margin": float(np.mean(absd > MARGIN))},
        "breakdown": breakdown,
    }
    return summary, cells


# ----------------------------------------------------------------------------------
# predictive discrimination (out-of-block)
# ----------------------------------------------------------------------------------
def rankdata(a):
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=np.float64)
    ranks[order] = np.arange(1, len(a) + 1, dtype=np.float64)
    vals = a[order]
    i = 0
    while i < len(vals):
        j = i + 1
        while j < len(vals) and vals[j] == vals[i]:
            j += 1
        if j - i > 1:
            ranks[order[i:j]] = (i + 1 + j) / 2.0
        i = j
    return ranks


def auc_score(scores, positive):
    pos = scores[positive]
    neg = scores[~positive]
    if len(pos) == 0 or len(neg) == 0:
        return None
    ranks = rankdata(np.concatenate([pos, neg]))
    n_pos, n_neg = len(pos), len(neg)
    return float((np.sum(ranks[:n_pos]) - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))


def classify_centroid(F_train, y_train, F_test, labels):
    """Nearest-centroid on training-standardised features.  Returns predictions and the
    distance matrix (n_test x n_labels)."""
    mu = F_train.mean(axis=0)
    sd = F_train.std(axis=0)
    sd[sd == 0] = 1.0
    Ztr = (F_train - mu) / sd
    Zte = (F_test - mu) / sd
    cents, keep = [], []
    for w in labels:
        m = y_train == w
        if m.sum() == 0:
            continue
        cents.append(Ztr[m].mean(axis=0))
        keep.append(w)
    cents = np.asarray(cents)
    dist = np.column_stack([np.linalg.norm(Zte - cents[k], axis=1) for k in range(len(keep))])
    pred = np.array(keep)[np.argmin(dist, axis=1)]
    return pred, dist, keep


def accuracy_ci(pred, y, rng, R=1000):
    ok = (pred == y).astype(np.float64)
    n = len(ok)
    boot = rng.choice(ok, size=(R, n), replace=True).mean(axis=1)
    return float(ok.mean()), _pct(boot)


def predictive_discrimination(block_results, cfg):
    blocks = sorted(block_results, key=lambda r: r["block"])
    nb = len(blocks)
    nw = len(WORLDS)
    feats = {}
    for spec in FEATURE_SPECS:
        for dose in DOSES:
            for L in LINKS:
                if spec == "S4" and L == "inc":
                    continue
                feats[(spec, dose, L)] = np.array([r["feats"][(spec, dose, L, c)] for r in blocks
                                                   for c in range(cfg["NC"])])  # (nb*nc, nw)
    fkeys = list(feats.keys())
    n_units_per_world = nb * cfg["NC"]
    train_blocks = set(range(0, nb // 2))
    test_blocks = set(range(nb // 2, nb))
    unit_block = np.repeat(np.arange(nb), cfg["NC"] * nw)
    unit_country = np.tile(np.repeat(np.arange(cfg["NC"]), nw), nb)
    y = np.tile(np.array(WORLDS, dtype=object), nb * cfg["NC"])
    tr = np.isin(unit_block, list(train_blocks))
    te = np.isin(unit_block, list(test_blocks))
    rng = np.random.default_rng([SEED, 77])

    def build_F(keys):
        cols = []
        for k in keys:
            fd = feats[k]                 # (nb*nc, nw)
            cols.append(fd.reshape(-1))   # block-major, then country, then world
        return np.column_stack(cols)

    chance = 1.0 / len(WORLDS)
    n_test = int(te.sum())
    band_lo = chance - 1.96 * math.sqrt(chance * (1 - chance) / n_test)
    band_hi = chance + 1.96 * math.sqrt(chance * (1 - chance) / n_test)
    out = {"n_train_units": int(tr.sum()), "n_test_units": n_test,
           "train_blocks": sorted(train_blocks), "test_blocks": sorted(test_blocks),
           "chance_accuracy": chance, "chance_band_95": [band_lo, band_hi],
           "feature_specs": list(FEATURE_SPECS),
           "note": "country-level slopes; S3/S6 are not identified per country and S5's region "
                   "control is absorbed at the country level, so those specs are excluded (declared)."}
    # single-feature classifiers
    single = {}
    for k in fkeys:
        F = build_F([k])
        pred, _, _ = classify_centroid(F[tr], y[tr], F[te], list(WORLDS))
        acc = float(np.mean(pred == y[te]))
        single[f"{k[0]}|{k[1]}|{k[2]}"] = acc
    vals = np.array(list(single.values()))
    out["single_feature"] = {
        "n": len(single), "median_accuracy": float(np.median(vals)), "max_accuracy": float(vals.max()),
        "best_feature": max(single, key=single.get),
        "n_above_chance_band": int(np.sum(vals > band_hi)),
        "per_feature": single,
    }
    # combined classifiers: dose 0 only, and both doses
    combos = {"dose0": [k for k in fkeys if k[1] == 0.0], "all_doses": fkeys}
    combined = {}
    for cname, keys in combos.items():
        F = build_F(keys)
        pred, dist, keep = classify_centroid(F[tr], y[tr], F[te], list(WORLDS))
        acc, acc_ci = accuracy_ci(pred, y[te], rng)
        per_block = {}
        tb = unit_block[te]
        for bb in sorted(test_blocks):
            m = tb == bb
            per_block[f"block{int(bb)}"] = float(np.mean(pred[m] == y[te][m]))
        recall = {w: float(np.mean(pred[y[te] == w] == w)) for w in WORLDS}
        pos = np.array([np.where(keep == w)[0][0] for w in keep])
        scores = -dist[:, pos]
        aucs = {}
        for wi, w in enumerate(keep):
            a = auc_score(scores[:, wi], (y[te] == w))
            boot = []
            for _ in range(400):
                bi = rng.integers(0, n_test, size=n_test)
                aa = auc_score(scores[bi, wi], (y[te][bi] == w))
                if aa is not None:
                    boot.append(aa)
            aucs[w] = {"auc": a, "auc_ci95": _pct(np.array(boot)) if boot else None}
        combined[cname] = {"n_features": len(keys), "accuracy": acc, "accuracy_ci95": acc_ci,
                           "per_world_recall": recall, "per_test_block_accuracy": per_block,
                           "auc_one_vs_rest": aucs}
    out["combined"] = combined
    return out


# ----------------------------------------------------------------------------------
# self-checks / declarations
# ----------------------------------------------------------------------------------
def self_checks(cfg):
    cpt = cfg["NC"] // cfg["NTYPES"]
    checks = {}
    checks["M1_all_6_specs"] = list(SPECS) == ["S1", "S2", "S3", "S4", "S5", "S6"]
    checks["M2_s0_in_matrix"] = "s0" in WORLDS and len(WORLDS) == 5
    win = {}
    for spec in SPECS:
        rows = rows_for_spec(spec, (0,), cfg["YEARS"], cpt)
        win[spec] = sorted(set((rows["t1"] - rows["t0"]).tolist()))
    checks["M3_window_by_spec"] = win
    checks["M3_true_5y"] = bool(win["S2"] == [5] and win["S5"] == [5] and win["S6"] == [1]
                              and win["S1"] == [10] and win["S4"] == [10])
    checks["M4_n_blocks"] = cfg["NBLOCKS"]
    nus = [block_nuisance(b, cfg) for b in range(cfg["NBLOCKS"])]
    hashes = [nuisance_block_hash(x) for x in nus]
    checks["M4_independent_block_draws"] = len(set(hashes)) == cfg["NBLOCKS"]
    checks["M4_block_nuisance_sha256"] = hashes
    checks["M5_uncertainty"] = ("CR1 cluster sandwich over countries inside each independent block; "
                                "paired cross-block difference, Student t df=NBLOCKS-1")
    checks["M6_seeds"] = {"SEED": SEED, "kernel_unit_seed": "20270101+100000*block+100*country",
                          "measure_noise": "[SEED,11,block,world_index]"}
    checks["doses"] = list(DOSES)
    checks["n_countries"] = cfg["NC"]
    checks["n_households"] = cfg["N"]
    checks["years"] = cfg["YEARS"]
    checks["n_worlds"] = len(WORLDS)
    checks["links"] = list(LINKS)
    checks["tost_margin"] = MARGIN
    return checks


def departures(cfg):
    cpt = cfg["NC"] // cfg["NTYPES"]
    n_groupings = 1 + cfg["NC"] // cpt
    link_spec = len(LINKS) * len(SPECS) - 1   # S4 x income is undefined (control = outcome)
    n_cells = link_spec * len(DOSES) * n_groupings
    return [
        "Prereg estimated ~3,360 cells / <=16,800 regressions. The declared grouping dimension "
        "'full sample + 4 declared types' defines 5 groupings, so the implemented grid is "
        f"{link_spec} link-spec combinations x {len(DOSES)} doses x {n_groupings} groupings = "
        f"{n_cells} cells (x5 worlds = {n_cells*5} fitted regressions; {n_cells*10} pairwise contrasts). "
        "Arithmetic clarification only: no declared design element was changed.",
        "The prereg names '4 declared types' without enumerating them. Declared HERE, before the run: "
        "the first four rows of the v2 eight-type table, 16 countries per type (64 total).",
        "S4 (10y differences + income control) is not defined for the income outcome (the declared "
        "control is the outcome itself). That cell is excluded and counted, NOT silently replaced by "
        "S1 (the audited v2 behaviour).",
        "Country-level features for predictive discrimination are identifiable only for S1, S2 and S4. "
        "S3 (country FE) and S6 (24 first differences with year FE) are not identified at the "
        "individual-country level, and S5's region control is constant within a country; those three "
        "specs are excluded from the country-level classifier (declared before the run).",
        "Uncertainty: CR1 cluster-robust sandwich over countries inside each independent block; "
        f"cross-block inference from the {cfg['NBLOCKS']} independent blocks as paired replicates "
        f"(Student t, df={cfg['NBLOCKS']-1}). No binomial-over-cells uncertainty is used anywhere.",
        "2-seed smoke configuration (blocks=2, NC=32, N=1000, Phase B calibration/heldout/replication "
        "seeds 2/4/4) exists only to exercise every code path; it is not used for any result.",
        "Older exploratory results (v2, v2b, Phase B) are untouched by this run and remain "
        "EXPLORATORY PENDING REVIEW.",
    ]


# ----------------------------------------------------------------------------------
# runner
# ----------------------------------------------------------------------------------
def results_dir(mode):
    return os.path.join(REC, "results_smoke" if mode == "smoke" else "results")


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(json_safe(obj), f, indent=1)


def run(cfg):
    mode = cfg["mode"]
    outdir = results_dir(mode)
    os.makedirs(outdir, exist_ok=True)
    started = now_iso()
    t_start = time.time()
    code_hashes = {
        "run_corrected.py": sha256_file(os.path.abspath(__file__)),
        "model.py": sha256_file(os.path.join(HERE, "model.py")),
        "kernels_np_mlx.py": sha256_file(os.path.join(HERE, "port_backend", "kernels_np_mlx.py")),
        "gpu_compat.py": sha256_file(os.path.join(HERE, "port_backend", "gpu_compat.py")),
    }
    checks = self_checks(cfg)
    log("GRID: " + json.dumps(json_safe({"worlds": WORLDS, "specs": SPECS, "doses": DOSES,
                                         "N": cfg["N"], "NC": cfg["NC"], "blocks": cfg["NBLOCKS"],
                                         "links": LINKS,
                                         "tost_margin": MARGIN})))
    log("CHECKS: " + json.dumps(json_safe({k: v for k, v in checks.items()
                                           if not k.endswith("sha256") and k != "M4_block_nuisance_sha256"})))
    if not (checks["M1_all_6_specs"] and checks["M2_s0_in_matrix"] and checks["M3_true_5y"]
            and checks["M4_independent_block_draws"]):
        raise SystemExit("self-check failed: refusing to run")
    log(f"mode={mode} workers={cfg['workers']} out={outdir}")

    ctx = mp.get_context("fork")
    with ctx.Pool(cfg["workers"]) as pool:
        block_results = pool.map(
            block_task, [(b, cfg) for b in range(cfg["NBLOCKS"])], chunksize=1)
        log(f"matrix blocks done: {time.time()-t_start:.1f}s")

    matrix_summary, cells = summarise_matrix(block_results, cfg)
    log("MATRIX DECISION: " + json.dumps(json_safe({
        "n_pairwise": matrix_summary["n_pairwise_contrasts"],
        "share_tost_equivalent": matrix_summary["share_tost_equivalent_90"],
        "equivalent_ci95": matrix_summary["share_tost_equivalent_90_ci95"],
        "share_distinct95": matrix_summary["share_statistically_distinct_95"],
        "distinct_ci95": matrix_summary["share_statistically_distinct_95_ci95"],
        "median_abs_delta": matrix_summary["abs_delta"]["median"]})))
    with open(os.path.join(outdir, "matrix_corrected_cells.jsonl"), "w") as f:
        for c in cells:
            f.write(json.dumps(json_safe(c)) + "\n")
    write_json(os.path.join(outdir, "matrix_corrected_summary.json"), matrix_summary)
    # predictive discrimination (uses the country-level slopes from the same blocks)
    disc = predictive_discrimination(block_results, cfg)
    write_json(os.path.join(outdir, "predictive_discrimination.json"), disc)
    log("DISCRIMINATION: " + json.dumps(json_safe({
        "single_median": disc["single_feature"]["median_accuracy"],
        "single_max_best": disc["single_feature"]["best_feature"],
        "combined_dose0": disc["combined"]["dose0"]["accuracy"],
        "combined_dose0_ci95": disc["combined"]["dose0"]["accuracy_ci95"],
        "auc_s0": disc["combined"]["dose0"]["auc_one_vs_rest"]["s0"]["auc"]})))
    matrix_summary["predictive_discrimination"] = disc
    write_json(os.path.join(outdir, "matrix_corrected_summary.json"), matrix_summary)

    wall = round(time.time() - t_start, 1)
    manifest = {
        "task": "task-23", "label": "SIMULATION", "mode": mode,
        "started_utc": started, "finished_utc": now_iso(), "wall_s": wall,
        "host": platform.node(), "platform": platform.platform(),
        "python": sys.version.split()[0], "numpy": np.__version__,
        "cpu_count": mp.cpu_count(), "workers": cfg["workers"],
        "backend": model.BACKEND, "model_layout": model.LAYOUT,
        "prereg": {"commit": PREREG_COMMIT, "path": PREREG_PATH, "sha256": PREREG_SHA256},
        "code_sha256": code_hashes,
        "grid": {"worlds": WORLDS, "specs": SPECS, "spec_def": SPEC_DEF, "doses": DOSES,
                 "links": LINKS, "link_def": LINK_DEF, "N": cfg["N"], "NC": cfg["NC"],
                 "NTYPES": cfg["NTYPES"], "types": TYPES4, "YEARS": cfg["YEARS"],
                 "NBLOCKS": cfg["NBLOCKS"],
                 "seed": SEED, "tost_margin": MARGIN},
        "grid_sha256": sha256_obj({k: v for k, v in cfg.items() if k != "workers"}),
        "self_checks": checks,
        "departures": departures(cfg),
        "block_wall_s": {f"block{r['block']}": r["wall_s"] for r in block_results},
        "block_nuisance_sha256": checks["M4_block_nuisance_sha256"],
        "matrix_summary_file": "matrix_corrected_summary.json",
        "predictive_discrimination_file": "predictive_discrimination.json",
        "matrix": {"n_design_cells": matrix_summary["n_design_cells"],
                   "n_cells_fit_failed": matrix_summary["n_cells_fit_failed"],
                   "n_pairwise_contrasts": matrix_summary["n_pairwise_contrasts"]},
    }
    write_json(os.path.join(outdir, "run_manifest_corrected.json"), manifest)
    log(f"WALL {wall}s -> {outdir}")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="2-block code-path smoke (not a result)")
    ap.add_argument("--workers", type=int, default=min(96, mp.cpu_count()))
    args = ap.parse_args()
    cfg = smoke_config(args.workers) if args.smoke else full_config(args.workers)
    try:
        run(cfg)
    except Exception:
        tb = traceback.format_exc()
        sys.stderr.write(tb)
        write_json(os.path.join(results_dir(cfg["mode"]), "FAILURE.json"),
                   {"mode": cfg["mode"], "when_utc": now_iso(), "traceback": tb,
                    "label": "SIMULATION", "note": "failure preserved; no retuning"})
        raise SystemExit(1)


if __name__ == "__main__":
    main()
