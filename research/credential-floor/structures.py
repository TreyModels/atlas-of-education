"""Four rival structures for the credential-floor household model.

This file leaves engine/ untouched. It copies the household simulation from
engine/relfloor_countries.py (function `sim`) with attribution, and adds:

  * a fourth structure, M_RRA (relative risk aversion, Breen & Goldthorpe 1997);
  * graded liquidity as the default (the repo's --smooth-liq variant);
  * hooks used by the two experiments (early stopping, counterfactual changes,
    detail outputs for one survey year).

THE VALUE OF COMPLETING THE CREDENTIAL (present value, in the repo's stylised units)
  HC   human capital : Hz * premium * exp(gamma * ability)          (as in the repo)
  POS  positional    : Hz * b_pos * share of previous cohort holding it   (as in the repo)
  REL  relational    : Hz * b_rel, the same for every household         (as in the repo)
  RRA  relative risk aversion (NEW): Hz * b_rra * step(rank)
       'rank' is the household's position in the income distribution, from 0 (poorest)
       to 1 (richest). 'step' is a smooth step around a threshold rank tau:
       step = 1 / (1 + exp(-(rank - tau) / 0.05)). Households well above tau get the
       full b_rra: they need the credential to avoid falling below their parents'
       class position. Households well below tau get about zero: they already match
       their position without it. Like REL it does not depend on the child's ability;
       unlike REL it depends on the family's own position.
       The step width 0.05 is fixed, not estimated.

THE FOUR STRUCTURES
  M_HC   HC only                (b_pos = b_rel = b_rra = 0)
  M_POS  HC + POS               (b_rel = b_rra = 0)
  M_REL  HC + POS + REL         (b_rra = 0)          [the repo's M_REL]
  M_RRA  HC + RRA               (b_pos = b_rel = 0)  [new]
M_RRA does not nest the other three; it is a rival, not an extension. It has two new
parameters with uniform priors: b_rra ~ U(0, 0.8) (same range as b_rel) and
tau ~ U(0.3, 0.9).

Everything else (costs, taste shock, liquidity constraint, income growth, ability-income
correlation 0.3) is as in engine/relfloor_countries.py. The Cambodia configuration is used.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from relfloor import PRIORS, HZ                      # read-only imports from engine/
import relfloor_countries as rc                      # targets, tolerances, config

YEARS = rc.YEARS
yi = rc.yi
STRUCTS = ['M_HC', 'M_POS', 'M_REL', 'M_RRA']
CFG = rc.CFG['Cambodia']
KHM_Q = rc.KHM_Q
NEW_PRIORS = {'b_rra': (0.0, 0.8), 'tau': (0.3, 0.9)}
RRA_WIDTH = 0.05
SURVEY_YEARS = (2014, 2021)

def draw(rng, S, cfg=CFG, graded=True):
    """Draw one parameter set from the prior for structure S."""
    th = {k: rng.uniform(*v) for k, v in PRIORS.items()}
    th['s_liq'] = rng.uniform(0.1, 1.0) if graded else 0.0
    th['mu'] = rng.uniform(*cfg['mu']); th['g'] = rng.uniform(*cfg['g'])
    th['b_rra'] = rng.uniform(*NEW_PRIORS['b_rra']); th['tau'] = rng.uniform(*NEW_PRIORS['tau'])
    if S == 'M_HC':   th['b_pos'] = th['b_rel'] = th['b_rra'] = 0.0
    elif S == 'M_POS': th['b_rel'] = th['b_rra'] = 0.0
    elif S == 'M_REL': th['b_rra'] = 0.0
    elif S == 'M_RRA': th['b_pos'] = th['b_rel'] = 0.0
    return th

def simulate(th, n=1500, seed=0, until=2021, liq='graded', cfg=CFG,
             prem_scale=None, transfer=None, detail_year=None, checkpoints=None):
    """Simulate cohorts 1998..until. Returns {'c': completion by year,
    'q': completion by income quintile by year, ...}.

    liq: 'graded' (default; chance of financing rises smoothly with log income) or
         'hard' (the repo's threshold). 'hard' ignores th['s_liq'].
    prem_scale: (first_year, factor) multiplies the relative premium from first_year on.
    transfer: (year, amount) adds `amount` to income of the bottom 40% in that year only.
    detail_year: also return household-level outputs for that year (see below).
    checkpoints: {year: f(out_so_far) -> bool}; if f returns False the run stops and
         returns None (early rejection; the random stream is the same as a full run).
    """
    rng = np.random.default_rng(seed)
    logy0 = rng.normal(th['mu'], 0.7, n)
    ab = 0.3 * (logy0 - logy0.mean()) / 0.7 + np.sqrt(1 - 0.09) * rng.normal(size=n)
    q = np.searchsorted(np.quantile(logy0, [.2, .4, .6, .8]), logy0)
    rank = (np.argsort(np.argsort(logy0)) + 0.5) / n
    step = 1.0 / (1.0 + np.exp(-(rank - th['tau']) / RRA_WIDTH)) if th.get('b_rra', 0) != 0 else 0.0
    pm = np.full(len(YEARS), th['prem0'])
    if prem_scale is not None:
        pm[YEARS >= prem_scale[0]] *= prem_scale[1]
    s_prev = 0.3
    c_ = th['direct'] + th['forgo']
    thresh = th['y_sub'] + th['kappa'] * c_
    out = {'c': [], 'q': []}
    detail = None
    for t, yr in enumerate(YEARS):
        if yr > until: break
        y = np.exp(logy0) * (1 + th['g']) ** (yr - 1998)
        if transfer is not None and yr == transfer[0]:
            y = y.copy(); y[q <= 1] += transfer[1]
        R = HZ * (pm[t] * np.exp(th['gamma'] * ab) + th['b_pos'] * s_prev + th['b_rel']
                  + th.get('b_rra', 0.0) * step)
        want = R - cfg['L'] * c_ + rng.logistic(0, th['sig'], n) > 0
        if liq == 'graded' and th.get('s_liq', 0) > 0:
            pf = th['p_fin'] + (1 - th['p_fin']) / (1 + np.exp(-(np.log(y) - np.log(thresh)) / th['s_liq']))
            fin = rng.random(n) < pf
        else:
            fin = (y >= thresh) | (rng.random(n) < th['p_fin'])
        stay = want & fin
        s_prev = stay.mean()
        out['c'].append(s_prev)
        out['q'].append([stay[q == i].mean() for i in range(5)])
        if checkpoints and yr in checkpoints and not checkpoints[yr](out):
            return None
        if detail_year is not None and yr == detail_year:
            # rerouting among those who exit: same rule as engine/relfloor.py (1 year, half
            # cost, 30% of the HC value, r_nc of the relational value; for M_RRA r_nc of the
            # class-maintenance value). Uses its own random stream so the main one is untouched.
            r2 = np.random.default_rng(seed + 7919)
            R_nc = HZ * (0.3 * pm[t] * np.exp(th['gamma'] * ab)
                         + th['r_nc'] * (th['b_rel'] + th.get('b_rra', 0.0) * step))
            can_nc = y >= th['y_sub'] + 0.5 * th['kappa'] * c_ * 0.5
            reroute = ~stay & can_nc & (R_nc - 0.5 * c_ + r2.logistic(0, th['sig'], n) > 0)
            detail = dict(stay=stay, q=q, ab=ab, rank=rank, reroute=reroute)
    res = {k: np.array(v) for k, v in out.items()}
    if detail is not None: res['detail'] = detail
    return res

# ---- the test used on the real Cambodia data (mirrors relfloor_countries.t_khm_profile) ----
# aggregate windows: 2000 in [.12,.23], 2010 in [.33,.50], 2021 in [.50,.62] -> centre +/- half-width
AGG = {2000: (0.175, 0.055), 2010: (0.415, 0.085), 2021: (0.56, 0.06)}
Q_TOL = 0.10          # each quintile, 2014 and 2021: +/- 10 points
STAT_YEARS_AGG = (2000, 2010, 2021)

def summary_vector(r):
    """The 13 numbers an observer would see: aggregate completion in 3 years, and the
    five-quintile profile in 2014 and 2021."""
    v = [r['c'][yi(y)] for y in STAT_YEARS_AGG]
    v += list(r['q'][yi(2014)]) + list(r['q'][yi(2021)])
    return np.array(v)

def tolerances():
    tol = [AGG[y][1] for y in STAT_YEARS_AGG] + [Q_TOL] * 10
    return np.array(tol)

def real_observed_matches(r):
    """Same decision as repo t_khm_profile (applied to a simulate() result)."""
    return rc.t_khm_profile({'c': r['c'], 'q': r['q']})

def early_checkpoints():
    """Early-rejection checks equal to t_khm_profile, applied as soon as each year is simulated."""
    def at(year, lo, hi):
        return lambda o: lo <= o['c'][yi(year)] <= hi
    def q_ok(year):
        return lambda o: bool(np.all(np.abs(np.array(o['q'][yi(year)]) - KHM_Q[year]) <= .10))
    def y2010(o): return .33 <= o['c'][yi(2010)] <= .50
    return {2000: at(2000, .12, .23), 2010: y2010,
            2014: q_ok(2014), 2021: lambda o: (.50 <= o['c'][yi(2021)] <= .62) and q_ok(2021)(o)}
