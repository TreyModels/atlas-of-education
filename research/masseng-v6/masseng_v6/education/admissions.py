"""Fractional joint admissions with explicit proportional rationing."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping

from ..core.ledger import EntryFunnel
from .institutions import Market


@dataclass(frozen=True)
class Applicant:
    """A unique person or probability-mass cell.

    Latent willingness is evaluated at the lower of zero full cost and the
    actual subsidized cost. Thus a net-negative-cost transfer can raise E above
    conventional zero-cost willingness without violating the accounting funnel.
    Accessible markets may be reachable but unwanted; preferences are the
    acceptable subset that actually enters the assignment algorithm.
    """

    applicant_id: str
    preferences: tuple[str, ...]
    mass: float = 1.0
    qualified: bool = True
    latent_willing: bool = True
    effective: bool = True
    accessible_markets: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        if not self.applicant_id:
            raise ValueError("applicant_id is required")
        if not isfinite(self.mass) or self.mass < 0:
            raise ValueError("applicant mass must be finite and non-negative")
        if len(self.preferences) != len(set(self.preferences)):
            raise ValueError("an applicant cannot rank a market twice")
        accessible = self.accessible_markets if self.accessible_markets is not None else self.preferences
        if len(accessible) != len(set(accessible)):
            raise ValueError("accessible markets must be unique")
        if not set(self.preferences).issubset(accessible):
            raise ValueError("preferences must be a subset of accessible markets")
        if self.effective and not self.latent_willing:
            raise ValueError("effective demand must be a subset of latent willingness")
        if self.latent_willing and not self.qualified:
            raise ValueError("latent willingness must be a subset of qualification")


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
    # applicant -> market -> expected admitted mass; residual mass is unplaced.
    assignments: Mapping[str, Mapping[str, float]]
    markets: tuple[MarketResult, ...]
    funnel: EntryFunnel
    unique_applicants: float
    unmet_effective_demand: float
    rejected_eligible: float

    def assignments_for(self, market_id: str) -> tuple[str, ...]:
        return tuple(sorted(k for k, v in self.assignments.items() if v.get(market_id, 0) > 0))


def clear_admissions(applicants: Iterable[Applicant], markets: Iterable[Market]) -> Allocation:
    """Clear fractional mass by preference round and proportional rationing.

    If demand for a market exceeds remaining capacity, every cell requesting
    that market in the round receives the same proportion of its requesting
    mass. Unplaced residual mass may cascade to the next listed preference.
    Applicant IDs never determine priority. Assignments are expected mass, so a
    fractional allocation is not interpreted as a fraction of an individual.
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
        declared = set(person.preferences) | set(person.accessible_markets or ())
        unknown = declared - set(by_id)
        if unknown:
            raise ValueError(f"unknown markets: {sorted(unknown)}")

    remaining = {m.market_id: m.available_new_entrant_seats for m in market_tuple}
    unplaced = {a.applicant_id: (a.mass if a.effective else 0.0) for a in people}
    assignments: dict[str, dict[str, float]] = {a.applicant_id: {} for a in people}

    for rank in range(max((len(a.preferences) for a in people), default=0)):
        requests: dict[str, list[str]] = {m.market_id: [] for m in market_tuple}
        for person in people:
            if len(person.preferences) > rank and unplaced[person.applicant_id] > 0:
                requests[person.preferences[rank]].append(person.applicant_id)
        for market_id, requesters in requests.items():
            demand = sum(unplaced[applicant_id] for applicant_id in requesters)
            if demand <= 0 or remaining[market_id] <= 0:
                continue
            share = min(1.0, remaining[market_id] / demand)
            admitted_this_round = 0.0
            for applicant_id in requesters:
                admitted = unplaced[applicant_id] * share
                assignments[applicant_id][market_id] = assignments[applicant_id].get(market_id, 0.0) + admitted
                unplaced[applicant_id] -= admitted
                admitted_this_round += admitted
            remaining[market_id] -= admitted_this_round
            if abs(remaining[market_id]) < 1e-12:
                remaining[market_id] = 0.0

    accessible_to_effective = {
        m.market_id: any(
            m.market_id in (a.accessible_markets if a.accessible_markets is not None else a.preferences)
            for a in people if a.effective
        )
        for m in market_tuple
    }
    results = tuple(
        MarketResult(
            market_id=m.market_id,
            physical_seats=m.physical_capacity,
            continuing_reserved=m.continuing_reserved,
            places_open=m.available_new_entrant_seats,
            offers=sum(v.get(m.market_id, 0.0) for v in assignments.values()),
            acceptances=sum(v.get(m.market_id, 0.0) for v in assignments.values()),
            empty_seats=remaining[m.market_id],
            # Reachable by at least one effective applicant, whether wanted or not.
            accessible_empty_seats=(remaining[m.market_id] if accessible_to_effective[m.market_id] else 0.0),
        )
        for m in market_tuple
    )
    realized = sum(sum(v.values()) for v in assignments.values())
    funnel = EntryFunnel(
        qualified=sum(a.mass for a in people if a.qualified),
        latent_zero_cost=sum(a.mass for a in people if a.latent_willing),
        effective=sum(a.mass for a in people if a.effective),
        realized=realized,
    )
    return Allocation(
        assignments=assignments,
        markets=results,
        funnel=funnel,
        unique_applicants=sum(a.mass for a in people),
        unmet_effective_demand=sum(unplaced.values()),
        rejected_eligible=funnel.qualified - realized,
    )
