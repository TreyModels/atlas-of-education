"""Event windows for state-push mechanisms (anchor PHL + HKG/CHN portability + JPN/KOR/KHM context).
Policy dates: data-hunter POLICY_TIMELINE.csv (sha in 10_massification/data/SHA256SUMS.txt) + events I add and label.
Each event gets: date(s), affected level/cohort, event-window definition (pre/post, treated cohorts, excluded transition
cohorts), the observed series used, a DESCRIPTIVE pre-trend-adjusted level shift at the event, a data-quality rank,
and an explicit statement that this is not a causal design.
Writes data/event_windows.csv.
"""
import os, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
P=pd.read_csv(os.path.join(BASE,'10_massification','data','POLICY_TIMELINE.csv'))
U=pd.read_csv(os.path.join(BASE,'10_massification','data','UNIVERSALIZATION_SERIES.csv'))
U=U[U.status.isin(['observed','derived'])]

def ser(iso,ind):
    s=U[(U.iso3==iso)&(U.indicator==ind)][['year','value']].dropna().sort_values('year')
    return s[(s.year>=1950)&(s.year<=2026)]

def its(s,event):
    for pre,post in ((10,6),(8,5),(5,4)):
        r=_its(s,event,pre,post)
        if r is not None: return r
    return None
def _its(s,event,pre=10,post=6):
    """Descriptive interrupted-time-series: linear pre-trend fitted to the pre window; post mean residual."""
    w=s[(s.year>=event-pre)&(s.year<=event+post)]
    if len(w)<8: return None
    tr=w.year.values.astype(float)-event; y=w.value.values.astype(float)
    m=tr<0
    if m.sum()<5 or (~m).sum()<2: return None
    b=np.polyfit(tr[m],y[m],1)            # pre-trend only
    pred=np.polyval(b,tr[~m]); resid=y[~m]-pred
    dof=max(m.sum()-2,1)
    s2=float(np.sum((y[m]-np.polyval(b,tr[m]))**2)/dof)
    se=float(np.sqrt(s2*(1+1/m.sum())))
    return dict(pre_slope=round(float(b[0]),3),shift=round(float(resid.mean()),2),
                se_shift=round(se,2),t_shift=round(float(resid.mean()/se),2) if se>0 else np.nan,
                n_pre=int(m.sum()),n_post=int((~m).sum()),post_mean=round(float(y[~m].mean()),2),
                pre_mean=round(float(y[m].mean()),2))

