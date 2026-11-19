"""Shared simulator and train-only observation mapping for V7."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
from pathlib import Path
from dataclasses import asdict
import hashlib,json
import numpy as np
import pandas as pd
from model import Params,World
from memory import configure,FAMILIES
from evidence import LandDriver
P=Path(__file__).resolve().parent
BOUNDS=dict(rent=(-1.6,1.2),ramp_years=(1.,10.),nsc_multiplier=(1.,2.),peer=(0.,4.),report_capture=(0.,.85))

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def atomic(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_suffix('.tmp')
    temp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');temp.replace(path)
def source_hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.glob('*.py')) if p.name in ('common.py','model.py','memory.py','tilly.py','evidence.py','observation.py','fit.py')}
def candidates(n=64):
    rng=np.random.default_rng(70261118);u={k:(rng.permutation(n)+rng.random(n))/n for k in BOUNDS}
    return [{k:float(lo+(hi-lo)*u[k][i]) for k,(lo,hi) in BOUNDS.items()} for i in range(n)]
def params(theta,family,n=12500):
    org=16 if n==12500 else 64 if n==50000 else None
    if org is None:raise ValueError('Use 12500 or 50000; both have 625 official seats per organization')
    p=Params(n=n,organizations=org,capacity=.025,temperature=.35,**theta)
    return configure(p,family)
def simulate(theta,family,seed,end=2019,n=12500,mode='strict',driver_records=None):
    p=params(theta,family,n);w=World(p,seed)
    if driver_records is None:driver_records=pd.read_csv(P/'data/train_land.csv')
    w.evidence=LandDriver(driver_records,mode)
    for _ in range(30):w.step('campaign',1998)
    rows=[w.step('campaign',year) for year in range(1998,end+1)]
    return rows,list(w.cohort.values())
def profile(obs,sim):
    # Scale is fitted on training observations only. It is not a known population ratio.
    a=np.asarray(obs,float);b=np.maximum(np.asarray(sim,float),.5)
    logscale=float(np.mean(np.log(a)-np.log(b)));residual=np.log(b)+logscale-np.log(a)
    return dict(scale=float(np.exp(logscale)),log_rmse=float(np.sqrt(np.mean(residual**2))))
def score(actual,predicted):
    a=np.asarray(actual,float);b=np.maximum(np.asarray(predicted,float),1e-9)
    return dict(log_rmse=float(np.sqrt(np.mean((np.log(b)-np.log(a))**2))),mae=float(np.mean(abs(b-a))),rmse=float(np.sqrt(np.mean((b-a)**2))))
