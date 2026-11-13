"""One run of a country pack, flattened to plain JSON for the app, the LLM tools and reports.

    run_pack(country, over={}, drop_events=[], anchored=True, anchor_until=2015, seed=0, settled=True) -> engine
    snapshot(E, country) -> dict of year series, ledger rows (tickets), events, SDG 4 tiles, economy, instruments
    bands(country, k=8) -> min/max envelope of the headline series over the not-ruled-out runs of the history match

Every number here is either produced by the engine or read from the ledger's observation registry; nothing is typed in.
"""
import importlib, json, os, sys
import numpy as np
import warnings; warnings.filterwarnings('ignore')

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from eduengine import ledger as LG, measure as M
from countries._common import settled as _settled

COUNTRIES = ['cambodia', 'philippines', 'china']
LABELS = {'cambodia': 'Cambodia', 'philippines': 'Philippines', 'china': 'China'}
LEVELS = ['primary', 'lower secondary', 'upper secondary', 'tertiary']


def pack(country):
    if country not in COUNTRIES:
        raise ValueError(f'unknown country {country!r}; choose from {COUNTRIES}')
    return importlib.import_module(f'countries.{country}')


def run_pack(country, over=None, drop_events=(), anchored=True, anchor_until=2015, seed=0, settled=True, calibrate=None, iters=4, gain=0.7):
    """Run a pack. With anchoring on and calibrate=True, the anchoring targets are corrected a few times so that measured
    completion lands on the UIS series (anchoring maps survival per year, but repetition, exam failure and timing shift
    what the cohort measure then reports). The best iteration is kept; its error is reported as E.calibration."""
    if calibrate is None:
        calibrate = anchor_until > 2015  # replay correction only; temporal tests match the search
    C = pack(country)
    prm = dict(_settled(country)) if settled else {}
    prm.update(over or {})
    if drop_events:
        prm['events'] = [e for i, e in enumerate(C.PARAMS.get('events', [])) if i not in set(drop_events)]

    def once(extra):
        E = C.make(seed=seed, anchored=anchored, anchor_until=anchor_until, **{**prm, **extra})
        E._country = country
        E.run()
        return E
    if not (anchored and calibrate):
        E = once({}); E.calibration = None
        return E
    from countries._common import targets
    obs = targets(country, anchor_until)
    T = {m: list(v) for m, v in obs.items()}
    best = None
    for it in range(iters):
        E = once({'enrol_targets': T})
        errs, newT = [], {}
        for m, pts in obs.items():
            row = []
            for (Y, v), (_, tv) in zip(pts, T[m]):
                mv = M.completion_cohort(E, m, Y)
                if not np.isfinite(mv):
                    row.append((Y, tv)); continue
                errs.append(abs(mv - v))
                row.append((Y, float(min(0.999, max(0.005, tv + gain * (v - mv))))))
            newT[m] = row
        score = float(np.mean(errs)) if errs else 0.0
        if best is None or score < best[0]:
            best = (score, E, it, float(max(errs)) if errs else 0.0)
        T = newT
    E = best[1]
    E.calibration = dict(mean_abs_error=round(best[0], 4), max_abs_error=round(best[3], 4), iteration=best[2], iterations=iters)
    return E


def _f(x, nd=4):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return round(x, nd) if np.isfinite(x) else None


def _grades(E, m):
    lo = 0 if m == 0 else int(E.ends[m - 1])
    return list(range(lo + 1, int(E.ends[m]) + 1))


def _wtut(E, t, grades, broad):
    """Enrolment-weighted share of pupils in the given grades paying for tutoring (closed grades carry no weight)."""
    v = M.tutoring(E, E.p['start_year'] + t, grades, 'broad' if broad else 'narrow')
    return _f(v)


def _series(E, key, t_years, fn=lambda v: v):
    R = E.R.get(key)
    if R is None:
        return None
    out = []
    for t in t_years:
        out.append(_f(fn(R[t])) if t < len(R) else None)
    return out


