"""Plain-assert tests. Run:  python3 test_structures.py"""
import numpy as np
import structures as S
import nesting_check, recovery

def test_nesting():
    out = nesting_check.run(n_param_sets=5, n=800)
    assert out['worst_abs_difference_overall'] < 1e-12, out
    assert out['profile_test_verdict_mismatches'] == 0
    assert out['worst_difference_M_RRA_b_rra0_vs_other_tau'] < 1e-12

def test_determinism():
    th = S.draw(np.random.default_rng(3), 'M_RRA')
    a = S.simulate(th, n=800, seed=5); b = S.simulate(th, n=800, seed=5); c = S.simulate(th, n=800, seed=6)
    assert np.array_equal(a['q'], b['q']) and not np.array_equal(a['q'], c['q'])

def test_structure_restrictions():
    rng = np.random.default_rng(0)
    th = S.draw(rng, 'M_HC'); assert th['b_pos'] == th['b_rel'] == th['b_rra'] == 0
    th = S.draw(rng, 'M_POS'); assert th['b_rel'] == th['b_rra'] == 0 and th['b_pos'] > 0
    th = S.draw(rng, 'M_REL'); assert th['b_rra'] == 0 and th['b_rel'] > 0
    th = S.draw(rng, 'M_RRA'); assert th['b_pos'] == th['b_rel'] == 0 and 0 < th['b_rra'] and 0.3 <= th['tau'] <= 0.9

def test_rra_term_acts_on_rich_not_poor():
    th = S.draw(np.random.default_rng(1), 'M_RRA'); th.update(b_rra=0.8, tau=0.6)
    th0 = dict(th, b_rra=0.0)
    d = S.simulate(th, n=4000, seed=1)['q'][S.yi(2021)] - S.simulate(th0, n=4000, seed=1)['q'][S.yi(2021)]
    assert d[4] > d[0] and d[4] > 0

def test_early_stop_equals_full_verdict():
    rng = np.random.default_rng(8); chk = S.early_checkpoints(); agree = 0; passed = 0
    for i in range(400):
        th = S.draw(rng, 'M_HC')
        full = S.real_observed_matches(S.simulate(th, n=1500, seed=i, until=2021))
        early = S.simulate(th, n=1500, seed=i, until=2021, checkpoints=chk) is not None
        agree += (full == early); passed += full
    assert agree == 400

def test_recovery_tiny():
    res = recovery.run(N=250, K=1, n=800, tol_scales=(1.0,))
    sm = res['summary']['1.0']
    assert len(res['datasets']) == 4
    for s in S.STRUCTS:
        row = sm['confusion_mean_posterior'][s]
        if row[S.STRUCTS[0]] is not None:
            assert abs(sum(row.values()) - 1) < 1e-9

if __name__ == '__main__':
    for name, f in list(globals().items()):
        if name.startswith('test_'):
            f(); print('ok', name)
    print('all tests passed')
