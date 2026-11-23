#!/usr/bin/env python3
"""The full demographic transition, 1750-2024: long-run series, pre-antibiotic
corner, onsets, and the mortality-leads-fertility test.

Data (all downloaded from Our World in Data on 2026-11-23 with a browser user
agent; raw CSVs in raw/, citations in the README):
  child-mortality            under-5 deaths per 100 live births, 1751-2024
                             (Gapminder reconstructions before 1950, UN IGME after)
  child-mortality-complete-gapminder  same measure, 1800-2024 (Gapminder full)
  child-mortality-igme       under-5 deaths, 1931-2024 (UN IGME, observed/model)
  life-expectancy            years, 1543-2023
  effective-fertility-rate   children per woman expected to survive to
                             childbearing age, 1751-2023 (Malani & Jacob / OWID)
  children-per-woman         total fertility rate, 1950-2023 (UN WPP)
  mean-years-of-schooling    average years of education, 1870-2020
  gdp-per-capita-maddison    income per head (1990 int$), 1700-2022
  share-of-population-urban  share urban, 1950-2025

The implied pre-1950 total fertility rate is DERIVED, not observed:
  implied TFR = effective fertility / survival to childbearing,
  survival ~= 1 - 1.10 * child_mortality/100   (approximation, labelled everywhere).
It is used only for description and for a long-run sensitivity test; the headline
lead-lag test uses observed UN data from 1950.
"""
import csv, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = "/root/work/transition/raw"
OUT = "/root/work/transition/out"
FIG = "/root/work/transition/figures"
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIG, exist_ok=True)


def load(fname, col=None, minyear=0):
    rows = list(csv.DictReader(open(os.path.join(RAW, fname))))
    cols = [c for c in rows[0] if c not in ("entity", "code", "year")]
    c = col or cols[0]
    d = {}
    for r in rows:
        try:
            iso, y, v = r["code"], int(float(r["year"])), r[c]
            if iso and len(iso) == 3 and y >= minyear and v not in (None, ""):
                d[(iso, y)] = float(v)
        except (TypeError, ValueError, KeyError):
            pass
    return d


CM = load("child-mortality.csv")
CMG = load("child-mortality-complete-gapminder.csv")
CMI = load("child-mortality-igme.csv")
LE = load("life-expectancy.csv")
EFR = load("effective-fertility-rate-children-per-woman-who-are-expected-to-survive-until-childbearing-age.csv")
TFR = load("children-per-woman.csv")
CBR = load("crude-birth-rate.csv")
MYS = load("mean-years-of-schooling.csv")
GDP = load("gdp-per-capita-maddison-project-database.csv", minyear=1700)
URB = load("share-of-population-urban.csv")

META = json.load(open("/root/work/data/meta.json"))
REGION = {i: (m.get("region") or "").strip() for i, m in META.items()}

# fall back to the complete Gapminder series where the main series is missing
for k, v in CMG.items():
    CM.setdefault(k, v)
for k, v in CMI.items():
    CMI.setdefault(k, v)  # no-op, keeps name for clarity


def survival_cm(cm_pct):
    """Survival to childbearing age from under-5 mortality (per 100 live births)."""
    return max(1.0 - 1.10 * cm_pct / 100.0, 0.20)


TFR_IMP = {}
for (i, t), e in EFR.items():
    cm = CM.get((i, t))
    if cm is None:            # use nearest child-mortality year within 5 years
        cand = [v for (i2, t2), v in CM.items() if i2 == i and abs(t2 - t) <= 5]
        cm = float(np.median(cand)) if cand else None
    if cm is not None and e > 0:
        TFR_IMP[(i, t)] = e / survival_cm(cm)

YEARS = [i for i in range(1800, 2025)]
COUNTRIES8 = {"GBR": "England & Wales", "SWE": "Sweden", "FRA": "France", "JPN": "Japan",
              "IND": "India", "CHN": "China", "KEN": "Kenya", "BRA": "Brazil"}


def series(d, iso, lo=1750, hi=2024):
    return [(t, d[(iso, t)]) for t in range(lo, hi + 1) if (iso, t) in d]


