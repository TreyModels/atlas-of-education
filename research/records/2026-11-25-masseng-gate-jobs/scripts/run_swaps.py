"""Run the v6 gate+jobs prototype: modular one-block-at-a-time swaps, gate multiverse, labour rival, and the
pre-declared test bench (zero-signal, identifiability, shared-code ablation, structural multiverse, falsifiers).

Layer 3 is external: this runner calls the behavioural core (model_blocks.simulate) and the frozen dashboard
(dashboard.outcomes), and never measures anything itself. Everything is simulation; no causal claims.
Run:  python run_swaps.py --workers 8
"""
from __future__ import annotations

import json
import os
import platform
import sys
import time
import traceback
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)


def _model_dir():
    cands = [os.environ.get("MASSENG_MODEL_DIR"), "/root/work/gate-jobs/model",
             os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "masseng-v6")]
    for c in cands:
        if c and os.path.isdir(os.path.join(c, "masseng_v6")):
            return os.path.abspath(c)
    raise RuntimeError("model dir not found; set MASSENG_MODEL_DIR")


sys.path.insert(0, _model_dir())
RESULTS = os.path.join(RECORD, "results")
MAIN_SEEDS = list(range(10))
HOLD_SEEDS = list(range(10, 20))


def _run(cfg):
    """Worker: one model run -> frozen dashboard."""
    from model_blocks import Params, simulate
    from dashboard import outcomes
    t0 = time.time()
    try:
        p = Params(**cfg["params"])
        raw = simulate(p)
        out = outcomes(raw)
        return {"arm": cfg["arm"], "seed": cfg["seed"], "params": cfg["params"],
                "outcome": out, "seconds": round(time.time() - t0, 3)}
    except Exception:
        return {"arm": cfg.get("arm"), "seed": cfg.get("seed"), "error": traceback.format_exc()}


def _compare_zero_signal(seed):
    """T1a: complex block at strength 0 must equal the simple block off, array for array."""
    from model_blocks import Params, simulate
    a = simulate(Params(seed=seed, signal_strength=0.0, prep_on=False))
    b = simulate(Params(seed=seed, use_learning=False, prep_on=False))
    diff = 0.0
    for k in ("cred", "prep", "admitted", "state", "formal"):
        x = np.nan_to_num(np.asarray(a[k], float))
        y = np.nan_to_num(np.asarray(b[k], float))
        diff = max(diff, float(np.max(np.abs(x - y))))
    for k in ("ger", "q_pub", "pay"):
        x = np.nan_to_num(np.asarray(a[k], float))
        y = np.nan_to_num(np.asarray(b[k], float))
        diff = max(diff, float(np.max(np.abs(x - y))))
    return {"seed": seed, "max_abs_diff": diff}


def _zero_selection(seed):
    """T1b: with selection_strength=0, admission must not select on ability and prep must vanish."""
    from model_blocks import Params, simulate
    full = simulate(Params(seed=seed))
    zero = simulate(Params(seed=seed, selection_strength=0.0))
    def corr(d):
        m = np.asarray(d["admitted"][:, 2], bool)
        return float(np.corrcoef(np.asarray(d["ability"])[m], m[m].astype(float))[0, 1]) if m.sum() > 2 else float("nan")
    return {"seed": seed, "ability_admission_corr_full": corr(full),
            "ability_admission_corr_zero": corr(zero),
            "prep_participation_zero": float((np.asarray(zero["prep"]) > 0).any(axis=1).mean())}


def _moments(seed, params):
    from model_blocks import Params, simulate
    from dashboard import outcomes
    o = outcomes(simulate(Params(seed=seed, **params)))
    return [o["prep_participation"], o["admission_by_quintile"][2][0], o["formal_share"],
            o["pay_by_credential"][3] / max(o["pay_by_credential"][2], 1e-9), o["queue_share"]]


def _abc_draw(args):
    i, params, truth_moments = args
    try:
        m = _moments(1000 + i, params)
        truth = np.asarray(truth_moments, float)
        got = np.asarray(m, float)
        ok = np.isfinite(got)
        if ok.sum() < 3:
            return None
        d = float(np.sqrt(np.mean(((got[ok] - truth[ok]) / np.maximum(np.abs(truth[ok]), 1e-6)) ** 2)))
        return {"draw": i, "distance": d, "params": params, "moments": m}
    except Exception:
        return None


