#!/usr/bin/env python3
"""Tighter tests on the 22 Nov panel (pre-registered 2026-11-22 ~17:10 CST, before running).

A. WITHIN-COUNTRY LEAD-LAG (answers Acemoglu et al. 2005). For ordered pairs among FOCUS variables:
   dY(t->t+10) ~ X_t + Y_t + decade dummies + COUNTRY FIXED EFFECTS (within transform), standardized X.
   Nickell-type bias from Y_t under FE is reduced with the split-panel jackknife (Dhaene & Jochmans 2015):
   b_SPJ = 2*b_full - (b_early + b_late)/2, early = t<=1990, late = t>=1995.
   Direct asymmetry: D = b(X->Y) - b(Y->X), 400 country-cluster bootstrap draws.
   'X leads Y (within)' if the 90% CI of b(X->Y) excludes 0 AND the 90% CI of D excludes 0 in the same direction.
   Pooled (no FE) direction from sweep_all.py is reported alongside for comparison.
B. SPLIT STABILITY. For each outcome (ter, sec, lsc) and predictor: base regression (X + Y_t + decade, pooled),
   200 random country splits (region-stratified). Stability = share of splits with same-sign p<0.05 in BOTH halves.
C. TAKEOFF FUNCTIONAL FORM. Same risk set as takeoff.py (tertiary GER crossing 15%, conditions lagged 5 yrs).
   smooth = logistic in continuous H, E, S plus squares; threshold = median dummies h, e, s; count = 1/2/3 dummies;
   hybrid = smooth + all-three dummy. 10-fold country CV log loss, repeated over 20 fold seeds.
Outputs results/tight/{findings.txt, results.json}. Associations only.
"""
import json, os, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep as S
import takeoff as T

OUT = os.path.join(S.HERE, "results", "tight")
FOCUS = ["ter", "sec", "lsc", "prm_cmp", "prm_ner", "fertility", "u5mr", "young_share", "wage_emp", "emp_agri", "gdppc_log",
         "poverty", "electricity", "urban", "eci_pct", "tax", "gov_cons", "edu_xpd_gdp", "srv_va", "unemp_adv_edu"]
G = {}


def _within(v, g):
    out = v.copy()
    for k in np.unique(g):
        m = g == k; out[m] = v[m] - v[m].mean()
    return out


def _fe_b(y, x, yl, dec, g):
    """standardized-x coefficient under country FE (within transform)."""
    xs = (x - x.mean()) / (x.std() or 1)
    Z = np.column_stack([xs, yl, dec])
    Zw = np.column_stack([_within(Z[:, j], g) for j in range(Z.shape[1])]); yw = _within(y, g)
    keep = np.ones(len(y), bool)
    b = np.linalg.lstsq(Zw[keep], yw[keep], rcond=None)[0]
    return b[0]


def _pair_data(a, b):
    A = G["A"]; y = A[f"d_{b}"]; x = A[a]; yl = A[f"{b}_0"]
    m = np.isfinite(y) & np.isfinite(x) & np.isfinite(yl)
    return y[m], x[m], yl[m], G["dec"][m], G["iso"][m], G["t"][m]


def _spj(y, x, yl, dec, g, t):
    full = _fe_b(y, x, yl, dec, g)
    e, l = t <= 1990, t >= 1995
    parts = []
    for m in (e, l):
        # need countries with >= 2 obs in the half
        gg = g[m]; u, c = np.unique(gg, return_counts=True); ok = np.isin(gg, u[c >= 2])
        if ok.sum() < 60:
            return full
        parts.append(_fe_b(y[m][ok], x[m][ok], yl[m][ok], dec[m][ok], gg[ok]))
    return 2 * full - 0.5 * (parts[0] + parts[1])


