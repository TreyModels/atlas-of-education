"""Credential -> job / earnings link for the v6 prototype.

MASSENG v5 has no labour market: credentials enter only as exogenous wage-premium drivers of schooling demand, and
nothing maps a credential to a job, a formal/informal status or pay. This module adds the missing link in the v6
skeleton's style (plain arrays of expected mass, no hidden global state), with two declared rivals:

QueueLabour
    credential floors + a noisy credential/ability signal, formal vacancies arriving over a declared schedule, fixed
    credential premia, informal fallback, and an explicit waiting queue. Reference vocabulary: Thurow (1975) job
    competition, Spence (1973) signal, Harris-Todaro (1970) waiting/informality.

CompetitiveLabour
    the same formal vacancy stock but selection on true skill and wages that clear a declared supply-response
    schedule, so a credential's premium falls as its share of the cohort rises (Tinbergen 1974; Katz-Murphy 1992).
    No queue: the market clears at entry.

Both are declared, illustrative mechanisms -- not estimates, not a claim that either describes any country. Formal
and informal pay are in units of mean household income per year.

Fractional-mass clearing
-----------------------
Every cell carries expected mass (persons) and a vacancy is a quantity of mass. A cell can be hired *partially*:
the boundary applicant cell is split by the ranking, exactly as in ``education.gate.ranked_admit``. The outcome
``formal`` is therefore the expected *share* of each cell in formal work (in [0, 1]), not a boolean status, and
``income`` is the expected annual income of one person in that cell. Both clearings use the shared mass-aware
ranking, so a 25-vacancy stock never hires more than 25 mass (the old code converted a fraction to a boolean and
hired whole cells: 4x over-hiring in the two-cell test).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .education.gate import ranked_admit

CRED_YEARS = (6.0, 9.0, 12.0, 16.0)     # schooling years: primary, lower sec, upper sec, tertiary
REGIMES = ("queue", "competitive")


@dataclass(frozen=True)
class LabourParams:
    regime: str = "queue"
    vacancies: float = 0.25              # formal vacancies / cohort, total over the vacancy schedule
    vacancy_schedule: tuple = (0.50, 0.30, 0.20)
    floor_routine: int = 2               # formal routine job needs upper-secondary completion
    floor_skilled: int = 3               # formal skilled job needs tertiary completion
    skilled_share: float = 0.40          # share of formal vacancies in the skilled tier
    signal_noise: float = 0.50           # queue only: noise in the employers' signal
    signal_rho: float = 0.40             # queue only: weight on credential vs standardised ability
    w0: float = 1.0                      # base annual wage
    theta_formal: float = 0.06           # log wage per year of schooling, formal
    theta_informal: float = 0.03         # log wage per year of schooling, informal
    informal_relative: float = 0.55      # informal base relative to formal base
    tier_premium: float = 1.25           # skilled-tier formal premium
    queue_min_cred: int = 2              # only upper-secondary leavers may wait for formal work
    queue_max_years: int = 2
    queue_support: float = 0.20          # income while waiting (share of informal wage)
    queue_horizon: float = 6.0           # expected years of formal work in the waiting decision
    queue_k: float = 3.0                 # logit slope of the waiting decision
    sigma: float = 1.6                   # competitive: elasticity of substitution across skill types
    supply_ref: float = 0.30             # competitive: reference credential share for the supply response

    def __post_init__(self):
        if self.regime not in REGIMES:
            raise ValueError(f"unknown labour regime {self.regime!r}")
        if not 0.0 <= self.vacancies <= 1.0:
            raise ValueError("vacancies must be a share of the cohort in [0, 1]")
        if abs(sum(self.vacancy_schedule) - 1.0) > 1e-9:
            raise ValueError("vacancy_schedule must sum to 1")


@dataclass
class LabourOutcome:
    """Expected-mass result of one labour clearing.

    ``formal`` is the expected share of each cell in formal work, in [0, 1] (fractional, never a whole-cell
    indicator). ``income`` is the expected annual income of one person in the cell. ``p_hire`` is the declared
    belief used by the waiting decision (queue regime only), kept in [0, 1] and asserted in the clearing code.
    """

    formal: np.ndarray
    income: np.ndarray
    queue_years: np.ndarray
    accounting: dict
    pay_by_credential: tuple
    formal_by_credential: tuple
    p_hire: np.ndarray = field(default_factory=lambda: np.zeros(0))


def _years(cred):
    return np.asarray([CRED_YEARS[int(c)] for c in cred], float)


def _formal_wage(cred, params):
    return params.w0 * np.exp(params.theta_formal * (_years(cred) - 9.0))


def _informal_wage(cred, params):
    return params.w0 * params.informal_relative * np.exp(params.theta_informal * (_years(cred) - 9.0))


def _hired_mass(mask, capacity, priority, mass):
    """Mass-aware ranking (shared with the gate module: one ranking implementation).

    Returns the expected mass admitted from every cell (0 for cells outside ``mask``); the boundary cell is
    admitted partially, so the returned array sums to ``min(capacity, eligible mass)`` up to floating tolerance.
    """
    admitted, _ = ranked_admit(mask, capacity, priority, mass)
    return admitted


def clear_labour(cred, ability, mass, params: LabourParams, rng) -> LabourOutcome:
    """Map final credentials and ability to formal/informal work and pay."""
    cred = np.asarray(cred, int)
    ability = np.asarray(ability, float)
    mass = np.asarray(mass, float)
    if not (len(cred) == len(ability) == len(mass)):
        raise ValueError("cred, ability and mass must have equal length")
    if (mass < 0).any():
        raise ValueError("mass must be non-negative")
    total = float(mass.sum())
    if total <= 0:
        z = np.zeros(0)
        return LabourOutcome(z.astype(bool), z, z.astype(int), {}, (), ())
    ability_z = (ability - ability.mean()) / (ability.std() + 1e-9)
    if params.regime == "queue":
        outcome = _clear_queue(cred, ability_z, mass, params, rng)
    else:
        outcome = _clear_competitive(cred, ability_z, mass, params)
    formal, income, queue_years = outcome["formal"], outcome["income"], outcome["queue_years"]
    formal = np.clip(np.asarray(formal, float), 0.0, 1.0)     # expected share of each cell in formal work
    formal_mass = formal * mass
    informal_mass = mass - formal_mass
    cred_shares = [float(mass[cred == c].sum() / total) for c in range(4)]
    pay_by_cred, formal_by_cred = [], []
    for c in range(4):
        m = (cred == c) & (mass > 0)
        pay_by_cred.append(float(np.average(income[m], weights=mass[m])) if m.any() else float("nan"))
        formal_by_cred.append(float(np.average(formal[m], weights=mass[m])) if m.any() else float("nan"))
    has_formal = bool(formal_mass.sum() > 1e-12)
    has_informal = bool(informal_mass.sum() > 1e-12)
    formal_mean_pay = float(np.average(income, weights=formal_mass)) if has_formal else float("nan")
    informal_mean_pay = float(np.average(income, weights=informal_mass)) if has_informal else float("nan")
    accounting = dict(
        regime=params.regime, vacancies=params.vacancies,
        formal_share=float(formal_mass.sum() / total),
        queue_share=float(np.average(queue_years > 0, weights=mass)),
        mean_queue_years=float(np.average(queue_years, weights=mass)),
        credential_shares=cred_shares,
        mean_income=float(np.average(income, weights=mass)),
        formal_mean_pay=formal_mean_pay,
        informal_mean_pay=informal_mean_pay,
        formal_minus_informal=(formal_mean_pay - informal_mean_pay
                               if has_formal and has_informal else float("nan")),
        skills_mean_years=float(np.average(_years(cred), weights=mass)),
        formal_by_credential=formal_by_cred,
    )
    return LabourOutcome(formal=formal, income=income, queue_years=queue_years, accounting=accounting,
                         pay_by_credential=tuple(pay_by_cred), formal_by_credential=tuple(formal_by_cred),
                         p_hire=np.asarray(outcome.get("p_hire", np.zeros(0)), float))


def _clear_queue(cred, ability_z, mass, p: LabourParams, rng):
    """Queue clearing on fractional mass.

    Vacancies arrive in declared rounds; each tier ranks the remaining *mass* and can split the boundary cell.
    Status-year income is accumulated over the rounds: formal hires earn from the round they are hired onward,
    informal leavers from the round they leave onward, and waiters receive ``queue_support`` while waiting.

    The waiting decision is the pre-registered deterministic threshold (PRE_REGISTRATION_GATE_JOBS, declared
    model: "queue decision = wait if expected formal-minus-informal gain over the horizon exceeds informal
    income"), not an undeclared logit draw. ``p_hire[c]`` is the declared belief "chance a queuer of credential
    c is hired this year", so it is updated from the hires observed among the previous round's waiters -- not
    from all eligible mass. Both changes are required for the vacancy stock to clear at its declared mass: the
    old code (and a random logit) let early informal exits starve later vacancy rounds.
    """
    n = len(cred)
    total = float(mass.sum())
    formal_mass = np.zeros(n)          # expected formal mass (persons), accumulated over rounds
    formal_wage_mass = np.zeros(n)     # formal mass weighted by the tier premium
    informal_mass = np.zeros(n)        # expected mass that has taken informal work and stays there
    income_mass = np.zeros(n)          # status-year income, summed over the vacancy rounds
    queue_years = np.zeros(n, int)
    w_formal = _formal_wage(cred, p)
    w_informal = _informal_wage(cred, p)
    p_hire = {c: 0.30 for c in range(4)}       # prior belief before any queuer is observed
    prev_wait = np.zeros(n, bool)             # cells that chose to wait in the previous round
    signal = (p.signal_rho * cred / 3.0 + (1.0 - p.signal_rho) * ability_z
              + p.signal_noise * rng.standard_normal(n))
    remaining = mass.copy()            # expected mass still searching for (or queuing for) formal work
    left = np.zeros(n, bool)           # cells whose remaining mass has taken informal work
    rounds = len(p.vacancy_schedule)
    for t in range(rounds):
        vac_total = p.vacancies * total * p.vacancy_schedule[t]
        pool = ~left & (remaining > 1e-12)
        round_hired = np.zeros(n)      # expected formal mass hired in this round
        for tier, floor, share in (("skilled", p.floor_skilled, p.skilled_share),
                                   ("routine", p.floor_routine, 1.0 - p.skilled_share)):
            cap = vac_total * share
            mask = pool & (cred >= floor) & (remaining > 1e-12)
            if cap <= 0 or not mask.any():
                continue
            adm = _hired_mass(mask, cap, signal, remaining)
            hired = adm > 1e-12
            if not hired.any():
                continue
            formal_mass += adm
            round_hired += adm
            formal_wage_mass += adm * (p.tier_premium if tier == "skilled" else 1.0)
            remaining = np.maximum(remaining - adm, 0.0)
            pool &= remaining > 1e-12
        # beliefs update from the hires observed among last round's waiters (the declared p_hire meaning)
        for c in range(4):
            was = prev_wait & (cred == c) & (mass > 0)
            denom = float(mass[was].sum())
            if denom > 0:
                h = float(round_hired[was].sum() / denom)
                if not 0.0 <= h <= 1.0:
                    raise AssertionError(f"observed hire share {h!r} outside [0, 1] for credential {c}")
                p_hire[c] = 0.7 * p_hire.get(c, 0.3) + 0.3 * h
        unplaced = ~left & (remaining > 1e-12)
        wait = np.zeros(n, bool)
        if t < rounds - 1 and (unplaced & (cred >= p.queue_min_cred)).any():
            gain = (np.array([p_hire.get(int(c), 0.3) for c in cred]) * (w_formal - w_informal)
                    * p.queue_horizon - w_informal)
            can_wait = unplaced & (cred >= p.queue_min_cred) & (queue_years < p.queue_max_years)
            wait = can_wait & (gain > 0.0)          # pre-registered deterministic waiting rule
            queue_years[wait] += 1
        take_informal = unplaced & ~wait
        informal_mass += np.where(take_informal, remaining, 0.0)
        left |= take_informal
        # status-year incomes: each unit of mass earns from the round it enters a status onward
        income_mass += formal_wage_mass * w_formal + informal_mass * w_informal
        income_mass += np.where(wait, remaining * p.queue_support * w_informal, 0.0)
        remaining = np.where(left, 0.0, remaining)
        prev_wait = wait
    for c, v in p_hire.items():
        if not 0.0 <= v <= 1.0:
            raise AssertionError(f"p_hire[{c}]={v!r} outside [0, 1]")
    income = np.divide(income_mass, np.maximum(mass, 1e-12)) / rounds
    formal = np.divide(formal_mass, np.maximum(mass, 1e-12))
    p_hire_arr = np.array([p_hire.get(c, 0.3) for c in range(4)], float)
    return dict(formal=np.clip(formal, 0.0, 1.0), income=income, queue_years=queue_years, p_hire=p_hire_arr)


def _clear_competitive(cred, ability_z, mass, p: LabourParams):
    """Competitive clearing on fractional mass; expected pay is the formal/informal mixture."""
    n = len(cred)
    total = float(mass.sum())
    shares = np.array([max(float(mass[cred == c].sum() / total), 1e-6) for c in range(4)])
    supply_factor = (p.supply_ref / shares) ** (1.0 / p.sigma)
    w_formal = _formal_wage(cred, p) * supply_factor[cred]
    w_informal = _informal_wage(cred, p)
    skill = ability_z + 0.10 * cred
    formal_mass = np.zeros(n)
    formal_wage_mass = np.zeros(n)
    remaining = mass.copy()
    for tier, floor, share in (("skilled", p.floor_skilled, p.skilled_share),
                               ("routine", p.floor_routine, 1.0 - p.skilled_share)):
        cap = p.vacancies * total * share
        mask = (cred >= floor) & (remaining > 1e-12)
        if cap <= 0 or not mask.any():
            continue
        adm = _hired_mass(mask, cap, skill, remaining)
        formal_mass += adm
        formal_wage_mass += adm * (p.tier_premium if tier == "skilled" else 1.0)
        remaining = np.maximum(remaining - adm, 0.0)
    income = (formal_wage_mass * w_formal + (mass - formal_mass) * w_informal) / np.maximum(mass, 1e-12)
    formal = np.divide(formal_mass, np.maximum(mass, 1e-12))
    return dict(formal=np.clip(formal, 0.0, 1.0), income=income,
                queue_years=np.zeros(n, int), p_hire=np.zeros(0))
