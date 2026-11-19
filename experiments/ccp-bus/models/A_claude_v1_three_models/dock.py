"""Docking (Axtell et al. 1996): ABM with global mixing and no removal vs. analytic mean-field."""
import numpy as np, time, meanfield as MF
from dataclasses import replace, asdict
from bus_mm import World, MODEL_A, MODEL_B
rows=[]
t0=time.time()
for name,P in [('A',MODEL_A),('B',MODEL_B)]:
    mfp=dict(r=P.r,sigma=1.0,tau=P.tau,h=P.h,F=P.F,phi=P.phi,kappa=P.kappa)
    for e in [0.1,0.3,0.4,0.5,0.6]:
        q=replace(P,e=e,mixing='global',removal=False,N=2000)
        res=[]
        for x0 in (0.0,0.6):
            w=World(q,seed=1,x0=x0); xs=[w.step()['x'] for _ in range(150)]
            res.append(np.mean(xs[-50:]))
        mf=[round(x,3) for x,s in MF.fixed_points(mfp,e) if s]
        print(f'{name} e={e}: ABM from low={res[0]:.3f} from high={res[1]:.3f} | mean-field stable={mf}')
print('time %.1fs'%(time.time()-t0))
