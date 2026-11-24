#!/usr/bin/env python3
"""Reproduction checks for the auditor's three quoted numbers — SIMULATION ONLY.

Pre-registered in PREREGISTRATION_PHASE_SWEEP.md §5 (commit 408aa3e):
  A. "poor households exit mostly from liquidity (70.6%), not exam gates (0.8%)"
     -> run the committed multiverse's baseline combo 0 (cash_only, fixed_budget, public_only, bar,
        queue_floors, low_penalty; seed 0, N=400, T=70) with the fixed exit read and report q1 shares.
  B. "gates drive 42.4% of variance in skill_premium"
     -> one-way eta^2 of the gates axis on skill_premium from the committed multiverse raw grid
        (competitive arm), + 4-cell reproducibility re-run at the pinned engine.
  C. "learning drives 77.8% of formal_rate"
     -> one-way eta^2 of the learning axis on formal_rate (queue arm), + 4-cell re-run.

Writes results/quote_checks.json and results/QUOTE_CHECKS.md. numpy only; no causal/empirical claims.
"""
import importlib.util
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "..", "2026-11-25-masseng-edsystem")
RECORD = os.path.abspath(RECORD)
RES = os.path.join(HERE, "results")
DEV_ENGINE = "/Users/treymenefee/neon-boot/wt2/phase/engine"
AXIS_NAMES = ["afford", "supply", "learning", "gates", "jobs", "rural"]


