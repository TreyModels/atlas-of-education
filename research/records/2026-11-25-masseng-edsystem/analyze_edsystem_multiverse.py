#!/usr/bin/env python3
"""Analysis of the eduengine full-system multiverse: variance decomposition by equation choice,
non-identification ranges, group tables (push-out, prep purchases, tutoring pile-up), PHL check.

Pre-registered analysis in PRE_REGISTRATION_masseng_edsystem.md. Simulation only; no causal claims.
"""
import argparse
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
AXES = ["afford", "supply", "learning", "gates", "jobs", "rural"]
OUTCOMES = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
            "q_pub", "formal_share_gdp", "edu_gdp", "tut_rate", "mpl_primary",
            "parity_location_lower", "parity_wealth_lower"]


def clean(v):
    return v if v is not None else np.nan


def eta2(values, axis_vals):
    v = np.asarray(values, float)
    ok = np.isfinite(v)
    v, a = v[ok], np.asarray(axis_vals)[ok]
    if len(v) < 3 or len(set(a)) < 2 or np.var(v) == 0:
        return float("nan")
    grand = v.mean()
    ssb = 0.0
    for level in sorted(set(a)):
        g = v[a == level]
        ssb += len(g) * (g.mean() - grand) ** 2
    sst = np.sum((v - grand) ** 2)
    return float(ssb / sst) if sst > 0 else float("nan")


def ranges_overlap(values, axis_vals, q=(5, 95)):
    """Return worst pairwise 5-95 overlap fraction across variant levels (0=disjoint, 1=identical)."""
    rng = {}
    for level in sorted(set(axis_vals)):
        v = np.asarray(values, float)[np.asarray(axis_vals) == level]
        v = v[np.isfinite(v)]
        if len(v) < 5:
            continue
        rng[level] = (float(np.percentile(v, q[0])), float(np.percentile(v, q[1])))
    worst = 1.0
    for i, a in enumerate(sorted(rng)):
        for b in sorted(rng)[i + 1:]:
            lo = max(rng[a][0], rng[b][0]); hi = min(rng[a][1], rng[b][1])
            union = max(rng[a][1], rng[b][1]) - min(rng[a][0], rng[b][0])
            frac = max(0.0, hi - lo) / union if union > 0 else 1.0
            worst = min(worst, frac) if len(rng) > 1 else worst
            worst = min(worst, frac)
    return float(worst) if rng else float("nan")


