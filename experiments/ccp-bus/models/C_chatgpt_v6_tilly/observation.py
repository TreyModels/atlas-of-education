"""Delayed person-case outcomes, including cases resolved after retirement."""
import numpy as np

def keyed_uniform(ids,seed,tick,channel):
    """Counter-based random opportunities; variable case counts do not shift other streams."""
    with np.errstate(over='ignore'):
        z=np.asarray(ids,dtype=np.uint64)+np.uint64(seed%2**32)*np.uint64(0x9E3779B1)+np.uint64(tick+1)*np.uint64(0x85EBCA77)+np.uint64(channel)*np.uint64(0xC2B2AE3D)
        z=(z^(z>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
        z=(z^(z>>np.uint64(27)))*np.uint64(0x94D049BB133111EB)
        z=z^(z>>np.uint64(31))
    return ((z>>np.uint64(11)).astype(float)+.5)/2**53

class Cases:
    def __init__(self):
        self.person=np.empty(0,np.int64);self.filed=np.empty(0,np.int32)
        self.truth=np.empty(0,bool);self.evidence=np.empty(0,float);self.loyalty=np.empty(0,float)
    def add(self,person,tick,truth,evidence,loyalty):
        if len(person)!=len(np.unique(person)):raise ValueError('Duplicate persons in filing cohort')
        for k,x in [('person',person),('filed',np.full(len(person),tick)),('truth',truth),('evidence',evidence),('loyalty',loyalty)]:
            setattr(self,k,np.concatenate([getattr(self,k),np.asarray(x,dtype=getattr(self,k).dtype)]))
    def resolve(self,tick,seed,min_lag,ex_post_protection,exit_probability):
        age=tick-self.filed
        u=keyed_uniform(self.person+1000003*self.filed,seed,tick,1)
        hazard=1/(1+np.exp(-np.clip(-1+.8*age+self.evidence-ex_post_protection*self.loyalty,-30,30)))
        resolved=(age>=min_lag)&(u<hazard)
        sanction=resolved&(keyed_uniform(self.person+1000003*self.filed,seed,tick,2)<np.clip(self.evidence*(1-.6*ex_post_protection*self.loyalty),0,1))
        exits=sanction&(keyed_uniform(self.person+1000003*self.filed,seed,tick,3)<exit_probability)
        result=dict(sanctioned_ids=self.person[sanction].copy(),exit_ids=self.person[exits].copy(),
                    true_sanctioned_ids=self.person[sanction&self.truth].copy(),false_sanctioned_ids=self.person[sanction&~self.truth].copy(),
                    true_exit_ids=self.person[exits&self.truth].copy(),false_exit_ids=self.person[exits&~self.truth].copy(),
                    resolved=int(resolved.sum()),sanctions=int(sanction.sum()),true_sanctions=int((sanction&self.truth).sum()),
                    false_sanctions=int((sanction&~self.truth).sum()),mean_resolution_lag=float(age[resolved].mean()) if resolved.any() else 0.)
        for k in ['person','filed','truth','evidence','loyalty']:setattr(self,k,getattr(self,k)[~resolved])
        return result

def locate_persons(current,query):
    """Map surviving identities to seats; retired/departed identities return -1."""
    order=np.argsort(current);sorted_ids=current[order];idx=np.searchsorted(sorted_ids,query)
    valid=idx<len(current);safe=np.minimum(idx,len(current)-1);valid&=sorted_ids[safe]==query
    return np.where(valid,order[safe],-1)
