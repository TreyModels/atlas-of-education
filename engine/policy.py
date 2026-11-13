"""Policy lab: run an intervention against the settled history and report what it changes.

    lab(country, levers={'pay_ratio': 1.0, 'cct': 0.05}, year=2025, until=2039, seeds=(0, 1, 2)) -> dict

How it works
  1. Baseline: the settled pack, enrolment anchored to the UNESCO record up to `year`. From `year` on, the anchoring wedge
     is frozen at its recent mean and the mechanism decides (core.anchor_stop), so enrolment can respond to policy.
  2. Scenario: the same, plus the levers applied from `year`. Paired seeds reduce simulation noise. Branch-dependent random draws can
     diverge across arms; the seed spread remains part of the result. Results are averaged over seeds and the seed spread is reported.
  3. Effects: SDG 4 indicators, shadow education, private schooling, youth unemployment, learning, equity and public cost.
     The 'cost per extra completer' line is the effective-altruism view: extra public money over the horizon divided by
     extra upper-secondary completers, in years of median household income.

Levers are country-neutral: each sets or scales one engine parameter. Path parameters (coded as a time path in a pack)
are rewritten from `year` on, so the change persists; others are set by an event in `year`.
"""
import copy
import numpy as np
import snapshot as SN
from eduengine import measure as M
from eduengine.core import interp_path

LEVERS = [
    dict(id='pay_ratio', kind='set', lo=0.3, hi=1.6, step=0.05, unit='x median income',
         label='Teacher pay', doc='Public teacher salary relative to median income. With a fixed budget, higher pay means fewer teachers.'),
    dict(id='budget_per_child', kind='mult', lo=0.5, hi=2.0, step=0.05, unit='x current',
         label='Public school budget per child', doc='Scales the public education budget path.'),
    dict(id='monitoring', kind='set', lo=0.0, hi=1.0, step=0.05, unit='share',
         label='Teacher monitoring', doc='How well absence and withheld effort are detected (0 none, 1 full).'),
    dict(id='cct', kind='set', lo=0.0, hi=0.15, step=0.01, unit='x median income / yr',
         label='Cash transfer for secondary pupils', doc='Paid per enrolled secondary pupil in the poorest two income fifths (Progresa / 4Ps style).'),
    dict(id='fee_public', kind='set', lo=0.0, hi=0.10, step=0.01, unit='x median income / yr',
         label='Public school fees', doc='Official fees in public primary and secondary schools.'),
    dict(id='fee_tertiary', kind='set', lo=0.0, hi=0.6, step=0.02, unit='x median income / yr',
         label='University fees', doc='0 = free tertiary (Philippines 2018).'),
    dict(id='own_ban', kind='set', lo=0.0, hi=1.0, step=0.05, unit='enforcement',
         label="Ban on teachers tutoring their own pupils", doc='Share of own-pupil tutoring the ban actually stops.'),
    dict(id='firm_ban', kind='set', lo=0.0, hi=1.0, step=0.05, unit='enforcement',
         label='Ban on commercial tutoring', doc='Share of the commercial market the ban removes (China 2021 ~0.9).'),
    dict(id='vac0', kind='mult', lo=0.5, hi=2.0, step=0.05, unit='x current',
         label='Formal jobs (labour demand)', doc='Scales formal vacancies per cohort: growth, public hiring, investment.'),
]
LEVER = {l['id']: l for l in LEVERS}


def params_at(country, Y):
    """The pack's parameter values in year Y (settled values, events up to Y, paths interpolated)."""
    C = SN.pack(country)
    prm = {**C.PARAMS, **SN._settled(country)}
    out = {}
    for ev in prm.get('events', []):
        if ev['year'] <= Y:
            out.update(ev['set'])
    base = {}
    for l in LEVERS:
        k = l['id']
        if k in prm.get('paths', {}):
            base[k] = interp_path(prm['paths'][k], Y)
        elif k in out:
            base[k] = out[k]
        elif k in prm:
            base[k] = prm[k]
        else:
            base[k] = _default(k)
    return base


def _default(k):
    import eduengine as ee
    for mod in (ee.PublicSchools, ee.PrivateSchools, ee.TutoringMarket, ee.FiscalState, ee.QueueLabour):
        if k in mod.defaults:
            return mod.defaults[k]
    from eduengine.core import CORE_DEFAULTS
    return CORE_DEFAULTS.get(k)


