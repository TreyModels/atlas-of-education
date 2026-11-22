"""masseng v5: the demand engine (PROTOCOL_v5.md).

Same cohort accounting as engine.py (births, deciles, grades, sectors, repetition, cycle changes, UIS age bands),
with a different account of demand and four additions:

  utility of continuing into / within level L, decile d, year y =
      alpha_L (entry intercepts separate)
    + b_h * premium_L(y)                 human-capital value (wage premium of completing L; driver data)
    + b_p * S_L(y-1)                     positional pull: share of 20-29 year-olds holding L's credential (endogenous)
    + b_r * R(y)                         relational floor / credential threshold (driver data)
    + eta * ln(GDPpc_y / GDPpc_1990)     only in rival R0 (the v3-style national-income demand)
    + eta_x * ln(decile income / mean)
    - kappa * exp(-lam * Z_L) * ln(1 + burden_L,s,d(y))
        burden = (c_scale * direct cost + forgone earnings - targeted transfers) / decile income, shares of GDPpc
        Z_L = S_L(y-1) (rivals R1, R3, R4) or R(y) (rival R5)

  additions: (1) household direct spending is an output (shares of family expenditure by decile; household share of
  total education spending given public spending from WDI); (2) secondary completers who do not enter tertiary stay
  eligible to enter later (deferred pool, yearly reconsideration share h_def, until max_defer_age); (3) the transition
  rate into upper secondary is recorded; (4) optional rationing of public upper-secondary places with private
  absorption (vouchers act through the private cost).
"""
from dataclasses import dataclass, field

import numpy as np

from .data import Country, Series, decile_income_multipliers
from .array_admissions import clear_two_sector_array

PUB, PRIV = 0, 1
LEVEL_NAMES = ['primary', 'secondary', 'upper_secondary', 'tertiary']
N_GRADES = 16

DEFAULTS = dict(
    a_prim=5.0, a_sec=4.0, a_sec_entry=1.5, a_ter=6.0, a_ter_entry=0.0,
    b_h=0.0, b_p=0.0, b_r=0.0, eta=0.0, eta_x=0.0,
    kappa=3.0, lam=0.0, c_scale=1.0,
    mu_basic=-2.5, mu_ter=1.0, nu=0.5,
    h_def=0.2, late=0.15, rep_prim=0.04, rep_sec=0.02,
)

SPECS = {
    # name: (fitted demand parameters, Z source for lam or None, use eta)
    'R0': dict(fit=['eta'], z=None),
    'R1': dict(fit=['b_h', 'b_p', 'b_r', 'lam'], z='S'),
    'R2': dict(fit=['b_h'], z=None),
    'R3': dict(fit=['b_h', 'b_p', 'b_r'], z=None),
    'R4': dict(fit=['b_h', 'b_r', 'lam'], z='S'),
    'R5': dict(fit=['b_h', 'b_p', 'b_r', 'lam'], z='R'),
}
BASE_FIT = ['a_prim', 'a_sec', 'a_sec_entry', 'a_ter', 'a_ter_entry', 'eta_x', 'kappa', 'c_scale',
            'mu_basic', 'mu_ter', 'nu']


@dataclass
class Result:
    years: np.ndarray
    ind: dict
    extra: dict = field(default_factory=dict)


def _sig(x):
    return 1.0 / (1.0 + np.exp(-x))


