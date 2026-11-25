#!/usr/bin/env python3
"""Independent audit of the scout candidate estimates (runs/2026-11-25_all): point estimates and
design-based SEs recomputed from the frozen merged input; no restricted data leaves the Mac."""
import json, sys
import pandas as pd, numpy as np
RUN = 'runs/2026-11-25_all'; DATA = '/Users/treymenefee/neon-boot/dhs8_local/normalized_all.csv'
est = pd.read_csv(f'{RUN}/estimates.csv', dtype={'wave': str})
d = pd.read_csv(DATA, dtype={'wave': str})
SPECS = {'E1':('person',14,17,'attendance','wealth',None), 'E2':('person',14,17,'attendance','urban',None),
         'E3':('person',14,17,'attendance','sex',None), 'E4':('woman',40,49,'children_ever_born','education',None),
         'E5':('woman',25,34,'early_birth','education',None), 'E6':('person',20,24,'currently_in_school','urban',2),
         'E7':('woman',25,34,'early_union','education',None), 'E8':('woman',40,49,'household_size','education',None)}
def domain(df, row):
    rtype, lo, hi, outcol, group, sex = SPECS[row.experiment]
    z = df[(df.country == row.country) & (df.wave.astype(str) == str(row.wave)) & (df.record_type == rtype)].copy()
    z = z[pd.to_numeric(z.age, errors='coerce').between(lo, hi)]
    if sex is not None: z = z[pd.to_numeric(z.sex, errors='coerce') == sex]
    afb = pd.to_numeric(z.age_first_birth, errors='coerce'); afb[(afb > 0) & (afb < 10) & (afb != 99)] = np.nan
    afu = pd.to_numeric(z.age_first_union, errors='coerce'); afu[(afu > 0) & (afu < 10) & (afu != 99)] = np.nan
    outc = (afb < 20).astype(float) if outcol == 'early_birth' else (afu < 20).astype(float) if outcol == 'early_union' else pd.to_numeric(z[outcol], errors='coerce')
    grp = (pd.cut(pd.to_numeric(z.school_years, errors='coerce'), [-1,5,11,300], labels=['0-5','6-11','12+']).astype(object)
           if group == 'education' else pd.to_numeric(z[group], errors='coerce'))
    gs = pd.Series(grp, index=z.index)
    gk = gs.astype(str) if group == 'education' else gs.map(lambda v: str(int(v)) if (pd.notna(v) and np.isfinite(float(v))) else 'nan')
    ok = outc.notna() & gs.notna() & (gk == str(row.group))
    return z[ok], outc[ok], pd.to_numeric(z[ok].weight, errors='coerce')
def domain_mean_se(z, y, w):
    # full-design stratified one-stage with-replacement variance of the ratio mean (all base PSUs)
    W = w.values; yv = y.values; D = W.sum()
    mu = float((W * yv).sum() / D)
    zz = W * (yv - mu) / D
    key = z.stratum.astype(str) + '/' + z.psu.astype(str)
    tab = pd.Series(zz, index=key).groupby(level=0).sum()
    st = pd.Series([k.split('/')[0] for k in tab.index], index=tab.index)
    v = 0.0
    for h in st.unique():
        th = tab[st == h].values; nh = len(th)
        if nh > 1: v += (nh / (nh - 1)) * np.sum((th - th.mean()) ** 2)
    return mu, float(np.sqrt(v))
out = []
for _, row in est.iterrows():
    z, y, w = domain(d, row)
    mu, se = domain_mean_se(z, y, w) if len(z) else (np.nan, np.nan)
    out.append(dict(experiment=row.experiment, country=row.country, wave=str(row.wave), group=str(row.group),
                    scout_estimate=row.estimate, recomputed_mean=mu, mean_diff=row.estimate - mu,
                    scout_se=row.se, recomputed_se=se, se_ratio=(row.se / se if se and np.isfinite(se) else np.nan),
                    n=int(len(z))))
r = pd.DataFrame(out)
r.to_csv(f'{RUN}/../audit_scout_recompute.csv', index=False)
summ = dict(n=len(r), max_abs_mean_diff=float(np.nanmax(np.abs(r.mean_diff))),
            n_mean_diff_gt_1e_8=int((np.abs(r.mean_diff) > 1e-8).sum()),
            se_ratio_median=float(np.nanmedian(r.se_ratio)),
            se_ratio_p05=float(np.nanpercentile(r.se_ratio, 5)), se_ratio_p95=float(np.nanpercentile(r.se_ratio, 95)),
            n_se_under_10pct=int((r.se_ratio < 0.9).sum()), n_se_over_10pct=int((r.se_ratio > 1.1).sum()),
            worst_under=r.nsmallest(3, 'se_ratio')[['experiment','country','wave','group','se_ratio','n']].to_dict('records'))
json.dump(summ, open(f'{RUN}/../audit_scout_summary.json', 'w'), indent=1, default=str)
print(json.dumps(summ, indent=1, default=str))