def snapshot(E, country):
    p = E.p; y0 = p['start_year']
    years = list(range(y0 + p['measure_from'], y0 + p['T']))
    ts = [Y - y0 for Y in years]
    nl = min(E.nlev, 4)
    school_levels = [m for m in range(min(E.nlev, 3))]
    target_years = [int(y) for pts in p.get('enrol_targets', {}).values() for y, _ in pts]
    S = {'years': years, 'validation': dict(
        parameter_selection_until=2015, completion_targets_until=max(target_years) if target_years else None,
        mode='historical replay' if target_years and max(target_years) > 2015 else 'retrospective temporal evaluation',
        conditional_on_coded_paths_and_events=True, newly_blind=False)}
    S['completion'] = {LEVELS[m]: [_f(M.completion_cohort(E, m, Y)) for Y in years] for m in school_levels}
    S['tutoring_broad'] = {LEVELS[m]: [_wtut(E, t, _grades(E, m), True) for t in ts] for m in school_levels}
    allg = list(range(1, int(E.ends[min(2, E.nlev - 1)]) + 1))
    S['tutoring_all'] = dict(broad=[_wtut(E, t, allg, True) for t in ts], narrow=[_wtut(E, t, allg, False) for t in ts])
    S['tutoring_narrow'] = {LEVELS[m]: [_wtut(E, t, _grades(E, m), False) for t in ts] for m in school_levels}
    S['private_share'] = {LEVELS[m]: [_f(M.private_share(E, Y, _grades(E, m))) for Y in years] for m in school_levels}
    S['tutoring_by_quintile'] = {f'Q{q + 1}': _series(E, 'tut_by_q', ts, lambda v, q=q: v[q]) for q in range(5)}
    S['private_by_quintile'] = {f'Q{q + 1}': _series(E, 'priv_by_q', ts, lambda v, q=q: v[q]) for q in range(5)}
    S['own_teacher_share'] = _series(E, 'own_share', ts)
    S['implied_wedge'] = {LEVELS[m]: _series(E, 'implied_wedge', ts, lambda v, m=m: v[m]) for m in range(nl)}
    gdp = np.array(E.R['gdp'], float)
    econ = {
        'GDP per child (index)': _series(E, 'gdp', ts, lambda v: v / p['N'] / max(gdp[ts[0]] / p['N'], 1e-9)),
        'youth unemployment (graduates queuing)': _series(E, 'youth_unemp', ts),
        'graduate unemployment': _series(E, 'grad_unemp', ts),
        'formal-job rate of leavers': _series(E, 'formal_rate', ts),
        'formal vacancies (share of a cohort)': _series(E, 'vac', ts),
        'credential floor, routine formal jobs (years)': _series(E, 'floor_routine', ts),
        'credential floor, skilled jobs (years)': _series(E, 'floor_skilled', ts),
        'pupil-teacher ratio (public)': _series(E, 'ptr', ts),
        'teacher pay / median income': _series(E, 'teacher_pay', ts),
        'public school quality index': _series(E, 'q_pub', ts),
        'teacher effort withheld': _series(E, 'withheld', ts),
        'private school fee': _series(E, 'priv_fee', ts),
        'commercial tutoring price': _series(E, 'firm_price', ts),
        'tax / GDP': _series(E, 'tax_gdp', ts),
    }
    hh = E.R.get('hh_spend'); tsp = E.R.get('tut_spend')
    econ['household education spending / GDP'] = [_f(hh[t] / max(gdp[t], 1e-9)) if t < len(hh) else None for t in ts]
    econ['tutoring spending / GDP'] = [_f(tsp[t] / max(gdp[t], 1e-9)) if t < len(tsp) else None for t in ts]
    S['economy'] = {k: v for k, v in econ.items() if v is not None}
    # per-grade profiles (the "distribution" of shadow education) at fixed years
    prof = {}
    for Y in (2005, 2010, 2017, 2023):
        t = Y - y0
        if 0 <= t < len(E.R.get('tut_by_grade', [])):
            att = np.array(E.R['att_by_grade'][t], float)
            own = np.array(E.R['tut_own_by_grade'][t], float); firm = np.array(E.R['tut_firm_by_grade'][t], float)
            ng = int(E.ends[min(2, E.nlev - 1)])
            prof[str(Y)] = dict(own=[_f(x, 3) if att[i] > 0 else None for i, x in enumerate(own[:ng])],
                                firm=[_f(x, 3) if att[i] > 0 else None for i, x in enumerate(firm[:ng])],
                                enrolled=[int(x) for x in att[:ng]])
    S['tutoring_profile'] = prof
    # observations (for plotting) and the ledger (tickets)
    rows = LG.ledger(E, country, E.p.get('_train_until', 2015))
    S['ledger'] = [dict(indicator=r['indicator'], instrument=r['instrument'], year=r['year'], observed=r['value'],
                        model=_f(r['model']), gap=_f(r['gap']), tol=_f(r['tol']), within=r['within'], status=r['status'],
                        split=r['split'], source=r['source'], args={k: v for k, v in r['args'].items()}) for r in rows]
    sc = LG.score(rows)
    S['score'] = {k: dict(within=v[0], n=v[1]) for k, v in sc.items()}
    S['events'] = [dict(year=Y, label=lab) for (Y, lab, _) in E.event_log]
    S['all_events'] = [dict(index=i, year=e['year'], label=e.get('label', '')) for i, e in enumerate(pack(country).PARAMS.get('events', []))]
    # SDG 4 tiles over the measurement window
    S['levels'] = [dict(name=LEVELS[m], grades=_grades(E, m)) for m in range(nl)]
    S['country'] = country; S['label'] = LABELS[country]
    S['calibration'] = getattr(E, 'calibration', None)
    return S


