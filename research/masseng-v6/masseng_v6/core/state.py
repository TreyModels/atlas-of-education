"""Typed probability-mass cohort state with orthogonal schooling and work status."""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from math import isfinite
from typing import Dict, Iterable, Iterator, Tuple


class EducationStatus(str, Enum):
    ATTENDING = "attending"
    REPEATING = "repeating"
    QUALIFIED_WAITING = "qualified_waiting"
    OUT_OF_SCHOOL_REENTERABLE = "out_of_school_reenterable"
    COMPLETED = "completed"
    EXIT_TERMINAL = "exit_terminal"
    ALTERNATIVE = "alternative"


class WorkStatus(str, Enum):
    NONE = "none"
    PART_TIME = "part_time"
    FULL_TIME = "full_time"
    SEASONAL = "seasonal"


@dataclass(frozen=True, order=True)
class CohortKey:
    country: str
    birth_cohort: int
    decile: int
    region: str
    stage: str
    grade: int
    sector: str
    education_status: EducationStatus
    work_status: WorkStatus = WorkStatus.NONE

    def __post_init__(self) -> None:
        if not 1 <= self.decile <= 10:
            raise ValueError("decile must be in 1..10")
        if self.grade < 0:
            raise ValueError("grade cannot be negative")


@dataclass(frozen=True)
class CohortCell:
    key: CohortKey
    count: float

    def __post_init__(self) -> None:
        if not isfinite(self.count) or self.count < 0:
            raise ValueError("cohort count must be finite and non-negative")


class CohortState:
    """Sparse cohort cells; moving mass never creates or destroys people."""

    def __init__(self, cells: Iterable[CohortCell] = ()) -> None:
        self._cells: Dict[CohortKey, float] = {}
        for cell in cells:
            self.add(cell.key, cell.count)

    def __iter__(self) -> Iterator[CohortCell]:
        for key in sorted(self._cells):
            yield CohortCell(key, self._cells[key])

    @property
    def total(self) -> float:
        return sum(self._cells.values())

    def count(self, key: CohortKey) -> float:
        return self._cells.get(key, 0.0)

    def add(self, key: CohortKey, count: float) -> None:
        if not isfinite(count):
            raise ValueError("cohort delta must be finite")
        new_count = self.count(key) + count
        if new_count < -1e-9:
            raise ValueError(f"negative cohort mass for {key}: {new_count}")
        if abs(new_count) <= 1e-12:
            self._cells.pop(key, None)
        else:
            self._cells[key] = max(0.0, new_count)

    def move(self, source: CohortKey, destination: CohortKey, count: float) -> None:
        if not isfinite(count) or count < 0:
            raise ValueError("transition count must be finite and non-negative")
        if count > self.count(source) + 1e-9:
            raise ValueError(f"transition exceeds source mass: {count} > {self.count(source)}")
        self.add(source, -count)
        self.add(destination, count)

    def transition(self, source: CohortKey, count: float, **changes: object) -> CohortKey:
        destination = replace(source, **changes)
        self.move(source, destination, count)
        return destination

    def copy(self) -> "CohortState":
        return CohortState(self)

    def as_tuples(self) -> Tuple[Tuple[CohortKey, float], ...]:
        return tuple((cell.key, cell.count) for cell in self)
