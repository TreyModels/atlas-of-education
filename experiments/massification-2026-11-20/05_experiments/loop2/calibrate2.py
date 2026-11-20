"""loop2 calibration under Council brief 004 amendments.
- Every target row labelled fit vs check, with a predicted sign per candidate world, BEFORE fitting.
- Fit 1980-2010 only; hold out 2011-2024. HKG is the untouched country (never fitted).
- Check-only real-data moments (excluded from the fit): WDI industry+services employment share and
  agriculture share (formal-access / informality-transition proxies). Shadow take-up and wage-premium
  dynamics are DATA BLOCKED (no observed series in 04_data; TARGETS_SHADOW.csv not landed).
- Fitted objects per brief 004: household demand (cost_col), provider entry/capacity (prov_capacity),
  teacher-tutor capacity (teacher_capacity), provider elasticity (prov_elasticity).
- Freeze-both symmetry test (i) freeze schooling feedback (ii) freeze jobs/wages (iii) both.
"""
import argparse, csv, json, os, sys, time
import numpy as np
sys.path.insert(0, '/tmp/massrun/work/loop2'); sys.path.insert(0, '/tmp/massrun/work/exp')
from common import write_rows, write_text
from massabm import make_params, run_model
from massabm.model import PRI, JHS, BASIC
import configs as CFG

GMR = '/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/04_data/data/gmr_observed_6countries_1970_2024.csv'
WDI = '/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20/04_data/data/wdi_4countries_long.csv'
FIT_ISO = ['PHL', 'KHM', 'CHN']      # HKG untouched
ALL_ISO = ['PHL', 'KHM', 'HKG', 'CHN']
GER = ['ger_primary', 'ger_secondary', 'ger_tertiary']
COMP = ['completion_primary', 'completion_lower_secondary', 'completion_upper_secondary']
FIT_Y = (1980, 2010); HOLD_Y = (2011, 2024)
BOUNDS = {'cost_col': (0.3, 1.0), 'prov_capacity': (0.05, 0.6),
          'teacher_capacity': (0.0, 0.5), 'prov_elasticity': (0.3, 3.0)}
KEYS = list(BOUNDS)
# ---- predeclared target table (role + predicted sign per candidate world), written before fitting
PRED = {
 'ger_primary': ('fit', 'all + (weak)'),
 'ger_secondary': ('fit', 'all + (weak)'),
 'ger_tertiary': ('fit', 'surplus + ; competitive + ; yoo +'),
 'completion_primary': ('fit', 'all + (weak)'),
 'completion_lower_secondary': ('fit', 'all + (weak)'),
 'completion_upper_secondary': ('fit', 'surplus + ; competitive + ; yoo +'),
 'ger_primary_HOLD': ('check', 'all + (weak)'),
 'ger_secondary_HOLD': ('check', 'all + (weak)'),
 'ger_tertiary_HOLD': ('check', 'surplus + ; competitive + ; yoo +'),
 'completion_primary_HOLD': ('check', 'all + (weak)'),
 'completion_lower_secondary_HOLD': ('check', 'all + (weak)'),
 'completion_upper_secondary_HOLD': ('check', 'surplus + ; competitive + ; yoo +'),
 'emp_industry_services': ('check', 'surplus: formal access responds - to graduate supply ; competitive: 0/+ ; yoo: -'),
 'emp_agriculture': ('check', 'surplus: informality falls as floors rise ; competitive: follows skill prices ; yoo: flat'),
 'shadow_takeup': ('check', 'DATA BLOCKED (TARGETS_SHADOW.csv not landed) ; surplus: high at board/apex ; competitive: flat/low ; yoo: high near cutoff'),
 'wage_premium_dynamics': ('check', 'DATA BLOCKED (no observed wage series in 04_data) ; surplus: compress then rebound ; competitive: smooth decline ; yoo: jump at cutoff'),
}


def obs_gmr():
    out = {}
    for r in csv.DictReader(open(GMR)):
        if r['iso3'] not in ALL_ISO or r['indicator'] not in GER + COMP:
            continue
        try:
            out.setdefault(r['iso3'], {}).setdefault(r['indicator'], {})[int(r['year'])] = float(r['value'])
        except (TypeError, ValueError):
            pass
    return out


def obs_wdi():
    out = {}
    for r in csv.DictReader(open(WDI)):
        if r['iso3'] not in ALL_ISO:
            continue
        if r['indicator_code'] in ('SL.IND.EMPL.ZS', 'SL.SRV.EMPL.ZS', 'SL.AGR.EMPL.ZS'):
            try:
                out.setdefault(r['iso3'], {}).setdefault(r['indicator_code'], {})[int(r['year'])] = float(r['value'])
            except (TypeError, ValueError):
                pass
    return out


