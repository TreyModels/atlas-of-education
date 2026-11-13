"""Fit a country pack on observations up to TRAIN_UNTIL, score the rest blind. Run: python fit_country.py cambodia
Grid over S2 kappa, S4 poverty_line and S10 promote_bar (enrolment anchored to UIS completion up to TRAIN_UNTIL).
For the full context map use history_match.py, which supersedes this grid. Results -> results/<country>_fit.txt"""
import itertools, os, sys, importlib
from multiprocessing import Pool
import numpy as np
from eduengine import ledger as LG

TRAIN_UNTIL = 2015
GRID = dict(kappa=[6.0, 9.0, 12.0, 16.0], poverty_line=[0.7, 1.0, 1.4, 1.9], promote_bar=[0.3, 0.55])


def _run(C, over, seed=0):
    E = C.make(seed=seed, **over); E.run(); return E


def train_loss(args):
    country, over = args
    C = importlib.import_module(f'countries.{country}')
    E = _run(C, over)
    rows = [r for r in LG.ledger(E, country, TRAIN_UNTIL) if r['split'] == 'train' and np.isfinite(r['model'])]
    return float(sum((r['gap'] / r['tol']) ** 2 for r in rows))


def main(country):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    C = importlib.import_module(f'countries.{country}')
    combos = [dict(zip(GRID, v)) for v in itertools.product(*GRID.values())]
    with Pool(os.cpu_count() or 1) as pool:
        losses = pool.map(train_loss, [(country, c) for c in combos])
    best = combos[int(np.argmin(losses))]
    base = _run(C, {}); fit = _run(C, best); fit2 = _run(C, best, seed=1)
    L = [f'FIT {country}: grid over {list(GRID)} ({len(combos)} runs), loss on observations <= {TRAIN_UNTIL} only',
         f'best {best}  train loss {min(losses):.1f} (uncalibrated {train_loss((country, {})):.1f})', '']
    for name, E in (('UNCALIBRATED', base), ('FITTED (seed 0)', fit), ('FITTED (seed 1, replication)', fit2)):
        rows = LG.ledger(E, country, TRAIN_UNTIL)
        s = LG.score(rows)
        L += [f'--- {name}: within tolerance  train {s["train"][0]}/{s["train"][1]}  test (blind) {s["test"][0]}/{s["test"][1]}']
        if name.startswith('FITTED (seed 0)'):
            L.append(LG.fmt(rows))
    os.makedirs('results', exist_ok=True)
    open(f'results/{country}_fit.txt', 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'cambodia')
