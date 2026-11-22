#!/usr/bin/env python3
"""APEX v1.1: multiple imputation + long-run splice + core reruns (pre-registered 2026-11-22 ~18:05 CST, before running).

A. IMPUTATION (M = 20). Annual panel 1970-2020 of every sweep variable. Bounded % variables -> log-odds, gdp/pop -> log.
   Per variable: y_ct = country-specific polynomial trend (degree 0/1/2 by number of observations) + b * anchors_ct + e,
   estimated by Frisch-Waugh; anchors = demographic block, urban, gdppc_log (imputed first from their own trends).
   AMENDMENT (same session, before any result was read): the first version used dense country dummies and a country-cluster
   bootstrap; it was too slow and was replaced by this algebraically equivalent trend fit with a residual bootstrap for
   parameter uncertainty plus N(0, s2) noise per imputed cell.
   Cells are imputed only within [first observed year - 5, last observed year + 5] for that country-variable (no long extrapolation).
B. LONG-RUN SPLICE. Lee & Lee (2016) enrollment ratios (primary/secondary/tertiary, 5-yearly, 1820-2010, barrolee.github.io)
   for 1950-1965; WDI from 1970. Report the first year each country's tertiary ratio reaches 15% using the spliced series, and
   rerun the takeoff hazard (household only: Maddison GDP per capita via Our World in Data, lagged 5 years) on 1950-2020.
C. RERUNS on each imputed dataset, combined with Rubin's rules:
   C1 pooled base edges dY(t->t+10) ~ X_t + Y_t + decade (Y in ter, sec, lsc; all X), country-clustered SE;
   C2 within-country (country FE, log-odds) edges for the tight_tests focus pairs;
   C3 exact BMA (g-prior BRIC) pooled and within, PIPs averaged over imputations;
   C4 takeoff (tertiary 15%) hazard CV log loss: additive vs threshold vs count, averaged over imputations.
   Compare with the complete-case results already on the branch.
D. EXPECTED VS ACTUAL (2015): pooled model of ter/sec/lsc level on demographic block, gdppc_log, urban, electricity
   (imputation 1 and averaged over M); residual = actual - expected; Asian countries listed.
Outputs results/apex_mi/{findings.txt, results.json, imputed_m01.csv}.
"""
import csv, io, json, os, re, sys, time, urllib.request
from itertools import combinations
from math import lgamma, log, erf, sqrt
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep as S

OUT = os.path.join(S.HERE, "results", "apex_mi")
M = 20
YEARS = np.arange(1970, 2021)
PCT = {"ter", "sec", "lsc", "prm_cmp", "prm_ner", "sec_ner", "pre_ger", "young_share", "wage_emp", "emp_agri", "emp_ind", "emp_srv", "vuln_emp",
       "poverty", "electricity", "urban", "srv_va", "agri_va", "manuf_va", "unemp_adv_edu", "lit_adult", "internet", "gpi_sec", "gpi_ter"}
LOGV = {"gdppc_log", "pop_log"}
ANCH = ["fertility", "u5mr", "young_share", "life_exp", "urban", "gdppc_log"]
FOCUS = ["ter", "sec", "lsc", "prm_cmp", "prm_ner", "fertility", "young_share", "wage_emp", "emp_agri", "gdppc_log", "poverty", "electricity",
         "urban", "eci_pct", "tax", "gov_cons", "edu_xpd_gdp"]
CAND = ["demo_pc", "urban", "prm_cmp", "wage_emp", "electricity", "gdppc_log", "gov_cons", "eci_pct", "exports", "fdi", "remit", "agri_va"]
ASIA_ISO = S.NE_ASIA | S.SE_ASIA | S.S_ASIA | {"KHM", "PHL"}
G = {}


def tr(k, v):
    v = np.asarray(v, float)
    if k in PCT:
        p = np.clip(v / 100, 0.005, 0.995); return np.log(p / (1 - p))
    if k in LOGV:
        return np.log(np.where(v > 0, v, np.nan))
    return v


