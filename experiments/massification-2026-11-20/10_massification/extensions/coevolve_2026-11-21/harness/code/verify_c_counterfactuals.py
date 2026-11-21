"""Item 3 — re-verify the three one-change counterfactuals (§8.3) from the
delivered family tables, and test how the declared argmax / correlation rule is
applied.

Recomputes, from families_<arm>.csv only:
  * the 4-type gain vector of each arm (seed by seed and as the seed mean),
  * the argmax family type,
  * the "argmax gain >= 1.5x another type" sub-criterion under two readings,
  * the three pairwise Pearson correlations of the gain vectors,
and compares every number with RUNS.json DIFFERENT-FAMILIES_detail.

No threshold is changed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C


def f(x):
    return float("nan") if x is None or str(x).strip() == "" else float(x)


def i(x):
    return int(float(x))


TYPE_LABEL = ["%s_%s" % (loc, "poor" if poor else "nonpoor") for loc, poor in C.FAMILY_TYPES]


def gains_by_seed():
    base = {}
    for r in C.family_rows("baseline"):
        base[(i(r["seed"]), r["loc_type"], i(r["poor"]))] = f(r["mean_years_completed"])
    out = {}
    for arm in C.COUNTERFACTUAL_ARMS:
        per = {}
        for r in C.family_rows(arm):
            key = (i(r["seed"]), r["loc_type"], i(r["poor"]))
            per.setdefault(i(r["seed"]), {})[(r["loc_type"], i(r["poor"]))] = (
                f(r["mean_years_completed"]) - base[key])
        out[arm] = per
    return out


def vec(d):
    return [d[t] for t in C.FAMILY_TYPES]


def pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx = sum((a - mx) ** 2 for a in x) ** 0.5
    vy = sum((b - my) ** 2 for b in y) ** 0.5
    return cov / (vx * vy)


def main():
    P = C.params()
    runs = C.read_json("RUNS.json")
    detail = runs["verdicts"]["DIFFERENT-FAMILIES_detail"]
    per = gains_by_seed()
    seed_mean = {a: [sum(per[a][s][t] for s in C.SEEDS) / len(C.SEEDS) for t in C.FAMILY_TYPES]
                 for a in C.COUNTERFACTUAL_ARMS}
    rows = []
    mism = []
    for a in C.COUNTERFACTUAL_ARMS:
        for s in C.SEEDS:
            v = vec(per[a][s])
            rows.append(dict(arm=a, seed=s, vector=v, argmax=TYPE_LABEL[max(range(4), key=lambda k: v[k])],
                             ratio=None))
        v = seed_mean[a]
        am = max(range(4), key=lambda k: v[k])
        others = [v[k] for k in range(4) if k != am]
        positives = [x for x in others if x > 0]
        d = detail
        deliv = d["gain_vectors"][a]
        for k in range(4):
            if abs(v[k] - deliv[k]) > 1e-9:
                mism.append((a, "gain_vector[%d]" % k, v[k], deliv[k]))
        if TYPE_LABEL[am] != "%s_%s" % (d["argmax"][a][0], "poor" if d["argmax"][a][1] else "nonpoor"):
            mism.append((a, "argmax", TYPE_LABEL[am], d["argmax"][a]))
        rows.append(dict(arm=a, seed="seed_mean", vector=v, argmax=TYPE_LABEL[am],
                         ratio=(v[am] / max(positives) if positives else None),
                         literal_ratio=(v[am] / max(others) if max(others) > 0 else None),
                         argmax_gain=v[am]))
    corrs = {}
    for a, b in (("travel_cut", "ordinary_expansion"),
                 ("travel_cut", "selective_expansion"),
                 ("ordinary_expansion", "selective_expansion")):
        c = pearson(seed_mean[a], seed_mean[b])
        corrs["%s_vs_%s" % (a, b)] = c
        key = "%s_vs_%s" % (a, b)
        if abs(c - detail["pairwise_correlations"][key]) > 1e-8:
            mism.append((key, "corr", c, detail["pairwise_correlations"][key]))
    # robustness: per-seed correlations and argmax
    per_seed_corr = {}
    for a, b in (("travel_cut", "ordinary_expansion"),
                 ("travel_cut", "selective_expansion"),
                 ("ordinary_expansion", "selective_expansion")):
        per_seed_corr["%s_vs_%s" % (a, b)] = [
            pearson(vec(per[a][s]), vec(per[b][s])) for s in C.SEEDS]
    argmax_per_seed = {a: [TYPE_LABEL[max(range(4), key=lambda k: per[a][s][C.FAMILY_TYPES[k]])]
                           for s in C.SEEDS] for a in C.COUNTERFACTUAL_ARMS}
    argmax_differs = len({r["argmax"] for r in rows if r["seed"] == "seed_mean"}) >= 2
    corr_falsifier = any(c >= float(P["families_corr"]) for c in corrs.values())
    ratio_ok_strict = all(r["ratio"] is not None and r["ratio"] >= float(P["families_ratio"])
                          for r in rows if r["seed"] == "seed_mean")
    # literal reading of (ii): the argmax gain is >= 1.5x *some* other type
    # (a non-positive comparator satisfies it trivially)
    ratio_ok_literal = all(
        any(per[a][s][C.FAMILY_TYPES[am]] >= float(P["families_ratio"]) * per[a][s][C.FAMILY_TYPES[k]]
            for k in range(4) if k != am)
        for a in C.COUNTERFACTUAL_ARMS for s in C.SEEDS
        for am in [max(range(4), key=lambda k: per[a][s][C.FAMILY_TYPES[k]])])
    verdict_by_rule = ("DIFFERENT" if (argmax_differs and ratio_ok_strict and not corr_falsifier)
                       else "SAME-RESPONSE")
    checks = [dict(item="C1 gain vectors recomputed from families_*.csv",
                   n_values=12, n_disagreements=len([m for m in mism if m[1].startswith("gain")]),
                   verdict="PASS" if not [m for m in mism if m[1].startswith("gain")] else "FAIL"),
              dict(item="C2 argmax family type", argmax={a: r["argmax"] for a in C.COUNTERFACTUAL_ARMS
                                                         for r in rows if r["arm"] == a and r["seed"] == "seed_mean"},
                   differs_across_arms=argmax_differs,
                   verdict="PASS" if not [m for m in mism if m[1] == "argmax"] else "FAIL"),
              dict(item="C3 pairwise correlations of the gain vectors",
                   correlations={k: round(v, 6) for k, v in corrs.items()},
                   falsifier_threshold=float(P["families_corr"]),
                   any_at_or_above_threshold=corr_falsifier,
                   verdict="PASS" if not [m for m in mism if m[1] == "corr"] else "FAIL"),
              dict(item="C4 declared rule applied to the recomputed numbers",
                   argmax_differs_across_arms=argmax_differs,
                   corr_falsifier_triggered=corr_falsifier,
                   ratio_ok_strict_positive_reading=ratio_ok_strict,
                   ratio_ok_literal_reading=ratio_ok_literal,
                   verdict_applied=verdict_by_rule,
                   delivered_verdict=runs["verdicts"]["DIFFERENT-FAMILIES"],
                   verdict="PASS" if verdict_by_rule == runs["verdicts"]["DIFFERENT-FAMILIES"] else "FAIL"),
              dict(item="C5 robustness: per-seed correlations / argmax",
                   per_seed_correlations={k: [round(x, 4) for x in v] for k, v in per_seed_corr.items()},
                   argmax_per_seed=argmax_per_seed,
                   n_seeds_with_corr_ge_threshold={k: sum(1 for x in v if x >= float(P["families_corr"]))
                                                   for k, v in per_seed_corr.items()},
                   verdict="DESCRIPTIVE")]

    C.write_csv("C_gains.csv",
                ["arm", "seed", "town_nonpoor", "town_poor", "village_nonpoor", "village_poor",
                 "argmax", "ratio_strict", "argmax_gain"],
                [[r["arm"], r["seed"]] + ["%.10g" % x for x in r["vector"]] +
                [r["argmax"], "" if r.get("ratio") is None else "%.6g" % r["ratio"],
                 "" if r.get("argmax_gain") is None else "%.10g" % r["argmax_gain"]]
                 for r in rows])
    C.write_json("C_summary.json", {"label": "SIMULATED", "checks": checks,
                                    "seed_mean_gain_vectors": {a: seed_mean[a] for a in seed_mean},
                                    "mismatches": mism,
                                    "family_type_order": TYPE_LABEL})
    for c in checks:
        print("%-58s %s" % (c["item"], c.get("verdict")))
        for k, v in c.items():
            if k not in ("item", "verdict"):
                print("    %-40s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
