#!/usr/bin/env python3
"""Statistical screen of the full-system multiverse (eduengine, 1,440 runs).

REWRITTEN 25 Nov 2026 after the line audit (Neon) of the first version. The first version is in git
history; what changed and why:

  1. RANK/ESTIMABILITY GUARD instead of a blind `pinv`. Three of the nine outcomes are only populated
     in some arms (tut_rate only where tutoring exists, formal_share_gdp/skill_premium only in the
     fiscal/competitive arms), so the outcome-specific design loses whole levels and becomes
     rank-deficient. `np.linalg.pinv(X.T @ X)` returned coefficients and standard errors for contrast
     directions that the data cannot identify -- e.g. supply -> formal_share_gdp got
     effect 0.135, SE 0.003, p_holm 0.0, which is noise dressed as certainty. Every contrast is now
     tested for estimability (is e_j in the row space of X?) and reported as `not_estimable` when not.
  2. EMPTY-STRATUM GUARD. `sign_consistent = all(...)` over an empty stratum list is True in Python
     (`all([])`), so four rows passed the consistency check with no strata at all. Now
     `sign_consistent = bool(strat) and ...`, and a row with no strata cannot be called supported.
  3. ZERO-VARIANCE GUARD. A contrast in an outcome that is constant in the estimation sample (e.g.
     a zero tutoring effect where tutoring is switched off) is reported as not estimable, not as
     "supported with p = 0".
  4. Holm is computed only over ESTIMABLE outcomes in each contrast block; non-estimable rows carry
     `p_holm = None` and are never supported.
  5. Provenance (script/source hashes, numpy/python version, git commit, env) is written into the JSON
     so the committed numbers can be tied to the committed code.
  6. The whole thing is labelled EXPLORATORY: p-values, CIs, Holm and a "supported" rule were added
     after the multiverse pre-registration, which explicitly said "no p-values". See
     TEST_PREREGISTRATION_DEVIATION.md. The stratum step is a raw-mean sign heuristic with no seed FE
     or clustering and is documented as such.

This tests whether the reported multiverse effects are statistical regularities of the simulated
design, not whether they are true of the world (toy worlds; no causal claims).
"""
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from itertools import product

import numpy as np

SRC = "results_multiverse.json"
OUT = "full_system_tests.json"

OUTCOMES = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
            "tut_rate", "formal_share_gdp", "parity_wealth_lower", "skill_premium", "q_pub"]

RANK_REL_TOL = 1e-8     # singular values below RANK_REL_TOL * s_max are treated as zero
ESTIMABLE_TOL = 1e-8    # ||e_j - proj_rowspace(e_j)|| above this means the contrast is not identified
ZERO_VAR_TOL = 1e-12


def norm_p(t):
    """Two-sided normal p-value."""
    return math.erfc(abs(t) / math.sqrt(2.0))


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


def row_space_basis(X):
    """Orthonormal basis of the row space of X (columns of V), and the numerical rank."""
    _, s, Vt = np.linalg.svd(X, full_matrices=False)
    smax = float(s[0]) if s.size else 0.0
    tol = RANK_REL_TOL * smax * max(X.shape)
    rank = int((s > tol).sum())
    V = Vt[:rank].T                      # p x rank
    return rank, V, s


def contrast_estimable(V, col):
    """Is the functional e_col' beta estimable (i.e. identifiable from this design)?"""
    e = np.zeros(V.shape[0])
    e[col] = 1.0
    resid = e - V @ (V.T @ e)
    return float(np.linalg.norm(resid)) < ESTIMABLE_TOL


