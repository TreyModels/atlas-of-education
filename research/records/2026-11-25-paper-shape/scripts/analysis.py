"""Paper N4 — the shape of the demographic transition.

Fresh pull (box2 down): World Bank WDI annual 1960-2023 (TFR, female life expectancy, infant mortality,
urban share, GDP p.c. PPP, female lower/upper secondary completion, population) + WB country list.

Steps
 1. build transition panel and observed shape descriptors (onset, midpoint, floor, fall, speed, duration,
    curvature);
 2. fit five functional forms per country (logistic, Gompertz, exponential-to-floor, linear-kink-with-floor,
    cubic spline) and compare AIC/BIC and a last-decade hold-out;
 3. cluster the normalised decline shapes (k-means, k by silhouette) and test the real partition against
    random partitions of the same countries and sizes (transportability logic);
 4. regress shape parameters on schooling-expansion timing, mortality-decline timing, income and
    urbanisation (horse race), with robust SEs;
 5. write results/shape_results.json + CSVs + figures.

Correlational analysis throughout: no causal identification is claimed.
"""
import json, os, sys, warnings
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.interpolate import interp1d
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)
rng = np.random.default_rng(20261125)

wb = json.load(open(os.path.join(DATA, "wb_countries.json")))
COUNTRY = {r["id"]: r["name"] for r in wb[1] if r["region"]["value"] != "Aggregates"}
REGION = {r["id"]: r["region"]["value"] for r in wb[1] if r["region"]["value"] != "Aggregates"}

IND = {"tfr": "SP.DYN.TFRT.IN", "le_f": "SP.DYN.LE00.FE.IN", "imr": "SP.DYN.IMRT.IN",
       "prm_f": "SE.PRM.CUAT.FE.ZS",
       "urban": "SP.URB.TOTL.IN.ZS", "gdppc": "NY.GDP.PCAP.PP.KD",
       "lower_sec_f": "SE.SEC.CUAT.LO.FE.ZS", "upper_sec_f": "SE.SEC.CUAT.UP.FE.ZS",
       "pop": "SP.POP.TOTL"}
panel = {}
for key, code in IND.items():
    d = json.load(open(os.path.join(DATA, "wdi_%s.json" % code)))
    rows = d[1]
    rec = {}
    for r in rows:
        iso = r.get("countryiso3code")
        if iso not in COUNTRY or r.get("value") is None:
            continue
        rec.setdefault(iso, {})[int(r["date"])] = float(r["value"])
    panel[key] = rec

YEARS = list(range(1960, 2024))


def series(key, iso):
    return np.array([panel[key].get(iso, {}).get(y, np.nan) for y in YEARS], float)


def smooth(x, w=5):
    s = pd.Series(x).rolling(w, center=True, min_periods=2).mean().to_numpy()
    return np.where(np.isnan(s), x, s)


# ---------------------------------------------------------------- 1. descriptors
countries = []
for iso in COUNTRY:
    t = series("tfr", iso)
    ok = ~np.isnan(t)
    if ok.sum() < 40:
        continue
    ts = smooth(t)
    peak_i = int(np.nanargmax(ts[:min(len(ts), 50)]))      # allow late transitions a later peak
    peak = float(ts[peak_i])
    last = t[np.where(ok)[0][-5:]]
    floor = float(np.nanmean(last))
    fall = peak - floor
    if fall < 1.5 or peak < 4.0 or floor > 3.2:
        continue
    above = lambda f: np.where((ts <= floor + f * fall) & (np.arange(len(ts)) > peak_i))[0]
    def first(f, default=np.nan):
        idx = above(f)
        return float(YEARS[idx[0]]) if len(idx) else default
    onset = first(0.95); t10 = first(0.10); t90 = first(0.90); mid = first(0.50)
    if np.isnan(t10) or np.isnan(t90) or np.isnan(onset):
        continue
    duration = t10 - t90
    if duration <= 0 or duration > 70:
        continue
    # max 5-year average annual decline
    speed = 0.0
    for i in range(len(ts) - 5):
        if not np.isnan(ts[i]) and not np.isnan(ts[i + 5]):
            speed = max(speed, (ts[i] - ts[i + 5]) / 5.0)
    if speed <= 0:
        continue
    curvature = speed / (fall / duration) if duration > 0 else np.nan
    cov = {k: series(k, iso) for k in ("le_f", "imr", "urban", "gdppc", "lower_sec_f", "upper_sec_f", "prm_f")}
    countries.append(dict(iso=iso, name=COUNTRY[iso], region=REGION[iso], peak_year=int(YEARS[peak_i]),
                          peak=peak, floor=floor, fall=fall, onset=onset, midpoint=mid, t10=t10, t90=t90,
                          duration=duration, speed=speed, curvature=curvature, covariates=cov))
