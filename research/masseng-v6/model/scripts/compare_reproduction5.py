#!/usr/bin/env python3
"""Compare final PHL v5 outputs with an independently regenerated fresh copy."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRESH = Path(sys.argv[1]).resolve()
ORIGINAL = ROOT / 'outputs' / 'PHL' / 'v5'
OTHER = FRESH / 'outputs' / 'PHL' / 'v5'
EXPECTED = [f'fit_R{i}.json' for i in range(6)] + ['scores.json', 'report.md', 'figures/fit_and_test.png', 'figures/demand_rivals.png']
scores = json.loads((ORIGINAL / 'scores.json').read_text())
EXPECTED.append(f"recovery_{scores['winner_by_preregistered_rule']}.json")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


pairs = [(ORIGINAL / name, OTHER / name, name) for name in EXPECTED]
pairs += [
    (ROOT / 'README.md', FRESH / 'README.md', 'README.md'),
    (ROOT.parent / 'manuscripts' / 'Philippine_demand_rivals.md',
     FRESH.parent / 'manuscripts' / 'Philippine_demand_rivals.md',
     'manuscripts/Philippine_demand_rivals.md'),
]
rows = []
for a, b, name in pairs:
    row = {'file': name, 'original_exists': a.exists(), 'fresh_exists': b.exists()}
    if a.exists() and b.exists():
        row['original_sha256'] = digest(a)
        row['fresh_sha256'] = digest(b)
        row['byte_identical'] = a.read_bytes() == b.read_bytes()
    else:
        row['byte_identical'] = False
    rows.append(row)
report = {'fresh_copy': str(FRESH), 'all_byte_identical': all(r['byte_identical'] for r in rows), 'files': rows}
path = ROOT / 'outputs' / 'qa' / 'fresh_copy_comparison.json'
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'all_byte_identical': report['all_byte_identical'], 'files': [{k: r.get(k) for k in ('file', 'byte_identical')} for r in rows]}, indent=2))
if not report['all_byte_identical']:
    raise SystemExit(1)
