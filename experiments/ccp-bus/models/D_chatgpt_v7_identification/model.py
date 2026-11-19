"""V6 Tilly explanatory ABM: identities, promotions, adaptive relationships, output and observation.
All behavioral coefficients are experimental. Calendar labels are scenario time.
"""
from dataclasses import dataclass,replace
import numpy as np
from observation import Cases,locate_persons,keyed_uniform
from evidence import Evidence
from tilly import TillyMixin
from memory import MemoryMixin

SCENARIOS=('baseline','campaign','access_reform','obligations_off','protection_off','emulation_off','adaptation_off','equal_resources','strong_oversight','low_demand','network_reset','payment_blind','tilly_off','no_replacement','zero_attraction')
@dataclass(frozen=True)
class Params:
    family:str='bus';temperature:float=.35;report_capture:float=.6;ramp_years:float=4.;nsc_multiplier:float=1.3;appointment_shock:bool=False
    request_pressure:float=.2;request_rate:float=.35;obligation_gain:float=.25;obligation_pressure:float=.8
    extraction_rate:float=.25;settlement_fraction:float=.6;lawful_service:float=.06
    protection_supply:float=.65;resource_attraction:float=.45;adaptation:float=.15;emulation:float=.15
    closure_response:float=1.;exchange_promotion:float=.6;cohort_integrity:float=2.2
    n:int=50000;organizations:int=64;contacts:int=4
    rent:float=-.45;peer:float=.7;capacity:float=.025;protection:float=.5
    entry_bias:float=0.;coordination:float=.35;anti_client:float=.8
    concealment_cost:float=.4;memory:float=.6;rewiring:float=.10
    signal_noise:float=.25;performance_weight:float=.6;network_weight:float=.7
    informality:float=.7;reporting:float=.18;report_suppression:float=.6
    turnover:float=.04;sanction_cost:float=4.;case_lag:int=2;exit_probability:float=.65
    procurement_elasticity:float=.5;productive_patronage:bool=True
    empirical_flows:bool=True;contract_timing:str='current';initial_corruption:float=.25

def sig(z):return 1/(1+np.exp(-np.clip(z,-35,35)))

