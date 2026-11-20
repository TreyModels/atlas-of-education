"""E6 scaling-form test (constraint check only) + bootstrap of the common-shape test.
(a) Model comparison on declared holdout: logistic vs Gompertz vs linear vs exponential, fit 1980-2010, test 2011-2024.
(b) Bootstrap (residual, within-country, 100 reps) of the common-shape F test so 'no common shape' is not asserted
    from a single nonlinear-fit F statistic.
Writes data/e6_shape_comparison.csv and data/universalization_common_shape_bootstrap.csv.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import f as fdist
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
rng=np.random.default_rng(20261120)
def logistic(t,K,r,t0): return K/(1+np.exp(-r*(t-t0)))
def gompertz(t,K,r,t0): return K*np.exp(-np.exp(-r*(t-t0)))
def linear(t,a,b): return a+b*t
def exponential(t,a,b): return a*np.exp(b*(t-t.min()))
SHAPES={'logistic':(logistic,3),'gompertz':(gompertz,3),'linear':(linear,2),'exponential':(exponential,2)}

def fit(shape,t,y,cap=130.,warm=None):
    hi=float(np.max(y))
    if shape in (logistic,gompertz):
        lo=[max(hi,1.0),0.005,t.min()-30]; up=[max(cap,hi*1.02),1.5,t.max()+30]
        starts=([warm] if warm is not None else
                [[min(max(hi*1.05,lo[0]+1e-6),up[0]-1e-6),r0,t0] for r0 in (0.03,0.06,0.12,0.25)
                 for t0 in (np.median(t)-10,np.median(t),np.median(t)+10)])
    elif shape is linear:
        lo=[-500,0]; up=[500,50]; starts=[[float(np.mean(y)),0.01]]
    else:
        lo=[0,-0.5]; up=[500,0.5]; starts=[[max(float(y.min()),0.1),0.02]]
    best=None
    for p0 in starts:
        try: p,_=curve_fit(shape,t,y,p0=p0,bounds=(lo,up),maxfev=20000)
        except Exception: continue
        sse=float(np.sum((y-shape(t,*p))**2))
        if best is None or sse<best[0]: best=(sse,p)
    return best

# ---------- registry (six countries, GMR observed; plus key wide-panel series) ----------
g=pd.read_csv(os.path.join(BASE,'04_data','data','gmr_observed_6countries_1970_2024.csv'))
SER={'ger_secondary':('secondary GER','GER'),'ger_tertiary':('tertiary GER','GER'),
     'ger_upper_secondary':('upper-secondary GER','GER'),'ner_primary':('primary NER','completion'),
     'ner_secondary':('secondary NER','completion')}
recs=[]
for iso in ['PHL','KHM','CHN','HKG','KOR','JPN']:
    for ind,(lab,capm) in SER.items():
        s=g[(g.iso3==iso)&(g.indicator==ind)][['year','value']].dropna().sort_values('year')
        if len(s)>=20: recs.append(dict(iso3=iso,indicator=ind,label=lab,capm=capm,t=s.year.values.astype(float),y=s.value.values.astype(float)))

# ---------- (a) E6 model comparison ----------
rows=[]
for rec in recs:
    t,y=rec['t'],rec['y']; tr=(t>=1980)&(t<=2010); te=(t>=2011)
    if tr.sum()<12 or te.sum()<3: continue
    for nm,(sh,k) in SHAPES.items():
        b=fit(sh,t[tr],y[tr])
        if b is None: continue
        pred=sh(t[te],*b[1])
        rmse=float(np.sqrt(np.mean((y[te]-pred)**2))); mae=float(np.mean(np.abs(y[te]-pred)))
        sse=float(np.sum((y[tr]-sh(t[tr],*b[1]))**2)); n=int(tr.sum())
        aic=float(n*np.log(max(sse/n,1e-12))+2*k)
        rows.append(dict(iso3=rec['iso3'],indicator=rec['indicator'],label=rec['label'],form=nm,
            n_fit=n,n_test=int(te.sum()),fit_rmse=round(float(np.sqrt(sse/n)),3),aic=round(aic,1),
            holdout_rmse=round(rmse,3),holdout_mae=round(mae,3)))
e6=pd.DataFrame(rows)
# winner per series by holdout RMSE
e6['holdout_winner']=False
for (iso,ind),grp in e6.groupby(['iso3','indicator']):
    e6.loc[grp.holdout_rmse.idxmin(),'holdout_winner']=True
e6.to_csv(os.path.join(D,'e6_shape_comparison.csv'),index=False)
print('E6 rows:',len(e6))
print('\nWINNERS BY FORM (holdout 2011-2024):')
print(e6[e6.holdout_winner].form.value_counts().to_string())
print('\nby series:')
print(e6[e6.holdout_winner][['iso3','indicator','form','fit_rmse','holdout_rmse']].to_string(index=False))

# ---------- (b) bootstrap of the common-shape F test ----------
def common_shape(t_list,y_list,cap=130.,reps=40):
    data=[(t,y) for t,y in zip(t_list,y_list) if len(t)>=12]
    if len(data)<4: return None
    fitted=[]
    sse_free=0; N=0
    for t,y in data:
        b=fit(logistic,t,y,cap)
        if b is None: return None
        fitted.append((t,y,b)); sse_free+=b[0]; N+=len(t)
    npar_free=3*len(data)
    def restricted_sse(dataset):
        best=None
        for rg in np.arange(0.01,0.6,0.02):
            sse=0.0; ok=True
            for t,y in dataset:
                def f2(tt,K,t0,rr=rg): return logistic(tt,K,rr,t0)
                hi=float(np.max(y))
                try: p,_=curve_fit(f2,t,y,p0=[max(hi*1.05,1),float(np.median(t))],
                        bounds=([max(hi,1.0),t.min()-30],[max(cap,hi*1.02),t.max()+30]),maxfev=10000)
                except Exception: ok=False; break
                sse+=float(np.sum((y-f2(t,*p))**2))
            if ok and (best is None or sse<best[0]): best=(sse,rg)
        return best
    res=restricted_sse(data)
    if res is None: return None
    sse_c,rg=res; npar_c=2*len(data)+1
    def Fstat(sf,sc):
        d1=npar_free-npar_c; d2=N-npar_free
        if d1<=0 or d2<=0: return np.nan
        return ((sc-sf)/d1)/(sf/d2)
    F0=Fstat(sse_free,sse_c)
    # residual bootstrap: resample within-country residuals, refit both models with warm starts
    Fb=[]
    for _ in range(reps):
        syn=[]
        for (t,y,b) in fitted:
            pred=logistic(t,*b[1]); resid=y-pred
            ys=pred+rng.choice(resid,size=len(resid),replace=True)
            syn.append((t,ys))
        sf=0.0; ok=True
        for t,ys in syn:
            bb=fit(logistic,t,ys,cap)
            if bb is None: ok=False; break
            sf+=bb[0]
        if not ok: continue
        rr=restricted_sse(syn)
        if rr is None: continue
        Fb.append(Fstat(sf,rr[0]))
    Fb=np.array([f for f in Fb if np.isfinite(f)])
    pb=float(np.mean(Fb>=F0)) if len(Fb) else np.nan
    return dict(n_countries=len(data),N=N,rmse_free=round(float(np.sqrt(sse_free/N)),3),
                rmse_common=round(float(np.sqrt(sse_c/N)),3),shared_r=round(float(rg),3),
                F=round(float(F0),3),p_F_asymptotic=round(float(1-fdist.cdf(F0,3*len(data)-(2*len(data)+1),N-3*len(data))),4),
                boot_reps=len(Fb),boot_F_median=round(float(np.median(Fb)),3) if len(Fb) else np.nan,
                p_bootstrap=round(pb,3) if len(Fb) else np.nan)

boot=[]
for ind in ['ger_secondary','ger_tertiary','ger_upper_secondary']:
    rs=[r for r in recs if r['indicator']==ind]
    if len(rs)<4: continue
    r=common_shape([x['t'] for x in rs],[x['y'] for x in rs],reps=100)
    if r: boot.append(dict(indicator=ind,label=rs[0]['label'],**r))
for ind in ['SE.SEC.ENRR']:
    d=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
    tl=[];yl=[]
    for iso,s in d[['iso3','year',ind]].dropna().groupby('iso3'):
        s=s.sort_values('year')
        if len(s)>=20: tl.append(s.year.values.astype(float)); yl.append(s[ind].values.astype(float))
    if len(tl)>=8:
        r=common_shape(tl,yl,reps=25)
        if r: boot.append(dict(indicator=ind,label='wide panel',**r))
b=pd.DataFrame(boot); b.to_csv(os.path.join(D,'universalization_common_shape_bootstrap.csv'),index=False)
print('\nCOMMON-SHAPE BOOTSTRAP:')
print(b.to_string(index=False))
