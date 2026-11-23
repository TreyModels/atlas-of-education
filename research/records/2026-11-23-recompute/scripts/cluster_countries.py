import os
#!/usr/bin/env python3
"""Group countries from the data. Missing numbers are filled, not dropped."""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
rng = np.random.default_rng(3)

FEAT = ["lsc", "sec", "ter", "gpi_ter", "u5mr", "gdppc_log", "urban", "flfp", "electricity"]
CHG = ["lsc", "ter", "u5mr", "gdppc_log"]


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in set(FEAT + CHG + ["fertility"])}


def mean_level(f, iso):
    xs = [S[f][(iso, y)] for y in range(1985, 2021) if (iso, y) in S[f]]
    return float(np.mean(xs)) if len(xs) >= 3 else np.nan


def near(f, iso, y, tol=6):
    for d in range(tol + 1):
        for yy in (y - d, y + d):
            if (iso, yy) in S[f]:
                return S[f][(iso, yy)]
    return np.nan


isos = sorted(i for i in REG if any((i, y) in S["lsc"] for y in range(1990, 2020)))
X, keep = [], []
for iso in isos:
    row = [mean_level(f, iso) for f in FEAT]
    row += [near(f, iso, 2020) - near(f, iso, 1990) for f in CHG]
    X.append(row)
    keep.append(iso)
X = np.array(X, float)
names = FEAT + [f"{f} change" for f in CHG]

# fill missing with the column median
for j in range(X.shape[1]):
    col = X[:, j]
    bad = ~np.isfinite(col)
    if bad.all():
        X[:, j] = 0.0
    else:
        col[bad] = np.nanmedian(col)
print(f"{len(keep)} countries, {X.shape[1]} features, "
      f"{int((~np.isfinite(np.array(X))).sum())} blanks filled")

Z = (X - X.mean(0)) / (X.std(0) + 1e-9)


def kmeans(Z, k, restarts=30):
    best = None
    for _ in range(restarts):
        C = Z[rng.choice(len(Z), k, replace=False)]
        for _ in range(200):
            d = ((Z[:, None, :] - C[None, :, :]) ** 2).sum(2)
            lab = d.argmin(1)
            C2 = np.array([Z[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
            if np.allclose(C2, C):
                break
            C = C2
        inert = ((Z - C[lab]) ** 2).sum()
        if best is None or inert < best[0]:
            best = (inert, lab.copy(), C.copy())
    return best


def silhouette(Z, lab):
    d = np.sqrt(((Z[:, None, :] - Z[None, :, :]) ** 2).sum(2))
    out = []
    for i in range(len(Z)):
        same = lab == lab[i]
        same[i] = False
        if same.sum() == 0:
            out.append(0.0)
            continue
        a = d[i, same].mean()
        b = min(d[i, lab == j].mean() for j in set(lab.tolist()) if j != lab[i])
        out.append((b - a) / max(a, b))
    return float(np.mean(out))


print("\nchoosing how many groups")
sc = {}
for k in range(3, 8):
    _, lab, _ = kmeans(Z, k)
    sc[k] = silhouette(Z, lab)
    print(f"  {k} groups: separation {sc[k]:.3f}")
K = max(sc, key=sc.get)
_, lab, C = kmeans(Z, K, restarts=150)
print(f"chosen: {K} groups (separation {sc[K]:.3f})")

order = sorted(range(K), key=lambda j: -X[lab == j][:, FEAT.index("ter")].mean())
print("\n" + "=" * 80)
print("THE GROUPS")
print("=" * 80)
for rank, j in enumerate(order, 1):
    m = lab == j
    print(f"\nGROUP {rank} — {m.sum()} countries")
    for i, nm in enumerate(names):
        print(f"   {nm:16s} {X[m, i].mean():9.1f}   (all countries {X[:, i].mean():9.1f})")
    print("   " + ", ".join(sorted(np.array(keep)[m])))

print("\n" + "=" * 80)
print("HOW THESE CUT ACROSS WORLD BANK REGIONS")
print("=" * 80)
print(f"{'':40s}" + "".join(f"{'G'+str(r+1):>6}" for r in range(K)))
for r in sorted({REG[i] for i in keep}):
    ids = [n for n, i in enumerate(keep) if REG[i] == r]
    if not ids:
        continue
    print(f"{r[:38]:40s}" + "".join(f"{sum(1 for n in ids if lab[n]==j):6d}" for j in order))

print("\n" + "=" * 80)
print("SCHOOLING -> FERTILITY, INSIDE EACH GROUP")
print("=" * 80)
F = S["fertility"]
for rank, j in enumerate(order, 1):
    ids = set(np.array(keep)[lab == j])
    rows = [(i, t, F[(i, t + 10)] - v, S["lsc"][(i, t)])
            for (i, t), v in F.items()
            if i in ids and (i, t + 10) in F and (i, t) in S["lsc"]]
    if len(rows) < 40:
        print(f"  GROUP {rank}: only {len(rows)} observations")
        continue
    iso2 = [r[0] for r in rows]
    uq = {c: n for n, c in enumerate(sorted(set(iso2)))}
    g = np.array([uq[c] for c in iso2])
    y = np.array([r[2] for r in rows]); x = np.array([r[3] for r in rows])
    my = y - (np.bincount(g, weights=y) / np.bincount(g))[g]
    mx = x - (np.bincount(g, weights=x) / np.bincount(g))[g]
    b = (mx @ my) / (mx @ mx)
    res = my - b * mx
    meat = 0.0
    for c in set(g.tolist()):
        m = g == c
        meat += float((mx[m] @ res[m]) ** 2)
    se = np.sqrt(meat) / (mx @ mx)
    print(f"  GROUP {rank}: n={len(rows):5d}, {len(uq):3d} countries   "
          f"estimate {b:+.3f} (±{se:.3f}) {'**' if abs(b/se) > 1.96 else ''}")
