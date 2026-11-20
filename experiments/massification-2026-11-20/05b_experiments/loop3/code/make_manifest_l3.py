"""Build loop3/SUMMARY_L3.csv and RUN_MANIFEST_L3.json."""
import csv, hashlib, json, os, platform, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); L3 = os.path.abspath(os.path.join(HERE, '..'))
def sha(p):
    h = hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()[:16]
def rd(p): return list(csv.DictReader(open(p))) if os.path.exists(p) else []
def f(x):
    try:
        v=float(x); return f'{v:.6f}' if np.isfinite(v) else 'nan'
    except Exception: return str(x)
rows=[]
for r in rd(os.path.join(L3,'runs','s1_table.csv')):
    rows.append(dict(cell='S1', item=f"{r['source']}:{r['iso3']}:{r['stage']}",
                     estimand='model take-up % vs literature', value=f(r['model_pct']),
                     target=f(r['literature_pct']), status=r['assessment'],
                     note=r['note'], source='runs/s1_table.csv'))
for r in rd(os.path.join(L3,'runs','s2_search.csv')):
    if r['arm'] in ('joint_search',):
        rows.append(dict(cell='S2', item=f"{r['country']}:{r['arm']}", estimand='RMSE vs stage-matched targets (pp)',
                         value=f(r['rmse_pp']), target='', status=('<=5 reproduces' if float(r['rmse_pp'] or 1e9)<=5 else ('<=10 partial' if float(r['rmse_pp'] or 1e9)<=10 else 'none works')),
                         note=r['model'], source='runs/s2_search.csv'))
for r in rd(os.path.join(L3,'runs','s3_grid.csv')):
    rows.append(dict(cell='S3', item=f"{r['country']}:F_cm={r['F_cm_mult']}:F_tt={r['F_tt_mult']}:cap_cm={r['cap_cm_mult']}:cap_tt={r['cap_tt_mult']}:tcap={r['teacher_cap_mult']}",
                     estimand='price; provider counts; teacher share', value=f(r['price']), target='',
                     status=('floor' if r['price_floor_hit']=='True' else 'finite'),
                     note=f"n_cm={r['n_cm']}; n_tt={r['n_tt']}; tshare={r['teacher_share']}; price/income={r['price_income']}",
                     source='runs/s3_grid.csv'))
hdr=['cell','item','estimand','value','target','status','note','source']
with open(os.path.join(L3,'SUMMARY_L3.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=hdr); w.writeheader()
    for r in rows: w.writerow({k:r.get(k,'') for k in hdr})
meta=json.load(open(os.path.join(L3,'runs','run_meta.json')))
outs=[]
for root,_,files in os.walk(os.path.join(L3,'runs')):
    for fn in sorted(files):
        fp=os.path.join(root,fn); outs.append(dict(path=os.path.relpath(fp,L3), sha16=sha(fp), bytes=os.path.getsize(fp)))
man=dict(loop='3', owner='experiment-runner-2', scope='05b_experiments/loop3 only',
         module='code/shadow3.py (NEW; not massabm/floorworld/triad/paper reproduction)',
         environment=dict(python=sys.version.split()[0], platform=platform.platform(), numpy=np.__version__),
         predeclaration='PRE_DECLARATIONS_L3.md', meta=meta,
         intake_corrections=meta.get('intake_corrections'),
         code_sha={p: sha(os.path.join(L3,p)) for p in ['code/shadow3.py','code/make_manifest_l3.py']},
         outputs=outs, pending=['L2-4 recovery/forced-ID','L2-5 1980-2010 fit / 2011-2024 holdout'])
json.dump(man, open(os.path.join(L3,'RUN_MANIFEST_L3.json'),'w'), indent=1)
print(f'SUMMARY_L3.csv {len(rows)} rows; manifest {len(outs)} outputs')