def sdg4_tiles(E, Y=2019):
    """Headline SDG 4 indicators in one year, each tagged with its instrument."""
    T = []
    for m in range(min(3, E.nlev)):
        T.append(dict(code='4.1.2', name=f'Completion rate, {LEVELS[m]}', value=_f(M.completion_cohort(E, m, Y)), instrument='completion_cohort'))
    ends = E.ends
    T.append(dict(code='4.1.4', name='Out-of-school rate, primary age (administrative)', value=_f(M.oos_admin(E, 6, 5 + int(ends[0]), Y)), instrument='oos_admin'))
    T.append(dict(code='4.1.4', name='Out-of-school rate, primary age (household survey)', value=_f(M.oos_household(E, 6, 5 + int(ends[0]), Y)), instrument='oos_household'))
    T.append(dict(code='4.6.1', name='Youth literacy 15-24 (true skill)', value=_f(M.literacy(E, Y, 'true')), instrument='literacy_true'))
    T.append(dict(code='4.6.1', name='Youth literacy 15-24 (census self-report)', value=_f(M.literacy(E, Y, 'census_proxy')), instrument='literacy_census_proxy'))
    T.append(dict(code='4.6.1', name='Youth literacy 15-24 (DHS reading card)', value=_f(M.literacy(E, Y, 'dhs_card')), instrument='literacy_dhs_card'))
    T.append(dict(code='-', name='Street children aged 10-17 per 1,000 (no survey sees this)', value=_f(M.street_children(E, 10, 17, Y), 2), instrument='street_children'))
    T.append(dict(code='-', name='Gross intake ratio to last primary grade (World Bank "completion")', value=_f(M.gross_intake_last(E, 0, Y)), instrument='gross_intake_last'))
    return T


def full(country, **kw):
    E = run_pack(country, **kw)
    S = snapshot(E, country)
    S['sdg4'] = {str(Y): sdg4_tiles(E, Y) for Y in (2010, 2019)}
    S['settled_params'] = _settled(country) if kw.get('settled', True) else {}
    S['run'] = {k: v for k, v in kw.items()}
    return S


HEADLINE = [('completion', None), ('tutoring_all', 'broad'), ('tutoring_broad', None), ('private_share', None), ('economy', 'youth unemployment (graduates queuing)')]


def bands(country, k=8, anchor_until=2015):
    """Envelope of headline series over the not-ruled-out runs of the last history match (results/context_map.json)."""
    J = json.load(open(os.path.join(HERE, 'results', 'context_map.json')))
    if k < 1:
        raise ValueError('k must be positive')
    entry = J[country]
    if not entry['kept']:
        return dict(years=[], n=0, kept=0, completion={}, tutoring_all={},
                    tutoring_broad={}, private_share={}, economy={},
                    note='No training survivor; no plausible-setting band is available.')
    candidates = entry['runs']
    runs = [candidates[i] for i in np.linspace(0, len(candidates)-1, min(k, len(candidates)), dtype=int)]
    snaps = []
    for r in runs:
        E = run_pack(country, over=r['prm'], settled=False, seed=r.get('seed', 0), anchor_until=anchor_until, iters=3)
        snaps.append(snapshot(E, country))
    out = {'years': snaps[0]['years'], 'n': len(snaps), 'kept': J[country]['kept']}
    for key, sub in HEADLINE:
        out[key] = {}
        names = [sub] if sub else list(snaps[0][key])
        for nm in names:
            arr = np.array([[np.nan if v is None else v for v in s[key][nm]] for s in snaps], float)
            out[key][nm] = dict(lo=[_f(x) for x in np.nanmin(arr, 0)], hi=[_f(x) for x in np.nanmax(arr, 0)])
    return out


if __name__ == '__main__':
    import time
    t = time.time()
    S = full(sys.argv[1] if len(sys.argv) > 1 else 'china')
    print(json.dumps({k: (v if k in ('score', 'events') else '...') for k, v in S.items()}, indent=1)[:1500])
    print(f'{time.time() - t:.1f}s', len(json.dumps(S)) // 1024, 'KB')