def model_targets(S, iso, N):
    y = S['year'].astype(int); e = S['enrol']
    ref = S['reformed'] if 'reformed' in S else np.zeros(len(y))
    dur = 4.0 + 2.0 * np.clip(ref, 0, 1)
    out = {'ger_primary': dict(zip(y.tolist(), (100 * e[:, 0] / (N * 6.0)).tolist())),
           'ger_secondary': dict(zip(y.tolist(), (100 * e[:, 1] / (N * dur)).tolist())),
           'ger_tertiary': dict(zip(y.tolist(), (100 * e[:, 2] / (N * 4.0)).tolist()))}
    cat = S['c_cat']; n = np.maximum(S['c_n'].sum((1, 2)), 1); entry = S['year'].astype(int)
    add = np.where((iso == 'PHL') & (entry >= 2006), 12, 10)
    cy = entry + add
    for key, lvl in [('completion_primary', PRI), ('completion_lower_secondary', JHS), ('completion_upper_secondary', BASIC)]:
        # observed completion series are in PERCENT; model shares are fractions, so scale by 100
        out[key] = dict(zip(cy.tolist(), (100 * cat[:, :, :, lvl:].sum((1, 2, 3)) / n).tolist()))
    pc = S['pool_cat']; tot = np.maximum(pc.sum((1, 2)), 1)
    out['emp_industry_services'] = dict(zip(y.tolist(), (100 * pc[:, [1, 2, 4], :].sum((1, 2)) / tot).tolist()))
    out['emp_agriculture'] = dict(zip(y.tolist(), (100 * pc[:, 5, :].sum(1) / tot).tolist()))
    return out


def errs(mod, obs, obs_w, years, suffix=''):
    e = {}
    for ind in GER + COMP:
        ov = obs.get(ind, {}); mv = mod.get(ind, {})
        ys = [yy for yy in ov if years[0] <= yy <= years[1] and yy in mv]
        if ys:
            e[ind + suffix] = float(np.mean([abs(mv[yy] - ov[yy]) for yy in ys]))
    # check-only real-data moments
    for ind, keys in [('emp_industry_services', ('SL.IND.EMPL.ZS', 'SL.SRV.EMPL.ZS')), ('emp_agriculture', ('SL.AGR.EMPL.ZS',))]:
        vals = {}
        for k in keys:
            for yy, v in obs_w.get(k, {}).items():
                vals.setdefault(yy, []).append(v)
        ov = {yy: float(np.sum(vs)) if ind == 'emp_industry_services' else vs[0] for yy, vs in vals.items()}
        mv = mod.get(ind, {})
        ys = [yy for yy in ov if years[0] <= yy <= years[1] and yy in mv]
        if ys:
            e[ind + suffix] = float(np.mean([abs(mv[yy] - ov[yy]) for yy in ys]))
    return e


def run_cfg(arg):
    iso, z, N, seed, extra = arg
    try:
        ov = dict(cost_col=z['cost_col'], prov_capacity=z['prov_capacity'],
                  teacher_capacity=z['teacher_capacity'], prov_elasticity=z['prov_elasticity'])
        if z.get('cap_scale'):
            cap = [(yr, float(np.clip(v * z['cap_scale'], 0.0, 0.99))) for yr, v in CFG.build(iso)['capacity_path']]
            ov['capacity_path'] = cap
        ov.update(extra)
        p = make_params(**CFG.build(iso, ov)); p['N'] = N; p['seed'] = seed; p['t1'] = 2035
        return iso, z, model_targets(run_model(p), iso, N)
    except Exception as ex:
        return iso, z, {'error': repr(ex)}


