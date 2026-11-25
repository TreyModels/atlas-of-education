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
        # ---- Tullock contest tutoring (only active when at least one gate has kind='contest')
        contest_e_now = np.zeros(n)
        contest_spend_now = np.zeros(n)
        contest_gates = [(m_, gt) for m_, gt in enumerate(p['gates']) if gt.get('kind') == 'contest']
        if contest_gates and len(idx):
            pc = float(p['contest_price'])
            e_cap = float(p['contest_max_e'])
            cash_rem = np.maximum(E._cash[idx] - y['extra_spend'][idx], 0.0)
            yy = np.maximum(k['y'][idx], 0.05)
            # Assign each attending child to their nearest upcoming contest gate
            cred_i = k['cred'][idx]
            g_i = k['g'][idx]
            voc_i = k['voc'][idx]
            lam_learn = E.lrate * np.exp(p['beta_a'] * k['a'][idx])
            assigned = np.full(len(idx), -1, int)
            for m_, gt in contest_gates:
                elig_m = (assigned < 0) & (cred_i <= m_) & (~voc_i if gt.get('academic_only') else True)
                assigned[elig_m] = m_
            for m_, gt in contest_gates:
                sub = np.flatnonzero(assigned == m_)
                if len(sub) == 0:
                    continue
                r_c = float(gt.get('r', p['contest_r']))
                alpha_c = float(gt.get('alpha', p['contest_alpha']))
                x0_c = float(gt.get('x0', p['contest_x0']))
                elw = float(gt.get('elite_logw', p['elite_logw']))
                if elw <= 0.0 and gt.get('fail') != 'track':
                    elw = max(float(E.B[min(m_ + 1, E.nlev)] - E.B[m_]), 0.1)
                yrs_left = np.maximum(E.ends[m_] - g_i[sub], 1)
                dV = (p['delta'] ** (yrs_left - 1)) * p['kappa'] * elw
                L_proj = k['L'][idx[sub]] + lam_learn[sub] * yrs_left
                b_i = x0_c * np.maximum(L_proj, 0.1) / max(E.ends[m_], 1)
                e_cum = k['contest_e'][idx[sub]]
                lam_m = float(E.lam_contest[m_])
                e_hi = np.minimum(e_cap, cash_rem[sub] / max(pc, 1e-9))
                e_hi = np.maximum(e_hi, 0.0)
                c_y = pc / yy[sub]
                # Vectorized 25-point grid search + 8 golden-section refinement steps for exact global max on [0, e_hi]
                grid = np.linspace(0.0, 1.0, 25)[None, :] * e_hi[:, None]
                x_g = np.maximum(b_i[:, None] + alpha_c * (e_cum[:, None] + grid), 1e-6)
                u_g = dV[:, None] * (1.0 - np.exp(-np.clip(lam_m * (x_g ** r_c), 0.0, 50.0))) - c_y[:, None] * grid
                best_j = np.argmax(u_g, axis=1)
                step_w = e_hi / 24.0
                lo = np.maximum(0.0, (best_j - 1) * step_w)
                hi = np.minimum(e_hi, (best_j + 1) * step_w)
                phi = 0.6180339887498949
                for _ in range(8):
                    e1 = hi - phi * (hi - lo)
                    e2 = lo + phi * (hi - lo)
                    x1 = np.maximum(b_i + alpha_c * (e_cum + e1), 1e-6)
                    x2 = np.maximum(b_i + alpha_c * (e_cum + e2), 1e-6)
                    u1 = dV * (1.0 - np.exp(-np.clip(lam_m * (x1 ** r_c), 0.0, 50.0))) - c_y * e1
                    u2 = dV * (1.0 - np.exp(-np.clip(lam_m * (x2 ** r_c), 0.0, 50.0))) - c_y * e2
                    lo = np.where(u1 < u2, e1, lo)
                    hi = np.where(u1 < u2, hi, e2)
                e_opt = 0.5 * (lo + hi)
                # Compare against e=0 corner explicitly
                x0_val = np.maximum(b_i + alpha_c * e_cum, 1e-6)
                u0_val = dV * (1.0 - np.exp(-np.clip(lam_m * (x0_val ** r_c), 0.0, 50.0)))
                x_opt = np.maximum(b_i + alpha_c * (e_cum + e_opt), 1e-6)
                u_opt = dV * (1.0 - np.exp(-np.clip(lam_m * (x_opt ** r_c), 0.0, 50.0))) - c_y * e_opt
                e_opt = np.where((u_opt > u0_val + 1e-9) & (e_opt > 1e-4), e_opt, 0.0)
                contest_e_now[idx[sub]] = e_opt
                contest_spend_now[idx[sub]] = pc * e_opt
            k['contest_e'] += contest_e_now
            y['extra_spend'] += contest_spend_now
        y['tut_kind'] = choice
        g = k['g']                                   # grade being studied this year = g (before increment) + 1
        k12 = att & (g < 12)
        k['tut_k12'] += np.where(k12, y['extra_spend'], 0.0)
        tut_any = (choice > 0) | (contest_e_now > 1e-4)
        G = E.ends[-1]
        by_grade = [float((tut_any & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        own_g = [float((own & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        firm_g = [float(((firm | (contest_e_now > 1e-4)) & att & (g == j)).sum() / max((att & (g == j)).sum(), 1)) for j in range(G)]
        by_q = [float((tut_any & att & (k['q'] == j)).sum() / max((att & (k['q'] == j)).sum(), 1)) for j in range(5)]
        k12_rate_q = [float((tut_any & k12 & (k['q'] == j)).sum() / max((k12 & (k['q'] == j)).sum(), 1)) for j in range(5)]
        k12_spend_q = [float(y['extra_spend'][k12 & (k['q'] == j)].mean()) if (k12 & (k['q'] == j)).any() else 0.0 for j in range(5)]
        g12_mask = att & (g == 11)
        E.note(tut_rate=float(tut_any[att].mean()) if att.any() else 0.0, tut_by_grade=by_grade,
               tut_own_by_grade=own_g, tut_firm_by_grade=firm_g, tut_by_q=by_q, firm_price=pf,
               tut_spend=float(y['extra_spend'][att].sum()),
               firm_rev=float(pf * (firm & att).sum() + contest_spend_now[att].sum()),  # commercial tutoring revenue
               own_share=float(own.sum() / max(tut_any.sum(), 1)),
               tut_k12_rate=float(tut_any[k12].mean()) if k12.any() else 0.0,
               tut_k12_spend=float(y['extra_spend'][k12].sum()),
               tut_k12_rate_by_q=k12_rate_q,
               tut_k12_spend_by_q=k12_spend_q,
               tut_g12_rate=float(tut_any[g12_mask].mean()) if g12_mask.any() else 0.0,
               contest_e_mean=float(contest_e_now[k12].mean()) if k12.any() else 0.0)

    def summary(self, E):
        R, m = E.R, E.p['measure_from']
        A = lambda key: np.mean(np.array(R[key][m:], float), 0)
        return dict(tut_rate=float(A('tut_rate')), tut_by_grade=list(A('tut_by_grade')),
                    tut_own_by_grade=list(A('tut_own_by_grade')), tut_firm_by_grade=list(A('tut_firm_by_grade')),
                    tut_by_q=list(A('tut_by_q')), firm_price=float(A('firm_price')), own_share=float(A('own_share')),
                    tut_k12_rate=float(A('tut_k12_rate')), tut_k12_spend=float(A('tut_k12_spend')),
                    tut_k12_rate_by_q=list(A('tut_k12_rate_by_q')), tut_k12_spend_by_q=list(A('tut_k12_spend_by_q')),
                    tut_g12_rate=float(A('tut_g12_rate')), contest_e_mean=float(A('contest_e_mean')))
