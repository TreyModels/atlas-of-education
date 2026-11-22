#!/usr/bin/env python3
"""Final tightening tests (pre-registered 2026-11-22 ~17:20 CST, before running).

1. LOG-ODDS WITHIN-COUNTRY. Re-run tight_tests test A (country FE, split-panel jackknife, cluster bootstrap,
   direct asymmetry) with every bounded percentage variable transformed to log-odds (p/100 clipped to [0.005, 0.995]),
   so floors and ceilings stop driving signs. Same focus set and decision rule.
2. BMA WITH A DEMOGRAPHIC BLOCK + FDR.
   (a) Demographic block = first principal component of standardized fertility, u5mr, young_share, life_exp (sign: higher = later transition).
   (b) For each outcome (10-yr change in ter, sec, lsc), BIC-approximated Bayesian model averaging over all subsets of
       CANDIDATES (2^12 models), always including the outcome's own level and decade dummies, starts 1990-2010.
       Report posterior inclusion probabilities (PIP) and posterior mean sign. PIP >= 0.75 = 'strong', 0.5-0.75 = 'positive'.
   (c) Benjamini-Yekutieli FDR (q = 0.05) over the base-model p-values of every ordered pair from sweep_all (pooled, clustered).
3. FEE-ABOLITION EVENT STUDY (external check on the household-cost direction).
   Treated: Malawi 1994, Ethiopia 1995, Uganda 1997, Lesotho 2000, Cameroon 2000, Tanzania 2001, Zambia 2002, Kenya 2003,
   Rwanda 2003, Mozambique 2004, Burundi 2005, Ghana 2005 (dates from the fee-abolition literature; to be verified).
   Outcome: primary GER (SE.PRM.ENRR), annual, event time -5..+6 (bin -1 omitted). Two-way FE (country, year) on
   Sub-Saharan Africa countries; controls = SSA countries without a listed abolition. Country-cluster bootstrap CIs (500).
   Placebo: same model with every abolition date moved 6 years earlier (pre-period only).
Outputs results/final/{findings.txt, results.json}.
"""
import json, os, sys, time, urllib.request
from itertools import combinations
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep as S
import tight_tests as TT

OUT = os.path.join(S.HERE, "results", "final")
PCT = {"ter", "sec", "lsc", "prm_cmp", "prm_ner", "sec_ner", "young_share", "wage_emp", "emp_agri", "poverty", "electricity",
       "urban", "srv_va", "unemp_adv_edu", "pre_ger", "lit_adult", "vuln_emp", "emp_srv", "emp_ind", "agri_va"}
CANDIDATES = ["demo_pc", "gdppc_log", "prm_cmp", "wage_emp", "electricity", "urban", "agri_va", "gov_cons", "eci_pct", "exports", "fdi", "remit"]
FEE = {"MWI": 1994, "ETH": 1995, "UGA": 1997, "LSO": 2000, "CMR": 2000, "TZA": 2001, "ZMB": 2002, "KEN": 2003, "RWA": 2003,
       "MOZ": 2004, "BDI": 2005, "GHA": 2005}


def _logodds(v):
    p = np.clip(v / 100.0, 0.005, 0.995)
    return np.log(p / (1 - p))


def test1(workers):
    rows, names, meta = S.build(); p = S._prep(rows, names); A = p["A"]
    for k in names:
        A[f"d_{k}"] = A[f"dx_{k}"]; A[f"{k}_0"] = A[k]
    for o in S.OUTCOMES:
        A[o] = A[f"{o}_0"]
    # transform levels and changes of bounded variables: recompute change on the log-odds scale
    for k in [v for v in TT.FOCUS if v in PCT and v in A]:
        lev = A[k].copy(); fut = lev + A[f"d_{k}"]
        A[k] = _logodds(lev); A[f"{k}_0"] = A[k]; A[f"d_{k}"] = _logodds(fut) - A[k]
    g = dict(A=A, iso=p["iso"], dec=p["dec"], t=np.array([r["t"] for r in rows]), region={i: meta[i]["region"] for i in set(p["iso"])})
    focus = [v for v in TT.FOCUS if v in A]
    with Pool(workers, initializer=TT._init, initargs=(g,)) as pl:
        pairs = pl.map(TT._job_pair, [(a, b) for a in focus for b in focus if a != b], chunksize=2)
    return {f"{a}->{b}": d for a, b, d in pairs if d}


