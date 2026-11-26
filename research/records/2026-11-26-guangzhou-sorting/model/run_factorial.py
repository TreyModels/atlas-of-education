#!/usr/bin/env python3
"""Second-review analysis (PREREG_V7.md): 2^4 factorial over reform mechanisms with Shapley decomposition; joint
score-and-talent diagnostic S*; interventions on pre-15 inputs. Model gz_v5.py (v5.1). ILLUSTRATIVE."""
import json, itertools, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/sig')
import gz_v5 as m
from eq_tests_v5 import R as R5
N_DRAWS, N, SEED = 150, 30_000, 20261202
MECH = ['BAN', 'BOARD', 'REBAND', 'SUBST']   # each on = current Guangzhou setting, off = pre-2021 / absent
# Expenditure period: cumulative per pupil over junior secondary (3 years, pre-gate tutoring) and senior 1-2 (2 years).
COST = dict(pre=15_000 * 3, term=17_540 * 2, hol=10_000 * 2)


def setting(dr, on):
    kw = {}
    kw['BAN_RED'] = dr['BAN_RED'] if on['BAN'] else 0.0
    kw['BOARD'] = bool(on['BOARD'])
    kw['REBAND'] = bool(on['REBAND'])
    if not on['SUBST']:
        kw.update(HOL_SHARE=0.0, FT_SHARE=0.0, ART_SHARE=0.0, HK_SHARE=0.0)
    return kw


def ratios(d):
    h = d['hukou']; uni = d['uni']; w = d['logw']; tal = d['tal']; zk = d['zk']
    q = np.searchsorted(np.quantile(w[h], [.2, .4, .6, .8]), w); rich = h & (q >= 3); poor = h & (q <= 1)
    def binned(var, k=10):
        hi = var >= np.quantile(var, .8); b = np.searchsorted(np.quantile(var[hi], np.linspace(0, 1, k + 1)[1:-1]), var)
        return hi, b
    hiT, bT = binned(tal); hiZ, bZ = binned(zk)
    T = np.nanmean([uni[hiT & (bT == k) & rich].mean() for k in range(10)]) / np.nanmean([uni[hiT & (bT == k) & poor].mean() for k in range(10)])
    S = np.nanmean([uni[hiZ & (bZ == k) & rich].mean() for k in range(10)]) / np.nanmean([uni[hiZ & (bZ == k) & poor].mean() for k in range(10)])
    # S*: joint cells of zhongkao score (5) x talent (5) within the top fifth of zhongkao, standardised to the pooled cell mix
    hz5, bz5 = binned(zk, 5); bt5 = np.searchsorted(np.quantile(tal[hz5], np.linspace(0, 1, 6)[1:-1]), tal)
    num = den = 0.0
    for a in range(5):
        for b in range(5):
            c = hz5 & (bz5 == a) & (bt5 == b); cr, cp = c & rich, c & poor
            if cr.sum() >= 5 and cp.sum() >= 5:
                wgt = (cr.sum() + cp.sum()); num += wgt * uni[cr].mean(); den += wgt * uni[cp].mean()
    Sstar = num / den if den > 0 else np.nan
    U = uni[rich].mean() / max(uni[poor].mean(), 1e-9)
    return dict(S=float(S), S_star=float(Sstar), T=float(T), U=float(U))


def spend(d, p):
    return float((COST['pre'] * d['pre'] + COST['term'] * d['term'] + COST['hol'] * d['hol'] + 2 * p['FT_COST'] * d['ft']).mean())


def one(item):
    i, dr = item; base = {**dr, 'HS_TEACH_SD': dr['TEACH_SD']}; out = {'i': i, 'params': dr, 'cells': {}, 'interv': {}}
    for bits in itertools.product([0, 1], repeat=4):
        on = dict(zip(MECH, bits)); par = {**base, **setting(dr, on)}
        d = m.run(n=N, seed=SEED + i, **par); r = ratios(d); r['spend'] = spend(d, {**m.P, **par})
        out['cells'][''.join(map(str, bits))] = r
    cur = {**base, **setting(dr, dict.fromkeys(MECH, 1))}
    for name, kw in dict(NO_HOME=dict(HOME=0.0), NO_ZONE_TEACH=dict(TEACH_ZONE=0.0), NO_PRE_TUT=dict(PRE_EFF=0.0),
                         NO_HEAD_START=dict(HOME=0.0, TEACH_ZONE=0.0, PRE_EFF=0.0), NO_ROUTES=dict(ART_SHARE=0.0, HK_SHARE=0.0)).items():
        d = m.run(n=N, seed=SEED + i, **{**cur, **kw}); out['interv'][name] = ratios(d)
    return out


if __name__ == '__main__':
    rng = np.random.default_rng(SEED); keys = list(R5)
    U = (rng.permuted(np.tile(np.arange(N_DRAWS), (len(keys), 1)), axis=1).T + rng.random((N_DRAWS, len(keys)))) / N_DRAWS
    draws = [{k: R5[k][0] + U[i, j] * (R5[k][1] - R5[k][0]) for j, k in enumerate(keys)} for i in range(N_DRAWS)]
    with Pool(2) as pool: res = pool.map(one, list(enumerate(draws)), chunksize=4)
    with open('/home/claude/sig/v7_factorial.jsonl', 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    print('done', len(res))
