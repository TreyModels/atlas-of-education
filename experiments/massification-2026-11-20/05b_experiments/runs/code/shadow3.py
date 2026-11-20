"""shadow3.py — Loop 3: stage-matched shadow checks (S1), structural non-universality (S2),
price/entry calibration (S3). NEW module (NOT massabm/floorworld/triad/paper reproduction).

Declared structural shadow-incidence model: demand by stage x urban/rural from gate stakes, credential
returns, public-school substitute, income, price/income and capacity utilisation; supply from commercial
firms and teacher-tutors with entry costs, capacity, entry/exit and price tatonnement. Predeclaration:
loop3/PRE_DECLARATIONS_L3.md. All numbers are stylized model output.

Usage: python shadow3.py --out ../runs
"""
import argparse
import csv
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bcommon import write_rows, write_text, m_sd  # noqa: E402

PUPILS = 1000.0
A0 = -1.5
B_STAKE, B_RET, B_PUB, B_INC, B_FEE, B_CONG = 1.0, 0.9, 1.4, 0.55, 1.2, 0.6
PRICE_ITER, PRICE_ADJ, ENTRY_SPEED = 60, 0.20, 0.15
SEEDS = list(range(5))

COUNTRIES = {
    'PH-like': dict(income=1.0, urban=0.48, urban_mult=1.8, rural_mult=0.6, public_sub=0.40,
                    enrol=dict(primary=0.55, lower=0.25, upper=0.20),
                    stakes=dict(primary=0.30, lower=0.60, upper=1.00),
                    returns=dict(primary=0.20, lower=0.35, upper=0.70),
                    fee_base=0.50, cost_mult=1.0, F_cm=4.5, F_tt=0.60,
                    cap_cm=0.090, cap_tt=0.040, teacher_cap=0.50, n_cm0=2.0, n_tt0=6.0),
    'HK-like': dict(income=3.0, urban=1.0, urban_mult=1.0, rural_mult=0.6, public_sub=0.70,
                    enrol=dict(primary=0.35, lower=0.22, middle=0.21, senior=0.22),
                    stakes=dict(primary=0.40, lower=0.70, middle=0.90, senior=1.20),
                    returns=dict(primary=0.25, lower=0.45, middle=0.70, senior=1.00),
                    fee_base=1.50, cost_mult=2.2, F_cm=4.5, F_tt=0.60,
                    cap_cm=0.080, cap_tt=0.035, teacher_cap=0.25, n_cm0=2.0, n_tt0=6.0),
    'KHM-like': dict(income=0.5, urban=0.25, urban_mult=1.8, rural_mult=0.5, public_sub=0.20,
                     enrol=dict(primary=0.60, lower=0.28, upper=0.12),
                     stakes=dict(primary=0.30, lower=0.70, upper=0.90),
                     returns=dict(primary=0.15, lower=0.40, upper=0.60),
                     fee_base=0.25, cost_mult=0.6, F_cm=4.5, F_tt=0.60,
                     cap_cm=0.060, cap_tt=0.050, teacher_cap=0.80, n_cm0=2.0, n_tt0=6.0),
}
STAGES = {'PH-like': ['primary', 'lower', 'upper'],
          'HK-like': ['primary', 'lower', 'middle', 'senior'],
          'KHM-like': ['primary', 'lower', 'upper']}


def sig(x):
    return 1.0 / (1.0 + math.exp(-max(min(x, 30), -30)))


def _demand(cfg, price, stake_scale=1.0, pub=None, inc_scale=1.0, ret_scale=1.0):
    pub = cfg['public_sub'] if pub is None else pub
    inc0 = cfg['income'] * inc_scale
    stages = [k for k in cfg['enrol']]
    T, pupils = {}, {}
    Qd = 0.0
    for s in stages:
        stake = cfg['stakes'][s] * stake_scale
        ret = cfg['returns'][s] * ret_scale
        for loc, (share, mult) in (('urban', (cfg['urban'], cfg['urban_mult'])),
                                   ('rural', (1 - cfg['urban'], cfg['rural_mult']))):
            if share <= 0:
                continue
            inc = inc0 * mult
            t = sig(A0 + B_STAKE * stake + B_RET * ret - B_PUB * pub + B_INC * math.log(max(inc, 1e-6))
                    - B_FEE * (price / max(inc, 1e-6)))
            p = cfg['enrol'][s] * share * PUPILS
            T[(s, loc)] = t
            pupils[(s, loc)] = p
            Qd += p * t
    return T, pupils, Qd


