"""Known 'true' parameters for the recovery check."""
import json, numpy as np, model as M
pan = json.load(open("data/panel.json")); rng = np.random.default_rng(5)
base = {"d_pi": .5, "d_si": 4, "d_sc": 7, "d_ti": 8.5, "d_tc": 10, "bl_sd": .1, "r_u": .2, "r_q": .2, "pblend": .5, "th_k": 2.2, "th_f": 2.5, "kappa": 1.0, "gam": 3., "lam_s": 2.,
        "Dlo": 1.8, "Dhi": 6.5, "sd_d": .6, "c0": .5, "phi0": .8, "k0": 1.8, "eps": .02, "a0": .25, "al_d": 2.5, "al_u": .4, "R0": 1.5, "rho_a": .2, "al_m": 1., "Rm": 1.5, "Kc": 6, "sexr": 1., "dsep": .02}
for s in "AB":
    th = [base[n] for n in M.PN]
    if s == "B": th[M.PN.index("kappa")] = 0.0
    json.dump(dict(scen=s, theta=th, f={c: float(rng.normal(0, .4)) for c in pan["FIT"]}, seed=77), open(f"data/truth_{s}.json", "w"))
