"""Zero-sum exam-gate shadow-education module (adapted from Yang 2026 & Kang 2025).

Key principles (aligned with Mark Bray's comparative shadow-education framework):
1. Separates exam-gate (positional) tutoring from remedial catch-up tutoring.
2. Uses a CES production function T(e_s, x) with an exam-vs-skill wedge omega in [0, 1]:
     h_exam  = T(e_s, p)
     h_skill = T(e_s, omega * p)
3. Fixed funded seats Q_funded are strictly conserved (zero-sum): tutoring shifts
   which income deciles win the funded seats via an endogenous exam-score cutoff,
   and adds directly to household education spending, without creating new seats.
4. Supports policy counterfactuals: baseline, seat expansion, tutoring tax recycled
   into public school spending e_s, strict ban, and imperfect-enforcement black market.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class TutoringPolicy:
    mode: str = "baseline"        # baseline | ban_strict | ban_black_market | tutoring_tax
    tax_rate: float = 0.0         # proportional tax on tutoring (recycled into e_s)
    recycle_tax: bool = True      # whether tax revenue augments public school spend e_s
    enforcement: float = 0.0      # phi >= 0 under ban_black_market
    access_gap: float = 1.0       # how steeply informal access favors richer deciles
    seat_multiplier: float = 1.0  # >1.0 for funded-seat expansion counterfactual


@dataclass
class TutoringParams:
    enabled: bool = True
    omega: float = 0.31           # skill-vs-exam conversion (0=pure zero-sum, 1=fully productive; Yang 2026 ~0.308)
    ces_A: float = 1.0
    ces_lam: float = 0.61         # weight on public school spend e_s (Yang 2026 ~0.613)
    ces_mu: float = 0.52          # CES substitution parameter (Yang 2026 ~0.519)
    rank_smoothness: float = 0.25 # within-decile exam score dispersion relative to cohort mean
    gate_sensitivity: float = 0.95  # how strongly tightness (applicants/seats) drives gate tutoring
    income_elast: float = 0.70    # income elasticity of tutoring spending (Kim, Tertilt & Yum 2024 ~0.698)
    base_spend_share: float = 0.035  # baseline tutoring share of GDPpc at tightness=1.5
    remedial_rate: float = 0.12   # baseline remedial tutoring participation for struggling students
    remedial_cost: float = 0.015  # modest remedial cost (share of GDPpc)


def ces_production(e_s: np.ndarray | float, x: np.ndarray | float, params: TutoringParams) -> np.ndarray:
    """CES combination of public school input e_s and private tutoring x."""
    e_s = np.maximum(np.asarray(e_s, dtype=float), 1e-6)
    x = np.maximum(np.asarray(x, dtype=float), 0.0)
    mu = params.ces_mu
    lam = params.ces_lam
    inner = lam * (e_s ** mu) + (1.0 - lam) * ((x + 1e-6) ** mu)
    return params.ces_A * (inner ** (1.0 / mu))


def solve_exam_gate_tutoring(
    applicants_by_decile: np.ndarray,
    funded_seats: float,
    income_mult: np.ndarray,
    public_spend_e_s: float,
    params: TutoringParams | None = None,
    policy: TutoringPolicy | None = None,
) -> dict:
    """Compute decile-level tutoring participation, spending, rank-based funded admissions,
    and productive vs. exam-relevant human capital under strict funded-seat conservation."""
    params = params or TutoringParams()
    policy = policy or TutoringPolicy()

    apps = np.maximum(np.asarray(applicants_by_decile, dtype=float), 0.0)
    inc = np.maximum(np.asarray(income_mult, dtype=float), 1e-4)
    total_apps = float(apps.sum())
    seats = max(float(funded_seats) * policy.seat_multiplier, 0.0)

    if total_apps <= 1e-12:
        zeros = np.zeros(10, dtype=float)
        return dict(
            admitted_funded=zeros,
            spillover=zeros,
            tutoring_part=zeros,
            gate_part=zeros,
            remedial_part=zeros,
            tutoring_spend_per_student=zeros,
            h_exam=np.ones(10, dtype=float),
            h_skill=np.ones(10, dtype=float),
            kappa=zeros,
            tightness=0.0,
            tax_revenue=0.0,
            effective_e_s=float(public_spend_e_s),
        )

    tightness = total_apps / max(seats, 1.0) if seats > 0 else 10.0
    pressure = np.log1p(max(tightness - 0.6, 0.0))

    decile_idx = np.linspace(0.0, 1.0, 10)
    if not params.enabled or policy.mode == "ban_strict":
        cost_wedge = np.full(10, np.inf)
    elif policy.mode == "ban_black_market":
        access_factor = 1.0 - 0.55 * policy.access_gap * decile_idx
        access_factor = np.clip(access_factor, 0.25, 1.5)
        cost_wedge = 1.0 + policy.enforcement * access_factor
    elif policy.mode == "tutoring_tax":
        cost_wedge = np.full(10, 1.0 + max(policy.tax_rate, 0.0))
    else:
        cost_wedge = np.ones(10, dtype=float)

    if np.isinf(cost_wedge).all():
        gate_part = np.zeros(10, dtype=float)
        gate_spend = np.zeros(10, dtype=float)
    else:
        logit_part = (
            -0.65
            + params.gate_sensitivity * pressure
            + 1.35 * np.log(inc)
            - 0.95 * np.log(cost_wedge)
        )
        gate_part = 1.0 / (1.0 + np.exp(-np.clip(logit_part, -20, 20)))
        gate_spend = (
            gate_part
            * params.base_spend_share
            * (inc ** params.income_elast)
            * (1.0 + 0.85 * pressure)
            / (cost_wedge ** 0.8)
        )

    remedial_part = (
        np.zeros(10, dtype=float)
        if (not params.enabled or policy.mode == "ban_strict")
        else np.clip(params.remedial_rate * (1.15 - 0.35 * decile_idx) / np.sqrt(cost_wedge), 0.0, 0.4)
    )
    remedial_spend = remedial_part * params.remedial_cost

    total_part = np.clip(1.0 - (1.0 - gate_part) * (1.0 - remedial_part), 0.0, 1.0)
    total_spend_per_student = gate_spend + remedial_spend

    tax_revenue = 0.0
    eff_e_s = float(public_spend_e_s)
    if policy.mode == "tutoring_tax" and policy.tax_rate > 0 and policy.recycle_tax:
        tax_revenue = float(np.sum(apps * gate_spend * policy.tax_rate) / total_apps)
        eff_e_s = float(public_spend_e_s) + tax_revenue

    readiness = 0.85 + 0.30 * decile_idx
    h_exam = readiness * ces_production(eff_e_s, gate_spend, params)
    h_skill = readiness * ces_production(eff_e_s, params.omega * gate_spend + 0.8 * remedial_spend, params)

    # Continuous exam-score distribution with within-decile dispersion sigma_exam
    h_mean = float(np.sum(apps * h_exam) / total_apps)
    h_rel = h_exam - h_mean
    sigma_exam = max(params.rank_smoothness * max(h_mean, 0.1), 1e-4)
    if seats <= 1e-12:
        admitted_funded = np.zeros(10, dtype=float)
        kappa = np.zeros(10, dtype=float)
    elif seats >= total_apps:
        admitted_funded = apps.copy()
        kappa = 1.0 / (1.0 + np.exp(-np.clip(h_rel / sigma_exam, -20, 20)))
    else:
        lo, hi = float(h_rel.min()) - 10.0 * sigma_exam, float(h_rel.max()) + 10.0 * sigma_exam
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            p_adm = 1.0 / (1.0 + np.exp(-np.clip((h_rel - mid) / sigma_exam, -30, 30)))
            if float(np.sum(apps * p_adm)) > seats:
                lo = mid
            else:
                hi = mid
        c_star = 0.5 * (lo + hi)
        p_adm = 1.0 / (1.0 + np.exp(-np.clip((h_rel - c_star) / sigma_exam, -30, 30)))
        admitted_funded = np.minimum(apps, apps * p_adm)
        kappa = 1.0 / (1.0 + np.exp(-np.clip(h_rel / sigma_exam, -20, 20)))
        diff = seats - float(admitted_funded.sum())
        if abs(diff) > 1e-9:
            room = (apps - admitted_funded) if diff > 0 else admitted_funded
            room_sum = float(room.sum())
            if room_sum > 1e-12:
                admitted_funded += diff * (room / room_sum)
                admitted_funded = np.clip(admitted_funded, 0.0, apps)

    spillover = np.maximum(apps - admitted_funded, 0.0)
    assert float(admitted_funded.sum()) <= seats + 1e-6, "Funded seats exceeded!"
    assert (admitted_funded <= apps + 1e-8).all(), "Admitted exceeded applicants!"

    return dict(
        admitted_funded=admitted_funded,
        spillover=spillover,
        tutoring_part=total_part,
        gate_part=gate_part,
        remedial_part=remedial_part,
        tutoring_spend_per_student=total_spend_per_student,
        h_exam=h_exam,
        h_skill=h_skill,
        kappa=kappa,
        tightness=tightness,
        tax_revenue=tax_revenue,
        effective_e_s=eff_e_s,
    )