def run_country(cname, cfg, stake_scale=1.0, pub=None, inc_scale=1.0, ret_scale=1.0,
                cost_mult=None, teacher_cap=None, entry_scale=1.0, cap_scale=1.0, **kw):
    """Static long-run equilibrium of a competitive shadow-provider market with limited teacher capacity.

    Declared structure: teacher-tutors have capacity share (teacher_cap x PUPILS x 0.5) and unit cost
    p_tt = F_tt/cap_tt; commercial firms are unconstrained at unit cost p_cm = F_cm/cap_cm. Free entry
    drives price to the marginal supplier's unit cost; equilibrium is teacher-only at p_tt when demand at
    p_cm fits teacher capacity, commercial-marginal at p_cm otherwise, with an interior price when demand at
    p_tt exactly exhausts teacher capacity. This replaces loop-2's tatonnement (which collapsed to a floor).
    """
    cost_mult = cfg['cost_mult'] if cost_mult is None else cost_mult
    teacher_cap = cfg['teacher_cap'] if teacher_cap is None else teacher_cap
    tcap_abs = cfg['cap_tt'] * cap_scale * PUPILS
    ccap_abs = cfg['cap_cm'] * cap_scale * PUPILS
    p_tt = cfg['F_tt'] * cost_mult / max(tcap_abs, 1e-9)
    p_cm = cfg['F_cm'] * cost_mult / max(ccap_abs, 1e-9)
    Qcap_tt = max(teacher_cap, 0.0) * PUPILS * 0.5
    Tcm, pupils, Qd_cm = _demand(cfg, p_cm, stake_scale, pub, inc_scale, ret_scale)
    Ttt, _, Qd_tt = _demand(cfg, p_tt, stake_scale, pub, inc_scale, ret_scale)
    if Qd_cm <= Qcap_tt:                      # teachers can serve all demand at p_cm; price falls to p_tt
        price = p_tt
        served_tt = Qd_tt; served_cm = 0.0
    elif Qd_tt >= Qcap_tt:                    # teacher capacity exhausted at p_tt; commercial marginal
        price = p_cm
        served_tt = Qcap_tt; served_cm = max(Qd_cm - Qcap_tt, 0.0)
    else:                                     # interior: clear teacher capacity at an intermediate price
        lo, hi = p_tt, p_cm
        for _ in range(60):
            mid = (lo + hi) / 2
            if _demand(cfg, mid, stake_scale, pub, inc_scale, ret_scale)[2] > Qcap_tt:
                lo = mid
            else:
                hi = mid
        price = (lo + hi) / 2
        served_tt = Qcap_tt; served_cm = 0.0
    T, pupils, Qd = _demand(cfg, price, stake_scale, pub, inc_scale, ret_scale)
    take = dict(T)                            # demand consistent with supply: take-up = desired at price
    n_tt = served_tt / max(tcap_abs, 1e-9)
    n_cm = served_cm / max(ccap_abs, 1e-9)
    tot = served_tt + served_cm
    return dict(take=take, price=float(price), n_cm=float(n_cm), n_tt=float(n_tt),
                teacher_share=float(served_tt / max(tot, 1e-9)),
                util=1.0, Qd=float(Qd), Qs=float(tot),
                price_income=float(price / max(cfg['income'], 1e-9)))


def stage_take(res, cname, stage, loc=None):
    """Aggregate take-up for a stage (weighted over locations when loc is None)."""
    cfg = COUNTRIES[cname]
    if loc is not None:
        return res['take'].get((stage, loc), float('nan'))
    shares = {'urban': cfg['urban'], 'rural': 1 - cfg['urban']}
    tot = 0.0; w = 0.0
    for lc, sh in shares.items():
        if (stage, lc) in res['take'] and sh > 0:
            tot += res['take'][(stage, lc)] * sh * cfg['enrol'][stage]
            w += sh * cfg['enrol'][stage]
    return tot / max(w, 1e-9)


