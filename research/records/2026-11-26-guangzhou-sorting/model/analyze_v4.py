import json,numpy as np
from scipy.stats import spearmanr
R=[json.loads(l) for l in open('/home/claude/sig/v4_results.jsonl')]
g=lambda s,k: np.array([r[s][k] for r in R],float)
P={k:np.array([r['params'][k] for r in R]) for k in R[0]['params']}
q=lambda x:[round(float(v),3) for v in np.nanpercentile(x,[5,25,50,75,95])]
def v(n,f,need): print(f'{n:62s}{f:6.3f} need {need:.2f} ->','SUPPORTED' if f>=need else 'NOT SUPPORTED')
cur,old,ban,tc=[g(s,'EO_local') for s in ('CURRENT','OLD','BAN_PERFECT','TIME_CONTROL')]
v('V1 current fairer than pre-2021 at equal talent',np.mean(cur<old),.90)
v('V2 perfect time control lowers the gap',np.mean(tc<cur),.80)
v('V3 perfect pre-gate ban lowers the gap',np.mean(ban<cur),.80)
print('\nleaks: pre-gate (cur-ban)',q(cur-ban),' post-gate (cur-tc)',q(cur-tc),' pre-gate larger in',round(np.mean((cur-ban)>(cur-tc)),3))
print('old minus current',q(old-cur))
for s in ('CURRENT','OLD','BAN_PERFECT','TIME_CONTROL'):
    print(f'{s:13s} equal talent {q(g(s,"EO_local"))}  equal zhongkao {q(g(s,"EO_equal_zk"))}  unconditional {q(g(s,"EO_uncond"))}')
print('\nEO_local CURRENT by head-start fade:')
dc=P['DECAY']
for lo in np.arange(0,.9,.15):
    mk=(dc>=lo)&(dc<lo+.15); print(f'  fade {lo:.2f}-{lo+.15:.2f}: median {np.median(cur[mk]):.2f}  [{np.percentile(cur[mk],10):.2f}, {np.percentile(cur[mk],90):.2f}]  n={mk.sum()}')
print('\ndrivers of CURRENT EO_local:',', '.join(f'{k} {r:+.2f}' for k,r in sorted(((k,spearmanr(x,cur)[0]) for k,x in P.items()),key=lambda t:-abs(t[1]))[:6]))
ft=g('CURRENT','EO_uncond')-g('TIME_CONTROL','EO_uncond')
print('full-time effect: EO_local change when FT_EFF>0.1',q((cur-tc)[P['FT_EFF']>.1]),' when FT_EFF<0',q((cur-tc)[P['FT_EFF']<0]))
print('pre-gate take-up Q1/Q5 current',q(g('CURRENT','pre_Q1')),q(g('CURRENT','pre_Q5')))
print('hukou ratio',q(g('CURRENT','HUKOU_ratio')),' NH public/private/exit/voc of cohort',[round(float(np.median(g('CURRENT',k))),3) for k in ('NH_public_of_cohort','NH_private_of_cohort','NH_exit_of_cohort','NH_vocational_of_cohort')])
