"""Summarize the completed independent parameter-and-cohort draws."""
import csv
from pathlib import Path
import numpy as np
from statistics import NormalDist

rows = list(csv.DictReader((Path(__file__).parent / 'draws.csv').open()))
assert len(rows) == 1024 and len({r['draw'] for r in rows}) == 1024
def column(key):
    a = np.array([float(r[key]) for r in rows])
    assert np.isfinite(a).all()
    return a

delta = column('T') - column('T_before')
for name, a in [(k, column(k)) for k in ('T_before','T','S','Sstar','support','spend_change','displaced')] + [('delta_T',delta)]:
    print(name, np.quantile(a, [.05,.5,.95]))
n = len(rows)
p = (delta < 0).mean()
z = NormalDist().inv_cdf(.975)
center = (p + z*z/(2*n)) / (1+z*z/n)
margin = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1+z*z/n)
print('T lower', (delta<0).sum(), p, 'Wilson 95%', center-margin, center+margin)
print('Displacement range', column('displaced').min(), column('displaced').max())
