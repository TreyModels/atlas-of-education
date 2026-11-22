"""Checks that do not depend on fitted values. Run: python3 -m pytest -q tests  (or python3 tests/test_model.py)"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import masseng as m
from masseng import targets as T, calibrate as C
from masseng.engine import Model


def _country(iso='PHL'):
    return m.Country(iso)


def test_stock_flow_conservation():
    """Every child who enters Grade 1 is, at the end, either enrolled, a dropout, a completer of some level,
    or censored at max_age. Checked for every cohort and decile."""
    c = _country()
    for rule in ('fiscal', 'responsive', 'unconstrained'):
        r = Model(c, supply_rule=rule).run()
        e = r.extra
        lhs = e['entered']
        rhs = e['final_enrolled'] + e['drops'] + e['grads'].sum(axis=2) + e['aged']
        assert np.allclose(lhs, rhs, atol=1e-12), (rule, np.abs(lhs - rhs).max())


def test_deterministic():
    c = _country()
    a = Model(c).run().ind['ger_tertiary']
    b = Model(c).run().ind['ger_tertiary']
    assert np.array_equal(a, b)


def test_upper_secondary_only_after_reform():
    """No Grade 11-12 enrolment before the reform year; Grade 11 appears in the reform year itself."""
    c = _country()
    r = Model(c).run()
    yrs = list(r.years)
    shs = c.config['structure']['upper_secondary_from']
    priv_us = r.ind['priv_upper_secondary']
    assert np.all(np.isnan(priv_us[:yrs.index(shs)]))
    assert not np.isnan(priv_us[yrs.index(shs)])


def test_k12_creates_tertiary_entry_gap():
    """With the reform, first-year tertiary entry falls sharply in the two transition years (the cohort is in
    Grades 11-12) compared with the same model without the reform."""
    c = _country()
    with_r = Model(c).run()
    c2 = _country()
    c2.config['structure']['upper_secondary_from'] = 10 ** 6
    no_r = Model(c2).run()
    yrs = list(with_r.years)
    for y in (2017, 2018):
        i = yrs.index(y)
        assert with_r.ind['ger_tertiary'][i] < 0.8 * no_r.ind['ger_tertiary'][i]
    i = yrs.index(2015)
    assert abs(with_r.ind['ger_tertiary'][i] - no_r.ind['ger_tertiary'][i]) < 1e-9


def test_fit_rejects_test_rows():
    """The fitting function refuses any row that is not a training row (protocol, section 5)."""
    c = _country()
    rows = T.build(c)
    bad = T.train_rows(rows) + T.test_rows(rows)[:1]
    try:
        C.fit(c, bad, max_nfev=1)
    except AssertionError:
        return
    raise AssertionError('fit accepted a test row')


def test_train_test_split_by_year():
    c = _country()
    lo, hi = c.config['years']['train']
    for r in T.build(c):
        if r['role'] == 'train' and not r['series'].startswith('gradlr_'):
            assert lo <= r['year'] <= hi
        if r['role'] == 'test':
            assert r['year'] > hi


def test_indicator_bands_follow_wdi_definitions():
    """GER denominators use the official entrance age and durations reported in WDI for that year."""
    c = _country()
    mod = Model(c)
    assert mod.band[1990]['primary'] == (7, 13)
    assert mod.band[2000]['primary'] == (6, 12)
    assert mod.band[2016]['secondary'] == (12, 16)
    assert mod.band[2018]['secondary'] == (12, 18)
    assert mod.band[2018]['tertiary'] == (18, 23)


def test_policy_switch_changes_only_after_event():
    """Turning policies off leaves every indicator unchanged before the first policy year."""
    c = _country()
    a = Model(c).run()
    b = Model(c, switches=dict(policies=False)).run()
    first = min(ev['year'] for ev in c.config['policy_events'])
    yrs = list(a.years)
    for k in ('ger_secondary', 'ger_tertiary', 'priv_secondary'):
        i = yrs.index(first) - 1
        assert np.allclose(a.ind[k][:i], b.ind[k][:i], equal_nan=True)


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print('ok', name)