# ---------------- event registry ----------------
# quality: A = observed policy date (law/act), B = inferred effective cohort (policy date -> cohort lag), C = inferred episode
EVENTS=[
 # iso, event, signed, effective, level, affected cohorts, excluded transition cohorts, series, quality, source
 ('PHL','RA 10533 K-12 reform: 10 -> 12 years + kindergarten',2013,2016,'upper secondary',
  'Grades 11-12 from SY2016-17; first SHS graduates 2018','cohorts already past Grade 10 in 2016 (never enter G11-12); tertiary entrants 2016-2018 defer',
  'completion_upper_secondary','A','POLICY_TIMELINE.csv (workspace papers); country card PHL §5 (primary docs NOT retrieved)'),
 ('PHL','RA 10533 K-12: secondary GER composition shift',2013,2016,'secondary',
  'G11-12 counted in secondary from SY2016-17','pre-2016 secondary cohorts',
  'ger_secondary','A','POLICY_TIMELINE.csv; observed GMR ger_secondary'),
 ('PHL','RA 10931 Universal Access to Tertiary Education (free SUC tuition)',2017,2018,'tertiary',
  'all SUC entrants from AY2018-19','K-12 transition cohorts (first SHS graduates enter tertiary only 2018-19)',
  'ger_tertiary','A','country card PHL §3; 04_data params tuition_path 2017->2018 (model-internal date, law date not retrieved)'),
 ('PHL','4Ps conditional cash transfer rollout',2007,2008,'secondary',
  'Q1-Q2 secondary pupils','none','ger_secondary','B','model-internal path only (massabm cct_path 2007/2008); NO primary source retrieved'),
 ('PHL','1987 Constitution: free public primary and secondary',1987,1988,'primary','all public-school cohorts','none',
  'ger_primary','A','POLICY_TIMELINE.csv'),
 ('HKG','6-year free primary education',1971,1971,'primary','primary-age cohorts from 1971','none','ner_primary','A','POLICY_TIMELINE.csv'),
 ('HKG','9-year free compulsory education (P6 + S1-S3)',1978,1979,'lower secondary','S1-S3 cohorts from SY1979-80','cohorts already above S3',
  'ner_lower_secondary','A','POLICY_TIMELINE.csv'),
 ('HKG','12-year free education rollout (free senior secondary)',2008,2009,'upper secondary','S4-S6 cohorts from 2008/09','none',
  'ner_upper_secondary','A','POLICY_TIMELINE.csv'),
 ('HKG','3-3-4 academic structure reform (first HKDSE 2012)',2012,2012,'upper secondary',
  'first NSS cohort sits HKDSE 2012','double-cohort years 2012-13 (7-year secondary cohorts overlapping)','completion_upper_secondary','A','country card HKG §5; POLICY_TIMELINE.csv'),
 ('CHN','Compulsory Education Law (9 years)',1986,1986,'primary','cohorts entering primary from 1986','none','completion_primary','A','POLICY_TIMELINE.csv'),
 ('CHN','Higher-education expansion (enrolment quota increase)',1999,1999,'tertiary','tertiary entrants from 1999','none','ger_tertiary','A',
  'country card CHN; widely documented 1999 expansion (NOT re-verified this session)'),
 ('CHN','Free rural compulsory education (fee abolition)',2006,2006,'primary','rural cohorts from 2006','urban cohorts (2008)','completion_primary','A',
  'secondary source only (NOT re-verified this session)'),
 ('KOR','Middle-school compulsory education (phased)',1985,1985,'lower secondary','rural cohorts first, national by 2004','none','completion_lower_secondary','B','POLICY_TIMELINE.csv'),
 ('KOR','High-school equalisation',1974,1974,'secondary','national cohorts from 1974','none','ger_secondary','A','prior phase event list (not in POLICY_TIMELINE.csv)'),
 ('JPN','9-year compulsory education (Fundamental Law of Education)',1947,1947,'primary','all cohorts from 1947','none','ger_primary','A','POLICY_TIMELINE.csv'),
 ('KHM','9-year compulsory education policy',1996,1996,'lower secondary','cohorts from 1996','post-conflict cohort disruption 1975-1979','completion_lower_secondary','A','POLICY_TIMELINE.csv'),
]
rows=[]
for iso,event,signed,eff,level,coh,excl,series,q,src in EVENTS:
    r=its(ser(iso,series),eff)
    base=dict(iso3=iso,event=event,date_signed=signed,date_effective=eff,affected_level=level,
              treated_cohorts=coh,excluded_transition_cohorts=excl,series_used=series,
              pre_window=f'{eff-10}-{eff-1}',post_window=f'{eff}-{eff+6}',
              data_quality=('A = observed policy date' if q=='A' else 'B = inferred effective cohort'),
              source=src,design_status='DESCRIPTIVE event-window association; no causal design claimed')
    if r is None:
        rows.append({**base,'status':'UNABLE: insufficient observed annual series around the event','note':''})
    else:
        rows.append({**base,'status':'computed',**r,
            'note':('shift = post-window mean minus the pre-window linear trend, in pp; se ignores serial correlation -> optimistic' )})
out=pd.DataFrame(rows)
# align each event with the observed/derived crossing year of the affected level (my timing layer)
TRY=pd.read_csv(os.path.join(D,'UNIVERSALIZATION_TIMING.csv'))
LEVELMAP={'primary':'primary_universal','lower secondary':'lower_secondary_universal',
          'secondary':'upper_secondary_mass','upper secondary':'upper_secondary_mass','tertiary':'tertiary_mass'}
