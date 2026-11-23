"""Scaling-law tests (task-19, The Networked Domus Appendix A + canonical laws).

Data on box2 at /root/work/data (World Bank / WCDE style country-year series) plus ILOSTAT
occupation counts pulled live from rplumber.ilo.org, plus GeoNames city populations.
Every result written to results/scaling_results.json; small extracts to results/.
"""
import json, os, sys, csv, math, warnings
import numpy as np
warnings.filterwarnings("ignore")
from scipy.optimize import least_squares
import statsmodels.api as sm

DATA = "/root/work/data"
WD = "/root/work/scaling"
OUT = os.path.join(WD, "results")
os.makedirs(OUT, exist_ok=True)
META = json.load(open(os.path.join(DATA, "meta.json")))
res = {"data_availability": [], "sections": {}}


def load(name):
    return json.load(open(os.path.join(DATA, name + ".json")))


def panel(rows):
    d = {}
    for r in rows:
        if r is None or len(r) < 3 or r[2] is None:
            continue
        try:
            v = float(r[2])
        except Exception:
            continue
        if math.isfinite(v):
            d[(str(r[0]), int(r[1]))] = v
    return d


def is_country(iso):
    m = META.get(iso)
    return bool(m) and m.get("region") != "Aggregates"


def ols_cluster(y, X, groups):
    X = sm.add_constant(np.asarray(X, float))
    m = sm.OLS(np.asarray(y, float), X).fit(cov_type="cluster",
                                            cov_kwds={"groups": np.asarray(groups)})
    return m


P = {k: panel(load(k)) for k in
     ("fertility", "sec", "gpi_sec", "urban", "gdppc_log", "tax", "flfp", "ter")}
AVAIL = dict(
    fertility=(len(P["fertility"]), min(k[1] for k in P["fertility"]), max(k[1] for k in P["fertility"])),
    sec=(len(P["sec"]), min(k[1] for k in P["sec"]), max(k[1] for k in P["sec"])),
    gpi_sec=(len(P["gpi_sec"]), min(k[1] for k in P["gpi_sec"]), max(k[1] for k in P["gpi_sec"])),
    urban=(len(P["urban"]), min(k[1] for k in P["urban"]), max(k[1] for k in P["urban"])),
    gdppc_levels=(len(P["gdppc_log"]), min(k[1] for k in P["gdppc_log"]), max(k[1] for k in P["gdppc_log"])),
    tax=(len(P["tax"]), min(k[1] for k in P["tax"]), max(k[1] for k in P["tax"])),
)
for k, v in AVAIL.items():
    res["data_availability"].append(dict(series=k, rows=v[0], year_min=v[1], year_max=v[2],
                                         used_in=""))

# ============================================================ A. urbanisation vs income
rows = []
for (iso, y), u in P["urban"].items():
    if not is_country(iso) or not (0.0 < u < 100.0):
        continue
    g = P["gdppc_log"].get((iso, y))
    if not g or g <= 0:
        continue
    rows.append((iso, y, u / 100.0, math.log(g)))
arr = np.array([(r[3]) for r in rows]); urb = np.array([r[2] for r in rows])
iso = np.array([r[0] for r in rows]); yrr = np.array([r[1] for r in rows])
logit = lambda x: np.log(np.clip(x, 1e-6, 1 - 1e-6) / (1 - np.clip(x, 1e-6, 1 - 1e-6)))


def fit_logistic(gdp, u, p0):
    def f(p):
        a, b = p
        z = a + b * gdp
        return 1.0 / (1.0 + np.exp(-np.clip(z, -40, 40))) - u
    s = least_squares(f, p0, bounds=([-10, 0.05], [10, 3.0]), max_nfev=4000)
    return s.x


def predict_logistic(p, gdp):
    return 1.0 / (1.0 + np.exp(-np.clip(p[0] + p[1] * gdp, -40, 40)))


p_glob = fit_logistic(arr, urb, [-4.0, 0.6])
pred_log = predict_logistic(p_glob, arr)
rmse_log = float(np.sqrt(np.mean((pred_log - urb) ** 2)))
# log-linear level model and power-law level model (curves compared out of sample, by country)
olsl = ols_cluster(urb, arr, iso); rmse_lin = float(np.sqrt(np.mean(olsl.resid ** 2)))


