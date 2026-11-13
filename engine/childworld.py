"""childworld: a fast, general school-and-work world for cross-country Monte Carlo (Asia comparison).

Generalises the household decision in camchild.js to one region with every structural feature exposed as a
parameter, vectorised with numpy so thousands of worlds run in minutes. Each year every household chooses, for each
child aged 6-17, one of four states (the design memo's A-D):
  school   in school, not working                      (A)
  both     in school and working                       (B)
  work     out of school, working                      (C)
  neither  out of school, not in market work: domestic care, marriage, idleness, inaccessible school   (D)
Child labour follows the ILO statistical definition used in camchild: any work under 15, work at 15-17 in a
hazardous share `haz`, and school-plus-work under 12.

Structural parameters (each a plausible range, drawn by the Monte Carlo):
  y_med     household income, in adult informal wages                       poverty
  w_child   child market wage, relative                                     labour-demand pull
  farm      share of households with a farm or family business              work available at home
  compat    how well work fits around school (seasonal, part-time)          both-ness
  v0, decay value of schooling at primary and its decline by level          returns, credential floor
  cost      school cost multiplier (fees, distance, tutoring)               supply / price
  neither   baseline value of not being in school or market work            disengagement, low quality
  girl_care extra value of 'neither' for girls (care, chores, marriage)     gender norms (state D)
  haz       share of 15-17 workers in hazardous work                        definition / sector mix
This is not docked to camchild.js (it drops regions, migration and wage clearing); it shares its utility form and
constants so its behaviour is comparable. camchild remains the Cambodia model.
"""
import math
import numpy as np

STATES = ('school', 'both', 'work', 'neither')

PRIORS = {   # name: (low, high, 'lin' | 'log')
    'y_med': (0.4, 3.0, 'log'), 'w_child': (0.05, 0.6, 'lin'), 'farm': (0.0, 0.8, 'lin'), 'compat': (0.0, 1.0, 'lin'),
    'v0': (1.0, 5.0, 'lin'), 'decay': (0.2, 1.2, 'lin'), 'cost': (0.5, 3.0, 'log'), 'neither': (-1.5, 4.5, 'lin'),
    'girl_care': (0.0, 2.0, 'lin'), 'haz': (0.2, 0.6, 'lin'),
}
# v2 (5 Nov 2026), revised AFTER the India composition test failed under PRIORS: India has teenagers in work that does
# not meet the child-labour definition (work only 1.8% vs child labour 1.0%), which needs a lower hazardous share.
PRIORS_V2 = dict(PRIORS, haz=(0.05, 0.6, 'lin'))


def draw(rng, n, priors=None):
    out = {}
    for k, (lo, hi, sc) in (priors or PRIORS).items():
        u = rng.random(n)
        out[k] = np.exp(np.log(lo) + u * (np.log(hi) - np.log(lo))) if sc == 'log' else lo + u * (hi - lo)
    return out


