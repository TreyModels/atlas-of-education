"""bus_v3.py — v2 (memory + credit/land economy + sectors) plus how factions actually work.

Faction mechanics (each grounded in a finding; every strength is a parameter to estimate)
------------------------------------------------------------------------------------------
F1 Factions form naturally. Sponsored entrants join their sponsor's faction; sponsors are chosen in
   proportion to how attractive their faction is (protected factions draw clients, targeted ones repel).
F2 Protection comes from an incumbent patron and lapses when the patron leaves power (Zeng & Yang 2017:
   ties to incumbent Standing Committee members protected, ties to retired members did not). At the 2012-13
   transition, the old factions' patrons retire -> 'rival'; the new leader's network becomes 'core'.
F3 Targeting ramps up with the campaign, one new faction a year at most. Targeted factions are encircled periphery-first, then contagion runs along ties: each detected
   neighbour last year raises your hazard (Wang et al., 'encircling' of Zhou Yongkang's network).
   Visible ties transmit contagion at c, hidden ties at c_hid < c.
F4 Purges are political as well as anti-corruption: clean members of targeted factions can be removed
   (rate pi_pol, also amplified by contagion).
F5 Hiding. Members of factions under attack convert visible in-faction ties to hidden ones ('trust chains',
   Ruan, Lu & Ruan 2026). Hidden ties give half the peer support and are harder for investigators to see.
F6 Bandwagoning. Members of targeted factions defect to the leader's faction.
F7 Fission and threat. When the leader's faction exceeds S_split of officials, a sub-clique splits off as
   'adjacent' (partly protected). Any non-core faction whose share of officials exceeds s_threat becomes a
   target (the centre knows appointment records, so hiding ties does not hide size): the leader purges power centres, including his own appointees (PLA 2023-26).
Model switches: A = no memory (no peer effects, capacity, sponsorship-selection, rewiring, hiding);
K = capacity only; C = everything. Faction targeting (F2-F4) is part of enforcement in all three.
"""
from __future__ import annotations
import numpy as np, pandas as pd
from dataclasses import dataclass, replace
from scipy import sparse
import bus_v2 as V
from bus_v2 import economy, rents, Scenario, civ_e, pla_e, res_mult, sig, SHARE

STATUS=['unaffiliated','core','adjacent','neutral','rival','targeted']

@dataclass(frozen=True)
class Scenario3(Scenario):
    succession:int|None=None   # year a new leader takes over: his base (largest adjacent clique) becomes core,
                               # the old core and the other cliques lose protection and are targeted

@dataclass(frozen=True)
class P3(V.Params):
    gamma:float=2.0        # extra detection hazard for targeted factions (x periphery weight)
    c_vis:float=0.15       # contagion per detected visible neighbour
    c_hid:float=0.05       # contagion per detected hidden neighbour
    pi_pol:float=0.01      # political removal rate of clean members of targeted factions
    eta:float=0.5          # hiding rate (x faction risk)
    b_wagon:float=0.3      # bandwagoning rate (x faction risk)
    S_split:float=0.30     # leader faction share that triggers fission
    s_threat:float=0.10    # visible share at which a non-core faction becomes a target
    unaff:float=0.20       # share of officials with no faction
    hiding:bool=True
def A3(p): return replace(V.model_A(p),hiding=False,b_wagon=0.0)
def K3(p): return replace(V.model_K(p),hiding=False,b_wagon=0.0)

