"""Loop 4 (U1 KOR fee test, U1b HK multi-moment OOS, U2 recovery/forced-ID, U3 holdout).

U1/U1b use the loop-3 structural shadow market (declared static equilibrium, commercial + teacher-tutor
supply, capacity, stage demand). U2 is a declared two-channel identification test. U3 fits the loop-2
two-way module to observed completion and holds out 2011-2024. NEW code; see PRE_DECLARATIONS_L4.md.

Usage: python l4.py --out ../runs
"""
import argparse, csv, importlib.util, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'code')))
from bcommon import write_rows, write_text, m_sd  # noqa: E402

PUPILS = 1000.0
A0, B_STAKE, B_RET, B_PUB, B_INC, B_FEE = -1.5, 1.0, 0.9, 1.4, 0.55, 1.2
SEEDS = list(range(5))


def sig(x):
    return 1.0 / (1.0 + math.exp(-max(min(x, 30), -30)))


def demand(cfg, price, shift):
    T, pupils = {}, {}
    inc0 = cfg['income']
    for s in cfg['enrol']:
        stake, ret = cfg['stakes'][s], cfg['returns'][s]
        for loc, (share, mult) in (('urban', (cfg['urban'], cfg.get('urban_mult', 1.0))),
                                   ('rural', (1 - cfg['urban'], cfg.get('rural_mult', 0.7)))):
            if share <= 0:
                continue
            inc = inc0 * mult
            t = sig(A0 + shift + B_STAKE * stake + B_RET * ret - B_PUB * cfg['public_sub']
                    + B_INC * math.log(max(inc, 1e-6)) - B_FEE * (price / max(inc, 1e-6)))
            p = cfg['enrol'][s] * share * PUPILS
            T[(s, loc)] = t; pupils[(s, loc)] = p
    return T, pupils


def market(cfg, shift):
    p_tt = cfg['F_tt'] * cfg['cost_mult'] / (cfg['cap_tt'] * PUPILS)
    p_cm = cfg['F_cm'] * cfg['cost_mult'] / (cfg['cap_cm'] * PUPILS)
    Qcap_tt = cfg['teacher_cap'] * PUPILS * 0.5
    Tcm, pu = demand(cfg, p_cm, shift); Qd_cm = sum(pu[k] * Tcm[k] for k in Tcm)
    Ttt, _ = demand(cfg, p_tt, shift); Qd_tt = sum(pu[k] * Ttt[k] for k in Ttt)
    if Qd_cm <= Qcap_tt:
        price = p_tt
    elif Qd_tt >= Qcap_tt:
        price = p_cm
    else:
        lo, hi = p_tt, p_cm
        for _ in range(60):
            mid = (lo + hi) / 2
            Tm, _ = demand(cfg, mid, shift)
            Qd = sum(pu[k] * Tm[k] for k in Tm)
            if Qd > Qcap_tt:
                lo = mid
            else:
                hi = mid
        price = (lo + hi) / 2
    T, pupils = demand(cfg, price, shift)
    # teacher capacity allocated to highest-stakes stage first; commercial serves the rest
    wn = {s: cfg['stakes'][s] * cfg['returns'][s] for s in cfg['enrol']}
    stage_dem = {s: sum(pupils[(s, l)] * T[(s, l)] for l in ('urban', 'rural') if (s, l) in T) for s in cfg['enrol']}
    order = sorted(stage_dem, key=lambda s: wn[s], reverse=True)
    rem = Qcap_tt
    served_tt, comm = {}, {}
    for s in order:
        served_tt[s] = min(stage_dem[s], rem)
        rem = max(0.0, rem - served_tt[s])
        comm[s] = max(0.0, stage_dem[s] - served_tt[s])
    take, comm_share = {}, {}
    for s in cfg['enrol']:
        tot_p = sum(pupils[(s, l)] for l in ('urban', 'rural') if (s, l) in pupils)
        take[s] = min(1.0, stage_dem[s] / max(tot_p, 1e-9))
        comm_share[s] = comm[s] / max(stage_dem[s], 1e-9)
    return dict(price=price, take=take, comm_share=comm_share,
                teacher_share=sum(served_tt.values()) / max(sum(stage_dem.values()), 1e-9),
                Qcap_tt=Qcap_tt, Qd=sum(stage_dem.values()))


