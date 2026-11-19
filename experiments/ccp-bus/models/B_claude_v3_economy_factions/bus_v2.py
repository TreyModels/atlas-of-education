"""bus_v2.py — the bus model with memory, a real economic engine, sectors and factions.

ODD summary (Grimm et al. 2020)
-------------------------------
Purpose. Ask how China's credit boom and land-finance collapse interact with enforcement, factional
protection and network memory to shape corruption, 1998-2041. Compare a memoryless model (A) with a
memory model (C) under identical economic inputs and calibration targets.

Entities. N officials in four sectors (seats keep their sector):
  land      land & construction (local land-finance officials)
  finance   finance & SOEs (credit allocation, rollovers)
  pla       PLA & defence procurement (separate discipline system; not in CCDI counts)
  admin     general administration
Each official: integrity theta, faction (0 = the leader's faction), entry route, corrupt state.
Ties cluster within factions (p_in) and, for sponsored entrants, within the sponsor's circle.

Economic engine (exogenous, from data/china_series.csv, then scenario paths to 2041):
  one rule        r_s = r0 + beta*ln(discretionary flow per official), common elasticity beta across sectors
  land            land-sale revenue as % of GDP (MOF series; peak 8.3% in 2020)
  finance         share c_fin of new credit as % of GDP (BIS total credit; Wright's credit boom)
  pla             equipment procurement as % of GDP = official defense budget x equipment share (white papers)
  fiscal gap      land revenue below sticky spending commitments (adjust 10%/yr) -> predatory extraction
                  ("deep-sea fishing", fines) available to land and admin officials
Rent (logit units): r_s,t = r0 + sector terms below.

Each year (synchronous):
  1. m_i = corrupt share of ties; x = corrupt share overall (non-PLA; PLA uses its own x).
  2. Detection D_i = e_s,t * ((1-phi) + phi*(1-m_i)) * min(1, kappa_t/x) * (1 - xi_t*[faction 0]).
  3. Corrupt with prob sigmoid((r_s,t - theta_i + h*m_i - F*D_i)/tau). The act is "predatory" if the
     fiscal-gap term is its largest positive rent component, otherwise "deal".
  4. Detected officials are purged; retirements at 1/T; vacancies refilled (sponsored with prob rho,
     theta ~ N(-delta,1), wired to sponsor's circle and faction; else open entry).
  5. Rewiring of undetected corrupt officials toward corrupt friends-of-friends with prob w*e.
Memory switch: model A sets h=phi=0, kappa=1, rho=delta=w=0.  Model C keeps them.
All parameters are hypotheses; enforcement paths are stylized from public events (documented in
ENFORCEMENT below). Synthetic; calibrated only to the shape of CCDI case counts.
"""
from __future__ import annotations
import numpy as np, pandas as pd
from dataclasses import dataclass, replace, field
from pathlib import Path
from scipy import sparse

DATA=pd.read_csv(Path(__file__).resolve().parent/'data'/'china_series.csv').set_index('year')
SECTORS=['land','finance','pla','admin']; SHARE=np.array([.25,.20,.10,.45])
NFAC=6; FAC_SHARE=np.array([.20,.16,.16,.16,.16,.16])

@dataclass(frozen=True)
class Params:
    N:int=2500; k_new:int=4; p_in:float=0.75; T:float=25.0; tau:float=0.35
    r0:float=-0.8; beta:float=0.6; c_fin:float=0.2; bP:float=0.6; F:float=6.0
    a_admin:float=-0.5     # admin intercept (no measured discretionary flow besides the fiscal gap)
    # memory mechanisms (model C); model A zeroes them
    h:float=1.0; phi:float=0.6; kappa0:float=0.04; rho:float=0.7; delta:float=0.5; lam:float=2.0; w:float=0.3
    e_scale:float=1.0; xi:float=0.6          # campaign intensity scale; leader-faction exemption
    m2018:float=1.5; m2024:float=1.3          # enforcement-resource jumps (NSC 2018; 2024 campaign); estimated
    memory:bool=True
def model_A(p:Params)->Params: return replace(p,h=0.0,phi=0.0,kappa0=1.0,rho=0.0,delta=0.0,w=0.0,memory=False)
def model_K(p:Params)->Params:
    """Capacity constraint only: finite investigators, but no peer effects, sponsorship or rewiring."""
    return replace(p,h=0.0,phi=0.0,rho=0.0,delta=0.0,w=0.0,memory=True)

