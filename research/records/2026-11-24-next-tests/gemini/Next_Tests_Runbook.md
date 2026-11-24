# Next-Tests Runbook & Parameters (Public Data & Local/Server Compute)

Ready-to-run specifications and starter scripts for the five open questions across **Methods**, **Fertility Audit (F + N2)**, **Sequencing (N1)**, **Transition Shape (N4)**, and the **DHS Stratum Check**.

---

## Test 1 — Orthogonalized `t+10` Placebo & Without-Trends Table 1 (Fertility Audit)

* **Where to run:** Local or `box2` (`ssh autodl2`) against `/root/work/data` (or `research/records/2026-11-23-corr-battery/`).
* **Goal:** Test whether future schooling (`S_{t+10}`) still predicts current fertility (`F_t`) once current schooling (`S_t`) is partialled out, and add `ΔF ~ ΔS` and without-country-trends columns to Table 1.

### Parameters
* **Outcome:** `tfr` (levels `F_{i,t}` and 10-year change `F_{i,t+10} - F_{i,t}`).
* **Schooling measures (8):** `yr_sch_fem`, `yr_sch_tot`, `sec_enr`, `lsec_comp`, `prm_comp`, `ter_enr`, `ter_gpi`, `sec_gpi`.
* **Controls:** `log_gdppc`, `urban_pct`, decade fixed effects, country-clustered SEs.
* **Specifications:**
  1. `F_t ~ dS_future + S_t + controls + FE` where `dS_future = S_{t+10} - S_t`
  2. `F_t ~ resid(S_{t+10} | S_t) + controls + FE`
  3. `(F_{t+10} - F_t) ~ (S_{t+10} - S_t) + controls + country_FE + decade_FE` (no country linear trends)

### Script (`run_ortho_placebo.py`)
```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Point to the committed panel CSV/parquet in /root/work/data
PANEL_PATH = "/root/work/data/panel_observed.parquet"
SCHOOL_VARS = [
    "yr_sch_fem", "yr_sch_tot", "sec_enr", "lsec_comp",
    "prm_comp", "ter_enr", "ter_gpi", "sec_gpi"
]

df = pd.read_parquet(PANEL_PATH).sort_values(["iso3", "year"])
df["decade"] = (df["year"] // 10) * 10

rows = []
for s in SCHOOL_VARS:
    sub = df[["iso3", "year", "decade", "tfr", "log_gdppc", "urban_pct", s]].dropna().copy()
    sub["s_fut"] = sub.groupby("iso3")[s].shift(-10)
    sub["tfr_fut"] = sub.groupby("iso3")["tfr"].shift(-10)
    sub["ds_fut"] = sub["s_fut"] - sub[s]
    sub["dtfr"] = sub["tfr_fut"] - sub["tfr"]

    # 1) Orthogonalized future innovation controlling for S_t
    d1 = sub.dropna(subset=["ds_fut", "tfr", "log_gdppc", "urban_pct"]).copy()
    m1 = smf.ols(
        f"tfr ~ ds_fut + {s} + log_gdppc + urban_pct + C(decade)", data=d1
    ).fit(cov_type="cluster", cov_kwds={"groups": d1["iso3"]})

    # 2) Pure residualized S_{t+10} | S_t
    aux = smf.ols(f"s_fut ~ {s}", data=d1).fit()
    d1["s_fut_resid"] = aux.resid
    m2 = smf.ols(
        "tfr ~ s_fut_resid + log_gdppc + urban_pct + C(decade)", data=d1
    ).fit(cov_type="cluster", cov_kwds={"groups": d1["iso3"]})

    # 3) Change-on-change without country linear trends
    d3 = sub.dropna(subset=["dtfr", "ds_fut", "log_gdppc", "urban_pct"]).copy()
    m3 = smf.ols(
        "dtfr ~ ds_fut + log_gdppc + urban_pct + C(iso3) + C(decade)", data=d3
    ).fit(cov_type="cluster", cov_kwds={"groups": d3["iso3"]})

    rows.append({
        "schooling": s,
        "n_ortho": len(d1),
        "b_ds_fut": m1.params["ds_fut"], "se_ds_fut": m1.bse["ds_fut"], "p_ds_fut": m1.pvalues["ds_fut"],
        "b_s_resid": m2.params["s_fut_resid"], "se_s_resid": m2.bse["s_fut_resid"], "p_s_resid": m2.pvalues["s_fut_resid"],
        "b_dF_dS_notrend": m3.params["ds_fut"], "se_dF_dS_notrend": m3.bse["ds_fut"], "p_dF_dS_notrend": m3.pvalues["ds_fut"],
    })

pd.DataFrame(rows).to_csv("ortho_placebo_results.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False))
```

