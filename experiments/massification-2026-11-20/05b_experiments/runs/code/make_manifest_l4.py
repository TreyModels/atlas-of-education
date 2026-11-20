"""Build loop4/SUMMARY_L4.csv and RUN_MANIFEST_L4.json."""
import csv, hashlib, json, os, platform, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); L4=os.path.abspath(os.path.join(HERE,'..'))
def sha(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()[:16]
def f(x):
    try:
        v=float(x); return f'{v:.6f}' if np.isfinite(v) else 'nan'
    except Exception: return str(x)
meta=json.load(open(os.path.join(L4,'runs','l4_meta.json')))
rows=[]
u1=meta['U1']
rows+=[dict(cell='U1',item='per-participant fee/income',value=f(u1['per_participant']),target='0.138',status='PASS' if u1['fee_ok'] else 'FAIL',source='runs/U1/findings.txt'),
       dict(cell='U1',item='per-student fee/income',value=f(u1['per_student']),target='0.108',status='PASS' if u1['fee_ok'] else 'FAIL',source='runs/U1/findings.txt'),
       dict(cell='U1',item='by-level participation ordering (E>M>H?)',value=str(u1['order_ok']),target='E 86/M 75.4/H 66.4',status='FAIL (ordering)',source='runs/U1/findings.txt'),
       dict(cell='U1',item='hours 7.3/wk',value='UNABLE',target='7.3',status='UNABLE',source='runs/U1/findings.txt')]
u1b=meta['U1b']
for s in ('lower','middle','senior'):
    rows.append(dict(cell='U1b',item=f'1998/99 {s} take-up %',value=f(u1b['model'][s]),target=f(u1b['obs'][s]),status=f"miss {u1b['model'][s]-u1b['obs'][s]:+.1f}pp",source='runs/U1b/findings.txt'))
rows.append(dict(cell='U1b',item='verdict',value=u1b['verdict'],target='predeclared 4-condition rule',status='FAIL',source='runs/U1b/findings.txt'))
u2=meta['U2']
rows+=[dict(cell='U2',item='recovery (candidate truths)',value=f(u2['recovery']),target='>=0.67',status='NEGATIVE',source='runs/U2/findings.txt'),
       dict(cell='U2',item='forced-ID (placebo)',value=f(u2['forced_placebo']),target='=0',status='NEGATIVE',source='runs/U2/findings.txt'),
       dict(cell='U2',item='forced-ID (no placebo)',value=f(u2['forced_noplacebo']),target='=0',status='NEGATIVE',source='runs/U2/findings.txt')]
for iso in ('PHL','KHM'):
    u=meta['U3'][iso]
    rows+=[dict(cell='U3',item=f'{iso} held-out MAE',value=f(u['holdout_mae']),target='<=5.0pp and < naive',status='PASS' if u['passed'] else 'FAIL',source='runs/U3/findings.txt'),
           dict(cell='U3',item=f'{iso} in-sample RMSE',value=f(u['fit_rmse']),target='-',status='caveat' if iso=='KHM' else '',source='runs/U3/findings.txt')]
hdr=['cell','item','value','target','status','source']
with open(os.path.join(L4,'SUMMARY_L4.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=hdr); w.writeheader()
    for r in rows: w.writerow(r)
outs=[]
for root,_,files in os.walk(os.path.join(L4,'runs')):
    for fn in sorted(files):
        fp=os.path.join(root,fn); outs.append(dict(path=os.path.relpath(fp,L4),sha16=sha(fp),bytes=os.path.getsize(fp)))
man=dict(loop='4',owner='experiment-runner-2',scope='05b_experiments/loop4 only',
         environment=dict(python=sys.version.split()[0],platform=platform.platform(),numpy=np.__version__),
         predeclaration='PRE_DECLARATIONS_L4.md',meta=meta,
         code_sha={p:sha(os.path.join(L4,p)) for p in ['code/l4.py','code/make_manifest_l4.py']},
         outputs=outs,
         verdicts=dict(U1=('price block USABLE for KOR; demand by-level UNABLE/failed; hours UNABLE'),
                       U1b='FAIL under predeclared rule -> incidence stays withdrawn for all countries',
                       U2='NEGATIVE: recovery 0.50 (<0.67), forced-ID 0.60 (!=0)',
                       U3='PHL FAIL (14.68pp held-out MAE); KHM mechanical pass only, no country claim',
                       U4='publishable = negative/identification map + KOR provider economics + data-first program'))
json.dump(man,open(os.path.join(L4,'RUN_MANIFEST_L4.json'),'w'),indent=1)
print(f'SUMMARY_L4.csv {len(rows)} rows; manifest {len(outs)} outputs')
