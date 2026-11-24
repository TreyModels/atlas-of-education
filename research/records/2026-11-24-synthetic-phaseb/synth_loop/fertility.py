"""Minimal birth-history layer (Phase B): education -> birth hazard, child mortality, replacement."""
import numpy as np
PARAMS={"P":(0.42,0.06,0.10,1.8),"S":(0.34,0.08,0.08,1.6),"C":(0.30,0.10,0.06,1.5),"R":(0.38,0.05,0.09,1.7)}
NULL=tuple(float(np.mean([PARAMS[w][i] for w in PARAMS])) for i in range(4))
WOMEN=400; AGES=25

def simulate(world, s, seed, ger_post, cl_post):
    lam0,beta,mort,rho = NULL if s==0 else PARAMS[world]
    rng=np.random.default_rng(int(seed)+7373)
    p8=np.clip(ger_post,0,0.9); p12=np.clip(0.3*ger_post,0,1-p8); p0=1-p8-p12
    e=rng.choice([0,8,12],size=WOMEN,p=[max(p0,0),p8,p12])
    ee=np.exp(-beta*e/8.0); mu=mort*np.exp(-0.3*e/8.0)
    parity=np.zeros(WOMEN,int); last_birth=np.full(WOMEN,np.nan); recent=np.zeros(WOMEN,int)
    first_age=np.full(WOMEN,np.nan); intervals=[]; post_death=[]; ceb=np.zeros(WOMEN,int)
    for t in range(AGES):
        age=15+t
        hz=lam0*ee*(1-0.10*parity)*np.where(recent>0,rho,1.0)
        birth=rng.random(WOMEN)<np.minimum(hz,0.95)
        # death of any existing child this year (approximation: at most one death event/woman/year)
        death=(rng.random(WOMEN)<mu)&(parity>0)
        nb=birth&(~np.isnan(last_birth))
        intervals.append(np.where(nb, age-last_birth, np.nan))
        post_death.append(nb&(recent>0))
        first_age=np.where(birth&np.isnan(first_age),age,first_age)
        last_birth=np.where(birth,age,last_birth)
        parity=parity+birth.astype(int); ceb=ceb+birth.astype(int)
        recent=np.where(death,2,np.maximum(recent-1,0))
    I=np.concatenate([x for x in intervals]); PD=np.concatenate([x for x in post_death])
    ok=~np.isnan(I); I=I[ok]; PD=PD[ok]
    b1=float(np.mean(I[PD])-np.mean(I[~PD])) if PD.sum()>=5 and (~PD).sum()>=5 else 0.0
    low=e<=8; high=e==12
    def ppr(mask):
        d=np.sum((parity>=1)&mask); n=np.sum((parity>=2)&mask); return float(n/d) if d>0 else np.nan
    b2=float((ppr(low) if not np.isnan(ppr(low)) else 0)-(ppr(high) if not np.isnan(ppr(high)) else 0))
    b3=float((np.nanmean(first_age[high]) if high.sum()>0 else 0)-(np.nanmean(first_age[low]) if low.sum()>0 else 0))
    return {"B1":b1,"B2":b2,"B3":b3,"mean_ceb":float(ceb.mean()),"ger_post":float(ger_post),"cl_post":float(cl_post)}
