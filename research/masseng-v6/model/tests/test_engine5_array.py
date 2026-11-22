"""Fractional admissions and Q/L/E/R accounting for Opus's engine5."""
import copy

import numpy as np
import pytest

import masseng as m
from masseng.array_admissions import clear_two_sector_array
from masseng.engine5 import LEVEL_NAMES, Model5, SPECS


def _country(iso='PHL', seats=1_000.0):
    c = m.Country(iso)
    c.config = copy.deepcopy(c.config)
    c.config['v5']['annual_capacity'] = {
        name: {'public': seats, 'private': seats / 2} for name in LEVEL_NAMES
    }
    return c


def _residual(result):
    e = result.extra
    return e['entered'] - (e['final_enrolled'] + e['drops'] + e['grads'].sum(axis=2)
                           + e['aged'] + e['final_pool'])


def test_fractional_half_seat_and_proportional_rationing():
    admitted, unmet = clear_two_sector_array(np.array([[1., 0.], [1., 0.]]), np.array([.5, 0.]))
    assert np.allclose(admitted[:, 0], .25)
    assert np.allclose(unmet, .75)


def test_permutation_invariance_and_single_cascade():
    demand = np.array([[1., 0.], [.2, .8], [.7, .3]])
    capacity = np.array([.6, .4])
    admitted, unmet = clear_two_sector_array(demand, capacity)
    order = np.array([2, 0, 1])
    shuffled, shuffled_unmet = clear_two_sector_array(demand[order], capacity)
    assert np.allclose(shuffled, admitted[order])
    assert np.allclose(shuffled_unmet, unmet[order])
    single, residual = clear_two_sector_array(np.array([[1., 0.]]), np.array([.5, .5]))
    assert np.allclose(single, [[.5, .5]]) and np.allclose(residual, 0.)


def test_default_off_preserves_every_original_indicator_for_all_specs():
    c = m.Country('PHL')
    params = dict(b_h=1., b_p=1., b_r=1., lam=1., eta=1.)
    for spec in SPECS:
        implicit = Model5(c, params, spec=spec).run()
        explicit = Model5(c, params, spec=spec, annual_market=False).run()
        for key in implicit.ind:
            assert np.allclose(implicit.ind[key], explicit.ind[key], equal_nan=True), (spec, key)
        assert np.allclose(_residual(implicit), 0., atol=1e-12)


@pytest.mark.parametrize('spec', list(SPECS))
def test_annual_market_conserves_mass_and_funnel(spec):
    result = Model5(_country(), dict(b_h=1., b_p=1., b_r=1., lam=1., eta=1.),
                    spec=spec, annual_market=True).run()
    mk = result.extra['markets']
    assert np.allclose(_residual(result), 0., atol=1e-3), spec
    assert np.all(mk['Q'] >= mk['L'] - 1e-7)
    assert np.all(mk['L'] >= mk['E'] - 1e-7)
    assert np.all(mk['E'] >= mk['R'] - 1e-7)
    assert np.allclose(mk['E'] - mk['R'], mk['unmet_effective'], atol=1e-6)
    assert np.all(mk['R'] >= 0) and np.any(mk['R'] > 0)
    assert np.all(mk['admitted_by_sector'].sum(axis=2) <= mk['capacity'].sum(axis=2) + 1e-6)


def test_net_negative_transfer_has_ordered_latent_demand():
    c = _country()
    c.config['transfers'] = [dict(year=1940, levels=['tertiary'], deciles=[0], value=100.)]
    result = Model5(c, annual_market=True).run()
    mk = result.extra['markets']
    assert np.all(mk['L'][:, 3, 0] >= mk['E'][:, 3, 0] - 1e-7)
    assert np.all(mk['Q'][:, 3, 0] >= mk['L'][:, 3, 0] - 1e-7)


def test_unadmitted_new_completers_remain_in_deferral_pool():
    c = _country(seats=1000.)
    # No tertiary places: all qualified secondary completers must be retained until expiry.
    c.config['v5']['annual_capacity']['tertiary'] = {'public': 0., 'private': 0.}
    result = Model5(c, dict(h_def=.3), annual_market=True).run()
    assert np.allclose(_residual(result), 0., atol=1e-3)
    assert result.extra['markets']['R'][:, 3].sum() == 0.
    assert result.extra['final_pool'].sum() > 0.


@pytest.mark.parametrize('iso', ['PHL', 'KHM'])
def test_country_annual_runs_are_finite_and_conserved(iso):
    result = Model5(_country(iso), annual_market=True).run()
    assert np.isfinite(result.ind['ger_tertiary']).all()
    assert np.allclose(_residual(result), 0., atol=1e-3)