def test2():
    rows, names, meta = S.build(); p = S._prep(rows, names); A = p["A"]
    t = np.array([r["t"] for r in rows]); iso = p["iso"]
    dem = ["fertility", "u5mr", "young_share", "life_exp"]
    M = np.column_stack([A[k] for k in dem]); ok = np.isfinite(M).all(1)
    Z = (M[ok] - M[ok].mean(0)) / M[ok].std(0); Z[:, 3] *= -1        # life_exp reversed so all point to 'early transition'
    w = np.linalg.svd(Z, full_matrices=False)[2][0]; w = w if w.sum() > 0 else -w
    pc = np.full(len(rows), np.nan); pc[ok] = Z @ w; A["demo_pc"] = pc
    res = {"demo_pc_loadings": dict(zip(dem, w.round(3).tolist()))}
    for o in S.OUTCOMES:
        y = A[f"d_{o}"]; m = np.isfinite(y) & np.isfinite(A[f"{o}_0"]) & (t >= 1990)
        for c in CANDIDATES:
            m &= np.isfinite(A[c])
        n = int(m.sum())
        if n < 100:
            res[o] = dict(skipped=f"complete cases {n}"); continue
        Xc = {c: S._z(A[c], m)[m] for c in CANDIDATES}
        base = [np.ones(n), S._z(A[f"{o}_0"], m)[m]] + [d[m] for d in np.column_stack([(t >= 1995) & (t < 2005), t >= 2005]).astype(float).T]
        yy = y[m]; bic, incl, coefs = [], [], []
        for r in range(len(CANDIDATES) + 1):
            for sub in combinations(range(len(CANDIDATES)), r):
                X = np.column_stack(base + [Xc[CANDIDATES[j]] for j in sub])
                b, *_ = np.linalg.lstsq(X, yy, rcond=None); e = yy - X @ b
                bic.append(n * np.log(e @ e / n) + X.shape[1] * np.log(n))
                v = np.zeros(len(CANDIDATES)); c = np.zeros(len(CANDIDATES))
                for k, j in enumerate(sub):
                    v[j] = 1; c[j] = b[len(base) + k]
                incl.append(v); coefs.append(c)
        bic = np.array(bic); wts = np.exp(-(bic - bic.min()) / 2); wts /= wts.sum()
        I, C = np.array(incl), np.array(coefs)
        pip = (wts[:, None] * I).sum(0)
        pmean = np.array([(wts * C[:, j] * I[:, j]).sum() / max(pip[j], 1e-12) for j in range(len(CANDIDATES))])
        res[o] = dict(n=n, countries=int(len(np.unique(iso[m]))),
                      pip={c: round(float(pip[j]), 3) for j, c in enumerate(CANDIDATES)},
                      post_mean_if_included={c: round(float(pmean[j]), 3) for j, c in enumerate(CANDIDATES)})
    # FDR over sweep_all ordered pairs, base model on the pooled sample
    for k in names:
        A[f"d_{k}"] = A[f"dx_{k}"]; A[f"{k}_0"] = A[k]
    for o in S.OUTCOMES:
        A[o] = A[f"{o}_0"]
    V = [k for k in names if np.isfinite(A[k]).sum() >= 300 and np.isfinite(A[f"d_{k}"]).sum() >= 200] + list(S.OUTCOMES)
    from math import erf, sqrt
    P = []
    for yv in V:
        for xv in V:
            if xv == yv:
                continue
            yy = A[f"d_{yv}"]; m = np.isfinite(yy) & np.isfinite(A[xv]) & np.isfinite(A[f"{yv}_0"]); n = int(m.sum())
            if n < 120 or len(np.unique(iso[m])) < 25:
                continue
            X = np.column_stack([np.ones(n), S._z(A[xv], m)[m], S._z(A[f"{yv}_0"], m)[m], p["dec"][m]])
            r = S.ols_cluster(X, yy[m], iso[m])
            if r is None:
                continue
            tstat = r[0][1] / r[1]; pv = 2 * (1 - 0.5 * (1 + erf(abs(tstat) / sqrt(2))))
            P.append((xv, yv, float(r[0][1]), float(pv)))
    m_ = len(P); cm = sum(1.0 / i for i in range(1, m_ + 1)); order = sorted(range(m_), key=lambda i: P[i][3])
    kmax = 0
    for rank, i in enumerate(order, 1):
        if P[i][3] <= rank / (m_ * cm) * 0.05:
            kmax = rank
    keep = {order[i] for i in range(kmax)}
    res["fdr"] = dict(tests=m_, survivors=kmax, q=0.05, method="Benjamini-Yekutieli",
                      ter_survivors=sorted([f"{P[i][0]}({'+' if P[i][2] > 0 else '-'})" for i in keep if P[i][1] == "ter"]),
                      sec_survivors=sorted([f"{P[i][0]}({'+' if P[i][2] > 0 else '-'})" for i in keep if P[i][1] == "sec"]),
                      lsc_survivors=sorted([f"{P[i][0]}({'+' if P[i][2] > 0 else '-'})" for i in keep if P[i][1] == "lsc"]))
    return res


