"""Loop 5 — E1 gate-architecture gradient, E1b KOR no-fit benchmark, E4 income gradient.

NEW code; new structural variable only (binding-gate stakes vector). No take-up fitting in E1; E1b fits
fee multipliers only to Korean fee moments. See PRE_DECLARATIONS_L5.md.

Usage: python e1.py --out ../runs
"""
import argparse, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'code')))
from bcommon import write_rows, write_text, m_sd  # noqa: E402

PUPILS = 1000.0
A0, B_STAKE, B_RET, B_PUB, B_INC, B_FEE = -1.5, 1.0, 0.9, 1.4, 0.55, 1.2

# frozen structural configs (loop-4 uncalibrated; no demand-intercept calibration)
KOR = dict(income=1.0, urban=0.81, urban_mult=1.0, rural_mult=0.75, public_sub=0.60,
           enrol=dict(elementary=0.42, middle=0.30, high=0.28),
           returns=dict(elementary=0.4, middle=0.6, high=0.9),
           F_cm=4.5, F_tt=0.6, cap_cm=0.08, cap_tt=0.035, cost_mult=2.4, teacher_cap=0.30)
HK = dict(income=1.0, urban=1.0, urban_mult=1.0, rural_mult=0.7, public_sub=0.70,
          enrol=dict(lower=0.34, middle=0.33, senior=0.33),
          returns=dict(lower=0.5, middle=0.7, senior=1.0),
          F_cm=4.5, F_tt=0.6, cap_cm=0.08, cap_tt=0.035, cost_mult=0.8, teacher_cap=0.35)
ARCH = {'terminal_only': [0.30, 0.50, 1.50],
        'gate_each_transition': [1.20, 0.90, 0.60],
        'continuous': [0.80, 0.80, 0.80]}
STAGES_KOR = ['elementary', 'middle', 'high']
STAGES_HK = ['lower', 'middle', 'senior']
TARGET_KOR = dict(zip(STAGES_KOR, [86.0, 75.4, 66.4]))
TARGET_HK = dict(zip(STAGES_HK, [35.1, 46.6, 70.3]))
POLICY_ARM = {'KOR-like': 'gate_each_transition', 'HK-like': 'terminal_only'}


def sig(x):
    return 1.0 / (1.0 + math.exp(-max(min(x, 30), -30)))


def demand(cfg, price, shift=0.0, fee_mult=None, income_mult=1.0):
    T, pupils = {}, {}
    fee_mult = fee_mult or {s: 1.0 for s in cfg['enrol']}
    inc0 = cfg['income'] * income_mult
    for s in cfg['enrol']:
        stake, ret = cfg['stakes'][s], cfg['returns'][s]
        for loc, (share, mult) in (('urban', (cfg['urban'], cfg.get('urban_mult', 1.0))),
                                   ('rural', (1 - cfg['urban'], cfg.get('rural_mult', 0.7)))):
            if share <= 0:
                continue
            inc = inc0 * mult
            t = sig(A0 + shift + B_STAKE * stake + B_RET * ret - B_PUB * cfg['public_sub']
                    + B_INC * math.log(max(inc, 1e-6))
                    - B_FEE * (price * fee_mult[s] / max(inc, 1e-6)))
            p = cfg['enrol'][s] * share * PUPILS
            T[(s, loc)] = t; pupils[(s, loc)] = p
    return T, pupils