def fit_power(gdp, u):
    def f(p):
        return np.exp(p[0] + p[1] * gdp) - u
    s = least_squares(f, [-6.0, 1.0], max_nfev=4000)
    return s.x


p_pow = fit_power(arr, urb)
rmse_pow = float(np.sqrt(np.mean((np.exp(p_pow[0] + p_pow[1] * arr) - urb) ** 2)))

# 5-fold out-of-sample by country
countries = np.unique(iso)
rng = np.random.default_rng(7)
folds = np.array_split(rng.permutation(countries), 5)
oos = {"logistic": [], "log_linear": [], "power": []}
for f in folds:
    te = np.isin(iso, f); tr = ~te
    if tr.sum() < 30 or te.sum() < 10:
        continue
    pl = fit_logistic(arr[tr], urb[tr], [-4.0, 0.6])
    oos["logistic"].append(np.sqrt(np.mean((predict_logistic(pl, arr[te]) - urb[te]) ** 2)))
    mm = sm.OLS(urb[tr], sm.add_constant(arr[tr])).fit()
    oos["log_linear"].append(np.sqrt(np.mean((mm.predict(sm.add_constant(arr[te])) - urb[te]) ** 2)))
    pp = fit_power(arr[tr], urb[tr])
    oos["power"].append(np.sqrt(np.mean((np.exp(pp[0] + pp[1] * arr[te]) - urb[te]) ** 2)))
# cluster bootstrap for logistic params
boot = []
for _ in range(300):
    pick = rng.choice(countries, size=len(countries), replace=True)
    idx = np.concatenate([np.where(iso == c)[0] for c in pick])
    try:
        boot.append(fit_logistic(arr[idx], urb[idx], p_glob))
    except Exception:
        pass
boot = np.array(boot)
midpoint = -p_glob[0] / p_glob[1]
res["sections"]["urban_income"] = dict(
    question="Is urbanisation vs income a logistic S-curve or a power law / log-linear relation?",
    nobs=int(len(rows)), ncountries=int(len(countries)),
    logistic=dict(a=float(p_glob[0]), b=float(p_glob[1]),
                  b_se=float(np.std(boot[:, 1], ddof=1)),
                  a_se=float(np.std(boot[:, 0], ddof=1)),
                  midpoint_log_income=float(midpoint),
                  midpoint_income_levels=float(np.exp(midpoint)),
                  rmse_share=rmse_log),
    log_linear=dict(slope=float(olsl.params[1]), slope_se=float(olsl.bse[1]),
                    r2=float(olsl.rsquared), rmse_share=rmse_lin),
    power_law=dict(A=float(np.exp(p_pow[0])), exponent=float(p_pow[1]), rmse_share=rmse_pow),
    out_of_sample_rmse_share={k: float(np.mean(v)) for k, v in oos.items()},
    verdict="logistic" if np.mean(oos["logistic"]) < min(np.mean(oos["power"]),
                                                         np.mean(oos["log_linear"])) else "not logistic",
)

# ============================================================ B. schooling vs income (Mincer proxy)
mm = []
for (iso_, y), s in P["sec"].items():
    if not is_country(iso_) or s <= 0:
        continue
    g = P["gdppc_log"].get((iso_, y))
    if not g or g <= 0:
        continue
    mm.append((iso_, y, math.log(s), math.log(g)))
miso = np.array([r[0] for r in mm])
mres = ols_cluster(np.array([r[2] for r in mm]), np.array([r[3] for r in mm]), miso)
res["sections"]["schooling_income"] = dict(
    question="Country-level weak Mincer proxy: is log schooling linear in log income?",
    n=int(len(mm)), ncountries=int(len(set(miso))),
    slope=float(mres.params[1]), slope_se=float(mres.bse[1]), r2=float(mres.rsquared),
    caveat="country-year aggregates, not individual earnings; not an individual Mincer return",
)

# ============================================================ C. Wagner's law (tax share vs income)
tw = []
for (iso_, y), t in P["tax"].items():
    if not is_country(iso_) or t <= 0:
        continue
    g = P["gdppc_log"].get((iso_, y))
    if not g or g <= 0:
        continue
    tw.append((iso_, y, math.log(t), math.log(g)))
