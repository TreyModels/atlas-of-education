"""Angkor Mandala Lab as an Atlas world: a read-only adapter over the unchanged reference engine.

The engine file worlds/angkor/reference/mandala_lab_v0.1/angkor.py is loaded by path and never edited; its SHA-256
goes into every manifest. The adapter adds what the world contract needs: metadata and mechanisms from the model card,
seeded reset, one-tick step with interventions, observables, internal validation, and per-run benchmark observables.

Regression guarantee (tests/test_world_angkor.py): stepping the adapter from 750 to 1500 with no interventions gives
exactly the history of the reference `scenario(name, seed)`, and the 500 stored Monte Carlo-lab runs are reproduced.
"""
import dataclasses
import importlib.util
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world_protocol as WP

ROOT = WP.here()
ENGINE = os.path.join(ROOT, 'worlds', 'angkor', 'reference', 'mandala_lab_v0.1', 'angkor.py')
CARD = os.path.join(ROOT, 'worlds', 'angkor', 'model_card.json')


def _load_engine():
    spec = importlib.util.spec_from_file_location('angkor_reference_v01', ENGINE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = _load_engine()
YEARS = list(range(750, 1501, 10))


class AngkorWorld(WP.WorldProtocol):
    source_files = (ENGINE,)

    def __init__(self):
        self.card = WP.load_card(CARD)
        self.w = None

    # ---- declarations
    def metadata(self):
        c = self.card
        return dict(name=c['name'], version=c['version'], status=c['status'], scale=c['scale'], claim_limits=c['claim_limits'])

    def mechanisms(self):
        return self.card['mechanisms']

    def struts(self):
        return self.card['struts']

    # ---- running
    def reset(self, seed, parameters=None):
        parameters = dict(parameters or {})
        scen = parameters.pop('scenario', 'reference')
        pol = dataclasses.replace(A.POLICIES[scen], **parameters) if parameters else A.POLICIES[scen]
        self.w = A.MandalaWorld(pol, seed=seed)
        self.i = 0

    def next_label(self):
        return YEARS[self.i]

    def step(self, intervention=None):
        if intervention:
            self.w.policy = dataclasses.replace(self.w.policy, **intervention)
        self._before = self.w.population.sum()
        self.w.tick(YEARS[self.i], 10)
        self.i += 1

    def done(self):
        return self.i >= len(YEARS)

    def observables(self):
        return dict(self.w.hist[-1])

    def validate(self):
        w = self.w
        h = w.hist[-1] if w.hist else None
        checks = {
            'population finite and positive': (bool(np.all(np.isfinite(w.population)) and np.all(w.population > 0)), ''),
            'irrigation, condition in [0,1]': (bool(np.all((w.irrigation >= 0) & (w.irrigation <= 1) & (w.condition >= 0) & (w.condition <= 1))), ''),
            'soil in engine bounds [0.55, 1.04]': (bool(np.all((w.soil >= .55 - 1e-12) & (w.soil <= 1.04 + 1e-12))), ''),
        }
        if h:
            checks['court shares sum to 1'] = (abs(sum(h['court_shares']) - 1) < 1e-9, f"{sum(h['court_shares']):.12f}")
            checks['every patch pledged to one court'] = (bool(len(w.pledge) == w.n and w.pledge.min() >= 0 and w.pledge.max() < 5), '')
        return checks


def benchmark_observables(history):
    """Per-run values of the model card's benchmarks B1-B5 (True / False / None = not comparable)."""
    by = {r['year']: r for r in history}
    ang = {r['year']: r['angkor_k'] for r in history}
    peak_total = max(r['population_k'] for r in history)
    peak_year_ang = max(history, key=lambda r: r['angkor_k'])['year']
    falls = [(ang[y] - ang[y + 10]) / ang[y] for y in range(1300, 1450, 10)]
    cond_late = np.mean([by[y]['mean_condition'] for y in range(1350, 1451, 10)])
    cond_peak = np.mean([by[y]['mean_condition'] for y in range(1200, 1301, 10)])
    return {
        'B1': by[1200]['strongest'] == 'Angkor',
        'B2': 700 <= peak_total <= 900,
        'B3': 1200 <= peak_year_ang <= 1299,
        'B4': (ang[1450] < ang[1300]) and max(falls) <= 0.15,
        'B5': bool(cond_late < cond_peak),
    }, dict(peak_total_k=peak_total, peak_year_angkor=peak_year_ang, angkor_share_1200=by[1200]['angkor_share'],
            strongest_1200=by[1200]['strongest'], pop_1300_k=by[1300]['population_k'], pop_1500_k=by[1500]['population_k'],
            water_condition_1500=by[1500]['mean_condition'], max_decade_fall_1300_1450=max(falls))


def run_one(scenario, seed):
    """Module-level (picklable) runner for mc.run_batch: one history through the protocol, reduced to a row."""
    world = AngkorWorld()
    res = WP.run(world, seed, dict(scenario=scenario), check_every=19)
    bm, vals = benchmark_observables(res['history'])
    return dict(scenario=scenario, seed=seed, benchmarks=bm, engine_sha256=res['manifest']['engine_sha256'],
                post_1300_decline=int(vals['pop_1500_k'] < vals['pop_1300_k']), **vals)
