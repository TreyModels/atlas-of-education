"""Interrupted-time-series event windows on the OBSERVED 6-country GMR panel (1970-2024)."""
import os, numpy as np, pandas as pd
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G=pd.read_csv(os.path.join(ROOT,'..','04_data','data','gmr_observed_6countries_1970_2024.csv'))
def its(ind, iso, event, pre=10, post=8):
    s=G[(G.iso3==iso)&(G.indicator==ind)][['year','value']].dropna().sort_values('year')
    s=s[(s.year>=event-pre)&(s.year<=event+post)]
    if len(s)<pre+3: return None
    lv=np.log(s.value.clip(lower=1e-3).values)
    tr=(s.year-event).values; po=(s.year>=event).astype(int).values
    X=np.column_stack([np.ones(len(s)),tr,po]); b,*_=np.linalg.lstsq(X,lv,rcond=None)
    e=lv-X@b; dof=max(len(s)-3,1); se=np.sqrt(np.diag(np.linalg.pinv(X.T@X)*(e@e/dof)))
    return dict(iso3=iso,event_year=event,indicator=ind,jump_log=float(b[2]),se=float(se[2]),
                t=float(b[2]/se[2]),pct_jump=100*(np.exp(b[2])-1),n=len(s),
                pre_rms=float(np.sqrt(np.mean(e[po==0]**2))),
                y_pre=float(np.exp(np.mean(lv[po==0]))),y_post=float(np.exp(np.mean(lv[po==1]))))
EV=[('PHL',2016,'ger_upper_secondary','RA 10533 K-12: Grade 11-12 added to upper secondary'),
    ('PHL',2016,'ger_secondary','RA 10533 K-12 (secondary GER accounting shift)'),
    ('PHL',2018,'ger_tertiary','RA 10931 free SUC tuition'),
    ('PHL',2013,'ger_secondary','RA 10533 signed Jan 2013 (anticipation)'),
    ('HKG',1978,'ger_secondary','HK 9-year free compulsory education (1978)'),
    ('HKG',1971,'ger_secondary','HK 6-year free compulsory primary (1971)'),
    ('KOR',1974,'ger_secondary','Korea high-school equalisation (1974)'),
    ('KOR',1985,'ger_tertiary','Korea tertiary expansion mid-1980s'),
    ('JPN',1980,'ger_tertiary','Japan tertiary expansion 1980s'),
    ('CHN',1986,'ger_secondary','China Compulsory Education Law (1986)'),
    ('KHM',1996,'ger_secondary','Cambodia post-conflict reconstruction (1996)'),
    ('KHM',2001,'ger_secondary','Cambodia Education Law 2001 / EFA plan')]
rows=[]
for iso,yr,ind,lab in EV:
    r=its(ind,iso,yr)
    if r: rows.append({**r,'event':lab})
out=pd.DataFrame(rows)
out.to_csv(os.path.join(ROOT,'data','event_windows_gmr.csv'),index=False)
print(out[['iso3','event_year','indicator','jump_log','se','t','pct_jump','n','y_pre','y_post','pre_rms']].round(3).to_string(index=False))
