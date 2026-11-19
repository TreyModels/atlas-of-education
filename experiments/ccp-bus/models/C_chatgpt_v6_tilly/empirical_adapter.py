"""Conservative observed-edge adapter for a future source-backed career export.

No scraper, guessed faction labels or missing-as-clean coding. Input is a CSV
conforming to the documented schema. All rejected observations retain reasons.
"""
from pathlib import Path
import argparse
import pandas as pd
REQUIRED=['person_a','person_b','relation_type','service_start','service_end','source_published','source_url','end_imputed','verified']

def boolean(s):return s.astype(str).str.strip().str.lower().isin(['true','1','yes'])
def select_edges(frame,as_of):
    missing=set(REQUIRED)-set(frame.columns)
    if missing:raise ValueError('Missing required columns: '+', '.join(sorted(missing)))
    d=frame.copy();cutoff=pd.Timestamp(as_of);reasons=[[] for _ in range(len(d))]
    def reject(mask,label):
        for i,flag in enumerate(mask):
            if flag:reasons[i].append(label)
    start=pd.to_datetime(d.service_start,errors='coerce');end=pd.to_datetime(d.service_end,errors='coerce')
    published=pd.to_datetime(d.source_published,errors='coerce')
    reject(d.person_a.isna()|d.person_b.isna(),'missing_person_identity')
    reject(d.person_a.eq(d.person_b),'self_link')
    reject(d.relation_type.ne('co_service'),'basis_not_verified_coservice')
    reject(~boolean(d.verified),'verification_absent')
    explicit_end=d.end_imputed.astype(str).str.strip().str.lower().isin(['false','0','no'])
    reject(~explicit_end,'imputed_or_unspecified_service_end')
    reject(d.source_url.isna()|d.source_url.astype(str).str.strip().eq(''),'missing_source')
    reject(start.isna()|end.isna()|published.isna(),'missing_usable_date')
    reject((end<start),'invalid_service_interval')
    reject((published>cutoff),'source_unavailable_at_cutoff')
    reject((start>cutoff),'service_begins_after_cutoff')
    # Ongoing known intervals are clipped at the cutoff; future overlap cannot be counted.
    stop=end.clip(upper=cutoff);months=(stop-start).dt.days/30.4375
    reject(stop<start+pd.DateOffset(months=3),'less_than_three_observed_months')
    d['observed_overlap_months']=months;d['analysis_cutoff']=str(cutoff.date())
    d['rejection_reasons']=[';'.join(x) for x in reasons];d['primary_eligible']=d.rejection_reasons.eq('')
    return d

def check():
    base=dict(person_a='a',person_b='b',relation_type='co_service',service_start='2018-01-01',service_end='2020-01-01',source_published='2020-02-01',source_url='https://example.org/official',end_imputed=False,verified=True)
    rows=[base,dict(base,relation_type='rumor'),dict(base,source_published='2026-01-01'),dict(base,end_imputed=True),dict(base,verified=False),dict(base,end_imputed=None),dict(base,service_end='2018-04-01'),dict(base,service_end='2018-03-31')]
    result=select_edges(pd.DataFrame(rows),'2021-01-01')
    assert result.primary_eligible.tolist()==[True,False,False,False,False,False,True,False]
    assert 'source_unavailable_at_cutoff' in result.iloc[2].rejection_reasons
    print('Evidence adapter: verified link retained; rumor, future source, imputed end and unverified link rejected.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path);p.add_argument('--as-of');p.add_argument('--output',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.check:check();return
    if not(a.input and a.as_of and a.output):p.error('--input, --as-of and --output are required')
    d=select_edges(pd.read_csv(a.input,dtype={'person_a':'string','person_b':'string'}),a.as_of);a.output.parent.mkdir(parents=True,exist_ok=True);d.to_csv(a.output,index=False)
    print(dict(records=len(d),primary_eligible=int(d.primary_eligible.sum()),rejected=int((~d.primary_eligible).sum())))
if __name__=='__main__':main()
