"""Summarize the exploratory parameter-and-cohort design."""
import csv
import json
from pathlib import Path
from statistics import NormalDist
import numpy as np

ROOT = Path(__file__).resolve().parent

def column(key):
    values = np.array([float(row[key]) for row in rows])
    assert np.isfinite(values).all(), key
    return values

def distribution(values):
    return dict(zip(['p05', 'median', 'p95'], map(float, np.quantile(values, [.05, .5, .95]))))

def improvement(values):
    n = len(values)
    count = int(np.count_nonzero(values < 0))
    p = count / n
    z = NormalDist().inv_cdf(.975)
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    margin = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return dict(n=n, count=count, proportion=p, wilson95=[center-margin, center+margin])

if __name__ == '__main__':
    rows = list(csv.DictReader((ROOT / 'draws.csv').open()))
    assert len(rows) == 1024 and len({r['draw'] for r in rows}) == 1024
    
    delta = column('T') - column('T_before')
    ban = column('T') - column('T_noban')
    summary = {key: distribution(column(key)) for key in
               ['T_before', 'T', 'T_noban', 'S', 'Sstar', 'support', 'spend_change', 'displaced']}
    summary['delta_T'] = {**distribution(delta), **improvement(delta)}
    summary['delta_T_ban'] = {**distribution(ban), **improvement(ban)}
    summary['ban_gradient_quartiles'] = []
    for i in range(4):
        mask = (column('BAN_GRAD') >= i/4) & (column('BAN_GRAD') < (i+1)/4)
        summary['ban_gradient_quartiles'].append(dict(
            lower=i/4, upper=(i+1)/4, **distribution(ban[mask]), **improvement(ban[mask])))
    summary['fade_bands'] = []
    for i in range(6):
        mask = (column('DECAY') >= i*.15) & (column('DECAY') < (i+1)*.15)
        summary['fade_bands'].append(dict(lower=i*.15, upper=(i+1)*.15,
                                         n=int(mask.sum()), **distribution(column('T')[mask])))
    summary['rule_envelope'] = {}
    mask = (column('QUOTA') <= .18) & (column('ZHIBIAO') >= .5)
    summary['rule_envelope'] = {**distribution(delta[mask]), **improvement(delta[mask])}
    (ROOT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