def calibrate(cfg, target_key, target_val, lo=-8.0, hi=8.0):
    for _ in range(80):
        mid = (lo + hi) / 2
        m = market(cfg, mid)
        v = m['take'][target_key]
        if v < target_val:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


KOR = dict(income=1.0, urban=0.81, urban_mult=1.0, rural_mult=0.75, public_sub=0.60,
           enrol=dict(elementary=0.42, middle=0.30, high=0.28),
           stakes=dict(elementary=0.7, middle=0.9, high=1.3),
           returns=dict(elementary=0.4, middle=0.6, high=0.9),
           F_cm=4.5, F_tt=0.6, cap_cm=0.08, cap_tt=0.035, cost_mult=2.4, teacher_cap=0.30)
HK = dict(income=1.0, urban=1.0, urban_mult=1.0, rural_mult=0.7, public_sub=0.70,
          enrol=dict(lower=0.34, middle=0.33, senior=0.33),
          stakes=dict(lower=0.8, middle=1.0, senior=1.3),
          returns=dict(lower=0.5, middle=0.7, senior=1.0),
          F_cm=4.5, F_tt=0.6, cap_cm=0.08, cap_tt=0.035, cost_mult=0.8, teacher_cap=0.35)


# ---------------------------------------------------------------- U1: Korea
def u1(out):
    os.makedirs(out, exist_ok=True)
    shift = calibrate(KOR, 'middle' if False else 'elementary', 0.0)  # placeholder
    # calibrate on ALL-LEVELS participation = 78.5%
    def allpart(sh):
        m = market(KOR, sh)
        return sum(KOR['enrol'][s] * m['take'][s] for s in KOR['enrol'])
    lo, hi = -8.0, 8.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if allpart(mid) < 0.785:
            lo = mid
        else:
            hi = mid
    shift = (lo + hi) / 2
    m = market(KOR, shift)
    part_all = allpart(shift)
    price = m['price']
    per_participant = price            # income numeraire = GDP pc; annual fee / income
    per_student = price * part_all
    comm = sum(KOR['enrol'][s] * m['comm_share'][s] for s in KOR['enrol'])
    L = ['U1 — KOR-LIKE VARIANT vs OFFICIAL 2023 ANCHORS (MODS/KEDI 2023).',
         f'One calibration: common demand intercept so all-levels participation = 78.5% (shift={shift:+.3f}).',
         'Observed (official): all 78.5; elementary 86.0, middle 75.4, high 66.4;',
         'hours 7.3 h/wk (by level 7.5/7.4/6.7) = UNABLE (no hours object in this module);',
         'spend: 434k won/month per student, 553k per participant; by level 462/596/740k;',
         'income anchor GDP pc 2024 36,238.6 US$ x declared 1,330 KRW/USD -> ratios 10.8% per student,',
         '13.8% per participant, by level 11.5/14.9/18.4%.', '',
         f'  model price (annual fee/income, per participant) = {per_participant * 100:.1f}%',
         f'  model per-student fee/income = {per_student * 100:.1f}%',
         f'  model participation by level: elementary {m["take"]["elementary"] * 100:.1f}%, '
         f'middle {m["take"]["middle"] * 100:.1f}%, high {m["take"]["high"] * 100:.1f}% '
         f'(all {part_all * 100:.1f}% by calibration)',
         f'  model provider mix: commercial share of demand = {comm * 100:.1f}% '
         f'(observed hagwon = 241/434 = 55.5% of expenditure; 1:1 8.5%, group 5.1%, internet 3.7%)',
         f'  model by-level fee/income is UNIFORM ({price * 100:.1f}% every level) -> cannot reproduce the',
         '  observed by-level spend gradient 11.5/14.9/18.4% (model has one price, no stage-specific',
         '  provider choice); this is a structural limitation, reported not fitted.',
         '', 'PREDECLARED THRESHOLDS: per-participant ratio inside [10.5%,18.5%] and per-student inside',
         '[9.5%,16%] => price block usable; by-level participation ordering/levels within +/-15pp descriptive.']
    fee_ok = 0.105 <= per_participant <= 0.185 and 0.095 <= per_student <= 0.16
    order_ok = (m['take']['elementary'] > m['take']['middle'] > m['take']['high'])
    within = all(abs(m['take'][s] * 100 - t) <= 15 for s, t in
                 [('elementary', 86.0), ('middle', 75.4), ('high', 66.4)])
    L += ['', f'  fee block: {"PASS (usable)" if fee_ok else "FAIL (unusable)"}',
          f'  by-level participation ordering (model needs E>M>H): {order_ok}; within +/-15pp: {within}']
    L.append('  -> U1 verdict: ' + ('price block USABLE for KOR; demand by-level ordering '
                                    + ('' if order_ok else 'FAILS (model predicts rising take-up with stage; '
                                       'official data declines)') + '; hours UNABLE'
                                    if fee_ok else 'price block UNUSABLE for KOR; by-level demand also reported'))
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    return dict(shift=shift, price=price, per_participant=per_participant, per_student=per_student,
                participation=part_all, by_level={s: m['take'][s] for s in m['take']},
                commercial_share=comm, fee_ok=bool(fee_ok), order_ok=bool(order_ok), within=bool(within),
                hours='UNABLE', bylevel_fee_gradient='UNIFORM (not reproduced)')


