from common import *
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
import argparse

def evaluate_job(job):
 f,theta,scale,seed,n,mode=job
 land=pd.read_csv(P/'data/train_land.csv')
 if mode=='conditional':
  future=pd.read_csv(P/'data/holdout_land.csv');land=pd.concat([land,future],ignore_index=True)
 rows,_=simulate(theta,f,seed,end=2025,n=n,mode=mode,driver_records=land)
 return dict(family=f,seed=seed,agents=n,mode=mode,prediction=[r['cases_filed_civilian']*scale*(12500/n) for r in rows if r['year']>=2020],latent=[r['true_misconduct'] for r in rows if r['year']>=2020])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=6);a=ap.parse_args()
 fits=json.loads((P/'results/frozen_fits.json').read_text()); assert fits['source_hashes']==source_hashes()
 best={f:min((r for r in fits['selected'] if r['family']==f),key=lambda r:r['log_rmse']) for f in FAMILIES}
 jobs=[(f,r['theta'],r['scale'],seed,n,mode) for f,r in best.items() for seed in range(3101,3105) for n in (12500,50000) for mode in ('strict','conditional')]
 with ProcessPoolExecutor(max_workers=a.workers) as pool: out=list(pool.map(evaluate_job,jobs))
 actual=pd.read_csv(P/'data/holdout_cases.csv').value.to_numpy();train=pd.read_csv(P/'data/train_cases.csv').value.to_numpy();years=np.arange(2013,2020)
 forecasts={'last_value':np.repeat(train[-1],6),'log_linear':np.exp(np.polyval(np.polyfit(years,np.log(train),1),np.arange(2020,2026)))}
 summary=[]
 for name,v in forecasts.items():summary.append(dict(model=name,agents=None,mode='strict',**score(actual,v)))
 for f in FAMILIES:
  for n in (12500,50000):
   for mode in ('strict','conditional'):
    group=[x for x in out if x['family']==f and x['agents']==n and x['mode']==mode];pred=np.mean([x['prediction'] for x in group],axis=0)
    summary.append(dict(model=f,agents=n,mode=mode,**score(actual,pred)))
 atomic(P/'results/holdout_runs.json',out);pd.DataFrame(summary).to_csv(P/'results/holdout_scores.csv',index=False)
 print(pd.DataFrame(summary).to_string(index=False))
if __name__=='__main__':main()
