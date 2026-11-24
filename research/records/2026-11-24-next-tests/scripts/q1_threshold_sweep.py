"""Q1. Is 'schooling first' (31 of 34 identifiable) stable across event definitions and windows?

Rules follow research/records/2026-11-23-subsistence-v2/scripts/sequencing.py (pre-registered):
  schooling onset: first year y in window with mean years of schooling(y+10) - (y) >= delta_s   (5-year grid)
  release onset:   first year y in window with ag employment share(y+10) - (y) <= -delta_r     (annual, series starts 1991)
  fertility onset: first year y in window with TFR(y+10) - TFR(y) <= -1.0
Censoring follows scripts/sequencing_stats.py of the sequencing paper: a date equal to the first observable year is left-censored.
Inputs (../data): long_run_panel.csv (mean_years_schooling), emp_agri.json, fertility.json, n1_event_dates.csv (for the reproduction check).
Usage: python3 -I q1_threshold_sweep.py ../data   -> q1_sweep.csv, q1_sweep.json, q1_reproduction.txt, q1_reverse_cases.txt
"""
import sys, json, itertools, statistics as st
import pandas as pd, numpy as np
base = sys.argv[1].rstrip('/') + '/'
lr = pd.read_csv(base + 'long_run_panel.csv')
sch = {i: dict(zip(g.year.astype(int), g.mean_years_schooling)) for i, g in lr.dropna(subset=['mean_years_schooling']).groupby('iso3')}
def js(n):
    d = {}
    for i, y, v in json.load(open(base + n + '.json')):
        if v is not None: d.setdefault(i, {})[int(y)] = float(v)
    return d
ag, tfr = js('emp_agri'), js('fertility')

def onset(s, delta, direction, start, end, w=10):
    for y in range(start, end + 1):
        if y in s and y + w in s:
            ch = s[y + w] - s[y]
            if (direction == 'down' and ch <= -delta) or (direction == 'up' and ch >= delta): return y
    return None

def events(iso, ds, dr, start, end):
    return (onset(sch.get(iso, {}), ds, 'up', start, end), onset(ag.get(iso, {}), dr, 'down', start, end),
            onset(tfr.get(iso, {}), 1.0, 'down', start, end))

def classify(s, r, s_floor, r_floor=1991):
    sc, rc = s == s_floor, r == r_floor
    if not sc and not rc: return 'both_exact', ('forward' if r > s else 'reverse')
    if sc and not rc: return 'schooling_censored', 'forward'
    if rc and not sc: return 'release_censored', ('reverse_or_tie' if s >= r_floor else 'undetermined')
    return 'both_censored', 'undetermined'

def run(ds, dr, start, end, need_fertility):
    s_floor = min(y for y in range(start, end + 1) if y % 5 == 0)       # first grid year in window
    rows = []
    for iso in sorted(set(sch) & set(ag)):
        s, r, f = events(iso, ds, dr, start, end)
        if s is None or r is None or (need_fertility and f is None): continue
        c, o = classify(s, r, s_floor); rows.append((iso, s, r, c, o))
    n = len(rows); fw = sum(o == 'forward' for *_, o in rows); rv = sum(o in ('reverse', 'reverse_or_tie') for *_, o in rows)
    ex = [r - s for _, s, r, c, o in rows if c == 'both_exact']
    return dict(n=n, forward=fw, reverse=rv, undetermined=n - fw - rv, identified=fw + rv,
                forward_share_identified=round(100 * fw / (fw + rv), 1) if fw + rv else None,
                forward_lower_bound_all=round(100 * fw / n, 1) if n else None,
                forward_upper_bound_all=round(100 * (fw + (n - fw - rv)) / n, 1) if n else None,
                both_exact_n=len(ex), both_exact_median_lead=st.median(ex) if ex else None), rows

# ---- reproduction of the paper's default (delta_s=1.0, delta_r=3.0, 1965-2010, three events) ----
res, rows = run(1.0, 3.0, 1965, 2010, True)
ev = pd.read_csv(base + 'n1_event_dates.csv'); paper = ev.dropna(subset=['release', 'schooling', 'fertility'])
mine = {iso: (s, r) for iso, s, r, *_ in rows}
agree = sum(1 for _, p in paper.iterrows() if mine.get(p.iso3) == (p.schooling, p.release))
txt = [f"reproduction of the paper's default definitions, three-event sample: {res}",
       f"paper event_dates.csv: {len(paper)} three-event countries; mine: {len(rows)}; identical (schooling, release) dates for {agree}",
       "paper headline: 31 forward, 3 reverse of 34 identifiable, 30 undetermined, both-exact median lead 18 (n=18)"]
open('q1_reproduction.txt', 'w').write('\n'.join(txt) + '\n'); print('\n'.join(txt))
# ---- sweep ----
out = []
for ds, dr, (a, b), nf in itertools.product([0.5, 1.0, 1.5], [2.0, 3.0, 5.0], [(1960, 2010), (1965, 2010), (1970, 2015)], [True, False]):
    r, _ = run(ds, dr, a, b, nf); out.append(dict(delta_s=ds, delta_r=dr, window=f'{a}-{b}', three_event_sample=nf, **r))
df = pd.DataFrame(out); df.to_csv('q1_sweep.csv', index=False); json.dump(out, open('q1_sweep.json', 'w'), indent=1)
pd.set_option('display.width', 250); print(df[df.three_event_sample].to_string(index=False))
big = df[(df.identified >= 20)]
print('\nrange of forward share among identifiable (cells with >=20 identifiable):', big.forward_share_identified.min(), '-', big.forward_share_identified.max(), '; cells', len(big), 'of', len(df))
# ---- reverse cases ----
L = []
for iso in ('AFG', 'KHM', 'SEN', 'MLI', 'MOZ'):
    L.append(f'{iso}: schooling(5y)={dict(sorted(sch.get(iso, {}).items())[-12:])}')
    L.append(f'{iso}: ag employment share={dict(sorted(ag.get(iso, {}).items())[::3])}')
    L.append(f'{iso}: events (paper defaults) schooling/release/fertility = {events(iso, 1.0, 3.0, 1965, 2010)}\n')
open('q1_reverse_cases.txt', 'w').write('\n'.join(L)); print('\n'.join(L[:6]))