def market(cfg, shift=0.0, fee_mult=None):
    fee_mult = fee_mult or {s: 1.0 for s in cfg['enrol']}
    p_tt = cfg['F_tt'] * cfg['cost_mult'] / (cfg['cap_tt'] * PUPILS)
    p_cm = cfg['F_cm'] * cfg['cost_mult'] / (cfg['cap_cm'] * PUPILS)
    Qcap = cfg['teacher_cap'] * PUPILS * 0.5
    Tcm, pu = demand(cfg, p_cm, shift, fee_mult); Qd_cm = sum(pu[k] * Tcm[k] for k in Tcm)
    Ttt, _ = demand(cfg, p_tt, shift, fee_mult); Qd_tt = sum(pu[k] * Ttt[k] for k in Ttt)
    if Qd_cm <= Qcap:
        price = p_tt
    elif Qd_tt >= Qcap:
        price = p_cm
    else:
        lo, hi = p_tt, p_cm
        for _ in range(60):
            mid = (lo + hi) / 2
            Tm, _ = demand(cfg, mid, shift, fee_mult)
            if sum(pu[k] * Tm[k] for k in Tm) > Qcap:
                lo = mid
            else:
                hi = mid
        price = (lo + hi) / 2
    T, pupils = demand(cfg, price, shift, fee_mult)
    take = {}
    for s in cfg['enrol']:
        tot_p = sum(pupils[(s, l)] for l in ('urban', 'rural') if (s, l) in pupils)
        dem = sum(pupils[(s, l)] * T[(s, l)] for l in ('urban', 'rural') if (s, l) in T)
        take[s] = min(1.0, dem / max(tot_p, 1e-9))
    # provider mix direction: commercial share of demand (teacher capacity to highest-stakes stage first)
    wn = {s: cfg['stakes'][s] * cfg['returns'][s] for s in cfg['enrol']}
    sd = {s: sum(pupils[(s, l)] * T[(s, l)] for l in ('urban', 'rural') if (s, l) in T) for s in cfg['enrol']}
    rem = Qcap; comm = 0.0; tot = 0.0
    for s in sorted(sd, key=lambda x: wn[x], reverse=True):
        served = min(sd[s], rem); rem = max(0.0, rem - served)
        comm += max(0.0, sd[s] - served); tot += sd[s]
    return dict(price=float(price), take=take, commercial_share=float(comm / max(tot, 1e-9)),
                spend_by_stage={s: float(price * fee_mult[s]) for s in cfg['enrol']})


def with_arch(cfg, arm):
    c = dict(cfg); c['stakes'] = dict(zip(c['enrol'].keys(), ARCH[arm]))
    return c


def e1(out):
    os.makedirs(out, exist_ok=True)
    rows, L = [], ['E1 — GATE-ARCHITECTURE GRADIENT (new structural variable; no take-up fitting).',
                   'Frozen structural configs from loop-4 uncalibrated KOR/HK; only the binding-gate stakes',
                   'vector differs across arms. Gate dates from country cards: KOR CSAT terminal (1994 date',
                   'ASSUMED), high-school equalisation; HKG single terminal HKDSE from 2012 (ASSUMED era),',
                   'SSPA at primary->secondary. No demand-intercept calibration.', '',
                   'Policy-dated assignment: KOR -> gate_each_transition; HKG -> terminal_only.', '',
                   f'  {"country":9s} {"arm":22s} {"stage1":>8s} {"stage2":>8s} {"stage3":>8s}']
    all_pass = True
    results = {}
    for cname, cfg, stages, target in [('KOR-like', KOR, STAGES_KOR, TARGET_KOR),
                                       ('HK-like', HK, STAGES_HK, TARGET_HK)]:
        for arm in ARCH:
            m = market(with_arch(cfg, arm))
            vals = [m['take'][s] * 100 for s in stages]
            rows.append(dict(country=cname, arm=arm, stage1=vals[0], stage2=vals[1], stage3=vals[2],
                             target1=target[stages[0]], target2=target[stages[1]], target3=target[stages[2]],
                             policy_arm=(POLICY_ARM[cname] == arm)))
            L.append(f'  {cname:9s} {arm:22s} {vals[0]:8.1f} {vals[1]:8.1f} {vals[2]:8.1f}')
            if POLICY_ARM[cname] == arm:
                misses = [vals[i] - target[stages[i]] for i in range(3)]
                results[cname] = dict(arm=arm, rates=vals, misses=misses,
                                      within5=all(abs(x) <= 5 for x in misses))
    write_rows(os.path.join(out, 'e1_arms.csv'),
               ['country', 'arm', 'stage1', 'stage2', 'stage3', 'target1', 'target2', 'target3', 'policy_arm'],
               [[r[k] for k in ['country', 'arm', 'stage1', 'stage2', 'stage3', 'target1', 'target2',
                                'target3', 'policy_arm']] for r in rows])
    L += ['', 'PREDECLARED THRESHOLD: all SIX stage rates within +/-5 pp under the policy-dated assignment.']
    for cname, r in results.items():
        stages = STAGES_KOR if 'KOR' in cname else STAGES_HK
        target = TARGET_KOR if 'KOR' in cname else TARGET_HK
        L.append(f'  {cname} policy arm={r["arm"]}: model ' +
                 '/'.join(f'{v:.1f}' for v in r['rates']) + ' vs target ' +
                 '/'.join(f'{target[s]:.1f}' for s in stages) + ' -> misses ' +
                 '/'.join(f'{m:+.1f}' for m in r['misses']) +
                 f' -> {"within +/-5pp" if r["within5"] else "OUTSIDE +/-5pp"}')
        all_pass = all_pass and r['within5']
    L += ['', f'  -> E1 verdict: {"PASS (all six within +/-5 pp)" if all_pass else "FAIL — the gate-position story is dropped, not re-fitted"}']
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    return dict(all_pass=bool(all_pass), results=results, all_arms=rows)


