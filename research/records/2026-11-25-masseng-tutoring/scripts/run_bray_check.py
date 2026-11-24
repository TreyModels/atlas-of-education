"""Demand-mix check: does the ported household-demand block reproduce the seven published Bray et al.
(2016, 2018) Siem Reap patterns in six schools?

This is a demand-mix check on CAMBODIAN schools.  It is NOT Philippine validation and it cannot validate the
massification coupling.  The checker itself is the standalone ``ported/bray_reality_check.py`` (verbatim copy,
branch research/shadow-equations-2026-11-25 @ fdc8da0); this script only runs it in parallel chunks and records
the results.  A draw "passes" a pattern when |value - target| / tolerance <= 1.

Run from the model package directory:
    PYTHONPATH=/root/work/masseng-tutoring/model /root/miniconda3/bin/python run_bray_check.py --draws 50000
"""
import argparse
import json
import os
import sys
import time
from dataclasses import asdict
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RECORD, 'ported'))

import bray_reality_check as B   # noqa: E402


def _chunk(args):
    seed, n = args
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n):
        p = B.draw(rng)
        out = B.simulate_bray(p)
        z = B.zscores(out)
        rows.append({'max_z': max(z.values()), **asdict(p), **out,
                     **{f'z_{k}': float(v) for k, v in z.items()}})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draws', type=int, default=50000)
    ap.add_argument('--chunk', type=int, default=500)
    ap.add_argument('--workers', type=int, default=min(48, os.cpu_count() or 4))
    ap.add_argument('--out', default=os.path.join(RECORD, 'results', 'bray_check.json'))
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    n_chunks = max(1, args.draws // args.chunk)
    jobs = [(20261125 + i, args.chunk) for i in range(n_chunks)]
    t0 = time.time()
    with Pool(processes=min(args.workers, len(jobs))) as pool:
        chunks = pool.map(_chunk, jobs)
    rows = [r for ch in chunks for r in ch]
    rows.sort(key=lambda r: r['max_z'])
    n = len(rows)
    acc = [r for r in rows if r['max_z'] <= 1.0]
    print(f'SIMULATION — Bray demand-mix check, {n} prior draws, {len(acc)} fit all seven patterns '
          f'({100 * len(acc) / n:.2f}%) in {time.time() - t0:.1f}s')
    best = rows[0]
    print('best max_z:', f"{best['max_z']:.3f}")
    for k in B.TARGETS:
        print(f'  {k:22s} target {B.TARGETS[k][0]:.3f} tol {B.TARGETS[k][1]:.3f}  best {best[k]:.3f}')
    res = {
        'label': 'SIMULATION — Bray et al. (2016, 2018) six-school demand-mix check; illustrative priors, rejection '
                 'sampling; NOT Philippine validation',
        'checker_provenance': 'ported/bray_reality_check.py @ research/shadow-equations-2026-11-25 fdc8da0',
        'n_draws': n, 'n_fit_all_seven': len(acc), 'fit_share': len(acc) / n,
        'targets': B.TARGETS, 'best': best, 'top10': rows[:10],
        'accepted_param_ranges': ({k: [float(np.percentile([r[k] for r in acc], 5)),
                                       float(np.percentile([r[k] for r in acc], 95))] for k in B.RANGES}
                                  if acc else {}),
        'wall_seconds': round(time.time() - t0, 2),
    }
    json.dump(res, open(args.out, 'w'), indent=2)
    print('wrote', args.out)


if __name__ == '__main__':
    main()
