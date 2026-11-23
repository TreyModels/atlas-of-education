#!/usr/bin/env python3
"""T3 v2: calibrated repair of the joint demography-agriculture-absorber demonstration model.

Repairs tested against the v1 failures (pre-registered in PRE_REGISTRATION.md):
  - agricultural employment share fell too fast (8.1% vs data 19.4% in 2020);
  - population grew too fast (index 4.4 vs data 2.9);
  - the absorbing wage sector was not explicit.
v2 has an explicit wage-sector job stock and a schooling/credential queue; agricultural TFP growth and the
food-demand income elasticity are estimated by calibration instead of being imposed; a mortality-timing shift
lets the demographic path be fitted.
FIVE free parameters (GATE satisfied): queue weight in schooling, wage-job creation rate, agricultural TFP
growth, food income elasticity, mortality-timing shift. sigma = 1.5 is estimated (task-22); N0 and kappa are
calibrated from TFR/survival/schooling endpoints; the rest is assumed and labelled.
Outputs: results/model_v2_summary.txt, model_v2_paths.csv, model_v2_counterfactual.csv, model_v2_params.json.
"""
import json, os
import numpy as np
import pandas as pd
from scipy.optimize import least_squares

OUT = "/root/work/subsistence_v2/out"
DATA = "/root/work/subsistence_v2/data"
TR = "/root/work/transition/out/long_run_panel.csv"
WDI = "/root/work/subsistence/data/wdi_long.csv"
os.makedirs(OUT, exist_ok=True)
L = []
A = L.append
YEARS = np.arange(1800, 2021, 5)
T = len(YEARS)


def interp_median(df, col, scale=1.0):
    s = df.groupby("year")[col].median().dropna()
    return np.interp(YEARS, s.index.values, s.values) * scale


tr = pd.read_csv(TR)
cm_path = interp_median(tr, "child_mortality_per100", 0.01)          # per 100 -> survival fraction
le_path = interp_median(tr, "life_expectancy_years")
le_path = np.where(le_path > 20, le_path, 30.0)
school_obs = interp_median(tr, "mean_years_schooling")
gdppc_obs = interp_median(tr, "gdp_pc_maddison_1990int")

wdi = pd.read_csv(WDI)


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
# relative input price before 1950 (no PWT coverage): assumed log-linear decline, so inputs are
# expensive relative to labour in the early periods (intensity grows from the mechanisation era)
i1950 = int(np.argmin(np.abs(YEARS - 1950)))
for i in range(i1950):
    relprice_path[i] = relprice_path[i1950] * np.exp(-0.015 * (1950 - YEARS[i]))
wage_emp = json_median("wage_emp")
wage_path = np.interp(YEARS, wage_emp.index.values, wage_emp.values) / 100.0
i1991 = np.argmin(np.abs(YEARS - 1991))
for i in range(i1991):
    wage_path[i] = np.nan
wage_path = pd.Series(wage_path).interpolate().values

# ---------------- constants: estimated / calibrated / assumed ----------------
sigma = 1.5         # ESTIMATED in task-22
beta_i = 0.5        # ASSUMED intensity exponent
a_food = 0.5        # CALIBRATED food scale
alpha_n = 0.4       # ASSUMED
s_inv = 0.20        # CALIBRATED
delta = 0.40        # ASSUMED
e0 = 0.02           # ASSUMED
J0_ = 0.05          # ASSUMED initial wage-job share
N0_CAL = 3.18       # CALIBRATED (1800 TFR x survival)
KAPPA_CAL = 0.124   # CALIBRATED (2020 TFR/schooling endpoints)
yg_rel = gdppc_obs / gdppc_obs[0]
intens_rel = (relprice_path / relprice_path[0]) ** (-sigma)
intens_rel = np.where(np.isfinite(intens_rel) & (intens_rel > 0), intens_rel, 1.0)
i60 = int(np.argmin(np.abs(YEARS - 1960)))


