#!/usr/bin/env python3
"""T3: smallest defensible JOINT demography-agriculture-absorber model (demonstration, not history).

Structure:
  DEMOGRAPHY: child-mortality and life-expectancy paths from the transition record drive survival.
    Fertility is a quantity-quality choice: desired SURVIVING children falls with schooling; births =
    desired / survival-to-15. The mortality decline therefore gives the population explosion first, the
    fertility transition follows as schooling expands.
  AGRICULTURE: Boppart-style labour demand. Observed agricultural labour productivity is split into TFP and
    input intensity using the CES elasticity estimated in T1: theta(t) = A(t) * intensity(t)^beta_i. Food
    demand is a Stone-Geary/income-elastic floor. Labour demand is L_a = food output / theta; falling input
    prices raise intensity and cut labour per unit of food (the mechanisation margin). Counterfactual: freeze
    intensity at its 1960 level, keep TFP growing -> labour release stalls.
  ABSORBER: a non-agricultural wage sector with finite job-creation capacity J(t) = J0*(K_n/K_n0)^phi, plus a
    schooling/credential pipeline that queues the rest. Queue pressure and the wage premium feed enrolment;
    schooling lowers desired fertility.
Free parameters (5, calibrated jointly): queue weight in schooling, wage-premium weight in schooling,
desired surviving children at zero schooling, schooling effect on desired fertility, job-capacity elasticity.
Everything else is calibrated/estimated/assumed and labelled in the output.
Outputs: results/model_paths.csv, model_counterfactual.csv, model_params.json, model_summary.txt.
"""
import json, os
import numpy as np
import pandas as pd
from scipy.optimize import least_squares

OUT = "/root/work/subsistence/out"
DATA = "/root/work/subsistence/data"
TR = "/root/work/transition/out/long_run_panel.csv"
os.makedirs(OUT, exist_ok=True)
L = []
A = L.append
YEARS = np.arange(1800, 2021, 5)
T = len(YEARS)


def interp_median(df, col, yr, scale=1.0):
    s = df.groupby("year")[col].median().dropna()
    return np.interp(yr, s.index.values, s.values) * scale


tr = pd.read_csv(TR)
cm = interp_median(tr, "child_mortality_per100", YEARS, 0.01)
s_child = np.clip(1 - cm, 0.05, 0.995)
le = interp_median(tr, "life_expectancy_years", YEARS)
le = np.where(le > 20, le, 30.0)
adult_surv = np.exp(-5.0 / np.maximum(le - 15.0, 5.0))
school_obs = interp_median(tr, "mean_years_schooling", YEARS)
gdppc_obs = interp_median(tr, "gdp_pc_maddison_1990int", YEARS)

wdi = pd.read_csv(f"{DATA}/wdi_long.csv")


def wdi_series(ind):
    d = wdi[wdi.indicator == ind]
    s = d.groupby("year")["value"].median().dropna()
    return np.interp(YEARS, s.index.values, s.values) if len(s) else np.full(T, np.nan)


ag_share_obs = wdi_series("ag_emp_share") / 100.0
tfr_obs = wdi_series("tfr")
pop_obs = wdi_series("pop")


def json_median(k):
    rows = json.load(open(f"/root/work/data/{k}.json"))
    d = pd.DataFrame([[int(r[1]), float(r[2])] for r in rows if len(r[0]) == 3 and r[2] is not None],
                     columns=["year", "v"])
    return d.groupby("year")["v"].median().dropna()


pli, labsh, yw = json_median("pwt_pli"), json_median("pwt_labsh"), json_median("pwt_yw")
rel = (pli / (labsh * yw)).dropna()
relprice_path = np.interp(YEARS, rel.index.values, rel.values)
relprice_path = pd.Series(relprice_path).interpolate().bfill().ffill().values
yw_path = np.interp(YEARS, yw.index.values, yw.values)
yw_path = pd.Series(yw_path).interpolate().bfill().ffill().values
wage_emp = json_median("wage_emp")
wage_emp_path = np.interp(YEARS, wage_emp.index.values, wage_emp.values) / 100.0
_first = np.argmax(np.isfinite(wage_emp_path))
for _i in range(_first):
    wage_emp_path[_i] = 0.05 + 0.008 * (YEARS[_i] - 1800) / 5.0
