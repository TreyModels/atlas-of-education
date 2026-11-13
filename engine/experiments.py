"""Toy-world experiments T1-T5 (SPEC.md). Run: python experiments.py -> results/toy_worlds.txt"""
import os
from multiprocessing import Pool
import numpy as np
import worlds as W

SEEDS = (0, 1)


def job(a):
    world, mods, over = a
    return W.run(world, mods, seeds=SEEDS, **over)


CONFIGS = {
    # T1 low-pay state
    'T1_base': ('low_pay', None, {}),
    'T1_pay075': ('low_pay', None, dict(pay_ratio=0.75)),
    'T1_pay100': ('low_pay', None, dict(pay_ratio=1.0)),
    'T1_ownban': ('low_pay', None, dict(own_ban=0.9)),
    'T1_inc_base': ('low_pay', None, dict(withhold_mode='incentive')),
    'T1_inc_pay100': ('low_pay', None, dict(withhold_mode='incentive', pay_ratio=1.0)),
    'T1_notut': ('low_pay', dict(tutoring=False), {}),
    # T2 exam race
    'T2_base': ('exam_race', None, {}),
    'T2_q_scarce': ('exam_race', None, dict(vac_growth=0.0)),
    'T2_q_plenty': ('exam_race', None, dict(vac_growth=0.02)),
    'T2_c_scarce': ('exam_race', dict(labour='competitive'), dict(demand_growth=0.0)),
    'T2_c_mid': ('exam_race', dict(labour='competitive'), dict(demand_growth=0.012)),
    'T2_c_plenty': ('exam_race', dict(labour='competitive'), dict(demand_growth=0.025)),
    'T2_firmban': ('exam_race', None, dict(firm_ban=0.9)),
    'T2_firmban_ownok': ('exam_race', None, dict(firm_ban=0.9, monitoring=0.3)),
    'T2_bargates': ('exam_race', None, dict(gates=[dict(kind='bar', bar=3.0), dict(kind='bar', bar=5.5),
                                                   dict(kind='bar', bar=8.0), dict(kind='bar', bar=11.5)])),
    # T3 excess demand
    'T3_b030': ('excess_demand', None, dict(budget_per_child=0.03)),
    'T3_b045': ('excess_demand', None, {}),
    'T3_b070': ('excess_demand', None, dict(budget_per_child=0.07)),
    'T3_b100': ('excess_demand', None, dict(budget_per_child=0.10)),
    'T3_nopriv': ('excess_demand', dict(private=False), {}),
    'T3_voucher': ('excess_demand', None, dict(voucher=0.5)),
    'T3_privdear': ('excess_demand', None, dict(priv_wage=1.6)),
    # T4 formal-economy loop
    **{f'T4_e{e}_tax{tx}': ('formal_loop', None, dict(job_elasticity=e, tax_formal=tx))
       for e in (0.0, 0.5, 1.0, 1.5) for tx in (0.15, 0.25)},
    # T5 schooling is not learning: same budget, more seats per teacher
    'T5_ptr45': ('low_pay', None, dict(ptr_max=45.0)),
    'T5_ptr120': ('low_pay', None, dict(ptr_max=120.0, alpha_ptr=0.35)),
}


def f(x, d=3):
    return '[' + ' '.join(f'{v:.{d}f}' for v in x) + ']'


def main():
    os.makedirs('results', exist_ok=True)
    with Pool(os.cpu_count() or 1) as pool:
        outs = pool.map(job, list(CONFIGS.values()))
    R = dict(zip(CONFIGS, outs))
    import json
    json.dump(R, open('results/toy_worlds.json', 'w'), default=float)
    L = ['TOY WORLDS (SPEC.md expectations written before running; 2 seeds each; grades shown 1..16)', '']
    key = lambda o: (f"completion P/L/U/T {o['completion_primary']:.2f}/{o['completion_lower']:.2f}/{o['completion_upper']:.2f}/"
                     f"{o['completion_tertiary']:.2f} | MPL prim {o['mpl_primary']:.2f} | LP {o['learning_poverty']:.2f} | "
                     f"wealth parity lower {o['parity_wealth_lower']:.2f}")
    L.append('--- T1 low-pay state')
    for k in [c for c in R if c.startswith('T1')]:
        o = R[k]
        L.append(f"  {k:15s} {key(o)} | withheld {o.get('withheld', 0):.3f} | tutoring {o.get('tut_rate', 0):.2f} own-share {o.get('own_share', 0):.2f}")
        if 'tut_own_by_grade' in o:
            L.append(f"      own-teacher by grade 1-12 {f(o['tut_own_by_grade'][:12], 2)}")
            L.append(f"      firm by grade 1-16        {f(o['tut_firm_by_grade'], 2)}")
    L.append('--- T2 exam race (quota gates after Grades 9 and 12)')
    for k in [c for c in R if c.startswith('T2')]:
        o = R[k]
        q45 = np.mean(o['completion_tertiary_q'][3:])
        inc = o.get('inc_by_cred', [np.nan] * 5)
        L.append(f"  {k:17s} {key(o)} | tertiary Q4-5 {q45:.2f} | tutoring {o.get('tut_rate', 0):.2f} Q4-5 {np.mean(o['tut_by_q'][3:]):.2f} | degree income {inc[4]:.2f}")
        L.append(f"      tutoring by grade 1-16 {f(o['tut_by_grade'], 2)}  (firm {f(o['tut_firm_by_grade'], 2)})")
    L.append('--- T3 excess demand')
    for k in [c for c in R if c.startswith('T3')]:
        o = R[k]
        L.append(f"  {k:12s} {key(o)} | private {o.get('priv_share', 0):.2f} by Q {f(o.get('priv_by_q', [0]*5), 2)} | "
                 f"rationed {o['rationed_share']:.2f} | no-seat exits {o['exit_reasons']['no_seat']:.3f} | ptr {o['ptr']:.0f}")
    L.append('--- T4 formal-economy loop (FiscalState on)')
    for k in [c for c in R if c.startswith('T4')]:
        o = R[k]
        L.append(f"  {k:16s} {key(o)} | formal share of GDP {o['formal_share_gdp']:.2f} | edu/GDP {o['edu_gdp']:.3f} | ptr {o['ptr']:.0f}")
    L.append('--- T5 schooling vs learning (low-pay world, same budget)')
    for k in [c for c in R if c.startswith('T5')]:
        o = R[k]
        L.append(f"  {k:10s} {key(o)} | ptr {o['ptr']:.0f} | q_pub {o['q_pub']:.2f} | OOS primary {o['oos_primary']:.3f}")
    open('results/toy_worlds.txt', 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