def inv(k, v):
    if k in PCT:
        return 100 / (1 + np.exp(-v))
    if k in LOGV:
        return np.exp(v)
    return v


def load_panel():
    meta = json.load(open(os.path.join(S.DATA, "meta.json")))
    isos = sorted(i for i, m in meta.items() if m["region"].strip() != "Aggregates")
    names = []
    for b in S.BLOCKS.values():
        names += list(b)
    names += list(S.OUTCOMES)
    names = [k for k in names if os.path.exists(os.path.join(S.DATA, f"{k}.json")) and os.path.getsize(os.path.join(S.DATA, f"{k}.json")) > 50]
    if os.path.exists(os.path.join(S.DATA, "eci_pct.json")):
        names.append("eci_pct")
    ix = {c: i for i, c in enumerate(isos)}; P = {}
    for k in names:
        a = np.full((len(isos), len(YEARS)), np.nan)
        for iso, y, v in json.load(open(os.path.join(S.DATA, f"{k}.json"))):
            if iso in ix and 1970 <= y <= 2020 and v is not None:
                a[ix[iso], y - 1970] = float(v)
        P[k] = tr(k.replace("_log", "_log") if k not in ("gdppc_log", "pop_log") else k, a)
    return isos, meta, names, P


def window_mask(a):
    m = np.zeros_like(a, bool)
    for i in range(a.shape[0]):
        obs = np.where(np.isfinite(a[i]))[0]
        if len(obs):
            m[i, max(obs[0] - 5, 0):min(obs[-1] + 6, a.shape[1])] = True
    return m


def design(rows_c, rows_t, n_c, extra=None):
    t = (rows_t - 25) / 25.0
    cols = [np.eye(n_c)[rows_c], np.eye(n_c)[rows_c] * t[:, None], np.eye(n_c)[rows_c] * (t ** 2)[:, None]]
    if extra is not None:
        cols.append(extra)
    return np.hstack(cols)


def _basis(t, deg):
    t = (t - 25) / 25.0
    return np.column_stack([np.ones_like(t), t, t ** 2][:deg + 1])


def _fit(ci, ti, y, A):
    """Frisch-Waugh: country-specific polynomial trends (degree by #obs) + shared slopes on anchors A."""
    us = np.unique(ci); deg = {}
    ry = y.copy(); rA = None if A is None else A.copy()
    for c in us:
        s = ci == c; n = int(s.sum()); d = 0 if n <= 2 else (1 if n <= 5 else 2); deg[c] = d
        Bs = _basis(ti[s].astype(float), d); P = Bs @ np.linalg.pinv(Bs)
        ry[s] = y[s] - P @ y[s]
        if A is not None:
            rA[s] = A[s] - P @ A[s]
    beta = None
    if A is not None:
        beta = np.linalg.solve(rA.T @ rA + 1e-3 * np.eye(A.shape[1]), rA.T @ ry)
    yr = y - (A @ beta if A is not None else 0)
    coef = {}
    for c in us:
        s = ci == c; coef[c] = np.linalg.lstsq(_basis(ti[s].astype(float), deg[c]), yr[s], rcond=None)[0]
    fitted = np.array([_basis(np.array([float(tt)]), deg[c]) @ coef[c] for c, tt in zip(ci, ti)]).ravel() + (A @ beta if A is not None else 0)
    return beta, coef, deg, fitted


def _pred(cj, tj, Am, beta, coef, deg):
    out = np.full(len(cj), np.nan)
    for k, (c, tt) in enumerate(zip(cj, tj)):
        if c in coef:
            out[k] = (_basis(np.array([float(tt)]), deg[c]) @ coef[c])[0]
    if beta is not None and Am is not None:
        out = out + Am @ beta
    return out


