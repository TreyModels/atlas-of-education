"""School supply: public schools (the state's seats, teachers and quality) and private schools (free entry).

PublicSchools   budget -> teachers at a set pay -> class size -> quality (Hanushek 1986; Krueger 1999 on class size);
                informal levies where operating money falls short (Bray 1999, 2009); teachers withhold lessons when they
                can sell them back (Biswal 1999; Jayachandran 2014); seats rationed above a maximum class size.
PrivateSchools  low-cost private schools enter until fees cover costs (James 1993 excess vs differentiated demand;
                Andrabi, Das & Khwaja 2008; Muralidharan & Sundararaman 2015).
Basic education = Grades 1-12. Tertiary is fee-paying and unrationed in v0.1 (a stated simplification).
"""
import numpy as np
from ..core import Module


class PublicSchools(Module):
    name = 'public_schools'
    defaults = dict(
        budget_per_child=0.08, budget_growth=0.0,   # yearly budget per school-age child (wage units), unless FiscalState sets it
        salary_share=0.8, pay_ratio=1.0, w_outside=2.5,   # teacher pay = pay_ratio x outside wage of a graduate
        ptr_target=35.0, ptr_max=70.0, alpha_ptr=0.25,    # class-size elasticity of quality; rationing above ptr_max
        ops_need=0.02, fee_public=0.0, fee_tertiary=0.45,
        h_max=0.4, monitoring=0.3,
        staffing='budget',          # 'budget': pay fixed, teachers = salary budget / pay, class size floats (v0.3).
                                    # 'norm' (planning rule, v0.4 amendment): hire to ptr_target; if the salary budget
                                    # cannot pay the scale for that many teachers, effective pay falls (contract teachers,
                                    # arrears, unpaid allowances) and the pay gap that drives withholding widens.
        withhold_mode='pay_gap',    # 'pay_gap': h grows with the pay gap (Biswal); 'incentive': h depends only on being able to sell it
    )

    def setup(self, E):
        self.E_pub = None
        E.budget = None

    def budget(self, E, t):
        p = E.p
        if E.budget is not None:                      # set by FiscalState
            return E.budget
        return p['budget_per_child'] * p['N'] * 12 * (1 + p['budget_growth']) ** t

    def supply(self, E, t):
        p, k, y = E.p, E.kids, E.yr
        B = self.budget(E, t)
        demand = self.E_pub if self.E_pub is not None else 0.6 * p['N'] * 12
        wT = p['pay_ratio'] * p['w_outside']
        if p['staffing'] == 'norm':
            T_norm = max(demand, 1.0) / p['ptr_target']
            wT = min(wT, p['salary_share'] * B / T_norm)
        T = p['salary_share'] * B / wT
        ptr = max(demand, 1.0) / max(T, 1e-9)
        q = p['q0'] * min(1.25, (p['ptr_target'] / max(ptr, 1e-9)) ** p['alpha_ptr'])
        grant = (1 - p['salary_share']) * B / max(demand, 1.0)
        levy = max(0.0, p['ops_need'] - grant)
        sell = getattr(E, 'tut_sell', 0.0)            # can teachers sell tutoring to their own pupils? (TutoringMarket)
        driver = max(0.0, 1 - wT / p['w_outside']) if p['withhold_mode'] == 'pay_gap' else 1.0
        h = p['h_max'] * driver * (1 - p['monitoring']) * sell
        basic = k['g'] < 12
        pub = k['sector'] == 0
        y['cost'] += np.where(basic & pub, p['fee_public'] + levy, np.where(~basic, p['fee_tertiary'], 0.0))
        y['quality'] = np.where(basic & pub, q, y['quality'])
        y['withheld'] = np.where(basic & pub, h, y['withheld'])
        self.T, self.seats, self.q, self.h, self.levy, self.B, self.wT = T, T * p['ptr_max'], q, h, levy, B, wT

    def sector(self, E, t):
        p, k, r = E.p, E.kids, E.rng
        cand = k['att'] & (k['g'] < 12) & (k['sector'] == 0)
        idx = np.flatnonzero(cand)
        rationed = np.zeros(len(k['y']), bool)
        if len(idx) > self.seats:
            out = r.choice(idx, len(idx) - int(self.seats), replace=False)
            rationed[out] = True
        E.yr['rationed'] = rationed
        if not getattr(E, 'has_private', False):       # nowhere else to go
            k['att'][rationed] = False
            k['reason'][rationed & k['started']] = 5
        n_pub = int((cand & ~rationed).sum())
        self.E_pub = n_pub
        spend = min(self.T * self.wT + (1 - p['salary_share']) * self.B, self.B)
        E.note(pub_enrol=n_pub, teachers=self.T, ptr=n_pub / max(self.T, 1e-9), q_pub=self.q, withheld=self.h,
               levy=self.levy, pub_budget=self.B, pub_spend=spend, rationed=int(rationed.sum()),
               teacher_pay=self.wT)

    def summary(self, E):
        R, m = E.R, E.p['measure_from']
        g = lambda key: float(np.mean(R[key][m:]))
        return dict(ptr=g('ptr'), q_pub=g('q_pub'), withheld=g('withheld'), levy=g('levy'),
                    pub_spend=g('pub_spend'), pub_budget=g('pub_budget'), rationed_share=g('rationed') / max(g('pub_enrol'), 1))


