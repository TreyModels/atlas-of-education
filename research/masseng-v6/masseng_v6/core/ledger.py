"""Exact entry-funnel and stock-flow accounting checks."""
from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite
from typing import Iterable

from .state import CohortState


@dataclass(frozen=True)
class EntryFunnel:
    qualified: float
    latent_zero_cost: float
    effective: float
    realized: float

    def __post_init__(self) -> None:
        values = (self.qualified, self.latent_zero_cost, self.effective, self.realized)
        if any(not isfinite(x) or x < 0 for x in values):
            raise ValueError("Q/L/E/R must be finite and non-negative")
        if not (self.realized <= self.effective <= self.latent_zero_cost <= self.qualified):
            raise ValueError("entry funnel violates 0 <= R <= E <= L <= Q")

    @property
    def factors(self) -> tuple[float, float, float]:
        """Conditional L/Q, E/L and R/E; zero denominators have undefined factors."""
        if min(self.qualified, self.latent_zero_cost, self.effective) == 0:
            raise ValueError("factors are undefined when any preceding denominator is zero")
        return (
            self.latent_zero_cost / self.qualified,
            self.effective / self.latent_zero_cost,
            self.realized / self.effective,
        )

    def reconcile(self, tolerance: float = 1e-9) -> None:
        factors = self.factors
        reconstructed = self.qualified
        for factor in factors:
            reconstructed *= factor
        if not isclose(reconstructed, self.realized, abs_tol=tolerance):
            raise AssertionError("entry-funnel factorization does not reconstruct R")


@dataclass(frozen=True)
class StockLedger:
    start: float
    end: float
    entrants_external: float = 0.0
    reentries: float = 0.0
    deaths: float = 0.0
    exits_external: float = 0.0

    def __post_init__(self) -> None:
        values = tuple(self.__dict__.values())
        if any(not isfinite(x) or x < 0 for x in values):
            raise ValueError("ledger quantities must be finite and non-negative")

    @property
    def residual(self) -> float:
        return self.start + self.entrants_external + self.reentries - self.deaths - self.exits_external - self.end

    def validate(self, tolerance: float = 1e-9) -> None:
        if abs(self.residual) > tolerance:
            raise AssertionError(f"stock-flow conservation residual {self.residual}")


def reconcile_states(
    before: CohortState,
    after: CohortState,
    entrants_external: float = 0.0,
    reentries: float = 0.0,
    deaths: float = 0.0,
    exits_external: float = 0.0,
) -> StockLedger:
    ledger = StockLedger(before.total, after.total, entrants_external, reentries, deaths, exits_external)
    ledger.validate()
    return ledger


def assert_disjoint_destinations(destinations: Iterable[object]) -> None:
    values = list(destinations)
    if len(values) != len(set(values)):
        raise ValueError("mutually exclusive destinations must be unique")
