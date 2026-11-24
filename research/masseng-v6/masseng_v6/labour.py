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
"""
from __future__ import annotations

from dataclasses import dataclass

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
    formal: np.ndarray
    income: np.ndarray
    queue_years: np.ndarray
    accounting: dict
    pay_by_credential: tuple
    formal_by_credential: tuple


def _years(cred):
    return np.asarray([CRED_YEARS[int(c)] for c in cred], float)


def _formal_wage(cred, params):
    return params.w0 * np.exp(params.theta_formal * (_years(cred) - 9.0))


def _informal_wage(cred, params):
    return params.w0 * params.informal_relative * np.exp(params.theta_informal * (_years(cred) - 9.0))


def _hired_frac(mask, capacity, priority, mass):
    """Mass-aware ranking (shared with the gate module: one ranking implementation)."""
    admitted, _ = ranked_admit(mask, capacity, priority, mass)
    return admitted / np.maximum(mass, 1e-12)


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
    cred_shares = [float(mass[cred == c].sum() / total) for c in range(4)]
    pay_by_cred, formal_by_cred = [], []
    for c in range(4):
        m = (cred == c) & (mass > 0)
        pay_by_cred.append(float(np.average(income[m], weights=mass[m])) if m.any() else float("nan"))
        formal_by_cred.append(float(np.average(formal[m], weights=mass[m])) if m.any() else float("nan"))
    accounting = dict(
        regime=params.regime, vacancies=params.vacancies,
        formal_share=float(np.average(formal, weights=mass)),
        queue_share=float(np.average(queue_years > 0, weights=mass)),
        mean_queue_years=float(np.average(queue_years, weights=mass)),
        credential_shares=cred_shares,
        mean_income=float(np.average(income, weights=mass)),
        formal_mean_pay=float(np.average(income[formal], weights=mass[formal])) if formal.any() else float("nan"),
        informal_mean_pay=(float(np.average(income[~formal], weights=mass[~formal]))
                           if (~formal).any() else float("nan")),
        formal_minus_informal=(float(np.average(income[formal], weights=mass[formal])
                                     - np.average(income[~formal], weights=mass[~formal]))
                               if formal.any() and (~formal).any() else float("nan")),
        skills_mean_years=float(np.average(_years(cred), weights=mass)),
        formal_by_credential=formal_by_cred,
    )
    return LabourOutcome(formal=formal, income=income, queue_years=queue_years, accounting=accounting,
                         pay_by_credential=tuple(pay_by_cred), formal_by_credential=tuple(formal_by_cred))


def _clear_queue(cred, ability_z, mass, p: LabourParams, rng):
    n = len(cred)
    total = float(mass.sum())
    formal = np.zeros(n, bool)
    income_mass = np.zeros(n)
    queue_years = np.zeros(n, int)
    w_formal = _formal_wage(cred, p)
    w_informal = _informal_wage(cred, p)
    p_hire = {c: 0.30 for c in range(4)}
    signal = (p.signal_rho * cred / 3.0 + (1.0 - p.signal_rho) * ability_z
              + p.signal_noise * rng.standard_normal(n))
    searching = np.ones(n, bool)
    left = np.zeros(n, bool)
    premium_arr = np.ones(n)
    rounds = len(p.vacancy_schedule)
    for t in range(rounds):
        vac_total = p.vacancies * total * p.vacancy_schedule[t]
        avail = searching & ~left & ~formal          # only the still-unplaced compete for new vacancies
        pool = avail.copy()
        for tier, floor, share in (("skilled", p.floor_skilled, p.skilled_share),
                                   ("routine", p.floor_routine, 1.0 - p.skilled_share)):
            cap = vac_total * share
            mask = pool & (cred >= floor)
            frac = _hired_frac(mask, cap, signal, mass)
            newly = (frac > 0) & mask
            formal |= newly
            premium_arr[newly] = p.tier_premium if tier == "skilled" else 1.0
            pool &= ~newly
            for c in range(4):
                sel = newly & (cred == c)
                denom = mass[(cred == c) & mask].sum()
                if sel.any() and denom > 0:
                    p_hire[c] = 0.7 * p_hire.get(c, 0.3) + 0.3 * float(mass[sel].sum() / denom)
        unhired = avail & ~formal
        wait = np.zeros(n, bool)
        if t < rounds - 1 and (unhired & (cred >= p.queue_min_cred)).any():
            gain = (np.array([p_hire.get(int(c), 0.3) for c in cred]) * (w_formal - w_informal)
                    * p.queue_horizon - w_informal)
            pr_wait = 1.0 / (1.0 + np.exp(-p.queue_k * gain / np.maximum(w_informal, 1e-3)))
            can_wait = unhired & (cred >= p.queue_min_cred) & (queue_years < p.queue_max_years)
            wait = can_wait & (rng.random(n) < pr_wait)
            queue_years[wait] += 1
        take_informal = unhired & ~wait
        left |= take_informal
        # pay for this round: formal workers, informal workers (current), waiters on support
        income_mass += np.where(formal, mass * w_formal * premium_arr, 0.0)
        income_mass += np.where(left, mass * w_informal, 0.0)
        income_mass += np.where(wait, mass * p.queue_support * w_informal, 0.0)
    income = np.divide(income_mass, np.maximum(mass, 1e-12)) / rounds
    return dict(formal=formal, income=income, queue_years=queue_years)


def _clear_competitive(cred, ability_z, mass, p: LabourParams):
    n = len(cred)
    total = float(mass.sum())
    formal = np.zeros(n, bool)
    skilled = np.zeros(n, bool)
    shares = np.array([max(float(mass[cred == c].sum() / total), 1e-6) for c in range(4)])
    supply_factor = (p.supply_ref / shares) ** (1.0 / p.sigma)
    w_formal = _formal_wage(cred, p) * supply_factor[cred]
    w_informal = _informal_wage(cred, p)
    skill = ability_z + 0.10 * cred
    for tier, floor, share in (("skilled", p.floor_skilled, p.skilled_share),
                               ("routine", p.floor_routine, 1.0 - p.skilled_share)):
        cap = p.vacancies * total * share
        mask = (cred >= floor) & ~formal
        frac = _hired_frac(mask, cap, skill, mass)
        newly = (frac > 0) & mask
        formal |= newly
        if tier == "skilled":
            skilled |= newly
    income = np.where(formal, np.where(skilled, w_formal * p.tier_premium, w_formal), w_informal)
    return dict(formal=formal, income=income, queue_years=np.zeros(n, int))
