#!/usr/bin/env python3
"""The state-presence bundle: roads, electricity, hospitals, schools, cops.

World Bank availability, checked honestly:
  electricity  EG.ELC.ACCS.ZS   1960-2023, wide
  hospitals    SH.MED.BEDS.ZS   1960-2023, wide   (physicians and nurses too)
  cops         no WDI series. Approximated by the inverse homicide rate,
               which measures security, not police establishment.
  schools      no count series in WDI. Not measurable here.
  roads        IS.ROD.PAVE.ZS   1990-2010, 58 countries. Subsample only.

So the bundle tested is electricity + hospital beds + physicians + security,
with roads added on the subsample where they exist.
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT = ["lsc", "sec", "ter", "pov_215"]
CTRL = ["gdppc_log", "urban"]
CORE = ["electricity", "beds", "phys", "security"]
ALL = CORE + ["roads"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
LOADK = ["electricity", "beds", "phys", "roads", "nurses", "homicide"] + OUT + CTRL
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in LOADK}
S["security"] = {k: 100.0 - v for k, v in S["homicide"].items()}
for c in ("beds", "phys"):
    vals = list(S[c].values())
    p95 = np.percentile(vals, 99)
    S[c] = {k: min(v, p95) for k, v in S[c].items()}


def dm(a, g):
    s = np.bincount(g, weights=a); c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def pair_corr(comps):
    common = sorted(set.intersection(*[set(S[c]) for c in comps]))
    if len(common) < 50:
        return None
    iso = [k[0] for k in common]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    M = np.array([[S[c][k] for c in comps] for k in common], float)
    Mz = np.column_stack([dm(M[:, j], gi) for j in range(M.shape[1])])
    Mc = np.column_stack([np.array([M[gi == j, a].mean() for j in range(len(ui))])
                          for a in range(M.shape[1])])
    return common, M, Mz, Mc


print("=" * 84)
print("THE STATE-PRESENCE BUNDLE: does it cohere?")
print("=" * 84)
res = pair_corr(CORE)
common, M, Mz, Mc = res
print(f"{len(common)} country-years where all four are observed, "
      f"{len({k[0] for k in common})} countries")
print("\n                     " + "".join(f"{c[:9]:>10s}" for c in CORE))
for lab, MM in (("across countries", Mc), ("within countries", Mz)):
    print(f"  {lab}:")
    for a, c in enumerate(CORE):
        print(f"    {c[:10]:>10s}  " + "".join(f"{np.corrcoef(MM[:,a],MM[:,b])[0,1]:10.2f}"
                                               for b in range(len(CORE))))
Zc = (Mc - Mc.mean(0)) / Mc.std(0)
w, V = np.linalg.eigh(np.cov(Zc.T))
pc1 = V[:, -1] * (1 if V[:, -1].sum() > 0 else -1)
print(f"\n  PC1 loadings: " + ", ".join(f"{c}={pc1[j]:+.2f}" for j, c in enumerate(CORE)))
print(f"  variance explained: {w[-1]/w.sum()*100:.1f}%")


def fit(outcome, xmap, extra=()):
    rows = []
    for (i, t), v in S[outcome].items():
        if (i, t + 10) not in S[outcome] or (i, t) not in xmap:
            continue
        rec = [i, t, S[outcome][(i, t + 10)] - v, v, xmap[(i, t)]]
        ok = True
        for c in CTRL + list(extra):
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
    gi = np.array([ui[v] for v in iso]); gy = np.array([(r[1] // 10) * 10 for r in rows])
    y = np.array([r[2] for r in rows]); own = np.array([r[3] for r in rows])
    xx = np.array([r[4] for r in rows], float)
    cols = [xx, own] + [np.array([r[5 + j] for r in rows]) for j in range(len(CTRL) + len(extra))]
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
    return float(b[1]), float(np.sqrt(max(Vb[1, 1], 0))), len(rows), len(ui)


def zmap(d):
    v = np.array(list(d.values()))
    mu, sd = v.mean(), v.std()
    return {k: (x - mu) / sd for k, x in d.items()}


# time- varying bundle over whatever components are present
keyed = set().union(*[set(S[c]) for c in CORE])
BUNDLE = {}
for k in keyed:
    vs = [S[c][k] for c in CORE if k in S[c]]
    if len(vs) >= 3:
        BUNDLE[k] = float(np.mean(vs))
print(f"\n  time-varying bundle built for {len(BUNDLE)} country-years")

print("\n" + "=" * 86)
print("SCHOOLING AND POVERTY, BY THE STATE-PRESENCE BUNDLE AND ITS PARTS")
print("(per SD, within country; income and urbanisation controlled)")
print("=" * 86)
names = ["BUNDLE", "electricity", "hospital beds", "physicians", "security"]
maps = [BUNDLE] + [S[c] for c in CORE]
print(f"{'outcome':10s}" + "".join(f"{n:>13s}" for n in names))
for o in OUT:
    line = f"{o:10s}"
    for xm in maps:
        r = fit(o, zmap(xm))
        if r:
            line += f"{r[0]:+9.2f}{'*' if abs(r[0]/r[1]) > 1.96 else ' '}  "
        else:
            line += f"{'--':>13s}"
    print(line)

print("\n  roads added (subsample where the series exists, 1990-2010):")
for o in ["lsc", "sec"]:
    r = fit(o, zmap(BUNDLE), extra=("roads",))
    print(f"    {o:6s} bundle controlling for roads: "
          + (f"{r[0]:+.2f} (±{r[1]:.2f})  n={r[2]}, {r[3]} countries" if r else "too few"))