def _ablation(args):
    """T4: shared-code ablation; each labour rival must still respond to its own parameter."""
    from model_blocks import Params, simulate
    from dashboard import outcomes
    regime, own_param, value = args
    kw = {"labour_regime": regime, "ablate_shared": True}
    if regime == "queue":
        kw["signal_noise"] = value
    else:
        kw["sigma"] = value
    o = outcomes(simulate(Params(seed=0, **kw)))
    return {"regime": regime, "param": own_param, "value": value,
            "formal_share": o["formal_share"], "queue_share": o["queue_share"],
            "pay_tertiary_over_upper": o["pay_by_credential"][3] / max(o["pay_by_credential"][2], 1e-9),
            "pay_by_quintile": o["pay_by_quintile"]}


def build_configs(abc_draws=1000):
    full = dict()
    cfgs = []
    # ---- modular one-block-at-a-time swaps (incremental build + leave-one-out ablation)
    blocks = {
        "M0_base_scalar_binary_nogate_nojobs": dict(use_components=False, use_learning=False,
                                                    use_gate=False, use_jobs=False),
        "M1_plus_affordability_components_4states": dict(use_components=True, use_learning=False,
                                                         use_gate=False, use_jobs=False),
        "M2_plus_learning_quality": dict(use_components=True, use_learning=True, use_gate=False, use_jobs=False),
        "M3_plus_gate_rank_caps": dict(use_components=True, use_learning=True, use_gate=True, use_jobs=False),
        "M4_full_plus_jobs": dict(use_components=True, use_learning=True, use_gate=True, use_jobs=True),
        "LOO_minus_affordability": dict(use_components=False),
        "LOO_minus_learning": dict(use_learning=False),
        "LOO_minus_gate": dict(use_gate=False),
        "LOO_minus_jobs": dict(use_jobs=False),
    }
    for arm, kw in blocks.items():
        cfgs += [dict(arm=arm, seed=s, params=dict(kw)) for s in MAIN_SEEDS]
    # ---- gate multiverse
    gate_arms = {
        "gate_bar_all": dict(),
        "gate_capacity_g3": dict(rules=("bar", "bar", "capacity")),
        "gate_quota030_g3": dict(rules=("bar", "bar", "quota")),
        "gate_quota015_g3": dict(rules=("bar", "bar", "quota"), quota_share=0.15),
        "gate_quota050_g3": dict(rules=("bar", "bar", "quota"), quota_share=0.50),
        "gate_exam_g3": dict(rules=("bar", "bar", "exam")),
        "gate_tullock_g3": dict(rules=("bar", "bar", "tullock")),
        "gate_quota030_g1": dict(rules=("quota", "bar", "bar")),
        "gate_bar_noprep": dict(prep_on=False),
        "gate_quota030_noprep": dict(rules=("bar", "bar", "quota"), prep_on=False),
        "gate_caps_low": dict(caps=(0.85, 0.50, 0.20)),
        "gate_caps_high": dict(caps=(1.00, 0.80, 0.45)),
        "gate_open_access": dict(use_gate=False),
    }
    for arm, kw in gate_arms.items():
        cfgs += [dict(arm=arm, seed=s, params=dict(kw)) for s in MAIN_SEEDS]
    # ---- labour rival + vacancies
    labour_arms = {
        "labour_competitive": dict(labour_regime="competitive"),
        "labour_vac_low": dict(vacancies=0.15),
        "labour_vac_high": dict(vacancies=0.35),
    }
    for arm, kw in labour_arms.items():
        cfgs += [dict(arm=arm, seed=s, params=dict(kw)) for s in MAIN_SEEDS]
    # ---- multiverse structural swaps (T5)
    multi_arms = {
        "multi_prep_concave": dict(prep_form="concave"),
        "multi_bar_concave": dict(prep_form="concave"),
        "multi_tullock_concave": dict(rules=("bar", "bar", "tullock"), prep_form="concave"),
        "multi_quota_tullock": dict(rules=("bar", "bar", "quota"), prep_form="linear"),
    }
    for arm, kw in multi_arms.items():
        cfgs += [dict(arm=arm, seed=s, params=dict(kw)) for s in MAIN_SEEDS]
    # ---- F1 shock: 30% capacity cut on held-out seeds
    for arm, kw in (("shock_caps_70_base", dict()), ("shock_caps_70_cut", dict(caps=(0.665, 0.455, 0.21)))):
        cfgs += [dict(arm=arm, seed=s, params=dict(kw)) for s in HOLD_SEEDS]
    return cfgs


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 4))
    ap.add_argument("--abc-draws", type=int, default=1000)
    ap.add_argument("--out", default=os.path.join(RESULTS, "swaps_raw.json"))
    args = ap.parse_args()
    os.makedirs(RESULTS, exist_ok=True)
    t0 = time.time()
    cfgs = build_configs()
    print(f"{len(cfgs)} model runs, {args.workers} workers", flush=True)
    with Pool(processes=args.workers) as pool:
        runs = pool.map(_run, cfgs)
    errors = [r for r in runs if "error" in r]
    for e in errors[:3]:
        print("ERROR", e["arm"], e["seed"], "\n", e["error"], flush=True)
    # test bench
    with Pool(processes=args.workers) as pool:
        zero = pool.map(_compare_zero_signal, [0, 1, 2])
        zero_sel = pool.map(_zero_selection, [0, 1, 2])
    # truth moments for the ABC from the full baseline, averaged over 3 seeds
    truth = np.mean([_moments(s, {}) for s in (0, 1, 2)], axis=0).tolist()
    prior = dict(gamma=(0.20, 0.90), quota_share=(0.0, 0.60), vacancies=(0.10, 0.40), signal_noise=(0.10, 0.90))
    truth_params = dict(gamma=0.55, quota_share=0.30, vacancies=0.25, signal_noise=0.50)
    rng = np.random.default_rng(20261125)
    draws = []
    for i in range(args.abc_draws):
        prm = {k: float(rng.uniform(*v)) for k, v in prior.items()}
        draws.append(prm)
    with Pool(processes=args.workers) as pool:
        abc = pool.map(_abc_draw, [(i, prm, truth) for i, prm in enumerate(draws)])
    abc = [a for a in abc if a is not None]
    abc.sort(key=lambda a: a["distance"])
    n_acc = max(1, int(round(0.025 * len(abc))))
    accepted = abc[:n_acc]
    ident = {}
    for k, (lo, hi) in prior.items():
        vals = np.array([a["params"][k] for a in accepted]) if accepted else np.array([])
        if len(vals) > 2:
            q05, q95 = np.quantile(vals, [0.05, 0.95])
            ident[k] = dict(prior=(lo, hi), q05=float(q05), q95=float(q95),
                            width_ratio=float((q95 - q05) / (hi - lo)),
                            truth=truth_params[k], truth_in_interval=bool(q05 <= truth_params[k] <= q95),
                            identified=bool((q95 - q05) / (hi - lo) <= 0.80))
        else:
            ident[k] = dict(prior=(lo, hi), width_ratio=None, truth=truth_params[k], identified=False)
    abl = []
    with Pool(processes=args.workers) as pool:
        for regime, param, values in (("queue", "signal_noise", (0.1, 0.9)),
                                      ("competitive", "sigma", (0.8, 3.0))):
            abl += pool.map(_ablation, [(regime, param, v) for v in values])
    meta = {
        "label": "SIMULATION — v6 gate+jobs prototype; modular block swaps + pre-declared test bench; no causal claims",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "command": " ".join([sys.executable] + sys.argv), "host": platform.node(), "python": sys.version.split()[0],
        "numpy": np.__version__, "model_dir": _model_dir(), "workers": args.workers,
        "n_model_runs": len(runs), "errors": len(errors), "wall_seconds": round(time.time() - t0, 2),
        "main_seeds": MAIN_SEEDS, "holdout_seeds": HOLD_SEEDS,
        "abc_draws": len(abc), "abc_accepted": n_acc, "abc_truth_moments": truth,
        "abc_prior": {k: list(v) for k, v in prior.items()}, "abc_truth_params": truth_params,
    }
    json.dump({"meta": meta, "runs": runs, "zero_signal_identity": zero,
               "zero_signal_selection": zero_sel, "abc_identifiability": ident,
               "shared_code_ablation": abl},
              open(args.out, "w"), indent=1)
    print(f"wrote {args.out} ({os.path.getsize(args.out) / 1e6:.2f} MB) in {meta['wall_seconds']}s; "
          f"errors={len(errors)}")
    print("T1a max diff:", max(z["max_abs_diff"] for z in zero))


if __name__ == "__main__":
    main()
