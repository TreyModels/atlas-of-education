"""Labour-market modules: the demand pull. Exactly one is used per run.

QueueLabour      job competition with credential floors (Thurow 1975; Fields 1974; Bhagwati & Srinivasan 1977),
                 a noisy signal (Spence 1973; Arrow 1973), informality (Harris & Todaro 1970), and formal jobs that
                 can respond to the educated workforce (Acemoglu 1998 directed technical change; Moretti 2004).
CompetitiveLabour the rival: wages clear a CES market for skills (Tinbergen 1974; Katz & Murphy 1992; Goldin & Katz 2008).
"""
import numpy as np
from ..core import Module


class _Stock:
    """Earnings stock: each year's entrants keep their entry income for `work_life` years (no wage growth)."""
    def __init__(self, work_life):
        self.L = work_life; self.flows = []

    def add(self, formal, informal):
        self.flows.append((formal, informal))

    def bill(self):
        f = sum(a for a, _ in self.flows[-self.L:]); i = sum(b for _, b in self.flows[-self.L:])
        return f, i


class QueueLabour(Module):
    name = 'queue_labour'
    defaults = dict(
        vac0=0.10, vac_growth=0.012,          # formal vacancies per labour-market entrant at t=0; growth per year
        skilled_share=0.3,                     # share of formal vacancies in the skilled tier
        w_skilled=3.0, w_routine=1.8, w_informal=1.0,
        theta_L=0.06, theta_L_inf=0.02,        # log-wage per grade-equivalent of learning (the gray box)
        signal_rho=0.4,                        # weight of the noisy learning signal in employers' ranking
        floor_adapt=True, floor0=(3, 1), screen_kappa=4.0, floor_p=0.3,
        job_elasticity=0.0, job_ref_year=25, job_window=15,   # formal jobs x (educated share / ref)^elasticity
        work_life=40,
        # graduate queue (v0.2): unhired leavers with a high credential may wait for a formal job instead of taking informal
        # work, if their family can support them (Harris & Todaro 1970; Fields 1975). Waiting = youth unemployment.
        queue_on=False, queue_min_cred=3, queue_max_years=3, queue_support=1.2, queue_horizon=8.0, queue_k=3.0,
        # which tiers are ranked contests (the positional race). Trey's null hypothesis: only the scarce skilled tier
        # (university / civil-service jobs) is ranked; routine formal jobs take any eligible applicant (floor + lottery)
        rank_routine=True, street_wage=0.7,
        # the tutoring industry as a graduate employer (v0.3): commercial tutoring revenue pays tutors, who are recruited
        # from degree holders. Positions = labour share x revenue / routine wage; openings = turnover + growth. When a ban
        # shrinks the industry, displaced tutors re-enter the job queue. This ties the two ends of the pipeline together.
        tutor_jobs=True, tutor_labour_share=0.6, tutor_turnover=0.25, tutor_min_cred=4,
    )

    def setup(self, E):
        p = E.p
        self.floor = list(p['floor0'])
        self.stock = _Stock(p['work_life'])
        self.edu_hist = []
        self.ref = None
        E.bill = (0.0, 0.0)
        self.Q = None                       # queue: dict of arrays cred, L, y, wait
        self.p_hire_q = {}                  # believed chance a queuer of credential c is hired this year
        self.young = []                     # recent entrants into work, for the youth unemployment denominator
        self.tutors = 0.0                   # tutoring-industry positions (stock)

    def vacancies(self, E, t):
        p = E.p
        v = p['vac0'] * (1 + p['vac_growth']) ** t
        if p['job_elasticity'] > 0 and len(self.edu_hist) > p['job_window']:
            cur = np.mean(self.edu_hist[-p['job_window']:])
            if t >= p['job_ref_year'] and self.ref is None:
                self.ref = cur
            if self.ref:
                v *= (max(cur, 1e-3) / self.ref) ** p['job_elasticity']
        return min(v, 0.95)

    def labour(self, E, t, ex):
        p, r, k = E.p, E.rng, E.kids
        n = len(ex)
        # applicants = this year's leavers + anyone queuing from earlier years
        cred = k['cred'][ex].astype(int); L = k['L'][ex].astype(float); y = k['y'][ex].astype(float)
        pid = k['pid'][ex].astype(np.int64)
        elite_prize = k['elite_prize'][ex].astype(float)
        track = np.asarray(k['track'][ex], int)
        nq = 0 if self.Q is None else len(self.Q['cred'])
        if nq:
            cred = np.concatenate([cred, self.Q['cred']]); L = np.concatenate([L, self.Q['L']])
            y = np.concatenate([y, self.Q['y']]); pid = np.concatenate([pid, self.Q['pid']])
            elite_prize = np.concatenate([elite_prize, self.Q['elite_prize']])
            track = np.concatenate([track, self.Q['track']])
        wait = np.concatenate([np.zeros(n), self.Q['wait'] if nq else np.zeros(0)])
        m = n + nq
        inc = np.full(m, np.nan)
        if m == 0:
            self.stock.add(0.0, 0.0); E.bill = self.stock.bill(); return np.zeros(0)
        zL = (L - L.mean()) / (L.std() + 1e-9)
        # event-keyed signal noise (contract §7): a person's signal does not depend on who else applied
        sig = cred + p['signal_rho'] * (zL + r.normal(t, 'labour_signal', pid)) - 0.15 * wait
        V = p['N'] * self.vacancies(E, t)
        Vs, Vr = int(round(V * p['skilled_share'])), int(round(V * (1 - p['skilled_share'])))
        tier = np.zeros(m, int)                 # 0 informal / waiting, 1 routine, 2 skilled
        order = np.argsort(sig)[::-1]
        lottery = np.argsort(r.uniform(t, 'labour_lottery', pid), kind='stable')   # per-pid U replaces r.permutation
        for vac, j in [(Vs, 0), (Vr, 1)]:
            o_ = order if (j == 0 or p['rank_routine']) else lottery
            elig = o_[(tier[o_] == 0) & (cred[o_] >= self.floor[j])]
            hire = elig[:vac]
            tier[hire] = 2 - j
            if p['floor_adapt'] and float(r.uniform(t, 'labour_floor', -1)) < p['floor_p']:
                up = np.count_nonzero((tier == 0) & (cred >= self.floor[j] + 1)) + len(hire)
                if len(elig) > p['screen_kappa'] * max(vac, 1) and up >= 1.5 * vac and self.floor[j] < E.nlev:
                    self.floor[j] += 1
                elif len(elig) < vac and self.floor[j] > 0:
                    self.floor[j] -= 1
        # tutoring-industry openings, filled after the formal tiers from the best remaining degree holders (routine wage)
        Vt, displaced = 0, 0
        if p['tutor_jobs'] and E.R.get('firm_rev'):
            stock = p['tutor_labour_share'] * E.R['firm_rev'][-1] / p['w_routine']
            Vt = int(round(p['tutor_turnover'] * self.tutors + max(0.0, stock - self.tutors)))
            displaced = int(round(max(0.0, self.tutors - stock)))
            self.tutors = stock
            elig = order[(tier[order] == 0) & (cred[order] >= p['tutor_min_cred'])]
            tier[elig[:Vt]] = 1
        wf = lambda tr: np.where(tr == 2, p['w_skilled'], p['w_routine']) * np.exp(p['theta_L'] * (L - 9))
        winf = p['w_informal'] * np.exp(p['theta_L_inf'] * (L - 9))
        st = np.concatenate([k['street'][ex], np.zeros(nq, bool)])
        winf = np.where(st, winf * p['street_wage'], winf)
        inc = np.where(tier > 0, wf(tier), np.nan)
        # queue decision for the unhired
        unh = tier == 0
        queue = np.zeros(m, bool)
        if p['queue_on']:
            for c in np.unique(cred[unh & (cred >= p['queue_min_cred'])]):
                was = (cred == c) & (wait > 0)
                if was.any():
                    h = float(np.mean(tier[was] > 0))
                    self.p_hire_q[c] = 0.7 * self.p_hire_q.get(c, h) + 0.3 * h
            ph = np.array([self.p_hire_q.get(c, 0.3) for c in cred])
            gain = ph * (wf(np.ones(m, int)) - winf) * p['queue_horizon'] - winf          # expected gain of waiting a year
            pr = 1 / (1 + np.exp(-p['queue_k'] * gain / np.maximum(winf, 1e-3)))
            can = unh & (cred >= p['queue_min_cred']) & (wait < p['queue_max_years']) & (y >= p['queue_support'])
            queue = can & (r.uniform(t, 'queue_accept', pid) < pr)
        informal = unh & ~queue
        inc = np.where(informal, winf, inc)
        # ---- Gate-1 prizes (contract §8): applied LAST, multiplicatively, to every applicable income.
        # The direct elite-status premium (won prize, not a global parameter) and the persistent G9 track
        # earnings premium are kept separate from wage structure: they never enter tier assignment or queueing.
        base_inc = inc.copy()
        mult = np.exp(elite_prize)
        if getattr(E, 'track_effect', None):
            mult = mult * np.where(track == 1, np.exp(float(E.track_earnings_logw)), 1.0)
        inc = inc * mult
        if n:
            self._record_prize_audit(E, ex, elite_prize[:n], track[:n], base_inc[:n], inc[:n], mult[:n])
        # bookkeeping
        new_inc = inc[:n].copy()
        hired_q = np.flatnonzero(~np.isnan(inc[n:])) + n
        if len(hired_q):          # queuers who now have an income: beliefs learn the wait (discounted income)
            E.observe(cred[hired_q], inc[hired_q] * p.get('delta', 0.93) ** wait[hired_q])
        keepq = np.flatnonzero(queue)
        self.Q = (dict(cred=cred[keepq], L=L[keepq], y=y[keepq], wait=wait[keepq] + 1, pid=pid[keepq],
                       elite_prize=elite_prize[keepq], track=track[keepq]) if len(keepq) else None)
        if displaced and p['queue_on']:       # laid-off tutors (young degree holders) look for formal work next year
            dg = cred >= p['tutor_min_cred']
            add = dict(cred=np.full(displaced, p['tutor_min_cred']), L=np.full(displaced, float(L[dg].mean()) if dg.any() else float(L.mean())),
                       y=np.full(displaced, float(np.median(y))), wait=np.ones(displaced),
                       pid=-(t * 100000 + np.arange(displaced, dtype=np.int64) + 1),
                       elite_prize=np.zeros(displaced), track=np.full(displaced, -1, int))
            self.Q = add if self.Q is None else {kk: np.concatenate([self.Q[kk], add[kk]]) for kk in add}
            keepq = np.arange(len(self.Q['cred']))
        worked = ~np.isnan(inc)
        self.stock.add(float(inc[worked & (tier > 0)].sum()), float(inc[worked & (tier == 0)].sum()))
        E.bill = self.stock.bill()
        self.edu_hist.append(float(np.mean(cred[:n] >= 2)) if n else self.edu_hist[-1] if self.edu_hist else 0.0)
        self.young.append(int(worked.sum()))
        nqueue = len(keepq)
        youth_u = nqueue / max(nqueue + sum(self.young[-8:]), 1)
        grads = cred >= p['queue_min_cred']
        E.note(formal_rate=float(np.mean(tier[:n] > 0)) if n else 0.0, floor_skilled=self.floor[0], floor_routine=self.floor[1],
               vac=V / p['N'], queue=nqueue, youth_unemp=youth_u,
               tutor_jobs=self.tutors / p['N'], tutor_openings=Vt / p['N'], tutors_displaced=displaced / p['N'],
               grad_unemp=float(np.mean(queue[grads])) if grads.any() else 0.0,
               deg_queue=float(np.count_nonzero(queue & (cred >= p['tutor_min_cred']))) / p['N'],   # degree holders waiting, per cohort-size (v0.4)
               formal_by_cred=[float(np.mean(tier[:n][cred[:n] == c] > 0)) if (cred[:n] == c).any() else np.nan for c in range(E.nlev + 1)],
               inc_by_cred=[float(np.nanmean(inc[cred == c])) if ((cred == c) & worked).any() else np.nan for c in range(E.nlev + 1)])
        return new_inc

    @staticmethod
    def _record_prize_audit(E, ex, elite_prize, track, base_inc, inc_after, mult):
        """§8 audit series: the raw elite gap and its direct/composition decomposition (leavers only)."""
        elite = np.asarray(E.kids['elite'][ex], bool)
        fin = np.isfinite(inc_after)
        raw = np.nan
        if fin.any() and (elite & fin).any() and (~elite & fin).any():
            raw = float(np.nanmean(inc_after[elite & fin]) - np.nanmean(inc_after[~elite & fin]))
        direct = float(np.nanmean((mult - 1.0) * base_inc)) if fin.any() else np.nan
        composition = (raw - direct) if np.isfinite(raw) and np.isfinite(direct) else np.nan
        track1 = np.asarray(track) == 1
        E.note(elite_share=float(elite.mean()) if len(elite) else 0.0,
               elite_prize_mean=float(np.mean(elite_prize)) if len(elite_prize) else 0.0,
               track_share=float(track1.mean()) if len(track1) else 0.0,
               track_prize_mean=float(E.track_earnings_logw) if (track1.any() and getattr(E, 'track_effect', None)) else 0.0,
               elite_inc_gap_raw=raw, elite_inc_gap_direct=direct,
               elite_inc_gap_composition=composition)

    def summary(self, E):
        R = E.R; m = E.p['measure_from']
        sl = slice(m, None)
        fr = np.array(R['formal_by_cred'][sl], float)
        ic = np.array(R['inc_by_cred'][sl], float)
        return dict(formal_rate=float(np.mean(R['formal_rate'][sl])), youth_unemp=float(np.mean(R['youth_unemp'][sl])),
                    grad_unemp=float(np.mean(R['grad_unemp'][sl])),
                    formal_by_cred=list(np.nanmean(fr, 0)), inc_by_cred=list(np.nanmean(ic, 0)),
                    floor_skilled=float(np.mean(R['floor_skilled'][sl])), floor_routine=float(np.mean(R['floor_routine'][sl])))


