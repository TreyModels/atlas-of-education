import pytest

from masseng_v6.core.runner import run_admissions_year
from masseng_v6.core.state import CohortCell, CohortKey, CohortState, EducationStatus
from masseng_v6.education.admissions import Applicant, clear_admissions
from masseng_v6.education.institutions import Market


def market(mid="public", capacity=1, reserved=0, region="urban"):
    return Market(mid, region, "tertiary", "public" if mid == "public" else "private", capacity, reserved)


def test_multiple_preferences_never_duplicate_mass():
    allocation = clear_admissions([Applicant("a", ("public", "private")), Applicant("b", ("public", "private"))], [market("public", 1), market("private", 1)])
    assert all(sum(v.values()) <= 1 for v in allocation.assignments.values())
    assert sum(v.get("public", 0) for v in allocation.assignments.values()) == 1
    assert sum(v.get("private", 0) for v in allocation.assignments.values()) == 1
    assert allocation.funnel.qualified == 2
    assert allocation.funnel.realized == 2


def test_fractional_seat_admits_fractional_expected_mass_not_a_whole_person():
    result = clear_admissions([Applicant("cell", ("public",), mass=1)], [market(capacity=0.5)])
    assert result.assignments["cell"]["public"] == 0.5
    assert result.funnel.realized == 0.5
    assert result.unmet_effective_demand == 0.5


def test_proportional_rationing_does_not_depend_on_alphabetical_id():
    people = [Applicant("aa_rich", ("public",)), Applicant("zz_poor", ("public",))]
    result = clear_admissions(people, [market(capacity=1)])
    assert result.assignments == {"aa_rich": {"public": 0.5}, "zz_poor": {"public": 0.5}}
    assert result.assignments == clear_admissions(list(reversed(people)), [market()]).assignments


def test_proportional_rationing_respects_cell_mass():
    people = [Applicant("small", ("public",), mass=0.25), Applicant("large", ("public",), mass=0.75)]
    result = clear_admissions(people, [market(capacity=0.5)])
    assert result.assignments["small"]["public"] == pytest.approx(0.125)
    assert result.assignments["large"]["public"] == pytest.approx(0.375)


def test_residual_mass_cascades_without_exceeding_original_mass():
    result = clear_admissions([Applicant("a", ("public", "private"), mass=1), Applicant("b", ("public",), mass=1)], [market("public", 1), market("private", 1)])
    assert result.assignments["a"] == {"public": 0.5, "private": 0.5}
    assert result.assignments["b"] == {"public": 0.5}
    assert result.funnel.realized == pytest.approx(1.5)


def test_zero_capacity_and_unlimited_capacity_limiting_cases():
    people = [Applicant(str(i), ("public",)) for i in range(4)]
    zero = clear_admissions(people, [market(capacity=0)])
    assert zero.funnel.realized == 0
    assert zero.unmet_effective_demand == 4
    enough = clear_admissions(people, [market(capacity=4)])
    assert enough.funnel.realized == 4
    assert enough.unmet_effective_demand == 0


def test_continuing_students_reduce_new_entrant_seats():
    result = clear_admissions([Applicant("a", ("public",)), Applicant("b", ("public",))], [market(capacity=5, reserved=4)])
    assert result.funnel.realized == 1
    assert result.markets[0].continuing_reserved == 4
    assert result.markets[0].places_open == 1


def test_inaccessible_empty_seat_is_not_accessible_empty():
    result = clear_admissions([Applicant("rural", ("urban_public",))], [market("urban_public", 2, region="urban"), Market("rural_private", "rural", "tertiary", "private", 3)])
    rural = next(m for m in result.markets if m.market_id == "rural_private")
    assert rural.empty_seats == 3
    assert rural.accessible_empty_seats == 0


def test_reachable_but_unwanted_seat_counts_as_accessible_empty():
    result = clear_admissions([Applicant("a", ("public",), accessible_markets=("public", "private"))], [market("public", 1), market("private", 2)])
    private = next(m for m in result.markets if m.market_id == "private")
    assert private.empty_seats == 2
    assert private.accessible_empty_seats == 2


def test_cost_exclusion_preserves_latent_demand():
    result = clear_admissions([Applicant("poor", ("public",), effective=False), Applicant("rich", ("public",))], [market(capacity=2)])
    assert (result.funnel.qualified, result.funnel.latent_zero_cost, result.funnel.effective, result.funnel.realized) == (2, 2, 1, 1)


def test_net_negative_cost_subsidy_can_make_effective_exceed_zero_cost_willing():
    result = clear_admissions([Applicant("transfer_recipient", ("public",), latent_willing=True, effective=True)], [market(capacity=1)])
    assert result.funnel.effective <= result.funnel.latent_zero_cost
    assert result.funnel.realized == 1


def test_duplicate_applicant_ids_and_markets_fail_closed():
    with pytest.raises(ValueError):
        clear_admissions([Applicant("a", ("public",)), Applicant("a", ("public",))], [market()])
    with pytest.raises(ValueError):
        clear_admissions([], [market(), market()])


def test_unknown_market_and_invalid_nested_funnel_fail_closed():
    with pytest.raises(ValueError):
        clear_admissions([Applicant("a", ("missing",))], [market()])
    with pytest.raises(ValueError):
        Applicant("a", ("public",), latent_willing=False, effective=True)
    with pytest.raises(ValueError):
        Applicant("a", ("private",), accessible_markets=("public",))


def test_annual_adapter_conserves_fractional_stocks_and_defers_unplaced():
    source_a = CohortKey("PHL", 2006, 1, "urban", "tertiary", 12, "none", EducationStatus.QUALIFIED_WAITING)
    source_b = CohortKey("PHL", 2006, 2, "urban", "tertiary", 12, "none", EducationStatus.QUALIFIED_WAITING)
    target_a = CohortKey("PHL", 2006, 1, "urban", "tertiary", 12, "public", EducationStatus.ATTENDING)
    target_b = CohortKey("PHL", 2006, 2, "urban", "tertiary", 12, "public", EducationStatus.ATTENDING)
    state = CohortState([CohortCell(source_a, 1), CohortCell(source_b, 1)])
    result = run_admissions_year(state, {"a": source_a, "b": source_b}, [Applicant("a", ("public",)), Applicant("b", ("public",))], [market(capacity=1)])
    assert result.state.total == 2
    assert result.state.count(target_a) == 0.5
    assert result.state.count(target_b) == 0.5
    assert result.state.count(source_a) == 0.5
    assert result.state.count(source_b) == 0.5
    assert result.stock_ledger.residual == 0
