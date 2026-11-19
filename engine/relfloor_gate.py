"""Credential floor with an explicit eligibility gate (M_GATE): an institutional version of the relational term.

Why this exists
  In relfloor_countries.sim the relational value of a credential is an additive constant b_rel. Nothing in the model
  says who sets eligibility, which jobs enforce it, or who gets access to those jobs. A constant benefit is
  observationally close to a taste for schooling or to an unmodelled return, which is part of why the HC / POS / REL
  structures cannot be told apart on wealth profiles (external review, 16 Nov 2026).

  M_GATE makes the relational channel institutional and observable:
    * a share G_t of desirable jobs screens on the credential (an employer rule, Collins 1979; Bills 2003). G_t is an
      observable in principle: the share of wage jobs that require the certificate (labour-force or employer surveys);
    * the credential is necessary, not sufficient. Access to a screened job also needs connections, which rise with
      household income (a = logistic in log income around y_net). Credential-gated access through networks is the
      sense of "relational" in the comparative literature (Collins 1979; Di Stasio, Bol & van de Werfhorst 2016);
    * the household values completion by b_gate x G_t x access(y), so the relational value moves with an observable
      institutional quantity and has a wealth gradient of its own.

  Under M_GATE a change in G_t (an employer or state rule that extends the requirement) shifts completion; under
  HC, POS and REL it does not. A premium change moves HC most. These are the comparisons a recovery study can test.

Docking
  With b_gate = 0, sim_gate reproduces relfloor_countries.sim draw for draw (same RNG call order; the gate adds no
  random draws). research/tests/test_rigor.py checks this to machine precision.

All gate parameters are ASSUMED (uniform judgement ranges); none is measured. Units follow relfloor.py.
"""
import numpy as np

import relfloor_countries as RC
from relfloor import HZ

YEARS = RC.YEARS
yi = RC.yi
STRUCTS = ('M_HC', 'M_POS', 'M_REL', 'M_GATE')

GATE_PRIORS = {
    'b_gate': (0.0, 0.8),     # value of a screened job relative to the non-graduate wage (same scale as b_rel)
    'G0': (0.05, 0.30),       # share of desirable jobs screening on the credential in 1998 (assumed)
    'dG': (0.0, 0.40),        # rise in that share by 2020 (assumed linear 1998-2020, flat after)
    'net_shift': (-0.5, 1.0), # log-income point of 50% network access, relative to mu
    's_net': (0.2, 1.0),      # log-income scale of the access curve
}


def draw(rng, structure, cfg, smooth_liq=True):
    """Same base draw as relfloor_countries.draw (identical RNG order), then gate parameters from a separate stream."""
    base_structure = 'M_REL' if structure in ('M_REL', 'M_GATE') else structure
    th = RC.draw(rng, base_structure, cfg, smooth_liq=smooth_liq)
    g = {k: rng.uniform(*v) for k, v in GATE_PRIORS.items()}
    th.update(g)
    if structure == 'M_GATE':
        th['b_rel'] = 0.0
    else:
        th['b_gate'] = 0.0
    return th


def gate_path(th, scen):
    G = th['G0'] + th['dG'] * np.clip((YEARS - 1998) / 22, 0, 1)
    if scen in ('gate', 'gate_fall'):            # employer/state rule extends the requirement from 2025
        k = YEARS >= 2025
        G = G.copy(); G[k] = np.minimum(1.0, G[k] + 0.20)
    return G


