import math
import unittest
import numpy as np
from phaseb_corrected import (WORLDS, advance_interval_death_flag, classify,
                              next_year_recency, seed_registry, simulate_b1,
                              run_smoke_design)

class PhaseBCorrectedSmoke(unittest.TestCase):
    def test_b1_is_missing_not_zero_without_events(self):
        u=simulate_b1("P", 7, 0.0, women=0)
        self.assertIsNone(u["B1"])
        self.assertFalse(u["estimable"])
        self.assertIsNotNone(u["missing_reason"])

    def test_within_mother_support_and_finite_when_estimable(self):
        u=simulate_b1("P", 8, 0.6, women=800)
        if u["estimable"]:
            self.assertGreaterEqual(u["n_mothers_with_both"],5)
            self.assertTrue(math.isfinite(u["B1"]))
        else:
            self.assertIsNone(u["B1"])

    def test_death_remains_attached_to_interval_beyond_two_year_hazard_window(self):
        flag=np.array([False])
        # Death occurs after the prior birth; two intervening years pass without
        # another death, then the next birth closes an exposed interval.
        _,flag=advance_interval_death_flag([True],[False],flag)
        _,flag=advance_interval_death_flag([False],[False],flag)
        _,flag=advance_interval_death_flag([False],[False],flag)
        exposed,flag=advance_interval_death_flag([False],[True],flag)
        self.assertTrue(bool(exposed[0]))
        self.assertFalse(bool(flag[0]))

    def test_death_only_changes_next_two_year_hazards(self):
        recency=np.array([0])
        hazard_multiplier=[]
        # Year t hazard is computed from prior state; death at end of t sets 2.
        hazard_multiplier.append(1.8 if recency[0] else 1.0)
        recency=next_year_recency([True],recency)
        for _ in range(2):
            hazard_multiplier.append(1.8 if recency[0] else 1.0)
            recency=next_year_recency([False],recency)
        hazard_multiplier.append(1.8 if recency[0] else 1.0)
        self.assertEqual(hazard_multiplier,[1.0,1.8,1.8,1.0])

    def test_sha256_namespaced_seed_registry_has_no_collisions(self):
        keys=[]
        for split,n in (("calibration",20),("heldout",60),("replication",60)):
            for k in range(n):
                keys.append(("upstream_s0",split,k,"shared"))
                for w in WORLDS:
                    keys.extend((("upstream_s1",split,k,w),("fertility_s1",split,k,w),
                                 ("fertility_s0",split,k,w)))
        values=list(seed_registry(keys).values())
        self.assertEqual(len(values),len(set(values)))
        self.assertEqual(len(values),4*(20+60+60)*3+(20+60+60))

    def test_null_uses_independent_samples_instead_of_relabelled_clone(self):
        vals=[simulate_b1(w,123+1000*i,0.5,cl_post=.3,null=True,women=500)["B1"]
              for i,w in enumerate(WORLDS)]
        self.assertGreater(len(set(vals)), 1)

    def test_classifier_accounts_for_missingness(self):
        train=[{"world":w,"B1":float(i)} for i,w in enumerate(WORLDS)]
        test=[{"world":w,"B1":float(i)} for i,w in enumerate(WORLDS)] + [{"world":"P","B1":None}]
        got=classify(train,test,"B1")
        self.assertEqual(got["n"],4)
        self.assertEqual(got["accuracy"],1.0)

    def test_smoke_result_has_separate_blocks_and_null_units(self):
        d=run_smoke_design(women=100)
        self.assertTrue(all(k+"_gates" in d for k in ("calibration","heldout","replication")))
        self.assertEqual(set(d["heldout_gates"]), {"B1","B2","B3"})
        self.assertEqual(set(d["s0_heldout_descriptive"]), {"B1","B2","B3"})
        self.assertIn("no p-values", " ".join(d["limitations"]))
        self.assertEqual(len(d["units"]), 80)

if __name__=="__main__": unittest.main()
