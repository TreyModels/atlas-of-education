import pytest

from masseng_v6.core.runner import run_admissions_year
from masseng_v6.core.state import CohortCell, CohortKey, CohortState, EducationStatus
from masseng_v6.education.admissions import Applicant, clear_admissions
from masseng_v6.education.institutions import Market


def market(mid="public", capacity=1, reserved=0, region="urban"):
    return Market(mid, region, "tertiary", "public" if mid == "public" else "private", capacity, reserved)


def test_multiple_preferences_never_duplicate_a_person():
    allocation = clear_admissions(
        [Applicant("a", ("public", "private")), Applicant("b", ("public", "private"))],
        [market("public", 1), market("private", 1)],
    )
    assert allocation.assignments == {"a": "public", "b": "private"}
    assert allocation.funnel.qualified == 2
    assert allocation.funnel.realized == 2


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


def test_inaccessible_empty_seat_is_not_accessible_empty_or_met_demand():
    result = clear_admissions(
        [Applicant("rural", ("urban_public",))],
        [market("urban_public", 2, region="urban"), Market("rural_private", "rural", "tertiary", "private", 3)],
    )
    assert result.funnel.realized == 1
    rural = next(m for m in result.markets if m.market_id == "rural_private")
    assert rural.empty_seats == 3
    assert rural.accessible_empty_seats == 0


def test_cost_exclusion_preserves_latent_demand():
    result = clear_admissions(
        [Applicant("poor", ("public",), effective=False), Applicant("rich", ("public",))],
        [market(capacity=2)],
    )
    assert (result.funnel.qualified, result.funnel.latent_zero_cost, result.funnel.effective, result.funnel.realized) == (2, 2, 1, 1)


def test_duplicate_applicant_ids_and_markets_fail_closed():
    with pytest.raises(ValueError):
        clear_admissions([Applicant("a", ("public",)), Applicant("a", ("public",))], [market()])
    with pytest.raises(ValueError):
        clear_admissions([], [market(), market()])


def test_unknown_market_and_invalid_nested_funnel_fail_closed():
    with pytest.raises(ValueError):
        clear_admissions([Applicant("a", ("missing",))], [market()])
    with pytest.raises(ValueError):
        Applicant("a", ("public",), zero_cost_willing=False, effective=True)


def test_ties_are_stable_and_do_not_depend_on_input_order():
    people = [Applicant("b", ("public",)), Applicant("a", ("public",))]
    first = clear_admissions(people, [market()])
    second = clear_admissions(list(reversed(people)), [market()])
    assert first.assignments == second.assignments == {"a": "public"}


def test_annual_adapter_conserves_stocks_and_defers_unplaced():
    source_a = CohortKey("PHL", 2006, 1, "urban", "tertiary", 12, "none", EducationStatus.QUALIFIED_WAITING)
    source_b = CohortKey("PHL", 2006, 2, "urban", "tertiary", 12, "none", EducationStatus.QUALIFIED_WAITING)
    target = CohortKey("PHL", 2006, 1, "urban", "tertiary", 12, "public", EducationStatus.ATTENDING)
    state = CohortState([CohortCell(source_a, 1), CohortCell(source_b, 1)])
    result = run_admissions_year(
        state,
        {"a": source_a, "b": source_b},
        [Applicant("a", ("public",)), Applicant("b", ("public",))],
        [market()],
    )
    assert result.state.total == 2
    assert result.state.count(target) == 1
    assert result.state.count(source_b) == 1
    assert result.stock_ledger.residual == 0
