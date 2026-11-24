"""Smoke tests for the first-pass shadow-equation model (fast, no inference)."""
import os, sys, unittest
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shadow_model import Params, simulate, _softmax, gini, price_elasticity, SCENARIOS


class TestShadowModel(unittest.TestCase):
    def test_softmax_rows_sum_to_one(self):
        V = np.array([[0.0, 1.0, -1.0, 2.0], [1.0, 0.0, 0.0, 0.0]])
        P = _softmax(V)
        np.testing.assert_allclose(P.sum(axis=1), 1.0, atol=1e-12)
        self.assertTrue((P >= 0).all())

    def test_gini_zero_for_equal(self):
        self.assertAlmostEqual(gini(np.ones(50)), 0.0, places=12)

    def test_ban_reduces_own_teacher_share(self):
        base = Params(n=2000, seed=1)
        a = simulate(base)["own_share"]
        b = simulate(Params(n=2000, seed=1, ban_own=True))["own_share"]
        self.assertLess(b, a)

    def test_higher_price_reduces_participation(self):
        lo = simulate(Params(n=2000, seed=1, price_fee=0.8))["tut_participation"]
        hi = simulate(Params(n=2000, seed=1, price_fee=1.2))["tut_participation"]
        self.assertLess(hi, lo)

    def test_quota_changes_admission_gap(self):
        base = simulate(Params(n=3000, seed=2))
        quota = simulate(Params(n=3000, seed=2, quota=True))
        self.assertNotAlmostEqual(base["admission_gap_q5_q1"], quota["admission_gap_q5_q1"], places=6)

    def test_scenarios_run(self):
        from shadow_model import run_scenarios
        base = Params(n=200, seed=0)
        out, deltas, _ = run_scenarios(base, seeds=1, scenarios={"baseline": {}, "ban_own": {"ban_own": True}})
        self.assertIn("baseline", out)
        self.assertIn("ban_own", deltas)
        self.assertIn("tut_participation", out["baseline"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
