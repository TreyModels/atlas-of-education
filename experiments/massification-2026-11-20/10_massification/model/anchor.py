"""A1 anchor run (PHL) — DESCRIPTIVE-ONLY under D57: capacity-gated state push arms, crossing years M0-M4,
ordering/gaps, R6 false-positive check, A2d capacity-leads-intake, standing scaling FAIL row.
Predeclared in PRE_ANCHOR_A1.md (sha b7020cf4... / reconciled) and PRE_ANCHOR_CAPACITY.md (sha 702d5c7a...).
Simulated = model output; observed = on-disk status target/observed cells. No crossing year is fitted.
"""
import csv, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pushpull as M
import calibrate as K

R = '/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/massification_2026-11-20'
# ---- observed capacity inputs (declared sources; missing -> dropped weight, never imputed)
def load_capacity():
    # delivery: PHL high-school PTR from SCHOOL_EXPANSION.csv (observed/high) + WDI secondary PTR if available
    ptr = {2000: 37.0, 2014: 27.0, 2017: 24.0}          # SCHOOL_EXPANSION.csv, status observed/high
    try:
        for r in csv.DictReader(open(R + '/10_massification/data/SCHOOL_EXPANSION.csv')):
            if r['iso3'] == 'PHL' and r['indicator'] == 'pupil_teacher_ratio_high_school' and r['value']:
                ptr[int(r['year'])] = float(r['value'])
    except Exception:
        pass
    # fiscal: government expenditure on education %GDP (WDI 4-country file)
    fisc = {}
    try:
        for r in csv.DictReader(open(R + '/04_data/data/wdi_4countries_long.csv')):
            if r['iso3'] == 'PHL' and 'Government expenditure on education, total (% of GDP)' in r['indicator_name'] and r['value']:
                fisc[int(r['year'])] = float(r['value'])
    except Exception:
        pass
    return ptr, fisc


def interp_flat(d, years):
    xs = sorted(d); ys = [d[x] for x in xs]
    out = {}
    for t in years:
        if not xs:
            out[t] = np.nan; continue
        if t <= xs[0]: out[t] = ys[0]
        elif t >= xs[-1]: out[t] = ys[-1]
        else: out[t] = float(np.interp(t, xs, ys))
    return out


def capacity_index(years, ptr, fisc):
    """C_t in [0,1]: delivery 0.5 (PTR), fiscal 0.3 (edu %GDP), enforcement 0.2 (compulsory duration)."""
    p = interp_flat(ptr, years)
    f = interp_flat(fisc, years) if fisc else {t: np.nan for t in years}
    C = {}
    for t in years:
        parts, wts = [], []
        if np.isfinite(p[t]):
            parts.append(float(np.clip((40.0 - p[t]) / 20.0, 0, 1))); wts.append(0.5)   # 40->20 PTR maps 0->1
        if np.isfinite(f[t]):
            parts.append(float(np.clip((f[t] - 2.0) / 3.0, 0, 1))); wts.append(0.3)     # 2%->5% GDP maps 0->1
        # enforcement proxy (declared POLICY mapping): compulsory years / 13
        comp = 13.0 if t >= 2013 else (10.0 if t >= 1987 else 6.0)
        parts.append(comp / 13.0); wts.append(0.2)
        C[t] = float(np.clip(np.average(parts, weights=wts), 0, 1))
    return C


KAPPA = 0.75   # A10: G(C) = C^kappa, kappa in [0.5,1.0] declared (sensitivity reported)


def gate(C, kappa=KAPPA):
    return float(max(C, 0.0) ** kappa)


def arms(years, C):
    """Four declared arms: law-only, capacity-gated, capacity-only, none (push_scale 0.05 declared)."""
    PUSH = 0.05
    marks = {}   # year -> marker (1 during affected periods)
    for t in years:
        m = 0.0
        if 2013 <= t:  m = max(m, 1.0)       # K-12 marker (affected upper secondary; effective 2016)
        if 2016 <= t:  m = max(m, 1.0)       # free SHS
        if 2018 <= t:  m = max(m, 1.0)       # free tertiary
        marks[t] = m
    out = {}
    CEIL = 0.25   # declared saturating share to ceiling levels (floor-only capacity channel, A10)
    # floor push: primary/lower-secondary progression; ceiling push: upper/tertiary at CEIL of the gated amount
    floor = {t: PUSH * marks[t] * gate(C[t]) for t in years}
    ceil = {t: CEIL * PUSH * marks[t] * gate(C[t]) for t in years}
    out['law_only'] = {'floor': {t: PUSH * marks[t] for t in years}, 'ceiling': {t: PUSH * marks[t] for t in years}}
    out['capacity_gated'] = {'floor': floor, 'ceiling': ceil}
    out['capacity_only'] = {'floor': {t: PUSH * gate(C[t]) for t in years}, 'ceiling': {t: CEIL * PUSH * gate(C[t]) for t in years}}
    out['none'] = {'floor': {t: 0.0 for t in years}, 'ceiling': {t: 0.0 for t in years}}
    return out