align=[]
for _,r in out.iterrows():
    lv=LEVELMAP.get(r.get('affected_level',''))
    hit=TRY[(TRY.iso3==r.iso3)&(TRY.level==lv)] if lv else TRY.iloc[0:0]
    if len(hit):
        h=hit.iloc[0]
        align.append(dict(event_id=f"{r.iso3}-{r.date_effective}",crossing_level=lv,
            crossing_interval=f"{h.crossing_lo if pd.notna(h.crossing_lo) else '?'}-{h.crossing_hi if pd.notna(h.crossing_hi) else '?'}",
            crossing_status=h.status, event_vs_crossing_gap=(
              round(float(h.crossing_mid)-float(r.date_effective),1) if pd.notna(h.crossing_mid) else np.nan)))
    else:
        align.append(dict(event_id=f"{r.iso3}-{r.date_effective}",crossing_level=lv or '',crossing_interval='',
            crossing_status='no timing row',event_vs_crossing_gap=np.nan))
a=pd.DataFrame(align)
out['crossing_of_affected_level']=a.crossing_interval.values
out['crossing_status']=a.crossing_status.values
out['event_vs_crossing_gap_years']=a.event_vs_crossing_gap.values
# expansion episodes (grade C: inferred from observed teacher/PTR/stock data, not a named programme)
EXP=[('PHL','Teacher-stock expansion episode (inferred: fastest observed growth in primary+secondary teachers)',None,'all levels',
      'teacher count growth > 2x trend','log_tch','SE.TER.ENRL'),
     ('KHM','Teacher-stock expansion episode (inferred)',None,'primary','teacher count growth > 2x trend','log_tch',''),
     ('CHN','Tertiary expansion episode (inferred from enrolment growth)',1999,'tertiary','enrolment growth > 2x 5y trend','log_ter','')]
# simpler: derive expansion episodes from WDI teacher series where available
W=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
def ep(iso,ind,label,level):
    s=W[(W.iso3==iso)&W[ind].notna()][['year',ind]].dropna().sort_values('year')
    if len(s)<15: return None
    s['g']=np.log(s[ind].clip(lower=1)).diff()
    thr=s.g.quantile(0.9)
    hi=s[s.g>=thr]
    if len(hi)==0: return None
    return dict(iso3=iso,event=label,date_signed=np.nan,date_effective=int(hi.year.median()),
        affected_level=level,treated_cohorts='depends on hiring date',excluded_transition_cohorts='',
        series_used=ind,pre_window='',post_window='',data_quality='C = inferred episode from observed series',
        source=f'WDI {ind} (observed), top-decile 1y growth',
        design_status='DESCRIPTIVE; episode inferred from data, not a policy document',
        status='inferred',note=f'median year of top-decile growth; years={hi.year.min()}-{hi.year.max()}')
exp=[]
for iso,ind,lab in [('PHL','SE.SEC.TCHR','Secondary teacher-stock expansion (inferred)'),
                    ('PHL','SE.PRM.TCHR','Primary teacher-stock expansion (inferred)'),
                    ('KHM','SE.PRM.TCHR','Primary teacher-stock expansion (inferred)'),
                    ('CHN','SE.TER.ENRL','Tertiary enrolment expansion (inferred)')]:
    r=ep(iso,ind,lab,'secondary' if 'SEC' in ind else 'primary' if 'PRM' in ind else 'tertiary')
    if r: exp.append(r)
if exp:
    out=pd.concat([out,pd.DataFrame(exp)],ignore_index=True,sort=False)
out.to_csv(os.path.join(D,'event_windows.csv'),index=False)
cols=[c for c in ['iso3','event','date_effective','affected_level','series_used','status','pre_slope','shift','se_shift','t_shift','data_quality','crossing_of_affected_level','event_vs_crossing_gap_years'] if c in out]
print(out[cols].to_string(index=False))
