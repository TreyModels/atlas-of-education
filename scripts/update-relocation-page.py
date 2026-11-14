"""Rebuild the numbers on public/research/relocation.html from relocation-results.csv / relocation-summary.json.
Run after `OUT=public/research node run-relocation.cjs`."""
import csv, json, re, statistics as st
from pathlib import Path
R = Path(__file__).resolve().parents[1] / 'public' / 'research'
rows = list(csv.DictReader(open(R / 'relocation-results.csv')))
summ = json.load(open(R / 'relocation-summary.json'))
p = R / 'relocation.html'; s = p.read_text()
pct = lambda x: f'{100 * x:.1f}%'
# table body
body = ''.join(f"<tr><td>{g['outside']}</td><td>{g['climate']}</td><td>{g['exits']}/{g['runs']}</td><td>{pct(g['finalEliteShare'])}</td>"
               f"<td>{pct(g['oldCoreRetained'])}</td><td>{pct(g['oldRuralRetained'])}</td><td>{100 * g['waterDelta']:+.1f} pp</td></tr>" for g in summ)
s = re.sub(r'(</thead>\s*<tbody[^>]*>\s*).*?(</tbody>)', lambda m: m.group(1) + body + m.group(2), s, count=1, flags=re.S)
sel = lambda **k: [r for r in rows if all(r[a] == str(b) for a, b in k.items())]
dep = lambda rs: sum(1 for r in rs if r['exitYear'])
d12 = sel(outside=1.2, climate='drought')
mc = {m: dep([r for r in d12 if r['movingCost'] == m]) for m in ('0.05', '0.25', '0.5')}
pt = {m: dep([r for r in d12 if r['portability'] == m]) for m in ('0.75', '0.25')}
d16 = sel(outside=1.6, climate='drought'); mean = lambda k: st.mean(float(r[k]) for r in d16)
s = re.sub(r'At outside opportunity 1\.2 with drought, persistent departure occurs in .*?compared with \d+/192 at portability 0\.25\.',
           f"At outside opportunity 1.2 with drought, persistent departure occurs in {mc['0.05']}/128 settings at moving hurdle 0.05, {mc['0.25']}/128 at 0.25, and {mc['0.5']}/128 at 0.5. With portability 0.75 it occurs in {pt['0.75']}/192 settings, compared with {pt['0.25']}/192 at portability 0.25.", s, count=1, flags=re.S)
s = re.sub(r'At opportunity 1\.6 with drought, average final old water condition is .*?with workers only\.',
           f"At opportunity 1.6 with drought, average final old water condition is {pct(mean('oldWater'))} with both groups mobile, {pct(mean('closedWater'))} with neither mobile, {pct(mean('eliteOnlyWater'))} with elites only, and {pct(mean('workersOnlyWater'))} with workers only.", s, count=1, flags=re.S)
s = re.sub(r'The old residential core retains about [0-9.]+% of its own peak', f"The old residential core retains about {pct(mean('oldCoreRetained'))} of its own peak", s, count=1)
p.write_text(s); print('updated', mc, pt)
