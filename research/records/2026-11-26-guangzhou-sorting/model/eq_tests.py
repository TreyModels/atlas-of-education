#!/usr/bin/env python3
"""Fit inventory equations (prior/equation-inventory-20261124.txt numbering) to gz_v3 output and compare with
the model's known truth. ILLUSTRATIVE. Verdicts: HOLDS / BIASED (sign right, size off) / MISLEADS (wrong sign or
wrong mechanism) / BY CONSTRUCTION."""
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/sig')
import gz_v3 as m


def ols(y, X):
    X = np.column_stack([np.ones(len(y))] + list(X)); b = np.linalg.lstsq(X, y, rcond=None)[0]; return b


def conc(y, w):
    r = (np.argsort(np.argsort(w)) + .5) / w.size
    return float(2 * np.cov(y, r, bias=True)[0, 1] / y.mean())


def tests(d):
    p = d['p']; a = d['acad']; out = {}
    gk, zk, hs = d['gk'], d['zk'], d['hs']
    el_school = (hs >= 0) & (hs < d['n_elite_hs'])
    # E35 school fixed effects: elite-school mean minus regular, raw and with lagged score
    out['E35_naive_elite_gap'] = float(gk[a & el_school].mean() - gk[a & ~el_school].mean())
    out['E32_VA_elite_coef'] = float(ols(gk[a], [zk[a], el_school[a].astype(float)])[2])
    out['truth_school_VA_gap'] = p['SCHOOL_VA']
    # E151-153 RD at the open-ranking elite cutoff (fuzzy because of zhibiao): local linear, bandwidth 0.15
    open_el = d['elite'] & ~d['zhib']
    cut = zk[open_el].min()
    x = zk - cut; w = a & (np.abs(x) < .15)
    above = (x >= 0).astype(float)
    fs = ols(el_school[w].astype(float), [above[w], x[w], (x * above)[w]])[1]
    rf = ols(gk[w], [above[w], x[w], (x * above)[w]])[1]
    out['E152_fuzzyRD_elite_effect'] = float(rf / fs) if abs(fs) > .05 else float('nan')
    out['RD_first_stage'] = float(fs)
    # truth at the margin: school VA gap minus lost top-band (teacher+peer) chance
    near = w
    out['truth_margin_band_rate_elite'] = float(d['band2'][near & el_school].mean())
    out['truth_margin_band_rate_regular'] = float(d['band2'][near & ~el_school].mean())
    # E159 multilevel: between-high-school share of gaokao variance vs share due to true school VA
    g = gk[a]; s = hs[a]; means = np.array([g[s == k].mean() for k in np.unique(s)])
    sizes = np.array([(s == k).sum() for k in np.unique(s)])
    between = float(np.sum(sizes * (means - g.mean()) ** 2) / np.sum((g - g.mean()) ** 2))
    out['E159_between_school_share'] = between
    out['truth_VA_share_of_variance'] = float(np.var(d['school_va'][a]) / np.var(g))
    # E34 junior teacher effects: class means of zhongkao, demeaned within junior school (classes randomly assigned)
    key = d['jr'] * 100 + np.array([0])  # placeholder
    jr = d['jr']; jt = d['jteach']
    cls_id = jr * 100 + np.searchsorted(np.unique(jt), jt) % 100
    est, tru = [], []
    for j in range(p['N_JUNIOR']):
        mj = jr == j; zj = zk[mj].mean()
        for t in np.unique(jt[mj]):
            mc = mj & (jt == t)
            if mc.sum() >= 5: est.append(zk[mc].mean() - zj); tru.append(t - jt[mj].mean())
    est, tru = np.array(est), np.array(tru)
    out['E34_teacher_est_vs_true_corr'] = float(np.corrcoef(est, tru)[0, 1])
    out['E34_reliability_slope'] = float(ols(tru, [est])[1])
    within_t = float(np.var(tru) / np.var(zk))
    out['within_school_teacher_share_zk'] = within_t
    # E36 linear-in-means peer effect at senior 2: gaokao on own obs score and class mean score
    c2 = d['cls2']; aa = a & (c2 >= 0)
    cm = {}
    for c in np.unique(c2[aa]): cm[c] = zk[aa & (c2 == c)].mean()
    peer_mean = np.array([cm.get(c, np.nan) for c in c2])
    b = ols(gk[aa], [zk[aa], peer_mean[aa]])
    out['E36_peer_coef'] = float(b[2])
    out['truth_peer_part_of_top_class'] = p['PEER'] / (p['PEER'] + p['TOP_TEACH'])
    # E129/E131/E133 inequality of outcomes by wealth
    gfull = np.where(a, gk, gk.min() - 10 + zk * 1e-3)   # vocational ranked below academic
    nn = gk.size
    out['E133_rank_rank_slope'] = float(ols((np.argsort(np.argsort(gfull)) + .5) / nn, [(np.argsort(np.argsort(d['logw'])) + .5) / nn])[1])
    out['E131_conc_elite_uni'] = conc(d['uni'].astype(float), d['logw'])
    # E116/E117 benefit incidence of high-school subsidies [D: public academic 41,500/yr; vocational 34,900+3,500]
    sub = np.where(a, 41_500, 38_400) * 3.0
    out['E117_conc_HS_subsidy'] = conc(sub, d['logw'])
    sub_novoc = np.where(a, 41_500 * 3.0, 0.0)
    out['E117_conc_if_no_vocational_subsidy'] = conc(sub_novoc, d['logw'])
    # E123 Gini of subsidy received
    x = np.sort(sub); k = x.size
    out['E123_gini_HS_subsidy'] = float((2 * np.arange(1, k + 1) - k - 1).dot(x) / (k * x.sum()))
    # E179 seat constraint
    out['E179_elite_seats_ok'] = bool(d['elite'].sum() <= int(p['ELITE'] * p['n']))
    return out


if __name__ == '__main__':
    res = {}
    for name, kw in {'current (zhibiao 50%, reband)': {}, 'no zhibiao': dict(ZHIBIAO=0.0),
                     'no reband': dict(REBAND=False), 'teacher SD 0.4': dict(TEACH_SD=0.4, HS_TEACH_SD=0.4)}.items():
        rs = [tests(m.run(seed=s, **kw)) for s in range(5)]
        res[name] = {k: float(np.nanmean([r[k] for r in rs])) for k in rs[0]}
    json.dump(res, open('/home/claude/sig/eq_tests_results.json', 'w'), indent=1)
    for k in res['current (zhibiao 50%, reband)']:
        print(f'{k:40s}' + ''.join(f'{res[n][k]:10.3f}' for n in res))
