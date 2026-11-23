#!/usr/bin/env python3
"""Luck test v2 (REVIEW item 6: a circular time-shift of a trending series is an easy null).
Adds a HARDER null: each country's lower-secondary series is replaced by ANOTHER country's series at the same calendar
years (keeps trend, shape, year effects, and the distribution of levels; destroys only the link to this country's fertility).
Also reports the original time-shift null. Observed statistic is unchanged (11.97%)."""
import random, statistics, sys
from multiprocessing import Pool
import mc_big as M

LSC = M.V["lsc"]
BYISO = {}
for (i, t) in LSC:
    BYISO.setdefault(i, set()).add(t)
DONORS = sorted(i for i in BYISO if len(BYISO[i]) > 5)


def swap_run(seed):
    g = random.Random(seed)
    Y, X, I, T = [], [], [], []
    for k, (yrs, dv, xv) in enumerate(M.BLOCKS):
        for _ in range(5):
            d = g.choice(DONORS)
            xs = [(t, y, LSC.get((d, t))) for t, y in zip(yrs, dv)]
            if sum(1 for z in xs if z[2] is not None) >= 0.6 * len(xs):
                break
        for t, y, x in xs:
            if x is not None:
                Y.append(y); X.append(x); I.append(k); T.append(t)
    return M.r2_within(Y, X, I, T)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    with Pool(24) as p:
        a = sorted(p.map(M.null_run, range(n), chunksize=100))
        b = sorted(p.map(swap_run, range(n), chunksize=100))
    print(f"observed share explained (lsc -> 10-yr fertility change, country+year effects): {M.OBS:.2f}%")
    for lab, v in (("time-shift null (original)", a), ("other-country swap null (harder)", b)):
        print(f"  {lab:34s} median {statistics.median(v):.3f}%  99th pct {v[int(.99*len(v))]:.3f}%  max {v[-1]:.3f}%  reached observed: {sum(1 for z in v if z >= M.OBS)} of {len(v)}")