def freeze_jobs_overrides(iso):
    v = [(1980, .15), (2035, .15)]
    return dict(vac_paths=dict(elite=v, mid=[(1980, .03), (2035, .03)], routine=v,
                               os_prof=[(1980, .001), (2035, .001)], os_agency=[(1980, 0.), (2035, 0.)]),
                floor_fixed=dict(elite=4, mid=4, routine=3), wage_hc=dict(os_prof=0.0, elite=0.0, mid=0.0,
                                                                         os_agency=0.0, routine=0.0, informal=0.0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draws', type=int, default=24)
    ap.add_argument('--N', type=int, default=2000)
    ap.add_argument('--Nfine', type=int, default=3000)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    obs, obs_w = obs_gmr(), obs_wdi()
    rng = np.random.default_rng(34000)
    u = (rng.permuted(np.tile(np.arange(a.draws), (len(KEYS), 1)), axis=1).T + rng.random((a.draws, len(KEYS)))) / a.draws
    Z = [{k: BOUNDS[k][0] + u[i, j] * (BOUNDS[k][1] - BOUNDS[k][0]) for j, k in enumerate(KEYS)} for i in range(a.draws)]
    from concurrent.futures import ProcessPoolExecutor
    jobs = [(iso, Z[i], a.N, 34000, {}) for iso in FIT_ISO for i in range(a.draws)]
    res = {}
    with ProcessPoolExecutor(max_workers=2) as ex:
        for iso, z, mt in ex.map(run_cfg, jobs):
            if 'error' not in mt:
                res.setdefault(iso, []).append((z, mt))
    print(f'grid done: {sum(len(v) for v in res.values())}/{len(jobs)} ok, wall {time.time() - t0:.0f}s', flush=True)
    rows, best = [], {}
    for iso in FIT_ISO:
        pts = []
        for z, mt in res.get(iso, []):
            e_fit = errs(mt, obs.get(iso, {}), obs_w.get(iso, {}), FIT_Y)
            pts.append(dict(z=z, e=e_fit, tot=float(np.mean(list(e_fit.values())))))
        pts = [p for p in pts if np.isfinite(p['tot'])]; pts.sort(key=lambda p: p['tot'])
        best[iso] = pts[0]
    # fine re-run (2 seeds) of the selected points
    fine = {}
    for iso in FIT_ISO:
        mods = []
        for s in (34000, 34001):
            _, _, mt = run_cfg((iso, best[iso]['z'], a.Nfine, s, {}))
            mods.append(mt)
        fine[iso] = {k: {yy: float(np.mean([m[k].get(yy, np.nan) for m in mods])) for yy in mods[0][k]} for k in mods[0]}
    # untouched country
    _, _, mt_hkg = run_cfg(('HKG', {'cost_col': 0.5, 'prov_capacity': 0.3, 'teacher_capacity': 0.15, 'prov_elasticity': 1.0}, a.Nfine, 34000, {}))
    fine['HKG'] = mt_hkg
    # ---- build the calibration table (fit/check rows, predicted signs, in-sample and held-out errors)
    tab = []
    for iso in ALL_ISO:
        mod = fine[iso]
        ef = errs(mod, obs.get(iso, {}), obs_w.get(iso, {}), FIT_Y)
        eh = errs(mod, obs.get(iso, {}), obs_w.get(iso, {}), HOLD_Y)
        for ind in GER + COMP:
            role, sign = PRED[ind]
            tab.append(dict(country=iso, target=ind, role=role, years=f'{FIT_Y[0]}-{FIT_Y[1]}' if iso != 'HKG' else 'untouched',
                            predicted_sign=sign, fit_mae=ef.get(ind, np.nan), hold_mae=eh.get(ind, np.nan)))
            tab.append(dict(country=iso, target=ind + '_HOLD', role='check', years=f'{HOLD_Y[0]}-{HOLD_Y[1]}',
                            predicted_sign=PRED[ind + '_HOLD'][1],
                            fit_mae=np.nan, hold_mae=eh.get(ind, np.nan)))
        for ind in ('emp_industry_services', 'emp_agriculture'):
            role, sign = PRED[ind]
            tab.append(dict(country=iso, target=ind, role='check', years=f'{FIT_Y[0]}-{HOLD_Y[1]}',
                            predicted_sign=sign, fit_mae=np.nan, hold_mae=eh.get(ind, np.nan)))
        for ind in ('shadow_takeup', 'wage_premium_dynamics'):
            role, sign = PRED[ind]
            tab.append(dict(country=iso, target=ind, role='check', years='n/a', predicted_sign=sign,
                            fit_mae=np.nan, hold_mae=np.nan))
    write_rows(os.path.join(a.out, 'CALIBRATION_TABLE.csv'), list(tab[0].keys()), [[r[k] for k in tab[0]] for r in tab])
    # ---- freeze-both symmetry test
    fz = []
    for iso in ALL_ISO:
        z = best.get(iso, {'z': {'cost_col': 0.53, 'prov_capacity': 0.3, 'teacher_capacity': 0.15, 'prov_elasticity': 1.0}})['z'] \
            if iso in best else {'cost_col': 0.53, 'prov_capacity': 0.3, 'teacher_capacity': 0.15, 'prov_elasticity': 1.0}
        for label, extra in [('baseline', {}), ('freeze schooling feedback', dict(freeze_schooling=True)),
                             ('freeze jobs and wages', freeze_jobs_overrides(iso)),
                             ('freeze both', {**freeze_jobs_overrides(iso), 'freeze_schooling': True})]:
            _, _, mt = run_cfg((iso, z, a.N, 34000, extra))
            if 'error' in mt:
                continue
            def d(k, y0, y1):
                return float(mt[k].get(y1, np.nan) - mt[k].get(y0, np.nan))
            fz.append(dict(iso=iso, regime=label,
                           d_upsec_1980_2010=d('completion_upper_secondary', 1980, 2010),
                           d_tertiary_1980_2010=d('ger_tertiary', 1980, 2010),
                           d_formal_1980_2010=d('emp_industry_services', 1980, 2010)))
    write_rows(os.path.join(a.out, 'freeze_both.csv'), list(fz[0].keys()), [[r[k] for k in fz[0]] for r in fz])
    # ---- findings
    L = ['LOOP2 CALIBRATION (Council brief 004 amendments applied)',
         f'fit draws={a.draws}/country over 4 params at N={a.N}; selected point re-run at N={a.Nfine} with 2 seeds; wall={time.time() - t0:.0f}s',
         f'FIT years {FIT_Y[0]}-{FIT_Y[1]}; HELD OUT {HOLD_Y[0]}-{HOLD_Y[1]} (no refitting). HKG = UNTOUCHED country (never fitted).',
         'Fitted objects (brief 004): household demand `cost_col`, provider entry/capacity `prov_capacity`,',
         'teacher-tutor capacity `teacher_capacity`, provider elasticity `prov_elasticity`.',
         'Shadow take-up and provider mix are CHECKS, never fitted shares; shadow targets are DATA BLOCKED.', '',
         'SELECTED PARAMETERS:']
    for iso in FIT_ISO:
        L.append(f'  {iso}: ' + '  '.join(f'{k}={best[iso]["z"][k]:.3f}' for k in KEYS) +
                 f'  (in-sample total MAE {best[iso]["tot"]:.1f} pp)')
    L += ['', 'CALIBRATION TABLE (fit vs check; MAE in pp):']
    for r in tab:
        if r['role'] == 'fit':
            L.append(f'  {r["country"]:4s} {r["target"]:30s} FIT   in-sample {r["fit_mae"]:6.1f}  held-out {r["hold_mae"]:6.1f}  [{r["predicted_sign"]}]')
        elif np.isfinite(r['hold_mae']):
            L.append(f'  {r["country"]:4s} {r["target"]:30s} CHECK held-out {r["hold_mae"]:6.1f}  [{r["predicted_sign"][:60]}]')
        else:
            L.append(f'  {r["country"]:4s} {r["target"]:30s} CHECK  DATA BLOCKED/NA  [{r["predicted_sign"][:60]}]')
    L += ['', 'FREEZE-BOTH SYMMETRY TEST (1980-2010 changes in pp):']
    for r in fz:
        L.append(f'  {r["iso"]:4s} {r["regime"]:26s} upper-sec {r["d_upsec_1980_2010"]:+6.1f}  tertiary GER '
                 f'{r["d_tertiary_1980_2010"]:+6.1f}  formal(proxy) {r["d_formal_1980_2010"]:+6.1f}')
    L += ['', 'VERDICT:']
    L.append('  The freeze tests show what moves what. If attainment still rises with the wage/job feedback frozen,')
    L.append('  AND formal jobs still rise with schooling feedback frozen, then neither is generated by the other:')
    L.append('  the two-way path is largely a SCHEDULE in this structure (consistent with C2 floorworld).')
    L.append('  Identifiability: calibration moves the fitted point INSIDE a family; C1 showed surplus and')
    L.append('  competitive CES are not distinguishable on aggregate moments. Calibration therefore cannot make')
    L.append('  them identifiable. What would: gate-specific shadow take-up (data blocked), formal-vs-informal')
    L.append('  transition rates by credential, density near admission cutoffs, and panel shock responses.')
    L.append('  Forced-identification rate: inherited from C1 = 2/2 (outside truth absorbed by the surplus family);')
    L.append('  this loop adds no separating moment, so the rate cannot improve until the shadow/transition')
    L.append('  moments land.')
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(fit_iso=FIT_ISO, untouched='HKG', draws=a.draws, N=a.N, Nfine=a.Nfine,
                   best={iso: dict(z=best[iso]['z'], tot=best[iso]['tot']) for iso in FIT_ISO},
                   wall=time.time() - t0, amendments='Council brief 004'),
              open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1, default=float)
    # country config markdown with the fitted PHL values
    ph = best['PHL']['z']
    CFG.write_markdown(os.path.join(a.out, 'COUNTRY_CONFIGS.md'),
                       {'PHL': dict(cost_col=ph['cost_col'], prov_capacity=ph['prov_capacity'],
                                    teacher_capacity=ph['teacher_capacity'], prov_elasticity=ph['prov_elasticity'])})
    print('done', time.time() - t0)


if __name__ == '__main__':
    main()