tiso = np.array([r[0] for r in tw])
tres = ols_cluster(np.array([r[2] for r in tw]), np.array([r[3] for r in tw]), tiso)
res["sections"]["wagner"] = dict(
    question="Wagner: does the tax/spending share rise with income (elasticity > 1)?",
    n=int(len(tw)), ncountries=int(len(set(tiso))),
    elasticity=float(tres.params[1]), se=float(tres.bse[1]), r2=float(tres.rsquared),
    caveat="the stored series is a single tax-revenue share whose exact definition is not documented "
           "in the data bundle; treat the elasticity as indicative",
)

# ============================================================ D. fertility vs income / urbanisation
fi = []
for (iso_, y), t in P["fertility"].items():
    if not is_country(iso_) or t <= 0:
        continue
    g = P["gdppc_log"].get((iso_, y))
    if not g or g <= 0:
        continue
    fi.append((iso_, y, math.log(t), math.log(g), P["urban"].get((iso_, y))))
fiso = np.array([r[0] for r in fi]); ly = np.array([r[2] for r in fi]); lg = np.array([r[3] for r in fi])
m1 = ols_cluster(ly, lg, fiso)
X2 = np.column_stack([lg, lg ** 2])
m2 = ols_cluster(ly, X2, fiso)
cv1, cv2 = [], []
for f in np.array_split(rng.permutation(np.unique(fiso)), 5):
    te = np.isin(fiso, f); tr = ~te
    a = sm.OLS(ly[tr], sm.add_constant(lg[tr])).fit()
    cv1.append(np.sqrt(np.mean((a.predict(sm.add_constant(lg[te])) - ly[te]) ** 2)))
    Xtr = sm.add_constant(np.column_stack([lg[tr], lg[tr] ** 2]))
    b = sm.OLS(ly[tr], Xtr).fit()
    cv2.append(np.sqrt(np.mean((b.predict(sm.add_constant(np.column_stack([lg[te], lg[te] ** 2]))) - ly[te]) ** 2)))
res["sections"]["fertility_income"] = dict(
    question="Is fertility vs income a simple power law or curved?",
    n=int(len(fi)), ncountries=int(len(set(fiso))),
    power_law=dict(exponent=float(m1.params[1]), se=float(m1.bse[1]), r2=float(m1.rsquared)),
    quadratic=dict(linear=float(m2.params[1]), linear_se=float(m2.bse[1]),
                   squared=float(m2.params[2]), squared_se=float(m2.bse[2]), r2=float(m2.rsquared)),
    oos_rmse_logtfr=dict(power_law=float(np.mean(cv1)), quadratic=float(np.mean(cv2))),
)

# ============================================================ E. collapse curve
COH = range(1950, 1997)
crows = []
for iso_, c in [(i, c) for i in META for c in COH]:
    if not is_country(iso_):
        continue
    f_att = P["sec"].get((iso_, c + 20))
    g = P["gpi_sec"].get((iso_, c + 20))
    tfr = P["fertility"].get((iso_, c + 28))
    if f_att is None or g is None or tfr is None or tfr <= 0 or not (0.2 <= g <= 2.0):
        continue
    female_att = f_att * 2.0 * g / (1.0 + g)     # female secondary completion (%), approximation
    crows.append((iso_, c, female_att, tfr))
print("collapse rows:", len(crows), file=sys.stderr)
CA = np.array([r[2] for r in crows]); CT = np.array([r[3] for r in crows])
CISO = np.array([r[0] for r in crows]); CCOH = np.array([r[1] for r in crows])
keep = np.array([np.sum(CISO == c) >= 15 for c in CISO])
CA, CT, CISO, CCOH = CA[keep], CT[keep], CISO[keep], CCOH[keep]


def fit_exp(F, y):
    def f(p):
        return p[0] + p[1] * np.exp(-np.clip(p[2], 1e-4, 1) * F) - y
    s = least_squares(f, [1.0, 6.0, 0.02], bounds=([-5, 0, 1e-5], [8, 40, 1.0]), max_nfev=8000)
    return s.x