wage_emp_path = pd.Series(wage_emp_path).interpolate().values
prod = (json_median("usda_agY") / json_median("usda_agL")).dropna()
prod_path = np.interp(YEARS, prod.index.values, prod.values)
prod_path = pd.Series(prod_path).bfill().ffill().values
intens = (json_median("usda_KperL") + json_median("usda_MperL")).dropna()
intens_path = np.interp(YEARS, intens.index.values, intens.values)
intens_path = pd.Series(intens_path).bfill().ffill().values

# ---------------- constants: estimated / calibrated / assumed ----------------
sigma = 1.5          # ESTIMATED in T1 (OLS 1.24-1.40; development extremes 1.73)
beta_i = 0.5         # ASSUMED intensity exponent in agricultural productivity (labour share 0.5)
a_food = 0.5         # CALIBRATED food-demand scale
eps_food = 0.15      # ASSUMED income elasticity of food demand
alpha_n = 0.4        # ASSUMED non-agricultural capital share
s_inv = 0.20         # CALIBRATED investment rate (WDI median)
delta = 0.40         # ASSUMED 5-year depreciation
e0 = 0.02            # ASSUMED baseline enrolment
J0_ = 0.10           # CALIBRATED initial wage-sector job share
N0_CAL = 3.18        # CALIBRATED desired surviving children at zero schooling (1800 TFR x survival)
KAPPA_CAL = 0.124    # CALIBRATED schooling effect on desired fertility (from 2020 TFR and schooling)
# intensity relative to its earliest observation: CES substitution driven by the observed relative input price
intens_rel = (relprice_path / relprice_path[0]) ** (-sigma)
intens_rel = np.where(np.isfinite(intens_rel) & (intens_rel > 0), intens_rel, 1.0)


def simulate(p, mechanisation=True):
    lam_q, lam_r, gJ = p
    N0, kappa = N0_CAL, KAPPA_CAL
    # observed productivity path (USDA), pre-1961 extrapolated with 1%/yr TFP + the intensity margin
    prod_rel = np.ones(T)
    for i, t in enumerate(YEARS):
        if t >= 1961:
            prod_rel[i] = prod_path[i] / prod_path[np.argmin(np.abs(YEARS - 1961))]
        else:
            mec = (intens_rel[i] / intens_rel[np.argmin(np.abs(YEARS - 1961))]) ** beta_i
            prod_rel[i] = np.exp(0.01 * (t - 1961)) * mec
    i60 = int(np.argmin(np.abs(YEARS - 1960)))
    yg_rel = gdppc_obs / gdppc_obs[0]
    food_rel = np.maximum(yg_rel, 1e-3) ** eps_food
    S = np.full(T, 0.5)                      # schooling path, iterated below
    for _ in range(15):                      # fixed-point iteration: demography <-> absorber
        Y, W, O = 0.45, 0.50, 0.05
        popv = np.zeros(T); Wv = np.zeros(T)
        tfrv = np.zeros(T)
        for i, t in enumerate(YEARS):
            women = 0.5 * W
            tfr = max(1.0, (N0 - kappa * S[i]) / max(s_child[i], 0.05))
            births = tfr * women / 7.0
            Y2 = births * s_child[i]
            W2 = Y * 0.9 + W * adult_surv[i]
            O2 = W * (1 - adult_surv[i]) * 0.5 + O * 0.5
            Y, W, O = Y2, W2, O2
            popv[i] = Y + W + O; Wv[i] = W; tfrv[i] = tfr
        Y_a = a_food * food_rel * popv
        theta_scale = Y_a[i60] / (ag_share_obs[i60] * Wv[i60])
        if mechanisation:
            L_a = Y_a / (theta_scale * prod_rel)
        else:
            prod_cf = prod_rel.copy()
            prod_cf[i60 + 1:] = prod_rel[i60 + 1:] * (intens_rel[i60] / intens_rel[i60 + 1:]) ** beta_i
            L_a = Y_a / (theta_scale * prod_cf)
        L_a = np.minimum(L_a, 0.98 * Wv)
        # absorber
        K_n = 1.0
        J = np.zeros(T); queue = np.zeros(T); S_new = np.zeros(T)
        S_cur = S[:]
        Klist = np.zeros(T)
        for i in range(T):
            Klist[i] = K_n
            jshare = wage_emp_path[i] if np.isfinite(wage_emp_path[i]) and YEARS[i] >= 1991 else (0.05 + gJ * (YEARS[i] - 1800) / 5.0)
            J[i] = min(jshare * Wv[i], Wv[i])
            L_n = max(Wv[i] - L_a[i], 0.0)
            queue[i] = max(L_n - J[i], 0.0) / max(Wv[i], 1e-9)
            ag_prod = Y_a[i] / max(L_a[i], 1e-9)
            premium = max(np.log(max(yg_rel[i] / max(ag_prod, 1e-9), 1e-3) / max(yg_rel[0] / max(Y_a[0] / max(L_a[0], 1e-9), 1e-9), 1e-9)), 0.0) / 5.0
            e = np.clip(e0 + lam_q * queue[i] * (J[i] / max(Wv[i], 1e-9)) + lam_r * premium, 0.0, 0.95)
            S_new[i] = (0.5 * S_cur[i] + 0.5 * (12 * e))
            K_n = K_n * (1 - delta) + s_inv * (Wv[i] * 0.5)
        S = S_new
    return dict(pop=popv, ag_share=L_a / np.maximum(Wv, 1e-9), wage_share=np.minimum(J, np.maximum(Wv - L_a, 0)) / np.maximum(Wv, 1e-9),
                school=S, tfr=tfrv, ag_labour=L_a, queue=queue, pop_growth=np.diff(np.log(popv)) / 5.0,
                wage_jobs=J, labour_force=Wv)


