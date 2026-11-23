#!/usr/bin/env python3
"""Power check for the country-trend test (queue job 2).

World A (original null): electricity is a consequence of development, no causal effect.
World B(E): electricity rolls out as an S-curve with country-specific timing (partly
independent of development), and DOES raise schooling: going from 0 to 100% of the
population with electricity adds E points to lower-secondary and secondary completion.
Same panels (common seeds) across E, so E=0 is the false-positive rate for the
S-curve electricity process. Test = identical to boppart_world.fit (10-year change on
starting level, country + year effects, clustered SE; with/without country trends).
"""
import sys
from multiprocessing import Pool
import numpy as np
import boppart_world as bw

N_PANELS = 500
EFFECTS = [0.0, 5.0, 10.0, 20.0, 40.0]
C, T = bw.N_COUNTRIES, bw.N_YEARS


def simulate_s(seed, mom):
    D = bw.simulate(seed, mom)           # same latent development, schooling noise etc.
    rng = np.random.default_rng(seed + 10_000_000)
    ly = D["ly"]
    ly0 = ly[:, 0]
    mid = 22.0 - 4.0 * (ly0 - ly0.mean()) / mom["ly_sd"] + rng.normal(0, 8.0, C)   # rollout midpoint (years)
    width = rng.uniform(3.0, 7.0, C)
    t = np.arange(T)[None, :]
    elec = 100.0 / (1.0 + np.exp(-(t - mid[:, None]) / width[:, None]))
    elec = np.clip(elec + rng.normal(0, 4.0, (C, T)), 0, 100)
    D["elec_s"] = elec
    return D


def one(seed):
    D = simulate_s(seed, MOM)
    gi = np.repeat(np.arange(C), T - 10)
    gy = np.tile(np.arange(T - 10), C)
    d10 = lambda a: (a[:, 10:] - a[:, :-10]).ravel()
    out = {}
    # World A: original null, electricity = f(development)
    for nm, ya in (("lsc", D["lsc"]), ("sec", D["sec"])):
        out[("A", 0.0, nm)] = bw.fit(d10(ya), D["elec"][:, :-10].ravel(), ya[:, :-10].ravel(), gi, gy, False) + \
                              bw.fit(d10(ya), D["elec"][:, :-10].ravel(), ya[:, :-10].ravel(), gi, gy, True)
    # World B(E)
    for E in EFFECTS:
        for nm, ya in (("lsc", D["lsc"]), ("sec", D["sec"])):
            y2 = ya + E * D["elec_s"] / 100.0
            x = D["elec_s"][:, :-10].ravel(); own = y2[:, :-10].ravel(); dy = d10(y2)
            out[("B", E, nm)] = bw.fit(dy, x, own, gi, gy, False) + bw.fit(dy, x, own, gi, gy, True)
    return out


if __name__ == "__main__":
    MOM = bw.observed_moments()
    print("moments:", MOM, flush=True)
    print(f"{N_PANELS} panels, {C} countries x {T} years, effect sizes (pts per 0->100% electricity): {EFFECTS}", flush=True)
    with Pool(24) as p:
        res = p.map(one, range(N_PANELS), chunksize=4)
    print("\nDETECTION RATE = share of panels where the electricity coefficient is significant (|t|>1.96) AND positive")
    print(f"{'world':6s}{'true E':>8s}{'outcome':>9s}{'median coef FE':>16s}{'detect FE':>11s}{'median coef trend':>19s}{'detect trend':>14s}")
    for k in res[0]:
        arr = np.array([r[k] for r in res])
        b, se, bt, st = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
        d = np.mean((b / se > 1.96)) * 100
        dt = np.mean((bt / st > 1.96)) * 100
        print(f"{k[0]:6s}{k[1]:>8.0f}{k[2]:>9s}{np.median(b):>16.3f}{d:>10.1f}%{np.median(bt):>19.3f}{dt:>13.1f}%")
