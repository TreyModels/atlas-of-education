"""Layer 1 (behavioural core) of the v6 gate+jobs prototype: four switchable equation blocks.

The four blocks the Lead's protocol names:
  A. affordability: the scalar cost is replaced by explicit F_pub + H_hidden + forgone child wage, with the four
     schooling/work states school_only, study_and_work, visible_work_only, hidden_work;
  B. learning: L = q_pub(GER) * a * time_school + gamma * T, with public quality diluted by gross enrolment;
  C. gate: a hard rank gate at lower-secondary, upper-secondary and tertiary entry with real seat caps, plus
     bar / quota / exam-pass / Tullock-contest variants;
  D. jobs: credential -> formal/informal job and pay, queue versus competitive clearing (masseng_v6.labour).

Every block has its own switch, so exactly one block can be swapped at a time. The measurement/accounting layer
(dashboard.py) only sees the returned arrays and never a switch. All parameters are declared, illustrative and
unestimated; no causal claims.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

import numpy as np

from masseng_v6.education.gate import Gate, apply_gate
from masseng_v6.labour import LabourParams, clear_labour

DECILES = 10
GATES = 3                      # 0 = entry to lower secondary, 1 = entry to upper secondary, 2 = entry to tertiary
# declared relative income by decile (mean 1 after normalisation)
INCOME_RAW = (0.30, 0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.45, 1.80, 2.40)
INCOME_MULT = np.array(INCOME_RAW) / np.mean(INCOME_RAW)
CRED_VALUE = (0.00, 0.15, 0.35, 0.80)      # value of completing primary, lower sec, upper sec, tertiary


@dataclass
class Params:
    # population
    n: int = 100_000
    seed: int = 0
    # ---- block A: affordability / 4 states
    use_components: bool = True          # False -> scalar cost and two states (school vs visible work)
    F_pub: Tuple[float, float, float] = (0.02, 0.04, 0.08)      # public fee per level, share of mean income
    H_hidden: Tuple[float, float, float] = (0.05, 0.07, 0.10)   # hidden household cost per level
    forgone_share: float = 0.60          # forgone child wage = child_wage x school time x forgone_share
    child_wage: float = 0.18             # full-time child wage, share of mean income
    scalar_cost: float = 0.10            # v5-style scalar cost per year when use_components=False
    work_share: float = 0.50             # study_and_work: share of time in work
    hidden_work_income: float = 0.70     # hidden work pays this fraction of the child wage
    hidden_work_shifter: float = 0.10    # declared preference for hidden (unmeasured) work
    study_work_shifter: float = 0.05
    b_school: float = 1.00               # declared consumption/option value of being in school this level
    beta_ret: float = 1.00               # weight on the next credential's value
    beta_income: float = 0.20            # log-income taste for school (and work)
    lam_cost: float = 1.20               # cost-burden sensitivity
    beta_work: float = 0.70              # weight on the child's work income
    # ---- block B: learning
    use_learning: bool = True
    q0: float = 1.00                     # public school quality scale
    ger_ref: float = 0.65                # reference enrolment ratio for quality dilution
    dilution_alpha: float = 0.50         # q_pub = q0 * (ger_ref / GER)^alpha, clipped
    gamma: float = 0.55                  # tutoring/prep learning return per unit of prep intensity
    learning_noise: float = 0.50
    # ---- block C: gate
    use_gate: bool = True
    caps: Tuple[float, float, float] = (0.95, 0.65, 0.30)       # seats as share of the cohort
    rules: Tuple[str, str, str] = ("bar", "bar", "bar")
    bars: Tuple[float, float, float] = (-2.0, -0.50, 0.00)
    quota_share: float = 0.30
    quota_group_max: int = 2             # bottom three deciles
    quota_threshold: float = -0.50
    pass_rate: float = 0.80
    tullock_scale: float = 0.50
    # ---- block D: jobs
    use_jobs: bool = True
    labour_regime: str = "queue"
    vacancies: float = 0.25
    signal_noise: float = 0.50
    sigma: float = 1.60
    # ---- prep (tutoring) demand
    prep_on: bool = True
    prep_form: str = "linear"            # 'linear' or 'concave' return to prep intensity
    prep_cost_share: Tuple[float, float, float] = (0.02, 0.03, 0.04)
    prep_scale: float = 0.50             # logistic scale of the admission-probability approximation
    prep_levels: Tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 1.00)
    # ---- test-control switches (not structural claims)
    signal_strength: float = 1.0         # 0 -> learning-block content has zero strength (zero-signal control A)
    selection_strength: float = 1.0      # 0 -> exam scores carry no signal (zero-signal control B)
    ablate_shared: bool = False          # T4 shared-code ablation: constant ability and constant decile
    # ---- labour heterogeneities (multiverse)
    labour_overrides: dict = field(default_factory=dict)

    def labour_params(self, vacancies=None, signal_noise=None, sigma=None):
        kw = dict(regime=self.labour_regime, vacancies=self.vacancies,
                  signal_noise=self.signal_noise, sigma=self.sigma)
        kw.update(self.labour_overrides)
        if vacancies is not None:
            kw["vacancies"] = vacancies
        if signal_noise is not None:
            kw["signal_noise"] = signal_noise
        if sigma is not None:
            kw["sigma"] = sigma
        return LabourParams(**kw)


def _gumbel(u):
    u = np.clip(u, 1e-12, 1 - 1e-12)
    return -np.log(-np.log(u))


def _mnl_choice(utilities, uniforms):
    """utilities: (n, k); uniforms: (n, k) pre-drawn; returns chosen index."""
    return np.argmax(utilities + _gumbel(uniforms), axis=1)


def simulate(p: Params) -> dict:
    """Run the four-block toy for one seed. Returns raw arrays only (no measurement)."""
    rng = np.random.default_rng(p.seed)
    n = p.n
    # all randomness drawn up front, independent of any switch, so a block set to zero strength cannot change
    # the random draw order (this is what makes the zero-signal control meaningful)
    decile = rng.integers(0, DECILES, n)
    ability = rng.standard_normal(n)
    if p.ablate_shared:
        ability = np.zeros(n)
        decile = np.full(n, 5, dtype=int)
    st_unif = rng.random((n, GATES, 4))
    gate_noise = rng.standard_normal((n, GATES))
    prep_unif = rng.random((n, 1))          # unused tie-break, kept for reproducible draw order
    income = INCOME_MULT[decile]
    z_inc = (income - 1.0) / income.std()

    cred = np.zeros(n, dtype=int)           # highest completed credential (0 primary .. 3 tertiary)
    state = np.full((n, GATES), -1, dtype=int)   # 0 school_only,1 study_and_work,2 visible_work,3 hidden_work
    prep = np.zeros((n, GATES))
    prep_spend = np.zeros(n)                # share of household income
    learning = np.full((n, GATES), np.nan)
    score = np.full((n, GATES), np.nan)
    admitted = np.zeros((n, GATES), bool)
    reject_reason = np.full((n, GATES), -1, dtype=int)   # 0 below bar, 1 capacity, 2 exam, 3 no school state
    ger = np.full(GATES, np.nan)
    q_pub = np.full(GATES, np.nan)
    ger_prev = p.ger_ref
    alive = np.ones(n, bool)                # still in the schooling pipeline

    for g in range(GATES):
        elig = alive.copy()
        if not p.use_gate:
            elig[:] = alive
        # ---------------- block A: affordability and the four schooling/work states
        if p.use_components:
            fee = p.F_pub[g] + p.H_hidden[g]
            forgone = p.forgone_share * p.child_wage
            u_school = (p.b_school + p.beta_ret * CRED_VALUE[g + 1] + p.beta_income * np.log(income)
                        - p.lam_cost * (fee + forgone) / income)
            u_study_work = (p.b_school + p.beta_ret * CRED_VALUE[g + 1] * (1 - 0.5 * p.work_share)
                            + p.beta_income * np.log(income)
                            - p.lam_cost * fee / income
                            + p.beta_work * p.work_share * p.child_wage / income
                            + p.study_work_shifter)
            u_visible = (p.beta_income * np.log(income)
                         + p.beta_work * p.child_wage / income)
            u_hidden = (p.beta_income * np.log(income)
                        + p.beta_work * p.hidden_work_income * p.child_wage / income
                        + p.hidden_work_shifter)
            utils = np.stack([u_school, u_study_work, u_visible, u_hidden], axis=1)
            st = _mnl_choice(utils, st_unif[:, g, :])
        else:
            fee = p.scalar_cost
            forgone = 0.0
            u_school = (p.b_school + p.beta_ret * CRED_VALUE[g + 1] + p.beta_income * np.log(income)
                        - p.lam_cost * fee / income)
            u_work = p.beta_income * np.log(income) + p.beta_work * p.child_wage / income
            utils = np.stack([u_school, np.full(n, -1e9), u_work, np.full(n, -1e9)], axis=1)
            st2 = _mnl_choice(utils, st_unif[:, g, :])
            st = np.where(st2 == 0, 0, 2)
        state[:, g] = np.where(elig, st, -1)
        in_school = elig & (st <= 1)
        # public quality is diluted by the PREVIOUS level's realised enrolment ratio (declared one-level lag)
        if p.use_learning:
            q_dil = p.q0 * np.clip(p.ger_ref / max(ger_prev, 1e-6), 0.5, 2.0) ** p.dilution_alpha
            q = 1.0 + p.signal_strength * (q_dil - 1.0)
            time_school = np.where(st == 0, 1.0, np.where(st == 1, 1.0 - p.work_share, 0.0))
            base_learn = q * ability * time_school
        else:
            q = 1.0
            time_school = np.where(st == 0, 1.0, np.where(st == 1, 1.0 - p.work_share, 0.0))
            base_learn = ability * time_school        # == the signal_strength -> 0 limit of the block above
        q_pub[g] = float(q)
        # ---------------- prep decision (tutoring) against the gate
        prep_gain = np.zeros(n)
        if p.prep_on and p.use_gate and p.selection_strength > 0 and in_school.any():
            prep_gain, chosen = _prep_choice(p, g, base_learn, in_school, income, rng,
                                             p.gamma * p.signal_strength)
            prep[:, g] = np.where(in_school, chosen, 0.0)
            prep_spend += np.where(in_school, p.prep_cost_share[g] * prep[:, g] / income, 0.0)
        learning[:, g] = np.where(in_school, base_learn + prep_gain, np.nan)
        # ---------------- block C: gate
        if p.use_gate:
            tie = np.arange(n, dtype=float) / max(n, 1)      # declared deterministic tie-break, independent of ability
            sc = np.where(in_school, p.selection_strength * (learning[:, g]
                                                             + p.learning_noise * gate_noise[:, g]) + 1e-9 * tie,
                          np.nan)
            score[:, g] = sc
            cap = p.caps[g] * n
            gate = Gate(kind=p.rules[g], capacity=cap, threshold=p.bars[g],
                        quota_share=p.quota_share, quota_threshold=p.quota_threshold,
                        quota_group_max=p.quota_group_max, pass_rate=p.pass_rate,
                        tullock_scale=p.tullock_scale, label=f"gate{g}")
            safe = np.where(in_school, np.nan_to_num(sc, nan=-1e9), -1e9)
            out = apply_gate(gate, safe, np.ones(n), in_school, decile, rng=np.random.default_rng(p.seed * 100 + g))
            admitted[:, g] = out.admitted_mass > 0
            # rejection reasons: exam, below bar, capacity
            acc = out.accounting
            if gate.kind == "exam":
                rng_g = np.random.default_rng(p.seed * 100 + g)
                passed = rng_g.random(n) < gate.pass_rate
                reject_reason[in_school & ~passed, g] = 2
                reject_reason[in_school & passed & ~admitted[:, g], g] = 1
            elif gate.kind in ("bar", "quota"):
                reject_reason[in_school & ~admitted[:, g], g] = 0
            else:
                reject_reason[in_school & ~admitted[:, g], g] = 1
            # those who pass the gate complete the level; those who do not leave
            cred[admitted[:, g]] = g + 1
            alive = admitted[:, g]
        else:
            learning[:, g] = np.where(in_school, learning[:, g], np.nan)
            score[:, g] = np.where(in_school, p.selection_strength * (learning[:, g]
                                                                      + p.learning_noise * gate_noise[:, g]), np.nan)
            admitted[:, g] = in_school
            cred[in_school] = g + 1
            alive = in_school
        ger[g] = float(admitted[:, g].sum() / n)
        ger_prev = ger[g]
        if not alive.any():
            break
    # ---------------- block D: jobs
    formal = np.zeros(n, bool)
    pay = np.full(n, np.nan)
    queue_years = np.zeros(n, int)
    lab = {}
    if p.use_jobs:
        lo = clear_labour(cred, ability, np.ones(n), p.labour_params(),
                          np.random.default_rng(p.seed + 991))
        formal, pay, queue_years = lo.formal, lo.income, lo.queue_years
        lab = lo.accounting
    hidden_income = np.where(state[:, -1] == 3, p.hidden_work_income * p.child_wage, 0.0)
    return dict(n=n, seed=p.seed, decile=decile, income=income, ability=ability, state=state,
                prep=prep, prep_spend=prep_spend, learning=learning, score=score, admitted=admitted,
                reject_reason=reject_reason, cred=cred, ger=ger, q_pub=q_pub,
                formal=formal, pay=pay, queue_years=queue_years, labour=lab,
                hidden_income=hidden_income)


def _prep_choice(p: Params, g: int, base_learn, in_school, income, rng, gamma_eff):
    """Choose prep intensity on a declared grid by expected admission value minus cost.

    Expected admission probability uses a declared logistic approximation around the no-prep cut implied by the
    seat cap; the decision is iterated twice as prep shifts the expected cut. Not an estimate of any regression.
    """
    elig = in_school
    n = len(income)
    levels = np.array(p.prep_levels, float)
    if p.prep_form == "linear":
        ret = gamma_eff * levels
    else:
        ret = gamma_eff * np.sqrt(levels)
    val = CRED_VALUE[g + 1]
    best = np.zeros(n)
    best_u = np.full(n, -np.inf)
    scores0 = base_learn[elig]
    cap_share = min(1.0, p.caps[g] * n / max(elig.sum(), 1))
    cap_cut = np.quantile(scores0, 1.0 - cap_share) if (len(scores0) and cap_share < 1.0) else -np.inf
    cut = max(cap_cut, p.bars[g]) if p.rules[g] in ('bar', 'quota', 'exam') else cap_cut
    for _ in range(2):
        for li, s in enumerate(levels):
            cost = p.prep_cost_share[g] * s / income
            p_adm = 1.0 / (1.0 + np.exp(-(base_learn + ret[li] - cut) / max(p.prep_scale, 1e-9)))
            p0 = 1.0 / (1.0 + np.exp(-(base_learn - cut) / max(p.prep_scale, 1e-9)))
            u = (p_adm - p0) * val - p.lam_cost * cost
            better = (u > best_u) & elig
            best[better] = s
            best_u[better] = u[better]
        # update the expected cut once prep changes the score distribution
        chosen_ret = gamma_eff * best if p.prep_form == "linear" else gamma_eff * np.sqrt(best)
        new_scores = scores0 + chosen_ret[elig]
        cap_cut = np.quantile(new_scores, 1.0 - cap_share) if (len(new_scores) and cap_share < 1.0) else -np.inf
        cut = max(cap_cut, p.bars[g]) if p.rules[g] in ('bar', 'quota', 'exam') else cap_cut
    return ret[np.searchsorted(levels, best)], best