def _fetch_prm():
    fn = os.path.join(S.DATA, "prm_ger.json")
    if not os.path.exists(fn):
        raw = S._get("https://api.worldbank.org/v2/country/all/indicator/SE.PRM.ENRR?format=json&per_page=20000&date=1970:2024")
        j = json.loads(raw); json.dump([(d["countryiso3code"], int(d["date"]), d["value"]) for d in j[1] if d["value"] is not None and d["countryiso3code"]], open(fn, "w"))
    out = {}
    for iso, y, v in json.load(open(fn)):
        out.setdefault(iso, {})[y] = float(v)
    return out


def _es(panel, events, isos, years, K=(-5, 6), boot=500, seed=0):
    """two-way FE event study; returns coefs for event times (bin -1 omitted)."""
    ks = [k for k in range(K[0], K[1] + 1) if k != -1]
    def design(sample):
        Y, X, G, Tt = [], [], [], []
        for gi, c in enumerate(sample):
            for y in years:
                v = panel.get(c, {}).get(y)
                if v is None:
                    continue
                row = np.zeros(len(ks))
                if c in events:
                    e = y - events[c]
                    e = min(max(e, K[0]), K[1])
                    if e != -1:
                        row[ks.index(e)] = 1
                Y.append(v); X.append(row); G.append(gi); Tt.append(y)
        Y, X, G, Tt = np.array(Y), np.array(X), np.array(G), np.array(Tt)
        def dm(v):
            v = v.astype(float).copy()
            for _ in range(10):          # alternating projections for two-way FE
                for grp in (G, Tt):
                    u, idx = np.unique(grp, return_inverse=True); s = np.bincount(idx, v); n = np.bincount(idx)
                    v = v - (s / n)[idx]
            return v
        Yd = dm(Y); Xd = np.column_stack([dm(X[:, j]) for j in range(X.shape[1])])
        return np.linalg.lstsq(Xd, Yd, rcond=None)[0]
    b = design(isos)
    rng = np.random.default_rng(seed); B = []
    for _ in range(boot):
        pick = list(rng.choice(isos, len(isos)))
        # relabel duplicates to keep separate FE
        relab = {}; samp = []
        for k, c in enumerate(pick):
            name = f"{c}#{k}"; relab[name] = c; samp.append(name)
        pan = {n: panel.get(relab[n], {}) for n in samp}; ev = {n: events[relab[n]] for n in samp if relab[n] in events}
        try:
            B.append(_es_core(pan, ev, samp, years, ks, K))
        except Exception:
            pass
    B = np.array(B)
    return dict(event_time=ks, coef=b.round(2).tolist(), ci90_lo=np.percentile(B, 5, 0).round(2).tolist(), ci90_hi=np.percentile(B, 95, 0).round(2).tolist(), boots=len(B))


def _es_core(panel, events, isos, years, ks, K):
    Y, X, G, Tt = [], [], [], []
    for gi, c in enumerate(isos):
        for y in years:
            v = panel.get(c, {}).get(y)
            if v is None:
                continue
            row = np.zeros(len(ks))
            if c in events:
                e = min(max(y - events[c], K[0]), K[1])
                if e != -1:
                    row[ks.index(e)] = 1
            Y.append(v); X.append(row); G.append(gi); Tt.append(y)
    Y, X, G, Tt = np.array(Y), np.array(X), np.array(G), np.array(Tt)
    def dm(v):
        v = v.astype(float).copy()
        for _ in range(10):
            for grp in (G, Tt):
                u, idx = np.unique(grp, return_inverse=True); s = np.bincount(idx, v); n = np.bincount(idx)
                v = v - (s / n)[idx]
        return v
    return np.linalg.lstsq(np.column_stack([dm(X[:, j]) for j in range(X.shape[1])]), dm(Y), rcond=None)[0]


