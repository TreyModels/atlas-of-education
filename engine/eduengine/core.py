"""eduengine core: children, ladder, household choice, learning, gates, beliefs, and the module loop.

Units: money in multiples of the informal adult annual wage (= 1). Learning in grade-equivalents (one year of
full-quality schooling for an average child adds 1). See SPEC.md for the phase order and LITERATURE.md for sources.
"""
import numpy as np
from scipy.special import ndtr

CORE_DEFAULTS = dict(
    seed=0, N=1500, T=70, measure_from=35,          # children per cohort; years simulated; cohorts entering >= measure_from are scored
    levels=[('primary', 6), ('lower', 3), ('upper', 3), ('tertiary', 4)],
    gates=[dict(kind='bar', bar=3.0), dict(kind='bar', bar=5.5), dict(kind='bar', bar=8.0), dict(kind='bar', bar=11.5)],
    exam_sd=1.0,                 # noise in gate scores (grade-equivalents)
    entry_age=6, max_entry_age=9,
    # households
    y_median=1.0, y_sigma=0.75, y_growth=0.0, urban_share=0.4, urban_income=1.6,
    subsist=0.55, shock_sigma=0.3, borrow=0.15,
    child_wage=((8, 0.0), (11, 0.10), (14, 0.35), (17, 0.70), (20, 0.95)),
    need_share=0.5,              # need_mode='constant': share of a child's potential earnings the household must replace
    need_mode='luxury',          # 'luxury' (Basu & Van 1998): a household needs a child's earnings only when poor
    need_max=1.0, poverty_line=1.0, need_width=0.35,   # need = need_max x logistic((poverty_line - y) / (need_width x poverty_line))
    # grade repetition and exam retakes (v0.3)
    promote_bar=0.0,             # promoted if learning >= promote_bar x grade (+ noise); 0 = automatic promotion
    gate_retakes=0,              # times a child who fails a gate exam may repeat the final grade and resit
    voc_quality=0.85,            # learning per year on a vocational track (gates with fail='track' send failers there)
    # anchored enrolment (v0.3): HOW MANY continue follows observed completion (UIS), the mechanism decides WHO
    enrol_targets={},            # {level: [(year, completion), ...]}; levels without targets stay fully modelled
    anchor_stop=None,            # year from which anchoring ends: the implied wedge is frozen at its recent mean and the
                                 # mechanism decides (policy experiments; cf. Chari, Kehoe & McGrattan 2007)
    entry_share=0.97,            # share of a cohort that ever enrols (anchor for the first level)
    rural_cost=0.03,             # extra yearly cost of schooling beyond primary for rural children (distance)
    delta=0.93, kappa=12.0,      # discount factor; weight on the child's future log income (altruism x working-life annuity)
    tau=0.25,                    # logit noise in the continue decision (utility units)
    # learning
    q0=1.0, beta_a=0.25, home_effect=0.15, ses_home=0.6,   # base quality; ability; home input per year; corr(income, home capital)
    learn_noise=0.15,
    # beliefs
    prior_logw=[0.0, 0.05, 0.15, 0.35, 0.8], belief_decay=0.85,
    # measurement anchors (assumed scale; see SDG4 module)
    mpl_primary=4.5, mpl_lower=7.0,
    # calendar, paths and interventions (v0.2)
    start_year=0,                # calendar year of t = 0
    paths={},                    # {param: [(year, value), ...]} interpolated every year (e.g. income growth, budgets)
    events=[],                   # [{'year': Y, 'set': {param: value}, 'label': str}] step changes = interventions
    level_open=None,             # per level: [(year, 0/1), ...] or None; a closed level is skipped (e.g. no Senior High before 2016)
    # street state (v0.2): urban children who leave school young and whom no kin network absorbs (Tilly's trust networks)
    kin_support=0.7, street_age=15,
    # struts that can be switched off for strut-removal tests (see struts.py)
    belief_floor=True,
)


def interp_path(path, x):
    xs, ys = zip(*path)
    return float(np.interp(x, xs, ys))


