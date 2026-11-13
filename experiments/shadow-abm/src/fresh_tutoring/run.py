import json,csv,argparse,os
from dataclasses import replace
from multiprocessing import Pool
import numpy as np
from model import World
from calibrate import distances
from smc import to_params

def task(a):
 variant,idx,names,vec,seed,rep=a;p=to_params(names,vec)
 b=World(p,seed).solve().outcomes();t=World(replace(p,ban_own=True),seed).solve().outcomes()
 return [variant,idx,rep,seed,max(distances(b).values()),int(max(distances(b).values())<=1),int(b['converged']),b['participation'],b['withholding_mean'],t['participation']-b['participation'],t['nonbuyer_class_instruction']-b['nonbuyer_class_instruction']]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--particles',type=int,default=40);ap.add_argument('--worlds',type=int,default=5);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--out',default='results');a=ap.parse_args();os.makedirs(a.out,exist_ok=True);rng=np.random.default_rng(118013);jobs=[]
 for variant in ('thin','diversion','favour','full'):
  d=json.load(open('source_results/posterior_'+variant+'.json'));arr=d['particles'];w=np.array([x['weight'] for x in arr]);w=w/w.sum();ix=rng.choice(len(arr),a.particles,replace=True,p=w)
  for particle in ix:
   x=arr[particle];vec=[float(x[k]) for k in d['free']]
   for j in range(a.worlds):jobs.append((variant,int(particle),d['free'],vec,9700000+j,j))
 if a.workers==1:rows=list(map(task,jobs))
 else:
  with Pool(a.workers) as pool:rows=list(pool.imap(task,jobs,chunksize=2))
 with open(a.out+'/draws.csv','w',newline='') as f:w=csv.writer(f);w.writerow(['variant','particle_index','world','seed','max_distance','fit','converged','participation','withholding','ban_delta_participation','ban_delta_nonbuyer_instruction']);w.writerows(rows)
 with open(a.out+'/summary.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['variant','n_particle_draws','n_worlds','fits_share','converged_share','median_max_distance','ban_participation_median','ban_instr_median','ban_instr_p05','ban_instr_p95'])
  for variant in ('thin','diversion','favour','full'):
   z=[x for x in rows if x[0]==variant];v=np.array([x[10] for x in z]);w.writerow([variant,a.particles,a.worlds,np.mean([x[5] for x in z]),np.mean([x[6] for x in z]),np.median([x[4] for x in z]),np.median([x[9] for x in z]),np.median(v),*np.quantile(v,[.05,.95])])
 print('Completed',len(rows),'fresh world pairs')
if __name__=='__main__':main()
