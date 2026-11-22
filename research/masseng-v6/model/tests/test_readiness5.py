import copy
import math

import numpy as np
import pytest

import masseng as m
from masseng import calibrate5 as C
from masseng.readiness5 import audit, assert_ready


@pytest.mark.parametrize('iso', ['PHL', 'KHM'])
def test_registered_inputs_pass_preflight(iso):
    report = assert_ready(m.Country(iso))
    assert report['train_rows'] > 0 and report['test_rows'] > 0
    assert report['errors'] == []


def test_phl_registered_targets_and_roles():
    rows = C.build_rows(m.Country('PHL'))
    train = [r for r in rows if r['role'] == 'train']
    test = [r for r in rows if r['role'] == 'test']
    assert sum(r['series'] == 'edu_share_hh' for r in train) == 2
    assert sum(r['series'] == 'hh_share_total_spending' for r in test) == 6
    ched = [r for r in test if r['series'] == 'enrol_tertiary' and r.get('transform') == 'index_2016']
    assert len(ched) == 5
    assert math.isclose(next(r['value'] for r in ched if r['year'] == 2016), 1.0)
    assert not any(r['year'] == 2023 and r['series'] == 'edu_share_hh' for r in rows)
    assert any(r['series'] == 'trans_lsec_usec' and r['year'] == 2018 and r['value'] == 93.3 for r in test)


def test_missing_driver_fails_instead_of_becoming_zero():
    c = m.Country('PHL')
    c.config = copy.deepcopy(c.config)
    c.config['v5']['driver_map']['relational'] = 'does_not_exist'
    report = audit(c)
    assert not report['ready']
    assert any('missing mapped driver' in e for e in report['errors'])


def test_percent_premium_fails_unit_check():
    c = m.Country('KHM')
    c.config = copy.deepcopy(c.config)
    c.config['v5']['driver_map']['premium_tertiary'] = 'premium_tertiary_annualised_wb'
    report = audit(c)
    assert not report['ready']
    assert any('requires log points' in e for e in report['errors'])


def test_transition_prediction_uses_registered_percent_units():
    res = type('Result', (), {})()
    res.years = np.array([2018])
    res.ind = {'trans_lsec_usec': np.array([0.88])}
    rows = [{'series': 'trans_lsec_usec', 'year': 2018}]
    assert C._pred(res, rows)[0] == pytest.approx(88.0)
