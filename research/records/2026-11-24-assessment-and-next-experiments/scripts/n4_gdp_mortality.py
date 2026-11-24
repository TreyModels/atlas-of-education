"""N4 extension: income at onset (GDP per capita from 1960) and starting child mortality as correlates of
fertility-transition timing. Post-hoc, exploratory; HC1 robust SEs; countries as rows.
Inputs: ../data/n4_country_shape_parameters.csv (identical to fix/n4 results/country_shape_parameters.csv),
        ../data/gdppc_log.json, ../data/u5mr.json.   Usage: python3 -I n4_gdp_mortality.py ../data"""
import sys, json, numpy as np, pandas as pd, statsmodels.api as sm
base = sys.argv[1].rstrip('/') + '/'
D = pd.read_csv(base + 'n4_country_shape_parameters.csv')
def load(f):
    d = {}
    for iso, y, v in json.load(open(base + f)):
        if v is not None: d.setdefault(iso, {})[y] = v
    return d
g, u = load('gdppc_log.json'), load('u5mr.json')
def near(s, yr, tol=2):
    for k in range(tol+1):
        for yy in (yr-k, yr+k):
            if yy in s: return s[yy]
    return np.nan
D['lgdp'] = [np.log(v) if (v := near(g.get(i, {}), int(round(o)))) == v else np.nan for i, o in zip(D.iso, D.onset)]
# NOTE: gdppc_log.json holds GDP per capita in LEVELS despite its name (values 123-247,170); the log is taken here.
D['u5_start'] = [np.log(u[i][min(u[i])]) if i in u and min(u[i]) <= 1965 else np.nan for i in D.iso]
def t75(i):
    s = u.get(i)
    if not s: return np.nan
    ys = sorted(s); v0 = s[ys[0]]
    if ys[0] > 1965: return np.nan
    return next((float(y) for y in ys if s[y] <= 0.75*v0), np.nan)
D['u5_t75'] = [t75(i) for i in D.iso]
print('coverage: lgdp at onset', int(D.lgdp.notna().sum()), '| u5 start', int(D.u5_start.notna().sum()), '| u5 t75', int(D.u5_t75.notna().sum()), '| of', len(D))
out = {}
def reg(dep, preds):
    d = D.dropna(subset=[dep]+preds); m = sm.OLS(d[dep], sm.add_constant(d[preds])).fit(cov_type='HC1')
    r = {'n': int(len(d)), 'coef': {k: [round(float(m.params[k]), 3), round(float(m.bse[k]), 3)] for k in preds}, 'r2': round(float(m.rsquared), 2)}
    print(dep, preds, r); out[f'{dep} ~ {"+".join(preds)}'] = r
for dep in ('onset', 'midpoint'):
    for preds in (['lgdp'], ['school_50'], ['school_50', 'lgdp'], ['u5_t75'], ['u5_start'], ['school_50', 'u5_start'],
                  ['school_50', 'u5_start', 'lgdp'], ['school_50', 'u5_t75', 'lgdp', 'urban_onset']):
        reg(dep, preds)
json.dump(out, open('n4_gdp_mortality.json', 'w'), indent=1)