def cluster_ols(y, X, groups, j):
    """OLS with cluster-robust SEs for coefficient j.

    Returns (beta_j, se_j, estimable, reason). When the contrast is not estimable returns
    (None, None, False, reason) instead of a fabricated number.
    """
    if y.size <= 2 or float(np.std(y)) < ZERO_VAR_TOL:
        return None, None, False, "outcome has no variance in the estimation sample"
    rank, V, s = row_space_basis(X)
    if rank < X.shape[1] and not contrast_estimable(V, j):
        return None, None, False, f"design rank {rank} < {X.shape[1]}: contrast not identifiable"
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    # generalized inverse of X'X restricted to the identifiable subspace
    G = (V / (s[:rank] ** 2)) @ V.T
    groups_u = np.unique(groups)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for g in groups_u:
        m = groups == g
        sc = X[m].T @ resid[m]
        meat += np.outer(sc, sc)
    Gc = len(groups_u)
    n = X.shape[0]
    corr = (Gc / (Gc - 1)) * ((n - 1) / (n - rank)) if Gc > 1 and n > rank else 1.0
    Vbeta = G @ meat @ G * corr
    se = math.sqrt(max(float(Vbeta[j, j]), 0.0))
    return float(beta[j]), se, True, "ok"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def main():
    path_d = os.path.abspath(SRC)
    d = json.load(open(path_d))
    rows = d["rows"]
    axes = d["design"]["axes"]
    names = list(axes)
    refs = {a: axes[a][0] for a in names}

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
    X_full = np.column_stack(X_parts)
    groups = np.array([r["combo_index"] for r in rows])

    # cell index for the (stricter) per-cell sign disclosure: one cell = one design combo
    cells = {}
    for r in rows:
        cells.setdefault(tuple(r["combo"]), []).append(r)

    def cell_sign_disclosure(a, ai, v, oc, eff):
        """How many of the paired cell contrasts disagree in sign with the pooled effect?

        This is a DISCLOSURE, not part of the supported rule: a cell contrast is the mean across
        seeds inside one combo vs the same combo with axis a at its reference level. Cells are
        small (10 seeds) and levels can be near zero, so sign flips alone are weak evidence; we
        also count flips whose |cell contrast| is at least 10% of |pooled effect|.
        """
        pairs = flips = big = 0
        for c, rs_ in cells.items():
            if c[ai] != v:
                continue
            ref = tuple((axes[a][0] if i == ai else x) for i, x in enumerate(c))
            mv = [r["metrics"].get(oc) for r in rs_]
            mr = [r["metrics"].get(oc) for r in cells.get(ref, [])]
            mv = [x for x in mv if x is not None]
            mr = [x for x in mr if x is not None]
            if not mv or not mr:
                continue
            dl = float(np.mean(mv) - np.mean(mr))
            pairs += 1
            if abs(dl) > 1e-12 and (dl > 0) != (eff > 0):
                flips += 1
                if abs(dl) >= 0.1 * abs(eff):
                    big += 1
        return pairs, flips, big

    results = {
        "label": "EXPLORATORY SIGNIFICANCE SCREEN — full-system multiverse; toy worlds; no causal claims",
        "status": "exploratory",   # p-values/Holm were added post hoc; not pre-registered (see deviations file)
        "n_runs": len(rows),
        "outcomes": OUTCOMES,
        "contrasts": {},
        "not_estimable": [],
        "notes": [
            "Holm family = the estimable outcomes within one contrast block; families are not joint across blocks.",
            "The stratum check is a raw-mean sign heuristic (no seed FE, no clustering) and is a necessary, not sufficient, condition.",
            "A row is 'supported' only if estimable AND variable AND Holm p<0.05 AND sign-consistent across a non-empty set of strata.",
            "These p-values were not pre-registered; the multiverse pre-registration said 'no p-values'. Treat as exploratory.",
        ],
        "provenance": {
            "script": os.path.basename(os.path.abspath(__file__)),
            "script_sha256": sha256(os.path.abspath(__file__)),
            "source": os.path.basename(path_d),
            "source_sha256": sha256(path_d),
            "numpy": np.__version__,
            "python": platform.python_version(),
            "git_commit": git_commit(),
            "rank_full_design": row_space_basis(X_full)[0],
            "n_columns": int(X_full.shape[1]),
        },
    }

    for a in names:
        if len(axes[a]) < 2:
            continue
        key = f"{a}: {axes[a][1:]} vs {axes[a][0]}"
        results["contrasts"][key] = {}
        for v in axes[a][1:]:
            col = col_names.index(f"{a}={v}")
            plist, rows_out, estimable_rows = [], [], []
            for oc in OUTCOMES:
                y = np.array([np.nan if r["metrics"].get(oc) is None else r["metrics"][oc]
                              for r in rows], float)
                m = np.isfinite(y)
                if int(m.sum()) < 50:
                    rows_out.append({"outcome": oc, "effect": None, "se": None, "p": None, "p_holm": None,
                                     "ci": None, "stratum_min": None, "stratum_max": None,
                                     "n_strata": 0, "sign_consistent": None,
                                     "estimable": False, "supported": False,
                                     "note": "too few finite rows"})
                    continue
                eff, se, ok, why = cluster_ols(y[m], X_full[m], groups[m], col)
                if not ok:
                    rows_out.append({"outcome": oc, "effect": None, "se": None, "p": None, "p_holm": None,
                                     "ci": None, "stratum_min": None, "stratum_max": None,
                                     "n_strata": 0, "sign_consistent": None,
                                     "estimable": False, "supported": False, "note": why})
                    results["not_estimable"].append({"contrast": key, "value": v, "outcome": oc, "reason": why})
                    continue
                t = eff / se if se > 0 else None
                p = norm_p(t) if t is not None else None
                # stratum sign check: raw mean contrast in each level of each other axis
                strat = []
                for o in [o for o in names if o != a]:
                    for ov in axes[o]:
                        idx = [i for i, rr in enumerate(rows)
                               if rr["combo"][names.index(o)] == ov and np.isfinite(y[i])]
                        vals_v = [y[i] for i in idx if rows[i]["combo"][names.index(a)] == v]
                        vals_r = [y[i] for i in idx if rows[i]["combo"][names.index(a)] == refs[a]]
                        if vals_v and vals_r:
                            strat.append(float(np.mean(vals_v) - np.mean(vals_r)))
                sign_consistent = None
                if strat:
                    sign_consistent = bool(all(x > 0 for x in strat)) if eff > 0 else bool(all(x < 0 for x in strat))
                pairs_, flips_, big_ = cell_sign_disclosure(a, names.index(a), v, oc, eff)
                row = {"outcome": oc, "effect": eff, "se": se, "p": p,
                       "cell_pairs": pairs_, "cell_sign_flips": flips_,
                       "cell_sign_flips_10pct": big_,
                       "ci": [eff - 1.96 * se, eff + 1.96 * se],
                       "stratum_min": min(strat) if strat else None,
                       "stratum_max": max(strat) if strat else None,
                       "n_strata": len(strat), "sign_consistent": sign_consistent,
                       "estimable": True, "n": int(m.sum())}
                if p is not None:
                    plist.append(p)
                    estimable_rows.append(row)
                rows_out.append(row)
            # Holm across the estimable outcomes of this block only
            if plist:
                for row, pa in zip(estimable_rows, holm(np.array(plist))):
                    row["p_holm"] = float(pa)
            for row in rows_out:
                row.setdefault("p_holm", None)
                row["supported"] = bool(row.get("estimable") is True
                                        and row.get("p_holm") is not None
                                        and row["p_holm"] < 0.05
                                        and row.get("sign_consistent") is True)
            results["contrasts"][key][v] = rows_out

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)

    supported = [(key, v, r) for key, block in results["contrasts"].items()
                 for v, rs in block.items() for r in rs if r["supported"]]
    print("EXPLORATORY — full-system multiverse screen (cluster-robust OLS, seed FE, Holm, stratum sign check)")
    print(f"runs={len(rows)}  supported rows={len(supported)}  not estimable rows={len(results['not_estimable'])}")
    for key, block in results["contrasts"].items():
        hits = [(v, r) for v, rs in block.items() for r in rs if r["supported"]]
        if not hits:
            continue
        print("\n" + key)
        for v, r in hits:
            print(f"  {v:22s} {r['outcome']:22s} {r['effect']:+.4f} [{r['ci'][0]:+.4f},{r['ci'][1]:+.4f}] "
                  f"p_holm={r['p_holm']:.2g} strata(n={r['n_strata']}) {r['stratum_min']:+.3f}..{r['stratum_max']:+.3f}")
    print("\nNOT ESTIMABLE (reported, never 'supported'):")
    for n in results["not_estimable"]:
        print(f"  {n['contrast']} / {n['value']} / {n['outcome']}: {n['reason']}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
