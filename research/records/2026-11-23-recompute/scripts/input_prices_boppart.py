#!/usr/bin/env python3
"""Input-price test rebuilt to follow Boppart, Kiernan, Krusell & Malmberg (2023, NBER w31101), with a TRUE log income control.

Their set-up (paper sections 2 and 4): four agricultural inputs (labour h incl. human capital, capital k, land l,
intermediates x = fertiliser/pesticides/etc.), prices w (labour compensation per worker = PWT labour share x output
per worker), Pk (PWT investment price), Px (BACI trade unit values of fertiliser and pesticides, country-specific),
quantities of k and x per unit of labour (FAO/UN). Elasticities come from the 2005 CROSS-SECTION: log quantity ratio on
log price ratio, matched at the two extremes of the sample (poorest vs richest), nested CES.
Ours: the same objects as far as the data allow. Px is the World Bank Pink Sheet world fertiliser price (no cross-country
variation: BACI is not available here), quantities are USDA ERS agricultural inputs per worker.

PART 1 (their object, intensity): log(M/L) on log(w/Px) and log(K/L) on log(w/Pk): 2005 cross-section OLS, arc
        elasticity (bottom vs top income decile), and a 10-year within-country panel with country and year effects.
PART 2 (the structural-change test): world fertiliser price change x baseline exposure, outcomes farm share,
        paid-job share, births; income controlled with TRUE log GDP per head (level, 10-yr change, change x exposure).
        Exposure A = baseline farm employment share (as before); exposure B = baseline log intermediates per worker
        (their mechanism: farms that use more purchased inputs feel the input price more).
        Wage-ratio variant: x = d log(Px / w_it) (their relative price), with and without income.
"""
import json, os, gzip, sys
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


# gdppc_log.json: true log if the fixed data are used, levels in the original file. Detect and log if needed.
gd = load("gdppc_log")
if np.median(list(gd.values())) > 30:
    gd = {k: np.log(v) for k, v in gd.items() if v > 0}
    print("NOTE: gdppc_log.json held levels; logged here.")
else:
    print("gdppc_log.json is already a true log.")
meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items() if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
K = ["emp_agri", "wage_emp", "fertility", "urban", "pwt_yw", "pwt_labsh", "pwt_pli", "usda_KperL", "usda_MperL"]
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in K}
S["gdp"] = {k: v for k, v in gd.items() if k[0] in REG}

# fertiliser real price index (Pink Sheet): phosphate rock, DAP, potassium chloride averaged
import openpyxl
wb = openpyxl.load_workbook(os.path.join(DATA, "pinksheet.xlsx"), read_only=True, data_only=True)
rows = [r for r in wb["Annual Prices (Real)"].iter_rows(values_only=True)]
hdr = next(i for i, r in enumerate(rows[:12]) if any("DAP" in str(c) for c in r[1:] if c))
names = [str(c) if c else "" for c in rows[hdr]]
want = [j for j, n in enumerate(names) if any(k in n for k in ("DAP", "Phosphate rock", "Potassium"))]
fer = {}
for r in rows[hdr + 1:]:
    if isinstance(r[0], (int, float)) and 1955 <= r[0] <= 2024:
        v = [r[j] for j in want if isinstance(r[j], (int, float))]
        if v:
            fer[int(r[0])] = float(np.mean(v))
LF = {y: np.log(v) for y, v in fer.items()}


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def reg(y, cols, gi=None, gy=None, trend_yr=None, cluster=None):
    """OLS of y on cols (first col = focus). Optional country FE (gi), year/decade FE (gy), country trends. Cluster SE."""
    X = np.column_stack([np.ones(len(y))] + cols)
    if trend_yr is not None:
        T = np.column_stack([((gi == j) * trend_yr) for j in np.unique(gi)]).astype(float)
        X = np.column_stack([X, T])
    Y = y.copy()
    if gi is not None:
        X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])]); Y = dm(Y, gi)
    if gy is not None:
        X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])]); Y = dm(Y, gy)
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    cl = cluster if cluster is not None else np.arange(len(y))
    meat = np.zeros_like(XtX)
    for c in np.unique(cl):
        m = cl == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    P = np.linalg.pinv(XtX)
    V = P @ meat @ P
    return float(b[1]), float(np.sqrt(max(V[1, 1], 0))), len(y)


