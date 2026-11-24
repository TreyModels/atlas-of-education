"""Q5. How far back can a backcast be trusted?  Mask-and-recover validation (no variable is imputed from another variable).
Truth: long_run_panel.csv 1950-2020 (UN / WDI / Maddison / Barro-Lee-Lee; modelled in places, so 'truth' = best available series, not ground truth).
For each series and each country with a complete 1950-2020 record: pretend observation starts at ANCHOR=1990 and backcast 1950-1989.
Methods (own-history or donor-history only):
  M0 carry back the 1990 level (naive); M1 country linear trend fitted on 1990-2004, extrapolated back;
  M2 donor-dynamics: pooled backward-change model  z(t)-z(t+1) ~ 1 + z(t+1) + z(t+1)^2  fitted on DONOR countries 1950-1989, run backwards from the target's 1990 value;
  M3 analog: mean change 1990->t of the 5 donors nearest in (1990 level, 1990-2000 slope).
Scenarios: RANDOM (random half donors, 3 repeats) and RICH->POOR (donors = richest half by 1990 log GDP, targets = poorest half; the realistic case, long histories exist for early developers).
Metrics: RMSE in original units by horizon band; skill = 1 - RMSE/RMSE(M0); 80% interval coverage from a calibration half of the targets.
Usage: python3 -I q5_backcast_validation.py ../data -> q5_backcast.csv, q5_backcast_summary.txt
"""
import sys, numpy as np, pandas as pd
base = sys.argv[1].rstrip('/') + '/'
P = pd.read_csv(base + 'long_run_panel.csv')
SER = {  # column: (transform, inverse, step)
    'tfr_observed_1950plus': (np.log, np.exp, 1), 'child_mortality_per100': (np.log, np.exp, 1), 'life_expectancy_years': (lambda x: x, lambda x: x, 1),
    'urban_share_pct': (lambda x: np.log(x/(100-x)), lambda z: 100/(1+np.exp(-z)), 1), 'mean_years_schooling': (np.log1p, np.expm1, 5),
    'gdp_pc_maddison_1990int': (np.log, np.exp, 1)}
ANCHOR = 1990; BANDS = [(1, 10), (11, 20), (21, 30), (31, 40)]
rng = np.random.default_rng(20261124)
gdp = P[P.year == ANCHOR].set_index('iso3').gdp_pc_maddison_1990int

def wide(col, step):
    w = P[(P.year >= 1950) & (P.year <= 2020) & (P.year % step == 0)].pivot(index='iso3', columns='year', values=col)
    return w.dropna()

def methods(Z, years, donors, targets, step):
    ia = years.index(ANCHOR); hid = [j for j in range(ia)]; res = {}
    # M2 backward-change model from donors
    X, Y = [], []
    for j in range(ia):
        later = Z.loc[donors].iloc[:, j+1].values; X.append(np.c_[np.ones(len(donors)), later, later**2]); Y.append(Z.loc[donors].iloc[:, j].values - later)
    beta = np.linalg.lstsq(np.vstack(X), np.concatenate(Y), rcond=None)[0]
    n_slope = max(3, int(15/step)); n_slope2 = max(3, int(10/step) + 1)
    sl_d = np.array([np.polyfit(np.arange(n_slope2), Z.loc[d].iloc[ia:ia+n_slope2].values, 1)[0] for d in donors]); zA_d = Z.loc[donors].iloc[:, ia].values
    for c in targets:
        z = Z.loc[c].values; za = z[ia]; out = {}
        out['M0'] = np.full(ia, np.mean(z[ia:ia+3]))
        b = np.polyfit(np.arange(n_slope), z[ia:ia+n_slope], 1); out['M1'] = np.array([b[1] + b[0]*(j-ia) for j in range(ia)])
        pred = np.empty(ia); cur = za
        for j in range(ia-1, -1, -1):
            cur = cur + beta @ np.array([1, cur, cur**2]); pred[j] = cur
        out['M2'] = pred
        s = np.polyfit(np.arange(n_slope2), z[ia:ia+n_slope2], 1)[0]
        d_sc = np.sqrt(((zA_d - za)/zA_d.std())**2 + ((sl_d - s)/(sl_d.std()+1e-9))**2); nn = np.argsort(d_sc)[:5]
        out['M3'] = za + np.mean([Z.loc[donors[k]].values[:ia] - Z.loc[donors[k]].values[ia] for k in nn], axis=0)
        res[c] = out
    return res

