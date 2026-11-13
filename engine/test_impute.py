"""Tests for the Atlas imputation system (engine/impute): provenance, the six-rung ladder,
known-answer recoveries, bounded-rate behaviour, gap-length ordering on the real public data,
interval calibration, determinism and the hold-out harness.

Run from the project root:   python -m unittest engine.test_impute -v
Deterministic (fixed seeds throughout) and fast (<20 s).
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import impute
from impute import (DERIVED, MEMORY, MISSING, OBSERVED_FLAGS, VERIFIED, AmeliaMI, CohortBackcast,
                    ImputationResult, KalmanSmoother, LinearInterpolator, LogitSCurve,
                    LogLinearInterpolator, ProvenancePanel, from_long, holdout, impute_panel,
                    make_deletions, make_imputer)
from impute import data


# ---------------------------------------------------------------- helpers
def panel(values, years=None, flags=None, name='synthetic'):
    """A ProvenancePanel from a 2-D array (rows are entities)."""
    values = np.atleast_2d(np.asarray(values, dtype=float))
    n, T = values.shape
    if years is None:
        years = np.arange(T, dtype=float)
    return ProvenancePanel([f'C{i}' for i in range(n)], np.asarray(years, dtype=float), values,
                           flags=flags, name=name)


def errors(res, truth):
    """(values, truth) arrays of the filled cells, for error assertions."""
    truth = np.asarray(truth, dtype=float)
    if truth.shape != res.values.shape:
        truth = np.broadcast_to(truth, res.values.shape)
    m = res.filled & np.isfinite(truth)
    return res.values[m] - truth[m]


def mae(res, truth):
    e = errors(res, truth)
    return float(np.mean(np.abs(e))) if e.size else float('nan')


def rmse(res, truth):
    e = errors(res, truth)
    return float(np.sqrt(np.mean(e ** 2))) if e.size else float('nan')


def max_abs(res, truth):
    e = errors(res, truth)
    return float(np.max(np.abs(e))) if e.size else float('nan')


def local_linear_trend(n_entities=8, n_years=80, q_level=0.05, q_slope=1e-4, obs_var=0.10,
                       start=1960.0, seed=7, mu0=10.0, beta0=0.10):
    """Simulate the state-space rung's own data-generating process (known hyperparameters)."""
    rng = np.random.default_rng(seed)
    mu = np.full(n_entities, mu0) + rng.normal(0.0, 0.5, n_entities)
    beta = np.full(n_entities, beta0)
    truth = np.empty((n_entities, n_years))
    for t in range(n_years):
        if t > 0:
            mu = mu + beta + rng.normal(0.0, np.sqrt(q_level), n_entities)
            beta = beta + rng.normal(0.0, np.sqrt(q_slope), n_entities)
        truth[:, t] = mu + rng.normal(0.0, np.sqrt(obs_var), n_entities)
    years = start + np.arange(n_years, dtype=float)
    return truth, years


