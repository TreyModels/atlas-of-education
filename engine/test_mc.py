"""Tests for the Monte Carlo manager (mc.py): known answers, determinism, and equivalence with the old code paths."""
import math, os, sys, unittest
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc
import childworld as W


def ishigami(t):
    a, b = 7.0, 0.1
    return math.sin(t['x1']) + a * math.sin(t['x2']) ** 2 + b * t['x3'] ** 4 * math.sin(t['x1'])


ISH = {k: (-math.pi, math.pi, 'lin') for k in ('x1', 'x2', 'x3')}


def noisy(seed, policy):
    """Toy world: outcome = 10 + big common shock(seed) + effect of policy + small idiosyncratic noise."""
    r = np.random.default_rng(seed)
    common = 5 * r.standard_normal()
    small = 0.2 * r.standard_normal()
    return 10 + common + small - policy.get('dose', 0.0)


def _out(x):
    return x


def cw(theta, seed):
    return W.simulate(theta, seed=seed)


def lin_a(theta, seed):
    return dict(y=2 * theta['u'] + 0.0 * seed)


def lin_b(theta, seed):
    return dict(y=2 * theta['u'] + 1.0)


def lin_c(theta, seed):
    return dict(y=-2 * theta['u'])


class Seeds(unittest.TestCase):
    def test_rng_is_default_rng_for_a_plain_seed(self):
        self.assertTrue(np.array_equal(mc.rng(13).random(5), np.random.default_rng(13).random(5)))

    def test_streams_differ_and_repeat(self):
        a, b, c = mc.rng(5, 1).random(4), mc.rng(5, 2).random(4), mc.rng(5, 1).random(4)
        self.assertTrue(np.array_equal(a, c))
        self.assertFalse(np.array_equal(a, b))

    def test_spawned_seeds_are_distinct_and_repeatable(self):
        s = mc.spawn_seeds(1, 200)
        self.assertEqual(len(set(s)), 200)
        self.assertEqual(s, mc.spawn_seeds(1, 200))

    def test_matched_seeds_follow_the_childworld_convention(self):
        self.assertEqual(mc.matched_seeds(3), [0, 1, 2])
        self.assertEqual(mc.matched_seeds(3, reseed=1), [100000, 100001, 100002])


class Draws(unittest.TestCase):
    def test_random_design_reproduces_childworld_draw_exactly(self):
        old = W.draw(np.random.default_rng(7), 500, W.PRIORS_V2)
        new = mc.draw_prior(W.PRIORS_V2, 500, master=7)
        for k in old:
            self.assertTrue(np.array_equal(old[k], new[k]), k)

    def test_designs_stay_inside_the_box(self):
        for design in ('random', 'sobol', 'lhs'):
            D = mc.draw_prior(W.PRIORS, 256, master=3, design=design)
            for k, (lo, hi, _) in W.PRIORS.items():
                self.assertTrue(lo <= D[k].min() and D[k].max() <= hi, (design, k))

    def test_log_scale_is_log_uniform(self):
        D = mc.draw_prior({'c': (0.5, 3.0, 'log')}, 4096, master=1, design='sobol')
        self.assertAlmostEqual(float(np.mean(np.log(D['c']))), 0.5 * (math.log(.5) + math.log(3.0)), places=2)


class Running(unittest.TestCase):
    def test_parallel_equals_serial_and_keeps_order(self):
        thetas = mc.as_rows(mc.draw_prior(W.PRIORS_V2, 12, master=2))
        a = mc.monte_carlo(cw, thetas, mc.matched_seeds(12), workers=1)
        b = mc.monte_carlo(cw, thetas, mc.matched_seeds(12), workers=2)
        self.assertEqual(a, b)


