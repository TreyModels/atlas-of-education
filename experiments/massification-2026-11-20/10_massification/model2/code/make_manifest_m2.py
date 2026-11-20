import csv, hashlib, json, os, platform, sys
import pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__)); M2=os.path.abspath(os.path.join(HERE,'..'))
def sha(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()[:16]
rows=[]
s=pd.read_csv(os.path.join(M2,'runs','scaling_estimates.csv'))
cl=pd.read_csv(os.path.join(M2,'runs','scaling_classification.csv'))
keep=cl[cl['classification']!='unidentified'][['sample','pair','classification']]
sel=s[(s['status'].fillna('')=='')&s['exponent'].notna()&(s['estimator']=='between')]
for _,r in sel.iterrows():
    rows.append(dict(group='scaling', key=f"{r['sample']}:{r['pair']}", exponent=round(float(r['exponent']),4),
                     se=round(float(r['se']),4), n=int(r['n']), estimator=r['estimator']))
try:
    rec=pd.read_csv(os.path.join(M2,'runs','recovery.csv'))
    for t in ['D','S','C']:
        rows.append(dict(group='recovery', key=f'truth_{t}', exponent='', se='', n=int((rec['truth']==t).sum()),
                         estimator=f"recovered_share={(rec[rec['truth']==t]['best']==t).mean():.2f}"))
    out=rec[rec['truth']=='OUT']
    rows.append(dict(group='recovery', key='forced_id_OUTSIDE', exponent='', se='', n=len(out),
                     estimator=f"forced_share={(out['best'].isin(['D','S','C'])).mean():.2f}"))
except Exception:
    pass
with open(os.path.join(M2,'SUMMARY_M2.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['group','key','exponent','se','n','estimator']); w.writeheader()
    for r in rows: w.writerow(r)
outs=[]
for root,_,files in os.walk(os.path.join(M2,'runs')):
    for fn in sorted(files):
        fp=os.path.join(root,fn); outs.append(dict(path=os.path.relpath(fp,M2),sha256_16=sha(fp),bytes=os.path.getsize(fp)))
man=dict(phase='massification',owner='experiment-runner-2',scope='10_massification/model2 only',
         predeclaration='PRE_DECLARATIONS_M2.md',label='observed estimation (Parts 1-3) + SIMULATED recovery (Part 4)',
         environment=dict(python=sys.version.split()[0],platform=platform.platform()),
         data_fallback='10_massification/data|relations empty at run; 04_data + 09_relations/data used; no imputed panel',
         commit='no git push (Lead handles); artifact hashes below',
         code_sha={p:sha(os.path.join(M2,p)) for p in ['code/m2.py','code/make_manifest_m2.py']},
         outputs=outs,
         key_results=dict(scaling_laws=['WDI30 GER secondary ~ income +0.286 (0.045)',
                                        'WDI30 GER tertiary ~ income +0.776 (0.086)',
                                        'WDI30 lower-sec completion (logit) ~ income, ratio 1.76'],
                          regularities=['upper-sec completion', 'agriculture share', 'spending->secondary',
                                        'urbanisation sample-flip', 'all UIS6 pairs'],
                          unidentified=['GER primary vs income (saturation)', 'returns vs schooling (UNABLE)'],
                          logistic='countries do not share a common slope; parameter uncertainty wide',
                          lead_lag='NOT IDENTIFIABLE (short panels)',
                          rivals='supply-led wins 15/23, demand-led 8/23; push coef +0.026',
                          recovery=dict(demand=1.0,supply=1.0,complementary=0.0,forced_id=1.0,equivalence=0.07),
                          push_pull='NOT IDENTIFIABLE'))
json.dump(man,open(os.path.join(M2,'RUN_MANIFEST_M2.json'),'w'),indent=1)
print(f'SUMMARY_M2.csv {len(rows)} rows; manifest {len(outs)} outputs')