def _job_pair(args):
    a, b = args
    d1 = _pair_data(a, b); d2 = _pair_data(b, a)
    if len(d1[0]) < 150 or len(d2[0]) < 150 or len(np.unique(d1[4])) < 30:
        return (a, b, None)
    b1, b2 = _spj(*d1), _spj(*d2)
    rng = np.random.default_rng(hash((a, b)) % 2**32)
    c1 = np.unique(d1[4]); B1, D = [], []
    for _ in range(400):
        pick = rng.choice(c1, len(c1))
        idx1 = np.concatenate([np.where(d1[4] == c)[0] for c in pick])
        idx2 = np.concatenate([np.where(d2[4] == c)[0] for c in pick if (d2[4] == c).any()])
        # relabel duplicated countries so FE stay separate
        g1 = np.concatenate([np.full((d1[4] == c).sum(), k) for k, c in enumerate(pick)])
        g2 = np.concatenate([np.full((d2[4] == c).sum(), k) for k, c in enumerate(pick) if (d2[4] == c).any()])
        try:
            x1 = _spj(d1[0][idx1], d1[1][idx1], d1[2][idx1], d1[3][idx1], g1, d1[5][idx1])
            x2 = _spj(d2[0][idx2], d2[1][idx2], d2[2][idx2], d2[3][idx2], g2, d2[5][idx2])
        except Exception:
            continue
        B1.append(x1); D.append(x1 - x2)
    B1, D = np.array(B1), np.array(D)
    ci1, ciD = np.percentile(B1, [5, 95]), np.percentile(D, [5, 95])
    lead = bool((ci1[0] > 0 or ci1[1] < 0) and (ciD[0] > 0 or ciD[1] < 0) and np.sign(np.median(D)) == np.sign(b1))
    return (a, b, dict(b_xy=float(b1), b_yx=float(b2), ci_xy=ci1.tolist(), ci_diff=ciD.tolist(), x_leads_within=lead, n=int(len(d1[0]))))


def _job_split(args):
    o, x, seeds = args
    A = G["A"]; y = A[f"d_{o}"]; m0 = np.isfinite(y) & np.isfinite(A[x]) & np.isfinite(A[f"{o}_0"])
    hits, sgn0 = 0, None
    for s in seeds:
        rng = np.random.default_rng(s); half = {}
        for reg in sorted(set(G["region"].values())):
            cs = sorted(i for i in G["region"] if G["region"][i] == reg); rng.shuffle(cs)
            for k, c in enumerate(cs):
                half[c] = k % 2
        res = []
        for h in (0, 1):
            m = m0 & np.array([half.get(i, -1) == h for i in G["iso"]])
            n = int(m.sum())
            if n < 80 or len(np.unique(G["iso"][m])) < 20:
                res.append(None); continue
            X = np.column_stack([np.ones(n), S._z(A[x], m)[m], S._z(A[f"{o}_0"], m)[m], G["dec"][m]])
            r = S.ols_cluster(X, y[m], G["iso"][m]); res.append(None if r is None else r[0][1] / r[1])
        if None in res:
            continue
        if sgn0 is None:
            sgn0 = np.sign(res[0])
        if all(abs(t) > 1.96 for t in res) and np.sign(res[0]) == np.sign(res[1]) == sgn0:
            hits += 1
    return (o, x, hits / len(seeds))


def _init(g):
    global G
    G = g


def test_c():
    panel, eci_label = T.build_panel(); risk, _ = T.risk_set(panel)
    rows = [r for r in risk if all(np.isfinite(r[k]) for k in ("H", "E", "S"))]
    y = np.array([r["event"] for r in rows], float)
    for k in ("H", "E", "S"):
        v = np.array([r[k] for r in rows]); T.MU[k], T.SD[k] = float(v.mean()), float(v.std() or 1)
    thr = [float(np.median([r[k] for r in rows])) for k in ("H", "E", "S")]
    z = lambda k: (np.array([r[k] for r in rows]) - T.MU[k]) / T.SD[k]
    H, E, Sx = z("H"), z("E"), z("S")
    h, e, s = [(np.array([r[k] for r in rows]) >= t).astype(float) for k, t in zip(("H", "E", "S"), thr)]
    yr = np.array([r["year"] for r in rows], float); dec = [((yr >= d) & (yr < d + 10)).astype(float) for d in (1975, 1985, 1995, 2005, 2015)]
    base = [np.ones(len(rows))] + dec
    D = {"smooth": base + [H, E, Sx, H ** 2, E ** 2, Sx ** 2], "linear": base + [H, E, Sx], "threshold": base + [h, e, s],
         "count": base + [((h + e + s) == k).astype(float) for k in (1, 2, 3)], "hybrid": base + [H, E, Sx, H ** 2, E ** 2, Sx ** 2, h * e * s]}
    isos = sorted({r["iso"] for r in rows}); out = {k: [] for k in D}
    for seed in range(20):
        rng = np.random.default_rng(seed); order = isos[:]; rng.shuffle(order); fold = {c: i % 10 for i, c in enumerate(order)}
        fr = np.array([fold[r["iso"]] for r in rows])
        for k, cols in D.items():
            X = np.column_stack(cols); ll = np.zeros(len(rows))
            for f in range(10):
                te = fr == f; b, _, _ = T.logit(X[~te], y[~te], ridge=1e-3)
                p = np.clip(1 / (1 + np.exp(-(X[te] @ b))), 1e-6, 1 - 1e-6); ll[te] = -(y[te] * np.log(p) + (1 - y[te]) * np.log(1 - p))
            out[k].append(float(ll.mean()))
    res = {k: dict(mean=float(np.mean(v)), sd=float(np.std(v))) for k, v in out.items()}
    wins = {k: float(np.mean([out[k][i] <= min(out[j][i] for j in out) for i in range(20)])) for k in out}
    return dict(n_rows=len(rows), n_takeoffs=int(y.sum()), cv_logloss=res, share_seeds_best=wins, eci_source=eci_label)


