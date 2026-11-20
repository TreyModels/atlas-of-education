"""Build the wide country-year panel from WDI JSON pulls (observed cells only; no imputation).
Indicator id is taken from the payload itself, so chunked multi-country files merge cleanly."""
import json, glob, os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WDIR = os.path.join(ROOT, 'raw', 'wdi')
rows, bad = [], []
for f in sorted(glob.glob(os.path.join(WDIR, '*.json'))):
    base = os.path.basename(f)
    if base.startswith('_'): continue
    try:
        payload = json.load(open(f))
    except Exception as e:
        bad.append(base); continue
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        bad.append(base); continue
    for rec in payload[1]:
        v = rec.get('value')
        if v is None: continue                        # observed cells only
        rows.append(dict(iso3=rec['countryiso3code'], country=rec['country']['value'],
                         indicator=rec['indicator']['id'], year=int(rec['date']), value=float(v)))
long = pd.DataFrame(rows).drop_duplicates(['iso3','indicator','year'])
wide = long.pivot_table(index=['iso3','country','year'], columns='indicator', values='value').reset_index()
wide.columns.name = None
wide.to_csv(os.path.join(ROOT,'data','panel_wdi_wide.csv'), index=False)
long.to_csv(os.path.join(ROOT,'data','panel_wdi_long.csv'), index=False)
print('panel:', wide.shape, '| countries:', wide.iso3.nunique(), '| years:', int(wide.year.min()), '-', int(wide.year.max()))
print('bad files:', bad)
print(wide.drop(columns=['iso3','country','year']).notna().sum().sort_values(ascending=False).to_string())