def load_driver(engine_root):
    path = os.path.join(RECORD, "run_edsystem_multiverse.py")
    spec = importlib.util.spec_from_file_location("mdriver", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.init_engine(engine_root)
    return mod


def eta2(rows, axis_idx, metric):
    vals = []
    for r in rows:
        v = r["metrics"].get(metric)
        if v is None or not np.isfinite(v):
            continue
        vals.append((r["combo"][axis_idx], float(v)))
    if not vals:
        return None
    groups = {}
    for g, v in vals:
        groups.setdefault(g, []).append(v)
    allv = np.array([v for _, v in vals])
    grand = allv.mean()
    ss_b = sum(len(v) * (np.mean(v) - grand) ** 2 for v in groups.values())
    ss_t = float(np.sum((allv - grand) ** 2))
    return {"eta2": float(ss_b / ss_t) if ss_t > 0 else None, "n": len(allv),
            "groups": {str(k): float(np.mean(v)) for k, v in groups.items()}}


def reproduce_combo0(mod, seed=0):
    """Combo 0 (the committed RUN_REPORT baseline) with the FIXED exit read."""
    combo = ("cash_only", "fixed_budget", "public_only", "bar", "queue_floors", "low_penalty")
    mods, over = mod.combo_params(combo, seed)
    e = mod._G["worlds"].make("formal_loop", mods=mods, **over)
    out = e.run()
    pop = mod.aggregate_exits(e)     # fixed helper: e.exits + survivors (censored)
    y = np.asarray(pop["y"], float)
    reason = np.asarray(pop["reason"], int)
    started = np.asarray(pop["started"], bool)
    cut = np.quantile(y, [0.2, 0.4, 0.6, 0.8])
    q = np.searchsorted(cut, y, side="right")

    def dec(sel):
        n = int(sel.sum())
        if n == 0:
            return None
        return {"n": n,
                "liquidity": float(np.mean(reason[sel] == 1)),
                "gate_fail": float(np.mean(reason[sel] == 2)),
                "choice": float(np.mean(reason[sel] == 0)),
                "never_enrolled": float(np.mean(reason[sel] == 4)),
                "no_seat": float(np.mean(reason[sel] == 5)),
                "not_admitted": float(np.mean(reason[sel] == 6)),
                "finished": float(np.mean(reason[sel] == 3)),
                "censored": float(np.mean(reason[sel] == -1))}
    allsel = np.ones(len(reason), bool)
    meas = np.asarray(pop["cohort"]) >= 35
    exited_started = started & (reason >= 0)
    return {"combo": list(combo), "seed": seed, "N": 400, "T": 70,
            "population_all_cohorts": dec(allsel),
            "population_measured_cohorts": dec(meas),
            "q1_all_cohorts": dec(q == 0),
            "q1_measured_cohorts": dec(meas & (q == 0)),
            "liquidity_share_among_exited_started": float(np.mean(reason[exited_started] == 1))
            if exited_started.any() else None,
            "overall_liquidity_share_all": float(np.mean(reason == 1)),
            "overall_gate_fail_share_all": float(np.mean(reason == 2))}


def main():
    engine_root = sys.argv[1] if len(sys.argv) > 1 else DEV_ENGINE
    with open(os.path.join(RECORD, "results_multiverse.json")) as f:
        commit = json.load(f)
    rows = commit["rows"]
    mod = load_driver(engine_root)

    res = {"label": "SIMULATION ONLY - reproduction checks; no causal/empirical claims",
           "preregistration": "PREREGISTRATION_PHASE_SWEEP.md (commit 408aa3e) §5",
           "engine_root": engine_root,
           "committed_raw": os.path.join(RECORD, "results_multiverse.json"),
           "committed_raw_sha256_prefix": os.popen(f"shasum -a 256 {os.path.join(RECORD, 'results_multiverse.json')}"
                                                   ).read().split()[0][:16] if sys.platform == "darwin" else None}

    # ---- A: exit decomposition, baseline combo 0 with fixed read (+ seed spread of the q1 quote)
    res["A"] = reproduce_combo0(mod, 0)
    spread = []
    for s in range(5):
        a = reproduce_combo0(mod, s)
        spread.append({"seed": s, "q1_liquidity": a["q1_all_cohorts"]["liquidity"],
                       "q1_gate_fail": a["q1_all_cohorts"]["gate_fail"],
                       "overall_liquidity": a["overall_liquidity_share_all"]})
    arr = np.array([[x["q1_liquidity"], x["q1_gate_fail"]] for x in spread])
    res["A_seed_spread"] = {"per_seed": spread, "mean": arr.mean(0).tolist(),
                            "sd": arr.std(0, ddof=1).tolist()}

    # ---- B/C: eta^2 from the committed raw grid (these metrics are NOT affected by the exit-reason bug)
    comp = [r for r in rows if r["combo"][4] == "competitive"]
    que = [r for r in rows if r["combo"][4] == "queue_floors"]
    etaB_all = {AXIS_NAMES[i]: eta2(comp, i, "skill_premium") for i in range(6)}
    etaC_all = {AXIS_NAMES[i]: eta2(que, i, "formal_rate") for i in range(6)}
    res["B"] = {"metric": "skill_premium", "arm": "competitive", "n_rows": len(comp),
                "eta2_by_axis": etaB_all, "quoted_value": 0.424,
                "computed_gates_eta2": (etaB_all["gates"] or {}).get("eta2")}
    res["C"] = {"metric": "formal_rate", "arm": "queue_floors", "n_rows": len(que),
                "eta2_by_axis": etaC_all, "quoted_value": 0.778,
                "computed_learning_eta2": (etaC_all["learning"] or {}).get("eta2")}

    # ---- reproducibility re-runs: 4 cells each (2 combos x 2 seeds)
    combo_by_index = {}
    for r in rows:
        combo_by_index[r["combo_index"]] = tuple(r["combo"])

    def rerun(ci, seed):
        # rows are ordered (combo, seed); index by the explicit combo_index field, never list position
        return mod.one((ci, combo_by_index[ci], seed))

    def lookup(ci, seed, metric):
        for r in rows:
            if r["combo_index"] == ci and r["seed"] == seed:
                return r["metrics"].get(metric)
        return None

    rep = []
    for ci in (37, 71):
        for s in (0, 1):
            rec = rerun(ci, s)
            rep.append({"combo_index": ci, "seed": s, "metric": "skill_premium",
                        "committed": lookup(ci, s, "skill_premium"),
                        "rerun": rec["metrics"].get("skill_premium")})
    for ci in (0, 36):
        for s in (0, 1):
            rec = rerun(ci, s)
            rep.append({"combo_index": ci, "seed": s, "metric": "formal_rate",
                        "committed": lookup(ci, s, "formal_rate"),
                        "rerun": rec["metrics"].get("formal_rate")})
    for r in rep:
        if r["committed"] is not None and r["rerun"] is not None:
            r["abs_diff"] = abs(r["committed"] - r["rerun"])
    res["reproducibility_reruns"] = rep
    res["max_abs_diff"] = (max((r.get("abs_diff", 0.0) for r in rep), default=None))

    with open(os.path.join(RES, "quote_checks.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({"A_q1_liquidity": res["A"]["q1_all_cohorts"]["liquidity"],
                      "A_q1_gate_fail": res["A"]["q1_all_cohorts"]["gate_fail"],
                      "B_gates_eta2_skill_premium": res["B"]["computed_gates_eta2"],
                      "C_learning_eta2_formal_rate": res["C"]["computed_learning_eta2"],
                      "max_rerun_diff": res["max_abs_diff"]}, indent=1))


if __name__ == "__main__":
    main()
