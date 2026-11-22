"""Conservative annual transition adapter used by Phase 1 experiments."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Mapping

from ..education.admissions import Allocation, Applicant, clear_admissions
from ..education.institutions import Market
from .ledger import StockLedger, reconcile_states
from .state import CohortKey, CohortState, EducationStatus


@dataclass(frozen=True)
class YearResult:
    state: CohortState
    allocation: Allocation
    stock_ledger: StockLedger


def run_admissions_year(
    state: CohortState,
    applicant_sources: Mapping[str, CohortKey],
    applicants: Iterable[Applicant],
    markets: Iterable[Market],
) -> YearResult:
    """Move admitted mass from unique source cells and leave unplaced mass deferred.

    This adapter deliberately does not yet implement v5 behaviour or estimated
    country parameters. It supplies the accounting boundary for later integration.
    """
    people = tuple(applicants)
    ids = {a.applicant_id for a in people}
    if ids != set(applicant_sources):
        raise ValueError("every applicant must map to exactly one source cohort cell")
    market_tuple = tuple(markets)
    sectors = {m.market_id: m.sector for m in market_tuple}
    before = state.copy()
    after = state.copy()
    allocation = clear_admissions(people, market_tuple)
    for applicant_id, admitted_by_market in allocation.assignments.items():
        source = applicant_sources[applicant_id]
        for market_id, admitted_mass in admitted_by_market.items():
            target = replace(source, sector=sectors[market_id], education_status=EducationStatus.ATTENDING)
            after.move(source, target, admitted_mass)
    ledger = reconcile_states(before, after)
    return YearResult(after, allocation, ledger)


def expire_waiting(
    state: CohortState,
    waiting: Iterable[CohortKey],
    terminal_destination: Mapping[CohortKey, CohortKey],
) -> CohortState:
    """Move expired eligible people once, from waiting to a terminal destination."""
    result = state.copy()
    for key in waiting:
        if key.education_status != EducationStatus.QUALIFIED_WAITING:
            raise ValueError("only qualified_waiting cells can expire through this operation")
        result.move(key, terminal_destination[key], result.count(key))
    return result
