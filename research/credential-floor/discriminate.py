"""What would tell the four theories apart? Outputs the current data do not measure.

Step 1. For each structure, keep prior draws that fit the REAL Cambodia targets (the repo's
        aggregate windows plus the UIS quintile profiles of 2014 and 2021, +/-10 points;
        this is relfloor_countries.t_khm_profile, applied with early stopping, which gives
        the same verdict as the full run).
Step 2. For each kept draw, re-simulate the 2021 cohort and compute outputs that the fitted
        targets do not constrain (see OUTPUTS below).
Step 3. For every output and every pair of structures: the AUC of telling one from the other
        (the chance that a random draw of one structure has a higher value than a random draw
        of the other; 0.5 = no separation, folded here to 0.5-1) and a standardised difference
        (difference of means in pooled standard deviations). Overall ranking of an output = its
        mean folded AUC over the six pairs; also the best output for each pair.

Counterfactuals (read in 2021, same households and random numbers as the baseline):
  prem20 / prem40  the relative premium is 20% / 40% lower from 2018 on (so the positional
                   term has had three years to respond); change in completion in 2021.
  transfer         a one-off cash transfer to the bottom 40% in 2021, equal to the full cost of
                   the credential (cost per year x years); it works only through the liquidity
                   constraint, the model has no other income effect.
Ability 'high' means above the median ability of all households in the cohort.
"""
import json, os, sys, time
import numpy as np
from scipy.stats import rankdata
import structures as S

YEAR = 2021
PAIRS = [(a, b) for i, a in enumerate(S.STRUCTS) for b in S.STRUCTS[i + 1:]]
FAMILIES = {'ab_gap': 'Completion gap, high- minus low-ability children, within income quintile',
            'prem20': 'Change in completion if the relative premium falls 20%',
            'prem40': 'Change in completion if the relative premium falls 40%',
            'transfer': 'Change in completion after a one-off transfer to the bottom 40%',
            'noncomp': 'Share of non-completers who are high-ability',
            'reroute': 'Rerouting rate among non-completers, by quintile'}

def by_q(x, mask, q):
    return [float(x[mask & (q == i)].mean()) if (mask & (q == i)).any() else np.nan for i in range(5)]

def outputs(th, n, seed):
    base = S.simulate(th, n=n, seed=seed, until=YEAR, detail_year=YEAR)
    d = base['detail']; stay, q, ab = d['stay'], d['q'], d['ab']
    hi = ab > np.median(ab); out = {}
    for i in range(5):
        m = q == i
        out[f'ab_gap_q{i+1}'] = float(stay[m & hi].mean() - stay[m & ~hi].mean())
    top = q >= 3
    out['ab_gap_top2'] = float(stay[top & hi].mean() - stay[top & ~hi].mean())
    bot = q <= 1
    out['ab_gap_bottom2'] = float(stay[bot & hi].mean() - stay[bot & ~hi].mean())
    for tag, f in (('prem20', 0.8), ('prem40', 0.6)):
        r = S.simulate(th, n=n, seed=seed, until=YEAR, prem_scale=(2018, f))
        dq = r['q'][S.yi(YEAR)] - base['q'][S.yi(YEAR)]
        for i in range(5): out[f'{tag}_dq{i+1}'] = float(dq[i])
        out[f'{tag}_dall'] = float(r['c'][S.yi(YEAR)] - base['c'][S.yi(YEAR)])
    cost = (th['direct'] + th['forgo']) * S.CFG['L']
    r = S.simulate(th, n=n, seed=seed, until=YEAR, transfer=(YEAR, cost))
    dq = r['q'][S.yi(YEAR)] - base['q'][S.yi(YEAR)]
    out['transfer_dq1'] = float(dq[0]); out['transfer_dq2'] = float(dq[1])
    out['transfer_dbottom2'] = float((dq[0] + dq[1]) / 2)
    ex = ~stay
    out['noncomp_highab'] = float((ex & hi).sum() / max(ex.sum(), 1))
    rr = d['reroute']
    for i in range(5):
        m = ex & (q == i)
        out[f'reroute_q{i+1}'] = float(rr[m].mean()) if m.any() else np.nan
    return out

