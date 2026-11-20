"""Reduced rival generators for C1 recovery study.
INDEPENDENTLY NAMED NEW IMPLEMENTATIONS, NOT REPRODUCTIONS of Yoo (2011) or any atlas engine.
They exist only to give the recovery study a third in-set rival (a fixed-cutoff model) and a truth
outside the candidate set (random-among-eligible). All produce the SAME six moments as massabm.
"""
import numpy as np
from scipy.special import ndtr

MOMENTS = ['completion', 'tertiary', 'premium', 'formal_share', 'prep_takeup', 'gap_q5_q1']
N = 2000
ZQ = np.array([-1.2816, -0.5244, 0.0, 0.5244, 1.2816])   # quintile midpoints


def _cohort(seed):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(N)
    a = 0.3 * z + np.sqrt(1 - 0.09) * rng.standard_normal(N)
    return rng, z, a


def yoo(t_star=-0.1, beta=0.22, premium=2.2, alpha=1.0, seed=0):
    """Yoo-style fixed standard: score T = alpha*e + eps; choose e to maximise X*P(pass) - beta*e^2."""
    rng, z, a = _cohort(seed)
    eps = rng.standard_normal(N)
    egrid = np.linspace(0, 2.5, 60)
    # X is normalised so that one unit of expected pass probability is worth 1; beta is the cost slope
    X = 1.0
    passgrid = ndtr((alpha * (egrid[None, :] + 0.4 * a[:, None]) - t_star) / 1.0)   # ability shifts prep
    util = X * passgrid - beta * (egrid[None, :] ** 2)
    e = egrid[np.argmax(util, axis=1)]
    score = alpha * (e + 0.4 * a) + eps
    passed = score > t_star
    college = score > t_star + 0.8
    inc_deg = premium
    formal = np.where(passed, 1.0, 0.0) * 0.55 + 0.05
    q = np.searchsorted(np.quantile(z, [0.2, 0.4, 0.6, 0.8]), z)
    return dict(completion=float(passed.mean()), tertiary=float(college.mean()),
                premium=float(inc_deg), formal_share=float(formal.mean()),
                prep_takeup=float((e > 1e-6).mean()),
                gap_q5_q1=float(passed[q == 4].mean() - passed[q == 0].mean()))


def random_eligible(a0=-0.3, a1=0.6, f_formal=0.4, premium=1.08, prep=0.15, seed=0):
    """TRUTH OUTSIDE THE CANDIDATE SET: completion is an exogenous logistic in income; formal jobs are
    allocated at random among the eligible, so the credential carries no premium."""
    rng, z, a = _cohort(seed)
    p = 1 / (1 + np.exp(-(a0 + a1 * z)))
    completed = rng.random(N) < p
    formal = completed & (rng.random(N) < f_formal)
    q = np.searchsorted(np.quantile(z, [0.2, 0.4, 0.6, 0.8]), z)
    return dict(completion=float(completed.mean()), tertiary=float((completed & (rng.random(N) < 0.35)).mean()),
                premium=float(premium), formal_share=float(formal.mean()),
                prep_takeup=float(prep),
                gap_q5_q1=float(completed[q == 4].mean() - completed[q == 0].mean()))
