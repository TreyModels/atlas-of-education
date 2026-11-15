"""Recovery experiment: can ABC on this kind of data tell the four theories apart?

For each structure taken as TRUE:
  1. pick K true parameter sets from prior draws that give a plausible completion path
     (they pass the repo's aggregate Cambodia test);
  2. simulate synthetic 'observed' data at the real test's resolution: aggregate completion
     in 2000, 2010 and 2021, plus the five-quintile profile in 2014 and 2021 (13 numbers);
     a fresh random seed, so the synthetic data carry sampling noise;
  3. run ABC rejection with all four structures against it: a prior draw is accepted if each
     of the 13 numbers is within the repo's tolerance of the synthetic value (aggregate:
     +/-.055, +/-.085, +/-.06 for 2000, 2010, 2021; quintiles: +/-.10);
  4. posterior probability of a structure = its share of all accepted draws (equal prior,
     equal number of prior draws per structure).
One bank of prior simulations per structure is simulated once and reused for every dataset.
The true draw itself is removed from the bank for its own dataset.

Interpretation rule, fixed before running: if the diagonal of the confusion matrix is not
clearly above the off-diagonal entries (chance = 0.25), this kind of data cannot tell these
theories apart however well the fitting is done.
"""
import json, os, sys, time
import numpy as np
import structures as S

def build_bank(N, n, seed0=2026):
    bank = {}
    for si, s in enumerate(S.STRUCTS):
        rng = np.random.default_rng([seed0, 99, si])
        ths, vecs = [], np.zeros((N, 13))
        for i in range(N):
            th = S.draw(rng, s)
            r = S.simulate(th, n=n, seed=1_000_003 * (si + 1) + i)
            ths.append(th); vecs[i] = S.summary_vector(r)
        bank[s] = (ths, vecs)
    return bank

def accepted_counts(bank, obs, tol, exclude=None):
    counts = {}
    for s in S.STRUCTS:
        _, vecs = bank[s]
        ok = np.all(np.abs(vecs - obs) <= tol, axis=1)
        if exclude is not None and exclude[0] == s: ok[exclude[1]] = False
        counts[s] = int(ok.sum())
    return counts

def agg_plausible(vec):
    return all(abs(vec[i] - S.AGG[y][0]) <= S.AGG[y][1] for i, y in enumerate(S.STAT_YEARS_AGG))

def run(N=40000, K=10, n=1500, tol_scales=(1.0, 0.5), seed=2026, verbose=True):
    t0 = time.time()
    bank = build_bank(N, n, seed)
    t_bank = time.time() - t0
    tol0 = S.tolerances()
    rng = np.random.default_rng([seed, 5])
    datasets = []
    for si, s in enumerate(S.STRUCTS):
        ths, vecs = bank[s]
        plaus = [i for i in range(N) if agg_plausible(vecs[i])]
        pick = rng.choice(plaus, size=min(K, len(plaus)), replace=False)
        for j, i in enumerate(pick):
            r = S.simulate(ths[i], n=n, seed=77_000_000 + 1000 * si + j)      # fresh seed = new noise
            obs = S.summary_vector(r)
            d = {'true': s, 'bank_index': int(i), 'params': {k: float(v) for k, v in ths[i].items()},
                 'observed': [float(x) for x in obs], 'by_tol': {}}
            for sc in tol_scales:
                c = accepted_counts(bank, obs, tol0 * sc, exclude=(s, int(i)))
                tot = sum(c.values())
                post = {k: (c[k] / tot if tot else None) for k in S.STRUCTS}
                d['by_tol'][str(sc)] = {'counts': c, 'total': tot, 'posterior': post}
            datasets.append(d)
    summary = {}
    for sc in tol_scales:
        key = str(sc)
        mat = {}; hit = {}; ndat = {}; tot_mean = {}; tot_med = {}; zero = {}; weak = {}
        for s in S.STRUCTS:
            ds = [d for d in datasets if d['true'] == s]
            use = [d for d in ds if d['by_tol'][key]['total'] > 0]
            ndat[s] = len(ds); zero[s] = len(ds) - len(use)
            tots = [d['by_tol'][key]['total'] for d in ds]
            tot_mean[s] = float(np.mean(tots)); tot_med[s] = float(np.median(tots))
            weak[s] = int(sum(t < 10 for t in tots))
            mat[s] = {c: (float(np.mean([d['by_tol'][key]['posterior'][c] for d in use])) if use else None)
                      for c in S.STRUCTS}
            h = []
            for d in use:
                p = d['by_tol'][key]['posterior']; m = max(p.values())
                top = [k for k in S.STRUCTS if p[k] == m]
                h.append((1.0 / len(top)) if s in top else 0.0)    # ties share the credit
            hit[s] = float(np.mean(h)) if h else None
        diag = [mat[s][s] for s in S.STRUCTS if mat[s][s] is not None]
        summary[key] = {'confusion_mean_posterior': mat, 'share_true_highest': hit,
                        'n_datasets': ndat, 'n_datasets_zero_accepted': zero,
                        'n_datasets_fewer_than_10_accepted': weak,
                        'mean_accepted_per_dataset': tot_mean, 'median_accepted_per_dataset': tot_med,
                        'mean_diagonal': float(np.mean(diag)) if diag else None,
                        'mean_offdiagonal': float(np.mean([mat[s][c] for s in S.STRUCTS for c in S.STRUCTS
                                                           if s != c and mat[s][c] is not None]))
                        if diag else None}
    return {'config': {'draws_per_structure_in_bank': N, 'datasets_per_true_structure': K,
                       'households': n, 'tolerance_scales': list(tol_scales), 'seed': seed,
                       'liquidity': 'graded', 'structures': S.STRUCTS,
                       'repo_main_run_draws': 24000, 'repo_main_run_households': '1500 screen / 4000 for outputs',
                       'seconds_bank': round(t_bank, 1), 'seconds_total': round(time.time() - t0, 1)},
            'tolerances': [float(x) for x in tol0], 'summary': summary, 'datasets': datasets}

if __name__ == '__main__':
    tiny = '--tiny' in sys.argv
    res = run(N=300, K=2) if tiny else run()
    fn = 'recovery_results_tiny.json' if tiny else 'recovery_results.json'
    os.makedirs(os.path.join(S.HERE, 'results'), exist_ok=True)
    json.dump(res, open(os.path.join(S.HERE, 'results', fn), 'w'), indent=1)
    for k, v in res['summary'].items():
        print('tolerance scale', k)
        for s in S.STRUCTS:
            print(' ', s, {c: (round(x, 3) if x is not None else None) for c, x in v['confusion_mean_posterior'][s].items()},
                  'top:', v['share_true_highest'][s], 'meanN', round(v['mean_accepted_per_dataset'][s], 1))
    print(res['config'])
