#!/usr/bin/env python3
"""A world in which Boppart et al. are right.

Their model, taken as true:
  - agriculture is CES in (labour, capital, intermediates, land), sigma > 1
  - non-agricultural TFP drives the relative price of capital and intermediates
  - cheap capital pulls labour off the farm; productivity follows
  - demand is non-homothetic (income elasticity 0.35)

We simulate that world, and then ask the only question that matters for our own
findings: in a world where ONE latent process drives everything, and electricity
has NO causal effect on schooling, do our regressions still recover our results?

If yes, our results are consistent with a Boppart-true world and are not evidence
for any schooling mechanism.
"""
import json, os
from multiprocessing import Pool
import numpy as np

DATA = "/root/work/data"
SIGMA = 1.5          # their claim: substitutability above one
N_PANELS = 100
N_COUNTRIES = 120
N_YEARS = 55


def load(n):
    p = os.path.join(DATA, n + ".json")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(open(p))}


def observed_moments():
    yw = load("pwt_yw"); ea = load("emp_agri"); el = load("electricity")
    ly = np.log([v for v in yw.values() if v > 0])
    ea_v = np.array([v for v in ea.values()])
    el_v = np.array([v for v in el.values() if v is not None])
    return dict(ly_sd=float(ly.std()), ea_mean=float(ea_v.mean()),
                ea_sd=float(ea_v.std()), el_mean=float(el_v.mean()))


def simulate(seed, mom):
    rng = np.random.default_rng(seed)
    C, T = N_COUNTRIES, N_YEARS
    # latent development: country random walk with common drift
    drift = rng.normal(0.018, 0.006, (C, 1))
    shock = rng.normal(0, 0.055, (C, T))
    ly = np.cumsum(shock, axis=1) + drift * np.arange(T)[None, :]
    ly += rng.normal(0, mom["ly_sd"] * 0.9, (C, 1))          # initial level
    ly += 10.0

    # the relative price of capital: falls with development, plus noise
    relp = -0.55 * (ly - ly.mean()) / mom["ly_sd"] + rng.normal(0, 0.25, (C, T))
    # Boppart mechanism: cheap capital -> capital per worker -> fewer farmers
    k_per_l = SIGMA * (np.exp(-relp)) * np.exp(rng.normal(0, 0.3, (C, T)))
    logit_ea = 3.0 - 1.1 * np.log(k_per_l) + rng.normal(0, 0.35, (C, T))
    farm_share = 100.0 / (1.0 + np.exp(-logit_ea))
    wage_share = 100.0 - farm_share

    # electricity: a consequence of development only. NO effect on schooling.
    p_elec = 1.0 / (1.0 + np.exp(-(ly - 8.6) / 0.9))
    elec = 100.0 * p_elec + rng.normal(0, 4.0, (C, T))
    elec = np.clip(elec, 0, 100)

    # schooling and fertility: consequences of development only.
    lsc = 30 + 22 * (ly - 6) + rng.normal(0, 6, (C, T))
    sec = 25 + 24 * (ly - 6) + rng.normal(0, 7, (C, T))
    ter = 5 + 14 * (ly - 6) + rng.normal(0, 5, (C, T))
    fert = 6.5 - 1.6 * (ly - 6) + rng.normal(0, 0.5, (C, T))

    return dict(ly=ly, elec=elec, lsc=lsc, sec=sec, ter=ter, fert=fert,
                farm=farm_share, wage=wage_share, relp=relp)


def fit(dy, x, own, gi, gy, trend=False):
    n = len(dy)
    cols = [x, own]
    if trend:
        for j in range(gi.max() + 1):
            cols.append((gi == j).astype(float) * gy)
    X = np.column_stack([np.ones(n)] + cols)
    def dm(a, g):
        s = np.bincount(g, weights=a); c = np.bincount(g)
        return a - (s / np.maximum(c, 1))[g]
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(dy, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return b[1], np.sqrt(max(Vb[1, 1], 0))


def one(seed):
    mom = MOM
    D = simulate(seed, mom)
    gi = np.repeat(np.arange(N_COUNTRIES), N_YEARS - 10)
    gy = np.tile(np.arange(N_YEARS - 10), N_COUNTRIES)
    def d10(a):
        return (a[:, 10:] - a[:, :-10]).ravel()
    tests = {}
    for name, xa, ya in (("elec->lsc", D["elec"], D["lsc"]),
                         ("elec->sec", D["elec"], D["sec"]),
                         ("wage->ter", D["wage"], D["ter"]),
                         ("farm->fert", D["farm"], D["fert"])):
        dy = d10(ya); xx = xa[:, :-10].ravel(); own = ya[:, :-10].ravel()
        b, se = fit(dy, xx, own, gi, gy, trend=False)
        bt, set_ = fit(dy, xx, own, gi, gy, trend=True)
        tests[name] = (b, se, bt, set_)
    return tests


if __name__ == "__main__":
    MOM = observed_moments()
    print("observed moments used for calibration:", MOM, flush=True)
    print(f"simulating {N_PANELS} panels of {N_COUNTRIES} countries x {N_YEARS} years, "
          f"sigma = {SIGMA} (Boppart's claim)", flush=True)
    with Pool(28) as p:
        res = p.map(one, range(N_PANELS), chunksize=4)
    print("\n" + "=" * 88)
    print("IN A WORLD WHERE BOPPART IS RIGHT AND ELECTRICITY HAS NO CAUSAL ROLE")
    print("=" * 88)
    print(f"{'relationship':16s}{'median coef':>13s}{'% significant':>15s}"
          f"{'% significant w/ trends':>25s}")
    for k in ("elec->lsc", "elec->sec", "wage->ter", "farm->fert"):
        b = np.array([r[k][0] for r in res])
        se = np.array([r[k][1] for r in res])
        bt = np.array([r[k][2] for r in res])
        st = np.array([r[k][3] for r in res])
        sig = np.mean(np.abs(b / se) > 1.96) * 100
        sigt = np.mean(np.abs(bt / st) > 1.96) * 100
        print(f"{k:16s}{np.median(b):>+13.3f}{sig:>14.1f}%{sigt:>24.1f}%")
    print("\nThe simulated world contains NO causal path from electricity to schooling.")
    print("Any significance above is the same latent process appearing twice.")
