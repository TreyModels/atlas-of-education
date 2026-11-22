"""Fit one pre-registered v5 rival after strict input preflight."""
import argparse
import json
from pathlib import Path

from masseng.data import Country
from masseng import calibrate5 as C
from masseng.readiness5 import assert_ready


def main():
    p = argparse.ArgumentParser()
    p.add_argument('iso')
    p.add_argument('spec', choices=['R0', 'R1', 'R2', 'R3', 'R4', 'R5'])
    p.add_argument('--max-nfev', type=int, default=250)
    p.add_argument('--continue-existing', action='store_true',
                   help='Computational continuation only: start from the existing fit without changing targets or protocol.')
    args = p.parse_args()
    c = Country(args.iso)
    report = assert_ready(c)
    rows = C.build_rows(c)
    train = [r for r in rows if r['role'] == 'train']
    # Only the protocol's explicitly registered later FIES and APIS gradient rows are calibration targets.
    assert all(r['year'] <= c.config['years']['train'][1] or r['series'].startswith(('gradlr_', 'edu_share_'))
               for r in train)
    path = Path('outputs') / args.iso / 'v5' / f'fit_{args.spec}.json'
    previous = None
    if args.continue_existing:
        previous = json.loads(path.read_text())
        if previous['spec'] != args.spec:
            raise ValueError('Existing fit is for a different rival')
    fit = C.fit(c, train, args.spec, start=previous['params'] if previous else None, max_nfev=args.max_nfev)
    if previous:
        fit['continued_from'] = {'cost': previous['cost'], 'nfev': previous['nfev']}
        fit['total_nfev'] = previous.get('total_nfev', previous['nfev']) + fit['nfev']
    fit['preflight'] = report
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(fit, indent=2) + '\n')
    print(json.dumps({k: fit[k] for k in ('spec', 'cost', 'nfev', 'at_bounds')}, indent=2))


if __name__ == '__main__':
    main()
