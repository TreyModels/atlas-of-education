#!/usr/bin/env python3
"""Analysis for X1 (exposure-matched sequencing) and X3 (feedback-elasticity surface).

Reads the committed seed-level result JSONs (produced by run_x1_x3.py on region-42), applies the
pre-declared material thresholds / decision categories / falsifier rules from
PRE_REGISTRATION_masseng_staging_x1_x3.md, and writes audit_tables/summary_x1.json and
summary_x3.json. No causal interpretation; simulation only.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audit_tables")
META_HASH = "20261125"  # analysis bootstrap seed (declared here, not tuned)
RNG = np.random.default_rng(20261125)
B = 4000

SCALARS = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
           "tut_rate", "mpl_primary", "q_pub", "formal_share_gdp", "edu_gdp",
           "parity_location_lower", "parity_wealth_lower", "parity_location_upper", "parity_wealth_upper"]
COMPLETIONS = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary"]
FAMILY_EXPOSURE = ["formal_share_gdp", "edu_gdp", "q_pub"]
FAMILY_COMPLETION_EQUITY = COMPLETIONS + ["tut_rate", "parity_location_lower", "parity_wealth_lower",
                                          "parity_location_upper", "parity_wealth_upper"]
MATERIAL_THRESH = {m: 0.005 for m in COMPLETIONS}
MATERIAL_THRESH.update({m: 0.02 for m in (FAMILY_EXPOSURE + FAMILY_COMPLETION_EQUITY) if m not in COMPLETIONS})
MATERIAL_THRESH["mpl_primary"] = 0.02  # reported only; not in a decision family


def boot_ci(d, q=0.95):
    bs = np.mean(RNG.choice(d, size=(B, len(d)), replace=True), axis=1)
    return [float(np.quantile(bs, (1 - q) / 2)), float(np.quantile(bs, 1 - (1 - q) / 2))]


def stats(d):
    d = np.asarray(d, float)
    mean = float(d.mean())
    ci90 = boot_ci(d, 0.90)
    ci95 = boot_ci(d, 0.95)
    loo = [float(np.delete(d, i).mean()) for i in range(len(d))]
    return {"n": int(len(d)), "mean": mean, "sd": float(d.std(ddof=1)),
            "ci90": ci90, "ci95": ci95,
            "n_pos": int((d > 0).sum()), "n_neg": int((d < 0).sum()),
            "sign_stable": bool((d > 0).all() or (d < 0).all()),
            "sign_stable_loo": bool(len(set(np.sign(loo))) == 1),
            "min": float(d.min()), "max": float(d.max()),
            "per_seed": [float(x) for x in d],
            "ci90_excludes_zero": bool(ci90[0] > 0 or ci90[1] < 0)}


def material(m, st):
    thr = MATERIAL_THRESH[m]
    return bool(abs(st["mean"]) >= thr and st["ci90_excludes_zero"])


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def rows_x1(d):
    out = {}
    for r in d["rows"]:
        out.setdefault((r["arm"], r["feedback"], r["gate"]), {})[r["seed"]] = r
    return out


def contrast(by, cond, a, b, metric):
    left, right = by[(a,) + cond], by[(b,) + cond]
    seeds = sorted(set(left) & set(right))
    return [left[s]["metrics"][metric] - right[s]["metrics"][metric] for s in seeds]


def exposure_check(d):
    exp = d["config"]["exposure_arithmetic"]
    return {k: {"education_share_years": round(v["education_share_years"], 4),
                "vacancy_years": round(v["vacancy_years"], 4)} for k, v in exp.items()}


# ----------------------------------------------------------------------------- X1
def analyse_x1():
    fn = "results_x1_EXPLORATORY_corrected.json"
    if not os.path.exists(os.path.join(HERE, fn)):
        fn = "results_x1_EXPLORATORY.json"
    d = load(fn)
    by = rows_x1(d)
    arms = d["config"]["arms"]
    out = {"label": "X1 exposure-matched sequencing — pre-declared analysis",
           "source_file": fn,
           "experiment": "x1", "runs": len(d["rows"]), "elapsed_s": d["elapsed_s"],
           "exposure_check": exposure_check(d),
           "thresholds": {"completions_abs_pp": 0.005, "other_metrics_abs": 0.02,
                          "ci": "90% seed bootstrap excludes 0", "matched_approx_zero": "90% CI includes 0 and |matched| <= 0.25|unmatched|"},
           "conditions": {}}
    overall_cats = []
    for fb in (0.0, 1.0):
        for gate in ("bar", "quota"):
            cname = f"feedback_{fb:g}_gates_{gate}"
            cond = {"contrasts": {}}
            cond_key = (fb, gate)
            cont = {name: {m: stats(contrast(by, cond_key, a, b, m)) for m in SCALARS}
                    for name, (a, b) in {
                        "unmatched_school_minus_jobs": ("school_first", "jobs_first"),
                        "matched_school_minus_jobs": ("matched_school_first", "matched_jobs_first"),
                        "matched_school_minus_matched_simultaneous": ("matched_school_first", "matched_simultaneous"),
                        "matched_jobs_minus_matched_simultaneous": ("matched_jobs_first", "matched_simultaneous"),
                        "placebo_shifted_school_minus_jobs": ("shifted_school_first", "shifted_jobs_first"),
                    }.items()}
            cond["contrasts"] = cont
            # per-metric materiality + matched comparison
            per_metric = {}
            for m in SCALARS:
                um = material(m, cont["unmatched_school_minus_jobs"][m])
                mm = material(m, cont["matched_school_minus_jobs"][m])
                matched = cont["matched_school_minus_jobs"][m]
                unmatched = cont["unmatched_school_minus_jobs"][m]
                approx_zero = bool(matched["ci90"][0] <= 0 <= matched["ci90"][1]
                                   and unmatched["mean"] != 0
                                   and abs(matched["mean"]) <= 0.25 * abs(unmatched["mean"]))
                per_metric[m] = {
                    "family": ("exposure" if m in FAMILY_EXPOSURE else
                               "completion_equity" if m in FAMILY_COMPLETION_EQUITY else "reported_only"),
                    "unmatched_material": um, "matched_material": mm,
                    "matched_approx_zero": approx_zero,
                    "unmatched_mean": unmatched["mean"], "matched_mean": matched["mean"],
                    "ratio_matched_over_unmatched": (abs(matched["mean"]) / abs(unmatched["mean"])
                                                     if unmatched["mean"] != 0 else None),
                }
            # pre-declared decision categories
            any_unmatched_material = any(per_metric[m]["unmatched_material"] for m in SCALARS)
            a_family_i = [m for m in FAMILY_EXPOSURE if per_metric[m]["unmatched_material"] and per_metric[m]["matched_approx_zero"]]
            a_family_ii = [m for m in FAMILY_COMPLETION_EQUITY if per_metric[m]["unmatched_material"] and per_metric[m]["matched_approx_zero"]]
            b_metrics = [m for m in FAMILY_COMPLETION_EQUITY
                         if per_metric[m]["matched_material"]
                         and np.sign(per_metric[m]["matched_mean"]) == np.sign(per_metric[m]["unmatched_mean"])]
            if not any_unmatched_material:
                cats = ["C"]
            else:
                cats = []
                if a_family_i or a_family_ii:
                    cats.append("A")
                if b_metrics:
                    cats.append("B")
                if not cats:
                    cats.append("D")
            # placebo check on material unmatched metrics
            placebo = {}
            for m in SCALARS:
                if per_metric[m]["unmatched_material"]:
                    p = cont["placebo_shifted_school_minus_jobs"][m]
                    u = cont["unmatched_school_minus_jobs"][m]
                    placebo[m] = {
                        "placebo_mean": p["mean"], "unmatched_mean": u["mean"],
                        "difference": p["mean"] - u["mean"],
                        "placebo_ci90": p["ci90"], "unmatched_ci90": u["ci90"],
                        "outside_unmatched_ci": bool(p["mean"] < u["ci90"][0] or p["mean"] > u["ci90"][1]),
                    }
            cond.update({"per_metric": per_metric, "categories": cats,
                         "a_family_i_metrics": a_family_i, "a_family_ii_metrics": a_family_ii,
                         "b_metrics": b_metrics,
                         "placebo_on_material_metrics": placebo,
                         "description": f"feedback={fb:g}, gates={gate}"})
            overall_cats.append({"condition": cname, "categories": cats})
            out["conditions"][cname] = cond
    # overall (>=3/4 rule), per family
    def overall(family):
        cats = []
        for c in out["conditions"].values():
            if family == "exposure":
                ok = bool(c["a_family_i_metrics"])
                cats.append("A" if ok else ("C" if not any(c["per_metric"][m]["unmatched_material"] for m in FAMILY_EXPOSURE) else "D"))
            else:
                ok = bool(c["a_family_ii_metrics"]) or bool(c["b_metrics"])
                cats.append("A" if c["a_family_ii_metrics"] else ("B" if c["b_metrics"] else ("C" if not any(c["per_metric"][m]["unmatched_material"] for m in FAMILY_COMPLETION_EQUITY) else "D")))
        from collections import Counter
        cnt = Counter(cats)
        top, n = cnt.most_common(1)[0]
        return {"per_condition": cats, "counts": dict(cnt), "overall": top if n >= 3 else "inconsistent"}
    out["overall"] = {"exposure_family": overall("exposure"),
                      "completion_equity_family": overall("completion_equity")}
    # expected-outcome check (pre-declared anticipation)
    out["anticipated_outcome_check"] = {
        "declared": "A on exposure-sensitive family and C on completion/equity family (audit prior)",
        "observed": {"exposure_family": out["overall"]["exposure_family"]["overall"],
                     "completion_equity_family": out["overall"]["completion_equity_family"]["overall"]},
    }
    with open(os.path.join(OUT, "summary_x1.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


# ----------------------------------------------------------------------------- X3
def analyse_x3():
    d = load("results_x3_EXPLORATORY.json")
    by = {}
    for r in d["rows"]:
        by.setdefault((r["arm"], r["elasticity"], r["gate"]), {})[r["seed"]] = r
    elasts = d["config"]["elasticities"]
    out = {"label": "X3 feedback-elasticity surface — pre-declared analysis",
           "experiment": "x3", "runs": len(d["rows"]), "elapsed_s": d["elapsed_s"],
           "elasticities": elasts, "gates": ["bar", "quota"], "surface": {}}
    for gate in ("bar", "quota"):
        out["surface"][gate] = {}
        for e in elasts:
            cell = {}
            for name, (a, b) in {"school_minus_jobs": ("school_first", "jobs_first"),
                                 "simultaneous_minus_none": ("simultaneous", "none")}.items():
                cell[name] = {}
                for m in SCALARS:
                    left, right = by[(a, e, gate)], by[(b, e, gate)]
                    seeds = sorted(set(left) & set(right))
                    diffs = [left[s]["metrics"][m] - right[s]["metrics"][m] for s in seeds]
                    st = stats(diffs)
                    st["material"] = material(m, st)
                    cell[name][m] = st
            out["surface"][gate][str(e)] = cell
    # verdict per metric per contrast across the elasticity grid
    verdicts = {}
    for gate in ("bar", "quota"):
        for name in ("school_minus_jobs", "simultaneous_minus_none"):
            for m in SCALARS:
                cells = [out["surface"][gate][str(e)][name][m] for e in elasts]
                mats = [c["material"] for c in cells]
                signs = [np.sign(c["mean"]) for c in cells]
                if all(mats) and len(set(signs)) == 1:
                    v = "ROBUST"
                elif any(mats) and len({s for c, s in zip(cells, signs) if c["material"]}) > 1:
                    v = "REVERSAL"
                elif not any(mats):
                    v = "NULL"
                else:
                    v = "MIXED"
                verdicts.setdefault(f"{gate}|{name}", {})[m] = {
                    "verdict": v,
                    "means_by_elasticity": {str(e): cells[i]["mean"] for i, e in enumerate(elasts)},
                    "ci90_by_elasticity": {str(e): cells[i]["ci90"] for i, e in enumerate(elasts)},
                    "material_by_elasticity": {str(e): mats[i] for i, e in enumerate(elasts)},
                    "signs_by_elasticity": {str(e): float(signs[i]) for i, e in enumerate(elasts)},
                }
    out["verdicts"] = verdicts
    # headline summary for the pre-declared contrasts
    out["headline"] = {}
    for key, block in verdicts.items():
        from collections import Counter
        c = Counter(x["verdict"] for x in block.values())
        out["headline"][key] = dict(c)
    with open(os.path.join(OUT, "summary_x3.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    s1 = analyse_x1()
    print("X1 overall:", json.dumps(s1["overall"], indent=1))
    print("X1 anticipated check:", json.dumps(s1["anticipated_outcome_check"]))
    if os.path.exists(os.path.join(HERE, "results_x3_EXPLORATORY.json")):
        s3 = analyse_x3()
        print("X3 headline:", json.dumps(s3["headline"], indent=1))
    else:
        print("X3 results not present yet; X1 only")
