"""Fast residual-bootstrap of the common-shape F test (warm-started refits). REPLACES the slow loop.
Writes data/universalization_common_shape_bootstrap.csv.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import f as fdist
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
rng=np.random.default_rng(20261120)
def logistic(t,K,r,t0): return K/(1.0+np.exp(-r*(t-t0)))
def gompertz(t,K,r,t0): return K*np.exp(-np.exp(-r*(t-t0)))
def fit3(t,y,warm=None,cap=130.):
    hi=float(np.max(y)); lo=[max(hi,1.0),0.005,t.min()-30]; up=[max(cap,hi*1.02),1.5,t.max()+30]
    starts=([warm] if warm is not None else
            [[min(max(hi*1.05,lo[0]+1e-6),up[0]-1e-6),r0,t0] for r0 in (0.03,0.06,0.12) for t0 in (np.median(t),np.median(t)+10)])
    best=None
    for p0 in starts:
        try: p,_=curve_fit(logistic,t,y,p0=p0,bounds=(lo,up),maxfev=8000)
        except Exception: continue
        sse=float(np.sum((y-logistic(t,*p))**2))
        if best is None or sse<best[0]: best=(sse,p)
    return best
def fit2(t,y,rg,warm=None,cap=130.):
    """restricted: r fixed at rg, estimate K,t0."""
    hi=float(np.max(y)); lo=[max(hi,1.0),t.min()-30]; up=[max(cap,hi*1.02),t.max()+30]
    def f2(tt,K,t0): return logistic(tt,K,rg,t0)
    starts=([warm] if warm is not None else [[max(hi*1.05,1),np.median(t)]])
    best=None
    for p0 in starts:
        try: p,_=curve_fit(f2,t,y,p0=p0,bounds=(lo,up),maxfev=8000)
        except Exception: continue
        sse=float(np.sum((y-f2(t,*p))**2))
        if best is None or sse<best[0]: best=(sse,p)
    return best
def run(series,reps=50):
    data=[(t,y) for t,y in series if len(t)>=12]
    if len(data)<4: return None
    fits=[]
    for t,y in data:
        b=fit3(t,y)
        if b is None: return None
        fits.append((t,y,b[0],b[1]))
    sse_free=sum(f[2] for f in fits); N=sum(len(f[0]) for f in fits)
    # restricted: grid for shared r, warm-started per country
    best=None; bestrg=None
    for rg in np.arange(0.01,0.6,0.01):
        sse=0.0; params=[]
        ok=True
        for t,y,_,p3 in fits:
            b=fit2(t,y,rg,warm=[p3[0],p3[2]])
            if b is None: ok=False; break
            sse+=b[0]; params.append(b[1])
        if ok and (best is None or sse<best): best=sse; bestrg=rg; bestpar=params
    sse_c=best; npar_free=3*len(data); npar_c=2*len(data)+1
    d1=npar_free-npar_c; d2=N-npar_free
    F0=((sse_c-sse_free)/d1)/(sse_free/d2)
    def Fb(sf,sc):
        return ((sc-sf)/d1)/(sf/d2)
    Fs=[]
    for _ in range(reps):
        sf=0.0; syn=[]
        for (t,y,sse0,p3) in fits:
            pred=logistic(t,*p3); resid=y-pred
            ys=pred+rng.choice(resid,size=len(resid),replace=True)
            b=fit3(t,ys,warm=[p3[0],p3[1],p3[2]])
            if b is None: break
            sf+=b[0]; syn.append((t,ys,p3))
        else:
            sc=0.0; ok=True
            for (t,ys,p3) in syn:
                b=fit2(t,ys,bestrg,warm=[p3[0],p3[2]])
                if b is None: ok=False; break
                sc+=b[0]
            if ok: Fs.append(Fb(sf,sc))
    Fs=np.array(Fs)
    return dict(n_countries=len(data),N=N,rmse_free=round(float(np.sqrt(sse_free/N)),3),
                rmse_common=round(float(np.sqrt(sse_c/N)),3),shared_r=round(float(bestrg),3),
                F=round(float(F0),3),df1=int(d1),df2=int(d2),
                p_asymptotic=round(float(1-fdist.cdf(F0,d1,d2)),4),
                boot_reps=len(Fs),boot_F_median=round(float(np.median(Fs)),3) if len(Fs) else np.nan,
                p_bootstrap=round(float(np.mean(Fs>=F0)),3) if len(Fs) else np.nan,
                verdict_bootstrap=('common shape NOT rejected at 0.05 (bootstrap)' if len(Fs) and np.mean(Fs>=F0)>0.05
                                   else 'common shape rejected at 0.05 (bootstrap)' if len(Fs) else 'bootstrap failed'))
g=pd.read_csv(os.path.join(BASE,'04_data','data','gmr_observed_6countries_1970_2024.csv'))
SER={'ger_secondary':'secondary GER','ger_tertiary':'tertiary GER','ger_upper_secondary':'upper-secondary GER','ner_primary':'primary NER','ner_secondary':'secondary NER'}
rows=[]
for ind,lab in SER.items():
    ser=[]
    for iso in ['PHL','KHM','CHN','HKG','KOR','JPN']:
        s=g[(g.iso3==iso)&(g.indicator==ind)][['year','value']].dropna().sort_values('year')
        s=s[(s.year>=1970)&(s.year<=2024)]
        if len(s)>=20: ser.append((s.year.values.astype(float),s.value.values.astype(float)))
    if len(ser)>=4:
        r=run(ser,reps=50)
        if r: rows.append(dict(indicator=ind,label=lab,source='GMR observed',**r))
d=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
for ind,lab in [('SE.SEC.ENRR','secondary GER'),('SE.TER.ENRR','tertiary GER')]:
    ser=[]
    for iso,s in d[['iso3','year',ind]].dropna().groupby('iso3'):
        s=s.sort_values('year')
        if len(s)>=20: ser.append((s.year.values.astype(float),s[ind].values.astype(float)))
    if len(ser)>=8:
        r=run(ser,reps=25)
        if r: rows.append(dict(indicator=ind,label=lab,source='WDI 30-country panel',**r))
out=pd.DataFrame(rows); out.to_csv(os.path.join(D,'universalization_common_shape_bootstrap.csv'),index=False)
print(out.to_string(index=False))