class Module:
    """Base class. A module declares defaults and fills in any of the phase hooks."""
    name = 'module'
    defaults = {}

    def setup(self, E): pass
    def supply(self, E, t): pass
    def sector(self, E, t): pass
    def extras(self, E, t): pass
    def labour(self, E, t, ex): return None     # only a labour module returns incomes
    def after(self, E, t): pass
    def measure(self, E, t): pass
    def summary(self, E): return {}


class Engine:
    def __init__(self, modules, **params):
        self.modules = list(modules)
        p = dict(CORE_DEFAULTS)
        for m in self.modules:
            p.update(m.defaults)
        unknown = [k for k in params if k not in p]
        if unknown:
            raise KeyError(f'unknown parameters: {unknown}')
        p.update(params)
        if p['measure_from'] >= p['T'] - 1:              # short runs: score the second half instead of crashing
            p['measure_from'] = p['T'] // 2
        self.p = p
        self.rng = np.random.default_rng(p['seed'])
        lv = [n for _, n in p['levels']]
        self.ends = np.cumsum(lv)                     # grade at which each level ends
        self.nlev = len(lv)
        self.B = np.array(p['prior_logw'], float)     # beliefs: expected log income by credential 0..nlev
        self.Bn = np.zeros(self.nlev + 1)
        self.cut = [g.get('cut0', 0.0) for g in p['gates']]   # believed/realised score cutoff for quota gates
        self.cut_adm = [g.get('admit', {}).get('cut0', 0.0) for g in p['gates']]   # admission cutoffs (e.g. gaokao)
        self.lrate = p['q0']                          # believed mean learning per school year
        self.kids = None
        self.labour_module = [m for m in self.modules if m.labour.__func__ is not Module.labour]
        if len(self.labour_module) > 1:
            raise ValueError('use one labour module')
        self.R = dict(year=[])                        # time series, filled by record()
        self.exits = []                               # exited children (dicts of arrays), for cohort tables
        self.census = {}                              # (cohort, age) -> [enrolled, population]
        self.cw = np.array([interp_path(p['child_wage'], a) for a in range(0, 41)])
        self.modules_by_name = {m.name: m for m in self.modules}
        self.event_log = []
        self.closed = [False] * self.nlev
        self.wedge = np.zeros(self.nlev)              # completion wedges (Anchor module; strut S0)
        self.frozen = None                            # frozen implied wedge after anchor_stop
        self.pass_rate = np.ones(self.nlev)           # recent gate pass rates (used by anchored enrolment)
        self.comp_count = {}                          # cohort -> completions by level (for anchoring)
        for m in self.modules:
            m.setup(self)

    # ------------------------------------------------------------------ population
    def add_cohort(self, t):
        p, r, N = self.p, self.rng, self.p['N']
        z = r.standard_normal(N)
        urban = r.random(N) < p['urban_share']
        y = p['y_median'] * np.exp(p['y_sigma'] * z) * (1 + p['y_growth']) ** t * np.where(urban, p['urban_income'], 1.0)
        home = ndtr(p['ses_home'] * z + np.sqrt(1 - p['ses_home'] ** 2) * r.standard_normal(N))  # 0..1 home capital
        new = dict(cohort=np.full(N, t), y=y, z=z, a=r.standard_normal(N), home=home, urban=urban,
                   L=np.zeros(N), g=np.zeros(N, int), cred=np.zeros(N, int), started=np.zeros(N, bool),
                   sector=np.zeros(N, int), att=np.zeros(N, bool), reason=np.full(N, -1),
                   L6=np.full(N, np.nan), L9=np.full(N, np.nan), spend=np.zeros(N), pub_years=np.zeros(N),
                   comp_age=np.full((N, self.nlev), np.nan),
                   q=np.searchsorted(np.quantile(z, [0.2, 0.4, 0.6, 0.8]), z), street=np.zeros(N, bool),
                   gtimes=np.zeros(N, int), repeats=np.zeros(N, int), retakes=np.zeros(N, int), voc=np.zeros(N, bool))
        if self.kids is None:
            self.kids = new
        else:
            self.kids = {k: np.concatenate([self.kids[k], v]) for k, v in new.items()}

    def age(self, t):
        return t - self.kids['cohort'] + self.p['entry_age']

    def level_of(self, g):
        """Index of the level a child with g completed grades is in (nlev if finished)."""
        return np.searchsorted(self.ends, g, side='right')

    # ------------------------------------------------------------------ household valuation
    def values(self, t, L=None, idx=None):
        """Backward induction over remaining levels. Returns (V_stop, V_continue, MVL) per child."""
        p, k = self.p, self.kids
        sl = slice(None) if idx is None else idx
        L = k['L'][sl] if L is None else L
        g, cred, y = k['g'][sl], k['cred'][sl], k['y'][sl]
        lam = self.lrate * np.exp(p['beta_a'] * k['a'][sl])
        Vc = p['kappa'] * self.B                     # value of holding each credential
        n = len(g)
        age_now = self.age(t)[sl]
        ycost = self.yr['cost'][sl] if hasattr(self, 'yr') else np.zeros(n)
        d = p['delta']
        need_frac = self.need_frac(y)
        voc = k['voc'][sl]
        U = np.full(n, Vc[self.nlev])                # value of entering level nlev (= holding top credential)
        cont_now = np.zeros(n)
        lev_now = cred                                # the level a child is working on = credentials held
        for m in range(self.nlev - 1, -1, -1):
            if self.closed[m]:
                continue                               # a level that does not exist: holding m behaves like holding m+1
            start_g = 0 if m == 0 else self.ends[m - 1]
            yrs_left = np.where(lev_now == m, self.ends[m] - g, self.ends[m] - start_g)
            Lend = L + lam * np.maximum(self.ends[m] - g, 0)
            gate = p['gates'][m]
            ref = gate['bar'] if gate['kind'] == 'bar' else self.cut[m]
            P = ndtr((Lend - ref) / p['exam_sd'])
            if gate.get('academic_only'):
                P = np.where(voc, 0.0, P)                # vocational-track pupils cannot sit this exam
            Vfail = Vc[m + 1] if gate.get('fail') == 'track' else Vc[m]   # failing a tracking exam still gives the credential
            Upass = U
            adm = gate.get('admit')
            if adm and m + 1 < self.nlev:              # passing completes level m; a quota rations entry to level m+1
                Pa = ndtr((Lend - self.cut_adm[m]) / p['exam_sd'])
                if adm.get('academic_only'):
                    Pa = np.where(voc, 0.0, Pa)
                Upass = Pa * U + (1 - Pa) * Vc[m + 1]
            # cost per year of this level, relative to household income (log-consumption approximation)
            pv = np.zeros(n)
            for j in range(int(yrs_left.max()) + 1):
                a_ = np.clip(age_now + np.maximum(start_g - g, 0) + j, 0, 40)
                c = ycost + need_frac * self.cw[a_.astype(int)]
                pv += np.where(j < yrs_left, d ** j * c / np.maximum(y, 0.05), 0.0)
            cont = d ** yrs_left * (P * Upass + (1 - P) * Vfail) - pv + self.wedge[m]
            Um = np.maximum(Vc[m], cont)
            cont_now = np.where(lev_now == m, cont, cont_now)
            U = np.where(lev_now <= m, Um, U)
        V_stop = Vc[np.minimum(cred, self.nlev)]
        cont_now = np.where(cred >= self.nlev, -np.inf, cont_now)
        return V_stop, cont_now

    def _target(self, m, Y):
        T = self.p['enrol_targets']
        if m not in T and str(m) not in T:
            return None
        return interp_path(T.get(m, T.get(str(m))), Y)

    def anchored_choice(self, t, idx, net, go):
        """Quantity from data, selection from the mechanism. For each targeted level, the share of started pupils who
        continue this year is the per-year survival implied by the observed completion series (adjusted for gate pass
        rates); the pupils who continue are those with the highest net value among those who can pay this year."""
        p, k, r = self.p, self.kids, self.rng
        Y = self.year(t)
        lev = k['cred'][idx]; g = k['g'][idx]
        started = k['started'][idx]
        age = self.age(t)[idx]
        cash = np.maximum(k['y'][idx] * np.exp(p['shock_sigma'] * self._shock_now[idx]) - p['subsist'], 0) + p['borrow'] * k['y'][idx] + self.yr['cct'][idx]
        need = self.yr['cost'][idx] + self.need_frac(k['y'][idx]) * self.cw[np.clip(age, 0, 40)]
        afford = need <= cash
        wedges = np.full(self.nlev, np.nan)
        for m in range(self.nlev):
            if self.closed[m]:
                continue
            grp = np.flatnonzero(started & (lev == m))
            if len(grp) == 0:
                continue
            Ym = Y + int(np.median(self.ends[m] - g[grp])) + 4          # when this group's completion will be measured
            Cm = self._target(m, Ym)
            if Cm is None:
                continue
            Cprev = p['entry_share'] if m == 0 else self._target(m - 1, Ym - self.p['levels'][m][1])
            if Cprev is None:
                Cprev = p['entry_share']
            n_m = self.p['levels'][m][1]
            q = min(1.0, (max(Cm, 1e-4) / max(Cprev, 1e-4)) ** (1 / n_m) / max(self.pass_rate[m], 0.05) ** (1 / n_m))
            n_go = int(round(q * len(grp)))
            score = net[grp] + p['tau'] * r.logistic(size=len(grp))
            score = np.where(afford[grp], score, -np.inf)               # cash first: who cannot pay cannot stay
            order = np.argsort(-score)
            chosen = order[:n_go]
            chosen = chosen[np.isfinite(score[chosen])]
            go[grp] = False
            go[grp[chosen]] = True
            if 0 < len(chosen) < len(grp):
                wedges[m] = -float(score[order[len(chosen) - 1]])          # implied wedge: value the marginal stayer needed
        self.note(implied_wedge=wedges)
        return go

    def need_frac(self, y):
        """Share of a child's potential earnings the household must replace if the child stays in school."""
        p = self.p
        if p['need_mode'] == 'constant':
            return np.full(np.shape(y), p['need_share'])
        z = (p['poverty_line'] - y) / (p['need_width'] * p['poverty_line'])
        return p['need_max'] / (1 + np.exp(-np.clip(z, -30, 30)))

    def mvl_all(self, t):
        """Marginal value of learning for every child attending this year (cached per year)."""
        if 'mvl' not in self.yr:
            k = self.kids
            m = np.zeros(len(k['y']))
            idx = np.flatnonzero(k['att'])
            if len(idx):
                m[idx] = self.mvl(t, idx)
            self.yr['mvl'] = m
        return self.yr['mvl']

    def mvl(self, t, idx):
        """Marginal value of one grade-equivalent of learning (finite difference through the gates)."""
        k = self.kids
        _, c0 = self.values(t, idx=idx)
        _, c1 = self.values(t, L=k['L'][idx] + 0.5, idx=idx)
        return np.maximum((c1 - c0) / 0.5, 0.0)

    # ------------------------------------------------------------------ one year
    def year(self, t):
        return self.p['start_year'] + t

    def apply_calendar(self, t):
        p, Y = self.p, self.year(t)
        for name, path in p['paths'].items():
            p[name] = interp_path(path, Y)
        for ev in p['events']:
            if ev['year'] == Y:
                p.update(ev['set'])
                self.event_log.append((Y, ev.get('label', ''), dict(ev['set'])))
        if p['level_open']:
            self.closed = [bool(lo is not None and interp_path(lo, Y) < 0.5) for lo in p['level_open']]

    def step(self, t):
        p, r = self.p, self.rng
        self.apply_calendar(t)
        self.add_cohort(t)
        k = self.kids
        n = len(k['y'])
        self.yr = dict(cost=np.zeros(n), quality=np.full(n, p['q0']), withheld=np.zeros(n), tut_gain=np.zeros(n),
                       buyback=np.zeros(n, bool), extra_spend=np.zeros(n), cct=np.zeros(n), tut_kind=np.zeros(n, int))
        for m in self.modules:
            m.supply(self, t)
        age = self.age(t)
        # rural distance cost beyond primary
        self.yr['cost'] += np.where(~k['urban'] & (k['g'] >= 6), p['rural_cost'], 0.0)
        # ---- continue / enter
        alive = k['reason'] < 0
        eligible = alive & (k['started'] | (age >= p['entry_age']))
        idx = np.flatnonzero(eligible)
        V_stop, V_cont = self.values(t, idx=idx)
        net = V_cont - V_stop
        anchoring = bool(p['enrol_targets']) and (p['anchor_stop'] is None or self.year(t) < p['anchor_stop'])
        if p['enrol_targets'] and not anchoring:
            if self.frozen is None:                   # the wedge the data needed in the last 5 anchored years, held fixed
                W = np.array(self.R.get('implied_wedge', [])[-5:], float)
                self.frozen = np.nan_to_num(np.nanmean(W, 0)) if len(W) else np.zeros(self.nlev)
            net = net + self.frozen[np.minimum(k['cred'][idx], self.nlev - 1)]
            self.note(implied_wedge=self.frozen.copy())
        pr = 1 / (1 + np.exp(-np.clip(net / p['tau'], -30, 30)))
        go = r.random(len(idx)) < pr
        self._shock_now = np.zeros(n); self._shock_now[idx] = r.standard_normal(len(idx))
        if anchoring:
            go = self.anchored_choice(t, idx, net, go)
        # liquidity: this year's cost must be payable from this year's cash
        cash = np.maximum(k['y'][idx] * np.exp(p['shock_sigma'] * self._shock_now[idx]) - p['subsist'], 0) \
            + p['borrow'] * k['y'][idx] + self.yr['cct'][idx]
        need = self.yr['cost'][idx] + self.need_frac(k['y'][idx]) * self.cw[np.clip(age[idx], 0, 40)]
        broke = go & (need > cash)
        att = np.zeros(n, bool)
        att[idx[go & ~broke]] = True
        # exits: started children who stop; never-starters past max entry age
        started = k['started']
        stop = np.zeros(n, bool)
        stop[idx[~go & started[idx]]] = True
        stop[idx[broke & started[idx]]] = True
        k['reason'][idx[broke & started[idx]]] = 1          # liquidity
        k['reason'][idx[~go & started[idx]]] = 0            # choice
        never = alive & ~k['started'] & ~att & (age >= p['max_entry_age'])
        k['reason'][never] = 4
        k['reason'][stop & (k['reason'] < 0)] = 0
        k['started'] |= att
        k['att'] = att
        self._cash = np.zeros(n); self._cash[idx] = cash - np.where(go, need, 0)
        # ---- sector choice and rationing, extras (tutoring)
        for m in self.modules:
            m.sector(self, t)
        att = k['att']
        for m in self.modules:
            m.extras(self, t)
        # ---- learning
        y = self.yr
        eff = y['quality'] * (1 - np.where(y['buyback'], 0.0, y['withheld'])) * np.where(k['voc'], p['voc_quality'], 1.0)
        dL = eff * np.exp(p['beta_a'] * k['a']) + y['tut_gain'] + p['home_effect'] * (k['home'] - 0.5) \
            + p['learn_noise'] * r.standard_normal(n)
        dL = np.where(att, np.maximum(dL, 0.0), 0.0)
        k['L'] += dL
        if att.any():
            self.lrate = 0.8 * self.lrate + 0.2 * float(np.mean((dL[att]) / np.exp(p['beta_a'] * k['a'][att])))
        k['spend'] += np.where(att, y['cost'] + y['extra_spend'], 0.0)
        # ---- progression: promotion (repetition if learning lags the grade), then gates
        new_in_grade = att & (k['gtimes'] == 0)        # first year in this grade (for gross intake ratios)
        self.R.setdefault('new_by_grade', []).append(np.bincount(k['g'][new_in_grade], minlength=self.ends[-1] + 2)[:self.ends[-1] + 1])
        # attendance by grade, indexed like tutoring and private counts: index j = pupils studying grade j+1 this year
        # (recorded before promotion; v0.3 fix: it was recorded after promotion, one grade off from the numerators)
        self.R.setdefault('att_by_grade', []).append(np.bincount(k['g'][att], minlength=self.ends[-1] + 2)[:self.ends[-1] + 1])
        if p['promote_bar'] > 0:
            promote = att & ((k['L'] + 0.5 * r.standard_normal(n)) >= p['promote_bar'] * (k['g'] + 1))
        else:
            promote = att.copy()
        k['repeats'][att & ~promote] += 1
        k['gtimes'][att & ~promote] += 1
        k['gtimes'][promote] = 0
        k['g'][promote] += 1
        gated = np.zeros(n, bool)                        # each child meets at most one gate per year
        for m_ in range(self.nlev):
            at_gate = promote & ~gated & (k['g'] == self.ends[m_])
            gated |= at_gate
            if not at_gate.any():
                continue
            if self.ends[m_] == 6: k['L6'][at_gate] = k['L'][at_gate]
            if self.ends[m_] == 9: k['L9'][at_gate] = k['L'][at_gate]
            gate = p['gates'][m_]
            score = k['L'] + p['exam_sd'] * r.standard_normal(n)
            if gate['kind'] == 'bar':
                ok = score >= gate['bar']
            else:   # quota: seats = share x cohort size (as zhongkao/gaokao places are planned); cutoff -> next year's belief
                # (fixed 1 Nov after the first run: a share of *takers* let selective dropout ratchet the cutoff upward)
                s = np.sort(score[at_gate])[::-1]
                seats = int(round(gate['share'] * p['N']))
                c = s[seats - 1] if len(s) > seats else (s[-1] if len(s) else self.cut[m_])
                self.cut[m_] = 0.7 * self.cut[m_] + 0.3 * c
                ok = score >= c
            if gate.get('academic_only'):
                ok = ok & ~k['voc']
            if gate.get('fail') == 'track':            # failers continue on a vocational track (e.g. zhongkao)
                tracked = at_gate & ~ok
                k['voc'][tracked] = True
                ok = ok | tracked
            passed = at_gate & ok
            self.pass_rate[m_] = 0.8 * self.pass_rate[m_] + 0.2 * passed.sum() / max(at_gate.sum(), 1)
            k['cred'][passed] = m_ + 1
            k['comp_age'][passed, m_] = age[passed]
            for c_, nn in zip(*np.unique(k['cohort'][passed], return_counts=True)):
                self.comp_count.setdefault(int(c_), np.zeros(self.nlev))[m_] += nn
            nxt = m_ + 1
            while nxt < self.nlev and self.closed[nxt] and passed.any():   # skipped stage: awarded on passing the one below
                k['cred'][passed] = nxt + 1
                k['comp_age'][passed, nxt] = age[passed]
                k['g'][passed] = self.ends[nxt]
                for c_, nn in zip(*np.unique(k['cohort'][passed], return_counts=True)):
                    self.comp_count.setdefault(int(c_), np.zeros(self.nlev))[nxt] += nn
                nxt += 1
            adm = gate.get('admit')
            if adm and passed.any() and m_ + 1 < self.nlev:   # admission quota to the next level (e.g. gaokao)
                cand = passed & (~k['voc'] if adm.get('academic_only') else True)
                ci = np.flatnonzero(cand)
                seats = int(round(adm['share'] * p['N']))
                if len(ci) > seats:
                    sc = score[ci] + p['exam_sd'] * r.standard_normal(len(ci)) * 0.5
                    order = ci[np.argsort(-sc)]
                    cutv = sc[np.argsort(-sc)][seats - 1]
                    self.cut_adm[m_] = 0.7 * self.cut_adm[m_] + 0.3 * float(cutv)
                    refused = np.zeros(n, bool); refused[order[seats:]] = True
                else:
                    refused = np.zeros(n, bool)
                refused |= passed & ~cand                     # vocational track: no academic admission
                k['reason'][refused & (k['reason'] < 0)] = 6  # leave with the credential just earned
            failed = at_gate & ~ok
            retake = failed & (k['retakes'] < p['gate_retakes'])
            k['retakes'][retake] += 1
            k['g'][retake] -= 1                          # repeat the final grade and sit the exam again next year
            k['gtimes'][retake] = 1
            k['reason'][failed & ~retake] = 2
        finished = att & (k['cred'] >= self.nlev)
        k['reason'][finished & (k['reason'] < 0)] = 3
        # ---- census for out-of-school rates (all children of a cohort, enrolled or not)
        for c_ in np.unique(k['cohort']):
            sel = k['cohort'] == c_
            a_ = t - c_ + p['entry_age']
            self.census[(c_, a_)] = int(att[sel].sum())
        # ---- labour market for leavers
        ex = np.flatnonzero(k['reason'] >= 0)
        if len(ex):   # street state: urban, young, poor leavers without a kin network to absorb them
            young = (age[ex] < p['street_age']) & k['urban'][ex] & (k['y'][ex] < p['y_median'] * p['urban_income'])
            k['street'][ex] = young & (r.random(len(ex)) >= p['kin_support'])
        inc = None
        if self.labour_module:
            inc = self.labour_module[0].labour(self, t, ex)
        if inc is None:          # no labour module: Mincer-style fixed returns
            inc = np.exp(0.08 * k['g'][ex] + 0.05 * (k['L'][ex] - k['g'][ex]))
        self.update_beliefs(ex, inc)
        self.leaver_income = inc
        for m in self.modules:
            m.after(self, t)
        for m in self.modules:
            m.measure(self, t)
        self.record(t, ex, inc)
        if len(ex):
            self.exits.append({kk: (v[ex] if v.ndim == 1 else v[ex]) for kk, v in k.items()})
            self.exits[-1]['inc'] = inc; self.exits[-1]['exit_year'] = np.full(len(ex), t)
            keep = k['reason'] < 0
            self.kids = {kk: v[keep] for kk, v in k.items()}

    def update_beliefs(self, ex, inc):
        if len(ex) == 0:
            return
        self.observe(self.kids['cred'][ex], inc)

    def observe(self, c, inc):
        """Update beliefs from realised incomes (NaN = not yet working, e.g. queuing graduates)."""
        ok = np.isfinite(inc)
        c, inc = c[ok], inc[ok]
        if len(c) == 0:
            return
        lw = np.log(np.maximum(inc, 1e-3))
        d = self.p['belief_decay']
        for j in range(self.nlev + 1):
            s = c == j
            if s.sum() >= 5:
                w = s.sum()
                self.B[j] = (d * self.Bn[j] * self.B[j] + w * lw[s].mean()) / (d * self.Bn[j] + w)
                self.Bn[j] = d * self.Bn[j] + w
        # credentials with few recent holders are valued at the prior premium over the next credential down (fixed 1 Nov:
        # otherwise a never-observed level looks worthless and nobody ever tries it - the cold-start trap the triad model hit)
        prior = np.array(self.p['prior_logw'], float)
        for j in range(1, self.nlev + 1):
            if self.p['belief_floor'] and self.Bn[j] < 20:
                self.B[j] = max(self.B[j], self.B[j - 1] + prior[j] - prior[j - 1])

    def record(self, t, ex, inc):
        R, k = self.R, self.kids
        R['year'].append(t)
        att = k['att']
        R.setdefault('enrolled', []).append(int(att.sum()))
        R.setdefault('beliefs', []).append(self.B.copy())
        R.setdefault('lrate', []).append(self.lrate)
        # every yearly series stays aligned with R['year']: a module that has nothing to report in a year (e.g. the
        # labour market before the first leavers) gets a NaN of the right shape, so R[key][t] is always calendar year t.
        # (Fixed 1 Nov 2026: unpadded series were shifted, e.g. China's labour series ran 3 years ahead.)
        n = len(R['year'])
        nanlike = lambda v: np.full(np.shape(v), np.nan) if np.ndim(v) else np.nan
        rec = getattr(self, 'yr_record', {})
        for key, v in rec.items():
            lst = R.setdefault(key, [])
            while len(lst) < n - 1:
                lst.append(nanlike(v))
            lst.append(v)
        for key, lst in R.items():
            if key not in rec and key not in ('year', 'enrolled', 'beliefs', 'lrate') and len(lst) < n:
                lst.append(nanlike(lst[-1]))
        self.yr_record = {}

    def note(self, **kv):
        """Modules call this to add yearly series."""
        if not hasattr(self, 'yr_record'):
            self.yr_record = {}
        self.yr_record.update(kv)

    def run(self):
        for t in range(self.p['T']):
            self.step(t)
        self.X = {kk: np.concatenate([e[kk] for e in self.exits]) for kk in self.exits[0]} if self.exits else {}
        # everyone ever born in the run (exited + still in school), for calendar-year indicator series
        k = self.kids
        rest = {kk: v for kk, v in k.items()}
        rest['inc'] = np.full(len(k['y']), np.nan); rest['exit_year'] = np.full(len(k['y']), -1)
        self.ALL = {kk: np.concatenate([self.X[kk], rest[kk]]) for kk in self.X} if self.X else rest
        out = {}
        for m in self.modules:
            out.update(m.summary(self))
        return out
