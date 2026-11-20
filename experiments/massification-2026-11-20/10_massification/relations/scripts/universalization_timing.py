"""Timing layer for universalization (user directive: JPN/KOR/HKG are probably near-universal already; when?).
(1) Crossing-year intervals for milestones per country from OBSERVED series (censored -> interval, never a point).
(2) Milestone ordering and spacing -> is there a common timing pattern behind different levels?
(3) E6 timing comparison: which fitted curve form reproduces the observed crossing years out of sample.
Writes data/UNIVERSALIZATION_TIMING.csv, data/UNIVERSALIZATION_TIMING_PATTERN.csv, data/e6_timing_comparison.csv.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
U=pd.read_csv(os.path.join(BASE,'10_massification','data','UNIVERSALIZATION_SERIES.csv'))
U=U[U.status.isin(['observed','derived'])]  # never use check/proxy rows as milestones
def series(iso,ind):
    s=U[(U.iso3==iso)&(U.indicator==ind)][['year','value']].dropna().sort_values('year')
    return s[(s.year>=1960)&(s.year<=2026)]
# milestone definitions (declared): (name, series priority list, threshold, direction)
MILESTONES=[
 ('primary_universal',   ['completion_primary','ner_primary'], 95.0,'up'),   # GER excluded: over-100 overstates universality
 ('lower_secondary_universal', ['completion_lower_secondary','ner_lower_secondary'], 90.0,'up'),
 ('upper_secondary_mass',['completion_upper_secondary','ner_upper_secondary'], 50.0,'up'),
 ('upper_secondary_universal',['completion_upper_secondary','ner_upper_secondary'], 90.0,'up'),
 ('tertiary_mass',       ['ger_tertiary'], 50.0,'up'),
]
def crossing(s,thr,direction='up'):
    """Sustained crossing interval. A crossing is the first year above threshold that is followed by
    NO return below it in the observed series. Censored if already sustained at the first observation."""
    if len(s)==0: return (np.nan,np.nan,'no_series')
    y=s.year.values.astype(int); v=s.value.values.astype(float)
    above=(v>=thr) if direction=='up' else (v<=thr)
    if not above.any(): return (int(y[-1]),np.nan,'not_crossed_by_last_obs')
    # last index where series is below threshold
    below_idx=np.where(~above)[0]
    if len(below_idx)==0:
        return (np.nan,int(y[0]),'censored_above_at_first_obs')
    last_below=below_idx[-1]
    if last_below==len(y)-1:
        return (int(y[-1]),np.nan,'not_crossed_by_last_obs')
    lo=int(y[last_below]); hi=int(y[last_below+1])
    return (lo,hi,'crossed')
rows=[]
for iso in ['JPN','KOR','HKG','PHL','KHM','CHN']:
    cname=U.loc[U.iso3==iso,'country'].iloc[0]
    for name,priority,thr,direction in MILESTONES:
        used=None; res=(np.nan,np.nan,'no_series')
        for ind in priority:
            s=series(iso,ind)
            if len(s)>=4:
                r=crossing(s,thr,direction); used=ind; res=r
                if r[2] in ('crossed','censored_above_at_first_obs'): break
        lo,hi,status=res
        rows.append(dict(iso3=iso,country=cname,milestone=name,threshold=thr,
            series_used=used or '',series_priority=priority[0],
            crossing_lo=lo,crossing_hi=hi,status=status,
            midpoint_estimate=(round((lo+hi)/2,1) if status=='crossed' else np.nan),
            interval_width=(hi-lo if (status=='crossed') else np.nan),
            note=('already above threshold at first observation: the crossing PRECEDES the observed window' if status=='censored_above_at_first_obs'
                  else 'not universal by the last observation' if status=='not_crossed_by_last_obs' else '')))
t=pd.DataFrame(rows); t.to_csv(os.path.join(D,'UNIVERSALIZATION_TIMING.csv'),index=False)
print(t[['iso3','milestone','threshold','series_used','crossing_lo','crossing_hi','status']].to_string(index=False))

# ---------- ordering and spacing ----------
pat=[]
for iso in ['JPN','KOR','HKG','PHL','KHM','CHN']:
    sub=t[(t.iso3==iso)&(t.status=='crossed')].sort_values('crossing_hi')
    order=' < '.join(sub.milestone.tolist())
    gaps={}
    ms=sub.milestone.tolist(); mids=sub.midpoint_estimate.tolist()
    for i in range(len(ms)-1): gaps[f'{ms[i]}->{ms[i+1]}']=round(mids[i+1]-mids[i],1)
    pat.append(dict(iso3=iso,order=order,n_crossed=len(sub),
        first_crossing=round(min(mids),1) if mids else np.nan,
        last_crossing=round(max(mids),1) if mids else np.nan,
        primary_to_lower=gaps.get('primary_universal->lower_secondary_universal',np.nan),
        lower_to_upper_mass=gaps.get('lower_secondary_universal->upper_secondary_mass',np.nan),
        upper_mass_to_tertiary=gaps.get('upper_secondary_mass->tertiary_mass',np.nan),
        groups='early (JPN/KOR/HKG)' if iso in ('JPN','KOR','HKG') else 'late (PHL/KHM/CHN)'))
p=pd.DataFrame(pat); p.to_csv(os.path.join(D,'UNIVERSALIZATION_TIMING_PATTERN.csv'),index=False)
print('\nORDER/SPACING:'); print(p.to_string(index=False))

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
    elif sh is linear:
        lo=[-500,0]; up=[500,50]; starts=[[float(np.mean(y)),0.01]]
    else:
        lo=[0,-0.5]; up=[500,.5]; starts=[[max(float(y.min()),0.1),0.02]]
    best=None
    for p0 in starts:
        try: p,_=curve_fit(sh,t,y,p0=p0,bounds=(lo,up),maxfev=10000)
        except Exception: continue
        sse=float(np.sum((y-sh(t,*p))**2))
        if best is None or sse<best[0]: best=(sse,p)
    return best
def cross_from_curve(sh,p,thr,form,tmin=None):
    if form in ('logistic','gompertz'):
        K,r,t0=p
        if K<=thr: return np.nan
        if form=='logistic': return t0+np.log(thr/(K-thr))/r
        return t0-np.log(-np.log(thr/K))/r
    if form=='linear':
        a,b=p; return (thr-a)/b if abs(b)>1e-9 else np.nan
    a,b=p
    if a<=0 or b<=0: return np.nan
    return tmin+np.log(thr/a)/b
tm=[]
KEY=[('primary_universal','completion_primary',95.),('primary_universal','ner_primary',95.),
     ('lower_secondary_universal','completion_lower_secondary',90.),
     ('upper_secondary_mass','completion_upper_secondary',50.),
     ('tertiary_mass','ger_tertiary',50.)]
for iso in ['JPN','KOR','HKG','PHL','KHM','CHN']:
    for mname,ind,thr in KEY:
        s=series(iso,ind)
        if len(s)<15: continue
        tr=(s.year>=1980)&(s.year<=2010); te=(s.year>=2011)&(s.year<=2026)
        if tr.sum()<10 or te.sum()<2: continue
        obs=crossing(s,thr)  # observed crossing from the full series (sustained definition)
        for fname,(sh,k) in FORMS.items():
            b=fitf(sh,s.year.values[tr].astype(float),s.value.values[tr].astype(float),k)
            if b is None: continue
            pred=cross_from_curve(sh,b[1],thr,fname,tmin=float(s.year.values[tr].min()))
            err=(pred-obs[1]) if obs[2]=='crossed' and np.isfinite(pred) else np.nan
            tm.append(dict(iso3=iso,milestone=mname,series=ind,threshold=thr,form=fname,
                observed_cross_lo=obs[0],observed_cross_hi=obs[1],observed_status=obs[2],
                predicted_crossing=(round(pred,1) if np.isfinite(pred) else np.nan),
                timing_error_years=(round(err,1) if np.isfinite(err) else np.nan)))
tm=pd.DataFrame(tm); tm.to_csv(os.path.join(D,'e6_timing_comparison.csv'),index=False)
print('\nE6 TIMING (mean |error| in years by form, crossed milestones only):')
ok=tm.dropna(subset=['timing_error_years'])
if len(ok):
    print(ok.groupby('form').timing_error_years.agg(['count','mean','median','max']).round(2).to_string())
print('\nby milestone:')
print(ok.groupby('milestone').timing_error_years.agg(['count','mean','median']).round(2).to_string())