def sim_gate(th, cfg, scen='base', n=2000, seed=0):
    """relfloor_countries.sim plus the gate term. scen: base | fall | gate | gate_fall."""
    rng = np.random.default_rng(seed)
    logy0 = rng.normal(th['mu'], 0.7, n)
    ab = 0.3 * (logy0 - logy0.mean()) / 0.7 + np.sqrt(1 - 0.09) * rng.normal(size=n)
    q = np.searchsorted(np.quantile(logy0, [.2, .4, .6, .8]), logy0)
    pm = RC.prem(th, cfg, 'fall' if scen in ('fall', 'gate_fall') else 'base')
    G = gate_path(th, scen)
    s_prev = 0.3
    c_ = th['direct'] + th['forgo']
    out = {'c': [], 'q': [], 'exit_low': [], 'q3': []}
    b_gate = th.get('b_gate', 0.0)
    for t, yr in enumerate(YEARS):
        y = np.exp(logy0) * (1 + th['g']) ** (yr - 1998)
        R = HZ * (pm[t] * np.exp(th['gamma'] * ab) + th['b_pos'] * s_prev + th['b_rel'])
        if b_gate > 0:
            access = 1 / (1 + np.exp(-(np.log(y) - (th['mu'] + th['net_shift'] + th['g'] * (yr - 1998))) / th['s_net']))
            R = R + HZ * b_gate * G[t] * access
        want = R - cfg['L'] * c_ + rng.logistic(0, th['sig'], n) > 0
        thresh = th['y_sub'] + th['kappa'] * c_
        if th.get('s_liq', 0) > 0:
            pf = th['p_fin'] + (1 - th['p_fin']) / (1 + np.exp(-(np.log(y) - np.log(thresh)) / th['s_liq']))
            fin = rng.random(n) < pf
        else:
            fin = (y >= thresh) | (rng.random(n) < th['p_fin'])
        stay = want & fin
        s_prev = stay.mean()
        ex = ~stay
        out['c'].append(stay.mean())
        out['q'].append([stay[q == i].mean() for i in range(5)])
        out['exit_low'].append((ex & (q <= 1)).sum() / max(ex.sum(), 1))
        out['q3'].append(stay[q >= 2].mean())
    return {k: np.array(v) for k, v in out.items()}


# Summaries a researcher could observe, grouped by study design. Order is fixed; analysis selects columns by name.
SUMMARY_NAMES = (
    ['c_2000', 'c_2010', 'c_2021'] + [f'q2014_{i}' for i in range(1, 6)] + [f'q2021_{i}' for i in range(1, 6)]
    + ['premium_resp_2030', 'premium_resp_gradient_2030', 'gate_resp_2030', 'gate_resp_gradient_2030']
)
DESIGNS = {
    'D0_profiles_now': SUMMARY_NAMES[:13],                                  # data in hand (UIS CR.2 + aggregates)
    'D1_plus_premium_shock': SUMMARY_NAMES[:15],                            # + a quasi-experiment on the premium
    'D2_plus_gate_shock': SUMMARY_NAMES[:13] + SUMMARY_NAMES[15:17],        # + a change in the eligibility rule
    'D3_all': SUMMARY_NAMES,
}
# Observation-error SDs (ASSUMED): survey quintile completion ~2.5 pts; aggregates 2 pts; a good quasi-experimental
# response estimate 2 pts; a wealth-gradient of a response is harder to estimate, 3 pts.
NOISE = dict({n: 0.02 for n in SUMMARY_NAMES[:3]}, **{n: 0.025 for n in SUMMARY_NAMES[3:13]},
             premium_resp_2030=0.02, premium_resp_gradient_2030=0.03, gate_resp_2030=0.02, gate_resp_gradient_2030=0.03)


def summaries(th, cfg, n, seed):
    b = sim_gate(th, cfg, 'base', n, seed)
    f = sim_gate(th, cfg, 'fall', n, seed)
    g = sim_gate(th, cfg, 'gate', n, seed)
    t30 = yi(2030)
    qb, qf, qg = np.array(b['q'][t30]), np.array(f['q'][t30]), np.array(g['q'][t30])
    s = {'c_2000': b['c'][yi(2000)], 'c_2010': b['c'][yi(2010)], 'c_2021': b['c'][yi(2021)]}
    for yr in (2014, 2021):
        for i, v in enumerate(b['q'][yi(yr)], 1):
            s[f'q{yr}_{i}'] = v
    s['premium_resp_2030'] = f['c'][t30] - b['c'][t30]                     # paired, same year
    s['premium_resp_gradient_2030'] = (qf[4] - qb[4]) - (qf[0] - qb[0])     # richest minus poorest response
    s['gate_resp_2030'] = g['c'][t30] - b['c'][t30]
    s['gate_resp_gradient_2030'] = (qg[4] - qb[4]) - (qg[0] - qb[0])
    s = {k: float(v) for k, v in s.items()}
    prof_err = max(abs(s[f'q{yr}_{i}'] - RC.KHM_Q[yr][i - 1]) for yr in (2014, 2021) for i in range(1, 6))
    return s, float(prof_err)
