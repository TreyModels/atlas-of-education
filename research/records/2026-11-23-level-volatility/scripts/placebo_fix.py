#!/usr/bin/env python3
"""Variance-matched country placebo for the volatility series.

The naive cross-country permutation in level_vol.py scrambles volatility values
across countries, which inflates the within-country variance of the placebo
relative to the real series; because standard errors shrink as the regressor's
variance grows, the naive placebo distribution is too tight to compare against.
Here each country's scrambled series is rescaled back to that country's own mean
and standard deviation, so only the *timing* is scrambled and the coefficient is
on the same scale as the real one.
"""
import json
import numpy as np
import level_vol as L

rows = L.build(["level", "vol"])
base = L.fit_multi(rows, 2, True)
actual = base["b"][1]
print(f"actual volatility coefficient {actual:+.5f} (se {base['se'][1]:.5f}, "
      f"n={base['n']}, countries={base['nc']})")

orig = dict(L.VOL)
by_country = {}
for (i, t), v in orig.items():
    by_country.setdefault(i, []).append((t, v))

rng = np.random.default_rng(20261123)
null = []
for _ in range(200):
    placebo = {}
    for i, lst in by_country.items():
        lst = sorted(lst)
        vals = np.array([v for _, v in lst], float)
        scr = vals[rng.permutation(len(vals))]          # scramble timing within country
        # rescale to the country's own mean and sd (variance-matched)
        scr = (scr - scr.mean()) / (scr.std(ddof=0) or 1.0) * vals.std(ddof=0) + vals.mean()
        for (t, _), v in zip(lst, scr):
            placebo[(i, t)] = float(v)
    L.VOL.clear(); L.VOL.update(placebo)
    try:
        r = L.fit_multi(L.build(["level", "vol"]), 2, True)
    finally:
        L.VOL.clear(); L.VOL.update(orig)
    if r:
        null.append(abs(r["b"][1]))
null = np.array(null)
res = dict(actual=float(actual), se=float(base["se"][1]),
           p=float((null >= abs(actual)).mean()),
           q05=float(np.percentile(null, 5)), q50=float(np.percentile(null, 50)),
           q95=float(np.percentile(null, 95)), draws=int(len(null)))
print("variance-matched placeholder placebo:", json.dumps(res, indent=1))
json.dump(res, open("/root/work/level_vol/out/placebo_variance_matched.json", "w"), indent=1)
print("wrote /root/work/level_vol/out/placebo_variance_matched.json")
