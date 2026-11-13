"""Checks from SPEC.md. Run: python checks.py"""
import numpy as np
import eduengine as ee
import worlds as W


def main():
    L = ['CHECKS']
    # 1. accounting
    E = W.make('excess_demand'); E.run()
    over = max(np.array(E.R['pub_spend']) - np.array(E.R['pub_budget']))
    capneg = min(E.R['priv_cap'])
    ids = len(E.X['cohort'])
    L.append(f"1. public spend <= budget (max excess {over:.6f}); private capacity >= 0 (min {capneg:.1f}); "
             f"exited records {ids} <= children created {E.p['N'] * E.p['T']} -> {'PASS' if over <= 1e-9 and capneg >= 0 and ids <= E.p['N'] * E.p['T'] else 'FAIL'}")
    # 2. core alone
    E = ee.build([], N=800, T=50, measure_from=20); o = E.run()
    L.append(f"2. core alone runs: primary completion {o['completion_primary']:.3f}, lower {o['completion_lower']:.3f} -> {'PASS' if 0 < o['completion_primary'] <= 1 else 'FAIL'}")
    # 3. no withholding -> no own-teacher buy-back value beyond tutoring effect: check h = 0 when pay parity
    E = W.make('low_pay', pay_ratio=1.0); o = E.run()
    L.append(f"3. pay parity -> withheld share {o['withheld']:.3f} -> {'PASS' if o['withheld'] == 0 else 'FAIL'}")
    # 4. full firm ban -> no firm tutoring
    E = W.make('exam_race', firm_ban=1.0); o = E.run()
    L.append(f"4. full firm ban -> firm tutoring max {max(o['tut_firm_by_grade']):.3f} -> {'PASS' if max(o['tut_firm_by_grade']) == 0 else 'FAIL'}")
    # 5. reproducible
    a = W.make('low_pay', seed=3).run(); b = W.make('low_pay', seed=3).run()
    L.append(f"5. same seed reproduces -> {'PASS' if a['completion_lower'] == b['completion_lower'] and a['tut_rate'] == b['tut_rate'] else 'FAIL'}")
    # 6. no gate failures with bar = -inf
    g = [dict(kind='bar', bar=-1e9)] * 4
    E = W.make('low_pay', gates=g); o = E.run()
    L.append(f"6. bars at -inf -> gate failures {o['exit_reasons']['gate_fail']:.4f} -> {'PASS' if o['exit_reasons']['gate_fail'] == 0 else 'FAIL'}")
    print('\n'.join(L))
    open('results/checks.txt', 'w').write('\n'.join(L) + '\n')
    return not any('FAIL' in line for line in L)


if __name__ == '__main__':
    import os, sys; os.makedirs('results', exist_ok=True); sys.exit(0 if main() else 1)
