"""Loop 8 — relations→model wiring, re-run of the synthetic frontier (EVERYTHING SYNTHETIC).

Wires 9 graded relations as declared parameter distributions into the loop-6 synthetic generator and reruns the
SAME LHS design (256 draws x 5 seeds). Predeclaration: loop8/PRE_DECLARATIONS_L8.md. No fitting; programme CLOSED;
brief-008 limits stand.

Usage: python synth_wired.py --out ../runs
"""
import argparse, csv, importlib.util, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'code')))
from bcommon import write_rows, write_text  # noqa: E402

# loop-6 generator module (constants, country configs, target set)
spec6 = importlib.util.spec_from_file_location('synth6', os.path.abspath(os.path.join(HERE, '..', '..', 'loop6', 'code', 'synth.py')))
s6 = importlib.util.module_from_spec(spec6); spec6.loader.exec_module(s6)
spec_tw = importlib.util.spec_from_file_location('tww', os.path.abspath(os.path.join(HERE, '..', '..', 'loop2', 'code', 'twoway.py')))
tw = importlib.util.module_from_spec(spec_tw); spec_tw.loader.exec_module(tw)

sig, A0, B_STAKE, B_RET, B_PUB = s6.sig, s6.A0, s6.B_STAKE, s6.B_RET, s6.B_PUB
PUPILS = s6.PUPILS
CONFIGS = s6.CONFIGS
TARGETS = s6.TARGETS
# ECI conditioning: eci_hs92 mean 2015-2024 (10 obs each) from 09_relations/data/economic_complexity_panel.csv
ECI = {'KOR': 1.754, 'HKG': 1.218, 'PHL': 0.718, 'KHM': -0.281}
ECI_REF = 0.852  # mean of the four model countries
ECI_MAP_TW = {'PH-like': 'PHL', 'KHM-like': 'KHM'}
BURN = s6.BURN if hasattr(s6, 'BURN') else None
STAGES = {'KOR': ['elementary', 'middle', 'high'], 'HKG': ['lower', 'middle', 'senior'],
          'KHM': ['primary', 'lower', 'upper'], 'PHL': ['primary', 'lower', 'upper']}
ARCH = {'terminal_only': [0.30, 0.50, 1.50], 'gate_each_transition': [1.20, 0.90, 0.60],
        'continuous': [0.80, 0.80, 0.80]}
ARCH_LIST = list(ARCH)
NDRAW, NSEED = 256, 5
SEEDS = list(range(NSEED))
# declared ranges: loop-6 nine params + wired relation distributions (PRE_DECLARATIONS_L8.md)
RANGES = dict(stakes_scale=(0.5, 2.0), pub=(0.1, 0.9), income=(0.5, 3.0), returns_scale=(0.6, 1.4),
              cost_mult=(0.4, 3.0), teacher_cap=(0.05, 0.95), delta=(-4.0, 4.0),
              fee_mult_scale=(0.5, 2.0), eps_ec=(-1.035, 0.6),
              b01=(0.010, 0.189), b04=(0.281, 1.075), b07=(0.10, 0.30), b21=(0.4, 1.0),
              b22=(0.6, 1.3), b23=(0.10, 0.60), r24=(2.29, 2.62), B_FEE_scale=(0.5, 2.0),
              births_ratio=(0.6, 1.3), spend_ratio=(0.8, 1.6),
              b_eci_stake=(0.05, 0.25), b_eci_ret=(0.05, 0.20), b_eci_comp=(0.05, 0.20),
              b_eci_formal=(0.05, 0.20))


def lhs(n, rng):
    out = {}
    for k, (lo, hi) in RANGES.items():
        u = (rng.permutation(n) + rng.random(n)) / n
        out[k] = lo + u * (hi - lo)
    out['arch'] = [ARCH_LIST[i % 3] for i in range(n)]
    return out


