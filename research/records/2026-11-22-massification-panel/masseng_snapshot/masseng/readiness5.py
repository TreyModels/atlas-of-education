"""Preflight checks for v5 fitting. Never substitute zero or assumptions for missing drivers."""
import json
import os

import numpy as np

from . import calibrate5 as C
from .engine5 import Model5


def audit(country):
    errors, warnings = [], []
    cfg = country.config.get('v5', {})
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'countries', country.iso3, 'drivers_v5.json')
    raw = json.load(open(path)).get('series', {}) if os.path.exists(path) else {}
    for kind, name in cfg.get('driver_map', {}).items():
        if kind.startswith('_'):
            continue
        spec = raw.get(name)
        if spec is None:
            errors.append(f"missing mapped driver: {kind} -> {name}")
            continue
        if not spec.get('verified', False):
            errors.append(f"unverified mapped driver: {name}")
        if not spec.get('points'):
            errors.append(f"empty mapped driver: {name}")
        if kind.startswith('premium_') and spec.get('unit') != 'log points':
            errors.append(f"{name}: engine5 requires log points, found {spec.get('unit')!r}")
    rows = C.build_rows(country)
    train = [r for r in rows if r['role'] == 'train']
    test = [r for r in rows if r['role'] == 'test']
    if not train:
        errors.append('no training targets')
    if not test:
        errors.append('no held-out test targets')
    if country.iso3 == 'PHL':
        required = {'edu_share_hh', 'edu_share_bottom30', 'edu_share_top70'}
        absent = required - {r['series'] for r in train}
        if absent:
            errors.append(f"missing registered FIES training targets: {sorted(absent)}")
    result = Model5(country).run()
    bad = [(r['series'], r['year']) for r, value in zip(train + test, C._pred(result, train + test))
           if not np.isfinite(value)]
    if bad:
        errors.append(f"non-finite model predictions at registered targets: {bad[:8]}")
    target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'countries', country.iso3, 'targets_v5.json')
    excluded = []
    if os.path.exists(target_path):
        for row in json.load(open(target_path)).get('rows', []):
            if not row.get('verified', False):
                excluded.append(f"{row.get('series')} {row.get('year')}")
    if excluded:
        warnings.append(f"unverified targets excluded: {excluded}")
    if country.iso3 == 'PHL':
        warnings.append('PHL premium_tertiary combines methods; interpolation across 1995-2013 is a declared comparability limitation')
        warnings.append('PHL relational driver is formal_share; short occupation series are not spliced')
    return dict(country=country.iso3, ready=not errors, errors=errors, warnings=warnings,
                train_rows=len(train), test_rows=len(test), diagnostic_rows=sum(r['role'] == 'diagnostic' for r in rows))


def assert_ready(country):
    report = audit(country)
    if not report['ready']:
        raise ValueError('v5 fit preflight failed: ' + '; '.join(report['errors']))
    return report


if __name__ == '__main__':
    import sys
    from .data import Country
    for iso in sys.argv[1:] or ['PHL', 'KHM']:
        print(json.dumps(audit(Country(iso)), indent=2))
