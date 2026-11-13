"""Monte Carlo over childworld: which structures produce which school-and-work patterns, and what each Asian
country's numbers imply (scenario discovery + approximate Bayesian computation).

1. Draw many worlds from PRIORS (parameter uncertainty), simulate each (random variation inside), and measure seed
   noise on a subsample by rerunning with new seeds.
2. Classify every world into the four quadrants of lower-secondary out-of-school (>= 10%) x child labour (>= 5%), and
   rank which parameters separate each quadrant from the rest (AUC: 0.5 = no separation, 1 or 0 = perfect).
3. For each country in data/asia_school_work.json, keep the worlds within tolerance of its two headline numbers
   (ABC rejection) and report what must be true there: posterior medians, and the predicted composition of the
   out-of-school (working vs. neither) and of child labour (in school or not).
4. Test: where a survey gives the composition (India, Kyrgyzstan, Bangladesh), compare it with the prediction. The
   composition was NOT used in the matching.
Run from engine/:  python childworld_mc.py [--worlds N]  -> results/childworld_mc.{json,md}
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


def run_worlds(n, seed=7, reseed=0, priors=None):
    """n worlds from the priors (parameter seed `seed`), each with its own simulation noise (see mc.matched_seeds)."""
    ths = MC.as_rows(MC.draw_prior(priors or W.PRIORS, n, master=seed))
    return ths, MC.monte_carlo(_sim, ths, MC.matched_seeds(n, reseed))


def auc(x, y):
    """P(random x from group 1 > random x from group 0); y boolean."""
    a, b = x[y], x[~y]
    if len(a) == 0 or len(b) == 0:
        return float('nan')
    ranks = np.argsort(np.argsort(np.concatenate([a, b]))) + 1
    return float((ranks[:len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b)))


def main(n, version='v1'):
    os.makedirs(OUT, exist_ok=True)
    priors = W.PRIORS if version == 'v1' else W.PRIORS_V2
    ths, outs = run_worlds(n, priors=priors)
    P = {k: np.array([t[k] for t in ths]) for k in W.PRIORS}
    O = {k: 100 * np.array([o[k] for o in outs]) for k in outs[0]}
    # seed noise on the first 300 worlds
    outs2 = MC.monte_carlo(_sim, ths[:300], MC.matched_seeds(300, reseed=1))      # the SAME 300 worlds, new random seeds
    noise = {k: float(np.std([100 * (a[k] - b[k]) for a, b in zip(outs[:300], outs2)]) / np.sqrt(2))
             for k in ('oos_lower', 'cl', 'neither_share_oos', 'both_share_cl')}
    hi_o, hi_c = O['oos_lower'] >= 10, O['cl'] >= 5
    quads = {'A: dropout + child labour': hi_o & hi_c, 'B: dropout, little child labour': hi_o & ~hi_c,
             'C: child labour, little dropout': ~hi_o & hi_c, 'D: neither': ~hi_o & ~hi_c}
    res = dict(n=n, version=version, noise_sd=noise, quadrants={}, countries={},
               provenance=MC.provenance(design='random', master=7, reseed=0))
    for q, mask in quads.items():
        res['quadrants'][q] = dict(share=float(mask.mean()), auc={k: auc(P[k], mask) for k in W.PRIORS},
                                   neither_share_oos=float(np.median(O['neither_share_oos'][mask])) if mask.any() else None,
                                   both_share_cl=float(np.median(O['both_share_cl'][mask])) if mask.any() else None)
    res['global_check'] = dict(oos_among_cl=float(np.median(O['oos_among_cl_5_14'])),
                               oos_among_noncl=float(np.median(O['oos_among_noncl_5_14'])))
    for c, d in DATA.items():
        if d.get('child_labour') is None:
            continue
        to, tc = d['oos_lower'], d['child_labour']
        ok = MC.abc_accept(O, {'oos_lower': to, 'cl': tc}, {'oos_lower': max(2.5, .2 * to), 'cl': max(1.5, .2 * tc)})
        k = int(ok.sum())
        e = dict(oos_lower=to, child_labour=tc, accepted=k)
        if k >= 5:
            e['posterior'] = {p: [float(np.percentile(P[p][ok], q)) for q in (10, 50, 90)] for p in W.PRIORS}
            e['predicted'] = {m: [float(np.percentile(O[m][ok], q)) for q in (10, 50, 90)]
                              for m in ('neither_share_oos', 'work_share_oos', 'boys1417_work_share_oos', 'both_share_cl', 'both', 'oos_upper',
                                        'girls_neither', 'boys_neither')}
        res['countries'][c] = e
    json.dump(res, open(os.path.join(OUT, f'childworld_mc_{version}.json'), 'w'), indent=1)
    report(res)


LAB = dict(y_med='income', w_child='child wage', farm='family farm/business', compat='work fits around school',
           v0='value of school', decay='value decline by level', cost='school cost', neither='value of neither (D)',
           girl_care="girls' care/marriage pull", haz='hazardous share 15-17')


def report(res):
    L = [f"# What produces each school-and-work pattern: Monte Carlo over childworld (priors {res['version']})", '',
         f"Generated by `python engine/childworld_mc.py`. {res['n']:,} worlds drawn from the priors in `childworld.py`, "
         '2,000 children each. Seed noise (SD between reruns of the same world, pts): ' +
         ', '.join(f"{k} {v:.2f}" for k, v in res['noise_sd'].items()) + '.', '',
         '## The four patterns and what separates them', '',
         'AUC per parameter: above 0.5 means the parameter is higher in that pattern than elsewhere; 0.70+ or 0.30- is a '
         'strong separator.', '',
         '| Pattern | Share of worlds | ' + ' | '.join(LAB[k] for k in W.PRIORS) + ' |', '|---|---:|' + '---:|' * len(W.PRIORS)]
    for q, r in res['quadrants'].items():
        cells = [(f"**{v:.2f}**" if (v >= .7 or v <= .3) else f"{v:.2f}") for v in r['auc'].values()]
        L.append(f"| {q} | {100 * r['share']:.0f}% | " + ' | '.join(cells) + ' |')
    L += ['', '| Pattern | Out-of-school who are in state D (not working), median | Child labourers still in school, median |',
          '|---|---:|---:|']
    for q, r in res['quadrants'].items():
        f = lambda v: '' if v is None else f'{v:.0f}%'
        L.append(f"| {q} | {f(r['neither_share_oos'])} | {f(r['both_share_cl'])} |")
    g = res['global_check']
    L += ['', f"Sanity check against the ILO-UNICEF 2024 global estimate (31% of child labourers aged 5-14 out of school "
          f"vs 8% of other children): across all worlds the medians are {g['oos_among_cl']:.0f}% vs {g['oos_among_noncl']:.0f}%.", '',
          '## Countries: what their two headline numbers imply', '',
          'Worlds kept if within max(2.5 pts, 20%) of lower-secondary out-of-school and max(1.5 pts, 20%) of child labour. '
          'Medians with 10-90% ranges.', '',
          '| Country | OOS / CL (%) | Worlds | Out-of-school in state D | Child labourers in school | Income | Child wage | Work fits school | Value of D | Girls\' pull |',
          '|---|---|---:|---|---|---|---|---|---|---|']
    fr = lambda v, s=1: f"{s * v[1]:.0f} [{s * v[0]:.0f}-{s * v[2]:.0f}]"
    fp = lambda v: f"{v[1]:.2f} [{v[0]:.2f}-{v[2]:.2f}]"
    for c, e in sorted(res['countries'].items(), key=lambda kv: -kv[1]['oos_lower']):
        if 'predicted' not in e:
            L.append(f"| {c} | {e['oos_lower']:.1f} / {e['child_labour']:.1f} | {e['accepted']} | too few worlds | | | | | | |")
            continue
        pr, po = e['predicted'], e['posterior']
        L.append(f"| {c} | {e['oos_lower']:.1f} / {e['child_labour']:.1f} | {e['accepted']} | {fr(pr['neither_share_oos'])}% | "
                 f"{fr(pr['both_share_cl'])}% | {fp(po['y_med'])} | {fp(po['w_child'])} | {fp(po['compat'])} | {fp(po['neither'])} | {fp(po['girl_care'])} |")
    L += ['', '## Tests against survey compositions (not used in matching)', '']
    tests = []
    ind = res['countries'].get('India', {})
    if 'predicted' in ind:
        obs = 100 * 4.8 / (4.8 + 1.8)
        p = ind['predicted']['neither_share_oos']
        tests.append(f"- **India** (PLFS 2018/19): {obs:.0f}% of out-of-school 6-17s were neither working nor in school. "
                     f"Predicted {p[1]:.0f}% [{p[0]:.0f}-{p[2]:.0f}]: " + ('**pass**' if p[0] <= obs <= p[2] else '**fail**') + '.')
    kg = res['countries'].get('Kyrgyzstan', {})
    if 'predicted' in kg:
        p = kg['predicted']['both']
        tests.append(f"- **Kyrgyzstan** (US DOL): 38.4% of 7-14s combine work and school. Predicted share of all children "
                     f"in school-and-work {p[1]:.0f}% [{p[0]:.0f}-{p[2]:.0f}]: " + ('**pass**' if p[0] <= 38.4 <= p[2] else '**fail**') + '.')
    bd = res['countries'].get('Bangladesh', {})
    if 'predicted' in bd:
        p = bd['predicted']['boys1417_work_share_oos']
        verdict = ('**pass**' if p[0] <= 68 <= p[2] else '**fail**') + (' but uninformative (the range is too wide to test anything)' if p[2] - p[0] > 50 else '')
        tests.append(f"- **Bangladesh** (MICS 2019): 68% of rural boys aged 14-17 who dropped out were working. Predicted "
                     f"for out-of-school boys 14-17 (national, not rural only) {p[1]:.0f}% [{p[0]:.0f}-{p[2]:.0f}]: " + verdict + '.')
    L += tests or ['- no country with a survey composition matched enough worlds']
    open(os.path.join(OUT, f"childworld_mc_{res['version']}.md"), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--worlds', type=int, default=6000)
    ap.add_argument('--priors', default='v1', choices=['v1', 'v2'])
    a = ap.parse_args(); main(a.worlds, a.priors)
