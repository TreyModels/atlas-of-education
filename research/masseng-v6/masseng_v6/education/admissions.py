"""Deterministic joint admissions: each effective applicant receives at most one seat."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from ..core.ledger import EntryFunnel
from .institutions import Market


@dataclass(frozen=True)
class Applicant:
    applicant_id: str
    preferences: tuple[str, ...]
    qualified: bool = True
    zero_cost_willing: bool = True
    effective: bool = True

    def __post_init__(self) -> None:
        if not self.applicant_id:
            raise ValueError("applicant_id is required")
        if len(self.preferences) != len(set(self.preferences)):
            raise ValueError("an applicant cannot rank a market twice")
        if self.effective and not self.zero_cost_willing:
            raise ValueError("effective demand must be a subset of zero-cost willingness")
        if self.zero_cost_willing and not self.qualified:
            raise ValueError("zero-cost willingness must be a subset of qualification")


@dataclass(frozen=True)
class MarketResult:
    market_id: str
    physical_seats: float
    continuing_reserved: float
    places_open: float
    offers: float
    acceptances: float
    empty_seats: float
    accessible_empty_seats: float


@dataclass(frozen=True)
class Allocation:
    assignments: Mapping[str, str]
    markets: tuple[MarketResult, ...]
    funnel: EntryFunnel
    unique_applicants: float
    unmet_effective_demand: float
    rejected_eligible: float

    def assignments_for(self, market_id: str) -> tuple[str, ...]:
        return tuple(sorted(k for k, v in self.assignments.items() if v == market_id))


def clear_admissions(applicants: Iterable[Applicant], markets: Iterable[Market]) -> Allocation:
    """Clear ranked accessible choices in stable applicant order.

    Preferences are the applicant's accessible, acceptable markets. Non-effective
    applicants stay in Q/L accounting but do not enter the assignment problem.
    The mass-cell implementation represents each distinct person/mass unit once.
    """
    people = tuple(applicants)
    market_tuple = tuple(markets)
    by_id = {m.market_id: m for m in market_tuple}
    if len(by_id) != len(market_tuple):
        raise ValueError("market ids must be unique")
    ids = [a.applicant_id for a in people]
    if len(ids) != len(set(ids)):
        raise ValueError("applicant ids must be unique; multiple choices are preferences, not persons")
    for person in people:
        unknown = set(person.preferences) - set(by_id)
        if unknown:
            raise ValueError(f"unknown markets in preferences: {sorted(unknown)}")

    remaining = {m.market_id: m.available_new_entrant_seats for m in market_tuple}
    assignments: dict[str, str] = {}
    # Stable ID order is the deterministic tie-break; no random seed is hidden.
    for person in sorted(people, key=lambda a: a.applicant_id):
        if not person.effective:
            continue
        for market_id in person.preferences:
            if remaining[market_id] > 0:
                assignments[person.applicant_id] = market_id
                remaining[market_id] -= 1.0
                break

    effective_ids = {a.applicant_id for a in people if a.effective}
    accessible_to_effective = {
        m.market_id: any(m.market_id in a.preferences for a in people if a.effective)
        for m in market_tuple
    }
    results = tuple(
        MarketResult(
            market_id=m.market_id,
            physical_seats=m.physical_capacity,
            continuing_reserved=m.continuing_reserved,
            places_open=m.available_new_entrant_seats,
            offers=sum(v == m.market_id for v in assignments.values()),
            acceptances=sum(v == m.market_id for v in assignments.values()),
            empty_seats=remaining[m.market_id],
            accessible_empty_seats=(remaining[m.market_id] if accessible_to_effective[m.market_id] else 0.0),
        )
        for m in market_tuple
    )
    funnel = EntryFunnel(
        qualified=sum(a.qualified for a in people),
        latent_zero_cost=sum(a.zero_cost_willing for a in people),
        effective=sum(a.effective for a in people),
        realized=len(assignments),
    )
    return Allocation(
        assignments=assignments,
        markets=results,
        funnel=funnel,
        unique_applicants=float(len(people)),
        unmet_effective_demand=float(len(effective_ids - set(assignments))),
        rejected_eligible=float(sum(a.qualified and a.applicant_id not in assignments for a in people)),
    )