def e1b(out):
    os.makedirs(out, exist_ok=True)
    # KOR fee moments: official by-level annual spend/GDP-pc ratios
    ratios = dict(elementary=0.115, middle=0.149, high=0.184)
    cfg = with_arch(KOR, POLICY_ARM['KOR-like'])
    fm = {s: 1.0 for s in cfg['enrol']}
    for _ in range(60):   # fixed point: fee multipliers -> price -> multipliers
        m = market(cfg, 0.0, fm)
        fm = {s: ratios[s] / max(m['price'], 1e-9) for s in cfg['enrol']}
    m = market(cfg, 0.0, fm)
    target = TARGET_KOR
    rates = {s: m['take'][s] * 100 for s in STAGES_KOR}
    misses = {s: rates[s] - target[s] for s in STAGES_KOR}
    within = all(abs(v) <= 5 for v in misses.values())
    provider_ok = m['commercial_share'] >= 0.50
    spend = m['spend_by_stage']
    hours_dir_ok = (rates['elementary'] > rates['middle'] > rates['high']) and \
                   (spend['elementary'] < spend['middle'] < spend['high'])
    # overall checks (not fitted): per-student and per-participant ratios
    part_all = sum(cfg['enrol'][s] * m['take'][s] for s in STAGES_KOR)
    per_student = sum(cfg['enrol'][s] * m['take'][s] * spend[s] for s in STAGES_KOR) / part_all
    L = ['E1b — KOR NO-FIT BENCHMARK (frozen structural params; only fee multipliers fitted to Korean fee',
         'moments 11.5/14.9/18.4%; overall 10.8/13.8% are checks; participation NOT fitted).',
         f'  fitted stage fee multipliers: ' + ', '.join(f'{s}={fm[s]:.3f}' for s in STAGES_KOR),
         f'  model annual fee/income by stage: ' +
         '/'.join(f'{spend[s] * 100:.1f}' for s in STAGES_KOR) + '% vs fitted targets 11.5/14.9/18.4%',
         f'  overall checks: per-participant {m["price"] * 100:.1f}% vs 13.8% observed; '
         f'per-student {per_student * 100:.1f}% vs 10.8% observed',
         '', f'  {"stage":12s} {"target":>8s} {"model":>8s} {"miss":>8s}']
    for s in STAGES_KOR:
        L.append(f'  {s:12s} {target[s]:8.1f} {rates[s]:8.1f} {misses[s]:+8.1f}')
    L += ['', 'PREDECLARED THRESHOLD: all three stages within +/-5 pp AND direction checks',
          f'  (provider commercial share >= 50% [{m["commercial_share"] * 100:.1f}%] and',
          f'   participation falling + spend rising with stage [{hours_dir_ok}]).',
          '  Hours level 7.3 h/wk = UNABLE (no hours object). KHM/PH transfer stays out-of-sample (not run).',
          f'  -> E1b verdict: {"PASS — ONE-COUNTRY incidence claim for Korea restored (not cross-country)" if (within and provider_ok and hours_dir_ok) else "FAIL — the stop-rule stands permanently"}']
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    return dict(rates=rates, misses=misses, within=bool(within), provider_ok=bool(provider_ok),
                hours_dir_ok=bool(hours_dir_ok), fee_mult=fm, spend=spend,
                pass_=(bool(within and provider_ok and hours_dir_ok)),
                per_participant=float(m['price']), per_student=float(per_student),
                commercial_share=float(m['commercial_share']))