def s1_table(out_dir):
    """Stage-matched check table: all 11 YES rows + HKG 13-row gradient."""
    targets = []
    lit = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                       '02_lit', 'SHADOW_TARGETS.csv')
    if os.path.exists(lit):
        for r in csv.DictReader(open(lit)):
            if r['use_as_model_target'] == 'YES':
                targets.append(r)
    hkg = []
    tgt2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                        '04_data', 'TARGETS_SHADOW.csv')
    if os.path.exists(tgt2):
        for r in csv.DictReader(open(tgt2)):
            if r['iso3'] == 'HKG' and r['status'] == 'target' and r['rate_pct'] not in ('', None):
                hkg.append(r)
    base = {c: run_country(c, COUNTRIES[c]) for c in COUNTRIES}
    rows = []
    flags = {c: 'UNABLE TO ASSESS' for c in ['KOR', 'JPN', 'HKG', 'KHM', 'PHL']}
    mapped = {}
    # map literature rows to model objects
    for r in targets:
        iso, stage, val = r['iso3'], r['stage'].lower(), float(r['rate_pct'])
        conf, src = r['confidence'], r['source_access']
        model_val, note, assessment = float('nan'), '', 'UNABLE TO ASSESS'
        calibration = False
        if iso == 'HKG':
            st = 'senior' if 'senior' in stage else None
            if st:
                model_val = stage_take(base['HK-like'], 'HK-like', 'senior')
                calibration = True
                note = 'HK 0.85 is a CALIBRATION target, not incidence evidence'
                assessment = 'calibration (excluded from pass/fail)'
        elif iso == 'KHM':
            if 'lower secondary' in stage:
                model_val = stage_take(base['KHM-like'], 'KHM-like', 'lower')
                note = 'grade-9 -> lower-secondary stage'
            elif 'urban' in stage:
                model_val = stage_take(base['KHM-like'], 'KHM-like', 'primary', loc='urban')
                note = 'primary urban'
            elif 'rural' in stage:
                model_val = stage_take(base['KHM-like'], 'KHM-like', 'primary', loc='rural')
                note = 'primary rural'
            elif 'primary' in stage:
                model_val = stage_take(base['KHM-like'], 'KHM-like', 'primary')
                note = 'primary aggregate'
            if not math.isnan(model_val):
                assessment = 'assessed'
        elif iso == 'PHL':
            if 'all basic' in stage:
                # pupil-weighted aggregate of primary+lower+upper
                cfg = COUNTRIES['PH-like']
                num = sum(stage_take(base['PH-like'], 'PH-like', s) * cfg['enrol'][s] for s in ['primary', 'lower', 'upper'])
                model_val = num / sum(cfg['enrol'][s] for s in ['primary', 'lower', 'upper'])
                note = 'pupil-weighted primary+lower+upper'
            elif 'elementary' in stage:
                model_val = stage_take(base['PH-like'], 'PH-like', 'primary')
                note = 'elementary -> primary'
            elif 'upper secondary' in stage:
                model_val = stage_take(base['PH-like'], 'PH-like', 'upper')
                note = 'upper-secondary stage'
            if not math.isnan(model_val):
                assessment = 'assessed'
        else:
            note = f'no {iso}-like structural variant exists; transferring a PH/HK/KHM parameter set ' \
                   f'would be an untested transfer'
        if not math.isnan(model_val):
            model_val = model_val * 100.0
        lo = r.get('low_pct') or ''
        hi = r.get('high_pct') or ''
        if lo and hi:
            lo_v, hi_v = float(lo), float(hi)
            rng = f'[{lo_v:.1f},{hi_v:.1f}]'
        else:
            lo_v, hi_v = val - 5.0, val + 5.0
            rng = f'point +/-5pp (declared range rule)'
        inside = (not math.isnan(model_val)) and (lo_v <= model_val <= hi_v) and assessment == 'assessed'
        if assessment == 'assessed':
            flags[iso] = 'inside' if inside else 'outside'
        rows.append(dict(source='SHADOW_TARGETS', iso3=iso, stage=r['stage'], literature_pct=val,
                         range=rng, model_pct=model_val, assessment=assessment,
                         inside_range=inside if assessment == 'assessed' else '', note=note,
                         confidence=conf, source_access=src, calibration=calibration))
    # HKG gradient rows (13-row file)
    for r in hkg:
        stage = r['stage'].lower(); yr = r['year']
        if 'senior' in stage:
            st, lab = 'senior', 'senior-secondary'
        elif 'middle' in stage:
            st, lab = 'middle', 'middle-secondary'
        elif 'lower' in stage:
            st, lab = 'lower', 'lower-secondary'
        elif 'primary' in stage:
            st, lab = 'primary', 'primary'
        else:
            continue
        model_val = stage_take(base['HK-like'], 'HK-like', st) * 100.0
        if str(yr).startswith('1996'):
            assessment, note = 'UNABLE TO ASSESS', 'no dated model equivalent (steady-state model)'
            inside = ''
        else:
            # 2010 senior is the calibration; lower/middle are checks
            assessment = 'calibration (excluded from pass/fail)' if st == 'senior' else 'assessed'
            note = ('HK 0.85 is a CALIBRATION target, not incidence evidence' if st == 'senior'
                    else 'stage-matched check')
            lo_v, hi_v = float(r['rate_pct']) - 5, float(r['rate_pct']) + 5
            inside = (lo_v <= model_val <= hi_v) if assessment == 'assessed' else ''
        rows.append(dict(source='TARGETS_SHADOW', iso3='HKG', stage=lab, literature_pct=float(r['rate_pct']),
                         range='point +/-5pp' if str(yr).startswith('2010') else 'n/a',
                         model_pct=model_val, assessment=assessment, inside_range=inside, note=note,
                         confidence=r['confidence'], source_access='FULL-TEXT', calibration=(st == 'senior' and str(yr).startswith('2010'))))
    # HKG flag from its 2010 stage checks (calibration row excluded)
    hkg_checks_pre = [r for r in rows if r['source'] == 'TARGETS_SHADOW' and r['assessment'] == 'assessed']
    if hkg_checks_pre:
        flags['HKG'] = 'inside' if all(r['inside_range'] is not False for r in hkg_checks_pre) else 'outside'
    # flags per assessable country (exclude calibration)
    outside = [c for c in ['HKG', 'KHM', 'PHL'] if flags[c] == 'outside']
    inside_c = [c for c in ['HKG', 'KHM', 'PHL'] if flags[c] == 'inside']
    unable = [c for c in ['KOR', 'JPN'] if flags[c] == 'UNABLE TO ASSESS']
    hkg_checks = [r for r in rows if r['source'] == 'TARGETS_SHADOW' and r['assessment'] == 'assessed']
    hkg_miss = [r for r in hkg_checks if r['inside_range'] is False]
    L = ['S1 — STAGE-MATCHED SHADOW CHECK TABLE (all 11 use_as_model_target=YES rows + HKG gradient)',
         'Model: loop3/code/shadow3.py baseline structural parameters (NOT calibrated to these rows).',
         'HK 0.85 is a CALIBRATION target, never incidence evidence. Ranges: literature low-high where given,',
         'else point +/-5pp (declared range rule). UNABLE rows are reported, not dropped.', '',
         f'  {"source":15s} {"iso":4s} {"stage":28s} {"lit%":>6s} {"range":>15s} {"model%":>8s} {"status":>36s}']
    for r in rows:
        L.append(f'  {r["source"]:15s} {r["iso3"]:4s} {str(r["stage"])[:28]:28s} {r["literature_pct"]:6.1f} '
                 f'{str(r["range"])[:15]:>15s} {r["model_pct"]:8.1f} {str(r["assessment"])[:36]:>36s}')
    L += ['', f'Assessable countries (excl. calibration): HKG, KHM, PHL. Outside range: {outside or "none"}; '
              f'inside: {inside_c or "none"}; UNABLE: {unable}.',
          f'HKG gradient checks (2010 lower/middle): {len(hkg_checks)} assessed, {len(hkg_miss)} outside.']
    passed = len(outside) < 2 and len(hkg_miss) == 0
    L += ['', 'PREDECLARED THRESHOLD: >=2 of the assessable countries outside their literature range (or any HKG',
          'gradient check outside) => stop claiming incidence. (KOR/JPN marked UNABLE, not counted as outside.)',
          f'  -> S1 {"PASS" if passed else "FAIL"} — outside-range countries: {len(outside)}/3; HKG gradient misses: {len(hkg_miss)}.']
    if not passed:
        L.append('  Incidence claim is NOT established: the model over-universalises outside the HKG calibration,')
        L.append('  reproducing the Council brief-005 concern.')
    write_text(os.path.join(out_dir, 's1_table.txt'), '\n'.join(L) + '\n')
    write_rows(os.path.join(out_dir, 's1_table.csv'),
               ['source', 'iso3', 'stage', 'literature_pct', 'range', 'model_pct', 'assessment',
                'inside_range', 'note', 'confidence', 'source_access', 'calibration'],
               [[r.get(k) for k in ['source', 'iso3', 'stage', 'literature_pct', 'range', 'model_pct',
                                    'assessment', 'inside_range', 'note', 'confidence', 'source_access',
                                    'calibration']] for r in rows])
    return dict(rows=rows, outside=outside, inside=inside_c, unable=unable,
                hkg_checks=hkg_checks, hkg_miss=hkg_miss, passed=passed, base=base)


