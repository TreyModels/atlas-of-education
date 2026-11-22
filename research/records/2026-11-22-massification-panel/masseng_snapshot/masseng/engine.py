"""Cohort-flow engine for a national education system.

State: for every birth cohort b, income decile d (ten equal groups), grade g and sector s (public/private), the
share of the cohort enrolled in a reference year. Reference year y = year in which the school year ends (UIS).
Flows are deterministic expected values (no random draws), so a run is exactly reproducible.

Each year, every enrolled pupil either repeats (fixed share r of the level) or passes, and then the household
decides whether the child continues. The decision is a logit in:
    alpha_level (+ separate intercept when entering a new level)
  + eta   * ln(household income relative to the 1990 national mean)        demand rises with income
  - kappa * (annual cost of a school year / household income)              cost and affordability
At entry to a level the household also chooses a sector (nested logit): private carries an intercept mu_level
and an income slope nu, public is the reference. Public tertiary first-year places are rationed (capacity rule
is a named hypothesis); applicants not offered a public place can still take a private one at private cost.

Grades 0-5 primary, 6-9 lower secondary, 10-11 upper secondary (only from the year the country introduces it),
12-15 tertiary (4 years). Before upper secondary exists, lower-secondary completers go straight to tertiary.
"""
from dataclasses import dataclass, field

import numpy as np

from .data import Country, decile_income_multipliers

PUB, PRIV = 0, 1
LEVEL_OF_GRADE = np.array([0] * 6 + [1] * 4 + [2] * 2 + [3] * 4)   # 0 prim, 1 lower sec, 2 upper sec, 3 tertiary
LEVEL_NAMES = ['primary', 'secondary', 'upper_secondary', 'tertiary']
N_GRADES = 16
FIRST_GRADE_OF_LEVEL = {0: 0, 1: 6, 2: 10, 3: 12}

# Names and default values of the behavioural parameters. Which of them are fitted is set in calibrate.py.
DEFAULTS = dict(
    eta=1.0,          # demand growth over time: log-odds per log of national income per head (or trend)
    eta_x=0.5,        # cross-sectional income gradient: log-odds per log of decile income relative to the mean
    kappa=1.0,        # cost burden coefficient (log-odds per unit of cost / income)
    a_prim=4.0,       # primary entry and continuation intercept
    a_sec=3.0,        # secondary continuation intercept (within level)
    a_sec_entry=1.0,  # primary -> secondary transition intercept (also used for JHS -> SHS)
    a_ter=2.5,        # tertiary continuation intercept
    a_ter_entry=-1.0, # secondary -> tertiary transition intercept
    late=0.15,        # share of children who start Grade 1 one year after their planned age
    rep_prim=0.04,    # yearly repetition share, primary
    rep_sec=0.02,     # yearly repetition share, secondary
    mu_basic=-2.5,    # private-sector intercept, primary and secondary
    mu_ter=0.5,       # private-sector intercept, tertiary
    nu=1.0,           # income slope of choosing private (basic education; also tertiary unless split_nu)
    nu_ter=1.0,       # income slope of choosing private, tertiary (v4)
    k_ter=0.06,       # public tertiary first-year places / population at tertiary entry age, in anchor year
    k_growth=0.03,    # yearly growth of k_ter under the 'trend' rule
    k_resp=0.10,      # share of the unmet public demand converted into new places per year ('responsive' rule)
)