class ProvenanceTests(unittest.TestCase):
    def test_flags_are_stored_validated_and_counted(self):
        p = panel([[1.0, np.nan, 3.0], [np.nan, 5.0, 6.0]],
                  flags=[[VERIFIED, MISSING, MEMORY], [MISSING, DERIVED, VERIFIED]])
        self.assertEqual(p.flag_counts(), {'verified': 2, 'memory': 1, 'derived': 1, 'missing': 2})
        self.assertEqual(int(p.observed().sum()), 3)                 # 'd' is not an observation
        self.assertEqual(int(p.observed((VERIFIED, MEMORY, DERIVED)).sum()), 4)
        with self.assertRaises(ValueError):
            panel([[1.0]], flags=[['z']])
        with self.assertRaises(ValueError):
            panel([[1.0]], flags=[[MISSING]])                        # value without a flag
        with self.assertRaises(ValueError):
            panel([[np.nan]], flags=[[VERIFIED]])                    # flag without a value
        with self.assertRaises(ValueError):
            ProvenancePanel(['A', 'B'], [2000, 2001], [[1.0, 2.0]])  # row/entities count

    def test_long_records_roundtrip_and_duplicates_rejected(self):
        p = from_long([('A', 2000, 1.0, VERIFIED), ('A', 2001, 2.0, MEMORY),
                       ('B', 2000, 3.0, VERIFIED)], years=[2000, 2001], entities=['A', 'B'])
        self.assertEqual(p.n_entities, 2)
        self.assertEqual(p.flags.tolist(), [['v', 'm'], ['v', '']])
        with self.assertRaises(ValueError):
            from_long([('A', 2000, 1.0, VERIFIED), ('A', 2000, 2.0, VERIFIED)])

    def test_imputed_cells_are_derived_and_originals_kept(self):
        p = panel([[1.0, np.nan, 3.0]])
        before = p.values.copy()
        out = impute_panel(p, LinearInterpolator())
        np.testing.assert_array_equal(p.values, before)              # input not mutated
        self.assertEqual(out.flags.tolist(), [[VERIFIED, DERIVED, VERIFIED]])
        self.assertAlmostEqual(out.values[0, 1], 2.0, places=12)
        self.assertIn('linear', out.history[0])
        # a second imputation may refill its own derived cell, flagging it derived again
        out2 = impute_panel(out, LinearInterpolator())
        self.assertEqual(out2.flags[0, 1], DERIVED)
        # ... but it must not overwrite a verified observation without an explicit opt-in
        with self.assertRaises(ValueError):
            out.with_fill(np.zeros_like(out.values), where=np.ones(out.shape, bool))
        forced = out.with_fill(np.array([[9.9, 0.0, 0.0]]),
                               where=np.array([[True, False, False]]), overwrite=True)
        self.assertEqual(forced.values[0, 0], 9.9)
        self.assertEqual(forced.flags[0, 0], DERIVED)

    def test_methods_fit_only_on_requested_flags(self):
        # a wild memory-flagged point must not pull the fitted trend when use_flags=('v',)
        years = np.arange(2000.0, 2011.0)
        values = 2.0 + 0.1 * (years - 2000)
        values[5] = np.nan
        flags = np.where(np.isfinite(values), VERIFIED, MISSING).astype('<U1')[None, :]
        flags[0, 4] = MEMORY
        base = panel([values], years, flags=flags)
        base_v = LogitSCurve().fit(base, use_flags=(VERIFIED,)).predict()
        # move the memory point far off the trend: only the ('v', 'm') fit should react
        values2 = values.copy()
        values2[4] = 99.0
        moved = panel([values2], years, flags=flags)
        v_only = LogitSCurve().fit(moved, use_flags=(VERIFIED,)).predict()
        all_flags = LogitSCurve().fit(moved, use_flags=OBSERVED_FLAGS).predict()
        self.assertAlmostEqual(base_v.values[0, 5], v_only.values[0, 5], places=10)
        self.assertGreater(abs(all_flags.values[0, 5] - v_only.values[0, 5]), 1.0)

    def test_harness_scores_only_requested_flags(self):
        # only 3 verified years per entity, so verified-only deletions are capacity-limited
        T = 22
        values = np.tile(np.arange(T, dtype=float), (3, 1))
        flags = np.full(values.shape, MEMORY, dtype='<U1')
        flags[:, :3] = VERIFIED
        p = panel(values, flags=flags)
        plan = make_deletions(p, gap_lengths=(1,), n_replicates=1, seed=0,
                              score_flags=(VERIFIED,), points_per_gap=6)[0]
        self.assertTrue(plan['mask'].any())
        self.assertFalse((plan['score'] & (p.flags == MEMORY)).any())
        rep_v = holdout(p, methods=['linear'], gap_lengths=(1,), n_replicates=1, seed=0,
                        points_per_gap=6, score_flags=(VERIFIED,))
        rep_both = holdout(p, methods=['linear'], gap_lengths=(1,), n_replicates=1, seed=0,
                           points_per_gap=6, score_flags=(VERIFIED, MEMORY))
        n_v = rep_v.scores['linear'][1]['n']
        n_both = rep_both.scores['linear'][1]['n']
        self.assertGreater(n_v, 0)
        self.assertGreater(n_both, n_v)