class World(MemoryMixin,TillyMixin):
    def __init__(self,p,seed):
        if not 0<=p.capacity<=1 or not 0<=p.reporting<=1:raise ValueError('Invalid probabilities')
        if p.n<128*p.organizations:raise ValueError('Need at least 128 agents per organization for five ranks')
        if p.contract_timing not in ('current','lagged'):raise ValueError('contract_timing')
        if any(not 0<=x<=1 for x in (p.request_rate,p.extraction_rate,p.settlement_fraction,p.adaptation,p.emulation,p.protection_supply)):raise ValueError('Invalid Tilly probability/share')
        if min(p.obligation_gain,p.lawful_service,p.obligation_pressure)<0:raise ValueError('Invalid obligation coefficient')
        self.p=p;self.seed=int(seed);self.tick=0;self.e=.15;self.last_report=.01
        seq=np.random.SeedSequence(seed);self.rng={k:np.random.default_rng(s) for k,s in zip(('init','choice','signals','careers','relations','contracts'),seq.spawn(6))}
        r=self.rng['init'];self.O=int(.8*p.n)//p.organizations*p.organizations;O=self.O;self.S=p.n-O;self.size=O//p.organizations
        self.org=np.repeat(np.arange(p.organizations),self.size);local=np.tile(np.arange(self.size),p.organizations)
        self.rank=np.select([local<1,local<4,local<16,local<80],[0,1,2,3],default=4).astype(np.int8)
        self.pools={k:np.flatnonzero(self.rank==k) for k in range(5)}
        self.parent=np.full(O,-1,np.int32)
        for k,lo,hi in [(1,0,1),(2,1,4),(3,4,16),(4,16,min(80,self.size))]:
            ix=self.pools[k];self.parent[ix]=self.org[ix]*self.size+r.integers(lo,hi,len(ix))
        self.sector=(self.org%5).astype(np.int8)
        self.person=np.arange(O,dtype=np.int64);self.integrity=r.normal(.6,.7,O);self.competence=np.clip(r.normal(.65,.18,O),.05,1.)
        self.loyalty=r.beta(2,2,O);self.tenure=r.integers(0,8,O);self.state=r.random(O)<p.initial_corruption
        self.patron=np.where((self.parent>=0)&(r.random(O)<p.informality),self.parent,-1).astype(np.int32)
        # Initial sponsored integrity can be better, equal or worse; no default adverse selection.
        self.integrity+=p.entry_bias*(self.patron>=0)
        self.covert=np.zeros(O,bool);self.broker=np.full(O,-1,np.int32)
        self.dst=(self.org[:,None]*self.size+r.integers(0,self.size,(O,p.contacts))).astype(np.int32)
        self.dst=np.where(self.dst==np.arange(O)[:,None],(self.dst+1)%O,self.dst).astype(np.int32)
        self.trust=np.full((O,p.contacts),.15,np.float32);self.hidden=np.zeros((O,p.contacts),bool)
        self.firm_cost=r.uniform(.5,1.3,self.S);self.firm_quality=r.uniform(.5,1.,self.S);self.firm_integrity=r.normal(.5,.7,self.S)
        self.offices=np.arange(0,O,8,dtype=np.int32);self.repeated_supplier=r.integers(0,self.S,len(self.offices));self.supplier_tie=np.full(len(self.offices),.1)
        self.output=np.full(O,.7);self.expected_detection=np.full(O,.03);self.receipts=np.zeros(O)
        self.cases=Cases();self.evidence=Evidence(p.empirical_flows);self.total_promotions=0
        self.last_event={};self.last_contract={}
        self.init_tilly()
        self.force_effort=None

    def roots(self,visible=False):
        ptr=np.where(self.covert,-1,self.patron) if visible else self.patron
        root=np.arange(self.O,dtype=np.int32)
        for _ in range(5):
            nxt=ptr[root];root=np.where(nxt>=0,nxt,root)
        return root

    def policy(self,scenario,year):
        if scenario not in SCENARIOS:raise ValueError(scenario)
        active=year>=2013 and scenario!='baseline'
        policy=dict(active=active,entry_open=False,bypass=1. if active and scenario=='strong_oversight' else .15,
            conceal=True,memory=True,coordination=True,network=self.p.network_weight,performance=self.p.performance_weight,
            protection=0. if active and scenario=='strong_oversight' else self.p.protection,
            capacity=min(1.,self.p.capacity*(3 if active and scenario=='strong_oversight' else 1)),procurement=1.,
            access=not(active and scenario in ('access_reform','tilly_off')),
            obligations=not(active and scenario in ('obligations_off','tilly_off')),
            protection_exchange=not(active and scenario in ('protection_off','strong_oversight','tilly_off')),
            emulate=not(active and scenario in ('emulation_off','tilly_off')),
            adapt=not(active and scenario in ('adaptation_off','tilly_off')),
            equal=active and scenario=='equal_resources',
            demand=self.p.request_rate*(.1 if active and scenario=='low_demand' else 1.),
            favor_promotion=not(active and scenario in ('payment_blind','tilly_off')),
            attraction=0. if active and scenario=='zero_attraction' else self.p.resource_attraction,
            tilly=False)
        ramp=.15 if year<2013 else 1-np.exp(-(year-2012)/self.p.ramp_years)
        policy.update(capacity=min(.8,self.p.capacity*ramp*(self.p.nsc_multiplier if year>=2018 else 1)),
                      conceal=False,network=0.,performance=0.,protection=0.,demand=0.,obligations=False,
                      protection_exchange=False,emulate=False,adapt=False,access=False,attraction=0.,
                      favor_promotion=False,memory=self.p.family=='bus')
        return policy

    def _contracts(self,act,effort,flow,uniforms):
        p=self.p;ix=self.offices;K=len(ix);S=self.S
        candidates=uniforms['candidates'].copy();candidates[:,0]=self.repeated_supplier
        insider=(candidates==self.repeated_supplier[:,None])
        closed=(uniforms['closure']<self.closure[self.org[ix]])&self.current_policy['access']
        bribe=sig(p.rent-self.firm_integrity[candidates]+.5*self.supplier_tie[:,None])>uniforms['bribes']
        bid=self.firm_cost[candidates]+.1*uniforms['bid_noise']
        merit=self.firm_quality[candidates]-bid*.35
        favor=act[ix,None]*bribe*(.4+.3*(candidates==self.repeated_supplier[:,None])*self.supplier_tie[:,None])
        score=np.where(closed[:,None]&~insider,-1e6,merit+favor)
        winner=np.argmax(score,axis=1);firm=candidates[np.arange(K),winner]
        deal=act[ix]&bribe[np.arange(K),winner]
        amount=self.allocation[ix]
        diverted=p.extraction_rate*amount*deal
        quality=np.clip(self.firm_quality[firm]*(.5+.5*effort[ix])-.25*deal,0,1)
        repeat=firm==self.repeated_supplier
        self.supplier_tie=np.clip(.8*self.supplier_tie+.2*repeat,0,1);self.repeated_supplier=firm
        receipts=np.zeros(self.O);receipts[ix]=diverted
        # All allocated budgets are conserved between delivery expenditure and diversion.
        delivered=amount-diverted
        self.last_contract=dict(allocated=amount.copy(),delivered=delivered,diverted=diverted,quality=quality)
        return receipts,dict(contracts=K,corrupt_contract_share=float(deal.mean()),diverted_share=float(diverted.sum()/amount.sum()),
            procurement_quality=float(quality[self.sector[ix]==0].mean()),mean_contract_quality=float(quality.mean()),
            supplier_repeat_share=float(repeat.mean()),closed_award_share=float(closed.mean()))

    def _careers(self,depart,pol,draw):
        """Promote real identities; carry their attributes and remap person-bound relationships."""
        O=self.O;p=self.p;source=np.arange(O,dtype=np.int32);source[depart]=-1
        unavailable=depart.copy();promoted=np.zeros(O,bool);chosen_mode=np.full(O,-1,np.int8)
        promoted_count=0;client_considered=0;client_selected=0;appointed=0
        for level in range(4):
            dest=self.pools[level];dest=dest[source[dest]<0]
            if not len(dest):continue
            cand=draw['career_candidates'][dest]
            boss=self.parent[dest]
            familiar=(self.patron[cand]==boss[:,None])|(self.patron[cand]==dest[:,None])
            familiar&=self.patron[cand]>=0
            support=self.support_to[cand];support_slots=locate_persons(self.person,support.ravel()).reshape(cand.shape)
            relevant=(boss>=0)[:,None]&(support==self.person[np.maximum(boss,0)][:,None])
            live=(support_slots>=0)&~depart[np.maximum(support_slots,0)]
            favor_support=p.exchange_promotion*self.paid_support[cand]*relevant*live if pol['favor_promotion'] else 0.
            base=favor_support+1.2*self.competence[cand]+.6*self.output[cand]+(.9 if pol['active'] else .3)*self.loyalty[cand]+draw['career_noise'][dest]
            risk=2.5*p.anti_client*self.e*pol['active']
            # Appointment mode choice is behavioral; a client can be rejected under broad purge risk.
            visible=base+.55*familiar-risk*familiar
            covert=base+.40*familiar-.6*p.concealment_cost-.15*risk*familiar
            open_score=base-.05
            if pol['entry_open']:
                visible[:]=-1e6;covert[:]=-1e6
            if not pol['conceal']:covert[:]=-1e6
            options=np.stack([visible,covert,open_score],axis=2)
            modes=np.argmax(options,axis=2);scores=np.max(options,axis=2)
            valid=(source[cand]>=0)&~unavailable[cand]&~promoted[cand]
            scores=np.where(valid,scores,-1e9)
            client_considered+=int((familiar&valid).sum())
            # Select destinations in a randomized priority order; each donor is used at most once.
            order=np.argsort(draw['career_priority'][dest])
            for j in order:
                d=int(dest[j]);options_idx=np.argsort(-scores[j])
                for cix in options_idx:
                    donor=int(cand[j,cix])
                    if scores[j,cix]<-1e8 or unavailable[donor] or promoted[donor] or source[donor]<0:continue
                    source[d]=source[donor];source[donor]=-1;unavailable[donor]=True;promoted[d]=True
                    chosen_mode[d]=modes[j,cix];promoted_count+=1;client_selected+=int(familiar[j,cix]);appointed+=1;break
        fresh=source<0;old_to_new=np.full(O,-1,np.int32);old_to_new[source[~fresh]]=np.flatnonzero(~fresh)
        safe=np.maximum(source,0)
        old_patron=self.patron.copy();old_dst=self.dst.copy();old_person=self.person.copy();old_trust=self.trust.copy();old_hidden=self.hidden.copy()
        for name in ['person','integrity','competence','loyalty','tenure','state','covert','broker','output','expected_detection','receipts']:
            setattr(self,name,getattr(self,name)[safe].copy())
        self.person[fresh]=O+(self.tick+1)*O+np.flatnonzero(fresh)
        self.integrity[fresh]=draw['entrant_integrity'][fresh]
        self.competence[fresh]=draw['entrant_competence'][fresh]
        self.loyalty[fresh]=draw['entrant_loyalty'][fresh]**(.65 if pol['active'] else 1)
        self.tenure[fresh]=0;self.state[fresh]=False;self.output[fresh]=.6;self.expected_detection[fresh]=.03;self.receipts[fresh]=0
        mapped=old_patron[safe];new_patron=np.where(mapped>=0,old_to_new[np.maximum(mapped,0)],-1)
        valid=(new_patron>=0)&(self.rank[np.maximum(new_patron,0)]<self.rank)
        new_patron=np.where(valid,new_patron,-1).astype(np.int32)
        self.patron=new_patron
        # For entrants, sponsorship is chosen on the tradeoff between coordination and visible political risk.
        familiarity=p.informality+.4*p.coordination-2*p.anti_client*self.e*pol['active']
        desired=sig(familiarity)
        sponsor=fresh&(self.parent>=0)&(draw['entry_mode']<desired)&(not pol['entry_open'])
        self.patron[fresh]=-1;self.patron[sponsor]=self.parent[sponsor]
        self.covert[fresh]=False
        hide_sponsor=sponsor&pol['conceal']&(draw['entry_covert']<sig(2*p.anti_client*self.e-p.concealment_cost-.5))
        self.covert[hide_sponsor]=True
        self.integrity[sponsor]+=p.entry_bias
        # Promotion changes reporting authority while the person retains characteristics.
        for mode in [0,1,2]:
            ids=np.flatnonzero((chosen_mode==mode)&(self.parent>=0))
            self.patron[ids]=self.parent[ids] if mode<2 else -1
            self.covert[ids]=mode==1
        self.covert[self.patron<0]=False
        if not pol['conceal']:self.covert[:]=False
        self.broker=np.where(self.covert,draw['broker'], -1).astype(np.int32)
        # Contact rows travel with the person; destinations follow surviving identities to new seats.
        owner_source=np.where(fresh,np.arange(O),safe)
        dst_before=old_dst[owner_source];remap=old_to_new[dst_before]
        self.trust=old_trust[owner_source].copy();self.hidden=old_hidden[owner_source].copy()
        reset=fresh[:,None]|(remap<0)
        # Legacy office obligations are distinct from surviving person-bound relationships.
        inherit=reset&(draw['tie_keep']<p.memory)&(self.patron>=0)[:,None]&pol['memory']
        retained_destination=np.where(remap>=0,remap,dst_before)
        self.dst=np.where(reset&~inherit,draw['new_contacts'],retained_destination).astype(np.int32)
        self.trust[reset&~inherit]=.05;self.hidden[reset&~inherit]=False
        # Structural-memory ablation clears carried relationship strength, independent of intrinsic types.
        if not pol['memory']:
            self.trust[:]=.05;self.hidden[:]=False;self.patron[:]=-1;self.covert[:]=False;self.broker[:]=-1
        self.dst=np.where(self.dst==np.arange(O)[:,None],(self.dst+1)%O,self.dst).astype(np.int32)
        self.remap_tilly(source,fresh,old_person,pol)
        self.total_promotions+=promoted_count
        self.last_event=dict(source=source,old_person=old_person,fresh=fresh,promoted=promoted)
        return dict(promotions=promoted_count,new_entrants=int(fresh.sum()),client_candidates=client_considered,
                    client_promotions=client_selected,internal_appointments=appointed,covert_appointments=int((chosen_mode==1).sum()+hide_sponsor.sum()),inherited_org_ties=int(inherit.sum()))

    def _draws(self):
        O=self.O;S=self.S;p=self.p;k=p.contacts
        c=self.rng['choice'];s=self.rng['signals'];r=self.rng['relations'];a=self.rng['careers'];f=self.rng['contracts']
        d={key:c.random(O) for key in ['act','complaint','complaint_bypass','report_pass','retire','finding','false_filing']}
        d['performance_noise']=s.normal(0,p.signal_noise,O);d['investigation_noise']=s.gumbel(0,.4,O)
        d['tie_hide']=r.random((O,k));d['tie_keep']=r.random((O,k));d['tie_rewire']=r.random((O,k));d['new_contacts']=r.integers(0,O,(O,k),dtype=np.int32)
        d['entrant_integrity']=a.normal(.6,.7,O);d['entrant_competence']=np.clip(a.normal(.65,.18,O),.05,1)
        d['entrant_loyalty']=a.random(O);d['entry_mode']=a.random(O);d['entry_covert']=a.random(O);d['broker']=a.integers(0,S,O)
        d['career_candidates']=np.zeros((O,3),np.int32)
        for level in range(4):
            ix=self.pools[level];pool=self.pools[level+1]
            # Candidate seats in the same organization; small cross-organization transfers are allowed.
            local_pool=(pool%self.size)[self.org[pool]==0]
            local=self.org[ix,None]*self.size+local_pool[a.integers(0,len(local_pool),(len(ix),3))]
            global_=pool[a.integers(0,len(pool),(len(ix),3))]
            d['career_candidates'][ix]=np.where(a.random((len(ix),3))<.1,global_,local)
        d['career_noise']=a.gumbel(0,.15,(O,3));d['career_priority']=a.random(O)
        K=len(self.offices);d['contracts']=dict(candidates=f.integers(0,S,(K,3)),bribes=f.random((K,3)),bid_noise=f.random((K,3)),closure=self.t_rng.random(K))
        d['help']=self.t_rng.random(O);d['help_deliver']=self.t_rng.random(O);d['provider_choice']=self.t_rng.integers(0,p.contacts,O);d['provider_mode']=self.t_rng.random(O);d['model_org']=self.t_rng.integers(0,p.organizations,p.organizations);d['emulate']=self.t_rng.random(p.organizations)
        return d

    def step(self,scenario,year):
        p=self.p;O=self.O;pol=self.policy(scenario,year);self.current_policy=pol
        if self.p.appointment_shock and year==2013 and not self.cohort and scenario!='no_replacement':self.appoint_outsiders(scenario)
        d=self._draws()
        target=.15 if not pol['active'] else np.clip(.45+2*self.last_report+.5*max(0,.75-self.output.mean()),.35,.85)
        self.e=.7*self.e+.3*target
        if self.force_effort is not None:self.e=float(self.force_effort)
        root=self.roots();resource=np.ones(O) if pol['equal'] else 1+2*(4-self.rank.astype(float));flow=np.asarray(self.evidence.flows(year),float);flow[0]*=pol['procurement']
        observed_root=self.roots(visible=True)
        group=np.bincount(observed_root,weights=resource,minlength=O);power=group[observed_root]/group.sum()
        visible_political=~self.covert
        political_signal=power/(.01+power)*visible_political
        support=self.trust*(1-.25*self.hidden);peer=(support*self.state[self.dst]).sum(1)/np.maximum(support.sum(1),1e-9)
        conceal=(self.hidden*self.trust).sum(1)/np.maximum(self.trust.sum(1),1e-9)
        self.prepare_tilly(pol,d,flow)
        peer=self.prepare_memory(pol)
        protect=np.clip(pol['protection']*self.loyalty+(self.shield if pol['protection_exchange'] else 0.),0,.95)
        opportunity=p.procurement_elasticity*np.log(np.maximum(flow[self.sector],.1))
        # Land decline creates a separate pressure channel while reducing ordinary transaction opportunities.
        fiscal_pressure=.2*max(0,1-flow[1])*np.isin(self.sector,[1,3,4])
        relational_pressure=self.relational_pressure if pol['tilly'] else 0.
        prob=sig((p.rent+opportunity+fiscal_pressure-self.integrity+p.peer*peer-p.sanction_cost*self.expected_detection)/p.temperature)
        act=d['act']<prob
        coordination=p.coordination if pol['coordination'] and p.productive_patronage else 0
        pat_comp=np.where(self.patron>=0,self.competence[np.maximum(self.patron,0)],0)
        effort=sig(1.5*self.competence+coordination*pat_comp-.5*self.e*(1-protect)-.25*act)
        contract_act=act if p.contract_timing=='current' else self.state
        receipts,contract=self._contracts(contract_act,effort,flow,d['contracts'])
        output=np.clip(self.competence*(.5+.5*effort)+coordination*.25*pat_comp-.15*act,0,1)
        # Observations are generated before investigation; the center does not receive true acts or hidden edges.
        reporting_probability=p.reporting*(1-(p.report_capture*self.memory_peer if p.family!='current_incentives' else 0.))
        complaint=((d['complaint']<reporting_probability)&act)|((d['complaint']<.001)&~act)
        suppressed=np.clip((p.report_suppression*(self.patron>=0)+.3*(self.shield if pol['protection_exchange'] else 0.))*(1-pol['bypass']),0,.95)
        reports=complaint&((d['complaint_bypass']<pol['bypass'])|(d['report_pass']>suppressed))
        performance=np.clip(output+d['performance_noise'],0,1.5)
        bad_performance=np.maximum(0,(.75 if pol['active'] else .65)-performance)
        score=.1+1.5*reports+pol['active']*(pol['network']*political_signal+pol['performance']*bad_performance)-.5*pol['protection']*self.loyalty+d['investigation_noise']
        pending=np.isin(self.person,self.cases.person)
        eligible=np.flatnonzero(~pending)
        capacity=int(np.floor(pol['capacity']*O*(.5+self.e)))
        count=min(capacity,len(eligible));invest=np.zeros(O,bool)
        if count:
            chosen=eligible[np.argpartition(score[eligible],-count)[-count:]];invest[chosen]=True
        self.last_investigated=self.person[invest].copy()
        sensitivity=np.clip(.85*(1-.6*conceal)*(1-.3*protect),.05,.95)
        true_filing=invest&act&(d['finding']<sensitivity)
        false_filing=invest&~act&(d['false_filing']<(.005+.05*pol['active']*(pol['network']*political_signal+pol['performance']*bad_performance)))
        file=true_filing|false_filing
        evidence=np.where(true_filing,.9,.35)
        self.cases.add(self.person[file],self.tick,act[file],evidence[file],self.loyalty[file])
        resolved=self.cases.resolve(self.tick,self.seed,p.case_lag,pol['protection']*.5,p.exit_probability)
        exit_slots=locate_persons(self.person,resolved['exit_ids']);exit_slots=exit_slots[exit_slots>=0]
        employment_exit=np.zeros(O,bool);employment_exit[exit_slots]=True
        self.expected_detection=.8*self.expected_detection+.2*(count/O)*sensitivity
        self.output=output;self.state=act;self.tenure+=1;self.last_report=reports.mean()
        # Ties respond to cooperative returns; unproductive weak ties may be replaced.
        self.trust=np.clip(.88*self.trust+.12*(act[:,None]&act[self.dst]),.01,1).astype(np.float32)
        hide=sig((p.sanction_cost*self.e*self.trust*act[:,None]*.6-p.concealment_cost)/.3)
        self.hidden=(d['tie_hide']<hide) if pol['conceal'] else np.zeros_like(self.hidden)
        weak=(self.trust<.2)&(d['tie_rewire']<p.rewiring)
        candidate=d['new_contacts'];prefer=self.state[candidate]|(self.competence[candidate]>.75)
        rewire=weak&prefer
        self.dst[rewire]=candidate[rewire];self.trust[rewire]=.1;self.hidden[rewire]=False
        before_patron=self.patron>=0
        out=dict(year=year,tick=self.tick,officials=O,suppliers=self.S,true_misconduct=float(act.mean()),
            pla_misconduct=float(act[self.sector==0].mean()),mean_output=float(output.mean()),mean_effort=float(effort.mean()),
            complaints=int(complaint.sum()),reported_complaints=int(reports.sum()),investigations=count,capacity=capacity,
            cases_filed=int(file.sum()),civilian_officials=int((self.sector!=0).sum()),cases_filed_civilian=int((file&(self.sector!=0)).sum()),true_cases=int(true_filing.sum()),false_cases=int(false_filing.sum()),
            cases_resolved=resolved['resolved'],sanctions=resolved['sanctions'],false_sanctions=resolved['false_sanctions'],
            mean_resolution_lag=resolved['mean_resolution_lag'],employment_exits=int(employment_exit.sum()),pending_cases=len(self.cases.person),
            hidden_trust_share=float((self.hidden*self.trust).sum()/max(self.trust.sum(),1e-9)),patron_share=float(before_patron.mean()),
            covert_patron_share=float(self.covert.mean()),largest_patron_group=float(np.bincount(root,minlength=O).max()/O),
            campaign_effort=float(self.e),mean_competence=float(self.competence.mean()),rewired_contacts=int(rewire.sum()),**contract)
        retired=(d['retire']<p.turnover)&~employment_exit
        departed=employment_exit|retired
        out.update(self.finish_tilly(act,receipts,output,file,true_filing,false_filing,resolved,employment_exit,retired,pol,d,year))
        careers=self._careers(departed,pol,d)
        out.update(careers);out.update(self.final_tilly_accounting());
        if p.family!='bus':self.patron[:]=-1;self.covert[:]=False
        self.tick+=1
        return out

def simulate(p,seed,scenario,start=1998,end=2042,burn=30):
    w=World(p,seed)
    for _ in range(burn):w.step(scenario,1998)
    return [w.step(scenario,y) for y in range(start,end+1)]

RANGES=dict(rent=(-.8,-.1),capacity=(.01,.06),request_rate=(.1,.7),obligation_pressure=(0.,1.6),
            resource_attraction=(-.2,.8),protection_supply=(0.,.9),adaptation=(0.,.3),emulation=(0.,.3),
            closure_response=(0.,2.),request_pressure=(-.4,.6),exchange_promotion=(0.,1.2),lawful_service=(.01,.15),cohort_integrity=(1.5,3.5))
def draw_params(n,draws,seed=20261118):
    r=np.random.default_rng(seed);columns={k:lo+(hi-lo)*(r.permutation(draws)+r.random(draws))/draws for k,(lo,hi) in RANGES.items()}
    return [Params(n=n,**{k:float(v[i]) for k,v in columns.items()}) for i in range(draws)]