class Policies(unittest.TestCase):
    def test_matched_seeds_cancel_the_common_shock(self):
        seeds = list(range(1, 21))
        res = mc.paired_effects(noisy, {'dose2': {'dose': 2.0}}, seeds, _out, workers=1)
        e = res['dose2']
        self.assertAlmostEqual(e['mean'], -2.0, places=12)          # the shock cancels exactly within a seed
        self.assertEqual(e['sign'], 'lower')
        unmatched = [noisy(s + 1000, {'dose': 2.0}) - noisy(s, {}) for s in seeds]
        self.assertGreater(np.std(unmatched), 10 * e['sd'] + 1)     # without matching the noise buries it

    def test_no_sign_claim_when_the_interval_includes_zero(self):
        s = mc.summarize([0.4, -0.5, 0.3, -0.2, 0.1, -0.1])
        self.assertEqual(s['sign'], 'none')
        self.assertEqual(mc.summarize([-1.0, -1.1, -0.9, -1.05])['sign'], 'lower')
        self.assertEqual(mc.summarize([1.0, 1.1, 0.9, 1.05])['sign'], 'higher')


class Sobol(unittest.TestCase):
    def test_ishigami_matches_the_analytic_indices(self):
        idx, meta = mc.sobol_indices(ishigami, ISH, n=4096, master=1, boot=40, workers=1)
        S1 = [0.3139, 0.4424, 0.0]
        ST = [0.5576, 0.4424, 0.2437]
        for k, s1, st in zip(('x1', 'x2', 'x3'), S1, ST):
            self.assertAlmostEqual(idx[k]['S1'], s1, delta=0.04, msg=k)
            self.assertAlmostEqual(idx[k]['ST'], st, delta=0.04, msg=k)
        self.assertEqual(meta['evaluations'], 4096 * 5)
        self.assertEqual(mc.stiff_directions(idx, 0.2), ['x1', 'x2', 'x3'])

    def test_additive_model_has_equal_first_and_total_order_and_shares_proportional_to_variance(self):
        pri = {'a': (0, 1, 'lin'), 'b': (0, 1, 'lin')}
        idx, _ = mc.sobol_indices(lambda D: 3 * D['a'] + 1 * D['b'], pri, n=2048, vectorized=True, boot=20)
        self.assertAlmostEqual(idx['a']['S1'], 0.9, delta=0.03)
        self.assertAlmostEqual(idx['b']['S1'], 0.1, delta=0.03)
        self.assertAlmostEqual(idx['a']['ST'], idx['a']['S1'], delta=0.03)

    def test_a_dead_parameter_has_zero_index(self):
        pri = {'a': (0, 1, 'lin'), 'dead': (0, 1, 'lin')}
        idx, _ = mc.sobol_indices(lambda D: D['a'] ** 2, pri, n=1024, vectorized=True, boot=10)
        self.assertLess(abs(idx['dead']['ST']), 0.02)


class Structures(unittest.TestCase):
    def test_same_structure_differs_by_nothing_and_a_shift_is_detected(self):
        th = mc.as_rows(mc.draw_prior({'u': (0, 1, 'lin')}, 60, master=1))
        r = mc.compare_structures({'a': lin_a, 'b': lin_b, 'c': lin_c}, th, mc.matched_seeds(60), ['y'], workers=1)['y']
        self.assertAlmostEqual(r['pairs']['a - b']['mean'], -1.0, places=12)
        self.assertAlmostEqual(r['pairs']['a - b']['spearman'], 1.0, places=9)     # same worlds are high in both
        self.assertLess(r['pairs']['a - c']['spearman'], -0.99)                    # the structures disagree about which
        self.assertGreater(r['between_share'], 0.0)


class Abc(unittest.TestCase):
    def test_accepts_only_worlds_within_every_tolerance(self):
        o = {'a': [2, 2.5, 3.9, 4], 'b': [10, 10, 20, 10]}
        self.assertEqual(mc.abc_accept(o, {'a': 2.5, 'b': 10}, {'a': 1, 'b': 1}).tolist(), [True, True, False, False])


if __name__ == '__main__':
    unittest.main()