def collect(structure, target, max_draws, max_seconds, seed0=2026):
    si = S.STRUCTS.index(structure)
    rng = np.random.default_rng([seed0, 123, si])
    chk = S.early_checkpoints(); acc = []; tried = 0; t0 = time.time()
    while len(acc) < target and tried < max_draws and time.time() - t0 < max_seconds:
        th = S.draw(rng, structure); tried += 1
        r = S.simulate(th, n=1500, seed=5_000_011 * (si + 1) + tried, until=2021, checkpoints=chk)
        if r is not None: acc.append(th)
    return acc, tried, time.time() - t0

def auc(a, b):
    """P(a > b) + 0.5 P(a = b), by ranks."""
    a, b = np.asarray(a), np.asarray(b)
    r = rankdata(np.concatenate([a, b]))
    return float((r[:len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b)))

def run(target=300, max_draws=400000, max_seconds=120, n=4000):
    t0 = time.time(); res = {}; tried = {}; secs = {}
    for s in S.STRUCTS:
        acc, tried[s], secs[s] = collect(s, target, max_draws, max_seconds)
        res[s] = [outputs(th, n, 9_000_000 + i) for i, th in enumerate(acc)]
    names = list(res[S.STRUCTS[0]][0].keys()) if res[S.STRUCTS[0]] else []
    vals = {s: {k: np.array([o[k] for o in res[s]]) for k in names} for s in S.STRUCTS}
    per_struct = {k: {s: ([float(np.nanpercentile(vals[s][k], p)) for p in (5, 50, 95)] if len(vals[s][k]) else None)
                      for s in S.STRUCTS} for k in names}
    table = []
    for k in names:
        for a, b in PAIRS:
            x, y = vals[a][k], vals[b][k]; x = x[~np.isnan(x)]; y = y[~np.isnan(y)]
            if len(x) < 5 or len(y) < 5: continue
            u = auc(x, y); sp = np.sqrt((x.var(ddof=1) + y.var(ddof=1)) / 2)
            se = float(np.sqrt((len(x) + len(y) + 1) / (12 * len(x) * len(y))))
            table.append({'output': k, 'a': a, 'b': b, 'auc_a_greater': u, 'auc_folded': max(u, 1 - u),
                          'std_diff': float((x.mean() - y.mean()) / sp) if sp > 0 else 0.0,
                          'null_se_auc': se, 'n_a': len(x), 'n_b': len(y)})
    rank = []
    for k in names:
        rows = [t for t in table if t['output'] == k]
        if rows:
            best = max(rows, key=lambda t: t['auc_folded'])
            rank.append({'output': k, 'family': k.split('_')[0] if not k.startswith('ab_gap') else 'ab_gap',
                         'mean_auc_folded': float(np.mean([t['auc_folded'] for t in rows])),
                         'best_pair': [best['a'], best['b']], 'best_auc_folded': best['auc_folded'],
                         'best_std_diff': best['std_diff']})
    rank.sort(key=lambda r: -r['mean_auc_folded'])
    best_by_pair = {}
    for a, b in PAIRS:
        rows = [t for t in table if t['a'] == a and t['b'] == b]
        rows.sort(key=lambda t: -t['auc_folded'])
        best_by_pair[f'{a} vs {b}'] = rows[:3]
    nulls = [t['null_se_auc'] for t in table]
    return {'config': {'target_accepted_per_structure': target, 'households_for_outputs': n,
                       'households_for_fit': 1500, 'max_seconds_per_structure': max_seconds,
                       'year_read': YEAR, 'liquidity': 'graded'},
            'accepted': {s: len(res[s]) for s in S.STRUCTS}, 'draws_tried': tried,
            'acceptance_rate': {s: len(res[s]) / tried[s] for s in S.STRUCTS},
            'seconds': {'per_structure_search': {s: round(secs[s], 1) for s in S.STRUCTS},
                        'total': round(time.time() - t0, 1)},
            'null_se_auc_typical': float(np.median(nulls)) if nulls else None,
            'families': FAMILIES, 'per_structure_5_50_95': per_struct,
            'pair_table': table, 'ranking': rank, 'best_outputs_by_pair': best_by_pair}

if __name__ == '__main__':
    tiny = '--tiny' in sys.argv
    out = run(target=15, max_draws=3000, max_seconds=10, n=1500) if tiny else run()
    fn = 'discriminate_results_tiny.json' if tiny else 'discriminate_results.json'
    os.makedirs(os.path.join(S.HERE, 'results'), exist_ok=True)
    json.dump(out, open(os.path.join(S.HERE, 'results', fn), 'w'), indent=1)
    print(out['accepted'], out['draws_tried'], out['seconds'])
    for r in out['ranking'][:10]: print(r)
