#!/usr/bin/env python3
"""Model 2: the zhongkao gate. DEMONSTRATION model, illustrative parameters, not calibrated.

Idea (user, 2026-11-26): the elite competition is mostly at zhongkao (end of compulsory schooling), and that is
exactly where the 2021 'double reduction' crackdown on tutoring is hardest. The state's expectation is that the H
families believe is needed is delivered by schools. Junior schools are assigned by residence and are unequal (richer
neighbourhoods have schools that supply more H), but the claim is that school-delivered H still evens out equity
compared with a private market.

Mechanics per pupil:
  neighbourhood wealth -> junior school (residence) -> school H = H_base + A * (1 + g * school_wealth_z)
  gap = H_star - school H;  private H bought only if a seller exists (prob 1 - k), affordable at the
  underground price firm_price / (1 - 0.8 k), and >= MIN_PACKAGE (window not binding for day pupils).
  score = ability + beta * learn(total H) + noise;  top SEAT_SHARE go to elite (boarding, exam-admitted) high schools.
  Peer escalation: H_star = H_gate + RHO_PEER * (mean school H - H_base)  (the arms race the Lean model flagged).

Key question: with crackdown k and absorption A, is the wealth gradient of elite admission flatter than under an open
market, even though schools are unequal (g > 0)? And at what g does the advantage vanish?
Usage: python hflow_m2.py
"""
import numpy as np

P = dict(n=20000, n_schools=100, H_base=4.0, H_gate=12.0, A=0.0, g=0.0, k=0.0, RHO_PEER=0.0,
         firm_price=1.0, BUDGET_SHARE=0.08, MIN_PACKAGE=2.0, beta=0.08, SEAT_SHARE=0.3,
         ABILITY_WEALTH=0.3, SEG=0.7,
         eta=0.0, tau=0.0, TRACK_SHARE=0.3, w_low=1.0, w_high=1.0, quota=0.0)
# eta: H's marginal product scales with (1 + eta*ability) (dossier rec 2)
# tau: within-school tracking; top TRACK_SHARE by ability get A*(1+tau), others less (mean-preserving) (rec 1)
# w_low/w_high: effectiveness of bought H in the weakest/strongest school (substitute at bottom, status good at top) (rec 3)
# quota: share of elite seats allocated to each school's own top pupils (zhibiao dao xiao) (rec 4)


