"""Score every frozen forecast in ledger.csv against the observed months now in data/observed.csv. Nothing is refitted.

A ledger row is scored once its target month appears in observed.csv. Benchmarks: naive_same_month (frozen in the same
ledger, for every row) and, for the blind engine forecast, also its own frozen naive (blind_naive_2024).
Paired difference = |model error| - |benchmark error| per month, so negative means the model was closer.
Usage: python score.py [--ledger FILE] [--observed FILE] [--out DIR]
"""
import argparse, csv, math, os
import numpy as np
import models as M


def parse(label):
    y, m = map(int, label.split('-')); return M.idx(y, m)


def score(ledger_path=os.path.join(M.HERE, 'ledger.csv'), observed_path=M.OBSERVED):
    obs = M.load_observed(observed_path)
    rows = list(csv.DictReader(open(ledger_path, newline='')))
    fc = {}
    for r in rows:
        fc.setdefault(r['model'], {})[parse(r['target_month'])] = float(r['forecast'])
    cutoff = {r['model']: parse(r['data_cutoff'].split('..')[-1]) for r in rows}
    out = []
    plan = [(m, 'naive_same_month') for m in fc if m != 'naive_same_month'] + [('blind_seasonal_2024_spread11', 'blind_naive_2024')]
    plan = [(m, b) for m, b in plan if m in fc and b in fc and m != 'blind_naive_2024']
    for m, b in plan:
        ts = sorted(t for t in fc[m] if t in obs and t > cutoff[m] and t in fc[b])
        if not ts:
            continue
        em = np.array([abs(fc[m][t] - obs[t]) for t in ts]); eb = np.array([abs(fc[b][t] - obs[t]) for t in ts]); d = em - eb
        n = len(ts)
        t_stat = float(d.mean() / (d.std(ddof=1) / math.sqrt(n))) if n >= 3 and d.std(ddof=1) > 0 else None
        out.append(dict(model=m, benchmark=b, n_months=n, first_target=M.label(ts[0]), last_target=M.label(ts[-1]), mae=float(em.mean()),
                        benchmark_mae=float(eb.mean()), mean_diff=float(d.mean()), months_closer=int((d < 0).sum()), paired_t=t_stat))
    return out


def fmt(x, p=2):
    return 'n/a' if x is None else f'{x:.{p}f}'


def write(out, outdir):
    os.makedirs(outdir, exist_ok=True)
    if not out:
        msg = 'nothing to score yet: no ledger target month has an observation in data/observed.csv.'
        open(os.path.join(outdir, 'scoreboard.md'), 'w').write('# Scoreboard\n\n' + msg + '\n')
        return msg
    cols = ['model', 'benchmark', 'n_months', 'first_target', 'last_target', 'mae', 'benchmark_mae', 'mean_diff', 'months_closer', 'paired_t']
    with open(os.path.join(outdir, 'scoreboard.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(out)
    L = ['# Scoreboard', '', 'Mean absolute error in percentage points. Negative mean difference = closer than the benchmark. '
         'Paired t is blank below 3 months. With so few months, treat every row as descriptive.', '',
         '| Model | Benchmark | Months | Targets | MAE | Benchmark MAE | Mean diff | Months closer | Paired t |', '|---|---|---:|---|---:|---:|---:|---:|---:|']
    for r in out:
        L.append(f"| {r['model']} | {r['benchmark']} | {r['n_months']} | {r['first_target']} to {r['last_target']} | {r['mae']:.2f} | "
                 f"{r['benchmark_mae']:.2f} | {r['mean_diff']:+.2f} | {r['months_closer']}/{r['n_months']} | {fmt(r['paired_t'])} |")
    open(os.path.join(outdir, 'scoreboard.md'), 'w').write('\n'.join(L) + '\n')
    return '\n'.join(L)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', default=os.path.join(M.HERE, 'ledger.csv'))
    ap.add_argument('--observed', default=M.OBSERVED)
    ap.add_argument('--out', default=os.path.join(M.HERE, 'results'))
    a = ap.parse_args()
    print(write(score(a.ledger, a.observed), a.out))
