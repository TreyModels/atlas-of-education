"""China page: the official frame, a Shapley attribution of the engine's graduate-queue measure, and Monte Carlo interventions.

  1. Official frame: Five-Year Plan targets and the NBS youth-unemployment series, each with its source (results/china_frame.json).
  2. Attribution. Four causes the engine can switch, each with a declared counterfactual ("what if this had not happened"):
       seats    higher-education expansion (gaokao quotas rise from 1999): counterfactual = quotas stay at their 1980 shares
       dr       Double Reduction 2021 (commercial tutoring ban, which also removes tutoring-firm graduate jobs): counterfactual = no ban
       jobs     formal-job growth: counterfactual = formal vacancies 1.3x from 2015 (demand keeps pace)
       waiting  families' capacity to support waiting graduates: counterfactual = few can wait (queue_support 3.0 instead of 1.5)
     Shapley value of each = its average marginal effect over all orders of switching the causes on, so the shares add up to the
     total difference between the world with none of them and the actual history. Outcome = mean degree-holder queue (per cohort size) 2022-2024.
  3. Monte Carlo: uncertain parameters drawn from declared ranges; each intervention is run against the same draw's baseline
     (paired). Reported: median change and 10-90% band of the degree-holder queue (per cohort size) 2032-2034.
Not modelled (reported as such): field-of-study mismatch; the NBS definition itself (the engine measures graduates queuing, not
the NBS 16-24 rate), so the page reports changes and shares, not levels. Run: python china_page.py -> results/china_page.json/.txt
"""
import itertools, json, math, os, sys
import numpy as np
import warnings; warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snapshot as SN, policy as PO
from countries import china as CN
from eduengine import measure as M

SEEDS = (0, 1, 2, 3)
CAUSES = ['seats', 'dr', 'jobs', 'waiting']
LABEL = dict(seats='Higher-education seat expansion (1999 on)', dr='Double Reduction 2021 (incl. lost tutoring jobs)',
             jobs='Formal-job growth (kept at actual pace)', waiting='Family capacity to support waiting graduates')
BASE_GATES = CN._gates(0.35, 0.04)

FRAME = dict(
    plan_14=[
        dict(item='Higher-education gross enrolment ratio', target='60% (2025)', achieved='60.8%', status='met',
             source='https://en.people.cn/n3/2025/0924/c90000-20370227.html'),
        dict(item='Preschool gross enrolment ratio', target='over 90%', achieved='92%', status='met',
             source='https://en.people.cn/n3/2025/0924/c90000-20370227.html'),
        dict(item='Senior-high gross enrolment ratio', target='above 92%', achieved='not stated in the sources read', status='unverified',
             source='https://planipolis.iiep.unesco.org/sites/default/files/ressources/china%20THE%2014TH%20FIVE-YEAR%20PLAN-chapter43-Building%20a%20High-Quality%20Education%20System.pdf'),
        dict(item='University graduates supplied 2021-2025', target='none stated', achieved='over 55 million', status='no target',
             source='https://en.people.cn/n3/2025/0924/c90000-20370043.html'),
    ],
    plan_15='2030 goal: essentially complete a high-quality education system; 23 key tasks in five areas. Numeric education targets were NOT found in the sources read (gov.cn summary has none); get the full State Council outline before using any.',
    nbs_16_24_excl_students=[
        ('2023-06', 21.3, 'old method, all-time high (tradingeconomics)'), ('2024-06', 13.2, 'record low under the new method'),
        ('2025-06', 14.5, ''), ('2026-05', 15.6, ''), ('2026-06', 14.9, ''), ('2026-07', 17.9, ''), ('2026-08', 18.9, '12-month high'),
        ('2026-09', 18.0, ''),
    ],
    nbs_25_29=('2026-09', 7.4),
    source_unemployment='https://tradingeconomics.com/china/youth-unemployment-rate',
    caveat='Series compiled from one aggregator page and search headlines; the method change after the 2023 suspension was not confirmed on the page fetched.',
)


def over_for(active, T=None):
    """Parameter overrides for a coalition: causes in `active` take their historical value, the others their counterfactual."""
    ev = [dict(e, set=dict(e['set'])) for e in CN.PARAMS['events']]
    out_ev = []
    for e in ev:
        if 'gates' in e['set'] and 'seats' not in active:
            e['set']['gates'] = BASE_GATES
        if e['year'] == 2021 and 'dr' not in active:
            continue
        out_ev.append(e)
    over = dict(events=out_ev)
    if T:
        over['T'] = T
    if 'jobs' not in active:
        o, _ = PO.apply('china', {'vac0': 1.3}, 2015)
        over['paths'] = o['paths']
    if 'waiting' not in active:
        over['queue_support'] = 3.0
    return over


def outcome(E, y0=2022, y1=2024):
    """Degree holders waiting for formal jobs, per cohort-size (engine note deg_queue). The older youth_unemp measure also counts
    upper-secondary leavers who miss a university place, so it rises when seats are cut -- a different thing."""
    y = E.p['start_year']
    return float(np.nanmean([E.R['deg_queue'][Y - y] for Y in range(y0, y1 + 1)]))


