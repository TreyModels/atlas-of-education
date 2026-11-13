"""Age-aligned survey tests for the cross-country childworld model (India, Kyrgyzstan).

Why this exists. The first composition tests (childworld_mc.py) matched worlds to register-based out-of-school rates for
lower-secondary age and then compared the result with a survey composition for ages 6-17 (India) or 7-14 with an
undefined work concept (Kyrgyzstan). Two different age bands and two different sources; the India "fail" may only have
been that mismatch. Here the matching targets and the test targets come from the SAME survey, on the SAME age bands:

  India (PLFS 2018/19, UNICEF Innocenti 2024 Table 7)   match on out-of-school share of 7-14s and of 15-17s;
      test (not used in matching): share of out-of-school children who are neither in school nor in work, at 7-14, at
      15-17 and at 6-17, and the share of children combining school and work.
  Kyrgyzstan (MICS6 2018 snapshots)   match on out-of-school rates by school level; test the model's economic
      school-and-work share and child-labour rate against the survey's BROADER work concept as an upper bound only (the
      survey counts household chores; the model does not), so a point pass/fail would be meaningless.

Inputs and source links: data/asia_school_work.json -> countries.<name>.age_aligned.
Run from engine/:  python childworld_agealigned.py [--worlds N]   -> results/childworld_agealigned.{json,md}
Priors v1 are the default. v2 differs only in the hazardous-share box (revised after the first India test); that parameter
enters child labour but none of the quantities matched or tested here, so v1 and v2 give identical results for India
and Kyrgyzstan except for the child-labour line (use --priors both to check).
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import childworld as W
import mc as MC

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
DATA = json.load(open(os.path.join(HERE, 'data', 'asia_school_work.json')))['countries']


def _sim(th, seed):
    return W.simulate(th, seed=seed)


def pct(v):
    return [float(np.percentile(v, q)) for q in (10, 50, 90)]


def run(n, version):
    priors = W.PRIORS if version == 'v1' else W.PRIORS_V2
    ths = MC.as_rows(MC.draw_prior(priors, n, master=7))
    outs = MC.monte_carlo(_sim, ths, MC.matched_seeds(n, 0))
    O = {k: 100 * np.array([o[k] for o in outs]) for k in outs[0]}
    res = dict(n=n, version=version, provenance=MC.provenance(design='random', master=7, reseed=0), tests={})

    # ---- India
    b = DATA['India']['age_aligned']['bands']
    d = DATA['India']['age_aligned']['derived']
    tg = {'oos_7_14': d['oos_7_14'], 'oos_15_17': d['oos_15_17']}
    tol = {k: max(1.5, .2 * v) for k, v in tg.items()}
    ok = MC.abc_accept(O, tg, tol)
    obs = {
        'neither_share_oos_7_14': 100 * b['7_14']['neither'] / d['oos_7_14'],
        'neither_share_oos_15_17': 100 * b['15_17']['neither'] / d['oos_15_17'],
        'neither_share_oos': 100 * b['6_17']['neither'] / d['oos_6_17'],
        'both_7_14': b['7_14']['school_and_work'],
        'both_15_17': b['15_17']['school_and_work'],
        'both': b['6_17']['school_and_work'],
    }
    e = dict(targets=tg, tolerances=tol, accepted=int(ok.sum()), observed=obs, predicted={})
    if ok.sum() >= 5:
        for k in obs:
            e['predicted'][k] = pct(O[k][ok])
        e['posterior'] = {p: pct(np.array([t[p] for t in ths])[ok]) for p in W.PRIORS}
    res['tests']['India'] = e

    # ---- India, second specification: also match the school-and-work share (the thing the first specification fails on),
    # so that the composition of the out-of-school becomes the untouched test. If too few worlds reach it, loosen every
    # tolerance by 2x and 3x and report the ladder, so "the model cannot get there" is a number rather than a shrug.
    tg3 = dict(tg, both=b['6_17']['school_and_work'])
    e3 = dict(targets=tg3, ladder=[], observed={k: obs[k] for k in obs if k.startswith('neither')}, predicted={})
    for mult in (1, 2, 3):
        tol3 = {k: mult * v for k, v in dict(tol, both=1.0).items()}
        ok3 = MC.abc_accept(O, tg3, tol3)
        e3['ladder'].append(dict(multiplier=mult, tolerances=tol3, accepted=int(ok3.sum())))
        if ok3.sum() >= 30 and not e3['predicted']:
            e3.update(multiplier=mult, tolerances=tol3, accepted=int(ok3.sum()))
            for k in e3['observed']:
                e3['predicted'][k] = pct(O[k][ok3])
            e3['posterior'] = {p: pct(np.array([t[p] for t in ths])[ok3]) for p in W.PRIORS}
    e['share_of_prior_worlds_reaching_overlap_target'] = float((O['both'] <= 1.0 + tg3['both']).mean())
    e['overlap_among_matched_worlds_p10_p50_p90'] = e['predicted']['both'] if e['predicted'] else None
    res['tests']['India_with_overlap'] = e3

    # ---- Kyrgyzstan
    kk = DATA['Kyrgyzstan']['age_aligned']
    o = kk['oos_rate_by_level']
    tg = {'oos_prim': o['primary'], 'oos_lower': o['lower_secondary'], 'oos_upper': o['upper_secondary']}
    tol = {k: max(1.0, .2 * v) for k, v in tg.items()}
    ok = MC.abc_accept(O, tg, tol)
    e = dict(targets=tg, tolerances=tol, accepted=int(ok.sum()),
             upper_bounds={'both_7_14': 38.4, 'cl': kk['child_labour_5_17_broad']}, predicted={})
    if ok.sum() >= 5:
        for k in ('both_7_14', 'cl', 'neither_share_oos', 'oos_7_14'):
            e['predicted'][k] = pct(O[k][ok])
        e['posterior'] = {p: pct(np.array([t[p] for t in ths])[ok]) for p in W.PRIORS}
    res['tests']['Kyrgyzstan'] = e
    return res


def verdict_range(p, x):
    v = 'pass' if p[0] <= x <= p[2] else 'fail'
    return v + (' (weak: the range spans %d points)' % round(p[2] - p[0]) if p[2] - p[0] > 50 else '')


def report(results):
    L = ['# Age-aligned survey tests: India and Kyrgyzstan', '',
         'Generated by `python engine/childworld_agealigned.py`. Matching targets and test targets come from the same '
         'survey on the same age bands (inputs and links in `engine/data/asia_school_work.json`, `age_aligned`). Worlds '
         'are random draws from the priors (master seed 7, the same rule as `childworld_mc.py`, but a different number of draws, so not the same worlds); kept if within tolerance of every target. Predictions '
         'are medians with 10-90% ranges over kept worlds. A test passes if the observed value lies inside the 10-90% range.', '']
    for res in results:
        v = res['version']
        L += [f"## Priors {v}" + (' (default)' if v == 'v1' else ' (hazardous-share box widened after the first India test)'), '']
        e = res['tests']['India']
        L += [f"### India, PLFS 2018/19", '',
              f"Matched: out-of-school 7-14 = {e['targets']['oos_7_14']}% (+/-{e['tolerances']['oos_7_14']:.1f}), "
              f"15-17 = {e['targets']['oos_15_17']}% (+/-{e['tolerances']['oos_15_17']:.1f}). Worlds kept: {e['accepted']} of {res['n']:,}.", '']
        if e['predicted']:
            L += ['| Test (not matched) | Observed | Predicted median [10-90] | Result |', '|---|---:|---:|---|']
            lab = {'neither_share_oos_7_14': 'Out-of-school 7-14 who are neither in school nor working (%)',
                   'neither_share_oos_15_17': 'Out-of-school 15-17 who are neither (%)',
                   'neither_share_oos': 'Out-of-school 6-17 who are neither (%)',
                   'both_7_14': 'Share of 7-14s in school and working (%)',
                   'both_15_17': 'Share of 15-17s in school and working (%)',
                   'both': 'Share of 6-17s in school and working (%)'}
            for k, name in lab.items():
                p = e['predicted'][k]
                L.append(f"| {name} | {e['observed'][k]:.1f} | {p[1]:.1f} [{p[0]:.1f}-{p[2]:.1f}] | {verdict_range(p, e['observed'][k])} |")
        else:
            L.append('Too few worlds kept to test.')
        L.append('')
        e = res['tests']['India_with_overlap']
        L += ['### India, second specification: also matching the school-and-work share', '',
              f"Matched: the same two out-of-school targets plus school-and-work among 6-17s = {e['targets']['both']}%. "
              f"Only {100 * res['tests']['India']['share_of_prior_worlds_reaching_overlap_target']:.0f}% of prior worlds have school-and-work "
              'that low at all. Worlds kept as the tolerances loosen (tolerance multiplier: worlds kept of ' f"{res['n']:,}): " +
              ', '.join(f"x{r['multiplier']}: {r['accepted']}" for r in e['ladder']) + '.', '']
        if e['predicted']:
            L += [f"Tested at tolerance x{e['multiplier']} ({e['accepted']} worlds).", '',
                  '| Test (not matched) | Observed | Predicted median [10-90] | Result |', '|---|---:|---:|---|']
            for k, name in (('neither_share_oos_7_14', 'Out-of-school 7-14 who are neither (%)'), ('neither_share_oos_15_17', 'Out-of-school 15-17 who are neither (%)'),
                            ('neither_share_oos', 'Out-of-school 6-17 who are neither (%)')):
                p = e['predicted'][k]
                L.append(f"| {name} | {e['observed'][k]:.1f} | {p[1]:.1f} [{p[0]:.1f}-{p[2]:.1f}] | {verdict_range(p, e['observed'][k])} |")
            po = e['posterior']
            L += ['', 'What must be true there (median [10-90]): ' + '; '.join(f"{k} {v[1]:.2f} [{v[0]:.2f}-{v[2]:.2f}]" for k, v in po.items() if k in ('y_med', 'w_child', 'compat', 'v0', 'neither', 'girl_care')) + '.']
        else:
            L.append('Fewer than 30 worlds reach all three targets even at 3x tolerance: the model, as built, does not produce a country with this little out-of-school AND this little overlap. No composition test is possible.')
        L.append('')
        e = res['tests']['Kyrgyzstan']
        L += [f"### Kyrgyzstan, MICS6 2018", '',
              f"Matched: out-of-school primary {e['targets']['oos_prim']}%, lower secondary {e['targets']['oos_lower']}%, upper "
              f"secondary {e['targets']['oos_upper']}%. Worlds kept: {e['accepted']} of {res['n']:,}.", '']
        if e['predicted']:
            L += ['| Quantity | Survey (broader work concept, upper bound) | Predicted median [10-90] | Relation |', '|---|---:|---:|---|']
            for k, name in (('both_7_14', 'Share of 7-14s in school and working (%); DOL 38.4, definition unconfirmed'),
                            ('cl', 'Child labour, economic definition (%); MICS 26.7 for 5-17 includes chores')):
                p = e['predicted'][k]
                ub = e['upper_bounds'][k]
                L.append(f"| {name} | {ub} | {p[1]:.1f} [{p[0]:.1f}-{p[2]:.1f}] | " +
                         ('model below the bound, as expected for a narrower definition' if p[2] <= ub else
                          'range straddles the bound: the data do not discriminate' if p[0] <= ub else 'model ABOVE the bound: a real conflict') + ' |')
        else:
            L.append('Too few worlds kept.')
        L.append('')
    L += ['## What this does and does not show', '',
          '* The India test now uses one survey, one definition (economic activity only; chores excluded, so domestic care '
          'sits in "neither", which is what state D represents) and the same age bands for matching and testing.',
          '* Kyrgyzstan cannot be tested as a point prediction from what was retrievable: the survey work concept is broader '
          'than the model\'s, the age bands follow school levels, and the 38.4% has no definition on the page that reports it.',
          '* Unresolved items are listed in `data/asia_school_work.json` under `age_aligned.unresolved`.']
    open(os.path.join(OUT, 'childworld_agealigned.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--worlds', type=int, default=20000)
    ap.add_argument('--priors', default='v1', choices=['v1', 'v2', 'both'])
    ap.add_argument('--report-only', action='store_true', help='rebuild the .md from the stored .json without simulating')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.report_only:
        report(json.load(open(os.path.join(OUT, 'childworld_agealigned.json')))); sys.exit(0)
    results = [run(a.worlds, v) for v in (('v1', 'v2') if a.priors == 'both' else (a.priors,))]
    json.dump(results, open(os.path.join(OUT, 'childworld_agealigned.json'), 'w'), indent=1)
    report(results)