def summarize(rows, axes_map):
    recs = []
    for r in rows:
        d = {"axes": {a: r["combo"][i] for i, a in enumerate(AXES)}, "seed": r["seed"]}
        for m in OUTCOMES:
            d[m] = clean(r["metrics"].get(m))
        g = r["groups"]
        d["started_liquidity_share"] = g.get("started_liquidity_share")
        d["started_choice_share"] = g.get("started_choice_share")
        d["tut_q_gap_q5_q1"] = g.get("tut_q_gap_q5_q1")
        d["tut_gate_mass_share"] = g.get("tut_gate_mass_share")
        d["tut_gate_adjacent"] = g.get("tut_gate_adjacent")
        d["tut_non_gate"] = g.get("tut_non_gate")
        for lvl in ("lower", "upper", "tertiary"):
            d[f"completion_{lvl}_q_gap"] = g.get(f"completion_{lvl}_q_gap")
        for k2, v in (g.get("tut_level_share") or {}).items():
            d[f"tut_level_share_{k2}"] = v
        for q in range(5):
            qd = g.get(f"q{q+1}") or {}
            d[f"q{q+1}_liquidity"] = qd.get("liquidity")
            d[f"q{q+1}_choice"] = qd.get("choice")
            d[f"q{q+1}_never"] = qd.get("never")
            d[f"q{q+1}_started"] = qd.get("started_share")
        for grp in ("urban", "rural"):
            gd = g.get(grp) or {}
            d[f"{grp}_liquidity"] = gd.get("liquidity")
            d[f"{grp}_choice"] = gd.get("choice")
            d[f"{grp}_never"] = gd.get("never")
            d[f"{grp}_started"] = gd.get("started_share")
        recs.append(d)
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="results_multiverse.json")
    ap.add_argument("--out", default="summary_multiverse.json")
    a = ap.parse_args()
    data = json.load(open(os.path.join(HERE, a.inp)))
    recs = summarize(data["rows"], data["design"]["axes"])
    outcomes = OUTCOMES + ["started_liquidity_share", "started_choice_share", "tut_q_gap_q5_q1",
                            "tut_gate_mass_share", "tut_gate_adjacent", "tut_non_gate",
                            "completion_lower_q_gap", "completion_upper_q_gap", "completion_tertiary_q_gap",
                            "tut_level_share_primary", "tut_level_share_lower", "tut_level_share_upper",
                            "tut_level_share_tertiary", "formal_rate", "skill_premium"]
    var = {}
    for m in outcomes:
        var[m] = {}
        for ax in AXES:
            vals = [r.get(m, np.nan) for r in recs]
            axv = [r["axes"][ax] for r in recs]
            var[m][ax] = {"eta2": eta2(vals, axv), "worst_range_overlap": ranges_overlap(vals, axv)}
    # marginal means by axis variant for key outcomes
    marg = {}
    for m in ["completion_lower", "completion_upper", "completion_tertiary", "tut_rate",
              "q_pub", "formal_share_gdp", "started_liquidity_share", "tut_q_gap_q5_q1"]:
        marg[m] = {}
        for ax in AXES:
            marg[m][ax] = {}
            for lvl in sorted({r["axes"][ax] for r in recs}):
                v = np.array([r.get(m, np.nan) for r in recs if r["axes"][ax] == lvl], float)
                v = v[np.isfinite(v)]
                if len(v):
                    marg[m][ax][lvl] = {"mean": float(v.mean()),
                                        "ci90": [float(np.percentile(v, 5)), float(np.percentile(v, 95))],
                                        "n": int(len(v))}
    # group tables: baseline combo (first variant on every axis)
    base_combo = tuple(v[0] for v in data["design"]["axes"].values())
    base = [r for r in recs if r["axes"] == dict(zip(AXES, base_combo))]
    def mmean(rs, key):
        v = np.array([r.get(key, np.nan) for r in rs], float); v = v[np.isfinite(v)]
        return {"mean": float(v.mean()), "ci90": [float(np.percentile(v, 5)), float(np.percentile(v, 95))]} if len(v) else None
    groups = {}
    for q in range(5):
        groups[f"q{q+1}"] = {k: mmean(base, f"q{q+1}_{k}") for k in ("liquidity", "choice", "never", "started")}
    for g in ("urban", "rural"):
        groups[g] = {k: mmean(base, f"{g}_{k}") for k in ("liquidity", "choice", "never", "started")}
    tutoring = {"tut_rate": mmean(base, "tut_rate"), "tut_q_gap_q5_q1": mmean(base, "tut_q_gap_q5_q1"),
                "tut_gate_adjacent": mmean(base, "tut_gate_adjacent"), "tut_non_gate": mmean(base, "tut_non_gate"),
                "tut_gate_mass_share": mmean(base, "tut_gate_mass_share")}
    for lvl in ("primary", "lower", "upper", "tertiary"):
        tutoring[f"share_{lvl}"] = mmean(base, f"tut_level_share_{lvl}")
    # PHL check
    phl = {}
    p = os.path.join(HERE, "phl_lsc.json")
    if os.path.exists(p):
        obs = json.load(open(p))
        if obs:
            latest = max(obs, key=lambda x: x["year"])
            sim = np.array([r.get("completion_lower", np.nan) for r in recs], float)
            sim = sim[np.isfinite(sim)]
            phl = {"observed_series": obs, "latest": latest,
                   "simulated_completion_lower": {"mean": float(sim.mean()),
                                                  "ci90": [float(np.percentile(sim, 5)), float(np.percentile(sim, 95))]},
                   "note": "construct-limited: UIS/WDI lsc is lower-secondary completion; simulated completion_lower is a toy share; not a calibration."}
    summary = {"label": data["label"], "design": data["design"], "elapsed_s": data["elapsed_s"],
               "n_runs": len(recs), "variance_decomposition": var, "marginal_means": marg,
               "baseline_group_table": groups, "baseline_tutoring": tutoring, "phl_check": phl,
               "non_identifiable_outcomes": {m: {ax: v for ax, v in var[m].items() if v["worst_range_overlap"] >= 0.8}
                                             for m in outcomes}}
    with open(os.path.join(HERE, a.out), "w") as f:
        json.dump(summary, f, indent=1)
    # print key ranking
    print(json.dumps({"runs": len(recs), "top_movers_by_outcome": {
        m: sorted(var[m].items(), key=lambda kv: -(kv[1]["eta2"] or 0))[0][0] for m in outcomes}, "elapsed_s": data["elapsed_s"]}, indent=1)[:4000])


if __name__ == "__main__":
    main()