def shapley():
    vals = {}
    for r in range(len(CAUSES) + 1):
        for S in itertools.combinations(CAUSES, r):
            runs = [outcome(SN.run_pack('china', over=over_for(set(S)), anchor_until=2030, seed=s, calibrate=False)) for s in SEEDS]
            vals[frozenset(S)] = (float(np.mean(runs)), float(np.std(runs, ddof=1)))
    n = len(CAUSES); phi = {}
    for c in CAUSES:
        tot = 0.0
        for r in range(n):
            for S in itertools.combinations([x for x in CAUSES if x != c], r):
                w = math.factorial(r) * math.factorial(n - r - 1) / math.factorial(n)
                tot += w * (vals[frozenset(S) | {c}][0] - vals[frozenset(S)][0])
        phi[c] = tot
    return dict(none=vals[frozenset()], actual=vals[frozenset(CAUSES)], phi=phi,
                alone={c: vals[frozenset([c])][0] - vals[frozenset()][0] for c in CAUSES},
                without={c: vals[frozenset(CAUSES)][0] - vals[frozenset(set(CAUSES) - {c})][0] for c in CAUSES})


# Declared ranges for the Monte Carlo (assumed; they bound judgement, not data -- see struts S2, S3, S6, S11)
RANGES = dict(tutor_labour_share=(0.3, 0.9), tutor_turnover=(0.15, 0.35), queue_support=(1.0, 2.0), skilled_share=(0.25, 0.45),
              queue_horizon=(5.0, 11.0))
INTERVENTIONS = {
    'More formal jobs (public hiring, +20%)': dict(vac0=1.2),
    'Slow seat growth (gaokao quota back to 35%)': 'seats',
    'Reverse the commercial tutoring ban (to 20% enforcement)': dict(firm_ban=0.2),
}


def monte_carlo(n=24, Y=2026, until=2039, window=(2032, 2034), seed=12345):
    rng = np.random.default_rng(seed)
    T = until - 1980 + 1
    res = {k: [] for k in INTERVENTIONS}; base_l = []
    for i in range(n):
        draw = {k: float(rng.uniform(*v)) for k, v in RANGES.items()}
        sd = int(rng.integers(0, 10_000))
        def run(extra):
            return outcome(SN.run_pack('china', over=dict(T=T, anchor_stop=Y, **draw, **extra), anchor_until=2030, seed=sd, calibrate=False), *window)
        b = run({})
        base_l.append(b)
        for name, spec in INTERVENTIONS.items():
            if spec == 'seats':
                ev = [dict(e, set=dict(e['set'])) for e in CN.PARAMS['events']] + [dict(year=Y, set=dict(gates=CN._gates(0.55, 0.35)), label='quota back')]
                extra = dict(events=ev)
            else:
                extra, _ = PO.apply('china', spec, Y)
            res[name].append(run(extra) - b)
    out = {}
    for k, d in res.items():
        d = np.array(d)
        out[k] = dict(median=float(np.median(d)), p10=float(np.percentile(d, 10)), p90=float(np.percentile(d, 90)),
                      share_reducing=float(np.mean(d < -0.002)), share_raising=float(np.mean(d > 0.002)))
    return dict(n=n, year=Y, window=window, ranges=RANGES, baseline_median=float(np.median(base_l)), interventions=out)


def fmt(S, MC):
    L = ['CHINA PAGE', '', 'Official frame (Fourteenth Five-Year Plan):']
    for r in FRAME['plan_14']:
        L.append(f"  {r['item']:42s} target {r['target']:18s} achieved {r['achieved']:30s} [{r['status']}]")
    L += ['  Fifteenth Plan: ' + FRAME['plan_15'], '', 'NBS 16-24 excluding students (%): ' + ', '.join(f'{d} {v}' for d, v, _ in FRAME['nbs_16_24_excl_students']), '',
          'What accounts for the engine\'s degree-holder queue (per cohort size), 2022-24 (Shapley over four switchable causes; differences, not levels):',
          f"  world with none of the four: {S['none'][0]:.3f} (seed sd {S['none'][1]:.3f});  actual history: {S['actual'][0]:.3f} (seed sd {S['actual'][1]:.3f})"]
    tot = S['actual'][0] - S['none'][0]
    for c in CAUSES:
        L.append(f"  {LABEL[c]:52s} {S['phi'][c]:+.3f}   ({(S['phi'][c] / tot * 100 if abs(tot) > 1e-9 else float('nan')):+.0f}% of total {tot:+.3f};  alone {S['alone'][c]:+.3f}, drop-one {S['without'][c]:+.3f})")
    L += ['  Not modelled: field-of-study mismatch; the NBS definition.', '',
          f"Interventions from {MC['year']}, change in degree-holder queue (per cohort size) {MC['window'][0]}-{MC['window'][1]} ({MC['n']} paired draws; baseline median {MC['baseline_median']:.3f}):"]
    for k, v in MC['interventions'].items():
        L.append(f"  {k:60s} median {v['median']:+.3f}  10-90%: {v['p10']:+.3f} to {v['p90']:+.3f}   lowers in {v['share_reducing']:.0%} of draws, raises in {v['share_raising']:.0%}")
    L.append('Ranges drawn: ' + '; '.join(f'{k} {v[0]}-{v[1]}' for k, v in MC['ranges'].items()) + ' (assumed, not data).')
    return '\n'.join(L)


if __name__ == '__main__':
    S = shapley(); MC = monte_carlo()
    txt = fmt(S, MC)
    os.makedirs('results', exist_ok=True)
    open('results/china_page.txt', 'w').write(txt + '\n')
    json.dump(dict(frame=FRAME, shapley={k: (v if not isinstance(v, tuple) else list(v)) for k, v in S.items()}, monte_carlo=MC),
              open('results/china_page.json', 'w'), indent=1, default=float)
    print(txt)
