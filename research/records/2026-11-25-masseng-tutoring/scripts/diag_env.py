"""Environment/diagnostic check for the MASSENG tutoring coupling.

Run from the model package directory (research/masseng-v6/model or its server copy):
    /root/miniconda3/bin/python diag_env.py

Checks:
  1. the pristine R1 baseline runs and how long it takes;
  2. the committed R1 held-out three-GER RMSE is reproduced from the committed fit;
  3. the declared school-quality proxy candidates (teacher provision, per-pupil public
     spending) are available and in range;
  4. the engine has no score-gate/quota admissions margin (quota-vs-bar audit).
"""
import json
import time

import numpy as np

from masseng.data import Country
from masseng.engine5 import Model5
from masseng import calibrate5 as C


def main():
    t0 = time.time()
    c = Country('PHL')
    print(f'loaded PHL in {time.time() - t0:.2f}s')

    fit = json.load(open('outputs/PHL/v5/fit_R1.json'))
    t0 = time.time()
    res = Model5(c, fit['params'], spec='R1').run(record_deciles=True)
    dt = time.time() - t0
    print(f'R1 baseline run: {dt:.3f}s for {len(res.years)} years')

    # reproduce the committed R1 three-GER held-out RMSE (report says 7.458)
    rows = C.build_rows(c)
    test = [r for r in rows if r['role'] == 'test']
    ger = [r for r in test if r['series'] in ('ger_primary', 'ger_secondary', 'ger_tertiary')]
    obs = np.array([r['value'] for r in ger], float)
    pred = C._pred(res, ger)
    rmse = float(np.sqrt(np.mean((pred - obs) ** 2)))
    print(f'R1 three-GER held-out RMSE reproduced: {rmse:.3f} (committed report: 7.458)')

    yrs = list(res.years)

    def at(name, y):
        return float(res.ind[name][yrs.index(y)])

    print('headline model series:')
    for name in ('ger_primary', 'ger_secondary', 'ger_tertiary', 'trans_lsec_usec',
                 'edu_share_hh', 'edu_share_bottom30', 'edu_share_top70', 'hh_share_total_spending'):
        print(f'  {name:24s}', {y: round(at(name, y), 3) for y in (1970, 1990, 2010, 2018, 2024)})

    # --- quality proxy candidates (exogenous inputs, declared proxies for school quality)
    print('\nquality-proxy candidates:')
    prm_t, sec_t = c.wdi('SE.PRM.TCHR'), c.wdi('SE.SEC.TCHR')
    band = {}
    for y in res.years:
        age = y - 1 - (res.years - 1)  # placeholder, band from model below
    m = Model5(c, fit['params'], spec='R1')
    for y in (1971, 1990, 2010, 2024):
        b = m.band[y]
        pprim = m._band_pop(y, *b['primary'])
        psec = m._band_pop(y, *b['secondary'])
        tp = prm_t(y) if prm_t else float('nan')
        ts = sec_t(y) if sec_t else float('nan')
        print(f'  {y}: primary teachers {tp:,.0f} band-pop {pprim:,.0f} ratio {tp / pprim:.4f};'
              f' secondary teachers {ts:,.0f} band-pop {psec:,.0f} ratio {ts / psec:.4f}')
    print('teacher/pupil-band ratio range (primary):',
          min((prm_t(y) / m._band_pop(y, *m.band[y]['primary'])) for y in res.years),
          max((prm_t(y) / m._band_pop(y, *m.band[y]['primary'])) for y in res.years))
    print('teacher/pupil-band ratio range (secondary):',
          min((sec_t(y) / m._band_pop(y, *m.band[y]['secondary'])) for y in res.years),
          max((sec_t(y) / m._band_pop(y, *m.band[y]['secondary'])) for y in res.years))
    for code in ('SE.XPD.PRIM.PC.ZS', 'SE.XPD.SECO.PC.ZS', 'SE.XPD.TERT.PC.ZS'):
        s = c.wdi(code)
        print(f'  {code}:', s.observed() if s else 'MISSING')

    # --- admissions-gate audit: does the engine support quota vs score bar?
    print('\nadmissions-gate audit:')
    print('  config tertiary_entry_exam:', c.config.get('tertiary_entry_exam'))
    print('  v5 annual_capacity:', c.config.get('v5', {}).get('annual_capacity'))
    print('  v5 upper_secondary_public_capacity:', c.config.get('v5', {}).get('upper_secondary_public_capacity'))
    print('  model.exam:', m.exam, '| us_cap:', m.us_cap)

    print('\nSIMULATION/DIAGNOSTIC ONLY — no inference. env check done in %.1fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
