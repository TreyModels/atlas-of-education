#!/usr/bin/env python3
"""Cluster-preserving country placebo for the volatility series.

The naive cross-country value permutation (placebo_fix.py) scrambles values across
countries and, in doing so, destroys the within-country clustering that the
clustered standard error is built on; its null is therefore far too tight to be a
significance test.  The right placebo for a clustered design swaps *whole country
time series* between countries: each country receives another country's complete
volatility series, so within-country serial structure and clustering are kept and
only the country alignment is broken.

Writes out/placebo_swap.json.
"""
import json
import numpy as np
import level_vol as L

rows = L.build(["level", "vol"])
base = L.fit_multi(rows, 2, True)
actual = base["b"][1]
print(f"actual volatility coefficient {actual:+.5f} (clustered se {base['se'][1]:.5f}, "
      f"n={base['n']}, countries={base['nc']})")

orig = dict(L.VOL)
by_country = {}
for (i, t), v in orig.items():
    by_country.setdefault(i, []).append((t, v))
isos = sorted(by_country)
rng = np.random.default_rng(20261123)
null, sizes = [], []
for _ in range(200):
    perm = rng.permutation(isos)
    placebo = {}
    for target, donor in zip(isos, perm):
        for (t, v) in by_country[donor]:
            if (target, t) in orig:          # keep the target country's year grid
                placebo[(target, t)] = v
    L.VOL.clear(); L.VOL.update(placebo)
    try:
        r = L.fit_multi(L.build(["level", "vol"]), 2, True)
    finally:
        L.VOL.clear(); L.VOL.update(orig)
    if r:
        null.append(abs(r["b"][1])); sizes.append(r["n"])
null = np.array(null)
res = dict(actual=float(actual), clustered_se=float(base["se"][1]),
           p=float((null >= abs(actual)).mean()),
           q05=float(np.percentile(null, 5)), q50=float(np.percentile(null, 50)),
           q95=float(np.percentile(null, 95)), draws=int(len(null)),
           mean_n=int(np.mean(sizes)))
print("series-swap country placebo:", json.dumps(res, indent=1))
json.dump(res, open("/root/work/level_vol/out/placebo_swap.json", "w"), indent=1)
print("wrote /root/work/level_vol/out/placebo_swap.json")
