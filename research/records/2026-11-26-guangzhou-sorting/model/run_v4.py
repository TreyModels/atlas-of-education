#!/usr/bin/env python3
"""Pre-registered v4 sweep (PREREG_V4.md)."""
import json, hashlib, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/sig')
import gz_v4 as m
from run_v31 import metrics, R as R31
R = {**R31, 'ACAD': (.45, .65), 'PRE_SHARE': (.2, .6), 'BAN_RED': (0, .6), 'PRE_EFF': (0, .3), 'REBAND_PERF': (0, .5),
     'TERM_SHARE': (.02, .15), 'HOL_SHARE': (.2, .6), 'POST_EFF': (0, .2), 'FT_SHARE': (0, .05), 'FT_EFF': (-.2, .3)}
N_DRAWS, N, SEED = 400, 40_000, 20261129
SC = dict(CURRENT={}, OLD=dict(BAN_RED=0.0, BOARD=False, REBAND=False), BAN_PERFECT=dict(BAN_RED=1.0),
          TIME_CONTROL=dict(TERM_SHARE=0.0, HOL_SHARE=0.0, FT_SHARE=0.0))

def one(item):
    i, dr = item; out = {'i': i, 'params': dr}
    for name, kw in SC.items():
        try:
            d = m.run(n=N, seed=SEED + i, **{**dr, 'HS_TEACH_SD': dr['TEACH_SD'], **kw})
            r = metrics(d); a = d['acad']; w = d['logw']; q = np.searchsorted(np.quantile(w, [.2, .4, .6, .8]), w)
            r.update(pre_Q1=float(d['pre'][q == 0].mean()), pre_Q5=float(d['pre'][q == 4].mean()),
                     hol_share=float(d['hol'][a].mean()), term_share=float(d['term'][a].mean()), ft_share=float(d['ft'].mean()))
            out[name] = r
        except Exception as e:
            out[name] = {'error': repr(e)}
    return out

if __name__ == '__main__':
    rng = np.random.default_rng(SEED); keys = list(R)
    U = (rng.permuted(np.tile(np.arange(N_DRAWS), (len(keys), 1)), axis=1).T + rng.random((N_DRAWS, len(keys)))) / N_DRAWS
    draws = [{k: R[k][0] + U[i, j] * (R[k][1] - R[k][0]) for j, k in enumerate(keys)} for i in range(N_DRAWS)]
    with Pool(2) as pool: res = pool.map(one, list(enumerate(draws)), chunksize=8)
    with open('/home/claude/sig/v4_results.jsonl', 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    man = {fn: hashlib.sha256(open(f'/home/claude/sig/{fn}', 'rb').read()).hexdigest()
           for fn in ('gz_v4.py', 'run_v4.py', 'run_v31.py', 'eq_tests.py', 'PREREG_V4.md', 'v4_results.jsonl')}
    man.update(n_draws=N_DRAWS, n=N, seed=SEED); json.dump(man, open('/home/claude/sig/v4_manifest.json', 'w'), indent=1)
    print('done', len(res), 'errors', sum('error' in r[k] for r in res for k in SC))
