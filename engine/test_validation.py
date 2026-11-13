"""Regression tests for selection leakage and measurement aggregation."""
import unittest
from types import SimpleNamespace
import numpy as np
from eduengine import measure as M, ledger as LG
from history_match import training_metrics, rank_runs, lhs


def row(year=2010, gap=.02, status='UIS', indicator='a'):
    return dict(year=year, gap=gap, tol=.1, status=status, indicator=indicator,
                model=.5+gap, value=.5, within=abs(gap)<=.1,
                split='train' if year<=2015 else 'test')


class ValidationTests(unittest.TestCase):
    def test_test_rows_cannot_select_parameters(self):
        train=[row(), row(indicator='b',gap=.08)]
        self.assertEqual(training_metrics(train+[row(2020,gap=1000)]),
                         training_metrics(train+[row(2020,gap=float('nan'))]))
    def test_unverified_rows_are_diagnostic_only(self):
        self.assertEqual(training_metrics([row()]),training_metrics([row(),row(gap=1000,status='unverified')]))
    def test_missing_training_value_is_penalized(self):
        self.assertTrue(np.isinf(training_metrics([row(gap=float('nan'))])['loss']))
        self.assertTrue(np.isinf(training_metrics([row(),row(gap=float('nan'))])['second_max']))
    def test_missing_value_stays_in_score_denominator(self):
        self.assertEqual(LG.score([row(),row(gap=float('nan'))])['train'],(1,2))
    def test_indicators_have_equal_weight(self):
        base=[row(indicator='a',gap=.05),row(indicator='b',gap=.2)]
        self.assertEqual(training_metrics(base)['loss'],training_metrics(base+[row(indicator='a',gap=.05)] )['loss'])
    def test_acceptance_precedes_loss_ranking(self):
        runs=[dict(second_max=3,train_loss=0),dict(second_max=2,train_loss=1)]
        kept,use=rank_runs(runs)
        self.assertEqual(use,[runs[1]])
        self.assertEqual(kept,[runs[1]])
    def test_pupil_weighted_rates_and_closed_grades(self):
        E=SimpleNamespace(p={'start_year':2000}, R={
            'tut_own_by_grade':[[.1,.2,0]], 'tut_firm_by_grade':[[.4,.6,0]],
            'att_by_grade':[[90,10,0]]})
        self.assertAlmostEqual(M.tutoring(E,2000,[1,2,3]),.53)
        self.assertAlmostEqual(M.tutoring(E,2000,[1,2,3],'narrow'),.42)
        self.assertTrue(np.isnan(M.tutoring(E,2000,[3])))
        self.assertTrue(np.isnan(M.tutoring(E,1999,[1])))
    def test_lhs_is_reproducible_and_stratified(self):
        from history_match import SPACE
        a=lhs(16); self.assertEqual(a,lhs(16))
        for k,(lo,hi) in SPACE.items():
            bins=sorted(int((r[k]-lo)/(hi-lo)*16) for r in a)
            self.assertEqual(bins,list(range(16)))


if __name__=='__main__': unittest.main()