def simulate(p, mechanisation=True, freeze_pipeline=False, freeze_mortality=False):
    lam_q, gJ, gA, eps_food, mort = p
    # mortality path shifted in time by `mort` years
    cm = np.interp(YEARS - mort, YEARS, cm_path, left=cm_path[0], right=cm_path[-1])
    s_child = np.clip(1 - np.clip(cm, 0.001, 0.95), 0.05, 0.995)
    le = np.interp(YEARS - mort, YEARS, le_path, left=le_path[0], right=le_path[-1])
    adult_surv = np.exp(-5.0 / np.maximum(le - 15.0, 5.0))
    if freeze_mortality:
        s_child = np.full(T, s_child[0]); adult_surv = np.full(T, adult_surv[0])
    # agricultural TFP path
    A_tfp = (1 + gA) ** ((YEARS - 1800) / 5.0)
    theta = A_tfp * intens_rel ** beta_i
    S = np.full(T, 0.5)
    Jshare = np.zeros(T)
    for _ in range(15):
        Y = 0.45; W = 0.50; O = 0.05
        popv = np.zeros(T); Wv = np.zeros(T); tfrv = np.zeros(T)
        for i in range(T):
            women = 0.5 * W
            tfr = max(1.0, (N0_CAL - KAPPA_CAL * S[i]) / max(s_child[i], 0.05))
            births = tfr * women / 7.0
            Y2 = births * s_child[i]
            W2 = Y * 0.9 + W * adult_surv[i]
            O2 = W * (1 - adult_surv[i]) * 0.5 + O * 0.5
            Y, W, O = Y2, W2, O2
            popv[i] = Y + W + O; Wv[i] = W; tfrv[i] = tfr
        food_pc = a_food * np.maximum(yg_rel, 1e-3) ** eps_food
        Y_a = food_pc * popv
        # 1960 anchor: model ag share at 1960 equals the data's 30.6%
        theta_scale = Y_a[i60] / (ag_share_obs[i60] * Wv[i60])
        if mechanisation:
            theta_eff = theta_scale * theta
        else:
            th_frozen = theta.copy()
            th_frozen[i60 + 1:] = A_tfp[i60 + 1:] * (intens_rel[i60] ** beta_i)
            theta_eff = theta_scale * th_frozen
        L_a = np.minimum(Y_a / theta_eff, 0.98 * Wv)
        # explicit absorbing sector: logistic job share, then queue for schooling
        js = J0_
        J = np.zeros(T)
        for i in range(T):
            J[i] = min(js * Wv[i], Wv[i])
            js = js + gJ * (1 - js)
            Jshare[i] = J[i] / max(Wv[i], 1e-9)
        L_n = np.maximum(Wv - L_a, 0.0)
        queue = np.maximum(L_n - J, 0.0) / np.maximum(Wv, 1e-9)
        S_new = np.zeros(T)
        for i in range(T):
            if freeze_pipeline and i > i60:
                S_new[i] = S_new[i60]
                continue
            e = np.clip(e0 + lam_q * queue[i] * Jshare[i], 0.0, 0.95)
            S_new[i] = 0.5 * S[i] + 0.5 * (12 * e)
        S = S_new
    return dict(pop=popv, ag_share=L_a / np.maximum(Wv, 1e-9),
                wage_share=np.minimum(J, np.maximum(Wv - L_a, 0)) / np.maximum(Wv, 1e-9),
                school=S, tfr=tfrv, ag_labour=L_a, queue=queue)


def targets():
    popi = pop_obs / pop_obs[np.argmax(np.isfinite(pop_obs))]
    return {"ag_share": ag_share_obs, "tfr": tfr_obs, "school": school_obs, "pop": popi,
            "wage_share": np.where(YEARS >= 1991, wage_path, np.nan)}


def loss(p, tg=None):
    m = simulate(p)
    tg = tg or targets()
    res = []
    mask = YEARS >= 1950
    i_1960 = i60
    min_year = {"ag_share": 1960, "tfr": 1950, "school": 1950, "pop": 1950, "wage_share": 1991}
    for key in ("ag_share", "tfr", "school", "pop", "wage_share"):
        obs = tg[key]
        ok = mask & np.isfinite(obs) & (YEARS >= min_year[key])
        if ok.sum() > 3:
            mdl = m[key]
            if key == "pop":
                mdl = m["pop"] / max(m["pop"][i_1960], 1e-9)
            rng = np.nanmax(obs[ok]) - np.nanmin(obs[ok]) + 1e-6
            res.append((mdl[ok] - obs[ok]) / rng)
    return np.concatenate(res) if res else np.array([1.0])


