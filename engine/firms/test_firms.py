"""Tier 1 (identities) and tier 2 (theorems under stated assumptions) for the firm-side youth labour market.

Run from engine/:  python -m unittest firms.test_firms -v
A failure in tier 1 is a bug. A failure in tier 2 means the code does not implement the stated model.
Tier 3 (calibrated behaviour) is in calibrate_china.py and is never asserted here.
"""
import math, os, sys, unittest
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import model as M, data_china as D

BASE = dict(M.YouthMarket(D).p)
REF = dict(S_ref=BASE['S_ref'], g_H=BASE['g_H'], g_N=BASE['g_N'])


def run(**over):
    return M.YouthMarket(D, **dict(REF, **over)).run()


def after(R, key, y0=2019):
    return np.array([v for v, y in zip(R[key], R['year']) if y >= y0])


class Tier1Identities(unittest.TestCase):
    def test_people_are_conserved_every_month(self):
        for over in ({}, dict(rank='random'), dict(sigma_A=2.0, lam_g=0.01), dict(d=-1.0)):
            R = run(**over)
            self.assertLess(max(abs(b) for b in R['balance']), 1e-9, over)
            for k in ('UG', 'EGg', 'EGn', 'UN', 'EN'):
                self.assertGreaterEqual(min(R[k]), -1e-12, (k, over))

    def test_labour_force_independent_of_hiring(self):
        """LF of each type moves only with entry and ageing, so hiring cannot change it -- provided entry timing does not
        depend on hiring. (By design, unsigned graduates enter over Jul-Dec while signed ones start in July, so with
        july_g < 1 hiring shifts entry timing; with july_g = 1 the identity is exact.)"""
        a = run(july_g=1.0)
        b = run(july_g=1.0, f_g_ref=0.08, f_n_ref=0.10, rank='random', sigma_A=2.0)
        self.assertLess(np.max(np.abs(np.array(a['LF_G']) - np.array(b['LF_G']))), 1e-9)
        self.assertLess(np.max(np.abs(np.array(a['LF_N']) - np.array(b['LF_N']))), 1e-9)

    def test_free_entry_holds_in_the_nongraduate_market(self):
        R = run(d=-0.5)
        self.assertLess(max(abs(x) for x in R['resid_n']), 1e-6)

    def test_old_method_never_below_new(self):
        R = run()
        for o, n, m in zip(R['rate_old'], R['rate_new'], R['month']):
            self.assertGreaterEqual(o + 1e-12, n)
            if m in (7, 8):
                self.assertAlmostEqual(o, n, places=12)

    def test_urn_ball_bounds_and_constant_returns(self):
        for V, U, a in ((1.0, 2.0, 0.4), (3.0, 0.5, 1.0), (0.2, 7.0, 0.1)):
            h = M.urn_hires(V, U, a)
            self.assertLessEqual(h, min(V, a * U) + 1e-12)
            self.assertAlmostEqual(M.urn_hires(2 * V, 2 * U, a), 2 * h, places=12)

    def test_inverse_of_finding_rate(self):
        for f in (0.01, 0.1, 0.25, 0.39):
            x = M.urn_x_from_f(f, 0.4)
            self.assertAlmostEqual(0.4 * (1 - math.exp(-x)) / x, f, places=10)


class Tier2Theorems(unittest.TestCase):
    def test_supply_neutrality_under_constant_returns(self):
        """Pissarides: with CRS matching, free entry and no diminishing returns (sigma_A = inf), labour-market tightness
        is pinned by the job's value, so doubling graduates leaves their job-finding and unemployment rates unchanged.
        Downgrading is switched off (d large) so the graduate market is segmented."""
        kw = dict(sigma_A=math.inf, demand='flat', grad_demand='flat', d=50.0)
        a = run(**kw)
        b = run(grad_supply=lambda y: 2 * D.graduates(y), **kw)
        self.assertLess(np.max(np.abs(after(a, 'f_g') - after(b, 'f_g'))), 1e-12)
        self.assertLess(np.max(np.abs(after(a, 'u_G') - after(b, 'u_G'))), 1e-8)

    def test_diminishing_returns_break_neutrality(self):
        """With CES (sigma_A finite) and slow wages, more graduates lower graduate productivity and job finding."""
        kw = dict(sigma_A=5.0, demand='flat', grad_demand='flat', d=50.0, lam_g=0.02)
        a = run(**kw)
        b = run(grad_supply=lambda y: 1.5 * D.graduates(y) if y >= 2019 else D.graduates(y), **kw)
        sel = slice(-60, None)
        self.assertTrue(np.all(after(b, 'f_g')[sel] < after(a, 'f_g')[sel]))
        self.assertGreater(after(b, 'u_G')[sel].mean(), after(a, 'u_G')[sel].mean())

    def test_shimer_neutrality_of_aggregate_shocks(self):
        """If wages are a fixed share of productivity (z = 0, lam = 1) and vacancy costs scale with A, an aggregate
        productivity shock leaves tightness and job finding unchanged (Shimer 2005's puzzle in its exact form)."""
        shock = lambda y, m: 1.0 + 0.2 * math.sin(y + m / 2.0)
        kw = dict(sigma_A=math.inf, grad_demand='flat', z_g=0.0, z_n=0.0, lam_g=1.0, lam_n=1.0, d=50.0)
        a = run(demand='flat', **kw)
        b = run(demand=shock, **kw)
        self.assertLess(np.max(np.abs(after(a, 'f_g') - after(b, 'f_g'))), 1e-12)

    def test_ces_relative_wage(self):
        """Katz-Murphy: doubling a group's relative supply multiplies its marginal product by 2^(-1/sigma)."""
        for s in (1.5, 2.0, 5.0):
            self.assertAlmostEqual(M.ces_relative(2.0, 1.0, s), 2 ** (-1 / s), places=14)
        self.assertEqual(M.ces_relative(2.0, 1.0, math.inf), 1.0)

    def test_reservation_wage_solves_the_bellman_equations(self):
        """rU in the code equals rho*U from (rho)U = z + f(W-U), (rho)W = w + s(U-W), rho = r + exit."""
        for z, w, f, s, rho in ((0.75, 1.36, 0.2, 0.02, 0.004 + 1 / 27), (0.5, 1.0, 0.05, 0.03, 0.01)):
            Amat = np.array([[rho + f, -f], [-s, rho + s]])
            U, W = np.linalg.solve(Amat, [z, w])
            dg = rho + s
            self.assertAlmostEqual(rho * U, (dg * z + f * w) / (dg + f), places=12)

    def test_flexible_wages_absorb_supply(self):
        """Wage rigidity is what turns a supply shock into unemployment: with lam_g = 1 the rise in graduate
        unemployment from the same shock is smaller than with lam_g = 0.02."""
        shock = lambda y: 1.5 * D.graduates(y) if y >= 2019 else D.graduates(y)
        kw = dict(sigma_A=5.0, demand='flat', grad_demand='flat', d=50.0)
        rise = lambda lam: (after(run(grad_supply=shock, lam_g=lam, **kw), 'u_G')[-60:].mean()
                            - after(run(lam_g=lam, **kw), 'u_G')[-60:].mean())
        self.assertLess(rise(1.0), rise(0.02))