class InterpolationTests(unittest.TestCase):
    def test_linear_recovers_an_exactly_linear_series(self):
        years = np.arange(1990.0, 2010.0)
        truth = np.vstack([1.0 + 0.5 * (years - 1990.0),
                           10.0 - 0.2 * (years - 1990.0)])
        values = truth.copy()
        values[0, 4:9] = np.nan
        values[1, 12:18] = np.nan
        res = LinearInterpolator().fit(panel(values, years)).predict()
        self.assertLess(max_abs(res, truth), 1e-12)
        self.assertEqual(int(res.n_filled), 5 + 6)

    def test_linear_extrapolation_holds_the_nearest_observation(self):
        years = np.arange(2000.0, 2006.0)
        values = np.array([[1.0, np.nan, 3.0, np.nan, 5.0, np.nan]])
        res = LinearInterpolator(extrapolate='hold').fit(panel(values, years)).predict()
        self.assertEqual(res.values[0, 5], 5.0)                     # right end held
        no_ext = LinearInterpolator(extrapolate='none').fit(panel(values, years)).predict()
        self.assertTrue(np.isnan(no_ext.values[0, 5]))
        lin_ext = LinearInterpolator(extrapolate='linear').fit(panel(values, years)).predict()
        self.assertAlmostEqual(lin_ext.values[0, 5], 6.0, places=12)  # last-segment slope continued

    def test_loglinear_recovers_an_exactly_exponential_series(self):
        years = np.arange(1970.0, 2000.0)
        truth = np.exp(2.0 + 0.03 * (years - 1970.0))
        values = truth.copy()
        values[10:16] = np.nan
        res = LogLinearInterpolator().fit(panel([values], years)).predict()
        self.assertLess(max_abs(res, truth), 1e-10)
        self.assertTrue(np.all(res.values[res.filled] > 0))

    def test_loglinear_falls_back_to_linear_on_nonpositive_segments(self):
        years = np.arange(2000.0, 2008.0)
        values = np.array([[0.0, np.nan, np.nan, 3.0, np.nan, -2.0, np.nan, 4.0]])
        logres = LogLinearInterpolator().fit(panel(values, years)).predict()
        linres = LinearInterpolator().fit(panel(values, years)).predict()
        self.assertTrue(np.all(np.isfinite(logres.values[logres.filled])))
        # segments whose endpoint is non-positive use the linear fallback, cell for cell
        for j in (1, 2, 4, 6):
            self.assertAlmostEqual(logres.values[0, j], linres.values[0, j], places=10)

    def test_fit_predict_contract(self):
        p = panel([[1.0, np.nan, 3.0]])
        with self.assertRaises(RuntimeError):
            LinearInterpolator().predict()
        imp = LinearInterpolator().fit(p)
        with self.assertRaises(ValueError):
            imp.predict(np.ones((2, 2), bool))
        res = imp.predict(np.array([[False, True, False]]))
        self.assertEqual(int(res.n_filled), 1)
        self.assertAlmostEqual(res.values[0, 1], 2.0, places=12)
        self.assertTrue(np.isnan(res.values[0, 0]))                 # predictions only where asked
        with self.assertRaises(TypeError):
            LinearInterpolator().fit(np.zeros((2, 2)))


class BoundedRateTests(unittest.TestCase):
    def test_scurve_beats_linear_on_a_known_logistic_series(self):
        x = np.arange(0.0, 101.0)
        truth = 100.0 / (1.0 + np.exp(-0.15 * (x - 50.0)))
        values = truth.copy()
        values[43:58] = np.nan
        p = panel([values], x)
        scurve = LogitSCurve().fit(p).predict()
        linear = LinearInterpolator().fit(p).predict()
        self.assertLess(mae(scurve, truth), 0.05 * mae(linear, truth))
        self.assertLess(mae(scurve, truth), 1e-8)                   # exactly logit-linear

    def test_scurve_predictions_stay_inside_the_bounds(self):
        x = np.arange(1990.0, 2020.0)
        truth = np.clip(100.0 / (1.0 + np.exp(-0.3 * (x - 2005.0))), 0.0, 100.0)
        truth[3] = 0.0                                              # observed at the bounds
        truth[27] = 100.0
        values = truth.copy()
        values[10] = np.nan
        values[20] = np.nan
        res = LogitSCurve(lower=0.0, upper=100.0).fit(panel([values], x)).predict(
            np.ones((1, x.size), bool))
        vals = res.values[np.isfinite(res.values)]
        self.assertGreater(vals.size, x.size - 2)
        self.assertGreaterEqual(float(vals.min()), 0.0)
        self.assertLessEqual(float(vals.max()), 100.0)

    def test_ilostat_unemployment_rates_stay_bounded(self):
        p = data.load_ilostat('all')
        self.assertGreater(p.n_entities, 50)
        res = LogitSCurve(0.0, 100.0).fit(p).predict()
        finite = res.values[np.isfinite(res.values)]
        self.assertGreater(finite.size, 100)
        self.assertGreaterEqual(float(finite.min()), 0.0)
        self.assertLessEqual(float(finite.max()), 100.0)


