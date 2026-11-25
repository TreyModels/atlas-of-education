#!/usr/bin/env python3
"""Independent QA audit of the data team's normalized DHS layers (SYNTHETIC-FREE: real microdata,
aggregate/non-disclosive outputs only).  Recomputes the adapter's own evidence from the normalized
CSVs and checks experiment readiness; writes non-disclosive JSON/CSV under qa/logs/real/."""
import json, sys, os
import pandas as pd, numpy as np

DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/neon-boot/dhs8_local/normalized_all.csv')
MANIFEST = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/neon-boot/dhs8_local/manifest.json')
OUT = sys.argv[3] if len(sys.argv) > 3 else 'qa/logs/real'
os.makedirs(OUT, exist_ok=True)
COLS = ['country','wave','weight','stratum','psu','record_type','age','sex','urban','wealth','attendance',
        'school_years','children_ever_born','age_first_birth','currently_in_school','age_first_union','household_size']
df = pd.read_csv(DATA, usecols=COLS, dtype={'wave': str})
man = json.load(open(MANIFEST))
rep = {'data_file': DATA, 'manifest': MANIFEST, 'n_rows': int(len(df)), 'surveys': {}}
issues = []
def num(s): return pd.to_numeric(s, errors='coerce')

for (c, w, rt), g in df.groupby(['country','wave','record_type'], dropna=False):
    tag = f'{c}-{w}:{rt}'
    ev = {}
    ev['n_rows'] = int(len(g))
    ev['n_psu'] = int(g['psu'].nunique()); ev['n_strata'] = int(g['stratum'].nunique())
    tab = g.groupby(['stratum','psu']).size()
    ev['singleton_strata'] = int((tab.groupby('stratum').size() == 1).sum())
    ev['dup_psu_ids_within_stratum'] = int(g.groupby(['stratum','psu']).size().gt(0).groupby('stratum').sum().sub(g['stratum'].nunique()).sum())  # always 0 by construction; replaced below
    percr = g.groupby('psu')['stratum'].nunique()
    ev['psu_label_shared_across_strata'] = int((percr > 1).sum())
    ev['pos_psus'] = int(g['psu'][g['weight'] > 0].nunique())
    ev['weight_missing'] = int(g['weight'].isna().sum()); ev['weight_nonpositive'] = int((g['weight'] <= 0).sum())
    ev['weight_min'] = float(g['weight'].min()); ev['weight_sum'] = float(g['weight'].sum())
    ev['year_min'] = int(num(g['age']).min()); ev['age_max'] = int(num(g['age']).max())
    for col in COLS[6:]:
        ev[f'nonmissing_{col}'] = int(g[col].notna().sum())
    # special-code checks (README rule: 97/98 are never; 99 allowed only for first birth/union = known never)
    afb = num(g['age_first_birth']); afu = num(g['age_first_union'])
    ev['afb_99_known_never'] = int((afb == 99).sum()); ev['afb_97_98'] = int(afb.isin([97,98]).sum())
    ev['afb_95_96'] = int(afb.isin([95,96]).sum()); ev['afb_0'] = int((afb == 0).sum())
    ev['afu_99_known_never'] = int((afu == 99).sum()); ev['afu_97_98'] = int(afu.isin([97,98]).sum())
    ev['school_years_gt_25'] = int((num(g['school_years']) > 25).sum())
    ev['ceb_99'] = int((num(g['children_ever_born']) == 99).sum()); ev['ceb_gt_25'] = int((num(g['children_ever_born']) > 25).sum())
    ev['hh_lt1_or_gt60'] = int(((num(g['household_size']) < 1) | (num(g['household_size']) > 60)).sum())
    ev['wealth_values'] = sorted([int(v) for v in num(g['wealth']).dropna().unique()])
    ev['sex_values'] = sorted([int(v) for v in num(g['sex']).dropna().unique()]) if g['sex'].notna().any() else []
    ev['urban_values'] = sorted([int(v) for v in num(g['urban']).dropna().unique()]) if g['urban'].notna().any() else []
    # attendance coding sanity (independent of adapter's declared code): attendance prevalence by age band
    att = num(g['attendance'])
    ev['attendance_share_9_14'] = float(att[(num(g['age']) >= 9) & (num(g['age']) <= 14)].mean()) if ((num(g['age'])>=9)&(num(g['age'])<=14)&att.notna()).any() else None
    ev['attendance_share_25_49'] = float(att[(num(g['age']) >= 25) & (num(g['age']) <= 49)].mean()) if ((num(g['age'])>=25)&(num(g['age'])<=49)&att.notna()).any() else None
    # compare with manifest evidence
    mk = f'{tag.split(":")[0]}:{rt}' if False else tag
    rep['surveys'][tag] = ev
    m = man.get(tag) or man.get(f'{c}-{w}:{rt}')
    if m:
        me = m.get('evidence', {})
        for a, b in [('n_rows','n_rows'), ('n_psu','n_psu'), ('n_strata','n_strata'),
                     ('singleton_strata','singleton_strata'), ('weight_min','weight_min')]:
            if a in me and me[a] is not None and b in ev and abs(float(ev[b]) - float(me[a])) > 1e-6:
                issues.append(f'{tag}: manifest {a}={me[a]} but recomputed {ev[b]}')
        mc = m.get('cells', {})
        for col in COLS[6:]:
            if col in mc and abs(int(mc[col]) - ev[f'nonmissing_{col}']) > 0:
                issues.append(f'{tag}: manifest cells[{col}]={mc[col]} but recomputed {ev[f"nonmissing_{col}"]}')
    else:
        issues.append(f'{tag}: no manifest entry')
    # E1-E8 readiness domains (README definitions)
    A = num(g['age']); out = {}
    if rt == 'person':
        dom = g[(A >= 14) & (A <= 17)]
        out['E1'] = dict(n=int((dom['attendance'].notna() & dom['wealth'].notna()).sum()))
        out['E2'] = dict(n=int((dom['attendance'].notna() & dom['urban'].notna()).sum()))
        out['E3'] = dict(n=int((dom['attendance'].notna() & dom['sex'].notna()).sum()))
        e6 = g[(A >= 20) & (A <= 24) & (num(g['sex']) == 2)]
        out['E6_person_alt'] = dict(n=int(e6['attendance'].notna().sum()))
    else:
        w40 = g[(A >= 40) & (A <= 49)]
        w25 = g[(A >= 25) & (A <= 34)]
        w20 = g[(A >= 20) & (A <= 24)]
        out['E4'] = dict(n=int((w40['children_ever_born'].notna() & w40['school_years'].notna()).sum()))
        out['E5'] = dict(n=int((w25['age_first_birth'].notna() & w25['school_years'].notna()).sum()))
        out['E6'] = dict(n=int((w20['currently_in_school'].notna()).sum()))
        out['E7'] = dict(n=int((w25['age_first_union'].notna() & w25['school_years'].notna()).sum()))
        out['E8'] = dict(n=int((w40['household_size'].notna() & w40['school_years'].notna()).sum()))
    ev['experiments'] = out

# readiness matrix: which experiments are runnable per survey (domain n >= 50 and variable present)
ready = []
for tag, ev in rep['surveys'].items():
    for ex, d in ev['experiments'].items():
        ready.append(dict(survey=tag, experiment=ex, n_domain=d['n'], runnable=bool(d['n'] >= 50)))
ready = pd.DataFrame(ready)
rep['readiness'] = ready.to_dict(orient='records')
rep['issues'] = issues
json.dump(rep, open(os.path.join(OUT, 'real_data_audit.json'), 'w'), indent=1)
ready.to_csv(os.path.join(OUT, 'experiment_readiness.csv'), index=False)
print(json.dumps({'rows': rep['n_rows'], 'surveys': len(rep['surveys']), 'issues': issues[:20],
                  'n_issues': len(issues)}, indent=1))
print('\nreadiness (runnable cells):')
print(ready[ready.runnable].groupby('experiment').size().to_string())
print('\nnot runnable per experiment:')
print(ready[~ready.runnable].groupby('experiment').size().to_string())
