"""Analyze cohort events and matched counterfactuals without an empirical fitting claim."""
from pathlib import Path
from collections import Counter
import argparse,json,math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import provenance,reusable
P=Path(__file__).resolve().parent
METRICS=['true_misconduct','mean_output','hidden_trust_share','mean_obligation','mean_closure',
         'cohort_act_10','cohort_act_20','cohort_act_30','cohort_true_exit_30','cohort_false_exit_30',
         'cohort_true_sanction_30','cohort_dependency_10','cohort_owed_10','rank_incidence_gap','rank_extraction_gap',
         'cases_per_1000','sanctions_per_1000','illicit_transferred','closed_award_share']
LABELS={'baseline':'Weak enforcement','campaign':'Sustained campaign','access_reform':'Open supplier access',
        'obligations_off':'Obligations removed','protection_off':'Exchange protection removed','emulation_off':'Emulation removed',
        'adaptation_off':'Adaptation removed','equal_resources':'Equal resource allocations','strong_oversight':'Stronger oversight',
        'low_demand':'Low demand for assistance','network_reset':'Organizational reset','payment_blind':'Payment-blind promotion',
        'tilly_off':'New mechanisms removed','no_replacement':'No outsider appointment','zero_attraction':'Zero resource-attraction coefficient'}

def outcomes(records):
    n=len(records)
    result=dict(cohort_n=n,cohort_personyears=sum(r['exposure_years'] for r in records))
    for horizon in [10,20,30]:
        for key,field in [('act','first_act'),('dependency','first_dependency'),('owed','first_owed_obligation')]:
            result[f'cohort_{key}_{horizon}']=sum(r[field] is not None and r[field]-r['appointed_tick']<horizon for r in records)/n if n else np.nan
    for key,field in [('true_sanction','first_true_sanction'),('false_sanction','first_false_sanction'),('retired','retirement')]:
        result[f'cohort_{key}_30']=sum(r[field] is not None for r in records)/n if n else np.nan
    for truth,name in [(True,'true'),(False,'false')]:
        result[f'cohort_{name}_exit_30']=sum(r['employment_exit'] is not None and r['exit_true_case']==truth for r in records)/n if n else np.nan
    result['cohort_ever_received_illicit']=sum(r['ever_received_illicit'] for r in records)/n if n else np.nan
    result['first_acts_receiving_illicit']=sum(r['first_act_received_illicit'] is True for r in records)
    result['first_act_count']=sum(r['first_act'] is not None for r in records)
    result['retired_before_any_act']=sum(r['retirement'] is not None and (r['first_act'] is None or r['retirement']<r['first_act']) for r in records)
    return result

def load(out):
    m=json.loads((out/'manifest.json').read_text())
    if m['provenance']!=provenance():raise ValueError('Behavior/data differ from executed manifest')
    annual=[];end=[];people=[]
    for j in m['jobs']:
        path=out/'runs'/(j['id']+'.json')
        if not reusable(path,j,m['design_hash']):raise ValueError('Incomplete or stale job '+j['id'])
        r=json.loads(path.read_text());meta=dict(job_id=j['id'],family=j['family'],point=j['point'],scenario=j['scenario'],seed=j['seed'],n=j['params']['n'])
        a=pd.DataFrame(r['rows'])
        a['cases_per_1000']=1000*a.cases_filed/a.officials;a['sanctions_per_1000']=1000*a.sanctions/a.officials
        a['cohort_annual_incidence']=a.cohort_first_acts/a.cohort_first_act_risk.replace(0,np.nan)
        a['cohort_cumulative_act']=a.cohort_ever_act/a.cohort_size.replace(0,np.nan)
        a['cohort_cumulative_true_exit']=a.cohort_removed_true/a.cohort_size.replace(0,np.nan)
        for key,value in meta.items():a[key]=value
        annual.append(a)
        row=dict(meta,**a[a.year>=2038].select_dtypes('number').mean().to_dict(),**outcomes(r['cohort_records']))
        row.update(meta);row['rank_incidence_gap']=row['rank0_misconduct']-row['rank4_misconduct']
        row['rank_extraction_gap']=row['rank0_extraction_per_official']-row['rank4_extraction_per_official']
        end.append(row)
        for person in r['cohort_records']:people.append(dict(**meta,**person))
    return m,pd.concat(annual,ignore_index=True),pd.DataFrame(end),pd.DataFrame(people)

