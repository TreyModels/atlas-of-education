import json,numpy as np
from scipy.stats import spearmanr
R=[json.loads(l) for l in open('/home/claude/sig/v31_results.jsonl')]
g=lambda s,k: np.array([r[s][k] for r in R],float)
q=lambda x:[round(float(v),3) for v in np.nanpercentile(x,[5,25,50,75,95])]
def verdict(name,frac,need): print(f'{name:58s}{frac:6.3f}  need {need:.2f}  ->','SUPPORTED' if frac>=need else 'NOT SUPPORTED')
cur,noq,eqm=g('CURRENT','HUKOU_ratio'),g('NO_QUOTA','HUKOU_ratio'),g('EQUAL_MIGRANT','HUKOU_ratio')
verdict('H1a HUKOU_ratio(no quota) < current',np.mean(noq<cur),.95)
verdict('H1b quota share >= minban share of hukou gap',np.mean((cur-noq)>=(noq-eqm)),.80)
eo,eoz,eor=g('CURRENT','EO_local'),g('NO_ZHIBIAO','EO_local'),g('NO_REBAND','EO_local')
verdict('H2 zhibiao narrows local wealth gap',np.mean(eo<eoz),.90)
verdict('H3 re-banding narrows local wealth gap',np.mean(eo<eor),.90)
va=np.array([r['params']['SCHOOL_VA'] for r in R]); e35=g('CURRENT','E35')
q1=np.where(va<.02,e35>.1,e35>=5*np.maximum(va,1e-9)); verdict('Q1 E35 school FE >= 5x true',np.mean(q1),.95)
verdict('Q2 E159 between share >= 10x VA share',np.mean(g('CURRENT','E159')>=10*g('CURRENT','VA_share')),.95)
e152=g('CURRENT','E152'); verdict('Q3 RD below true school VA gap',np.nanmean(e152<va),.90)
e36c,e36n=g('CURRENT','E36'),g('NO_REBAND','E36'); verdict('Q4 peer coef >0 with reband and lower without',np.mean((e36c>0)&(e36n<e36c)),.80)
print('\nDescriptive (5/25/50/75/95 pct)')
for s,k in [('CURRENT','EO_local'),('NO_ZHIBIAO','EO_local'),('NO_REBAND','EO_local'),('CURRENT','HUKOU_ratio'),('NO_QUOTA','HUKOU_ratio'),('EQUAL_MIGRANT','HUKOU_ratio'),
            ('CURRENT','NH_hiTal_public'),('CURRENT','NH_hiTal_private'),('CURRENT','NH_hiTal_exit'),('CURRENT','SUB_conc'),('CURRENT','SUB_gap'),('CURRENT','E35'),('CURRENT','E159'),('CURRENT','E152'),('CURRENT','E36'),('NO_REBAND','E36')]:
    print(f'  {s:14s}{k:16s}',q(g(s,k)))
P={k:np.array([r['params'][k] for r in R]) for k in R[0]['params']}
for tgt,lab in [(cur,'HUKOU_ratio'),(eo,'EO_local'),(g('CURRENT','NH_hiTal_exit'),'NH exit share'),(eoz-eo,'zhibiao benefit')]:
    top=sorted(((k,spearmanr(v,tgt)[0]) for k,v in P.items()),key=lambda t:-abs(t[1]))[:4]
    print(f'drivers of {lab}:',', '.join(f'{k} {r:+.2f}' for k,r in top))
print('\nv3.1 extra (5/25/50/75/95)')
for s,k in [('CURRENT','EO_equal_zk'),('CURRENT','EO_uncond'),('CURRENT','NH_public_of_cohort'),('CURRENT','NH_private_of_cohort'),('CURRENT','NH_exit_of_cohort'),('CURRENT','NH_vocational_of_cohort')]:
    print(f'  {s:14s}{k:24s}',q(g(s,k)))
d=eoz-eo; print('  zhibiao effect on EO_local (no-zhibiao minus current):',q(d),' helps in',round(np.mean(d>0),3))
d=eor-eo; print('  re-banding effect on EO_local:',q(d),' helps in',round(np.mean(d>0),3))
