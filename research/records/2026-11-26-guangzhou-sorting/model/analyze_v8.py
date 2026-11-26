import json,itertools,math,numpy as np
R=[json.loads(l) for l in open('/home/claude/sig/v8_results.jsonl')]
q=lambda x:[round(float(v),3) for v in np.nanpercentile(x,[5,50,95])]
g=lambda a,b: np.array([r[a][b] for r in R],float)
print('S* grids current:', {k:q(g('CURRENT',k)) for k in ('Sstar5','Sstar10','Sstar20')})
print('support:', {k:q(g('CURRENT',k)) for k in ('support5','support10','support20')}, ' cells ok/occupied 10x10', q(g('CURRENT','cells_ok10')), q(g('CURRENT','cells10')))
for s in ('CURRENT','POST_OFF','CURRENT_ordinary','POST_OFF_ordinary'):
    print(f'{s:18s} T {q(g(s,"T"))} S {q(g(s,"S"))} S*5 {q(g(s,"Sstar5"))} S*10 {q(g(s,"Sstar10"))} U {q(g(s,"U"))}')
d=g('POST_OFF','Sstar5')-g('CURRENT','Sstar5'); print('paired change in S*5 when post-gate off',q(d),' share of excess removed', q((g('CURRENT','Sstar5')-g('POST_OFF','Sstar5'))/(g('CURRENT','Sstar5')-1)))
print('S*5 >1 share: current',round(np.mean(g('CURRENT','Sstar5')>1),2),' post-off',round(np.mean(g('POST_OFF','Sstar5')>1),2))
H=lambda k,m: np.array([r['HIST'][k][m] for r in R],float)
for m in ('T','S','U','spend'):
    b,a=H('00',m),H('11',m); print(f'HIST {m}: before {q(b)} now {q(a)} paired change {q(a-b)} now lower {np.mean(a<b):.2f}  median-of-difference vs difference-of-medians {np.median(a-b):.3f} / {np.median(a)-np.median(b):.3f}')
    phi_ban=0.5*((H('10',m)-H('00',m))+(H('11',m)-H('01',m))); phi_rb=0.5*((H('01',m)-H('00',m))+(H('11',m)-H('10',m)))
    print(f'     Shapley ban {q(phi_ban)}  re-banding {q(phi_rb)}')
c=g('CURRENT','T'); cl=g('CURRENT','learn'); ca=g('CURRENT','learn_all')
for k in ('NO_HOME','NO_ZONE_TEACH','NO_PRE_TUT','NO_HEAD_START'):
    t=np.array([r['INT'][k]['T'] for r in R]); la=np.array([r['INT'][k]['learn_all'] for r in R]); lac=np.array([r['INT'][k]['learn'] for r in R])
    print(f'{k:14s} T {q(t)} paired change {q(t-c)}  excess removed {q((c-t)/(c-1))}  learning change: academic {q(lac-cl)} cohort {q(la-ca)}')
