#!/usr/bin/env python3
"""X5 — synthetic parameter recovery for the MASSENG v5 R1 prior importance screen.

Generator: for declared known (b_h,b_p,b_r,lam) settings, run the SAME v5 R1 model with the SAME
fixed nuisance block as the audited screen, add Gaussian observation noise at the screen's own
declared scales (4/4/5 pp) for the synthetic training block 1971-1995 and holdout 1996-2024, then
run the same pseudo-likelihood importance screen on the synthetic data and ask whether the known
parameters are recovered (error/coverage/confusion, ESS, holdout).

Reuses `run_screen.py` helpers unchanged (imported), so the likelihood/weights are identical to
the audited screen. Original files are not modified; output is exclusive-create.

Pre-registered usability criteria: see SIGMA_X5_PLAN.md (committed before this code).
SIMULATION ONLY; conditional importance weights, not posteriors; no causal claims.
"""
import os

for _k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"

import argparse
import hashlib
import json
import socket
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_screen as RS  # noqa: E402  (identical likelihood/weights to the audited screen)

LABEL = "SIMULATION ONLY — conditional importance weights on synthetic data; not a posterior; no causal claims"
TRUTH_SETTINGS = [
    (0.5, 2.0, 2.0, 1.0),
    (3.0, 5.0, 5.0, 4.0),
    (6.0, 8.0, 10.0, 6.0),
    (-1.0, 1.0, 0.0, 0.5),
    (7.0, 9.0, 11.0, 7.0),
    (1.0, 4.0, 7.0, 3.0),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def fixed_params():
    fixed = json.loads(RS.FIT_PATH.read_text())["params"]
    for k in RS.PARAMS:
        fixed.pop(k, None)
    return fixed


def model_series(truth):
    c = RS.Country("PHL")
    p = dict(fixed_params())
    p.update(dict(zip(RS.PARAMS, truth)))
    result = RS.Model5(c, p, spec="R1").run()
    years = list(map(int, result.years))
    return {s: dict(zip(years, map(float, result.ind[s]))) for s in RS.GER_SERIES}


def synthetic_blocks(truth, gen_seed):
    series = model_series(truth)
    rng = np.random.default_rng(int(gen_seed))
    train, test = [], []
    for s in RS.GER_SERIES:
        sigma = RS.SIGMA_PP[s]
        for y in range(1971, 1996):
            train.append({"series": s, "year": y, "value": float(series[s][y] + rng.normal(0.0, sigma))})
        for y in range(1996, 2025):
            test.append({"series": s, "year": y, "value": float(series[s][y] + rng.normal(0.0, sigma))})
    return train, test


def screen(train, test, draws, fixed, workers):
    tasks = [(i, draws[i].tolist(), fixed, train, test) for i in range(len(draws))]
    if workers > 1:
        with Pool(workers) as pool:
            runs = pool.map(RS._evaluate_one, tasks, chunksize=max(1, len(draws) // (workers * 8)))
    else:
        runs = [RS._evaluate_one(t) for t in tasks]
    runs.sort(key=lambda r: r["i"])
    weights = RS.normalized_weights(np.array([r["loglik"] for r in runs], float))
    mat = np.array([r["test_pred"] for r in runs], float)
    obs = np.array([r["value"] for r in test], float)
    post_mean = weights @ mat
    persistence = []
    for r in test:
        hist = [q for q in train if q["series"] == r["series"]]
        persistence.append(max(hist, key=lambda q: q["year"])["value"])
    theta = {}
    for k in RS.PARAMS:
        vals = np.array([r["theta"][k] for r in runs], float)
        theta[k] = {"mean": float(weights @ vals),
                    "q05": RS._weighted_quantile(vals, weights, 0.05),
                    "q95": RS._weighted_quantile(vals, weights, 0.95),
                    "median": RS._weighted_quantile(vals, weights, 0.5)}
    return {"weights": weights, "theta": theta,
            "ess": RS.effective_sample_size(weights),
            "max_weight": float(weights.max()),
            "rmse_model": RS._rmse(post_mean, obs),
            "rmse_persistence": RS._rmse(persistence, obs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--n-draws", type=int, default=256)
    ap.add_argument("--screen-seed", type=int, default=20261125)
    ap.add_argument("--gen-seeds", type=int, nargs="+", default=[20261201, 20261202])
    ap.add_argument("--prior", choices=sorted(RS.PRIORS), default="main")
    ap.add_argument("--truth", type=str, default=None,
                    help="optional single truth setting as comma-separated b_h,b_p,b_r,lam (debug/smoke)")
    args = ap.parse_args()
    out_path = Path(args.out).resolve()
    if out_path.exists():
        raise FileExistsError(f"refusing to overwrite: {out_path}")
    truth_list = TRUTH_SETTINGS
    if args.truth:
        truth_list = [tuple(float(x) for x in args.truth.split(","))]
    fixed = fixed_params()
    rng = np.random.default_rng(args.screen_seed)
    bounds = np.array([RS.PRIORS[args.prior][k] for k in RS.PARAMS], float)
    ranges = bounds[:, 1] - bounds[:, 0]
    overall_t0 = time.time()
    per_dataset = []
    for ti, truth in enumerate(truth_list):
        for gen_seed in args.gen_seeds:
            t0 = time.time()
            train, test = synthetic_blocks(truth, gen_seed)
            draws = RS.make_draws(args.n_draws, args.screen_seed, args.prior)  # identical draws everywhere
            sc = screen(train, test, draws, fixed, args.workers)
            theta_mean = np.array([sc["theta"][k]["mean"] for k in RS.PARAMS], float)
            truth_arr = np.array(truth, float)
            err = theta_mean - truth_arr
            err_frac = np.abs(err) / ranges
            coverage = [bool(sc["theta"][k]["q05"] <= truth[i] <= sc["theta"][k]["q95"])
                        for i, k in enumerate(RS.PARAMS)]
            # confusion: nearest declared setting in prior-range-normalised space
            dists = [float(np.sqrt(np.mean(((theta_mean - np.array(s, float)) / ranges) ** 2)))
                     for s in TRUTH_SETTINGS]
            nearest = int(np.argmin(dists))
            per_dataset.append({
                "setting_index": ti, "truth": list(truth), "gen_seed": int(gen_seed),
                "screen_seed": int(args.screen_seed), "prior": args.prior, "n_draws": args.n_draws,
                "ess": sc["ess"], "ess_fraction": sc["ess"] / args.n_draws,
                "max_weight": sc["max_weight"], "theta": sc["theta"],
                "recovery_error": {k: float(err[i]) for i, k in enumerate(RS.PARAMS)},
                "recovery_error_fraction_of_prior_range": {k: float(err_frac[i]) for i, k in enumerate(RS.PARAMS)},
                "coverage_90": {k: bool(coverage[i]) for i, k in enumerate(RS.PARAMS)},
                "coverage_rate": float(np.mean(coverage)),
                "nearest_setting": nearest, "nearest_correct": bool(nearest == ti),
                "rmse_model": sc["rmse_model"], "rmse_persistence": sc["rmse_persistence"],
                "wall_s": round(time.time() - t0, 2)})
    n_cases = len(per_dataset)
    all_cov = [c for d in per_dataset for c in d["coverage_90"].values()]
    all_err_frac = [e for d in per_dataset for e in d["recovery_error_fraction_of_prior_range"].values()]
    ess_fracs = [d["ess_fraction"] for d in per_dataset]
    max_weights = [d["max_weight"] for d in per_dataset]
    agg = {
        "n_datasets": n_cases,
        "median_ess_fraction": float(np.median(ess_fracs)),
        "min_ess_fraction": float(np.min(ess_fracs)),
        "max_max_weight": float(np.max(max_weights)),
        "coverage_rate_overall": float(np.mean(all_cov)),
        "error_fraction_median": float(np.median(all_err_frac)),
        "error_fraction_le_0.15_rate": float(np.mean(np.array(all_err_frac) <= 0.15)),
        "confusion_diagonal_rate": float(np.mean([d["nearest_correct"] for d in per_dataset])),
        "rmse_model_median": float(np.median([d["rmse_model"] for d in per_dataset])),
        "rmse_persistence_median": float(np.median([d["rmse_persistence"] for d in per_dataset])),
    }
    crit = {
        "(a)_median_ess_fraction_ge_0.02": bool(agg["median_ess_fraction"] >= 0.02),
        "(b)_coverage_rate_ge_0.60": bool(agg["coverage_rate_overall"] >= 0.60),
        "(c)_error_le_15pct_prior_range_rate_ge_0.60": bool(agg["error_fraction_le_0.15_rate"] >= 0.60),
        "(d)_confusion_diagonal_ge_0.60": bool(agg["confusion_diagonal_rate"] >= 0.60),
    }
    degenerate = bool(agg["median_ess_fraction"] < 0.02 and agg["max_max_weight"] > 0.10)
    if degenerate or not crit["(a)_median_ess_fraction_ge_0.02"]:
        verdict = "SCREENS_UNUSABLE"
        verdict_text = ("Under a correctly specified synthetic generating model the importance screen still shows "
                        "degenerate weights (median ESS fraction %.4f, max single-draw weight %.3f); recoverability "
                        "is therefore not established and the real-data screens are unusable for posterior-style "
                        "inference at these draw counts." % (agg["median_ess_fraction"], agg["max_max_weight"]))
    elif all(crit.values()):
        verdict = "RECOVERY_WORKS_UNDER_TRUE_MODEL"
        verdict_text = ("Under the true generating model the screen recovers parameters by the pre-declared criteria; "
                        "this does NOT make the real-data screens a calibrated posterior, does not validate the "
                        "pseudo-likelihood scales, and does not fix prior sensitivity or real-data misspecification.")
    else:
        verdict = "MIXED"
        verdict_text = ("Recovery is mixed; failing criteria are named in criteria. No posterior claim is licensed "
                        "from the real-data screens.")
    out = {"label": LABEL, "experiment": "x5_synthetic_recovery",
           "design": {"truth_settings": [list(t) for t in TRUTH_SETTINGS],
                      "gen_seeds": args.gen_seeds, "screen_seed": args.screen_seed,
                      "prior": args.prior, "n_draws": args.n_draws, "workers": args.workers,
                      "noise": "Gaussian at the screen's own declared noise scales 4/4/5 pp",
                      "likelihood": "identical to run_screen.block_loglik (imported, unchanged)",
                      "criteria": crit, "degenerate_weights": degenerate},
           "datasets": per_dataset, "aggregate": agg,
           "verdict": verdict, "verdict_text": verdict_text,
           "wall_s": round(time.time() - overall_t0, 2),
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(overall_t0)),
           "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "host": socket.gethostname(), "python": sys.version.split()[0], "numpy": np.__version__,
           "code_sha256": {"run_x5_recovery.py": sha(Path(__file__).resolve()),
                           "run_screen.py": sha(Path(RS.__file__)),
                           "model/engine5.py": sha(Path(RS.MODEL) / "masseng" / "engine5.py"),
                           "model/data.py": sha(Path(RS.MODEL) / "masseng" / "data.py")},
           "limitations": ["Synthetic generator uses the same v5 R1 model and the same fixed nuisance block as the screen.",
                           "Conditional importance weights, not a posterior; no MCMC/adaptive resampling.",
                           "Recovery under a true model does not license real-data posterior or causal claims.",
                           "No E1 comparison; simulation only."]}
    out_path.write_text(json.dumps(out, indent=1, allow_nan=False) + "\n")
    print(json.dumps({"verdict": verdict, "aggregate": agg, "criteria": crit,
                      "wall_s": out["wall_s"]}, indent=1))


if __name__ == "__main__":
    main()
