"""Smoke check for the tutoring module: calibration target, demand properties, one coupled run.

Run from the model package directory:
    PYTHONPATH=/root/work/masseng-tutoring/model /root/miniconda3/bin/python smoke_coupling.py
"""
import json
import os
import time
from dataclasses import replace

import numpy as np

from masseng.data import Country
from masseng.engine5 import Model5
from masseng import calibrate5 as C
from masseng.tutoring import TutoringModel5, TutoringParams


def main():
    c = Country('PHL')
    fit = json.load(open('outputs/PHL/v5/fit_R1.json'))
    rec = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bray_path = os.path.join(rec, 'results', 'bray_check.json')
    anchor = (TutoringParams.from_bray_draw(json.load(open(bray_path))['best'])
              if os.path.exists(bray_path) else TutoringParams())
    t0 = time.time()
    m = TutoringModel5(c, fit['params'], spec='R1', switches={'tutoring': True},
                       tut_params=anchor, calibrate_b0_to=(2010, 0.436))
    print(f'constructed in {time.time() - t0:.2f}s; calibrated b0 = {m.tut_b0:.4f}')
    yrs = list(m.years)
    yi = yrs.index(2010)
    part = m.tut_part[yi]
    print('2010 demand by level (decile mean):')
    for li, lev in enumerate(('primary', 'secondary', 'upper_secondary', 'tertiary')):
        print(f'  {lev:16s} participation {part[:, li].mean():.3f}  range {part[:, li].min():.3f}-{part[:, li].max():.3f}')
    print(f'  target: mean of primary and secondary = {0.5 * (part[:, 0].mean() + part[:, 1].mean()):.3f} '
          f'(PHL survey mean 0.436; grade6 0.407, grade10 0.465)')
    prob = m.tut_prob[yi]
    for li, lev in enumerate(('primary', 'secondary', 'upper_secondary', 'tertiary')):
        p = prob[:, li, :].mean(axis=0)
        print(f'  {lev:16s} mix none {p[0]:.3f} own {p[1]:.3f} other {p[2]:.3f} commercial {p[3]:.3f}')
    print(f'  expected spend per pupil at primary 2010: {m.tut_spend[yi][:, 0].mean():.4f} of GDPpc '
          f'(ref fee {m.tutp.fee_ref})')
    t0 = time.time()
    res = m.run(record_deciles=True)
    print(f'coupled ON run: {time.time() - t0:.2f}s')
    for name in ('tut_participation', 'tut_own_share', 'tut_other_share', 'tut_commercial_share',
                 'tut_spend_share_gdp', 'ger_secondary', 'ger_tertiary', 'edu_share_hh', 'S_secondary'):
        print(f'  {name:24s}', {y: (None if not np.isfinite(res.ind[name][yrs.index(y)])
                                     else round(float(res.ind[name][yrs.index(y)]), 3))
                                 for y in (2010, 2018, 2024)})
    # demand monotonicity properties
    for fee in (0.5, 1.0, 2.0):
        mm = TutoringModel5(c, fit['params'], spec='R1', switches={'tutoring': True},
                            tut_params=replace(anchor, fee=fee), calibrate_b0_to=(2010, 0.436))
        p = mm.tut_part[yrs.index(2010)]
        print(f'  fee={fee}: 2010 mean participation primary {p[:, 0].mean():.3f} secondary {p[:, 1].mean():.3f}, '
              f'expected spend/pupil primary {mm.tut_spend[yrs.index(2010)][:, 0].mean():.4f}')
    mm = TutoringModel5(c, fit['params'], spec='R1', switches={'tutoring': True},
                        tut_params=replace(anchor, fee=1.0, ban_own=True), calibrate_b0_to=(2010, 0.436))
    p = mm.tut_prob[yrs.index(2010)][:, 0, :].mean(axis=0)
    print(f'  ban own: 2010 primary mix none {p[0]:.3f} own {p[1]:.3f} other {p[2]:.3f} commercial {p[3]:.3f}')


if __name__ == '__main__':
    main()