class CompetitiveLabour(Module):
    name = 'competitive_labour'
    defaults = dict(
        demand0=0.15, demand_growth=0.012,     # relative demand for skilled (credential >= 3) labour, and its growth
        ces_sigma=1.6, wu0=1.2, theta_L=0.06, cred_step=0.08, work_life=40, skilled_cred=4,
    )

    def setup(self, E):
        self.S = None; self.stock = _Stock(E.p['work_life']); E.bill = (0.0, 0.0)

    def labour(self, E, t, ex):
        p, k = E.p, E.kids
        n = len(ex)
        if n == 0:
            self.stock.add(0.0, 0.0); E.bill = self.stock.bill(); return np.zeros(0)
        cred = k['cred'][ex]; L = k['L'][ex]
        sk = cred >= p['skilled_cred']                     # fixed 1 Nov: 'skilled' = degree by default (was upper secondary)
        sh = float(np.clip(sk.mean(), 0.01, 0.99))
        self.S = sh if self.S is None else 0.8 * self.S + 0.2 * sh
        D = p['demand0'] * (1 + p['demand_growth']) ** t
        rel = 2.0 * (D / self.S) ** (1 / p['ces_sigma'])     # skilled/unskilled wage ratio
        wu = p['wu0']; ws = wu * rel
        inc = np.where(sk, ws, wu) * np.exp(p['theta_L'] * (L - 9) + p['cred_step'] * cred)
        self.stock.add(float(inc[sk].sum()), float(inc[~sk].sum()))
        E.bill = self.stock.bill()
        E.note(skill_premium=rel,
               inc_by_cred=[float(np.mean(inc[cred == c])) if (cred == c).any() else np.nan for c in range(E.nlev + 1)])
        return inc

    def summary(self, E):
        m = E.p['measure_from']
        return dict(skill_premium=float(np.mean(E.R['skill_premium'][m:])),
                    inc_by_cred=list(np.nanmean(np.array(E.R['inc_by_cred'][m:], float), 0)))