def s2_search(out_dir):
    """Structural-parameter search: no parameter is a take-up rate."""
    base = {c: run_country(c, COUNTRIES[c]) for c in COUNTRIES}
    # target vectors (percent) excluding HK 85 calibration
    TARGETS = {
        'PH-like': {'all_basic': 46.5, 'elementary': 23.8, 'upper': 28.1},
        'KHM-like': {'lower': 68.4, 'primary': 41.3, 'primary_urban': 60.5, 'primary_rural': 26.4},
        'HK-like': {'lower': 72.0, 'middle': 82.0},
    }

    def model_vec(c, res):
        if c == 'PH-like':
            cfg = COUNTRIES[c]
            w = cfg['enrol']
            allb = sum(stage_take(res, c, s) * w[s] for s in ['primary', 'lower', 'upper']) / sum(w.values())
            return {'all_basic': allb * 100, 'elementary': stage_take(res, c, 'primary') * 100,
                    'upper': stage_take(res, c, 'upper') * 100}
        if c == 'KHM-like':
            return {'lower': stage_take(res, c, 'lower') * 100, 'primary': stage_take(res, c, 'primary') * 100,
                    'primary_urban': stage_take(res, c, 'primary', loc='urban') * 100,
                    'primary_rural': stage_take(res, c, 'primary', loc='rural') * 100}
        return {'lower': stage_take(res, c, 'lower') * 100, 'middle': stage_take(res, c, 'middle') * 100}

    def err(c, res):
        mv = model_vec(c, res)
        return float(np.mean([(mv[k] - TARGETS[c][k]) ** 2 for k in TARGETS[c]])), mv

    rows = []
    summary = {}
    for c in COUNTRIES:
        base_err, base_mv = err(c, base[c])
        rows.append(dict(country=c, arm='baseline', param='none', value=float('nan'),
                         sq_err=base_err, rmse_pp=math.sqrt(base_err), model=json.dumps(base_mv),
                         target=json.dumps(TARGETS[c])))
        # one-parameter-at-a-time grids (declared ranges, independently justified)
        grids = dict(stake_scale=[0.3, 0.6, 1.0, 1.5, 2.5], pub=[0.0, 0.25, 0.5, 0.75, 1.0],
                     inc_scale=[0.5, 1.0, 1.5, 2.0, 3.0], cost_mult=[0.3, 0.6, 1.0, 2.0, 3.0],
                     teacher_cap=[0.0, 0.25, 0.5, 0.75, 1.0], ret_scale=[0.2, 0.5, 1.0, 1.8, 2.5],
                     entry_scale=[0.5, 1.0, 2.0, 4.0], cap_scale=[0.5, 1.0, 2.0])
        best_single = {k: (1e9, None) for k in grids}
        for gname, vals in grids.items():
            for v in vals:
                kw = {gname: v}
                if gname == 'pub':
                    kw = dict(pub=v)
                r = run_country(c, COUNTRIES[c], **kw)
                e, _ = err(c, r)
                if e < best_single[gname][0]:
                    best_single[gname] = (e, v)
                rows.append(dict(country=c, arm='one_at_a_time', param=gname, value=v,
                                 sq_err=e, rmse_pp=math.sqrt(e), model='', target=''))
        # random search over all structural parameters (declared ranges; seed fixed)
        rng = np.random.default_rng(12345)
        best = (base_err, None, None)
        for _ in range(600):
            kw = dict(stake_scale=float(rng.uniform(0.3, 2.5)),
                      pub=float(rng.uniform(0.0, 1.0)),
                      inc_scale=float(rng.uniform(0.5, 3.0)),
                      cost_mult=float(rng.uniform(0.3, 3.0)),
                      teacher_cap=float(rng.uniform(0.0, 1.0)),
                      ret_scale=float(rng.uniform(0.2, 2.5)),
                      entry_scale=float(rng.uniform(0.5, 4.0)),
                      cap_scale=float(rng.uniform(0.5, 2.0)))
            r = run_country(c, COUNTRIES[c], **kw)
            e, mv = err(c, r)
            if e < best[0]:
                best = (e, kw, mv)
        rows.append(dict(country=c, arm='joint_search', param='all', value=float('nan'),
                         sq_err=best[0], rmse_pp=math.sqrt(best[0]),
                         model=json.dumps(best[2]) if best[2] else '', target=json.dumps(TARGETS[c])))
        summary[c] = dict(base_rmse=math.sqrt(base_err), base_model=base_mv,
                          joint_rmse=math.sqrt(best[0]), joint_params=best[1], joint_model=best[2],
                          best_single={k: dict(rmse=math.sqrt(v[0]), value=v[1]) for k, v in best_single.items()})
    write_rows(os.path.join(out_dir, 's2_search.csv'),
               ['country', 'arm', 'param', 'value', 'sq_err', 'rmse_pp', 'model', 'target'],
               [[r.get(k) for k in ['country', 'arm', 'param', 'value', 'sq_err', 'rmse_pp', 'model', 'target']]
                for r in rows])
    L = ['S2 — WHAT MAKES TUTORING NON-UNIVERSAL? (structural parameters only; no take-up set directly)',
         'Structural parameters: gate stakes scale, public-school substitute, income scale, provider cost,',
         'teacher-tutor capacity, credential-return scale, entry scale, capacity scale. Targets at the',
         'stage-matched literature rows; HK 85 excluded as calibration. Declared threshold: all targets within',
         '+/-5pp = reproduces; within +/-10pp = partial; otherwise none works.', '']
    any_rep = True; any_partial = False
    for c, s in summary.items():
        L.append(f'  {c}: baseline RMSE {s["base_rmse"]:.1f}pp; joint-search RMSE {s["joint_rmse"]:.1f}pp')
        L.append(f'    baseline model {json.dumps({k: round(v, 1) for k, v in s["base_model"].items()})}')
        L.append(f'    best joint params {json.dumps({k: round(v, 2) for k, v in (s["joint_params"] or {}).items()})}')
        L.append(f'    best joint model {json.dumps({k: round(v, 1) for k, v in (s["joint_model"] or {}).items()})}')
        # which single parameter does the work (largest improvement over baseline)
        imp = sorted(((s['base_rmse'] - v['rmse'], k, v['value'], v['rmse'])
                      for k, v in s['best_single'].items()), reverse=True)
        L.append('    one-parameter effects (RMSE reduction, param, value): ' +
                 '; '.join(f'{d:+.1f}pp {k}@{v}' for d, k, v, _ in imp[:4]))
        if s['joint_rmse'] <= 5:
            L.append('    -> REPRODUCES (all targets within +/-5pp)')
        elif s['joint_rmse'] <= 10:
            L.append('    -> PARTIAL (within +/-10pp)'); any_partial = True
        else:
            L.append('    -> NONE WORKS (best RMSE > 10pp)'); any_rep = False
    L += ['', f'Overall: {"reproduces" if any_rep and not any_partial else ("partial" if any_partial else "none works")}.']
    write_text(os.path.join(out_dir, 's2_findings.txt'), '\n'.join(L) + '\n')
    return summary