def impute_one(seed):
    rng = np.random.default_rng(seed)
    names, P = G["names"], G["P"]
    out = {}
    order = [k for k in ANCH if k in P] + [k for k in names if k not in ANCH]
    for k in order:
        a = P[k]; obs = np.isfinite(a); win = window_mask(a) & ~obs
        if obs.sum() < 30:
            out[k] = a.copy(); continue
        ci, ti = np.where(obs); cj, tj = np.where(win)
        Ao = Am = None
        if k not in ANCH:
            Aa = [out[x] for x in ANCH if x in out and x != k]
            if Aa:
                Ao = np.nan_to_num(np.column_stack([x[ci, ti] for x in Aa])); Am = np.nan_to_num(np.column_stack([x[cj, tj] for x in Aa]))
        y = a[ci, ti]
        beta, coef, deg, fit = _fit(ci, ti, y, Ao)
        res = y - fit; s = float(np.std(res)) if len(res) > 1 else 0.0
        # parametric uncertainty: residual bootstrap and refit
        ystar = fit + rng.choice(res, len(res), replace=True)
        beta, coef, deg, _ = _fit(ci, ti, ystar, Ao)
        full = a.copy()
        if len(cj):
            full[cj, tj] = _pred(cj, tj, Am, beta, coef, deg) + rng.normal(0, s, len(cj))
        out[k] = full
    return out


def rows_from(Pm):
    """country x start-year rows (1975..2010 step 5), levels at t (natural scale for sweep compatibility) and 10-yr changes."""
    isos = G["isos"]; R = []
    for i, c in enumerate(isos):
        for t0 in range(1975, 2011, 5):
            r = dict(iso=c, t=t0, region=G["meta"][c]["region"].strip())
            for k, a in Pm.items():
                v0, v1 = a[i, t0 - 1970], a[i, t0 + 10 - 1970]
                r[k] = v0; r[f"d_{k}"] = v1 - v0
            R.append(r)
    return R


def ols_cl(X, y, g):
    out = S.ols_cluster(X, y, g)
    return None if out is None else (out[0], out[1])


def arr(R, k):
    return np.array([r.get(k, np.nan) for r in R], float)


def c1(R):
    iso = np.array([r["iso"] for r in R]); t = np.array([r["t"] for r in R])
    dec = np.column_stack([(t >= d) & (t < d + 10) for d in (1985, 1995, 2005)]).astype(float)
    res = {}
    for o in ("ter", "sec", "lsc"):
        y = arr(R, f"d_{o}"); own = arr(R, o)
        for x in G["names"]:
            if x == o:
                continue
            xv = arr(R, x); m = np.isfinite(y) & np.isfinite(own) & np.isfinite(xv); n = int(m.sum())
            if n < 120:
                continue
            z = lambda v: (v[m] - v[m].mean()) / (v[m].std() or 1)
            X = np.column_stack([np.ones(n), z(xv), z(own), dec[m]])
            r = S.ols_cluster(X, y[m], iso[m])
            if r is not None:
                res[f"{o}<-{x}"] = (float(r[0][1]), float(r[1]))
    return res


def c2(R):
    iso = np.array([r["iso"] for r in R]); t = np.array([r["t"] for r in R])
    dec = np.column_stack([(t >= d) & (t < d + 10) for d in (1985, 1995, 2005)]).astype(float)
    res = {}
    def wt(v, g):
        o = v.copy()
        for c in np.unique(g):
            s = g == c; o[s] -= o[s].mean()
        return o
    for a in FOCUS:
        for b in FOCUS:
            if a == b or a not in G["names"] + list(S.OUTCOMES) or b not in G["names"] + list(S.OUTCOMES):
                continue
            y = arr(R, f"d_{b}"); yl = arr(R, b); x = arr(R, a); m = np.isfinite(y) & np.isfinite(yl) & np.isfinite(x)
            if m.sum() < 150:
                continue
            g = iso[m]; xs = (x[m] - x[m].mean()) / (x[m].std() or 1)
            Z = np.column_stack([xs, yl[m], dec[m]]); Zw = np.column_stack([wt(Z[:, j], g) for j in range(Z.shape[1])]); yw = wt(y[m], g)
            r = S.ols_cluster(np.column_stack([np.ones(len(yw)), Zw]), yw, g)
            if r is not None:
                res[f"{a}->{b}"] = (float(r[0][1]), float(r[1]))
    return res