class CohortTests(unittest.TestCase):
    @staticmethod
    def _cohort_series(L=40.0, n=61, s0=2.0, e0=2.0, slope=0.05):
        E = e0 + slope * np.arange(float(n))
        S = np.zeros(n)
        S[0] = s0
        for k in range(1, n):
            S[k] = (1.0 - 1.0 / L) * S[k - 1] + (1.0 / L) * E[k]
        return S, E

    def test_recovers_a_cohort_generated_series(self):
        S, _ = self._cohort_series()
        years = 1980.0 + np.arange(S.size)
        values = S.copy()
        values[20:31] = np.nan
        p = panel([values], years)
        cohort = CohortBackcast(replacement_years=40.0).fit(p).predict()
        linear = LinearInterpolator().fit(p).predict()
        self.assertLess(max_abs(cohort, S), 1e-9)
        self.assertGreater(max_abs(linear, S), 1e-3)                # the cohort shape is not linear

    def test_recovers_the_entering_cohort_series(self):
        S, _ = self._cohort_series()
        years = 1980.0 + np.arange(S.size)
        values = S.copy()
        values[20:31] = np.nan
        imp = CohortBackcast(replacement_years=40.0).fit(panel([values], years))
        nodes = imp.cohort_attainment()
        self.assertEqual(list(nodes), ['C0'])
        node_years, node_vals = nodes['C0']
        self.assertGreater(node_years.size, 10)
        truth = 2.0 + 0.05 * (node_years - 1980.0)                 # E(t) used to generate the series
        np.testing.assert_allclose(node_vals, truth, atol=1e-9)

    def test_backcasts_before_the_span_and_projects_after_it(self):
        S, _ = self._cohort_series()
        years = 1980.0 + np.arange(S.size)
        values = S.copy()
        values[:5] = np.nan                                         # back-cast 1975-1979
        values[-5:] = np.nan                                        # project 2036-2040
        res = CohortBackcast().fit(panel([values], years)).predict()
        self.assertEqual(int(res.n_filled), 10)
        self.assertTrue(np.all(np.isfinite(res.values[res.filled])))
        self.assertLess(float(res.values[0, :5].max()), S[5] + 1e-6)   # below the first observed
        self.assertGreater(float(res.values[0, -5:].min()), S[-6] - 1e-6)  # above the last observed

    def test_barro_lee_five_year_waves(self):
        p = data.load_barro_lee()
        self.assertEqual(p.n_years, 13)
        sub = p.subset(entity_mask=np.arange(p.n_entities) < 20)
        truth = sub.values.copy()
        values = truth.copy()
        values[:, 6] = np.nan                                       # delete the 1980 wave
        values[0:5, 9:11] = np.nan                                  # delete the 1995-2000 waves
        res = CohortBackcast().fit(panel(values, sub.years)).predict()
        self.assertEqual(int(res.n_filled), 20 + 10)
        self.assertTrue(np.all(np.isfinite(res.values[res.filled])))
        self.assertGreaterEqual(float(res.values[res.filled].min()), 0.0)
        self.assertLessEqual(float(res.values[res.filled].max()), 20.0)
        self.assertLess(mae(res, truth), 0.5)


