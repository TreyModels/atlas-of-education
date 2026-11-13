import time, numpy as np
from model import Params, run, draw_params, World
t=time.time(); o=run(Params(), 1); print(round(time.time()-t,3),'s'); print({k:round(v,3) for k,v in o.items()})
rng=np.random.default_rng(0); ts=[]; conv=0
for i in range(40):
    v=['thin','diversion','favour','full'][i%4]; pr=draw_params(rng,v)
    t=time.time(); w=World(pr,i).solve(); o=w.outcomes(); ts.append(time.time()-t); conv+=o['converged']
print('mean time',np.mean(ts),'max',np.max(ts),'converged',conv,'/40')