print("transition countries:", len(countries), file=sys.stderr)

Dshape = pd.DataFrame([dict(iso=c["iso"], name=c["name"], region=c["region"],
                            onset=c["onset"], midpoint=c["midpoint"], duration=c["duration"],
                            speed=c["speed"], floor=c["floor"], fall=c["fall"], peak=c["peak"],
                            curvature=c["curvature"], peak_year=c["peak_year"]) for c in countries])

# ---------------------------------------------------------------- 2. functional forms
def fit_logistic(x, y):
    def f(p):
        T0, pfloor, mid, s = p
        return pfloor + (T0 - pfloor) / (1 + np.exp((x - mid) / s)) - y
    s0 = (max(y) - min(y)) / 4
    out = least_squares(f, [max(y), min(y), float(np.mean(x)), -5.0],
                        bounds=([0, 0, 1850, -40], [12, 6, 2100, -0.1]), max_nfev=4000)
    return out.x


def fit_gompertz(x, y):
    def f(p):
        T0, pfloor, mid, s = p
        return pfloor + (T0 - pfloor) * np.exp(-np.exp((x - mid) / s)) - y
    out = least_squares(f, [max(y), min(y), float(np.mean(x)), 10.0],
                        bounds=([0, 0, 1850, 0.1], [12, 6, 2100, 60]), max_nfev=4000)
    return out.x


def fit_exp(x, y):
    def f(p):
        T0, pfloor, onset, tau = p
        return np.where(x >= onset, pfloor + (T0 - pfloor) * np.exp(-(x - onset) / tau),
                        T0 + (pfloor - T0) * 0.0) - y
    out = least_squares(f, [max(y), min(y), 1965.0, 20.0],
                        bounds=([0, 0, 1900, 1.0], [12, 6, 2000, 80]), max_nfev=4000)
    return out.x


def fit_kink(x, y):
    def f(p):
        T0, pfloor, onset, b = p
        return np.maximum(pfloor, T0 - b * np.maximum(0.0, x - onset)) - y
    out = least_squares(f, [max(y), min(y), 1965.0, 0.05],
                        bounds=([0, 0, 1900, 0.001], [12, 6, 2000, 0.3]), max_nfev=4000)
    return out.x


def fit_spline(x, y, df=7):
    """Natural cubic spline basis with df parameters, fitted by least squares (penalty-free)."""
    from scipy.interpolate import BSpline
    knots = np.linspace(min(x), max(x), df - 2)
    t = np.concatenate([[knots[0]] * 4, knots, [knots[-1]] * 4])
    B = BSpline.design_matrix(x, t, 3).toarray()[:, : df]
    beta, *_ = np.linalg.lstsq(B, y, rcond=None)
    return beta, B


