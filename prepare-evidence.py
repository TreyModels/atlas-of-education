"""Build the browser evidence bundle from unchanged source tables."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import quantiles

site = Path(__file__).parent / 'dist'
lab = site.parent / 'inputs'
trajectories = defaultdict(list)
with (lab / 'trajectories_100_seeds.csv').open(newline='') as source:
    for row in csv.DictReader(source):
        trajectories[row['scenario'], int(row['year'])].append(float(row['population_k']) * 1000)
ensemble = json.loads((lab / 'results.json').read_text())
ensemble['population'] = {}
for (scenario, year), values in sorted(trajectories.items()):
    cuts = quantiles(values, n=10, method='inclusive')
    ensemble['population'].setdefault(scenario, []).append([year, cuts[0], cuts[4], cuts[8]])
bundle = {
    'mandala': ensemble,
    'relfloor': json.loads((site / 'reference/relfloor_countries.json').read_text()),
    'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        *(site / 'engines').glob('*.js'), site / 'reference/angkor/model.js',
        site / 'reference/relfloor_countries.json', lab / 'results.json', lab / 'trajectories_100_seeds.csv'
    ]},
}
(site / 'evidence.js').write_text('globalThis.AtlasEvidence = ' + json.dumps(bundle, separators=(',', ':')) + ';\n')
