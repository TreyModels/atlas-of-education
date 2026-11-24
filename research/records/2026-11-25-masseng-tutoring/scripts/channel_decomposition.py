"""Channel decomposition: how much of the coupled effect comes from the declared achievement shift vs the
financing (outlay-in-burden) channel?

Four ON arms against the untouched baseline:
  learning + financing, learning only, financing only, neither (module on but no effect).
Plus the ban and fee lever for the record.  Run from the model package directory:
    PYTHONPATH=/root/work/masseng-tutoring/model /root/miniconda3/bin/python channel_decomposition.py
"""
import json
import os

import numpy as np

from masseng.data import Country
from masseng.engine5 import Model5
from masseng.tutoring import TutoringModel5, TutoringParams

YEARS = [2010, 2018, 2024]
IND = ['ger_primary', 'ger_secondary', 'ger_tertiary', 'ner_primary', 'ner_secondary',
       'trans_lsec_usec', 'S_secondary', 'S_tertiary', 'edu_share_hh', 'hh_share_total_spending',
       'priv_secondary', 'priv_tertiary', 'tut_participation', 'tut_spend_share_gdp']


def main():
    c = Country('PHL')
    fit = json.load(open('outputs/PHL/v5/fit_R1.json'))
    rec = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bray_path = os.path.join(rec, 'results', 'bray_check.json')
    anchor = (TutoringParams.from_bray_draw(json.load(open(bray_path))['best'])
              if os.path.exists(bray_path) else TutoringParams())
    base = Model5(c, fit['params'], spec='R1').run(record_deciles=True)
    yrs = list(base.years)
    arms = {
        'baseline_off': None,
        'ON_fb1_learn1': dict(spend_feedback=True, learning=True),
        'ON_fb1_learn0': dict(spend_feedback=True, learning=False),
        'ON_fb0_learn1': dict(spend_feedback=False, learning=True),
        'ON_fb0_learn0': dict(spend_feedback=False, learning=False),
        'ON_fb0_learn1_ban': dict(spend_feedback=False, learning=True, ban_own=True),
    }
    out = {'baseline': {}}
    for name, kw in arms.items():
        if kw is None:
            res = base
        else:
            from dataclasses import replace
            tp = replace(anchor, fee=1.0, **{k: v for k, v in kw.items()})
            m = TutoringModel5(c, fit['params'], spec='R1', switches={'tutoring': True}, tut_params=tp,
                               calibrate_b0_to=(2010, 0.436))
            res = m.run(record_deciles=True)
        row = {}
        for k in IND:
            if k not in res.ind:
                continue
            row[k] = {y: (None if not np.isfinite(res.ind[k][yrs.index(y)])
                          else round(float(res.ind[k][yrs.index(y)]), 4)) for y in YEARS}
        e = res.extra
        row['dropout_per_entrant_by_decile'] = (
            np.asarray(e['drops']).sum(axis=0) / np.maximum(np.asarray(e['entered']).sum(axis=0), 1)
        ).round(4).tolist()
        out[name] = row
    # deltas vs baseline for the readable years
    out['deltas_vs_baseline'] = {}
    for name in arms:
        if name == 'baseline_off':
            continue
        d = {}
        for k in IND:
            if k in out[name] and k in out['baseline_off']:
                d[k] = {y: (None if out[name][k][y] is None or out['baseline_off'][k][y] is None
                            else round(out[name][k][y] - out['baseline_off'][k][y], 4)) for y in YEARS}
        out['deltas_vs_baseline'][name] = d
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results',
                    'channel_decomposition.json')
    json.dump(out, open(path, 'w'), indent=2)
    print(json.dumps(out['deltas_vs_baseline'], indent=1))
    print('\nwrote', path)


if __name__ == '__main__':
    main()
