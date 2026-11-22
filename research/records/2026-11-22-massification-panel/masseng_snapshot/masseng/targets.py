"""Observed targets, split into training and test by the protocol. Each row: series, year, value, role, source.
The fitting code receives only rows with role == 'train' (see calibrate.fit and tests/test_protocol.py)."""

WDI_SERIES = {
    'ger_primary': 'SE.PRM.ENRR', 'ger_secondary': 'SE.SEC.ENRR', 'ger_tertiary': 'SE.TER.ENRR',
    'ner_primary': 'SE.PRM.NENR', 'ner_secondary': 'SE.SEC.NENR',
    'priv_primary': 'SE.PRM.PRIV.ZS', 'priv_secondary': 'SE.SEC.PRIV.ZS',
}
# series used in training (within the training window); others are test-only
TRAIN_SERIES = ('ger_primary', 'ger_secondary', 'ger_tertiary', 'ner_primary', 'priv_primary')


def build(country):
    cfg = country.config
    lo, hi = cfg['years']['train']
    tlo, thi = cfg['years']['test']
    rows = []
    for name, code in WDI_SERIES.items():
        s = country.wdi(code)
        if s is None:
            continue
        for y, v in s.observed().items():
            if lo <= y <= hi:
                role = 'train' if name in TRAIN_SERIES else 'diagnostic'
            elif tlo <= y <= thi:
                role = 'test'
            else:
                continue
            rows.append(dict(series=name, year=y, value=v, role=role, source=f'WDI {code}'))
    t = cfg.get('targets', {})
    for y, o in t.get('tertiary_private_share', {}).items():
        if y.startswith('_'):
            continue
        y = int(y)
        if y == 2015:          # conflicting secondary source; CHED preferred for 2016-2020
            role = 'diagnostic'
        else:
            role = 'train' if lo <= y <= hi else 'test'
        rows.append(dict(series='priv_tertiary', year=y, value=o['value'], role=role, source=o['source']))
    for ay, o in t.get('ched_tertiary', {}).items():
        y = int(ay[:4]) + 1
        rows.append(dict(series='priv_tertiary', year=y, value=o['private_share'], role='test',
                         source='CHED Higher Education Data and Indicators, Table 1'))
    if 'shs_private_share_2019' in t:
        rows.append(dict(series='priv_upper_secondary', year=2019, value=t['shs_private_share_2019']['value'],
                         role='test', source=t['shs_private_share_2019']['source']))
    if 'jhs_private_share_2019' in t:
        rows.append(dict(series='priv_lower_secondary', year=2019, value=t['jhs_private_share_2019']['value'],
                         role='test', source=t['jhs_private_share_2019']['source']))
    # income gradient (richest vs poorest participation) as 10 x ln(ratio). Role set in config:
    # PHL moved it from test to calibration in amendment A3 (dated in the facts register).
    for key in ('income_gradient_2019', 'income_gradient_2012'):
        if key in t:
            g = t[key]
            y = int(key[-4:])
            role = g.get('_role', 'test')
            for lev, v in g.items():
                if lev.startswith('_'):
                    continue
                import math
                rows.append(dict(series=f'gradlr_{lev}', year=y, value=10 * math.log(v['richest'] / v['poorest']),
                                 role=role, source=g.get('_note', key)[:120]))
    # drop duplicate tertiary private-share years (CHED wins over secondary sources)
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: (r['series'], r['year'], not r['source'].startswith('CHED Higher'))):
        k = (r['series'], r['year'])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def train_rows(rows):
    # gradient rows are calibration targets even though they fall in a later year (moved from test, dated)
    return [r for r in rows if r['role'] == 'train']


def test_rows(rows):
    return [r for r in rows if r['role'] == 'test']
