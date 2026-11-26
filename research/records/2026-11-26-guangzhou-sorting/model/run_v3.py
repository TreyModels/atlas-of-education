#!/usr/bin/env python3
"""Pre-registered v3 sweep (PREREG_V3.md)."""
import json, hashlib, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/sig')
import gz_v3 as m
from eq_tests import tests

R = dict(TEACH_SD=(.15, .45), TEACH_ZONE=(0, .25), HOME=(0, .3), DECAY=(0, .9), TAL_WEALTH=(0, .3), SCHOOL_VA=(0, .2),
         TOP_TEACH=(.2, .4), PEER=(.05, .25), ZHIBIAO=(.3, .6), NONHUKOU=(.1, .4), QUOTA=(.08, .2), MINBAN_PEN=(0, .3),
         NH_WEALTH=(-.6, 0), NOISE=(.25, .5))
N_DRAWS, N, SEED = 800, 40_000, 20261127


def eq_ratio(d, out, grpA, grpB, mask_extra=None):
    tal = d['tal']; hi = tal >= np.quantile(tal, .8)
    bins = np.searchsorted(np.quantile(tal[hi], np.linspace(0, 1, 11)[1:-1]), tal)
    a, b = [], []
    for k in range(10):
        mk = hi & (bins == k)
        if mask_extra is not None: mk &= mask_extra
        a.append(out[mk & grpA].mean() if (mk & grpA).any() else np.nan)
        b.append(out[mk & grpB].mean() if (mk & grpB).any() else np.nan)
    return float(np.nanmean(a) / max(np.nanmean(b), 1e-9))


def metrics(d):
    h = d['hukou']; uni = d['uni']; w = d['logw']
    wl = w[h]; q = np.searchsorted(np.quantile(wl, [.2, .4, .6, .8]), w)
    r = dict(EO_local=eq_ratio(d, uni, q >= 3, q <= 1, h), HUKOU_ratio=eq_ratio(d, uni, h, ~h))
    hiNH = (~h) & (d['tal'] >= np.quantile(d['tal'], .8))
    r.update(NH_hiTal_public=float(d['public'][hiNH].mean()), NH_hiTal_private=float(d['private'][hiNH].mean()),
             NH_hiTal_exit=float(d['exitp'][hiNH].mean()))
    rk = (np.argsort(np.argsort(w)) + .5) / w.size; s = d['subsidy']
    r['SUB_conc'] = float(2 * np.cov(s, rk, bias=True)[0, 1] / s.mean())
    r['SUB_gap'] = float(s[h].mean() - s[~h].mean())
    t = tests(d)
    r.update(E35=t['E35_naive_elite_gap'], E159=t['E159_between_school_share'], VA_share=t['truth_VA_share_of_variance'],
             E36=t['E36_peer_coef'], E152=t['E152_fuzzyRD_elite_effect'], VA_gap=t['truth_school_VA_gap'])
    return r


def one(item):
    i, dr = item; s = SEED + i
    sc = dict(CURRENT={}, NO_QUOTA=dict(QUOTA=1.0), EQUAL_MIGRANT=dict(QUOTA=1.0, MINBAN_PEN=0.0),
              NO_REBAND=dict(REBAND=False), NO_ZHIBIAO=dict(ZHIBIAO=0.0))
    out = {'i': i, 'params': dr}
    for name, kw in sc.items():
        par = {**dr, 'HS_TEACH_SD': dr['TEACH_SD'], **kw}
        try:
            out[name] = metrics(m.run(n=N, seed=s, **par))
        except Exception as e:
            out[name] = {'error': repr(e)}
    return out


if __name__ == '__main__':
    rng = np.random.default_rng(SEED); keys = list(R)
    U = (rng.permuted(np.tile(np.arange(N_DRAWS), (len(keys), 1)), axis=1).T + rng.random((N_DRAWS, len(keys)))) / N_DRAWS
    draws = [{k: R[k][0] + U[i, j] * (R[k][1] - R[k][0]) for j, k in enumerate(keys)} for i in range(N_DRAWS)]
    with Pool(2) as pool:
        res = pool.map(one, list(enumerate(draws)), chunksize=8)
    with open('/home/claude/sig/v3_results.jsonl', 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    man = {fn: hashlib.sha256(open(f'/home/claude/sig/{fn}', 'rb').read()).hexdigest()
           for fn in ('gz_v3.py', 'eq_tests.py', 'run_v3.py', 'PREREG_V3.md', 'v3_results.jsonl')}
    man.update(n_draws=N_DRAWS, n=N, seed=SEED); json.dump(man, open('/home/claude/sig/v3_manifest.json', 'w'), indent=1)
    print('done', len(res), 'errors', sum('error' in r[k] for r in res for k in r if isinstance(r[k], dict) and k != 'params'))
