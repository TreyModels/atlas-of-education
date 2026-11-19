"""All experiments. Run: python3 experiments.py   (about a few seconds). Writes results/*.json."""
import json, os, itertools
import numpy as np
from scipy.optimize import brentq, least_squares
import model as M
import data_inputs as D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
OBS_W, OBS_M = 0.48, 0.77
OBS_GAP = OBS_M - OBS_W


def save(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, indent=1, default=float)


def mean_r(country):
    v = D.SRB[country]
    return float(np.mean(list(v.values()))) / 100.0


R = {c: mean_r(c) for c in D.SRB}


def calibrate_m(r, p, target=D.EVER_MARRIED_TARGET, g=M.AGE_GAP):
    """m such that pooled ever-married at 30-34 equals target (None if even m=1 is too low)."""
    f = lambda m: M.ever_married(M.run(r, p, p, m, g))["pooled"] - target
    if f(1.0) < 0:
        return None
    return float(brentq(f, 1e-3, 1.0))


def row(res):
    pr = M.profile(res)
    em = M.ever_married(res)
    return dict(share_w=pr["all"]["w"], share_m=pr["all"]["m"], gap=pr["all"]["gap"],
                gap_pooled=M.gap(res, standardise=False),
                by_band={k: dict(w=v["w"], m=v["m"], gap=v["gap"]) for k, v in pr.items() if k != "all"},
                ever_married=em)


# ---------------------------------------------------------------- reference point
P_BEST = 0.90   # lowest round p for which realistic ever-married is reachable at China's r (see sweep)
R_CHINA = R["China"]
M0 = calibrate_m(R_CHINA, P_BEST)
save("inputs_used.json", dict(R=R, srb_years="1992-2008 mean of UN WPP 2024 via OWID", R_CHINA=R_CHINA,
                              P_BEST=P_BEST, M0=M0, ever_married_target=D.EVER_MARRIED_TARGET,
                              window=D.EVER_MARRIED_WINDOW, obs=dict(w=OBS_W, m=OBS_M, gap=OBS_GAP),
                              chart=D.CHART))

# ---------------------------------------------------------------- (a) how big a gap can selection give?
rs = np.round(np.arange(1.00, 1.2001, 0.01), 2)
ps = np.round(np.arange(0.60, 0.9501, 0.05), 2)
ms = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
grid = []
for r, p, m in itertools.product(rs, ps, ms):
    res = M.run(r, p, p, m)
    em = M.ever_married(res)["pooled"]
    grid.append((float(r), float(p), float(m), M.gap(res), M.gap(res, standardise=False), em))
G = np.array(grid)
inwin = (G[:, 5] >= D.EVER_MARRIED_WINDOW[0]) & (G[:, 5] <= D.EVER_MARRIED_WINDOW[1])


def best(mask, col=3):
    i = np.argmax(np.where(mask, G[:, col], -9))
    return dict(r=G[i, 0], p=G[i, 1], m=G[i, 2], gap=G[i, 3], gap_pooled=G[i, 4], ever_married_pooled=G[i, 5])


# calibrated m (to census target) at each (r, p): realistic-by-construction frontier
cal = []
for r in rs:
    for p in ps:
        m = calibrate_m(float(r), float(p))
        if m is None:
            cal.append(dict(r=float(r), p=float(p), m=None, gap=None)); continue
        res = M.run(float(r), float(p), float(p), m)
        cal.append(dict(r=float(r), p=float(p), m=m, gap=M.gap(res), gap_pooled=M.gap(res, standardise=False)))
calfeas = [c for c in cal if c["m"] is not None]
cal_best = max(calfeas, key=lambda c: c["gap"])
cal_best_r_le_china = max([c for c in calfeas if c["r"] <= round(R_CHINA, 2)], key=lambda c: c["gap"])

res_best = M.run(R_CHINA, P_BEST, P_BEST, M0)
r_ok = G[:, 0] <= round(R_CHINA, 2) + 1e-9
by_m = []
for mm in ms:
    msk = inwin & r_ok & (np.isclose(G[:, 2], mm))
    by_m.append(dict(m=mm, n=int(msk.sum()), best=(best(msk) if msk.any() else None)))
