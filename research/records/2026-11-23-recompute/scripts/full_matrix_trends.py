import os
#!/usr/bin/env python3
"""Every variable against every other, with and without country-specific trends.

The question: of the directed edges that survive country fixed effects, how many
survive each country having its own linear trend?
"""
import json, os, gzip
from multiprocessing import Pool
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
VARS = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp", "gdppc_log",
        "urban", "tax", "agri_va", "emp_agri", "flfp", "life_exp", "u5mr",
        "gpi_sec", "gpi_ter", "fertility"]
CTRL = ["gdppc_log", "urban"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {}
for v in VARS:
    try:
        S[v] = {kk: vv for kk, vv in load(v).items() if kk[0] in REG}
    except FileNotFoundError:
        pass
VARS = [v for v in VARS if v in S]
print(f"{len(VARS)} variables, {len(VARS)*(len(VARS)-1)} ordered pairs", flush=True)


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def edge(args):
    x, y, trend = args
    ctrls = [c for c in CTRL if c not in (x, y)]
    rows = []
    for (i, t), v in S[y].items():
        if (i, t + 10) not in S[y] or (i, t) not in S[x]:
            continue
        if not all((i, t) in S[c] for c in ctrls):
            continue
        rows.append([i, t, S[y][(i, t + 10)] - v, v, S[x][(i, t)]] +
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
    se = float(np.sqrt(max(Vb[1, 1], 0)))
    return (x, y, trend, float(b[1]), se, len(yv), len(ui))


if __name__ == "__main__":
    jobs = [(x, y, t) for x in VARS for y in VARS if x != y for t in (False, True)]
    with Pool(28) as p:
        res = [r for r in p.map(edge, jobs, chunksize=4) if r]
    store = {}
    for x, y, t, b, se, n, nc in res:
        store[(x, y, t)] = (b, se, n, nc)

    pairs = [(x, y) for x in VARS for y in VARS if x != y]
    both = [(x, y) for x, y in pairs if (x, y, False) in store and (x, y, True) in store]
    print(f"\npairs estimable without trends: {sum(1 for p2 in pairs if (p2[0],p2[1],False) in store)}")
    print(f"pairs estimable with trends:    {sum(1 for p2 in pairs if (p2[0],p2[1],True) in store)}")
    print(f"pairs estimable both ways:      {len(both)}")

    def sig(k):
        b, se, n, nc = k
        return se > 0 and abs(b / se) > 1.96

    n_base = [p2 for p2 in both if sig(store[(p2[0], p2[1], False)])]
    n_trend = [p2 for p2 in both if sig(store[(p2[0], p2[1], True)])]
    survivors = [p2 for p2 in n_base
                 if sig(store[(p2[0], p2[1], True)])
                 and (store[(p2[0], p2[1], False)][0] > 0) == (store[(p2[0], p2[1], True)][0] > 0)]
    print(f"\nsignificant with country FE only:   {len(n_base)}")
    print(f"significant with country trends:    {len(n_trend)}")
    print(f"significant in BOTH, same sign:     {len(survivors)}")
    if n_base:
        print(f"  => {100*len(survivors)/len(n_base):.1f}% of FE edges survive trends")

    print("\n" + "=" * 84)
    print("EDGES THAT SURVIVE BOTH COUNTRY FE AND COUNTRY TRENDS")
    print("=" * 84)
    for x, y in sorted(survivors, key=lambda p2: -abs(store[(p2[0], p2[1], True)][0] /
                                                      store[(p2[0], p2[1], True)][1])):
        b1, s1, _, _ = store[(x, y, False)]
        b2, s2, n2, nc2 = store[(x, y, True)]
        print(f"  {x:12s} -> {y:12s}  FE {b1:+8.3f}  trends {b2:+8.3f} (±{s2:.3f})  n={n2}")
