"""Known-answer and docking tests for research/rigor. These check code, not social theories."""
import json
from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research'))
sys.path.insert(0, str(ROOT / 'engine'))
from rigor import stats as S  # noqa: E402
import relfloor_countries as RC  # noqa: E402
import relfloor_gate as G  # noqa: E402


class ForecastStats(unittest.TestCase):
    def test_mase_of_naive_is_one_in_sample(self):
        y = np.cumsum(np.random.default_rng(1).normal(size=50))
        self.assertAlmostEqual(S.mase(y[1:] - y[:-1], y), 1.0)

    def test_dm_identical_errors_gives_no_test(self):
        e = np.random.default_rng(2).normal(size=40)
        r = S.diebold_mariano(e, e)
        self.assertIsNone(r['stat'])

    def test_dm_detects_clearly_better_model(self):
        rng = np.random.default_rng(3)
        r = S.diebold_mariano(rng.normal(0, .5, 200), rng.normal(0, 2, 200))
        self.assertLess(r['stat'], -5)
        self.assertLess(r['p_two_sided'], 1e-6)

    def test_dm_size_is_roughly_nominal(self):
        rng = np.random.default_rng(4)
        rej = sum(S.diebold_mariano(rng.normal(size=60), rng.normal(size=60))['p_two_sided'] < .05 for _ in range(400))
        self.assertTrue(8 <= rej <= 35, rej)       # 5% of 400 = 20

    def test_hln_matches_hand_calculation_h1(self):
        d1 = np.array([1., -1, 2, 0, 1, -2, 3, 1]); d2 = np.zeros(8)
        loss = np.abs(d1)
        n = 8; dm = loss.mean() / np.sqrt(loss.var() / n)
        r = S.diebold_mariano(d1, d2, h=1)
        self.assertAlmostEqual(r['stat'], dm * np.sqrt((n - 1) / n))


class Recovery(unittest.TestCase):
    def test_separated_structures_are_recovered(self):
        rng = np.random.default_rng(5)
        X = np.vstack([rng.normal(0, .1, (200, 2)), rng.normal(3, .1, (200, 2))])
        lab = ['A'] * 200 + ['B'] * 200
        r = S.abc_recovery(X, lab, [.1, .1])
        self.assertGreater(r['accuracy'], .99)

    def test_identical_structures_are_at_chance(self):
        rng = np.random.default_rng(6)
        X = rng.normal(size=(600, 3))
        lab = ['A', 'B', 'C'] * 200
        r = S.abc_recovery(X, lab, [.1] * 3)
        self.assertLess(abs(r['accuracy'] - 1 / 3), .08)

    def test_noise_destroys_recovery(self):
        rng = np.random.default_rng(7)
        X = np.vstack([rng.normal(0, .05, (200, 1)), rng.normal(.2, .05, (200, 1))])
        lab = ['A'] * 200 + ['B'] * 200
        self.assertGreater(S.abc_recovery(X, lab, [.01])['accuracy'], .9)
        self.assertLess(S.abc_recovery(X, lab, [2.0])['accuracy'], .65)


class GateDocking(unittest.TestCase):
    def test_gate_off_reproduces_relfloor_exactly(self):
        cfg = RC.CFG['Cambodia']
        for structure in ('M_HC', 'M_POS', 'M_REL'):
            for smooth in (False, True):
                th = G.draw(np.random.default_rng(11), structure, cfg, smooth_liq=smooth)
                for scen in ('base', 'fall'):
                    a = RC.sim(th, cfg, scen, 300, 4); b = G.sim_gate(th, cfg, scen, 300, 4)
                    for k in a:
                        np.testing.assert_array_equal(np.asarray(a[k]), np.asarray(b[k]))

    def test_only_gate_structure_responds_to_gate_shock(self):
        cfg = RC.CFG['Cambodia']
        for structure in ('M_HC', 'M_POS', 'M_REL'):
            th = G.draw(np.random.default_rng(12), structure, cfg)
            s, _ = G.summaries(th, cfg, 300, 2)
            self.assertEqual(s['gate_resp_2030'], 0.0)
        th = G.draw(np.random.default_rng(12), 'M_GATE', cfg); th['b_gate'] = .6
        s, _ = G.summaries(th, cfg, 2000, 2)
        self.assertGreater(s['gate_resp_2030'], 0.0)

    def test_designs_name_known_summaries(self):
        for cols in G.DESIGNS.values():
            self.assertTrue(set(cols) <= set(G.SUMMARY_NAMES))
            self.assertTrue(set(cols) <= set(G.NOISE))


class Protocol(unittest.TestCase):
    def test_every_rigor_family_has_a_protocol_and_sources_resolve(self):
        p = json.loads((ROOT / 'research/rigor/protocols_rigor.json').read_text())
        sys.path.insert(0, str(ROOT / 'research'))
        import lab
        for fam in lab.RIGOR_FAMILIES:
            self.assertIn(fam, p['families'])
            for s in p['families'][fam].get('sources', []):
                self.assertTrue(s in p['sources'] or s in json.loads(
                    (ROOT / 'research/literature.json').read_text())['sources'], s)


class YouthDefault(unittest.TestCase):
    def test_step_date_default_unchanged(self):
        from firms import model as M, data_china as D
        a = M.YouthMarket(D, dr_drop=.2).run()
        b = M.YouthMarket(D, dr_drop=.2, dr_date=(2021, 8)).run()
        self.assertEqual(a['rate_new'], b['rate_new'])
        c = M.YouthMarket(D, dr_drop=.2, dr_date=(2020, 1)).run()
        self.assertNotEqual(a['rate_new'], c['rate_new'])


if __name__ == '__main__':
    unittest.main()
