"""Coupled PHL R1 runs: MASSENG v5 massification engine with the shadow-tutoring sub-module switched on/off.

The multiverse (all switches declared in PRE_REGISTRATION_COUPLING.md):
  * tutoring ON vs OFF (OFF must be bit-identical to Model5; see verify_switch_off.py);
  * tutoring fee low / mid / high (0.5 / 1.0 / 2.0 of the declared reference fee = 3% of GDPpc per pupil-year);
  * own-teacher ban on / off;
  * tutoring outlay enters the household burden term ON / OFF (financing channel);
  * 3 declared parameter-uncertainty seeds (MASSENG v5 is deterministic, so a seed is a draw from a declared
    +/-20% band on the unestimated demand parameters, NOT sampling uncertainty);
  * learning odds multiplier 1.00 / 1.05 / 1.10 / 1.20 (1.00 = no achievement channel);
  * school-quality proxy: per-pupil public spending (headline) vs teacher provision (robustness);
  * limited public upper-secondary places (declared public-seat share 0.529 from DepEd SY2018-19) ON / OFF.

Run from the model package directory:
    PYTHONPATH=/root/work/masseng-tutoring/model /root/miniconda3/bin/python run_coupling.py
"""
import argparse
import copy
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from dataclasses import replace
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)


def _model_dir():
    """Locate the MASSENG model package in either the server deployment or the repo worktree."""
    cands = [os.environ.get('MASSENG_MODEL_DIR'),
             '/root/work/masseng-tutoring/model',
             os.path.join(os.path.dirname(os.path.dirname(RECORD)), 'masseng-v6', 'model')]
    for c in cands:
        if c and os.path.isdir(os.path.join(c, 'masseng')):
            return os.path.abspath(c)
    raise RuntimeError('MASSENG model dir not found; set MASSENG_MODEL_DIR')


MODEL_DIR = _model_dir()
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

from masseng.data import Country                      # noqa: E402
from masseng.engine5 import Model5                     # noqa: E402
from masseng import calibrate5 as C                    # noqa: E402
from masseng.tutoring import TutoringModel5, TutoringParams   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
RESULTS = os.path.join(RECORD, 'results')

# Declared calibration target: PHL 2010 survey (De Castro & de Guzman 2010, via Bray & Lykins 2012),
# Grade 6 40.7% and Grade 10 46.5% -> mean 43.6%.  Small purposive sample (1,235 pupils, 23 schools),
# NOT nationally representative; used for ONE parameter (b0) and then reported as a check, not reused as validation.
PHL_TUT_TARGET = (2010, 0.436)
REF_FEE_SHARE_OF_GDPPC = 0.03      # declared: no PHL tutoring-fee data exist in the repo

# declared public SHS seat share (DepEd SY2018-19 via PHL config targets: SHS 47.1% private => 52.9% public)
SHS_PUBLIC_SEAT_SHARE = {'2017': 0.529, '2024': 0.529}
SHORT = dict(cover=(0.95, 0.80, 0.67, 0.24), private=(0.15, 0.24, 0.38, 0.65))

KEY_SERIES = ['ger_primary', 'ger_secondary', 'ger_tertiary', 'ner_primary', 'ner_secondary',
              'priv_primary', 'priv_secondary', 'priv_lower_secondary', 'priv_upper_secondary', 'priv_tertiary',
              'enrol_primary', 'enrol_secondary', 'enrol_tertiary', 'S_primary', 'S_secondary', 'S_tertiary',
              'trans_lsec_usec', 'ter_entrants_deferred_share', 'edu_share_hh', 'edu_share_bottom30',
              'edu_share_top70', 'edu_share_d1', 'edu_share_d10', 'hh_share_total_spending',
              'gradlr_primary', 'gradlr_secondary', 'gradlr_tertiary', 'pool_share_20_24',
              'tut_participation', 'tut_own_share', 'tut_other_share', 'tut_commercial_share',
              'tut_spend_share_gdp', 'tut_spend_share_hh_edu', 'tut_participation_gap_q5_q1']
SELECT_YEARS = [1970, 1990, 2000, 2010, 2018, 2024]

_CTX = {}


