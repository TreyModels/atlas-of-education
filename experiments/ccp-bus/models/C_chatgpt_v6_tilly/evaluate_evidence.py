"""Audit available empirical evidence and emit an explicit validation target register."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from evidence import Evidence
P=Path(__file__).resolve().parent
TARGETS=[
 ('appointment_clients','Client appointment probability declines during broad purge pressure','Li and Manion 2023','2013–2017 provincial appointments','Eligible candidate lists, boss-client histories, appointment dates','client_promotions / comparable candidate exposure','not_tested; candidate sampling differs from published estimand'),
 ('productive_patronage','Some patron relationships improve public performance','Jiang 2018; Jia et al. 2015','Local bureaucratic coordination and performance','Career links, organizational output, covariates','Output difference when productive coordination is switched off','synthetic_ablation_only'),
 ('report_suppression','Connected complaints lose visibility inside the hierarchy','Pan and Chen 2018','Complaints entering internal reporting channels','Complaint-level subject, routing, connectedness and outcome','Reported / generated complaints by connection status','synthetic_ablation_only'),
 ('network_regeneration','Networks can regenerate following elite turnover','2026 military-network draft in literature review','Observed officer positions and overlapping careers','Dated officer career panel, purge events, network exposure','Network survival, new entrants and regenerated ties after exits','not_tested; measure must be harmonized'),
 ('case_pipeline','Filed cases and sanctioned persons differ and can span years','CCDI annual releases','2013–2025 national discipline and supervision statistics','Population coverage by year, case/person crosswalk, filing/outcome cohorts','Stage-specific annual counts with appropriate denominator and delays','blocked_for_fit; denominators and cohort crosswalk missing'),
 ('procurement','Procurement method and repeated suppliers are observable separately from misconduct','CSET Harnessed Lightning','Selected public AI procurement notices, chiefly 2020','Deduplicated contract panel, unsuccessful bids, award dates, independent adjudications','Supplier repeat rate, value missingness, method distribution','descriptive_profile_only'),
 ('military_rivals','Network control and noisy performance monitoring may yield similar removals','Woods 2026; CSIS purge database','Observed senior military removals','Position-at-risk panel, performance proxies, censoring and dated evidence','Common outcomes: exits, output, filed cases, appointment patterns','synthetic_comparison_only'),
 ('institutional_comparison','Reporting access and selection institutions change model outcomes','Singapore comparison; Carothers 2022','Distinct countries and institutions','Comparable agency populations, offenses, measurement and enforcement coverage','Mechanism interventions under a shared observation model','not_a_fitted_Singapore_baseline')]

TARGETS=[tuple(list(row[:-1])+['previous_v5_comparison;not_reexecuted_as_isolated_v6_arm']) if row[0] in ('productive_patronage','report_suppression','military_rivals') else row for row in TARGETS]
TARGETS += [('appointment_cohort','Initially clean appointees can develop misconduct and later face a true-case removal','Project hypothesis; Tilly-inspired extension','Documented appointment-at-risk cohort','Personal-selection evidence, dated offices, conduct windows, retirement and event histories','First-act event fractions versus observed conduct and enforcement dates','synthetic_cohort_experiment;empirical_fit_blocked'),('observed_career_graph','Prior co-service may expose new appointees to established dependencies','ccporg.org methods; project hypothesis','Common person-position-year risk population','Source-backed career intervals, publication dates, rumor exclusion, complete outcome follow-up','Observed overlap graph kept distinct from latent obligation graph','source_assessed;bulk_export_not_acquired')]

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=P/'results/evidence');args=parser.parse_args()
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    obs=pd.read_csv(P/'data/verified_observations.csv');cset=pd.read_csv(P/'data/cset_procurement_fields.csv')
    pd.DataFrame(TARGETS,columns=['target','claim','literature','population','needed','model_mapping','status']).to_csv(out/'target_register.csv',index=False)
    profile=dict(official_records=len(obs),source_ids=int(pd.read_csv(P/'data/sources.csv').source_id.nunique()),
                 official_variables={str(k):int(v) for k,v in obs.variable.value_counts().items()},
                 procurement_records=len(cset),procurement_nonmissing={str(k):int(v) for k,v in cset.notna().sum().items()},
                 procurement_notice_categories={str(k):int(v) for k,v in cset.purchase_type.fillna('MISSING').value_counts().items()},
                 validation_gate='Behavioral parameters remain experimental; no empirical likelihood, posterior or national prevalence estimate has been fitted.',
                 annual_2026_in_fit=False,reason='Monitoring includes year-to-date totals and a budget; neither is a completed annual execution observation.')
    (out/'available_data_profile.json').write_text(json.dumps(profile,indent=2,ensure_ascii=False)+'\n')
    evidence=Evidence();rows=[]
    for year in range(1998,2043):
        a=evidence.flows(year)
        for sector,value in zip(['defense','land','finance','administration_A','administration_B'],a):
            observed=evidence.land if sector=='land' else evidence.fin if sector=='finance' else {}
            status='observed_annual_flow_normalized' if year in observed else 'assumed_normalized_before_observation' if observed and year<min(observed) else 'held_flat_after_last_observation' if observed else 'normalized_assumption'
            if sector=='defense' and year>=2026:status='2026_budget_to_2025_execution_comparator_then_held_flat'
            rows.append(dict(year=year,sector=sector,normalized_factor=value,status=status))
    pd.DataFrame(rows).to_csv(out/'economic_drivers.csv',index=False)
    print(json.dumps(profile,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
