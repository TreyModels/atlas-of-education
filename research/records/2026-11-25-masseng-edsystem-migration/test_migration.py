#!/usr/bin/env python3
"""Statistical tests of the full-system multiverse (eduengine, 1,440 runs).

For each design-axis contrast and outcome: OLS with all main effects + seed fixed effects,
cluster-robust SEs by design cell (combo), 95% CI, Holm correction across outcomes, and a
stratum check (does the sign hold across every level of the other axes?).

This tests whether the reported multiverse effects are statistical regularities of the
simulated design, not whether they are true of the world (toy worlds; no causal claims).
"""
import json, math, sys
from itertools import product
import numpy as np

SRC = "results_migration.json"
OUT = "migration_tests.json"

OUTCOMES = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
            "tut_rate", "formal_share_gdp", "parity_wealth_lower", "skill_premium", "q_pub"]


def norm_p(t):
    # two-sided normal p
    return math.erfc(abs(t) / math.sqrt(2.0))


def cluster_ols(y, X, groups, j):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    XtX_inv = np.linalg.pinv(X.T @ X)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for g in np.unique(groups):
        m = groups == g
        s = X[m].T @ resid[m]
        meat += np.outer(s, s)
    G = len(np.unique(groups))
    n, p = X.shape
    corr = (G / (G - 1)) * ((n - 1) / (n - p)) if G > 1 and n > p else 1.0
    V = XtX_inv @ meat @ XtX_inv * corr
    se = math.sqrt(max(V[j, j], 0.0))
    return float(beta[j]), se


def holm(pvals):
    order = np.argsort(pvals)
    m = len(pvals)
    adj = np.empty(m)
    prev = 0.0
    for rank, idx in enumerate(order):
        val = min(1.0, (m - rank) * pvals[idx])
        prev = max(prev, val)
        adj[idx] = prev
    return adj