class World3:
    def __init__(self,p:P3,seed:int):
        self.p=p; rng=self.rng=np.random.default_rng(seed); N=p.N
        self.sector=rng.choice(4,N,p=SHARE)
        # factions: 0 = future leader's provincial network (small), 1-4 old incumbent factions, 5 neutral
        self.fac=np.where(rng.random(N)<p.unaff,-1,rng.choice(6,N,p=[.08,.20,.20,.18,.17,.17]))
        self.status={0:'neutral',1:'protected',2:'protected',3:'protected',4:'protected',5:'neutral'}
        self.patron={f:int(rng.choice(np.flatnonzero(self.fac==f))) for f in range(6)}
        self.vis=[set() for _ in range(N)]; self.hid=[set() for _ in range(N)]
        for i in range(N): self._wire(i,None)
        self.sponsored=rng.random(N)<p.rho; self.theta=rng.normal(0,1,N)-p.delta*self.sponsored
        self.s=rng.random(N)<0.3; self.det_prev=np.zeros(N,bool); self.purge_rate={}
        self.joined=np.full(N,-1); self.events=[]

    def _wire(self,i,sponsor):
        p,rng,N=self.p,self.rng,self.p.N; pick=[]
        if sponsor is not None:
            circ=[q for q in self.vis[sponsor] if q!=i]
            pick=[sponsor]+([int(q) for q in rng.choice(circ,min(p.k_new-1,len(circ)),replace=False)] if circ else [])
        same=np.flatnonzero(self.fac==self.fac[i]) if self.fac[i]>=0 else None
        while len(pick)<p.k_new:
            q=int(rng.choice(same)) if (same is not None and len(same)>1 and rng.random()<p.p_in) else int(rng.integers(N))
            if q!=i and q not in pick: pick.append(q)
        for q in pick: self.vis[i].add(q); self.vis[q].add(i)

    def _mat(self,sets):
        N=self.p.N; rows=np.repeat(np.arange(N),[len(n) for n in sets]); cols=np.fromiter((j for n in sets for j in n),int,len(rows))
        return sparse.csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(N,N))

    def _stat(self,i): f=self.fac[i]; return 'unaffiliated' if f<0 else self.status[f]

    def step(self,y,erow,sc):
        p,rng,N=self.p,self.rng,self.p.N
        # ---- F2: succession at 2013 ----
        if y==2013:
            # patrons of the old factions retire: two rival networks are encircled at once (e.g. the security
            # and PLA networks); the other old factions lose protection and wait their turn
            for f in (1,2): self.status[f]='targeted'
            for f in (3,4): self.status[f]='neutral'
            self.status[0]='core'
        if getattr(sc,'succession',None)==y:
            adj=[f for f,st in self.status.items() if st in ('adjacent','targeted') and f>=5 and (self.fac==f).any()]
            new=max(adj,key=lambda f:(self.fac==f).sum()) if adj else None
            for f in list(self.status):
                if (self.fac==f).any(): self.status[f]='targeted'
            if new is not None: self.status[new]='core'; self.events.append((y,new,'new_core'))
            self.succ_core=new
        Av,Ah=self._mat(self.vis),self._mat(self.hid)
        dv=np.asarray(Av.sum(1)).ravel(); dh=np.asarray(Ah.sum(1)).ravel()
        sf=self.s.astype(float)
        m=(Av@sf+0.5*(Ah@sf))/np.maximum(dv+0.5*dh,1e-9); m[dv+dh==0]=0
        civ=self.sector!=2; x_civ=max(self.s[civ].mean(),1e-3); x_pla=max(self.s[~civ].mean(),1e-3)
        relax=sc.e_after is not None and y>=sc.relax_year
        e_c=sc.e_after if relax else civ_e(y); e_p=pla_e(y) if y<=2027 else sc.pla_after
        R=1.0 if relax else res_mult(p,y); kap=p.kappa0*R if p.memory else 1.0
        e_i=np.where(civ,np.minimum(1,e_c*p.e_scale*(1.0 if p.memory else R)),e_p)
        cong=np.where(civ,min(1.0,kap/x_civ),min(1.0,(p.kappa0*2 if p.memory else 1.0)/x_pla))
        # ---- faction multipliers (F2, F3) ----
        stat=np.array([self._stat(i) for i in range(N)])
        fac_in_v=np.zeros(N)
        for i in range(N):
            f=self.fac[i]
            if f>=0: fac_in_v[i]=sum(1 for j in self.vis[i] if self.fac[j]==f)
        periph=1/(1+fac_in_v); periph=periph/max(periph[self.fac>=0].mean(),1e-9)
        xi_eff=p.xi if not (sc.xi_after is not None and y>=sc.relax_year) else sc.xi_after
        mult=np.ones(N)
        mult[stat=='core']=1-xi_eff; mult[stat=='adjacent']=1-xi_eff/2; mult[stat=='protected']=1-xi_eff
        ramp=min(1.0,civ_e(y)/0.42) if y>=2013 else 0.0      # targeting builds up with the campaign
        tgt=stat=='targeted'; mult[tgt]=1+p.gamma*ramp*periph[tgt]
        Dbase=np.clip(e_i*((1-p.phi)+p.phi*(1-m))*cong*mult,0,1)
        dprev=self.det_prev.astype(float)
        nv=Av@dprev; nh=Ah@dprev
        D=1-(1-Dbase)*(1-p.c_vis)**nv*(1-p.c_hid)**nh
        r,predflag=rents(p,erow)
        s=rng.random(N)<sig((r[self.sector]-self.theta+p.h*m-p.F*D)/p.tau)
        det=s&(rng.random(N)<D)
        # ---- F4: political removals of clean members of targeted factions ----
        pol_p=np.where(tgt&~s,1-(1-p.pi_pol*ramp)*(1-p.c_vis/3)**nv,0.0) if y>=2013 else np.zeros(N)
        pol=rng.random(N)<pol_p
        removed=det|pol
        # ---- outputs ----
        out=dict(year=y,x=s[civ].mean(),x_land=s[self.sector==0].mean(),x_fin=s[self.sector==1].mean(),
                 x_pla=s[self.sector==2].mean(),x_admin=s[self.sector==3].mean(),
                 pred_share=(s&predflag[self.sector]).sum()/max(s[civ].sum(),1),
                 cases_civ=int((removed&civ).sum()),political_share=pol.sum()/max(removed.sum(),1),
                 hidden_share=dh.sum()/max(dv.sum()+dh.sum(),1),
                 n_factions=len({f for f in self.fac if f>=0}),core_share=np.mean([self._stat(i)=='core' for i in range(N)]),
                 contagion_hr=(removed[nv>0].mean()/max(removed[nv==0].mean(),1e-9)) if (nv>0).any() else np.nan)
        for st in ['unaffiliated','core','adjacent','neutral','protected','targeted']:
            mk=stat==st; out[f'n_{st}']=int(mk.sum())
            out[f'rem_{st}']=removed[mk].mean() if mk.any() else np.nan
            out[f'x_{st}']=s[mk].mean() if mk.any() else np.nan
        # periphery-first: in-faction degree of removed vs all members in targeted factions
        if (tgt&removed).any(): out['deg_removed_tgt']=fac_in_v[tgt&removed].mean(); out['deg_all_tgt']=fac_in_v[tgt].mean()
        self.records=(removed.copy(),s.copy(),stat.copy(),fac_in_v.copy(),(dh/np.maximum(dv+dh,1)).copy())
        # purge rate by faction (risk signal for hiding / bandwagoning)
        risk={f:removed[self.fac==f].mean() for f in set(self.fac.tolist()) if f>=0}
        self.s=s; self.det_prev=removed
        # ---- F5 hiding and F6 bandwagoning ----
        if p.hiding and y>=2013:
            for i in np.flatnonzero((self.fac>=0)&~removed):
                f=self.fac[i]; rk=risk.get(f,0)
                if rk<=0: continue
                ph=p.eta*rk/(rk+0.02)
                for j in [j for j in self.vis[i] if self.fac[j]==f]:
                    if rng.random()<ph: self.vis[i].discard(j); self.vis[j].discard(i); self.hid[i].add(j); self.hid[j].add(i)
                if self.status.get(f)=='targeted' and rng.random()<p.b_wagon*rk/(rk+0.02):
                    cf_=getattr(self,'succ_core',None); cf_=0 if cf_ is None else cf_
                    core=np.flatnonzero((self.fac==cf_)&~removed)
                    if len(core):
                        for j in [j for j in self.vis[i] if self.fac[j]==f]:   # old ties go underground
                            self.vis[i].discard(j); self.vis[j].discard(i); self.hid[i].add(j); self.hid[j].add(i)
                        self.fac[i]=cf_; self.joined[i]=y; q=int(rng.choice(core)); self.vis[i].add(q); self.vis[q].add(i)
        # ---- rewiring toward corrupt friends of friends (memory, as v2) ----
        if p.w>0:
            for i in np.flatnonzero(s&~removed&(rng.random(N)<p.w*np.minimum(1,e_i))):
                honest=[j for j in self.vis[i] if not s[j]]
                fof=[k for j in self.vis[i] if s[j] for k in self.vis[j] if s[k] and k!=i and k not in self.vis[i]]
                if honest and fof:
                    d_=honest[rng.integers(len(honest))]; a_=fof[rng.integers(len(fof))]
                    self.vis[i].discard(d_); self.vis[d_].discard(i); self.vis[i].add(a_); self.vis[a_].add(i)
        # ---- vacancies and entry (F1) ----
        vac=removed|(rng.random(N)<1/p.T); idx=np.flatnonzero(vac)
        for i in idx:
            for j in self.vis[i]: self.vis[j].discard(i)
            for j in self.hid[i]: self.hid[j].discard(i)
            self.vis[i]=set(); self.hid[i]=set(); self.joined[i]=-1
        stay=np.flatnonzero(~vac)
        attract={'core':3.0,'adjacent':2.0,'protected':2.0,'neutral':1.0,'targeted':0.3,'unaffiliated':0.5}
        w8=(1+p.lam*self.s[stay])*np.array([attract[self._stat(j)] for j in stay])
        for i in idx:
            spons=rng.random()<p.rho and len(stay)>0
            self.sponsored[i]=spons; self.theta[i]=rng.normal(-p.delta if spons else 0,1); self.s[i]=False
            if spons:
                j=int(rng.choice(stay,p=w8/w8.sum())); self.fac[i]=self.fac[j]; self._wire(i,j)
            else:
                self.fac[i]=-1 if rng.random()<0.5 else self.fac[int(rng.choice(stay))]; self._wire(i,None)
        # patrons replaced by the best-connected remaining member
        for f in list(self.status):
            mem=np.flatnonzero(self.fac==f)
            if len(mem)==0: continue
            if self.patron.get(f) not in set(mem.tolist()):
                self.patron[f]=int(mem[np.argmax([len(self.vis[k]) for k in mem])])
        # ---- F7 fission of the leader's faction, and threat targeting ----
        if y>=2013:
            cf=getattr(self,'succ_core',None); cf=0 if cf is None else cf
            core=np.flatnonzero(self.fac==cf)
            if len(core)>p.S_split*N:
                cand=[k for k in core if k!=self.patron[cf]]
                newp=int(cand[np.argmax([len(self.vis[k]) for k in cand])])
                g=max(self.status)+1; self.status[g]='adjacent'; self.patron[g]=newp; self.events.append((y,g,'split'))
                movers=[newp]+[k for k in self.vis[newp] if self.fac[k]==cf]+[k for k in core if self.joined[k]>=0 and self.rng.random()<0.5]
                for k in set(movers):
                    if k!=self.patron[cf]: self.fac[k]=g
            # the centre sees appointment records, so size (not visible ties) reveals a power centre;
            # it takes on at most one new faction a year, the largest above the threshold
            cands=[(float((self.fac==f).mean()),f,st) for f,st in self.status.items() if st in ('adjacent','neutral')]
            cands=[c for c in cands if c[0]>p.s_threat]
            if cands:
                _,f,st=max(cands); self.status[f]='targeted'; self.events.append((y,f,'targeted_'+st))
        return out

def simulate3(p:P3,seed:int,sc:Scenario=Scenario(),end:int=2041,burn:int=60,keep_records=False):
    econ=economy(sc,range(1998,end+1)); w=World3(p,seed); out=[]; recs={}
    for _ in range(burn): w.step(1998,econ.loc[1998],sc)
    for y in range(1998,end+1):
        out.append(w.step(y,econ.loc[y],sc))
        if keep_records: recs[y]=w.records
    df=pd.DataFrame(out); df.attrs['events']=w.events
    return (df,recs) if keep_records else df