# ---------- exogenous paths ----------
ENFORCEMENT="""Stylized civilian campaign intensity e (before e_scale): 0.12 to 2012; 0.25 (2013), 0.35 (2014),
0.42 from 2015. Enforcement resources jump by m2018 (National Supervisory Commission, March 2018) and by
m2024 (2024 campaign on misconduct 'around the masses'); both jump sizes are estimated. In model A the
resources multiply detection; in model C they multiply investigative capacity kappa.
Leader-faction exemption xi applies from 2013 (Lorentzen & Lu). PLA e: 0.08 to 2013, 0.30 2014-16
(Xu Caihou, Guo Boxiong), 0.20 2017-22, 0.60 2023-26 (Rocket Force, He Weidong, Miao Hua, Zhang Youxia)."""
def civ_e(y):  return .12 if y<=2012 else .25 if y==2013 else .35 if y==2014 else .42
def res_mult(p,y): return 1.0 if y<=2017 else p.m2018 if y<=2023 else p.m2018*p.m2024
def pla_e(y):  return .08 if y<=2013 else .30 if y<=2016 else .20 if y<=2022 else .60

@dataclass(frozen=True)
class Scenario:
    name:str='Baseline'
    land_growth:float=0.0      # nominal growth of land revenue after 2026 (2026 = 3.8 trn yuan)
    land_floor:float=0.0       # trn yuan floor
    credit_flow:float=22.0     # new credit, % of GDP, 2026+ (target reached by credit_by)
    credit_by:int=2027
    gdp_growth:float=0.03      # nominal
    e_after:float|None=None    # civilian enforcement from relax_year (None = keep 0.55)
    relax_year:int=2031
    pla_after:float=0.30       # PLA enforcement from 2028
    xi_after:float|None=None   # leader exemption from relax_year (None = keep)
    defense_growth:float=0.07  # nominal growth of the official defense budget after 2025 (2026 budget: +7%)
    equip_share:float=0.366    # equipment share of defense spending after 2025 (UN report, 2022)
    off_budget:float=1.0       # multiplier for off-budget procurement (Pentagon: 2024 budget 32-63% higher)

def economy(sc:Scenario, years=range(1998,2042)):
    d=DATA.copy(); rows=[]
    gdp=d.loc[2025,'gdp_trn_yuan']; land=3.8; flow0=d.loc[2025,'new_credit_pct_gdp']; dfn=d.loc[2025,'defense_budget_trn']
    for y in years:
        if y<=2025:
            rows.append(dict(year=y,land_pct=d.loc[y,'land_pct_gdp'],credit_flow=d.loc[y,'new_credit_pct_gdp'] if y>1998 else 21.4,
                             equip_pct=d.loc[y,'equip_pct_gdp']*sc.off_budget)); continue
        gdp*=1+sc.gdp_growth
        if y>2026: land=max(sc.land_floor,land*(1+sc.land_growth))
        k=min(1.0,(y-2025)/max(1,sc.credit_by-2025)); flow=flow0+(sc.credit_flow-flow0)*k
        dfn*=1+sc.defense_growth
        rows.append(dict(year=y,land_pct=100*land/gdp,credit_flow=flow,equip_pct=100*dfn*sc.equip_share/gdp*sc.off_budget))
    e=pd.DataFrame(rows).set_index('year')
    e['credit_flow_s']=e.credit_flow.rolling(3,min_periods=1).mean()
    # fiscal gap: spending commitments (ref) rise with land revenue at once but fall only 10%/yr toward it
    ref=[];r_=None
    for v in e.land_pct:
        r_=v if r_ is None else (v if v>=r_ else r_+0.10*(v-r_)); ref.append(r_)
    e['ref']=ref; e['gap']=(e.ref-e.land_pct).clip(lower=0)
    return e

M_REF=10.0   # reference discretionary flow per unit share of officials (% of GDP)
def rents(p:Params,row):
    """One rule for every sector: rents rise with the log of discretionary money per official,
    r_s = r0 + beta*ln(flow_s / staff_share_s / M_REF). Flows (% of GDP): land-sale revenue; c_fin x new credit;
    equipment procurement (official defense budget x equipment share x off-budget multiplier).
    Admin has no measured flow and gets an intercept. The fiscal gap adds predatory rents to land and admin."""
    m=np.array([row.land_pct/SHARE[0], p.c_fin*row.credit_flow_s/SHARE[1], row.equip_pct/SHARE[2]])/M_REF
    land_term,cred_term,pla_term=p.beta*np.log(np.maximum(m,1e-3))
    gap_term=p.bP*row.gap/2.5
    r=np.array([p.r0+land_term+gap_term, p.r0+cred_term, p.r0+pla_term, p.r0+p.a_admin+gap_term])
    # which component dominates (for labelling acts as predatory)
    pred=np.array([gap_term>max(land_term,0) and gap_term>0, False, False, gap_term>0])
    return r,pred

def sig(z): return 1/(1+np.exp(-np.clip(z,-40,40)))

