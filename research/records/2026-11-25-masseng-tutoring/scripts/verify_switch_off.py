"""Switch-off identity test: TutoringModel5(switches={'tutoring': False}) must be bit-identical to Model5.

Run from the model package directory with PYTHONPATH pointing at it:
    PYTHONPATH=/root/work/masseng-tutoring/model /root/miniconda3/bin/python verify_switch_off.py

Compares, for a FULL run (1940-2024) and a SHORT run (2000-2024):
  * every array in Result.ind (byte-for-byte, so NaN payloads must match too);
  * every array in Result.extra (flows, markets, decile panels).
The committed engine5.py is not modified on this branch, so Model5 here IS the pristine baseline; the test also
records its git blob hash for the report.
"""
import copy
import hashlib
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)


def _model_dir():
    """Locate the MASSENG model package in either the server deployment or the repo worktree."""
    cands = [os.environ.get('MASSENG_MODEL_DIR'),
             '/root/work/masseng-tutoring/model',
             os.path.join(os.path.dirname(os.path.dirname(RECORD)), 'masseng-v6', 'model')]
    for c in cands:
        if c and os.path.isdir(os.path.join(c, 'masseng')):
            return os.path.abspath(c)
    raise RuntimeError('MASSENG model dir not found; set MASSENG_MODEL_DIR')


MODEL_DIR = _model_dir()
if MODEL_DIR not in sys.path:
    sys.path.insert(0, MODEL_DIR)

from masseng.data import Country
from masseng.engine5 import Model5
from masseng.tutoring import TutoringModel5


def _arrays_equal(a, b, path, out):
    if isinstance(a, dict):
        assert set(a) == set(b), f'{path}: key mismatch {set(a) ^ set(b)}'
        for k in a:
            _arrays_equal(a[k], b[k], f'{path}.{k}', out)
        return
    if isinstance(a, np.ndarray):
        assert isinstance(b, np.ndarray), f'{path}: type mismatch'
        same = a.shape == b.shape and a.dtype == b.dtype and a.tobytes() == b.tobytes()
        out.append(dict(path=path, shape=list(a.shape), identical=bool(same)))
        if not same:
            raise AssertionError(f'{path}: arrays differ')
        return
    # scalars / lists of numbers / None / strings
    if isinstance(a, float) and isinstance(b, float):
        ok = (a == b) or (np.isnan(a) and np.isnan(b))
    else:
        ok = a == b
    out.append(dict(path=path, identical=bool(ok)))
    if not ok:
        raise AssertionError(f'{path}: {a!r} != {b!r}')


def run_pair(params, short=False):
    c = Country('PHL')
    if short:
        c.config = copy.deepcopy(c.config)
        c.config['v5']['years'] = dict(simulate_from=2000, simulate_to=2024)
    t0 = time.time()
    base = Model5(c, params, spec='R1').run(record_deciles=True)
    t1 = time.time()
    off = TutoringModel5(c, params, spec='R1', switches={'tutoring': False}).run(record_deciles=True)
    t2 = time.time()
    checks = []
    _arrays_equal(base.ind, off.ind, 'ind', checks)
    # The only permitted difference in ``extra`` is the diagnostics key the subclass always attaches; every
    # numerical array must be byte-identical.
    extra_off = {k: v for k, v in off.extra.items() if k != 'tutoring'}
    _arrays_equal(base.extra, extra_off, 'extra', checks)
    assert off.extra['tutoring']['switch'] is False
    checks.append(dict(path='extra.tutoring.switch', identical=off.extra['tutoring']['switch'] is False))
    return dict(short_run=short, years=len(base.years),
                baseline_seconds=round(t1 - t0, 3), switch_off_seconds=round(t2 - t1, 3),
                n_checks=len(checks), all_identical=all(c['identical'] for c in checks),
                checks=checks)


def main():
    fit = json.load(open('outputs/PHL/v5/fit_R1.json'))
    out = {
        'label': 'switch-off identity test (Model5 vs TutoringModel5 tutoring=False)',
        'engine_file_sha256': hashlib.sha256(
            open(os.path.join(MODEL_DIR, 'masseng', 'engine5.py'), 'rb').read()).hexdigest(),
        'tutoring_sha256': hashlib.sha256(
            open(os.path.join(MODEL_DIR, 'masseng', 'tutoring.py'), 'rb').read()).hexdigest(),
        'fit': {'spec': fit['spec'], 'cost': fit['cost'], 'nfev': fit['nfev']},
        'full': run_pair(fit['params'], short=False),
        'short': run_pair(fit['params'], short=True),
    }
    out['verdict'] = ('IDENTICAL — switch-off reproduces the untouched baseline bit-for-bit'
                      if out['full']['all_identical'] and out['short']['all_identical'] else 'FAILED')
    path = os.path.join(RECORD, 'results', 'switch_off_identity.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, 'w'), indent=2)
    print(out['verdict'])
    print(f"full run: {out['full']['years']} years, {out['full']['n_checks']} comparisons, "
          f"{out['full']['baseline_seconds']}s + {out['full']['switch_off_seconds']}s")
    print(f"short run: {out['short']['years']} years, {out['short']['n_checks']} comparisons")
    print('wrote', path)


if __name__ == '__main__':
    main()
