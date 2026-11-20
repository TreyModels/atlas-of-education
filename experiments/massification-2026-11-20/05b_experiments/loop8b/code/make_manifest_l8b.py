import csv, hashlib, json, os, platform, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); L8B=os.path.abspath(os.path.join(HERE,'..'))
def sha(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()[:16]
rows=[]
fa=os.path.join(L8B,'runs','frontier_before_after.csv')
keep={'KOR_gradient','HKG_gradient','KOR_fee','KOR_income'}
if os.path.exists(fa):
    for r in csv.DictReader(open(fa)):
        if r['target'] in keep:
            rows.append(dict(target=r['target'],loop6_inside=r['loop6_inside'],loop8_inside=r['loop8_inside'],
                             loop8b_inside=r['loop8_inside'],delta_vs_loop6=r['delta']))
tm=os.path.join(L8B,'runs','kor_two_margin.csv')
joint=None
if os.path.exists(tm):
    for r in csv.DictReader(open(tm)):
        if r['metric']=='joint_draws': joint=r['value']
rows.append(dict(target='KOR_two_margin_joint',loop6_inside='0',loop8_inside='0',loop8b_inside=joint,delta_vs_loop6='0'))
with open(os.path.join(L8B,'SUMMARY_L8B.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['target','loop6_inside','loop8_inside','loop8b_inside','delta_vs_loop6']); w.writeheader()
    for r in rows: w.writerow(r)
outs=[]
for root,_,files in os.walk(os.path.join(L8B,'runs')):
    for fn in sorted(files):
        fp=os.path.join(root,fn); outs.append(dict(path=os.path.relpath(fp,L8B),sha16=sha(fp),bytes=os.path.getsize(fp)))
man=dict(loop='8b',owner='experiment-runner-2',scope='05b_experiments/loop8b only',label='SYNTHETIC/POSSIBILITY ONLY; programme CLOSED',
         eci_metric='eci_hs92 (eci_sitc robustness only; no ranks/growth_proj/HS12)',
         eci_values=dict(KOR=1.754,HKG=1.218,PHL=0.718,KHM=-0.281,ref=0.852),
         environment=dict(python=sys.version.split()[0],platform=platform.platform(),numpy=np.__version__),
         predeclaration='PRE_DECLARATIONS_L8B.md', deviation='L8B-1 run launched before predeclare file committed (contents fixed beforehand)',
         unscoreable=['R44','R45','R46','R47','R48','R49','CX-01','CX-02','CX-03','CX-04'],
         code_sha={p:sha(os.path.join(L8B,p)) for p in ['code/synth_wired_eci.py','code/make_manifest_l8b.py']},
         outputs=outs)
json.dump(man,open(os.path.join(L8B,'RUN_MANIFEST_L8B.json'),'w'),indent=1)
print(f'SUMMARY_L8B.csv {len(rows)} rows; manifest {len(outs)} outputs')
