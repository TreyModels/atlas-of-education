#!/usr/bin/env python3
"""Pre-registered v6 sweep (PREREG_V6.md): Guangzhou vs pre-2021 vs stylised Hong Kong, rich routes, double reduction."""
import json, hashlib, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/sig')
import gz_v5 as m
from run_v31 import metrics
from eq_tests_v5 import R as R5
R = dict(R5)
N_DRAWS, N, SEED = 400, 40_000, 20261201
HK = dict(BAN_RED=0.0, BOARD=False, REBAND=False, ZHIBIAO=0.0, NONHUKOU=0.0, QUOTA=1.0, MINBAN_PEN=0.0,
          ELITE_BUY=0.2, ZONE_ADMIT=0.3, ART_SHARE=0.0, HK_SHARE=0.0)
SC = dict(CURRENT={}, OLD=dict(BAN_RED=0.0, BOARD=False, REBAND=False), HK_STYLE=HK,
          BAN_PERFECT=dict(BAN_RED=1.0), TIME_CONTROL=dict(TERM_SHARE=0.0, HOL_SHARE=0.0, FT_SHARE=0.0))
COST = dict(pre=15_000 * 3, term=17_540 * 2, hol=10_000 * 2)   # yuan per pupil over the stage (CIEFR participant mean for term)


def extra(d, p):
    a = d['acad']; n = a.size; w = d['logw']; q = np.searchsorted(np.quantile(w, [.2, .4, .6, .8]), w)
    spend = COST['pre'] * d['pre'] + COST['term'] * d['term'] + COST['hol'] * d['hol'] + 2 * p['FT_COST'] * d['ft']
    # individual effect of post-gate tutoring and the full-time route on own admission, cutoff held fixed
    inschool = d['hteach2'] + d['peer2']
    gain = p['POST_EFF'] * (d['term'].astype(float) + d['hol']) + np.where(d['ft'], p['FT_EFF'] - inschool, 0.0)
    cut = np.sort(np.where(a, d['gk_eff'], -np.inf))[::-1][int(.10 * n) - 1]
    with_ = a & (d['gk_eff'] >= cut); without = a & (d['gk_eff'] - gain >= cut)
    rich = a & (q == 4); spent = spend[rich] - COST['pre'] * d['pre'][rich]
    pp_per_100k = float((with_[rich].astype(float) - without[rich]).sum() / max(spent.sum(), 1) * 1e5 * 100)
    rr = (np.argsort(np.argsort(spend)) + .5) / n
    return dict(spend_mean=float(spend.mean()), spend_rich=float(spend[q == 4].mean()), spend_poor=float(spend[q == 0].mean()),
                pre_takeup=float(d['pre'].mean()), post_takeup=float((d['term'] | d['hol'])[a].mean()),
                rich_pp_per_100k=pp_per_100k, uni_share_rich=float(d['uni'][q == 4].mean() / d['uni'].mean() / 5 * 5),
                conc_spend=float(2 * np.cov(spend, (np.argsort(np.argsort(w)) + .5) / n, bias=True)[0, 1] / max(spend.mean(), 1)))


def one(item):
    i, dr = item; out = {'i': i, 'params': dr}
    for name, kw in SC.items():
        try:
            par = {**dr, 'HS_TEACH_SD': dr['TEACH_SD'], **kw}
            d = m.run(n=N, seed=SEED + i, **par); r = metrics(d); r.update(extra(d, {**m.P, **par})); out[name] = r
        except Exception as e:
            out[name] = {'error': repr(e)}
    return out


if __name__ == '__main__':
    rng = np.random.default_rng(SEED); keys = list(R)
    U = (rng.permuted(np.tile(np.arange(N_DRAWS), (len(keys), 1)), axis=1).T + rng.random((N_DRAWS, len(keys)))) / N_DRAWS
    draws = [{k: R[k][0] + U[i, j] * (R[k][1] - R[k][0]) for j, k in enumerate(keys)} for i in range(N_DRAWS)]
    with Pool(2) as pool: res = pool.map(one, list(enumerate(draws)), chunksize=8)
    with open('/home/claude/sig/v6_results.jsonl', 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    man = {fn: hashlib.sha256(open(f'/home/claude/sig/{fn}', 'rb').read()).hexdigest()
           for fn in ('gz_v5.py', 'run_v6.py', 'PREREG_V6.md', 'v6_results.jsonl')}
    man.update(n_draws=N_DRAWS, n=N, seed=SEED); json.dump(man, open('/home/claude/sig/v6_manifest.json', 'w'), indent=1)
    print('done', len(res), 'errors', sum('error' in r[k] for r in res for k in SC))
