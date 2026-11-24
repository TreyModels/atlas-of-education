"""Q3. Does the logistic still lose to exponential-to-floor when the pre-transition plateau is observed?  (E14 + E15)
Data: long_run_panel.csv effective_fertility (Gapminder/OWID reconstruction before 1950, UN/WDI after; MEASUREMENT CAVEAT: pre-1950 values are modelled).
Models (all fitted by bounded least squares, 8 starts each; BIC = n ln(RSS/n) + k ln n):
  logistic (4), gompertz (4), exp_floor with free onset kink (4), double_logistic (7: two summed logistic declines; stand-in for Alkema et al. 2011).
Window: transition = first year with data (>=1750) up to the first sustained rebound (smoothed TFR rises >=0.4 above its running minimum) or 2023.
Two windows per country: FULL (from first observation) and CENSORED_20PCT (artificially left-censored: starts once 20% of the fall has already happened, mimicking a series that begins mid-transition), same end year. Hold-out RMSE = fit on all but the last 10
years of the window, predict those 10 (skipped if the window has < 40 years).
Usage: python3 -I q3_form_race.py ../data  -> q3_form_race.csv, q3_form_race_summary.txt
"""
import sys, json, warnings, numpy as np, pandas as pd
from scipy.optimize import least_squares
warnings.filterwarnings('ignore')
base = sys.argv[1].rstrip('/') + '/'
d = pd.read_csv(base + 'long_run_panel.csv').dropna(subset=['effective_fertility'])
if len(sys.argv) > 2:      # optional extra long-run TFR (e.g. OWID/HFD download): csv with columns iso3,year,tfr  -> overrides the panel for those countries
    ex = pd.read_csv(sys.argv[2]).rename(columns={'tfr': 'effective_fertility'})[['iso3', 'year', 'effective_fertility']]
    d = pd.concat([d[~d.iso3.isin(ex.iso3.unique())][['iso3', 'year', 'effective_fertility']], ex])
rng = np.random.default_rng(20261124)

def logistic(p, t):  return p[0] + (p[1]-p[0]) / (1 + np.exp(np.clip(p[2]*(t-p[3]), -50, 50)))
def gompertz(p, t):  return p[0] + (p[1]-p[0]) * np.exp(-np.exp(np.clip(p[2]*(t-p[3]), -50, 50)))
def expfloor(p, t):  return np.where(t < p[3], p[1], p[0] + (p[1]-p[0]) * np.exp(-p[2]*np.maximum(t-p[3], 0)))
def dlogis(p, t):
    f, c, a1, k1, m1, k2, m2 = p
    return f + a1*(1/(1+np.exp(np.clip(k1*(t-m1), -50, 50)))) + (c-f-a1)*(1/(1+np.exp(np.clip(k2*(t-m2), -50, 50))))
MODELS = {'logistic': (logistic, 4), 'gompertz': (gompertz, 4), 'exp_floor': (expfloor, 4), 'double_logistic': (dlogis, 7)}