def onset(d, iso, drop=0.10, sustain=10, lo=1750, min_pts=25):
    """Onset of the durable decline, measured against the series' own peak.

    The peak of the series so far is used as the reference (not a fixed early
    baseline), so the answer does not depend on how much early data a country has.
    Onset = first year whose value is at least 10% below the running peak AND
    whose next ten-year median is also at least 10% below the running peak.
    """
    pts = series(d, iso, lo)
    if len(pts) < min_pts:
        return None
    peak = -np.inf
    peak_t = None
    for j, (t, v) in enumerate(pts):
        if v > peak:
            peak, peak_t = v, t
        window = [x for _, x in pts[j:j + sustain]]
        if (len(window) >= sustain and v <= 0.9 * peak
                and v < peak and np.median(window) <= 0.9 * peak
                and t - (peak_t or t) >= 0):
            return dict(onset=t, peak=float(peak), peak_year=int(peak_t),
                        value=float(v), share_fall=float(1 - v / peak))
    return None


# ---------- 1. pre-antibiotic corner ----------
def _country_medians(d, lo, hi):
    by = {}
    for (i, t), v in d.items():
        if lo <= t < hi and i in REGION:
            by.setdefault(i, []).append(v)
    return {i: float(np.median(vs)) for i, vs in by.items() if len(vs) >= 2}


def period_stats(lo, hi):
    cm = list(_country_medians(CM, lo, hi).values())
    ef = list(_country_medians(EFR, lo, hi).values())
    le = list(_country_medians(LE, lo, hi).values())
    return dict(n_countries_cm=len(cm),
                median_cm=round(float(np.median(cm)), 1) if cm else None,
                iqr_cm=[round(float(np.percentile(cm, 25)), 1),
                        round(float(np.percentile(cm, 75)), 1)] if cm else None,
                n_countries_efr=len(ef),
                median_efr=round(float(np.median(ef)), 2) if ef else None,
                n_countries_le=len(le),
                median_le=round(float(np.median(le)), 1) if le else None)


CORNERS = {f"{lo}-{hi}": period_stats(lo, hi) for lo, hi in
           [(1700, 1800), (1800, 1850), (1850, 1900), (1900, 1940), (1940, 1980), (1980, 2024)]}
IMPLIED_TFR_PERIODS = {}
for lo, hi in [(1800, 1850), (1850, 1900), (1900, 1940), (1940, 1980), (1980, 2024)]:
    vals = [v for (i, t), v in TFR_IMP.items()
            if lo <= t < hi and i in REGION and np.isfinite(v) and 0 < v < 15]
    IMPLIED_TFR_PERIODS[f"{lo}-{hi}"] = dict(
        n_country_years=len(vals),
        median=round(float(np.median(vals)), 2) if vals else None)
print("implied TFR by period (derived, not observed):", json.dumps(IMPLIED_TFR_PERIODS, indent=1))
print("pre-antibiotic / period stats:", json.dumps(CORNERS, indent=1))

# ---------- 2. onsets and lags ----------
ONSETS = {}
for iso in sorted({i for (i, t) in CM if i in REGION}):
    mo = onset(CM, iso)
    fo = onset(TFR, iso, lo=1950)                            # observed TFR, 1950+
    fi = onset(TFR_IMP, iso)                                # implied TFR, long-run
    mo_obs = onset(CMI, iso, lo=1950)                        # observed-era mortality
    if any([mo, fo, fi, mo_obs]):
        ONSETS[iso] = dict(mort_long=mo, mort_obs=mo_obs, fert_obs=fo, fert_implied=fi,
                           region=REGION.get(iso, ""))

lags_obs, lags_long = [], []
for iso, o in ONSETS.items():
    if o["mort_obs"] and o["fert_obs"]:
        lags_obs.append(dict(iso=iso, lag=o["fert_obs"]["onset"] - o["mort_obs"]["onset"],
                             mort=o["mort_obs"]["onset"], fert=o["fert_obs"]["onset"]))
    if o["mort_long"] and o["fert_implied"]:
        lags_long.append(dict(iso=iso, lag=o["fert_implied"]["onset"] - o["mort_long"]["onset"],
                              mort=o["mort_long"]["onset"], fert=o["fert_implied"]["onset"]))


