import unittest
import numpy as np
import run_corrected as m

class MatrixChecks(unittest.TestCase):
    def test_seed_is_repeatable_and_namespaced(self):
        self.assertEqual(m.seed('country',0,1),m.seed('country',0,1))
        self.assertNotEqual(m.seed('country',0,1),m.seed('country',1,1))
        self.assertNotEqual(m.seed('households',0,1,'P'),m.seed('households',0,1,'S'))
    def test_planned_full_design_has_no_seed_collisions(self):
        seeds=[m.seed('households',b,c,w) for b in range(10) for c in range(64) for w in m.WORLDS]
        self.assertEqual(len(seeds),len(set(seeds)))
    def test_simulator_repeats_and_changes_by_block(self):
        a=m.generate((0,0,'P',60));b=m.generate((0,0,'P',60));c=m.generate((1,0,'P',60))
        np.testing.assert_array_equal(a[4]['ger'],b[4]['ger'])
        self.assertFalse(np.array_equal(a[4]['ger'],c[4]['ger']))
    def test_null_is_shared_baseline_not_world_label(self):
        self.assertEqual(m.model.theta_of('P',0),m.model.theta_of('S',0))
        self.assertNotEqual(m.seed('households',0,1,'P'),m.seed('households',0,1,'null'))
    def test_five_year_windows_have_more_observations(self):
        series={}
        for i in range(8):
            t=np.arange(25,dtype=float); y=np.sin(t/5+i)+i/3; ger=np.cos(t/7+i/3)+i/4
            series[i,'P']={'group':i%4,'values':{'cl':y,'ger':ger,'inc':t*(i+1)}}
        five=m.fit(series,'S2','cl',0,0,'all');ten=m.fit(series,'S1','cl',0,0,'all')
        self.assertEqual(five['n'],8*20);self.assertEqual(ten['n'],8*15)
        self.assertNotAlmostEqual(five['slope'],ten['slope'])
    def test_paired_contrast_uses_block_variation(self):
        a=m.summarize([.01,.02,.03],.05)
        self.assertAlmostEqual(a['mean_difference'],.02)
        self.assertEqual(a['blocks'],3)
        self.assertIn('ci90',a)
        self.assertIn('error',m.summarize([.01,None],.05))
    def test_rank_deficiency_is_not_fabricated(self):
        series={(i,'P'):{'group':i%4,'values':{'cl':np.arange(25.),'ger':np.ones(25),'inc':np.arange(25.)}} for i in range(8)}
        self.assertIn('error',m.fit(series,'S1','cl',0,0,'all'))
if __name__=='__main__':unittest.main()