class KalmanTests(unittest.TestCase):
    def _setup(self):
        truth, years = local_linear_trend()
        obs = np.ones(truth.shape, bool)
        rng = np.random.default_rng(21)
        holes = rng.random(truth.shape) < 0.10
        holes[:, :3] = False
        holes[:, -3:] = False
        obs[holes] = False
        p = panel(np.where(obs, truth, np.nan), years)
        hyper = (0.05, 1e-4, 0.10)                                  # known DGP parameters
        return truth, years, p, hyper

    def test_interval_coverage_is_near_nominal(self):
        truth, _, p, hyper = self._setup()
        k = KalmanSmoother(coverage=0.90, hyper=hyper).fit(p)
        res = k.predict()
        self.assertGreater(res.n_filled, 20)
        coverage = res.coverage(truth)
        self.assertGreater(coverage, 0.80)
        self.assertLess(coverage, 0.985)
        self.assertGreater(res.width(), 0.0)

    def test_intervals_widen_with_gap_length(self):
        truth, years, _, hyper = self._setup()
        widths = []
        for g in (1, 3, 10):
            obs = np.ones(truth.shape, bool)
            obs[:, 30:30 + g] = False
            p = panel(np.where(obs, truth, np.nan), years)
            res = KalmanSmoother(coverage=0.90, hyper=hyper).fit(p).predict()
            widths.append(res.width())
        self.assertLess(widths[0], widths[1])
        self.assertLess(widths[1], widths[2])

    def test_smoother_tracks_the_state_through_gaps(self):
        truth, years, p, hyper = self._setup()
        res = KalmanSmoother(coverage=0.90, hyper=hyper).fit(p).predict()
        m = res.filled
        self.assertGreater(float(np.corrcoef(res.values[m], truth[m])[0, 1]), 0.8)

    def test_entity_with_no_observations_stays_missing(self):
        truth, years = local_linear_trend(n_entities=2, n_years=30, seed=2)
        values = truth.copy()
        values[1] = np.nan                                          # second country never observed
        values[0, 5:8] = np.nan                                     # a gap to fill in the first
        res = KalmanSmoother(fit_hyper=True).fit(panel(values, years)).predict()
        self.assertTrue(np.all(np.isnan(res.values[1])))
        self.assertTrue(np.isfinite(res.values[0]).any())

    def test_fitted_observation_variance_is_reasonable(self):
        truth, years, p, _ = self._setup()
        k = KalmanSmoother(fit_hyper=True).fit(p)
        self.assertAlmostEqual(k.hyper_['q_level'] / 0.05, 1.0, delta=1.0)
        self.assertAlmostEqual(k.hyper_['obs_var'] / 0.10, 1.0, delta=0.5)
        self.assertGreater(k.loglik_, -np.inf)

    def test_deterministic(self):
        truth, years, p, hyper = self._setup()
        a = KalmanSmoother(hyper=hyper).fit(p).predict()
        b = KalmanSmoother(hyper=hyper).fit(p).predict()
        np.testing.assert_array_equal(a.values, b.values)
        np.testing.assert_array_equal(a.lower, b.lower)


class MultipleImputationTests(unittest.TestCase):
    @staticmethod
    def _panel(seed=3, n=30, T=30):
        rng = np.random.default_rng(seed)
        years = 1990.0 + np.arange(T, dtype=float)
        year_factor = np.cumsum(rng.normal(0.0, 0.8, T))
        level = rng.normal(10.0, 1.0, n)
        truth = level[:, None] + year_factor[None, :] + rng.normal(0.0, 0.3, (n, T))
        obs = np.ones((n, T), bool)
        obs[0, 5:25] = False                                        # one country, a 20-year gap
        obs[1, 8:18] = False
        obs[:, :2] = True
        return truth, years, panel(np.where(obs, truth, np.nan), years)

    def test_deterministic_draws_and_pooling_rule(self):
        truth, years, p = self._panel()
        r1 = AmeliaMI(draws=10, iterations=2, seed=4).fit(p).predict()
        r2 = AmeliaMI(draws=10, iterations=2, seed=4).fit(p).predict()
        self.assertEqual(r1.draws.shape, (10, p.n_entities, p.n_years))
        np.testing.assert_array_equal(r1.draws, r2.draws)
        r3 = AmeliaMI(draws=10, iterations=2, seed=5).fit(p).predict()
        self.assertFalse(np.array_equal(np.nan_to_num(r1.draws), np.nan_to_num(r3.draws)))
        # pooled point is the mean of the draws, and the interval is the Rubin interval
        m = r1.filled
        at_draws = r1.draws[:, m]                                   # (M, n_filled), all finite
        point = at_draws.mean(axis=0)
        between = at_draws.var(axis=0, ddof=1)
        se = np.sqrt((1.0 + 1.0 / 10) * between)
        from scipy.stats import norm
        z = norm.ppf(0.95)
        np.testing.assert_allclose(r1.values[m], point, rtol=1e-10, atol=1e-10)
        np.testing.assert_allclose(r1.lower[m], point - z * se, rtol=1e-10, atol=1e-10)
        np.testing.assert_allclose(r1.upper[m], point + z * se, rtol=1e-10, atol=1e-10)

    def test_borrows_the_year_cross_section_from_other_countries(self):
        truth, years, p = self._panel()
        mi = AmeliaMI(draws=10, iterations=2, seed=1).fit(p).predict()
        linear = LinearInterpolator().fit(p).predict()
        self.assertLess(mae(mi, truth), 0.5 * mae(linear, truth))
        self.assertGreater(mi.coverage(truth), 0.75)
        self.assertLess(mi.coverage(truth), 0.99)

    def test_sparse_panel_does_not_crash(self):
        p = data.load_ilostat('all')
        res = AmeliaMI(draws=4, iterations=1, seed=0).fit(p).predict()
        finite = res.values[np.isfinite(res.values)]
        self.assertGreater(finite.size, 100)
        self.assertTrue(np.all(np.isfinite(res.draws[:, res.filled][:, :10])))