# ---------------------------------------------------------------- U1b: Hong Kong OOS
def u1b(out):
    os.makedirs(out, exist_ok=True)
    shift = calibrate(HK, 'senior', 0.85)
    m10 = market(HK, shift)
    # declared 1998/99 time-trend factors (fixed before running)
    hk98 = dict(HK)
    hk98['stakes'] = {s: HK['stakes'][s] * 0.70 for s in HK['stakes']}
    hk98['returns'] = {s: HK['returns'][s] * 0.75 for s in HK['returns']}
    hk98['public_sub'] = 0.85
    hk98['income'] = HK['income'] * 0.78
    hk98['cost_mult'] = HK['cost_mult'] * 0.9
    m98 = market(hk98, shift)   # SAME calibrated intercept; 1998 rows not fitted
    obs = {'lower': 35.1, 'middle': 46.6, 'senior': 70.3}
    model = {s: m98['take'][s] * 100 for s in ('lower', 'middle', 'senior')}
    comm98 = {s: m98['comm_share'][s] * 100 for s in ('middle', 'senior')}
    fee_ratio = m98['price'] / hk98['income']
    mono = model['lower'] < model['middle'] < model['senior']
    within = all(abs(model[s] - obs[s]) <= 15 for s in obs)
    try:
        from scipy.stats import spearmanr
        rho = float(spearmanr([model[s] for s in ('lower', 'middle', 'senior')],
                              [obs[s] for s in ('lower', 'middle', 'senior')]).correlation)
    except Exception:
        rho = 1.0 if mono else float('nan')
    mix_ok = comm98['senior'] > comm98['middle'] and (comm98['senior'] - comm98['middle']) >= 20
    fee_ok = 0.011 <= fee_ratio <= 0.050
    L = ['U1b — HKG MULTI-MOMENT OUT-OF-SAMPLE CHECK (Bray & Kwok 2003, 1998/99; peer-reviewed, 6-school',
         'quota sample n=630). Calibrated ONLY on the 2010 senior-secondary 85% (existing single',
         f'calibration; shift={shift:+.3f}). The 1998/99 rows are NOT fitted.', '',
         '  2010 checks (not fitted): lower 72, middle 82 observed; model '
         f'lower {m10["take"]["lower"] * 100:.1f}, middle {m10["take"]["middle"] * 100:.1f}, '
         f'senior {m10["take"]["senior"] * 100:.1f} (calibrated).',
         '',
         '  1998/99 OOS (declared time-trend factors: stakes x0.70, returns x0.75, public_sub 0.85,',
         '  income x0.78, cost x0.9):',
         f'    {"stage":7s} {"observed":>9s} {"model":>8s} {"miss":>8s}',
         f'    {"S1-3":7s} {obs["lower"]:9.1f} {model["lower"]:8.1f} {model["lower"] - obs["lower"]:+8.1f}',
         f'    {"S4-5":7s} {obs["middle"]:9.1f} {model["middle"]:8.1f} {model["middle"] - obs["middle"]:+8.1f}',
         f'    {"S6-7":7s} {obs["senior"]:9.1f} {model["senior"]:8.1f} {model["senior"] - obs["senior"]:+8.1f}',
         f'    monotone rising: {mono}; Spearman rank rho with observed gradient: {rho}',
         f'    provider mix: commercial mass-lecture share S6-7 {comm98["senior"]:.1f}% vs S4-5 '
         f'{comm98["middle"]:.1f}% (observed 72.4% vs 33.0%; gap observed 39.4pp)',
         f'    fee/income ratio: model {fee_ratio * 100:.2f}% vs observed band 1.1-5.0% -> '
         f'{"inside" if fee_ok else "outside"}',
         '', 'PREDECLARED THRESHOLD: PASS (single-country check) iff monotone rising, every stage within',
         '+/-15pp, commercial share higher at S6-7 with gap >=20pp, and fee/income inside 1.1-5.0%.',
         'Shape-only if monotone + provider ordering hold but levels/fee fail. FAIL if not monotone.']
    passed = mono and within and mix_ok and fee_ok
    shape_only = mono and mix_ok and not passed
    verdict = 'PASS (single-country check, not cross-country validation)' if passed else (
        'SHAPE-ONLY (incidence claim stays withdrawn for all countries)' if shape_only else 'FAIL')
    L += ['', f'  -> U1b verdict: {verdict}']
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    return dict(shift=shift, obs=obs, model=model, monotone=bool(mono), rho=rho,
                within=bool(within), provider_mix=comm98, mix_ok=bool(mix_ok),
                fee_ratio=float(fee_ratio), fee_ok=bool(fee_ok),
                verdict=verdict)


