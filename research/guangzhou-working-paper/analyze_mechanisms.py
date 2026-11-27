"""Summaries of paired mechanism, enforcement and repeated-cohort experiments."""
import csv
import json
from pathlib import Path
import numpy as np
from summarize import distribution, improvement

ROOT = Path(__file__).resolve().parent
rows=[json.loads(line) for line in (ROOT/'mechanisms.jsonl').read_text().splitlines()]
assert len(rows)==150
summary={}
def values(scenario, key):
    return np.array([r[scenario][key] for r in rows])
for scenario in ['current','no_post','no_home','no_zone','no_pre','no_head','no_reband','no_ban','before']:
    summary[scenario]={key:distribution(values(scenario,key)) for key in ['T','S','U','spend','learn','learn_all']}
    for k in [5,10,20]:
        for measure in ['ratio','support']:
            summary[scenario]['joint'+str(k)+'_'+measure]=distribution(np.array([r[scenario]['joint'+str(k)][measure] for r in rows]))
    for key in ['T','S','Sstar']:
        summary[scenario]['ordinary_'+key]=distribution(np.array([r[scenario]['ordinary'][key] for r in rows]))
    if scenario not in ['current','before','no_reband','no_ban']:
        summary[scenario]['delta_T']=distribution(values(scenario,'T')-values('current','T'))
        summary[scenario]['excess_T_removed']=distribution((values('current','T')-values(scenario,'T'))/(values('current','T')-1))
        summary[scenario]['delta_learn']=distribution(values(scenario,'learn')-values('current','learn'))
current_joint=np.array([r['current']['joint5']['ratio'] for r in rows])
off_joint=np.array([r['no_post']['joint5']['ratio'] for r in rows])
summary['post_joint_excess_removed']=distribution((current_joint-off_joint)/(current_joint-1))
summary['factorial']={}
for key in ['T','spend']:
    c=values('current',key);b=values('before',key);nb=values('no_ban',key);nr=values('no_reband',key)
    summary['factorial'][key]=dict(ban=distribution(.5*((nr-b)+(c-nb))),reband=distribution(.5*((nb-b)+(c-nr))))
enforcement=list(csv.DictReader((ROOT/'enforcement.csv').open()))
assert len(enforcement)==768
summary['enforcement']=[]
for gradient in [0,.5,1]:
    a=np.array([float(r['delta_T_ban']) for r in enforcement if float(r['BAN_GRAD'])==gradient])
    summary['enforcement'].append(dict(gradient=gradient,**distribution(a),**improvement(a)))
repeats=list(csv.DictReader((ROOT/'repeats.csv').open()))
assert len(repeats)==1024 and len({(r['setting'],r['replicate']) for r in repeats})==1024
summary['repeats']={}
for key in ['delta_T','delta_T_ban']:
    a=np.array([float(r[key]) for r in repeats]).reshape(128,8)
    within=a.var(axis=1,ddof=1).mean()
    between=max(0,a.mean(1).var(ddof=1)-within/8)
    summary['repeats'][key]=dict(within_sd=float(np.sqrt(within)),between_sd=float(np.sqrt(between)),
                                sign_changes=int(((a.min(1)<0)&(a.max(1)>0)).sum()),mean_lower=int((a.mean(1)<0).sum()))
(ROOT/'mechanism_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'post_joint_excess_removed':summary['post_joint_excess_removed'],'enforcement':summary['enforcement'],'repeats':summary['repeats']},indent=2))
