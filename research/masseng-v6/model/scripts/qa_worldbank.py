"""Independently spot-check stored World Bank values against the current API."""
import json
import urllib.request
from pathlib import Path

CHECKS = [
    ('PHL', 'SL.EMP.WORK.ZS', 1991), ('PHL', 'SL.EMP.WORK.ZS', 2013),
    ('PHL', 'SL.EMP.WORK.ZS', 2024), ('PHL', 'SP.URB.TOTL.IN.ZS', 1960),
    ('PHL', 'SP.URB.TOTL.IN.ZS', 2000), ('PHL', 'BX.TRF.PWKR.DT.GD.ZS', 2001),
    ('KHM', 'SL.EMP.WORK.ZS', 1991), ('KHM', 'SL.EMP.WORK.ZS', 2019),
    ('KHM', 'SP.URB.TOTL.IN.ZS', 1975), ('KHM', 'SP.URB.TOTL.IN.ZS', 2019),
    ('KHM', 'BX.TRF.PWKR.DT.GD.ZS', 1998), ('KHM', 'BX.TRF.PWKR.DT.GD.ZS', 2019),
]


def stored(iso, code, year):
    path = Path('countries') / iso / 'drivers_v5.json'
    data = json.loads(path.read_text())['series']
    name = {'SL.EMP.WORK.ZS': 'formal_share', 'SP.URB.TOTL.IN.ZS': 'urban_share',
            'BX.TRF.PWKR.DT.GD.ZS': 'remittances_gdp'}[code]
    return data[name]['points'][str(year)]


def main():
    rows = []
    for iso, code, year in CHECKS:
        url = f'https://api.worldbank.org/v2/country/{iso}/indicator/{code}?format=json&per_page=100&date={year}:{year}'
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = json.load(response)
        api = payload[1][0]['value']
        local = stored(iso, code, year)
        rows.append(dict(iso=iso, code=code, year=year, stored=local, api=api,
                         difference=None if api is None else local-api,
                         match=api is not None and abs(local-api) <= 5e-4,
                         source=url))
    report = dict(n=len(rows), passed=sum(r['match'] for r in rows), rows=rows)
    path = Path('outputs/qa/world_bank_spotchecks.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    assert report['passed'] == report['n'], 'World Bank spot-check mismatch'


if __name__ == '__main__':
    main()