def lag_stats(lags):
    if not lags:
        return dict(n=0)
    x = np.array([l["lag"] for l in lags], float)
    return dict(n=len(x), median=float(np.median(x)),
                q25=float(np.percentile(x, 25)), q75=float(np.percentile(x, 75)),
                share_positive=float((x > 0).mean()), min=float(x.min()), max=float(x.max()))


LAGS = dict(observed_1950plus=lag_stats(lags_obs), long_run_implied=lag_stats(lags_long))
# split the long-run lags by mortality-onset era
pre = [l for l in lags_long if l["mort"] < 1950]
post = [l for l in lags_long if l["mort"] >= 1950]
LAGS["long_run_pre1950_onset"] = lag_stats(pre)
LAGS["long_run_post1950_onset"] = lag_stats(post)
clean = [l for l in lags_obs if l["mort"] >= 1950 and l["fert"] >= 1950]
LAGS["clean_observed_both_onsets_1950plus"] = lag_stats(clean)
# late transitioners only: total fertility still at 4+ in 1950, so the 1950+
# series captures the transition rather than a late baby-boom correction
late = [l for l in lags_obs if TFR.get((l["iso"], 1950), 0) >= 4.0]
LAGS["late_transitioners_only"] = lag_stats(late)
# region medians for the observed test
REG_LAGS = {}
for l in lags_obs:
    REG_LAGS.setdefault(REGION.get(l["iso"], "other"), []).append(l["lag"])
LAGS["by_region"] = {k: dict(n=len(v), median=float(np.median(v)))
                     for k, v in sorted(REG_LAGS.items()) if len(v) >= 5}
print("lag stats:", json.dumps(LAGS, indent=1))

# ---------- 3. cross-correlations of 20-year changes ----------
def step_change(d, iso, step=20):
    s = series(d, iso)
    out = {}
    for t, v in s:
        if (iso, t + step) in d:
            try:
                out[t] = np.log(d[(iso, t + step)] / v)
            except (ValueError, ZeroDivisionError):
                pass
    return out


def lead_lag_corr(dm, df, maxlag=40):
    lags, cors = [], []
    for lag in range(-maxlag, maxlag + 1, 5):
        a, b = [], []
        for t, dmv in dm.items():
            if (t + lag) in df:
                a.append(dmv); b.append(df[t + lag])
        if len(a) >= 15:
            lags.append(lag); cors.append(float(np.corrcoef(a, b)[0, 1]))
    if not cors:
        return None
    corr0 = cors[lags.index(0)] if 0 in lags else None
    j = int(np.argmax(cors))            # strongest POSITIVE co-movement
    return dict(best_lag=lags[j], best_corr=cors[j], corr_lag0=corr0, n=len(cors))


CROSS = {"observed_tfr": [], "implied_tfr": []}
for iso in {i for (i, t) in CM if i in REGION}:
    dm = step_change(CM, iso)
    df_obs = step_change(TFR, iso)
    r = lead_lag_corr(dm, df_obs)
    if r:
        CROSS["observed_tfr"].append(dict(iso=iso, **r))
    df_imp = step_change(TFR_IMP, iso)
    r2 = lead_lag_corr(dm, df_imp)
    if r2:
        CROSS["implied_tfr"].append(dict(iso=iso, **r2))
CROSS_SUM = {k: dict(
    n=len(v),
    median_best_lag=float(np.median([x["best_lag"] for x in v])) if v else None,
    share_best_lag_positive=float(np.mean([x["best_lag"] > 0 for x in v])) if v else None,
    median_corr_lag0=float(np.median([x["corr_lag0"] for x in v if x["corr_lag0"] is not None])) if v else None,
    share_corr_lag0_above_half=float(np.mean([x["corr_lag0"] > 0.5 for x in v if x["corr_lag0"] is not None])) if v else None)
    for k, v in CROSS.items()}
