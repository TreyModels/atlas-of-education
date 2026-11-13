"""Tests for floorworld (education and industrialisation, four countries)."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import floorworld as F

MID = {k: (lo + hi) / 2 for k, (lo, hi) in F.PRIORS.items()}


class FloorWorld(unittest.TestCase):
    def test_deterministic_and_bounded(self):
        for S in ('S1', 'S2', 'S3', 'S4', 'S5'):
            for c in F.COUNTRIES:
                a, b = F.simulate(c, S, MID), F.simulate(c, S, MID)
                for k in F.OUTS:
                    self.assertEqual(list(a[k]), list(b[k]))
                for k in ('informal', 'formal', 'complex', 'floor', 'tertiary'):
                    self.assertTrue(all(-1e-9 <= v <= 1 + 1e-9 for v in a[k]), (S, c, k))
                self.assertTrue(all(abs(f + i - 1) < 1e-9 for f, i in zip(a['formal'], a['informal'])))

    def test_raising_the_floor_raises_completion(self):
        hi = dict(floor_lower=[(1980, .05), (2020, .56), (2030, .85)])
        self.assertGreater(F.at(F.simulate('Cambodia', 'S2', MID, hi), 'floor', 2030),
                           F.at(F.simulate('Cambodia', 'S2', MID), 'floor', 2030))

    def test_demand_led_investment_lowers_informality(self):
        more = dict(invest=[(1980, 0), (2020, .2), (2030, .4)])
        self.assertLess(F.at(F.simulate('Cambodia', 'S2', MID, more), 'informal', 2035),
                        F.at(F.simulate('Cambodia', 'S2', MID), 'informal', 2035))


if __name__ == '__main__':
    unittest.main()
