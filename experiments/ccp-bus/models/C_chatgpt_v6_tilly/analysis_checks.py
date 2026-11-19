"""Independent tests of competing-event denominators and forced identity transitions."""
from dataclasses import replace
import json
from pathlib import Path
import numpy as np
from model import Params,World
from analyze import outcomes
from observation import locate_persons

def main():
    template=dict(appointed_tick=45,exposure_years=20,first_act=None,first_dependency=None,first_owed_obligation=None,
        first_true_sanction=None,first_false_sanction=None,retirement=None,employment_exit=None,exit_true_case=None,
        ever_received_illicit=False,first_act_received_illicit=None)
    records=[dict(template,first_act=54,employment_exit=58,exit_true_case=True),
             dict(template,retirement=46),dict(template,first_act=55)]
    x=outcomes(records)
    assert np.isclose(x['cohort_act_10'],1/3) and np.isclose(x['cohort_act_20'],2/3)
    assert np.isclose(x['cohort_true_exit_30'],1/3) and x['retired_before_any_act']==1
    assert np.isnan(outcomes([])['cohort_act_10'])
    # A moved creditor retains the claim; a replacement receives none of it.
    p=Params(n=10000,organizations=32,request_rate=0.,lawful_service=0.)
    for cause in ['creditor_exit','debtor_exit']:
        w=World(p,23);debtor=int(w.pools[4][0]);creditor=int(w.pools[0][1]);destination=int(w.pools[1][4])
        creditor_id=int(w.person[creditor]);w.debt[debtor]=2.;w.creditor[debtor]=creditor_id
        w.shield[debtor]=.5;w.shield_to[debtor]=creditor_id
        w.balance=dict(opening=2.,created=0.,lawful=0.,illicit=0.,writeoff=0.)
        source=np.arange(w.O);source[creditor],source[destination]=source[destination],source[creditor]
        old=w.person.copy();w.person=old[source];w.remap_tilly(source,np.zeros(w.O,bool),old,w.policy('campaign',2015))
        assert w.debt[debtor]==2. and w.creditor[debtor]==creditor_id
        assert locate_persons(w.person,np.array([creditor_id]))[0]==destination
        assert w.shield[debtor]==.5
        assert abs(w.final_tilly_accounting()['obligation_residual'])<1e-10
        source=np.arange(w.O);fresh=np.zeros(w.O,bool)
        departing=destination if cause=='creditor_exit' else debtor
        source[departing]=-1;fresh[departing]=True;old=w.person.copy();w.person[departing]=2*10**12
        w.balance=dict(opening=2.,created=0.,lawful=0.,illicit=0.,writeoff=0.)
        w.remap_tilly(source,fresh,old,w.policy('campaign',2015))
        assert w.debt.sum()==0. and w.balance['writeoff']==2.
        assert w.shield[debtor]==0.
        assert abs(w.final_tilly_accounting()['obligation_residual'])<1e-10
    result=dict(competing_event_denominator_and_horizon_boundaries=True,undefined_empty_cohort=True,
                creditor_claim_and_protection_follow_identity=True,creditor_and_debtor_exit_writeoffs=True)
    (Path(__file__).resolve().parent/'results_completed/analysis_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
