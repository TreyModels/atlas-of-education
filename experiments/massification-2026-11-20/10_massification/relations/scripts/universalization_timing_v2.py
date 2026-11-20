"""Timing layer v2 (user directive: for JPN/KOR/HKG the outcome is WHEN, not the level).
Crossing years + uncertainty intervals, sustained-crossing definition, observed series only.
Where completion is absent (JPN/HKG) use observed NER, then observed in-school rate (100 - OOS), labelled.
Where nothing observed: reconstruct NER from observed enrolment headcounts / observed population denominators,
flagged 'reconstructed' and used as a BOUND only. Never impute as observation.
Writes:
  data/universalization_timing.csv          (milestone crossings, intervals, method, flags)
  data/universalization_timing_pattern.csv  (ordering + spacing; early vs late groups)
  data/e6_timing_comparison.csv             (which curve form reproduces crossing years out of sample)
  data/universalization_timing_summary.md   (human-readable table for the NEW)
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
U=pd.read_csv(os.path.join(BASE,'10_massification','data','UNIVERSALIZATION_SERIES.csv'))
U=U[U.status.isin(['observed','derived'])].copy()
G=pd.read_csv(os.path.join(BASE,'04_data','data','gmr_observed_6countries_1970_2024.csv'))
W=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
COUNTRIES=['JPN','KOR','HKG','PHL','CHN','KHM']
GROUP={c:('early (JPN/KOR/HKG)' if c in ('JPN','KOR','HKG') else 'late (PHL/CHN/KHM)') for c in COUNTRIES}

def s_of(iso,ind,frame=None):
    f=frame if frame is not None else U
    s=f[(f.iso3==iso)&(f.indicator==ind)][['year','value']].dropna().sort_values('year')
    return s[(s.year>=1960)&(s.year<=2026)]

def sustained_crossing(y,v,thr):
    """First year at/above threshold never followed by a return below, with the bracketing interval."""
    y=np.asarray(y,dtype=int); v=np.asarray(v,dtype=float)
    if len(y)==0: return dict(lo=np.nan,hi=np.nan,status='no_series')
    above=v>=thr
    if not above.any(): return dict(lo=int(y[-1]),hi=np.nan,status='not_crossed_by_last_obs')
    below=np.where(~above)[0]
    if len(below)==0: return dict(lo=np.nan,hi=int(y[0]),status='censored_above_at_first_obs')
    lb=below[-1]
    if lb==len(y)-1: return dict(lo=int(y[-1]),hi=np.nan,status='not_crossed_by_last_obs')
    return dict(lo=int(y[lb]),hi=int(y[lb+1]),status='crossed')

def in_school(iso,ind):
    s=s_of(iso,ind)
    if len(s)==0: return s
    s=s.copy(); s['value']=100.0-s['value'].astype(float)
    return s

def recon_ner_primary(iso):
    """Reconstructed primary NER: observed enrolment_primary / (observed pop x observed 0-14 share x 6/15).
    Denominator assumes uniform ages within 0-14 -> a BOUND, flagged reconstructed."""
    en=s_of(iso,'enrolment_primary',G)
    pop=W[W.iso3==iso][['year','SP.POP.TOTL','SP.POP.0014.TO.ZS']].dropna()
    if len(en)==0 or len(pop)==0: return None
    m=en.merge(pop,on='year')
    m['denom']=m['SP.POP.TOTL']*m['SP.POP.0014.TO.ZS']/100.0*6.0/15.0
    m['value']=100.0*m['value']/m['denom']
    return m[['year','value']].sort_values('year')

# (level, threshold, [(series_name, getter, kind)])
def getter(iso,ind,frame):
    return lambda: s_of(iso,ind,frame)

LEVELS=[
 ('primary_universal',95,[('completion_primary',lambda i: s_of(i,'completion_primary'),'completion'),
                            ('ner_primary',lambda i: s_of(i,'ner_primary'),'NER'),
                            ('in_school_primary',lambda i: in_school(i,'oos_primary'),'in-school (100-OOS)'),
                            ('reconstructed_ner_primary',recon_ner_primary,'reconstructed NER (BOUND)')]),
 ('lower_secondary_universal',90,[('completion_lower_secondary',lambda i: s_of(i,'completion_lower_secondary'),'completion'),
                            ('ner_lower_secondary',lambda i: s_of(i,'ner_lower_secondary'),'NER'),
                            ('in_school_lower_secondary',lambda i: in_school(i,'oos_lower_secondary'),'in-school (100-OOS)')]),
 ('upper_secondary_mass',50,[('completion_upper_secondary',lambda i: s_of(i,'completion_upper_secondary'),'completion'),
                            ('ner_upper_secondary',lambda i: s_of(i,'ner_upper_secondary'),'NER'),
                            ('in_school_upper_secondary',lambda i: in_school(i,'oos_upper_secondary'),'in-school (100-OOS)')]),
 ('upper_secondary_universal',90,[('completion_upper_secondary',lambda i: s_of(i,'completion_upper_secondary'),'completion'),
                            ('ner_upper_secondary',lambda i: s_of(i,'ner_upper_secondary'),'NER'),
                            ('in_school_upper_secondary',lambda i: in_school(i,'oos_upper_secondary'),'in-school (100-OOS)')]),
 ('tertiary_mass',50,[('ger_tertiary',lambda i: s_of(i,'ger_tertiary'),'GER (labelled)')]),
]
rows=[]
for iso in COUNTRIES:
    for level,thr,options in LEVELS:
        for sname,fn,kind in options:
            s=fn(iso)
            if s is None or len(s)<4: continue
            r=sustained_crossing(s.year.values,s.value.values,thr)
            rows.append(dict(iso3=iso,country=(s_of(iso,level if False else 'ger_primary') if False else
                    (U.loc[U.iso3==iso,'country'].iloc[0] if (U.iso3==iso).any() else iso)),
                level=level,threshold_pct=thr,measure=kind,series=sname,
                series_years=f"{int(s.year.min())}-{int(s.year.max())}",n_obs=len(s),
                crossing_lo=r['lo'],crossing_hi=r['hi'],status=r['status'],
                crossing_mid=(round((r['lo']+r['hi'])/2.0,1) if r['status']=='crossed' else np.nan),
                interval_width_years=(r['hi']-r['lo'] if r['status']=='crossed' else np.nan),
                method=('observed sustained crossing' if kind!='reconstructed NER (BOUND)' else 'RECONSTRUCTED from observed headcounts/population - BOUND only'),
                reconstructed=(kind=='reconstructed NER (BOUND)'),
                flags=(';'.join([f for f,c in [
                    ('censored_before_observed_window', r['status']=='censored_above_at_first_obs'),
                    ('not_crossed_by_last_obs', r['status']=='not_crossed_by_last_obs'),
                    ('proxy_for_completion', kind in ('NER','in-school (100-OOS)','GER (labelled)')),
                    ('reconstructed_bound', kind=='reconstructed NER (BOUND)')] if c]))))
t=pd.DataFrame(rows)
# keep the best (earliest-priority) source per country x level, but keep all rows for transparency
t['priority']=t.groupby(['iso3','level']).cumcount()
t.to_csv(os.path.join(D,'universalization_timing.csv'),index=False)
best=t[t.priority==0].copy()
print('TIMING (best available source per country x level):')
print(best[['iso3','level','threshold_pct','measure','series','crossing_lo','crossing_hi','status','flags']].to_string(index=False))

# ---------- ordering and spacing ----------
pat=[]
for iso in COUNTRIES:
    b=best[best.iso3==iso]
    crossed=b[b.status=='crossed'].copy()
    cens=b[b.status=='censored_above_at_first_obs']
    notc=b[b.status=='not_crossed_by_last_obs']
    order=' < '.join(crossed.sort_values('crossing_mid').level.tolist()) if len(crossed) else '(none measured)'
    mids=dict(zip(crossed.level,crossed.crossing_mid))
    pat.append(dict(iso3=iso,group=GROUP[iso],order_measured=order,
        n_crossed=len(crossed),n_censored=len(cens),n_not_crossed=len(notc),
        first_measured_crossing=(min(mids.values()) if mids else np.nan),
        last_measured_crossing=(max(mids.values()) if mids else np.nan),
        primary_to_lower=(round(mids['lower_secondary_universal']-mids['primary_universal'],1)
                          if 'primary_universal' in mids and 'lower_secondary_universal' in mids else np.nan),
        lower_to_upper_universal=(round(mids['upper_secondary_universal']-mids['lower_secondary_universal'],1)
                          if 'upper_secondary_universal' in mids and 'lower_secondary_universal' in mids else np.nan),
        upper_mass_to_tertiary=(round(mids['tertiary_mass']-mids['upper_secondary_mass'],1)
                          if 'tertiary_mass' in mids and 'upper_secondary_mass' in mids else np.nan),
        censored_levels=';'.join(cens.level.tolist()) or '',
        note=('universalization precedes the observed window for: '+';'.join(cens.level.tolist()) if len(cens) else '')))
p=pd.DataFrame(pat); p.to_csv(os.path.join(D,'universalization_timing_pattern.csv'),index=False)
print('\nPATTERN:'); print(p.to_string(index=False))

# ---------- E6 timing comparison ----------
def logistic(t,K,r,t0): return K/(1.0+np.exp(-r*(t-t0)))
def gompertz(t,K,r,t0): return K*np.exp(-np.exp(-r*(t-t0)))
def linear(t,a,b): return a+b*t
def exponential(t,a,b): return a*np.exp(b*(t-t.min()))
FORMS={'logistic':(logistic,3),'gompertz':(gompertz,3),'linear':(linear,2),'exponential':(exponential,2)}
def fitf(sh,t,y,k,cap=130.):
    hi=float(np.max(y))
    if k==3:
        lo=[max(hi,1.),0.005,t.min()-30]; up=[max(cap,hi*1.02),1.5,t.max()+30]
        starts=[[hi,r0,t0] for r0 in (0.02,0.05,0.1) for t0 in (np.median(t),np.median(t)+10)]
    elif sh is linear: lo=[-500,0]; up=[500,50]; starts=[[float(np.mean(y)),0.01]]
    else: lo=[0,-0.5]; up=[500,.5]; starts=[[max(float(y.min()),0.1),0.02]]
    best=None
    for p0 in starts:
        try: p,_=curve_fit(sh,t,y,p0=p0,bounds=(lo,up),maxfev=10000)
        except Exception: continue
        sse=float(np.sum((y-sh(t,*p))**2))
        if best is None or sse<best[0]: best=(sse,p)
    return best
def cross_curve(sh,p,thr,form,tmin):
    if form in ('logistic','gompertz'):
        K,r,t0=p
        if K<=thr: return np.nan
        return t0+np.log(thr/(K-thr))/r if form=='logistic' else t0-np.log(-np.log(thr/K))/r
    if form=='linear':
        a,b=p; return (thr-a)/b if abs(b)>1e-9 else np.nan
    a,b=p
    if a<=0 or b<=0: return np.nan
    return tmin+np.log(thr/a)/b
tm=[]
for iso in COUNTRIES:
    for level,thr,_ in LEVELS:
        row=best[(best.iso3==iso)&(best.level==level)].iloc[0]
        ser=s_of(iso,row.series,G if row.series=='enrolment_primary' else U)
        if len(ser)<15: continue
        tr=(ser.year>=1980)&(ser.year<=2010); te=(ser.year>=2011)&(ser.year<=2026)
        if tr.sum()<10 or te.sum()<2: continue
        for fname,(sh,k) in FORMS.items():
            b=fitf(sh,ser.year.values[tr].astype(float),ser.value.values[tr].astype(float),k)
            if b is None: continue
            pred=cross_curve(sh,b[1],thr,fname,float(ser.year.values[tr].min()))
            obs=row.crossing_mid
            err=(pred-obs) if np.isfinite(pred) and np.isfinite(obs) else np.nan
            tm.append(dict(iso3=iso,level=level,threshold_pct=thr,measure=row.measure,form=fname,
                observed_crossing_mid=obs,observed_status=row.status,
                predicted_crossing=(round(pred,1) if np.isfinite(pred) else np.nan),
                timing_error_years=(round(err,1) if np.isfinite(err) else np.nan)))
tm=pd.DataFrame(tm); tm.to_csv(os.path.join(D,'e6_timing_comparison.csv'),index=False)
ok=tm.dropna(subset=['timing_error_years'])
print('\nE6 TIMING ERROR by form:'); print(ok.groupby('form').timing_error_years.agg(['count','mean','median','max']).round(2).to_string())

# ---------- human-readable summary ----------
L=['# Universalization timing — crossing years and intervals','',
   'Crossing = first year at/above the threshold never followed by a return below it (sustained-crossing definition).',
   'Interval = [last year below, first year at/above]. Censored = already universal at the first observed year: the crossing',
   'PRECEDES the observed window and only an upper bound is reported. No imputation; reconstructed rows are bounds, flagged.','']
L.append('| country | level | threshold | measure (source) | crossing interval | status | flags |')
L.append('|---|---|---|---|---|---|---|')
for _,r in best.sort_values(['iso3','level']).iterrows():
    iv=f"{int(r.crossing_lo) if pd.notna(r.crossing_lo) else '?'}–{int(r.crossing_hi) if pd.notna(r.crossing_hi) else '?'}"
    L.append(f"| {r.iso3} | {r.level} | {r.threshold_pct:.0f}% | {r.measure} ({r.series}, {r.series_years}) | {iv} | {r.status} | {r.flags} |")
L.append('')
open(os.path.join(D,'universalization_timing_summary.md'),'w').write('\n'.join(L))
print('\nsummary written')