# ----------------------------------------------------------------------------- worker
def _extract(res):
    out = {'ind': {k: [None if not np.isfinite(x) else float(x) for x in np.asarray(v)]
                   for k, v in res.ind.items()},
           'years': [int(y) for y in res.years]}
    e = res.extra
    out['flows'] = {
        'drops_by_decile': np.asarray(e['drops']).sum(axis=0).tolist(),
        'entered_by_decile': np.asarray(e['entered']).sum(axis=0).tolist(),
        'aged_by_decile': np.asarray(e['aged']).sum(axis=0).tolist(),
        'final_enrolled_by_decile': np.asarray(e['final_enrolled']).sum(axis=0).tolist(),
        'final_pool_by_decile': np.asarray(e['final_pool']).sum(axis=0).tolist(),
        'grads_by_decile_level': np.asarray(e['grads']).sum(axis=0).tolist(),
    }
    dec = e.get('deciles') or {}
    out['decile_enrolment'] = {str(y): dec[str(y)] if str(y) in dec else dec.get(y) for y in SELECT_YEARS}
    tut = e.get('tutoring') or {}
    panel = tut.get('panel') or {}
    out['tutoring'] = {'switch': tut.get('switch'), 'b0_used': tut.get('b0_used'),
                       'quality_proxy': tut.get('quality_proxy'),
                       'panel': {str(y): panel.get(y) for y in SELECT_YEARS if panel.get(y) is not None}}
    # fit comparison against the same held-out rows the repo scorecard uses
    test = _CTX['test']
    pred = C._pred(res, test)
    obs = np.array([r['value'] for r in test], float)
    table, ger_idx = {}, []
    for s in sorted({r['series'] for r in test}):
        idx = [i for i, r in enumerate(test) if r['series'] == s]
        p, o = pred[idx], obs[idx]
        m = np.isfinite(p) & np.isfinite(o)
        table[s] = dict(n=len(idx), rmse=float(np.sqrt(np.mean((p[m] - o[m]) ** 2))) if m.any() else None)
        if s in ('ger_primary', 'ger_secondary', 'ger_tertiary'):
            ger_idx.extend(idx)
    gi = np.array(ger_idx)
    p, o = pred[gi], obs[gi]
    m = np.isfinite(p) & np.isfinite(o)
    out['score'] = {'by_series': table,
                    'three_ger_rmse': float(np.sqrt(np.mean((p[m] - o[m]) ** 2))) if m.any() else None}
    return out


def _run_one(cfg):
    try:
        c = _CTX['country']
        if cfg.get('capacity'):
            c = copy.copy(c)
            c.config = copy.deepcopy(c.config)
            c.config['v5']['upper_secondary_public_capacity'] = dict(SHS_PUBLIC_SEAT_SHARE)
        tp = replace(_CTX['anchor'], fee=float(cfg['fee']), fee_ref=REF_FEE_SHARE_OF_GDPPC,
                     ban_own=bool(cfg['ban']), spend_feedback=bool(cfg['feedback']),
                     learning=bool(cfg['learning']), odds_multiplier=float(cfg['odds_multiplier']),
                     label=cfg['tag'])
        if cfg.get('seed', 0) > 0:
            rng = np.random.default_rng(20261125 + int(cfg['seed']))
            tp = tp.perturbed(rng)
        t0 = time.time()
        if cfg.get('off'):
            m = TutoringModel5(c, _CTX['fit']['params'], spec='R1', switches={'tutoring': False},
                               tut_params=tp, quality=cfg.get('quality', 'spend'),
                               calibrate_b0_to=PHL_TUT_TARGET)
        else:
            m = TutoringModel5(c, _CTX['fit']['params'], spec='R1', switches={'tutoring': True},
                               tut_params=tp, quality=cfg.get('quality', 'spend'),
                               calibrate_b0_to=PHL_TUT_TARGET)
        res = m.run(record_deciles=True)
        out = {'config': cfg, 'seconds': round(time.time() - t0, 3),
               'params_used': {k: v for k, v in tp.__dict__.items()},
               'b0_calibrated': getattr(m, 'tut_b0', None),
               **_extract(res)}
        return out
    except Exception:
        return {'config': cfg, 'error': traceback.format_exc()}


