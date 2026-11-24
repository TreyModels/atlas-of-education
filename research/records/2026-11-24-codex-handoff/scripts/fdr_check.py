#!/usr/bin/env python3
"""Apply BH and BY step-up to all p-values in each declared family; requires valid input p-values."""
import argparse
import csv
import json
import math
from pathlib import Path

def step_up(p, q=0.05, by=False):
    if not 0 < q < 1 or not p or any(not math.isfinite(x) or not 0 <= x <= 1 for x in p):
        raise ValueError('Require non-empty finite p-values in [0,1] and 0 < q < 1')
    m = len(p)
    harmonic = sum(1/i for i in range(1, m+1)) if by else 1
    ranked = sorted(range(m), key=lambda i: (p[i], i))
    passing = [k for k, i in enumerate(ranked, 1) if p[i] <= q*k/(m*harmonic)]
    k = max(passing, default=0)
    return {i for i in ranked[:k]}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path, required=True, help='CSV columns family,link,p; one complete test family per family label')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--q', type=float, default=.05)
    args = ap.parse_args()
    with args.input.open(newline='') as f:
        data = list(csv.DictReader(f))
    if not data or not {'family','link','p'} <= set(data[0]):
        raise ValueError('Require nonempty CSV with family,link,p')
    families = {}
    for row in data:
        if not row['family'] or not row['link']:
            raise ValueError('Blank family/link')
        families.setdefault(row['family'], []).append(row)
    results = []
    for family, rows in sorted(families.items()):
        if len({r['link'] for r in rows}) != len(rows):
            raise ValueError('Duplicate link in family: ' + family)
        p = [float(r['p']) for r in rows]
        bh, by = step_up(p, args.q), step_up(p, args.q, True)
        for i, row in enumerate(rows):
            results.append({'family':family, 'link':row['link'], 'p':p[i], 'bh':int(i in bh), 'by':int(i in by)})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=['family','link','p','bh','by']); w.writeheader(); w.writerows(results)
    print(json.dumps({'families':len(families), 'tests':len(results), 'bh':sum(x['bh'] for x in results), 'by':sum(x['by'] for x in results), 'note':'FDR guarantees require valid p-values and an appropriate family definition.'}))

if __name__ == '__main__':
    main()
