"""Re-fit the six-country curves from data-hunter's UNIVERSALIZATION_SERIES.csv and compare with my GMR-observed fits.
Before/after table for the NEW post. Observed/derived only; status=check (gross-intake proxies) excluded.
"""
import os, warnings
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
warnings.filterwarnings('ignore')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'data'); BASE=os.path.abspath(os.path.join(ROOT,'..','..'))
def logistic(t,K,r,t0): return K/(1+np.exp(-r*(t-t0)))
def gompertz(t,K,r,t0): return K*np.exp(-np.exp(-r*(t-t0)))
def fit(shape,t,y,cap):
    hi=float(np.max(y)); lo=[max(hi,1.0),0.005,t.min()-30]; up=[max(cap,hi*1.02),1.5,t.max()+30]; best=None
    for K0 in [hi,hi+0.1*(up[0]-hi),hi+0.4*(up[0]-hi)]:
        for r0 in (0.03,0.06,0.12,0.25):
            for t0 in (np.median(t)-10,np.median(t),np.median(t)+10):
                try: p,_=curve_fit(shape,t,y,p0=[min(max(K0,lo[0]+1e-6),up[0]-1e-6),r0,t0],bounds=(lo,up),maxfev=20000)
                except Exception: continue
                sse=float(np.sum((y-shape(t,*p))**2))
                if best is None or sse<best[0]: best=(sse,p,_)
    if best is None: return None
    sse,p,cov=best; se=np.sqrt(np.diag(cov)); n=len(t)
    return dict(K=p[0],K_se=se[0],r=p[1],r_se=se[1],t0=p[2],t0_se=se[2],
                rmse=float(np.sqrt(sse/n)),r2=1-sse/max(float(np.sum((y-y.mean())**2)),1e-12),n=n)
u=pd.read_csv(os.path.join(BASE,'10_massification','data','UNIVERSALIZATION_SERIES.csv'))
print('UNI series indicators:'); print(u.groupby(['indicator','level','measure','status']).size().to_string())
