#!/usr/bin/env python3
"""Bayesian analyses for the APEX panel (pre-registered 2026-11-22 ~17:50 CST, before running).

B1. HIERARCHICAL BAYESIAN REGRESSION (Gibbs sampler, written here; no external PPL).
    For outcome Y in {ter, sec, lsc} (10-yr change, starts 1990-2010):
      dY = X b + u_country + sum_r 1[region=r] * Zs g_r + e
      X = [own level, demo_pc, urban, prm_cmp, wage_emp, electricity, gdppc_log, gov_cons, eci_pct, decade dummies] (standardized)
      Zs = [demo_pc, wage_emp, electricity, urban]: region-specific slope DEVIATIONS g_r ~ N(0, w2) (partial pooling).
      b ~ N(0, 10^2), u_c ~ N(0, t2), t2, w2, s2 ~ InvGamma(1, 1). 4 chains x 6000 draws, 2000 burn-in. Report posterior
      mean, 90% credible interval, P(b>0), split-R-hat; region slopes = b + g_r for Asia regions vs others.
B2. EXACT BAYESIAN MODEL AVERAGING with Zellner g-prior (g = max(n, K^2), BRIC) and beta-binomial(1,1) model-size prior,
    over all subsets of the 12 B-candidates, (a) pooled and (b) within-country (country-demeaned), for ter/sec/lsc.
B3. CHILD LABOUR (for Nordtveit). ILO/UCW series via WDI: SL.TLF.0714.ZS (children 7-14 in employment), .WK (work only),
    .SW (study and work), SL.AGR.0714.ZS (in agriculture).
    (a) Hierarchical model of the child-employment level (logit-transformed share) on demo_pc, gdppc_log, emp_agri, urban,
        electricity, wage_emp, with country random intercepts and region slope deviations.
    (b) Does child employment at t predict the 10-yr change in lower-secondary completion and primary completion, controlling
        own level, demo_pc, gdppc_log? (hierarchical, same sampler).
    (c) Share of working children who also study (SW / total) vs completion; Cambodia and Southeast Asia data points listed.
Associations only. Outputs results/bayes/{findings.txt, results.json}.
"""
import json, os, sys, time
from itertools import combinations
from math import lgamma, log
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep as S

OUT = os.path.join(S.HERE, "results", "bayes")
CL = {"cl_total": "SL.TLF.0714.ZS", "cl_work_only": "SL.TLF.0714.WK.ZS", "cl_study_work": "SL.TLF.0714.SW.ZS", "cl_agri": "SL.AGR.0714.ZS"}
CAND = ["demo_pc", "urban", "prm_cmp", "wage_emp", "electricity", "gdppc_log", "gov_cons", "eci_pct", "exports", "fdi", "remit", "agri_va"]
XB = ["demo_pc", "urban", "prm_cmp", "wage_emp", "electricity", "gdppc_log", "gov_cons", "eci_pct"]
ZS = ["demo_pc", "wage_emp", "electricity", "urban"]
ASIA = {"East Asia & Pacific", "South Asia"}


