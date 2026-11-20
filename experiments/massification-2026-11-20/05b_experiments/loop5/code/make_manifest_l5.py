import csv, hashlib, json, os, platform, sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); L5=os.path.abspath(os.path.join(HERE,'..'))
def sha(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()[:16]
meta=json.load(open(os.path.join(L5,'runs','l5_meta.json')))
rows=[]
for r in csv.DictReader(open(os.path.join(L5,'runs','E1','e1_arms.csv'))):
    rows.append(dict(cell='E1',item=f"{r['country']}:{r['arm']}",stage1=r['stage1'],stage2=r['stage2'],stage3=r['stage3'],
                     target=f"{r['target1']}/{r['target2']}/{r['target3']}",policy=r['policy_arm']))
e1b=meta['E1b']
for s,v in e1b['rates'].items():
    rows.append(dict(cell='E1b',item=f'KOR {s}',stage1=f'{v:.1f}',stage2=f'miss {e1b["misses"][s]:+.1f}',stage3='',target='',
                     policy='fee-fit'))
rows.append(dict(cell='E1b',item='verdict',stage1=str(e1b['pass_']),stage2=f'commercial {e1b["commercial_share"]:.3f}',
                 stage3=f'per-participant {e1b["per_participant"]:.3f}',target='',policy=''))
e4=meta['E4']
rows.append(dict(cell='E4',item='income spend ratio top/bottom',stage1=f'{e4["ratio"]:.2f}',stage2='obs 3.67',
                 stage3=f'mono {e4["monotone"]}',target='[1.84,5.51]',policy=str(e4['pass_'])))
with open(os.path.join(L5,'SUMMARY_L5.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['cell','item','stage1','stage2','stage3','target','policy']); w.writeheader()
    for r in rows: w.writerow(r)
outs=[]
for root,_,files in os.walk(os.path.join(L5,'runs')):
    for fn in sorted(files):
        fp=os.path.join(root,fn); outs.append(dict(path=os.path.relpath(fp,L5),sha16=sha(fp),bytes=os.path.getsize(fp)))
man=dict(loop='5',owner='experiment-runner-2',scope='05b_experiments/loop5 only',
         environment=dict(python=sys.version.split()[0],platform=platform.platform(),numpy=np.__version__),
         predeclaration='PRE_DECLARATIONS_L5.md',meta=meta,
         relations='PENDING (09_relations slot tables not consulted)',
         code_sha={p:sha(os.path.join(L5,p)) for p in ['code/e1.py','code/make_manifest_l5.py']},
         outputs=outs,
         verdicts=dict(E1='FAIL (all six rates outside +/-5pp; gate-position story dropped)',
                       E1b='FAIL (no one-country claim; stop-rule permanent)',
                       E4='PASS demand-consistent (ratio 2.14 vs observed 3.67)'))
json.dump(man,open(os.path.join(L5,'RUN_MANIFEST_L5.json'),'w'),indent=1)
print(f'SUMMARY_L5.csv {len(rows)} rows; manifest {len(outs)} outputs')
