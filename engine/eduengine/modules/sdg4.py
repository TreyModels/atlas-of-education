"""UNESCO SDG 4 indicators computed from the simulated cohorts (definitions as in ../../sdg4/indicators.py).

4.1.2 completion: share of a cohort that completed the last grade of a level by 5 years after its intended age.
4.1.4 out-of-school: person-years at official ages not enrolled (never-enrolled children counted).
4.1.1 minimum proficiency: share of pupils reaching the end of primary (lower secondary) at or above a threshold on the
      engine's absolute learning scale. The thresholds are an ASSUMED anchor (grade-equivalents), not SEA-PLM/PISA.
Learning poverty (World Bank/UIS): 1 - (1 - OOS primary) x share proficient at end of primary.
4.5.1 parity: adjusted parity index, poorest/richest fifth and rural/urban.
"""
import numpy as np
from ..core import Module


def parity(d, a):
    if not a or not np.isfinite(a) or a <= 0 or not np.isfinite(d):
        return float('nan')
    r = d / a
    return float(r if r <= 1 else 2 - 1 / r)


class SDG4(Module):
    name = 'sdg4'
    defaults = {}

    def summary(self, E):
        p, X = E.p, E.X
        if not X:
            return {}
        last_cohort = p['T'] - 26                     # cohorts old enough to have finished tertiary age windows
        sel = (X['cohort'] >= p['measure_from']) & (X['cohort'] <= last_cohort)
        out = {}
        names = [n for n, _ in p['levels']]
        for m_, nm in enumerate(names):
            intended = p['entry_age'] + E.ends[m_] - 1
            done = np.isfinite(X['comp_age'][:, m_]) & (X['comp_age'][:, m_] <= intended + 5)
            out[f'completion_{nm}'] = float(done[sel].mean())
            q, u = X['q'][sel], X['urban'][sel]
            d = done[sel]
            out[f'completion_{nm}_q'] = [float(d[q == j].mean()) for j in range(5)]
            out[f'parity_wealth_{nm}'] = parity(d[q == 0].mean(), d[q == 4].mean())
            out[f'parity_location_{nm}'] = parity(d[~u].mean(), d[u].mean())
        # out-of-school by official age band
        cohorts = range(p['measure_from'], last_cohort + 1)
        bands = dict(primary=(6, 11), lower=(12, 14), upper=(15, 17))
        for nm, (a0, a1) in bands.items():
            vals = [1 - E.census.get((c, a), 0) / p['N'] for c in cohorts for a in range(a0, a1 + 1)]
            out[f'oos_{nm}'] = float(np.mean(vals))
        L6 = X['L6'][sel]; L9 = X['L9'][sel]
        r6 = np.isfinite(L6); r9 = np.isfinite(L9)
        out['mpl_primary'] = float(np.mean(L6[r6] >= p['mpl_primary'])) if r6.any() else float('nan')
        out['mpl_lower'] = float(np.mean(L9[r9] >= p['mpl_lower'])) if r9.any() else float('nan')
        q = X['q'][sel]
        mq = [float(np.mean(L6[r6 & (q == j)] >= p['mpl_primary'])) if (r6 & (q == j)).any() else np.nan for j in range(5)]
        out['mpl_primary_q'] = mq
        out['parity_wealth_mpl'] = parity(mq[0], mq[4])
        out['learning_poverty'] = float(1 - (1 - out['oos_primary']) * out['mpl_primary'])
        out['mean_years'] = float(X['g'][sel].mean())
        # spending: household vs public (per year, measured window)
        R, m = E.R, p['measure_from']
        hh = float(np.mean(R['hh_spend'][m:])) if 'hh_spend' in R else 0.0
        pub = float(np.mean(R['pub_spend'][m:])) if 'pub_spend' in R else 0.0
        out['household_share_spending'] = hh / max(hh + pub, 1e-9)
        reasons = X['reason'][sel]
        st = X['g'][sel] > 0
        out['exit_reasons'] = {nm: float(np.mean(reasons[st] == i)) for i, nm in
                               enumerate(['choice', 'liquidity', 'gate_fail', 'finished', 'never_enrolled', 'no_seat', 'not_admitted'])}
        out['never_enrolled'] = float(np.mean(reasons == 4))
        return out

    def measure(self, E, t):
        k, y = E.kids, E.yr
        att = k['att']
        E.note(hh_spend=float((y['cost'][att] + y['extra_spend'][att]).sum()))