p_exp = fit_exp(CA, CT)
pred_exp = p_exp[0] + p_exp[1] * np.exp(-p_exp[2] * CA)
sse_exp = float(np.sum((pred_exp - CT) ** 2))
m_lin = sm.OLS(CT, sm.add_constant(CA)).fit()
m_loglog = sm.OLS(np.log(CT), sm.add_constant(np.log(CA))).fit()
pred_lin = m_lin.predict(sm.add_constant(CA))
pred_pow = np.exp(m_loglog.predict(sm.add_constant(np.log(CA))))
sse_lin = float(np.sum((pred_lin - CT) ** 2))
sse_pow = float(np.sum((pred_pow - CT) ** 2))
SST = float(np.sum((CT - np.mean(CT)) ** 2))
rng_ = np.random.default_rng(11)
# AIC comparable across fits only when computed on the same (TFR) scale
aics = dict(exponential=float(len(CT) * math.log(sse_exp / len(CT)) + 2 * 3),
            linear=float(len(CT) * math.log(sse_lin / len(CT)) + 2 * 2),
            power=float(len(CT) * math.log(sse_pow / len(CT)) + 2 * 2))
# out-of-sample by country (5 folds), TFR scale
model_oos = {"exponential": [], "linear": [], "power": []}
cuniq0 = np.unique(CISO)
for f in np.array_split(rng_.permutation(cuniq0), 5):
    te = np.isin(CISO, f); tr = ~te
    if tr.sum() < 100 or te.sum() < 20:
        continue
    pe = fit_exp(CA[tr], CT[tr])
    model_oos["exponential"].append(float(np.sqrt(np.mean((pe[0] + pe[1] * np.exp(-pe[2] * CA[te]) - CT[te]) ** 2))))
    lm = sm.OLS(CT[tr], sm.add_constant(CA[tr])).fit()
    model_oos["linear"].append(float(np.sqrt(np.mean((lm.predict(sm.add_constant(CA[te])) - CT[te]) ** 2))))
    pm = sm.OLS(np.log(CT[tr]), sm.add_constant(np.log(CA[tr]))).fit()
    model_oos["power"].append(float(np.sqrt(np.mean((np.exp(pm.predict(sm.add_constant(np.log(CA[te])))) - CT[te]) ** 2))))
model_oos = {k: (float(np.mean(v)) if v else None) for k, v in model_oos.items()}
# clustered bootstrap of exponential params
cb = []
cuniq = np.unique(CISO)
for _ in range(200):
    pick = rng_.choice(cuniq, size=len(cuniq), replace=True)
    idx = np.concatenate([np.where(CISO == c)[0] for c in pick])
    try:
        cb.append(fit_exp(CA[idx], CT[idx]))
    except Exception:
        pass
cb = np.array(cb)
# collapse tests: country intercepts then country slopes
Xc = sm.add_constant(np.column_stack([CA, np.ones(len(CA)) * 0]))
# demeaned within-country (country fixed intercepts, common slope)
dm = lambda v: v - np.array([np.mean(v[CISO == c]) for c in CISO])
b_within = float(np.sum(dm(CA) * dm(CT)) / np.sum(dm(CA) ** 2))
resid_within = dm(CT) - b_within * dm(CA)
sse_within = float(np.sum(resid_within ** 2))
sse_pooled = sse_exp
# country-specific slopes (countries with >=15 cohorts)
slopes, intercepts, csse, cn = [], [], 0.0, 0
for c in cuniq:
    m = CISO == c
    if m.sum() < 15:
        continue
    mm_ = sm.OLS(CT[m], sm.add_constant(CA[m])).fit()
    slopes.append(mm_.params[1]); intercepts.append(mm_.params[0])
    csse += float(np.sum(mm_.resid ** 2)); cn += m.sum()
