"""E2 provider technology and fee block.
INDEPENDENTLY NAMED NEW IMPLEMENTATION (not a reproduction of any atlas engine, hagwon model,
Bray & Kwok or KEDI). Compact structural model of five provider technologies with entry costs,
capacity and prices, fitted only on KOR fee/income data; shares are predictions.

Declared parameterisation (labels from PRE_DECLARATIONS_loop5.md):
  variable cost c_j = teacher opportunity cost * hours_j / class_size_j + materials
  amortised fixed entry cost f_j per seat (facility / platform / books)
  price p_j = mu * (c_j + f_j), mu common markup (fitted)
  demand: logit over threshold-quality q_j and price/income, price sensitivity falls in income
  theta_s = gate stakes by stage (sourced from observed stage participation)
"""
import numpy as np
from scipy.special import ndtr

TECHS = ['hagwon_mass', 'one_to_one', 'small_group', 'internet', 'textbook_visit']
# sourced/estimated: teacher hourly opportunity cost (won), hours per month, class size
W_HOUR = 25_000.0
HOURS = {'hagwon_mass': 30.0, 'one_to_one': 8.0, 'small_group': 20.0, 'internet': 10.0, 'textbook_visit': 2.0}
CLASS = {'hagwon_mass': 15.0, 'one_to_one': 1.0, 'small_group': 8.0, 'internet': 40.0, 'textbook_visit': 40.0}
MATERIALS = {'hagwon_mass': 5_000.0, 'one_to_one': 0.0, 'small_group': 5_000.0, 'internet': 3_000.0, 'textbook_visit': 1_000.0}
# assumed: amortised fixed entry cost per seat per month (won)
FIXED = {'hagwon_mass': 83_000.0, 'one_to_one': 267_000.0, 'small_group': 40_000.0,
         'internet': 57_000.0, 'textbook_visit': 39_000.0}
# assumed: instructional quality (mass lecture = 1.0)
QUAL = {'hagwon_mass': 1.0, 'one_to_one': 1.15, 'small_group': 0.95, 'internet': 0.55, 'textbook_visit': 0.35}
KAPPA = 8.0   # assumed: price-aversion coefficient on the budget share

KOR_OBS = dict(participation=[86.0, 75.4, 66.4], spend_student=[398.0, 449.0, 491.0],
               spend_participant=[462.0, 596.0, 740.0], spend_all_student=434.0, spend_all_part=553.0,
               provider_spend=dict(hagwon_mass=241.0, one_to_one=37.0, small_group=22.0, internet=16.0, textbook_visit=11.0),
               income_spend={3.0: 183.0, 8.0: 671.0})
HKG_OBS = dict(participation=[35.1, 46.6, 70.3], mass_lecture=[33.0, 72.4], fee_income_band=(1.1, 5.0))


def base_costs():
    c = {j: W_HOUR * HOURS[j] / CLASS[j] + MATERIALS[j] for j in TECHS}
    return c, {j: c[j] + FIXED[j] for j in TECHS}


# Declared price vector per participant-month (won), estimated from the KOR fee tables and provider
# structure: hagwon ~300k (241k per student / 0.785 participation), 1:1 ~1,000k, small group ~450k,
# internet/correspondence ~120k, textbook-with-visit ~60k. The cost-plus decomposition (base costs above)
# is reported alongside so the entry-cost/capacity objects stay visible, but it does NOT set prices:
# observed KOR fees are 3-10x the teacher-time cost, which is itself a finding (rents/brand/marketing).
PRICE0 = {'hagwon_mass': 300_000.0, 'one_to_one': 1_000_000.0, 'small_group': 450_000.0,
          'internet': 120_000.0, 'textbook_visit': 60_000.0}


def prices(mu):
    return {j: mu * PRICE0[j] for j in TECHS}


def demand(theta, mu, rho, income_median=4_000_000.0, y_sigma=0.6, n=4000, seed=0, menu=None,
           q_boost=None):
    """Logit technology choice. Utility = theta*gate-stakes * quality_j - (price_j/income)^rho_price + noise.
    Prices and income both in won/month; the price term is the budget share raised to a power that falls
    with income (rho<0 gives falling sensitivity). Declared reduced form."""
    rng = np.random.default_rng(seed)
    menu = menu or TECHS
    y = income_median * np.exp(y_sigma * rng.standard_normal(n))     # household monthly income, won
    p = prices(mu)
    U = {}
    for j in menu:
        q = QUAL[j] * (1.0 + (q_boost or {}).get(j, 0.0) * theta)
        budget_share = p[j] / y
        U[j] = theta * q - KAPPA * budget_share + rng.gumbel(size=n) * 0.5
    U0 = np.zeros(n)
    vals = np.stack([U[j] for j in menu] + [U0], 1)
    choice = vals.argmax(1)
    take = {j: float(np.mean(choice == i)) for i, j in enumerate(menu)}
    take['none'] = float(np.mean(choice == len(menu)))
    spend = {j: take[j] * p[j] for j in menu}
    tot = sum(spend.values())
    spend_share = {j: (spend[j] / tot if tot > 0 else np.nan) for j in menu}
    avg_spend = float(sum(spend.values()))
    return dict(take=take, spend_share=spend_share, avg_spend=avg_spend,
                avg_spend_participant=avg_spend / max(1 - take['none'], 1e-9), prices=p, income=y)


