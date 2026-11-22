"""Score fitted rivals without fitting on post-1995 enrolment."""
import json
from pathlib import Path

import numpy as np

from masseng.data import Country
from masseng import calibrate5 as C


def rmse(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    keep = np.isfinite(a) & np.isfinite(b)
    return float(np.sqrt(np.mean((a[keep] - b[keep]) ** 2))) if keep.any() else None


def main(iso='PHL'):
    c = Country(iso)
    rows = C.build_rows(c)
    root = Path('outputs') / iso / 'v5'
    paths = sorted(root.glob('fit_R*.json'))
    expected = {f'R{i}' for i in range(6)}
    found = {json.loads(path.read_text())['spec'] for path in paths}
    if found != expected:
        raise RuntimeError(f'Refusing incomplete scorecard: expected {sorted(expected)}, found {sorted(found)}')
    output = {
        'status': 'retrospective inspected test; not blind; not calibrated; losses reported before model preference',
        'decision_rule': 'lowest RMSE across all held-out observations of the three GER series',
        'protocol_amendments': [],
        'rivals': {},
    }
    results = {}
    test = [r for r in rows if r['role'] == 'test']
    ger = [r for r in test if r['series'] in ('ger_primary', 'ger_secondary', 'ger_tertiary')]
    observed_ger = [r['value'] for r in ger]
    window = [r for r in rows if r['role'] in ('train', 'diagnostic') and r['year'] <= c.config['years']['train'][1]]
    for path in paths:
        fit = json.loads(path.read_text())
        res, table = C.score(c, fit, rows)
        results[fit['spec']] = res
        pred = C._pred(res, ger)
        bm = C.benchmarks(window, ger)
        output['rivals'][fit['spec']] = {
            'train_cost': fit['cost'], 'nfev': fit['nfev'], 'total_nfev': fit.get('total_nfev', fit['nfev']),
            'at_bounds': fit['at_bounds'], 'series_losses': table,
            'three_ger_rmse': {'model': rmse(pred, observed_ger),
                               'persistence': rmse(bm[:, 0], observed_ger),
                               'trend': rmse(bm[:, 1], observed_ger)},
            'parameters': fit['params'],
        }
    if 'R0' in results:
        r0_ger = rmse(C._pred(results['R0'], ger), observed_ger)
        for spec, res in results.items():
            comparison = {}
            for s in sorted({r['series'] for r in test}):
                selected = [r for r in test if r['series'] == s]
                observed = [r['value'] for r in selected]
                model_loss = rmse(C._pred(res, selected), observed)
                r0_loss = rmse(C._pred(results['R0'], selected), observed)
                comparison[s] = {'model': model_loss, 'R0': r0_loss,
                                 'model_minus_R0': None if model_loss is None or r0_loss is None else model_loss-r0_loss}
            output['rivals'][spec]['rmse_comparison_with_R0'] = comparison
            output['rivals'][spec]['three_ger_rmse']['model_minus_R0'] = output['rivals'][spec]['three_ger_rmse']['model']-r0_ger
    for spec, res in results.items():
        years = list(res.years)
        output['rivals'][spec]['separating_observations'] = {
            'tertiary_ger_2013': float(res.ind['ger_tertiary'][years.index(2013)]),
            'tertiary_ger_2024': float(res.ind['ger_tertiary'][years.index(2024)]),
            'grade10_to_grade11_2018': 100.0 * float(res.ind['trans_lsec_usec'][years.index(2018)]),
            'recession_secondary_ger': {str(y): float(res.ind['ger_secondary'][years.index(y)]) for y in (1984, 1985, 1986, 1998)},
        }
    separating = {}
    for key, series, target_years in (
        ('tertiary_2013_2024', 'ger_tertiary', [2013, 2024]),
        ('recession_secondary', 'ger_secondary', [1984, 1985, 1986, 1998]),
        ('grade10_to_grade11_2018', 'trans_lsec_usec', [2018]),
    ):
        base = output['rivals']['R0']['series_losses'][series]
        selected = [i for i, y in enumerate(base['years']) if y in target_years]
        observed = [base['obs'][i] for i in selected]
        years = [base['years'][i] for i in selected]
        losses = {}
        for spec in results:
            table = output['rivals'][spec]['series_losses'][series]
            by_year = dict(zip(table['years'], table['pred']))
            losses[spec] = rmse([by_year[y] for y in years], observed)
        separating[key] = {'series': series, 'years': years, 'observed': observed, 'rmse': losses,
                           'supported_rival': min(losses, key=lambda s: losses[s]) if years and all(v is not None for v in losses.values()) else None,
                           'rule': 'lowest error on this observation; no support claim if observations are absent'}
    output['separating_test_outcomes'] = separating
    winner = min(output['rivals'], key=lambda s: output['rivals'][s]['three_ger_rmse']['model'])
    output['winner_by_preregistered_rule'] = winner
    path = root / 'scores.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({s: v['three_ger_rmse'] for s, v in output['rivals'].items()}, indent=2))
    print('winner:', winner)


if __name__ == '__main__':
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else 'PHL')