def fmt(r):
    return "n/a" if r is None else f"{r[0]:+8.4f} (±{1.96*r[1]:.4f}){'*' if abs(r[0]) > 1.96*r[1] else ' '} n={r[2]}"


# wage per worker (PWT labour compensation per worker, in levels of PPP$), log
W = {k: np.log(S["pwt_yw"][k] * S["pwt_labsh"][k]) for k in S["pwt_yw"] if k in S["pwt_labsh"] and S["pwt_yw"][k] * S["pwt_labsh"][k] > 0}
PLI = {k: np.log(v) for k, v in S["pwt_pli"].items() if v > 0}
LM = {k: np.log(v) for k, v in S["usda_MperL"].items() if v > 0}
LK = {k: np.log(v) for k, v in S["usda_KperL"].items() if v > 0}

print("=" * 100)
print("PART 1. INTENSITY (their object). Elasticity = d log(quantity per worker) / d log(w / price).  Boppart et al.: capital-labour 1.90 (agriculture; 0.98 non-agriculture), intermediates 1.75 (text reading), land-vs-rest 0.66")
print("=" * 100)
for lab, Q, PR, PNAME in (("intermediates M/L on w/Px", LM, None, "fert"), ("capital K/L on w/Pk(pli)", LK, PLI, "pli")):
    # 2005 cross-section, mean of 2003-2007
    cs = {}
    for i in {k[0] for k in Q}:
        v = []
        for t in range(2003, 2008):
            if (i, t) in Q and (i, t) in W and ((t in LF) if PNAME == "fert" else ((i, t) in PLI)) and (i, t) in S["gdp"]:
                p = LF[t] if PNAME == "fert" else PLI[(i, t)]
                v.append((Q[(i, t)], W[(i, t)] - p, S["gdp"][(i, t)], W[(i, t)]))
        if v:
            cs[i] = np.mean(v, axis=0)
    ids = sorted(cs)
    q = np.array([cs[i][0] for i in ids]); r = np.array([cs[i][1] for i in ids]); inc = np.array([cs[i][2] for i in ids])
    if len(ids) > 20:
        b = reg(q, [r])
        # robust (HC1-like via per-observation cluster)
        lo, hi = inc <= np.percentile(inc, 10), inc >= np.percentile(inc, 90)
        arc = (q[hi].mean() - q[lo].mean()) / (r[hi].mean() - r[lo].mean())
        print(f"  {lab:28s} 2005 cross-section: slope {fmt(b)}  | arc elasticity poorest vs richest decile {arc:+.2f} "
              f"(quantity ratio x{np.exp(q[hi].mean()-q[lo].mean()):.0f}, price ratio x{np.exp(r[hi].mean()-r[lo].mean()):.1f})")
    # panel: 10-yr changes, country + year effects
    rows = []
    for (i, t), v in Q.items():
        if (i, t + 10) in Q and (i, t) in W and (i, t + 10) in W:
            if PNAME == "fert":
                if t in LF and t + 10 in LF:
                    d = (W[(i, t + 10)] - LF[t + 10]) - (W[(i, t)] - LF[t])
                else:
                    continue
            else:
                if (i, t) in PLI and (i, t + 10) in PLI:
                    d = (W[(i, t + 10)] - PLI[(i, t + 10)]) - (W[(i, t)] - PLI[(i, t)])
                else:
                    continue
            rows.append((i, t, Q[(i, t + 10)] - v, d))
    if rows:
        ids2 = sorted({r_[0] for r_ in rows}); ui = {c: n for n, c in enumerate(ids2)}
        gi = np.array([ui[r_[0]] for r_ in rows]); yr = np.array([r_[1] for r_ in rows])
        y = np.array([r_[2] for r_ in rows]); x = np.array([r_[3] for r_ in rows])
        a = reg(y, [x], gi=gi, gy=yr, cluster=gi)
        a2 = reg(y, [x], gi=gi, gy=yr, trend_yr=yr.astype(float), cluster=gi)
    lv = []
    for (i, t), v in Q.items():
        if (i, t) in W and (i, t) in S["gdp"] and ((t in LF) if PNAME == "fert" else ((i, t) in PLI)):
            lv.append((i, t, v, W[(i, t)] - (LF[t] if PNAME == "fert" else PLI[(i, t)])))
    if lv:
        ui3 = {c: n for n, c in enumerate(sorted({r_[0] for r_ in lv}))}
        g3 = np.array([ui3[r_[0]] for r_ in lv]); y3 = np.array([r_[1] for r_ in lv])
        L = reg(np.array([r_[2] for r_ in lv]), [np.array([r_[3] for r_ in lv])], gi=g3, gy=y3, cluster=g3)
        print(f"  {lab:28s} annual LEVELS, country+year effects (our CES design, no country-specific slopes): {fmt(L)}")
        print(f"  {lab:28s} 10-yr within-country panel, country+year effects: {fmt(a)} | + country trends: {fmt(a2)}")