---

## Test 2 — Pre-1960 Complete-Transition Benchmark (Paper N4)

* **Where to run:** Any machine with internet access (100% public OWID/Gapminder CSV, no login).
* **Goal:** Test whether exponential-to-floor still beats logistic when pre-transition plateaus (1800–1960) are observed.

### Parameters
* **Public source:** `https://ourworldindata.org/grapher/children-born-per-woman.csv?v=1&csvType=full&useColumnShortNames=true`
* **Benchmark countries (12 early transitioners):** `SWE, FRA, GBR, USA, JPN, DEU, NLD, CHE, NOR, DNK, AUS, CAN`
* **Window:** `1800–2023` (training `1800–2013`, hold-out `2014–2023`).
* **Models:** `logistic` (4-param), `gompertz` (4-param), `exp_floor` (3-param: `floor + (start - floor)*exp(-k*(t - t0))`), `linear_kink` (4-param).

### Script (`run_n4_pre1960.py`)
```python
import numpy as np
import pandas as pd
from scipy.optimize import least_squares

URL = "https://ourworldindata.org/grapher/children-born-per-woman.csv?v=1&csvType=full&useColumnShortNames=true"
COUNTRIES = ["SWE", "FRA", "GBR", "USA", "JPN", "DEU", "NLD", "CHE", "NOR", "DNK", "AUS", "CAN"]

df = pd.read_csv(URL)
tfr_col = [c for c in df.columns if c not in ("Entity", "Code", "Year")][0]
df = df[df["Code"].isin(COUNTRIES) & df["Year"].between(1800, 2023)].rename(columns={tfr_col: "tfr"})

def bic(n, rss, k):
    return n * np.log(max(rss / n, 1e-12)) + k * np.log(n)

def fit_models(years, y):
    t = years - years[0]
    res = {}
    # 1. Logistic: floor + (ceil - floor) / (1 + exp(k*(t - tmid)))
    f_log = lambda p: p[0] + (p[1] - p[0]) / (1.0 + np.exp(np.clip(p[2] * (t - p[3]), -50, 50))) - y
    r = least_squares(f_log, [1.6, y[:10].mean(), 0.05, len(t) * 0.5], bounds=([0.5, 2.0, 0.001, 0], [4.0, 9.0, 0.5, len(t)]))
    res["logistic"] = (bic(len(y), np.sum(r.fun**2), 4), r)

    # 2. Gompertz: floor + (ceil - floor) * exp(-exp(k*(t - tmid)))
    f_gomp = lambda p: p[0] + (p[1] - p[0]) * np.exp(-np.exp(np.clip(p[2] * (t - p[3]), -50, 50))) - y
    r = least_squares(f_gomp, [1.6, y[:10].mean(), 0.03, len(t) * 0.5], bounds=([0.5, 2.0, 0.001, 0], [4.0, 9.0, 0.5, len(t)]))
    res["gompertz"] = (bic(len(y), np.sum(r.fun**2), 4), r)

    # 3. Exponential-to-floor (free onset t0)
    f_exp = lambda p: np.where(t < p[3], p[1], p[0] + (p[1] - p[0]) * np.exp(-p[2] * (t - p[3]))) - y
    r = least_squares(f_exp, [1.6, y[:10].mean(), 0.03, len(t) * 0.3], bounds=([0.5, 2.0, 0.001, 0], [4.0, 9.0, 0.5, len(t)]))
    res["exp_floor"] = (bic(len(y), np.sum(r.fun**2), 4), r)

    return min(res, key=lambda k: res[k][0]), {k: v[0] for k, v in res.items()}

out = []
for iso, g in df.groupby("Code"):
    g = g.sort_values("Year").dropna(subset=["tfr"])
    winner, bics = fit_models(g["Year"].to_numpy(float), g["tfr"].to_numpy(float))
    out.append({"iso3": iso, "start_yr": int(g["Year"].min()), "n_yrs": len(g), "bic_winner": winner, **bics})

print(pd.DataFrame(out).to_string(index=False))
```

---

## Test 3 — 1,200-Draw BY Multiverse + §6.8 Known-Truth Simulation (Methods Paper)