best_in_window_r_le_china = best(inwin & r_ok)
a = dict(
    n_runs=len(G), r_range=[1.0, 1.2], p_range=[0.6, 0.95], m_grid=ms,
    max_gap_any=best(np.ones(len(G), bool)),
    max_gap_in_realistic_window=best(inwin),
    max_gap_in_realistic_window_r_at_or_below_china=best_in_window_r_le_china,
    max_in_window_r_at_or_below_china_by_m=by_m,
    max_gap_calibrated_m=cal_best,
    max_gap_calibrated_m_r_at_or_below_china=cal_best_r_le_china,
    best_guess=dict(r=R_CHINA, p=P_BEST, m=M0, **row(res_best)),
    observed_gap=OBS_GAP,
    calibrated_table=cal,
    share_of_grid_reaching_observed_gap=float(np.mean(G[:, 3] >= OBS_GAP)),
    share_of_window_reaching_observed_gap=float(np.mean(G[inwin, 3] >= OBS_GAP)) if inwin.any() else None,
    n_window=int(inwin.sum()),
)
# gap with the unstandardised (pooled) measure at the best guess is in row(); also g=2 robustness
m0_g2 = calibrate_m(R_CHINA, P_BEST, g=2)
a["best_guess_age_gap_2"] = dict(m=m0_g2, **row(M.run(R_CHINA, P_BEST, P_BEST, m0_g2, g=2)))
# if China's real marriage-market ratio is below the birth ratio, show gap at several r
a["gap_by_r_at_p_best_calibrated"] = [
    dict(r=float(r), m=calibrate_m(float(r), P_BEST),
         gap=(M.gap(M.run(float(r), P_BEST, P_BEST, calibrate_m(float(r), P_BEST)))
              if calibrate_m(float(r), P_BEST) is not None else None))
    for r in (1.0, 1.05, 1.10, 1.15, R_CHINA, 1.20)]
save("a_selection_ceiling.json", a)


# ---------------------------------------------------------------- (b) fit each rival
# Three numbers are matched: women's share (48), men's share (77) and pooled ever-married at 30-34
# (0.816). Each rival has three free parameters, so each fit is exactly identified: a good fit is
# not a test of either rival. What matters is whether the implied parameters are believable.
TARGET = np.array([OBS_W, OBS_M, D.EVER_MARRIED_TARGET])


def stats(res):
    s = M.shares(res)
    return np.array([s["w"], s["m"], M.ever_married(res)["pooled"]])


def multi_fit(make_res, lower, upper, starts):
    best = None
    for x0 in starts:
        sol = least_squares(lambda x: stats(make_res(x)) - TARGET, x0, bounds=(lower, upper))
        if best is None or sol.cost < best.cost:
            best = sol
    return best


def sel_res(x): return M.run(x[0], x[1], x[1], x[2])
def div_res(x): return M.run(1.0, x[0], x[1], x[2])
def mix_res(x): return M.run(R_CHINA, x[0], x[1], x[2])

fit_sel = multi_fit(sel_res, [1.0, 0.3, 0.02], [4.0, 1.0, 1.0],
                    [[1.1, .8, .3], [1.3, .9, .3], [1.6, .9, .2], [1.05, .95, .5]])