def main():
    d = json.load(open(SRC))
    rows = d["rows"]
    axes = d["design"]["axes"]
    names = list(axes)
    refs = {a: axes[a][0] for a in names}
    # design matrix: intercept + dummy per axis (drop ref) + seed dummies
    seeds = sorted({r["seed"] for r in rows})
    X_parts = [np.ones(len(rows))]
    col_names = ["intercept"]
    for a in names:
        for v in axes[a][1:]:
            X_parts.append(np.array([1.0 if r["combo"][names.index(a)] == v else 0.0 for r in rows]))
            col_names.append(f"{a}={v}")
    for s in seeds[1:]:
        X_parts.append(np.array([1.0 if r["seed"] == s else 0.0 for r in rows]))
        col_names.append(f"seed={s}")
    X = np.column_stack(X_parts)
    groups = np.array([r["combo_index"] for r in rows])

    results = {"label": "SIMULATION — tests of the migration extension of the full-system multiverse; toy worlds, no causal claims",
               "n_runs": len(rows), "outcomes": OUTCOMES, "contrasts": {}, "interactions": {}, "notes": []}
    for a in names:
        if len(axes[a]) < 2:
            continue
        key = f"{a}: {axes[a][1:]} vs {axes[a][0]}"
        results["contrasts"][key] = {}
        for v in axes[a][1:]:
            col = col_names.index(f"{a}={v}")
            plist, rows_out = [], []
            for oc in OUTCOMES:
                y = np.array([np.nan if r["metrics"].get(oc) is None else r["metrics"][oc] for r in rows], float)
                m = np.isfinite(y)
                if m.sum() < 50:
                    rows_out.append({"outcome": oc, "effect": None, "se": None, "p": None, "ci": None, "stratum_min": None,
                                     "stratum_max": None, "sign_consistent": None, "note": "too few finite rows"})
                    plist.append(1.0)
                    continue
                eff, se = cluster_ols(y[m], X[m], groups[m], col)
                t = eff / se if se > 0 else 0.0
                p = norm_p(t)
                # stratum effects across other axes
                strat = []
                others = [o for o in names if o != a]
                for o in others:
                    for ov in axes[o]:
                        idx = [i for i, rr in enumerate(rows)
                               if rr["combo"][names.index(o)] == ov and np.isfinite(y[i])]
                        vals_v = [y[i] for i in idx if rows[i]["combo"][names.index(a)] == v]
                        vals_r = [y[i] for i in idx if rows[i]["combo"][names.index(a)] == refs[a]]
                        if vals_v and vals_r:
                            strat.append(float(np.mean(vals_v) - np.mean(vals_r)))
                sgn = all(x > 0 for x in strat) if eff > 0 else all(x < 0 for x in strat)
                rows_out.append({"outcome": oc, "effect": eff, "se": se, "p": p,
                                 "ci": [eff - 1.96 * se, eff + 1.96 * se],
                                 "stratum_min": min(strat) if strat else None,
                                 "stratum_max": max(strat) if strat else None,
                                 "sign_consistent": bool(sgn),
                                 "n": int(m.sum())})
                plist.append(p)
            adj = holm(np.array(plist))
            for r, pa in zip(rows_out, adj):
                r["p_holm"] = float(pa)
                r["supported"] = bool(r["p_holm"] < 0.05 and r.get("sign_consistent") is True and r.get("effect") is not None)
            results["contrasts"][key][v] = rows_out
    # ------- declared interaction terms: migration x gates / affordability / jobs -------
    pairs = [("migration", "gates"), ("migration", "afford"), ("migration", "jobs")]
    for a1, a2 in pairs:
        key = f"{a1} x {a2}"
        results["interactions"][key] = {}
        for v1 in axes[a1][1:]:
            for v2 in axes[a2][1:]:
                prod = np.array([1.0 if (r["combo"][names.index(a1)] == v1 and r["combo"][names.index(a2)] == v2) else 0.0
                                 for r in rows])
                Xi = np.column_stack([X, prod])
                names_i = list(col_names) + [f"{a1}={v1}:{a2}={v2}"]
                jcol = names_i.index(f"{a1}={v1}:{a2}={v2}")
                plist, rlist = [], []
                for oc in OUTCOMES:
                    y = np.array([np.nan if r["metrics"].get(oc) is None else r["metrics"][oc] for r in rows], float)
                    m = np.isfinite(y)
                    if m.sum() < 50 or np.std(prod[m]) == 0:
                        rlist.append({"outcome": oc, "effect": None, "se": None, "p": None, "ci": None,
                                      "stratum_min": None, "stratum_max": None, "sign_consistent": None,
                                      "note": "insufficient rows/variation"})
                        plist.append(1.0)
                        continue
                    eff, se = cluster_ols(y[m], Xi[m], groups[m], jcol)
                    t = eff / se if se > 0 else 0.0
                    p = norm_p(t)
                    strat = []
                    others = [o for o in names if o not in (a1, a2)]
                    for o in others:
                        for ov in axes[o]:
                            idx = [i for i, rr in enumerate(rows) if rr["combo"][names.index(o)] == ov and np.isfinite(y[i])]
                            va = [y[i] for i in idx if rows[i]["combo"][names.index(a1)] == v1 and rows[i]["combo"][names.index(a2)] == v2]
                            vb = [y[i] for i in idx if rows[i]["combo"][names.index(a1)] == axes[a1][0] and rows[i]["combo"][names.index(a2)] == axes[a2][0]]
                            if va and vb:
                                strat.append(float(np.mean(va) - np.mean(vb)))
                    sgn = all(x > 0 for x in strat) if eff > 0 else all(x < 0 for x in strat)
                    rlist.append({"outcome": oc, "effect": eff, "se": se, "p": p,
                                  "ci": [eff - 1.96 * se, eff + 1.96 * se],
                                  "stratum_min": min(strat) if strat else None,
                                  "stratum_max": max(strat) if strat else None,
                                  "sign_consistent": bool(sgn), "n": int(m.sum())})
                    plist.append(p)
                adj = holm(np.array(plist))
                for r_, pa in zip(rlist, adj):
                    r_["p_holm"] = float(pa)
                    r_["supported"] = bool(r_["p_holm"] < 0.05 and r_.get("sign_consistent") is True and r_.get("effect") is not None)
                results["interactions"][key][f"{v1}|{v2}"] = rlist

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    # print compact table of supported effects
    print("SIMULATION — full-system multiverse tests (cluster-robust, Holm)")
    for key, block in results["contrasts"].items():
        print("\n" + key)
        for v, rs in block.items():
            for r in rs:
                if r.get("supported") and r.get("effect") is not None and r.get("ci") and r.get("stratum_min") is not None:
                    print(f"  {r['outcome']:22s} {r['effect']:+.4f} [{r['ci'][0]:+.4f},{r['ci'][1]:+.4f}] "
                          f"p_holm={r['p_holm']:.2g} strata {r['stratum_min']:+.3f}..{r['stratum_max']:+.3f}")
    print("\nINTERACTIONS (supported)")
    for key, block in results["interactions"].items():
        print("\n" + key)
        for v, rs in block.items():
            for r in rs:
                if r.get("supported") and r.get("effect") is not None:
                    print(f"  {v:22s} {r['outcome']:22s} {r['effect']:+.4f} [{r['ci'][0]:+.4f},{r['ci'][1]:+.4f}] holm={r['p_holm']:.2g}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