def e4(out):
    os.makedirs(out, exist_ok=True)
    cfg = with_arch(KOR, POLICY_ARM['KOR-like'])
    mults = [0.50, 0.75, 1.00, 1.40, 2.00]
    rows = []
    m0 = market(cfg, 0.0, None)
    price = m0['price']   # single market price; income bands differ only in demand
    spend = []
    mech = []
    for g, im in enumerate(mults):
        # demand-consistent: recompute demand with this band's income, holding the market price
        T, pu = demand(cfg, price, 0.0, None, income_mult=im)
        take = {}
        for s_ in cfg['enrol']:
            tot_p = sum(pu[(s_, l)] for l in ('urban', 'rural') if (s_, l) in pu)
            dem = sum(pu[(s_, l)] * T[(s_, l)] for l in ('urban', 'rural') if (s_, l) in T)
            take[s_] = min(1.0, dem / max(tot_p, 1e-9))
        part = sum(cfg['enrol'][s_] * take[s_] for s_ in STAGES_KOR)
        sp = price * part
        spend.append(sp)
        mech.append(price * part * im)   # mechanical identity for comparison
        rows.append(dict(group=g + 1, income_mult=im, participation=part, spend=sp))
    write_rows(os.path.join(out, 'e4_income.csv'),
               ['group', 'income_mult', 'participation', 'spend'],
               [[r[k] for k in ['group', 'income_mult', 'participation', 'spend']] for r in rows])
    ratio = spend[-1] / max(spend[0], 1e-9)
    ratio_mech = mech[-1] / max(mech[0], 1e-9)
    mono = all(spend[i] < spend[i + 1] for i in range(len(spend) - 1))
    inside = 1.84 <= ratio <= 5.51
    L = ['E4 — KOR INCOME GRADIENT (model spend by declared income band; observed official 2023 spend',
         '183k won (<3m won) -> 671k (>=8m won); observed top/bottom ratio = 3.67.',
         'Income multipliers declared from band midpoints: ' + ', '.join(str(m) for m in mults), '',
         f'  {"group":6s} {"income x":>9s} {"participation":>14s} {"model spend":>12s}']
    for r in rows:
        L.append(f'  {r["group"]:6d} {r["income_mult"]:9.2f} {r["participation"] * 100:13.1f}% '
                 f'{r["spend"] * 100:11.1f}%')
    L += ['', f'  demand-consistent top/bottom spend ratio = {ratio:.2f} vs observed 3.67; monotone: {mono}',
          f'  (mechanical income-multiplier identity would give {ratio_mech:.2f}; reported only as a diagnostic)',
          'PREDECLARED THRESHOLD: monotone increasing AND ratio inside 3.67 x [0.5,1.5] = [1.84,5.51].',
          f'  -> E4 verdict: {"PASS (demand-consistent)" if (mono and inside) else "FAIL / NOT IDENTIFIED"}']
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    return dict(ratio=float(ratio), monotone=bool(mono), inside=bool(inside),
                pass_=bool(mono and inside), spend=spend, mults=mults)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    r1 = e1(os.path.join(a.out, 'E1'))
    r1b = e1b(os.path.join(a.out, 'E1b'))
    r4 = e4(os.path.join(a.out, 'E4'))
    meta = dict(module='e1.py (NEW loop-5 code; gate-stakes structural variable only)',
                gate_dates=dict(KOR=dict(CSAT_terminal='1994 ASSUMED', source='02_lit/COUNTRY_CARDS/KOR.md §2'),
                                HKG=dict(HKDSE_first_cohort='2012', source='02_lit/COUNTRY_CARDS/HKG.md §2',
                                         note='card says dates not independently verified; pre-DSE HKCEE+HKALE')),
                relations='PENDING (09_relations slot tables not consulted)',
                E1=r1, E1b=r1b, E4=r4)
    json.dump(meta, open(os.path.join(a.out, 'l5_meta.json'), 'w'), indent=1, default=str)
    print('E1 all_pass:', r1['all_pass'])
    for c, v in r1['results'].items():
        print(c, v['arm'], [round(x, 1) for x in v['rates']], 'misses', [round(x, 1) for x in v['misses']])
    print('E1b', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r1b.items() if k not in ('fee_mult', 'spend', 'misses')})
    print('E4', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r4.items() if k != 'spend'})


if __name__ == '__main__':
    main()