def simulate(p=None, seed=0, **kw):
    p = {**P, **(p or {}), **kw}
    rng = np.random.default_rng(seed)
    n, S = p['n'], p['n_schools']
    school_w = rng.normal(size=S)                                   # neighbourhood wealth level
    school = rng.integers(0, S, size=n)
    logw = p['SEG'] * school_w[school] + np.sqrt(1 - p['SEG'] ** 2) * rng.normal(size=n)  # residential segregation
    ability = p['ABILITY_WEALTH'] * logw + np.sqrt(1 - p['ABILITY_WEALTH'] ** 2) * rng.normal(size=n)
    wealth = np.exp(0.8 * logw)
    wq = np.searchsorted(np.quantile(wealth, [.2, .4, .6, .8]), wealth)

    sz = (school_w - school_w.mean()) / school_w.std()
    A_s = p['A'] * np.clip(1 + p['g'] * sz, 0, None)                         # unequal schools when g > 0
    rank = np.zeros(n)
    for j in range(S):
        m = school == j
        if m.any():
            rank[m] = ability[m].argsort().argsort() / max(m.sum() - 1, 1)
    top = rank >= 1 - p['TRACK_SHARE']
    ts = p['TRACK_SHARE']
    mult = np.where(top, 1 + p['tau'], 1 - p['tau'] * ts / (1 - ts))
    H_school = p['H_base'] + A_s[school] * np.clip(mult, 0, None)
    H_star = p['H_gate'] + p['RHO_PEER'] * (H_school.mean() - p['H_base'])
    gap = np.maximum(H_star - H_school, 0)

    k = p['k']
    price = p['firm_price'] / (1 - 0.8 * k)
    seller = rng.random(n) < (1 - k)
    afford = p['BUDGET_SHARE'] * wealth * 40 / price
    T = np.where(seller, np.minimum(gap, afford), 0.0)
    T = np.where(T >= p['MIN_PACKAGE'], T, 0.0)
    H_tot = H_school + T
    q01 = (sz[school] - sz.min()) / (sz.max() - sz.min())
    w = p['w_low'] + (p['w_high'] - p['w_low']) * q01                     # effectiveness of bought H
    H_eff = H_school + w * T

    eff_beta = p['beta'] * np.clip(1 + p['eta'] * ability, 0, None)
    score = ability + eff_beta * np.sqrt(H_eff) * 4 + 0.5 * rng.normal(size=n)
    seats = int(round(p['SEAT_SHARE'] * n)); elite = np.zeros(n, bool)
    if p['quota'] > 0:
        for j in range(S):
            idx = np.flatnonzero(school == j)
            kq = int(round(p['quota'] * p['SEAT_SHARE'] * idx.size))
            if kq: elite[idx[np.argsort(-score[idx])[:kq]]] = True
    rest = np.flatnonzero(~elite); left = seats - elite.sum()
    elite[rest[np.argsort(-score[rest])[:left]]] = True
    adm = np.array([elite[wq == q].mean() for q in range(5)])
    slope = lambda y: np.polyfit(logw, y, 1)[0]
    _ex=dict(_score=score,_ab=ability,_lw=logw,_el=elite)
    return dict(_ex=_ex, part=100 * (T > 0).mean(), part_Q1=100 * (T[wq == 0] > 0).mean(), part_Q5=100 * (T[wq == 4] > 0).mean(),
                H_school=H_school.mean(), T=T.mean(), unmet=np.maximum(H_star - H_tot, 0).mean(), H_star=H_star,
                slope_school=slope(H_school), slope_priv=slope(T), slope_total=slope(H_tot),
                adm_Q5_Q1=adm[4] / max(adm[0], 1e-9), gini_H=float(np.abs(H_tot[:, None][:2000] - H_tot[None, :2000]).mean() / (2 * H_tot[:2000].mean())), elite_from_Q1=100 * (elite & (wq == 0)).sum() / elite.sum())


REGIMES = {
    'open market':           dict(A=0.0, k=0.0),
    'crackdown only':        dict(A=0.0, k=0.9),
    'absorb + crackdown':    dict(A=6.0, k=0.9),
    'absorb, open market':   dict(A=6.0, k=0.0),
}


def mean_runs(p, seeds=range(5)):
    rs = [simulate(p, s) for s in seeds]
    return {key: float(np.mean([r[key] for r in rs])) for key in rs[0]}


def main():
    cols = ['part', 'part_Q1', 'part_Q5', 'H_school', 'T', 'unmet', 'slope_school', 'slope_priv', 'slope_total',
            'adm_Q5_Q1', 'elite_from_Q1']
    print('Model 2 (zhongkao gate). ILLUSTRATIVE. slope_* = gradient of hours on log wealth.')
    for g in (0.0, 0.3):
        print(f'\n-- school inequality g = {g} --')
        print(f"{'regime':22s}" + ''.join(f'{c[:12]:>13s}' for c in cols))
        for name, r in REGIMES.items():
            m = mean_runs(dict(r, g=g))
            print(f'{name:22s}' + ''.join(f'{m[c]:13.2f}' for c in cols))
    print('\n-- break-even school inequality: absorb+crackdown vs open market, admission Q5/Q1 --')
    base = mean_runs(REGIMES['open market'])['adm_Q5_Q1']
    for g in (0, .25, .5, .75, 1.0, 1.5, 2.0):
        m = mean_runs(dict(REGIMES['absorb + crackdown'], g=g))
        print(f'g={g:4.2f}  absorb+crackdown {m["adm_Q5_Q1"]:.2f}  vs open market {base:.2f}  '
              f'slope_total {m["slope_total"]:.2f}')
    print('\n-- peer escalation (RHO_PEER) under absorb+crackdown, g=0.3 --')
    for rho in (0, .5, 1.0):
        m = mean_runs(dict(REGIMES['absorb + crackdown'], g=0.3, RHO_PEER=rho))
        print(f'rho={rho:.1f}  H_star {m["H_star"]:.1f}  part {m["part"]:.1f}%  unmet {m["unmet"]:.2f}  '
              f'adm Q5/Q1 {m["adm_Q5_Q1"]:.2f}')


if __name__ == '__main__':
    main()
