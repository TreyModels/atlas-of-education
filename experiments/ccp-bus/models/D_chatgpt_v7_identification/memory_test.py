from common import *
from concurrent.futures import ProcessPoolExecutor
import argparse

def run(job):
 family,theta,seed=job;paths=[]
 for initial in (.05,.95):
  w=World(params(theta,family),seed);w.evidence=LandDriver(pd.read_csv(P/'data/train_land.csv'));w.force_effort=.55
  w.state=w.rng['init'].random(w.O)<initial
  rows=[w.step('campaign',2019) for _ in range(80)]
  paths.append([r['true_misconduct'] for r in rows])
 return dict(family=family,seed=seed,low=paths[0],high=paths[1],gap_1=paths[1][0]-paths[0][0],gap_10=paths[1][9]-paths[0][9],gap_30=paths[1][29]-paths[0][29],gap_60=paths[1][59]-paths[0][59])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=6);a=ap.parse_args();fits=json.loads((P/'results/frozen_fits.json').read_text())
 best={f:min((r for r in fits['selected'] if r['family']==f),key=lambda r:r['log_rmse']) for f in FAMILIES}
 jobs=[(f,best[f]['theta'],seed) for f in FAMILIES for seed in range(4101,4105)]
 with ProcessPoolExecutor(max_workers=a.workers) as pool:r=list(pool.map(run,jobs))
 atomic(P/'results/memory_runs.json',r);print(pd.DataFrame(r).groupby('family')[['gap_1','gap_10','gap_30','gap_60']].mean().to_string())
if __name__=='__main__':main()