def main(workers=21):
    os.makedirs(OUT, exist_ok=True); t0 = time.time()
    rows, names, meta = S.build(); p = S._prep(rows, names); A = p["A"]
    for k in names:
        A[f"d_{k}"] = A[f"dx_{k}"]; A[f"{k}_0"] = A[k]
    for o in S.OUTCOMES:
        A[o] = A[f"{o}_0"]
    g = dict(A=A, iso=p["iso"], dec=p["dec"], t=np.array([r["t"] for r in rows]), region={i: meta[i]["region"] for i in set(p["iso"])})
    focus = [v for v in FOCUS if v in A]
    pool = [k for k in names if np.isfinite(A[k]).sum() >= 300]
    with Pool(workers, initializer=_init, initargs=(g,)) as pl:
        pairs = pl.map(_job_pair, [(a, b) for a in focus for b in focus if a != b], chunksize=2)
        splits = pl.map(_job_split, [(o, x, list(range(5000, 5200))) for o in S.OUTCOMES for x in pool], chunksize=4)
    C = test_c()
    pooled = {}
    pa = os.path.join(S.HERE, "results", "sweep_all", "leads.csv")
    if os.path.exists(pa):
        import csv
        for r in csv.DictReader(open(pa)):
            pooled[(r["leader"], r["follower"])] = r["kind"]
    P = {f"{a}->{b}": d for a, b, d in pairs if d}
    L = [f"TIGHT TESTS ({round(time.time() - t0)}s)", "", "A. WITHIN-COUNTRY (country FE, split-panel jackknife, cluster bootstrap) lead-lag among focus variables:"]
    within = [(k, d) for k, d in P.items() if d["x_leads_within"]]
    L.append(f"   {len(within)} of {len(P)} ordered pairs show a within-country lead with a significant asymmetry.")
    for k, d in sorted(within, key=lambda kv: -abs(kv[1]["b_xy"])):
        a, b = k.split("->")
        L.append(f"   {k:28s} b={d['b_xy']:+.2f} (CI {d['ci_xy'][0]:+.2f},{d['ci_xy'][1]:+.2f})  diff CI ({d['ci_diff'][0]:+.2f},{d['ci_diff'][1]:+.2f})  pooled: {pooled.get((a, b), 'not a pooled one-way lead')}")
    lost = [f"{a}->{b}" for (a, b), kind in pooled.items() if kind == "one-way" and a in focus and b in focus and not P.get(f"{a}->{b}", {}).get("x_leads_within")]
    L.append(f"   pooled one-way leads among focus vars that do NOT survive within-country: {', '.join(sorted(lost)) or 'none'}")
    L += ["", "B. SPLIT STABILITY (share of 200 random country splits with same-sign p<0.05 in both halves; base model):"]
    for o in S.OUTCOMES:
        top = sorted([(x, s) for oo, x, s in splits if oo == o], key=lambda kv: -kv[1])[:12]
        L.append(f"   {o}: " + ", ".join(f"{x}({s:.0%})" for x, s in top))
    L += ["", "C. TAKEOFF FUNCTIONAL FORM (10-fold country CV log loss, 20 fold seeds; lower = better):"]
    for k, v in sorted(C["cv_logloss"].items(), key=lambda kv: kv[1]["mean"]):
        L.append(f"   {k:10s} {v['mean']:.4f} (sd {v['sd']:.4f})  best in {C['share_seeds_best'][k]:.0%} of seeds")
    L += ["", "Associations only. Within-country tests remove stable country traits but not time-varying confounders."]
    json.dump(dict(within=P, splits=[dict(outcome=o, var=x, stability=s) for o, x, s in splits], takeoff_form=C),
              open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 21)
