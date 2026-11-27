"""Variance check at 128 independent settings, each repeated with eight cohort seeds."""
import csv
from concurrent.futures import ProcessPoolExecutor
import sys
import numpy as np
from sweep import N, RANGES, gz_v5, rates

def one(job):
    i, j = job
    design = np.random.default_rng(np.random.SeedSequence([12272026, i, 0]))
    p = {key: design.uniform(*b) for key, b in RANGES.items()}
    p['HS_TEACH_SD'] = p['TEACH_SD']
    seed = int(np.random.SeedSequence([12272026, i, 1, j]).generate_state(1)[0])
    d = gz_v5.run(n=N, seed=seed, **p)
    b = gz_v5.run(n=N, seed=seed, **{**p, 'BAN_RED': 0, 'REBAND': False})
    noban = gz_v5.run(n=N, seed=seed, **{**p, 'BAN_RED': 0})
    return i, j, seed, rates(d,d['uni'],'tal') - rates(b,b['uni'],'tal'), rates(d,d['uni'],'tal') - rates(noban,noban['uni'],'tal')

if __name__ == '__main__':
    w = csv.writer(sys.stdout)
    w.writerow(['setting','replicate','seed','delta_T','delta_T_ban'])
    with ProcessPoolExecutor(4) as pool:
        w.writerows(pool.map(one, ((i,j) for i in range(128) for j in range(8)), chunksize=4))