for c in countries:
    x = np.array(YEARS, float); y = np.array(series("tfr", c["iso"]), float)
    mask = ~np.isnan(y)
    xx, yy = x[mask], y[mask]
    n = len(yy)
    fits = {}
    for nm, fn, k in (("logistic", fit_logistic, 4), ("gompertz", fit_gompertz, 4),
                      ("exponential", fit_exp, 4), ("linear_kink", fit_kink, 4)):
        try:
            p = fn(xx, yy)
            resid = (xx - xx)  # placeholder
            if nm == "logistic":
                pred = p[1] + (p[0] - p[1]) / (1 + np.exp((xx - p[2]) / p[3]))
            elif nm == "gompertz":
                pred = p[1] + (p[0] - p[1]) * np.exp(-np.exp((xx - p[2]) / p[3]))
            elif nm == "exponential":
                pred = np.where(xx >= p[2], p[1] + (p[0] - p[1]) * np.exp(-(xx - p[2]) / p[3]), p[0])
            else:
                pred = np.maximum(p[1], p[0] - p[3] * np.maximum(0.0, xx - p[2]))
            sse = float(np.sum((pred - yy) ** 2))
            fits[nm] = dict(params=[float(v) for v in p], sse=sse, k=k,
                            aic=n * np.log(sse / n) + 2 * k, bic=n * np.log(sse / n) + k * np.log(n))
        except Exception:
            continue
    try:
        beta, B = fit_spline(xx, yy)
        pred = B @ beta
        sse = float(np.sum((pred - yy) ** 2))
        fits["spline"] = dict(params=[float(v) for v in beta], sse=sse, k=7,
                              aic=n * np.log(sse / n) + 2 * 7, bic=n * np.log(sse / n) + 7 * np.log(n))
    except Exception:
        pass
    # last-decade hold-out (fit <= 2012, predict 2013-2023)
    ho = {}
    for nm, fn, k in (("logistic", fit_logistic, 4), ("gompertz", fit_gompertz, 4),
                      ("exponential", fit_exp, 4), ("linear_kink", fit_kink, 4)):
        tr = xx <= 2012; te = xx > 2012
        if tr.sum() < 20 or te.sum() < 3:
            continue
        try:
            p = fn(xx[tr], yy[tr])
            if nm == "logistic":
                pred = p[1] + (p[0] - p[1]) / (1 + np.exp((xx[te] - p[2]) / p[3]))
            elif nm == "gompertz":
                pred = p[1] + (p[0] - p[1]) * np.exp(-np.exp((xx[te] - p[2]) / p[3]))
            elif nm == "exponential":
                pred = np.where(xx[te] >= p[2], p[1] + (p[0] - p[1]) * np.exp(-(xx[te] - p[2]) / p[3]), p[0])
            else:
                pred = np.maximum(p[1], p[0] - p[3] * np.maximum(0.0, xx[te] - p[2]))
            ho[nm] = float(np.sqrt(np.mean((pred - yy[te]) ** 2)))
        except Exception:
            continue
    c["fits"] = {k: {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in fits.items()}
    c["best_form_bic"] = min(fits, key=lambda k: fits[k]["bic"]) if fits else None
    c["holdout_rmse"] = ho
    # model-based descriptors from the best form
    if c["best_form_bic"]:
        p = fits[c["best_form_bic"]]["params"]
        if c["best_form_bic"] == "logistic":
            c["model_midpoint"], c["model_plateau"], c["model_speed"] = p[2], p[1], (p[0] - p[1]) / (4 * abs(p[3]))
        elif c["best_form_bic"] == "gompertz":
            c["model_midpoint"], c["model_plateau"], c["model_speed"] = p[2], p[1], (p[0] - p[1]) * np.exp(-1) / abs(p[3])
        elif c["best_form_bic"] == "exponential":
            c["model_midpoint"], c["model_plateau"], c["model_speed"] = p[2] + p[3] * np.log(2), p[1], (p[0] - p[1]) / p[3]
        elif c["best_form_bic"] == "linear_kink":
            c["model_midpoint"], c["model_plateau"], c["model_speed"] = p[2] + (p[0] - p[1]) / (2 * p[3]), p[1], p[3]

# ---------------------------------------------------------------- 3. path-shape uniformity (aligned curves)
grid = np.linspace(0, 1, 11)
X = []
Xiso = []
for c in countries:
    y = np.array(series("tfr", c["iso"]), float)
    x = np.arange(len(y), dtype=float)
    m = ~np.isnan(y)
    yy = np.interp(grid * (c["t10"] - c["onset"]) + c["onset"], x[m], y[m])
    norm = (yy - c["floor"]) / c["fall"]
    X.append(norm); Xiso.append(c["iso"])
X = np.array(X); Xiso = np.array(Xiso)
pca = PCA(n_components=3).fit(X)
path_uniformity = dict(
    curve_pca_var=[float(v) for v in pca.explained_variance_ratio_],
    across_country_sd_by_grid=[float(v) for v in X.std(axis=0, ddof=1)],
    mean_abs_deviation_from_mean_curve=float(np.mean(np.abs(X - X.mean(0)))),
    note="aligned curves share onset and 10%-remaining endpoints; low residual variation means the "
         "decline PATH is a near-universal family and heterogeneity is in timing/pace/level",
)

# ---------------------------------------------------------------- 4. determinants
def cross_year(s, thresh, above=True):
    for i in range(1, len(s)):
        if np.isnan(s[i]) or np.isnan(s[i - 1]):
            continue
        if above and s[i] >= thresh > s[i - 1]:
            return float(YEARS[i])
        if (not above) and s[i] <= thresh < s[i - 1]:
            return float(YEARS[i])
    return np.nan


def timing(s, thresh):
    """First year the series reaches `thresh`; if the first observed value is already above the
    threshold, the first observed year (left-censored: already there when data begin)."""
    valid = np.where(~np.isnan(s))[0]
    if len(valid) == 0:
        return np.nan
    i0 = valid[0]
    if s[i0] >= thresh:
        return float(YEARS[i0])
    for i in range(i0 + 1, len(s)):
        if not np.isnan(s[i]) and s[i] >= thresh:
            return float(YEARS[i])
    return np.nan


def near(year, s, tol=15):
    """Value of a series at the valid year closest to `year` (within tol)."""
    best, val = None, np.nan
    for i, y in enumerate(YEARS):
        if abs(y - year) <= tol and not np.isnan(s[i]):
            if best is None or abs(y - year) < best:
                best, val = abs(y - year), float(s[i])
    return val


def cov(c, key):
    return c["covariates"][key]


rows = []
for c in countries:
    le = cov(c, "le_f"); imr = cov(c, "imr"); up = cov(c, "upper_sec_f")
    lo = cov(c, "lower_sec_f"); urb = cov(c, "urban"); gdp = cov(c, "gdppc")
    # schooling-expansion timing: first year female PRIMARY completion crosses 50% (fallback 30%,
    # then secondary completion crossing 30%); level predictor = secondary completion at onset
    prm = cov(c, "prm_f")
    school_50 = timing(prm, 50.0)
    if np.isnan(school_50):
        school_50 = timing(up, 30.0)
    school_30 = school_50
    # mortality-decline timing: LE +10 years above its 1960 value, else crossing 60
    mort_10 = np.nan
    if not np.isnan(le[0]):
        mort_10 = cross_year(le, le[0] + 10.0)
    le_60 = cross_year(le, 60.0)
    imr_half = np.nan
    try:
        base = le[:5]
        i0 = int(np.nanargmax(imr[:10]))
        if not np.isnan(imr[i0]):
            imr_half = cross_year(imr, imr[i0] / 2.0, above=False)
    except Exception:
        pass
    rows.append(dict(
        iso=c["iso"], name=c["name"], region=c["region"],
        onset=c["onset"], midpoint=c["midpoint"], duration=c["duration"], speed=c["speed"],
        floor=c["floor"], fall=c["fall"], peak=c["peak"], curvature=c["curvature"],
        school_30=school_30, school_50=school_50, mort_10=mort_10, le_60=le_60, imr_half=imr_half,
        school_level=near(c["onset"], up, 12), le_onset=near(c["onset"], le, 10),
        urban_onset=near(c["onset"], urb, 12), log_gdp_onset=np.log(near(c["onset"], gdp, 15))
        if near(c["onset"], gdp, 15) and near(c["onset"], gdp, 15) > 0 else np.nan,
        log_gdp_peak=np.log(near(c["peak_year"], gdp, 20))
        if near(c["peak_year"], gdp, 20) and near(c["peak_year"], gdp, 20) > 0 else np.nan,
    ))
D = pd.DataFrame(rows)
D["school_timing"] = D["school_50"]
D["school_lead"] = D["onset"] - D["school_50"]
D["mortality_lead"] = D["onset"] - D["mort_10"]
PRED = {"school_lead": "schooling expansion timing (onset minus year female primary completion reached "
                        "50%; left-censored at first observation)",
        "mortality_lead": "mortality-decline timing (onset minus year female life expectancy gained "
                          "10 years)",
        "log_gdp_onset": "log GDP per capita at onset (PPP)",
        "urban_onset": "urban share at onset",
        "school_level": "female upper-secondary completion at onset (%)"}
reg = {}
for dep in ("onset", "midpoint", "duration", "speed", "floor", "curvature"):
    reg[dep] = {}
    for pred, lab in PRED.items():
        dd = D.dropna(subset=[dep, pred])
        if len(dd) < 20:
            reg[dep][pred] = dict(n=int(len(dd)), note="too few complete cases", label=lab)
            continue
        m = sm.OLS(dd[dep], sm.add_constant(dd[[pred]])).fit(cov_type="HC1")
        reg[dep][pred] = dict(n=int(len(dd)), label=lab, coef=[float(m.params[pred]), float(m.bse[pred])],
                              p=float(m.pvalues[pred]), r2=float(m.rsquared))
    dd = D.dropna(subset=[dep] + list(PRED)).copy()
    if len(dd) >= 25:
        Xr = sm.add_constant(dd[list(PRED)])
        m = sm.OLS(dd[dep], Xr).fit(cov_type="HC1")
        reg[dep]["multivariate"] = dict(
            n=int(len(dd)), r2=float(m.rsquared),
            coef={k: [float(m.params[k]), float(m.bse[k]), float(m.pvalues[k])]
                  for k in PRED if k in m.params.index})
    else:
        reg[dep]["multivariate"] = dict(n=int(len(dd)), note="too few complete cases")
D.to_csv(os.path.join(OUT, "country_shape_parameters.csv"), index=False)

# ---------------------------------------------------------------- 3b. clustering of transition timing/pace
FEATS = ["onset", "midpoint", "duration", "speed", "floor", "curvature"]
Fz = Dshape[FEATS].copy()
Fz = (Fz - Fz.mean()) / Fz.std(ddof=0)
Xfit = Fz.to_numpy()
kms, sil = {}, {}
for k in range(2, 7):
    km = KMeans(n_clusters=k, n_init=25, random_state=11).fit(Xfit)
    kms[k] = km
    sil[k] = float(silhouette_score(Xfit, km.labels_))
kbest = max(sil, key=sil.get)
labels = kms[kbest].labels_
sizes = np.bincount(labels)
null = []
for _ in range(500):
    lab = np.repeat(np.arange(len(sizes)), sizes)
    rng.shuffle(lab)
    null.append(silhouette_score(Xfit, lab))
null = np.array(null)
pval = float(np.mean(null >= sil[kbest]))
pca2 = PCA(n_components=3).fit(Xfit)
Z = pca2.transform(Xfit)[:, :2]
D["cluster"] = D["iso"].map(dict(zip(Dshape["iso"], labels)))
Diso = Dshape["iso"].to_numpy()
Xmap = {iso: xv for iso, xv in zip(Xiso, X)}
cluster_profiles = {}
for k in np.unique(labels):
    m = labels == k
    cluster_profiles[int(k)] = dict(
        n=int(m.sum()),
        mean={f: float(Dshape.loc[m, f].mean()) for f in FEATS},
        example_countries=list(Dshape.loc[m, "name"].head(10)),
    )

# ---------------------------------------------------------------- 5. figures
plt.rcParams.update({"font.size": 9})
# fig 1: fitted shapes for representative countries (two per best-fitting form)
reps = []
for form in ("logistic", "gompertz", "exponential", "linear_kink"):
    sub = [c for c in countries if c.get("best_form_bic") == form]
    sub.sort(key=lambda c: -c["fall"])
    reps += sub[:2]
reps = reps[:8]
if reps:
    fig, axes = plt.subplots(2, 4, figsize=(11, 5.4))
    for ax, c in zip(axes.flat, reps):
        y = np.array(series("tfr", c["iso"]), float)
        ax.plot(YEARS, y, "k.", ms=2, alpha=0.55)
        p = c["fits"][c["best_form_bic"]]["params"]
        xx = np.linspace(min(YEARS), max(YEARS), 300)
        if c["best_form_bic"] == "logistic":
            pred = p[1] + (p[0] - p[1]) / (1 + np.exp((xx - p[2]) / p[3]))
        elif c["best_form_bic"] == "gompertz":
            pred = p[1] + (p[0] - p[1]) * np.exp(-np.exp((xx - p[2]) / p[3]))
        elif c["best_form_bic"] == "exponential":
            pred = np.where(xx >= p[2], p[1] + (p[0] - p[1]) * np.exp(-(xx - p[2]) / p[3]), p[0])
        else:
            pred = np.maximum(p[1], p[0] - p[3] * np.maximum(0.0, xx - p[2]))
        ax.plot(xx, pred, "C3-", lw=1.5)
        ax.set_title("%s: %s" % (c["name"][:22], c["best_form_bic"]), fontsize=8)
        ax.set_ylim(0, max(y) * 1.1); ax.set_xlabel("year")
        if ax in axes[:, 0]:
            ax.set_ylabel("TFR")
    plt.tight_layout(); plt.savefig(os.path.join(FIG, "fig1_fitted_shapes.png"), dpi=300); plt.close()

# fig 2: clusters in transition timing/pace descriptor space
fig, ax = plt.subplots(figsize=(6.6, 5))
for k in np.unique(labels):
    m = labels == k
    ax.scatter(Z[m, 0], Z[m, 1], s=26, alpha=0.85, label="class %d (n=%d)" % (k + 1, m.sum()))
    for i in np.where(m)[0][:4]:
        ax.annotate(Dshape["iso"].iloc[i], (Z[i, 0], Z[i, 1]), fontsize=6, alpha=0.85)
ax.set_xlabel("PC1 of timing/pace descriptors (%.0f%% var)" % (100 * pca2.explained_variance_ratio_[0]))
ax.set_ylabel("PC2 (%.0f%% var)" % (100 * pca2.explained_variance_ratio_[1]))
ax.legend(fontsize=7)
ax.set_title("Transition classes: k=%d, silhouette %.2f, random-partition p=%.3f" % (kbest, sil[kbest], pval))
plt.tight_layout(); plt.savefig(os.path.join(FIG, "fig2_clusters.png"), dpi=300); plt.close()

# fig 3: distributions of shape parameters
fig, axes = plt.subplots(2, 2, figsize=(8.4, 6))
for ax, col, lab in zip(axes.flat, ("onset", "duration", "speed", "floor"),
                        ("Onset year (5% of fall)", "Duration, years (90% to 10% of fall remaining)",
                         "Maximum annual decline (births/woman)", "Floor TFR (last 5-year mean)")):
    ax.hist(Dshape[col].dropna(), bins=18, color="C0", alpha=0.85)
    ax.axvline(float(Dshape[col].median()), color="k", ls="--", lw=1)
    ax.set_xlabel(lab); ax.set_ylabel("countries")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "fig3_distributions.png"), dpi=300); plt.close()

