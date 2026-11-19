"""bus_mm.py — a minimal many-model family for the "bus" hypothesis.

ODD summary (Grimm et al. 2020)
-------------------------------
Purpose. Discriminate between three mechanism families for persistent cadre corruption:
  A  Principal-agent / Markov: an official's choice depends only on current deterrence.
     History cannot matter in the long run (Markov convergence; Page, Model Thinking).
  B  Social trap: strategic complementarities -- peer norms/complicity (h), detection that
     depends on honest peers reporting (phi; Andvig & Moene 1990) and finite enforcement
     capacity (kappa; Lui 1986). Can produce multiple equilibria and hysteresis.
  C  Bus: B plus sponsored entry (rho) that selects pliable clients (delta) and wires them into
     the sponsor's circle, plus threat-driven rewiring of corrupt officials toward each other
     ("trust chains"; Ruan, Lu & Ruan 2026; Baker & Faulkner 1993).
Entities. N officials on an undirected tie network. State: corrupt (0/1), integrity theta,
  entry route (sponsored / open), tenure.
Process (one step = one year, synchronous):
  1. m_i = share of i's ties that were corrupt last year; x = population share corrupt.
  2. Detection risk D_i = e * ((1-phi) + phi*(1-m_i)) * min(1, kappa/x).
  3. Choose corrupt with prob sigmoid((r - theta_i + h*m_i - F*D_i)/tau).
  4. Corrupt officials are detected with prob D_i and removed (purged).
  5. Officials retire with prob 1/T. Vacancies are filled by entrants:
     sponsored (prob rho): theta ~ N(-delta,1); tie to a sponsor (chosen with weight 1+lam*corrupt)
     and to that sponsor's ties (triadic closure). Open entry: theta ~ N(0,1), random ties.
  6. Rewiring: each undetected corrupt official, with prob w*e, drops a tie to an honest
     neighbour and adds a tie to a corrupt friend-of-a-friend (or any corrupt official).
Mechanism switches: A = h=phi=0, kappa=1, rho=0, w=0;  B = A + h,phi,kappa;  C = B + rho,delta,w.
Every parameter is a hypothesis to be estimated, not a fact. Synthetic; not calibrated to China.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, replace, asdict
from scipy import sparse

@dataclass(frozen=True)
class Params:
    N:int=1000; k_new:int=4           # each entrant creates k_new ties -> mean degree ~ 2*k_new
    r:float=-0.6; tau:float=0.35; F:float=6.0
    h:float=0.0; phi:float=0.0; kappa:float=1.0
    rho:float=0.0; delta:float=0.0; lam:float=2.0; w:float=0.0
    e:float=0.35; T:float=25.0
    mixing:str='network'              # 'network' or 'global' (mean-field docking)
    removal:bool=True                 # False: sanction without removal (docking variant)

MODEL_A=Params()
MODEL_B=replace(MODEL_A,h=1.0,phi=0.6,kappa=0.04)
MODEL_C=replace(MODEL_B,rho=0.7,delta=0.5,w=0.3)
MODELS={'A: principal-agent':MODEL_A,'B: social trap':MODEL_B,'C: bus':MODEL_C}

def sig(z): return 1/(1+np.exp(-np.clip(z,-40,40)))

class World:
    def __init__(self,p:Params,seed:int,x0:float|None=None):
        self.p=p; self.rng=np.random.default_rng(seed); N=p.N; rng=self.rng
        self.nbr=[set() for _ in range(N)]
        for i in range(N):
            for j in rng.choice(N,p.k_new,replace=False):
                if j!=i: self.nbr[i].add(int(j)); self.nbr[int(j)].add(i)
        self.sponsored=rng.random(N)<p.rho
        self.theta=rng.normal(0,1,N)-p.delta*self.sponsored
        self.s=np.zeros(N,bool) if x0 is None else rng.random(N)<x0
        self.t=0; self.cum_purged=0

    def adj(self):
        rows=np.repeat(np.arange(self.p.N),[len(n) for n in self.nbr])
        cols=np.fromiter((j for n in self.nbr for j in n),int,count=len(rows))
        return sparse.csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(self.p.N,self.p.N))

    def step(self,p:Params|None=None):
        p=p or self.p; rng=self.rng; N=p.N
        A=self.adj(); deg=np.asarray(A.sum(1)).ravel(); x=self.s.mean()
        m=(A@self.s.astype(float))/np.maximum(deg,1) if p.mixing=='network' else np.full(N,x)
        D=p.e*((1-p.phi)+p.phi*(1-m))*min(1.0,p.kappa/max(x,1e-3))
        s=rng.random(N)<sig((p.r-self.theta+p.h*m-p.F*D)/p.tau)
        detected=s&(rng.random(N)<D)
        # co-offending assortativity: P(both ends corrupt)/x^2 over ties
        rows,cols=A.nonzero(); xc=s.mean()
        assort=(s[rows]&s[cols]).mean()/max(xc**2,1e-9) if len(rows) else np.nan
        stats=dict(t=self.t,x=xc,detected=detected.mean(),assort=assort,
                   theta=self.theta.mean(),sponsored_share=self.sponsored.mean(),
                   x_sponsored=s[self.sponsored].mean() if self.sponsored.any() else np.nan,
                   x_open=s[~self.sponsored].mean() if (~self.sponsored).any() else np.nan,
                   mean_deg=deg.mean())
        self.s=s
        # rewiring toward trust chains (before vacancies)
        if p.w>0 and p.e>0:
            movers=np.flatnonzero(s&~detected&(rng.random(N)<p.w*p.e))
            corrupt_ids=np.flatnonzero(s)
            for i in movers:
                honest=[j for j in self.nbr[i] if not s[j]]
                if not honest: continue
                fof={k for j in self.nbr[i] if s[j] for k in self.nbr[j] if s[k]}-self.nbr[i]-{i}
                cand=list(fof) if fof else [int(c) for c in corrupt_ids if c!=i and c not in self.nbr[i]]
                if not cand: continue
                drop=honest[rng.integers(len(honest))]; add=cand[rng.integers(len(cand))]
                self.nbr[i].discard(drop); self.nbr[drop].discard(i)
                self.nbr[i].add(add); self.nbr[add].add(i)
        vac=(rng.random(N)<1/p.T)|(detected if p.removal else np.zeros(N,bool))
        self.cum_purged+=int(detected.sum()) if p.removal else 0
        idx=np.flatnonzero(vac)
        for i in idx:                       # clear ties of departing officials
            for j in self.nbr[i]: self.nbr[j].discard(i)
            self.nbr[i]=set()
        stay=np.flatnonzero(~vac); w8=1+p.lam*self.s[stay]
        for i in idx:
            spons=rng.random()<p.rho
            self.sponsored[i]=spons; self.theta[i]=rng.normal(-p.delta if spons else 0,1); self.s[i]=False
            if spons and len(stay):
                j=int(rng.choice(stay,p=w8/w8.sum()))
                circle=[q for q in self.nbr[j] if q!=i]
                pick=[j]+list(rng.choice(circle,min(p.k_new-1,len(circle)),replace=False)) if circle else [j]
            else: pick=[]
            while len(pick)<p.k_new:
                q=int(rng.integers(N))
                if q!=i and q not in pick: pick.append(q)
            for q in pick: self.nbr[i].add(int(q)); self.nbr[int(q)].add(i)
        self.t+=1
        stats['purged']=int(detected.sum()) if p.removal else 0
        return stats

def run(p:Params,seed:int,schedule,x0=0.5,burn=100):
    """schedule: function t->Params for t>=0 after burn-in at p."""
    w=World(p,seed,x0=x0)
    for _ in range(burn): w.step(p)
    out=[]; t=0
    for q in schedule:
        out.append(w.step(q)); t+=1
    return out,w
