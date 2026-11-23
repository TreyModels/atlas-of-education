import os
#!/usr/bin/env python3
"""Lead-lag matrices for the MASSIFICATION variables, computed inside each grouping.

Fast version: within-transformation instead of dummy columns.
Pair is 'robust' only if it holds pooled AND within countries, same sign.
"""
import json, os, gzip, itertools, sys
from multiprocessing import Pool
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
VARS = ["lsc", "sec", "ter", "prm_cmp", "gpi_ter",
        "u5mr", "gdppc_log", "urban", "electricity", "wage_emp", "flfp"]
SH = {"fertility": "births", "lsc": "lowsec comp", "sec": "upper sec comp",
      "ter": "higher ed", "prm_cmp": "primary comp", "gpi_ter": "F/M higher",
      "u5mr": "child surv", "gdppc_log": "income", "urban": "cities",
      "electricity": "electricity", "wage_emp": "paid jobs", "flfp": "women work"}


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in VARS + ["fertility"]}
F = S["fertility"]

# ---- flat panel ----
keys = sorted({(i, t) for (i, t) in F if 1955 <= t <= 2015})
IDX = {k: n for n, k in enumerate(keys)}
ISOS = sorted({i for (i, t) in keys})
UI = {v: n for n, v in enumerate(ISOS)}
N = len(keys)
ISO = np.array([UI[i] for (i, t) in keys])
YR = np.array([t for (i, t) in keys])
COL = {}
for v in VARS:
    a = np.full(N, np.nan)
    for (i, t), val in S[v].items():
        j = IDX.get((i, t))
        if j is not None:
            a[j] = val
    COL[v] = a
FWD = {}
for v in VARS:
    a = np.full(N, np.nan)
    for (i, t), val in S[v].items():
        j = IDX.get((i, t + 10))
        if j is not None:
            a[j] = val
    FWD[v] = a


def dm(a, g):
    s = np.bincount(g, weights=a)
    c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(y, x, own, gi, gy, fe):
    n = len(y)
    if n < 100:
        return None
    yy = y - own.mean() * 0 + 0.0  # keep y raw; own added as column
    X = np.column_stack([np.ones(n), x, own])
    Y = y
    if fe:
        X = np.column_stack([dm(X[:, j], gi) for j in range(X.shape[1])])
        X = np.column_stack([dm(X[:, j], gy) for j in range(X.shape[1])])
        Y = dm(dm(y, gi), gy)
    else:
        for d in np.unique(gy)[1:]:
            X = np.column_stack([X, (gy == d).astype(float)])
    try:
        b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    except Exception:
        return None
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    try:
        Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
        se = float(np.sqrt(max(Vb[1, 1], 0)))
    except Exception:
        return None
    return float(b[1]), se


def edge(args):
    a, b, members = args
    mid = np.array([UI[m] for m in members if m in UI], dtype=int)
    inm = np.isin(ISO, mid)
    mask = np.isfinite(COL[a]) & np.isfinite(COL[b]) & np.isfinite(FWD[b]) & inm
    if mask.sum() < 100:
        return None
    gi = ISO[mask]; gy = (YR[mask] // 10) * 10
    if len(np.unique(gi)) < 8:
        return None
    y = FWD[b][mask] - COL[b][mask]
    x = COL[a][mask]; own = COL[b][mask]
    p = fit(y, x, own, gi, gy, False)
    f = fit(y, x, own, gi, gy, True)
    if not p or not f:
        return None
    same = (p[0] > 0) == (f[0] > 0) and p[0] != 0
    rob = same and p[1] > 0 and f[1] > 0 and abs(p[0] / p[1]) > 1.96 and abs(f[0] / f[1]) > 1.96
    return (a, b, p[0], f[0], rob)


# ---------- groupings ----------
def mm(iso, key, a=1990, b=2020):
    xs = [S[key][(iso, y)] for y in range(a, b + 1) if (iso, y) in S[key]]
    return float(np.mean(xs)) if len(xs) >= 3 else np.nan


isos = [i for i in ISOS]
D = {}
for i in isos:
    onset = None
    for y in sorted(y for (j, y) in F if j == i):
        if F[(i, y)] < 5.0:
            onset = y
            break
    D[i] = dict(onset=onset, lsc=mm(i, "lsc"), ter=mm(i, "ter"), sec=mm(i, "sec"),
                gdppc=mm(i, "gdppc_log"), elec=mm(i, "electricity"), tax=np.nan)


def g_onset(i):
    o = D[i]["onset"]
    if o is None: return "never yet"
    if o <= 1975: return "early (by 1975)"
    if o <= 1990: return "middle (1976-90)"
    if o <= 2005: return "late (1991-2005)"
    return "just starting (after 2005)"


def g_gate(i):
    t, s = D[i]["ter"], D[i]["sec"]
    if not (np.isfinite(t) and np.isfinite(s) and s > 0): return None
    g = t / s
    return "tight gate" if g < 0.28 else ("open gate" if g > 0.55 else "middling gate")


GROUPINGS = {"ONSET COHORT": g_onset, "GATE TIGHTNESS": g_gate}
TARGETS = ["ter", "sec", "lsc"]

if __name__ == "__main__":
    tasks = []
    meta_g = []
    for title, fn in GROUPINGS.items():
        buckets = {}
        for i in isos:
            g = fn(i)
            if g: buckets.setdefault(g, []).append(i)
        for g, mem in sorted(buckets.items()):
            meta_g.append((title, g, len(mem)))
            for a in VARS:
                for b in VARS:
                    if a != b:
                        tasks.append((title, g, tuple(mem), a, b))
    print("tasks:", len(tasks), flush=True)
    with Pool(48) as p:
        res = p.map(edge, [(t[3], t[4], t[2]) for t in tasks], chunksize=16)
    # reassemble
    store = {}
    for t, r in zip(tasks, res):
        if r:
            store.setdefault((t[0], t[1]), {})[(r[0], r[1])] = r
    for title in GROUPINGS:
        print("\n" + "=" * 82)
        print(title)
        print("=" * 82)
        for (tt, g, nc) in meta_g:
            if tt != title:
                continue
            D2 = store.get((tt, g), {})
            print(f"\n  {g} — {nc} countries, {len(D2)} pairs computed")
            for T in TARGETS:
                ins, outs2 = [], []
                for a in VARS:
                    if a == T: continue
                    ab = D2.get((a, T)); ba = D2.get((T, a))
                    if not ab or not ba: continue
                    if ab[4] and not ba[4]: ins.append((a, ab[2]))
                    elif ba[4] and not ab[4]: outs2.append((a, ba[2]))
                ins.sort(key=lambda z: abs(z[1]), reverse=True)
                outs2.sort(key=lambda z: abs(z[1]), reverse=True)
                print(f"     -> {SH[T]:12s} " + (", ".join(f"{SH[a]}({v:+.2f})" for a, v in ins[:6]) or "(none)"))
                if outs2:
                    print(f"        {SH[T]:12s} -> " + ", ".join(f"{SH[a]}({v:+.2f})" for a, v in outs2[:5]))
            outs = []
            for b in VARS:
                if b == "fertility": continue
                ab = D2.get(("fertility", b)); ba = D2.get((b, "fertility"))
                if ab and ba and ab[4] and not ba[4]:
                    outs.append((b, ab[2]))
            outs.sort(key=lambda z: -abs(z[1]))
            if outs:
                print("     births -> " + ", ".join(f"{SH[b]}({v:+.2f})" for b, v in outs[:6]))
