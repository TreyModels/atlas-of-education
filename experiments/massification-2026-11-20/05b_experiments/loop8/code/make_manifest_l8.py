import csv, hashlib, json, os, platform, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); L8=os.path.abspath(os.path.join(HERE,'..'))
def sha(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()[:16]
meta=json.load(open(os.path.join(L8,'runs','synth_wired_meta.json')))
rows=[]
for t,b in meta['before'].items():
    a=meta['after'].get(t,0)
    rows.append(dict(target=t,loop6_inside=b,loop8_inside=a,delta=a-b,
                     shrink='YES' if (b==0 and a>=1) else 'no'))
for k,v in meta['two_margin'].items():
    rows.append(dict(target=f'TWO_MARGIN:{k}',loop6_inside='',loop8_inside=v,delta='',shrink=''))
with open(os.path.join(L8,'SUMMARY_L8.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['target','loop6_inside','loop8_inside','delta','shrink']); w.writeheader()
    for r in rows: w.writerow(r)
outs=[]
for root,_,files in os.walk(os.path.join(L8,'runs')):
    for fn in sorted(files):
        fp=os.path.join(root,fn); outs.append(dict(path=os.path.relpath(fp,L8),sha16=sha(fp),bytes=os.path.getsize(fp)))
man=dict(loop='8',owner='experiment-runner-2',scope='05b_experiments/loop8 only',label='SYNTHETIC/POSSIBILITY ONLY; programme CLOSED',
         environment=dict(python=sys.version.split()[0],platform=platform.platform(),numpy=np.__version__),
         predeclaration='PRE_DECLARATIONS_L8.md',meta=meta,
         decision='shrink = target 0/256 in loop6 -> >=1/256 in loop8',
         code_sha={p:sha(os.path.join(L8,p)) for p in ['code/synth_wired.py','code/make_manifest_l8.py']},
         outputs=outs)
json.dump(man,open(os.path.join(L8,'RUN_MANIFEST_L8.json'),'w'),indent=1)
print(f'SUMMARY_L8.csv {len(rows)} rows; manifest {len(outs)} outputs')
