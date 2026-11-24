#!/usr/bin/env python3
"""Prior importance screening for MASSENG v5 Philippines R1.

This is a conditional pseudo-likelihood importance screen, not MCMC and not a
claim of a calibrated posterior. Existing R1 fit values fix all but four R1
mechanism parameters. Outputs are written to a new directory and never
overwrite existing results.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from multiprocessing import Pool

import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = HERE.parents[1] / "model"
sys.path.insert(0, str(MODEL))

from masseng.data import Country
from masseng.engine5 import Model5
from masseng import targets

FIT_PATH = MODEL / "outputs/PHL/v5/fit_R1.json"
PARAMS = ("b_h", "b_p", "b_r", "lam")
GER_SERIES = ("ger_primary", "ger_secondary", "ger_tertiary")
# Deliberately explicit uniform prior ranges. Expanded sensitivity ranges match
# the broad bounds used by the v5 fitter for these parameters.
PRIORS = {
    "main": {"b_h": [-2.0, 8.0], "b_p": [0.0, 10.0], "b_r": [-2.0, 12.0], "lam": [0.0, 8.0]},
    "expanded": {"b_h": [-6.0, 12.0], "b_p": [-6.0, 12.0], "b_r": [-12.0, 24.0], "lam": [-6.0, 12.0]},
}
# Fixed observational scales in GER percentage points. These are working
# pseudo-likelihood scales, not claimed official sampling standard errors.
SIGMA_PP = {"ger_primary": 4.0, "ger_secondary": 4.0, "ger_tertiary": 5.0}
# sigma multiplier set from the CLI in run(); the original run_screen.py leaves it at 1.0.
SIGMA_MULT = 1.0


def make_draws(n: int, seed: int, prior: str) -> np.ndarray:
    if n < 2:
        raise ValueError("n_draws must be at least 2")
    rng = np.random.default_rng(seed)
    bounds = np.array([PRIORS[prior][k] for k in PARAMS], dtype=float)
    return rng.uniform(bounds[:, 0], bounds[:, 1], size=(n, len(PARAMS)))


def normalized_weights(logw: np.ndarray) -> np.ndarray:
    x = np.asarray(logw, dtype=float)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).any():
        raise ValueError("log weights must be a nonempty vector with finite values")
    z = np.where(np.isfinite(x), x - np.max(x[np.isfinite(x)]), -np.inf)
    w = np.exp(z)
    return w / w.sum()


def effective_sample_size(weights: np.ndarray) -> float:
    w = np.asarray(weights, dtype=float)
    return float(1.0 / np.sum(w * w))


def block_loglik(pred: dict, train: list[dict]) -> tuple[float, dict]:
    """Gaussian pseudo-likelihood: average within each GER series, then sum blocks."""
    parts = {}
    for series in GER_SERIES:
        rows = [r for r in train if r["series"] == series]
        if not rows:
            raise ValueError(f"missing training GER block: {series}")
        err = np.array([pred[series][r["year"]] - r["value"] for r in rows], float)
        sigma = SIGMA_PP[series] * SIGMA_MULT
        # Mean log density makes each of the three series one equal-weight block.
        parts[series] = float(np.mean(-0.5 * (err / sigma) ** 2 - np.log(sigma * np.sqrt(2 * np.pi))))
    return float(sum(parts.values())), parts


def _evaluate_one(task):
    i, vals, fixed, train, test = task
    c = Country("PHL")
    p = dict(fixed)
    p.update(dict(zip(PARAMS, vals)))
    result = Model5(c, p, spec="R1").run()
    years = list(map(int, result.years))
    byyear = {s: dict(zip(years, map(float, result.ind[s]))) for s in GER_SERIES}
    ll, blocks = block_loglik(byyear, train)
    test_pred = [byyear[r["series"]][r["year"]] for r in test]
    return dict(i=i, theta=dict(zip(PARAMS, map(float, vals))), loglik=ll,
                block_loglik=blocks, test_pred=test_pred)


def _rmse(pred, obs):
    p, o = np.asarray(pred, float), np.asarray(obs, float)
    return float(np.sqrt(np.mean((p - o) ** 2))) if len(o) else float("nan")


def run(prior: str, n: int, seed: int, workers: int, out: Path, sigma_mult: float = 1.0):
    global SIGMA_MULT
    SIGMA_MULT = float(sigma_mult)
    if out.exists():
        raise FileExistsError(f"refusing to overwrite output directory: {out}")
    out.mkdir(parents=True)
    c = Country("PHL")
    rows = targets.build(c)
    train = [r for r in rows if r["role"] == "train" and r["series"] in GER_SERIES
             and 1971 <= r["year"] <= 1995]
    test = [r for r in rows if r["role"] == "test" and r["series"] in GER_SERIES
            and 1996 <= r["year"] <= 2024]
    if not train or not test:
        raise RuntimeError(f"GER rows unavailable; train={len(train)} test={len(test)}")
    # Remove the four varied entries from the baseline file; these are replaced
    # by prior draws. Every other R1 fit parameter stays fixed.
    fixed = json.loads(FIT_PATH.read_text())["params"]
    for k in PARAMS:
        fixed.pop(k, None)
    draws = make_draws(n, seed, prior)
    tasks = [(i, draws[i].tolist(), fixed, train, test) for i in range(n)]
    if workers > 1:
        with Pool(workers) as pool:
            runs = pool.map(_evaluate_one, tasks, chunksize=max(1, n // (workers * 8)))
    else:
        runs = [_evaluate_one(t) for t in tasks]
    runs.sort(key=lambda r: r["i"])
    logw = np.array([r["loglik"] for r in runs])
    weights = normalized_weights(logw)
    obs = np.array([r["value"] for r in test], float)
    mat = np.array([r["test_pred"] for r in runs], float)
    post_mean = weights @ mat
    # Posterior weighted 5/95% intervals by target row.
    lo = np.array([_weighted_quantile(mat[:, j], weights, .05) for j in range(mat.shape[1])])
    hi = np.array([_weighted_quantile(mat[:, j], weights, .95) for j in range(mat.shape[1])])
    persistence = []
    for r in test:
        hist = [q for q in train if q["series"] == r["series"]]
        persistence.append(max(hist, key=lambda q: q["year"])["value"])
    by_series = {}
    for s in GER_SERIES:
        ix = [j for j, r in enumerate(test) if r["series"] == s]
        by_series[s] = dict(n=len(ix), model_rmse=_rmse(post_mean[ix], obs[ix]),
                            persistence_rmse=_rmse(np.array(persistence)[ix], obs[ix]))
    theta_summary = {}
    for k in PARAMS:
        vals = np.array([r["theta"][k] for r in runs])
        theta_summary[k] = dict(prior=PRIORS[prior][k], mean=float(weights @ vals),
                                q05=_weighted_quantile(vals, weights, .05),
                                median=_weighted_quantile(vals, weights, .5),
                                q95=_weighted_quantile(vals, weights, .95))
    result = {
        "title": "MASSENG v5 PHL R1 prior importance screen",
        "status": "exploratory Bayesian-style importance screening; not a calibrated posterior",
        "prior": prior, "prior_bounds": PRIORS[prior], "draws": n, "seed": seed,
        "varied_parameters": list(PARAMS), "fixed_parameters": fixed,
        "baseline_source": str(FIT_PATH),
        "baseline_note": "Other parameters fixed at an existing R1 fit estimated using broader data. This is empirically informed conditioning and involves data reuse; results are conditional, not a fresh independent calibration.",
        "likelihood": {"form": "sum of equal-weight mean Gaussian log densities for GER primary, secondary, tertiary training blocks",
                       "sigma_multiplier": SIGMA_MULT,
                       "sigma_percentage_points": SIGMA_PP,
                       "sigma_percentage_points_effective": {s: SIGMA_PP[s] * SIGMA_MULT for s in SIGMA_PP},
                       "training_years": [1971, 1995], "training_rows": {s: sum(r['series'] == s for r in train) for s in GER_SERIES}},
        "holdout": {"years": [1996, 2024], "status": "retrospective and inspected under PROTOCOL_v5; not blind",
                    "scores": by_series, "macro_rmse_model": _rmse(post_mean, obs), "macro_rmse_persistence": _rmse(persistence, obs),
                    "weighted_predictive_intervals_90": {"lower": lo.tolist(), "upper": hi.tolist()},
                    "rows": [{"series": r["series"], "year": r["year"], "observed": r["value"], "posterior_mean": float(post_mean[j]), "lower90": float(lo[j]), "upper90": float(hi[j])} for j, r in enumerate(test)]},
        "importance": {"ess": effective_sample_size(weights), "ess_fraction": effective_sample_size(weights) / n,
                       "max_weight": float(weights.max()), "prior_parameter_summary": theta_summary},
        "limitations": ["No causal interpretation.", "The model and targets are deterministic conditional on inputs; weights reflect a chosen pseudo-likelihood, not a validated observation model.", "R1 baseline fit reuses data beyond the GER training block, so this is conditional on empirically informed nuisance parameters.", "Holdout is previously inspected, and persistence scores do not provide a blind benchmark.", "The importance sample may have low ESS; no adaptive resampling or MCMC is used."],
    }
    (out / "summary.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    (out / "draws.json").write_text(json.dumps([dict(**r, weight=float(weights[i])) for i, r in enumerate(runs)], indent=2, allow_nan=False) + "\n")
    (out / "run.json").write_text(json.dumps({"n": n, "seed": seed, "workers": workers, "prior": prior}, indent=2) + "\n")
    print(f"Saved {out}; sigma x{SIGMA_MULT:g}; ESS {result['importance']['ess']:.1f}/{n}; "
          f"max weight {result['importance']['max_weight']:.4f}; holdout macro RMSE model "
          f"{result['holdout']['macro_rmse_model']:.3f}, persistence {result['holdout']['macro_rmse_persistence']:.3f}")


def _weighted_quantile(x, w, q):
    x, w = np.asarray(x, float), np.asarray(w, float)
    order = np.argsort(x)
    xs, ws = x[order], w[order]
    cdf = np.cumsum(ws) - 0.5 * ws
    cdf /= ws.sum()
    return float(np.interp(q, cdf, xs, left=xs[0], right=xs[-1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-draws", type=int, default=512)
    ap.add_argument("--seed", type=int, default=20261124)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--prior", choices=sorted(PRIORS), default="main")
    ap.add_argument("--sigma", type=float, default=1.0, help="multiplier on all three pseudo-likelihood scales")
    ap.add_argument("--out", type=Path, required=True, help="new output directory; must not already exist")
    a = ap.parse_args()
    run(a.prior, a.n_draws, a.seed, a.workers, a.out.resolve(), sigma_mult=a.sigma)


if __name__ == "__main__":
    main()
