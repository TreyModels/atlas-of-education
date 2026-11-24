"""First-pass placement model for the shadow-education equations.

All equations are placed where first-order reasoning says they belong; the literature
check comes after the build.  Catalogue numbers in comments refer to Trey's pasted
"Master Equation Inventory" (1-183).  Every parameter is illustrative, not estimated.

Modules
  household demand   : MNL over none / own-teacher / other-teacher / commercial
                       (catalogue 23, 57-63, budget 70; elasticities 65-69 as outputs)
  learning production: CES school/tutoring nest (26, 28, 30-31, 71-75), SES interaction 76
  admissions gate    : score bar vs quota seats (81-82; contest form deferred)
  earnings           : Mincer equation (42-43) with admission/credential shift
  distribution       : Gini, gaps, concentration index (123-131)
"""
from dataclasses import dataclass, replace, asdict
import numpy as np


@dataclass
class Params:
    n: int = 20000
    seed: int = 0
    # population
    mu_log_y: float = 0.0
    sigma_log_y: float = 0.6
    urban_share: float = 0.40
    q_mean: float = 0.70
    q_sd: float = 0.12
    # school / tutoring inputs
    hours_school: float = 1.0
    hours_tutor: float = 1.2
    rho_ces: float = 0.5
    omega_school: float = 0.5
    ces_scale: float = 1.2
    ability_effect: float = 0.25
    ses_interaction: float = 0.15
    noise_sd: float = 0.15
    # demand MNL (catalogue 23 / 57-63)
    b0: float = -0.5
    b_income: float = 0.55
    b_ability: float = 0.20
    b_school_gap: float = 0.80
    b_teacher: float = 0.30
    price_fee: float = 1.0
    price_other: float = 0.8
    price_commercial: float = 1.5
    cost_other: float = 0.5
    cost_commercial: float = 1.0
    rural_other_extra: float = 0.2
    rural_commercial_extra: float = 0.7
    # policy levers
    ban_own: bool = False
    rural_access: bool = False
    transfer_q1: float = 0.0
    # gate (81-82; quota variant)
    quota: bool = False
    quota_share_low: float = 0.30
    seat_share: float = 0.50
    years_add: float = 3.0
    # earnings (42-43)
    earn_alpha: float = 0.5
    earn_school: float = 0.08
    earn_ability: float = 0.10
    earn_admit: float = 0.15
    earn_noise: float = 0.20


def _softmax(V):
    V = np.asarray(V, float)
    V = V - V.max(axis=1, keepdims=True)
    E = np.exp(V)
    return E / E.sum(axis=1, keepdims=True)


def gini(x):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    s = x.sum()
    if n == 0 or s <= 0:
        return float("nan")
    idx = np.arange(1, n + 1)
    return float(2.0 * np.sum(idx * x) / (n * s) - (n + 1) / n)


