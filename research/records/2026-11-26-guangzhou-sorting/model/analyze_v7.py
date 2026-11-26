import json,itertools,math,numpy as np
R=[json.loads(l) for l in open('/home/claude/sig/v7_factorial.jsonl')]
M=['BAN','BOARD','REBAND','SUBST']; q=lambda x:[round(float(v),3) for v in np.nanpercentile(x,[5,50,95])]
def shap(cells,k):
    phi=np.zeros(4)
    for j in range(4):
        others=[x for x in range(4) if x!=j]
        for r in range(4):
            for S in itertools.combinations(others,r):
                w=math.factorial(r)*math.factorial(3-r)/math.factorial(4)
                a=['0']*4; [a.__setitem__(s,'1') for s in S]; b=a.copy(); b[j]='1'
                phi[j]+=w*(cells[''.join(b)][k]-cells[''.join(a)][k])
    return phi
for k in ('T','S','U','spend'):
    ph=np.array([shap(r['cells'],k) for r in R]); tot=np.array([r['cells']['1111'][k]-r['cells']['0000'][k] for r in R])
    print(f'{k}: total change all-off->all-on {q(tot)}'); [print(f'   {M[j]:7s} {q(ph[:,j])}') for j in range(4)]
# realistic before: ban off, boarding on, reband off, substitution on (holiday tutoring and routes existed before 2021)
for k in ('T','S','U','spend'):
    b=np.array([r['cells']['0101'][k] for r in R]); a=np.array([r['cells']['1111'][k] for r in R])
    print(f'{k}: realistic before (no ban, boarding, no reband, substitution) {q(b)} -> now {q(a)}  change {q(a-b)}  now lower in {np.mean(a<b):.2f}')
print('\nS vs S* (current):',q([r['cells']['1111']['S'] for r in R]),q([r['cells']['1111']['S_star'] for r in R]))
print('S* share >1:',round(np.mean(np.array([r['cells']['1111']['S_star'] for r in R])>1),2))
for k in ('NO_HOME','NO_ZONE_TEACH','NO_PRE_TUT','NO_HEAD_START','NO_ROUTES'):
    t=np.array([r['interv'][k]['T'] for r in R]); c=np.array([r['cells']['1111']['T'] for r in R]); u=np.array([r['interv'][k]['U'] for r in R]); cu=np.array([r['cells']['1111']['U'] for r in R])
    print(f'{k:14s} T {q(t)} (change {q(t-c)})   U change {q(u-cu)}')
