"""Orthogonalised future-schooling placebo: does S(t+10) predict fertility(t) once S(t) is controlled?
Panel: 5-year country-years, standardised schooling, country-clustered OLS. Exploratory, 22 Nov panel (not the 23 Nov battery panel).
Usage: python3 -I placebo_orthogonal.py ../data > ../results/placebo_orthogonal.txt"""
import sys, json, numpy as np, pandas as pd, statsmodels.formula.api as smf
base = sys.argv[1].rstrip('/') + '/'
def load(n):
    return pd.DataFrame([(i, y, v) for i, y, v in json.load(open(base + n + '.json')) if v is not None], columns=['iso', 'year', n])
F = load('fertility'); res = {}
for sname in ['lsc', 'sec', 'prm_cmp', 'ter']:
    S = load(sname); d = F.merge(S, on=['iso', 'year'])
    fut = S.copy(); fut['year'] -= 10; fut = fut.rename(columns={sname: 'S10'})
    d = d.merge(fut, on=['iso', 'year']); d = d[d.year % 5 == 0].dropna().copy()
    for c in (sname, 'S10'): d[c] = (d[c] - d[c].mean()) / d[c].std()
    print(f'== {sname}  n={len(d)} countries={d.iso.nunique()}'); res[sname] = {}
    for form, lab in [(f'fertility ~ {sname}', 'S_t only'), ('fertility ~ S10', 'S_t+10 only'), (f'fertility ~ {sname} + S10', 'both'),
                      (f'fertility ~ {sname} + S10 + C(year)', 'both + year FE'), (f'fertility ~ {sname} + S10 + C(iso)', 'both + country FE')]:
        m = smf.ols(form, d).fit(cov_type='cluster', cov_kwds={'groups': d.iso})
        r = {k: [round(float(m.params[k]), 3), round(float(m.bse[k]), 3)] for k in (sname, 'S10') if k in m.params}
        res[sname][lab] = r; print('  ', lab, r, 'R2', round(m.rsquared, 3))
json.dump(res, open('placebo_orthogonal.json', 'w'), indent=1)