sse_slopes = csse
n_c = len(cuniq)
k_pool, k_within, k_slopes = 3, 1 + n_c, 2 * n_c
nobs = len(CT)
a_p = nobs * math.log(sse_pooled / nobs) + 2 * k_pool
a_w = nobs * math.log(sse_within / nobs) + 2 * k_within
a_s = nobs * math.log(sse_slopes / nobs) + 2 * k_slopes
# F tests (nested least squares)
df_w = nobs - k_within; df_s = nobs - k_slopes
F_slopes_vs_pooled = ((sse_pooled - sse_slopes) / (k_slopes - k_pool)) / (sse_slopes / df_s)
F_within_vs_pooled = ((sse_pooled - sse_within) / (k_within - k_pool)) / (sse_within / df_w)
F_slopes_given_intercepts = ((sse_within - sse_slopes) / (n_c - 1)) / (sse_slopes / df_s)
# collapse after a country-level multiplicative rescaling of the common exponential shape
sc = np.array([np.mean(CT[CISO == c]) / np.mean(pred_exp[CISO == c]) for c in CISO])
pred_sc = pred_exp * sc
sse_sc = float(np.sum((pred_sc - CT) ** 2))
# residual structure
resid = CT - pred_exp
bucket = np.where(CA < 50, "primary-dominant (<50%)", np.where(CA < 80, "secondary (50-80%)", "universal (>80%)"))
by_bucket = {}
for b in ("primary-dominant (<50%)", "secondary (50-80%)", "universal (>80%)"):
    m = bucket == b
    if m.sum() > 5:
        by_bucket[b] = dict(n=int(m.sum()), mean_resid=float(np.mean(resid[m])),
                            sd_resid=float(np.std(resid[m], ddof=1)))
inc = META.get  # noqa
by_income = {}
for iso_, c, a, t in crows:
    pass
# residual by country income group and cohort band
income_of = np.array([META.get(c, {}).get("income", "?") for c in CISO])
for g in sorted(set(income_of)):
    m = income_of == g
    if m.sum() > 5:
        by_income[g] = dict(n=int(m.sum()), mean_resid=float(np.mean(resid[m])))