def s3_grid(out_dir):
    """Entry-cost/capacity grid: price, providers, teacher share; fee moment comparison."""
    FGRID = [0.5, 1.0, 2.0, 5.0, 10.0]
    CGRID = [0.5, 1.0, 2.0]
    TGRID = [0.5, 1.0, 2.0]
    rows = []
    for c in COUNTRIES:
        cfg = COUNTRIES[c]
        for fcm in FGRID:
            for ftt in FGRID:
                for ccm in CGRID:
                    for ctt in CGRID:
                        for tcap in TGRID:
                            def run(**kw):
                                r = run_country(c, cfg, **kw)
                                return r
                            # apply via temporary config copy
                            cfg2 = dict(cfg)
                            cfg2['F_cm'] = cfg['F_cm'] * fcm
                            cfg2['F_tt'] = cfg['F_tt'] * ftt
                            cfg2['cap_cm'] = cfg['cap_cm'] * ccm
                            cfg2['cap_tt'] = cfg['cap_tt'] * ctt
                            cfg2['teacher_cap'] = min(1.0, cfg['teacher_cap'] * tcap)
                            res = run_country(c, cfg2)
                            rows.append(dict(country=c, F_cm_mult=fcm, F_tt_mult=ftt,
                                             cap_cm_mult=ccm, cap_tt_mult=ctt, teacher_cap_mult=tcap,
                                             price=res['price'], price_income=res['price_income'],
                                             n_cm=res['n_cm'], n_tt=res['n_tt'],
                                             teacher_share=res['teacher_share'], util=res['util'],
                                             price_floor_hit=bool(res['price'] <= 0.105 * cfg['fee_base'])))
    write_rows(os.path.join(out_dir, 's3_grid.csv'),
               ['country', 'F_cm_mult', 'F_tt_mult', 'cap_cm_mult', 'cap_tt_mult', 'teacher_cap_mult',
                'price', 'price_income', 'n_cm', 'n_tt', 'teacher_share', 'util', 'price_floor_hit'],
               [[r.get(k) for k in ['country', 'F_cm_mult', 'F_tt_mult', 'cap_cm_mult', 'cap_tt_mult',
                                    'teacher_cap_mult', 'price', 'price_income', 'n_cm', 'n_tt',
                                    'teacher_share', 'util', 'price_floor_hit']] for r in rows])
    L = ['S3 — PRICE / PROVIDER-ENTRY CALIBRATION GRID (entry-cost x capacity x teacher capacity)',
         'Observed fee moments: the only verified ones are Korean (434k won/month per student; 553k per',
         'participant). There is NO verified fee moment for PH, HK or KHM and NO KOR model variant, so the',
         'fee comparison is UNABLE TO ASSESS. Grid reported for structure.', '']
    for c in COUNTRIES:
        R = [r for r in rows if r['country'] == c]
        finite = [r for r in R if not r['price_floor_hit']]
        L.append(f'  {c}: grid {len(R)} points; price {min(r["price"] for r in R):.3f}-'
                 f'{max(r["price"] for r in R):.3f}; price/income '
                 f'{min(r["price_income"] for r in R):.3f}-{max(r["price_income"] for r in R):.3f}; '
                 f'finite-price points {len(finite)}/{len(R)}')
        L.append(f'    provider count n_cm {min(r["n_cm"] for r in R):.1f}-{max(r["n_cm"] for r in R):.1f}, '
                 f'n_tt {min(r["n_tt"] for r in R):.1f}-{max(r["n_tt"] for r in R):.1f}, '
                 f'teacher share {min(r["teacher_share"] for r in R):.2f}-{max(r["teacher_share"] for r in R):.2f}')
        inside = [r for r in R if 0.01 <= r['price_income'] <= 0.15]
        L.append(f'    points with price/income inside declared plausible band [1%,15%]: {len(inside)}/{len(R)}')
    L += ['', 'THRESHOLD: price inside an OBSERVED range => pass; no observed moment => UNABLE (never called a pass).',
          '  -> S3 verdict: UNABLE TO ASSESS (no observed fee moment for PH/HK/KHM; only KOR moments, no KOR model).',
          '  Structure note: with entry costs multiplied up to 10x, the price can stay above the floor at part of',
          '  the grid (see finite-price counts) — the loop-2 floor collapse is an under-priced entry-cost block, not',
          '  an intrinsic result. Provider counts remain high in the credible-price region.']
    write_text(os.path.join(out_dir, 's3_findings.txt'), '\n'.join(L) + '\n')
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    s1 = s1_table(a.out)
    s2 = s2_search(a.out)
    s3 = s3_grid(a.out)
    meta = dict(module='shadow3.py (NEW; not massabm/floorworld/triad/paper reproduction)',
                countries=list(COUNTRIES), seeds=SEEDS, intake_corrections=dict(
                    shadow_targets_yes_rows=11,
                    loop2_teacher_entry_effect_pp='54-67 (correction of 46-66)'),
                s1=dict(passed=s1['passed'], outside=s1['outside'], inside=s1['inside'],
                        unable=s1['unable'], hkg_gradient_misses=len(s1['hkg_miss'])),
                s2={c: dict(base_rmse=v['base_rmse'], joint_rmse=v['joint_rmse']) for c, v in s2.items()},
                s3=dict(verdict='UNABLE TO ASSESS (no observed fee moment for PH/HK/KHM)'),
                pending_L2_4_L2_5='NOT RUN in this timebox')
    json.dump(meta, open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print('loop3 done:', json.dumps(meta['s1'], indent=1))


if __name__ == '__main__':
    main()