def make_cfg(cname, p):
    base, stages = CONFIGS[cname]
    c = dict(base)
    c['stakes'] = {s: ARCH[p['arch']][i] * p['stakes_scale'] for i, s in enumerate(stages)}
    c['returns'] = {s: base['returns'][s] * p['returns_scale'] for s in stages}
    c['public_sub'] = p['pub']
    c['income'] = base['income'] * p['income']
    c['cost_mult'] = base['cost_mult'] * p['cost_mult']
    c['teacher_cap'] = p['teacher_cap']
    if 'urban_mult' in c:
        c['urban_mult'] = max(1.2, c['urban_mult'] * (p['r24'] / 2.0))
    else:
        c['urban_mult'] = max(1.2, p['r24'] / 2.0)
    grad = 0.30 * (p['fee_mult_scale'] - 1.0)
    c['fee_mult'] = {s: 1.0 + grad * (i - 1) for i, s in enumerate(stages)}
    # ECI conditions upper-stage (terminal) gate demand: stakes and credential returns
    eci = ECI[cname]; last = stages[-1]
    c['stakes'][last] = c['stakes'][last] * (1 + p['b_eci_stake'] * (eci - ECI_REF))
    c['returns'][last] = c['returns'][last] * (1 + p['b_eci_ret'] * (eci - ECI_REF))
    return c, stages


def demand(cfg, stages, price, p, noise, income_mult=1.0):
    T, pu = {}, {}
    inc0 = cfg['income'] * income_mult
    B_INC = 0.55 * p['b22']
    B_FEE = p['B_FEE_scale'] * 1.1
    n = max(len(stages) - 1, 1)
    for i, s in enumerate(stages):
        prox = i / n
        stake = cfg['stakes'][s] * (1 + p['b21'] * (prox - 0.5))
        fm = cfg['fee_mult'][s] * (1 + p['b23'] * (prox - 0.5))
        ret = cfg['returns'][s]
        for loc, (share, mult) in (('urban', (cfg['urban'], cfg.get('urban_mult', 1.0))),
                                   ('rural', (1 - cfg['urban'], cfg.get('rural_mult', 0.7)))):
            if share <= 0:
                continue
            inc = inc0 * mult
            t = sig(A0 + p['delta'] + noise[s] + B_STAKE * stake + B_RET * ret - B_PUB * cfg['public_sub']
                    + B_INC * math.log(max(inc, 1e-6)) - B_FEE * (price * fm / max(inc, 1e-6)))
            pp = cfg['enrol'][s] * share * PUPILS
            T[(s, loc)] = t; pu[(s, loc)] = pp
    return T, pu


