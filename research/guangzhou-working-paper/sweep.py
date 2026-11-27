"""Run from this directory with NumPy and the two bundled model inputs."""
import csv
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import gz_v5

ROOT = Path(__file__).resolve().parent
RANGES = json.loads((ROOT / 'ranges.json').read_text())
N, DRAWS, SEED = 40000, 1024, 27112026


def rates(data, outcome, variable):
    wealth, local = data['logw'], data['hukou']
    low, high = np.quantile(wealth[local], [.4, .6])
    x = data[variable]
    top = x >= np.quantile(x, .8)
    bins = np.searchsorted(np.quantile(x[top], np.arange(1, 10) / 10), x)
    def rate(group):
        return np.mean([outcome[top & local & group & (bins == i)].mean() for i in range(10)])
    return rate(wealth >= high) / rate(wealth <= low)


def joint_ratio(d):
    w, z, t = d['logw'], d['zk'], d['tal']
    low, high = np.quantile(w[d['hukou']], [.4, .6])
    top = z >= np.quantile(z, .8)
    def partition(x):
        return np.searchsorted(np.quantile(x[top], [.2, .4, .6, .8]), x)
    cell = 5 * partition(z) + partition(t)
    def counts(g):
        mask = top & d['hukou'] & g
        return (np.bincount(cell[mask], minlength=25),
                np.bincount(cell[mask & d['uni']], minlength=25))
    nr, ar = counts(w >= high)
    np_, ap = counts(w <= low)
    keep = (nr >= 5) & (np_ >= 5)
    weights = (nr + np_)[keep]
    ratio = np.sum(weights * ar[keep] / nr[keep]) / np.sum(weights * ap[keep] / np_[keep])
    return ratio, weights.sum() / (nr + np_).sum()


def spend(d):
    return (45000 * d['pre'] + 35080 * d['term'] + 20000 * d['hol']
            + 2 * d['p']['FT_COST'] * d['ft']).mean()


def simulate(i):
    design, cohort = np.random.SeedSequence([SEED, i]).spawn(2)
    rng = np.random.default_rng(design)
    p = {key: rng.uniform(*bounds) for key, bounds in RANGES.items()}
    p['HS_TEACH_SD'] = p['TEACH_SD']
    seed = int(cohort.generate_state(1)[0])
    d = gz_v5.run(n=N, seed=seed, **p)
    before = gz_v5.run(n=N, seed=seed, **{**p, 'BAN_RED': 0, 'REBAND': False})
    cutoff = np.sort(d['gk'][d['acad']])[-(N // 10)]
    ordinary = d['acad'] & (d['gk'] >= cutoff)
    gain = d['uni'] & ~ordinary
    loss = ordinary & ~d['uni']
    assert d['uni'].sum() == ordinary.sum() == N // 10
    assert gain.sum() == loss.sum() and not np.any(gain & ~(d['art'] | d['hkr']))
    sizes = np.bincount(d['hs'][d['acad']])
    target = np.where(sizes, np.maximum(1, np.rint(d['p']['TOP_BAND'] * sizes)), 0)
    for key in ('band1', 'band2'):
        assert np.array_equal(np.bincount(d['hs'][d[key]], minlength=len(sizes)), target)
    joint, support = joint_ratio(d)
    return dict(Sstar=joint, support=support, spend_change=spend(d)-spend(before), draw=i, seed=seed, T=rates(d, d['uni'], 'tal'), S=rates(d, d['uni'], 'zk'),
                T_before=rates(before, before['uni'], 'tal'), displaced=int(loss.sum()), **p)


if __name__ == '__main__':
    with ProcessPoolExecutor(4) as pool, (ROOT / 'draws.csv').open('w', newline='') as out:
        for i, result in enumerate(pool.map(simulate, range(DRAWS), chunksize=4)):
            if i == 0:
                writer = csv.DictWriter(out, fieldnames=result)
                writer.writeheader()
            writer.writerow(result)
