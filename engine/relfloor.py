"""relfloor: household credential choice with three value components.

Tests H2 of Menefee & Nordtveit, "Massification and Its Mechanisms".
Each household decides whether its child completes the terminal basic credential
(4 secondary years before the 2016 K-12 switch, 6 after).

Value of completing, present value in units of one year's non-graduate adult wage:
  HC   human capital : Hz * prem_rel(t) * exp(gamma * ability)   (ability-dependent)
  POS  positional    : Hz * b_pos * s(t-1)    s = share of previous cohort holding it
  REL  relational    : Hz * b_rel             threshold eligibility, ability-independent
Cost: L(t) * (direct + foregone child earnings), shrinking against growing income.
Liquidity: households with income below y_sub + kappa*annual_cost cannot finance,
except with probability p_fin.
Exit can reroute to a cheaper legible credential (TESDA NC-style), carrying
part of the relational value and part of the HC value.

Structures: M_HC (b_pos=b_rel=0), M_POS (b_rel=0), M_REL (all three).
Units and magnitudes are stylised; the outputs are patterns, not estimates.
"""
import numpy as np

YEARS = np.arange(1998, 2036)
K12_YEAR = 2016

PRIORS = {
    'prem0':  (0.2, 0.9),    # relative HS-completer premium, fraction of non-grad wage
    'gamma':  (0.0, 0.8),    # ability gradient of the HC return
    'b_pos':  (0.0, 0.6),
    'b_rel':  (0.0, 0.8),
    'direct': (0.05, 0.3),   # annual direct cost
    'forgo':  (0.1, 0.5),    # annual foregone child earnings
    'sig':    (0.5, 4.0),    # taste-shock scale (PV units)
    'y_sub':  (0.4, 1.2),    # subsistence income
    'kappa':  (1.0, 4.0),    # liquidity multiple of annual cost
    'p_fin':  (0.0, 0.3),    # chance a constrained household finds the money anyway
    'g':      (0.015, 0.035),# real household income growth per year
    'r_nc':   (0.2, 0.7),    # share of relational value a rerouted credential carries
}
HZ = 12.0   # discounted working-life horizon

def draw(rng, structure):
    th = {k: rng.uniform(*v) for k, v in PRIORS.items()}
    if structure == 'M_HC':
        th['b_pos'] = 0.0; th['b_rel'] = 0.0
    elif structure == 'M_POS':
        th['b_rel'] = 0.0
    return th

def prem_path(th, scenario):
    """Relative premium by year. History to 2024 is 'bumping' (relative premium
    held as absolute graduate wages compress). From 2025:
      'hold'  relative premium unchanged (absolute compression only);
      'fall'  relative premium falls 40% by 2035."""
    p = np.full(len(YEARS), th['prem0'])
    if scenario == 'fall':
        k = YEARS >= 2025
        p[k] = th['prem0'] * (1 - 0.4 * (YEARS[k] - 2024) / 11)
    return p

def simulate(th, scenario='hold', n=4000, seed=0, k12=True):
    rng = np.random.default_rng(seed)
    logy0 = rng.normal(np.log(1.5), 0.7, n)
    ability = 0.3 * (logy0 - logy0.mean()) / 0.7 + np.sqrt(1 - 0.09) * rng.normal(size=n)
    q = np.searchsorted(np.quantile(logy0, [.2, .4, .6, .8]), logy0)  # quintile 0..4
    prem = prem_path(th, scenario)
    s_prev = 0.6
    out = {'complete': [], 'byq': [], 'exit_low_share': [], 'reroute_q3plus': [],
           'exit_q3plus': []}
    for t, yr in enumerate(YEARS):
        y = np.exp(logy0) * (1 + th['g']) ** (yr - 1998)
        L = 6 if (k12 and yr >= K12_YEAR) else 4
        c = th['direct'] + th['forgo']
        R = HZ * (prem[t] * np.exp(th['gamma'] * ability) + th['b_pos'] * s_prev + th['b_rel'])
        eps = rng.logistic(0, th['sig'], n)
        want = R - L * c + eps > 0
        constrained = y < th['y_sub'] + th['kappa'] * c
        finance = ~constrained | (rng.random(n) < th['p_fin'])
        stay = want & finance
        # reroute among exiters: 1 year, half cost, partial values
        R_nc = HZ * (0.3 * prem[t] * np.exp(th['gamma'] * ability) + th['r_nc'] * th['b_rel'])
        can_nc = y >= th['y_sub'] + 0.5 * th['kappa'] * c * 0.5
        reroute = ~stay & can_nc & (R_nc - 0.5 * c + rng.logistic(0, th['sig'], n) > 0)
        s_prev = stay.mean()
        ex = ~stay
        out['complete'].append(stay.mean())
        out['byq'].append([stay[q == i].mean() for i in range(5)])
        out['exit_low_share'].append((ex & (q <= 1)).sum() / max(ex.sum(), 1))
        e3 = ex & (q >= 2)
        out['exit_q3plus'].append(e3.mean())
        out['reroute_q3plus'].append((reroute & e3).sum() / max(e3.sum(), 1))
    return {k: np.array(v) for k, v in out.items()}

def yidx(yr):
    return int(yr - YEARS[0])