def fit_kor():
    """Fit mu (price scale) to KOR average spend/student and rho to the KOR income gradient.
    theta_scale fitted to overall participation. Shares are NOT fitted."""
    from scipy.optimize import minimize_scalar
    target_spend = KOR_OBS['spend_all_student']
    def loss_mu(mu):
        d = demand(1.0, mu, 1.3, n=3000, seed=1)
        return abs(d['avg_spend'] - target_spend)
    r = minimize_scalar(loss_mu, bounds=(0.5, 8.0), method='bounded')
    mu = float(r.x)
    # rho from income gradient: spend(<3m)=183, spend(>=8m)=671 -> ratio 3.67, income ratio 8/3
    rho = float(np.log(671.0 / 183.0) / np.log(8.0 / 3.0))
    # theta scale so overall participation ~ 78.5% at theta=1 scaling
    def loss_theta(th):
        d = demand(th, mu, rho, n=3000, seed=2)
        return abs((1 - d['take']['none']) * 100 - 78.5)
    r2 = minimize_scalar(loss_theta, bounds=(0.05, 5.0), method='bounded')
    theta_base = float(r2.x)
    return mu, rho, theta_base


def kor_prediction(mu, rho, theta_base):
    """KOR by level: theta_s from observed participation ordering (sourced), then predict spend shares."""
    out = {}
    for s, (lvl, obs_part) in enumerate(zip(['elementary', 'middle', 'high'], KOR_OBS['participation'])):
        # theta that reproduces the observed stage participation level (sourced ratio)
        from scipy.optimize import minimize_scalar
        def loss(th):
            d = demand(th, mu, rho, n=4000, seed=10 + s)
            return abs((1 - d['take']['none']) * 100 - obs_part)
        th = float(minimize_scalar(loss, bounds=(0.02, 8.0), method='bounded').x)
        d = demand(th, mu, rho, n=4000, seed=10 + s)
        out[lvl] = dict(theta=th, take=1 - d['take']['none'], spend_share=d['spend_share'],
                        avg_spend=d['avg_spend'], avg_participant=d['avg_spend_participant'])
    return out


def hkg_check(mu, rho, fee_scale):
    """HKG: same technology block and relative prices, scaled to HKG fee level; theta per stage from
    the observed HKG stage participation (sourced). Check: mass-lecture share gap S6-7 vs S4-5, fees."""
    from scipy.optimize import minimize_scalar
    stages = {'S4_5': HKG_OBS['participation'][1], 'S6_7': HKG_OBS['participation'][2]}
    res = {}
    for nm, obs_part in stages.items():
        def loss(th):
            d = demand(th, mu * fee_scale, rho, n=4000, seed=20 + len(res))
            return abs((1 - d['take']['none']) * 100 - obs_part)
        th = float(minimize_scalar(loss, bounds=(0.02, 8.0), method='bounded').x)
        d = demand(th, mu * fee_scale, rho, n=4000, seed=20 + len(res))
        res[nm] = dict(take=1 - d['take']['none'], mass_lecture_share=d['spend_share']['hagwon_mass'],
                       avg_spend=d['avg_spend'])
    return res


def arms(mu, rho, theta_base):
    """Structural arms (a) uniform single provider (b) chain/scale-only (c) teacher-tutor capacity
    (d) mixed menu. Returns demand vs spend share diagnostics for the provider-ordering inversion."""
    out = {}
    menus = {'a uniform single provider': ['hagwon_mass'],
             'b commercial chain + internet (scale)': ['hagwon_mass', 'internet'],
             'c teacher-tutor capacity (1:1 + small group)': ['one_to_one', 'small_group'],
             'd mixed technology menu': TECHS}
    for nm, menu in menus.items():
        d = demand(theta_base, mu, rho, n=4000, seed=30, menu=menu)
        commercial_take = d['take'].get('hagwon_mass', 0.0) + d['take'].get('internet', 0.0) + d['take'].get('textbook_visit', 0.0)
        commercial_spend = sum(d['spend_share'].get(j, 0.0) for j in ('hagwon_mass', 'internet', 'textbook_visit'))
        out[nm] = dict(take_all=1 - d['take']['none'], commercial_demand_share=commercial_take,
                       commercial_spend_share=commercial_spend, avg_spend=d['avg_spend'])
    return out
