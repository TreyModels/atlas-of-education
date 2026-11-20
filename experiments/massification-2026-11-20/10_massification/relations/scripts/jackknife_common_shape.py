"""Leave-one-country-out jackknife of the common-shape F test.
Purpose (auditor PAGE caveat): the asymptotic F on a 4-6 country nonlinear fit is provisional. A full residual
bootstrap is unstable here (nonlinear restricted refits fail to converge in most replications), so the robustness
evidence reported is (a) this jackknife and (b) the E6 out-of-sample model comparison. Rejection is only asserted
if it survives dropping each country in turn.
Appends to data/universalization_common_shape_bootstrap.csv (column robustness='jackknife_LOCO').
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import f as fdist
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
def logistic(t,K,r,t0): return K/(1.0+np.exp(-r*(t-t0)))
def fit3(t,y,cap=130.):
    hi=float(np.max(y)); lo=[max(hi,1.0),0.005,t.min()-30]; up=[max(cap,hi*1.02),1.5,t.max()+30]; best=None
    for r0 in (0.02,0.05,0.1,0.2):
        for t0 in (np.median(t)-10,np.median(t),np.median(t)+10):
            try: p,_=curve_fit(logistic,t,y,p0=[min(max(hi*1.05,lo[0]+1e-6),up[0]-1e-6),r0,t0],bounds=(lo,up),maxfev=20000)
            except Exception: continue
            sse=float(np.sum((y-logistic(t,*p))**2))
            if best is None or sse<best[0]: best=(sse,p)
    return best
def restricted(t,y,cap=130.):
    hi=float(np.max(y)); best=None
    for rg in np.arange(0.01,0.6,0.01):
        def f2(tt,K,t0): return logistic(tt,K,rg,t0)
        try: p,_=curve_fit(f2,t,y,p0=[max(hi*1.05,1),np.median(t)],
                bounds=([max(hi,1.0),t.min()-30],[max(cap,hi*1.02),t.max()+30]),maxfev=20000)
        except Exception: continue
        sse=float(np.sum((y-f2(t,*p))**2))
        if best is None or sse<best[0]: best=(sse,rg)
    return best
def Ftest(fits):
    sse_free=0; N=0
    for t,y in fits:
        b=fit3(t,y)
        if b is None: return None
        sse_free+=b[0]; N+=len(t)
    sc=0; ok=True
    for t,y in fits:
        r=restricted(t,y)
        if r is None: ok=False; break
        sc+=r[0]
    if not ok: return None
    nc=len(fits); d1=3*nc-(2*nc+1); d2=N-3*nc
    F=((sc-sse_free)/d1)/(sse_free/d2)
    return F,float(1-fdist.cdf(F,d1,d2))
g=pd.read_csv(os.path.join(BASE,'04_data','data','gmr_observed_6countries_1970_2024.csv'))
SER={'ger_secondary':'secondary GER','ger_tertiary':'tertiary GER','ger_upper_secondary':'upper-secondary GER','ner_primary':'primary NER','ner_secondary':'secondary NER'}
rows=[]
for ind,lab in SER.items():
    per={}
    for iso in ['PHL','KHM','CHN','HKG','KOR','JPN']:
        s=g[(g.iso3==iso)&(g.indicator==ind)][['year','value']].dropna().sort_values('year')
        s=s[(s.year>=1970)&(s.year<=2024)]
        if len(s)>=20: per[iso]=(s.year.values.astype(float),s.value.values.astype(float))
    if len(per)<4: continue
    base=Ftest(list(per.values()))
    if base is None: continue
    loco=[]
    for drop in per:
        sub=[v for k,v in per.items() if k!=drop]
        if len(sub)>=4:
            r=Ftest(sub)
            if r: loco.append(dict(dropped=drop,F=r[0],p=r[1]))
    if not loco: continue
    Fs=[x['F'] for x in loco]; ps=[x['p'] for x in loco]
    rows.append(dict(indicator=ind,label=lab,source='GMR observed',method='jackknife_LOCO',
        n_countries=len(per),N=sum(len(v[0]) for v in per.values()),
        F_all=round(base[0],3),p_all=round(base[1],4),
        F_jack_min=round(min(Fs),3),F_jack_max=round(max(Fs),3),
        p_jack_max=round(max(ps),4),n_loco=len(loco),
        verdict=('rejection survives dropping every country in turn' if max(ps)<0.05
                 else 'rejection NOT robust - at least one leave-one-out gives p>=0.05')))
out=pd.DataFrame(rows); out.to_csv(os.path.join(D,'universalization_common_shape_jackknife.csv'),index=False)
print(out.to_string(index=False))