def apply(country, levers, Y):
    """Parameter overrides that put the levers into effect from year Y."""
    C = SN.pack(country)
    prm = {**C.PARAMS, **SN._settled(country)}
    paths = copy.deepcopy(prm.get('paths', {}))
    events = list(prm.get('events', []))
    now = params_at(country, Y)
    setv, labels = {}, []
    for k, v in (levers or {}).items():
        if k not in LEVER:
            raise ValueError(f'unknown lever {k!r}; choose from {list(LEVER)}')
        l = LEVER[k]; v = float(v)
        target = now[k] * v if l['kind'] == 'mult' else v
        if abs(target - now[k]) < 1e-9:
            continue
        labels.append(f"{l['label']}: {now[k]:.3g} -> {target:.3g}")
        if k in paths:
            old = paths[k]
            f = (lambda x, v=v: x * v) if l['kind'] == 'mult' else (lambda x, t=target: t)
            paths[k] = [(y, x) for (y, x) in old if y < Y] + [(Y - 1, interp_path(old, Y - 1)), (Y, f(interp_path(old, Y)))] + \
                       [(y, f(x)) for (y, x) in old if y > Y]
            paths[k] = sorted({y: x for y, x in paths[k]}.items())
        else:
            setv[k] = target
    if setv:
        events = events + [dict(year=Y, set=setv, label='Policy package')]
    return dict(paths=paths, events=events), labels


def _completers(E, m, Y0, Y1):
    """People who completed level m in calendar years [Y0, Y1]."""
    A = E.ALL
    yr = E.p['start_year'] + A['cohort'] + A['comp_age'][:, m] - E.p['entry_age']
    return int(np.sum(np.isfinite(yr) & (yr >= Y0) & (yr <= Y1)))


def _parity_q(E, m, Y):
    """SDG 4.5.1 wealth parity for completion: poorest fifth / richest fifth (cohort 3-5 years above the last grade age)."""
    a = Y - (E.p['start_year'] + E.ALL['cohort']) + E.p['entry_age']
    intended = E.p['entry_age'] + E.ends[m] - 1
    sel = (a >= intended + 3) & (a <= intended + 5)
    q = E.ALL['q'][sel]; ca = E.ALL['comp_age'][sel, m]; done = np.isfinite(ca) & (ca <= a[sel])
    lo, hi = done[q == 0].mean() if (q == 0).any() else np.nan, done[q == 4].mean() if (q == 4).any() else np.nan
    return float(lo / hi) if hi and np.isfinite(hi) and hi > 0 else np.nan


def measures(E, Y0, Y1):
    """Indicator values at the end year and spending over [Y0, Y1]."""
    p, R, y0 = E.p, E.R, E.p['start_year']
    nl = min(E.nlev, 3)
    allg = list(range(1, int(E.ends[nl - 1]) + 1))
    t0, t1 = Y0 - y0, Y1 - y0
    ts = range(t0, min(t1 + 1, len(R['pub_spend'])))
    gdp = np.array(R['gdp'], float)
    spend = float(sum(R['pub_spend'][t] + R.get('cct_cost', [0] * len(R['pub_spend']))[t] + R.get('voucher_cost', [0] * len(R['pub_spend']))[t] for t in ts))
    hh = float(sum(R['hh_spend'][t] for t in ts))
    med = float(np.mean([interp_path(p['paths']['y_median'], y0 + t) if 'y_median' in p['paths'] else p.get('y_median', 1.0) for t in ts]))
    out = {}
    for m in range(nl):
        out[f'completion: {SN.LEVELS[m]}'] = M.completion_cohort(E, m, Y1)
    out['wealth parity in completion (poorest / richest fifth): lower secondary'] = _parity_q(E, min(1, nl - 1), Y1)
    out['wealth parity in completion (poorest / richest fifth): upper secondary'] = _parity_q(E, min(2, nl - 1), Y1)
    out['paying for tutoring (all grades)'] = SN._wtut(E, t1, allg, True)
    out['paying for commercial tutoring'] = SN._wtut(E, t1, allg, False)
    out['tutoring paid to own teacher (share of tutored)'] = R['own_share'][t1] if t1 < len(R['own_share']) else np.nan
    out['private-school share, lower secondary'] = M.private_share(E, Y1, SN._grades(E, min(1, nl - 1)))
    out['youth unemployment (graduates queuing)'] = M.youth_unemployment(E, Y1)
    out['tutoring jobs (share of a cohort)'] = R['tutor_jobs'][t1] if 'tutor_jobs' in R and t1 < len(R['tutor_jobs']) else np.nan
    out['youth literacy 15-24 (true skill)'] = M.literacy(E, Y1, 'true')
    out['pupil-teacher ratio (public)'] = R['ptr'][t1] if t1 < len(R['ptr']) else np.nan
    out['teacher effort withheld'] = R['withheld'][t1] if t1 < len(R['withheld']) else np.nan
    out['public education spending / GDP'] = spend / max(float(gdp[list(ts)].sum()), 1e-9)
    out['household education spending / GDP'] = hh / max(float(gdp[list(ts)].sum()), 1e-9)
    out['_spend'] = spend; out['_median'] = med
    out['_completers_upper'] = _completers(E, min(2, nl - 1), Y0, Y1)
    out['_completers_lower'] = _completers(E, min(1, nl - 1), Y0, Y1)
    return {k: (float(v) if v is not None else np.nan) for k, v in out.items()}


