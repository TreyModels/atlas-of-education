#!/usr/bin/env python3
"""Step 4: validation.  usage: validate.py TARGET
V1  mask a random 20% of the observed values of the series;
V2  for countries whose series starts by 1972 and has >=10 values after 1995, mask every value before 1995
    (an early-decades backcast test, horizons up to ~25 years).
Predict the masked values from the rest; report error and 90% / 50% interval coverage by horizon, choose the
spread calibration factor kappa, and the longest horizon at which the series is still trustworthy."""
import sys, json
import numpy as np
from common import *
from implib import *

TARGET = sys.argv[1]
M = 40
KAPPAS = [1.0, 1.5, 2.0, 3.0, 4.0]
BINS = [(1, 1), (2, 3), (4, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 99)]
aux = dict(np.load(f"{OUT}/aux.npz"))
X, ng, names = build_cells(aux)
y = to_panel(load(TARGET))
lo = float(np.nanmin(y)); hi = float(np.nanpercentile(y, 99.9)) if TARGET.startswith("gpi") else float(np.nanmax(y))
y = np.clip(y, lo, hi)
rng = np.random.default_rng(20261123)
sd_obs = float(np.nanstd(y))


def run(ymask, cells, tag):
    mod = Model(TARGET, ymask, X, ng, lo, hi)
    h = horizon(ymask)
    d = {k: mod.draw(M, k, rng) for k in KAPPAS}
    rows = []
    for (i, j) in cells:
        if i not in mod.gp:
            continue
        rows.append((i, j, y[i, j], h[i, j], tag, [d[k][:, i, j] for k in KAPPAS]))
    return rows, mod


# V1
cnt = np.isfinite(y).sum(1)
cells = [(i, j) for i in range(NC) if cnt[i] >= 5 for j in np.flatnonzero(np.isfinite(y[i]))]
sel = rng.choice(len(cells), int(0.2 * len(cells)), replace=False)
c1 = [cells[k] for k in sel]
y1 = y.copy()
for i, j in c1:
    y1[i, j] = np.nan
r1, m1 = run(y1, c1, "V1")
# V2
first = np.array([np.flatnonzero(np.isfinite(y[i]))[0] if np.isfinite(y[i]).any() else 999 for i in range(NC)])
late = np.array([np.isfinite(y[i, 45:]).sum() for i in range(NC)])
cs = [i for i in range(NC) if first[i] + 1950 <= 1972 and late[i] >= 10]
y2 = y.copy(); c2 = []
for i in cs:
    for j in np.flatnonzero(np.isfinite(y[i, :45])):
        y2[i, j] = np.nan; c2.append((i, j))
r2, m2 = run(y2, c2, "V2") if c2 else ([], None)
rows = r1 + r2
truth = np.array([r[2] for r in rows]); hz = np.array([r[3] for r in rows]); tag = np.array([r[4] for r in rows])
yr = np.array([1950 + r[1] for r in rows])
D = np.array([np.array(r[5]) for r in rows])  # (n, nk, M)


def metrics(sel, k):
    t = truth[sel]; d = D[sel, k, :]
    mean = d.mean(1)
    l90, h90 = np.percentile(d, [5, 95], axis=1); l50, h50 = np.percentile(d, [25, 75], axis=1)
    e = mean - t
    return dict(n=int(sel.sum()), rmse=float(np.sqrt((e ** 2).mean())), mae=float(np.abs(e).mean()), bias=float(e.mean()),
                nrmse=float(np.sqrt((e ** 2).mean()) / sd_obs), cov90=float(((t >= l90) & (t <= h90)).mean()),
                cov50=float(((t >= l50) & (t <= h50)).mean()))


allsel = np.ones(len(rows), bool)
kap = None
for k, kv in enumerate(KAPPAS):
    if metrics(allsel, k)["cov90"] >= 0.88:
        kap = k; break
if kap is None:
    kap = len(KAPPAS) - 1
res = dict(target=TARGET, sd_obs=sd_obs, lo=lo, hi=hi, kappa=KAPPAS[kap], lam=m1.lam, tau=m1.tau,
           by_kappa={str(kv): metrics(allsel, k) for k, kv in enumerate(KAPPAS)}, bins={}, n_v1=len(r1), n_v2=len(r2),
           v2_countries=len(cs))
for name, s in (("V1", tag == "V1"), ("V2", tag == "V2"), ("all", allsel)):
    res["bins"][name] = {}
    for a, b in BINS:
        sel = s & (hz >= a) & (hz <= b)
        if sel.sum() >= 5:
            res["bins"][name][f"{a}-{b}"] = metrics(sel, kap)
    if s.sum() >= 5:
        res["bins"][name]["total"] = metrics(s, kap)
# cutoff: largest horizon such that every bin up to it (pooled V1+V2) has nrmse<=0.35 and 90% coverage >=0.80
cut = 0
for a, b in BINS:
    mt = res["bins"]["all"].get(f"{a}-{b}")
    if mt is None or mt["n"] < 30:
        if mt is None and cut >= a - 1 and b >= 99:
            pass
        break
    if mt["nrmse"] <= 0.35 and mt["cov90"] >= 0.80:
        cut = b
    else:
        break
res["max_horizon_years"] = int(min(cut, 25)) if cut < 99 else 25
json.dump(res, open(f"{OUT}/validation_{TARGET}.json", "w"), indent=1)
print(TARGET, "kappa", KAPPAS[kap], "max horizon", res["max_horizon_years"], "n", len(rows))
for name in ("V1", "V2"):
    for kk, v in res["bins"][name].items():
        print(f"  {name} {kk:6s} n={v['n']:5d} rmse={v['rmse']:.3f} nrmse={v['nrmse']:.3f} bias={v['bias']:+.3f} cov90={v['cov90']:.2f} cov50={v['cov50']:.2f}")