fit_div = multi_fit(div_res, [0.05, 0.05, 0.02], [1, 1, 1], [[.9, .8, .3], [.95, .85, .2], [.8, .5, .3]])
fit_mix = multi_fit(mix_res, [0.05, 0.05, 0.02], [1, 1, 1], [[.9, .8, .3], [.95, .85, .2], [.8, .5, .3]])
rs_, rd_, rm_ = sel_res(fit_sel.x), div_res(fit_div.x), mix_res(fit_mix.x)
b = dict(
    targets=dict(w=OBS_W, m=OBS_M, ever_married_pooled=D.EVER_MARRIED_TARGET),
    real_r_china=R_CHINA,
    selection=dict(r=float(fit_sel.x[0]), p=float(fit_sel.x[1]), m=float(fit_sel.x[2]),
                   resid_max=float(np.abs(fit_sel.fun).max()), **row(rs_)),
    divergence=dict(p_m=float(fit_div.x[0]), p_w=float(fit_div.x[1]), m=float(fit_div.x[2]),
                    resid_max=float(np.abs(fit_div.fun).max()), **row(rd_)),
    mixed=dict(r=R_CHINA, p_m=float(fit_mix.x[0]), p_w=float(fit_mix.x[1]), m=float(fit_mix.x[2]),
               resid_max=float(np.abs(fit_mix.fun).max()), **row(rm_)),
    note="Each fit has 3 free parameters and 3 targets; a close fit is not evidence for either rival.")
# how r and p trade off if the timing of marriage (m) is not pinned by ever-married: fits to the two
# shares only, for several fixed m
def two_target_sel(m):
    best_ = None
    for r0, p0 in ((1.1, .7), (1.3, .8), (1.8, .8), (2.5, .9), (1.05, .6)):
        sol = least_squares(lambda x: [M.shares(M.run(x[0], x[1], x[1], m))[k] - v for k, v in (("w", OBS_W), ("m", OBS_M))],
                            [r0, p0], bounds=([1.0, 0.3], [4.0, 1.0]))
        if best_ is None or sol.cost < best_.cost:
            best_ = sol
    res = M.run(best_.x[0], best_.x[1], best_.x[1], m)
    return dict(m=m, r=float(best_.x[0]), p=float(best_.x[1]), resid=float(np.sqrt(2 * best_.cost)),
                ever_married_pooled=M.ever_married(res)["pooled"])
b["selection_two_target_by_m"] = [two_target_sel(m) for m in (0.1, 0.2, 0.3, 0.4, 0.5, 0.8)]
save("b_fits.json", b)

# ---------------------------------------------------------------- (c) age profile (decided before building)
def single_age_gaps(res):
    sw = res["w_wants"] / (res["w_wants"] + res["w_nowant"])
    sm = res["m_wants"] / (res["m_wants"] + res["m_nowant"])
    return [float(v) for v in (sm - sw)]


def decompose(pm, pw, m):
    tot = M.run(R_CHINA, pm, pw, m)
    sel_only = M.run(R_CHINA, pm, pm, m)    # r from data, equal preferences (= p_m for both)
    pref_only = M.run(1.0, pm, pw, m)       # preferences as fitted, r = 1
    return dict(total=M.gap(tot), selection_only=M.gap(sel_only), preferences_only=M.gap(pref_only),
                interaction=M.gap(tot) - M.gap(sel_only) - M.gap(pref_only),
                by_band_total={k: v["gap"] for k, v in M.profile(tot).items() if k != "all"},
                by_band_selection_only={k: v["gap"] for k, v in M.profile(sel_only).items() if k != "all"},
                by_band_preferences_only={k: v["gap"] for k, v in M.profile(pref_only).items() if k != "all"})


c = dict(
    decided_before_building="age profile of the gap: selection predicts a gap that is near zero among the "
                            "youngest and widens with age (the pool is only distorted after people start "
                            "leaving it); divergence predicts a gap that is already present at 18-22.",
    selection=dict(params=dict(r=b["selection"]["r"], p=b["selection"]["p"], m=b["selection"]["m"]),
                   by_band={k: v["gap"] for k, v in b["selection"]["by_band"].items()},
                   by_age=single_age_gaps(rs_)),
    divergence=dict(params=dict(p_m=b["divergence"]["p_m"], p_w=b["divergence"]["p_w"], m=b["divergence"]["m"]),
                    by_band={k: v["gap"] for k, v in b["divergence"]["by_band"].items()},
                    by_age=single_age_gaps(rd_)),
    mixed=dict(params=dict(r=R_CHINA, p_m=b["mixed"]["p_m"], p_w=b["mixed"]["p_w"], m=b["mixed"]["m"]),
               by_band={k: v["gap"] for k, v in b["mixed"]["by_band"].items()},
               by_age=single_age_gaps(rm_),
               decomposition=decompose(b["mixed"]["p_m"], b["mixed"]["p_w"], b["mixed"]["m"])),
    ages=[int(a) for a in rs_["ages"]],
    # a survey sample is small: smallest sample cell is sex x band; use ~1,047 China respondents as scale
    )