def concentration_index(x, y):
    """Concentration index of x ranked by y (catalogue 131)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if x.mean() == 0 or len(x) < 2:
        return float("nan")
    order = np.argsort(y)
    xs = x[order]
    n = len(xs)
    ranks = (np.arange(1, n + 1) - 0.5) / n
    cov = np.mean((xs - xs.mean()) * (ranks - ranks.mean()))
    return float(2.0 * cov / xs.mean())


def _income_elasticity(Y, spend):
    """OLS slope of log spending on log income among takers (catalogue 65-66)."""
    m = spend > 0
    if m.sum() < 10:
        return float("nan")
    ly = np.log(Y[m])
    ls = np.log(spend[m])
    A = np.column_stack([np.ones(len(ly)), ly])
    coef, *_ = np.linalg.lstsq(A, ls, rcond=None)
    return float(coef[1])


def simulate(p: Params) -> dict:
    rng = np.random.default_rng(p.seed)
    n = p.n

    # population
    Y = np.exp(p.mu_log_y + p.sigma_log_y * rng.standard_normal(n))
    ability = rng.standard_normal(n)
    urban = rng.random(n) < p.urban_share
    q = np.clip(p.q_mean + p.q_sd * rng.standard_normal(n) + 0.05 * urban, 0.20, 1.00)
    teacher_q = 0.20 * rng.standard_normal(n)

    # cash transfer to bottom quintile (policy; illustrative)
    q1_cut = np.quantile(Y, 0.20)
    if p.transfer_q1 > 0:
        Y = Y * np.where(Y <= q1_cut, 1.0 + p.transfer_q1, 1.0)
    logY = np.log(Y)

    # provider non-price costs; rural access lowers them
    other_cost = np.full(n, p.cost_other)
    com_cost = np.full(n, p.cost_commercial)
    if not p.rural_access:
        other_cost = other_cost + p.rural_other_extra * (~urban)
        com_cost = com_cost + p.rural_commercial_extra * (~urban)

    # demand: MNL utilities (catalogue 23)
    common = (p.b_income * logY + p.b_ability * ability
              + p.b_school_gap * (1.0 - q) + p.b_teacher * teacher_q + 0.30 * urban)
    V = np.zeros((n, 4))
    V[:, 1] = p.b0 + common - p.price_fee          # own teacher
    V[:, 2] = p.b0 - other_cost + common - p.price_other
    V[:, 3] = p.b0 - com_cost + common - p.price_commercial
    if p.ban_own:
        V[:, 1] = -1e9                              # option removed, not re-priced
    probs = _softmax(V)

    u = rng.random(n)
    choice = (u[:, None] > np.cumsum(probs, axis=1)).sum(axis=1)
    choice = np.clip(choice, 0, 3)

    # spending and tutoring hours
    price = np.where(choice == 1, p.price_fee,
                     np.where(choice == 2, p.price_other,
                              np.where(choice == 3, p.price_commercial, 0.0)))
    spend = np.where(choice > 0, price * p.hours_tutor, 0.0)
    H = np.where(choice > 0, p.hours_tutor, 0.0)

    # learning production: CES nest (catalogue 30-31, 71-75)
    S = p.hours_school * q
    ces = (p.omega_school * S ** p.rho_ces
           + (1.0 - p.omega_school) * H ** p.rho_ces) ** (1.0 / p.rho_ces)
    tutor_dummy = (choice > 0).astype(float)
    learn = (p.ces_scale * ces + p.ability_effect * ability
             + p.ses_interaction * tutor_dummy * logY
             + rng.normal(0.0, p.noise_sd, n))

    # admissions gate: bar vs quota (catalogue 81-82; contest form deferred)
    total_seats = int(round(p.seat_share * n))
    if p.quota:
        # Hard quota: reserved seats are contested only by the bottom 40% by income;
        # the remaining seats are contested only by the rest.  This is the strong
        # reserved-seat reading of the quota gate, chosen to make the mechanism bite.
        low = Y <= np.quantile(Y, 0.40)
        reserved = int(round(p.quota_share_low * total_seats))
        admitted = np.zeros(n, bool)
        low_idx = np.where(low)[0]
        order_low = low_idx[np.argsort(-learn[low_idx])]
        admitted[order_low[:min(reserved, len(order_low))]] = True
        remaining = max(total_seats - int(admitted.sum()), 0)
        high_idx = np.where(~low)[0]
        if remaining > 0 and len(high_idx) > 0:
            order_high = high_idx[np.argsort(-learn[high_idx])]
            admitted[order_high[:min(remaining, len(order_high))]] = True
    else:
        cutoff = np.quantile(learn, 1.0 - p.seat_share)
        admitted = learn >= cutoff

    # earnings: Mincer with admission shift (catalogue 42-43)
    schooling = 9.0 + p.years_add * admitted.astype(float)
    lnw = (p.earn_alpha + p.earn_school * schooling
           + p.earn_ability * ability + p.earn_admit * admitted.astype(float)
           + rng.normal(0.0, p.earn_noise, n))
    earnings = np.exp(lnw)

    # income quintiles (post-transfer)
    cuts = np.quantile(Y, [0.2, 0.4, 0.6, 0.8])
    qb = np.searchsorted(cuts, Y, side="right")  # 0..4

    part = choice > 0
    metrics = {
        "tut_participation": float(part.mean()),
        "own_share": float((choice == 1).mean()),
        "other_share": float((choice == 2).mean()),
        "com_share": float((choice == 3).mean()),
        "spend_share": float((spend / Y).mean()),
        "income_elasticity": _income_elasticity(Y, spend),
        "learning_mean": float(learn.mean()),
        "learning_gini": gini(learn),
        "learning_gap_q5_q1": float(learn[qb == 4].mean() - learn[qb == 0].mean()),
        "admission_rate": float(admitted.mean()),
        "admission_q1": float(admitted[qb == 0].mean()),
        "admission_q5": float(admitted[qb == 4].mean()),
        "admission_gap_q5_q1": float(admitted[qb == 4].mean() - admitted[qb == 0].mean()),
        "earnings_gini": gini(earnings),
        "earnings_mean": float(earnings.mean()),
        "tut_gap_q5_q1": float(part[qb == 4].mean() - part[qb == 0].mean()),
        "spend_concentration_index": concentration_index(spend, Y),
        "part_concentration_index": concentration_index(part.astype(float), Y),
    }
    return metrics


def price_elasticity(base: Params, seeds=10, step=0.10):
    """Numerical own-price elasticity of participation (catalogue 67)."""
    els = []
    for seed in range(seeds):
        lo = replace(base, seed=seed, price_fee=base.price_fee * (1 - step))
        hi = replace(base, seed=seed, price_fee=base.price_fee * (1 + step))
        p_lo = simulate(lo)["tut_participation"]
        p_hi = simulate(hi)["tut_participation"]
        if p_lo > 0 and p_hi > 0:
            els.append((np.log(p_hi) - np.log(p_lo)) / (np.log(1 + step) - np.log(1 - step)))
    return float(np.mean(els)) if els else float("nan")


# Scenarios declared in PRE_REGISTRATION.md
SCENARIOS = {
    "baseline": {},
    "quota": {"quota": True},
    "ban_own": {"ban_own": True},
    "rural_access": {"rural_access": True},
    "cash_transfer": {"transfer_q1": 0.30},
    "quota_ban": {"quota": True, "ban_own": True},
    "quota_rural": {"quota": True, "rural_access": True},
}


def run_scenarios(base: Params, seeds=10, scenarios=None):
    scenarios = scenarios or SCENARIOS
    out = {}
    per_seed = {}
    for name, kw in scenarios.items():
        rows = [simulate(replace(base, seed=s, **kw)) for s in range(seeds)]
        keys = rows[0].keys()
        agg = {}
        for k in keys:
            vals = np.array([r[k] for r in rows], float)
            agg[k] = {"mean": float(np.nanmean(vals)), "sd": float(np.nanstd(vals, ddof=1)) if len(vals) > 1 else 0.0}
        out[name] = agg
        per_seed[name] = rows
    # paired deltas vs baseline
    deltas = {}
    for name in scenarios:
        if name == "baseline":
            continue
        d = {}
        for k in per_seed["baseline"][0].keys():
            diffs = np.array([per_seed[name][s][k] - per_seed["baseline"][s][k] for s in range(seeds)], float)
            d[k] = {"mean": float(np.nanmean(diffs)), "sd": float(np.nanstd(diffs, ddof=1)) if len(diffs) > 1 else 0.0}
        deltas[name] = d
    return out, deltas, per_seed
