"""Training-only multi-seed matching. Protocol: tune_protocol.json.
Run python engine/history_match.py 256. Writes beside script, from any cwd.
Post-2015 rows are reported but never used to accept or rank settings.
"""
import importlib, json, os, sys
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import warnings; warnings.filterwarnings('ignore')
from eduengine import ledger as LG, measure as M

HERE = Path(__file__).resolve().parent
COUNTRIES = ['cambodia', 'philippines', 'china']
SPACE = {
    'kappa': (6.0, 16.0),          # S2 value of a child's future income
    'poverty_line': (0.5, 1.8),    # S4 income below which child earnings are needed
    'h_max': (0.1, 0.6),           # S5 withholding at a full pay gap
    'p_own': (0.02, 0.10),         # own-teacher tutoring price
    'p_firm': (0.03, 0.15),        # commercial tutoring price
    'tut_effect': (0.15, 0.50),    # learning gain from tutoring
    'r0': (0.0, 0.08),             # remedial demand
    'priv_quality': (0.95, 1.30),  # private-school quality premium
    'priv_wage': (0.5, 1.5),       # private teachers' wage
}
TRAIN_UNTIL = 2015
TRAIN_SEEDS = (0, 1)
EXCLUDED_STATUS = {'unverified', 'stylised'}


def lhs(n, seed=32):
    if n < 1: raise ValueError('sample count must be positive')
    r = np.random.default_rng(seed)
    cols = []
    for lo, hi in SPACE.values():
        u = (r.permutation(n) + r.random(n)) / n
        cols.append(lo + u * (hi - lo))
    return [dict(zip(SPACE, row)) for row in np.array(cols).T]


def training_metrics(rows):
    """The sole selection gate; test rows cannot affect these metrics."""
    eligible = [r for r in rows if r['year'] <= TRAIN_UNTIL and r['status'] not in EXCLUDED_STATUS]
    if not eligible: raise ValueError('no eligible training observations')
    imp = [abs(r['gap']) / r['tol'] if np.isfinite(r['gap']) else float('inf') for r in eligible]
    groups = {}
    for row, v in zip(eligible, imp):
        groups.setdefault(row['indicator'], []).append(0.5 * v * v if v <= 1 else v - 0.5)
    ordered = sorted(imp, reverse=True)
    return dict(second_max=ordered[min(1, len(ordered)-1)] if all(np.isfinite(imp)) else float('inf'),
                loss=float(np.mean([np.mean(v) for v in groups.values()])),
                mean_imp=float(np.mean(imp)), indicators=sorted(groups))


def outputs(E):
    R, t0 = E.R, E.p['start_year']
    o = {}
    for Y in (2010, 2017, 2023):
        t = Y - t0
        if 0 <= t < len(R.get('tut_by_grade', [])):
            o[f'tutoring_by_grade_{Y}'] = [round(float(x), 3) for x in R['tut_by_grade'][t][:12]]
            o[f'own_teacher_share_{Y}'] = round(float(R['own_share'][t]), 3)
            o[f'tutoring_by_quintile_{Y}'] = [round(float(x), 3) for x in R['tut_by_q'][t]]
    W = R.get('implied_wedge')
    if W and 0 <= 2010-t0 < len(W):
        o['implied_wedge_2010'] = [None if not np.isfinite(x) else round(float(x), 2) for x in W[2010-t0]]
    o['youth_unemployment_2019'] = round(M.youth_unemployment(E, 2019), 3)
    return o


def job(a):
    country, prm, seeds = a
    if isinstance(seeds, int): seeds = (seeds,)
    C = importlib.import_module(f'countries.{country}')
    metrics, ledgers, first = [], [], None
    for seed in seeds:
        E = C.make(seed=seed, anchor_until=TRAIN_UNTIL, **prm); E.run()
        rows = LG.ledger(E, country, TRAIN_UNTIL)
        metrics.append(training_metrics(rows)); ledgers.append(rows)
        if first is None: first = outputs(E)
    averaged = []
    for rs in zip(*ledgers):
        r = rs[0]; mv = float(np.mean([x['model'] for x in rs]))
        averaged.append((r['indicator'], r['year'], r['value'], mv,
                         bool(np.isfinite(mv) and abs(mv-r['value']) <= r['tol']), r['split']))
    return dict(country=country, prm=prm, seed=seeds[0], seeds=list(seeds),
                second_max=max(x['second_max'] for x in metrics),
                train_loss=float(np.mean([x['loss'] for x in metrics])),
                mean_imp=float(np.mean([x['mean_imp'] for x in metrics])),
                training_indicators=metrics[0]['indicators'], rows=averaged, out=first)


def rank_runs(runs):
    kept = [r for r in runs if r['second_max'] <= 2.5]
    use = sorted(kept or runs, key=lambda r: (r['train_loss'], r['second_max']))
    return kept, use if kept else use[:5]


def main(n=256):
    designs = lhs(n)
    tasks = [(c, d, TRAIN_SEEDS) for c in COUNTRIES for d in designs]
    with Pool(min(8, os.cpu_count() or 1)) as pool:
        res = []
        for i, result in enumerate(pool.imap(job, tasks), 1):
            res.append(result)
            if i % 32 == 0: print(f'{i}/{len(tasks)} settings evaluated', flush=True)
    L = [f'CONTEXT MAP ({n} samples per country; training <=2015 ONLY; seeds {TRAIN_SEEDS}; second-largest training gap <=2.5 tolerances on each seed)',
         'Rank: indicator-balanced Huber loss. Unverified/stylised observations excluded from selection.',
         'Post-2015 rows: retrospective evaluation conditional on coded paths/events, not blind predictions.', '']
    J = {}
    for c in COUNTRIES:
        kept, use = rank_runs([x for x in res if x['country'] == c])
        J[c] = dict(kept=len(kept), samples=n, train_until=TRAIN_UNTIL, training_seeds=list(TRAIN_SEEDS),
                    design_seed=32, selection='training-only indicator-balanced Huber loss; multi-seed acceptance', runs=use)
        L.append(f'=== {c}: {len(kept)} of {n} not ruled out on training observations' + ('' if kept else ' (NONE: least-loss settings shown; unmatched)'))
        for k in SPACE:
            v = [x['prm'][k] for x in use]
            L.append(f'    {k:13s} {min(v):6.3f} - {max(v):6.3f} (searched {SPACE[k][0]} - {SPACE[k][1]})')
        best = use[0]
        L.append(f'    training loss {best["train_loss"]:.4f}; worst-seed second-max {best["second_max"]:.3f}')
        L.append('    training indicators: ' + ', '.join(best['training_indicators']))
        for ind, Y, v, mv, ok, split in best['rows']:
            L.append(f'      {ind:24s} {Y} observed {v:.3f} model {mv:.3f} {"ok" if ok else "TICKET"} ({split})')
        L.append('')
    dest = HERE / 'results'; dest.mkdir(exist_ok=True)
    (dest/'context_map.txt').write_text('\n'.join(L)+'\n')
    (dest/'context_map.json').write_text(json.dumps(J, default=float, allow_nan=False))
    print('\n'.join(L))


if __name__ == '__main__': main(int(sys.argv[1]) if len(sys.argv)>1 else 256)