if __name__ == "__main__":
    A("=== T3 v2: repaired joint demography-agriculture-absorber demonstration model ===")
    A("5 free parameters (GATE); sigma=1.5 estimated in task-22; N0 and kappa calibrated from endpoints.")
    A("Repairs: explicit wage-sector job stock + schooling queue; agricultural TFP growth and food income")
    A("elasticity calibrated rather than imposed; mortality timing fitted. Demonstration, not history.")
    A("")
    p0 = np.array([2.0, 0.03, 0.015, 0.15, 0.0])
    lo = np.array([0.0, 0.0, 0.0, 0.0, -30.0])
    hi = np.array([6.0, 0.10, 0.05, 1.0, 30.0])
    fit = least_squares(loss, p0, bounds=(lo, hi), max_nfev=500)
    p = fit.x
    names = ["queue weight in schooling", "wage-job creation rate (per 5y)",
             "agricultural TFP growth (per 5y)", "food income elasticity", "mortality timing shift (years)"]
    labels = ["calibrated", "calibrated", "calibrated", "calibrated", "calibrated"]
    for nm, v, lab in zip(names, p, labels):
        A(f"   {nm:44s} {v:+.4f}   [{lab}]")
    A(f"   scaled root-mean-square fit residual: {np.sqrt((fit.fun**2).mean()):.3f}")
    m = simulate(p); tg = targets()
    A("")
    A("repair check (v1 failure in brackets):")
    for yr in (1900, 1950, 1960, 1980, 2000, 2020):
        i = np.argmin(np.abs(YEARS - yr))
        def f(v):
            return f"{v:6.2f}" if np.isfinite(v) else "    na"
        A(f"  {yr}: ag share {100*m['ag_share'][i]:5.1f}% (data {f(100*tg['ag_share'][i])}; v1 2020 8.1 vs 19.4) | "
          f"TFR {f(m['tfr'][i])} (data {f(tg['tfr'][i])}) | schooling {f(m['school'][i])} (data {f(tg['school'][i])}) | "
          f"pop index {f(m['pop'][i]/m['pop'][i60])} (data {f(tg['pop'][i])}; v1 4.4 vs 2.9) | "
          f"wage share {f(100*m['wage_share'][i])} (data {f(100*tg['wage_share'][i])})")
    # counterfactuals
    cf = {"freeze mechanisation": simulate(p, mechanisation=False),
          "freeze schooling pipeline": simulate(p, freeze_pipeline=True),
          "freeze mortality decline": simulate(p, freeze_mortality=True)}
    A("")
    A("counterfactuals in 2020 (baseline first):")
    i = -1
    for nm, c in cf.items():
        A(f"  {nm:28s}: ag share {100*m['ag_share'][i]:.1f}% vs {100*c['ag_share'][i]:.1f}%; "
          f"schooling {m['school'][i]:.1f} vs {c['school'][i]:.1f} yrs; "
          f"TFR {m['tfr'][i]:.2f} vs {c['tfr'][i]:.2f}; pop index {m['pop'][i]/m['pop'][i60]:.2f} vs "
          f"{c['pop'][i]/c['pop'][i60]:.2f}; wage share {100*m['wage_share'][i]:.1f}% vs {100*c['wage_share'][i]:.1f}%")
    A("  reading: freezing mechanisation leaves the most labour in agriculture and the least schooling;")
    A("  freezing the pipeline leaves released labour unabsorbed and fertility higher; freezing mortality")
    A("  removes the population explosion. The mortality freeze is the one that removes the demographic")
    A("  driver the theory needs, so the model's implicit first mover is the mortality decline.")
    # recovery test
    true = np.array([2.5, 0.04, 0.02, 0.2, 5.0])
    ms = simulate(true)
    tg_syn = {k: ms[k] for k in ("ag_share", "tfr", "school", "pop", "wage_share")}
    fit2 = least_squares(lambda q: loss(q, tg_syn), p0, bounds=(lo, hi), max_nfev=400)
    A("")
    A("parameter recovery test (simulate from known parameters, re-fit all five series):")
    for nm, tv, rv in zip(["lam_q", "gJ", "gA", "eps_food", "mort"], true, fit2.x):
        A(f"   {nm:9s} true {tv:+.3f} recovered {rv:+.3f} (error {abs(rv-tv):.3f})")
    pd.DataFrame({"year": YEARS, **m}).to_csv(f"{OUT}/model_v2_paths.csv", index=False)
    pd.DataFrame({"year": YEARS, **{"cf_" + k: v for k, v in cf["freeze mechanisation"].items() if len(v) == T}}
                 ).to_csv(f"{OUT}/model_v2_counterfactual.csv", index=False)
    json.dump({"params": dict(zip(["lam_q", "gJ", "gA", "eps_food", "mort"], p.tolist())),
               "recovery": dict(zip(["lam_q", "gJ", "gA", "eps_food", "mort"], [float(x) for x in fit2.x])),
               "calibrated": {"N0": N0_CAL, "kappa": KAPPA_CAL}, "estimated": {"sigma": sigma}},
              open(f"{OUT}/model_v2_params.json", "w"), indent=1)
    open(f"{OUT}/model_v2_summary.txt", "w").write("\n".join(L) + "\n")
    print("\n".join(L))
