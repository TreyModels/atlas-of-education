"""Seasonal-structure variant of the youth market (TODO §5 P1: seasonal mechanisms).

forecast_2024.md shows the two-type model gets the 2025-26 level right but the seasonal amplitude wrong: unemployment
drains too fast through spring and the graduating class lands too abruptly in July. Two candidate mechanisms:
  dd, tau_long  duration dependence. Unemployed graduates move to a long-term pool after tau_long months on average;
                the long-term pool searches with relative intensity dd (< 1: fewer hires, so a stock that persists
                through spring). dd = 1 makes the two pools identical.
  spread        graduates who do not start in July enter the measured labour force evenly over `spread` months after
                July (model.py fixes 5, Aug-Dec); longer spreads model exam and postgraduate-application calendars.
Docking (tier 1, tests in test_firms.py): with dd = 1 and spread = 5 this class reproduces model.YouthMarket to floating
point. The run loop is model.YouthMarket.run with the marked changes; keep the two in step.
"""
import math
import numpy as np
from . import model as M
from .model import urn_x_from_f, ces_relative, _months

SEASONAL_DEFAULTS = dict(dd=1.0, tau_long=6.0, spread=5)


class SeasonalMarket(M.YouthMarket):
    def __init__(self, data, **over):
        sk = {k: over.pop(k) for k in list(over) if k in SEASONAL_DEFAULTS}
        super().__init__(data, **over)
        self.p.update(SEASONAL_DEFAULTS, **sk)
        self.p['spread'] = int(round(self.p['spread']))

    # ---- story hooks (identity by default, so docking with model.YouthMarket is unchanged); see stories.py
    def _demand_mult(self, y, m):            # multiplier on aggregate demand A_t (consumption feedback)
        return 1.0

    def _nongrad_mult(self, y, m):           # multiplier on non-graduate job productivity (automation)
        return 1.0

    def _eps(self, y, m, eps, LF_G, LF_N):   # graduates' edge in non-graduate jobs (credential inflation)
        return eps

    def _class(self, y, cls):                # graduating class entering the labour force this July (queues, delay)
        return cls

    def _after_month(self, y, m, rate_new, st):
        pass

    def run(self):
        p, D = self.p, self.data
        a, r = p['a'], p['r']
        G = p['grad_supply'] or D.graduates
        NL = p['nongrad_supply'] or D.nongrad_school_leavers
        p = dict(p); p['s_g'] *= p['sep_scale']; p['s_n'] *= p['sep_scale']; p['s_gn'] *= p['sep_scale']
        dg, dn, dgn = r + p['s_g'] + p['age_g'], r + p['s_n'] + p['age_n'], r + p['s_gn'] + p['age_g']
        # reference wages, bargaining shares and vacancy costs (kappa in units of aggregate output A_t)
        w_g0 = p['p_g0'] * (1 - p['m_g']); w_n0 = p['p_n0'] * (1 - p['m_n'])
        om_g = (w_g0 - p['z_g']) / (p['p_g0'] - p['z_g']); om_n = (w_n0 - p['z_n']) / (p['p_n0'] - p['z_n'])
        kap_g = (1 - math.exp(-urn_x_from_f(p['f_g_ref'], a))) * (p['p_g0'] - w_g0) / dg
        kap_n = (1 - math.exp(-urn_x_from_f(p['f_n_ref'], a))) * (p['p_n0'] - w_n0) / dn
        SG_ref, SN_ref = p['S_ref']
        st = dict(UG=0.0, UL=0.0, EGg=0.0, EGn=0.0, UN=0.0, EN=0.0)
        dd, to_long = p['dd'], 1.0 / p['tau_long']
        S_un = S_sig = 0.0; pending = 0.0
        w_g, w_n = w_g0, w_n0
        hist_G, hist_N = [], []                                 # trailing 12-month labour-force stocks (CES supply)
        out = {k: [] for k in ('year', 'month', 'rate_old', 'rate_new', 'UG', 'EGg', 'EGn', 'UN', 'EN', 'LF_G', 'LF_N',
                               'f_g', 'f_n', 'phi', 'p_g', 'p_n', 'w_g', 'w_n', 'V_g', 'V_n', 'grad_share_n_hires',
                               'A', 'u_G', 'u_N', 'under', 'S_un', 'resid_n', 'balance', 'UL')}
        t_ref = p['ref_years'][0] + 0.5 * (p['ref_years'][1] - p['ref_years'][0]) + 0.5
        for y, m in _months(p['start'], p['end']):
            tt = y + (m - 0.5) / 12 - t_ref
            A = self.A_at(y, m) * self._demand_mult(y, m)
            hist_G.append(st['UG'] + st['UL'] + st['EGg'] + st['EGn']); hist_N.append(st['UN'] + st['EN'])
            LF_G = float(np.mean(hist_G[-12:])); LF_N = float(np.mean(hist_N[-12:]))
            # CES: young-group productivity falls with its supply relative to a demand drift (balanced growth at g leaves p fixed)
            warm = (y, m) < p['warm_until']
            sig = math.inf if warm else p['sigma_A']
            Dg = 1.0
            if p['grad_demand'] == 'observed' and not warm:
                Dg = D.property_index(y, m) ** p['e_prop'] * (1 - p['dr_drop'] * ((y, m) >= (2021, 8)))
                if p['grad_shift'] is not None:
                    Dg *= p['grad_shift'](y, m)
            p_g = Dg * A * p['p_g0'] * ces_relative(max(LF_G, 1e-9), SG_ref * math.exp(p['g_H'] * tt), sig)
            p_n = A * p['p_n0'] * ces_relative(max(LF_N, 1e-9), SN_ref * math.exp(p['g_N'] * tt), sig)
            p_n *= self._nongrad_mult(y, m)
            # wages: partial adjustment toward the bargained target
            lg, ln = (1.0, 1.0) if warm else (p['lam_g'], p['lam_n'])
            w_g += lg * (p['z_g'] + om_g * (p_g - p['z_g']) - w_g)
            w_n += ln * (p['z_n'] + om_n * (p_n - p['z_n']) - w_n)
            J_g = (p_g - w_g) / dg
            J_Nn = (p_n - w_n) / dn
            J_Gn = (p_n * (1 + self._eps(y, m, p['eps'], LF_G, LF_N)) - w_n) / dgn
            # students search Feb-Jun of the final year
            if m == 9:                                   # autumn recruitment opens for next summer's graduating class
                S_un, S_sig = p['psi_g'] * G(y + 1), 0.0
            searching = m >= 9 or m <= 6
            stud = p['zeta'] * S_un if searching else 0.0
            # ---- graduate-job market (degree required)
            Ueff = st['UG'] + dd * st['UL'] + p['chi'] * st['EGn'] + stud
            kg = kap_g * A
            if J_g > kg and Ueff > 0:
                x = -math.log(1 - kg / J_g)
                f_g = a * (1 - math.exp(-x)) / x
                V_g = a * Ueff / x
            else:
                f_g, V_g = 0.0, 0.0
            hG_U, hG_O, hG_S = f_g * st['UG'], f_g * p['chi'] * st['EGn'], f_g * stud
            hG_L = dd * f_g * st['UL']
            # ---- reservation value of an unemployed graduate and the downgrading share
            rU = (dg * p['z_g'] + f_g * w_g) / (dg + f_g)
            phi = 1 / (1 + math.exp(-((w_n - p['d']) - rU) / (p['nu'] * p['p_n0'])))
            rem_s, rem_l = st['UG'] - hG_U, st['UL'] - hG_L
            Gapp = phi * (rem_s + rem_l)
            UN = st['UN']
            kn = kap_n * A
            hGn = hNn = V_n = 0.0
            resid = 0.0
            if UN + Gapp > 0:
                def value(xN):                      # expected value of a vacancy at applications-per-vacancy xN (non-grads)
                    xG = xN * Gapp / UN if UN > 0 else xN
                    xNn = xN if UN > 0 else 0.0
                    if p['rank'] == 'value':                 # higher-value type first
                        (x1, J1), (x2, J2) = sorted([(xG, J_Gn), (xNn, J_Nn)], key=lambda z: -z[1])
                        return (1 - math.exp(-x1)) * J1 + math.exp(-x1) * (1 - math.exp(-x2)) * J2
                    tot = xG + xNn
                    return (1 - math.exp(-tot)) * (xG * J_Gn + xNn * J_Nn) / tot if tot > 0 else 0.0
                if value(200.0) > kn:
                    lo, hi = 1e-12, 200.0
                    for _ in range(100):
                        mid = math.sqrt(lo * hi)
                        if value(mid) > kn:
                            hi = mid
                        else:
                            lo = mid
                    xN = math.sqrt(lo * hi)
                    resid = value(xN) - kn
                    base = UN if UN > 0 else Gapp
                    V_n = a * base / xN
                    xG = xN * Gapp / UN if UN > 0 else xN
                    xNn = xN if UN > 0 else 0.0
                    if p['rank'] == 'value' and J_Gn >= J_Nn:
                        hGn = V_n * (1 - math.exp(-xG)); hNn = V_n * math.exp(-xG) * (1 - math.exp(-xNn))
                    elif p['rank'] == 'value':
                        hNn = V_n * (1 - math.exp(-xNn)); hGn = V_n * math.exp(-xNn) * (1 - math.exp(-xG))
                    else:
                        tot = xG + xNn
                        h = V_n * (1 - math.exp(-tot)); hGn = h * xG / tot; hNn = h * xNn / tot
            f_n = hNn / UN if UN > 0 else 0.0
            # ---- entry flows
            infl_g = 0.0; signed_now = 0.0
            if m == 7:                                               # signed students start; unsigned enter gradually
                cls = self._class(y, p['psi_g'] * G(y))
                signed_now = S_sig
                pending = cls - S_sig
                S_un = S_sig = 0.0
            k7 = (m - 7) % 12
            if pending > 0 and k7 == 0:
                infl_g = pending * p['july_g']
            elif pending > 0 and 1 <= k7 <= p['spread']:
                infl_g = pending * (1 - p['july_g']) / p['spread']
            infl_n = p['psi_n'] * NL(y) * (p['july_n'] if m == 7 else (1 - p['july_n']) / 11)
            # ---- stock updates (explicit; balance checked below)
            before = sum(st.values())
            age_out = p['age_g'] * (st['UG'] + st['UL'] + st['EGg'] + st['EGn']) + p['age_n'] * (st['UN'] + st['EN'])
            UG, UL, EGg, EGn, EN = st['UG'], st['UL'], st['EGg'], st['EGn'], st['EN']
            tot = rem_s + rem_l
            hGn_s = hGn * rem_s / tot if tot > 0 else hGn
            hGn_l = hGn - hGn_s
            st['UG'] = UG + infl_g - hG_U - hGn_s + p['s_g'] * EGg + p['s_gn'] * EGn - p['age_g'] * UG - to_long * UG
            st['UL'] = UL - hG_L - hGn_l + to_long * UG - p['age_g'] * UL
            st['EGg'] = EGg + hG_U + hG_L + hG_O + signed_now - p['s_g'] * EGg - p['age_g'] * EGg   # signed students start jobs
            st['EGn'] = EGn + hGn - hG_O - p['s_gn'] * EGn - p['age_g'] * EGn
            st['UN'] = UN + infl_n - hNn + p['s_n'] * EN - p['age_n'] * UN
            st['EN'] = EN + hNn - p['s_n'] * EN - p['age_n'] * EN
            if searching:
                S_un -= hG_S; S_sig += hG_S
            balance = sum(st.values()) - (before + infl_g + infl_n - age_out) - signed_now
            # ---- observation equations
            U = st['UG'] + st['UL'] + st['UN']; LF = sum(st.values())
            su = p['zeta'] * S_un if searching else 0.0              # searching, unsigned students (old method only)
            rate_new = 100 * U / LF if LF > 0 else float('nan')
            self._after_month(y, m, rate_new, st)
            rate_old = 100 * (U + su) / (LF + su) if LF > 0 else float('nan')
            LG = st['UG'] + st['UL'] + st['EGg'] + st['EGn']; LN = st['UN'] + st['EN']
            for k, v in (('year', y), ('month', m), ('rate_old', rate_old), ('rate_new', rate_new), ('LF_G', LG), ('LF_N', LN),
                         ('f_g', f_g), ('f_n', f_n), ('phi', phi), ('p_g', p_g), ('p_n', p_n), ('w_g', w_g), ('w_n', w_n),
                         ('V_g', V_g), ('V_n', V_n), ('grad_share_n_hires', hGn / (hGn + hNn) if hGn + hNn > 0 else 0.0),
                         ('A', A), ('u_G', 100 * (st['UG'] + st['UL']) / LG if LG > 0 else 0.0), ('u_N', 100 * st['UN'] / LN if LN > 0 else 0.0),
                         ('under', 100 * st['EGn'] / (st['EGg'] + st['EGn']) if st['EGg'] + st['EGn'] > 0 else 0.0),
                         ('S_un', S_un), ('resid_n', resid), ('balance', balance)):
                out[k].append(v)
            for k in ('UG', 'EGg', 'EGn', 'UN', 'EN', 'UL'):
                out[k].append(st[k])
        self.R = out
        return out