print("\n" + "=" * 100)
print("PART 2. STRUCTURAL OUTCOMES: d log(world fertiliser price) x baseline exposure, 10-year changes, true-log income controlled")
print("=" * 100)


def baseline(series, iso, year=1990):
    for d in range(12):
        for y in (year + d, year - d):
            if (iso, y) in series:
                return series[(iso, y)]
    return None


def fit(outcome, xkind, expkind, inc, trend):
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome] or t not in LF or t + 10 not in LF:
            continue
        g0, g10, u = S["gdp"].get((i, t)), S["gdp"].get((i, t + 10)), S["urban"].get((i, t))
        expo = baseline(S["emp_agri"], i) if expkind == "farm" else baseline(LM, i)
        if g0 is None or g10 is None or u is None or expo is None:
            continue
        dlg = g10 - g0
        dp = LF[t + 10] - LF[t]
        if xkind == "WAGE":
            if (i, t) not in W or (i, t + 10) not in W:
                continue
            xr = dp - (W[(i, t + 10)] - W[(i, t)])
        else:
            xr = dp
        x = xr * expo
        ctrl = [u] + ([g0, dlg, dlg * expo] if inc else [])
        rows.append([i, t, S[outcome][(i, t + 10)] - v, v, x] + ctrl)
    if trend:
        cnt = {}
        for r_ in rows:
            cnt[r_[0]] = cnt.get(r_[0], 0) + 1
        rows = [r_ for r_ in rows if cnt[r_[0]] >= 4]
    if len(rows) < 150:
        return None
    ui = {c: n for n, c in enumerate(sorted({r_[0] for r_ in rows}))}
    gi = np.array([ui[r_[0]] for r_ in rows]); yr = np.array([r_[1] for r_ in rows]); gy = (yr // 10) * 10
    y = np.array([r_[2] for r_ in rows])
    cols = [np.array([r_[4] for r_ in rows], float), np.array([r_[3] for r_ in rows], float)] + \
           [np.array([r_[5 + j] for r_ in rows], float) for j in range(len(rows[0]) - 5)]
    return reg(y, cols, gi=gi, gy=gy, trend_yr=yr.astype(float) if trend else None, cluster=gi)


SPECS = [("PRICE x farm share, no income", "PRICE", "farm", False),
         ("PRICE x farm share + log income", "PRICE", "farm", True),
         ("PRICE x intermediates/worker, no income", "PRICE", "inten", False),
         ("PRICE x intermediates/worker + log income", "PRICE", "inten", True),
         ("Px/WAGE x farm share, no income", "WAGE", "farm", False),
         ("Px/WAGE x farm share + log income", "WAGE", "farm", True)]
for o, lab in (("emp_agri", "FARM EMPLOYMENT SHARE"), ("wage_emp", "PAID EMPLOYMENT SHARE"), ("fertility", "BIRTHS PER WOMAN")):
    print(f"\n{lab}\n{'specification':46s}{'country FE':>38s}{'country trends':>40s}")
    for sl, xk, ek, inc in SPECS:
        print(f"{sl:46s}{fmt(fit(o, xk, ek, inc, False)):>38s}{fmt(fit(o, xk, ek, inc, True)):>40s}")
print("\n(± = 95% half-width; * = excludes zero. Coefficient scale: per unit of d log price x exposure, exposure in percent or in log units.)")
