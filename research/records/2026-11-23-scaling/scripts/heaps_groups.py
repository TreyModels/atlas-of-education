"""Compute-ready extension: rarefied Heaps exponents by institutional group, with cluster bootstrap.

The theory's theta/gamma (kin-network inhibition, specialisation) are model primitives, NOT measured
variables in our data. We therefore cannot test "low-theta vs high-theta" directly. The closest
observable stratifiers are the country's income group and region (institutional context); they are
reported explicitly as PROXIES, not as theta/gamma. Everything here is a diversity-size fit with
cluster resampling on the countries.
"""
import csv, json, math, os
import numpy as np
from scipy import stats

WD = "/root/work/scaling"; OUT = os.path.join(WD, "results")
DATA = "/root/work/data"; META = json.load(open(os.path.join(DATA, "meta.json")))
rng = np.random.default_rng(20261123)


def panel(name):
    d = {}
    for r in json.load(open(os.path.join(DATA, name + ".json"))):
        try:
            d[(r[0], int(r[1]))] = float(r[2])
        except Exception:
            pass
    return d


SEC, GPI = panel("sec"), panel("gpi_sec")
rows = []
with open(os.path.join(WD, "ilo_test.csv"), encoding="utf-8-sig") as fh:
    for r in csv.DictReader(fh):
        c = r["classif1"]
        if c.startswith("OCU_ISCO08_") and c.split("_")[-1].isdigit() and c != "OCU_ISCO08_TOTAL":
            try:
                v = float(r["obs_value"])
            except Exception:
                continue
            if math.isfinite(v) and v > 0:
                rows.append((r["ref_area"], int(r["time"]), int(c.split("_")[-1]), v))
latest = {}
for a, y, cat, v in rows:
    latest.setdefault((a, y), {})[cat] = v


def curve(ni):
    N = ni.sum(); xs, ys = [], []
    for u in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3):
        n = max(1.0, u * N); es = 0.0
        for x in ni:
            if x <= 0:
                continue
            if n > N - x:
                es += 1.0; continue
            lg = math.lgamma
            lp = lg(N - x + 1) - lg(N - x - n + 1) - lg(N + 1) + lg(N - n + 1)
            es += 1.0 - math.exp(lp)
        xs.append(math.log(n)); ys.append(math.log(max(es, 1e-9)))
    return np.array(xs), np.array(ys)


curves = {}
for (a, y), d in latest.items():
    m = META.get(a)
    if not m or m.get("region") == "Aggregates" or len(d) < 8:
        continue
    ni = np.array([d.get(k, 0.0) for k in range(10)])
    if ni.sum() < 100:
        continue
    x, yy = curve(ni)
    if np.var(x) > 0:
        b_i = float(np.sum((x - x.mean()) * (yy - yy.mean())) / np.sum((x - x.mean()) ** 2))
    else:
        continue
    curves[a] = dict(x=x, y=yy, b=b_i, income=m.get("income", "?"), region=m.get("region", "?"))


def pooled_b(keys):
    xs = np.concatenate([curves[k]["x"] for k in keys])
    ys = np.concatenate([curves[k]["y"] for k in keys])
    gs = np.concatenate([np.full(len(curves[k]["x"]), i) for i, k in enumerate(keys)])
    dx = xs - np.array([xs[gs == i].mean() for i in gs])
    dy = ys - np.array([ys[gs == i].mean() for i in gs])
    return float(np.sum(dx * dy) / np.sum(dx ** 2))


def pooled_curv(keys):
    xs = np.concatenate([curves[k]["x"] for k in keys])
    ys = np.concatenate([curves[k]["y"] for k in keys])
    gs = np.concatenate([np.full(len(curves[k]["x"]), i) for i, k in enumerate(keys)])
    dm = lambda v: v - np.array([v[gs == i].mean() for i in gs])
    dx, dy = dm(xs), dm(ys)
    X = np.column_stack([dx, dx ** 2])
    beta = np.linalg.lstsq(X, dy, rcond=None)[0]
    resid = dy - X @ beta
    inv = np.linalg.inv(X.T @ X)
    meat = sum(np.outer(X[gs == i].T @ resid[gs == i], X[gs == i].T @ resid[gs == i])
               for i in sorted(set(gs)))
    cov = inv @ meat @ inv
    return beta, np.sqrt(np.diag(cov))


