#!/usr/bin/env python3
"""Final verified E1-E8 availability matrix (country x wave x experiment) from the adapter/aggregate outputs."""
import json, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_out')
EXP = ['E1','E2','E3','E4','E5','E6','E7','E8']
cov = pd.read_csv(os.path.join(OUT, 'coverage_missingness.csv'))
agg = pd.read_csv(os.path.join(OUT, 'aggregate_layer.csv'))
cov['wave'] = cov['wave'].astype(str); agg['wave'] = agg['wave'].astype(str)
rows = []
for (c, w), g in cov.groupby(['country', 'wave']):
    rec = dict(country=c, wave=w)
    for e in EXP:
        ge = g[g.experiment == e]
        if len(ge) == 0:
            rec[e] = 'NO_RECODE'; continue
        st = ge.status.iloc[0]
        if st == 'OK':
            n = int(ge.n_complete.iloc[0])
            a = agg[(agg.experiment == e) & (agg.country == c) & (agg.wave == w)]
            groups = sorted(a['group'].dropna().astype(str).unique())
            rec[e] = f'FEASIBLE n={n} groups={len(groups)}'
        elif st == 'NO_ROWS':
            rec[e] = 'BLOCKED: no rows for record type'
        elif st == 'BLOCKED_OUTCOME_VARIABLE_MISSING':
            rec[e] = 'BLOCKED: outcome variable absent/all-missing in recode'
        elif st == 'BLOCKED_GROUP_VARIABLE_MISSING':
            rec[e] = 'BLOCKED: grouping variable (wealth/education) absent/all-missing'
        else:
            rec[e] = st
    rows.append(rec)
out = pd.DataFrame(rows).sort_values(['country', 'wave'])
out.to_csv(os.path.join(OUT, 'availability_E1_E8.csv'), index=False)
print(f"wrote availability_E1_E8.csv ({len(out)} country-wave rows)")
