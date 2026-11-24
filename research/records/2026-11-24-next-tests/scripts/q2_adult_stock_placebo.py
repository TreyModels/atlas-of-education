"""Q2. Does a placebo that fertility choices cannot contaminate still fire?  (E17 + E13)
Adult schooling stock = OWID / Barro-Lee-Lee mean years of schooling (population 25+), 5-year grid, long_run_panel.csv.
A: F(t) on S(t-10), S(t), S(t+10), S(t+20) with country FE and year FE (country-clustered SEs). Outcome: effective_fertility
   (1751+) and tfr_observed_1950plus. Standardised schooling. Read the *lead* terms: S(t+10), S(t+20).
B: direction test in 10-year changes (country FE): dF(t,t+10) on dS(t-10,t), dS(t,t+10), dS(t+10,t+20);
   and dS(t,t+10) on dF(t-10,t), dF(t,t+10), dF(t+10,t+20).
Usage: python3 -I q2_adult_stock_placebo.py ../data > q2_adult_stock_placebo.txt"""
import sys, json, numpy as np, pandas as pd, statsmodels.formula.api as smf
base = sys.argv[1].rstrip('/') + '/'
d = pd.read_csv(base + 'long_run_panel.csv'); d = d[d.year % 5 == 0].sort_values(['iso3', 'year'])
g = d.groupby('iso3')
out = {}
def fit(f, dat):
    return smf.ols(f, dat).fit(cov_type='cluster', cov_kwds={'groups': dat.iso3})
for F in ('effective_fertility', 'tfr_observed_1950plus'):
    x = d[['iso3', 'year', F, 'mean_years_schooling']].copy().rename(columns={F: 'F', 'mean_years_schooling': 'S'})
    gg = x.groupby('iso3')
    for k in (-10, 10, 20): x[f'S{k:+d}'.replace('+', 'p').replace('-', 'm')] = gg['S'].shift((-k) // 5)   # rows are 5-year steps
    x = x[(x.year >= 1950)].dropna(subset=['F', 'S', 'Sp10', 'Sm10'])
    for c in ('S', 'Sm10', 'Sp10', 'Sp20'):
        if c in x: x[c] = (x[c] - x[c].mean()) / x[c].std()
    print(f'=== A. level ladder, outcome {F}: n={len(x)} countries={x.iso3.nunique()} years {int(x.year.min())}-{int(x.year.max())}')
    res = {}
    for lab, f in [('S only', 'F ~ S'), ('S(t-10), S, S(t+10)', 'F ~ Sm10 + S + Sp10')]:
        for fe, term in [('year FE', '+ C(year)'), ('country+year FE', '+ C(year) + C(iso3)')]:
            m = fit(f + ' ' + term, x); res[f'{lab} | {fe}'] = {k: (round(m.params[k], 3), round(m.bse[k], 3)) for k in ('Sm10', 'S', 'Sp10') if k in m.params}
            print(f'  {lab:22s} {fe:16s}', res[f'{lab} | {fe}'])
    x2 = x.dropna(subset=['Sp20'])
    m = fit('F ~ Sm10 + S + Sp10 + Sp20 + C(year) + C(iso3)', x2)
    res['four-term | country+year FE'] = {k: (round(m.params[k], 3), round(m.bse[k], 3)) for k in ('Sm10', 'S', 'Sp10', 'Sp20')}
    print('  four-term ladder      country+year FE ', res['four-term | country+year FE'], 'n=', len(x2))
    out[F] = res
# B. direction test
x = d[['iso3', 'year', 'effective_fertility', 'mean_years_schooling']].rename(columns={'effective_fertility': 'F', 'mean_years_schooling': 'S'}).copy()
gg = x.groupby('iso3')
for v in ('F', 'S'):
    x[f'd{v}_prev'] = gg[v].shift(0) - gg[v].shift(2)      # t-10 -> t
    x[f'd{v}_next'] = gg[v].shift(-2) - gg[v].shift(0)     # t -> t+10
    x[f'd{v}_next2'] = gg[v].shift(-4) - gg[v].shift(-2)   # t+10 -> t+20
x = x[x.year >= 1950].dropna(subset=['dF_prev', 'dF_next', 'dF_next2', 'dS_prev', 'dS_next', 'dS_next2'])
for c in [c for c in x if c.startswith('d')]: x[c] = (x[c] - x[c].mean()) / x[c].std()
print(f'\n=== B. direction test, 10-year changes (standardised), country FE: n={len(x)} countries={x.iso3.nunique()}')
for lab, f, keys in [('dF(t,t+10) on dS prev/next/next2', 'dF_next ~ dS_prev + dS_next + dS_next2 + C(iso3)', ('dS_prev', 'dS_next', 'dS_next2')),
                     ('dS(t,t+10) on dF prev/next/next2', 'dS_next ~ dF_prev + dF_next + dF_next2 + C(iso3)', ('dF_prev', 'dF_next', 'dF_next2'))]:
    m = fit(f, x); r = {k: (round(m.params[k], 3), round(m.bse[k], 3)) for k in keys}; out[lab] = r; print(' ', lab, r)
json.dump(out, open('q2_adult_stock_placebo.json', 'w'), indent=1)
