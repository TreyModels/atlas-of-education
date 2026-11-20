"""State-capacity trajectory + alignment tests (task-36 capacity layer).
Index of state capacity from PUBLIC observed series with DECLARED weights; governance (WGI) component BLOCKED this
session (WDI API unreachable during the window) and declared as such. Capacity is an observed input series, never a
fitted parameter. All tests descriptive; no direction claims (R13).
Writes data/state_capacity.csv, data/capacity_alignment.csv, data/capacity_leadlag.csv.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.stats import spearmanr
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
W=pd.read_csv(os.path.join(BASE,'09_relations','data','panel_wdi_wide.csv'))
SIX=['PHL','KHM','CHN','HKG','KOR','JPN']
T=pd.read_csv(os.path.join(D,'UNIVERSALIZATION_TIMING.csv'))

# ---------------- components ----------------
W['ptr_p']=W['SE.PRM.ENRL.TC.ZS']; W['ptr_s']=W['SE.SEC.ENRL.TC.ZS']
W['teachers_pc']=1000.0*(W['SE.PRM.TCHR'].fillna(0)+W['SE.SEC.TCHR'].fillna(0))/W['SP.POP.TOTL'].replace(0,np.nan)
W['spend_gdp']=W['SE.XPD.TOTL.GD.ZS']; W['spend_budget']=W['SE.XPD.TOTL.GB.ZS']
W['tax_gdp']=W['GC.TAX.TOTL.GD.ZS']; W['xpn_gdp']=W['GC.XPN.TOTL.GD.ZS']
W['perstud_p']=W['SE.XPD.PRIM.PC.ZS']
COMP=[('spend_gdp','fiscal effort: education spending (%GDP)',0.15,1),
      ('spend_budget','fiscal priority: education (% of govt expenditure)',0.10,1),
      ('tax_gdp','revenue capacity: tax revenue (%GDP)',0.20,1),
      ('xpn_gdp','state size: govt expenditure (%GDP)',0.05,1),
      ('ptr_p','delivery: primary teachers per pupil (inverted PTR)',0.30,1),
      ('teachers_pc','delivery: teacher stock per 1,000 population',0.10,1),
      ('perstud_p','fiscal depth: primary spending per pupil (% of GDP pc)',0.10,1)]
# governance component BLOCKED
BLOCKED=[('GE.EST','governance/enforcement proxy: WGI government effectiveness',0.15)]
# robust fixed bounds from the whole 30-country panel (declared): 5th-95th percentile, clipped
BOUNDS={}
for c,lab,w,sign in COMP:
    s=W[c].dropna()
    lo=float(np.percentile(s,5)); hi=float(np.percentile(s,95))
    if c in ('ptr_p','ptr_s'):   # invert: lower PTR = better delivery
        BOUNDS[c]=(lo,hi,-1)
    else:
        BOUNDS[c]=(lo,hi,+1)
def norm(c,v):
    lo,hi,sg=BOUNDS[c]
    if pd.isna(v) or hi<=lo: return np.nan
    x=(float(v)-lo)/(hi-lo)
    if sg<0: x=1.0-x
    return float(np.clip(x,0,1))
rows=[]
for _,r in W.iterrows():
    comps={}
    for c,lab,w,sg in COMP:
        comps[c]=norm(c,r[c])
    avail=[(c,w) for c,lab,w,sg in COMP if not pd.isna(comps[c])]
    if not avail: continue
    tot_w=sum(w for _,w in avail)
    idx=sum(w*comps[c] for c,w in avail)/tot_w
    rows.append(dict(iso3=r.iso3,country=r.country,year=int(r.year),
        **{c:comps[c] for c,_,_,_ in COMP},
        capacity_index=round(100*idx,2), n_components=len(avail),
        weight_coverage=round(tot_w/sum(w for _,_,w,_ in COMP),3),
        ptr_primary_raw=r.ptr_p, spend_gdp_raw=r.spend_gdp, tax_gdp_raw=r.tax_gdp,
        teachers_total=(r['SE.PRM.TCHR'] if 'SE.PRM.TCHR' in W else np.nan),
        governance_available=False))
cap=pd.DataFrame(rows)
# add source/weights metadata as columns (machine-readable)
cap['weights_declared']=('fiscal 0.25 (spend_gdp .15, spend_budget .10); revenue .20; state size .05; '
                         'delivery .40 (ptr .30 inverted, teachers_pc .10); per-student .10; governance .15 BLOCKED')
cap.to_csv(os.path.join(D,'state_capacity.csv'),index=False)
print('capacity panel:',cap.shape,'| countries:',cap.iso3.nunique(),'| years:',int(cap.year.min()),'-',int(cap.year.max()))
print('six-country index (selected years):')
piv=cap[cap.iso3.isin(SIX)].pivot_table(index='year',columns='iso3',values='capacity_index')
print(piv.loc[[1970,1980,1990,2000,2010,2020]].round(1).to_string() if 1970 in piv.index else piv.head().round(1).to_string())

# ---------------- alignment with crossing years ----------------
al=[]
for iso in SIX:
    sub=cap[cap.iso3==iso].set_index('year').sort_index()
    for level in ['primary_universal','lower_secondary_universal','upper_secondary_mass','tertiary_mass']:
        h=T[(T.iso3==iso)&(T.level==level)]
        if len(h)==0: continue
        h=h.iloc[0]
        cy=h.crossing_mid if pd.notna(h.crossing_mid) else (h.crossing_hi if pd.notna(h.crossing_hi) else np.nan)
        # capacity at / around the crossing; censored rows use the upper bound year
        cy_use=cy if pd.notna(cy) else np.nan
        def at(y):
            if pd.isna(y): return np.nan
            s=sub.loc[(sub.index>=y-1)&(sub.index<=y+1),'capacity_index']
            return round(float(s.mean()),1) if len(s) else np.nan
        c_pre=at(cy_use-5); c_at=at(cy_use); c_post=at(cy_use+5)
        al.append(dict(iso3=iso,level=level,crossing_status=h.status,
            crossing_year_used=(cy_use if pd.notna(cy_use) else np.nan),
            capacity_5y_before=c_pre,capacity_at_crossing=c_at,capacity_5y_after=c_post,
            capacity_change_pre=(round(c_at-c_pre,1) if pd.notna(c_at) and pd.notna(c_pre) else np.nan),
            capacity_rising_before=('yes' if (pd.notna(c_at) and pd.notna(c_pre) and c_at>c_pre) else
                                   'no' if (pd.notna(c_at) and pd.notna(c_pre)) else 'unknown'),
            note=('censored: uses upper-bound year' if h.status!='crossed' else '')))
al=pd.DataFrame(al); al.to_csv(os.path.join(D,'capacity_alignment.csv'),index=False)
print('\nALIGNMENT (six countries x milestones):'); print(al.to_string(index=False))

# ---------------- lead-lag: does capacity lead completion? (5-year differences) ----------------
def spearman_lag(iso,capc,out,milestone):
    sub=cap[cap.iso3==iso][['year',capc]].dropna().sort_values('year').set_index('year')
    Wl=W[W.iso3==iso][['year',out]].dropna().sort_values('year').set_index('year')
    j=sub.join(Wl,how='inner').sort_index()
    if len(j)<15: return []
    d=j.diff(5).dropna()
    out_rows=[]
    for lag in range(-10,11,5):
        x=d[capc].shift(lag) if lag>=0 else d[capc].shift(lag)
        yv=d[out].shift(-lag) if lag>=0 else d[out].shift(-lag)
        m=x.notna()&yv.notna()
        if m.sum()<8: continue
        r=float(np.corrcoef(x[m],yv[m])[0,1])
        out_rows.append(dict(iso3=iso,milestone=milestone,driver=capc,outcome=out,lag_years=lag,
            r=round(r,3),n=int(m.sum()),
            reading=('capacity change LEADS completion change' if lag>0 else
                     'completion change LEADS capacity change' if lag<0 else 'contemporaneous')))
    return out_rows
ll=[]
for iso in SIX:
    ll+=spearman_lag(iso,'capacity_index','SE.PRM.CMPT.ZS','primary completion')
    ll+=spearman_lag(iso,'capacity_index','SE.SEC.CMPT.LO.ZS','lower-secondary completion')
ll=pd.DataFrame(ll)
if len(ll): ll.to_csv(os.path.join(D,'capacity_leadlag.csv'),index=False)
print('\nLEAD-LAG (5y differences, within country):')
if len(ll): print(ll.sort_values(['iso3','milestone','lag_years']).to_string(index=False))

# ---------------- cross-country: does capacity predict crossing timing? ----------------
cc=[]
for level in ['primary_universal','lower_secondary_universal','upper_secondary_mass','tertiary_mass']:
    xs=[]; ys=[]
    for iso in SIX:
        h=T[(T.iso3==iso)&(T.level==level)].iloc[0]
        cy=h.crossing_mid if pd.notna(h.crossing_mid) else h.crossing_hi
        if pd.isna(cy): continue
        c=cap[(cap.iso3==iso)&(cap.year>=1980)&(cap.year<=2000)]['capacity_index'].mean()
        if pd.isna(c): continue
        xs.append(float(c)); ys.append(float(cy))
    if len(xs)>=4:
        rho,p=spearmanr(xs,ys)
        cc.append(dict(level=level,n=len(xs),spearman_rho=round(float(rho),3),p=round(float(p),3),
            reading=('higher 1980-2000 capacity associates with EARLIER crossing' if rho<0 else
                     'higher capacity associates with LATER crossing' if rho>0 else 'no monotone association'),
            identification='DESCRIPTIVE; n<=6, capacity is endogenous to schooling demand and income; cannot identify'))
cc=pd.DataFrame(cc); cc.to_csv(os.path.join(D,'capacity_crosscountry.csv'),index=False)
print('\nCROSS-COUNTRY (capacity 1980-2000 vs crossing year):'); print(cc.to_string(index=False))

# ---------------- PHL narrative numbers ----------------
phl=cap[cap.iso3=='PHL'][['year','capacity_index','ptr_primary_raw','spend_gdp_raw','tax_gdp_raw']].dropna(subset=['ptr_primary_raw'])
print('\nPHL PTR path (observed):')
print(phl[phl.year.isin([1990,1995,2000,2005,2010,2015,2020,2024])].to_string(index=False))
