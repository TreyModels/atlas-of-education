"""Push-pull tests: panel Granger-style lead-lag between schooling and the economy.
Two-way FE (country+year), CR1 clustered on country; Wald test on the block of lags of the candidate driver
after controlling for own lags. Reports sign, lag structure, coefficient sum, and an explicit discrimination note.
Writes data/push_pull_tests.csv.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.stats import chi2
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); os.makedirs(D,exist_ok=True)
BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
d=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
eci=pd.read_csv(os.path.join(BASE,'09_relations','raw','eci_growth_proj_rankings.csv')).rename(columns={'country_iso3_code':'iso3'})[['iso3','year','eci_sitc']]
d=d.merge(eci,on=['iso3','year'],how='left')
def L(c,eps=1e-3): return np.log(pd.to_numeric(d[c],errors='coerce').clip(lower=eps))
d['log_gdppc']=L('NY.GDP.PCAP.KD'); d['log_ger_s']=L('SE.SEC.ENRR'); d['log_ger_t']=L('SE.TER.ENRR')
d['log_cmpt_s']=L('SE.SEC.CMPT.LO.ZS'); d['log_spend']=L('SE.XPD.TOTL.GD.ZS')
d['log_wage']=L('SL.EMP.WORK.ZS'); d['log_cmpt_p']=L('SE.PRM.CMPT.ZS')
d=d.sort_values(['iso3','year'])
for c in ['log_gdppc','log_ger_s','log_ger_t','log_cmpt_s','log_spend','log_wage','eci_sitc','log_cmpt_p']:
    d['d_'+c]=d.groupby('iso3')[c].diff()
d=d.replace([np.inf,-np.inf],np.nan)

def _demean(M,gid,tid,iters=80,tol=1e-10):
    M=M.copy()
    for _ in range(iters):
        old=M.copy()
        M=M-pd.DataFrame(M).groupby(gid).transform('mean').values
        M=M-pd.DataFrame(M).groupby(tid).transform('mean').values
        if np.nanmax(np.abs(M-old))<tol: break
    return M

def granger(df,y,x,maxlag=5):
    cols={'y':y,'x':x,'g':'iso3','t':'year'}
    base=df[['iso3','year',y,x]].dropna().copy()
    if len(base)<80: return {'error':f'insufficient annual observations (n={len(base)})'}
    for k in range(1,maxlag+1):
        base[f'y_l{k}']=base.groupby('iso3')[y].shift(k)
        base[f'x_l{k}']=base.groupby('iso3')[x].shift(k)
    dd=base.dropna()
    if len(dd)<60 or dd.iso3.nunique()<8: return {'error':f'insufficient after lags (n={len(dd)})'}
    Xcols=[f'y_l{k}' for k in range(1,maxlag+1)]+[f'x_l{k}' for k in range(1,maxlag+1)]
    X=dd[Xcols].values.astype(float); yv=dd[[y]].values.astype(float)
    gid=dd.iso3.values; tid=dd.year.values
    Xw=_demean(X,gid,tid); yw=_demean(yv,gid,tid).ravel()
    b,*_=np.linalg.lstsq(Xw,yw,rcond=None); e=yw-Xw@b
    n,k=Xw.shape; G=dd.iso3.nunique(); nent=G; nyr=dd.year.nunique()
    dof=max(n-k-(nent-1)-(nyr-1),1)
    inv=np.linalg.pinv(Xw.T@Xw); meat=np.zeros((k,k))
    for g in dd.iso3.unique():
        m=(dd.iso3.values==g); s=Xw[m].T@e[m]; meat+=np.outer(s,s)
    V=inv@meat@inv*((G/(G-1))*((n-1)/dof))
    L=len(Xcols); q=maxlag
    R=np.zeros((q,k))
    for i in range(q): R[i,maxlag+i]=1.0
    Rb=R@b; Vsub=R@V@R.T
    F=float(Rb@np.linalg.pinv(Vsub)@Rb/q)
    p=float(1-chi2.cdf(F*q,q))
    idx=list(range(maxlag,2*maxlag))
    csum=float(b[idx].sum()); w=np.zeros(k); w[idx]=1.0
    cse=float(np.sqrt(w@V@w))
    coefs=[round(float(b[i]),4) for i in idx]
    ses=[round(float(np.sqrt(V[i,i])),4) for i in idx]
    # best single lag by |t|
    ts=[abs(coefs[i]/max(ses[i],1e-9)) for i in range(maxlag)]
    bl=int(np.argmax(ts))+1
    return dict(n=int(n),n_cty=int(G),maxlag=maxlag,F=round(F,3),p=round(p,4),
                coef_sum=round(csum,4),se_sum=round(cse,4),t_sum=round(csum/max(cse,1e-9),2),
                best_lag=bl,lag_coefs=';'.join(map(str,coefs)),lag_ses=';'.join(map(str,ses)),
                sign='+' if csum>0 else '-' if csum<0 else '0')

TESTS=[
 ('P1','demand-led: growth -> secondary enrollment','d_log_gdppc','d_log_ger_s',
  'do lagged GDP-per-capita growth changes predict secondary-GER growth (after own lags)?'),
 ('P2','demand-led: growth -> tertiary enrollment','d_log_gdppc','d_log_ger_t',
  'do lagged GDP-per-capita growth changes predict tertiary-GER growth (after own lags)?'),
 ('P3','demand-led: growth -> completion','d_log_gdppc','d_log_cmpt_s',
  'do lagged GDP-per-capita growth changes predict lower-secondary completion growth?'),
 ('P4','education-led: secondary enrollment -> growth','d_log_ger_s','d_log_gdppc',
  'do lagged secondary-GER growth changes predict GDP-per-capita growth (after own lags)?'),
 ('P5','education-led: tertiary enrollment -> growth','d_log_ger_t','d_log_gdppc',
  'do lagged tertiary-GER growth changes predict GDP-per-capita growth (after own lags)?'),
 ('P6','education-led: completion -> growth','d_log_cmpt_s','d_log_gdppc',
  'do lagged completion growth changes predict GDP-per-capita growth?'),
 ('P7','supply-led: public spending -> secondary enrollment','d_log_spend','d_log_ger_s',
  'does lagged education-spending growth predict secondary enrolment growth?'),
 ('P8','demand-driven budget: enrollment -> spending','d_log_ger_s','d_log_spend',
  'does lagged enrolment growth predict education-spending growth (budget follows pupils)?'),
 ('P9','jobs channel: formal jobs -> secondary enrollment','d_log_wage','d_log_ger_s',
  'does lagged growth of the wage-and-salaried share predict secondary enrolment growth (demand-led)?'),
 ('P10','jobs channel: secondary enrollment -> formal jobs','d_log_ger_s','d_log_wage',
  'does lagged secondary-enrolment growth predict the wage-and-salaried share (education-led job creation)?'),
 ('P11','demand-led: complexity -> tertiary enrollment','d_eci_sitc','d_log_ger_t',
  'does lagged ECI change predict tertiary-GER growth (complexity pulls enrolment)?'),
 ('P12','education-led: completion -> complexity','d_log_cmpt_s','d_eci_sitc',
  'does lagged completion growth predict ECI change (educated cohorts upgrade exports)?'),
 ('P13','supply-led: primary completion -> secondary enrollment','d_log_cmpt_p','d_log_ger_s',
  'does lagged primary-completion growth predict secondary GER (pipeline/supply)?'),
]
rows=[]
for tid,hyp,y,x,q in TESTS:
    r=granger(d,y,x,maxlag=5)
    base=dict(id=tid,hypothesis=hyp,dependent=y,driver=x,test='panel Granger: y_t ~ own lags(1-5) + driver lags(1-5), two-way FE, CR1 cluster')
    if 'error' in r:
        rows.append({**base,'error':r['error'],'cannot_discriminate':'yes - insufficient annual variation'}); continue
    rows.append({**base,**r,'identification_grade':'correlational (Granger-style prediction, not causality)',
                 'cannot_discriminate':('yes' if r['p']>0.10 else 'no')})
pp=pd.DataFrame(rows); pp.to_csv(os.path.join(D,'push_pull_tests.csv'),index=False)
print(pp[['id','hypothesis','sign','coef_sum','se_sum','t_sum','best_lag','F','p','n','n_cty']].to_string(index=False))
