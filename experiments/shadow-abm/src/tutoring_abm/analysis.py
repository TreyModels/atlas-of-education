"""Posterior summaries, policy experiments, discriminating signatures, sensitivity and robustness."""
import json
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata
import model
from model import PRIORS, VARIANTS, World
from smc import to_params
from calibrate import TARGETS, distances, CAL_WORLDS

R = Path("results")
POLICIES = {
    "baseline": {},
    "ban_own": {"ban_own": True},
    "cond_pay": {"cond_pay": 0.3},
    "extra_time": {"extra_time": 0.10},
    "com_entry": {"com_entry": 1.5},
}
OUTCOMES = ["participation", "participation_q1", "participation_q5", "own_purchase_share",
            "other_purchase_share", "com_purchase_share", "teacher_tutor_share", "teacher_own_share",
            "withholding_mean", "class_instruction", "nonbuyer_class_instruction", "coverage",
            "coverage_q1", "coverage_q5"]


def load(variant):
    d = json.loads((R / f"posterior_{variant}.json").read_text())
    df = pd.DataFrame(d["particles"])
    df["weight"] = df["weight"] / df["weight"].sum()
    return d, df


def policy_job(args):
    variant, i, names, x, seed = args
    base = to_params(names, x)
    rows = []
    for name, change in POLICIES.items():
        out = World(replace(base, **change), seed).solve().outcomes()
        rows.append({"variant": variant, "particle": i, "world": seed, "policy": name, **out})
    return rows


def robustness_job(args):
    variant, i, names, x, seed, label = args
    saved = (model.CLASS_SIZE, model.TUTOR_CONTENT, model.FEE[12], model.SCHOOLS, model.SUBJECT_OFFSETS)
    if label == "class_size_50":
        model.CLASS_SIZE = 50
    elif label == "tutor_content_0.10":
        model.TUTOR_CONTENT = 0.10
    elif label == "fee12_1.0":
        model.FEE[12] = 1.0
    elif label == "one_urban_school":
        model.SCHOOLS = [("lower", False), ("lower", False), ("lower", False),
                         ("high", True), ("high", False), ("high", False)]
    elif label == "flat_subjects":
        model.SUBJECT_OFFSETS = np.zeros(4)
    try:
        p = to_params(names, x)
        base = World(p, seed).solve().outcomes()
        ban = World(replace(p, ban_own=True), seed).solve().outcomes()
    finally:
        model.CLASS_SIZE, model.TUTOR_CONTENT, model.FEE[12], model.SCHOOLS, model.SUBJECT_OFFSETS = saved
    z = distances(base)
    return {"variant": variant, "particle": i, "assumption": label, "fits": int(max(z.values()) <= 1),
            "max_z": max(z.values()), "withholding_mean": base["withholding_mean"],
            "ban_nonbuyer_instr": ban["nonbuyer_class_instruction"] - base["nonbuyer_class_instruction"],
            "ban_participation": ban["participation"] - base["participation"]}


def wq(values, weights, qs=(.05, .5, .95)):
    o = np.argsort(values); v, w = np.asarray(values)[o], np.asarray(weights)[o]
    c = np.cumsum(w) / w.sum()
    return [float(np.interp(q, c, v)) for q in qs]


def prcc(X, y):
    Xr = np.column_stack([rankdata(c) for c in X.T]); yr = rankdata(y)
    out = []
    for j in range(Xr.shape[1]):
        others = np.column_stack([np.ones(len(yr)), np.delete(Xr, j, axis=1)])
        rx = Xr[:, j] - others @ np.linalg.lstsq(others, Xr[:, j], rcond=None)[0]
        ry = yr - others @ np.linalg.lstsq(others, yr, rcond=None)[0]
        out.append(float(np.corrcoef(rx, ry)[0, 1]))
    return out