def _series(E, Y0, Y1):
    y0 = E.p['start_year']
    years = list(range(Y0 - 10, Y1 + 1))
    nl = min(E.nlev, 3)
    allg = list(range(1, int(E.ends[nl - 1]) + 1))
    return dict(years=years,
                completion={SN.LEVELS[m]: [SN._f(M.completion_cohort(E, m, Y)) for Y in years] for m in range(nl)},
                tutoring=[SN._wtut(E, Y - y0, allg, True) for Y in years],
                youth_unemployment=[SN._f(M.youth_unemployment(E, Y)) for Y in years],
                private_lower=[SN._f(M.private_share(E, Y, SN._grades(E, min(1, nl - 1)))) for Y in years])


def lab(country, levers=None, year=2025, until=2039, seeds=(0, 1, 2)):
    T = until - 1980 + 1
    over_s, labels = apply(country, levers or {}, year)
    res = {'baseline': [], 'scenario': []}
    ser = {}
    for s in seeds:
        for arm, extra in (('baseline', {}), ('scenario', over_s)):
            E = SN.run_pack(country, over=dict(T=T, anchor_stop=year, **extra), anchor_until=2030, seed=s, calibrate=False)
            res[arm].append(measures(E, year, until))
            if s == seeds[0]:
                ser[arm] = _series(E, year, until)
    keys = list(res['baseline'][0])
    rows = []
    for k in keys:
        b = np.array([r[k] for r in res['baseline']]); sc = np.array([r[k] for r in res['scenario']])
        d = sc - b
        if k.startswith('_'):
            continue
        rows.append(dict(indicator=k, baseline=SN._f(np.nanmean(b)), scenario=SN._f(np.nanmean(sc)), delta=SN._f(np.nanmean(d)),
                         spread=SN._f(np.nanstd(d, ddof=1)) if len(seeds) > 1 else None))
    mean = lambda arm, k: float(np.mean([r[k] for r in res[arm]]))
    d_spend = mean('scenario', '_spend') - mean('baseline', '_spend')
    d_up = mean('scenario', '_completers_upper') - mean('baseline', '_completers_upper')
    d_low = mean('scenario', '_completers_lower') - mean('baseline', '_completers_lower')
    med = mean('baseline', '_median')
    cost = dict(extra_public_spending_median_incomes=SN._f(d_spend / med, 2),
                extra_upper_completers=SN._f(d_up, 1), extra_lower_completers=SN._f(d_low, 1),
                per_extra_upper_completer=SN._f(d_spend / med / d_up, 2) if d_up > 0.5 and d_spend > 0 else None,
                per_extra_lower_completer=SN._f(d_spend / med / d_low, 2) if d_low > 0.5 and d_spend > 0 else None,
                cohort_size=SN.pack(country).PARAMS.get('N', 1000))
    return dict(country=country, label=SN.LABELS[country], year=year, until=until, seeds=list(seeds), levers=levers or {},
                applied=labels, now=params_at(country, year), rows=rows, cost=cost, series=ser)


if __name__ == '__main__':
    import json, sys, time
    t = time.time()
    out = lab(sys.argv[1] if len(sys.argv) > 1 else 'cambodia', json.loads(sys.argv[2]) if len(sys.argv) > 2 else {'pay_ratio': 1.0})
    print(out['applied'], out['now'])
    for r in out['rows']:
        print(f"  {r['indicator']:55s} {r['baseline']!s:>8} {r['scenario']!s:>8} {r['delta']!s:>8} ±{r['spread']}")
    print(out['cost'], f'{time.time() - t:.1f}s')