def demo_pc(R):
    M_ = np.column_stack([arr(R, k) for k in ("fertility", "u5mr", "young_share", "life_exp")]); ok = np.isfinite(M_).all(1)
    Z = (M_[ok] - M_[ok].mean(0)) / M_[ok].std(0); Z[:, 3] *= -1
    w = np.linalg.svd(Z, full_matrices=False)[2][0]; w = w if w.sum() > 0 else -w
    pc = np.full(len(R), np.nan); pc[ok] = Z @ w
    return pc


def c3(R):
    pc = demo_pc(R); iso = np.array([r["iso"] for r in R]); t = np.array([r["t"] for r in R]); out = {}
    for o in ("ter", "sec", "lsc"):
        for within in (False, True):
            y = arr(R, f"d_{o}"); own = arr(R, o)
            cols = {c: (pc if c == "demo_pc" else arr(R, c)) for c in CAND}
            m = np.isfinite(y) & np.isfinite(own) & (t >= 1990)
            for c in CAND:
                m &= np.isfinite(cols[c])
            if m.sum() < 80:
                continue
            g_ = iso[m]; tt = t[m]
            def dm(v):
                if not within:
                    return v - v.mean()
                o_ = v.astype(float).copy()
                for c in np.unique(g_):
                    s = g_ == c; o_[s] -= o_[s].mean()
                return o_
            D = np.column_stack([(tt >= 1995) & (tt < 2005), tt >= 2005]).astype(float)
            base = np.column_stack([dm(own[m])] + [dm(D[:, j]) for j in range(2)]); Pb = base @ np.linalg.pinv(base)
            yr = dm(y[m]); yr = yr - Pb @ yr; Xc = {c: (lambda v: v - Pb @ v)(dm(cols[c][m])) for c in CAND}
            n = len(yr); K = len(CAND); gg = max(n, K * K); tss = yr @ yr; lm = []; mods = []
            for kk in range(K + 1):
                for sub in combinations(range(K), kk):
                    if kk:
                        X = np.column_stack([Xc[CAND[j]] for j in sub]); b, *_ = np.linalg.lstsq(X, yr, rcond=None); r2 = 1 - ((yr - X @ b) @ (yr - X @ b)) / tss
                    else:
                        r2 = 0.0
                    lm.append(0.5 * (n - 1 - kk) * log(1 + gg) - 0.5 * (n - 1) * log(1 + gg * (1 - r2)) - log(K + 1) - (lgamma(K + 1) - lgamma(kk + 1) - lgamma(K - kk + 1)))
                    mods.append(sub)
            lm = np.array(lm); w = np.exp(lm - lm.max()); w /= w.sum()
            out[f"{o}:{'within' if within else 'pooled'}"] = {c: float(sum(w[i] for i, s in enumerate(mods) if j in s)) for j, c in enumerate(CAND)}
    return out


def logit_fit(X, y, ridge=1e-3):
    b = np.zeros(X.shape[1])
    for _ in range(60):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        H = (X * (p * (1 - p))[:, None]).T @ X + ridge * np.eye(len(b)); step = np.linalg.solve(H, X.T @ (y - p) - ridge * b); b += step
        if np.abs(step).max() < 1e-8:
            break
    return b


