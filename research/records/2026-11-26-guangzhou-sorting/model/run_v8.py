#!/usr/bin/env python3
"""Third-review analyses (PREREG_V8.md). Model gz_v5.py (v5.1). ILLUSTRATIVE."""
import json, itertools, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/sig')
import gz_v5 as m
from eq_tests_v5 import R as R5
N_DRAWS, N, SEED = 150, 40_000, 20261203
COST = dict(pre=15_000 * 3, term=17_540 * 2, hol=10_000 * 2)   # cumulative per pupil, junior 1-3 + senior 1-2
POST_OFF = dict(TERM_SHARE=0.0, HOL_SHARE=0.0, FT_SHARE=0.0, ART_SHARE=0.0, HK_SHARE=0.0)


def groups(d):
    h = d['hukou']; w = d['logw']; q = np.searchsorted(np.quantile(w[h], [.2, .4, .6, .8]), w)
    return h & (q >= 3), h & (q <= 1)


def ratio_binned(out, var, rich, poor, k=10):
    hi = var >= np.quantile(var, .8); b = np.searchsorted(np.quantile(var[hi], np.linspace(0, 1, k + 1)[1:-1]), var)
    a = np.nanmean([out[hi & (b == j) & rich].mean() for j in range(k)]); c = np.nanmean([out[hi & (b == j) & poor].mean() for j in range(k)])
    return float(a / c)


def sstar(out, zk, tal, rich, poor, k):
    hz = zk >= np.quantile(zk, .8)
    bz = np.searchsorted(np.quantile(zk[hz], np.linspace(0, 1, k + 1)[1:-1]), zk)
    bt = np.searchsorted(np.quantile(tal[hz], np.linspace(0, 1, k + 1)[1:-1]), tal)
    num = den = 0.0; used = 0; total = int((hz & (rich | poor)).sum()); cells = 0; ok = 0
    for a in range(k):
        for b in range(k):
            c = hz & (bz == a) & (bt == b); cr, cp = c & rich, c & poor
            if (cr | cp).any(): cells += 1
            if cr.sum() >= 5 and cp.sum() >= 5:
                ok += 1; wgt = cr.sum() + cp.sum(); used += wgt; num += wgt * out[cr].mean(); den += wgt * out[cp].mean()
    return dict(Sstar=float(num / den) if den else np.nan, support=used / max(total, 1), cells_ok=ok, cells=cells)


def measures(d, out=None):
    out = d['uni'] if out is None else out
    rich, poor = groups(d); zk, tal = d['zk'], d['tal']
    r = dict(T=ratio_binned(out, tal, rich, poor), S=ratio_binned(out, zk, rich, poor),
             U=float(out[rich].mean() / max(out[poor].mean(), 1e-9)))
    for k in (5, 10, 20):
        s = sstar(out, zk, tal, rich, poor, k); r[f'Sstar{k}'] = s['Sstar']; r[f'support{k}'] = s['support']; r[f'cells_ok{k}'] = s['cells_ok']; r[f'cells{k}'] = s['cells']
    return r


def ordinary(d):
    a = d['acad']; n = a.size; g = np.where(a, d['gk'], -np.inf)
    return g >= np.sort(g)[::-1][int(.10 * n) - 1]


def spend(d, p):
    return float((COST['pre'] * d['pre'] + COST['term'] * d['term'] + COST['hol'] * d['hol'] + 2 * p['FT_COST'] * d['ft']).mean())


def one(item):
    i, dr = item; base = {**dr, 'HS_TEACH_SD': dr['TEACH_SD']}; s = SEED + i; o = {'i': i, 'params': dr}
    d = m.run(n=N, seed=s, **base)
    o['CURRENT'] = measures(d); o['CURRENT_ordinary'] = measures(d, ordinary(d)); o['CURRENT']['spend'] = spend(d, {**m.P, **base})
    o['CURRENT']['learn'] = float(d['skill18'][d['acad']].mean()); o['CURRENT']['learn_all'] = float(d['skill18'].mean())
    d2 = m.run(n=N, seed=s, **{**base, **POST_OFF}); o['POST_OFF'] = measures(d2); o['POST_OFF_ordinary'] = measures(d2, ordinary(d2))
    # historically anchored: boarding and pre-existing holiday tutoring and routes held on; vary ban and re-banding
    o['HIST'] = {}
    for ban, rb in itertools.product([0, 1], repeat=2):
        par = {**base, 'BAN_RED': dr['BAN_RED'] if ban else 0.0, 'REBAND': bool(rb)}
        dd = m.run(n=N, seed=s, **par); r = measures(dd); r['spend'] = spend(dd, {**m.P, **par}); o['HIST'][f'{ban}{rb}'] = r
    # interventions, with learning totals (mean skill at 18 among academic pupils and in the whole cohort)
    o['INT'] = {}
    for name, kw in dict(NO_HOME=dict(HOME=0.0), NO_ZONE_TEACH=dict(TEACH_ZONE=0.0), NO_PRE_TUT=dict(PRE_EFF=0.0),
                         NO_HEAD_START=dict(HOME=0.0, TEACH_ZONE=0.0, PRE_EFF=0.0)).items():
        dd = m.run(n=N, seed=s, **{**base, **kw}); r = measures(dd)
        r['learn'] = float(dd['skill18'][dd['acad']].mean()); r['learn_all'] = float(dd['skill18'].mean()); o['INT'][name] = r
    return o


if __name__ == '__main__':
    rng = np.random.default_rng(SEED); keys = list(R5)
    U = (rng.permuted(np.tile(np.arange(N_DRAWS), (len(keys), 1)), axis=1).T + rng.random((N_DRAWS, len(keys)))) / N_DRAWS
    draws = [{k: R5[k][0] + U[i, j] * (R5[k][1] - R5[k][0]) for j, k in enumerate(keys)} for i in range(N_DRAWS)]
    with Pool(2) as pool: res = pool.map(one, list(enumerate(draws)), chunksize=4)
    with open('/home/claude/sig/v8_results.jsonl', 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    print('done', len(res))