class PrivateSchools(Module):
    name = 'private_schools'
    defaults = dict(
        priv_wage=1.0, priv_ptr=25.0, priv_overhead=0.02, priv_markup=0.15,   # cost per pupil = wage/ptr + overhead
        priv_quality=1.1, priv_entry=0.3, priv_elast=1.0, voucher=0.0, priv_taste=0.05,
    )

    def setup(self, E):
        E.has_private = True
        p = E.p
        self.c = p['priv_wage'] / p['priv_ptr'] + p['priv_overhead']
        self.K = 0.0; self.D = 0.0

    def price(self, E):
        p = E.p
        self.c = p['priv_wage'] / p['priv_ptr'] + p['priv_overhead']
        lr = self.c * (1 + p['priv_markup'])
        if self.K <= 0:
            return lr * 1.5
        return lr * max(1.0, self.D / self.K) ** (1 / p['priv_elast'])

    def supply(self, E, t):
        p, k, y = E.p, E.kids, E.yr
        self.p_t = self.price(E)
        priv = (k['sector'] == 1) & (k['g'] < 12)
        y['cost'] = np.where(priv, y['cost'] + self.p_t * (1 - p['voucher']), y['cost'])
        y['quality'] = np.where(priv, p['q0'] * p['priv_quality'], y['quality'])
        y['withheld'] = np.where(priv, 0.0, y['withheld'])   # owners monitor their own teachers

    def sector(self, E, t):
        p, k, r, y = E.p, E.kids, E.rng, E.yr
        att = k['att']; basic = att & (k['g'] < 12)
        rationed = y.get('rationed', np.zeros(len(att), bool))
        decide = basic & (np.isin(k['g'], [0, 6, 9]) | rationed | (k['sector'] == 1))
        idx = np.flatnonzero(decide)
        fee = self.p_t * (1 - p['voucher'])
        go_priv = np.zeros(len(att), bool)
        if len(idx):
            mvl = E.mvl(t, idx)
            q_pub = getattr(E.modules_by_name.get('public_schools'), 'q', p['q0'])
            h = getattr(E.modules_by_name.get('public_schools'), 'h', 0.0)
            gain = mvl * (p['q0'] * p['priv_quality'] - q_pub * (1 - h))      # one year of better schooling
            cost = fee / np.maximum(k['y'][idx], 0.05)
            want = gain - cost + p['priv_taste'] * r.standard_normal(len(idx)) > 0
            want |= rationed[idx]                                                # no public seat: private or nothing
            afford = E._cash[idx] >= fee
            go_priv[idx[want & afford]] = True
        # capacity: if more want private than seats, the highest-income get them (they bid most)
        dem = np.flatnonzero(go_priv)
        self.D = len(dem)
        if self.K > 0 and len(dem) > self.K:
            keep = dem[np.argsort(-k['y'][dem])][:int(self.K)]
            go_priv[:] = False; go_priv[keep] = True
        elif self.K <= 0:
            go_priv[:] = False
        # free entry: capacity moves toward demand when the price covers cost
        if self.p_t >= self.c:
            self.K += p['priv_entry'] * (self.D - self.K) + (1.0 if self.K < 1 else 0.0) * min(self.D, 0.02 * p['N'])
        else:
            self.K *= 0.9
        self.K = max(self.K, 0.0)
        # switch sectors; rationed children with no private seat leave
        newly = go_priv & (k['sector'] == 0)
        back = basic & (k['sector'] == 1) & ~go_priv
        k['sector'][go_priv] = 1; k['sector'][back] = 0
        lost = rationed & ~go_priv
        k['att'][lost] = False
        k['reason'][lost & k['started']] = 5
        # this year's cost and quality for movers
        y['cost'] = np.where(newly, y['cost'] + fee, np.where(back, y['cost'] - fee, y['cost']))
        y['quality'] = np.where(go_priv, p['q0'] * p['priv_quality'], y['quality'])
        y['withheld'] = np.where(go_priv, 0.0, y['withheld'])
        n_priv = int(go_priv.sum())
        G = E.ends[-1]
        E.note(priv_by_grade=np.bincount(k['g'][go_priv], minlength=G + 1)[:G + 1])
        E.note(priv_enrol=n_priv, priv_share=n_priv / max(int(basic.sum()), 1), priv_fee=self.p_t, priv_cap=self.K,
               priv_by_q=[float(go_priv[basic & (k['q'] == j)].mean()) if (basic & (k['q'] == j)).any() else 0.0 for j in range(5)],
               voucher_cost=n_priv * self.p_t * p['voucher'])

    def summary(self, E):
        R, m = E.R, E.p['measure_from']
        return dict(priv_share=float(np.mean(R['priv_share'][m:])), priv_fee=float(np.mean(R['priv_fee'][m:])),
                    priv_by_q=list(np.mean(np.array(R['priv_by_q'][m:]), 0)))
