"""Vectorized two-sector fractional admissions for annual cohort integration.

The rule mirrors the v6 reference kernel: proportional rationing within each
first-choice sector, followed by one proportional cascade of residual mass to
the other sector. No applicant/cohort ordering affects an allocation.
"""
from __future__ import annotations

import numpy as np


def clear_two_sector_array(demand, capacity, allow_cascade=True):
    """Allocate unique expected mass against one shared public/private capacity.

    ``demand`` has arbitrary leading cohort/decile dimensions and a final sector
    dimension. ``capacity`` is the national or market-level pair shared by all
    leading cells, not a capacity repeated independently for every cell.
    """
    demand = np.asarray(demand, dtype=float)
    capacity = np.asarray(capacity, dtype=float)
    if demand.ndim < 1 or demand.shape[-1] != 2 or capacity.shape != (2,):
        raise ValueError("demand must end in two sectors and capacity must have shape (2,)")
    if not np.isfinite(demand).all() or not np.isfinite(capacity).all():
        raise ValueError("demand and capacity must be finite")
    if (demand < 0).any() or (capacity < 0).any():
        raise ValueError("demand and capacity must be non-negative")

    cap = capacity.copy()
    total_demand = demand.sum(axis=tuple(range(demand.ndim - 1)))
    first_share = np.divide(cap, total_demand, out=np.ones(2), where=total_demand > 0)
    first_share = np.minimum(1.0, first_share)
    admitted = demand * first_share
    residual = demand - admitted
    cap -= admitted.sum(axis=tuple(range(demand.ndim - 1)))

    if allow_cascade:
        cross = residual[..., ::-1]
        cross_total = cross.sum(axis=tuple(range(demand.ndim - 1)))
        cross_share = np.divide(cap, cross_total, out=np.ones(2), where=cross_total > 0)
        cross_share = np.minimum(1.0, cross_share)
        extra_cross = cross * cross_share
        admitted += extra_cross
        residual -= extra_cross[..., ::-1]

    admitted = np.maximum(admitted, 0.0)
    unmet = np.maximum(residual.sum(axis=-1), 0.0)
    admitted_by_sector = admitted.sum(axis=tuple(range(demand.ndim - 1)))
    if (admitted.sum(axis=-1) > demand.sum(axis=-1) + 1e-8).any():
        raise AssertionError("array admissions duplicated applicant mass")
    if (admitted_by_sector > capacity + 1e-8).any():
        raise AssertionError("array admissions exceeded shared physical capacity")
    return admitted, unmet
