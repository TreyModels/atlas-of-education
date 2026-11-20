"""Literacy x GDP x ECI, with cohort-replacement decomposition (population pyramids).
Observed cells only. ECI = Growth Lab / Harvard Dataverse doi:10.7910/DVN/XTAQMC (CC0), eci_sitc/eci_hs92.
Key idea (Menefee): a rising adult literacy rate is partly old illiterates dying, not new learning.
We separate (a) cohort replacement from (b) within-cohort/adult learning and quantify the split.
"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from panel_lib import load_panel, fe_ols

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,'data')
d=load_panel()
eci=pd.read_csv(os.path.join(ROOT,'raw','eci_growth_proj_rankings.csv'))
eci=eci.rename(columns={'country_iso3_code':'iso3'})[['iso3','year','eci_sitc','eci_hs92','eci_hs12','eci_rank_sitc','growth_proj','in_rankings']]
d=d.merge(eci,on=['iso3','year'],how='left')
d.to_csv(os.path.join(D,'panel_wdi_eci.csv'),index=False)

# ---------- derived ----------
d['lit_adult']=d['SE.ADT.LITR.ZS']; d['lit_youth']=d['SE.ADT.1524.LT.ZS']
d['lit_gap']=d['lit_youth']-d['lit_adult']
d['log_gdppc']=np.log(d['NY.GDP.PCAP.KD'].clip(lower=1e-3))
d['log_gdp']=np.log(d['NY.GDP.MKTP.KD'].clip(lower=1e-3))
d['sh014']=d['SP.POP.0014.TO.ZS']; d['sh1564']=d['SP.POP.1564.TO.ZS']; d['sh65']=d['SP.POP.65UP.TO.ZS']
d['log_tfr']=np.log(d['SP.DYN.TFRT.IN'].clip(lower=1e-3))
d['log_cmpt_p']=np.log(d['SE.PRM.CMPT.ZS'].clip(lower=1e-3))
d['log_secattain']=np.log(d['SE.SEC.CUAT.UP.ZS'].clip(lower=1e-3))
d['cbr']=d['SP.DYN.CBRT.IN']; d['cdr']=d['SP.DYN.CDRT.IN']; d['le']=d['SP.DYN.LE00.IN']
d['pop']=d['SP.POP.TOTL']; d['pop15plus']=d['pop']*(1-d['sh014']/100.0)
# births 15 years earlier -> size of the cohort now entering the 15+ stock (derived, not observed)
d=d.sort_values(['iso3','year'])
d['births']=d['cbr']/1000.0*d['pop']
d['entrants15']=d.groupby('iso3')['births'].shift(15)
d['entrant_share']=d['entrants15']/d['pop15plus']          # annual inflow into the 15+ stock
d['exit_share']=d['cdr']/1000.0*d['pop']/d['pop15plus']    # annual deaths over 15+ (upper bound: all deaths)
d['replacement_flow']=d['entrant_share']*(d['lit_youth'].shift(5)-d['lit_adult']) \
                      + d['exit_share']*(d['lit_adult']-d.groupby('iso3')['lit_youth'].shift(55))
d['dlit5']=d.groupby('iso3')['lit_adult'].diff(5)

# ---------- ECI x GDP x literacy ----------
rows=[]
def add(name,y,x,res,note=''):
    if 'error' in res: rows.append(dict(test=name,outcome=y,driver=x,error=res['error'],note=note)); return
    keys=list(res.keys())
    for xi in [t.strip() for t in x.split('+')]:
        xi = xi if xi in keys else next((k for k in keys if k.split(' ')[0]==xi.split(' ')[0]), xi)
        a=res[xi]; rows.append(dict(test=name,outcome=y,driver=xi,coef=a['coef'],se=a['se'],t=a['t'],p=a['p'],
            n=res['n'],n_cty=res['n_cty'],period=res['period'],within_r2=res['r2_within'],note=note))
add('E1','log_gdppc','eci_hs92',fe_ols(d,'log_gdppc',['eci_hs92']))
add('E2','eci_hs92','lit_adult',fe_ols(d,'eci_hs92',['lit_adult']))
add('E3','eci_hs92','log_gdppc',fe_ols(d,'eci_hs92',['log_gdppc']))
add('E4','log_gdppc','eci_hs92 + lit_adult',fe_ols(d,'log_gdppc',['eci_hs92','lit_adult']))
add('E5','eci_hs92','log_cmpt_p (t-10)',fe_ols(d,'eci_hs92',['log_cmpt_p'],lags={'log_cmpt_p':10}))
add('E6','eci_hs92','log_secattain',fe_ols(d,'eci_hs92',['log_secattain']))
add('E7','lit_adult','log_gdppc',fe_ols(d,'lit_adult',['log_gdppc']))
add('E8','lit_adult','log_cmpt_p (t-20)',fe_ols(d,'lit_adult',['log_cmpt_p'],lags={'log_cmpt_p':20}))
add('E9','lit_youth','log_cmpt_p',fe_ols(d,'lit_youth',['log_cmpt_p']))
# growth: ECI vs literacy horse race for 10y-ahead growth
g=d.copy()
g['cum_growth_10y']=g.groupby('iso3')['log_gdp'].diff(10)
add('E10','cum_growth_10y','eci_hs92 (t)',fe_ols(g,'cum_growth_10y',['eci_hs92']))
add('E11','cum_growth_10y','eci_hs92 + lit_adult',fe_ols(g,'cum_growth_10y',['eci_hs92','lit_adult']))
add('E12','cum_growth_10y','lit_adult',fe_ols(g,'cum_growth_10y',['lit_adult']))
add('E13','cum_growth_10y','growth_proj',fe_ols(g,'cum_growth_10y',['growth_proj']))
# first differences (trend-free)
d['dlog_gdppc']=d.groupby('iso3')['log_gdppc'].diff(); d['deci']=d.groupby('iso3')['eci_hs92'].diff()
d['dlit']=d.groupby('iso3')['lit_adult'].diff()
add('E14','dlog_gdppc','deci',fe_ols(d,'dlog_gdppc',['deci'],diff=False))
add('E15','deci','dlit',fe_ols(d,'deci',['dlit']))
res=pd.DataFrame(rows); res.to_csv(os.path.join(D,'eci_literacy_results.csv'),index=False)
print(res.round(3).to_string(index=False))

# ---------- population pyramids ----------
pyr=[]
for iso in ['PHL','KHM','CHN','HKG','KOR','JPN','IND','VNM','THA','IDN']:
    s=d[(d.iso3==iso)&d.sh014.notna()].copy()
    for dec in [1960,1970,1980,1990,2000,2010,2020]:
        r=s[s.year==dec]
        if len(r)==0: continue
        r=r.iloc[0]
        pyr.append(dict(iso3=iso,year=dec,pop_m=round(r['pop']/1e6,2),sh_0_14=r.sh014,sh_15_64=r.sh1564,
                        sh_65plus=r.sh65,lit_adult=r.lit_adult,lit_youth=r.lit_youth,lit_gap=r.lit_gap))
py=pd.DataFrame(pyr); py.to_csv(os.path.join(D,'population_pyramids.csv'),index=False)

# ---------- cohort-replacement decomposition ----------
# Identity: lit_adult(t) is a stock; its 5-year change = entrants + exits + within-cohort learning.
#   entrant component : new 15-24 literates joining a stock whose average is lit_adult
#   exit component    : old (largely illiterate) cohorts leaving on death
#   within-cohort     : adults who learn after 15 (adult education / literacy campaigns)
# Data: youth literacy (15-24) observed; entrants = births 15y earlier / pop15+; exits = death rate scaled.
# The dying cohort's literacy is NOT observed -> bounded between 0 and the earliest observed youth literacy.
dec=[]
for iso in d.iso3.unique():
    s2=d[(d.iso3==iso)&d.lit_adult.notna()&d.lit_youth.notna()].sort_values('year')
    if len(s2)<3: continue
    ymin=s2.lit_youth.iloc[0]           # earliest observed youth literacy = proxy for old cohorts
    for i in range(1,len(s2)):
        t0,t1=s2.iloc[i-1],s2.iloc[i]
        if t1.year-t0.year>8: continue
        dt=t1.year-t0.year
        if pd.isna(t0.entrant_share) or pd.isna(t0.exit_share) or pd.isna(t0.lit_gap): continue
        ent=t0.entrant_share*dt*(t0.lit_youth-t0.lit_adult)          # pp change over the period
        ex_lo=t0.exit_share*dt*(t0.lit_adult-t0.lit_adult)           # dying cohort assumed as literate as the stock (lower bound)
        ex_hi=t0.exit_share*dt*(t0.lit_adult-max(min(ymin,t0.lit_youth),0.0))  # dying cohort at earliest youth literacy (upper bound)
        dlit=float(t1.lit_adult-t0.lit_adult)
        dec.append(dict(iso3=iso,y0=int(t0.year),y1=int(t1.year),dt=dt,
            lit0=float(t0.lit_adult),lit1=float(t1.lit_adult),dlit=dlit,
            youth0=float(t0.lit_youth),gap0=float(t0.lit_gap),
            entrant_share=float(t0.entrant_share),exit_share=float(t0.exit_share),
            E_entrant=float(ent),X_exit_lo=float(ex_lo),X_exit_hi=float(ex_hi),
            replacement_lo=float(ent+ex_lo),replacement_hi=float(ent+ex_hi),
            resid_lo=float(dlit-(ent+ex_hi)),resid_hi=float(dlit-(ent+ex_lo))))
dec=pd.DataFrame(dec); dec.to_csv(os.path.join(D,'literacy_cohort_decomposition.csv'),index=False)
print('decomposition rows:',len(dec),'| countries:',dec.iso3.nunique())
print('\n--- per-country mean 5y change and components (pp) ---')
tab=dec.groupby('iso3').agg(n=('dlit','size'),dlit=('dlit','mean'),E=('E_entrant','mean'),
    X_lo=('X_exit_lo','mean'),X_hi=('X_exit_hi','mean'),resid_lo=('resid_lo','mean'),resid_hi=('resid_hi','mean'))
tab['repl_total_lo']=tab.E+tab.X_lo; tab['repl_total_hi']=tab.E+tab.X_hi
tab['replacement_share_lo']=tab.repl_total_lo/(tab.dlit.replace(0,np.nan))
tab['replacement_share_hi']=tab.repl_total_hi/(tab.dlit.replace(0,np.nan))
print(tab.round(3).to_string())
pos=tab[(tab.dlit>0)&tab.replacement_share_hi.notna()]
print('\nMEDIAN replacement share of observed literYU increase (hi bound):', round(float(pos.replacement_share_hi.median()),3),
      '| lo bound:', round(float(pos.replacement_share_lo.median()),3), '| n countries:', len(pos))
print('unweighted mean dlit pp/period:', round(float(pos.dlit.mean()),3),
      '| mean replacement hi pp:', round(float(pos.repl_total_hi.mean()),3))

# panel regression: does the entrant flow explain the change?
dd=dec[dec.dlit.notna()].copy()
dd['ctry']=dd.iso3
r1=fe_ols(dd,'dlit',['E_entrant'],entity='ctry',time='y1',cluster='ctry',min_n=40,min_cty=8)
r2=fe_ols(dd,'dlit',['E_entrant','gap0'],entity='ctry',time='y1',cluster='ctry',min_n=40,min_cty=8)
print('\nD1 dlit ~ E_entrant:', r1.get('error') or f"b={r1['E_entrant']['coef']:.3f} se={r1['E_entrant']['se']:.3f} p={r1['E_entrant']['p']:.3f} n={r1['n']} ctys={r1['n_cty']} R2w={r1['r2_within']:.3f}")
print('D2 dlit ~ E_entrant + gap0:', r2.get('error') or f"E b={r2['E_entrant']['coef']:.3f} (se {r2['E_entrant']['se']:.3f}); gap0 b={r2['gap0']['coef']:.3f} (se {r2['gap0']['se']:.3f}); n={r2['n']}")
def pack(nm,dep,x,r):
    if 'error' in r: return dict(test=nm,dep=dep,driver=x,error=r['error'])
    a=r[x]; return dict(test=nm,dep=dep,driver=x,coef=a['coef'],se=a['se'],t=a['t'],p=a['p'],n=r['n'],
                        n_cty=r['n_cty'],within_r2=r['r2_within'])
pd.DataFrame([pack('D1','dlit','E_entrant',r1),pack('D2a','dlit','E_entrant',r2),pack('D2b','dlit','gap0',r2)]
             ).to_csv(os.path.join(D,'literacy_decomposition_regressions.csv'),index=False)


# ---------- E16/E17: canonical cross-sectional ECI growth test (year FE only, no country FE) ----------
def year_fe_ols(df, y, xs, time='year', cluster='iso3'):
    import numpy as np, pandas as pd
    dd=df[[time,cluster,y]+list(xs)].dropna().copy()
    if len(dd)<40 or dd[cluster].nunique()<8: return {'error':f'insufficient (n={len(dd)})'}
    Xd=pd.get_dummies(dd[time],drop_first=True,dtype=float)
    X=np.column_stack([np.ones(len(dd)),dd[list(xs)].values.astype(float),Xd.values])
    yv=dd[y].values.astype(float)
    b,*_=np.linalg.lstsq(X,yv,rcond=None)
    e=yv-X@b; k=X.shape[1]; dof=max(len(dd)-k,1)
    inv=np.linalg.pinv(X.T@X); meat=np.zeros((k,k))
    for g in dd[cluster].unique():
        m=(dd[cluster].values==g); s=X[m].T@e[m]; meat+=np.outer(s,s)
    V=inv@meat@inv*(dd[cluster].nunique()/(dd[cluster].nunique()-1))
    se=np.sqrt(np.diag(V))
    out={'n':len(dd),'n_cty':dd[cluster].nunique(),'period':f"{int(dd[time].min())}-{int(dd[time].max())}"}
    for i,x in enumerate(xs): out[x]=dict(coef=float(b[1+i]),se=float(se[1+i]),t=float(b[1+i]/se[1+i]),p=float(2*(1-0.5*(1+np.vectorize(__import__('math').erf)(abs(b[1+i]/se[1+i])/np.sqrt(2))))))
    return out
rows=[]
for nm,y,xs in [('E16','cum_growth_10y',['eci_hs92','log_gdppc']),('E17','cum_growth_10y',['eci_hs92','lit_adult','log_gdppc'])]:
    r=year_fe_ols(g,y,xs)
    if 'error' in r: rows.append(dict(test=nm,error=r['error'])); continue
    for x in xs:
        a=r[x]; rows.append(dict(test=nm,outcome=y,driver=x,coef=a['coef'],se=a['se'],t=a['t'],p=a['p'],
            n=r['n'],n_cty=r['n_cty'],period=r['period'],note='year FE only (cross-sectional test, no country FE)'))
pd.DataFrame(rows).to_csv(os.path.join(D,'eci_growth_crosssection.csv'),index=False)
print('\nE16/E17 (year-FE cross-sectional ECI growth test):')
print(pd.DataFrame(rows).round(3).to_string(index=False))

# ---------- did literacy gains come from schooling, or from death? country examples ----------
ex=[]
for iso in ['PHL','KHM','CHN','IND','VNM','THA','IDN','KOR','JPN','HKG']:
    s2=d[d.iso3==iso].sort_values('year')
    s2=s2[s2.lit_adult.notna()]
    if len(s2)<2: 
        ex.append(dict(iso3=iso,note='no adult literacy series in WDI (developed-country reporting gap)')); continue
    a,b=s2.iloc[0],s2.iloc[-1]
    ex.append(dict(iso3=iso,y0=int(a.year),y1=int(b.year),lit_start=a.lit_adult,lit_end=b.lit_adult,
                   change=b.lit_adult-a.lit_adult,pop_start_m=a['pop']/1e6,pop_end_m=b['pop']/1e6,
                   sh014_start=a.sh014,sh014_end=b.sh014,sh65_start=a.sh65,sh65_end=b.sh65,
                   youth_end=b.lit_youth,gap_end=b.lit_gap,
                   note=''))
pd.DataFrame(ex).to_csv(os.path.join(D,'literacy_country_examples.csv'),index=False)
print('\ncountry examples written')
