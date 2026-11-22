#!/usr/bin/env python3
"""Is it electrification, or the bundle?

Builds a time-varying composite infrastructure index (electricity, water,
sanitation, internet) and asks whether it explains schooling better than any
single component — and whether it too stops at the floor.
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
COMP = ["electricity", "water", "sanit", "internet"]
OUT = ["prm_cmp", "lsc", "sec", "ter"]
CTRL = ["gdppc_log", "urban"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in COMP + OUT + CTRL}

# ---------- the bundle as one factor (country means, for description) ----------
isos = sorted({i for (i, t) in S["electricity"]})
cm = {c: {} for c in COMP}
for c in COMP:
    for i in isos:
        xs = [S[c][(i, y)] for y in range(2000, 2021) if (i, y) in S[c]]
        if len(xs) >= 3:
            cm[c][i] = np.mean(xs)
common = [i for i in isos if all(i in cm[c] for c in COMP)]
M = np.array([[cm[c][i] for c in COMP] for i in common])
print(f"components observed together for {len(common)} countries (2000-2020)")
print("\ncorrelation among the components:")
print("        " + "".join(f"{c[:9]:>11s}" for c in COMP))
for a, c in enumerate(COMP):
    print(f"{c[:8]:>8s}" + "".join(f"{np.corrcoef(M[:, a], M[:, b])[0,1]:11.2f}"
                                   for b in range(len(COMP))))
Zc = (M - M.mean(0)) / M.std(0)
w, V = np.linalg.eigh(np.cov(Zc.T))
pc1 = V[:, -1]
if pc1.sum() < 0:
    pc1 = -pc1
print(f"\nPC1 loadings: " + ", ".join(f"{c}={pc1[j]:+.2f}" for j, c in enumerate(COMP)))
print(f"variance explained by PC1: {w[-1]/w.sum()*100:.1f}%")

# ---------- time-varying index ----------
bz, bs = {}, {}
for c in COMP:
    vals = np.array(list(S[c].values()))
    mu, sd = vals.mean(), vals.std()
    bz[c] = {k: (v - mu) / sd for k, v in S[c].items()}
keyed = set()
for c in COMP:
    keyed |= set(bz[c])
IDX, NZ = {}, {}
for k in keyed:
    vs = [bz[c][k] for c in COMP if k in bz[c]]
    if len(vs) >= 2:
        IDX[k] = float(np.mean(vs))
        NZ[k] = len(vs)
print(f"\ntime-varying index built for {len(IDX)} country-years "
      f"(median components per observation: {int(np.median(list(NZ.values())))})")


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def run(outcome, xmap, ctrls=CTRL):
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome] or (i, t) not in xmap:
            continue
        rec = [i, t, S[outcome][(i, t + 10)] - v, v, xmap[(i, t)]]
        ok = True
        for c in ctrls:
            if (i, t) in S[c]:
                rec.append(S[c][(i, t)])
            else:
                ok = False
                break
        if ok:
            rows.append(rec)
    if len(rows) < 120:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    gy = np.array([(r[1] // 10) * 10 for r in rows])
    y = np.array([r[2] for r in rows])
    own = np.array([r[3] for r in rows])
    xx = np.array([r[4] for r in rows], float)
    cols = [xx, own] + [np.array([r[5 + j] for r in rows]) for j in range(len(ctrls))]
    X = np.column_stack([np.ones(len(y))] + cols)
    X = np.column_stack([dm(X[:, j], gi) for j in range(X.shape[1])])
    X = np.column_stack([dm(X[:, j], gy) for j in range(X.shape[1])])
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
    se = float(np.sqrt(max(Vb[1, 1], 0)))
    sd = xx.std()
    return float(b[1]), se, len(rows), len(ui), sd


print("\n" + "=" * 92)
print("EACH SCHOOLING OUTCOME, BY THE BUNDLE AND BY ITS PARTS")
print("(coefficient per one standard deviation of the predictor, within country)")
print("=" * 92)
names = ["BUNDLE", "electricity", "water", "sanitation", "internet"]
maps = [IDX] + [bz[c] for c in COMP]
print(f"{'outcome':10s}" + "".join(f"{n:>13s}" for n in names))
for o in OUT:
    line = f"{o:10s}"
    for xm in maps:
        r = run(o, xm)
        if r:
            t = r[0] / r[1] if r[1] > 0 else 0
            line += f"{r[0]:+9.3f}{'*' if abs(t) > 1.96 else ' '}  "
        else:
            line += f"{'--':>13s}"
    print(line)
print("\n  * significant at 5%. Country and decade fixed effects; own starting level,")
print("  income and urbanisation controlled throughout.")
