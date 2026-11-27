"""Controlled enforcement-gradient sensitivity at the same 256 parameter settings."""
import csv
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from sweep import N,SEED,RANGES,gz_v5 as model,rates

def one(i):
    design,cohort=np.random.SeedSequence([SEED,i]).spawn(2)
    rng=np.random.default_rng(design);p={key:rng.uniform(*b) for key,b in RANGES.items()}
    p['HS_TEACH_SD']=p['TEACH_SD'];seed=int(cohort.generate_state(1)[0])
    no_ban=model.run(n=N,seed=seed,**{**p,'BAN_RED':0})
    reference=rates(no_ban,no_ban['uni'],'tal')
    values=[]
    for gradient in [0,.5,1]:
        d=model.run(n=N,seed=seed,**{**p,'BAN_GRAD':gradient})
        values.append((i,gradient,rates(d,d['uni'],'tal')-reference))
    return values

if __name__=='__main__':
    with ProcessPoolExecutor(4) as pool,(Path(__file__).parent/'enforcement.csv').open('w') as out:
        writer=csv.writer(out);writer.writerow(['setting','BAN_GRAD','delta_T_ban'])
        for values in pool.map(one,range(256),chunksize=4):writer.writerows(values)