band = (CCOH // 10) * 10
by_band = {}
for b in sorted(set(band.tolist())):
    m = band == b
    by_band[str(b)] = dict(n=int(m.sum()), mean_resid=float(np.mean(resid[m])))
# how much does country identity explain? one-way ICC on the collapse residual
grand = float(np.mean(resid)); sst = float(np.sum((resid - grand) ** 2))
ssb = float(sum((np.mean(resid[CISO == c]) - grand) ** 2 * np.sum(CISO == c) for c in cuniq))
res["sections"]["collapse"] = dict(
    question="Do fertility and female attainment across countries and cohorts fall on ONE common curve?",
    cohort_definition="cohort born c: female secondary completion (%) at year c+20, total fertility at year c+28",
    female_attainment_note="female attainment = gross secondary completion x 2*gpi/(1+gpi) (approximation; "
                           "the stored series is both-sexes, the parity index supplies the female/male ratio)",
    n=int(nobs), ncountries=int(n_c), cohorts=[int(min(CCOH)), int(max(CCOH))],
    fits=dict(
        exponential=dict(a=float(p_exp[0]), a_se=float(np.std(cb[:, 0], ddof=1)),
                         b=float(p_exp[1]), b_se=float(np.std(cb[:, 1], ddof=1)),
                         decay=float(p_exp[2]), decay_se=float(np.std(cb[:, 2], ddof=1)),
                         r2=float(1 - sse_exp / np.sum((CT - np.mean(CT)) ** 2))),
        linear=dict(slope=float(m_lin.params[1]), se=float(m_lin.bse[1]),
                    r2=float(m_lin.rsquared)),
        power=dict(exponent=float(m_loglog.params[1]), se=float(m_loglog.bse[1]),
                   r2=float(1 - sse_pow / SST)),
        aic_tfr_scale=aics),
    collapse_quality=dict(
        residual_sd=float(np.sqrt(sse_exp / nobs)),
        fertility_range=float(np.max(CT) - np.min(CT)),
        residual_sd_over_range=float(np.sqrt(sse_exp / nobs) / (np.max(CT) - np.min(CT))),
        r2_pooled=float(1 - sse_exp / np.sum((CT - np.mean(CT)) ** 2)),
        r2_country_intercepts=float(1 - sse_within / np.sum((CT - np.mean(CT)) ** 2)),
        r2_country_slopes=float(1 - sse_slopes / np.sum((CT - np.mean(CT)) ** 2)),
        country_variance_share_of_residual=float(ssb / sst) if sst > 0 else None,
        r2_country_mult_rescale=float(1 - sse_sc / SST),
        residual_sd_rescaled=float(np.sqrt(sse_sc / nobs)),
        F_country_slopes_vs_pooled=dict(F=float(F_slopes_vs_pooled), df=(int(k_slopes - k_pool), int(df_s))),
        F_country_slopes_given_intercepts=dict(F=float(F_slopes_given_intercepts),
                                               df=(int(n_c - 1), int(df_s))),
    ),
    oos_rmse_tfr=model_oos,
    residual_structure=dict(by_attainment_bucket=by_bucket, by_income_group=by_income,
                            by_cohort_band=by_band),
    country_slope_median=float(np.median(slopes)) if slopes else None,
    country_slope_iqr=[float(np.percentile(slopes, 25)), float(np.percentile(slopes, 75))] if slopes else None,
    verdict="single curve adequate" if (F_slopes_vs_pooled < 1.5 and by_income) else "country structure remains",
)

# ============================================================ F. Heaps' law (ILOSTAT occupation counts)
heap = {"status": "unavailable"}
try:
    rows_ilo = []
    with open(os.path.join(WD, "ilo_test.csv"), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            c = r["classif1"]
            if c.startswith("OCU_ISCO08_") and c.split("_")[-1].isdigit() and c != "OCU_ISCO08_TOTAL":
                try:
                    v = float(r["obs_value"])
                except Exception:
                    continue
                if math.isfinite(v) and v > 0:
                    rows_ilo.append((r["ref_area"], int(r["time"]), int(c.split("_")[-1]), v))
    # latest year per area, require >=8 nonzero categories
    latest = {}
    for a, y, cat, v in rows_ilo:
        latest.setdefault((a, y), {})[cat] = v
    curves = []
    for (a, y), d in latest.items():
        if not is_country(a) or len(d) < 8:
            continue
        curves.append((a, y, np.array([d.get(k, 0.0) for k in range(10)])))
    if curves:
        xs, ys, gs = [], [], []
        per_b = []
        for a, y, ni in curves:
            N = ni.sum()
            if N < 100:
                continue
            for u in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3):
                n = max(1.0, u * N)
                # exact expected distinct categories in a sample of n from N
                es = 0.0
                for x in ni:
                    if x <= 0 or n > N:
                        continue
                    if n > N - x:
                        # a sample larger than the non-category pool is certain to include it
                        es += 1.0
                        continue
                    lg = math.lgamma
                    lp = lg(N - x + 1) - lg(N - x - n + 1) - lg(N + 1) + lg(N - n + 1)
                    es += 1.0 - math.exp(lp)
                xs.append(math.log(n)); ys.append(math.log(max(es, 1e-9))); gs.append(a)
        xs = np.array(xs); ys = np.array(ys); gs = np.array(gs)
        # pooled with country fixed effects (demean within country)
        dmx = xs - np.array([np.mean(xs[gs == c]) for c in gs])
        dmy = ys - np.array([np.mean(ys[gs == c]) for c in gs])
        b = float(np.sum(dmx * dmy) / np.sum(dmx ** 2))
        resid = dmy - b * dmx
        lib = np.unique(gs)
        meat = sum((dmx[gs == c] * resid[gs == c]).sum() ** 2 for c in lib)
        se = float(math.sqrt(meat) / np.sum(dmx ** 2))
        for c in lib:
            m = gs == c
            if m.sum() >= 4 and np.var(xs[m]) > 0:
                per_b.append(float(np.sum((xs[m] - xs[m].mean()) * (ys[m] - ys[m].mean())) /
                                   np.sum((xs[m] - xs[m].mean()) ** 2)))
        # raw distinct categories vs workforce size
        raw = [(math.log(ni.sum()), math.log(np.sum(ni > 0))) for a, y, ni in curves if ni.sum() > 0]
        rl = np.array(raw)
        braw = float(np.sum((rl[:, 0] - rl[:, 0].mean()) * (rl[:, 1] - rl[:, 1].mean())) /
                     np.sum((rl[:, 0] - rl[:, 0].mean()) ** 2))
        heap = dict(
            status="ok", classification_depth="ISCO-08 1-digit major groups (10 categories) — 2-/3-digit "
                                              "ILOSTAT indicators are deprecated in the public API",
            ncountries=len(lib), npoints=int(len(xs)),
            heaps_exponent=b, se=se,
            per_country_median=float(np.median(per_b)) if per_b else None,
            per_country_iqr=[float(np.percentile(per_b, 25)), float(np.percentile(per_b, 75))] if per_b else None,
            raw_count_vs_workforce_exponent=braw,
            literature_range=[0.4, 0.6],
            test_vs_literature=dict(z_0_4=float((b - 0.4) / se) if se > 0 else None,
                                    z_0_6=float((b - 0.6) / se) if se > 0 else None),
            test_vs_1_proportional=float((b - 1.0) / se) if se > 0 else None,
            caveat="10-category ceiling truncates the accumulation curve; the exponent is estimated where "
                   "the curve is still rising (samples up to 30% of the workforce)",
        )
        # save small extract
        with open(os.path.join(OUT, "ilo_occupation_extract.csv"), "w") as fh:
            fh.write("area,year,category,count\n")
            for a, y, ni in curves:
                for k, v in enumerate(ni):
                    fh.write("%s,%d,%d,%f\n" % (a, y, k, v))
except Exception as e:
    heap = {"status": "error", "error": str(e)[:300]}
res["sections"]["heaps"] = heap

# ============================================================ G. Zipf (GeoNames city populations)
zipf = {"status": "unavailable"}
gp = os.path.join(WD, "cities15000.txt")
if os.path.exists(gp):
    cities = {}
    with open(gp, encoding="utf-8") as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 15:
                continue
            if not p[7].startswith("PPL"):
                continue
            try:
                pop = int(p[11])
            except Exception:
                continue
            if pop <= 0:
                continue
            cities.setdefault(p[8], []).append(pop)
    est = []
    for cc, pops in cities.items():
        if len(pops) < 50:
            continue
        pops = np.sort(np.array(pops))[::-1]
        rank = np.arange(1, len(pops) + 1)
        m = sm.OLS(np.log10(rank), sm.add_constant(np.log10(pops))).fit()
        est.append((cc, -float(m.params[1]), float(m.bse[1]), len(pops)))
    if est:
        z = np.array([e[1] for e in est])
        zipf = dict(status="ok", ncountries=len(est), ncities=int(sum(e[3] for e in est)),
                    median_zipf_exponent=float(np.median(z)),
                    iqr=[float(np.percentile(z, 25)), float(np.percentile(z, 75))],
                    mean=float(np.mean(z)), sd=float(np.std(z, ddof=1)),
                    frac_countries_ci_contains_1=float(np.mean([abs(e[1] - 1) < 1.96 * e[2] for e in est])),
                    test_vs_1=dict(wilcoxon_p=None,
                                   mean_z=float((np.mean(z) - 1) / (np.std(z, ddof=1) / math.sqrt(len(z))))),
                    caveat="GeoNames localities (not UN agglomerations), crowdsourced coverage; the UN WUP "
                           "city file was not reachable from box2 (all known URLs 404), so Gibrat (needs two "
                           "WUP waves) is data-limited")
        with open(os.path.join(OUT, "zipf_countries.csv"), "w") as fh:
            fh.write("country,zipf_exponent,se,ncities\n")
            for e in est:
                fh.write("%s,%f,%f,%d\n" % e)
res["sections"]["zipf"] = zipf

# ============================================================ H. unavailable laws
res["sections"]["unavailable"] = {
    "bettencourt_output": "no city-level GDP/wages/patents/infrastructure on box2; city output scaling "
                          "(beta~1.15) and infrastructure (beta~0.85) cannot be tested — documented as data-limited",
    "gibrat": "needs two city-population waves (WUP); WUP files not reachable from box2, GeoNames has one "
              "vintage — documented as data-limited",
    "credential_vs_occupation": "no Credential Engine or BLS SOC series on box2; US credential:occupation "
                                "time-series test cannot be run — documented as a gap",
    "gravity_migration": "no clean bilateral migration matrix + distance on box2 within the time budget — gap",
    "teacher_student_ratio": "no school-level data on box2 — gap",
}
AVAIL["ilostat_occupation"] = (len(rows_ilo) if 'rows_ilo' in dir() else 0, 1969, 2025)
res["notes"] = ("A scaling regularity is not a causal identification. Rarefaction is applied to all "
                "category-count claims; exponents carry clustered SEs; nulls are reported.")
json.dump(res, open(os.path.join(OUT, "scaling_results.json"), "w"), indent=1)
print("WROTE", os.path.join(OUT, "scaling_results.json"))