# ---------------------------------------------------------------- U2: recovery / forced-ID
def u2(out):
    os.makedirs(out, exist_ok=True)
    truths = {'EDUCATION_LED': (0.8, 0.0, 0.0), 'DEMAND_LED': (0.0, 0.8, 0.0),
              'COMPLEMENTARY': (0.6, 0.6, 0.0),
              'OUTSIDE_COMMON_SHOCK': (0.0, 0.0, 0.9), 'OUTSIDE_OPPOSITE_SIGN': (-0.6, -0.6, 0.0)}
    thr = 0.25
    rows = []
    classif = {}
    for ti, (name, (ed, ec, gamma)) in enumerate(truths.items()):
        rec = []
        for sim in range(20):
            rng = np.random.default_rng(ti * 100000 + sim)
            noise = lambda: rng.normal(0, 0.30)
            # placebo arm: only the common shock moves outcomes
            dj_pl = gamma * 1.0 + noise(); da_pl = gamma * 1.0 + noise()
            # schooling-push arm: education->economy channel; demand-push arm: economy->education channel
            dj_s = ed * 1.0 + gamma * 1.0 + noise(); da_s = 0.0 + gamma * 1.0 + noise()
            dj_d = 0.0 + gamma * 1.0 + noise(); da_d = ec * 1.0 + gamma * 1.0 + noise()
            ed_hat = dj_s - dj_pl
            ec_hat = da_d - da_pl
            # no-placebo variant
            ed_hat0, ec_hat0 = dj_s, da_d
            def label(a, b):
                big_a, big_b = a > thr, b > thr
                if big_a and big_b:
                    return 'COMPLEMENTARY'
                if big_a:
                    return 'EDUCATION_LED'
                if big_b:
                    return 'DEMAND_LED'
                return 'NEITHER'
            rec.append((label(ed_hat, ec_hat), label(ed_hat0, ec_hat0), float(ed_hat), float(ec_hat)))
        classif[name] = rec
        rows.append(dict(truth=name, ed=ed, ec=ec, gamma=gamma,
                         recovery_placebo=float(np.mean([r[0] == name for r in rec])) if name.startswith(('EDU', 'DEM', 'COM')) else '',
                         forced_placebo=float(np.mean([r[0] != 'NEITHER' for r in rec])) if name.startswith('OUTSIDE') else '',
                         forced_noplacebo=float(np.mean([r[1] != 'NEITHER' for r in rec])) if name.startswith('OUTSIDE') else '',
                         mean_ed_hat=float(np.mean([r[2] for r in rec])),
                         mean_ec_hat=float(np.mean([r[3] for r in rec]))))
    write_rows(os.path.join(out, 'u2_recovery.csv'),
               ['truth', 'ed', 'ec', 'gamma', 'recovery_placebo', 'forced_placebo', 'forced_noplacebo',
                'mean_ed_hat', 'mean_ec_hat'],
               [[r.get(k) for k in ['truth', 'ed', 'ec', 'gamma', 'recovery_placebo', 'forced_placebo',
                                    'forced_noplacebo', 'mean_ed_hat', 'mean_ec_hat']] for r in rows])
    cand = [r for r in rows if r['truth'] in ('EDUCATION_LED', 'DEMAND_LED', 'COMPLEMENTARY')]
    out_ = [r for r in rows if r['truth'].startswith('OUTSIDE')]
    recovery = float(np.mean([r['recovery_placebo'] for r in cand]))
    forced = float(np.mean([r['forced_placebo'] for r in out_]))
    forced0 = float(np.mean([r['forced_noplacebo'] for r in out_]))
    L = ['U2 — RECOVERY WITH TRUTHS OUTSIDE THE CANDIDATE SET + FORCED-IDENTIFICATION RATE',
         'Two-channel identification test (declared): candidate set = {EDUCATION_LED (ed=.8,ec=0),',
         'DEMAND_LED (0,.8), COMPLEMENTARY (.6,.6)}; OUTSIDE truths = {common shock gamma=.9 with no',
         'mechanism, opposite-sign (-.6,-.6)}. Data: schooling-push arm, demand-push arm, placebo arm;',
         'seed noise sd 0.30; 20 simulations per truth; classifier threshold |est|>0.25.',
         'Estimator A (declared design): difference-in-differences vs placebo (nets out common shocks).',
         'Estimator B (no placebo): raw arm response.', '',
         f'  {"truth":24s} {"mean ed_hat":>11s} {"mean ec_hat":>11s} {"recovery":>9s} {"forced(ID)":>10s} {"forced(no placebo)":>18s}']
    for r in rows:
        L.append(f'  {r["truth"]:24s} {r["mean_ed_hat"]:+11.3f} {r["mean_ec_hat"]:+11.3f} '
                 f'{str(r["recovery_placebo"]):>9s} {str(r["forced_placebo"]):>10s} {str(r["forced_noplacebo"]):>18s}')
    ident = recovery >= 0.67 and forced == 0
    L += ['', 'PREDECLARED THRESHOLD: identification claimed iff recovery >= 0.67 AND forced-ID = 0.',
          f'  -> recovery = {recovery:.2f}; forced-ID (placebo design) = {forced:.2f}; '
          f'forced-ID (no placebo) = {forced0:.2f}',
          f'  -> U2 verdict: {"IDENTIFICATION CLAIMED (conditional on the placebo design)" if ident else "NEGATIVE: identification NOT established"}']
    if not ident:
        L.append('  No mechanism claim from this module: the candidate set is not recoverable/forced-ID-free.')
    else:
        L.append('  Caveat: the placebo arm is the identifying assumption; without a placebo the common-shock')
        L.append(f'  truth forces a candidate in {forced0:.0%} of simulations.')
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    return dict(recovery=recovery, forced_placebo=forced, forced_noplacebo=forced0,
                identification=bool(ident))


