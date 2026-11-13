"""Monte Carlo over floorworld v2: which theory of education and industrialisation can produce China, Vietnam, the
Philippines and Cambodia at once; how much signalling (Caplan) the evidence allows; and what Cambodia gets from
finishing the floor, expanding universities, attracting more zone investment, or vocational schools as pipeline vs
parking.

Pattern-oriented test: draw parameters from PRIORS, run all four countries on their documented schedules, keep draws
that reproduce every pattern. Schedules are inputs; enrolment levels are therefore checks on inputs, not tests.

Tests
  T1 complexity, 2018: China above Vietnam and the Philippines, both above Cambodia (Harvard ECI ranks 18, 52, 35, 90)
  T2 Cambodia informal employment 2019: 80-95% (ILO 89.4%)
  T3 Vietnam informal employment 2023: 55-80% (ILO 67.7%)
  T4 Philippine graduates abroad, 2023: 1-8% of the workforce (2.16m OFWs, PSA 2023; model counts graduates only)
  T5 China graduate surplus: share of graduates outside complex and public posts up >= 10 pts, 1998 -> 2019
  T6 Philippine K-12 adds little formal employment: formal share 2015 -> 2023 up < 3 pts (PIDS 2023)
  T7 Undereducation in formal work higher in Cambodia than Vietnam, 2013 (ILO school-to-work surveys 2012-13)
  T8 Overeducation higher in Vietnam than Cambodia, 2013 (ILO: Vietnam 23.5% of young workers overeducated)
Run from engine/:  python floorworld_mc.py [--draws N]  -> results/floorworld_mc.{json,md}
"""
import argparse, json, os, sys
from concurrent.futures import ProcessPoolExecutor
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import floorworld as F

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
TESTS = ['T1 complexity order', 'T2 Cambodia informal', 'T3 Vietnam informal', 'T4 Philippine emigration',
         'T5 China graduate surplus', 'T6 K-12 little formal gain', 'T7 undereducation KH>VN', 'T8 overeducation VN>KH']
STRUCT = {'S1': 'S1 human-capital-led', 'S2': 'S2 demand-led', 'S3': 'S3 complexity', 'S4': 'S4 adoption (floor attracts investment)',
          'S5': 'S5 floor attracts factories, complex jobs follow demand'}


def tests(o):
    a = F.at
    cx = {c: a(o[c], 'complex', 2018) for c in o}
    return [cx['China'] > max(cx['Vietnam'], cx['Philippines']) and min(cx['Vietnam'], cx['Philippines']) > cx['Cambodia'],
            .80 <= a(o['Cambodia'], 'informal', 2019) <= .95,
            .55 <= a(o['Vietnam'], 'informal', 2023) <= .80,
            .01 <= a(o['Philippines'], 'emig', 2023) <= .08,
            a(o['China'], 'surplus', 2019) - a(o['China'], 'surplus', 1998) >= .10,
            a(o['Philippines'], 'formal', 2023) - a(o['Philippines'], 'formal', 2015) < .03,
            a(o['Cambodia'], 'undereduc', 2013) > a(o['Vietnam'], 'undereduc', 2013),
            a(o['Vietnam'], 'overeduc', 2013) > a(o['Cambodia'], 'overeduc', 2013)]


VN, CN = F.COUNTRIES['Vietnam'], F.COUNTRIES['China']
CF = {
    'finish the floor (Vietnam-like lower secondary)': dict(floor_lower=[(1980, .05), (2020, .56), (2030, .85)]),
    'expand universities (to 35% by 2030)': dict(he_cap=[(1980, .005), (2019, .15), (2030, .35)]),
    'double zone investment': dict(invest=[(1980, 0), (1995, .03), (2005, .1), (2015, .15), (2020, .2), (2030, .4)]),
    'floor + zone investment': dict(floor_lower=[(1980, .05), (2020, .56), (2030, .85)],
                                    invest=[(1980, 0), (1995, .03), (2005, .1), (2015, .15), (2020, .2), (2030, .4)]),
    'vocational at 30%, as parking': dict(vshare=[(1980, 0), (2020, .05), (2030, .3)], _roles=dict(v_skill=0, v_pipe=0, v_protect=0)),
    'vocational at 30%, as pipeline + protection': dict(vshare=[(1980, 0), (2020, .05), (2030, .3)], _roles=dict(v_skill=.8, v_pipe=1, v_protect=1)),
}
COUT = ('informal', 'complex', 'overeduc', 'undereduc', 'output', 'floor')


def _job(args):
    S, ths = args
    res = []
    for th in ths:
        o = {c: F.simulate(c, S, th) for c in F.COUNTRIES}
        res.append(tests(o))
    return res


def counterfactual(S, th, name):
    over = dict(CF[name]); roles = over.pop('_roles', {})
    th2 = dict(th, **roles)
    base = F.simulate('Cambodia', S, th2 if roles else th); cf = F.simulate('Cambodia', S, th2, over)
    return {k: F.at(cf, k, 2035) - F.at(base, k, 2035) for k in COUT}