print("cross-correlation summary:", json.dumps(CROSS_SUM, indent=1))

# ---------- 4. schooling vs fertility timing ----------
SCHOOL = {}
rows = []
for iso, o in ONSETS.items():
    fo = o["fert_obs"]
    if not fo:
        continue
    for thr in (2.0, 6.0):
        cross = next((t for t, v in series(MYS, iso, 1870) if v >= thr), None)
        if cross:
            rows.append(dict(iso=iso, threshold=thr, school_year=cross,
                             fert_onset=fo["onset"], gap=fo["onset"] - cross))
for thr in (2.0, 6.0):
    g = [r["gap"] for r in rows if r["threshold"] == thr]
    if g:
        SCHOOL[f"school_crosses_{thr}y"] = dict(n=len(g), median_gap=float(np.median(g)),
                                                q25=float(np.percentile(g, 25)),
                                                q75=float(np.percentile(g, 75)),
                                                share_after_fertility_onset=float(np.mean(np.array(g) < 0)))
print("schooling vs fertility onset:", json.dumps(SCHOOL, indent=1))

# ---------- 5. event study around each country's mortality onset ----------
EVENT = {}
ev = []
for iso, o in ONSETS.items():
    if not (o["mort_long"] and o["fert_implied"]):
        continue
    t0 = o["mort_long"]["onset"]
    base = np.median([v for t, v in series(TFR_IMP, iso, t0 - 20, t0 - 1)])
    if not np.isfinite(base) or base <= 0:
        continue
    for dt in range(-40, 61, 10):
        v = TFR_IMP.get((iso, t0 + dt))
        if v and np.isfinite(v):
            ev.append((dt, v / base))
if ev:
    EVENT = {dt: dict(n=int(sum(1 for d, _ in ev if d == dt)),
                      mean_ratio=float(np.mean([r for d, r in ev if d == dt])))
             for dt in sorted({d for d, _ in ev})}
print("event study (fertility / pre-onset baseline by years since mortality onset):",
      json.dumps(EVENT, indent=1))

# ---------- 6. figures ----------
COLORS = {"GBR": "#1f77b4", "SWE": "#ff7f0e", "FRA": "#2ca02c", "JPN": "#d62728",
          "IND": "#9467bd", "CHN": "#8c564b", "KEN": "#e377c2", "BRA": "#7f7f7f"}
plt.rcParams.update({"font.size": 9, "axes.titlesize": 10})


def xy(iso, d_cm, d_y, lo=1800, hi=2024):
    return [(t, d_cm[(iso, t)], d_y[(iso, t)]) for t in range(lo, hi + 1)
            if (iso, t) in d_cm and (iso, t) in d_y]


fig, ax = plt.subplots(figsize=(8.8, 5.9))
for iso, name in COUNTRIES8.items():
    pts = xy(iso, CM, EFR)
    if not pts:
        continue
    ax.plot([p[1] for p in pts], [p[2] for p in pts], "-", color=COLORS[iso], lw=1.5,
            alpha=0.9, label=name)
    ax.scatter([pts[0][1]], [pts[0][2]], color=COLORS[iso], s=16, zorder=5)
    ax.scatter([pts[-1][1]], [pts[-1][2]], color=COLORS[iso], s=26, zorder=6)
ax.axvspan(20, 45, color="0.93", zorder=0)
ax.axvspan(0, 2.5, color="0.90", zorder=0)
ax.annotate("pre-antibiotic corner\n(most countries before c. 1940)\nhigh child mortality, moderate surviving fertility",
            xy=(33, 5.9), fontsize=8, color="0.25", ha="center", va="top")
ax.annotate("collapse corner\n(rich countries after c. 1980)\nlow child mortality, fertility below 2",
            xy=(1.2, 0.55), xytext=(9.5, 0.75), fontsize=8, color="0.25",
            arrowprops=dict(arrowstyle="->", color="0.35", lw=0.9))