def market(cfg, stages, p, noise, income_mult=1.0):
    def Qd(price):
        T, pu = demand(cfg, stages, price, p, noise, income_mult)
        return sum(pu[k] * T[k] for k in T), T, pu
    p_tt = cfg['F_tt'] * cfg['cost_mult'] / (cfg['cap_tt'] * PUPILS)
    p_cm = cfg['F_cm'] * cfg['cost_mult'] / (cfg['cap_cm'] * PUPILS)
    Qcap = cfg['teacher_cap'] * PUPILS * 0.5
    Qd_cm, _, _ = Qd(p_cm); Qd_tt, _, _ = Qd(p_tt)
    if Qd_cm <= Qcap:
        price = p_tt
    elif Qd_tt >= Qcap:
        price = p_cm
    else:
        lo, hi = p_tt, p_cm
        for _ in range(40):
            mid = (lo + hi) / 2
            if Qd(mid)[0] > Qcap:
                lo = mid
            else:
                hi = mid
        price = (lo + hi) / 2
    _, T, pupils = Qd(price)
    take, dem_s = {}, {}
    for s in stages:
        tot_p = sum(pupils[(s, l)] for l in ('urban', 'rural') if (s, l) in pupils)
        dem = sum(pupils[(s, l)] * T[(s, l)] for l in ('urban', 'rural') if (s, l) in T)
        take[s] = min(1.0, dem / max(tot_p, 1e-9)); dem_s[s] = dem
    B_INC = 0.55 * p['b22']
    ratio = {s: price * cfg['fee_mult'][s] * (1 + p['b23'] * (0.5 - 0.5)) / max(cfg['income'], 1e-9) for s in stages}
    part_all = sum(cfg['enrol'][s] * take[s] for s in stages)
    per_part = sum(cfg['enrol'][s] * take[s] * ratio[s] for s in stages) / max(part_all, 1e-9)
    per_student = part_all * per_part
    wn = {s: cfg['stakes'][s] * cfg['returns'][s] for s in stages}
    rem = Qcap; comm = {}
    for s in sorted(dem_s, key=lambda x: wn[x], reverse=True):
        served = min(dem_s[s], rem); rem = max(0.0, rem - served)
        comm[s] = (dem_s[s] - served) / max(dem_s[s], 1e-9)
    comm_overall = sum(dem_s[s] * comm[s] for s in comm) / max(sum(dem_s.values()), 1e-9)
    # income-gradient spend ratio (demand-consistent, B_INC wired)
    spend = []
    for im in (0.5, 0.75, 1.0, 1.4, 2.0):
        T2, pu2 = demand(cfg, stages, price, p, noise, income_mult=im)
        c2 = dict(cfg); c2['income'] = cfg['income'] * im
        part = 0.0
        for s in stages:
            tot = sum(pu2[(s, l)] for l in ('urban', 'rural') if (s, l) in pu2)
            dem = sum(pu2[(s, l)] * T2[(s, l)] for l in ('urban', 'rural') if (s, l) in T2)
            part += c2['enrol'][s] * min(1.0, dem / max(tot, 1e-9))
        spend.append(price * part)
    income_ratio = spend[-1] / max(spend[0], 1e-9)
    return dict(take=take, per_part=per_part, per_student=per_student, comm=comm,
                comm_overall=comm_overall, income_ratio=income_ratio, price=price)


