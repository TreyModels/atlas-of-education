#!/usr/bin/env python3
"""Every-variable-as-outcome sweep (extends sweep.py; pre-registered 2026-11-22 ~16:50 CST before running).
For every variable Y in the pool (schooling, skills, employment, economy, state, demography, ECI) and every other X:
  dY(t->t+10) ~ X_t + Y_t + decade dummies + ONE other predictor Z_t, over all Z (lighter bounds than sweep.py: one
  extra, not two, to keep 58x57x56x2 regressions tractable). Country-clustered SEs. n >= 120 rows, >= 25 countries.
ROBUST(X->Y) = Sala-i-Martin CDF(0) >= 0.95, same sign, in both country halves (same split as sweep.py).
LEADS: X leads Y if ROBUST(X->Y) and not ROBUST(Y->X); mutual if both; neither otherwise.
Outputs results/sweep_all/{matrix.csv, leads.csv, findings.txt}. Associations only.
"""
import csv, json, os, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep as S

OUT = os.path.join(S.HERE, "results", "sweep_all")


def _job(args):
    y, x, V, half = args
    m = S.P["half_mask"][half]; A = S.P["A"]
    res = []
    for z in [None] + [v for v in V if v not in (x, y)]:
        cols = [x, f"{y}_0"] + ([z] if z else [])
        yy = A[f"d_{y}"]; mm = m & np.isfinite(yy)
        for c in cols:
            mm &= np.isfinite(A[c])
        n = int(mm.sum())
        if n < 120 or len(np.unique(S.P["iso"][mm])) < 25:
            continue
        X = np.column_stack([np.ones(n)] + [S._z(A[c], mm)[mm] for c in cols] + [S.P["dec"][mm]])
        r = S.ols_cluster(X, yy[mm], S.P["iso"][mm])
        if r is not None:
            res.append((r[0][1], r[1], r[2], n))
    return (y, x, half, S._summ(res))


def main(workers=21):
    os.makedirs(OUT, exist_ok=True)
    rows, names, meta = S.build()
    p = S._prep(rows, names)
    A = p["A"]
    for k in names:                      # predictors as outcomes
        A[f"d_{k}"] = A[f"dx_{k}"]; A[f"{k}_0"] = A[k]
    for o in S.OUTCOMES:                 # outcomes as predictors
        A[o] = A[f"{o}_0"]
    iso = p["iso"]; regions = {i: meta[i]["region"] for i in set(iso)}
    rng = np.random.default_rng(20261122); half = {}
    for reg in sorted(set(regions.values())):
        cs = sorted(i for i in set(iso) if regions[i] == reg); rng.shuffle(cs)
        for k, c in enumerate(cs):
            half[c] = "discovery" if k % 2 == 0 else "confirmation"
    p["half_mask"] = {h: np.array([half[i] == h for i in iso]) for h in ("discovery", "confirmation")}
    V = [k for k in names if np.isfinite(A[k]).sum() >= 300 and np.isfinite(A[f"d_{k}"]).sum() >= 200] + list(S.OUTCOMES)
    jobs = [(y, x, V, h) for y in V for x in V if x != y for h in ("discovery", "confirmation")]
    print(f"{len(V)} variables, {len(jobs)} jobs", flush=True)
    t0 = time.time()
    with Pool(workers, initializer=S._init, initargs=(p,)) as pl:
        out = pl.map(_job, jobs, chunksize=8)
    R = {}
    for y, x, h, s in out:
        R.setdefault((y, x), {})[h] = s
    block = {k: b for b, d in S.BLOCKS.items() for k in d}; block["eci_pct"] = "economy"; block.update({o: "schooling" for o in S.OUTCOMES})
    mat = []
    for (y, x), d in R.items():
        a, b = d.get("discovery"), d.get("confirmation")
        rob = bool(a and b and a["cdf0"] >= 0.95 and b["cdf0"] >= 0.95 and a["modal_sign"] == b["modal_sign"])
        mat.append(dict(outcome=y, outcome_block=block.get(y), predictor=x, predictor_block=block.get(x), robust=rob,
                        sign=(a["modal_sign"] if a else None), coef_disc=(round(a["median_coef"], 3) if a else None),
                        coef_conf=(round(b["median_coef"], 3) if b else None), cdf_disc=(round(a["cdf0"], 3) if a else None),
                        cdf_conf=(round(b["cdf0"], 3) if b else None)))
    with open(os.path.join(OUT, "matrix.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(mat[0])); w.writeheader(); w.writerows(mat)
    rob = {(r["predictor"], r["outcome"]): r for r in mat if r["robust"]}
    leads = []
    for (x, y), r in rob.items():
        rev = rob.get((y, x))
        if rev is None:
            leads.append(dict(leader=x, follower=y, sign=r["sign"], coef=r["coef_disc"], kind="one-way", lb=block.get(x), fb=block.get(y)))
        elif x < y:
            leads.append(dict(leader=x, follower=y, sign=r["sign"], coef=r["coef_disc"], kind="mutual", lb=block.get(x), fb=block.get(y)))
    with open(os.path.join(OUT, "leads.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(leads[0]) if leads else ["leader"]); w.writeheader(); w.writerows(leads)
    L = [f"EVERY-VARIABLE SWEEP: {len(V)} variables, {len(mat)} ordered pairs, {len(rob)} robust (both halves). {round(time.time() - t0)}s.", ""]
    for y in V:
        rs = sorted([r for r in mat if r["outcome"] == y and r["robust"]], key=lambda r: -abs(r["coef_disc"] or 0))
        L.append(f"[{y}] ({block.get(y)}) robust predictors of its 10-yr change: " + ", ".join(
            f"{'+' if r['sign'] > 0 else '-'}{r['predictor']}({r['coef_disc']:+.2f})" for r in rs[:10]))
    L.append("")
    bb = {}
    for l in leads:
        if l["kind"] == "one-way":
            bb.setdefault((l["lb"], l["fb"]), 0); bb[(l["lb"], l["fb"])] += 1
    L.append("ONE-WAY LEADS BY BLOCK (count of robust X->Y with no robust Y->X):")
    for (a, b), n in sorted(bb.items(), key=lambda kv: -kv[1]):
        L.append(f"   {a:10s} -> {b:10s} {n}")
    out_deg = {}; in_deg = {}
    for l in leads:
        if l["kind"] == "one-way":
            out_deg[l["leader"]] = out_deg.get(l["leader"], 0) + 1; in_deg[l["follower"]] = in_deg.get(l["follower"], 0) + 1
    L.append("MOST-LEADING variables (one-way out-degree): " + ", ".join(f"{k}({v})" for k, v in sorted(out_deg.items(), key=lambda kv: -kv[1])[:15]))
    L.append("MOST-FOLLOWING variables (one-way in-degree): " + ", ".join(f"{k}({v})" for k, v in sorted(in_deg.items(), key=lambda kv: -kv[1])[:15]))
    L += ["", "Associations only; 10-year horizon; country-split replicated. Mechanical links (e.g. a cohort-size denominator) are not removed."]
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 21)