* **Where to run:** `box2` (`ssh autodl2`) using `/root/work/data` and `/root/work/groups/out/final400.pkl`.
* **Goal:** Clear the Benjamini–Yekutieli cluster-30 threshold (`~1,120` draws) and benchmark empirical Type-I error and power on synthetic DGPs.

### Parameters
* **Draw budget (`E1`):** `R = 1200` (`seed = 1000 + r`, `r = 1..1200`; reuse `r = 1..400` from `final400.pkl`, compute `r = 401..1200`, ~3–4 hrs on 16 workers).
* **BY threshold:** `M = 272` links, `H_272 = 6.185`, `alpha_BY = 0.05 / 6.185 = 0.00808`. At `R = 1200`, empirical floor is `1/1201 = 0.000833`, clearing BY for any floor cluster of size `j >= 29`.
* **§6.8 Synthetic DGPs (`E2`, `N_rep = 100` panels per DGP, `R_sim = 400` draws per panel):**
  1. `DGP_NULL`: `beta = 0.00` across all groups (checks empirical false-positive rate of `travels` / `group_specific`).
  2. `DGP_UNIFORM`: `beta = -0.05` across all countries, `AR(1) rho = 0.85`, `sigma_eps = 0.15` (checks recovery of `travels_everywhere`).
  3. `DGP_GROUP`: `beta = -0.10` in `region == "Sub-Saharan Africa"` (or 1 income tier), `0.00` elsewhere (checks recovery of `group_specific`).

---

## Test 4 — Stratum-Level DHS STATcompiler API Check (Macro Survival vs. ABM Tension)

* **Where to run:** Any machine with internet access (100% public `api.dhsprogram.com`, no registration).
* **Goal:** Check whether the schooling–fertility gradient and cohort attenuation persist *within* wealth quintiles and urban/rural strata.

### Parameters
* **Endpoint:** `https://api.dhsprogram.com/rest/dhs/data`
* **Indicators:** `FE_FRTY_W_TFR` (TFR) and `FE_CEBA_W_CHB` (mean children ever born to women 40–49)
* **Query params:** `breakdown=all`, `perpage=1000` — filter `CharacteristicCategory` in `{"Education", "Wealth quintile", "Residence"}`.

### Script (`pull_dhs_strata.py`)
```python
import requests
import pandas as pd

BASE = "https://api.dhsprogram.com/rest/dhs/data"
PARAMS = {"indicatorIds": "FE_FRTY_W_TFR,FE_CEBA_W_CHB", "breakdown": "all", "perpage": 1000}

all_rows = []
for page in range(1, 30):
    r = requests.get(BASE, params={**PARAMS, "page": page}, timeout=30).json()
    data = r.get("Data", [])
    if not data:
        break
    all_rows.extend(data)
    if page >= r.get("TotalPages", 1):
        break

df = pd.DataFrame(all_rows)
df = df[df["CharacteristicCategory"].isin(["Education", "Wealth quintile", "Residence"])]
df.to_csv("dhs_strata_public.csv", index=False)
print(f"Saved {len(df)} rows across {df['CountryName'].nunique()} countries.")
```

---

## Test 5 — Censoring-Aware Threshold Sweep & `AFG`/`KHM`/`SEN` Audit (Paper N1)

* **Where to run:** Local against `research/records/2026-11-25-paper-sequencing-novel/results/event_dates.csv` and raw WDI/ILOSTAT series.
* **Goal:** Verify stability of `31/34` (`91%`) across threshold definitions, reconcile the `7%` vs. `28%` demand share, and inspect the 3 reverse cases (`AFG`, `KHM`, `SEN`).

### Parameter Grid
* `schooling_delta`: `[0.5, 1.0, 1.5]` years of schooling per 10-year window
* `release_delta`: `[2.0, 3.0, 5.0]` percentage-point drop in agricultural employment share per 10-year window
* `window`: `[(1965, 2010), (1970, 2015)]`
* **Censoring rule:** Any date equal to `window_start` (`schooling`) or `1991` (`release`, ILOSTAT start) is marked `left_censored = True`; compute `identifiable_n`, `schooling_first_n`, `release_first_n`, and `undetermined_n`.
* **Reverse-case inspection:** Print full decadal `yr_sch` and `agri_emp_pct` trajectories for `AFG`, `KHM`, `SEN` (and `MLI`, `MOZ` in the 81-country sample).
* **SSA Fee-Abolition Date Audit (12 countries):** Cross-check abolition year, grade scope, and UNESCO/World Bank/national gazette primary URL for each of the 12 countries in `2026-11-22-massification-panel/scripts/final_tests.py`.