class Model5:
    def __init__(self, country: Country, params=None, spec='R1', switches=None, annual_market=False):
        self.c = country
        self.cfg = country.config
        self.v5 = self.cfg.get('v5', {})
        self.spec = spec
        self.annual_market = bool(annual_market)
        self.p = dict(DEFAULTS)
        if params:
            self.p.update({k: v for k, v in params.items() if k in DEFAULTS})
        allowed = set(SPECS[spec]['fit'])
        for k in ('b_h', 'b_p', 'b_r', 'lam', 'eta'):
            if k not in allowed:
                self.p[k] = 0.0
        self.zsrc = SPECS[spec]['z']
        self.sw = dict(policies=True, deferred=True)
        if switches:
            self.sw.update(switches)
        yrs = self.v5.get('years', self.cfg['years'])
        self.y0, self.y1 = yrs['simulate_from'], yrs['simulate_to']
        st = self.cfg['structure']
        self.max_age = st['max_age']
        self.shs_from = st.get('upper_secondary_from', 10 ** 6)
        L = st.get('lower_secondary_grades', 4)
        self.n_lower = L
        self.level_of_grade = np.array([0] * 6 + [1] * L + [2] * (6 - L) + [3] * 4)
        self.first_grade = {0: 0, 1: 6, 2: 6 + L, 3: 12}
        self.last_lower = 5 + L
        self.late_max_age = st.get('late_entry_max_age', 8)
        self.late_hazard = st.get('late_entry_hazard', 0.0)
        self.catch_up = self.cfg.get('catch_up_entry')
        self.max_defer_age = self.v5.get('max_defer_age', 25)
        gate = self.cfg.get('tertiary_entry_exam')
        self.exam = None
        if gate:
            pts = sorted((int(k), v) for k, v in gate['pass_rate'].items() if not k.startswith('_'))
            self.exam = dict(pts=pts, default=gate.get('default_before_data', pts[0][1]))
        self._prepare()

    def set_params(self, params):
        """Reuse the prepared exogenous paths with new behavioural parameters (fast refits)."""
        self.p = dict(DEFAULTS)
        self.p.update({k: v for k, v in params.items() if k in DEFAULTS})
        allowed = set(SPECS[self.spec]['fit'])
        for k in ('b_h', 'b_p', 'b_r', 'lam', 'eta'):
            if k not in allowed:
                self.p[k] = 0.0
        return self

    # ------------------------------------------------------------------ exogenous paths
    def _driver(self, name, default=0.0):
        d = getattr(self.c, 'drivers', {}) or {}
        s = d.get(name)
        if s is None:
            return np.full(len(self.years), default)
        return np.array([s(y) for y in self.years])

    def _prepare(self):
        c, cfg, v5 = self.c, self.cfg, self.v5
        Y = np.arange(self.y0, self.y1 + 1)
        self.years = Y
        self.gdp = np.array([c.gdppc(y) for y in Y])
        self.gdp_ref = c.gdppc(1990)
        gdef = cfg.get('demography', {}).get('gini_default', 0.42)
        self.mult = np.array([decile_income_multipliers((c.gini(y) / 100) if c.gini else gdef) for y in Y])
        self.lnmult = np.log(self.mult)
        self.lngdp = np.log(self.gdp / self.gdp_ref)
        # drivers (shares in 0-1 for formal/occupation; premia in log points)
        dm = v5.get('driver_map', {})
        self.prem = np.zeros((len(Y), 4))
        self.prem[:, 1] = self.prem[:, 2] = self._driver(dm.get('premium_secondary', 'premium_secondary'))
        self.prem[:, 3] = self._driver(dm.get('premium_tertiary', 'premium_tertiary'))
        r = self._driver(dm.get('relational', 'formal_share'))
        self.R = r / 100.0 if np.nanmax(r) > 1.5 else r
        # costs: direct (relative schedule, scaled by c_scale) and forgone earnings, shares of GDPpc
        dc = v5['direct_costs_share_of_gdppc']
        fe = v5['forgone_earnings_share_of_gdppc']
        direct = np.zeros((len(Y), 4, 2))
        forgone = np.zeros((len(Y), 4))
        for li, name in enumerate(LEVEL_NAMES):
            direct[:, li, PUB] = dc[name]['public']
            direct[:, li, PRIV] = dc[name]['private']
            forgone[:, li] = fe[name]
        if self.sw['policies']:
            for ev in v5.get('policy_events', cfg.get('policy_events', [])):
                li = LEVEL_NAMES.index(ev['level'])
                si = PUB if ev['sector'] == 'public' else PRIV
                direct[Y >= ev['year'], li, si] += ev['direct_cost_change'] if 'direct_cost_change' in ev else ev['cost_change']
        self.direct = np.maximum(direct, 0.002)
        self.forgone = forgone
        self.transfer = np.zeros((len(Y), 10, 4))
        if self.sw['policies']:
            for tr in cfg.get('transfers', []):
                ramp = np.clip((Y - tr['year'] + 1) / max(tr.get('ramp_years', 1), 1), 0, 1)
                for li in tr['levels']:
                    for d in tr['deciles']:
                        self.transfer[:, d, LEVEL_NAMES.index(li)] += tr['value'] * ramp
        self.s6 = np.array([np.interp(y, *zip(*sorted((int(k), v) for k, v in cfg['entry_age']['share_at_6'].items()
                                                         if not k.startswith('_')))) for y in Y])
        self.b_lo = self.y0 - self.max_age - 2
        self.b_hi = self.y1
        self.cohort = np.array([c.survivors(b) for b in range(self.b_lo, self.b_hi + 1)])
        prm_age, sec_dur, prm_dur = c.wdi('SE.PRM.AGES'), c.wdi('SE.SEC.DURS'), c.wdi('SE.PRM.DURS')
        self.band = {}
        for y in Y:
            a0 = int(round(prm_age(y))) if prm_age else 6
            pd = int(round(prm_dur(y))) if prm_dur else 6
            sd = int(round(sec_dur(y))) if sec_dur else 6
            self.band[y] = dict(primary=(a0, a0 + pd), secondary=(a0 + pd, a0 + pd + sd),
                                tertiary=(a0 + pd + sd, a0 + pd + sd + 5))
        # public education spending, % GDP (for the household share of total spending)
        xs = c.wdi('SE.XPD.TOTL.GD.ZS')
        self.pub_xpd = np.array([xs(y) for y in Y]) / 100.0 if xs else np.full(len(Y), np.nan)
        self.cons_share = v5.get('household_consumption_share_of_gdp', 0.72)
        upc = v5.get('upper_secondary_public_capacity')     # share of upper-secondary entrants with a public seat
        self.us_cap = None if upc is None else np.array([np.interp(y, *zip(*sorted((int(k), v) for k, v in upc.items()
                                                                                    if not k.startswith('_')))) for y in Y])

    def _annual_seats(self, y, li):
        """Declared new-entrant places in persons, never inferred from enrolled stocks."""
        cfg = self.v5.get('annual_capacity', {}).get(LEVEL_NAMES[li], {})
        seats = []
        for sector in ('public', 'private'):
            value = cfg.get(sector, 0.0)
            if isinstance(value, dict):
                points = sorted((int(k), float(v)) for k, v in value.items() if not k.startswith('_'))
                value = np.interp(y, [p[0] for p in points], [p[1] for p in points]) if points else 0.0
            seats.append(float(value))
        return np.array(seats)

    # ------------------------------------------------------------------ behaviour
    def _base(self, yi, li, S):
        p = self.p
        return (p['b_h'] * self.prem[yi, li] + p['b_p'] * S[li] + p['b_r'] * self.R[yi]
                + p['eta'] * self.lngdp[yi] + p['eta_x'] * self.lnmult[yi])          # decile vector

    def _v(self, yi, li, S):
        p = self.p
        z = S[li] if self.zsrc == 'S' else (self.R[yi] if self.zsrc == 'R' else 0.0)
        k = p['kappa'] * np.exp(-p['lam'] * z)
        cost = p['c_scale'] * self.direct[yi, li, :][None, :] + self.forgone[yi, li]
        burden = (cost - self.transfer[yi, :, li][:, None]).clip(0.0) / self.mult[yi][:, None]
        v = -k * np.log1p(burden)
        mu = p['mu_ter'] if li == 3 else p['mu_basic']
        v[:, PRIV] += mu + p['nu'] * (self.lngdp[yi] + self.lnmult[yi])
        return v

    def _pass_rate(self, y):
        pts = self.exam['pts']
        if y < pts[0][0]:
            return self.exam['default'] / 100.0
        return float(np.interp(y, [q[0] for q in pts], [q[1] for q in pts])) / 100.0

    def _entry_prob(self, yi, li, base, V, S, latent=False):
        """Actual-cost demand, or demand at the lower of zero and subsidised cost."""
        if not latent:
            return _sig(base + np.logaddexp(V[li][:, PUB], V[li][:, PRIV]))
        p = self.p
        z = S[li] if self.zsrc == 'S' else (self.R[yi] if self.zsrc == 'R' else 0.0)
        k = p['kappa'] * np.exp(-p['lam'] * z)
        free_burden = np.maximum(self.forgone[yi, li] / self.mult[yi], 0.0)
        free = np.repeat((-k * np.log1p(free_burden))[:, None], 2, axis=1)
        free[:, PRIV] += (p['mu_ter'] if li == 3 else p['mu_basic']) + p['nu'] * (self.lngdp[yi] + self.lnmult[yi])
        best = np.maximum(V[li], free)
        return _sig(base + np.logaddexp(best[:, PUB], best[:, PRIV]))

    def _record_market(self, mk, li, qualified, pe, pe_latent, admitted=None, unmet=None, seats=None, realized=None):
        """All panels are persons by decile; Q >= L >= E >= R within floating precision."""
        q = (qualified * self.cohort[:, None]).sum(axis=0)
        e = q * pe
        mk['Q'][li] += q
        mk['L'][li] += q * pe_latent
        mk['E'][li] += e
        if admitted is None:
            mk['R'][li] += (realized * self.cohort[:, None]).sum(axis=0) if realized is not None else e
        else:
            mk['R'][li] += admitted.sum(axis=(0, 2))
            mk['unmet_effective'][li] += unmet.sum(axis=0)
            mk['capacity'][li, :, PUB] += seats[PUB] / 10.0
            mk['capacity'][li, :, PRIV] += seats[PRIV] / 10.0
            mk['admitted_by_sector'][li, :, PUB] += admitted[:, :, PUB].sum(axis=0)
            mk['admitted_by_sector'][li, :, PRIV] += admitted[:, :, PRIV].sum(axis=0)

    # ------------------------------------------------------------------ simulation
    def run(self, record_deciles=False):
        p = self.p
        nb = self.b_hi - self.b_lo + 1
        E = np.zeros((nb, 10, N_GRADES, 2))
        comp = np.zeros((nb, 10, 4))          # ever completed level (credential held): prim, (unused), secondary, tertiary
        pool = np.zeros((nb, 10))             # secondary completers not (yet) in tertiary
        grads = np.zeros((nb, 10, 4))
        drops = np.zeros((nb, 10))
        aged = np.zeros((nb, 10))
        entered = np.zeros((nb, 10))
        notyet = np.full((nb, 10), 0.1)
        Y = self.years
        bidx = np.arange(self.b_lo, self.b_hi + 1)
        rep = np.array([p['rep_prim'], p['rep_sec'], p['rep_sec'], 0.0])
        rc = self.cfg.get('repetition', {})
        rep[0] = rc.get('primary', rep[0]); rep[1] = rep[2] = rc.get('secondary', rep[1])
        a_w = np.array([p['a_prim'], p['a_sec'], p['a_sec'], p['a_ter']])
        a_e = np.array([p['a_prim'], p['a_sec_entry'], p['a_sec_entry'], p['a_ter_entry']])
        names = ['ger_primary', 'ner_primary', 'ger_secondary', 'ner_secondary', 'ger_tertiary', 'priv_primary',
                 'priv_secondary', 'priv_lower_secondary', 'priv_upper_secondary', 'priv_tertiary', 'enrol_primary',
                 'enrol_secondary', 'enrol_tertiary', 'S_primary', 'S_secondary', 'S_tertiary', 'trans_lsec_usec',
                 'ter_entrants_deferred_share', 'edu_share_hh', 'edu_share_bottom30', 'edu_share_top70',
                 'edu_share_d1', 'edu_share_d10', 'hh_share_total_spending', 'gradlr_primary', 'gradlr_secondary',
                 'gradlr_tertiary', 'pool_share_20_24']
        out = {k: np.full(len(Y), np.nan) for k in names}
        market_names = ('Q', 'L', 'E', 'R', 'unmet_effective')
        markets = {k: np.zeros((len(Y), 4, 10)) for k in market_names}
        markets['capacity'] = np.zeros((len(Y), 4, 10, 2))
        markets['admitted_by_sector'] = np.zeros_like(markets['capacity'])
        dec_part = {}
        S = np.zeros(4)
        for yi, y in enumerate(Y):
            age = y - 1 - bidx
            alive = (age >= 5) & (age <= self.max_age)
            # positional pull from LAST year's stock: share of 20-29 year-olds holding each credential
            band = (age >= 20) & (age <= 29)
            w = self.cohort[band]
            if w.sum() > 0:
                for li in (0, 2, 3):
                    S[li] = float((comp[band, :, li].sum(axis=1) * w).sum() / w.sum())
                S[1] = S[2]                                  # lower-secondary decisions face the secondary credential
            base = [self._base(yi, li, S) for li in range(4)]
            V = [self._v(yi, li, S) for li in range(4)]
            IV = [np.logaddexp(v[:, 0], v[:, 1]) for v in V]
            sp = [np.exp(v[:, 1] - iv) for v, iv in zip(V, IV)]
            mk = {k: np.zeros_like(v[0]) for k, v in markets.items()}
            newE = np.zeros_like(E)
            t1 = np.zeros((nb, 10))
            trans_num = trans_den = 0.0
            for g in range(N_GRADES):
                mass = E[:, :, g, :]
                if not mass.any():
                    continue
                li = self.level_of_grade[g]
                stay = mass * rep[li]
                passed = mass - stay
                pc = _sig(a_w[li] + base[li][:, None] + V[li])
                newE[:, :, g, :] += stay * pc[None]
                drops += (stay * (1 - pc[None])).sum(axis=2)
                if g in (5, self.last_lower, 11, 15):
                    tot = passed.sum(axis=2)
                    if g == 5:
                        comp[:, :, 0] += tot
                        nxt = 1
                    elif g == self.last_lower:
                        if y >= self.shs_from:
                            nxt = 2
                        else:
                            comp[:, :, 2] += tot             # final secondary credential (pre-reform cycle)
                            nxt = 3
                    elif g == 11:
                        comp[:, :, 2] += tot
                        nxt = 3
                    else:
                        comp[:, :, 3] += tot
                        grads[:, :, 3] += tot
                        continue
                    if nxt == 3:
                        t1 += tot
                        continue
                    ng = self.first_grade[nxt]
                    pe = _sig(a_e[nxt] + base[nxt] + IV[nxt])
                    pe_latent = self._entry_prob(yi, nxt, a_e[nxt] + base[nxt], V, S, latent=True)
                    if self.annual_market:
                        seats = self._annual_seats(y, nxt)
                        demand = tot[:, :, None] * (pe[:, None] * np.stack([1 - sp[nxt], sp[nxt]], axis=1))[None]
                        demand *= self.cohort[:, None, None]
                        admitted, unmet = clear_two_sector_array(demand, seats)
                        sector_cont = admitted / self.cohort[:, None, None]
                        newE[:, :, ng, :] += sector_cont
                        cont = sector_cont.sum(axis=2)
                        self._record_market(mk, nxt, tot, pe, pe_latent, admitted, unmet, seats)
                    elif nxt == 2 and self.us_cap is not None:
                        # Legacy share rule, preserved byte-for-byte in behaviour when annual markets are off.
                        pe_priv = _sig(a_e[2] + base[2] + V[2][:, PRIV])
                        f = self.us_cap[yi]
                        cont_pub = tot * (f * pe * (1 - sp[2]))[None]
                        cont_priv = tot * (f * pe * sp[2] + (1 - f) * pe_priv)[None]
                        newE[:, :, ng, PUB] += cont_pub
                        newE[:, :, ng, PRIV] += cont_priv
                        cont = cont_pub + cont_priv
                        self._record_market(mk, nxt, tot, pe, pe_latent, realized=cont)
                    else:
                        cont = tot * pe[None]
                        newE[:, :, ng, PUB] += cont * (1 - sp[nxt])[None]
                        newE[:, :, ng, PRIV] += cont * sp[nxt][None]
                        self._record_market(mk, nxt, tot, pe, pe_latent)
                    if nxt == 2:
                        trans_num += (cont.sum(axis=1) * self.cohort).sum()
                        trans_den += (tot.sum(axis=1) * self.cohort).sum()
                    grads[:, :, self.level_of_grade[g]] += tot - cont
                else:
                    newE[:, :, g + 1, :] += passed * pc[None]
                    drops += (passed * (1 - pc[None])).sum(axis=2)
            out['trans_lsec_usec'][yi] = trans_num / trans_den if trans_den > 0 else np.nan
            # exam gate
            if t1.any() and self.exam is not None:
                pr = self._pass_rate(y)
                grads[:, :, 2] += t1 * (1 - pr)
                t1 = t1 * pr
            # New completers and deferred candidates form one unique-mass admissions market.
            pe3 = _sig(a_e[3] + base[3] + IV[3])
            pe3_latent = self._entry_prob(yi, 3, a_e[3] + base[3], V, S, latent=True)
            eligible = (age <= self.max_defer_age)[:, None]
            considered_def = pool * p['h_def'] * eligible if self.sw['deferred'] else np.zeros_like(pool)
            if self.annual_market:
                qualified = t1 + considered_def
                prefs = pe3[:, None] * np.stack([1 - sp[3], sp[3]], axis=1)
                demand_new = t1[:, :, None] * prefs[None] * self.cohort[:, None, None]
                demand_def = considered_def[:, :, None] * prefs[None] * self.cohort[:, None, None]
                seats = self._annual_seats(y, 3)
                admitted, unmet = clear_two_sector_array(demand_new + demand_def, seats)
                # Ration each source in the same proportion; deferred candidates never enter twice.
                source_total = demand_new + demand_def
                ratio = np.divide(demand_new, source_total, out=np.zeros_like(demand_new), where=source_total > 0)
                admitted_new = admitted * ratio
                ent_new = admitted_new.sum(axis=2) / self.cohort[:, None]
                ent_def = (admitted - admitted_new).sum(axis=2) / self.cohort[:, None]
                ent = ent_new + ent_def
                newE[:, :, 12, :] += admitted / self.cohort[:, None, None]
                pool = pool - considered_def + (t1 - ent_new)
                self._record_market(mk, 3, qualified, pe3, pe3_latent, admitted, unmet, seats)
            else:
                ent_new = t1 * pe3[None]
                ent_def = considered_def * pe3[None]
                pool = pool - ent_def + (t1 - ent_new)
                ent = ent_new + ent_def
                newE[:, :, 12, PUB] += ent * (1 - sp[3])[None]
                newE[:, :, 12, PRIV] += ent * sp[3][None]
                self._record_market(mk, 3, t1 + considered_def, pe3, pe3_latent, realized=ent)
            tot_ent = (ent.sum(axis=1) * self.cohort).sum()
            out['ter_entrants_deferred_share'][yi] = (ent_def.sum(axis=1) * self.cohort).sum() / tot_ent if tot_ent > 0 else np.nan
            # those leaving the deferral window stop being eligible (counted as secondary completers who left)
            expire = pool * (~eligible) if self.sw['deferred'] else pool
            grads[:, :, 2] += expire
            pool = pool - expire
            # entrants to Grade 1
            s6n, s61, s62 = self.s6[yi], self.s6[max(yi - 1, 0)], self.s6[max(yi - 2, 0)]
            lam_l = p['late']
            share_at = {6: s6n * (1 - lam_l), 7: (1 - s61) * (1 - lam_l) + s61 * lam_l, 8: (1 - s62) * lam_l}
            pe0 = _sig(a_e[0] + base[0] + IV[0])
            pe0_latent = self._entry_prob(yi, 0, a_e[0] + base[0], V, S, latent=True)
            primary_demand = np.zeros((nb, 10, 2))
            primary_qualified = np.zeros((nb, 10))
            primary_realized = np.zeros((nb, 10))
            for a, sh in share_at.items():
                m = age == a
                if m.any():
                    q = np.zeros((nb, 10)); q[m] = 0.1 * sh
                    primary_qualified += q
                    primary_demand[m] = q[m, :, None] * (pe0[:, None] * np.stack([1 - sp[0], sp[0]], axis=1))[None]
                    if not self.annual_market:
                        e = q[m] * pe0[None]
                        primary_realized[m] += e
                        entered[m] += e; notyet[m] -= e
                        newE[m, :, 0, PUB] += e * (1 - sp[0])[None]
                        newE[m, :, 0, PRIV] += e * sp[0][None]
            hz = np.zeros(nb)
            if self.late_hazard > 0:
                hz[(age >= 9) & (age <= self.late_max_age)] = self.late_hazard
            if self.catch_up and self.catch_up['years'][0] <= y <= self.catch_up['years'][1]:
                mm = (age >= 7) & (age <= self.catch_up['max_age'])
                hz[mm] = np.maximum(hz[mm], self.catch_up['rate'])
            if hz.any():
                q = notyet * hz[:, None]
                primary_qualified += q
                primary_demand += q[:, :, None] * (pe0[:, None] * np.stack([1 - sp[0], sp[0]], axis=1))[None]
                if not self.annual_market:
                    e = q * pe0[None]
                    primary_realized += e
                    entered += e; notyet -= e
                    newE[:, :, 0, PUB] += e * (1 - sp[0])[None]
                    newE[:, :, 0, PRIV] += e * sp[0][None]
            if self.annual_market:
                seats = self._annual_seats(y, 0)
                demand = primary_demand * self.cohort[:, None, None]
                admitted, unmet = clear_two_sector_array(demand, seats)
                sector_ent = admitted / self.cohort[:, None, None]
                ent = sector_ent.sum(axis=2)
                entered += ent; notyet -= ent
                newE[:, :, 0, :] += sector_ent
                self._record_market(mk, 0, primary_qualified, pe0, pe0_latent, admitted, unmet, seats)
            else:
                self._record_market(mk, 0, primary_qualified, pe0, pe0_latent, realized=primary_realized)
            aged[~alive] += newE[~alive].sum(axis=(2, 3))
            grads[~alive, :, 2] += pool[~alive]
            pool[~alive] = 0.0
            newE[~alive] = 0.0
            E = newE
            self._record(out, yi, y, E, age, S, pool, record_deciles, dec_part)
            for key in markets:
                markets[key][yi] = mk[key]
        return Result(Y, out, dict(deciles=dec_part, grads=grads, drops=drops, aged=aged, entered=entered,
                                   final_enrolled=E.sum(axis=(2, 3)), final_pool=pool, params=dict(self.p),
                                   spec=self.spec, markets=markets))

    # ------------------------------------------------------------------ indicators
    def _pop_at_age(self, y, a):
        b = y - 1 - a
        return self.cohort[b - self.b_lo] if self.b_lo <= b <= self.b_hi else 0.0

    def _band_pop(self, y, lo, hi):
        return sum(self._pop_at_age(y, a) for a in range(lo, hi))

    def _record(self, out, yi, y, E, age, S, pool, record_deciles, dec_part):
        persons = E * self.cohort[:, None, None, None]
        bands = self.band[y]
        sl = dict(primary=slice(0, 6), secondary=slice(6, 12), tertiary=slice(12, 16))
        for lev, s in sl.items():
            lo, hi = bands[lev]
            pop = self._band_pop(y, lo, hi)
            enr = persons[:, :, s, :].sum()
            out[f'ger_{lev}'][yi] = 100 * enr / pop if pop > 0 else np.nan
            out[f'enrol_{lev}'][yi] = enr
            if lev != 'tertiary':
                on = (age >= lo) & (age < hi)
                out[f'ner_{lev}'][yi] = 100 * persons[on][:, :, s, :].sum() / pop if pop > 0 else np.nan
            out[f'priv_{lev}'][yi] = 100 * persons[:, :, s, PRIV].sum() / enr if enr > 0 else np.nan
            pop_d = pop / 10
            if pop_d > 0:
                byd = persons[:, :, s, :].sum(axis=(0, 2, 3)) / pop_d
                out[f'gradlr_{lev}'][yi] = 10 * np.log(max(byd[9], 1e-12) / max(byd[0], 1e-12))
                if record_deciles:
                    dec_part.setdefault(int(y), {})[lev] = (100 * byd).tolist()
        for name, s in (('lower_secondary', slice(6, 6 + self.n_lower)), ('upper_secondary', slice(6 + self.n_lower, 12))):
            enr = persons[:, :, s, :].sum()
            out[f'priv_{name}'][yi] = 100 * persons[:, :, s, PRIV].sum() / enr if enr > 0 else np.nan
        out['S_primary'][yi], out['S_secondary'][yi], out['S_tertiary'][yi] = S[0], S[2], S[3]
        a20 = (age >= 20) & (age <= 24)
        w = self.cohort[a20]
        out['pool_share_20_24'][yi] = float((pool[a20].sum(axis=1) * w).sum() / w.sum()) if w.sum() > 0 else np.nan
        # household direct spending (share of GDPpc units) by decile
        cdir = self.p['c_scale'] * self.direct[yi]                                  # level x sector
        lvl = self.level_of_grade
        spend_d = np.zeros(10)
        for g in range(N_GRADES):
            spend_d += (persons[:, :, g, :] * cdir[lvl[g]][None, None, :]).sum(axis=(0, 2))
        total_pop = self.c.pop(y)
        cons_d = self.cons_share * self.mult[yi] * total_pop / 10.0                 # GDPpc units per decile
        out['edu_share_hh'][yi] = 100 * spend_d.sum() / cons_d.sum()
        out['edu_share_bottom30'][yi] = 100 * spend_d[:3].sum() / cons_d[:3].sum()
        out['edu_share_top70'][yi] = 100 * spend_d[3:].sum() / cons_d[3:].sum()
        out['edu_share_d1'][yi] = 100 * spend_d[0] / cons_d[0]
        out['edu_share_d10'][yi] = 100 * spend_d[9] / cons_d[9]
        hh_gdp = spend_d.sum() / total_pop                                          # share of GDP
        pub = self.pub_xpd[yi]
        out['hh_share_total_spending'][yi] = 100 * hh_gdp / (hh_gdp + pub) if pub == pub else np.nan
