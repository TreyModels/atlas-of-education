"""Round 2 (sequential ABC): sample model C from the region of round-1 pattern-passers (box widened 50%),
and add P6: most removals are of actually corrupt officials (political share < 0.5; Lorentzen & Lu)."""
import numpy as np, pandas as pd
from multiprocessing import Pool
import calibrate_v3 as C
df=pd.read_csv('abc_v3_all.csv')
ok=df[(df.model=='C')&df.x2012.between(.05,.6)&(df.rr_core_tgt<.3)&(df.contagion_hr>=1.5)&(df.hidden2025>=.1)&df.p5]
box={}
for k,(lo,hi) in C.PRIOR.items():
    a,b=ok[k].min(),ok[k].max(); w=(b-a)*0.5+1e-9; box[k]=(max(lo,a-w),min(hi,b+w))
if __name__=='__main__':
    rng=np.random.default_rng(11)
    jobs=[('C',1000+i,{k:float(rng.uniform(*v)) for k,v in box.items()}) for i in range(400)]
    with Pool(2) as pool: res=pd.DataFrame(pool.map(C.evaluate,jobs,chunksize=3))
    all_=pd.concat([df[df.model=='C'],res]); all_.to_csv('abc_v3_C_rounds.csv',index=False)
    P=lambda d:(d.x2012.between(.05,.6)&(d.rr_core_tgt<.3)&(d.contagion_hr>=1.5)&(d.hidden2025>=.1)&d.p5.astype(bool)&(d.political_share<.5))
    ok2=all_[P(all_)]
    print('round-2 draws passing P0-P6:',int(P(res).sum()),'of',len(res),'| total passers:',len(ok2))
    tol=ok2.dist.quantile(0.5); acc=ok2[ok2.dist<=tol]; acc.to_csv('abc_v3_accepted.csv',index=False)
    print(f'accepted: {len(acc)} (tol {tol:.3f}); best distance {ok2.dist.min():.3f}')
    cols=['auc_faction','auc_corrupt','auc_degree','auc_hidden','rr_tgt_vs_rest','rr_corrupt','rr_core_tgt','contagion_hr','political_share','hidden2025','x2012','x2025']
    print(acc[cols].quantile([.1,.5,.9]).T.round(3))
    print('runs where faction beats corruption as a predictor (AUC):',round((acc.auc_faction>acc.auc_corrupt).mean(),2))
    print(acc[list(C.PRIOR)].quantile([.1,.5,.9]).T.round(3))
