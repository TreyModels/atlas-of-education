"""Monte Carlo for relfloor: which structures fit Philippine history, and what
does each predict for the household-level observables H2 names?

Acceptance (history, all must hold):
  A1 completion 2000 in [0.57, 0.67]           (paper: about 62%)
  A2 completion 2024 in [0.68, 0.78]           (paper: about 73%)
  A3 bottom-40% completion 2000 in [0.30, 0.52]; top-60% in [0.62, 0.85]
     (late-1990s APIS: poorest third ~40%, non-poor 70-75%)
  A4 no collapse at K-12: completion 2018 >= completion 2015 - 0.05
Predictions read from accepted draws:
  P1 change in Q3+ completion 2024->2035 when the RELATIVE premium falls 40%
  P2 same when only ABSOLUTE wages compress (relative held)
  P3 share of all exits from the bottom two quintiles, 2024
  P4 share of Q3+ exiters who reroute to another credential, 2024
  P5 K-12 effect on Q1 vs Q5 completion (with vs without reform, 2018)
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from relfloor import simulate, draw, yidx

def accept(r):
    c = r['complete']; bq = r['byq']
    low = bq[yidx(2000), :2].mean(); high = bq[yidx(2000), 2:].mean()
    return (0.57 <= c[yidx(2000)] <= 0.67 and 0.68 <= c[yidx(2024)] <= 0.78
            and 0.30 <= low <= 0.52 and 0.62 <= high <= 0.85
            and c[yidx(2018)] >= c[yidx(2015)] - 0.05)

def q3p(r, yr):
    return r['byq'][yidx(yr), 2:].mean()

def run(n_draws=3000, seed=11):
    rng = np.random.default_rng(seed)
    res = {}
    for S in ['M_HC', 'M_POS', 'M_REL']:
        acc = []
        for i in range(n_draws):
            th = draw(rng, S)
            r = simulate(th, 'hold', n=2500, seed=i)
            if not accept(r):
                continue
            rf = simulate(th, 'fall', n=2500, seed=i)
            r0 = simulate(th, 'hold', n=2500, seed=i, k12=False)
            acc.append({
                'th': th,
                'P1': q3p(rf, 2035) - q3p(rf, 2024),
                'P2': q3p(r, 2035) - q3p(r, 2024),
                'P3': float(r['exit_low_share'][yidx(2024)]),
                'P4': float(r['reroute_q3plus'][yidx(2024)]),
                'P5_q1': float(r['byq'][yidx(2018), 0] - r0['byq'][yidx(2018), 0]),
                'P5_q5': float(r['byq'][yidx(2018), 4] - r0['byq'][yidx(2018), 4]),
                'rel_share': None,
            })
        def band(k):
            v = np.array([a[k] for a in acc])
            return [round(float(np.percentile(v, p)), 3) for p in (5, 50, 95)] if len(v) else None
        res[S] = {'accepted': len(acc), 'rate': len(acc) / n_draws,
                  **{k: band(k) for k in ['P1', 'P2', 'P3', 'P4', 'P5_q1', 'P5_q5']}}
        if acc:
            res[S]['post_b_rel'] = band_th(acc, 'b_rel')
            res[S]['post_gamma'] = band_th(acc, 'gamma')
            res[S]['post_prem0'] = band_th(acc, 'prem0')
    return res

def band_th(acc, k):
    v = np.array([a['th'][k] for a in acc])
    return [round(float(np.percentile(v, p)), 3) for p in (5, 50, 95)]

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    res = run(n)
    here = os.path.dirname(__file__)
    os.makedirs(os.path.join(here, 'results'), exist_ok=True)
    with open(os.path.join(here, 'results', 'relfloor_mc.json'), 'w') as f:
        json.dump(res, f, indent=1)
    lines = ['| | accepted | P1 Q3+ change, relative premium falls | P2 Q3+ change, absolute only | P3 exits from Q1-Q2 | P4 Q3+ exiters rerouting | P5 K-12 effect Q1 | P5 K-12 effect Q5 |',
             '|---|---|---|---|---|---|---|---|']
    for S, d in res.items():
        f = lambda b: '—' if b is None else f'{b[1]:+.3f} [{b[0]:+.3f}, {b[2]:+.3f}]'
        lines.append(f"| {S} | {d['accepted']} ({d['rate']:.1%}) | {f(d.get('P1'))} | {f(d.get('P2'))} | {f(d.get('P3'))} | {f(d.get('P4'))} | {f(d.get('P5_q1'))} | {f(d.get('P5_q5'))} |")
    md = '\n'.join(lines)
    with open(os.path.join(here, 'results', 'relfloor_mc.md'), 'w') as f:
        f.write(md + '\n\n' + json.dumps({S: {k: v for k, v in d.items() if k.startswith('post')} for S, d in res.items()}, indent=1))
    print(md)
    print(json.dumps({S: {k: v for k, v in d.items() if k.startswith('post')} for S, d in res.items()}, indent=1))
