#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
def load(name):
    spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
fdr=load('fdr_check'); pairs=load('country_pairs'); world=load('competing_worlds')

class Checks(unittest.TestCase):
    def test_fdr_nonfloor_rank(self):
        # No floor p-values; the second attainable p still clears BY at rank 168.
        p=[2/401]*168+[1.0]*104
        self.assertEqual(len(fdr.step_up(p,by=True)),168)
        self.assertEqual(len(fdr.step_up([1.0]*272,by=True)),0)
    def test_fdr_invalid(self):
        with self.assertRaises(ValueError): fdr.step_up([float('nan')])
    def test_pairs_do_not_use_future(self):
        rows=[]
        for i in range(6):
            for y in [1980,1990,2010]:
                rows.append({'iso3':f'C{i}','year':y,'mean_years_schooling':1+i+(y-1980)/20,
                  'tfr_observed_1950plus':6-i/4-(y-1980)/30,'gdp_pc_maddison_1990int':500+i*100,
                  'urban_share_pct':20+i*5})
        d=pd.DataFrame(rows); a,_=pairs.match(d)
        d.loc[d.year==2010,'tfr_observed_1950plus'] *= 50
        b,_=pairs.match(d.sample(frac=1,random_state=42))
        pd.testing.assert_frame_equal(a[['country_a','country_b','baseline_distance']],b[['country_a','country_b','baseline_distance']])
        self.assertEqual(len(a),3)
        self.assertEqual(len(set(a.country_a)|set(a.country_b)),6)
    def test_synthetic_macro_and_rng(self):
        for _,_,p,mu in world.cells():
            a,b=world.rates(p,mu,0.65)
            self.assertAlmostEqual((1-p)*a+p*b,mu)
        x=world.experiment(100,0.65,np.random.default_rng(3))
        y=world.experiment(100,0.65,np.random.default_rng(3))
        self.assertEqual(x[2:],y[2:])
    def test_duplicate_country_year_rejected(self):
        row={'iso3':'AAA','year':1980,**{key:1 for key in pairs.FEATURES}}
        with self.assertRaises(ValueError): pairs.match(pd.DataFrame([row,row]))

if __name__=='__main__': unittest.main()