class World:
    def __init__(self,p:Params,seed:int):
        self.p=p; rng=self.rng=np.random.default_rng(seed); N=p.N
        self.sector=rng.choice(4,N,p=SHARE); self.faction=rng.choice(NFAC,N,p=FAC_SHARE)
        self.nbr=[set() for _ in range(N)]
        for i in range(N): self._wire(i,sponsor=None)
        self.sponsored=rng.random(N)<p.rho; self.theta=rng.normal(0,1,N)-p.delta*self.sponsored
        self.s=rng.random(N)<0.3; self.cum=0

    def _wire(self,i,sponsor):
        p,rng,N=self.p,self.rng,self.p.N; pick=[]
        if sponsor is not None:
            circle=[q for q in self.nbr[sponsor] if q!=i]
            pick=[sponsor]+([int(q) for q in rng.choice(circle,min(p.k_new-1,len(circle)),replace=False)] if circle else [])
        same=np.flatnonzero(self.faction==self.faction[i])
        while len(pick)<p.k_new:
            q=int(rng.choice(same)) if rng.random()<p.p_in else int(rng.integers(N))
            if q!=i and q not in pick: pick.append(q)
        for q in pick: self.nbr[i].add(q); self.nbr[q].add(i)

    def step(self,y:int,econ_row,sc:Scenario):
        p,rng,N=self.p,self.rng,self.p.N
        rows=np.repeat(np.arange(N),[len(n) for n in self.nbr]); cols=np.fromiter((j for n in self.nbr for j in n),int,len(rows))
        A=sparse.csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(N,N)); deg=np.asarray(A.sum(1)).ravel()
        m=(A@self.s.astype(float))/np.maximum(deg,1)
        civ=self.sector!=2
        x_civ=max(self.s[civ].mean(),1e-3); x_pla=max(self.s[~civ].mean(),1e-3)
        e_c=civ_e(y) if (sc.e_after is None or y<sc.relax_year) else sc.e_after
        e_p=pla_e(y) if y<=2027 else sc.pla_after
        xi=(p.xi if y>=2013 else 0.0) if (sc.xi_after is None or y<sc.relax_year) else sc.xi_after
        R=res_mult(p,y) if (sc.e_after is None or y<sc.relax_year) else 1.0
        kap=p.kappa0*R if p.memory else 1.0
        e_i=np.where(civ,np.minimum(1,e_c*p.e_scale*(1.0 if p.memory else R)),e_p)
        cong=np.where(civ,min(1.0,kap/x_civ),min(1.0,(p.kappa0*2 if p.memory else 1.0)/x_pla))
        D=np.clip(e_i*((1-p.phi)+p.phi*(1-m))*cong*(1-xi*(self.faction==0)),0,1)
        r,predflag=rents(p,econ_row)
        s=rng.random(N)<sig((r[self.sector]-self.theta+p.h*m-p.F*D)/p.tau)
        det=s&(rng.random(N)<D)
        out=dict(year=y,x=s[civ].mean(),x_land=s[self.sector==0].mean(),x_fin=s[self.sector==1].mean(),
                 x_pla=s[self.sector==2].mean(),x_admin=s[self.sector==3].mean(),
                 pred_share=(s&predflag[self.sector]).sum()/max(s[civ].sum(),1),
                 cases_civ=int((det&civ).sum()),purged_pla=int((det&~civ).sum()),
                 x_fac0=s[self.faction==0].mean(),x_other=s[self.faction!=0].mean(),
                 det_rate_fac0=det[self.faction==0].mean(),det_rate_other=det[self.faction!=0].mean(),
                 sponsored=self.sponsored.mean(),theta=self.theta.mean())
        self.s=s
        if p.w>0:
            movers=np.flatnonzero(s&~det&(rng.random(N)<p.w*np.minimum(1,e_i)))
            for i in movers:
                honest=[j for j in self.nbr[i] if not s[j]]
                if not honest: continue
                fof=[k for j in self.nbr[i] if s[j] for k in self.nbr[j] if s[k] and k!=i and k not in self.nbr[i]]
                if not fof: continue
                drop=honest[rng.integers(len(honest))]; add=fof[rng.integers(len(fof))]
                self.nbr[i].discard(drop); self.nbr[drop].discard(i); self.nbr[i].add(add); self.nbr[add].add(i)
        vac=det|(rng.random(N)<1/p.T); idx=np.flatnonzero(vac)
        for i in idx:
            for j in self.nbr[i]: self.nbr[j].discard(i)
            self.nbr[i]=set()
        stay=np.flatnonzero(~vac); w8=1+p.lam*self.s[stay]
        for i in idx:
            spons=rng.random()<p.rho and len(stay)>0
            self.sponsored[i]=spons; self.theta[i]=rng.normal(-p.delta if spons else 0,1); self.s[i]=False
            if spons:
                j=int(rng.choice(stay,p=w8/w8.sum())); self.faction[i]=self.faction[j]; self._wire(i,j)
            else:
                self.faction[i]=rng.choice(NFAC,p=FAC_SHARE); self._wire(i,None)
        return out

def simulate(p:Params,seed:int,sc:Scenario=Scenario(),end:int=2041,burn:int=60):
    econ=economy(sc,range(1998,end+1)); w=World(p,seed); out=[]
    for _ in range(burn): w.step(1998,econ.loc[1998],sc)
    for y in range(1998,end+1): out.append(w.step(y,econ.loc[y],sc))
    return pd.DataFrame(out)