class Tier2Screening(unittest.TestCase):
    def test_no_graduate_applicants_means_ranking_is_irrelevant(self):
        kw = dict(d=50.0)
        a, b = run(rank='value', **kw), run(rank='random', **kw)
        self.assertLess(np.max(np.abs(np.array(a['f_n']) - np.array(b['f_n']))), 1e-6)

    def test_ranking_displaces_non_graduates(self):
        """Property check (not a general theorem): when graduates apply for non-graduate jobs and firms prefer them,
        non-graduates find jobs less often than under random hiring."""
        kw = dict(d=-0.5, eps=0.2)
        a, b = run(rank='value', **kw), run(rank='random', **kw)
        self.assertLess(after(a, 'f_n').mean(), after(b, 'f_n').mean())


class Tier1InformationSet(unittest.TestCase):
    def test_strict_demand_index_ignores_post_cutoff_data(self):
        """The vintage demand index must not move when youth data after the cutoff move (TODO 5, strict forecast)."""
        from firms import forecast_strict as F
        self.assertEqual(F.demand_leak_check(), 0.0)

    def test_vintage_hides_the_future(self):
        from firms import forecast_strict as F
        V = F.Vintage()
        self.assertIsNone(V.youth(2023, 1)); self.assertIsNone(V.urban(2023, 1))
        self.assertAlmostEqual(V.graduates(2023), D.GRADUATES[2023])          # announced autumn 2022
        self.assertNotEqual(V.graduates(2025), D.GRADUATES[2025])             # rule, not the realised class


class Tier1WageData(unittest.TestCase):
    def test_wage_anchor_uses_only_classes_public_at_cutoff(self):
        from firms import wage_anchor as W
        self.assertEqual(W.KNOWN, [2018, 2019, 2020, 2021])
        self.assertTrue(all(D.STARTING_WAGE_PUBLISHED[y] > (2022, 12) for y in W.TEST))

    def test_relative_starting_wage_arithmetic(self):
        self.assertAlmostEqual(D.relative_starting_wage(2022), 12 * 5990 / 114029, places=12)


class Tier1SeasonalDocking(unittest.TestCase):
    def test_seasonal_variant_nests_the_base_model(self):
        from firms import seasonal as S
        a, b = run(), S.SeasonalMarket(D, **REF).run()
        for k in ('rate_old', 'rate_new', 'V_g', 'w_g', 'u_G'):
            self.assertLess(max(abs(x - y) for x, y in zip(a[k], b[k])), 1e-9)

    def test_seasonal_variant_conserves_people(self):
        from firms import seasonal as S
        R = S.SeasonalMarket(D, dd=0.3, spread=10, **REF).run()
        self.assertLess(max(abs(x) for x in R['balance']), 1e-9)


class Tier1StoriesStrict(unittest.TestCase):
    def test_tournament_winner_strict_fit_ignores_post_cutoff_data(self):
        """Altering observations after Dec 2024 must not move a single fit residual (TODO R, strict protocol)."""
        from firms import stories_strict as SS
        self.assertEqual(SS.leak_check(), 0.0)

    def test_leak_check_is_not_vacuous(self):
        """Altering observations BEFORE the cutoff does move the residuals, so the zero above means something."""
        from firms import stories_strict as SS
        import numpy as np
        x = np.array([f[3] for f in SS.SPEC]); base = SS.residuals(x); saved = dict(D._NEW)
        try:
            for k in list(D._NEW):
                if k <= SS.CUT:
                    D._NEW[k] = (D._NEW[k][0] + 3.0, D._NEW[k][1])
            moved = float(np.max(np.abs(base - SS.residuals(x))))
        finally:
            D._NEW.clear(); D._NEW.update(saved)
        self.assertGreater(moved, 1.0)


if __name__ == '__main__':
    unittest.main()