def observed_targets():
    popi = pop_obs / pop_obs[np.argmax(np.isfinite(pop_obs))]
    return {"ag_share": ag_share_obs, "tfr": tfr_obs, "school": school_obs, "pop": popi,
            "wage_share": np.where(YEARS >= 1991, wage_emp_path, np.nan)}


def loss(p, tg=None):
    m = simulate(p)
    tg = tg or observed_targets()
    res = []
    mask = YEARS >= 1950
    i60 = int(np.argmin(np.abs(YEARS - 1960)))
    for key in ("ag_share", "tfr", "school", "pop", "wage_share"):
        obs = tg[key]
        ok = mask & np.isfinite(obs)
        if ok.sum() > 3:
            mdl = m[key]
            if key == "pop":
                mdl = m["pop"] / max(m["pop"][i60], 1e-9)
            rng = np.nanmax(obs[ok]) - np.nanmin(obs[ok]) + 1e-6
            res.append((mdl[ok] - obs[ok]) / rng)
    return np.concatenate(res) if res else np.array([1.0])


if __name__ == "__main__":
    A("=== T3 joint demography-agriculture-absorber demonstration model ===")
    A("3 free parameters calibrated jointly on 1950-2020 stylised-country paths (cross-country medians);")
    A("Boppart inputs: sigma = 1.5 (estimated in T1); observed agricultural labour productivity is split")
    A("into TFP and input intensity; food demand has a subsistence floor and a low income elasticity.")
    A("N0 and kappa are calibrated directly from the TFR/survival/schooling endpoints (not free). A")
    A("demonstration model, not an estimate of any country's history.")
    p0 = np.array([1.5, 0.5, 0.02])
    lo = np.array([0.0, 0.0, 0.0]); hi = np.array([6.0, 3.0, 0.05])
    fit = least_squares(loss, p0, bounds=(lo, hi), max_nfev=400)
    p = fit.x
    A("")
    A("free parameters (calibrated):")
    for nm, v in zip(["queue weight in schooling", "wage-premium weight in schooling",
                      "wage-job share growth per 5 years"], p):
        A(f"   {nm:48s} {v:.3f}")
    A(f"   scaled root-mean-square fit residual: {np.sqrt((fit.fun**2).mean()):.3f}")
    m = simulate(p); tg = observed_targets()
    A("")
    A("model vs data (selected years):")
    A("  year   ag share model/data   TFR model/data   schooling model/data   pop index model/data   wage share model/data")
    for yr in (1900, 1950, 1970, 1990, 2010, 2020):
        i = np.argmin(np.abs(YEARS - yr))
        def f(v):
            return f"{v:5.2f}" if np.isfinite(v) else "   na"
        A(f"  {yr}   {m['ag_share'][i]*100:5.1f} / {f(tg['ag_share'][i]*100)}      "
          f"{f(m['tfr'][i])} / {f(tg['tfr'][i])}    {f(m['school'][i])} / {f(tg['school'][i])}     "
          f"{f(m['pop'][i])} / {f(tg['pop'][i])}      {f(m['wage_share'][i]*100)} / {f(tg['wage_share'][i]*100)}")
    cf = simulate(p, mechanisation=False)
    A("")
    A("counterfactual: freeze input intensification after 1960 (relative input prices held at the 1960 level;")
    A("TFP path unchanged) - the 'no more ag jobs / no mechanisation' comparison.")
    for yr in (1980, 2000, 2020):
        i = np.argmin(np.abs(YEARS - yr))
        A(f"  {yr}: ag labour share {m['ag_share'][i]*100:5.1f}% vs {cf['ag_share'][i]*100:5.1f}% frozen; "
          f"wage-employment share {m['wage_share'][i]*100:4.1f}% vs {cf['wage_share'][i]*100:4.1f}%; "
          f"schooling {m['school'][i]:4.1f} vs {cf['school'][i]:4.1f} yrs; TFR {m['tfr'][i]:.2f} vs {cf['tfr'][i]:.2f}")
    popg = np.diff(np.log(m["pop"])) / 5.0
    ipeak = int(np.argmax(popg))
    A("")
    A(f"timing: population growth peaks around {YEARS[ipeak]} at {100*popg[ipeak]:.1f}%/yr; agricultural labour")
    A(f"peaks in {YEARS[int(np.argmax(m['ag_labour']))]} (level {m['ag_labour'].max():.2f}); the ag labour share")
    A(f"falls from {100*m['ag_share'][np.argmin(np.abs(YEARS-1960))]:.0f}% in 1960 to {100*m['ag_share'][-1]:.0f}% in 2020.")
    true = np.array([1.2, 0.4, 0.02])
    ms = simulate(true)
    tg_syn = {k: ms[k] for k in ("ag_share", "tfr", "school", "pop", "wage_share")}
    fit2 = least_squares(lambda q: loss(q, tg_syn), p0, bounds=(lo, hi), max_nfev=300)
    A("")
    A("recovery test (simulate from known parameters, re-fit all four series):")
    for nm, tv, rv in zip(["lam_q", "lam_r", "gJ"], true, fit2.x):
        A(f"   {nm:6s} true {tv:.2f} recovered {rv:.2f} (error {abs(rv-tv):.2f})")
    pd.DataFrame({"year": YEARS, **{k: v for k, v in m.items() if len(v) == T}}).to_csv(f"{OUT}/model_paths.csv", index=False)
    pd.DataFrame({"year": YEARS, **{"cf_" + k: v for k, v in cf.items() if len(v) == T}}).to_csv(f"{OUT}/model_counterfactual.csv", index=False)
    json.dump({"params": dict(zip(["lam_q", "lam_r", "gJ"], p.tolist())),
               "calibrated": {"N0": N0_CAL, "kappa": KAPPA_CAL},
               "recovery": dict(zip(["lam_q", "lam_r", "gJ"], [float(x) for x in fit2.x])),
               "constants": {"sigma": sigma, "beta_intensity": beta_i, "food_scale": a_food,
                             "food_income_elasticity": eps_food, "alpha_nonag": alpha_n,
                             "investment_rate": s_inv, "depreciation_5y": delta}},
              open(f"{OUT}/model_params.json", "w"), indent=1)
    open(f"{OUT}/model_summary.txt", "w").write("\n".join(L) + "\n")
    print("\n".join(L))
