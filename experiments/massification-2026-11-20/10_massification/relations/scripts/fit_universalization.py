"""Universalization curves: logistic and Gompertz fits to observed enrollment/completion series.
Design declared before fitting: fit window 1980-2010, holdout 2011-2024. Six countries (GMR observed, never imputed)
plus the 30-country WDI panel. Also tests the common-shape/country-timing hypothesis (shared slope r).
Writes data/universalization_fits.csv and data/universalization_common_shape.csv.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import f as fdist
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); os.makedirs(D,exist_ok=True)
BASE=os.path.abspath(os.path.join(ROOT,'..','..'))

def logistic(t,K,r,t0): return K/(1.0+np.exp(-r*(t-t0)))
def gompertz(t,K,r,t0): return K*np.exp(-np.exp(-r*(t-t0)))
SHAPES={'logistic':logistic,'gompertz':gompertz}

def fit_shape(t,y,shape,cap):
    """Multi-start bounded NLS. Ceiling must be >= observed max (a curve cannot top out below the data)."""
    hi_y=float(np.max(y)); Kmin=max(hi_y,1.0); Kmax=max(cap, Kmin*1.02)
    lo=[Kmin,0.005,float(t.min())-30]; hi=[Kmax,1.5,float(t.max())+30]
    best=None
    for K0 in [Kmin, Kmin+0.05*(Kmax-Kmin), Kmin+0.25*(Kmax-Kmin), Kmin+0.6*(Kmax-Kmin)]:
        for r0 in [0.03,0.06,0.12,0.25]:
            for t0 in [float(np.median(t))-10, float(np.median(t)), float(np.median(t))+10]:
                p0=[min(max(K0,Kmin+1e-6),Kmax-1e-6),r0,min(max(t0,lo[2]+1e-6),hi[2]-1e-6)]
                try: p,cov=curve_fit(shape,t,y,p0=p0,bounds=(lo,hi),maxfev=50000)
                except Exception: continue
                pred=shape(t,*p); sse=float(np.sum((y-pred)**2))
                if best is None or sse<best[0]:
                    best=(sse,p,cov)
    if best is None: return None
    sse,p,cov=best
    se=np.sqrt(np.diag(cov)); pred=shape(t,*p); n=len(t)
    K,r_,t0=p
    return dict(K=K,K_se=se[0],r=r_,r_se=se[1],t0=t0,t0_se=se[2],
                rmse=float(np.sqrt(sse/n)),r2=1-sse/max(float(np.sum((y-y.mean())**2)),1e-12),
                aic=float(n*np.log(max(sse/n,1e-12))+6),sse=sse,n=n,pred=pred,
                ident_flags=';'.join([f for f,c in [
                    ('ceiling_at_bound', K>Kmax-1e-3),
                    ('ceiling_imprecise(K_se/K>0.3)', se[0]/max(K,1e-9)>0.3),
                    ('slope_at_bound', r_<=0.0051 or r_>=1.4999),
                    ('midpoint_outside_window', t0<t.min() or t0>t.max())] if c]))

CAPS={'GER':130.0,'completion':100.5}
def series_registry():
    reg=[]
    g=pd.read_csv(os.path.join(BASE,'04_data','data','gmr_observed_6countries_1970_2024.csv'))
    specs=[('ger_primary','GER','primary','GER'),('ger_secondary','GER','secondary','GER'),
           ('ger_tertiary','GER','tertiary','GER'),('ger_lower_secondary','GER','lower secondary','GER'),
           ('ger_upper_secondary','GER','upper secondary','GER'),('ner_primary','NER','primary','NER'),
           ('ner_secondary','NER','secondary','NER'),('completion_primary','completion','primary','completion'),
           ('completion_lower_secondary','completion','lower secondary','completion'),
           ('completion_upper_secondary','completion','upper secondary','completion')]
    for iso in ['PHL','KHM','CHN','HKG','KOR','JPN']:
        cname=g.loc[g.iso3==iso,'country'].iloc[0]
        for ind,lab,lev,mtype in specs:
            s=g[(g.iso3==iso)&(g.indicator==ind)][['year','value']].dropna()
            if len(s)>=12: reg.append(dict(iso3=iso,country=cname,indicator=ind,label=lab,level=lev,
                measure=mtype,source='GMR observed',df=s.sort_values('year')))
    d=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
    wide={'SE.PRM.ENRR':('GER','primary','GER'),'SE.SEC.ENRR':('GER','secondary','GER'),
          'SE.TER.ENRR':('GER','tertiary','GER'),'SE.SEC.ENRR.UP':('GER','upper secondary','GER'),
          'SE.PRM.CMPT.ZS':('completion','primary','completion'),
          'SE.SEC.CMPT.LO.ZS':('completion','lower secondary','completion')}
    for code,(lab,lev,mtype) in wide.items():
        for iso,s in d[['iso3','country','year',code]].dropna().groupby('iso3'):
            reg.append(dict(iso3=iso,country=s.country.iloc[0],indicator=code,label=lab,level=lev,
                measure=mtype,source='WDI 30-country panel',df=s[['year',code]].rename(columns={code:'value'}).sort_values('year')))
    return reg

def fit_series(rec):
    s=rec['df'].copy(); s=s[(s.year>=1970)&(s.year<=2024)]
    t=s.year.values.astype(float); y=s.value.values.astype(float)
    if len(t)<12: return []
    cap=CAPS['completion'] if rec['measure']=='completion' else CAPS['GER']
    base=dict(iso3=rec['iso3'],country=rec['country'],indicator=rec['indicator'],label=rec['label'],
              level=rec['level'],measure_type=rec['measure'],source=rec['source'])
    rows=[]
    alt={}
    for nm,sh in SHAPES.items():
        f=fit_shape(t,y,sh,cap)
        if f: alt[nm]=f
    if not alt: return []
    best=min(alt,key=lambda k:alt[k]['aic'])
    for nm,f in alt.items():
        rows.append({**base,'fit_sample':'full','years':f"{int(t.min())}-{int(t.max())}",'n_obs':f['n'],'model':nm,
            'K':round(f['K'],2),'K_se':round(f['K_se'],2),'r':round(f['r'],4),'r_se':round(f['r_se'],4),
            't0':round(f['t0'],1),'t0_se':round(f['t0_se'],1),'rmse':round(f['rmse'],3),'r2':round(f['r2'],4),
            'aic':round(f['aic'],1),'better_shape':(nm==best),'ident_flags':f['ident_flags']})
    # holdout
    tr=(t>=1980)&(t<=2010); te=(t>=2011)
    if tr.sum()>=12 and te.sum()>=3:
        for nm,sh in SHAPES.items():
            f=fit_shape(t[tr],y[tr],sh,cap)
            if not f: continue
            pred=sh(t[te],f['K'],f['r'],f['t0'])
            rhi=float(np.sqrt(np.mean((y[te]-pred)**2)))
            mhi=float(np.mean(np.abs((y[te]-pred)/np.maximum(np.abs(y[te]),1e-9)))*100)
            rows.append({**base,'fit_sample':'1980-2010','years':f"{int(t[tr].min())}-{int(t[tr].max())}",
                'n_obs':int(tr.sum()),'model':nm,'K':round(f['K'],2),'K_se':round(f['K_se'],2),
                'r':round(f['r'],4),'r_se':round(f['r_se'],4),'t0':round(f['t0'],1),'t0_se':round(f['t0_se'],1),
                'rmse':round(f['rmse'],3),'r2':round(f['r2'],4),'aic':round(f['aic'],1),
                'holdout_n':int(te.sum()),'holdout_rmse':round(rhi,3),'holdout_mape':round(mhi,1),
                'ident_flags':f['ident_flags']})
    return rows

def common_shape_test(recs, shape=logistic, cap=130.0, share_name='GER'):
    """H0: same slope r, country-specific ceiling K and midpoint t0. Free: country-specific r too."""
    data=[]
    for r in recs:
        s=r['df'].copy(); s=s[(s.year>=1970)&(s.year<=2024)]
        t=s.year.values.astype(float); y=s.value.values.astype(float)
        if len(t)>=12: data.append((t,y))
    if len(data)<4: return None
    # free
    sse_free=0.0; npar_free=0; N=0
    for t,y in data:
        f=fit_shape(t,y,shape,cap)
        if f is None: return None
        sse_free+=f['sse']; npar_free+=3; N+=len(t)
    # common r via grid search over r, per-country (K,t0)
    best=None
    for rg in np.arange(0.01,0.6,0.005):
        sse=0.0; ok=True
        for t,y in data:
            def f2(tt,K,t0): return shape(tt,K,rg,t0)
            try:
                p,_=curve_fit(f2,t,y,p0=[max(float(np.max(y))*1.05,1),float(np.median(t))],
                              bounds=([max(float(np.max(y))*0.98,1),float(t.min())-30],
                                      [cap,float(t.max())+30]),maxfev=20000)
            except Exception:
                ok=False; break
            sse+=float(np.sum((y-f2(t,*p))**2))
        if ok and (best is None or sse<best[0]): best=(sse,rg)
    if best is None: return None
    sse_c,rg=best; npar_c=2*len(data)+1
    df1=npar_free-npar_c; df2=N-npar_free
    if df1<=0 or df2<=0: return None
    F=((sse_c-sse_free)/df1)/(sse_free/df2)
    p=float(1-fdist.cdf(F,df1,df2))
    return dict(n_countries=len(data),N=N,rmse_free=round(float(np.sqrt(sse_free/N)),3),
                rmse_common=round(float(np.sqrt(sse_c/N)),3),shared_r=round(float(rg),4),
                F=round(float(F),3),df1=int(df1),df2=int(df2),p=round(p,4),
                verdict=('common shape with country-specific timing NOT rejected (p>0.05)' if p>0.05
                         else 'country-specific slopes REJECT common shape (p<=0.05)'))

reg=series_registry()
rows=[]
for rec in reg: rows+=fit_series(rec)
fit=pd.DataFrame(rows)
fit.to_csv(os.path.join(D,'universalization_fits.csv'),index=False)
print('fits rows:',len(fit),'| series:',fit.groupby(['iso3','indicator']).ngroups)

# common-shape tests over the six countries, by indicator
cs=[]
for ind in ['ger_primary','ger_secondary','ger_tertiary','ger_upper_secondary','ner_primary','ner_secondary',
            'completion_primary','completion_lower_secondary','completion_upper_secondary']:
    recs=[r for r in reg if r['indicator']==ind]
    cap=CAPS['completion'] if recs and recs[0]['measure']=='completion' else CAPS['GER']
    r=common_shape_test(recs,logistic,cap)
    if r: cs.append(dict(indicator=ind,label=recs[0]['label'],level=recs[0]['level'],measure_type=recs[0]['measure'],
                         source=recs[0]['source'],**r))
# and the wider panel: secondary GER across 30 countries
recs30=[r for r in reg if r['indicator']=='SE.SEC.ENRR']
r30=common_shape_test(recs30,logistic,CAPS['GER'])
if r30: cs.append(dict(indicator='SE.SEC.ENRR',label='GER',level='secondary',measure_type='GER',
                       source='WDI 30-country panel',**r30))
recs30p=[r for r in reg if r['indicator']=='SE.PRM.ENRR']
r30p=common_shape_test(recs30p,logistic,CAPS['GER'])
if r30p: cs.append(dict(indicator='SE.PRM.ENRR',label='GER',level='primary',measure_type='GER',
                        source='WDI 30-country panel',**r30p))
cs=pd.DataFrame(cs); cs.to_csv(os.path.join(D,'universalization_common_shape.csv'),index=False)
print(cs.to_string(index=False))
