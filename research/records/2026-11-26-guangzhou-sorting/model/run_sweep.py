#!/usr/bin/env python3
"""Pre-registered sweep for gz_talent.py (see PREREG_GZ_SORTING.md)."""
import json, hashlib, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/sig')
import gz_talent as g

RANGES = dict(TAL_WEALTH=(0, .3), ZONE_TEACH=(.05, .5), HOME=(0, .3), DECAY=(0, .9), GROW=(.2, .8),
              CLASS_EFF=(.2, .6), SCHOOL_EFF=(0, .2), NOISE=(.2, .6), SEG=(.3, .8), ACAD=(.55, .75),
              PRE_TUT=(0, .3), POST_TUT=(0, .15))
N_DRAWS, N_PUP, SEED = 2000, 40_000, 20261126


def lhs(n, k, rng):
    u = (rng.permuted(np.tile(np.arange(n), (k, 1)), axis=1).T + rng.random((n, k))) / n
    return u


def one(i_draw):
    i, d = i_draw
    common = {k: v for k, v in d.items() if k not in ('PRE_TUT', 'POST_TUT')}
    s = SEED + i
    cur = g.run(n=N_PUP, seed=s, **common, PRE_TUT=0, POST_TUT=0, REBAND=True)
    nor = g.run(n=N_PUP, seed=s, **common, PRE_TUT=0, POST_TUT=0, REBAND=False)
    eqz = g.run(n=N_PUP, seed=s, **{**common, 'ZONE_TEACH': 0.0}, PRE_TUT=0, POST_TUT=0, REBAND=True)
    old = g.run(n=N_PUP, seed=s, **common, PRE_TUT=d['PRE_TUT'], POST_TUT=d['POST_TUT'], REBAND=False)
    return dict(i=i, params=d, CURRENT=cur, NO_REBAND=nor, EQUAL_ZONES=eqz, COHORT_2015=old)


if __name__ == '__main__':
    rng = np.random.default_rng(SEED); keys = list(RANGES)
    U = lhs(N_DRAWS, len(keys), rng)
    draws = [{k: RANGES[k][0] + U[i, j] * (RANGES[k][1] - RANGES[k][0]) for j, k in enumerate(keys)} for i in range(N_DRAWS)]
    with Pool(8) as pool:
        res = pool.map(one, list(enumerate(draws)), chunksize=10)
    with open('/home/claude/sig/sweep_results.jsonl', 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    man = {fn: hashlib.sha256(open(f'/home/claude/sig/{fn}', 'rb').read()).hexdigest()
           for fn in ('gz_talent.py', 'run_sweep.py', 'PREREG_GZ_SORTING.md', 'sweep_results.jsonl')}
    man.update(n_draws=N_DRAWS, n_pupils=N_PUP, seed=SEED)
    json.dump(man, open('/home/claude/sig/sweep_manifest.json', 'w'), indent=1)
    print('done', len(res))
