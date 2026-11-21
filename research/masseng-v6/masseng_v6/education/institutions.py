"""Institution and market capacity objects for annual admissions clearing."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Institution:
    institution_id: str
    region: str
    stage: str
    sector: str
    grades: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.sector not in {"public", "private", "alternative"}:
            raise ValueError("unknown provider sector")
        if not self.grades or len(self.grades) != len(set(self.grades)):
            raise ValueError("institution grades must be non-empty and unique")


@dataclass(frozen=True)
class Market:
    market_id: str
    region: str
    stage: str
    sector: str
    physical_capacity: float
    continuing_reserved: float = 0.0

    def __post_init__(self) -> None:
        if self.sector not in {"public", "private", "alternative"}:
            raise ValueError("unknown provider sector")
        values = (self.physical_capacity, self.continuing_reserved)
        if any(not isfinite(x) or x < 0 for x in values):
            raise ValueError("capacities must be finite and non-negative")
        if self.continuing_reserved > self.physical_capacity:
            raise ValueError("continuing reservations exceed physical capacity")

    @property
    def available_new_entrant_seats(self) -> float:
        return self.physical_capacity - self.continuing_reserved
