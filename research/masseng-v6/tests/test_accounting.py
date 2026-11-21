from dataclasses import replace

import pytest

from masseng_v6.core.ledger import EntryFunnel, StockLedger, reconcile_states
from masseng_v6.core.state import CohortCell, CohortKey, CohortState, EducationStatus, WorkStatus


def key(status=EducationStatus.QUALIFIED_WAITING, work=WorkStatus.NONE):
    return CohortKey("PHL", 2006, 3, "rural", "tertiary", 12, "none", status, work)


def test_entry_funnel_known_answer():
    funnel = EntryFunnel(100, 80, 60, 30)
    assert funnel.factors == (0.8, 0.75, 0.5)
    funnel.reconcile()


@pytest.mark.parametrize("values", [(1, 0, 0, 1), (1, 0, 1, 0), (0, 1, 0, 0), (-1, 0, 0, 0)])
def test_invalid_funnels_fail(values):
    with pytest.raises(ValueError):
        EntryFunnel(*values)


def test_zero_denominator_is_not_a_fake_zero_factor():
    with pytest.raises(ValueError):
        EntryFunnel(0, 0, 0, 0).factors


def test_stock_flow_identity():
    StockLedger(100, 94, entrants_external=2, reentries=3, deaths=4, exits_external=7).validate()
    with pytest.raises(AssertionError):
        StockLedger(100, 99).validate()


def test_cohort_move_conserves_mass_and_work_is_orthogonal():
    source = key()
    destination = key(EducationStatus.ATTENDING, WorkStatus.PART_TIME)
    state = CohortState([CohortCell(source, 10)])
    state.move(source, destination, 4)
    assert state.total == 10
    assert state.count(source) == 6
    assert state.count(destination) == 4
    reconcile_states(state, state.copy())


def test_cannot_overdraw_or_create_negative_mass():
    state = CohortState([CohortCell(key(), 1)])
    with pytest.raises(ValueError):
        state.move(key(), key(EducationStatus.ATTENDING), 2)
    with pytest.raises(ValueError):
        state.add(key(), -2)


def test_expired_waiting_mass_moves_once():
    from masseng_v6.core.runner import expire_waiting

    waiting = key()
    terminal = key(EducationStatus.EXIT_TERMINAL)
    state = CohortState([CohortCell(waiting, 5)])
    result = expire_waiting(state, [waiting], {waiting: terminal})
    assert result.count(waiting) == 0
    assert result.count(terminal) == 5
    assert result.total == state.total
