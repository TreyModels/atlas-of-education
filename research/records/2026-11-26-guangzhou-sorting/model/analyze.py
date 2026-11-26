import json,numpy as np
from scipy.stats import spearmanr
R=[json.loads(l) for l in open('sweep_results.jsonl')]
g=lambda s,k: np.array([r[s][k] for r in R])
cur,nor,eqz,old=[g(s,'EO_uni') for s in ('CURRENT','NO_REBAND','EQUAL_ZONES','COHORT_2015')]
out={}
c1=np.mean((g('CURRENT','EO_track')>=.95)&(g('CURRENT','EO_track')<=1.05)); out['C1']=c1
c2=np.mean(cur<nor); out['C2']=c2
lift=g('CURRENT','weakzone_hiTal_topband_s2')-g('NO_REBAND','weakzone_hiTal_topband_s2'); c3=np.mean(lift>=.05); out['C3']=c3
c4=np.mean(cur<old); out['C4']=c4
ok=cur-1>=.02; share=(cur-eqz)/(cur-1); c5=np.mean(share[ok]>=.5); out['C5']=c5; out['C5_excluded']=int((~ok).sum())
def q(x): return [round(float(v),3) for v in np.percentile(x,[5,25,50,75,95])]
print('C1 track gate level      ',round(c1,3),'needs >=0.95 ->','SUPPORTED' if c1>=.95 else 'NOT SUPPORTED')
print('C2 reband narrows gap    ',round(c2,3),'needs >=0.95 ->','SUPPORTED' if c2>=.95 else 'NOT SUPPORTED')
print('C3 reband lifts climbers ',round(c3,3),'needs >=0.95 ->','SUPPORTED' if c3>=.95 else 'NOT SUPPORTED', ' lift pct', q(lift))
print('C4 current < 2015        ',round(c4,3),'needs >=0.95 ->','SUPPORTED' if c4>=.95 else 'NOT SUPPORTED')
print('C5 zone teachers >=half  ',round(c5,3),'needs >=0.80 ->','SUPPORTED' if c5>=.80 else 'NOT SUPPORTED',' excluded',int((~ok).sum()),' share pct',q(share[ok]))
print('\nEO_uni percentiles 5/25/50/75/95')
for n,x in [('CURRENT',cur),('NO_REBAND',nor),('EQUAL_ZONES',eqz),('COHORT_2015',old)]: print(f'  {n:12s}',q(x))
print('  conc index CURRENT',q(g('CURRENT','conc_uni')),' 2015',q(g('COHORT_2015','conc_uni')))
print('  share of draws CURRENT EO_uni < 1.2:',round(np.mean(cur<1.2),3),' <1.5:',round(np.mean(cur<1.5),3))
print('\nwhat drives CURRENT EO_uni (Spearman):')
P={k:np.array([r['params'][k] for r in R]) for k in R[0]['params']}
for k,rho in sorted(((k,spearmanr(v,cur)[0]) for k,v in P.items() if k not in('PRE_TUT','POST_TUT')),key=lambda t:-abs(t[1])): print(f'  {k:11s}{rho:+.2f}')
gap=old-cur
print('\n2015 minus current: drivers'); 
for k,rho in sorted(((k,spearmanr(v,gap)[0]) for k,v in P.items()),key=lambda t:-abs(t[1]))[:4]: print(f'  {k:11s}{rho:+.2f}')
print('  gap pct',q(gap))
json.dump({k:float(v) for k,v in out.items()},open('analysis.json','w'),indent=1)
