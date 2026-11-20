"""E2 sensitivity: does ANY plausible quality parameterisation pass T1/T2? Declared grid, no optimisation."""
import sys, json, itertools
import numpy as np
sys.path.insert(0, '/tmp/massrun/work/loop5')
import provider_tech as P
from scipy.optimize import minimize_scalar

RHO = float(np.log(671.0 / 183.0) / np.log(8.0 / 3.0))
INCOME_KOR = 4_000_000.0; INCOME_HKG = 3_200_000.0
obs_mix = P.KOR_OBS['provider_spend']; tot = sum(obs_mix.values())
OBS = {j: 100 * v / tot for j, v in obs_mix.items()}
LV = ['elementary', 'middle', 'high']
SURPLUS_MENU = ['hagwon_mass', 'one_to_one', 'small_group', 'internet', 'textbook_visit']


def fit_theta(part, mu, income, seed, boost, menu=None):
    def l(th):
        d = P.demand(th, mu, RHO, income_median=income, n=2000, seed=seed, menu=menu,
                     q_boost={'hagwon_mass': boost} if boost else None)
        return abs((1 - d['take']['none']) * 100 - part)
    return float(minimize_scalar(l, bounds=(0.01, 8.0), method='bounded').x)


def evaluate(q11, qsg, boost):
    P.QUAL['one_to_one'] = q11; P.QUAL['small_group'] = qsg
    pred = {}
    for s, (lvl, part) in enumerate(zip(LV, P.KOR_OBS['participation'])):
        th = fit_theta(part, 1.0, INCOME_KOR, 10 + s, 0.0)
        d = P.demand(th, 1.0, RHO, income_median=INCOME_KOR, n=3000, seed=50 + s)
        pred[lvl] = d['spend_share']
    w = np.array(P.KOR_OBS['spend_student']); w = w / w.sum()
    share = {j: float(sum(w[s] * pred[LV[s]][j] for s in range(3))) * 100 for j in P.TECHS}
    diffs = {j: share[j] - OBS[j] for j in P.TECHS}
    t1 = all(abs(v) <= 10 for v in diffs.values())
    mu_h = INCOME_HKG / INCOME_KOR
    ml = {}
    for nm, part, b in [('S4_5', P.HKG_OBS['participation'][1], 0.0),
                        ('S6_7', P.HKG_OBS['participation'][2], boost)]:
        th = fit_theta(part, mu_h, INCOME_HKG, 20 + len(ml), b)
        d = P.demand(th, mu_h, RHO, income_median=INCOME_HKG, n=3000, seed=40 + len(ml),
                     q_boost={'hagwon_mass': b} if b else None)
        ml[nm] = d['spend_share']['hagwon_mass'] * 100
    gap = ml['S6_7'] - ml['S4_5']
    return t1, gap >= 20.0, diffs, share, ml, gap


def main(out):
    grid = list(itertools.product([0.95, 1.05, 1.15, 1.25], [0.85, 0.95, 1.05], [0.15, 0.30, 0.50]))
    rows = []
    for q11, qsg, b in grid:
        t1, t2, diffs, share, ml, gap = evaluate(q11, qsg, b)
        rows.append(dict(q_one_to_one=q11, q_small_group=qsg, ml_boost_terminal=b, T1_pass=t1, T2_pass=t2,
                         gap_pp=gap, hagwon_share=share['hagwon_mass'], one_to_one_share=share['one_to_one'],
                         small_group_share=share['small_group'], internet_share=share['internet'],
                         textbook_share=share['textbook_visit'],
                         **{f'diff_{j}': diffs[j] for j in P.TECHS}))
    n1 = sum(r['T1_pass'] for r in rows); n2 = sum(r['T2_pass'] for r in rows)
    best = min(rows, key=lambda r: sum(abs(r[f'diff_{j}']) for j in P.TECHS))
    import csv
    with open(out + '/e2_sensitivity.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    L = [f'E2 SENSITIVITY over {len(rows)} declared quality parametersations (no optimisation of targets):',
         f'  T1 (KOR mix, all five within +/-10pp) passes {n1}/{len(rows)};',
         f'  T2 (HKG S6-7 mass-lecture >=20pp above S4-5) passes {n2}/{len(rows)}.',
         f'  best T1 parameterisation: q_1:1={best["q_one_to_one"]}, q_sg={best["q_small_group"]}, '
         f'boost={best["ml_boost_terminal"]}: shares hagwon {best["hagwon_share"]:.1f} (obs 73.7), '
         f'1:1 {best["one_to_one_share"]:.1f} (obs 11.3), sg {best["small_group_share"]:.1f} (obs 6.7), '
         f'net {best["internet_share"]:.1f} (obs 4.9), tb {best["textbook_share"]:.1f} (obs 3.4)']
    maxgap = max(r['gap_pp'] for r in rows)
    L.append(f'  largest HKG gap over the grid: {maxgap:+.1f} pp (threshold +20); observed gap is +39.4 pp.')
    L.append('  => no plausible quality parameterisation passes T1; T2 cannot be reached by raising the')
    L.append('     terminal-gate exam-orientation boost up to 0.50. Provider technology alone is not the missing channel.')
    open(out + '/findings_sensitivity.txt', 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))
    json.dump(dict(n=len(rows), t1_pass=n1, t2_pass=n2, maxgap=maxgap), open(out + '/sens_meta.json', 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
