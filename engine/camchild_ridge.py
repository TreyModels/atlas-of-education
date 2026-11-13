"""Cambodia child labour: does anything survive the calibration ridge?

The camchild world tunes six school-value constants (vPrim, vLow, vUp for Phnom Penh and the countryside) to three
national out-of-school targets (UNESCO UIS 2024: 3.7 / 17.6 / 48.9). Three constants are therefore set by an assumed
regional split, not by data (docs/facts_register.md). This script recalibrates the model under several defensible
splits and two target sets, then asks which results are robust:
  * the child labour level (the model's one external test: ~10.7% in the 2012 survey);
  * the effect of each curated policy on national child labour, and the ranking of policies.

Variants
  current      the shipped constants (implied rural/urban out-of-school ratios ~2.0 / 2.5 / 1.6)
  cses2012     ratios from CSES 2012 (All in School country study, tables 2-3, 2-6): primary 14.4/7.6 = 1.9,
               lower secondary 13.3/3.5 = 3.8; upper secondary not reported, kept at 1.6
  flat         a much weaker urban advantage: 1.3 / 1.5 / 1.2
  steep        a much stronger one: 2.5 / 5.0 / 2.5
  census2019   targets from the 2019 census attendance by age (6-11: 9.4, 12-14: 8.4, 15-17: 32.4, derived as
               100 - attendance), with the cses2012 ratios. Age groups, not levels, so only indicative: the two
               target sets disagree by a factor of two at lower secondary, which is itself the finding to check.

Run from engine/:  python camchild_ridge.py  -> results/camchild_ridge.{json,md}
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import camchild as CC
import mc as MC

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
UIS = (.0369, .1759, .4894)
CENSUS = (.094, .084, .324)
VARIANTS = {
    'current': None,
    'cses2012': (UIS, (1.9, 3.8, 1.6)),
    'flat': (UIS, (1.3, 1.5, 1.2)),
    'steep': (UIS, (2.5, 5.0, 2.5)),
    'census2019': (CENSUS, (1.9, 3.8, 1.6)),
}
SCEN = [('Thai border closes', dict(thaiOpen=0)), ('Factory-only ban', dict(ban=1)),
        ('Garment boom', dict(garmentBoom=.4)), ('Cash for the poorest', dict(cash=.03)),
        ('Schools as protection', dict(protection=.8, leftSupport=.8, harvest=.6, bridging=.7, feeding=.6)),
        ('The floor binds', dict(floorRise=.8))]
VK = ('vPrim', 'vLow', 'vUp')


def last(R, g, k, i=None):
    rows = R['rows'][-4:]
    return sum((r[g][k] if i is None else r[g][k][i]) for r in rows) / len(rows)


def logit(p):
    p = min(max(p, 1e-4), 1 - 1e-4)
    return math.log(p / (1 - p))


def calibrate(targets, ratios, iters=10):
    over = {k: {v: CC.REGIONS[k][v] for v in VK} for k in ('pp', 'rural')}
    for it in range(iters):
        R = CC.simulate(over=over)
        err = 0.0
        for i, vk in enumerate(VK):
            o_pp, o_r, o_all = last(R, 'pp', 'oos', i), last(R, 'rural', 'oos', i), last(R, 'all', 'oos', i)
            # regional targets: keep the model's own regional weights w (from o_all = w o_pp + (1-w) o_r)
            w = (o_all - o_r) / (o_pp - o_r) if abs(o_pp - o_r) > 1e-6 else .22
            w = min(max(w, .05), .5)
            t_pp = targets[i] / (w + (1 - w) * ratios[i]); t_r = ratios[i] * t_pp
            for reg, o, t in (('pp', o_pp, t_pp), ('rural', o_r, t_r)):
                over[reg][vk] += 0.35 * (logit(o) - logit(t))       # higher school value -> fewer out of school
                err = max(err, abs(o - t))
        if err < .004:
            break
    R = CC.simulate(over=over)
    return over, R, err


def profile(over):
    base = CC.simulate(over=over)
    out = dict(cl=last(base, 'all', 'cl'), cl_pp=last(base, 'pp', 'cl'), cl_rural=last(base, 'rural', 'cl'),
               oos={g: [last(base, g, 'oos', i) for i in range(3)] for g in ('pp', 'rural', 'all')}, effects={})
    for name, pol in SCEN:
        R = CC.simulate(over=over, policy=pol)
        out['effects'][name] = last(R, 'all', 'cl') - out['cl']
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for name, spec in VARIANTS.items():
        if spec is None:
            over = {k: {v: CC.REGIONS[k][v] for v in VK} for k in ('pp', 'rural')}; err = None
        else:
            over, _, err = calibrate(*spec)
        res[name] = dict(over=over, calib_err=err, **profile(over))
        print(name, f"cl {100 * res[name]['cl']:.1f}", {k: round(100 * v, 2) for k, v in res[name]['effects'].items()}, flush=True)
    res['_seeds'] = seed_check(res)
    json.dump(res, open(os.path.join(OUT, 'camchild_ridge.json'), 'w'), indent=1)
    report(res)


SEEDS = (1, 2, 3, 4)


def _cl(seed, policy, over=None):
    """National child labour (mean of the last four years) for one seed; module level so the manager can parallelise it."""
    return last(CC.simulate(seed=seed, over=over, policy=policy), 'all', 'cl')


def _sim_for(over):
    return lambda seed, policy: (seed, policy, over)


def _run(args):
    seed, policy, over = args
    return _cl(seed, policy, over)


def seed_check(res, variants=('current', 'census2019')):
    """Effects of every policy on seeds 1-4, on matched random numbers (mc.paired_effects), for two variants.
    Returns the per-seed effects as before; the interval and sign rule live in mc.summarize."""
    out = {}
    pol = dict(SCEN)
    for v in variants:
        eff = MC.paired_effects(_sim_for(res[v]['over']), pol, SEEDS, _run, workers=1)
        out[v] = {name: eff['_raw'][name] for name, _ in SCEN}
    return out


def rank(eff):
    return [k for k, _ in sorted(eff.items(), key=lambda kv: kv[1])]


def report(res):
    seeds = res.get('_seeds', {})
    res = {k: v for k, v in res.items() if not k.startswith('_')}
    names = list(res)
    L = ['# Cambodia child labour: robustness across the calibration ridge', '',
         'Generated by `python engine/camchild_ridge.py` (Python twin, seed 7, 6,000 children, last four of twelve years). '
         'Each variant recalibrates the six school-value constants to its own targets and regional split, then reruns '
         'the curated policies. See the module docstring for variants and sources.', '',
         '| | ' + ' | '.join(names) + ' |', '|---|' + '---:|' * len(names)]
    row = lambda lab, f: L.append(f'| {lab} | ' + ' | '.join(f(res[n]) for n in names) + ' |')
    for i, lev in enumerate(('primary', 'lower sec.', 'upper sec.')):
        row(f'Out of school, {lev} (all / PP / rural, %)',
            lambda r, i=i: f"{100 * r['oos']['all'][i]:.1f} / {100 * r['oos']['pp'][i]:.1f} / {100 * r['oos']['rural'][i]:.1f}")
    row('Constants vPrim / vLow / vUp, Phnom Penh', lambda r: ' / '.join(f"{r['over']['pp'][k]:.2f}" for k in VK))
    row('Constants vPrim / vLow / vUp, countryside', lambda r: ' / '.join(f"{r['over']['rural'][k]:.2f}" for k in VK))
    row('**Child labour, national (%)** (survey 2012: 10.7)', lambda r: f"**{100 * r['cl']:.1f}**")
    row('Child labour PP / countryside (%)', lambda r: f"{100 * r['cl_pp']:.1f} / {100 * r['cl_rural']:.1f}")
    for name, _ in SCEN:
        row(f'Effect: {name} (pts)', lambda r, name=name: f"{100 * r['effects'][name]:+.2f}")
    L.append('')
    L += ['**Policy ranking (most child labour reduced first):**', '']
    for n in names:
        L.append(f"- {n}: " + ' > '.join(rank(res[n]['effects'])))
    # robustness verdicts
    L += ['', '## Verdicts', '']
    for name, _ in SCEN:
        vals = [res[n]['effects'][name] for n in names] + [x for v in seeds.values() for x in v[name]]
        sign = ('always lowers child labour' if max(vals) < 0 else 'always raises child labour' if min(vals) > 0
                else 'effect on child labour has no established sign')
        L.append(f"- **{name}**: {sign} across variants and seeds; range {100 * min(vals):+.2f} to "
                 f"{100 * max(vals):+.2f} pts.")
    tops = {rank(res[n]['effects'])[0] for n in names}
    cls = [100 * res[n]['cl'] for n in names]
    L += [f"- Most effective policy in every variant: {', '.join(sorted(tops))}" + (' (robust).' if len(tops) == 1 else ' (NOT robust).'),
          f"- National child labour ranges {min(cls):.1f}-{max(cls):.1f}% across variants, against 10.7% in the 2012 survey."]
    if seeds:
        L += ['', '## Seed noise (effects in pts on seeds ' + ', '.join(map(str, SEEDS)) + '; the table above uses seed 7)', '',
              '| Policy | ' + ' | '.join(seeds) + ' |', '|---|' + '---|' * len(seeds)]
        for name, _ in SCEN:
            L.append(f'| {name} | ' + ' | '.join(', '.join(f"{100 * x:+.2f}" for x in seeds[v][name]) for v in seeds) + ' |')
    L += ['', '## What this establishes', '',
          '1. **The child labour gap is not a calibration-ridge problem.** Every variant gives about 14%, even when the '
          'out-of-school targets are roughly halved (census2019). The school-value constants do not set the level. '
          'The work side does: child earnings, the taste for work, and the 35% hazardous share applied to 15-17s. A '
          'retune aimed at 10.7% must free those, and the 2012 survey must be put on the same definition as the model.',
          '2. **Schools as protection ranks first everywhere**, but its size comes from placeholder magnitudes '
          '(TODO: Bjørn). It is robust to the calibration ridge, not to those magnitudes.',
          '3. **Cash and the factory-only ban lower child labour in every variant and seed.** Their size varies by a '
          'factor of 1.5-2.5.',
          '4. **The Thai border closure and the garment boom have no established sign.** Both are within seed noise and '
          'flip across variants. The interface should not present a direction for them without the 30-seed bands.',
          '5. **The targets disagree.** UNESCO UIS 2024 puts lower-secondary out-of-school at 17.6%. The 2019 census '
          'attendance gives about 8.4% for ages 12-14. Definitions differ: UIS counts by level and the census by age, '
          'among other differences. That observation equation must be settled before any retune.']
    open(os.path.join(OUT, 'camchild_ridge.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
