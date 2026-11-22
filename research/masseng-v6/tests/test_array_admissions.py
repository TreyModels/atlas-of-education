import json
from pathlib import Path
import numpy as np
import pytest
from masseng.array_admissions import clear_two_sector_array
from masseng.credential import CredentialModel
from masseng.data import Country
ROOT = Path(__file__).resolve().parents[1]

def test_fractional_capacity_and_proportional_rationing():
    admitted, unmet = clear_two_sector_array(np.array([[1.0, 0.0], [1.0, 0.0]]), np.array([0.5, 0.0]))
    assert np.allclose(admitted[:, 0], 0.25)
    assert np.isclose(admitted.sum(), 0.5)
    assert np.allclose(unmet, 0.75)

def test_permutation_does_not_change_cells_or_totals():
    demand = np.array([[0.2, 0.8], [0.7, 0.3], [0.5, 0.5]]); capacity = np.array([0.6, 0.4])
    admitted, unmet = clear_two_sector_array(demand, capacity); order = np.array([2, 0, 1])
    shuffled, shuffled_unmet = clear_two_sector_array(demand[order], capacity)
    assert np.allclose(shuffled, admitted[order]); assert np.allclose(shuffled_unmet, unmet[order])

def test_residual_mass_cascades_once_without_duplication():
    admitted, unmet = clear_two_sector_array(np.array([[1.0, 0.0]]), np.array([0.5, 0.5]))
    assert np.allclose(admitted, [[0.5, 0.5]]); assert np.allclose(unmet, 0.0)

def test_randomized_mass_and_capacity_invariants():
    rng = np.random.default_rng(731)
    for _ in range(100):
        demand = rng.uniform(0, 2, size=(4, 7, 2)); capacity = rng.uniform(0, 3, size=2)
        admitted, unmet = clear_two_sector_array(demand, capacity)
        assert np.all(admitted >= 0); assert np.all(admitted.sum(axis=0) <= capacity + 1e-9)
        assert np.allclose(admitted.sum(axis=-1) + unmet, demand.sum(axis=-1))

@pytest.mark.parametrize('iso', ['PHL', 'KHM'])
def test_annual_market_feeds_capacity_into_stocks_and_conserves_mass(iso):
    fit = json.loads((ROOT / f'outputs/{iso}/v3/fit_income_unconstrained.json').read_text())
    model = CredentialModel(Country(iso), params=fit['params'], supply_rule='unconstrained', split_nu=False, annual_market=True)
    result = model.run(record_deciles=True); extra = result.extra
    residual = extra['entered'] - (extra['final_enrolled'] + extra['drops'] + extra['grads'].sum(axis=2) + extra['aged'] + extra['pending'])
    assert np.allclose(residual, 0, atol=1e-9); markets = extra['markets']
    assert np.all(markets['admitted'] <= markets['effective_at_cost'] + 1e-7)
    assert np.allclose(markets['effective_at_cost'] - markets['admitted'], markets['unmet_effective'], atol=1e-6)
    assert markets['capacity_public'].sum() > 0; assert markets['capacity_private'].sum() > 0
    assert np.any(np.isclose(markets['admitted_public'].sum(axis=2), markets['capacity_public'].sum(axis=2)))
    assert np.all(np.isfinite(result.ind['ger_tertiary']))

@pytest.mark.parametrize('iso', ['PHL', 'KHM'])
def test_annual_market_off_preserves_default_run_exactly(iso):
    fit = json.loads((ROOT / f'outputs/{iso}/v3/fit_income_unconstrained.json').read_text())
    default = CredentialModel(Country(iso), params=fit['params'], supply_rule='unconstrained', split_nu=False).run()
    explicit_off = CredentialModel(Country(iso), params=fit['params'], supply_rule='unconstrained', split_nu=False, annual_market=False).run()
    for key in default.ind: assert np.allclose(default.ind[key], explicit_off.ind[key], equal_nan=True)
