"""Invariants for engine5 (PROTOCOL_v5). Run: python3 tests/test_engine5.py"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import masseng as m
from masseng.engine5 import Model5, SPECS
from masseng import calibrate5 as C5


def _c(iso='PHL'):
    return m.Country(iso)


def test_conservation_all_specs():
    c = _c()
    for spec in SPECS:
        r = Model5(c, dict(b_h=1, b_p=1, b_r=1, lam=1, eta=1), spec=spec).run()
        e = r.extra
        rhs = e['final_enrolled'] + e['drops'] + e['grads'].sum(axis=2) + e['aged'] + e['final_pool']
        assert np.allclose(e['entered'], rhs, atol=1e-12), spec


def test_spec_switches_terms_off():
    c = _c()
    r = Model5(c, dict(b_h=2, b_p=2, b_r=2, lam=2, eta=2), spec='R2')
    assert r.p['b_p'] == 0 and r.p['b_r'] == 0 and r.p['lam'] == 0 and r.p['eta'] == 0 and r.p['b_h'] == 2
    r0 = Model5(c, dict(b_h=2, eta=1), spec='R0')
    assert r0.p['b_h'] == 0 and r0.p['eta'] == 1


def test_set_params_matches_fresh_model():
    c = _c()
    prm = dict(b_h=1.5, b_p=0.7, b_r=2.0, lam=0.5, kappa=4.0)
    a = Model5(c, {}, spec='R1').set_params(prm).run().ind['ger_tertiary']
    b = Model5(c, prm, spec='R1').run().ind['ger_tertiary']
    assert np.allclose(a, b, equal_nan=True)


def test_deferred_entry_raises_k12_trough_enrolment():
    c = _c()
    on = Model5(c, dict(h_def=0.3), spec='R1').run()
    off = Model5(c, dict(h_def=0.3), spec='R1', switches=dict(deferred=False)).run()
    i = list(on.years).index(2018)
    assert on.ind['ger_tertiary'][i] > off.ind['ger_tertiary'][i]


def test_positional_share_rises_with_b_p():
    """More positional pull -> higher secondary completion share among 20-29 year-olds by 2010."""
    c = _c()
    lo = Model5(c, dict(b_p=0.0), spec='R1').run()
    hi = Model5(c, dict(b_p=3.0), spec='R1').run()
    i = list(lo.years).index(2010)
    assert hi.ind['S_secondary'][i] > lo.ind['S_secondary'][i]


def test_lambda_reduces_cost_sensitivity():
    """With lam > 0 a fee cut moves participation less (cost sensitivity falls with saturation)."""
    c = _c()
    def effect(lam):
        a = Model5(c, dict(lam=lam, kappa=5.0), spec='R1').run()
        b = Model5(c, dict(lam=lam, kappa=5.0), spec='R1', switches=dict(policies=False)).run()
        i = list(a.years).index(1992)
        return a.ind['ger_secondary'][i] - b.ind['ger_secondary'][i]
    assert effect(3.0) < effect(0.0)


def test_spending_outputs_bounded():
    c = _c()
    r = Model5(c, {}, spec='R1').run()
    for k in ('edu_share_hh', 'edu_share_bottom30', 'edu_share_top70', 'hh_share_total_spending'):
        v = r.ind[k][~np.isnan(r.ind[k])]
        assert np.all(v >= 0) and np.all(v <= 100), k


def test_fit_rejects_test_rows():
    c = _c()
    rows = C5.build_rows(c)
    bad = [r for r in rows if r['role'] == 'train'] + [r for r in rows if r['role'] == 'test'][:1]
    try:
        C5.fit(c, bad, 'R1', max_nfev=1)
    except AssertionError:
        return
    raise AssertionError('fit accepted a test row')


if __name__ == '__main__':
    for n, f in list(globals().items()):
        if n.startswith('test_'):
            f(); print('ok', n)
