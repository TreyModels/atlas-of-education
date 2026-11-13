"""Shadow education: a market with three motives and two suppliers.

Motives (Dang & Rogers 2008; Bray 1999, 2009):
  buy-back   restore lessons the own teacher withheld (Biswal 1999; Jayachandran 2014) - only the own teacher fully can
  gate prep  raise the chance of passing the next gate x what passing is worth (Kim & Lee 2010; Dang 2007), priced
             through the core's marginal value of learning, so it rises with exam stakes and labour-market scarcity
  remedial   help a home cannot give (parental education), independent of exams
Suppliers: the pupil's own teacher (fixed price, available unless banned and enforced) and firms (upward-sloping
short-run supply, flat long-run supply through entry; bans cut availability and push prices up).
"""
import numpy as np
from ..core import Module


class TutoringMarket(Module):
    name = 'tutoring'
    defaults = dict(
        tut_effect=0.35, tut_effect_own=0.25,       # grade-equivalents of learning per year of tutoring
        p_own=0.04, p_firm=0.06,                    # own-teacher price; firms' long-run price (wage units per year)
        firm_elast=1.0, firm_entry=0.3,
        own_ban=0.0, firm_ban=0.0,                  # enforcement share of a ban on own-pupil / commercial tutoring
        rural_firm_access=0.4, buyback_firm=0.3, r0=0.0, tut_taste=0.03,
    )

    def setup(self, E):
        E.tut_sell = 1.0 - E.p['own_ban']           # read by PublicSchools: withholding only pays if it can be sold
        self.K = 0.0; self.D = 0.0

    def firm_price(self, E):
        p = E.p
        base = p['p_firm'] * (1 + p['firm_ban'])     # a ban pushes surviving supply underground and dearer
        if self.K <= 0:
            return base * 1.5
        return base * max(1.0, self.D / self.K) ** (1 / p['firm_elast'])

    def extras(self, E, t):
        p, k, r, y = E.p, E.kids, E.rng, E.yr
        att = k['att']
        idx = np.flatnonzero(att)
        n = len(att)
        choice = np.zeros(n, int)          # 0 none, 1 own teacher, 2 firm
        pf = self.firm_price(E)
        if len(idx):
            mvl = E.mvl_all(t)[idx]
            h = y['withheld'][idx]; q = y['quality'][idx]
            rem = p['r0'] * (1 - k['home'][idx])
            yy = np.maximum(k['y'][idx], 0.05)
            u_own = mvl * (p['tut_effect_own'] + h * q) + rem * p['tut_effect_own'] - p['p_own'] / yy
            u_firm = mvl * (p['tut_effect'] + p['buyback_firm'] * h * q) + rem * p['tut_effect'] - pf / yy
            own_ok = (k['sector'][idx] == 0) & (k['g'][idx] < 12) & (r.random(len(idx)) >= p['own_ban'])
            firm_ok = (r.random(len(idx)) < (1 - p['firm_ban']) * np.where(k['urban'][idx], 1.0, p['rural_firm_access']))
            cash = E._cash[idx]
            u_own = np.where(own_ok & (cash >= p['p_own']), u_own + p['tut_taste'] * r.standard_normal(len(idx)), -np.inf)
            u_firm = np.where(firm_ok & (cash >= pf), u_firm + p['tut_taste'] * r.standard_normal(len(idx)), -np.inf)
            U = np.stack([np.zeros(len(idx)), u_own, u_firm], 1)
            ch = U.argmax(1)
            choice[idx] = ch
        # firm capacity rations demand (highest income first), then entry moves capacity toward demand
        dem = np.flatnonzero(choice == 2)
        self.D = len(dem)
        if self.K <= 0:
            choice[dem] = 0
        elif len(dem) > self.K:
            drop = dem[np.argsort(k['y'][dem])][:len(dem) - int(self.K)]
            choice[drop] = 0
        self.K = max(0.0, self.K + p['firm_entry'] * (self.D - self.K) + (min(self.D, 0.01 * p['N']) if self.K < 1 else 0))
        own, firm = choice == 1, choice == 2
        y['tut_gain'] += np.where(own, p['tut_effect_own'], 0.0) + np.where(firm, p['tut_effect'], 0.0)
        y['buyback'] |= own
        y['withheld'] = np.where(firm, y['withheld'] * (1 - p['buyback_firm']), y['withheld'])
        y['extra_spend'] += np.where(own, p['p_own'], 0.0) + np.where(firm, pf, 0.0)
        y['tut_kind'] = choice
        g = k['g']                                   # grade being studied this year = g (before increment) + 1
        G = E.ends[-1]
        by_grade = [float(((choice > 0) & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        own_g = [float((own & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        firm_g = [float((firm & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        by_q = [float(((choice > 0) & att & (k['q'] == j)).sum() / max((att & (k['q'] == j)).sum(), 1)) for j in range(5)]
        E.note(tut_rate=float((choice > 0)[att].mean()) if att.any() else 0.0, tut_by_grade=by_grade,
               tut_own_by_grade=own_g, tut_firm_by_grade=firm_g, tut_by_q=by_q, firm_price=pf,
               tut_spend=float(y['extra_spend'][att].sum()),
               firm_rev=float(pf * (firm & att).sum()),          # commercial tutoring revenue: pays tutors (labour module)
               own_share=float(own.sum() / max((choice > 0).sum(), 1)))

    def summary(self, E):
        R, m = E.R, E.p['measure_from']
        A = lambda key: np.mean(np.array(R[key][m:], float), 0)
        return dict(tut_rate=float(A('tut_rate')), tut_by_grade=list(A('tut_by_grade')),
                    tut_own_by_grade=list(A('tut_own_by_grade')), tut_firm_by_grade=list(A('tut_firm_by_grade')),
                    tut_by_q=list(A('tut_by_q')), firm_price=float(A('firm_price')), own_share=float(A('own_share')))
