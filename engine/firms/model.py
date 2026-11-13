"""Firm-side youth labour market: vacancies chosen by firms, two job types, credential ranking, rigid graduate wages.

This is the demand side the Atlas lacked. Firms decide how many vacancies to post; nothing about jobs is a coded path
except the aggregate demand index A_t, which is backed out of the OBSERVED adult unemployment rate (so the youth market
is tied to what the actual economy did) rather than chosen to fit youth unemployment.

Monthly, masses in millions. States of the 16-24 non-student urban population that is in the labour force:
    UG  graduates unemployed and searching            EGg  graduates in graduate jobs
    EGn graduates in non-graduate jobs (downgraded)   UN   non-graduates unemployed
    EN  non-graduates employed (non-graduate jobs)
Plus final-year students who search from the autumn recruitment season (September) until graduation in June
(S_un unsigned, S_sig signed). The old NBS method counted
searching students as unemployed; the method used from Dec 2023 excludes them. That is an observation equation, not a
fitted level shift.

Mechanisms and where they come from
  * Matching: urn-ball (Butters 1977; Blanchard & Diamond 1994), constant returns. Searchers send `a` applications a month.
  * Free entry of vacancies (Pissarides 2000): expected value of a vacancy equals its cost kappa*A_t, solved every month.
  * Graduate jobs need a degree (task requirement). Non-graduate jobs take anyone; with rank='value' a firm that
    receives applicants of both kinds hires the kind worth more to it (graduates, when the trainability edge eps
    outweighs their faster quitting): Thurow 1975 job competition; Blanchard & Diamond 1994 ranking; Moen 1999
    education and ranking; Gautier 2002 crowding out. rank='random' (hire whichever applicant arrives) is the rival
    with no credential screening; the gap between the two is the diploma-disease channel.
  * Productivity of young graduates falls with their relative supply: CES between young and older workers within a skill
    group, elasticity sigma_A (Card & Lemieux 2001 estimate roughly 4-6), with a demand drift g_H fitted to the period
    when supply and demand grew together (Tinbergen's race; Goldin & Katz 2008).
  * Wages adjust partially toward the bargained target w* = z + omega (p - z) at monthly speed lam (Hall 2005 wage
    rigidity). lam=1 is the flexible benchmark.
  * Graduates accept a non-graduate job when its wage, net of a downgrading cost d, beats their reservation value rU_g
    (logistic dispersion nu); that share phi is the downgrading / underemployment margin.
  * Demand: A_t from adult unemployment by inverting the same free-entry condition for adults with rigid adult wages.
    Graduate jobs additionally load on observed real-estate investment (elasticity e_prop) and lose a share dr_drop of
    their value from August 2021. dr_drop is a FITTED residual (the August-2021 step), not a measured demand shock: no
    sourced series maps onto its size (experiments/youth-review, item 1.1).
"""
import math
import numpy as np

DEFAULTS = dict(
    start=(1998, 1), end=(2026, 12), ref_years=(2018, 2019),
    a=0.40, r=0.004,                                      # applications per searcher per month (urn-ball)
    s_g=0.020, s_n=0.030, s_gn=0.035, chi=0.30,          # separations; on-the-job search intensity of downgraded grads
    sep_scale=1.0,                                        # common multiplier on the three separation rates (fitted)
    age_g=1 / 27, age_n=1 / 80,                           # exits from the 16-24 band (grads enter ~21-22, others ~17-18)
    psi_g=0.64, psi_n=0.25,                               # share of each entering flow joining the measured urban LF;
                                                          # set so 2018-19 LF ~33m with graduates ~1/3 (SOURCES lf_size, grad_share)
    july_g=0.9, july_n=0.5,                               # seasonal entry: grads july_g in July, rest spread Aug-Dec; non-grads
    p_g0=1.6, p_n0=1.0, z_g=0.75, z_n=0.55,              # productivities and flow value of unemployment (family support)
    m_g=0.15, m_n=0.10, f_g_ref=0.20, f_n_ref=0.25,      # reference profit margins and job-finding rates (fitted)
    lam_g=0.02, lam_n=0.05,                               # monthly wage adjustment speeds
    sigma_A=5.0, g_H=None, g_N=None,                      # CES elasticity; demand drifts (None = fitted to 2010-2018)
    eps=0.10, d=0.15, nu=0.10, rank='value',
    zeta=0.30,                                            # share of final-year students searching (and counted, old method)
    m_a=0.10, s_y=0.07,                                   # adult margin for the demand inversion; youth share of urban LF
    demand='observed',                                    # 'observed' | 'flat' | callable(year, month) -> A
    e_prop=0.0, dr_drop=0.0,                              # graduate-job demand: elasticity to real-estate investment and
                                                          # a step drop from Aug 2021 (Double Reduction tutoring ban)
    grad_demand='observed',                               # 'observed' (uses the two above) | 'flat'
    grad_shift=None,                                      # callable(year, month) -> multiplier on graduate-job demand (inversion)
    grad_supply=None,                                     # callable(year) -> graduates (millions); None = observed
    nongrad_supply=None,                                  # callable(year) -> non-graduate leavers; None = observed
    S_ref=None,                                           # reference stocks (LF_G, LF_N); None = computed in a first pass
    warm_until=(2008, 1),                                 # warm-up: no CES term and wages at target until this month
)


