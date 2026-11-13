"""Tilly's four mechanisms, one at a time and together, on the headline China parameters.

Run from engine/:  python -m firms.tilly_experiments   -> firms/results/tilly.{md,json}
Mechanism values are illustrative settings chosen from the ranges discussed in the doc, not estimates. The point is
what each mechanism does to the measured outcomes, conditional on the whole-record fit of model.py.
"""
import json, math, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import categorical as C, data_china as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
SECURE = dict(sec_open=0.10, hoard=0.0)                 # 10% of a graduate cohort can enter secure posts each year
SCEN = [
    ('No mechanism (model.py)', {}),
    ('Secure posts, open exam only', dict(SECURE)),
    ('Opportunity hoarding: 40% of secure posts to insiders', dict(SECURE, hoard=0.4)),
    ('+ Adaptation: waiting for posts', dict(SECURE, hoard=0.4, wait_max=0.06)),
    ('Emulation: degree requirements spread', dict(em_rate=0.5)),
    ('Exploitation: 20% wedge on outsiders', dict(ex=0.2)),
    ('All four', dict(SECURE, hoard=0.4, wait_max=0.06, em_rate=0.5, ex=0.2)),
]
EARLY, LATE = ((2018, 1), (2019, 12)), ((2024, 1), (2026, 9))


def wm(R, k, a, b):
    v = [x for x, y, m in zip(R[k], R['year'], R['month']) if a <= (y, m) <= b]
    v = [x for x in v if x == x]
    return float(np.mean(v)) if v else float('nan')


def main():
    h = json.load(open(os.path.join(OUT, 'china_fit.json')))['profiles']['full|sigma_A=5.0']['params']
    res = {}
    for name, over in SCEN:
        R = C.CategoricalMarket(D, **h, **over).run()
        L = lambda k: wm(R, k, *LATE); E = lambda k: wm(R, k, *EARLY)
        res[name] = dict(
            rate_early=E('rate_new'), rate_late=L('rate_new'), slack_late=L('slack'),
            uG_in=L('u_G_in'), uG_out=L('u_G_out'), uN_in=L('u_N_in'), uN_out=L('u_N_out'),
            w_gap_G=L('w_G_in') / L('w_G_out') - 1 if L('w_G_out') > 0 else float('nan'),
            w_gap_N=L('w_N_in') / L('w_N_out') - 1 if L('w_N_out') > 0 else float('nan'),
            waiting_m=L('waiting'), sec_ins_share=L('sec_ins_share'), c_req_late=L('c_req'), under_late=L('under'),
            grad_share_n_hires=L('grad_share_n_hires'), V_n_change=100 * (L('V_n') / E('V_n') - 1),
            output_late=L('output'), rent_exploit=L('rent_exploit'), rent_hoard=L('rent_hoard'),
            max_balance=float(max(abs(b) for b in R['balance'])))
    base_out = res[SCEN[0][0]]['output_late']
    for v in res.values():
        v['output_vs_base_pct'] = 100 * (v['output_late'] / base_out - 1)
    json.dump(res, open(os.path.join(OUT, 'tilly.json'), 'w'), indent=1)
    L = ['# Tilly mechanisms on the headline China parameters', '',
         'Late period = Jan 2024 - Sep 2026, new NBS definition. Insiders = half of each entering group. "Slack" adds '
         'graduates waiting outside the labour force to the unemployed.', '',
         '| Scenario | Youth rate | Slack | Grad u, insiders | Grad u, outsiders | Non-grad u, in / out | Insider share of secure hires | '
         'Waiting (m) | Degree-only share of non-grad vacancies | Insider wage premium, non-grads | Output vs no mechanism |',
         '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for n, v in res.items():
        L.append(f"| {n} | {v['rate_late']:.1f} | {v['slack_late']:.1f} | {v['uG_in']:.1f} | {v['uG_out']:.1f} | "
                 f"{v['uN_in']:.1f} / {v['uN_out']:.1f} | {v['sec_ins_share']:.2f} | {v['waiting_m']:.2f} | {v['c_req_late']:.2f} | "
                 f"{100 * v['w_gap_N']:+.0f}% | {v['output_vs_base_pct']:+.1f}% |")
    open(os.path.join(OUT, 'tilly.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
