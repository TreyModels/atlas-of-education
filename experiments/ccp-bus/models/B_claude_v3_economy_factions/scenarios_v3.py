"""2026-2041 scenarios on the posterior ensemble (all pattern-passing parameter sets, 2 seeds each)."""
import numpy as np, pandas as pd
from dataclasses import replace
from multiprocessing import Pool
import bus_v3 as W
PAR=list(__import__('calibrate_v3').PRIOR)
post=pd.read_csv('abc_v3_C_rounds.csv')
post=post[post.x2012.between(.05,.6)&(post.rr_core_tgt<.3)&(post.contagion_hr>=1.5)&(post.hidden2025>=.1)&post.p5.astype(bool)&(post.political_share<.5)]
S3=W.Scenario3
SCEN={
 'Muddle through: land flat, credit rollover':S3(),
 'Land keeps falling':S3(land_growth=-0.08,land_floor=1.5),
 'Deleveraging: land falls, credit to 12% of GDP':S3(land_growth=-0.08,land_floor=1.5,credit_flow=12,credit_by=2030),
 'Stimulus: credit to 30% of GDP':S3(credit_flow=30,credit_by=2028),
 'Succession 2032, new leader purges old network':S3(land_growth=-0.08,land_floor=1.5,succession=2032),
 'Post-2031 relaxation, no succession purge':S3(land_growth=-0.08,land_floor=1.5,e_after=0.25,xi_after=0.0),
 'Defense growth slows to 4% a year':S3(land_growth=-0.08,land_floor=1.5,defense_growth=0.04),
 'Off-budget procurement adds 50%':S3(land_growth=-0.08,land_floor=1.5,off_budget=1.5),
}
def run(args):
    k,row,seed,name=args
    p=replace(W.P3(),**{c:float(row[c]) for c in PAR})
    d=W.simulate3(p,seed,SCEN[name],end=2041); d['scenario']=name; d['draw']=k; d['seed']=seed; return d
if __name__=='__main__':
    jobs=[(k,r,s,n) for k,(_,r) in enumerate(post.iterrows()) for s in (1,2) for n in SCEN]
    with Pool(2) as pool: out=pd.concat(pool.map(run,jobs,chunksize=2))
    out.to_csv('scenarios_v3.csv',index=False)
    pd.set_option('display.width',250)
    t=out[out.year.isin([2025,2030,2035,2041])].groupby(['scenario','year'])[['x','pred_share','x_land','x_fin','x_pla','hidden_share','core_share','n_factions']].median().round(3)
    print(t.to_string())
    print(out[out.year.isin([2031,2032,2033,2035])&out.scenario.str.startswith('Succession')].groupby('year')[['cases_civ','political_share','rem_core','rem_targeted','core_share']].median().round(3))