class HarnessTests(unittest.TestCase):
    def test_deletions_have_anchors_and_disjoint_blocks(self):
        p = panel(np.tile(np.arange(40.0), (2, 1)))
        plans = make_deletions(p, gap_lengths=(1, 2, 5, 10), n_replicates=3, seed=0,
                               points_per_gap=6)
        self.assertEqual(len(plans), 3)
        for rep, plan in enumerate(plans):
            self.assertTrue(plan['mask'].any())
            for i in range(p.n_entities):
                cols = np.flatnonzero(plan['mask'][i])
                if cols.size == 0:
                    continue
                runs = np.split(cols, np.flatnonzero(np.diff(cols) != 1) + 1)
                for run in runs:
                    a, b = int(run[0]), int(run[-1])
                    self.assertEqual(int(plan['group'][i, a]), b - a + 1)
                    self.assertTrue(p.observed()[i, a - 1])
                    self.assertTrue(p.observed()[i, b + 1])
            if rep:
                self.assertFalse(np.array_equal(plans[rep - 1]['mask'], plan['mask']))

    def test_gap_length_ordering_and_determinism(self):
        years = np.arange(1960.0, 2010.0)
        truth = np.vstack([3.0 + 0.4 * (years - 1960.0) + 0.002 * (years - 1960.0) ** 2,
                           8.0 + 0.1 * (years - 1960.0)])
        truth = np.tile(truth, (2, 1))
        p = panel(truth, years)
        kwargs = dict(methods=['linear', 'loglinear'], gap_lengths=(1, 2, 5, 10),
                      n_replicates=2, seed=3, points_per_gap=8)
        rep = holdout(p, **kwargs)
        for m in ('linear', 'loglinear'):
            short, long_ = rep.scores[m][1]['mae'], rep.scores[m][10]['mae']
            self.assertTrue(np.isfinite(short) and np.isfinite(long_))
            self.assertLess(short, long_)
            self.assertGreater(rep.scores[m][1]['n'], 0)
        rep2 = holdout(p, **kwargs)
        self.assertEqual(rep.table('mae'), rep2.table('mae'))       # deterministic
        self.assertIn('| linear |', rep.table('mae'))
        self.assertEqual(rep.best(10)[0], 'linear')

    def test_bad_gap_length_raises(self):
        p = panel([np.arange(10.0)])
        with self.assertRaises(ValueError):
            make_deletions(p, gap_lengths=(10,), n_replicates=1)
        with self.assertRaises(ValueError):
            holdout(p, methods=['linear'], gap_lengths=(0,), n_replicates=1)


