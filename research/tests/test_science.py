"""Small known-answer checks; these do not validate any model against society."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research'))
sys.path.insert(0,str(ROOT/'engine'))
import lab
import relfloor_countries as floor

SHADOW=ROOT/'experiments/shadow-abm/src/tutoring_abm'
sys.path.insert(0,str(SHADOW))
import model
import calibrate
import smc


class Contrasts(unittest.TestCase):
    def test_growth_and_intervention_can_have_opposite_signs(self):
        b=np.full(len(floor.YEARS),.45);b[-1]=.8
        f=np.full(len(floor.YEARS),.45);f[-1]=.7
        d=floor.premium_contrasts({'q3':b},{'q3':f})
        self.assertAlmostEqual(d['premium_effect_2035_q3'],-.1)
        self.assertAlmostEqual(d['scenario_change_2024_2035_q3'],.25)

    def test_falling_premium_cannot_raise_completion_in_this_monotone_model(self):
        for structure in floor.STRUCTS:
            for smooth in (False,True):
                cfg=floor.CFG['Cambodia']
                p=floor.draw(np.random.default_rng(9),structure,cfg,smooth_liq=smooth)
                b=floor.sim(p,cfg,'base',n=60,seed=3)
                f=floor.sim(p,cfg,'fall',n=60,seed=3)
                self.assertTrue(np.all(f['q3']<=b['q3']))
                self.assertTrue(np.array_equal(f['q3'][:27],b['q3'][:27]))


class ShadowObservation(unittest.TestCase):
    def test_provider_probabilities_count_pupils_across_subjects(self):
        w=model.World(model.Params(subject_offsets=(0.,0.)),seed=2)
        n=w.pupil_class.size
        pr=np.broadcast_to([.2,.2,0.],(n,2,3)).copy()
        w.choice=lambda everyone:pr
        o=w.outcomes()
        self.assertAlmostEqual(o['own_purchase_share'],.5)
        self.assertAlmostEqual(o['source_own_provider_share'],.36/.64)
        self.assertNotAlmostEqual(o['own_purchase_share'],o['source_own_provider_share'])

    def test_source_school_subset_is_explicit(self):
        w=model.World(model.Params(provider_school_ids=(1,2,4)),seed=2)
        self.assertTrue(np.array_equal(w.school,model.World(model.Params(),2).school))
        self.assertEqual(w.p.provider_school_ids,(1,2,4))

    def test_initial_conditions_do_not_change_exogenous_attributes(self):
        from dataclasses import replace
        p=model.Params()
        a=model.World(p,13);b=model.World(replace(p,initial_state='none_sell'),13)
        self.assertTrue(np.array_equal(a.resources,b.resources))
        self.assertTrue(np.array_equal(a.side_job,b.side_job))
        self.assertTrue(a.sell_own.all());self.assertFalse(b.sell_own.any())

    def test_nonconverged_state_cannot_pass_pattern_screen(self):
        o={k:v[0] for k,v in calibrate.TARGETS.items()}
        o.update(participation_urban=.835,participation_rural=.809,
                 source_external_provider_share=.01,converged=0.)
        self.assertEqual(calibrate.distances(o)['solver_nonconvergence'],float('inf'))

    def test_raw_importance_estimator_known_integral(self):
        # q = U(-1,1), prior = U(0,1), target event is the entire prior box.
        # Half the raw proposals are outside. Integral must equal one.
        terms=smc.raw_importance_terms(1.,[.5,.5],[1.,1.],[False,True,False,True])
        self.assertEqual(terms.tolist(),[0.,2.,0.,2.])
        self.assertEqual(float(terms.mean()),1.)


class ExperimentDesign(unittest.TestCase):
    def test_plan_is_deterministic_and_structural_cells_are_paired(self):
        a=lab.make_tasks(['credential'],'smoke');b=lab.make_tasks(['credential'],'smoke')
        self.assertEqual(a,b)
        paired=[t for t in a if t['draw']==0 and t['replicate']==0]
        self.assertEqual(len({t['parameter_seed'] for t in paired}),1)
        self.assertEqual(len({t['seed'] for t in paired}),1)
        self.assertEqual(len({t['id'] for t in a}),len(a))

    def test_repeats_are_nested_not_pseudoreplicated(self):
        d=lab.nested_summary([(0,0.),(0,2.),(1,2.),(1,4.)])
        self.assertEqual(d['draw_means']['n'],2)
        self.assertEqual(d['mean_within_draw_variance'],2.)
        self.assertEqual(d['draw_means']['mean'],2.)

    def test_sources_exist_for_every_protocol(self):
        sources=json.loads((ROOT/'research/literature.json').read_text())['sources']
        proto=json.loads((ROOT/'research/protocols.json').read_text())
        self.assertEqual(set(proto['families']),set(lab.FAMILIES))
        for family,d in proto['families'].items():
            for ref in d['sources']+proto['common_methods']:self.assertIn(ref,sources)
            self.assertIn('failure_criterion',d)
            self.assertTrue(d['empirical_gaps'])

    def test_nonfinite_values_are_explicitly_recorded(self):
        bad=[];d=lab.clean({'x':float('nan'),'y':np.float64(3)},bad)
        self.assertEqual(d,{'x':None,'y':3.})
        self.assertEqual(bad,['/x'])


if __name__=='__main__':unittest.main()