def urn_x_from_f(f, a):
    """Applications per vacancy x such that a worker's monthly job-finding rate a(1-e^-x)/x equals f."""
    if f >= a:
        raise ValueError('f must be below a')
    lo, hi = 1e-12, 200.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if a * (1 - math.exp(-mid)) / mid > f:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def urn_hires(V, U, a):
    """Urn-ball hires: each of V vacancies is filled if it gets at least one of a*U applications. CRS in (V, U)."""
    if V <= 0 or U <= 0:
        return 0.0
    return V * (1 - math.exp(-a * U / V))


def ces_relative(S, S_ref, sigma):
    """Productivity factor of a group whose supply is S relative to S_ref: (S/S_ref)^(-1/sigma). sigma=inf -> 1."""
    if math.isinf(sigma):
        return 1.0
    return (S / S_ref) ** (-1.0 / sigma)


def _months(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        m += 1
        if m > 12:
            y, m = y + 1, 1


def demand_index(p, data):
    """A_t from adult unemployment: adult free entry with rigid adult wage w_a = 1 - m_a and p_a = 1:
    kappa_a (r+s_a)/q_t = A_t - w_a, with A = 1 at the reference adult rate. The adult rate is the urban rate net of the
    youth contribution (youth share s_y of the urban labour force), seasonally adjusted by calendar-month means.
    Returns dict (y, m) -> A and the adult rate."""
    s_a, a = 0.012, p['a']
    rows = {}
    for y, m in _months((2018, 1), p['end']):
        u = data.urban(y, m)
        yv = data.youth(y, m)
        if u is None:
            continue
        uy = yv[0] if yv else None
        rows[(y, m)] = (u[0], uy)
    # fill youth gaps by linear interpolation so the adult rate can be separated
    keys = sorted(rows)
    have = [(i, rows[k][1]) for i, k in enumerate(keys) if rows[k][1] is not None]
    adult = {}
    for i, k in enumerate(keys):
        uy = rows[k][1]
        if uy is None:
            lo = max([h for h in have if h[0] < i], default=have[0])
            hi = min([h for h in have if h[0] > i], default=have[-1])
            uy = lo[1] if hi[0] == lo[0] else lo[1] + (hi[1] - lo[1]) * (i - lo[0]) / (hi[0] - lo[0])
        adult[k] = (rows[k][0] - p['s_y'] * uy) / (1 - p['s_y']) / 100
    # seasonal adjustment: remove each calendar month's mean deviation (Spring Festival etc.), so A is a demand index
    allm = np.mean(list(adult.values()))
    dev = {mm: np.mean([v for k, v in adult.items() if k[1] == mm]) - allm for mm in range(1, 13)}
    adult = {k: v - dev[k[1]] for k, v in adult.items()}
    ref = np.mean([v for k, v in adult.items() if p['ref_years'][0] <= k[0] <= p['ref_years'][1]])
    q = lambda u: 1 - math.exp(-urn_x_from_f(s_a * (1 - u) / u, a))
    q_ref = q(ref)
    return {k: 1 - p['m_a'] + p['m_a'] * q_ref / q(u) for k, u in adult.items()}, adult


class YouthMarket:
    def __init__(self, data, **over):
        p = dict(DEFAULTS)
        bad = [k for k in over if k not in p]
        if bad:
            raise KeyError(f'unknown parameters {bad}')
        p.update(over)
        self.p, self.data = p, data
        if p['m_g'] >= 1 - p['z_g'] / p['p_g0'] or p['m_n'] >= 1 - p['z_n'] / p['p_n0']:
            raise ValueError('margin too large for the given z: the bargaining share would be negative')
        self.A, self.adult = (demand_index(p, data) if p['demand'] == 'observed' else ({}, {}))
        if p['S_ref'] is None or p['g_H'] is None or p['g_N'] is None:
            self._reference()

    # -------------------------------------------------------------- calibration helpers
    def _reference(self):
        """First pass with no CES and flat demand: reference stocks (2018-19 mean) and the 2010-2018 supply drifts."""
        q = dict(self.p, sigma_A=math.inf, demand='flat', S_ref=(1.0, 1.0), g_H=0.0, g_N=0.0)
        o = YouthMarket.__new__(YouthMarket)
        o.p, o.data, o.A, o.adult = q, self.data, {}, {}
        R = o.run()
        yr = np.array(R['year']); LG = np.array(R['LF_G']); LN = np.array(R['LF_N'])
        sel = (yr >= self.p['ref_years'][0]) & (yr <= self.p['ref_years'][1])
        S_ref = (float(LG[sel].mean()), float(LN[sel].mean()))
        g = lambda X: float(np.log(X[yr == 2018].mean() / X[yr == 2010].mean()) / 8)
        if self.p['S_ref'] is None:
            self.p['S_ref'] = S_ref
        if self.p['g_H'] is None:
            self.p['g_H'] = g(LG)
        if self.p['g_N'] is None:
            self.p['g_N'] = g(LN)

    def A_at(self, y, m):
        dmd = self.p['demand']
        if callable(dmd):
            return dmd(y, m)
        if dmd == 'flat':
            return 1.0
        return self.A.get((y, m), 1.0)

    # -------------------------------------------------------------- the run
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
        st = dict(UG=0.0, EGg=0.0, EGn=0.0, UN=0.0, EN=0.0)
        S_un = S_sig = 0.0; pending = 0.0
        w_g, w_n = w_g0, w_n0
        hist_G, hist_N = [], []                                 # trailing 12-month labour-force stocks (CES supply)
        out = {k: [] for k in ('year', 'month', 'rate_old', 'rate_new', 'UG', 'EGg', 'EGn', 'UN', 'EN', 'LF_G', 'LF_N',
                               'f_g', 'f_n', 'phi', 'p_g', 'p_n', 'w_g', 'w_n', 'V_g', 'V_n', 'grad_share_n_hires',
                               'A', 'u_G', 'u_N', 'under', 'S_un', 'resid_n', 'balance')}
        t_ref = p['ref_years'][0] + 0.5 * (p['ref_years'][1] - p['ref_years'][0]) + 0.5
        for y, m in _months(p['start'], p['end']):
            tt = y + (m - 0.5) / 12 - t_ref
            A = self.A_at(y, m)
            hist_G.append(st['UG'] + st['EGg'] + st['EGn']); hist_N.append(st['UN'] + st['EN'])
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
            # wages: partial adjustment toward the bargained target
            lg, ln = (1.0, 1.0) if warm else (p['lam_g'], p['lam_n'])
            w_g += lg * (p['z_g'] + om_g * (p_g - p['z_g']) - w_g)
            w_n += ln * (p['z_n'] + om_n * (p_n - p['z_n']) - w_n)
            J_g = (p_g - w_g) / dg
            J_Nn = (p_n - w_n) / dn
            J_Gn = (p_n * (1 + p['eps']) - w_n) / dgn
            # students search Feb-Jun of the final year
            if m == 9:                                   # autumn recruitment opens for next summer's graduating class
                S_un, S_sig = p['psi_g'] * G(y + 1), 0.0
            searching = m >= 9 or m <= 6
            stud = p['zeta'] * S_un if searching else 0.0
            # ---- graduate-job market (degree required)
            Ueff = st['UG'] + p['chi'] * st['EGn'] + stud
            kg = kap_g * A
            if J_g > kg and Ueff > 0:
                x = -math.log(1 - kg / J_g)
                f_g = a * (1 - math.exp(-x)) / x
                V_g = a * Ueff / x
            else:
                f_g, V_g = 0.0, 0.0
            hG_U, hG_O, hG_S = f_g * st['UG'], f_g * p['chi'] * st['EGn'], f_g * stud
            # ---- reservation value of an unemployed graduate and the downgrading share
            rU = (dg * p['z_g'] + f_g * w_g) / (dg + f_g)
            phi = 1 / (1 + math.exp(-((w_n - p['d']) - rU) / (p['nu'] * p['p_n0'])))
            Gapp = phi * (st['UG'] - hG_U)
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
                cls = p['psi_g'] * G(y)
                signed_now = S_sig
                pending = cls - S_sig
                S_un = S_sig = 0.0
            if m >= 7 and pending > 0:
                infl_g = pending * (p['july_g'] if m == 7 else (1 - p['july_g']) / 5)
            infl_n = p['psi_n'] * NL(y) * (p['july_n'] if m == 7 else (1 - p['july_n']) / 11)
            # ---- stock updates (explicit; balance checked below)
            before = sum(st.values())
            age_out = p['age_g'] * (st['UG'] + st['EGg'] + st['EGn']) + p['age_n'] * (st['UN'] + st['EN'])
            UG, EGg, EGn, EN = st['UG'], st['EGg'], st['EGn'], st['EN']
            st['UG'] = UG + infl_g - hG_U - hGn + p['s_g'] * EGg + p['s_gn'] * EGn - p['age_g'] * UG
            st['EGg'] = EGg + hG_U + hG_O + signed_now - p['s_g'] * EGg - p['age_g'] * EGg   # signed students start jobs
            st['EGn'] = EGn + hGn - hG_O - p['s_gn'] * EGn - p['age_g'] * EGn
            st['UN'] = UN + infl_n - hNn + p['s_n'] * EN - p['age_n'] * UN
            st['EN'] = EN + hNn - p['s_n'] * EN - p['age_n'] * EN
            if searching:
                S_un -= hG_S; S_sig += hG_S
            balance = sum(st.values()) - (before + infl_g + infl_n - age_out) - signed_now
            # ---- observation equations
            U = st['UG'] + st['UN']; LF = sum(st.values())
            su = p['zeta'] * S_un if searching else 0.0              # searching, unsigned students (old method only)
            rate_new = 100 * U / LF if LF > 0 else float('nan')
            rate_old = 100 * (U + su) / (LF + su) if LF > 0 else float('nan')
            LG = st['UG'] + st['EGg'] + st['EGn']; LN = st['UN'] + st['EN']
            for k, v in (('year', y), ('month', m), ('rate_old', rate_old), ('rate_new', rate_new), ('LF_G', LG), ('LF_N', LN),
                         ('f_g', f_g), ('f_n', f_n), ('phi', phi), ('p_g', p_g), ('p_n', p_n), ('w_g', w_g), ('w_n', w_n),
                         ('V_g', V_g), ('V_n', V_n), ('grad_share_n_hires', hGn / (hGn + hNn) if hGn + hNn > 0 else 0.0),
                         ('A', A), ('u_G', 100 * st['UG'] / LG if LG > 0 else 0.0), ('u_N', 100 * st['UN'] / LN if LN > 0 else 0.0),
                         ('under', 100 * st['EGn'] / (st['EGg'] + st['EGn']) if st['EGg'] + st['EGn'] > 0 else 0.0),
                         ('S_un', S_un), ('resid_n', resid), ('balance', balance)):
                out[k].append(v)
            for k in ('UG', 'EGg', 'EGn', 'UN', 'EN'):
                out[k].append(st[k])
        self.R = out
        return out


def series(R, key, y0, y1):
    return [v for v, y in zip(R[key], R['year']) if y0 <= y <= y1]


def at(R, key, y, m):
    for v, yy, mm in zip(R[key], R['year'], R['month']):
        if yy == y and mm == m:
            return v
    return None