rows = []
for col, (tf, inv, step) in SER.items():
    W = wide(col, step); Z = W.apply(lambda s: tf(s)).replace([np.inf, -np.inf], np.nan).dropna(); W = W.loc[Z.index]; years = list(W.columns); ia = years.index(ANCHOR)
    for scen in ('RANDOM1', 'RANDOM2', 'RANDOM3', 'RICH_TO_POOR'):
        idx = list(Z.index)
        if scen.startswith('RANDOM'):
            perm = rng.permutation(len(idx)); donors = [idx[i] for i in perm[:len(idx)//2]]; targets = [idx[i] for i in perm[len(idx)//2:]]
        else:
            g = gdp.reindex(idx).dropna().sort_values(); donors = list(g.index[len(g)//2:]); targets = list(g.index[:len(g)//2])
        if len(donors) < 10 or len(targets) < 10: continue
        pr = methods(Z, years, donors, targets, step)
        for c in targets:
            truth = W.loc[c].values[:ia]
            for m, zz in pr[c].items():
                for j in range(ia):
                    rows.append(dict(series=col, scenario=scen, method=m, iso3=c, horizon=ANCHOR - years[j], err=inv(zz[j]) - truth[j], abs_err=abs(inv(zz[j]) - truth[j]), z_err=zz[j] - Z.loc[c].values[j]))
df = pd.DataFrame(rows); df.to_csv('q5_backcast.csv.gz', index=False, compression='gzip')
def band(h): return next((f'{a}-{b}' for a, b in BANDS if a <= h <= b), None)
df['band'] = df.horizon.map(band); df = df.dropna(subset=['band'])
L = ['RMSE in original units by horizon band (years before the 1990 anchor); skill = 1 - RMSE/RMSE(M0); cov80 = coverage of an 80% interval built from the calibration half (|error| 80th percentile by method, series, scenario, band; in transformed units)']
for col in SER:
    for scen_grp, scens in (('RANDOM(avg of 3)', ['RANDOM1', 'RANDOM2', 'RANDOM3']), ('RICH->POOR', ['RICH_TO_POOR'])):
        x = df[(df.series == col) & df.scenario.isin(scens)]
        if x.empty: continue
        L.append(f'\n{col} | {scen_grp} | targets per scenario ~ {x.groupby("scenario").iso3.nunique().mean():.0f}')
        base_rmse = x[x.method == 'M0'].groupby('band').err.apply(lambda e: np.sqrt((e**2).mean()))
        for m in ('M0', 'M1', 'M2', 'M3'):
            xm = x[x.method == m]; r = xm.groupby('band').err.apply(lambda e: np.sqrt((e**2).mean()))
            cov = []
            for b in [f'{a}-{c}' for a, c in BANDS]:
                xb = xm[xm.band == b]; isos = sorted(xb.iso3.unique()); half = set(isos[::2]); cal = xb[xb.iso3.isin(half)].z_err.abs(); te = xb[~xb.iso3.isin(half)].z_err.abs()
                cov.append(np.nan if len(cal) < 20 or len(te) < 20 else float((te <= cal.quantile(0.8)).mean()))
            L.append(f'  {m}: ' + '  '.join(f'{b} RMSE {r[b]:.3g} skill {1 - r[b]/base_rmse[b]:+.2f} cov80 {c:.2f}' for b, c in zip([f"{a}-{c}" for a, c in BANDS], cov) if b in r.index))
open('q5_backcast_summary.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
