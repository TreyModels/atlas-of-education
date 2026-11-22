"""Synthetic parameter recovery for the selected rival, using only training-row structure."""
import argparse
import json
from pathlib import Path

import numpy as np

from masseng.data import Country
from masseng import calibrate5 as C
from masseng.engine5 import Model5


def main():
    p = argparse.ArgumentParser()
    p.add_argument('spec')
    p.add_argument('--replicates', type=int, default=20)
    p.add_argument('--max-nfev', type=int, default=250)
    args = p.parse_args()
    c = Country('PHL')
    rows = C.build_rows(c)
    train = [r for r in rows if r['role'] == 'train']
    true_fit = json.loads((Path('outputs/PHL/v5') / f'fit_{args.spec}.json').read_text())
    truth = true_fit['params']
    synthetic = C._pred(Model5(c, truth, spec=args.spec).run(), train)
    rng = np.random.default_rng(502028)
    recovered = []
    for i in range(args.replicates):
        # Fixed declared recovery noise: 1 pp for rates/shares, 0.1 pp spending, 0.01 index.
        noise = np.array([.1 if r['series'].startswith('edu_share') else
                          (.01 if r.get('transform') == 'index_2016' else 1.) for r in train])
        perturbed = []
        for r, value, sd in zip(train, synthetic, noise):
            q = dict(r); q['value'] = float(value + rng.normal(0, sd)); perturbed.append(q)
        fit = C.fit(c, perturbed, args.spec, start=truth, max_nfev=args.max_nfev)
        recovered.append(fit)
        print('replicate', i + 1, 'cost', fit['cost'], 'nfev', fit['nfev'], 'bounds', fit['at_bounds'], flush=True)
    summary = {'spec': args.spec, 'replicates': args.replicates, 'noise': 'declared Gaussian recovery noise',
               'truth': truth, 'parameters': {}, 'optimizer_cap_replicates': sum(r['nfev'] >= args.max_nfev for r in recovered)}
    for name in ('b_h', 'b_p', 'kappa'):
        if name not in C.fitted_names(args.spec):
            summary['parameters'][name] = {'status': 'not in rival'}
            continue
        vals = np.array([r['params'][name] for r in recovered]); base = truth[name]
        if abs(base) < 1e-8:
            status = 'not identified: zero true value prevents relative recovery criterion'
            success = None
        else:
            success = float(np.mean(np.abs(vals - base) <= .25 * abs(base)))
            status = 'identified' if success >= .8 else 'not identified'
        summary['parameters'][name] = {'median': float(np.median(vals)), 'q05': float(np.quantile(vals, .05)),
                                       'q95': float(np.quantile(vals, .95)), 'within_25pct_share': success,
                                       'bound_hit_replicates': sum(name in r['at_bounds'] for r in recovered), 'status': status}
    path = Path('outputs/PHL/v5') / f'recovery_{args.spec}.json'
    path.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary['parameters'], indent=2))


if __name__ == '__main__':
    main()
