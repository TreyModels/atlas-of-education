#!/usr/bin/env python3
"""Per-FILE singleton-PSU audit (the merged normalized_all.csv does not preserve file-level
PSU/stratum codes).  Writes qa/singleton_ledger.csv + qa/logs/real/singleton_summary.json."""
import glob, json, os, sys
import pandas as pd, numpy as np
root = os.path.expanduser('~/neon-boot/dhs-normalized')
out_ledger = sys.argv[1] if len(sys.argv) > 1 else 'qa/singleton_ledger.csv'
out_dir = os.path.dirname(out_ledger) or 'qa/logs/real'
os.makedirs(out_dir, exist_ok=True)
files = sorted(glob.glob(os.path.join(root, '*', '*.csv')))
rows, files_info = [], []
for f in files:
    d = pd.read_csv(f, usecols=lambda c: c in ['country','wave','record_type','stratum','psu','weight','age','attendance'], dtype={'wave':str})
    rt = str(d['record_type'].iloc[0]) if 'record_type' in d and len(d) else ('woman' if 'woman' in f else 'person')
    cty = str(d['country'].iloc[0]) if 'country' in d and len(d) else os.path.basename(f).split('_')[1]
    wv = str(d['wave'].iloc[0]) if 'wave' in d and len(d) else os.path.basename(f).split('_')[2]
    d['stratum'] = d['stratum'].astype(str); d['psu'] = d['psu'].astype(str)
    tab = d.groupby(['stratum','psu']).size()
    per_str = tab.groupby('stratum').size()
    sing = per_str[per_str == 1]
    for st in sing.index:
        sub = d[d.stratum == st]
        rows.append(dict(file=os.path.relpath(f, root), country=cty, wave=wv, record_type=rt,
                         stratum=st, n_psu=1, n_rows=int(len(sub))))
    files_info.append(dict(file=os.path.relpath(f, root), country=cty, wave=wv, record_type=rt,
                           n_rows=int(len(d)), n_strata=int(d.stratum.nunique()), n_psu=int(d.psu.nunique()),
                           n_singleton_strata=int(len(sing)),
                           attendance_nonmissing=int(d['attendance'].notna().sum()) if 'attendance' in d else None))
led = pd.DataFrame(rows)
if len(led):
    led = led.sort_values(['country','wave','record_type','stratum'])
led.to_csv(out_ledger, index=False)
summary = dict(n_files=len(files), n_files_with_singletons=sum(1 for x in files_info if x['n_singleton_strata'] > 0),
               n_singleton_strata_total=int(len(led)),
               by_file={x['file']: x['n_singleton_strata'] for x in files_info if x['n_singleton_strata'] > 0},
               files=files_info)
json.dump(summary, open(os.path.join(out_dir, 'singleton_summary.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'files'}, indent=1))