# ----------------------------------------------------------------------------- config grid
def build_configs():
    cfgs = []
    cfgs.append(dict(tag='OFF', off=True, fee=1.0, ban=False, feedback=True, learning=True,
                     odds_multiplier=1.10, seed=0, quality='spend', capacity=False))
    cfgs.append(dict(tag='OFF_capacity', off=True, fee=1.0, ban=False, feedback=True, learning=True,
                     odds_multiplier=1.10, seed=0, quality='spend', capacity=True))
    for fee in (0.5, 1.0, 2.0):
        for ban in (False, True):
            for fb in (True, False):
                for seed in (0, 1, 2):
                    cfgs.append(dict(tag=f'ON_f{fee}_ban{int(ban)}_fb{int(fb)}_s{seed}', off=False, fee=fee,
                                     ban=ban, feedback=fb, learning=True, odds_multiplier=1.10, seed=seed,
                                     quality='spend', capacity=False))
    # learning-channel sensitivity (central fee, no ban, financing feedback on)
    for m in (1.0, 1.05, 1.20):
        for seed in (0, 1, 2):
            cfgs.append(dict(tag=f'LEARN_m{m}_s{seed}', off=False, fee=1.0, ban=False, feedback=True,
                             learning=True, odds_multiplier=m, seed=seed, quality='spend', capacity=False))
    # quality-proxy robustness
    for seed in (0, 1, 2):
        cfgs.append(dict(tag=f'QUAL_teachers_s{seed}', off=False, fee=1.0, ban=False, feedback=True,
                         learning=True, odds_multiplier=1.10, seed=seed, quality='teachers', capacity=False))
    # limited public upper-secondary places (declared public-seat share) ON arm
    for seed in (0, 1, 2):
        cfgs.append(dict(tag=f'GATE_capacity_s{seed}', off=False, fee=1.0, ban=False, feedback=True,
                         learning=True, odds_multiplier=1.10, seed=seed, quality='spend', capacity=True))
    return cfgs


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=min(64, os.cpu_count() or 4))
    ap.add_argument('--out', default=os.path.join(RESULTS, 'coupling_raw.json'))
    args = ap.parse_args()
    os.makedirs(RESULTS, exist_ok=True)

    t0 = time.time()
    c = Country('PHL')
    fit = json.load(open(os.path.join(MODEL_DIR, 'outputs', 'PHL', 'v5', 'fit_R1.json')))
    rows = C.build_rows(c)
    test = [r for r in rows if r['role'] == 'test']
    bray_path = os.path.join(RESULTS, 'bray_check.json')
    if os.path.exists(bray_path):
        bray = json.load(open(bray_path))
        anchor = TutoringParams.from_bray_draw(bray['best'], label=f"bray_{bray['n_draws']}_best")
        anchor_source = f"{bray_path} best draw (max_z {bray['best']['max_z']:.3f}, {bray['n_draws']} draws)"
    else:
        anchor = TutoringParams()
        anchor_source = 'module fallback default (committed 8k-draw best)'
    _CTX.update(country=c, fit=fit, rows=rows, test=test, anchor=anchor)

    # pristine-engine baseline (Model5, no subclass) for the switch-off identity record in RUN_REPORT
    t = time.time()
    base = Model5(c, fit['params'], spec='R1').run(record_deciles=True)
    baseline_seconds = round(time.time() - t, 3)
    base_extract = _extract(base)

    cfgs = build_configs()
    print(f'{len(cfgs)} configs, {args.workers} workers; pristine baseline {baseline_seconds}s', flush=True)
    t1 = time.time()
    with Pool(processes=args.workers) as pool:
        runs = pool.map(_run_one, cfgs)
    wall = round(time.time() - t1, 3)
    errors = [r for r in runs if 'error' in r]
    for e in errors:
        print('ERROR', e['config']['tag'], '\n', e['error'], flush=True)

    meta = {
        'label': 'SIMULATION — MASSENG v5 R1 PHL with switchable shadow-tutoring module; no causal claims',
        'created_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'command': ' '.join([sys.executable] + sys.argv),
        'host': platform.node(), 'platform': platform.platform(),
        'python': sys.version.split()[0], 'numpy': np.__version__,
        'model_dir': MODEL_DIR, 'fit_R1_sha256': hashlib.sha256(
            open(os.path.join(MODEL_DIR, 'outputs', 'PHL', 'v5', 'fit_R1.json'), 'rb').read()).hexdigest(),
        'engine5_sha256': hashlib.sha256(
            open(os.path.join(MODEL_DIR, 'masseng', 'engine5.py'), 'rb').read()).hexdigest(),
        'tutoring_py_sha256': hashlib.sha256(
            open(os.path.join(MODEL_DIR, 'masseng', 'tutoring.py'), 'rb').read()).hexdigest(),
        'configs': len(cfgs), 'workers': args.workers, 'grid_wall_seconds': wall,
        'pristine_baseline_seconds': baseline_seconds, 'errors': len(errors),
        'phl_tut_target': list(PHL_TUT_TARGET), 'ref_fee_share_of_gdppc': REF_FEE_SHARE_OF_GDPPC,
        'shs_public_seat_share': SHS_PUBLIC_SEAT_SHARE,
        'anchor': {k: v for k, v in anchor.__dict__.items()}, 'anchor_source': anchor_source,
    }
    out = {'meta': meta, 'baseline_off_pristine': base_extract, 'runs': runs}
    json.dump(out, open(args.out, 'w'), indent=1)
    print(f'wrote {args.out} ({os.path.getsize(args.out) / 1e6:.2f} MB) in {wall}s; errors={len(errors)}')
    print(f'total wall {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
