#!/usr/bin/env python3
"""Large multiverse Monte Carlo over the four-piece shadow/massification chain.

Samples equation-form choices and parameters from declared ranges, runs the baseline and
policy scenarios, and reports distributions of outcomes and of scenario effects.

This is the "run the math" layer: not one point estimate, but how often each qualitative
conclusion holds across the declared model space.

Illustrative parameters only; simulation, no causal claims.
"""
import argparse, json, multiprocessing as mp, os, sys
from dataclasses import replace, asdict
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shadow_model import Params, simulate, SCENARIOS

RANGES = {
    "b0": (-3.0, 1.5),
    "b_income": (0.0, 1.8),
    "b_school_gap": (0.0, 2.5),
    "own_premium": (0.0, 2.5),
    "other_premium": (0.0, 2.5),
    "cost_other": (0.1, 1.5),
    "rho_ces": (0.3, 0.8),
    "omega_school": (0.3, 0.7),
    "ses_interaction": (0.0, 0.3),
    "seat_share": (0.35, 0.65),
    "quota_share_low": (0.4, 0.6),
}
SCEN = {k: v for k, v in SCENARIOS.items() if k in ("baseline", "quota", "ban_own", "rural_access", "cash_transfer")}
METRICS = ["tut_participation", "own_share", "other_share", "learning_gini",
           "admission_gap_q5_q1", "tut_gap_q5_q1", "earnings_gini", "spend_share"]


def draw(rng):
    p = {k: float(rng.uniform(*v)) for k, v in RANGES.items()}
    return p


def one(p, seed, n, kw):
    q = Params(n=n, seed=seed, **p)
    if kw:
        q = replace(q, **kw)
    o = simulate(q)
    return np.array([o[m] for m in METRICS], float)


def chunk(args):
    seed, count, n = args
    rng = np.random.default_rng(seed)
    names = list(SCEN)
    out = {s: np.zeros((count, len(METRICS))) for s in names}
    params = np.zeros((count, len(RANGES)))
    for i in range(count):
        p = draw(rng)
        params[i] = [p[k] for k in RANGES]
        for s in names:
            out[s][i] = one(p, seed * 1000003 + i, n, SCEN[s])
    return {"params": params, "scen": out, "names": names}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=200000)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--out", default="multiverse_summary.json")
    a = ap.parse_args()
    per = a.draws // a.workers
    tasks = [(20261125 + i * 7919, per, a.n) for i in range(a.workers)]
    print(f"multiverse: {a.draws} draws / {a.workers} workers / n={a.n}", flush=True)
    with mp.Pool(a.workers) as pool:
        parts = pool.map(chunk, tasks)
    names = parts[0]["names"]
    params = np.vstack([p["params"] for p in parts])
    scen = {s: np.vstack([p["scen"][s] for p in parts]) for s in names}
    N = params.shape[0]
    summary = {"label": "SIMULATION — multiverse Monte Carlo over illustrative four-piece chain",
               "n_draws": int(N), "n_pupils": a.n, "ranges": RANGES, "metrics": METRICS,
               "scenarios": {}}
    base = scen["baseline"]
    for s in names:
        v = scen[s]
        d = v - base
        block = {"mean": {}, "sd": {}, "q05": {}, "q50": {}, "q95": {},
                 "sign_prob": {}}
        for j, m in enumerate(METRICS):
            block["mean"][m] = float(np.nanmean(v[:, j]))
            block["sd"][m] = float(np.nanstd(v[:, j]))
            block["q05"][m] = float(np.nanpercentile(v[:, j], 5))
            block["q50"][m] = float(np.nanpercentile(v[:, j], 50))
            block["q95"][m] = float(np.nanpercentile(v[:, j], 95))
            if s != "baseline":
                block["sign_prob"][m] = float(np.nanmean(d[:, j] > 0))
        summary["scenarios"][s] = block
    # correlation of scenario deltas with parameters
    corr = {}
    for s in names:
        if s == "baseline":
            continue
        d = scen[s] - base
        c = {}
        for j, m in enumerate(METRICS):
            cc = []
            for k in range(params.shape[1]):
                x = params[:, k]
                y = d[:, j]
                msk = np.isfinite(x) & np.isfinite(y)
                cc.append(float(np.corrcoef(x[msk], y[msk])[0, 1]) if msk.sum() > 10 else float("nan"))
            c[m] = cc
        corr[s] = {"params": list(RANGES), "pearson": c}
    summary["delta_param_corr"] = corr
    with open(a.out, "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({s: {m: round(summary["scenarios"][s]["mean"][m], 4) for m in METRICS}
                      for s in names}, indent=1))
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
