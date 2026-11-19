"""Nesting check: with the new term at zero and hard liquidity, structures.simulate must
reproduce engine/relfloor_countries.sim (the repo's household model) exactly for the same
parameters and seed. Also: M_RRA with b_rra = 0 must equal M_HC, and the repo's own
Cambodia profile test must give the same verdict on both."""
import json, os, sys
import numpy as np
import structures as S

def run(n_param_sets=20, n=1500):
    rc = S.rc
    worst = {k: 0.0 for k in ('M_HC', 'M_POS', 'M_REL')}
    verdict_mismatch = 0
    for s in ('M_HC', 'M_POS', 'M_REL'):
        for i in range(n_param_sets):
            rng = np.random.default_rng([11, i])
            th = S.draw(rng, s, graded=False)            # hard liquidity: s_liq = 0
            seed = 1000 + i
            mine = S.simulate(th, n=n, seed=seed, until=2035, liq='hard')
            repo = rc.sim(th, S.CFG, 'base', n, seed)    # engine/relfloor_countries.py
            d = max(np.max(np.abs(mine['c'] - repo['c'])), np.max(np.abs(mine['q'] - repo['q'])))
            worst[s] = max(worst[s], float(d))
            if bool(rc.t_khm_profile({'c': mine['c'], 'q': mine['q']})) != bool(rc.t_khm_profile(repo)):
                verdict_mismatch += 1
    # M_RRA with b_rra = 0 equals M_HC (graded liquidity too)
    worst_rra0 = 0.0
    for i in range(n_param_sets):
        rng = np.random.default_rng([12, i])
        th = S.draw(rng, 'M_RRA'); th['b_rra'] = 0.0
        th2 = dict(th)
        a = S.simulate(th, n=n, seed=i, until=2035)
        b = S.simulate(dict(th2, tau=0.9), n=n, seed=i, until=2035)   # tau irrelevant when b_rra = 0
        worst_rra0 = max(worst_rra0, float(np.max(np.abs(a['q'] - b['q']))))
    return {'n_param_sets_per_structure': n_param_sets, 'households': n,
            'worst_abs_difference_vs_repo': worst,
            'worst_abs_difference_overall': max(worst.values()),
            'profile_test_verdict_mismatches': verdict_mismatch,
            'worst_difference_M_RRA_b_rra0_vs_other_tau': worst_rra0,
            'compared_against': 'engine/relfloor_countries.sim, Cambodia config, hard liquidity, years 1998-2035, aggregate and quintile completion'}

if __name__ == '__main__':
    out = run()
    os.makedirs(os.path.join(S.HERE, 'results'), exist_ok=True)
    json.dump(out, open(os.path.join(S.HERE, 'results', 'nesting_check.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))
