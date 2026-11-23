#!/usr/bin/env python3
"""Rebuilt input-price test with income controlled (queue job 3).

The original (input_price_shock.txt; script input_prices.py lost) used fertiliser price / GDP per head
interacted with baseline farm share. Because the price is global and year effects absorb it, the only
variation left is each country's own income growth x its farm share. This script asks whether the effect
survives when income is controlled directly.

x variants (all x baseline farm share, 1990-ish employment share in agriculture):
  RATIO : d log( real fert price / GDPpc )         (the original construction; GDPpc as in gdppc_log.json)
  PRICE : d log( real fert price )                  (pure world price shock, no income in it)
Controls (all specs): urban share, own starting level, plus
  +INC  : log GDPpc at t, 10-yr change in log GDPpc, and (10-yr change in log GDPpc) x farm share
Each spec with country FE + decade effects, and with country linear trends. SE clustered by country.
"""
import json, os, gzip, urllib.request
import numpy as np

DATA = "/root/work/data"


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items() if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
K = ["emp_agri", "wage_emp", "fertility", "gdppc_log", "urban"]
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in K}

xlsx = os.path.join(DATA, "pinksheet.xlsx")
if not os.path.exists(xlsx):
    u = ("https://thedocs.worldbank.org/en/doc/"
         "5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Historical-Data-Annual.xlsx")
    open(xlsx, "wb").write(urllib.request.urlopen(
        urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read())
import openpyxl
wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
rows = [r for r in wb["Annual Prices (Real)"].iter_rows(values_only=True)]
hdr = next(i for i, r in enumerate(rows[:12]) if any("DAP" in str(c) for c in r[1:] if c))
names = [str(c) if c else "" for c in rows[hdr]]
want = [j for j, n in enumerate(names) if any(k in n for k in ("DAP", "Phosphate rock", "Potassium"))]
print("fertiliser columns:", [names[j] for j in want])
fer = {}
for r in rows[hdr + 1:]:
    y = r[0]
    if isinstance(y, (int, float)) and 1955 <= y <= 2024:
        v = [r[j] for j in want if isinstance(r[j], (int, float))]
        if v:
            fer[int(y)] = float(np.mean(v))
print(f"real fertiliser price index {min(fer)}-{max(fer)}; first/last {fer[min(fer)]:.1f}/{fer[max(fer)]:.1f}")


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def baseline(iso, year=1990):
    for d in range(12):
        for y in (year + d, year - d):
            if (iso, y) in S["emp_agri"]:
                return S["emp_agri"][(iso, y)]
    return None


def fit(outcome, xkind, inc, trend):
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome] or t not in fer or t + 10 not in fer:
            continue
        g0, g10, u = S["gdppc_log"].get((i, t)), S["gdppc_log"].get((i, t + 10)), S["urban"].get((i, t))
        expo = baseline(i)
        if not g0 or not g10 or u is None or expo is None or g0 <= 0 or g10 <= 0:
            continue
        dlg = np.log(g10 / g0)
        dp = np.log(fer[t + 10] / fer[t])
        x = (dp - dlg if xkind == "RATIO" else dp) * expo
        ctrl = [u] + ([np.log(g0), dlg, dlg * expo] if inc else [])
        rows.append([i, t, S[outcome][(i, t + 10)] - v, v, x] + ctrl)
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150:
        return None
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    yv = np.array([r[2] for r in rows])
    nc = len(rows[0]) - 5
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows], float)] + \
           [np.array([r[5 + j] for r in rows], float) for j in range(nc)]
    if trend:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(yv, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u_ = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u_[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(yv), len(ui)


SPECS = [("RATIO, no income control (orig. construction)", "RATIO", False),
         ("RATIO + income controls", "RATIO", True),
         ("PRICE only (world price shock), no income control", "PRICE", False),
         ("PRICE only + income controls", "PRICE", True)]
for o, lab in (("emp_agri", "FARM EMPLOYMENT SHARE"), ("wage_emp", "PAID EMPLOYMENT SHARE"), ("fertility", "BIRTHS PER WOMAN")):
    print("\n" + "=" * 96)
    print(lab)
    print(f"{'specification':52s}{'FE only':>22s}{'with country trends':>26s}")
    for sl, xk, inc in SPECS:
        a, b = fit(o, xk, inc, False), fit(o, xk, inc, True)
        f = lambda r: f"{r[0]:+9.4f} (±{1.96*r[1]:.4f}){'*' if abs(r[0])>1.96*r[1] else ' '} n={r[2]}" if r else "n/a"
        print(f"{sl:52s}{f(a):>22s}  {f(b)}")
print("\n(± is a 95% interval half-width; * = interval excludes zero.)")