ax.annotate("effective fertility can RISE early:\nmore children survive, even while births\nper woman are unchanged",
            xy=(25, 4.1), xytext=(28, 3.2), fontsize=7.5, color="0.35",
            arrowprops=dict(arrowstyle="->", color="0.5", lw=0.8))
ax.set_xlabel("under-5 mortality (deaths per 100 live births)")
ax.set_ylabel("effective fertility (children per woman surviving to childbearing)")
ax.set_title("Phase diagram of the demographic transition, 1800-2024\n"
             "each country's trajectory runs left and down; dot = earliest point, larger dot = latest")
ax.legend(fontsize=7.5, loc="center left", bbox_to_anchor=(1.005, 0.5), frameon=False)
ax.set_xlim(0, 50); ax.set_ylim(0.5, 6.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_a_phase_diagram.png"), dpi=170)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5), sharex=True)
for iso, name in COUNTRIES8.items():
    cm = [(t, v) for t, v in series(CM, iso)]
    if cm:
        axes[0].plot([t for t, _ in cm], [v for _, v in cm], color=COLORS[iso], lw=1.3, label=name)
    ef = series(EFR, iso)
    if ef:
        axes[1].plot([t for t, _ in ef], [v for _, v in ef], color=COLORS[iso], lw=1.4)
    tf = series(TFR, iso, 1950)
    if tf:
        axes[1].plot([t for t, _ in tf], [v for _, v in tf], color=COLORS[iso], lw=1.1, ls=":", alpha=0.75)
axes[0].set_ylabel("under-5 deaths per 100 live births")
axes[0].set_title("Child mortality, 1800-2024 (reconstructions before 1950, UN estimates after)\n"
                  "vertical jumps are splice years between sources, not history")
axes[1].set_ylabel("children per woman")
axes[1].set_title("Fertility: effective (solid, surviving children per woman)\n"
                  "dotted = observed total fertility rate (UN, 1950+)")
axes[1].set_ylim(0, 9)
for a_ in axes:
    a_.set_xlabel("year"); a_.grid(alpha=0.25)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, fontsize=8, ncol=4, frameon=False, loc="lower center",
           bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig(os.path.join(FIG, "fig_b_time_series.png"), dpi=170, bbox_inches="tight")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
axes[0].hist([l["lag"] for l in lags_long], bins=range(-80, 131, 10), color="#1f77b4", alpha=0.85)
axes[0].axvline(0, color="k", lw=1)
axes[0].set_title(f"Long-run reconstruction (implied fertility), n={len(lags_long)}\n"
                  "derived series - onset dates are approximate")
axes[0].set_xlabel("years from child-mortality decline onset to fertility decline onset")
axes[0].set_ylabel("countries")
med = LAGS["long_run_implied"].get("median")
if med is not None:
    axes[0].axvline(med, color="red", ls="--", lw=1, label=f"median {med:+.0f}y")
    axes[0].legend(fontsize=8, frameon=False)
axes[1].hist([l["lag"] for l in lags_obs], bins=range(-80, 131, 10), color="#ff7f0e", alpha=0.9)
axes[1].axvline(0, color="k", lw=1)
med2 = LAGS["observed_1950plus"].get("median")
axes[1].set_title(f"Observed UN data, mortality onset 1950+, n={len(lags_obs)}\n"
                  "late transitioners: total fertility >= 4 in 1950")
axes[1].set_xlabel("years from child-mortality decline onset to fertility decline onset")
if med2 is not None:
    axes[1].axvline(med2, color="red", ls="--", lw=1, label=f"median {med2:+.0f}y")
    axes[1].legend(fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_c_lag_distribution.png"), dpi=170)
plt.close(fig)

# small label offsets only (no leader lines); the colour legend identifies the
# five early transitioners that converge in the collapse corner
LBL = {"CHN": (8, -13), "IND": (8, 6), "KEN": (8, 6), "BRA": (8, -12)}
fig, ax = plt.subplots(figsize=(8.8, 5.9))
for iso, name in COUNTRIES8.items():
    pts = xy(iso, CM, EFR)
    if not pts:
        continue
    ax.plot([p[1] for p in pts], [p[2] for p in pts], "-", color=COLORS[iso], lw=1.0,
            alpha=0.55, label=name)
    ax.scatter([pts[-1][1]], [pts[-1][2]], color=COLORS[iso], s=30, zorder=6)
    if iso in LBL:
        ax.annotate(name, (pts[-1][1], pts[-1][2]), fontsize=8, color=COLORS[iso],
                    xytext=LBL[iso], textcoords="offset points")
ax.axvspan(25, 45, color="#f2f2f2", zorder=0)
ax.axvspan(0, 2.5, color="#e9e9e9", zorder=0)
ax.text(35, 5.9, "PRE-ANTIBIOTIC CORNER\nhigh child mortality, moderate-to-high\nfertility; most countries before c. 1940",
        ha="center", va="top", fontsize=8.5)
ax.text(8.5, 0.62, "COLLAPSE CORNER\nlow child mortality, fertility below two;\nrich countries after c. 1980",
        ha="left", va="bottom", fontsize=8.5)
ax.annotate("China/Kenya jumps: source splice", xy=(30, 4.6), xytext=(33, 3.6), fontsize=7,
            color="0.4", arrowprops=dict(arrowstyle="->", color="0.5", lw=0.7))
ax.set_xlabel("under-5 mortality (deaths per 100 live births)")
ax.set_ylabel("effective fertility (surviving children per woman)")
ax.set_title("The two corners of the transition, annotated (larger dot = latest observation)")
ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1.005, 0.5), frameon=False)
ax.set_xlim(0, 50); ax.set_ylim(0.5, 6.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_d_corners_annotated.png"), dpi=170)
plt.close(fig)

# ---------- 7. write outputs ----------
json.dump(dict(corners=CORNERS, implied_tfr_periods=IMPLIED_TFR_PERIODS,
               onsets=ONSETS, lag_stats=LAGS,
               cross_correlation=CROSS_SUM, schooling=SCHOOL, event_study=EVENT),
          open(os.path.join(OUT, "transition_results.json"), "w"), indent=1, default=str)

# tidy long-run panel CSV (small)
with open(os.path.join(OUT, "long_run_panel.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["iso3", "year", "child_mortality_per100", "life_expectancy_years",
                "effective_fertility", "tfr_observed_1950plus", "tfr_implied_derived",
                "mean_years_schooling", "gdp_pc_maddison_1990int", "urban_share_pct",
                "cm_source"])
    for iso in sorted({i for (i, t) in CM if i in REGION}):
        for t in range(1750, 2025):
            row = [iso, t, CM.get((iso, t)), LE.get((iso, t)), EFR.get((iso, t)),
                   TFR.get((iso, t)), None if (t < 1950) else TFR_IMP.get((iso, t)),
                   MYS.get((iso, t)), GDP.get((iso, t)), URB.get((iso, t)),
                   ("gapminder_reconstruction" if t < 1950 else "un_igme_estimate")]
            if any(v is not None for v in row[2:-1]):
                w.writerow(row)

with open(os.path.join(OUT, "onsets.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["iso3", "region", "mort_decline_onset_longrun", "mort_decline_onset_observed",
                "fert_decline_onset_observed", "fert_decline_onset_implied",
                "lag_observed_years", "lag_implied_years"])
    for iso, o in sorted(ONSETS.items()):
        lo = (o["fert_obs"]["onset"] - o["mort_obs"]["onset"]) if (o["fert_obs"] and o["mort_obs"]) else None
        li = (o["fert_implied"]["onset"] - o["mort_long"]["onset"]) if (o["fert_implied"] and o["mort_long"]) else None
        w.writerow([iso, o["region"],
                    o["mort_long"]["onset"] if o["mort_long"] else None,
                    o["mort_obs"]["onset"] if o["mort_obs"] else None,
                    o["fert_obs"]["onset"] if o["fert_obs"] else None,
                    o["fert_implied"]["onset"] if o["fert_implied"] else None, lo, li])

print("\nfigures:", sorted(os.listdir(FIG)))
print("wrote", OUT, "and", FIG)
