"""Task-28: ECI relations, ECI as a conditioner of spending/returns channels, best-metric choice.
Inputs: 04_data/complexity/ECONOMIC_COMPLEXITY.csv (canonical, 6 ctys) + the 30-country WDI panel.
Writes: data/economic_complexity_panel.csv, data/economic_complexity_panel_30ctys.csv,
        data/complexity_results.csv, data/complexity_conditioning.csv, data/complexity_metric_choice.csv
"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from panel_lib import load_panel, fe_ols

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,'data')
C6=os.path.join(ROOT,'..','04_data','complexity','ECONOMIC_COMPLEXITY.csv')
eci=pd.read_csv(C6)[['iso3','country','year','eci_sitc','eci_rank_sitc','eci_hs92','eci_rank_hs92',
                     'eci_hs12','eci_rank_hs12','growth_proj','in_rankings']]
d=load_panel()
# canonical 6-country file for the deliverable; archived 30-country raw for panel power
eci30=pd.read_csv(os.path.join(ROOT,'raw','eci_growth_proj_rankings.csv')).rename(columns={'country_iso3_code':'iso3'})
eci30=eci30[['iso3','year','eci_sitc','eci_rank_sitc','eci_hs92','eci_rank_hs92','eci_hs12','eci_rank_hs12','growth_proj','in_rankings']]
d=d.merge(eci30,on=['iso3','year'],how='left',suffixes=('','_c'))

# ---------- derived ----------
d['log_gdppc']=np.log(d['NY.GDP.PCAP.KD'].clip(lower=1e-3)); d['log_gdp']=np.log(d['NY.GDP.MKTP.KD'].clip(lower=1e-3))
d['log_ger_t']=np.log(d['SE.TER.ENRR'].clip(lower=1e-3)); d['log_ger_s']=np.log(d['SE.SEC.ENRR'].clip(lower=1e-3))
d['log_cmpt_s']=np.log(d['SE.SEC.CMPT.LO.ZS'].clip(lower=1e-3)); d['log_cmpt_p']=np.log(d['SE.PRM.CMPT.ZS'].clip(lower=1e-3))
d['log_spend']=np.log(d['SE.XPD.TOTL.GD.ZS'].clip(lower=1e-3)); d['wage_share']=d['SL.EMP.WORK.ZS']
d['vuln_share']=d['SL.EMP.VULN.ZS']; d['log_ger_sup']=np.log(d['SE.SEC.ENRR.UP'].clip(lower=1e-3))
d['dlog_gdp10']=d.groupby('iso3')['log_gdp'].diff(10)
d['lit_youth']=d['SE.ADT.1524.LT.ZS']
# within-country centring of ECI for interaction identification
for c in ['eci_sitc','eci_hs92']:
    d[c+'_c']=d[c]-d.groupby('iso3')[c].transform('mean')
d['spend_x_eci']=d['log_spend']*d['eci_sitc_c']
d['inc_x_eci']=d['log_gdppc']*d['eci_sitc_c']
d['cmpt_x_eci']=d['log_cmpt_s']*d['eci_sitc_c']
d['tert_x_eci']=d['log_ger_t']*d['eci_sitc_c']

# ---------- usable ECI panel (6 countries, canonical) ----------
SIX=['PHL','KHM','CHN','HKG','KOR','JPN']
p6=d[d.eci_sitc.notna()&d.iso3.isin(SIX)].copy()
p6['eci_pctile']=p6.groupby('year')['eci_sitc'].rank(pct=True)*100
p6['eci_z_year']=p6.groupby('year')['eci_sitc'].transform(lambda s:(s-s.mean())/s.std(ddof=0))
p6['eci_growth_5y']=p6.groupby('iso3')['eci_sitc'].pct_change(5)*100
# complexity gap: ECI minus the cross-sectional income-implied ECI (year by year)
def gap(s):
    x=np.log(s['NY.GDP.PCAP.KD'].clip(lower=1e-3)); y=s['eci_sitc']
    m=x.notna()&y.notna()
    if m.sum()<5: return pd.Series(np.nan,index=s.index)
    b=np.polyfit(x[m],y[m],1); pred=np.polyval(b,x)
    return y-pred
p6['complexity_gap']=p6.groupby('year',group_keys=False).apply(gap, include_groups=False) if False else np.nan
gaps=[]
for yr,g in p6.groupby('year'):
    m=g['NY.GDP.PCAP.KD'].notna()&g['eci_sitc'].notna()
    if m.sum()>=5:
        b=np.polyfit(np.log(g.loc[m,'NY.GDP.PCAP.KD']),g.loc[m,'eci_sitc'],1)
        gaps.append(pd.Series(g['eci_sitc']-np.polyval(b,np.log(g['NY.GDP.PCAP.KD'])),index=g.index))
p6['complexity_gap']=pd.concat(gaps).sort_index() if gaps else np.nan
_inc_hi = p6['NY.GDP.PCAP.KD'] >= p6.groupby('year')['NY.GDP.PCAP.KD'].transform('median')
p6['complexity_quadrant']=np.where(p6.eci_pctile>=50,'high-ECI','low-ECI')+np.where(_inc_hi,'+high-income','+low-income')
keep=['iso3','country','year','eci_sitc','eci_rank_sitc','eci_hs92','eci_rank_hs92','eci_hs12','eci_rank_hs12',
      'growth_proj','in_rankings','eci_pctile','eci_z_year','eci_growth_5y','complexity_gap','complexity_quadrant',
      'NY.GDP.PCAP.KD','SE.TER.ENRR','SE.SEC.ENRR','SE.SEC.CMPT.LO.ZS','SE.XPD.TOTL.GD.ZS','SL.EMP.WORK.ZS',
      'SL.EMP.VULN.ZS','SE.ADT.1524.LT.ZS','SP.URB.TOTL.IN.ZS','SP.POP.TOTL','SP.DYN.TFRT.IN']
p6= p6[[c for c in keep if c in p6]].rename(columns={'NY.GDP.PCAP.KD':'gdppc_kd2015','SE.TER.ENRR':'ger_tertiary',
    'SE.SEC.ENRR':'ger_secondary','SE.SEC.CMPT.LO.ZS':'completion_lower_secondary','SE.XPD.TOTL.GD.ZS':'spend_gdp',
    'SL.EMP.WORK.ZS':'wage_salaried_share','SL.EMP.VULN.ZS':'vulnerable_share','SE.ADT.1524.LT.ZS':'literacy_youth',
    'SP.URB.TOTL.IN.ZS':'urban_share','SP.POP.TOTL':'population','SP.DYN.TFRT.IN':'fertility'})
p6.to_csv(os.path.join(D,'economic_complexity_panel.csv'),index=False)
print('economic_complexity_panel.csv:',p6.shape)

# 30-country version (for panel power)
allc=d[d.eci_sitc.notna()].copy()
allc[['iso3','country','year','eci_sitc','eci_hs92','eci_hs12','growth_proj']].to_csv(
    os.path.join(D,'economic_complexity_panel_30ctys.csv'),index=False)
print('30-cty panel rows:',allc.shape[0],'| countries:',allc.iso3.nunique())

# ---------- ECI relations ----------
rows=[]
def add(name,y,x,res,note='',grade='correlational'):
    if 'error' in res: rows.append(dict(test=name,outcome=y,driver=x,error=res['error'],note=note)); return
    keys=list(res.keys())
    for xi in [t.strip() for t in x.split('+')]:
        k = xi if xi in keys else next((kk for kk in keys if kk.split(' ')[0]==xi.split(' ')[0]), xi)
        a=res[k]; rows.append(dict(test=name,outcome=y,driver=xi,coef=a['coef'],se=a['se'],t=a['t'],p=a['p'],
            n=res['n'],n_cty=res['n_cty'],period=res['period'],within_r2=res['r2_within'],grade=grade,note=note))
add('C1','log_ger_t','eci_sitc',fe_ols(d,'log_ger_t',['eci_sitc']),'ECI -> tertiary GER')
add('C2','log_ger_t','eci_sitc lag5',fe_ols(d,'log_ger_t',['eci_sitc'],lags={'eci_sitc':5}),'ECI(t-5) -> tertiary GER')
add('C3','log_cmpt_s','eci_sitc',fe_ols(d,'log_cmpt_s',['eci_sitc']),'ECI -> lower-secondary completion')
add('C4','log_cmpt_s','eci_hs92',fe_ols(d,'log_cmpt_s',['eci_hs92']),'ECI (HS92) -> completion (metric check)')
add('C5','wage_share','eci_sitc',fe_ols(d,'wage_share',['eci_sitc']),'ECI -> wage-and-salaried share (formal proxy)')
add('C6','vuln_share','eci_sitc',fe_ols(d,'vuln_share',['eci_sitc']),'ECI -> vulnerable employment')
add('C7','dlog_gdp10','eci_sitc',fe_ols(d,'dlog_gdp10',['eci_sitc']),'ECI -> 10y growth (t to t+10)')
add('C8','log_ger_s','eci_sitc',fe_ols(d,'log_ger_s',['eci_sitc']),'ECI -> secondary GER')
add('C9','log_ger_sup','eci_sitc',fe_ols(d,'log_ger_sup',['eci_sitc']),'ECI -> upper-secondary GER')
add('C10','lit_youth','eci_sitc',fe_ols(d,'lit_youth',['eci_sitc']),'ECI -> youth literacy')
add('C11','log_ger_t','eci_sitc + log_gdppc',fe_ols(d,'log_ger_t',['eci_sitc','log_gdppc']),'ECI vs income horse race (tertiary)')
add('C12','log_cmpt_s','eci_sitc + log_gdppc',fe_ols(d,'log_cmpt_s',['eci_sitc','log_gdppc']),'ECI vs income horse race (completion)')
res=pd.DataFrame(rows); res.to_csv(os.path.join(D,'complexity_results.csv'),index=False)
print(res.round(3).to_string(index=False))

# ---------- conditioning tests ----------
cond=[]
def addc(name,y,x,res,note=''):
    if 'error' in res: cond.append(dict(test=name,outcome=y,driver=x,error=res['error'],note=note)); return
    keys=list(res.keys())
    for xi in [t.strip() for t in x.split('+')]:
        k = xi if xi in keys else next((kk for kk in keys if kk.split(' ')[0]==xi.split(' ')[0]), xi)
        a=res[k]; cond.append(dict(test=name,outcome=y,driver=xi,coef=a['coef'],se=a['se'],t=a['t'],p=a['p'],
            n=res['n'],n_cty=res['n_cty'],period=res['period'],within_r2=res['r2_within'],note=note))
# (a) does complexity condition the spending->enrolment elasticity?
addc('X1','log_ger_s','log_spend + spend_x_eci',fe_ols(d,'log_ger_s',['log_spend','spend_x_eci']),'spending x complexity interaction, secondary GER')
addc('X2','log_cmpt_s','log_spend + spend_x_eci',fe_ols(d,'log_cmpt_s',['log_spend','spend_x_eci']),'spending x complexity interaction, completion')
addc('X3','log_ger_s','log_spend + spend_x_eci lag5',fe_ols(d,'log_ger_s',['log_spend','spend_x_eci'],lags={'log_spend':5,'spend_x_eci':5}),'lagged interaction')
# (b) does complexity condition the income/returns->tertiary channel?
addc('X4','log_ger_t','log_gdppc + inc_x_eci',fe_ols(d,'log_ger_t',['log_gdppc','inc_x_eci']),'income x complexity, tertiary GER')
# (c) absorptive capacity: does schooling pay off more in complex economies?
addc('X5','dlog_gdp10','log_cmpt_s + cmpt_x_eci',fe_ols(d,'dlog_gdp10',['log_cmpt_s','cmpt_x_eci']),'completion x complexity -> 10y growth (returns channel)')
addc('X6','dlog_gdp10','log_ger_t + tert_x_eci',fe_ols(d,'dlog_gdp10',['log_ger_t','tert_x_eci']),'tertiary x complexity -> 10y growth (returns channel)')
# (d) credential payoff proxy: wage-share response to completion, conditioned on complexity
addc('X7','wage_share','log_cmpt_s',fe_ols(d,'wage_share',['log_cmpt_s']),'completion -> wage-share (payoff proxy)')
addc('X8','wage_share','log_gdppc',fe_ols(d,'wage_share',['log_gdppc']),'income -> wage-share (baseline)')
conf=pd.DataFrame(cond); conf.to_csv(os.path.join(D,'complexity_conditioning.csv'),index=False)
print('\n'+conf.round(3).to_string(index=False))

# ---------- which single metric? ----------
mc=[]
for c in ['eci_sitc','eci_hs92']:
    s=d[d[c].notna()]
    r_gdp=fe_ols(d,'log_gdppc',[c]); r_tert=fe_ols(d,'log_ger_t',[c]); r_cmpt=fe_ols(d,'log_cmpt_s',[c])
    stable=float(s.groupby('iso3')[c].diff().std())
    mc.append(dict(metric=c,n=s[c].notna().sum(),n_cty=s.iso3.nunique(),
        years=f"{int(s.year.min())}-{int(s.year.max())}",
        b_gdp=r_gdp[c]['coef'],t_gdp=r_gdp[c]['t'],r2_gdp=r_gdp['r2_within'],
        b_tert=r_tert[c]['coef'],t_tert=r_tert[c]['t'],r2_tert=r_tert['r2_within'],
        b_cmpt=r_cmpt[c]['coef'],t_cmpt=r_cmpt[c]['t'],r2_cmpt=r_cmpt['r2_within'],
        yr_on_yr_sd=stable))
m=pd.DataFrame(mc)
m['corr_sitc_hs92']=float(d[['eci_sitc','eci_hs92']].dropna().corr().iloc[0,1])
m.to_csv(os.path.join(D,'complexity_metric_choice.csv'),index=False)
print('\n'+m.round(3).to_string(index=False))
