#!/usr/bin/env python3
"""Recovery test (PROTOCOL.md section 4, GATE.md gate 4). Synthetic training data are generated from known
parameters (the preferred fit), with Gaussian noise whose standard deviation per series equals the training
residual SD of that fit. The fitting procedure is then run from the default starting values. Recovery is
accepted if eta and kappa are each within +-25% of the truth in at least 80% of replicates."""
import json, os, sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import masseng as m
from masseng import targets as T, calibrate as C
from masseng.engine import Model

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISO, FIT, NREP = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20


def setup():
    c = m.Country(ISO)
    truth = json.load(open(FIT))
    tr = T.train_rows(T.build(c))
    res = Model(c, truth['params'], supply_rule=truth['supply_rule'], demand_form=truth['demand_form'],
                burden_form=truth.get('burden_form', 'log'), split_income=truth.get('split_income', True),
                split_nu=truth.get('split_nu', True)).run()
    clean = C.predict(res, tr)
    obs = np.array([r['value'] for r in tr])
    sd = {}
    for s in {r['series'] for r in tr}:
        idx = [i for i, r in enumerate(tr) if r['series'] == s]
        sd[s] = float(np.std(clean[idx] - obs[idx])) if len(idx) > 1 else 1.0
    return c, truth, tr, clean, sd


def rep(k):
    c, truth, tr, clean, sd = setup()
    rng = np.random.default_rng(1000 + k)
    synth = [dict(r, value=float(clean[i] + rng.normal(0, sd[r['series']]))) for i, r in enumerate(tr)]
    f = C.fit(c, synth, supply_rule=truth['supply_rule'], demand_form=truth['demand_form'], max_nfev=200, ftol=1e-7,
              burden_form=truth.get('burden_form', 'log'), split_income=truth.get('split_income', True),
              split_nu=truth.get('split_nu', True))
    return {n: f['params'][n] for n in truth['fitted']}


if __name__ == '__main__':
    c, truth, tr, clean, sd = setup()
    with Pool(2) as p:
        reps = p.map(rep, range(NREP))
    names = truth['fitted']
    summ = {}
    for n in names:
        t = truth['params'][n]
        v = np.array([r[n] for r in reps])
        summ[n] = dict(truth=t, median=float(np.median(v)), p10=float(np.percentile(v, 10)),
                       p90=float(np.percentile(v, 90)),
                       within25=float(np.mean(np.abs(v - t) <= 0.25 * abs(t))) if t != 0 else None)
    ok = all(summ[n]['within25'] is not None and summ[n]['within25'] >= 0.8 for n in ('eta', 'kappa') if n in summ)
    out = dict(country=ISO, fit=os.path.basename(FIT), replicates=NREP, noise_sd=sd, params=summ,
               accepted=ok, rule='eta and kappa within +-25% of truth in >= 80% of replicates')
    path = os.path.join(ROOT, 'outputs', ISO, 'recovery.json')
    json.dump(out, open(path, 'w'), indent=1)
    print(json.dumps(out, indent=1))