def simulate(th, N=2000, years=8, keep=3, seed=0):
    """One world. th: dict of scalars. Returns averages over the last `keep` years."""
    r = np.random.default_rng(seed)
    z = r.standard_normal(N)
    y0 = th['y_med'] * np.exp(0.6 * z)
    age = r.integers(6, 18, N)
    girl = r.random(N) < .5
    ability = r.standard_normal(N); taste = r.standard_normal(N)
    farm = r.random(N) < th['farm']
    out_years = np.zeros(N)
    need = .85
    v = np.array([th['v0'], th['v0'] * th['decay'], th['v0'] * th['decay'] ** 2])
    acc = {k: [] for k in ('oos_prim', 'oos_lower', 'oos_upper', 'cl', 'neither_share_oos', 'both_share_cl',
                           'oos_among_cl_5_14', 'oos_among_noncl_5_14', 'girls_neither', 'boys_neither', 'work_share_oos',
                           'school', 'both', 'work', 'neither', 'boys1417_work_share_oos',
                           # age-banded outputs for survey tests (added 5 Nov 2026; consume no random numbers)
                           'oos_7_14', 'oos_15_17', 'neither_share_oos_7_14', 'neither_share_oos_15_17',
                           'both_7_14', 'both_15_17')}

    def util(c):
        x = c - .6 * need
        return np.where(x > .05, np.log(np.maximum(x, 1e-9)), math.log(.05) + (x - .05) / .05)

    for t in range(years):
        shocked = r.random(N) < .15
        y = y0 * np.where(shocked, .6, 1.0) + np.where(shocked, np.minimum(.4 * y0, .15 * y0), 0) - .08 * y0
        ageW = np.select([age < 10, age < 12, age < 15], [.25, .45, .7], 1.0)
        earn = .32 * ageW * np.maximum(th['w_child'] / .32 * 1.0, np.where(farm, .55, 0.0))
        lvl = np.select([age <= 11, age <= 14], [0, 1], 2)
        cost = th['cost'] * np.array([.05, .14, .22])[lvl]
        vl = v[lvl] + .25 * ability - 1.3 * np.minimum(out_years, 3) / 3
        U = np.stack([
            util(y - cost) + vl,
            util(y - cost + .5 * (1 + th['compat']) * earn) + vl * (.72 + .2 * th['compat']) + .4 * th['compat'] - .25,
            util(y + earn) - .2 * taste,
            util(y) + th['neither'] + np.where(girl, th['girl_care'], 0.0),
        ])
        P = np.exp((U - U.max(0)) / .3); P /= P.sum(0)
        c = (r.random(N)[None, :] > np.cumsum(P, 0)).sum(0)            # 0 school, 1 both, 2 work, 3 neither
        hazdraw = r.random(N) < th['haz']
        cl = ((c == 2) & ((age < 15) | hazdraw)) | ((c == 1) & (age < 12))
        oos = (c >= 2)
        if t >= years - keep:
            m = lambda mask: oos[mask].mean() if mask.any() else 0.0
            acc['oos_prim'].append(m(lvl == 0)); acc['oos_lower'].append(m(lvl == 1)); acc['oos_upper'].append(m(lvl == 2))
            acc['cl'].append(cl.mean())
            acc['neither_share_oos'].append((c == 3)[oos].mean() if oos.any() else 0.0)
            acc['work_share_oos'].append((c == 2)[oos].mean() if oos.any() else 0.0)
            acc['both_share_cl'].append((c == 1)[cl].mean() if cl.any() else 0.0)
            y14 = age <= 14
            acc['oos_among_cl_5_14'].append(oos[cl & y14].mean() if (cl & y14).any() else 0.0)
            acc['oos_among_noncl_5_14'].append(oos[~cl & y14].mean() if (~cl & y14).any() else 0.0)
            acc['girls_neither'].append((c == 3)[girl].mean()); acc['boys_neither'].append((c == 3)[~girl].mean())
            b = (~girl) & (age >= 14) & oos
            acc['boys1417_work_share_oos'].append((c == 2)[b].mean() if b.any() else 0.0)
            for i, s in enumerate(STATES):
                acc[s].append((c == i).mean())
            for tag, band in (('7_14', (age >= 7) & (age <= 14)), ('15_17', age >= 15)):
                acc['oos_' + tag].append(oos[band].mean() if band.any() else 0.0)
                ob = oos & band
                acc['neither_share_oos_' + tag].append((c == 3)[ob].mean() if ob.any() else 0.0)
                acc['both_' + tag].append((c == 1)[band].mean() if band.any() else 0.0)
        out_years = np.where(oos, out_years + 1, 0)
        age = age + 1
        old = age > 17
        age[old] = 6; out_years[old] = 0; ability[old] = r.standard_normal(old.sum()); girl[old] = r.random(old.sum()) < .5
    return {k: float(np.mean(v_)) for k, v_ in acc.items()}