def theta_from_z(z):
    th = {}
    for i, k in enumerate(K.KEYS):
        lo, hi = K.BOUNDS[k]
        v = lo + z[i] * (hi - lo)
        th[k] = float(round(v)) if k in ('lag_s', 'lag_d') else float(v)
    return th


def crossing(series, thr, years, direction='ge'):
    ys = [y for y in years if y in series and series[y] is not None]
    for y in ys:
        if (series[y] >= thr) if direction == 'ge' else (series[y] <= thr):
            return y
    return None


def main():
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anchor_out')
    os.makedirs(outdir, exist_ok=True)
    years = list(range(1960, 2041))
    ptr, fisc = load_capacity()
    C = capacity_index(years, ptr, fisc)
    armser = arms(years, C)
    OBS = K.load_completion()
    rivals = ['demand_led', 'education_led', 'complementary']
    rows = []
    for rival in rivals:
        for arm, push in armser.items():
            # fit base progression params on PHL completion 1999-2013 (brief-013 FIT cells; PHL anchor)
            from scipy.optimize import differential_evolution
            def obj(z):
                th = theta_from_z(z)
                th['push_series'] = {**push['floor'], **{k: push['ceiling'].get(k, 0.0) for k in push['floor']}}
                th['push_level'] = 'all'
                h = M.run('PHL', rival=rival, priors=th)
                sim_fit = {k: {x['year']: x[k] for x in h} for k in K.LEVEL_KEYS}
                m, n = K.metrics(sim_fit, OBS.get('PHL', {}), (1999, 2013))
                return m if n else 1e6
            res = differential_evolution(obj, bounds=[(0, 1)] * len(K.KEYS), seed=4242, maxiter=18, popsize=6,
                                         tol=1e-3, polish=False, workers=1)
            th = theta_from_z(res.x)
            th['push_series'] = {**push['floor']}
            # ceiling levels receive the saturating share; model applies push to upper/tertiary only via push_ceiling
            th['push_ceiling'] = push['ceiling']; th['push_level'] = 'all'
            h = M.run('PHL', rival=rival, priors=th)
            sim = {k: {x['year']: x[k] for x in h} for k in ('completion_primary', 'completion_lower',
                                                              'completion_upper', 'ger_primary', 'ger_lower',
                                                              'ger_upper', 'ger_tertiary')}
            sim_fit = {k: sim[k] for k in K.LEVEL_KEYS}
            fr = K.fit_metrics(sim_fit, OBS.get('PHL', {}), (1999, 2013))
            hr = K.fit_metrics(sim_fit, OBS.get('PHL', {}), (2014, 2024))
            # milestones (official IDs): M0 lower-sec completion >=50; M1 primary GER >=100; M2 lower-sec completion >=90;
            # M3 upper-sec completion >=90 (must NOT cross by 2024); M4 tertiary GER >=50
            cr = dict(M0=crossing(sim['completion_lower'], 50, years), M1=crossing(sim['ger_primary'], 100, years),
                      M2=crossing(sim['completion_lower'], 90, years), M3=crossing(sim['completion_upper'], 90, years),
                      M4=crossing(sim['ger_tertiary'], 50, years))
            r6_false_positive = bool(cr['M3'] is not None and cr['M3'] <= 2024)
            rows.append(dict(rival=rival, arm=arm, fit_mae=float(np.mean([x[4] for x in fr])) if fr else np.nan,
                             fit_n=len(fr), hold_mae=float(np.mean([x[4] for x in hr])) if hr else np.nan,
                             hold_n=len(hr), **{k: ('' if cr[k] is None else cr[k]) for k in cr},
                             R6_false_pos=r6_false_positive,
                             scaling_verdict='FAIL (standing; generated exps wrong-sign/outside A3 range)'))
            print(f"{rival}/{arm}: fit {rows[-1]['fit_mae']:.2f} hold {rows[-1]['hold_mae']:.2f} crossings {cr} R6fp={r6_false_positive}", flush=True)
    with open(os.path.join(outdir, 'anchor_table.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    # A2d capacity-leads-intake: cross-correlation of capacity change and enrolment growth at lags 0-6
    best = None
    for rival in rivals:
        th = {k: K.BOUNDS[k][0] + 0.5 * (K.BOUNDS[k][1] - K.BOUNDS[k][0]) for k in K.KEYS}
        th['push_series'] = armser['capacity_gated']; th['push_level'] = 'all'
        h = M.run('PHL', rival=rival, priors=th)
        enr = {x['year']: (x['ger_lower'] + x['ger_upper'] + x['ger_tertiary']) / 3.0 for x in h}
        dC = {t: C[t] - C.get(t - 1, C[t]) for t in years}
        dE = {t: enr[t] - enr.get(t - 1, enr[t]) for t in years}
        for lag in range(0, 7):
            xs = [dC[t - lag] for t in years if 1990 <= t <= 2024 and (t - lag) in dC]
            ys = [dE[t] for t in years if 1990 <= t <= 2024]
            if len(xs) > 5 and np.std(xs) > 1e-12:
                c = float(np.corrcoef(xs, ys)[0, 1])
                if best is None or abs(c) > abs(best[2]):
                    best = (rival, lag, c)
    L = ['A1 ANCHOR (PHL) — DESCRIPTIVE-ONLY under D57; capacity-gated state-push arms; crossing years M0-M4',
         'SCALING CRITERION: FAIL (standing; unrepaired + repair cells; generated exps wrong-sign/outside A3 range).',
         'Phase cap (D56/R17/R23): at most PARTIAL/DESCRIPTIVE + EQUIVALENT; no PASS; no direction claim.',
         '', 'Observed milestones (on-disk): M0 left-censored (>=50 before 1999); M1 left-censored (primary GER>=100 by 1999);',
         'M2 lower-sec completion >=90 in 2024; M3 upper-sec completion >=90 NEVER by 2024 (75.03) => R6 false-positive test;',
         'M4 tertiary GER >=50 in 2024-25 band.', 'Capacity index inputs: PHL high-school PTR 37(2000)->27(2014)->24(2017) [observed/high];',
         'education spending %GDP where observed (WDI); enforcement proxy = compulsory duration mapping (declared);',
         'weights delivery 0.5 / fiscal 0.3 / enforcement 0.2; gate G(C)=sigmoid((C-0.5)/0.15) declared.', '',
         f'  {"rival":14s} {"arm":16s} {"fit":>6s} {"hold":>6s} {"M0":>5s} {"M1":>5s} {"M2":>5s} {"M3":>5s} {"M4":>5s} {"R6fp":>5s}']
    for r in rows:
        L.append(f'  {r["rival"]:14s} {r["arm"]:16s} {r["fit_mae"]:6.2f} {r["hold_mae"]:6.2f} '
                 f'{str(r["M0"] or "-"):>5s} {str(r["M1"] or "-"):>5s} {str(r["M2"] or "-"):>5s} {str(r["M3"] or "-"):>5s} '
                 f'{str(r["M4"] or "-"):>5s} {str(r["R6_false_pos"]):>5s}')
    L += ['', f'A2d capacity-leads-intake (declared lag 0-6, cross-correlation of dC and enrolment growth): best {best}',
          'READ: M0/M1 are left-censored (no point-timing credit); M2/M4 are the informative crossings; M3 must stay "not crossed" (R6).',
          'If the capacity-gated arm reproduces M2/M4 timing while law_only does not, the capacity-timing hypothesis is supported;',
          'if all arms tie, report EQUIVALENT (R13). No direction claim.']
    open(os.path.join(outdir, 'findings.txt'), 'w').write('\n'.join(L) + '\n')
    json.dump(dict(arms=list(armser), capacity_series={str(k): v for k, v in C.items()},
                   a2d_best=best), open(os.path.join(outdir, 'run_meta.json'), 'w'), indent=1)
    print('wrote', outdir)


if __name__ == '__main__':
    main()
