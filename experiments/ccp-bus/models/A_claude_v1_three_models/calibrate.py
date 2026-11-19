"""Set each model's rent parameter r so all three sit at the same status-quo incidence (x=0.30 at e0=0.35).
This makes them observationally equivalent in cross-section -- the identification problem in miniature."""
import numpy as np, json, time
from dataclasses import replace, asdict
from bus_mm import World, MODELS
E0,TARGET=0.35,0.30
def stationary(P,seeds=(11,12)):
    v=[]
    for s in seeds:
        w=World(P,s,x0=0.6); xs=[w.step()['x'] for _ in range(160)]; v.append(np.mean(xs[-60:]))
    return float(np.mean(v))
out={}
for name,P in MODELS.items():
    t=time.time(); lo,hi=-3.0,2.0
    for _ in range(14):
        mid=(lo+hi)/2; x=stationary(replace(P,r=mid,e=E0))
        lo,hi=(lo,mid) if x>TARGET else (mid,hi)
    r=(lo+hi)/2; out[name]=r
    print(f'{name}: r={r:.3f}  x={stationary(replace(P,r=r,e=E0),seeds=(21,22,23)):.3f}  ({time.time()-t:.0f}s)')
json.dump(out,open('calibrated_r.json','w'),indent=1)