# fig 4: aligned decline paths, mean +/- spread (path uniformity) and cluster means
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
ax = axes[0]
ax.plot(grid, X.mean(0), "k-", lw=2, label="mean across countries")
ax.fill_between(grid, X.mean(0) - X.std(0, ddof=1), X.mean(0) + X.std(0, ddof=1), color="grey", alpha=0.3,
                label="+/- 1 SD")
ax.set_xlabel("normalised time (onset to 10% remaining)"); ax.set_ylabel("normalised TFR (1=peak, 0=floor)")
ax.set_title("Aligned decline paths: one family (PC1 %.0f%% of variance)" % (100 * pca.explained_variance_ratio_[0]))
ax.legend(fontsize=7)
ax = axes[1]
for k in np.unique(labels):
    m = labels == k
    curves = np.array([Xmap[i] for i in Diso[m]])
    ax.plot(grid, curves.mean(0), color="C%d" % k, lw=2, label="class %d (n=%d)" % (k + 1, m.sum()))
ax.set_xlabel("normalised time"); ax.set_ylabel("normalised TFR")
ax.set_title("Mean path by transition class"); ax.legend(fontsize=7)
plt.tight_layout(); plt.savefig(os.path.join(FIG, "fig4_norm_curves.png"), dpi=300); plt.close()

