"""Scaling laws: elasticities of education/economy quantities to income and structure.
Two-way FE (country+year) gives the WITHIN exponent; year-FE (or pooled) gives the BETWEEN exponent.
CR1 SE clustered on country. Every row states the functional form, sample, FE structure and identification grade.
Writes data/scaling_laws.csv.
"""
import os, sys, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); os.makedirs(D,exist_ok=True)
BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
sys.path.insert(0, os.path.join(BASE,'09_relations','scripts'))
from panel_lib import fe_ols

d=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
def L(c,eps=1e-3): return np.log(pd.to_numeric(d[c],errors='coerce').clip(lower=eps))
d['log_gdppc']=L('NY.GDP.PCAP.KD'); d['log_gdppc_ppp']=L('NY.GDP.PCAP.PP.CD')
d['log_ger_p']=L('SE.PRM.ENRR'); d['log_ger_s']=L('SE.SEC.ENRR'); d['log_ger_t']=L('SE.TER.ENRR')
d['log_ger_sup']=L('SE.SEC.ENRR.UP'); d['log_cmpt_p']=L('SE.PRM.CMPT.ZS'); d['log_cmpt_s']=L('SE.SEC.CMPT.LO.ZS')
d['log_attain_s']=L('SE.SEC.CUAT.UP.ZS'); d['log_attain_p']=L('SE.PRM.CUAT.ZS')
d['log_agri']=L('SL.AGR.EMPL.ZS'); d['log_ind']=L('SL.IND.EMPL.ZS'); d['log_srv']=L('SL.SRV.EMPL.ZS')
d['log_urban_share']=L('SP.URB.TOTL.IN.ZS') if False else d['SP.URB.TOTL.IN.ZS']
d['log_tfr']=L('SP.DYN.TFRT.IN'); d['log_pop']=L('SP.POP.TOTL')
d['log_wage_share']=L('SL.EMP.WORK.ZS'); d['tfr']=d['SP.DYN.TFRT.IN']
d['tert_share']=d['SE.TER.ENRL']/(d['SE.TER.ENRL']+d['SE.SEC.ENRL'])
d['log_tert_share']=np.log(d['tert_share'].clip(lower=1e-3))
d['urban']=d['SP.URB.TOTL.IN.ZS']

def year_fe_ols(df,y,xs,time='year',cluster='iso3'):
    dd=df[[time,cluster,y]+list(xs)].dropna().copy()
    if len(dd)<40 or dd[cluster].nunique()<8: return {'error':f'insufficient (n={len(dd)})'}
    Xd=pd.get_dummies(dd[time],drop_first=True,dtype=float)
    X=np.column_stack([np.ones(len(dd)),dd[list(xs)].values.astype(float),Xd.values])
    yv=dd[y].values.astype(float)
    b,*_=np.linalg.lstsq(X,yv,rcond=None)
    e=yv-X@b; k=X.shape[1]
    inv=np.linalg.pinv(X.T@X); meat=np.zeros((k,k))
    for g in dd[cluster].unique():
        m=(dd[cluster].values==g); s=X[m].T@e[m]; meat+=np.outer(s,s)
    V=inv@meat@inv*(dd[cluster].nunique()/(dd[cluster].nunique()-1))
    se=np.sqrt(np.diag(V)); out={'n':len(dd),'n_cty':dd[cluster].nunique()}
    for i,x in enumerate(xs):
        bb=b[1+i]; ss=se[1+i]; out[x]=dict(coef=float(bb),se=float(ss),t=float(bb/ss),
            p=float(2*(1-0.5*(1+np.vectorize(__import__('math').erf)(abs(bb/ss)/np.sqrt(2))))))
    return out

SPECS=[
 ('S1','log_ger_s','log_gdppc','secondary GER','GDP per capita','log-log','enrolment vs income (level)','scaling law candidate'),
 ('S2','log_ger_t','log_gdppc','tertiary GER','GDP per capita','log-log','tertiary vs income','scaling law candidate'),
 ('S3','log_ger_p','log_gdppc','primary GER','GDP per capita','log-log','primary vs income','empirical regularity (saturated)'),
 ('S4','log_cmpt_s','log_gdppc','lower-secondary completion','GDP per capita','log-log','completion vs income','scaling law candidate'),
 ('S5','log_attain_s','log_gdppc','upper-secondary attainment (stock)','GDP per capita','log-log','attainment vs income','scaling law candidate'),
 ('S6','log_tert_share','log_gdppc','tertiary share of enrolment','GDP per capita','log-log','tertiary share vs income','scaling law candidate'),
 ('S7','log_agri','log_gdppc','agricultural employment share','GDP per capita','log-log','sector share vs income (Engel)','scaling law candidate'),
 ('S8','log_ind','log_gdppc','industrial employment share','GDP per capita','log-log','sector share vs income','empirical regularity'),
 ('S9','log_srv','log_gdppc','services employment share','GDP per capita','log-log','sector share vs income','scaling law candidate'),
 ('S10','log_gdppc','log_attain_s','GDP per capita','upper-secondary attainment','log-log','education stock vs output','not identifiable as causal'),
 ('S11','log_ger_s','log_tfr','secondary GER','total fertility rate','log-log','cohort size vs enrolment','scaling law candidate'),
 ('S12','log_cmpt_p','tfr','primary completion','total fertility rate','semi-log','cohort size vs completion','scaling law candidate'),
 ('S13','log_ger_s','urban','secondary GER','urban population share','semi-log (pp)','urban share vs enrolment','empirical regularity'),
 ('S14','log_wage_share','log_gdppc','wage-and-salaried share','GDP per capita','log-log','formal share vs income','scaling law candidate'),
 ('S15','log_gdppc','log_cmpt_p','GDP per capita','primary completion','log-log','output vs education flow (reverse)','not identifiable as causal'),
]
rows=[]
for sid,y,x,ylab,xlab,form,rel,grade in SPECS:
    if y not in d or x not in d: continue
    # within (two-way FE)
    r=fe_ols(d,y,[x])
    if 'error' not in r:
        a=r[x]
        rows.append(dict(id=sid+'-within',outcome=ylab,driver=xlab,functional_form=form,relation=rel,
            fe_structure='country+year FE',coef=round(a['coef'],4),se=round(a['se'],4),t=round(a['t'],2),p=round(a['p'],4),
            n=r['n'],n_cty=r['n_cty'],period=r['period'],within_r2=round(r['r2_within'],3),
            identification_grade='correlational',classification=grade,
            note='within-country exponent; FE removes fixed country differences and common year shocks'))
    # between (year FE only)
    rb=year_fe_ols(d,y,[x])
    if 'error' not in rb:
        a=rb[x]
        rows.append(dict(id=sid+'-between',outcome=ylab,driver=xlab,functional_form=form,relation=rel,
            fe_structure='year FE only (cross-country)',coef=round(a['coef'],4),se=round(a['se'],4),
            t=round(a['t'],2),p=round(a['p'],4),n=rb['n'],n_cty=rb['n_cty'],period='',
            identification_grade='correlational',classification=grade,
            note='between-country (cross-sectional) exponent; the classic scaling-law object'))
out=pd.DataFrame(rows); out.to_csv(os.path.join(D,'scaling_laws.csv'),index=False)
print(out[['id','outcome','driver','coef','se','t','p','n','n_cty','classification']].to_string(index=False))