def test3():
    prm = _fetch_prm()
    meta = json.load(open(os.path.join(S.DATA, "meta.json")))
    ssa = sorted(i for i, m in meta.items() if m["region"] == "Sub-Saharan Africa" and i in prm)
    years = list(range(1985, 2016))
    real = _es(prm, {c: y for c, y in FEE.items() if c in ssa}, ssa, years, seed=1)
    plac = _es(prm, {c: y - 6 for c, y in FEE.items() if c in ssa}, ssa, list(range(1980, 2000)), K=(-5, 4), seed=2)
    return dict(treated=[c for c in FEE if c in ssa], n_ssa=len(ssa), real=real, placebo_minus6=plac)


def main(workers=21):
    os.makedirs(OUT, exist_ok=True); t0 = time.time()
    r1 = test1(workers); r2 = test2(); r3 = test3()
    L = [f"FINAL TESTS ({round(time.time() - t0)}s)", "", "1. WITHIN-COUNTRY on LOG-ODDS scale (FE + split-panel jackknife + asymmetry bootstrap):"]
    ks = list(r1); pv = np.array([r1[k]["p_lead"] for k in ks]); m = len(pv); o = np.argsort(pv)
    for nm, cm in (("q_bh", 1.0), ("q_by", float(np.sum(1.0 / np.arange(1, m + 1))))):
        q = np.minimum.accumulate((pv[o] * m * cm / np.arange(1, m + 1))[::-1])[::-1].clip(max=1)
        for i, j in enumerate(o):
            r1[ks[j]][nm] = float(q[i])
    lead = sorted([(k, d) for k, d in r1.items() if d["x_leads_within"]], key=lambda kv: -abs(kv[1]["b_xy"]))
    L.append(f"   {len(lead)} of {len(r1)} ordered pairs pass the raw CI rule; {sum(d['x_leads_within'] and d['q_bh'] < .10 for d in r1.values())} at BH q<0.10, "
             f"{sum(d['x_leads_within'] and d['q_by'] < .10 for d in r1.values())} at BY q<0.10 (p_lead = max(p_b, p_diff), bootstrap; b in SD-of-change per SD; A2 2026-11-22).")
    for k, d in lead:
        L.append(f"   {k:28s} b={d['b_xy']:+.3f} CI({d['ci_xy'][0]:+.3f},{d['ci_xy'][1]:+.3f}) diff CI({d['ci_diff'][0]:+.3f},{d['ci_diff'][1]:+.3f}) q_bh={d['q_bh']:.3f} q_by={d['q_by']:.3f}")
    L += ["", f"2a. Demographic block loadings: {r2['demo_pc_loadings']} (higher = earlier in the transition)", "2b. BMA posterior inclusion probabilities (starts 1990-2010, all subsets of 12 candidates):"]
    for o in S.OUTCOMES:
        d = r2.get(o, {})
        if "skipped" in d:
            L.append(f"   {o}: skipped ({d['skipped']})"); continue
        ordered = sorted(d["pip"].items(), key=lambda kv: -kv[1])
        L.append(f"   {o} (n={d['n']}, {d['countries']} countries): " + ", ".join(f"{c} {v:.2f}({'+' if d['post_mean_if_included'][c] > 0 else '-'})" for c, v in ordered))
    f = r2["fdr"]
    L += [f"2c. Benjamini-Yekutieli FDR q=0.05 over {f['tests']} pair tests: {f['survivors']} survive.",
          f"   ter: {', '.join(f['ter_survivors'])}", f"   sec: {', '.join(f['sec_survivors'])}", f"   lsc: {', '.join(f['lsc_survivors'])}", "",
          f"3. FEE-ABOLITION EVENT STUDY (primary GER, SSA two-way FE; {len(r3['treated'])} treated of {r3['n_ssa']} SSA countries):"]
    for name in ("real", "placebo_minus6"):
        e = r3[name]
        L.append(f"   {name}: " + "  ".join(f"t{k:+d}:{c:+.1f}[{lo:+.1f},{hi:+.1f}]" for k, c, lo, hi in zip(e["event_time"], e["coef"], e["ci90_lo"], e["ci90_hi"])))
    L += ["", "Associations only (1-2); the event study uses literature dates not yet verified against primary sources."]
    json.dump(dict(logodds_within=r1, bma_fdr=r2, fee_event_study=r3), open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 21)
