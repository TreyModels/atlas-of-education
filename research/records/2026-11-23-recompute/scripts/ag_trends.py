import os
#!/usr/bin/env python3
"""The agriculture paper's claims, put through the country-trend test.

Links as the paper states them:
  L1  input prices -> farm exit            (+0.445)
  L2  input prices -> wage employment      (-0.243)
  L3  input prices -> births               (-0.006, null)
  L4  fertility    -> farm exit            (+1.536)
  L5  farm exit    -> births               (+0.0011, null)

Each is estimated twice: with country fixed effects only, and with country-specific
linear trends added. A claim that only holds without trends is a trend.
"""
import json, os, gzip, urllib.request
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
K = ["emp_agri", "wage_emp", "fertility", "gdppc_log", "urban"]
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in K}

# ---- fertiliser price relative to income, rebuilt from the Pink Sheet ----
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
want = [j for j, n in enumerate(names)
        if any(k in n for k in ("DAP", "urea", "Phosphate rock", "Potassium"))]
fer = {}
for r in rows[hdr + 1:]:
    y = r[0]
    if isinstance(y, (int, float)) and 1955 <= y <= 2024:
        v = [r[j] for j in want if isinstance(r[j], (int, float))]
        if v:
            fer[int(y)] = float(np.mean(v))
print(f"fertiliser series: {min(fer)}-{max(fer)}, {len(fer)} years")


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def baseline(k, iso, year=1990):
    for d in range(12):
        for y in (year + d, year - d):
            if (iso, y) in S[k]:
                return S[k][(iso, y)]
    return None


def fit(outcome, kind, trend=False, ctrls=("urban",)):
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome]:
            continue
        if not all((i, t) in S[c] for c in ctrls):
            continue
        if kind == "input_price":
            if t not in fer or (t + 10) not in fer:
                continue
            g0, g10 = S["gdppc_log"].get((i, t)), S["gdppc_log"].get((i, t + 10))
            expo = baseline("emp_agri", i)
            if not g0 or not g10 or expo is None:
                continue
            r0, r10 = fer[t] / g0, fer[t + 10] / g10
            if r0 <= 0:
                continue
            x = np.log(r10 / r0) * expo
        else:
            if (i, t) not in S[kind]:
                continue
            x = S[kind][(i, t)]
        rows.append([i, t, S[outcome][(i, t + 10)] - v, v, x] +
                    [S[c][(i, t)] for c in ctrls])
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150 or len({r[0] for r in rows}) < 10:
        return None
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    yv = np.array([r[2] for r in rows])
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows])] + \
           [np.array([r[5 + j] for r in rows], float) for j in range(len(ctrls))]
    if trend:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(yv, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(yv), len(ui)


CLAIMS = [
    ("L1 input prices -> farm exit", "emp_agri", "input_price"),
    ("L2 input prices -> wage jobs", "wage_emp", "input_price"),
    ("L3 input prices -> births", "fertility", "input_price"),
    ("L4 fertility -> farm exit", "emp_agri", "fertility"),
    ("L5 farm exit -> births", "fertility", "emp_agri"),
]
print("\n" + "=" * 86)
print("THE AG PAPER'S FIVE CLAIMS, WITH AND WITHOUT COUNTRY TRENDS")
print("=" * 86)
print(f"{'claim':32s}{'FE only':>18s}{'with trends':>20s}   verdict")
for lab, o, k in CLAIMS:
    a = fit(o, k, False)
    b = fit(o, k, True)
    if not a or not b:
        print(f"{lab:32s} insufficient data")
        continue
    if abs(b[0]) <= 1.96 * b[1]:
        v = "dies"
    elif (a[0] > 0) != (b[0] > 0):
        v = "SIGN FLIP"
    else:
        v = "SURVIVES"
    print(f"{lab:32s}{a[0]:+9.4f}±{a[1]:.3f}{b[0]:+10.4f}±{b[1]:.3f}   {v}")
