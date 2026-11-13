"""Before and after the demand surge: does shadow education expand because schooling massified? ("Shadows always expand", Bray.)

For each country:
  1. Find the surge: the largest annual rise in a UIS completion series (any level) that leaves at least 10 years of
     history after it. Surge year Ys = the start of that interval.
  2. Actual: the settled history, enrolment anchored to the full UIS record (replay).
  3. No surge: identical, except every completion target after Ys is frozen at its Ys value -- the demand curve never
     moves. Same seeds, same coded events and income paths.
  4. Compare shadow education and the school system over time in the two arms (3 seeds each).

The difference is what the surge itself did, within this model. Run: python surge.py  -> results/surge.txt, results/surge.json
"""
import json, os, sys
import numpy as np
import warnings; warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snapshot as SN
from countries._common import targets
from eduengine.core import interp_path
from eduengine import measure as M

LEVELS = ['primary', 'lower secondary', 'upper secondary']
SEEDS = (0, 1, 2)


def find_surge(country, min_after=10, last_year=2024):
    best = None
    for m, pts in targets(country, 2030).items():
        for (y0, v0), (y1, v1) in zip(pts, pts[1:]):
            rate = (v1 - v0) / (y1 - y0)
            if last_year - y0 >= min_after and (best is None or rate > best['rate']):
                best = dict(level=m, start=y0, end=y1, rate=rate, v0=v0, v1=v1)
    return best


def frozen_targets(country, Ys):
    out = {}
    for m, pts in targets(country, 2030).items():
        vs = interp_path(pts, Ys)
        out[m] = [(y, v) for y, v in pts if y <= Ys] + [(Ys, vs), (2040, vs)]
        out[m] = sorted({y: v for y, v in out[m]}.items())
    return out


def series(E, years):
    y0, R = E.p['start_year'], E.R
    nl = min(E.nlev, 3)
    allg = list(range(1, int(E.ends[nl - 1]) + 1))
    sec = list(range(int(E.ends[0]) + 1, int(E.ends[nl - 1]) + 1))
    g = lambda key, t: float(R[key][t]) if key in R and 0 <= t < len(R[key]) else np.nan
    out = {k: [] for k in ('tutoring_all', 'tutoring_secondary', 'own_teacher_share', 'withheld', 'ptr', 'private_secondary',
                           'enrolled_secondary', 'tutoring_spend_per_pupil')}
    for Y in years:
        t = Y - y0
        out['tutoring_all'].append(M.tutoring(E, Y, allg))
        out['tutoring_secondary'].append(M.tutoring(E, Y, sec))
        out['own_teacher_share'].append(g('own_share', t))
        out['withheld'].append(g('withheld', t))
        out['ptr'].append(g('ptr', t))
        out['private_secondary'].append(M.private_share(E, Y, sec))
        att = np.array(R['att_by_grade'][t], float) if t < len(R['att_by_grade']) else None
        out['enrolled_secondary'].append(float(att[[x - 1 for x in sec]].sum()) / E.p['N'] if att is not None else np.nan)
        out['tutoring_spend_per_pupil'].append(g('tut_spend', t) / max(float(att.sum()), 1) if att is not None else np.nan)
    return out


def run(country):
    s = find_surge(country)
    Ys = s['start']
    years = list(range(max(1995, Ys - 10), 2025))
    arms = {}
    for arm, over in (('actual', {}), ('no surge', dict(enrol_targets=frozen_targets(country, Ys)))):
        runs = []
        for seed in SEEDS:
            E = SN.run_pack(country, over=over, anchor_until=2030, seed=seed, calibrate=False)
            runs.append(series(E, years))
        arms[arm] = {k: list(np.nanmean([r[k] for r in runs], 0)) for k in runs[0]}
        arms[arm]['completion'] = {LEVELS[m]: [M.completion_cohort(E, m, Y) for Y in years] for m in range(min(3, E.nlev))}
    return dict(country=country, surge=s, surge_level=LEVELS[s['level']], years=years, arms=arms)


def fmt(r):
    s, ys, A = r['surge'], r['years'], r['arms']
    pick = [y for y in (s['start'] - 5, s['start'], s['start'] + 5, s['start'] + 10, 2019, 2023) if y in ys]
    pick = sorted(set(pick))
    L = [f"=== {SN.LABELS[r['country']]}: surge = {r['surge_level']} completion {s['v0']:.0%} ({s['start']}) -> {s['v1']:.0%} ({s['end']}), "
         f"+{100 * s['rate']:.1f} points a year. 'No surge' freezes all completion targets at their {s['start']} level.",
         f"{'':32s}" + ''.join(f'{y:>14d}' for y in pick)]
    rows = [('enrolled in secondary (x cohort)', 'enrolled_secondary', '{:.2f}'), ('paying for tutoring, all grades', 'tutoring_all', '{:.0%}'),
            ('paying for tutoring, secondary', 'tutoring_secondary', '{:.0%}'), ('share paid to own teacher', 'own_teacher_share', '{:.0%}'),
            ('teacher effort withheld', 'withheld', '{:.2f}'), ('pupils per public teacher', 'ptr', '{:.0f}'),
            ('private share, secondary', 'private_secondary', '{:.0%}')]
    for name, k, f in rows:
        for arm in ('actual', 'no surge'):
            vals = [A[arm][k][ys.index(y)] for y in pick]
            L.append(f"{(name + ' [' + arm + ']'):32s}"[:44].ljust(32) + ''.join(f'{(f.format(v) if np.isfinite(v) else "-"):>14s}' for v in vals))
    return '\n'.join(L)


if __name__ == '__main__':
    out = [run(c) for c in SN.COUNTRIES]
    txt = '\n\n'.join(fmt(r) for r in out)
    os.makedirs('results', exist_ok=True)
    open('results/surge.txt', 'w').write(txt + '\n')
    json.dump(out, open('results/surge.json', 'w'), default=float)
    print(txt)
