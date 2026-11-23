"""Zipf / rank-size test on the GeoNames city list (pre-registered test; data integrity verified).

Data: /root/work/datahunt/raw/cities15000.txt (GeoNames dump, 34,248 rows, unzip -t OK).
Filter: feature class P, codes PPL/PPLA*/PPLC/PPLF/PPLG/PPLS (exclude section-of-place PPLX and
abandoned PPLQ), population > 0. A "country" needs >= 50 such cities.
Test: OLS log10(rank) = a - zeta log10(pop); zeta then compared with 1.
Caveats pre-registered: GeoNames is crowdsourced and lists city proper/localities, not UN urban
agglomerations; ranks are within country; boundary/definition noise is material.
"""
import json, math, os, sys
import numpy as np
import statsmodels.api as sm

RAW = "/root/work/datahunt/raw/cities15000.txt"
OUT = "/root/work/datahunt/results"; os.makedirs(OUT, exist_ok=True)
KEEP = {"PPL", "PPLC", "PPLA", "PPLA2", "PPLA3", "PPLA4", "PPLA5", "PPLF", "PPLG", "PPLS"}
cities = {}
nrows = 0
with open(RAW, encoding="utf-8") as fh:
    for line in fh:
        nrows += 1
        p = line.rstrip("\n").split("\t")
        if len(p) < 15:
            continue
        if not (p[6] == "P" and p[7] in KEEP):
            continue
        try:
            pop = int(p[11])
        except Exception:
            continue
        if pop <= 0:
            continue
        cities.setdefault(p[8], []).append(pop)
rows = []
for cc, pops in cities.items():
    if len(pops) < 50:
        continue
    pops = np.sort(np.array(pops, float))[::-1]
    rank = np.arange(1, len(pops) + 1)
    m = sm.OLS(np.log10(rank), sm.add_constant(np.log10(pops))).fit()
    rows.append(dict(country=cc, ncities=len(pops), zeta=-float(m.params[1]),
                     se=float(m.bse[1]), r2=float(m.rsquared),
                     maxpop=int(pops[0]), minpop=int(pops[-1])))
z = np.array([r["zeta"] for r in rows])
se = np.array([r["se"] for r in rows])
# pooled regression with country fixed effects, cluster SE by country
xs, ys, gs = [], [], []
for cc, pops in cities.items():
    if len(pops) < 50:
        continue
    pops = np.sort(np.array(pops, float))[::-1]
    xs.append(np.log10(pops)); ys.append(np.log10(np.arange(1, len(pops) + 1)))
    gs.append(np.full(len(pops), cc))
x = np.concatenate(xs); y = np.concatenate(ys); g = np.concatenate(gs)
dm = lambda v: v - np.array([np.mean(v[g == c]) for c in g])
dx, dy = dm(x), dm(y)
beta = float(np.sum(dx * dy) / np.sum(dx ** 2))
resid = dy - beta * dx
lib = np.unique(g)
meat = sum((dx[g == c] * resid[g == c]).sum() ** 2 for c in lib)
se_pooled = math.sqrt(meat) / np.sum(dx ** 2)
# bootstrap over countries (cluster)
rng = np.random.default_rng(7)
boot = []
for _ in range(1000):
    pick = rng.choice(lib, size=len(lib), replace=True)
    bb_x, bb_y = [], []
    for i, c in enumerate(pick):
        m = g == c
        bb_x.append(dx[m]); bb_y.append(dy[m])
    bx, by = np.concatenate(bb_x), np.concatenate(bb_y)
    boot.append(float(np.sum(bx * by) / np.sum(bx ** 2)))
boot = np.array(boot)
from scipy import stats
wil = stats.wilcoxon(z - 1.0) if len(z) > 5 else None
med_boot = np.array([np.median(rng.choice(z, size=len(z), replace=True)) for _ in range(2000)])
out = dict(
    source="GeoNames cities15000 dump", url="https://download.geonames.org/export/dump/cities15000.zip",
    rows_in_dump=nrows, countries_used=len(rows), cities_used=int(sum(r["ncities"] for r in rows)),
    filter="feature class P; codes PPL/PPLC/PPLA*/PPLF/PPLG/PPLS; population>0; >=50 cities/country",
    per_country=rows,
    distribution_of_zeta=dict(median=float(np.median(z)), mean=float(np.mean(z)),
                              sd=float(np.std(z, ddof=1)), iqr=[float(np.percentile(z, 25)),
                                                                float(np.percentile(z, 75))],
                              frac_within_0_8_1_2=float(np.mean((z >= 0.8) & (z <= 1.2)))),
    pooled_country_fe=dict(zeta=-beta, se=se_pooled, bootstrap_se=float(np.std(boot, ddof=1)),
                           ci95=[-float(np.percentile(boot, 97.5)), -float(np.percentile(boot, 2.5))],
                           n=int(len(x)), ncountries=int(len(lib)),
                           caveat="country-FE weighted by each country's log-population variance, so it "
                                  "is dominated by large countries with many small towns; the per-country "
                                  "distribution is the primary statistic"),
    test_vs_1=dict(wilcoxon_stat=float(wil.statistic) if wil else None,
                   wilcoxon_p=float(wil.pvalue) if wil else None,
                   median_minus_1=float(np.median(z) - 1.0),
                   median_bootstrap_ci95=[float(np.percentile(med_boot, 2.5)),
                                          float(np.percentile(med_boot, 97.5))]),
    literature="Zipf exponent ~1",
    caveat="GeoNames localities/city proper, crowdsourced, not UN agglomerations; definitional noise "
           "large; one vintage only so Gibrat (needs two waves) remains untestable from this source",
)
json.dump(out, open(os.path.join(OUT, "zipf.json"), "w"), indent=1)
import csv
with open(os.path.join(OUT, "zipf_countries.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["country", "ncities", "zeta", "se", "r2", "maxpop", "minpop"])
    for r in rows:
        w.writerow([r["country"], r["ncities"], r["zeta"], r["se"], r["r2"], r["maxpop"], r["minpop"]])
print(json.dumps({k: out[k] for k in ("rows_in_dump", "countries_used", "cities_used",
                                     "distribution_of_zeta", "pooled_country_fe", "test_vs_1")}, indent=1))
