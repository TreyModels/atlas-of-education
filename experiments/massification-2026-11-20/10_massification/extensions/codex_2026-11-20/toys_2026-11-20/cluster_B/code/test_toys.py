"""Structural tests for the Cluster B battery. Run: python3 -m unittest code/test_toys.py

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

These tests check accounting, pairing and reproducibility. They do NOT test any
substantive hypothesis: a passing test says the toy is wired correctly, never
that its outputs describe the world.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import exp4_visibility as e4
import exp5_queue as e5
import exp6_eligibility as e6


def _rows_mod(path):
    with open(path) as f:
        return [ln for ln in f if not ln.startswith("#")]


class CommonTests(unittest.TestCase):
    def test_seeded_draw_is_reproducible(self):
        a = e4.cell("signaling", 0.0, 20261120)
        b = e4.cell("signaling", 0.0, 20261120)
        self.assertEqual(a, b)

    def test_seed_41_reproduces_base_model(self):
        # model.run("signaling", visibility=0) at seed 41.
        r = e4.cell("signaling", 0.0, 41)
        self.assertEqual((r["applications"], r["public_admissions"],
                          r["private_admissions"], r["admissions"], r["graduate_hires"]),
                         (89, 30, 15, 45, 40))
        # model.run("signaling", visibility=1) has no applicants at all.
        self.assertEqual(e4.cell("signaling", 1.0, 41)["applications"], 0)
        # model.run("human_capital", visibility=1) hires 40 graduates.
        self.assertEqual(e4.cell("human_capital", 1.0, 41)["graduate_hires"], 40)

    def test_experiments_share_the_latent_draw_across_arms(self):
        for seed in (20261120, 20261121, 20261199):
            a, b = e4.cell("human_capital", 0.0, seed), e4.cell("signaling", 0.0, seed)
            for k in ("applications", "admissions", "public_admissions",
                      "private_admissions", "graduate_hires", "rejected_count"):
                self.assertEqual(a[k], b[k])


class Exp4Tests(unittest.TestCase):
    def test_accounting(self):
        for mech in e4.MECHANISMS:
            for v in e4.VISIBILITIES:
                r = e4.cell(mech, v, 20261120)
                self.assertEqual(r["public_admissions"] + r["private_admissions"], r["admissions"])
                self.assertEqual(r["rejected_count"], r["applications"] - r["applicant_hires"])
                self.assertLessEqual(r["private_admissions"], 30)

    def test_hc_applications_invariant_to_visibility(self):
        apps = {e4.cell("human_capital", v, 20261120)["applications"] for v in e4.VISIBILITIES}
        self.assertEqual(len(apps), 1)

    def test_signalling_market_shrinks_with_visibility(self):
        apps = [e4.cell("signaling", v, 20261120)["applications"] for v in (0.0, 0.5, 1.0)]
        self.assertEqual(apps, sorted(apps, reverse=True))
        self.assertEqual(apps[-1], 0)


class Exp5Tests(unittest.TestCase):
    def test_job_counts(self):
        for seed in (20261120, 20261121):
            self.assertEqual(e5.cell("skill_upgrade", "fixed_jobs", seed)["total_hires"],
                             e5.job_count(seed))
            self.assertTrue(35 <= e5.job_count(seed) <= 40)
            self.assertEqual(e5.cell("rank_upgrade", "responsive_jobs", seed)["total_hires"], 100)

    def test_treated_set_is_fully_hired_under_skill_upgrade(self):
        r = e5.cell("skill_upgrade", "fixed_jobs", 20261120)
        self.assertEqual(r["treated_group_hires"], 20)

    def test_rank_upgrade_leaves_skills_unchanged(self):
        a = e5.cell("rank_upgrade", "fixed_jobs", 20261120)
        b = e5.cell("reference", "fixed_jobs", 20261120)
        self.assertEqual(a["population_mean_skill"], b["population_mean_skill"])


class Exp6Tests(unittest.TestCase):
    def test_staging(self):
        for c in e6.CRED_SHARES:
            for vis in (True, False):
                retained = e6.cell(c, vis, False, 20261120)
                self.assertEqual(retained["uncred_offers"], 0)
                self.assertEqual(retained["eligible_count"], c)
                self.assertEqual(retained["vacancies"], max(0, e6.J_OFFERS - c))
                repealed = e6.cell(c, vis, True, 20261120)
                self.assertEqual(repealed["eligible_count"], 100)

    def test_blind_repealed_differs_from_visible_repealed(self):
        for c in e6.CRED_SHARES:
            vis = e6.cell(c, True, True, 20261120)["uncred_offer_rate"]
            blind = e6.cell(c, False, True, 20261120)["uncred_offer_rate"]
            self.assertGreater(blind, vis)


class OutputFileTests(unittest.TestCase):
    """Checks on RESULTS.csv, when present (run_all.py has been executed)."""

    def test_results_csv_schema_and_label(self):
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(here), "RESULTS.csv")
        if not os.path.exists(path):
            self.skipTest("RESULTS.csv not generated yet")
        with open(path) as f:
            lines = f.readlines()
        self.assertTrue(lines[0].startswith("# ILLUSTRATIVE TOY"))
        self.assertEqual(lines[1].strip(), "experiment,arm,seed,metric,value")
        body = [ln for ln in lines[2:] if ln.strip()]
        self.assertEqual(len(body) % 1, 0)
        experiments = {ln.split(",")[0] for ln in body}
        self.assertEqual(experiments,
                         {"exp4_visibility_mechanism", "exp5_queue_vs_human_capital",
                          "exp6_eligibility_vs_blind_ranking"})


if __name__ == "__main__":
    unittest.main()