def fetch_cl():
    for k, code in CL.items():
        fn = os.path.join(S.DATA, f"{k}.json")
        if os.path.exists(fn) and os.path.getsize(fn) > 50:
            continue
        raw = S._get(f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=20000&date=1960:2024")
        try:
            j = json.loads(raw); rows = [(d["countryiso3code"], int(d["date"]), d["value"]) for d in j[1] if d["value"] is not None and d["countryiso3code"]]
        except Exception as e:
            print("FAILED", k, e); rows = []
        json.dump(rows, open(fn, "w")); print(k, len(rows), flush=True)
    S.BLOCKS["employment"].update(CL)


def gibbs(y, X, cl, reg, Z, iters=6000, burn=2000, chains=4, seed=0):
    n, k = X.shape; C = int(cl.max()) + 1; R = int(reg.max()) + 1; q = Z.shape[1]
    # design for (b, g_1..g_R) jointly
    Zr = np.zeros((n, R * q))
    for r in range(R):
        Zr[reg == r, r * q:(r + 1) * q] = Z[reg == r]
    W = np.hstack([X, Zr]); p = W.shape[1]
    out = []
    for ch in range(chains):
        rng = np.random.default_rng(seed * 100 + ch)
        s2, t2, w2 = 1.0, 1.0, 0.1; u = np.zeros(C); draws = []
        for it in range(iters):
            prec = np.r_[np.full(k, 1 / 100.0), np.full(R * q, 1 / w2)]
            A = W.T @ W / s2 + np.diag(prec); L = np.linalg.cholesky(A)
            mu = np.linalg.solve(A, W.T @ (y - u[cl]) / s2)
            th = mu + np.linalg.solve(L.T, rng.standard_normal(p))
            res = y - W @ th
            cnt = np.bincount(cl, minlength=C); sm = np.bincount(cl, res, minlength=C)
            v = 1 / (cnt / s2 + 1 / t2); u = rng.normal(v * sm / s2, np.sqrt(v))
            e = res - u[cl]
            s2 = 1 / rng.gamma(1 + n / 2, 1 / (1 + e @ e / 2))
            t2 = 1 / rng.gamma(1 + C / 2, 1 / (1 + u @ u / 2))
            g = th[k:]; w2 = 1 / rng.gamma(1 + len(g) / 2, 1 / (0.1 + g @ g / 2))
            if it >= burn:
                draws.append(np.r_[th, s2, t2, w2])
        out.append(np.array(draws))
    D = np.array(out)                      # chains x draws x params
    m = D.shape[1] // 2; halves = np.concatenate([D[:, :m], D[:, m:2 * m]], 0)
    cm = halves.mean(1); cv = halves.var(1, ddof=1); Bv = m * cm.var(0, ddof=1); Wv = cv.mean(0)
    rhat = np.sqrt(((m - 1) / m * Wv + Bv / m) / np.maximum(Wv, 1e-12))
    flat = D.reshape(-1, D.shape[2])
    return flat, rhat, k, R, q


def summarise(flat, rhat, names):
    out = {}
    for j, nm in enumerate(names):
        v = flat[:, j]
        out[nm] = dict(mean=round(float(v.mean()), 3), ci90=[round(float(np.percentile(v, 5)), 3), round(float(np.percentile(v, 95)), 3)],
                       p_pos=round(float((v > 0).mean()), 3), rhat=round(float(rhat[j]), 3))
    return out


def prep():
    fetch_cl()
    rows, names, meta = S.build(); p = S._prep(rows, names); A = p["A"]
    t = np.array([r["t"] for r in rows]); iso = p["iso"]
    dem = ["fertility", "u5mr", "young_share", "life_exp"]
    M = np.column_stack([A[k] for k in dem]); ok = np.isfinite(M).all(1)
    Zm = (M[ok] - M[ok].mean(0)) / M[ok].std(0); Zm[:, 3] *= -1
    w = np.linalg.svd(Zm, full_matrices=False)[2][0]; w = w if w.sum() > 0 else -w
    pc = np.full(len(rows), np.nan); pc[ok] = Zm @ w; A["demo_pc"] = pc
    region = np.array([meta[i]["region"].strip() for i in iso])
    return rows, names, meta, A, t, iso, region, p["dec"]


def b1(A, t, iso, region, dec, outcome, X_names, Z_names, ymode="delta", extra_mask=None, start_min=1990):
    y = A[f"d_{outcome}"] if ymode == "delta" else A[outcome]
    own = A[f"{outcome}_0"] if ymode == "delta" else None
    m = np.isfinite(y) & (t >= start_min)
    if own is not None:
        m &= np.isfinite(own)
    for c in X_names:
        m &= np.isfinite(A[c])
    if extra_mask is not None:
        m &= extra_mask
    n = int(m.sum())
    if n < 80:
        return dict(skipped=f"n={n}")
    z = lambda v: (v[m] - v[m].mean()) / (v[m].std() or 1)
    cols = ([z(own)] if own is not None else []) + [z(A[c]) for c in X_names]
    names = (["own_level"] if own is not None else []) + X_names
    tt = t[m]; dd = np.column_stack([(tt >= d) & (tt < d + 10) for d in (1995, 2005)]).astype(float)
    keep = dd.std(0) > 0
    X = np.column_stack([np.ones(n)] + cols + [dd[:, keep]]); names = ["intercept"] + names + [f"dec{j}" for j in range(keep.sum())]
    Z = np.column_stack([z(A[c]) for c in Z_names])
    cu, cl = np.unique(iso[m], return_inverse=True)
    regs = np.array(["Asia" if r in ASIA else r for r in region[m]]); ru, rg = np.unique(regs, return_inverse=True)
    yy = y[m]; ys = yy.std() or 1; yy = (yy - yy.mean()) / ys
    flat, rhat, k, R, q = gibbs(yy, X, cl, rg, Z)
    base = summarise(flat[:, :k], rhat[:k], names)
    reg_slopes = {}
    for r in range(R):
        for jq, zn in enumerate(Z_names):
            bj = names.index(zn); v = flat[:, bj] + flat[:, k + r * q + jq]
            reg_slopes[f"{ru[r]}:{zn}"] = dict(mean=round(float(v.mean()), 3), ci90=[round(float(np.percentile(v, 5)), 3), round(float(np.percentile(v, 95)), 3)],
                                             p_pos=round(float((v > 0).mean()), 3))
    return dict(n=n, countries=int(len(cu)), regions=ru.tolist(), y_sd=float(ys), coef_standardized=base, region_slopes=reg_slopes,
                max_rhat=round(float(np.nanmax(rhat)), 3))


def b2(A, t, iso, dec, outcome, within):
    y = A[f"d_{outcome}"]; m = np.isfinite(y) & np.isfinite(A[f"{outcome}_0"]) & (t >= 1990)
    for c in CAND:
        m &= np.isfinite(A[c])
    n0 = int(m.sum())
    if n0 < 80:
        return dict(skipped=f"n={n0}")
    cols = {c: A[c][m] for c in CAND}; own = A[f"{outcome}_0"][m]; yy = y[m]; g_ = iso[m]
    tt = t[m]; D = np.column_stack([(tt >= d) & (tt < d + 10) for d in (1995, 2005)]).astype(float)
    def dm(v):
        if not within:
            return v - v.mean()
        o = v.astype(float).copy()
        for c in np.unique(g_):
            s = g_ == c; o[s] -= o[s].mean()
        return o
    yv = dm(yy); base = np.column_stack([dm(own)] + [dm(D[:, j]) for j in range(D.shape[1])])
    # partial out base (always-included) regressors
    Pb = base @ np.linalg.pinv(base); yr = yv - Pb @ yv
    Xc = {c: (lambda x: x - Pb @ x)(dm(cols[c])) for c in CAND}
    n = len(yr); K = len(CAND); g = max(n, K ** 2); tss = yr @ yr
    logml, models = [], []
    for kk in range(K + 1):
        for sub in combinations(range(K), kk):
            if kk == 0:
                r2 = 0.0
            else:
                X = np.column_stack([Xc[CAND[j]] for j in sub]); b, *_ = np.linalg.lstsq(X, yr, rcond=None); r2 = 1 - ((yr - X @ b) @ (yr - X @ b)) / tss
            lml = 0.5 * (n - 1 - kk) * log(1 + g) - 0.5 * (n - 1) * log(1 + g * (1 - r2))
            lprior = -log(K + 1) - (lgamma(K + 1) - lgamma(kk + 1) - lgamma(K - kk + 1))
            logml.append(lml + lprior); models.append(sub)
    lm = np.array(logml); w = np.exp(lm - lm.max()); w /= w.sum()
    pip = {c: round(float(sum(w[i] for i, s in enumerate(models) if j in s)), 3) for j, c in enumerate(CAND)}
    best = models[int(np.argmax(w))]
    return dict(n=n, within=within, pip=pip, top_model=[CAND[j] for j in best], top_model_prob=round(float(w.max()), 3))


def main():
    os.makedirs(OUT, exist_ok=True); t0 = time.time()
    rows, names, meta, A, t, iso, region, dec = prep()
    res = {"B1": {}, "B2": {}, "B3": {}}
    for o in ("ter", "sec", "lsc"):
        res["B1"][o] = b1(A, t, iso, region, dec, o, XB, ZS)
        res["B2"][o] = dict(pooled=b2(A, t, iso, dec, o, False), within=b2(A, t, iso, dec, o, True))
        print("done", o, round(time.time() - t0), flush=True)
    # child labour
    have = {k: int(np.isfinite(A[k]).sum()) if k in A else 0 for k in CL}
    res["B3"]["coverage_rows"] = have
    if have.get("cl_total", 0) >= 80:
        lg = lambda v: np.log(np.clip(v, 0.5, 99.5) / (100 - np.clip(v, 0.5, 99.5)))
        A["cl_logit"] = lg(A["cl_total"])
        res["B3"]["a_level"] = b1(A, t, iso, region, dec, "cl_logit", ["demo_pc", "gdppc_log", "emp_agri", "urban", "electricity", "wage_emp"],
                                  ["demo_pc", "emp_agri", "electricity"], ymode="level", start_min=1975)
        for o in ("lsc", "prm_cmp"):
            if f"d_{o}" not in A:
                A[f"d_{o}"] = A[f"dx_{o}"]; A[f"{o}_0"] = A[o]
            res["B3"][f"b_cl_predicts_{o}"] = b1(A, t, iso, region, dec, o, ["cl_total", "demo_pc", "gdppc_log"], ["cl_total"], start_min=1975)
        if have.get("cl_study_work", 0) >= 30:
            share = A["cl_study_work"] / np.where(A["cl_total"] > 0, A["cl_total"], np.nan)
            m = np.isfinite(share) & np.isfinite(A["prm_cmp"])
            res["B3"]["c_study_share_vs_prm_cmp_corr"] = dict(n=int(m.sum()), r=round(float(np.corrcoef(share[m], A["prm_cmp"][m])[0, 1]), 3) if m.sum() > 5 else None)
        sea = {}
        for c in sorted(S.SE_ASIA | {"KHM"}):
            for k in CL:
                s = S._series(k).get(c, {}) if os.path.exists(os.path.join(S.DATA, f"{k}.json")) else {}
                if s:
                    sea.setdefault(c, {})[k] = {str(y): round(v, 1) for y, v in sorted(s.items())}
        res["B3"]["southeast_asia_points"] = sea
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    L = [f"BAYESIAN ANALYSES ({round(time.time() - t0)}s)", "", "B1. Hierarchical Bayes (country random intercepts, region slope deviations), standardized coefficients, 10-yr change, starts 1990-2010:"]
    for o, d in res["B1"].items():
        if "skipped" in d:
            L.append(f"  [{o}] skipped {d['skipped']}"); continue
        L.append(f"  [{o}] n={d['n']} countries={d['countries']} max R-hat={d['max_rhat']}")
        for nm in ["own_level"] + XB:
            c = d["coef_standardized"].get(nm)
            if c:
                L.append(f"     {nm:12s} {c['mean']:+.3f} [{c['ci90'][0]:+.3f},{c['ci90'][1]:+.3f}] P(>0)={c['p_pos']:.2f}")
        asia = {k: v for k, v in d["region_slopes"].items() if k.startswith("Asia")}
        L.append("     Asia slopes: " + ", ".join(f"{k.split(':')[1]} {v['mean']:+.2f}[{v['ci90'][0]:+.2f},{v['ci90'][1]:+.2f}]" for k, v in asia.items()))
    L += ["", "B2. Exact BMA, Zellner g-prior (BRIC), beta-binomial size prior; PIPs pooled | within-country:"]
    for o, d in res["B2"].items():
        if "skipped" in d["pooled"]:
            L.append(f"  [{o}] skipped"); continue
        L.append(f"  [{o}] n={d['pooled']['n']}: " + ", ".join(f"{c} {d['pooled']['pip'][c]:.2f}|{d['within']['pip'][c]:.2f}" for c in CAND))
        L.append(f"       top model pooled: {d['pooled']['top_model']} ({d['pooled']['top_model_prob']}); within: {d['within']['top_model']} ({d['within']['top_model_prob']})")
    L += ["", f"B3. CHILD LABOUR (coverage rows: {res['B3'].get('coverage_rows')})"]
    a = res["B3"].get("a_level")
    if a and "skipped" not in a:
        L.append(f"  (a) logit child employment 7-14, n={a['n']} countries={a['countries']}:")
        for nm, c in a["coef_standardized"].items():
            if not nm.startswith(("intercept", "dec")):
                L.append(f"     {nm:12s} {c['mean']:+.3f} [{c['ci90'][0]:+.3f},{c['ci90'][1]:+.3f}] P(>0)={c['p_pos']:.2f}")
        L.append("     Asia slopes: " + ", ".join(f"{k.split(':')[1]} {v['mean']:+.2f}" for k, v in a["region_slopes"].items() if k.startswith("Asia")))
    for o in ("lsc", "prm_cmp"):
        b = res["B3"].get(f"b_cl_predicts_{o}")
        if b and "skipped" not in b:
            c = b["coef_standardized"]["cl_total"]
            L.append(f"  (b) child employment -> 10-yr change in {o}: {c['mean']:+.3f} [{c['ci90'][0]:+.3f},{c['ci90'][1]:+.3f}] P(>0)={c['p_pos']:.2f} (n={b['n']}, {b['countries']} countries)")
        elif b:
            L.append(f"  (b) {o}: {b}")
    if "c_study_share_vs_prm_cmp_corr" in res["B3"]:
        L.append(f"  (c) share of working children who also study vs primary completion: {res['B3']['c_study_share_vs_prm_cmp_corr']}")
    for c, d in res["B3"].get("southeast_asia_points", {}).items():
        L.append(f"  {c}: " + "; ".join(f"{k} " + ", ".join(f"{y}:{v}" for y, v in pts.items()) for k, pts in d.items()))
    L += ["", "Associations only. Child-labour series are sparse survey-year estimates (ILO/UCW via WDI)."]
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