def effects(e):
    points=[];l=e[e.family=='lhs']
    for comp in ['baseline','campaign']:
        b=l[l.scenario==comp].set_index(['point','seed'])
        for sc,g in l.groupby('scenario'):
            if sc==comp:continue
            diff=g.set_index(['point','seed'])[METRICS]-b[METRICS]
            for point,v in diff.groupby(level='point'):
                for metric in METRICS:
                    x=v[metric].dropna()
                    if not len(x):continue
                    points.append(dict(comparator=comp,scenario=sc,point=point,metric=metric,mean_effect=x.mean(),seed_mcse=x.std(ddof=1)/math.sqrt(len(x)),seeds=len(x)))
    p=pd.DataFrame(points);s=[]
    for (comp,sc,metric),g in p.groupby(['comparator','scenario','metric']):
        x=g.mean_effect;s.append(dict(comparator=comp,scenario=sc,metric=metric,parameter_points=len(x),median=x.median(),q05=x.quantile(.05),q95=x.quantile(.95),positive=int((x>0).sum()),negative=int((x<0).sum()),median_seed_mcse=g.seed_mcse.median()))
    return p,pd.DataFrame(s)

def morris(m,e):
    ends=e.set_index('job_id');jobs={(j['trajectory'],j['step'],j['seed']):j for j in m['jobs'] if j['family']=='morris'};rows=[]
    for (tr,step,seed),j in jobs.items():
        if not step:continue
        prev=jobs[(tr,step-1,seed)]
        for metric in ['true_misconduct','cohort_act_10','cohort_true_exit_30','mean_output']:
            effect=(ends.loc[j['id'],metric]-ends.loc[prev['id'],metric])/j['dx']
            rows.append(dict(trajectory=tr,step=step,seed=seed,factor=j['changed'],metric=metric,effect=effect))
    r=pd.DataFrame(rows);averaged=r.groupby(['trajectory','factor','metric'],as_index=False).effect.mean();summary=[]
    for (factor,metric),g in averaged.groupby(['factor','metric']):
        x=g.effect;summary.append(dict(factor=factor,metric=metric,paths=len(x),mu=x.mean(),mu_star=x.abs().mean(),sigma=x.std(ddof=1)))
    return r,pd.DataFrame(summary)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=P/'results_completed');args=ap.parse_args();out=args.output.resolve()
    m,d,e,people=load(out);e.to_csv(out/'endpoints.csv',index=False);people.to_csv(out/'cohort_event_histories.csv',index=False)
    points,summary=effects(e);points.to_csv(out/'paired_effects_by_point.csv',index=False);summary.to_csv(out/'paired_effects_summary.csv',index=False)
    raw,screen=morris(m,e);raw.to_csv(out/'morris_elementary_effects.csv',index=False);screen.to_csv(out/'morris_screening.csv',index=False)
    ref=e[e.family=='reference'];means=ref.groupby('scenario')[METRICS].mean();means.to_csv(out/'reference_regimes.csv')
    ref.groupby('scenario')[METRICS].sem().to_csv(out/'reference_seed_mcse.csv')
    e[e.family=='integrity'].groupby(['point','scenario'])[METRICS].mean().to_csv(out/'integrity_anchors.csv')
    # Keep rank participation and amounts per resource separate across three time windows.
    rankrows=[]
    for window,start,end in [('before',2008,2012),('early',2013,2022),('late',2038,2042)]:
        part=d[(d.year>=start)&(d.year<=end)]
        for rank in range(5):
            cols=[f'rank{rank}_misconduct',f'rank{rank}_extraction_per_official',f'rank{rank}_extraction_per_resource',f'rank{rank}_requests_per_official']
            r=part.groupby(['family','point','scenario','seed'])[cols].mean().reset_index();r['window']=window;r['rank']=rank
            r=r.rename(columns={cols[0]:'misconduct',cols[1]:'extraction_per_official',cols[2]:'extraction_per_resource',cols[3]:'requests_per_official'});rankrows.append(r)
    pd.concat(rankrows).to_csv(out/'rank_gradients.csv',index=False)
    # Structural checks, explicitly paired to matching 50k parameter points and seeds.
    robust=[];lhs=e[e.family=='lhs'].set_index(['point','scenario','seed'])
    for _,r in e[e.family=='scale'].iterrows():
        original=r.point.split(':')[1]
        for metric in ['true_misconduct','cohort_act_10','cohort_true_exit_30']:
            robust.append(dict(check='scale',point=r.point,scenario=r.scenario,seed=r.seed,metric=metric,difference=r[metric]-lhs.loc[(original,r.scenario,r.seed),metric]))
    init=e[e.family=='initialization'].copy();init[['burn','initial']]=init.point.str.split(':',expand=True)
    low=init[init.initial=='0.05'].set_index(['burn','seed'])
    for _,r in init[init.initial=='0.75'].iterrows():
        for metric in ['true_misconduct','cohort_act_10','cohort_true_exit_30']:robust.append(dict(check='initialization',point=r.burn,scenario=r.scenario,seed=r.seed,metric=metric,difference=r[metric]-low.loc[(r.burn,r.seed),metric]))
    pd.DataFrame(robust).to_csv(out/'robustness_differences.csv',index=False)
    # Audit counts from the reference campaign; original cohort denominator remains fixed.
    campaign_people=people[(people.family=='reference')&(people.scenario=='campaign')]
    audit=dict(reference_people=len(campaign_people),personyears=int(campaign_people.exposure_years.sum()),
        ever_misconduct=int(campaign_people.first_act.notna().sum()),true_case_employment_exits=int(((campaign_people.exit_true_case==True)&campaign_people.employment_exit.notna()).sum()),
        false_case_employment_exits=int(((campaign_people.exit_true_case==False)&campaign_people.employment_exit.notna()).sum()),
        ever_received_illicit=int(campaign_people.ever_received_illicit.sum()),
        first_act_after_owed=int((campaign_people.first_act.notna()&campaign_people.first_owed_obligation.notna()&(campaign_people.first_owed_obligation<=campaign_people.first_act)).sum()),
        first_acts_with_received_illicit=int(campaign_people.first_act_received_illicit.fillna(False).sum()))
    (out/'cohort_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    # Ribbons show variation among parameter points after seed averaging.
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    selected=['baseline','campaign','access_reform','obligations_off','strong_oversight','equal_resources']
    colors=dict(zip(selected,['#777777','#2377a8','#298957','#b77739','#b24158','#925cbe']))
    avg=d[d.family=='lhs'].groupby(['scenario','point','year']).mean(numeric_only=True).reset_index()
    fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for ax,metric,label in zip(axs.flat,['true_misconduct','cohort_cumulative_act','cohort_cumulative_true_exit','mean_output'],['Current misconduct, all officials','Original appointees with any misconduct','Original appointees removed on a true case','Public output index']):
        for sc in selected:
            data=avg[(avg.scenario==sc)&((avg.year>=2013) if metric.startswith('cohort') else True)]
            group=data.groupby('year')[metric];mid=group.median();lo=group.quantile(.1);hi=group.quantile(.9)
            ax.plot(mid.index,mid.values,label=LABELS[sc],color=colors[sc]);ax.fill_between(lo.index,lo.values,hi.values,color=colors[sc],alpha=.08)
        ax.set_ylabel(label);ax.set_xlabel('Scenario year');ax.axvline(2013,color='black',ls=':',lw=.7)
    axs[0,0].legend(fontsize=8);fig.suptitle('V6 synthetic experiments, uncalibrated\nLines: medians across parameter settings; bands: 10th–90th percentile after seed averaging',fontsize=12)
    fig.savefig(out/'overview.png',dpi=170);plt.close(fig)
    primary=screen[screen.metric=='cohort_act_10'].sort_values('mu_star',ascending=False)
    fig,ax=plt.subplots(figsize=(8,5),layout='constrained');ax.barh(primary.factor[::-1],primary.mu_star[::-1],color='#2377a8')
    ax.set_xlabel('Mean absolute elementary effect per normalized parameter range');ax.set_title('Morris screening: first misconduct within 10 years')
    fig.savefig(out/'sensitivity.png',dpi=170);plt.close(fig)
    npoints=e[e.family=='lhs'].point.nunique();nseeds=e[e.family=='lhs'].seed.nunique();nref=ref.seed.nunique()
    text=['# V6 Tilly extension: executed results','',f"Completed **{len(m['jobs'])} runs**, with {len(d):,} annual rows. Behavioral code and input hashes match the executed manifest.",'',
          'All people and event histories are synthetic. The appointment cohort consists of initially clean, high-integrity outsiders placed in organizational head positions in the 2013 experimental intervention. These are not identified historical Xi appointees. Behavioral parameters remain unestimated.','',
          '## Reference comparison','',f'{nref} seeds; 64 original appointees per run. Misconduct percentages refer to the final five-year mean across all officials. Cohort outcomes retain the original 64-person denominator, including people who retire while clean.','',
          '| Regime | Current misconduct | Cohort misconduct by year 10 | Cohort misconduct by year 30 | Cohort true-case removal by year 30 |',
          '|---|---:|---:|---:|---:|']
    for sc,r in means.iterrows():
        cells=[f'{r[k]:.1%}' if pd.notna(r[k]) else 'N/A' for k in ['true_misconduct','cohort_act_10','cohort_act_30','cohort_true_exit_30']]
        text.append('| '+LABELS[sc]+' | '+' | '.join(cells)+' |')
    text+=['','A true-case removal means the person was removed following a case tied to a modeled misconduct act. A false-case removal can affect someone with other misconduct in their history. Neither label supplies a complete moral classification of the person. Delayed sanctions after retirement remain in the event histories.','',
           '## Paired sensitivity across assumptions','',f'{npoints} Latin-hypercube parameter settings, {nseeds} matched seeds each. Quantiles describe parameter sensitivity; seed MCSE describes simulation noise conditional on a setting. Neither is an uncertainty interval for the actual CCP.','',
           '| Comparison with sustained campaign | Outcome | Median effect | 5th–95th percentile | Points above / below zero | Median seed MCSE |',
           '|---|---|---:|---:|---:|---:|']
    for sc,metric in [('access_reform','cohort_act_10'),('obligations_off','cohort_act_10'),('equal_resources','cohort_act_10'),('zero_attraction','cohort_act_10'),('strong_oversight','cohort_act_10'),('network_reset','cohort_act_10'),('emulation_off','true_misconduct'),('no_replacement','true_misconduct')]:
        r=summary[(summary.comparator=='campaign')&(summary.scenario==sc)&(summary.metric==metric)].iloc[0]
        if sc=='emulation_off':text.append(f'| {LABELS[sc]} | {metric} | {r["median"]:+.2e} | {r.q05:+.2e} to {r.q95:+.2e} | Numerically negligible | {r.median_seed_mcse:.2e} |')
        else:text.append(f'| {LABELS[sc]} | {metric} | {r["median"]:+.4f} | {r.q05:+.4f} to {r.q95:+.4f} | {r.positive} / {r.negative} | {r.median_seed_mcse:.4f} |')
    text+=['','Settings with exactly zero differences are omitted from the above/below counts. The emulation effects are numerically negligible at the substantive scale shown; signs on such small differences provide no useful directional evidence. At reference parameters, adaptation, exchange protection and the additional payment-based promotion term also have little effect at the reported precision. These comparisons do not establish those channels as necessary for the observed synthetic pattern.']
    text+=['','## Cohort accounting','',
           f"Across the reference campaign runs, {audit['ever_misconduct']} of {audit['reference_people']} original appointees had at least one misconduct act; {audit['true_case_employment_exits']} were removed on true cases and {audit['false_case_employment_exits']} on false cases. Total exposure was {audit['personyears']} person-years. At their first misconduct act, {audit['first_acts_with_received_illicit']} appointees received illicit payments from other officials in the same step. That count excludes their own direct contract diversion and unpaid obligations.",'',
           f"For {audit['first_act_after_owed']} appointees, the first recorded obligation owed preceded or occurred in the same step as their first misconduct. Assistance and obligation creation occur before misconduct within a step. This timing describes the simulated sequence and does not identify a causal effect by itself.",'',
           'The closed cohort is observed through the fixed horizon or a competing employment exit/retirement. The reported cumulative event fraction retains clean retirees in its denominator. Annual first-act incidence uses only still-employed, never-acted people at the step opening. Empty risk sets are undefined.','',
           '## What drives the result','',
           'Largest Morris screening effects on ten-year cohort misconduct: '+', '.join(primary.head(5).factor)+'. Four paths and two seeds per point provide an exploratory screen. Discrete cohort outcomes have appreciable Monte Carlo noise; larger replication is needed before ranking small effects.','',
           'The resource gradient, obligation pressure and response to assistance requests enter the decision rule explicitly. Their effects are conditional consequences of these assumptions. Negative and zero request-pressure coefficients, negative resource-attraction coefficients, equal-resource allocation and a zero-attraction arm permit contrary patterns. Rank extraction amounts and extraction per unit of resource are saved separately.','',
           'Organizational imitation uses public output and filed cases per official. Legitimate assistance can discharge obligations without misconduct. Organizational closure changes supplier access and can exist without a corrupt award. The campaign and no-replacement arms differ only in the exogenous appointment shock; cohort metrics are undefined in the no-replacement arm.','',
           'The model retains a positive baseline probability of misconduct and a positive baseline closure target. Long-horizon onset and rebuilt closure therefore follow partly from imposed propensities. The informative tests are paired changes in outcomes, including the new-mechanisms-off control. Onset alone cannot establish that obligations caused it.','',
           '## Empirical limits and artifacts','',
           'The package retains the official annual panel, 2026 monitoring/budget records and selected CSET notices. Existing normalized macro drivers affect resource allocation. Neither the Tilly mechanisms nor the synthetic appointee event rates have been fitted to observed Chinese officials. Historical evaluation requires a dated appointment-at-risk cohort and conduct-specific evidence, alongside institutional coverage and censoring rules.','',
           '- `cohort_event_histories.csv`: immutable identities, first events and competing exits.','- `paired_effects_by_point.csv`: assumption-specific effects and seed MCSE.','- `rank_gradients.csv`: participation, extraction per official, extraction per resource and assistance exposure.','- `morris_elementary_effects.csv`: raw screening calculations.','- `robustness_differences.csv`: population-scale and initialization checks.','- `runs/`: complete annual series, cohort records, parameters and seeds.','- `../PEER_REVIEW.md`: review by the requested gpt-6.1-terra agent.','']
    text+=['- `../CCPORG_ASSESSMENT.md`: audit of the career/event source supplied during execution.','']
    (out/'RESULTS.md').write_text('\n'.join(text))
    if out in (P/'results',P/'results_completed'):(P/'RESULTS.md').write_text('\n'.join(text))
    print(json.dumps(dict(runs=len(m['jobs']),families=dict(Counter(j['family'] for j in m['jobs'])),cohort_audit=audit,reference_campaign=means.loc['campaign'].to_dict()),indent=2))
if __name__=='__main__':main()
