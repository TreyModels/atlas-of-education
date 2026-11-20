"""Panel + heterogeneity estimates for the relation register. Writes data/*.csv.
Two-way FE (country + year), CR1 SE clustered on country. Observed cells only."""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from panel_lib import load_panel, fe_ols

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'data'); os.makedirs(D, exist_ok=True)
d = load_panel()

# ---------- derived variables (logs; clipped only where a rate can be 0) ----------
def lg(col, eps=1e-3):
    return np.log(d[col].clip(lower=eps))
d['log_spend_gdp'] = lg('SE.XPD.TOTL.GD.ZS')
d['log_spend_gb']  = lg('SE.XPD.TOTL.GB.ZS')
d['log_gdppc']     = lg('NY.GDP.PCAP.KD')
d['log_ger_p']     = lg('SE.PRM.ENRR')
d['log_ger_s']     = lg('SE.SEC.ENRR')
d['log_ger_t']     = lg('SE.TER.ENRR')
d['log_ger_sup']   = lg('SE.SEC.ENRR.UP')
d['log_ptr_p']     = lg('SE.PRM.ENRL.TC.ZS')
d['log_ptr_s']     = lg('SE.SEC.ENRL.TC.ZS')
d['log_tch_p']     = lg('SE.PRM.TCHR')
d['log_tch_s']     = lg('SE.SEC.TCHR')
d['log_pup_p']     = lg('SE.PRM.ENRL')
d['log_remit']     = np.log(d['BX.TRF.PWKR.DT.GD.ZS'].clip(lower=1e-4))
d['log_priv_p']    = lg('SE.PRM.PRIV.ZS')
d['log_priv_s']    = lg('SE.SEC.PRIV.ZS')
d['log_priv_t']    = lg('SE.TER.PRIV.ZS')
d['log_tax_gdp']   = lg('GC.TAX.TOTL.GD.ZS')
d['log_xpn_gdp']   = lg('GC.XPN.TOTL.GD.ZS')
d['log_internet']  = lg('IT.NET.USER.ZS')
d['log_cmpt_p']    = lg('SE.PRM.CMPT.ZS')
d['log_cmpt_s']    = lg('SE.SEC.CMPT.LO.ZS')
d['log_uner_p']    = lg('SE.PRM.UNER.ZS')
d['log_agri']      = lg('SL.AGR.EMPL.ZS')
d['log_xpd_prim_pc'] = lg('SE.XPD.PRIM.PC.ZS')
d['voc_share']     = d['SE.SEC.ENRL.VO.ZS']
d['urb']           = d['SP.URB.TOTL.IN.ZS']
d['tfr']           = d['SP.DYN.TFRT.IN']
d['pop0014']       = d['SP.POP.0014.TO.ZS']
d['neet']          = d['SL.UEM.NEET.ZS']
d['uem1524']       = d['SL.UEM.1524.ZS']
d['growth']        = d['NY.GDP.MKTP.KD.ZG']
d['log_sec_durs']  = lg('SE.SEC.DURS')

