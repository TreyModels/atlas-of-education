"""The state's budget closes the push-pull loop: formal jobs -> taxes -> teachers -> learning -> credentials -> formal jobs.

FiscalState  education budget = share of tax revenue; revenue = income tax on the formal wage bill + consumption tax on
             all earnings (Besley & Persson 2013 on tax capacity; Gordon & Li 2009 on informality and the tax base);
             optional conditional cash transfers to the poorest quintiles in secondary school (Schultz 2004).
"""
import numpy as np
from ..core import Module


class FiscalState(Module):
    name = 'fiscal_state'
    defaults = dict(tax_formal=0.15, tax_cons=0.06, edu_share=0.18, aid=0.0, cct=0.0, cct_quintiles=2,
                    budget_floor=0.02, fiscal_budget=True)   # fiscal_budget=False: keep PublicSchools' budget path, use only the CCT

    def setup(self, E):
        E.budget = None

    def supply(self, E, t):
        p, k = E.p, E.kids
        if p['cct'] > 0:
            E.yr['cct'] += np.where((k['q'] < p['cct_quintiles']) & (k['g'] >= 6) & (k['g'] < 12), p['cct'], 0.0)

    def after(self, E, t):
        p = E.p
        f, i = getattr(E, 'bill', (0.0, 0.0))
        rev = p['tax_formal'] * f + p['tax_cons'] * (f + i)
        floor = p['budget_floor'] * p['N'] * 12
        if p['fiscal_budget']:
            E.budget = max(p['edu_share'] * rev + p['aid'] * p['N'] * 12, floor)
        gdp = f + i
        cct_cost = float((E.yr['cct'] > 0)[E.kids['att']].sum() * p['cct']) if p['cct'] > 0 else 0.0
        E.note(revenue=rev, gdp=gdp, edu_budget=E.budget if E.budget is not None else 0.0, tax_gdp=rev / max(gdp, 1e-9),
               formal_share_gdp=f / max(gdp, 1e-9), cct_cost=cct_cost)

    def summary(self, E):
        R, m = E.R, E.p['measure_from']
        g = lambda key: float(np.mean(R[key][m:]))
        return dict(tax_gdp=g('tax_gdp'), edu_gdp=g('edu_budget') / max(g('gdp'), 1e-9), formal_share_gdp=g('formal_share_gdp'))
