"""E13c: level-matched rival for the graduate-supply shock (Council brief 002, follow-up).
Stage 1 calibrates fair_slots_mult and fair_income_scale per sigma to match the surplus world's
baseline formal share and degree income. Stage 2 runs the paired shock comparison."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from massabm import make_params, run_model
from massabm.experiments8 import BASE, SHOCKS, _outcomes

SIGMAS = [0.5, 1.0, 2.0]
SUR = dict(mode='full')
RIV = dict(mode='hc_fair_slots')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    # ---- stage 1: surplus baseline (target) and rival calibrations.
    # Calibrate SEQUENTIALLY: first the slot multiplier with income scale = 1 (the two are not independent:
    # the wage level changes household schooling decisions and therefore the formal share). Then fit the
    # income scale with the fitted multiplier. Iterate each 2x; report the achieved match honestly.
    NOSHOCK = [(1900, 1.0), (2100, 1.0)]
    S_sur = run_model(make_params(seed=20000, N=a.N, tuition_path=NOSHOCK,
                                  macro_elasticity=0.0, **BASE, **SUR))
    o_sur = _outcomes(S_sur)
    target_share, target_deg = o_sur['formal_rate_diploma'], o_sur['degree_income']
    calib = []
    for sg in SIGMAS:
        def run_r(rm, rs):
            return _outcomes(run_model(make_params(
                seed=20000, N=a.N, tuition_path=NOSHOCK, macro_elasticity=0.0,
                **BASE, **RIV, fair_sigma=sg, fair_slots_mult=rm, fair_income_scale=rs)))
        o0 = run_r(1.0, 1.0)
        # 1) fit the slot multiplier with the wage scale held at 1.0 (the wage scale is not
        #    behaviour-neutral: it changes affordability, hence entrants, hence the formal share)
        rm, rs = 1.0, 1.0
        for _ in range(2):
            o = run_r(rm, rs)
            rm = max(0.02, rm * target_share / max(o['formal_rate_diploma'], 1e-6))
        # 2) fit the wage level on the fitted slot multiplier, then refit the multiplier once
        o = run_r(rm, rs)
        rs = max(1e-3, rs * target_deg / max(o['degree_income'], 1e-9))
        o2 = run_r(rm, rs)
        rm = max(0.02, rm * target_share / max(o2['formal_rate_diploma'], 1e-6))
        o3 = run_r(rm, rs)
        calib.append(dict(sigma=sg, target_share=target_share, target_degree_income=target_deg,
                          mult=rm, scale=rs, achieved_share=o3['formal_rate_diploma'],
                          achieved_degree_income=o3['degree_income'],
                          rival_share_unmatched=o0['formal_rate_diploma'],
                          rival_degree_income_unmatched=o0['degree_income']))
        print(f'  sigma={sg}: mult={rm:.4f} scale={rs:.4f} -> share {o3["formal_rate_diploma"]:.4f} '
              f'(target {target_share:.4f}), deg inc {o3["degree_income"]:.3f} (target {target_deg:.3f})', flush=True)
    write_rows(os.path.join(a.out, 'e13c_calibration.csv'), list(calib[0].keys()), [[r[k] for k in calib[0]] for r in calib])
    # ---- stage 2: paired shock comparison
    jobs = []
    for sh, tp in SHOCKS.items():
        for r in range(a.reps):
            jobs.append((('surplus', None, sh, r), 'massabm',
                         make_params(seed=20000 + r, N=a.N, tuition_path=tp, macro_elasticity=0.0, **BASE, **SUR)))
    for c in calib:
        for sh, tp in SHOCKS.items():
            for r in range(a.reps):
                jobs.append((('rival', c['sigma'], sh, r), 'massabm',
                             make_params(seed=20000 + r, N=a.N, tuition_path=tp, macro_elasticity=0.0,
                                         **BASE, **RIV, fair_sigma=c['sigma'],
                                         fair_slots_mult=c['mult'], fair_income_scale=c['scale'])))
    print(f'E13c stage 2: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for (w, sg, sh, r), o in res.items():
        if isinstance(o, dict) and 'error' in o:
            continue
        B = res.get((w, sg, 'no shock', r))
        if B is None or (isinstance(B, dict) and 'error' in B):
            continue
        Aa, Bb = _outcomes(o), _outcomes(B)
        rows.append(dict(world=w, sigma=sg, shock=sh, rep=r,
                         formal_rate_diploma=Aa['formal_rate_diploma'],
                         d_formal_rate_diploma=Aa['formal_rate_diploma'] - Bb['formal_rate_diploma'],
                         diploma_income=Aa['basic_income'], d_diploma_income=Aa['basic_income'] - Bb['basic_income'],
                         degree_income=Aa['degree_income'], d_degree_income=Aa['degree_income'] - Bb['degree_income'],
                         ratio=Aa['basic_income'] / Aa['degree_income'],
                         d_ratio=Aa['basic_income'] / Aa['degree_income'] - Bb['basic_income'] / Bb['degree_income']))
    write_rows(os.path.join(a.out, 'e13c_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
    summ = []
    for w in ['surplus', 'rival']:
        for sg in ([None] if w == 'surplus' else SIGMAS):
            for sh in SHOCKS:
                R = [r for r in rows if r['world'] == w and r['sigma'] == sg and r['shock'] == sh]
                if not R:
                    summ.append(dict(world=w, sigma=sg, shock=sh, n_ok=0)); continue
                row = dict(world=w, sigma=sg, shock=sh, n_ok=len(R))
                for k in ['formal_rate_diploma', 'd_formal_rate_diploma', 'diploma_income', 'd_diploma_income',
                          'degree_income', 'd_degree_income', 'ratio', 'd_ratio']:
                    row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
                summ.append(row)
    KEYS = ['formal_rate_diploma', 'd_formal_rate_diploma', 'diploma_income', 'd_diploma_income',
            'degree_income', 'd_degree_income', 'ratio', 'd_ratio']
    hdr = ['world', 'sigma', 'shock', 'n_ok'] + [x for k in KEYS for x in (k, k + '_sd')]
    write_rows(os.path.join(a.out, 'e13c_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    L = ['E13c LEVEL-MATCHED RIVAL (Council brief 002, follow-up)',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         'Surplus baseline formal share 0.2858 and degree income 2.926 are the match targets (E13b, 6 reps).',
         'Stage 1 multiplies the rival formal vacancy count and wage level per sigma; achieved match below.', '',
         'CALIBRATION (achieved vs target):']
    for c in calib:
        L.append(f'  sigma={c["sigma"]:.1f}: formal share unmatched {c["rival_share_unmatched"]:.3f} -> matched '
                 f'{c["achieved_share"]:.3f} (target {c["target_share"]:.3f}); degree income unmatched '
                 f'{c["rival_degree_income_unmatched"]:.3f} -> matched {c["achieved_degree_income"]:.3f} '
                 f'(target {c["target_degree_income"]:.3f}); mult={c["mult"]:.4f} scale={c["scale"]:.4f}')
    L += ['', f'  {"world":10s} {"sigma":>5s} {"shock":28s} {"d formal|dip":>16s} {"d diploma inc":>16s} {"d ratio":>9s}']
    for r in summ:
        if not r.get('n_ok') or r['shock'] == 'no shock':
            continue
        sgv = r['sigma'] if r['sigma'] is not None else 0.0
        L.append(f'  {r["world"]:10s} {sgv:5.1f} {r["shock"]:28s} '
                 f'{r["d_formal_rate_diploma"]:+10.4f}({r["d_formal_rate_diploma_sd"]:.3f}) '
                 f'{r["d_diploma_income"]:+10.4f}({r["d_diploma_income_sd"]:.3f}) {r["d_ratio"]:+9.4f}')
    def G(w, sg, sh, k):
        for r in summ:
            if r['world'] == w and r['sigma'] == sg and r['shock'] == sh:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    sh = 'college half price from 1995'
    sur_f, sur_fsd = G('surplus', None, sh, 'd_formal_rate_diploma')
    L += ['', f'DECISION (predeclared): surplus d_formal|dip at half-price = {sur_f:+.4f} (±{sur_fsd:.4f}).']
    falls = []
    for sg in SIGMAS:
        f, fsd = G('rival', sg, sh, 'd_formal_rate_diploma')
        L.append(f'  rival sigma={sg}: d_formal|dip = {f:+.4f} (±{fsd:.4f})')
        if f < 0 and abs(f) > 2 * fsd:
            falls.append((sg, f))
    if sur_f < 0 and not falls:
        L.append('  -> the level-matched rival never shows a significant formal-probability fall while the')
        L.append('     surplus world does: PREDICTION 2 SURVIVES in its formal-access form.')
    elif falls:
        L.append('  -> the level-matched rival DOES fall at sigma=' + ', '.join(str(s) for s, _ in falls) +
                 ': PREDICTION 2 MUST BE WITHDRAWN.')
    else:
        L.append('  -> the surplus fall is itself not significant after level-matching; inconclusive/withdrawn.')
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E13c', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   calibration=calib), open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
