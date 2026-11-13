"""Tests for childworld (cross-country school-and-work model) and the China story hooks."""
import os, sys, unittest
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import childworld as W


def mid():
    return {k: (lo * hi) ** .5 if sc == 'log' else (lo + hi) / 2 for k, (lo, hi, sc) in W.PRIORS.items()}


class ChildWorld(unittest.TestCase):
    def test_states_sum_to_one_and_deterministic(self):
        a, b = W.simulate(mid(), seed=3), W.simulate(mid(), seed=3)
        self.assertEqual(a, b)
        self.assertAlmostEqual(a['school'] + a['both'] + a['work'] + a['neither'], 1.0, places=12)

    def test_richer_households_send_more_children_to_school(self):
        lo, hi = dict(mid(), y_med=0.5), dict(mid(), y_med=2.8)
        self.assertLess(W.simulate(hi)['oos_lower'], W.simulate(lo)['oos_lower'])

    def test_value_of_D_moves_exit_into_D_not_work(self):
        lo, hi = W.simulate(dict(mid(), neither=-1.0)), W.simulate(dict(mid(), neither=3.5))
        self.assertGreater(hi['neither_share_oos'], lo['neither_share_oos'])

    def test_compatibility_keeps_child_labourers_in_school(self):
        lo, hi = W.simulate(dict(mid(), compat=0.0)), W.simulate(dict(mid(), compat=1.0))
        self.assertGreater(hi['both_share_cl'], lo['both_share_cl'])


class StoryHooks(unittest.TestCase):
    def test_story_market_with_mechanisms_off_equals_seasonal(self):
        from firms import stories as S, seasonal as SE, data_china as D, calibrate_china as C
        x = S.starts('supply', 2)[1]
        a, _ = S.run('supply', x)
        kw = dict(C.REF, sigma_A=5.0, e_prop=0.0, dr_drop=0.0); kw.update({f[0]: float(v) for f, v in zip(S.spec('supply'), x)})
        b = SE.SeasonalMarket(D, **kw).run()
        self.assertLess(max(abs(p - q) for p, q in zip(a['rate_new'], b['rate_new'])), 1e-12)


if __name__ == '__main__':
    unittest.main()