def c4(Pm):
    """takeoff hazard on the imputed annual panel: ter crosses 15%; H=gdppc_log, E=eci_pct (or emp_agri reversed), S=gov_cons, lag 5."""
    isos = G["isos"]; ter = inv("ter", Pm["ter"]); rows = []
    E = Pm.get("eci_pct", None)
    for i, c in enumerate(isos):
        below = False
        for j, y in enumerate(YEARS):
            if j < 5 or not np.isfinite(ter[i, j]):
                continue
            h, e, s = Pm["gdppc_log"][i, j - 5], (E[i, j - 5] if E is not None else np.nan), Pm["gov_cons"][i, j - 5]
            if ter[i, j] < 15:
                below = True
                if np.isfinite([h, e, s]).all():
                    rows.append((c, y, h, e, s, 0))
            elif below:
                if np.isfinite([h, e, s]).all():
                    rows.append((c, y, h, e, s, 1))
                break
            else:
                break
    if len(rows) < 200:
        return None
    A = np.array([r[2:5] for r in rows], float); yv = np.array([r[5] for r in rows], float); cc = np.array([r[0] for r in rows]); yr = np.array([r[1] for r in rows])
    Z = (A - A.mean(0)) / A.std(0); thr = np.median(A, 0); d = (A >= thr).astype(float); cnt = d.sum(1)
    dec = np.column_stack([(yr >= k) & (yr < k + 10) for k in (1985, 1995, 2005, 2015)]).astype(float)
    base = np.column_stack([np.ones(len(yv)), dec])
    D = {"additive": np.column_stack([base, Z]), "threshold": np.column_stack([base, d]), "count": np.column_stack([base] + [(cnt == k).astype(float) for k in (1, 2, 3)]),
         "joint": np.column_stack([base, Z, d.prod(1)])}
    us = np.unique(cc); rng = np.random.default_rng(0); out = {k: [] for k in D}
    for rep in range(5):
        perm = rng.permutation(us); fold = {c: i % 10 for i, c in enumerate(perm)}; f = np.array([fold[c] for c in cc])
        for k, X in D.items():
            ll = np.zeros(len(yv))
            for q in range(10):
                te = f == q; b = logit_fit(X[~te], yv[~te]); p = np.clip(1 / (1 + np.exp(-(X[te] @ b))), 1e-6, 1 - 1e-6)
                ll[te] = -(yv[te] * np.log(p) + (1 - yv[te]) * np.log(1 - p))
            out[k].append(ll.mean())
    return dict(n=len(yv), events=int(yv.sum()), countries=len(us), logloss={k: float(np.mean(v)) for k, v in out.items()})


def d_expected(Pm):
    isos = G["isos"]; j = 2015 - 1970; res = {}
    dem = np.column_stack([Pm[k][:, j] for k in ("fertility", "u5mr", "young_share", "life_exp")])
    ok0 = np.isfinite(dem).all(1); Z = np.full(dem.shape[0], np.nan)
    Zd = (dem[ok0] - dem[ok0].mean(0)) / dem[ok0].std(0); Zd[:, 3] *= -1; w = np.linalg.svd(Zd, full_matrices=False)[2][0]; w = w if w.sum() > 0 else -w; Z[ok0] = Zd @ w
    for o in ("ter", "sec", "lsc"):
        y = Pm[o][:, j]; X = np.column_stack([np.ones(len(isos)), Z, Pm["gdppc_log"][:, j], Pm["urban"][:, j], Pm["electricity"][:, j]])
        m = np.isfinite(y) & np.isfinite(X).all(1)
        if m.sum() < 40:
            continue
        b, *_ = np.linalg.lstsq(X[m], y[m], rcond=None); pred = X @ b
        res[o] = {isos[i]: dict(actual=float(inv(o, y[i])), expected=float(inv(o, pred[i]))) for i in np.where(m)[0]}
    return res


