"""Implementation checks for the Tilly extension and immutable appointment cohort."""
from pathlib import Path
from dataclasses import replace
import json
import numpy as np
from model import Params,World,SCENARIOS,simulate
from observation import Cases,locate_persons
P=Path(__file__).resolve().parent

def main():
    p=Params(n=10000,organizations=32);checks={}
    a=simulate(p,1,'campaign',end=2016,burn=2);b=simulate(p,1,'access_reform',end=2016,burn=2)
    assert a[:15]==b[:15] and a[15:]!=b[15:]
    assert a==simulate(p,1,'campaign',end=2016,burn=2)
    checks['reproduction_and_identical_preshock_history']=True
    w=World(p,11)
    for year in range(1998,2043):
        old_integrity=w.integrity.copy();old_comp=w.competence.copy()
        r=w.step('campaign',year);event=w.last_event;survive=~event['fresh'];source=event['source'][survive]
        if year!=2013:
            assert np.allclose(w.integrity[survive],old_integrity[source])
            assert np.allclose(w.competence[survive],old_comp[source])
        assert len(np.unique(w.person))==w.O
        assert np.array_equal(w.person[survive],event['old_person'][source])
        assert abs(r['obligation_residual'])<1e-7 and np.all(w.debt>=-1e-12)
        assert np.isclose(r['resource_allocated'],r['resource_diverted']+r['resource_delivered'])
        assert np.isclose(r['net_private_receipts'],r['resource_diverted'])
        assert r['illicit_transferred']<=r['resource_diverted']+1e-9
        owing=w.debt>1e-12;assert not np.any(w.creditor[owing]==w.person[owing]);assert np.all(np.isin(w.creditor[owing],w.person))
        assert r['investigations']<=r['capacity']
        assert r['cohort_first_acts']<=r['cohort_first_act_risk']<=r['cohort_at_risk']
        t=w.last_tilly;paid=t['paid']>0;credit=t['creditor_slots'][paid]
        assert np.all(t['act'][paid]) and np.all(t['act'][credit])
        assert np.all(t['paid']<=t['before']+1e-10)
    checks['identity_and_attributes_survive_movement']=True
    checks['obligation_creation_discharge_exit_accounting']=True
    checks['full_public_budget_and_private_transfer_conservation']=True
    checks['illicit_settlement_requires_two_acts_and_existing_obligation']=True
    checks['creditor_identity_survives_or_debt_is_written_off']=True
    checks['cohort_incidence_risk_sets_and_investigation_capacity']=True
    cohort=set(w.cohort);assert len(cohort)==p.organizations
    assert all(r['modeled_prior_misconduct'] is False for r in w.cohort.values())
    assert all(r['first_act'] is None or r['first_act']>=r['appointed_tick'] for r in w.cohort.values())
    assert any(r['first_owed_obligation'] is not None for r in w.cohort.values())
    assert any(r['retirement'] is not None for r in w.cohort.values())
    # Force departure of all remaining cohort members, then verify successors remain non-cohort.
    ids=np.array(list(cohort),np.int64);slots=locate_persons(w.person,ids);slots=slots[slots>=0]
    pol=w.policy('campaign',2043);draw=w._draws();w.prepare_tilly(pol,draw,np.ones(5));depart=np.zeros(w.O,bool);depart[slots]=True
    w._careers(depart,pol,draw)
    assert not np.any(np.isin(w.person,ids));assert set(w.cohort)==cohort
    checks['cohort_ids_clocks_and_honest_baseline_not_inherited_by_successors']=True
    for scenario in SCENARIOS:
        q=World(p,2)
        for year in [2012,2013,2014]:r=q.step(scenario,year)
        if scenario=='obligations_off':assert np.all(q.debt==0) and r['illicit_transferred']==0
        if scenario=='protection_off':assert np.all(q.shield==0)
        if scenario=='access_reform':assert np.all(q.closure==0) and r['closed_award_share']==0
        if scenario=='equal_resources':assert np.allclose(q.relative_control,1)
        if scenario=='no_replacement':assert not q.cohort and r['cohort_dependency_share'] is None
    checks['all_regimes_and_isolated_mechanism_switches']=True
    control=World(p,4);campaign=control.policy('campaign',2015)
    assert campaign==control.policy('no_replacement',2015)
    zero=control.policy('zero_attraction',2015);assert zero.pop('attraction')==0.
    remaining=campaign.copy();remaining.pop('attraction');assert zero==remaining
    checks['replacement_and_attraction_controls_change_only_intended_switch']=True
    clean=World(replace(p,rent=-30.,initial_corruption=0.,request_rate=0.,obligation_pressure=0.,resource_attraction=0.,request_pressure=0.),3)
    for year in range(2013,2023):assert clean.step('campaign',year)['true_misconduct']==0
    assert all(r['first_act'] is None for r in clean.cohort.values())
    checks['clean_cohort_and_no_corrupt_transfer_possible_at_low_rent_limit']=True
    # Hold reports and performance targeting off; hidden shield must not change targets.
    v1=World(replace(p,performance_weight=0.),77);v2=World(replace(p,performance_weight=0.),77)
    v2.shield[:]=.9
    for v in (v1,v2):
        original=v._draws
        def controlled(original=original):
            draw=original();draw['complaint'][:]=1.;return draw
        v._draws=controlled
        v.step('campaign',2014)
    assert np.array_equal(v1.last_investigated,v2.last_investigated)
    checks['targeting_score_excludes_hidden_exchange_shield']=True
    q=Cases();q.add(np.array([11]),0,np.array([True]),np.array([1.]),np.array([0.]))
    assert q.resolve(1,1,2,0,1)['sanctions']==0
    total=0
    for tick in range(2,20):total+=len(q.resolve(tick,1,2,0,1)['true_exit_ids'])
    assert total==1 and locate_persons(np.array([12]),np.array([11]))[0]==-1
    checks['case_delay_truth_and_departed_person_mapping']=True
    from run import execute,design,reusable
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as tmp:
        job=design(10000,2,2,1)[1]
        execute(job,'export-test',tmp)
        path=Path(tmp)/(job['id']+'.json');export=json.loads(path.read_text())
        assert reusable(path,job,'export-test') and not reusable(path,job,'stale')
        assert len(export['cohort_records'])==64 and len(export['rows'])==45
        assert any(r['retirement'] is not None for r in export['cohort_records'])
    checks['complete_cohort_run_serializes_and_resume_rejects_stale_hash']=True
    (P/'results/checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