c["band_difference_18_22_selection_vs_divergence"] = (c["divergence"]["by_band"]["18-22"] -
                                                      c["selection"]["by_band"]["18-22"])
save("c_age_profile.json", c)


# ---------------------------------------------------------------- robustness: men marry women two years younger
def sel_res_g2(x): return M.run(x[0], x[1], x[1], x[2], g=2)
fit_g2 = multi_fit(sel_res_g2, [1.0, 0.3, 0.02], [4.0, 1.0, 1.0], [[1.1, .8, .3], [1.3, .9, .3], [1.05, .95, .5]])
r_eq = M.run(1.0, P_BEST, P_BEST, calibrate_m(1.0, P_BEST, g=2), g=2)
rob = dict(
    selection_fit_g2=dict(r=float(fit_g2.x[0]), p=float(fit_g2.x[1]), m=float(fit_g2.x[2]),
                          resid_max=float(np.abs(fit_g2.fun).max()), **row(sel_res_g2(fit_g2.x))),
    gap_at_r1_equal_preferences_g2=row(r_eq),
    note="With a 2-year age gap men stay unmarried longer at a given age, so a gap appears even at r = 1.")
save("e_robustness_age_gap.json", rob)

# ---------------------------------------------------------------- illustrative sampling noise
# ASSUMPTION (not data): about 100 unmarried respondents per sex in the 18-22 band.
n_assumed = 100
def se_gap(pw, pm, n=n_assumed): return float(np.sqrt(pw * (1 - pw) / n + pm * (1 - pm) / n))
bs, bd = b["selection"]["by_band"]["18-22"], b["divergence"]["by_band"]["18-22"]
save("f_sampling_noise.json", dict(assumed_n_per_sex_18_22=n_assumed,
     se_gap_selection_fit=se_gap(bs["w"], bs["m"]), se_gap_divergence_fit=se_gap(bd["w"], bd["m"]),
     predicted_gap_selection=bs["gap"], predicted_gap_divergence=bd["gap"],
     difference=bd["gap"] - bs["gap"]))

# ---------------------------------------------------------------- (d) three-country check
chart_gap = {k: (D.CHART[k][1] - D.CHART[k][0]) for k in ("China", "Korea", "Japan")}
d = dict(r=R, chart_gap_points=chart_gap, rows=[])
for p in (0.6, 0.75, 0.9):
    for country in ("China", "Korea", "Japan"):
        m = calibrate_m(R[country], max(p, 0.9)) if False else None
        # use one m for all countries: the China-calibrated M0 (same behaviour everywhere)
        res = M.run(R[country], p, p, M0)
        d["rows"].append(dict(common_p=p, country=country, m=M0, r=R[country], predicted_gap_points=100 * M.gap(res),
                              chart_gap_points=chart_gap[country]))
# variant using each country's own chart average as p (uses outcome data, so flattering to selection)
d["own_average_variant"] = []
for country in ("China", "Korea", "Japan"):
    w, mm, _ = D.CHART[country]
    p = (w + mm) / 200.0
    res = M.run(R[country], p, p, M0)
    d["own_average_variant"].append(dict(country=country, p=p, r=R[country], predicted_gap_points=100 * M.gap(res),
                                         chart_gap_points=chart_gap[country]))
pred = {r_["country"]: r_["predicted_gap_points"] for r_ in d["rows"] if r_["common_p"] == 0.9}
d["order_predicted_p0.9"] = sorted(pred, key=lambda k: -pred[k])
d["order_chart"] = sorted(chart_gap, key=lambda k: -chart_gap[k])
save("d_cross_country.json", d)
print("done; M0 =", round(M0, 4), "R_CHINA =", round(R_CHINA, 4))
