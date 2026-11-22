#!/usr/bin/env python3
"""Fit every pre-registered rival on training rows only (PROTOCOL.md sections 2 and 4). Two worker processes."""
import json, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import masseng as m
from masseng import targets as T, calibrate as C

ISO = sys.argv[1] if len(sys.argv) > 1 else 'PHL'
VERSION = sys.argv[2] if len(sys.argv) > 2 else 'v2'
BURDEN = 'linear' if VERSION == 'v1' else 'log'
SPLIT = VERSION not in ('v1', 'v2')
SPLIT_NU = VERSION not in ('v1', 'v2', 'v3')
RIVALS = [('income', 'fiscal'), ('trend', 'fiscal'), ('none', 'fiscal'),
          ('income', 'trend'), ('income', 'responsive'), ('income', 'unconstrained')]


def job(rv):
    demand, supply = rv
    c = m.Country(ISO)
    tr = T.train_rows(T.build(c))
    t = time.time()
    f = C.fit(c, tr, supply_rule=supply, demand_form=demand, max_nfev=300, ftol=1e-7, burden_form=BURDEN,
              split_income=SPLIT, split_nu=SPLIT_NU)
    f['seconds'] = time.time() - t
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs', ISO, VERSION,
                       f'fit_{demand}_{supply}.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(f, open(out, 'w'), indent=1, default=float)
    return demand, supply, f['cost'], f['seconds']


if __name__ == '__main__':
    with Pool(2) as p:
        for r in p.imap_unordered(job, RIVALS):
            print(*r, flush=True)
