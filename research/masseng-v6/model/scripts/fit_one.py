#!/usr/bin/env python3
"""Fit one specification on a country's training rows. Usage: fit_one.py ISO VERSION DEMAND SUPPLY"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import masseng as m
from masseng import targets as T, calibrate as C

ISO, VERSION, DEMAND, SUPPLY = sys.argv[1:5]
c = m.Country(ISO)
tr = T.train_rows(T.build(c))
t = time.time()
f = C.fit(c, tr, supply_rule=SUPPLY, demand_form=DEMAND, max_nfev=300, ftol=1e-7,
          burden_form='log', split_income=True, split_nu=VERSION not in ('v1', 'v2', 'v3'))
f['seconds'] = time.time() - t
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs', ISO, VERSION,
                   f'fit_{DEMAND}_{SUPPLY}.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(f, open(out, 'w'), indent=1, default=float)
print(ISO, DEMAND, SUPPLY, round(f['cost'], 3), round(f['seconds'], 1))
