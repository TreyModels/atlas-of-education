"""Heterogeneity splits, interrupted-time-series event windows, and shadow-education gradients."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from panel_lib import load_panel, fe_ols

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT,'data'); os.makedirs(D, exist_ok=True)
d = load_panel()
def lg(c,eps=1e-3): return np.log(d[c].clip(lower=eps)) if c in d else np.nan
d['log_spend_gdp']=lg('SE.XPD.TOTL.GD.ZS'); d['log_gdppc']=lg('NY.GDP.PCAP.KD')
d['log_ger_s']=lg('SE.SEC.ENRR'); d['log_ger_p']=lg('SE.PRM.ENRR'); d['log_ger_t']=lg('SE.TER.ENRR')
d['log_cmpt_s']=lg('SE.SEC.CMPT.LO.ZS'); d['log_cmpt_p']=lg('SE.PRM.CMPT.ZS')
d['log_priv_s']=lg('SE.SEC.PRIV.ZS'); d['log_ptr_p']=lg('SE.PRM.ENRL.TC.ZS')
d['log_tch_s']=lg('SE.SEC.TCHR'); d['log_tch_p']=lg('SE.PRM.TCHR'); d['log_tax_gdp']=lg('GC.TAX.TOTL.GD.ZS')
d['tfr']=d['SP.DYN.TFRT.IN']
d['log_ger_sup']=lg('SE.SEC.ENRR.UP')

# ---------- country baseline typology (pre-2000 means) ----------
base = d[(d.year>=1985)&(d.year<=2000)].groupby('iso3').agg(
    gdppc90=('NY.GDP.PCAP.KD','mean'), urb90=('SP.URB.TOTL.IN.ZS','mean'),
    tax90=('GC.TAX.TOTL.GD.ZS','mean'), gers90=('SE.SEC.ENRR','mean'),
    gert90=('SE.TER.ENRR','mean'), spend90=('SE.XPD.TOTL.GD.ZS','mean')).reset_index()
ASIA = {'CHN','HKG','KHM','PHL','KOR','JPN','VNM','THA','IDN','MYS','SGP','MMR','LAO','MNG','IND','BGD','PAK','LKA','NPL'}
base['region']=np.where(base.iso3.isin(ASIA),'Asia','non-Asia')
base['income_grp']=np.where(base.gdppc90 > base.gdppc90.median(),'high-income-1990','low-income-1990')
base['bursary_grp']=np.where(base.tax90 > base.tax90.median(),'high-tax-capacity','low-tax-capacity')
base['urb_grp']=np.where(base.urb90 > base.urb90.median(),'high-urban','low-urban')
base['base_ger']=np.where(base.gers90 > base.gers90.median(),'GER-high-1990','GER-low-1990')
base.to_csv(os.path.join(D,'country_typology.csv'), index=False)
print('typology thresholds: gdppc median', round(base.gdppc90.median(),0),
      '| tax median', round(base.tax90.median(),2), '| GERs median', round(base.gers90.median(),1),
      '| urb median', round(base.urb90.median(),1))

KEY = [('log_ger_s','log_spend_gdp',5),('log_ger_p','log_spend_gdp',5),('log_cmpt_s','log_spend_gdp',5),
       ('log_ger_s','log_gdppc',5),('log_ger_t','log_gdppc',0),('log_cmpt_s','log_gdppc',0),
       ('log_cmpt_p','tfr',0),('log_ger_s','log_priv_s',0),('log_cmpt_s','log_ptr_p',5),
       ('log_ger_p','log_tch_p',0),('log_spend_gdp','log_tax_gdp',0)]
rows=[]
for gcol in ['region','income_grp','bursary_grp','urb_grp','base_ger']:
    for y,x,kl in KEY:
        for g in base[gcol].unique():
            ctys = set(base.loc[base[gcol]==g,'iso3'])
            sub = d[d.iso3.isin(ctys)]
            r = fe_ols(sub, y, [x], lags={x:kl} if kl else None, min_cty=5, min_n=40)
            b = dict(group_type=gcol, group=g, outcome=y, driver=x, lag_years=kl)
            if 'error' in r: rows.append({**b,'error':r['error']}); continue
            rows.append({**b,'coef':r[x]['coef'],'se':r[x]['se'],'t':r[x]['t'],'p':r[x]['p'],
                         'n':r['n'],'n_cty':r['n_cty'],'period':r['period']})
het=pd.DataFrame(rows); het.to_csv(os.path.join(D,'panel_heterogeneity.csv'), index=False)
print('heterogeneity rows:', len(het))

# ---------- interrupted time series, within country, event windows ----------
def its(y, iso3, event, pre=10, post=7, logv=True, data=None):
    dd = (data if data is not None else d)
    s = dd[dd.iso3==iso3][['year',y]].dropna().sort_values('year')
    s = s[(s.year>=event-pre)&(s.year<=event+post)]
    if len(s) < pre+3: return None
    v = np.log(s[y].clip(lower=1e-3)) if logv else s[y]
    s = s.assign(lv=v.values)
    s['trend'] = s.year - event
    s['post'] = (s.year >= event).astype(int)
    X = np.column_stack([np.ones(len(s)), s.trend, s.post])
    b, *_ = np.linalg.lstsq(X, s.lv.values, rcond=None)
    e = s.lv.values - X@b
    dof = max(len(s)-3,1)
    s2 = (e@e)/dof
    XtXi = np.linalg.pinv(X.T@X)
    se = np.sqrt(np.diag(XtXi*s2))
    pre_rms = float(np.sqrt(np.mean(e[s.post.values==0]**2)))
    return dict(jump_log=float(b[2]), se=float(se[2]), t=float(b[2]/se[2]), n=len(s),
                pre_rms=pre_rms, pre_n=int((s.post==0).sum()), post_n=int((s.post==1).sum()),
                y_pre=float(np.mean(s.lv.values[s.post.values==0])),
                y_post=float(np.mean(s.lv.values[s.post.values==1])))

EVENTS = [
 ('PHL',2016,'log_ger_s','RA 10533 K-12: Grade 11-12 enters upper secondary (GER denominator/level shift)'),
 ('PHL',2016,'log_ger_sup','K-12 upper-secondary level'),
 ('PHL',2018,'log_ger_t','RA 10931 free SUC tuition (tertiary demand)'),
 ('HKG',1971,'log_ger_s','HK 6-year free compulsory primary (1971)'),
 ('HKG',1978,'log_ger_s','HK 9-year free compulsory education (1978)'),
 ('KOR',1974,'log_ger_s','Korea high-school equalisation (1974)'),
 ('KOR',2004,'log_ger_s','Korea compulsory middle schooling (2004)'),
 ('CHN',1986,'log_ger_s','China Compulsory Education Law (1986)'),
 ('IDN',1994,'log_ger_s','Indonesia 9-year compulsory education (1994)'),
 ('THA',1999,'log_ger_s','Thailand Education Act 1999'),
 ('VNM',1991,'log_ger_s','Vietnam universal primary/1991 reforms'),
 ('KHM',1996,'log_ger_s','Cambodia post-conflict secondary reconstruction (1996)'),
 ('KHM',2014,'log_ger_s','Cambodia teacher pay reform (2014-18)'),
 ('MYS',1996,'log_ger_s','Malaysia 6th Malaysia Plan K-12 expansion'),
 ('JPN',1980,'log_ger_t','Japan tertiary expansion 1980s'),
]
d['log_ger_sup']=lg('SE.SEC.ENRR.UP')
ev=[]
for iso,yr,y,lab in EVENTS:
    if y not in d: continue
    r = its(y, iso, yr)
    if r: ev.append(dict(iso3=iso, event_year=yr, outcome=y, event=lab, **r,
                         pct_jump=100*(np.exp(r['jump_log'])-1)))
evd=pd.DataFrame(ev); evd.to_csv(os.path.join(D,'event_windows.csv'), index=False)
print(evd[['iso3','event_year','outcome','jump_log','se','t','pct_jump','n','pre_rms']].to_string())

# ---------- shadow-education gradients (observed cells only) ----------
g=[]
# HK 2003 gate gradient across stages (Bray & Kwok 2003, Table 1 p.616)
hk = {'S1-3':35.1,'S4-5':46.6,'S6-7':70.3}
for st,v in hk.items(): g.append(dict(country='HKG',year=2003,dimension='stage',level=st,value_pct=v,
    source='Bray & Kwok (2003) EER 22:611-620, Table 1 p.616',note='same survey, same schools: gate proximity'))
g.append(dict(country='HKG',year=2003,dimension='gate-gradient',level='S6-7 minus S1-3',
              value_pct=70.3-35.1, source='Bray & Kwok (2003) Table 1',note='+35.2pp at the senior gate'))
# Korea 2023 income gradient (MODS/KEDI 2023, monthly spend per student, thousand won)
for band,v in {'<3m won':183,'>=8m won':671}.items():
    g.append(dict(country='KOR',year=2023,dimension='income-band',level=band,value_pct=v,
                  source='MODS/KEDI 2023 English release, income table',note='thousand won/month per student (not %)'))
g.append(dict(country='KOR',year=2023,dimension='income-elasticity',level='>=8m vs <3m',
              value_pct=float(np.log(671/183)/np.log(8/3)), source='derived from MODS/KEDI 2023 income bands',
              note='elasticity of tutoring expenditure wrt household income (2.67x income gap -> 3.67x spend)'))
# Korea 2023 level gradient: participation falls, spend per student rises
g.append(dict(country='KOR',year=2023,dimension='level-participation',level='elementary',value_pct=86.0,
              source='MODS/KEDI 2023 Table 2',note=''))
g.append(dict(country='KOR',year=2023,dimension='level-participation',level='high',value_pct=66.4,
              source='MODS/KEDI 2023 Table 2',note='-19.6pp from elementary to high'))
g.append(dict(country='KOR',year=2023,dimension='level-spend',level='elementary',value_pct=398,
              source='MODS/KEDI 2023 Table 2',note='thousand won/month per student'))
g.append(dict(country='KOR',year=2023,dimension='level-spend',level='high',value_pct=491,
              source='MODS/KEDI 2023 Table 2',note='+23% spend per student at the high-school gate'))
# Japan prefecture urban gradient 2018 (Rappleye & Komatsu 2020)
g.append(dict(country='JPN',year=2018,dimension='urbanisation',level='Tokyo (max)',value_pct=57.9,
              source='Rappleye & Komatsu (2020) EPAA 28(67), Table 2',note=''))
g.append(dict(country='JPN',year=2018,dimension='urbanisation',level='Akita (min)',value_pct=22.1,
              source='Rappleye & Komatsu (2020) EPAA 28(67), Table 2',note='2.6x urban/rural gap'))
# Cambodia urban/rural grade 6 (Brehm & Silova case study, 6 schools)
g.append(dict(country='KHM',year=2012,dimension='urbanisation',level='urban grade 6',value_pct=60.5,
              source='Brehm & Silova (2013 WP39; 2014 JERO 6(1))',note='ONE DISTRICT, six schools - case study only'))
g.append(dict(country='KHM',year=2012,dimension='urbanisation',level='rural grade 6',value_pct=26.4,
              source='Brehm & Silova (2013/2014)',note='2.3x urban/rural gap, case study'))
# China 2014 -> 2022 policy collapse (Double Reduction)
g.append(dict(country='CHN',year=2014,dimension='policy',level='pre-Double-Reduction',value_pct=29.8,
              source='Liu & Bray (2020) Educational Studies 46(2):170-187 (ERIC abstract)',note='national survey 2014'))
g.append(dict(country='CHN',year=2022,dimension='policy',level='post-Double-Reduction (<20%)',value_pct=20.0,
              source='China Education Daily 2022-03-03 headline (LOW confidence)',note='upper bound of reported <20%'))
gd=pd.DataFrame(g); gd.to_csv(os.path.join(D,'shadow_gradients.csv'), index=False)
print('shadow gradient rows:', len(gd))