def cohort_flows(p, eps):
    out = {}
    births_rel = p['births_ratio'] / 1.0
    for cname in ('PH-like', 'KHM-like'):
        c = dict(tw.COUNTRIES[cname])
        eci = ECI[ECI_MAP_TW[cname]]
        c['s0'] = min(0.95, c['s0'] * (p['spend_ratio'] ** p['b01']) * (births_rel ** (-p['b07']))
                      * (1 + p['b_eci_comp'] * (eci - ECI_REF)))
        c['c0'] = min(0.98, c['c0'] * (max(p['income'], 1e-6) ** p['b04'])
                      * (1 + p['b_eci_comp'] * (eci - ECI_REF)))
        tw.REGIMES['R3_complementary']['eps_ec'] = float(eps) + p['b_eci_formal'] * (eci - ECI_REF)
        S = tw.run_country(cname, c, 'R3_complementary', 0)
        out[cname] = float(np.mean([x['s_t'] for x in S[-5:]])) * 100
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True)
    a = ap.parse_args(); out = a.out
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(20261120)
    P = lhs(NDRAW, rng)
    recs = []
    for d in range(NDRAW):
        p = {k: (P[k][d] if k != 'arch' else P['arch'][d]) for k in P}
        for seed in SEEDS:
            nrng = np.random.default_rng(10_000 + d * 10 + seed)
            rec = dict(draw=d, seed=seed, arch=p['arch'], **{k: float(p[k]) for k in RANGES})
            for cname in CONFIGS:
                cfg, stages = make_cfg(cname, p)
                noise = {s: 0.15 * float(nrng.standard_normal()) for s in stages}
                m = market(cfg, stages, p, noise)
                for i, s in enumerate(stages):
                    rec[f'{cname}_take{i + 1}'] = m['take'][s] * 100
                rec[f'{cname}_per_part'] = m['per_part'] * 100
                rec[f'{cname}_per_student'] = m['per_student'] * 100
                rec[f'{cname}_comm_overall'] = m['comm_overall'] * 100
                if cname == 'HKG':
                    rec['HKG_comm_senior'] = m['comm']['senior'] * 100
                    rec['HKG_comm_middle'] = m['comm']['middle'] * 100
                if cname == 'KOR':
                    rec['KOR_income_ratio'] = m['income_ratio']
                    rec['KOR_spend_high_elem'] = (m['price'] * cfg['fee_mult']['high'] * (1 + p['b23'] * 0.5)) / \
                                                 max(m['price'] * cfg['fee_mult']['elementary'] * (1 - p['b23'] * 0.5), 1e-9)
            fl = cohort_flows(p, p['eps_ec'])
            rec['PHL_completion'] = fl['PH-like']; rec['KHM_completion'] = fl['KHM-like']
            recs.append(rec)
    hdr = list(recs[0].keys())
    write_rows(os.path.join(out, 'synth_wired_draws.csv'), hdr, [[r[k] for k in hdr] for r in recs])
    # means per draw
    means = {}
    for d in range(NDRAW):
        R = [r for r in recs if r['draw'] == d]
        means[d] = {k: float(np.mean([r[k] for r in R])) for k in R[0] if k not in ('draw', 'seed', 'arch')}
    # frontier (same targets as loop 6)
    before = {}
    p6 = os.path.join(HERE, '..', '..', 'loop6', 'runs', 'frontier.csv')
    if os.path.exists(p6):
        for r in csv.DictReader(open(p6)):
            before[r['target']] = int(float(r['n_inside']))
    rows, L = [], ['LOOP 8 — RELATIONS WIRED INTO THE SYNTHETIC GENERATOR; FRONTIER RE-RUN.',
                   f'{NDRAW} LHS draws x {NSEED} matched seeds; same targets/tolerances as loop 6; no tuning.',
                   'SYNTHETIC / POSSIBILITY ONLY; programme CLOSED; brief-008 limits stand.', '',
                   f'  {"target":18s} {"loop6 inside/256":>17s} {"loop8 inside/256":>17s} {"delta":>7s} {"shrink?":>8s}']
    after = {}
    for tname, t in TARGETS.items():
        inside = 0
        for d in range(NDRAW):
            ok = True
            if t['kind'] == 'vector':
                for i, s in enumerate(t['stages']):
                    v = means[d][f"{t['country']}_take{i + 1}"]
                    ok = ok and abs(v - t['values'][i]) <= t['tol']
            elif t['kind'] == 'scalar':
                for j, w in enumerate(t['which']):
                    v = means[d][f"{t['country']}_{w}"]
                    ok = ok and abs(v - t['values'][j]) <= t['tol'][j]
            else:
                ok = abs(means[d][f"{t['country']}_completion"] - t['values'][0]) <= t['tol'][0]
            if ok:
                inside += 1
        after[tname] = inside
        b = before.get(tname, 0)
        shrink = 'YES' if b == 0 and inside >= 1 else ('no' if b > 0 or inside == 0 else 'n/a')
        rows.append(dict(target=tname, loop6_inside=b, loop8_inside=inside, delta=inside - b, shrink=shrink))
        L.append(f'  {tname:18s} {b:17d} {inside:17d} {inside - b:+7d} {shrink:>8s}')
    write_rows(os.path.join(out, 'frontier_before_after.csv'), ['target', 'loop6_inside', 'loop8_inside', 'delta', 'shrink'],
               [[r[k] for k in ['target', 'loop6_inside', 'loop8_inside', 'delta', 'shrink']] for r in rows])
    # eps_ec arm (R13): synthetic outcomes eps in {-1.035, 0, 0.3, 0.6}
    eps_rows = []
    for eps in (-1.035, 0.0, 0.3, 0.6):
        for cname in ('PH-like', 'KHM-like'):
            for seed in range(5):
                c = dict(tw.COUNTRIES[cname]); c['s0'] = min(0.95, c['s0'] * 1.0)
                tw.REGIMES['R3_complementary']['eps_ec'] = eps
                S = tw.run_country(cname, c, 'R3_complementary', seed)
                eps_rows.append(dict(eps=eps, country=cname, seed=seed,
                                     completion=float(np.mean([x['s_t'] for x in S[-5:]]) * 100),
                                     degree_share=float(np.mean([x['C_t'] / (x['C_t'] + x['D_t'] + x['X_t']) for x in S[-5:]]) * 100),
                                     complex_jobs=float(np.mean([x['comp'] for x in S[-5:]]))))
    write_rows(os.path.join(out, 'eps_ec_arm.csv'), list(eps_rows[0].keys()), [[r[k] for k in eps_rows[0]] for r in eps_rows])
    # KOR two-margin arm (R23): joint test
    joint = part_only = inten_only = neither = 0
    for d in range(NDRAW):
        t = [means[d][f'KOR_take{i + 1}'] for i in range(3)]
        part_ok = abs(t[0] - 86.0) <= 5 and abs(t[1] - 75.4) <= 5 and abs(t[2] - 66.4) <= 5 and t[0] > t[1] > t[2]
        inten_ok = means[d]['KOR_spend_high_elem'] >= 1.15
        if part_ok and inten_ok:
            joint += 1
        elif part_ok:
            part_only += 1
        elif inten_ok:
            inten_only += 1
        else:
            neither += 1
    write_rows(os.path.join(out, 'kor_two_margin.csv'), ['metric', 'value'],
               [['joint_draws', joint], ['participation_only', part_only], ['intensity_only', inten_only], ['neither', neither]])
    # verdicts
    shrink_targets = [r['target'] for r in rows if r['shrink'] == 'YES']
    bands_zero = (after['KOR_gradient'] == 0 and after['HKG_gradient'] == 0)
    L += ['', f'EPS_EC ARM (R13; panel -1.035 rejects eps_ec>0): synthetic eps in {{-1.035, 0, 0.3, 0.6}} run; see runs/eps_ec_arm.csv.']
    eps_sum = {}
    for r in eps_rows:
        eps_sum.setdefault(r['eps'], {}).setdefault(r['country'], []).append(r)
    for eps in (-1.035, 0.0, 0.3, 0.6):
        for c in ('PH-like', 'KHM-like'):
            R = eps_sum[eps][c]
            L.append(f'  eps={eps:+.3f} {c:9s} completion {np.mean([x["completion"] for x in R]):6.2f} '
                     f'degree share {np.mean([x["degree_share"] for x in R]):5.2f} complex jobs {np.mean([x["complex_jobs"] for x in R]):7.1f}')
    L += ['', f'KOR TWO-MARGIN (R23) under wired intensity margin: joint {joint}/256; participation-only {part_only}; '
              f'intensity-only {inten_only}; neither {neither}',
          '', 'DECISION RULE (predeclared): shrink = a target 0/256 in loop 6 becomes >=1/256 in loop 8.',
          f'  shrink targets: {shrink_targets if shrink_targets else "NONE"}',
          f'  KOR/HKG stage gradients after wiring: KOR {after["KOR_gradient"]}/256, HKG {after["HKG_gradient"]}/256 -> ' +
          ('EMPTY SUPPORT PERSISTS' if bands_zero else 'empty support SHRANK for at least one stage gradient'),
          '', 'SYNTHETIC / POSSIBILITY ONLY — not evidence, not validation; programme stays CLOSED; brief-008 limits stand.']
    write_text(os.path.join(out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(label='SYNTHETIC/POSSIBILITY ONLY', before=before, after=after,
                   shrink_targets=shrink_targets, eps_arm_summary={str(k): {c: len(v) for c, v in d.items()} for k, d in eps_sum.items()},
                   two_margin=dict(joint=joint, part_only=part_only, inten_only=inten_only, neither=neither),
                   ranges=RANGES, eci='PENDING (04_data/complexity not on disk)',
                   decision='shrink = target 0/256 -> >=1/256'),
              open(os.path.join(out, 'synth_wired_meta.json'), 'w'), indent=1)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
