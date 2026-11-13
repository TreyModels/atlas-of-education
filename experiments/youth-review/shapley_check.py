"""Shapley decomposition of the modelled rise (review 1.6), for the on-disk headline and each widened-bound refit.
Uses calibrate_china.shapley with its own switches, so the 'sector' component is the Aug-2021 step (dr_drop; e_prop ~ 0).
Run: python shapley_check.py -> results/shapley_check.json"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import K, NEW_BOUNDS, dump  # noqa: E402
from run_fits import ondisk  # noqa: E402

names = [f[0] for f in K.FREE]
out = {}
sources = {'on_disk_headline': ondisk('full')}
for tag in ('bounds_new_full',):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', tag + '.json')
    if os.path.exists(p):
        sources[tag] = json.load(open(p))['params']
for tag, params in sources.items():
    th = np.array([params[n] for n in names])
    phi, full, none = K.shapley(th)
    out[tag] = dict(contributions=phi, total=full, all_off=none, sector_step=phi['sector'])
    print(tag, {k: round(v, 2) for k, v in phi.items()}, 'total', round(full, 2), 'all off', round(none, 2), flush=True)
dump('shapley_check.json', out)
