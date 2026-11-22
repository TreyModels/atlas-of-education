#!/usr/bin/env python3
"""The lead-lag matrix, computed separately inside each grouping.

For every ordered pair (X, Y): does X predict the 10-yr change in Y, once Y's own
starting level is controlled?  Run twice -- between countries (pooled) and within
countries (country fixed effects).  A pair is 'robust' only if it holds both ways.
Direction is decided by whether the reverse edge fails.
"""
import json, os, gzip, itertools
from multiprocessing import Pool
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
VARS = ["fertility", "lsc", "sec", "ter", "gpi_ter", "gpi_sec", "u5mr",
        "gdppc_log", "urban", "flfp", "electricity", "wage_emp", "prm_cmp",
        "life_exp", "tax"]
SHORT = {"fertility": "births", "lsc": "lowsec", "sec": "upper sec", "ter": "highered",
         "gpi_ter": "F/M higher", "gpi_sec": "F/M sec", "u5mr": "child surv",
         "gdppc_log": "income", "urban": "cities", "flfp": "women work",
         "electricity": "electricity", "wage_emp": "paid jobs",
         "prm_cmp": "primary comp", "life_exp": "life exp", "tax": "tax"}


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in VARS}
F = S["fertility"]


def fit(y, x, own, iso, yr, fe):
    n = len(y)
    if n < 90:
        return None
    cols = [np.ones(n), x, own]
    if fe:
        ui = {v: k for k, v in enumerate(sorted(set(iso)))}
        gi = np.array([ui[v] for v in iso])
        for c in sorted(set(iso))[1:]:
            cols.append((gi == ui[c]).astype(float))
    for d in sorted({(v // 10) * 10 for v in yr})[1:]:
        cols.append(np.array([1.0 if (v // 10) * 10 == d else 0.0 for v in yr]))
    X = np.column_stack(cols)
    if X.shape[1] > n - 15 or X.shape[1] > 400:
        return None
    b = np.linalg.lstsq(X.T @ X, X.T @ y, rcond=None)[0]
    u = y - X @ b
    XtX = X.T @ X
    ui2 = {v: k for k, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui2[v] for v in iso])
    meat = np.zeros_like(XtX)
    for c in set(gi.tolist()):
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
    rows = []
    for (i, t), v in S[b].items():
        if i not in members or (i, t + 10) not in S[b] or (i, t) not in S[a]:
            continue
        if (i, t) not in S[b]:
            continue
        rows.append((i, t, S[b][(i, t + 10)] - S[b][(i, t)], S[a][(i, t)], S[b][(i, t)]))
    if len(rows) < 90 or len({r[0] for r in rows}) < 8:
        return None
    y = np.array([r[2] for r in rows]); x = np.array([r[3] for r in rows])
    own = np.array([r[4] for r in rows])
    iso = [r[0] for r in rows]; yr = [r[1] for r in rows]
    pooled = fit(y, x, own, iso, yr, False)
    fe = fit(y, x, own, iso, yr, True)
    if not pooled or not fe:
        return None
    same = np.sign(pooled[0]) == np.sign(fe[0]) and pooled[0] != 0
    robust = same and abs(pooled[0] / pooled[1]) > 1.96 and abs(fe[0] / fe[1]) > 1.96
    return (a, b, pooled[0], fe[0], robust, len(rows))


def task(t):
    title, gname, members, a, b = t
    return (title, gname, edge((a, b, set(members))))


def assemble(title, gname, members, rows):
    D = {(r[0], r[1]): r for r in rows if r}
    out = []
    for a, b in itertools.combinations(VARS, 2):
        ab = D.get((a, b)); ba = D.get((b, a))
        if not ab or not ba:
            continue
        if ab[4] and not ba[4]:
            out.append((a, b, ab[2], ab[3]))
        elif ba[4] and not ab[4]:
            out.append((b, a, ba[2], ba[3]))
        elif ab[4] and ba[4]:
            out.append((a, b, ab[2], ab[3]))
    return gname, len(members), len(D), out


# ---------- grouping definitions (same as before) ----------
def m(iso, key, a=1990, b=2020):
    xs = [S[key][(iso, y)] for y in range(a, b + 1) if (iso, y) in S[key]]
    return float(np.mean(xs)) if len(xs) >= 3 else np.nan


isos = sorted(i for i in REG if any((i, y) in F for y in range(1990, 2021)))
D = {}
for i in isos:
    onset = None
    for y in sorted(y for (j, y) in F if j == i):
        if F[(i, y)] < 5.0:
            onset = y
            break
    D[i] = dict(onset=onset, lsc=m(i, "lsc"), ter=m(i, "ter"), sec=m(i, "sec"),
                gdppc=m(i, "gdppc_log"), flfp=m(i, "flfp"), urban=m(i, "urban"),
                elec=m(i, "electricity"), tax=m(i, "tax"), gpi_sec=m(i, "gpi_sec"))


def g_onset(i):
    o = D[i]["onset"]
    if o is None: return "never yet"
    if o <= 1975: return "early (by 1975)"
    if o <= 1990: return "middle (1976-90)"
    if o <= 2005: return "late (1991-2005)"
    return "just starting (after 2005)"


def g_state(i):
    e, t = D[i]["elec"], D[i]["tax"]
    if not (np.isfinite(e) and np.isfinite(t)): return None
    s = (e - 78) / 25 + (t - 18) / 8
    return "thin state" if s < -0.6 else ("deep state" if s > 0.6 else "middling state")


def g_out(i):
    v = [D[i][k] for k in ("flfp", "urban", "gpi_sec")]
    if not all(np.isfinite(x) for x in v): return None
    s = (v[0] - 50) / 12 + (v[1] - 55) / 20 + (v[2] - 1.0) / 0.15
    return "few options" if s < -0.6 else ("many options" if s > 0.6 else "middling options")


def g_gate(i):
    t, s = D[i]["ter"], D[i]["sec"]
    if not (np.isfinite(t) and np.isfinite(s) and s > 0): return None
    g = t / s
    return "tight gate" if g < 0.28 else ("open gate" if g > 0.55 else "middling gate")


GROUPINGS = {"A onset cohort": g_onset, "C gate": g_gate,
             "D outside options": g_out, "E state reach": g_state}

if __name__ == "__main__":
    tasks = []
    groups_meta = []
    for title, fn in GROUPINGS.items():
        buckets = {}
        for i in isos:
            g = fn(i)
            if g:
                buckets.setdefault(g, []).append(i)
        for g, mem in sorted(buckets.items()):
            groups_meta.append((title, g, tuple(mem)))
            for a in VARS:
                for b in VARS:
                    if a != b:
                        tasks.append((title, g, tuple(mem), a, b))
    print("tasks:", len(tasks), flush=True)
    with Pool(48) as p:
        res = p.map(task, tasks, chunksize=32)
    store = {}
    for t, g, r in res:
        store.setdefault((t, g), []).append(r)
    for title in GROUPINGS:
        print("\n" + "=" * 84)
        print(title.upper())
        print("=" * 84)
        for (t, g, mem) in groups_meta:
            if t != title:
                continue
            rows = store.get((t, g), [])
            D2 = {(r[0], r[1]): r for r in rows if r}
            out = []
            for a, b in itertools.combinations(VARS, 2):
                ab = D2.get((a, b)); ba = D2.get((b, a))
                if not ab or not ba:
                    continue
                if ab[4] and not ba[4]:
                    out.append((a, b, ab[2], ab[3]))
                elif ba[4] and not ab[4]:
                    out.append((b, a, ba[2], ba[3]))
            fin = [e for e in out if e[1] == "fertility"]
            fout = [e for e in out if e[0] == "fertility"]
            print(f"\n  {g} — {len(mem)} countries, {len(D2)} pairs, {len(out)} one-way leads")
            print("     -> BIRTHS:  " + (", ".join(f"{SHORT[a]}({b1:+.2f})" for a, b, b1, b2 in
                  sorted(fin, key=lambda z: -abs(z[3]))[:5]) if fin else "(nothing)"))
            if fout:
                print("     BIRTHS ->  " + ", ".join(f"{SHORT[b]}({b2:+.2f})" for a, b, b1, b2 in
                      sorted(fout, key=lambda z: -abs(z[3]))[:5]))
