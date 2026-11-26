import json,numpy as np
from scipy.stats import spearmanr
R=[json.loads(l) for l in open('/home/claude/sig/v6_results.jsonl')]
g=lambda s,k: np.array([r[s][k] for r in R],float); P=lambda k: np.array([r['params'][k] for r in R])
q=lambda x:[round(float(v),3) for v in np.nanpercentile(x,[5,25,50,75,95])]
def v(n,f,need): print(f'{n:66s}{f:6.3f} need {need:.2f} ->','SUPPORTED' if f>=need else 'NOT SUPPORTED')
v('M1 same zhongkao score, richer/poorer ratio <= 1.10 (CURRENT)',np.mean(g('CURRENT','EO_equal_zk')<=1.10),.80)
v('M2a equal-talent gap lower than stylised Hong Kong',np.mean(g('CURRENT','EO_local')<g('HK_STYLE','EO_local')),.90)
v('M2b unconditional gap lower than stylised Hong Kong',np.mean(g('CURRENT','EO_uncond')<g('HK_STYLE','EO_uncond')),.90)
v('M3 rich routes < 5 points of admission per 100,000 yuan',np.mean(g('CURRENT','rich_pp_per_100k')<5),.80)
print()
for s in ('CURRENT','OLD','HK_STYLE','BAN_PERFECT','TIME_CONTROL'):
    print(f'{s:13s} same-score {q(g(s,"EO_equal_zk"))} equal-talent {q(g(s,"EO_local"))} unconditional {q(g(s,"EO_uncond"))}')
print('\nCURRENT minus HK_STYLE equal talent',q(g('CURRENT','EO_local')-g('HK_STYLE','EO_local')),' unconditional',q(g('CURRENT','EO_uncond')-g('HK_STYLE','EO_uncond')))
print('CURRENT minus OLD equal talent',q(g('CURRENT','EO_local')-g('OLD','EO_local')),' share current lower',round(np.mean(g('CURRENT','EO_local')<g('OLD','EO_local')),3))
print('rich pp per 100k',q(g('CURRENT','rich_pp_per_100k')))
for s in ('OLD','CURRENT','BAN_PERFECT'):
    print(f'{s:12s} pre-gate take-up {q(g(s,"pre_takeup"))} mean household tutoring spend {q(g(s,"spend_mean"))} rich {q(g(s,"spend_rich"))} poor {q(g(s,"spend_poor"))}')
d=g('CURRENT','EO_local'); print('\nCURRENT equal-talent by fade:')
for lo in np.arange(0,.9,.15):
    mk=(P('DECAY')>=lo)&(P('DECAY')<lo+.15); print(f'  {lo:.2f}-{lo+.15:.2f} median {np.median(d[mk]):.2f}')
print('drivers CURRENT EO_local:',', '.join(f'{k} {r:+.2f}' for k,r in sorted(((k,spearmanr(P(k),d)[0]) for k in R[0]['params']),key=lambda t:-abs(t[1]))[:6]))
dz=g('CURRENT','EO_equal_zk'); print('drivers same-score ratio:',', '.join(f'{k} {r:+.2f}' for k,r in sorted(((k,spearmanr(P(k),dz)[0]) for k in R[0]['params']),key=lambda t:-abs(t[1]))[:5]))
print('hukou ratio',q(g('CURRENT','HUKOU_ratio')),' NH cohort public/private/exit/voc',[round(float(np.nanmedian(g('CURRENT',k))),3) for k in ('NH_public_of_cohort','NH_private_of_cohort','NH_exit_of_cohort','NH_vocational_of_cohort')])
