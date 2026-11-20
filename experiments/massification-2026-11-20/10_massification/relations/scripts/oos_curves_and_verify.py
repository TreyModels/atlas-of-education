"""Supplement: (a) universalization curves for the IN-SCHOOL rate (100 - out-of-school rate) from data-hunter's
UNIVERSALIZATION_SERIES.csv; (b) verification that re-fitting the six-country GER series from that file reproduces
my GMR-observed fits (same underlying observations). Writes data/universalization_fits_supplement.csv and
data/universalization_refit_verification.csv.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
def logistic(t,K,r,t0): return K/(1.0+np.exp(-r*(t-t0)))
def fit(t,y,cap):
    hi=float(np.max(y)); lo=[max(hi,1.0),0.005,t.min()-30]; up=[max(cap,hi*1.02),1.5,t.max()+30]; best=None
    for K0 in [hi,hi+0.15*(up[0]-hi),hi+0.45*(up[0]-hi)]:
        for r0 in (0.02,0.05,0.1,0.2):
            for t0 in (np.median(t)-10,np.median(t),np.median(t)+10):
                try: p,cov=curve_fit(logistic,t,y,p0=[min(max(K0,lo[0]+1e-6),up[0]-1e-6),r0,t0],bounds=(lo,up),maxfev=20000)
                except Exception: continue
                sse=float(np.sum((y-logistic(t,*p))**2))
                if best is None or sse<best[0]: best=(sse,p,cov)
    if best is None: return None
    sse,p,cov=best; se=np.sqrt(np.diag(cov)); n=len(t)
    return dict(K=p[0],K_se=se[0],r=p[1],r_se=se[1],t0=p[2],t0_se=se[2],
                rmse=float(np.sqrt(sse/n)),r2=1-sse/max(float(np.sum((y-y.mean())**2)),1e-12),n=n)
u=pd.read_csv(os.path.join(BASE,'10_massification','data','UNIVERSALIZATION_SERIES.csv'))
oos=[('oos_primary','primary'),('oos_lower_secondary','lower secondary'),('oos_upper_secondary','upper secondary')]
rows=[]
for iso in ['PHL','KHM','CHN','HKG','KOR','JPN']:
    for ind,lev in oos:
        s=u[(u.iso3==iso)&(u.indicator==ind)][['year','value']].dropna().sort_values('year')
        s=s[(s.year>=1970)&(s.year<=2024)]
        if len(s)<15: continue
        t=s.year.values.astype(float); y=(100.0-s.value.values.astype(float))  # in-school rate
        f=fit(t,y,130.)
        if f is None: continue
        rows.append(dict(iso3=iso,indicator=ind,label='in-school rate (100 - OOS)',level=lev,
            source='data-hunter UNIVERSALIZATION_SERIES.csv (sha 85bc8693)',
            years=f"{int(t.min())}-{int(t.max())}",n_obs=f['n'],model='logistic',
            K=round(f['K'],2),K_se=round(f['K_se'],2),r=round(f['r'],4),r_se=round(f['r_se'],4),
            t0=round(f['t0'],1),t0_se=round(f['t0_se'],1),rmse=round(f['rmse'],3),r2=round(f['r2'],4),
            better_shape='')) 
pd.DataFrame(rows).to_csv(os.path.join(D,'universalization_fits_supplement.csv'),index=False)
print('OOS in-school fits:',len(rows))
print(pd.DataFrame(rows)[['iso3','indicator','K','r','t0','r2','n_obs']].to_string(index=False))

# verification: refit GER secondary from data-hunter file vs my published fit
g=pd.read_csv(os.path.join(BASE,'04_data','data','gmr_observed_6countries_1970_2024.csv'))
mine=pd.read_csv(os.path.join(D,'universalization_fits.csv'))
mine=mine[(mine.fit_sample=='full')&(mine.model=='logistic')&(mine.indicator=='ger_secondary')]
ver=[]
for iso in ['PHL','KHM','CHN','HKG','KOR','JPN']:
    s=u[(u.iso3==iso)&(u.indicator=='ger_secondary')][['year','value']].dropna().sort_values('year')
    s=s[(s.year>=1970)&(s.year<=2024)]
    if len(s)<12: continue
    f=fit(s.year.values.astype(float),s.value.values.astype(float),130.)
    if f is None: continue
    m=mine[mine.iso3==iso]
    ver.append(dict(iso3=iso,K_datahunter=round(f['K'],2),K_mine=float(m.K.iloc[0]) if len(m) else np.nan,
                    r_datahunter=round(f['r'],4),r_mine=float(m.r.iloc[0]) if len(m) else np.nan,
                    t0_datahunter=round(f['t0'],1),t0_mine=float(m.t0.iloc[0]) if len(m) else np.nan,
                    n_datahunter=f['n'],n_mine=int(m.n_obs.iloc[0]) if len(m) else np.nan,
                    identical=(len(m)>0 and abs(f['K']-float(m.K.iloc[0]))<0.05 and abs(f['t0']-float(m.t0.iloc[0]))<0.2)))
v=pd.DataFrame(ver); v.to_csv(os.path.join(D,'universalization_refit_verification.csv'),index=False)
print('\nVERIFICATION (data-hunter source vs my GMR-based fit):'); print(v.to_string(index=False))