def main(n):
    rng = np.random.default_rng(23)
    draws = [{k: lo + rng.random() * (hi - lo) for k, (lo, hi) in F.PRIORS.items()} for _ in range(n)]
    res = dict(draws=n, structures={})
    for S in STRUCT:
        chunks = [(S, draws[i:i + 250]) for i in range(0, n, 250)]
        with ProcessPoolExecutor() as ex:
            T = np.array([t for part in ex.map(_job, chunks) for t in part])
        keep = [d for d, ok in zip(draws, T.all(1)) if ok]
        near = [d for d, t in zip(draws, T) if t.sum() >= len(TESTS) - 1]
        r = dict(pass_rate={t: float(T[:, j].mean()) for j, t in enumerate(TESTS)}, all_pass=float(T.all(1).mean()),
                 kept=len(keep), near=len(near))
        pool = keep if len(keep) >= 20 else near
        r['posterior_from'] = 'all tests' if pool is keep else 'all but one test'
        r['caplan'] = {k: [float(np.percentile([d[k] for d in pool], p)) for p in (10, 50, 90)] if pool else None
                       for k in ('sig_L', 'sig_U', 'sig_T', 'v_skill', 'v_pipe', 'v_protect', 'b_ok', 'legib', 'k_sup', 'eta', 'inv_scale')}
        r['cf'] = {}
        for name in CF:
            vals = [counterfactual(S, d, name) for d in pool[:150]]
            r['cf'][name] = {k: [float(np.percentile([v[k] for v in vals], p)) for p in (10, 50, 90)] if vals else None for k in COUT}
        res['structures'][S] = r
        print(S, 'all', r['all_pass'], 'kept', r['kept'], 'near', r['near'], {k: round(v, 2) for k, v in r['pass_rate'].items()}, flush=True)
    json.dump(res, open(os.path.join(OUT, 'floorworld_mc.json'), 'w'), indent=1)
    report(res)


def report(res):
    L = ['# What education does for industrialisation: China, Vietnam, the Philippines, Cambodia', '',
         f"Generated by `python engine/floorworld_mc.py`. {res['draws']:,} parameter draws, each run for all four countries "
         'under each theory (2 ms per country-run). A theory earns credibility to the extent its draws reproduce all '
         'eight patterns at once.', '',
         '| Test | ' + ' | '.join(STRUCT[s] for s in res['structures']) + ' |', '|---|' + '---:|' * len(res['structures'])]
    for t in TESTS:
        L.append(f'| {t} | ' + ' | '.join(f"{100 * r['pass_rate'][t]:.0f}%" for r in res['structures'].values()) + ' |')
    L.append('| **All eight** | ' + ' | '.join(f"**{100 * r['all_pass']:.2f}%** ({r['kept']})" for r in res['structures'].values()) + ' |')
    L.append('| All but one | ' + ' | '.join(f"{r['near']}" for r in res['structures'].values()) + ' |')
    L += ['', '## How much signalling (Caplan) and which vocational roles the evidence allows', '',
          'Medians [10-90%] among draws that pass (or, where too few pass, pass all but one), against priors of '
          'L 0-0.3, upper 0-0.7, tertiary 0-0.9 and 0-1 for the vocational roles.', '',
          '| Theory | Draws used | Signal share, lower sec | upper sec | tertiary | Voc. skills | Voc. pipeline | Voc. protection | Open (unscreened) factory jobs |',
          '|---|---|---|---|---|---|---|---|---|']
    f = lambda v: f"{v[1]:.2f} [{v[0]:.2f}-{v[2]:.2f}]" if v else ''
    for S, r in res['structures'].items():
        c = r['caplan']
        L.append(f"| {STRUCT[S]} | {r['posterior_from']} | {f(c['sig_L'])} | {f(c['sig_U'])} | {f(c['sig_T'])} | "
                 f"{f(c['v_skill'])} | {f(c['v_pipe'])} | {f(c['v_protect'])} | {f(c['b_ok'])} |")
    L += ['', '**Theory-specific parameters among the same draws:** ' + '; '.join(
        f"{STRUCT[S]}: legibility {f(r['caplan']['legib'])}, jobs per graduate {f(r['caplan']['k_sup'])}, "
        f"attraction to the floor {f(r['caplan']['eta'])}, investment scale {f(r['caplan']['inv_scale'])}"
        for S, r in res['structures'].items() if r['caplan']['legib'])]
    L += ['', '## Cambodia, 2035: what each policy changes (vs its own path), by theory', '',
          'Percentage points, median [10-90%] over the same draws. Output is per worker, in informal-wage units.', '']
    g = lambda v, s=100: f"{s * v[1]:+.1f} [{s * v[0]:+.1f}, {s * v[2]:+.1f}]" if v else ''
    for S, r in res['structures'].items():
        L += [f"**{STRUCT[S]}** ({r['posterior_from']})", '',
              '| Policy | Informal | Complex | Overeducated | Undereducated in factories | Output per worker | Floor completion |',
              '|---|---|---|---|---|---|---|']
        for name, d in r['cf'].items():
            L.append(f"| {name} | {g(d['informal'])} | {g(d['complex'])} | {g(d['overeduc'])} | {g(d['undereduc'])} | "
                     f"{g(d['output'], 1)} | {g(d['floor'])} |")
        L.append('')
    open(os.path.join(OUT, 'floorworld_mc.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--draws', type=int, default=4000)
    main(ap.parse_args().draws)
