#!/usr/bin/env python3
"""Do the Atlas inventory equations hold in the Guangzhou system? Fit each to gz_v5 output and compare with the
model's known truth, across a sweep of unknown parameters. ILLUSTRATIVE. Rules fixed in PREREG_V5_EQUATIONS.md."""
import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/sig')
import gz_v5 as m
from eq_tests import tests as base_tests
from run_v4 import R as R4

R = {**R4, 'INSURE': (0, 2), 'RHO_DEMAND': (0, 1), 'ART_SHARE': (0, .06), 'ART_BONUS': (.3, 1.2), 'HK_SHARE': (0, .02),
     'HK_BONUS': (.5, 1.5)}
N_DRAWS, N, SEED = 300, 40_000, 20261130


def ols(y, X):
    X = np.column_stack([np.ones(len(y))] + list(X)); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b; s2 = e @ e / (len(y) - X.shape[1]); se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X))); return b, se


def logit(y, X, it=25):
    X = np.column_stack([np.ones(len(y))] + list(X)); b = np.zeros(X.shape[1])
    for _ in range(it):
        pr = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30))); W = pr * (1 - pr) + 1e-9
        b += np.linalg.solve(X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1]), X.T @ (y - pr))
    pr = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30))); ll = np.sum(y * np.log(pr + 1e-12) + (1 - y) * np.log(1 - pr + 1e-12))
    p0 = y.mean(); ll0 = len(y) * (p0 * np.log(p0 + 1e-12) + (1 - p0) * np.log(1 - p0 + 1e-12))
    return b, 1 - ll / ll0


def eq_ratio(d, out, A, B, mask):
    tal = d['tal']; hi = tal >= np.quantile(tal, .8)
    bins = np.searchsorted(np.quantile(tal[hi], np.linspace(0, 1, 11)[1:-1]), tal)
    a = [out[hi & (bins == k) & mask & A].mean() for k in range(10)]; b = [out[hi & (bins == k) & mask & B].mean() for k in range(10)]
    return float(np.nanmean(a) / max(np.nanmean(b), 1e-9))


def one(item):
    i, dr = item
    d = m.run(n=N, seed=SEED + i, **{**dr, 'HS_TEACH_SD': dr['TEACH_SD']})
    a = d['acad']; tut = (d['term'] | d['hol']).astype(float); gk = d['gk']; zk = d['zk']; lw = d['logw']
    truth_post = dr['POST_EFF']; out = {'i': i, 'params': dr}
    # E74 baseline tutoring-achievement (no controls) and E72-type with prior score + SES controls
    out['E74_naive'] = float(ols(gk[a], [tut[a]])[0][1])
    out['E74_controls'] = float(ols(gk[a], [tut[a], zk[a], lw[a]])[0][1])
    # truth of the average effect of 'any tutoring' on gaokao for takers: POST_EFF x (term+hol) among takers
    nt = (d['term'].astype(float) + d['hol'])[a]; out['truth_any_tut'] = float(truth_post * nt[tut[a] > 0].mean()) if (tut[a] > 0).any() else 0.0
    # E76 SES x tutoring interaction (truth: zero, effect is homogeneous)
    b, se = ols(gk[a], [tut[a], zk[a], lw[a], tut[a] * lw[a]]); out['E76_coef'] = float(b[4]); out['E76_t'] = float(b[4] / se[4])
    # E58 participation logit: income only; then with score and score squared (U-shape)
    y = d['hol'][a].astype(float); _, r1 = logit(y, [lw[a]]); bq, r2 = logit(y, [lw[a], d['sr'][a], d['sr'][a] ** 2])
    out['E58_R2_income_only'] = float(r1); out['E58_R2_with_U'] = float(r2); out['E58_score_sq_coef'] = float(bq[3])
    # E79 peer effect in demand: own holiday tutoring on classmates' mean (leave-one-out)
    c = d['cls2']; ok = a & (c >= 0); uc, inv = np.unique(c[ok], return_inverse=True)
    s = np.bincount(inv, weights=y[(c[a] >= 0)] if False else d['hol'][ok].astype(float)); cnt = np.bincount(inv)
    loo = (s[inv] - d['hol'][ok]) / np.maximum(cnt[inv] - 1, 1)
    out['E79_coef'] = float(ols(d['hol'][ok].astype(float), [loo, d['sr'][ok], lw[ok]])[0][1])
    # school / class / peer / RD equations (from eq_tests)
    t = base_tests(d)
    out.update(E35=t['E35_naive_elite_gap'], E159=t['E159_between_school_share'], VA_share=t['truth_VA_share_of_variance'],
               E36=t['E36_peer_coef'], E152=t['E152_fuzzyRD_elite_effect'], E32=t['E32_VA_elite_coef'],
               E34_corr=t['E34_teacher_est_vs_true_corr'], E133=t['E133_rank_rank_slope'], E131=t['E131_conc_elite_uni'])
    # alternative gates: wealth gap with and without art/HK routes (same pupils, same seats)
    h = d['hukou']; q = np.searchsorted(np.quantile(lw[h], [.2, .4, .6, .8]), lw)
    g0 = np.where(a, gk, -np.inf); uni0 = g0 >= np.sort(g0)[::-1][int(.10 * N) - 1]
    out['EO_with_routes'] = eq_ratio(d, d['uni'], q >= 3, q <= 1, h); out['EO_no_routes'] = eq_ratio(d, uni0, q >= 3, q <= 1, h)
    out['route_share_of_seats'] = float((d['uni'] & (d['art'] | d['hkr'])).mean() / d['uni'].mean())
    out['tut_takeup'] = float(tut[a].mean())
    return out


if __name__ == '__main__':
    rng = np.random.default_rng(SEED); keys = list(R)
    U = (rng.permuted(np.tile(np.arange(N_DRAWS), (len(keys), 1)), axis=1).T + rng.random((N_DRAWS, len(keys)))) / N_DRAWS
    draws = [{k: R[k][0] + U[i, j] * (R[k][1] - R[k][0]) for j, k in enumerate(keys)} for i in range(N_DRAWS)]
    with Pool(2) as pool: res = pool.map(one, list(enumerate(draws)), chunksize=6)
    with open('/home/claude/sig/v5_eq_results.jsonl', 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    print('done', len(res))