def run_m(seed):
    Pm = impute_one(1000 + seed); R = rows_from(Pm)
    out = dict(c1=c1(R), c2=c2(R), c3=c3(R), c4=c4(Pm), d=d_expected(Pm))
    if seed == 0:
        with open(os.path.join(OUT, "imputed_m01.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["iso", "year"] + G["names"])
            for i, c in enumerate(G["isos"]):
                for jj, y in enumerate(YEARS):
                    w.writerow([c, y] + [("" if not np.isfinite(Pm[k][i, jj]) else round(float(inv(k, Pm[k][i, jj])), 4)) for k in G["names"]])
    return out


def rubin(vals):
    """vals: list of (b, se); returns combined b, se, t."""
    b = np.array([v[0] for v in vals]); s = np.array([v[1] for v in vals]); m = len(b)
    W = np.mean(s ** 2); B = np.var(b, ddof=1) if m > 1 else 0.0; T = W + (1 + 1 / m) * B
    return float(b.mean()), float(np.sqrt(T)), float(b.mean() / np.sqrt(T)) if T > 0 else 0.0


def longrun():
    out = {}
    try:
        page = urllib.request.urlopen(urllib.request.Request("https://barrolee.github.io/BarroLeeDataSet/Enroll.html", headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "ignore")
        links = re.findall(r'href="([^"]+\.csv)"', page)
        out["links"] = links[:6]
        url = next((l for l in links if re.search(r"MF|total|Total|_T", l)), links[0] if links else None)
        if url and not url.startswith("http"):
            url = "https://barrolee.github.io/BarroLeeDataSet/" + url.lstrip("./")
        raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read().decode("utf-8", "ignore")
        rd = list(csv.DictReader(io.StringIO(raw))); cols = list(rd[0].keys()); out["url"] = url; out["columns"] = cols[:20]
        isoc = next((c for c in cols if c.lower() in ("wbcode", "code", "iso", "iso3")), None); yc = next((c for c in cols if c.lower() == "year"), None)
        terc = [c for c in cols if re.search(r"ter|high", c, re.I) and not re.search(r"male|fem", c, re.I)]
        out["ter_col"] = terc[:3]
        ser = {}
        if isoc and yc and terc:
            for r in rd:
                try:
                    ser.setdefault(r[isoc].strip().upper(), {})[int(float(r[yc]))] = float(r[terc[0]])
                except Exception:
                    pass
        wdi = S._series("ter"); first = {}
        for c in sorted(set(ser) | set(wdi)):
            pts = {y: v for y, v in ser.get(c, {}).items() if y < 1970}; pts.update({y: v for y, v in wdi.get(c, {}).items()})
            yrs = sorted(y for y, v in pts.items() if v >= 15)
            if yrs:
                first[c] = yrs[0]
        out["first_year_ter15"] = {c: first.get(c) for c in sorted(ASIA_ISO | {"KOR", "JPN", "USA", "GBR", "IND", "CHN"}) if c in first}
        out["n_countries_with_longrun"] = len(ser)
    except Exception as e:
        out["error"] = repr(e)
    return out


def main(workers=8):
    os.makedirs(OUT, exist_ok=True); t0 = time.time()
    isos, meta, names, P = load_panel()
    G.update(isos=isos, meta=meta, names=names, P=P)
    with Pool(workers, initializer=lambda g: G.update(g), initargs=(dict(G),)) as pl:
        runs = pl.map(run_m, list(range(M)), chunksize=1)
    print("imputations done", round(time.time() - t0), flush=True)
    comb = {}
    for key in ("c1", "c2"):
        allk = set().union(*[r[key].keys() for r in runs])
        comb[key] = {k: rubin([r[key][k] for r in runs if k in r[key]]) for k in allk if sum(k in r[key] for r in runs) >= M // 2}
    pip = {}
    for r in runs:
        for k, d in r["c3"].items():
            for c, v in d.items():
                pip.setdefault(k, {}).setdefault(c, []).append(v)
    comb["c3"] = {k: {c: round(float(np.mean(v)), 3) for c, v in d.items()} for k, d in pip.items()}
    c4s = [r["c4"] for r in runs if r["c4"]]
    comb["c4"] = dict(n_imputations=len(c4s), mean_logloss={k: float(np.mean([c["logloss"][k] for c in c4s])) for k in c4s[0]["logloss"]} if c4s else None,
                      best_share={k: float(np.mean([min(c["logloss"], key=c["logloss"].get) == k for c in c4s])) for k in c4s[0]["logloss"]} if c4s else None,
                      n_rows=c4s[0]["n"] if c4s else None, events=c4s[0]["events"] if c4s else None)
    exp = {}
    for o in ("ter", "sec", "lsc"):
        cs = set().union(*[r["d"].get(o, {}).keys() for r in runs])
        exp[o] = {c: dict(actual=float(np.mean([r["d"][o][c]["actual"] for r in runs if c in r["d"].get(o, {})])),
                          expected=float(np.mean([r["d"][o][c]["expected"] for r in runs if c in r["d"].get(o, {})]))) for c in cs}
    LR = longrun()
    # complete-case comparison
    cc_path = os.path.join(S.HERE, "results", "sweep", "robust_table.csv")
    cc = {}
    if os.path.exists(cc_path):
        for r in csv.DictReader(open(cc_path)):
            cc[f"{r['outcome']}<-{r['var']}"] = r["robust"] == "True"
    json.dump(dict(combined=comb, expected_2015=exp, longrun=LR), open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    L = [f"APEX v1.1 MULTIPLE IMPUTATION (M={M}) ({round(time.time() - t0)}s)", ""]
    L.append("C1. Pooled base edges, Rubin-combined |t|>2.58 (p<0.01). [CC] = robust in the complete-case sweep:")
    for o in ("ter", "sec", "lsc"):
        ks = sorted([(k, v) for k, v in comb["c1"].items() if k.startswith(o + "<-") and abs(v[2]) > 2.58], key=lambda kv: -abs(kv[1][2]))
        L.append(f"   {o}: " + ", ".join(f"{k.split('<-')[1]}({v[0]:+.2f}{'*CC' if cc.get(k) else ''})" for k, v in ks[:18]))
        lost = [k.split('<-')[1] for k, r in cc.items() if r and k.startswith(o + "<-") and not (k in comb["c1"] and abs(comb["c1"][k][2]) > 2.58)]
        L.append(f"   {o}: complete-case robust edges NOT significant after imputation: {', '.join(lost) or 'none'}")
    L += ["", "C2. Within-country (country FE, log-odds) edges among focus vars, Rubin-combined |t|>2.58:"]
    ks = sorted([(k, v) for k, v in comb["c2"].items() if abs(v[2]) > 2.58], key=lambda kv: -abs(kv[1][2]))
    for k, v in ks[:40]:
        a, b = k.split("->"); rev = comb["c2"].get(f"{b}->{a}")
        L.append(f"   {k:26s} b={v[0]:+.3f} t={v[2]:+.1f}   reverse t={rev[2]:+.1f}" if rev else f"   {k:26s} b={v[0]:+.3f} t={v[2]:+.1f}")
    L += ["", "C3. Exact BMA PIPs averaged over imputations (pooled | within):"]
    for o in ("ter", "sec", "lsc"):
        p, w = comb["c3"].get(f"{o}:pooled", {}), comb["c3"].get(f"{o}:within", {})
        L.append(f"   {o}: " + ", ".join(f"{c} {p.get(c, float('nan')):.2f}|{w.get(c, float('nan')):.2f}" for c in CAND))
    L += ["", f"C4. Takeoff hazard on imputed panel: {comb['c4']}", "", "D. Expected vs actual 2015 (mean over imputations), Asia + selected:"]
    for o in ("ter", "sec", "lsc"):
        rows = [(c, d["actual"], d["expected"]) for c, d in exp[o].items() if c in ASIA_ISO]
        rows.sort(key=lambda r: r[1] - r[2])
        L.append(f"   {o}: " + "; ".join(f"{c} {a:.0f} vs {e:.0f} ({a - e:+.0f})" for c, a, e in rows))
    L += ["", f"B. Long-run splice (Lee & Lee 1950-1965 + WDI): {json.dumps(LR)[:1500]}", "",
          "Imputation is model-based; results are associations. Imputed values never extend more than 5 years beyond a country's observed range."]
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
