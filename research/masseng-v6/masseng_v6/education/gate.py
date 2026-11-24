"""Score/quota admissions gate for the v6 prototype.

MASSENG v5 has no selection gate: entry is a probabilistic demand logit with no score, no bar and no quota.  This
module adds the missing gate as a typed, fractional-mass allocator that respects the v6 skeleton's entry-funnel
accounting (`masseng_v6.core.ledger.EntryFunnel`, Q >= L >= E >= R).  It *consumes* exam scores and a capacity; it
does not produce scores, so score production stays a separate, declared part of the pipeline.

Gate rules (switchable; every quantity is expected mass, never a fraction of a person):

  capacity : rank by score, admit down to capacity (pure merit + quantity gate)
  bar      : declared score threshold first, then rank down to capacity; the bar can bind before capacity
  quota    : a declared share of capacity is reserved for a declared group (bottom income deciles) among those
             meeting a lower quota threshold; remaining places are open-merit; unfilled reserved places roll over
  exam     : a declared random pass probability is applied first (failers exit); the bar/capacity rule then runs
             on passers -- the "exam pass" pushout channel

All rules are declared, illustrative and *not* calibrated.  No causal claims.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite

import numpy as np

from ..core.ledger import EntryFunnel

GATE_KINDS = ("capacity", "bar", "quota", "exam", "tullock")


def ranked_admit(eligible: np.ndarray, capacity: float, scores: np.ndarray, mass: np.ndarray):
    """Admit expected mass by descending score up to ``capacity``.

    Returns ``(admitted_mass, boundary_fraction)``.  The boundary applicant cell can be admitted partially, so
    ``admitted_mass.sum()`` equals ``min(capacity, eligible mass)`` exactly (floating tolerance aside).
    """
    admitted = np.zeros_like(mass, dtype=float)
    mask = np.asarray(eligible, dtype=bool)
    remaining = float(max(capacity, 0.0))
    if remaining <= 0 or not mask.any():
        return admitted, 0.0
    idx = np.flatnonzero(mask)
    order = idx[np.argsort(-np.asarray(scores)[idx], kind="stable")]
    cum = 0.0
    boundary = 0.0
    for i in order:
        m = float(mass[i])
        if cum + m <= remaining + 1e-12:
            admitted[i] = m
            cum += m
        else:
            take = remaining - cum
            if take > 1e-12:
                admitted[i] = take
                boundary = take / m if m > 0 else 0.0
                cum = remaining
            break
    return admitted, boundary


@dataclass(frozen=True)
class Gate:
    """One admissions gate.  ``capacity`` is absolute expected mass (persons), not a share."""

    kind: str = "capacity"
    capacity: float = 0.0
    threshold: float = -inf          # bar (and the regular bar inside quota / exam rules)
    quota_share: float = 0.0
    quota_threshold: float = -inf
    quota_group_max: int = 2         # deciles 0..quota_group_max are the reserved-seat group
    pass_rate: float = 1.0
    tullock_scale: float = 0.5      # contest-success slope for the 'tullock' rule
    label: str = ""

    def __post_init__(self):
        if self.kind not in GATE_KINDS:
            raise ValueError(f"unknown gate kind {self.kind!r}; expected {GATE_KINDS}")
        for name in ("capacity", "threshold", "quota_share", "quota_threshold", "pass_rate"):
            value = getattr(self, name)
            if not isfinite(value) and value != -inf:
                raise ValueError(f"{name} must be finite (or -inf for an open bar)")
        if self.capacity < 0:
            raise ValueError("capacity must be non-negative")
        if not 0.0 <= self.pass_rate <= 1.0:
            raise ValueError("pass_rate must be in [0, 1]")
        if not 0.0 <= self.quota_share <= 1.0:
            raise ValueError("quota_share must be in [0, 1]")
        if not 0 <= self.quota_group_max <= 10:
            raise ValueError("quota_group_max must be in 0..10")


@dataclass
class GateOutcome:
    admitted_mass: np.ndarray
    eligible: np.ndarray
    accounting: dict
    funnel: EntryFunnel


def apply_gate(gate: Gate, scores, mass, eligible, group, rng=None) -> GateOutcome:
    """Apply one gate to expected mass.

    Parameters
    ----------
    scores : array of exam scores
    mass   : array of expected mass per cell (persons)
    eligible : bool array, reaches the gate (e.g. completed the previous level)
    group  : integer income-decile array (0 = poorest .. 9 = richest) used by the quota rule
    rng    : numpy Generator, used only for the declared random exam pass rule
    """
    scores = np.asarray(scores, float)
    mass = np.asarray(mass, float)
    eligible = np.asarray(eligible, bool)
    group = np.asarray(group, int)
    if not (len(scores) == len(mass) == len(eligible) == len(group)):
        raise ValueError("scores, mass, eligible and group must have equal length")
    if (mass < 0).any():
        raise ValueError("mass must be non-negative")
    total_eligible = float(mass[eligible].sum())
    adm = np.zeros_like(mass)
    below_bar = np.zeros_like(mass)
    exam_fail = np.zeros_like(mass)
    cap_reject = np.zeros_like(mass)
    quota_adm = np.zeros_like(mass)

    passed = np.ones_like(eligible)
    if gate.kind == "exam":
        if rng is None:
            raise ValueError("exam gate needs an rng for its declared random pass rule")
        passed = rng.random(len(scores)) < gate.pass_rate
        exam_fail = np.where(eligible & ~passed, mass, 0.0)
    allowed = eligible & passed

    if gate.kind in ("bar", "exam"):
        above = allowed & (scores >= gate.threshold)
        below_bar = np.where(allowed & ~above, mass, 0.0)
        adm, _ = ranked_admit(above, gate.capacity, scores, mass)
        cap_reject = np.where(above, mass - adm, 0.0)
    elif gate.kind == "capacity":
        adm, _ = ranked_admit(allowed, gate.capacity, scores, mass)
        cap_reject = np.where(allowed, mass - adm, 0.0)
    elif gate.kind == "tullock":
        # Contest-success admission (Tullock form): places are allocated in proportion to success probability
        # P_i = sigmoid((score_i - threshold)/scale), capped at each cell's mass.  This is the "contest" rival to a
        # fixed cutoff; it is a declared functional form, NOT a claim about which rule real admissions systems use.
        live = allowed
        if live.any():
            z = (scores[live] - gate.threshold) / max(gate.tullock_scale, 1e-9)
            p = 1.0 / (1.0 + np.exp(-z))
            target = min(gate.capacity, float(mass[live].sum()))
            sub = np.zeros(int(live.sum()))
            for _ in range(8):
                short = target - sub.sum()
                if short <= 1e-12:
                    break
                slack = mass[live] - sub
                w = np.where(slack > 0, p, 0.0)
                if w.sum() <= 0:
                    break
                sub += np.minimum(w / w.sum() * short, slack)
            adm[live] = sub
        cap_reject = np.where(allowed, np.maximum(mass - adm, 0.0), 0.0)
    elif gate.kind == "quota":
        qgroup = allowed & (group <= gate.quota_group_max)
        q_ok = qgroup & (scores >= gate.quota_threshold)
        below_bar = np.where(qgroup & ~q_ok, mass, 0.0)
        regular = allowed & ~qgroup
        regular_ok = regular & (scores >= gate.threshold)
        below_bar += np.where(regular & ~regular_ok, mass, 0.0)
        reserved = gate.quota_share * gate.capacity
        q_adm, _ = ranked_admit(q_ok, reserved, scores, mass)
        adm += q_adm
        quota_adm = q_adm
        open_capacity = gate.capacity - q_adm.sum()
        open_pool = (q_ok | regular_ok) & ~(q_adm > 0)
        o_adm, _ = ranked_admit(open_pool, open_capacity, scores, mass)
        adm += o_adm
        cap_reject = np.where(allowed, np.maximum(mass - adm, 0.0), 0.0)
    else:  # pragma: no cover - guarded by Gate
        raise ValueError(gate.kind)

    admitted_total = float(adm.sum())
    if admitted_total > total_eligible + 1e-9:
        raise AssertionError("gate admitted more mass than was eligible")
    funnel = EntryFunnel(qualified=total_eligible, latent_zero_cost=total_eligible,
                         effective=total_eligible, realized=admitted_total)
    if total_eligible > 0:
        funnel.reconcile()
    accounting = dict(
        kind=gate.kind, eligible=total_eligible, capacity=float(gate.capacity),
        admitted=admitted_total, fill_rate=(admitted_total / gate.capacity if gate.capacity > 0 else None),
        below_bar=float(below_bar.sum()), exam_fail=float(exam_fail.sum()),
        capacity_rejection=float(cap_reject.sum()), quota_admitted=float(quota_adm.sum()),
        rejected_eligible=total_eligible - admitted_total,
        threshold=gate.threshold, pass_rate=gate.pass_rate, quota_share=gate.quota_share,
    )
    return GateOutcome(admitted_mass=adm, eligible=eligible, accounting=accounting, funnel=funnel)
