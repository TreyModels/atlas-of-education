"""Build the wide country-year panel from WDI JSON pulls (observed cells only)."""
import json, glob, os, sys
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 09_relations
WDIR = os.path.join(ROOT, 'raw', 'wdi')
rows = []
for f in sorted(glob.glob(os.path.join(WDIR, '*.json'))):
    base = os.path.basename(f)[:-5]
    if base.startswith('_'): continue
    try:
        payload = json.load(open(f))
    except Exception:
        print('BAD', f); continue
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None: continue
    for rec in payload[1]:
        v = rec.get('value')
        if v is None: continue                      # observed cells only
        rows.append(dict(iso3=rec['countryiso3code'], country=rec['country']['value'],
                         indicator=base, year=int(rec['date']), value=float(v)))
long = pd.DataFrame(rows).drop_duplicates(['iso3','indicator','year'])
wide = long.pivot_table(index=['iso3','country','year'], columns='indicator', values='value').reset_index()
wide.columns.name = None
out = os.path.join(ROOT,'data','panel_wdi_wide.csv')
wide.to_csv(out, index=False)
print('panel:', wide.shape, 'countries:', wide.iso3.nunique(), 'years:', int(wide.year.min()), int(wide.year.max()))
print('n obs per indicator:')
print(wide.drop(columns=['iso3','country','year']).notna().sum().sort_values(ascending=False).to_string())