def main():
    global VARIANTS
    VARIANTS = [v for v in model.VARIANTS if (R / f"posterior_{v}.json").exists()]
    summary = {"targets": {k: v for k, v in TARGETS.items()}, "variants": {}}
    jobs, rob_jobs = [], []
    posts = {}
    for variant in VARIANTS:
        d, df = load(variant)
        posts[variant] = (d, df)
        names = d["free"]
        info = {"evidence": d["evidence"], "history": d["history"], "n": len(df),
                "converged_share": float(df["converged"].mean()), "parameters": {}, "fit": {}}
        for n in names:
            lo, hi = PRIORS[n]
            q = wq(df[n], df["weight"])
            sd_post = float(np.sqrt(np.cov(df[n], aweights=df["weight"])))
            info["parameters"][n] = {"q05_q50_q95": q, "prior": [lo, hi],
                                     "contraction": 1 - sd_post / ((hi - lo) / np.sqrt(12))}
        for k in ["participation", "participation_g9", "participation_g12", "participation_urban",
                  "participation_rural", "own_purchase_share", "other_purchase_share",
                  "com_purchase_share", "teacher_tutor_share", "own_share", "other_share",
                  "subjects_bought", "withholding_mean", "teacher_own_share"]:
            info["fit"][k] = wq(df[k], df["weight"])
        summary["variants"][variant] = info
        for i, row in df.iterrows():
            x = [row[n] for n in names]
            for w in CAL_WORLDS:
                jobs.append((variant, i, names, x, int(w)))
                if i < 100:
                    for label in ("class_size_50", "tutor_content_0.10", "fee12_1.0", "one_urban_school", "flat_subjects"):
                        rob_jobs.append((variant, i, names, x, int(w), label))
    with Pool(8) as pool:
        pol = [r for rows in pool.map(policy_job, jobs, chunksize=10) for r in rows]
        rob = pool.map(robustness_job, rob_jobs, chunksize=10)
    pol = pd.DataFrame(pol); rob = pd.DataFrame(rob)
    pol.to_csv(R / "policy_runs.csv", index=False); rob.to_csv(R / "robustness_runs.csv", index=False)
    # policy effects (paired differences from baseline), weighted by particle weight
    effects = {}
    for variant in VARIANTS:
        d, df = posts[variant]
        base = pol[(pol.variant == variant) & (pol.policy == "baseline")].set_index(["particle", "world"]).sort_index()
        w = df["weight"].reindex(base.index.get_level_values("particle")).values
        effects[variant] = {}
        for policy in POLICIES:
            if policy == "baseline":
                continue
            p = pol[(pol.variant == variant) & (pol.policy == policy)].set_index(["particle", "world"]).sort_index()
            effects[variant][policy] = {}
            for k in OUTCOMES:
                diff = (p[k] - base[k]).values
                effects[variant][policy][k] = wq(diff, w)
            gap_b = (base["coverage_q5"] - base["coverage_q1"]).values
            gap_p = (p["coverage_q5"] - p["coverage_q1"]).values
            effects[variant][policy]["coverage_gap_q5_q1"] = wq(gap_p - gap_b, w)
        sig = {}
        sig["buy_gap_tutoring_vs_not"] = wq((base["buy_tutoring_teacher"] - base["buy_nontutoring_teacher"]).values, w)
        sig["instr_gap_tutoring_vs_not"] = wq((base["instr_tutoring_teacher"] - base["instr_nontutoring_teacher"]).values, w)
        sig["other_ratio_tutoring_vs_not"] = wq((base["other_given_tutoring_teacher"] / base["other_given_nontutoring_teacher"]).values, w)
        summary["variants"][variant]["signatures"] = sig
    summary["policy_effects"] = effects
    # sensitivity: PRCC of parameters on key quantities within the richest available posterior
    d, df = posts["full" if "full" in posts else VARIANTS[-1]]
    names = d["free"]
    pv = d["variant"]
    base = pol[(pol.variant == pv) & (pol.policy == "baseline")].groupby("particle").mean(numeric_only=True).loc[df.index]
    ban = pol[(pol.variant == pv) & (pol.policy == "ban_own")].groupby("particle").mean(numeric_only=True).loc[df.index]
    X = df[names].values
    targets = {"withholding_mean": base["withholding_mean"].values,
               "own_purchase_share": base["own_purchase_share"].values,
               "ban_effect_nonbuyer_instruction": (ban["nonbuyer_class_instruction"] - base["nonbuyer_class_instruction"]).values,
               "ban_effect_participation": (ban["participation"] - base["participation"]).values}
    summary["prcc_full_posterior"] = {k: dict(zip(names, prcc(X, y))) for k, y in targets.items()}
    # prior-wide sensitivity of withholding (pilot prior runs, full variant)
    pr = pd.read_csv(R / "pilot_k10.csv") if (R / "pilot_k10.csv").exists() else None
    if pr is not None:
        pf = pr[pr.variant == "full"]
        pn = [n for n in PRIORS]
        summary["prcc_full_prior"] = {k: dict(zip(pn, prcc(pf[pn].values, pf[k].values)))
                                      for k in ("withholding_mean", "participation", "own_purchase_share")}
    summary["robustness"] = {
        v: {a: {"fit_share": float(g["fits"].mean()), "withholding_median": float(g["withholding_mean"].median()),
                "ban_nonbuyer_instr_median": float(g["ban_nonbuyer_instr"].median()),
                "ban_participation_median": float(g["ban_participation"].median())}
            for a, g in rob[rob.variant == v].groupby("assumption")}
        for v in VARIANTS}
    (R / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({v: summary["variants"][v]["evidence"] for v in VARIANTS}, indent=1))


if __name__ == "__main__":
    main()
