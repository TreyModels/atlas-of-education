"""Pre-registered test (ii): is there a regime change near the universalisation threshold?

Two tests on the ILOSTAT occupation data (the only category-count system available):
  (a) pooled curvature: log E[S_n] = a + b log n + c (log n)^2 with country fixed effects,
      clustered SE by country. Negative c = diminishing returns (saturating regime).
  (b) threshold split: per-country rarefaction exponent b_i, split by the country's female
      secondary completion level (universalisation proxy: <50 / 50-80 / >80 %), Welch test.
"""
import csv, json, math, os
import numpy as np
from scipy import stats

WD = "/root/work/scaling"; OUT = os.path.join(WD, "results")
DATA = "/root/work/data"; META = json.load(open(os.path.join(DATA, "meta.json")))


def panel(name):
    d = {}
    for r in json.load(open(os.path.join(DATA, name + ".json"))):
        try:
            d[(r[0], int(r[1]))] = float(r[2])
        except Exception:
            pass
    return d


FERT, SEC, GPI = panel("fertility"), panel("sec"), panel("gpi_sec")
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


def country_curve(ni):
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


def female_att(iso, years=(2015, 2014, 2013, 2012, 2011, 2010, 2016, 2017, 2018, 2019, 2020)):
    for y in years:
        s, g = SEC.get((iso, y)), GPI.get((iso, y))
        if s and g and 0.2 <= g <= 2.0:
            return s * 2 * g / (1 + g)
    return None


curves = {}
for (a, y), d in latest.items():
    m = META.get(a)
    if not m or m.get("region") == "Aggregates" or len(d) < 8:
        continue
    ni = np.array([d.get(k, 0.0) for k in range(10)])
    if ni.sum() < 100:
        continue
    curves[a] = country_curve(ni)

# (a) pooled curvature with country fixed effects (demean log n and its square within country)
xs, ys, x2s, gs = [], [], [], []
for a, (x, y) in curves.items():
    xs.append(x); ys.append(y); x2s.append(x ** 2); gs.append(np.full(len(x), a))
x = np.concatenate(xs); y = np.concatenate(ys); x2 = np.concatenate(x2s); g = np.concatenate(gs)
dm = lambda v: v - np.array([np.mean(v[g == c]) for c in g])
dx, dx2, dy = dm(x), dm(x2), dm(y)
X = np.column_stack([dx, dx2])
beta = np.linalg.lstsq(X, dy, rcond=None)[0]
resid = dy - X @ beta
lib = np.unique(g)
inv = np.linalg.inv(X.T @ X)
meat = sum(np.outer(X[g == c].T @ resid[g == c], X[g == c].T @ resid[g == c]) for c in lib)
cov = inv @ meat @ inv
se = np.sqrt(np.diag(cov))
# (b) per-country exponent and threshold split
bi, att = [], []
for a, (xx, yy) in curves.items():
    if len(xx) < 4:
        continue
    b = float(np.sum((xx - xx.mean()) * (yy - yy.mean())) / np.sum((xx - xx.mean()) ** 2))
    fa = female_att(a)
    if fa is not None:
        bi.append(b); att.append(fa)
bi = np.array(bi); att = np.array(att)
groups = {"<50%": bi[att < 50], "50-80%": bi[(att >= 50) & (att <= 80)], ">80%": bi[att > 80]}
summary = {k: dict(n=int(len(v)), mean=float(np.mean(v)), sd=float(np.std(v, ddof=1))) for k, v in groups.items() if len(v) > 2}
low, high = groups["<50%"], groups[">80%"]
welch = stats.ttest_ind(low, high, equal_var=False) if len(low) > 2 and len(high) > 2 else None
out = dict(
    curvature=dict(squared_coef=float(beta[1]), squared_se=float(se[1]),
                   linear_coef=float(beta[0]), linear_se=float(se[0]),
                   npoints=int(len(x)), ncountries=int(len(lib)),
                   verdict="negative curvature (saturating)" if beta[1] < -1.96 * se[1] else
                           "no significant curvature"),
    threshold_split=dict(groups=summary,
                         welch=dict(t=float(welch.statistic), p=float(welch.pvalue),
                                    df=float(welch.df)) if welch is not None else None,
                         verdict="exponents differ by universalisation stage" if (welch is not None and welch.pvalue < 0.05)
                                 else "no significant difference by stage"),
    female_attainment_proxy="gross secondary completion x 2*gpi/(1+gpi), latest available year",
)
json.dump(out, open(os.path.join(OUT, "regime_break.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
