#!/usr/bin/env python3
"""Five theory-motivated country groupings, each testing a different mechanism."""
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
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG}
     for k in ["fertility", "lsc", "sec", "ter", "gpi_ter", "gpi_sec",
               "u5mr", "gdppc_log", "urban", "flfp", "electricity", "tax"]}
F = S["fertility"]


def m(iso, key, a=1990, b=2020):
    xs = [S[key][(iso, y)] for y in range(a, b + 1) if (iso, y) in S[key]]
    return float(np.mean(xs)) if len(xs) >= 3 else np.nan


def z(v):
    v = np.array(v, float)
    s = np.nanstd(v)
    return (v - np.nanmean(v)) / (s if s > 0 else 1)


# ---------- build grouping variables ----------
isos = sorted(i for i in REG if any((i, y) in F for y in range(1990, 2021)))
D = {}
for iso in isos:
    onset = None
    ys = sorted(y for (i, y) in F if i == iso)
    for y in ys:
        if F[(iso, y)] < 5.0:
            onset = y
            break
    D[iso] = dict(
        onset=onset,
        lsc=m(iso, "lsc"), ter=m(iso, "ter"), sec=m(iso, "sec"),
        gdppc=m(iso, "gdppc_log"), u5mr=m(iso, "u5mr"), flfp=m(iso, "flfp"), urban=m(iso, "urban"),
        elec=m(iso, "electricity"), tax=m(iso, "tax"), gpi_sec=m(iso, "gpi_sec"),
    )

for i in isos:
    for k in ("resid", "gate", "out", "state"):
        D[i].setdefault(k, np.nan)

# A. onset cohort
def grp_onset(i):
    o = D[i]["onset"]
    if o is None: return "e) not yet below 5"
    if o <= 1960: return "a) began by 1960"
    if o <= 1975: return "b) 1961-75"
    if o <= 1990: return "c) 1976-90"
    if o <= 2005: return "d) 1991-2005"
    return "e) after 2005"

# B. over/under-schooled relative to income
ok = [i for i in isos if np.isfinite(D[i]["lsc"]) and np.isfinite(D[i]["gdppc"])]
Xg = np.column_stack([np.ones(len(ok)), np.array([D[i]["gdppc"] for i in ok])])
Yg = np.array([D[i]["lsc"] for i in ok])
coef = np.linalg.lstsq(Xg, Yg, rcond=None)[0]
resid = Yg - Xg @ coef
rq = np.percentile(resid, [33, 67])
for i, r in zip(ok, resid):
    D[i]["resid"] = r

def grp_resid(i):
    if "resid" not in D[i]: return None
    if D[i]["resid"] <= rq[0]: return "a) less schooling than income predicts"
    if D[i]["resid"] >= rq[1]: return "c) more schooling than income predicts"
    return "b) as predicted"

# C. gate tightness: tertiary per unit of secondary
for i in ok:
    t, s = D[i]["ter"], D[i]["sec"]
    D[i]["gate"] = t / s if (np.isfinite(t) and np.isfinite(s) and s > 0) else np.nan
gk = [i for i in isos if np.isfinite(D[i]["gate"])]
gq = np.percentile([D[i]["gate"] for i in gk], [33, 67])
def grp_gate(i):
    g = D[i]["gate"]
    if not np.isfinite(g): return None
    if g <= gq[0]: return "a) tight gate (few reach tertiary)"
    if g >= gq[1]: return "c) open gate"
    return "b) middling gate"

# D. women's outside option
ob = [i for i in isos if all(np.isfinite(D[i][k]) for k in ("flfp", "urban", "gpi_sec"))]
score = z([D[i]["flfp"] for i in ob]) + z([D[i]["urban"] for i in ob]) + z([D[i]["gpi_sec"] for i in ob])
oq = np.percentile(score, [33, 67])
for i, v in zip(ob, score):
    D[i]["out"] = v
def grp_out(i):
    if "out" not in D[i]: return None
    if D[i]["out"] <= oq[0]: return "a) few outside options for women"
    if D[i]["out"] >= oq[1]: return "c) many outside options"
    return "b) middling"

# E. state reach
sc = [i for i in isos if all(np.isfinite(D[i][k]) for k in ("elec", "tax"))]
sco = z([D[i]["elec"] for i in sc]) + z([D[i]["tax"] for i in sc])
sq = np.percentile(sco, [33, 67])
for i, v in zip(sc, sco):
    D[i]["state"] = v
def grp_state(i):
    if "state" not in D[i]: return None
    if D[i]["state"] <= sq[0]: return "a) thin state reach"
    if D[i]["state"] >= sq[1]: return "c) deep state reach"
    return "b) middling reach"

GROUPINGS = [("A. WHEN THE TRANSITION BEGAN (diffusion)", grp_onset),
             ("B. SCHOOLING RELATIVE TO INCOME (pent-up pressure)", grp_resid),
             ("C. GATE TIGHTNESS (how few reach tertiary)", grp_gate),
             ("D. WOMEN'S OUTSIDE OPTIONS (bargaining)", grp_out),
             ("E. STATE REACH (infrastructural power)", grp_state)]


def fit(subset):
    rows = [(i, t, F[(i, t + 10)] - v, S["lsc"][(i, t)])
            for (i, t), v in F.items()
            if i in subset and (i, t + 10) in F and (i, t) in S["lsc"]]
    if len(rows) < 60:
        return None
    iso2 = [r[0] for r in rows]
    uq = {c: n for n, c in enumerate(sorted(set(iso2)))}
    g = np.array([uq[c] for c in iso2])
    y = np.array([r[2] for r in rows]); x = np.array([r[3] for r in rows])
    my = y - (np.bincount(g, weights=y) / np.bincount(g))[g]
    mx = x - (np.bincount(g, weights=x) / np.bincount(g))[g]
    if mx @ mx == 0:
        return None
    b = (mx @ my) / (mx @ mx)
    res = my - b * mx
    meat = 0.0
    for c in set(g.tolist()):
        mm = g == c
        meat += float((mx[mm] @ res[mm]) ** 2)
    se = np.sqrt(meat) / (mx @ mx)
    return b, se, len(rows), len(uq)


for title, fn in GROUPINGS:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    buckets = {}
    for i in isos:
        gname = fn(i)
        if gname:
            buckets.setdefault(gname, []).append(i)
    for gname in sorted(buckets):
        mem = buckets[gname]
        print(f"\n  {gname}  — {len(mem)} countries")
        prof = []
        for k, lab in (("lsc", "basic schooling"), ("ter", "higher ed"), ("u5mr", "child deaths"),
                       ("gdppc", "income"), ("flfp", "women working"), ("elec", "electricity")):
            vals = [D[i][k] for i in mem if np.isfinite(D[i][k])]
            if vals:
                prof.append(f"{lab} {np.mean(vals):.0f}")
        print("     " + " | ".join(prof))
        reg = {}
        for i in mem:
            reg[REG[i]] = reg.get(REG[i], 0) + 1
        top = sorted(reg.items(), key=lambda kv: -kv[1])[:3]
        print("     mainly: " + ", ".join(f"{a} ({b})" for a, b in top))
        r = fit(set(mem))
        if r:
            print(f"     schooling->births: {r[0]:+.4f} (±{r[1]:.4f}) "
                  f"{'**' if abs(r[0]/r[1]) > 1.96 else ''}  n={r[2]}, {r[3]} countries")
        else:
            print("     too few observations for a separate estimate")