keys = sorted(curves)
b_all = pooled_b(keys)
boot = []
for _ in range(1000):
    sample = rng.choice(keys, size=len(keys), replace=True)
    try:
        boot.append(pooled_b(list(sample)))
    except Exception:
        pass
boot = np.array(boot)
out = dict(note="theta/gamma are NOT measured; groups below are institutional PROXIES (income group, "
                "region), not theta/gamma levels",
           method="rarefied expected-distinct-categories curves from ILOSTAT ISCO-08 major groups; "
                  "pooled exponent = country-demeaned log-log slope; cluster bootstrap over countries",
           overall=dict(exponent=b_all, bootstrap_se=float(np.std(boot, ddof=1)),
                        ci95=[float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
                        ncountries=len(keys), npoints=int(sum(len(curves[k]["x"]) for k in keys))),
           groups={})
# curvature by group
for gname, field in (("income", "income"), ("region", "region")):
    out["groups"][gname] = {}
    vals = sorted(set(curves[k][field] for k in keys))
    for v in vals:
        ks = [k for k in keys if curves[k][field] == v]
        if len(ks) < 5:
            continue
        beta, se = pooled_curv(ks)
        boot_v = []
        for _ in range(400):
            smp = rng.choice(ks, size=len(ks), replace=True)
            try:
                boot_v.append(pooled_curv(list(smp))[0][0])
            except Exception:
                pass
        boots = np.array([curves[k]["b"] for k in ks])
        out["groups"][gname][v] = dict(ncountries=len(ks),
                                       exponent=pooled_b(ks),
                                       curvature=float(beta[1]), curvature_se=float(se[1]),
                                       curvature_boot_se=float(np.std(boot_v, ddof=1)) if boot_v else None,
                                       mean_country_exponent=float(np.mean(boots)),
                                       sd_country_exponent=float(np.std(boots, ddof=1)))
# heterogeneity tests on per-country exponents
def grp(field):
    return {v: np.array([curves[k]["b"] for k in keys if curves[k][field] == v])
            for v in set(curves[k][field] for k in keys)}


inc = grp("income"); reg = grp("region")
inc = {k: v for k, v in inc.items() if len(v) >= 5}
reg = {k: v for k, v in reg.items() if len(v) >= 5}
kw_inc = stats.kruskal(*inc.values()) if len(inc) > 1 else None
kw_reg = stats.kruskal(*reg.values()) if len(reg) > 1 else None
hi = inc.get("High income"); lo = inc.get("Low income")
welch = stats.ttest_ind(hi, lo, equal_var=False) if hi is not None and lo is not None and len(hi) > 2 and len(lo) > 2 else None
# bootstrap difference high vs low income
diffs = []
if hi is not None and lo is not None:
    for _ in range(1000):
        diffs.append(float(np.mean(rng.choice(hi, len(hi))) - np.mean(rng.choice(lo, len(lo)))))
    diffs = np.array(diffs)
out["heterogeneity"] = dict(
    income_kruskal=dict(H=float(kw_inc.statistic), p=float(kw_inc.pvalue)) if kw_inc else None,
    region_kruskal=dict(H=float(kw_reg.statistic), p=float(kw_reg.pvalue)) if kw_reg else None,
    high_vs_low_income=dict(t=float(welch.statistic), p=float(welch.pvalue),
                            diff=float(np.mean(hi) - np.mean(lo)),
                            diff_ci95=[float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))]) if welch else None,
    verdict="exponents differ across institutional groups" if (kw_inc and kw_inc.pvalue < 0.05)
            else "no significant heterogeneity across institutional groups",
)
json.dump(out, open(os.path.join(OUT, "heaps_groups.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
