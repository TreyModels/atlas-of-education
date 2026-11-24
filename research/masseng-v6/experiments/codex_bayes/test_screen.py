import importlib.util
from pathlib import Path
import unittest

import numpy as np

MODULE_PATH = Path(__file__).with_name("run_screen.py")
spec = importlib.util.spec_from_file_location("run_screen", MODULE_PATH)
screen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screen)


class ScreenTests(unittest.TestCase):
  def test_draws_reproducible_distinct_and_inside_prior(self):
    a = screen.make_draws(25, 17, "main")
    b = screen.make_draws(25, 17, "main")
    c = screen.make_draws(25, 18, "main")
    bounds = np.array([screen.PRIORS["main"][k] for k in screen.PARAMS])
    self.assertTrue(np.array_equal(a, b))
    self.assertFalse(np.array_equal(a, c))
    self.assertTrue(np.all(a >= bounds[:, 0]) and np.all(a <= bounds[:, 1]))
    self.assertEqual(len(np.unique(a, axis=0)), len(a))


  def test_importance_weights_and_ess(self):
    w = screen.normalized_weights(np.array([-2.0, -1.0, -3.0]))
    self.assertTrue(np.isclose(w.sum(), 1.0))
    self.assertTrue(np.all(w > 0))
    self.assertTrue(1.0 <= screen.effective_sample_size(w) <= 3.0)


  def test_likelihood_weights_series_blocks_equally(self):
    train = []
    pred = {s: {} for s in screen.GER_SERIES}
    for s in screen.GER_SERIES:
        n = 2 if s == "ger_primary" else 7
        for i in range(n):
            train.append({"series": s, "year": 1971 + i, "value": 0.0})
            pred[s][1971 + i] = screen.SIGMA_PP[s]
    ll, parts = screen.block_loglik(pred, train)
    expected = sum(-0.5 - np.log(screen.SIGMA_PP[s] * np.sqrt(2 * np.pi)) for s in screen.GER_SERIES)
    self.assertTrue(np.isclose(ll, expected))
    self.assertEqual(set(parts), set(screen.GER_SERIES))


if __name__ == "__main__":
    unittest.main()