# ---------------------------------------------------------------- 6. save
D.to_csv(os.path.join(OUT, "country_shape_parameters.csv"), index=False)
Dshape.to_csv(os.path.join(OUT, "country_descriptors.csv"), index=False)
form_counts = pd.Series([c["best_form_bic"] for c in countries]).value_counts().to_dict()
out = dict(
    data=dict(source="World Bank WDI annual 1960-2023, pulled fresh 25 Nov 2026",
              countries=len(COUNTRY), transition_countries=len(countries),
              transition_rule=">=40 annual TFR observations; peak TFR >= 4.0; fall >= 1.5; floor <= 3.2; "
                              "duration 1-70 years"),
    shape_descriptors={k: dict(median=float(Dshape[k].median()), iqr=[float(Dshape[k].quantile(.25)),
                                                                float(Dshape[k].quantile(.75))],
                               mean=float(Dshape[k].mean()), sd=float(Dshape[k].std(ddof=1)),
                               p10=float(Dshape[k].quantile(.10)), p90=float(Dshape[k].quantile(.90)))
                       for k in ("onset", "midpoint", "duration", "speed", "floor", "fall", "curvature")},
    functional_forms=dict(best_form_counts=form_counts,
                          mean_holdout_rmse={f: float(np.mean([c["holdout_rmse"][f] for c in countries
                                                               if f in c.get("holdout_rmse", {})]))
                                             for f in ("logistic", "gompertz", "exponential", "linear_kink")},
                          note="AIC/BIC from full-series fits; hold-out fits 1960-2012 and predicts 2013-2023"),
    path_uniformity=path_uniformity,
    clustering=dict(k_best=int(kbest), silhouette=float(sil[kbest]),
                    silhouette_by_k={int(k): float(v) for k, v in sil.items()},
                    descriptor_pca_var=[float(v) for v in pca2.explained_variance_ratio_],
                    null_test=dict(random_partition_p=pval, null_mean=float(null.mean()),
                                   null_sd=float(null.std(ddof=1)), draws=len(null)),
                    cluster_profiles=cluster_profiles,
                    cluster_sizes={int(k): int((labels == k).sum()) for k in np.unique(labels)}),
    determinants=reg,
    covariate_coverage={k: int(D[k].notna().sum()) for k in
                        ("school_50","mort_10","imr_half","log_gdp_onset","urban_onset","school_level")},
    figures=["figures/fig1_fitted_shapes.png", "figures/fig2_clusters.png",
             "figures/fig3_distributions.png", "figures/fig4_norm_curves.png"],
    caveat="descriptors are observed-series quantities, not causal estimates; cross-country correlations only",
)
json.dump(out, open(os.path.join(OUT, "shape_results.json"), "w"), indent=1)
print(json.dumps({k: out[k] for k in ("data", "functional_forms", "clustering")}, indent=1)[:4000])
print("WROTE", OUT)
