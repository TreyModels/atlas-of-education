"""Tier 1 and tier 2 checks for the categorical (Tilly) core.

Run from engine/:  python -m unittest firms.test_tilly -v
"""
import math, os, sys, unittest
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import model as M, categorical as C, data_china as D

REF = {k: M.YouthMarket(D).p[k] for k in ('S_ref', 'g_H', 'g_N')}
ALL = dict(sec_open=0.10, hoard=0.4, wait_max=0.06, em_rate=0.5, ex=0.2)


def run(**kw):
    return C.CategoricalMarket(D, **dict(REF, **kw)).run()


def late(R, k):
    v = [x for x, y in zip(R[k], R['year']) if y >= 2024]
    v = [x for x in v if x == x]
    return float(np.mean(v))


class Tier1(unittest.TestCase):
    def test_nests_model_py_exactly(self):
        """With no boundary mechanisms the categorical core IS the two-type model."""
        for over in ({}, dict(rank='random'), dict(sigma_A=2.5, lam_g=0.01, d=-0.3), dict(dr_drop=0.2, e_prop=0.3)):
            a = M.YouthMarket(D, **REF, **over).run(); b = run(**over)
            for k in ('rate_old', 'rate_new', 'u_G', 'u_N', 'f_g', 'V_n', 'under', 'grad_share_n_hires'):
                self.assertLess(np.max(np.abs(np.array(a[k]) - np.array(b[k]))), 1e-10, (k, over))

    def test_people_conserved_with_all_mechanisms(self):
        for over in (ALL, dict(ALL, rank='random'), dict(ALL, d=-0.5, em_rate=2.0)):
            R = run(**over)
            self.assertLess(max(abs(b) for b in R['balance']), 1e-9)
            self.assertGreaterEqual(min(R['waiting']), -1e-12)

    def test_secure_hires_never_exceed_openings(self):
        R = run(**ALL)
        cap = 0.10 * M.DEFAULTS['psi_g'] * 0.5 * (D.graduates(2018) + D.graduates(2019)) / 12
        self.assertLessEqual(max(R['sec_hires']), cap + 1e-12)

    def test_exploitation_ledger(self):
        R = run(ex=0.2)
        self.assertTrue(all(x >= 0 for x in R['rent_exploit']))
        self.assertGreater(late(R, 'rent_exploit'), 0)
        self.assertEqual(max(run()['rent_exploit']), 0.0)


class Tier2(unittest.TestCase):
    def test_categories_without_boundaries_are_inert(self):
        """Tilly: a category matters only when an organizational boundary treats it differently. With secure posts and
        waiting switched on but no hoarding, no wage wedge, equal family support and no insider resources, the insider
        share is irrelevant to every aggregate and the two categories have identical outcomes."""
        kw = dict(sec_open=0.10, hoard=0.0, wait_max=0.06, ex=0.0, supp_in=0.7, supp_out=0.7, z_ins=0.0)
        a, b = run(ins_g=0.2, ins_n=0.2, **kw), run(ins_g=0.8, ins_n=0.8, **kw)
        for k in ('rate_new', 'slack', 'u_G', 'u_N', 'waiting', 'sec_hires', 'output'):
            self.assertLess(np.max(np.abs(np.array(a[k]) - np.array(b[k]))), 1e-9, k)
        self.assertLess(np.max(np.abs(np.array(a['u_G_in']) - np.array(a['u_G_out']))), 1e-9)

    def test_hoarding_tilts_posts_to_insiders(self):
        R = run(sec_open=0.10, hoard=0.4, supp_in=0.7, supp_out=0.7)
        self.assertGreater(late(R, 'sec_ins_share'), 0.5 + 0.1)
        self.assertLess(late(R, 'u_G_in'), late(R, 'u_G_out'))

    def test_exploitation_makes_outsiders_cheaper_and_hired_first(self):
        """With ranking by value, the wedge raises firms' value of outsiders, so outsider non-graduates find jobs more
        often while earning less: inequality in pay, not in jobs."""
        R = run(ex=0.2)
        self.assertLess(late(R, 'w_N_out'), late(R, 'w_N_in'))
        self.assertLess(late(R, 'u_N_out'), late(R, 'u_N_in'))

    def test_emulation_needs_prevalence(self):
        """Requirements spread only once degrees pass the threshold share; with an unreachable threshold nothing happens."""
        a, b = run(em_rate=0.5, em_threshold=0.99), run()
        self.assertEqual(max(a['c_req']), 0.0)
        self.assertLess(np.max(np.abs(np.array(a['rate_new']) - np.array(b['rate_new']))), 1e-10)
        self.assertGreater(late(run(em_rate=0.5, em_threshold=0.30), 'c_req'), 0.0)

    def test_adaptation_moves_slack_out_of_the_measured_rate(self):
        kw = dict(sec_open=0.10, hoard=0.4)
        a, b = run(wait_max=0.06, **kw), run(wait_max=0.0, **kw)
        self.assertLess(late(a, 'rate_new'), late(b, 'rate_new'))
        for s, r in zip(a['slack'], a['rate_new']):
            self.assertGreaterEqual(s + 1e-12, r)


if __name__ == '__main__':
    unittest.main()
