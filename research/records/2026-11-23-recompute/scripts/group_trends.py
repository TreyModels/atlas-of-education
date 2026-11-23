import os
#!/usr/bin/env python3
"""Six experimental clusterings, and the trend test run inside each.

The question this answers: electricity's effect collapses when each country gets
its own linear trend. Does it collapse everywhere, or only in some kinds of country?
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
KEYS = ["electricity", "wage_emp", "lsc", "sec", "ter", "gdppc_log", "urban", "tax", "u5mr"]
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in KEYS}
ISOS = sorted({i for (i, t) in S["electricity"]})


def mean_of(k, i, a=1990, b=2020):
    xs = [S[k][(i, y)] for y in range(a, b + 1) if (i, y) in S[k]]
    return float(np.mean(xs)) if len(xs) >= 3 else np.nan


def first_of(k, i, a=1960, b=1990):
    for y in range(a, b + 1):
        if (i, y) in S[k]:
            return S[k][(i, y)]
    return np.nan


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(outcome, xname, members, country_trend=False):
    rows = []
    for (i, t), v in S[outcome].items():
        if i not in members or (i, t + 10) not in S[outcome] or (i, t) not in S[xname]:
            continue
        if not all((i, t) in S[c] for c in ("gdppc_log", "urban")):
            continue
        rows.append([i, t, S[outcome][(i, t + 10)] - v, v, S[xname][(i, t)],
                     S["gdppc_log"][(i, t)], S["urban"][(i, t)]])
    if len(rows) < 120 or len({r[0] for r in rows}) < 8:
        return None
    if country_trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
        if len(rows) < 120 or len({r[0] for r in rows}) < 8:
            return None
    iso = [r[0] for r in rows]
    ui = {v2: n for n, v2 in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v2] for v2 in iso]); yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    y = np.array([r[2] for r in rows])
    cols = [np.array([r[4] for r in rows], float), np.array([r[3] for r in rows]),
            np.array([r[5] for r in rows], float), np.array([r[6] for r in rows], float)]
    if country_trend:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(y))] + cols)
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(y, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(y), len(ui)


def km(Z, k, restarts=25, seed=3):
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(restarts):
        C = Z[rng.choice(len(Z), k, replace=False)]
        for _ in range(200):
            lab = ((Z[:, None, :] - C[None, :, :]) ** 2).sum(2).argmin(1)
            C2 = np.array([Z[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
            if np.allclose(C2, C):
                break
            C = C2
        inert = ((Z - C[lab]) ** 2).sum()
        if best is None or inert < best[0]:
            best = (inert, lab.copy())
    return best[1]


def tercile(vals, labels):
    v = np.array(vals, float)
    ok = np.isfinite(v)
    q = np.percentile(v[ok], [33, 67])
    out = {}
    for i, x in zip(ISOS, v):
        if not np.isfinite(x):
            continue
        out[i] = labels[0] if x <= q[0] else (labels[2] if x >= q[1] else labels[1])
    return out


# ---------------- the six clusterings ----------------
CL = {}

# 1. baseline attainment: lower-secondary completion as first observed
base = {i: first_of("lsc", i) for i in ISOS}
CL["1. BASELINE SCHOOLING (where they started)"] = tercile(
    [base[i] for i in ISOS], [f"low start", "middle start", "high start"])

# 2. transition onset
def onset(i):
    for y in sorted(y for (j, y) in S["ter"] if j == i):
        pass
    for y in sorted(y for (j, y) in S["u5mr"] if j == i):
        pass
    return None
fert = {(r[0], int(r[1])): r[2] for r in []}
o = {}
for i in ISOS:
    pass
CL["2. TRAJECTORY (what changed 1990-2020)"] = {}
tr = []
for i in ISOS:
    a = first_of("lsc", i, 1985, 1995); b = mean_of("lsc", i, 2015, 2020)
    tr.append((i, (b - a) if (np.isfinite(a) and np.isfinite(b)) else np.nan))
tv = [x[1] for x in tr]
lab = tercile([x[1] for x in tr], ["stalled", "steady", "fast riser"])
CL["2. TRAJECTORY (what changed 1990-2020)"] = lab

# 3. state presence portfolio (k-means)
feat = []
ok_isos = []
for i in ISOS:
    row = [mean_of(k, i) for k in ("electricity", "gdppc_log", "urban", "tax")]
    if all(np.isfinite(row)):
        feat.append(row); ok_isos.append(i)
F = np.array(feat); Z = (F - F.mean(0)) / F.std(0)
lab3 = km(Z, 3)
order = np.argsort([F[lab3 == j][:, 0].mean() for j in range(3)])
names3 = {}
for rank, j in enumerate(order):
    names3[j] = ["thin state", "middling state", "deep state"][rank]
CL["3. STATE PRESENCE (k-means on power/income/cities/tax)"] = {
    ok_isos[n]: names3[lab3[n]] for n in range(len(ok_isos))}

# 4. wage economy depth
CL["4. WAGE ECONOMY DEPTH"] = tercile(
    [mean_of("wage_emp", i) for i in ISOS], ["thin wage economy", "middling", "deep wage economy"])

# 5. income band
CL["5. INCOME BAND (1990-2020 mean)"] = tercile(
    [mean_of("gdppc_log", i) for i in ISOS], ["low income", "middle income", "high income"])

# 6. child survival
CL["6. CHILD SURVIVAL (mean deaths under 5)"] = tercile(
    [mean_of("u5mr", i) for i in ISOS], ["high mortality", "middle", "low mortality"])

TESTS = [("electricity", "lsc"), ("electricity", "sec"), ("wage_emp", "ter")]

for title, assignment in CL.items():
    groups = {}
    for i, g in assignment.items():
        if g is not None and np.isfinite(1.0):
            groups.setdefault(g, set()).add(i)
    if not groups:
        continue
    print("\n" + "=" * 92)
    print(title)
    print("=" * 92)
    print(f"{'group':22s}{'countries':>10s}  {'relationship':22s}{'no trends':>14s}{'with trends':>14s}  verdict")
    for g in sorted(groups):
        mem = groups[g]
        for x, o2 in TESTS:
            a = fit(o2, x, mem, False)
            b = fit(o2, x, mem, True)
            if not a or not b:
                continue
            if abs(b[0]) > 50 or abs(a[0]) > 50:
                surv = "UNSTABLE"
            elif abs(b[0]) <= 1.96 * b[1]:
                surv = "dies"
            elif (b[0] > 0) != (a[0] > 0):
                surv = "SIGN FLIP"
            elif abs(b[0]) > 0.5 * abs(a[0]):
                surv = "SURVIVES"
            else:
                surv = "attenuates"
            print(f"{g[:21]:22s}{len(mem):>10d}  {x[:8]+' -> '+o2:22s}"
                  f"{a[0]:+8.3f}±{a[1]:.2f}{b[0]:+8.3f}±{b[1]:.2f}  {surv}")