@dataclass
class Result:
    years: np.ndarray
    ind: dict                    # indicator name -> array over years
    extra: dict = field(default_factory=dict)


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class Model:
    def __init__(self, country: Country, params=None, supply_rule=None, demand_form='income', switches=None,
                 burden_form='log', split_income=True, split_nu=True):
        self.c = country
        self.cfg = country.config
        self.p = dict(DEFAULTS)
        if params:
            self.p.update(params)
        self.supply_rule = supply_rule or self.cfg['tertiary_public_capacity']['rule']
        self.split_nu = split_nu            # v4: separate private-choice income slopes for basic and tertiary
        self.split_income = split_income    # v1/v2: one eta for time and cross-section; v3: eta and eta_x
        self.burden_form = burden_form      # 'linear': kappa * c/Y (v1);  'log': kappa * ln(1 + c/Y) (v2, graded)
        self.demand_form = demand_form      # 'income' (eta * ln income) or 'trend' (eta * smooth time trend) or 'none'
        self.sw = dict(policies=True, cost=True)
        if switches:
            self.sw.update(switches)
        yrs = self.cfg['years']
        self.y0, self.y1 = yrs['simulate_from'], yrs['simulate_to']
        self.max_age = self.cfg['structure']['max_age']
        st = self.cfg['structure']
        self.shs_from = st.get('upper_secondary_from', 10 ** 6)
        self.n_lower = st.get('lower_secondary_grades', 4)            # lower + upper secondary = 6 grades
        assert self.n_lower + st.get('upper_secondary_grades', 6 - self.n_lower) == 6
        L = self.n_lower
        self.level_of_grade = np.array([0] * 6 + [1] * L + [2] * (6 - L) + [3] * 4)
        self.first_grade = {0: 0, 1: 6, 2: 6 + L, 3: 12}
        self.last_lower = 5 + L
        # optional: entry beyond age 8 (late entrants and re-entry), and post-conflict catch-up entry
        self.late_max_age = st.get('late_entry_max_age', 8)
        self.late_hazard = st.get('late_entry_hazard', 0.0)
        self.catch_up = self.cfg.get('catch_up_entry')               # dict(years=[a,b], max_age=, rate=)
        # optional exam gate between upper secondary and tertiary: pass-rate series (share of candidates)
        gate = self.cfg.get('tertiary_entry_exam')
        self.exam = None
        if gate:
            pts = sorted((int(k), v) for k, v in gate['pass_rate'].items() if not k.startswith('_'))
            self.exam = dict(pts=pts, default=gate.get('default_before_data', pts[0][1]))
        self.anchor = self.cfg['tertiary_public_capacity'].get('anchor_year', 1985)
        self._prepare_exogenous()

    # ------------------------------------------------------------------ exogenous paths
    def _prepare_exogenous(self):
        c, cfg = self.c, self.cfg
        years = np.arange(self.y0, self.y1 + 1)
        self.years = years
        self.gdp = np.array([c.gdppc(y) for y in years])
        self.gdp_ref = c.gdppc(1990)
        gini_default = cfg.get('demography', {}).get('gini_default', 0.42)
        self.mult = np.array([decile_income_multipliers((c.gini(y) / 100) if c.gini else gini_default) for y in years])
        # log household income relative to 1990 national mean, by year x decile
        self.lninc = np.log(self.mult * self.gdp[:, None] / self.gdp_ref)
        # smooth trend alternative with the same 1971-1995 mean slope as ln GDP (for the 'trend' rival)
        t = years - 1990.0
        lo, hi = cfg['years']['train']
        m = (years >= lo) & (years <= hi)
        slope = np.polyfit(t[m], np.log(self.gdp[m] / self.gdp_ref), 1)[0]
        self.lntrend = (slope * t)[:, None] + np.log(self.mult)
        # costs: years x level x sector, share of GDP per capita
        base = cfg['costs_share_of_gdppc']
        cost = np.zeros((len(years), 4, 2))
        for li, name in enumerate(LEVEL_NAMES):
            cost[:, li, PUB] = base[name]['public']
            cost[:, li, PRIV] = base[name]['private']
        self.events_applied = []
        if self.sw['policies']:
            for ev in cfg.get('policy_events', []):
                if 'level' not in ev:
                    continue
                li = LEVEL_NAMES.index(ev['level'])
                si = PUB if ev['sector'] == 'public' else PRIV
                cost[years >= ev['year'], li, si] += ev['cost_change']
                self.events_applied.append(ev['what'])
        self.cost = np.maximum(cost, 0.005)
        # decile-targeted transfers (e.g. conditional cash transfers): years x decile x level reductions
        self.transfer = np.zeros((len(years), 10, 4))
        if self.sw['policies']:
            for tr in cfg.get('transfers', []):
                for li in tr['levels']:
                    for d in tr['deciles']:
                        ramp = np.clip((years - tr['year'] + 1) / max(tr.get('ramp_years', 1), 1), 0, 1)
                        self.transfer[:, d, LEVEL_NAMES.index(li)] += tr['value'] * ramp
        # entry-age plan
        self.s6 = np.array([np.interp(y, *zip(*sorted((int(k), v) for k, v in cfg['entry_age']['share_at_6'].items()
                                                         if not k.startswith('_')))) for y in years])
        # cohort sizes
        self.b_lo = self.y0 - self.max_age - 2
        self.b_hi = self.y1
        self.cohort = np.array([c.survivors(b) for b in range(self.b_lo, self.b_hi + 1)])
        # official age bands for indicators (UIS definitions as reported in WDI)
        prm_age = c.wdi('SE.PRM.AGES')
        sec_dur = c.wdi('SE.SEC.DURS')
        prm_dur = c.wdi('SE.PRM.DURS')
        self.band = {}
        for y in years:
            a0 = int(round(prm_age(y))) if prm_age else 6
            pd = int(round(prm_dur(y))) if prm_dur else 6
            sd = int(round(sec_dur(y))) if sec_dur else 6
            self.band[y] = dict(primary=(a0, a0 + pd), secondary=(a0 + pd, a0 + pd + sd),
                                tertiary=(a0 + pd + sd, a0 + pd + sd + 5))

    # ------------------------------------------------------------------ behaviour
    def _demand_term(self, yi):
        cross = np.log(self.mult[yi])
        if self.split_income:   # v3: separate time and cross-sectional coefficients
            if self.demand_form == 'income':
                time = np.log(self.gdp[yi] / self.gdp_ref)
            elif self.demand_form == 'trend':
                time = self.lntrend[yi][0] - cross[0]
            else:
                time = 0.0
            return self.p['eta'] * time + self.p['eta_x'] * cross
        if self.demand_form == 'income':
            return self.p['eta'] * self.lninc[yi]
        if self.demand_form == 'trend':
            return self.p['eta'] * self.lntrend[yi]
        return self.p['eta'] * np.log(self.mult[yi])      # 'none': cross-sectional income only, no growth

    def _v(self, yi, li):
        """Sector utilities (decile x sector) for level li in year index yi."""
        p = self.p
        k = p['kappa'] if self.sw['cost'] else 0.0
        burden = (self.cost[yi, li, :][None, :] - self.transfer[yi, :, li][:, None]).clip(0.0) / self.mult[yi][:, None]
        v = -k * (np.log1p(burden) if self.burden_form == 'log' else burden)
        mu = p['mu_ter'] if li == 3 else p['mu_basic']
        nu = p['nu_ter'] if (li == 3 and self.split_nu) else p['nu']
        v[:, PRIV] += mu + nu * self.lninc[yi]
        return v

    # ------------------------------------------------------------------ simulation
    def run(self, record_deciles=False):
        p = self.p
        nb = self.b_hi - self.b_lo + 1
        E = np.zeros((nb, 10, N_GRADES, 2))            # cohort share enrolled (each decile holds 0.1 of a cohort)
        grads = np.zeros((nb, 10, 4))                  # completers of each level (left the system after completing)
        drops = np.zeros((nb, 10))                     # left during a level (did not continue)
        aged = np.zeros((nb, 10))                      # still enrolled when the cohort passed max_age
        entered = np.zeros((nb, 10))
        notyet = np.full((nb, 10), 0.1)                # share of cohort never entered so far
        Y = self.years
        out = {k: np.full(len(Y), np.nan) for k in
               ['ger_primary', 'ner_primary', 'ger_secondary', 'ner_secondary', 'ger_tertiary',
                'priv_primary', 'priv_secondary', 'priv_lower_secondary', 'priv_upper_secondary', 'priv_tertiary',
                'ter_entrants', 'ter_rationed_share', 'k_ter']}
        dec_part = {}
        k_ter = p['k_ter']
        unmet_prev = 0.0
        rc = self.cfg.get('repetition', {})
        rp, rs = rc.get('primary', p['rep_prim']), rc.get('secondary', p['rep_sec'])
        rep = np.array([rp, rs, rs, 0.0])
        a_within = np.array([p['a_prim'], p['a_sec'], p['a_sec'], p['a_ter']])
        a_entry = np.array([p['a_prim'], p['a_sec_entry'], p['a_sec_entry'], p['a_ter_entry']])
        bidx = np.arange(self.b_lo, self.b_hi + 1)

        for yi, y in enumerate(Y):
            age = y - 1 - bidx                                    # age at start of school year
            alive = (age >= 5) & (age <= self.max_age)
            demand = self._demand_term(yi)                        # decile
            V = [self._v(yi, li) for li in range(4)]              # each decile x sector
            IV = [np.logaddexp(v[:, 0], v[:, 1]) for v in V]
            share_priv = [np.exp(v[:, 1] - iv) for v, iv in zip(V, IV)]

            newE = np.zeros_like(E)
            # ---- continuation of last year's pupils
            t1_pool = np.zeros((nb, 10))   # passers who reach the tertiary-entry decision this year
            for g in range(N_GRADES):
                mass = E[:, :, g, :]                               # nb x 10 x 2
                if not mass.any():
                    continue
                li = self.level_of_grade[g]
                stay = mass * rep[li]
                passed = mass - stay
                # repeaters continue in their own sector
                pc = _sigmoid(a_within[li] + demand[:, None] + V[li])           # 10 x 2
                newE[:, :, g, :] += stay * pc[None]
                drops += (stay * (1 - pc[None])).sum(axis=2)
                # passers
                if g == 5 or g == self.last_lower or g == 11 or g == 15:
                    tot = passed.sum(axis=2)                       # sector of the next level is chosen afresh
                    if g == 5:
                        grads[:, :, 0] += 0  # completion is counted at exit below
                        nxt_level = 1
                    elif g == self.last_lower:
                        nxt_level = 2 if y >= self.shs_from else 3
                    elif g == 11:
                        nxt_level = 3
                    else:
                        grads[:, :, 3] += tot
                        continue
                    lvl_done = self.level_of_grade[g]
                    if nxt_level == 3:
                        t1_pool += tot
                        # completers of the secondary cycle who do not enter tertiary are counted later
                        continue
                    ng = self.first_grade[nxt_level]
                    pe = _sigmoid(a_entry[nxt_level] + demand + IV[nxt_level])        # 10
                    cont = tot * pe[None]
                    newE[:, :, ng, PUB] += cont * (1 - share_priv[nxt_level])[None]
                    newE[:, :, ng, PRIV] += cont * share_priv[nxt_level][None]
                    grads[:, :, lvl_done] += tot - cont
                else:
                    newE[:, :, g + 1, :] += passed * pc[None]
                    drops += (passed * (1 - pc[None])).sum(axis=2)

            # ---- tertiary entry with rationed public places
            if t1_pool.any() and self.exam is not None:
                pr = self._pass_rate(y)
                failed = t1_pool * (1 - pr)
                grads[:, :, 1] += failed
                t1_pool = t1_pool * pr
            if t1_pool.any():
                pe_both = _sigmoid(a_entry[3] + demand + IV[3])                       # 10
                pe_priv = _sigmoid(a_entry[3] + demand + V[3][:, PRIV])
                sp = share_priv[3]
                pop_entry = self._pop_at_age(y, self.band[y]['tertiary'][0])
                persons = t1_pool * self.cohort[:, None]                               # nb x 10
                want_pub = (persons * (pe_both * (1 - sp))[None]).sum()
                cap = self._capacity(y, k_ter, unmet_prev) * pop_entry
                f = 1.0 if self.supply_rule == 'unconstrained' or want_pub <= cap else cap / want_pub
                to_pub = t1_pool * (f * pe_both * (1 - sp))[None]
                to_priv = t1_pool * (f * pe_both * sp + (1 - f) * pe_priv)[None]
                newE[:, :, 12, PUB] += to_pub
                newE[:, :, 12, PRIV] += to_priv
                done_sec = t1_pool - to_pub - to_priv
                grads[:, :, 1] += done_sec
                out['ter_entrants'][yi] = ((to_pub + to_priv) * self.cohort[:, None]).sum() / max(pop_entry, 1)
                out['ter_rationed_share'][yi] = 1 - f
                unmet_prev = max(0.0, want_pub - cap) / max(pop_entry, 1)
                if self.supply_rule == 'responsive':
                    k_ter = self._capacity(y, k_ter, unmet_prev)
            out['k_ter'][yi] = self._capacity(y, k_ter, unmet_prev) if self.supply_rule != 'responsive' else k_ter

            # ---- new entrants to Grade 1
            s6_now, s6_1, s6_2 = self.s6[yi], self.s6[max(yi - 1, 0)], self.s6[max(yi - 2, 0)]
            lam = p['late']
            share_at = {6: s6_now * (1 - lam), 7: (1 - s6_1) * (1 - lam) + s6_1 * lam, 8: (1 - s6_2) * lam}
            pe0 = _sigmoid(a_entry[0] + demand + IV[0])
            for a, sh in share_at.items():
                m = age == a
                if m.any():
                    ent = 0.1 * sh * pe0
                    entered[m] += ent[None]
                    notyet[m] -= ent[None]
                    newE[m, :, 0, PUB] += ent[None] * (1 - share_priv[0])[None]
                    newE[m, :, 0, PRIV] += ent[None] * share_priv[0][None]
            # late entry / re-entry of never-entered children aged 9..late_max_age, and catch-up after conflict
            hz = np.zeros(nb)
            if self.late_hazard > 0:
                hz[(age >= 9) & (age <= self.late_max_age)] = self.late_hazard
            if self.catch_up and self.catch_up['years'][0] <= y <= self.catch_up['years'][1]:
                hz[(age >= 7) & (age <= self.catch_up['max_age'])] = np.maximum(
                    hz[(age >= 7) & (age <= self.catch_up['max_age'])], self.catch_up['rate'])
            if hz.any():
                ent = notyet * hz[:, None] * pe0[None]
                entered += ent
                notyet -= ent
                newE[:, :, 0, PUB] += ent * (1 - share_priv[0])[None]
                newE[:, :, 0, PRIV] += ent * share_priv[0][None]

            aged[~alive] += newE[~alive].sum(axis=(2, 3))
            newE[~alive] = 0.0
            E = newE
            self._record(out, yi, y, E, age, record_deciles, dec_part)
        return Result(Y, out, dict(deciles=dec_part, grads=grads, drops=drops, aged=aged, entered=entered,
                                   final_enrolled=E.sum(axis=(2, 3)), events=self.events_applied))

    # ------------------------------------------------------------------ helpers
    def _capacity(self, y, k_ter, unmet_prev):
        p = self.p
        if self.supply_rule == 'fiscal':
            return p['k_ter'] * self.c.gdppc(y) / self.c.gdppc(self.anchor)
        if self.supply_rule == 'trend':
            return p['k_ter'] * np.exp(p['k_growth'] * (y - self.anchor))
        if self.supply_rule == 'responsive':
            return k_ter + p['k_resp'] * unmet_prev
        return np.inf

    def _pass_rate(self, y):
        pts = self.exam['pts']
        if y < pts[0][0]:
            return self.exam['default'] / 100.0
        return float(np.interp(y, [p[0] for p in pts], [p[1] for p in pts])) / 100.0

    def _pop_at_age(self, y, a):
        b = y - 1 - a
        return self.cohort[b - self.b_lo] if self.b_lo <= b <= self.b_hi else 0.0

    def _band_pop(self, y, lo, hi):
        return sum(self._pop_at_age(y, a) for a in range(lo, hi))

    def _record(self, out, yi, y, E, age, record_deciles, dec_part):
        persons = E * self.cohort[:, None, None, None]                  # nb x 10 x g x s
        bands = self.band[y]
        lvl_slices = dict(primary=slice(0, 6), secondary=slice(6, 12), tertiary=slice(12, 16))
        for lev, sl in lvl_slices.items():
            lo, hi = bands[lev]
            pop = self._band_pop(y, lo, hi)
            enr = persons[:, :, sl, :].sum()
            out[f'ger_{lev}'][yi] = 100 * enr / pop if pop > 0 else np.nan
            if lev != 'tertiary':
                on = (age >= lo) & (age < hi)
                out[f'ner_{lev}'][yi] = 100 * persons[on][:, :, sl, :].sum() / pop if pop > 0 else np.nan
            out[f'priv_{lev}'][yi] = 100 * persons[:, :, sl, PRIV].sum() / enr if enr > 0 else np.nan
            out.setdefault(f'enrol_{lev}', np.full(len(self.years), np.nan))[yi] = enr
        for name, sl in (('lower_secondary', slice(6, 6 + self.n_lower)), ('upper_secondary', slice(6 + self.n_lower, 12))):
            enr = persons[:, :, sl, :].sum()
            out[f'priv_{name}'][yi] = 100 * persons[:, :, sl, PRIV].sum() / enr if enr > 0 else np.nan
        for lev, sl in lvl_slices.items():
            lo, hi = bands[lev]
            pop_d = self._band_pop(y, lo, hi) / 10
            if pop_d > 0:
                byd = persons[:, :, sl, :].sum(axis=(0, 2, 3)) / pop_d
                out.setdefault(f'gradlr_{lev}', np.full(len(self.years), np.nan))[yi] = \
                    10 * np.log(max(byd[9], 1e-12) / max(byd[0], 1e-12))
        if record_deciles:
            # participation by decile: enrolled in level (any age) / decile population in the official band
            res = {}
            for lev, sl in lvl_slices.items():
                lo, hi = bands[lev]
                pop_d = self._band_pop(y, lo, hi) / 10
                res[lev] = (100 * persons[:, :, sl, :].sum(axis=(0, 2, 3)) / pop_d).tolist() if pop_d > 0 else None
            dec_part[int(y)] = res
