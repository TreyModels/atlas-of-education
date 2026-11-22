"""Run declared-capacity sensitivity scenarios in Opus's engine5.

Run from the Opus handoff model directory:
  python /path/to/run_engine5_array.py /path/to/engine5_array_summary.json
Capacities are not observed school supply and results are not fitted estimates.
"""
import copy
import json
import sys
from pathlib import Path

import numpy as np

import masseng as m
from masseng.engine5 import LEVEL_NAMES, Model5

COVERAGE = {
    'PHL': {'public': [.95, .80, .67, .24], 'private': [.15, .24, .38, .65]},
    'KHM': {'public': [.86, .65, .53, .20], 'private': [.11, .18, .17, .42]},
}


def run(iso):
    country = m.Country(iso)
    country.config = copy.deepcopy(country.config)
    default = Model5(country).run()
    annual = Model5(country, annual_market=True)
    # Anchor declared capacity to the reference-age population, never to model applicants.
    ages = [6, 12, 16, 18]
    capacity = {}
    for li, name in enumerate(LEVEL_NAMES):
        population = {str(y): annual._pop_at_age(y, ages[li]) for y in annual.years}
        capacity[name] = {
            sector: {y: COVERAGE[iso][sector][li] * pop for y, pop in population.items()}
            for sector in ('public', 'private')
        }
    country.config['v5']['annual_capacity'] = capacity
    capped = Model5(country, annual_market=True).run()
    e = capped.extra
    residual = e['entered'] - (e['final_enrolled'] + e['drops'] + e['grads'].sum(axis=2)
                               + e['aged'] + e['final_pool'])
    mk = e['markets']
    return {
        'status': 'DECLARED CAPACITY SENSITIVITY; not observed supply, not an R0-R5 fit',
        'capacity_coverage': COVERAGE[iso],
        'tertiary_ger_2024_unconstrained': float(default.ind['ger_tertiary'][-1]),
        'tertiary_ger_2024_capped': float(capped.ind['ger_tertiary'][-1]),
        'unmet_effective_entrants_2024': dict(zip(LEVEL_NAMES, mk['unmet_effective'][-1].sum(axis=1).tolist())),
        'realised_entrants_2024': dict(zip(LEVEL_NAMES, mk['R'][-1].sum(axis=1).tolist())),
        'max_absolute_cohort_share_conservation_residual': float(np.abs(residual).max()),
        'max_funnel_violation_persons': float(max(np.max(mk['L'] - mk['Q']),
                                                  np.max(mk['E'] - mk['L']), np.max(mk['R'] - mk['E']))),
    }


if __name__ == '__main__':
    output = {iso: run(iso) for iso in ('PHL', 'KHM')}
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('engine5_array_summary.json')
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))