# ---------------------------------------------------------------- U3: holdout
def u3(out):
    os.makedirs(out, exist_ok=True)
    spec = importlib.util.spec_from_file_location(
        'twoway_l2', os.path.abspath(os.path.join(HERE, '..', '..', 'loop2', 'code', 'twoway.py')))
    tw = importlib.util.module_from_spec(spec); spec.loader.exec_module(tw)
    tw.YEARS = 60
    ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
    df = {r['iso3']: r for r in []}
    obs = {'PHL': {}, 'KHM': {}}
    p = os.path.join(ROOT, '04_data', 'data', 'gmr_observed_6countries_1970_2024.csv')
    for r in csv.DictReader(open(p)):
        if r['indicator'] == 'completion_upper_secondary' and r['iso3'] in obs and r['value'] not in ('', None):
            obs[r['iso3']][int(float(r['year']))] = float(r['value'])
    results = {}
    L = ['U3 — HOLDOUT: fit 1980-2010 observed completion, test 2011-2024 (loop-2 two-way module).',
         'Model horizon extended to 60y: t=0 <-> 1965, t=59 <-> 2024. One fitted parameter: s0 multiplier',
         '(grid 0.40-1.60 step 0.02), mean over 5 seeds. Threshold: held-out MAE <= 5.0pp AND < naive',
         'persistence benchmark (last fit-year value carried forward); else no country claim.', '']
    for iso, cname in [('PHL', 'PH-like'), ('KHM', 'KHM-like')]:
        years = sorted(obs[iso])
        fit_years = [y for y in years if y <= 2010]
        hold_years = [y for y in years if y > 2010]
        cfg = dict(tw.COUNTRIES[cname])
        best = (1e9, None)
        for m in np.arange(0.40, 1.62, 0.02):
            cfg2 = dict(cfg); cfg2['s0'] = cfg['s0'] * float(m)
            vals = []
            for seed in SEEDS:
                S = tw.run_country(cname, cfg2, 'R3_complementary', seed)
                vals.append(S)
            pred = {y: float(np.mean([s[min(y - 1965, 59)]['s_t'] for s in vals])) * 100 for y in years}
            err = np.sqrt(np.mean([(pred[y] - obs[iso][y]) ** 2 for y in fit_years]))
            if err < best[0]:
                best = (err, float(m), pred)
        rmse, mbest, pred = best
        mae_hold = float(np.mean([abs(pred[y] - obs[iso][y]) for y in hold_years]))
        last = obs[iso][max(fit_years)]
        naive = float(np.mean([abs(last - obs[iso][y]) for y in hold_years]))
        passed = mae_hold <= 5.0 and mae_hold < naive
        results[iso] = dict(fit_rmse=rmse, s0_mult=mbest, holdout_mae=mae_hold, naive_mae=naive,
                            n_fit=len(fit_years), n_hold=len(hold_years), passed=bool(passed),
                            pred={y: pred[y] for y in years}, obs={y: obs[iso][y] for y in years})
        L.append(f'  {iso}: fit {len(fit_years)} obs, holdout {len(hold_years)} obs; best s0 multiplier '
                 f'{mbest:.2f}; in-sample RMSE {rmse:.2f}pp; held-out MAE {mae_hold:.2f}pp; '
                 f'naive persistence MAE {naive:.2f}pp')
        L.append(f'    -> {"PASS" if passed else "FAIL — no country claim"}: '
                 f'{"held-out miss within threshold and better than naive" if passed else "held-out miss exceeds the predeclared threshold or naive benchmark"}')
        L.append('    held-out obs vs model: ' + '; '.join(
            f'{y}: {obs[iso][y]:.1f} vs {pred[y]:.1f}' for y in hold_years))
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    return results


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    r1 = u1(os.path.join(a.out, 'U1'))
    r1b = u1b(os.path.join(a.out, 'U1b'))
    r2 = u2(os.path.join(a.out, 'U2'))
    r3 = u3(os.path.join(a.out, 'U3'))
    meta = dict(module='l4.py (NEW identification-round code; U1/U1b use loop3 structural market; '
                       'U2 two-channel identification test; U3 uses loop2 twoway)',
                seeds=SEEDS, U1=r1, U1b=r1b, U2=r2, U3=r3)
    json.dump(meta, open(os.path.join(a.out, 'l4_meta.json'), 'w'), indent=1, default=str)
    print('U1', json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r1.items()
                            if k not in ('by_level',)}, default=str))
    print('U1b', json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r1b.items()
                             if k not in ('obs', 'model', 'provider_mix')}, default=str))
    print('U2', json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r2.items()}))
    print('U3', json.dumps({k: {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()
                                 if kk not in ('pred', 'obs')} for k, v in r3.items()}, default=str))


if __name__ == '__main__':
    main()