class RealDataTests(unittest.TestCase):
    """Gap-length error ordering on the public data the module ships with (PWT, Barro-Lee)."""

    def test_pwt_gdp_short_gaps_beat_long_gaps(self):
        p = data.load_pwt('gdp_pc', year_min=1960, year_max=2019)
        p = p.subset(entity_mask=data.near_complete(p, min_obs=55))
        self.assertGreater(p.n_entities, 50)
        rep = holdout(p, methods=['linear', 'loglinear'], gap_lengths=(1, 2, 5, 10),
                      n_replicates=2, seed=0, points_per_gap=60, score_transform=np.log)
        for m in ('linear', 'loglinear'):
            mae_1 = rep.scores[m][1]['mae']
            mae_2 = rep.scores[m][2]['mae']
            mae_10 = rep.scores[m][10]['mae']
            self.assertTrue(np.isfinite(mae_1) and np.isfinite(mae_10))
            self.assertLess(mae_1, mae_10, m)
            self.assertLess(mae_2, mae_10, m)
            self.assertEqual(rep.scores[m][1]['n'], rep.scores[m][10]['n'])

    def test_attainment_short_gaps_beat_long_gaps(self):
        p = data.load_attainment(year_min=1991, year_max=2017)
        p = p.subset(entity_mask=p.observed().sum(axis=1) >= 20)
        self.assertGreater(p.n_entities, 100)
        rep = holdout(p, methods=['linear', 'cohort'], gap_lengths=(1, 2, 5, 10),
                      n_replicates=2, seed=0, points_per_gap=60)
        for m in ('linear', 'cohort'):
            mae_1 = rep.scores[m][1]['mae']
            mae_2 = rep.scores[m][2]['mae']
            mae_10 = rep.scores[m][10]['mae']
            self.assertTrue(np.isfinite(mae_1))
            self.assertLess(mae_1, mae_10, m)
            self.assertLess(mae_2, mae_10, m)
        # the cohort rung is designed for attainment: its predictions are plausible and finite
        cohort = rep.scores['cohort']
        for g in (1, 2, 5, 10):
            self.assertGreater(cohort[g]['n'], 100)
            self.assertLess(cohort[g]['mae'], 1.0)

    def test_barro_lee_holdout_bounded(self):
        p = data.load_barro_lee()
        rep = holdout(p, methods=['linear', 'cohort'], gap_lengths=(1, 2),
                      n_replicates=2, seed=0, points_per_gap=40)
        self.assertEqual(rep.gaps, [1, 2])
        for m in ('linear', 'cohort'):
            for g in (1, 2):
                self.assertGreater(rep.scores[m][g]['n'], 50)
                self.assertLess(rep.scores[m][g]['mae'], 1.0)


class LadderTests(unittest.TestCase):
    def test_ladder_names_and_instances(self):
        names = impute.method_names()
        self.assertEqual(names, ['linear', 'loglinear', 'scurve', 'cohort', 'kalman', 'amelia'])
        for n in names:
            self.assertIsInstance(make_imputer(n), impute.Imputer)
        with self.assertRaises(KeyError):
            make_imputer('nope')

    def test_imputation_result_validation(self):
        with self.assertRaises(ValueError):
            ImputationResult(np.zeros((2, 2)), np.zeros((3, 3), bool))
        with self.assertRaises(ValueError):
            ImputationResult(np.zeros((2, 2)), np.zeros((2, 2), bool), lower=np.zeros((2, 2)))
        r = ImputationResult(np.array([[1.0, np.nan]]), np.array([[True, True]]),
                             lower=np.array([[0.5, np.nan]]), upper=np.array([[1.5, np.nan]]),
                             nominal=0.9)
        self.assertEqual(r.n_filled, 1)
        self.assertEqual(r.coverage(np.array([[1.2, 5.0]])), 1.0)

    def test_full_ladder_runs_on_one_panel(self):
        years = np.arange(1990.0, 2020.0)
        truth = np.vstack([100.0 / (1.0 + np.exp(-0.2 * (years - 2005.0))),
                           5.0 + 0.2 * (years - 1990.0)])
        values = truth.copy()
        values[0, 8:14] = np.nan
        values[1, 20:26] = np.nan
        p = panel(values, years)
        for name in impute.method_names():
            res = make_imputer(name).fit(p).predict()
            self.assertGreater(res.n_filled, 0, name)
            self.assertTrue(np.all(np.isfinite(res.values[res.filled])), name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