SPECS = [
 # id, outcome, driver, lags, note
 ('S01','log_ger_s','log_spend_gdp',(0,5),'public education spending -> secondary GER'),
 ('S02','log_ger_p','log_spend_gdp',(0,5),'spending -> primary GER'),
 ('S03','log_ger_t','log_spend_gdp',(0,5),'spending -> tertiary GER'),
 ('S04','log_cmpt_s','log_spend_gdp',(0,5),'spending -> lower-sec completion'),
 ('S05','log_cmpt_p','log_spend_gdp',(0,5),'spending -> primary completion'),
 ('S06','log_uner_p','log_spend_gdp',(0,5),'spending -> out-of-school (should be negative)'),
 ('S07','log_ptr_p','log_spend_gdp',(0,5),'spending -> pupil-teacher ratio'),
 ('S08','log_ger_s','log_gdppc',(0,5),'income -> secondary GER (demand)'),
 ('S09','log_ger_t','log_gdppc',(0,5),'income -> tertiary GER'),
 ('S10','log_cmpt_s','log_gdppc',(0,5),'income -> completion'),
 ('S11','log_ger_s','urb',(0,5),'urbanisation -> secondary GER'),
 ('S12','log_cmpt_s','log_remit',(0,5),'remittances -> completion'),
 ('S13','log_cmpt_p','tfr',(0,5),'fertility -> completion (cohort competition)'),
 ('S14','log_ger_s','log_priv_s',(0,5),'private secondary share -> GER (supply vs crowd-out)'),
 ('S15','log_ger_t','log_priv_t',(0,5),'private tertiary share -> tertiary GER'),
 ('S16','log_ger_p','log_priv_p',(0,5),'private primary share -> primary GER'),
 ('S17','log_cmpt_s','log_ptr_p',(0,5),'pupil-teacher ratio -> completion (quality channel)'),
 ('S18','log_ger_p','log_tch_p',(0,5),'teacher supply -> primary GER'),
 ('S19','log_ger_s','log_tch_s',(0,5),'teacher supply -> secondary GER'),
 ('S20','log_ger_s','voc_share',(0,5),'vocational share -> GER'),
 ('S21','growth','log_ger_t',(10,15),'education -> growth (eps_ec proxy), 10y lag'),
 ('S22','growth','log_ger_s',(10,15),'secondary schooling -> growth, 10y lag'),
 ('S23','log_gdppc','urb',(0,),'urbanisation -> income'),
 ('S24','log_spend_gdp','log_tax_gdp',(0,),'fiscal space (tax/GDP) -> education spending'),
 ('S25','log_ger_s','neet',(0,5),'NEET (labour market) -> schooling demand'),
 ('S26','log_ger_s','log_internet',(0,5),'internet -> schooling demand'),
 ('S27','log_cmpt_s','log_spend_gb',(0,5),'education share of budget -> completion'),
 ('S28','log_ger_s','log_xpd_prim_pc',(0,5),'per-pupil primary spending -> secondary GER (spillover/quality)'),
 ('S29','log_cmpt_p','log_agri',(0,5),'agricultural employment (child labour opportunity cost) -> completion'),
 ('S30','log_ger_s','log_sec_durs',(0,),'structural duration (K-12) -> GER accounting'),
]

rows = []
for sid, y, x, lags, note in SPECS:
    for kl in lags:
        if y not in d or x not in d: continue
        r = fe_ols(d, y, [x], lags={x: kl} if kl else None)
        base = dict(spec=sid, outcome=y, driver=x, lag_years=kl, note=note)
        if 'error' in r:
            rows.append({**base, 'error': r['error']}); continue
        rows.append({**base, 'coef': r[x]['coef'], 'se': r[x]['se'], 't': r[x]['t'], 'p': r[x]['p'],
                     'n': r['n'], 'n_cty': r['n_cty'], 'period': r['period'],
                     'within_r2': r['r2_within'], 'spec_type': 'levels-two-way-FE'})
# first differences (kills slow country trends)
FD = [('S01','log_ger_s','log_spend_gdp'),('S02','log_ger_p','log_spend_gdp'),('S04','log_cmpt_s','log_spend_gdp'),
      ('S08','log_ger_s','log_gdppc'),('S11','log_ger_s','urb'),('S17','log_cmpt_s','log_ptr_p'),
      ('S18','log_ger_p','log_tch_p'),('S24','log_spend_gdp','log_tax_gdp'),('S26','log_ger_s','log_internet')]
for sid, y, x in FD:
    r = fe_ols(d, y, [x], diff=True)
    base = dict(spec=sid+'-FD', outcome='d.'+y, driver='d.'+x, lag_years=0,
                note='first differences (removes country-specific trends)')
    if 'error' in r: rows.append({**base,'error':r['error']}); continue
    rows.append({**base, 'coef': r[x]['coef'], 'se': r[x]['se'], 't': r[x]['t'], 'p': r[x]['p'],
                 'n': r['n'], 'n_cty': r['n_cty'], 'period': r['period'],
                 'within_r2': r['r2_within'], 'spec_type': 'first-difference'})
res = pd.DataFrame(rows)
res.to_csv(os.path.join(D,'panel_results.csv'), index=False)
print(res.to_string(max_rows=100))