def starts(name, t, y):
    T = t.max(); lo, hi = 0.5, max(y.max(), 3.0) + 1.0; out = []
    for _ in range(8):
        f0, c0 = rng.uniform(lo, 2.2), y[:max(3, len(y)//10)].mean()
        k0, m0 = rng.uniform(0.02, 0.2), rng.uniform(0.2, 0.8) * T
        if name == 'double_logistic':
            out.append([f0, c0, (c0-f0)*rng.uniform(.2, .8), rng.uniform(0.02, .3), rng.uniform(.2, .6)*T, rng.uniform(0.02, .3), rng.uniform(.5, .95)*T])
        else: out.append([f0, c0, k0, m0])
    return out, lo, hi, T

def fit(name, t, y):
    fn, k = MODELS[name]; st, lo, hi, T = starts(name, t, y); best = None
    for p0 in st:
        if name == 'double_logistic':
            lb = [0.3, 1.0, 0, 0.005, 0, 0.005, 0]; ub = [3.5, hi, hi, 1.0, T, 1.0, T*1.5 + 50]
            p0 = list(np.clip(p0, lb, ub))
        else:
            lb = [0.3, 1.0, 0.003, -T]; ub = [3.5, hi, 1.0, T*1.5 + 50]; p0 = list(np.clip(p0, lb, ub))
        try: r = least_squares(lambda p: fn(p, t) - y, p0, bounds=(lb, ub), max_nfev=400)
        except Exception: continue
        if best is None or r.cost < best.cost: best = r
    return best

def end_year(s):
    """end of the first transition: running minimum of the smoothed series, cut at the first rebound >= 0.4, but only once the series has fallen below 65% of its peak."""
    sm = s.rolling(5, center=True, min_periods=1).mean(); peak = sm.max(); rm, ry = np.inf, sm.index[0]
    for yr, v in sm.items():
        if v < rm: rm, ry = v, yr
        elif v - rm >= 0.4 and rm <= 0.65*peak: return int(ry)
    return int(s.index[-1])

def censored_start(s, e):
    """artificial left-censoring: start when 20% of the total fall (peak -> minimum within the window) has already happened."""
    w = s[s.index <= e].rolling(5, center=True, min_periods=1).mean(); peak, lo = w.max(), w.min(); py = w.idxmax()
    after = w[w.index >= py]; return int(after[after <= peak - 0.2*(peak - lo)].index[0])

rows = []
for iso, g in d.groupby('iso3'):
    s = g.set_index('year').effective_fertility.sort_index()
    if s.index.min() > 1900 or s.index.max() < 2000 or len(s) < 100: continue          # needs an observed pre-1900 plateau
    e = end_year(s)
    for wname, start in (('FULL', int(s.index.min())), ('CENSORED_20PCT', censored_start(s, e))):
        w = s[(s.index >= start) & (s.index <= e)]
        if len(w) < 20: continue
        t = (w.index.values - w.index.values[0]).astype(float); y = w.values
        rec = dict(iso3=iso, window=wname, start=int(w.index[0]), end=e, n=len(w), y_start=round(float(y[:5].mean()), 2), y_end=round(float(y[-3:].mean()), 2))
        bic = {}
        for m, (fn, k) in MODELS.items():
            r = fit(m, t, y)
            if r is None: continue
            rss = 2*r.cost; bic[m] = len(y)*np.log(max(rss/len(y), 1e-12)) + k*np.log(len(y)); rec[f'bic_{m}'] = round(bic[m], 1)
            if len(w) >= 40:
                rt = fit(m, t[:-10], y[:-10]); rec[f'rmse_{m}'] = round(float(np.sqrt(np.mean((MODELS[m][0](rt.x, t[-10:]) - y[-10:])**2))), 3) if rt is not None else np.nan
        rec['winner_bic'] = min(bic, key=bic.get) if bic else None; rows.append(rec)
df = pd.DataFrame(rows); df.to_csv('q3_form_race.csv', index=False)
L = [f'countries with a pre-1900 plateau: {df.iso3.nunique()}; windows fitted: {len(df)}', 'transition end = first sustained rebound (baby boom excluded) or 2023']
for w in ('FULL', 'CENSORED_20PCT'):
    x = df[df.window == w]; vc = x.winner_bic.value_counts(); L.append(f'\n{w}: n={len(x)} BIC winners: ' + ', '.join(f'{k} {v} ({100*v/len(x):.0f}%)' for k, v in vc.items()))
    for m in MODELS:
        c = f'rmse_{m}'
        if c in x: L.append(f'  hold-out RMSE (last 10 y) {m:16s} median {x[c].median():.3f}  mean {x[c].mean():.3f}  (n={x[c].notna().sum()})')
open('q3_form_race_summary.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L)); print(df[df.window == 'FULL'][['iso3', 'start', 'end', 'n', 'winner_bic']].head(40).to_string(index=False))
