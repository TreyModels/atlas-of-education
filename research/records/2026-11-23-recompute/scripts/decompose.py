import os
#!/usr/bin/env python3
"""Which of electricity / cities / paid jobs actually absorbs the higher-ed edge?

If they are collinear, 'the one that wins' depends on entry order. So: enter them
in every order and report the spread. Then test the direction between each and
higher education.
"""
import json, os, gzip, itertools
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
K = ["ter", "sec", "lsc", "prm_cmp", "electricity", "urban", "wage_emp", "gdppc_log"]
V = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in K}


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def reg(outcome, ctrls, focus="ter"):
    rows = []
    for (i, t), v in V[outcome].items():
        if (i, t + 10) not in V[outcome] or (i, t) not in V[focus]:
            continue
        r = [i, t, V[outcome][(i, t + 10)] - v, V[focus][(i, t)], v]
        ok = True
        for c in ctrls:
            x = V[c].get((i, t))
            if x is None:
                ok = False
                break
            r.append(x)
        if ok:
            rows.append(r)
    if len(rows) < 100:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso]); gy = np.array([(r[1] // 10) * 10 for r in rows])
    y = np.array([r[2] for r in rows])
    X = np.column_stack([[r[3] for r in rows], [r[4] for r in rows]]
                        + [[r[5 + j] for r in rows] for j in range(len(ctrls))])
    X = np.column_stack([np.ones(len(y)), X])
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
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(rows), len(ui)


print("=" * 76)
print("1. HOW CORRELATED ARE THE THREE? (country means, 1990-2020)")
print("=" * 76)
isos = sorted({i for (i, t) in V["ter"]})


def cm(k):
    d = {}
    for i in isos:
        xs = [V[k][(i, y)] for y in range(1990, 2021) if (i, y) in V[k]]
        if len(xs) >= 4:
            d[i] = np.mean(xs)
    return d


E, U, W = cm("electricity"), cm("urban"), cm("wage_emp")
common = sorted(set(E) & set(U) & set(W))
a, b, c = (np.array([E[i] for i in common]), np.array([U[i] for i in common]),
           np.array([W[i] for i in common]))
print(f"  n = {len(common)} countries")
print(f"  electricity vs cities   r = {np.corrcoef(a, b)[0,1]:+.2f}")
print(f"  electricity vs paid jobs r = {np.corrcoef(a, c)[0,1]:+.2f}")
print(f"  cities vs paid jobs      r = {np.corrcoef(b, c)[0,1]:+.2f}")

print()
print("=" * 76)
print("2. ENTER THEM IN EVERY ORDER — does the winner change?")
print("   (upper-secondary completion as the outcome)")
print("=" * 76)
base = reg("sec", [])[0]
print(f"  higher-ed effect with NO controls: {base:+.3f}")
trio = ["electricity", "urban", "wage_emp"]
for k in (1, 2, 3):
    for combo in itertools.combinations(trio, k):
        r = reg("sec", list(combo))
        if r:
            print(f"  + {', '.join(combo):34s} {r[0]:+.3f}  (n={r[2]})")
print()
print("  every ordering, final value after all three:")
vals = []
for perm in itertools.permutations(trio):
    seq = []
    for j in range(1, 4):
        r = reg("sec", list(perm[:j]))
        if r:
            seq.append(r[0])
    if seq:
        vals.append(seq[-1])
print(f"    always lands between {min(vals):+.3f} and {max(vals):+.3f}  (mean {np.mean(vals):+.3f})")

print()
print("=" * 76)
print("3. WHICH DIRECTION? each variable against higher education")
print("=" * 76)
for v in ["electricity", "urban", "wage_emp", "gdppc_log"]:
    f = reg("ter", [], focus=v)     # v -> change in higher ed
    r = reg(v, [], focus="ter")     # higher ed -> change in v
    if f and r:
        print(f"  {v:12s} -> higher ed: {f[0]:+.3f} (±{f[1]:.3f})   "
              f"higher ed -> {v}: {r[0]:+.3f} (±{r[1]:.3f})")
