"""Tilly-inspired mechanisms. All coefficients are experimental, all people synthetic."""
import numpy as np
from observation import locate_persons

def logistic(z):return 1/(1+np.exp(-np.clip(z,-35,35)))

class TillyMixin:
    def init_tilly(self):
        self.t_rng=np.random.default_rng(np.random.SeedSequence([self.seed,6301]))
        self.offices=np.arange(self.O,dtype=np.int32)
        self.repeated_supplier=self.t_rng.integers(0,self.S,self.O);self.supplier_tie=np.full(self.O,.1)
        self.debt=np.zeros(self.O);self.creditor=np.full(self.O,-1,np.int64)
        self.shield=np.zeros(self.O);self.paid_support=np.zeros(self.O)
        self.support_to=np.full(self.O,-1,np.int64)
        self.shield_to=np.full(self.O,-1,np.int64)
        self.closure=self.t_rng.uniform(.1,.3,self.p.organizations)
        self.cohort={};self.last_tilly={};self.balance={};self.appointment_writeoff=0.

    def appoint_outsiders(self,scenario):
        """Controlled appointment shock. Old people's cases and obligations retain their IDs."""
        heads=self.pools[0];old=self.person[heads].copy();new=10**12+self.org[heads]
        # Explicitly sever links to departed identities; an office is not its incumbent.
        lost=np.isin(self.creditor,old);self.appointment_writeoff=float(self.debt[lost].sum()+self.debt[heads[~lost[heads]]].sum())
        self.debt[lost]=0.;self.creditor[lost]=-1
        lost_protection=np.isin(self.shield_to,old);self.shield[lost_protection]=0.;self.shield_to[lost_protection]=-1
        linked=np.isin(self.patron,heads);self.patron[linked]=-1;self.covert[linked]=False
        affected=np.isin(self.dst,heads);self.trust[affected]=.05;self.hidden[affected]=False
        self.person[heads]=new;self.integrity[heads]=self.p.cohort_integrity;self.competence[heads]=.8
        self.loyalty[heads]=.9;self.tenure[heads]=0;self.state[heads]=False;self.patron[heads]=-1;self.covert[heads]=False
        self.debt[heads]=0.;self.creditor[heads]=-1;self.shield[heads]=0.;self.paid_support[heads]=0.;self.support_to[heads]=-1;self.shield_to[heads]=-1
        self.receipts[heads]=0.;self.output[heads]=.7;self.expected_detection[heads]=.03
        self.trust[heads]=.05;self.hidden[heads]=False
        # New people have no established personal contacts; weak slot contacts can develop afterward.
        for pid in new:
            self.cohort[int(pid)]=dict(person=int(pid),appointed_tick=self.tick,exposure_years=0,first_act=None,
                first_filing=None,first_true_filing=None,first_false_filing=None,first_true_sanction=None,
                first_false_sanction=None,employment_exit=None,retirement=None,exit_true_case=None,
                initial_integrity=self.p.cohort_integrity,initial_competence=.8,initial_loyalty=.9,
                modeled_prior_misconduct=False,first_dependency=None,first_owed_obligation=None,
                first_act_received_illicit=None,ever_received_illicit=False)
        if scenario=='network_reset':
            self.appointment_writeoff+=float(self.debt.sum());self.debt[:]=0.;self.creditor[:]=-1
            self.trust[:]=.05;self.hidden[:]=False;self.patron[:]=-1;self.covert[:]=False
            self.closure[:]=0.;self.supplier_tie[:]=0.;self.shield[:]=0.;self.paid_support[:]=0.
            # Fresh access identity is drawn with keyed opportunities, without shifting model RNGs.
            from observation import keyed_uniform
            self.repeated_supplier=np.floor(keyed_uniform(self.person,self.seed,self.tick,60)*self.S).astype(int)
            self.support_to[:]=-1;self.shield_to[:]=-1

    def prepare_tilly(self,pol,draw,flow):
        O=self.O;p=self.p;G=p.organizations
        weight=np.ones(O) if pol['equal'] else 1+2*(4-self.rank.astype(float))
        totals=np.bincount(self.org,weights=weight,minlength=G)
        self.relative_control=weight/(totals[self.org]/self.size)
        self.allocation=self.relative_control*flow[self.sector]
        self.balance=dict(opening=float(self.debt.sum()),created=0.,lawful=0.,illicit=0.,writeoff=0.)
        if not pol['obligations']:
            self.balance['writeoff']+=float(self.debt.sum());self.debt[:]=0.;self.creditor[:]=-1
        creditor_slot=locate_persons(self.person,self.creditor)
        invalid=(self.debt>0)&((creditor_slot<0)|(self.creditor==self.person))
        self.balance['writeoff']+=float(self.debt[invalid].sum());self.debt[invalid]=0.;self.creditor[invalid]=-1
        parent=np.maximum(self.parent,0)
        contact=self.dst[np.arange(O),draw['provider_choice']]
        provider=np.where((self.parent>=0)&(draw['provider_mode']<.75),parent,contact)
        demand=pol['demand'] if pol['tilly'] else 0.
        request=(provider!=np.arange(O))&(draw['help']<np.clip(demand*(1+.5*self.closure[self.org]),0,1))
        # Assistance is legitimate; accepting help does not set misconduct.
        assisted=request&(draw['help_deliver']<self.competence[provider])
        parent_person=self.person[provider]
        create=assisted&pol['obligations']&((self.debt<=1e-12)|(self.creditor==parent_person))
        amount=p.obligation_gain*self.allocation*create
        self.creditor[create]=parent_person[create];self.debt+=amount
        self.balance['created']=float(amount.sum())
        self.dependency_exposure=np.bincount(provider[assisted],minlength=O).astype(float)
        exposed_slots=locate_persons(self.person,self.creditor[self.debt>0])
        self.creditor_exposure=np.bincount(exposed_slots[exposed_slots>=0],minlength=O)
        self.debt_exposure=self.debt.copy()
        lawful=np.minimum(self.debt,p.lawful_service*self.competence*self.allocation)
        self.debt-=lawful;self.balance['lawful']=float(lawful.sum())
        self.creditor[self.debt<=1e-12]=-1
        self.incoming=self.dependency_exposure.copy()
        self.request=request;self.assisted=assisted
        self.relational_pressure=(p.obligation_pressure*self.debt/(.5+self.debt)
            +pol['attraction']*np.log(self.relative_control)
            +p.request_pressure*np.log1p(self.incoming))
        if not pol['tilly']:self.relational_pressure[:]=0.

    def track_cohort(self,act,file,true_filing,false_filing,resolved,employment_exit,retired,year,received):
        ids=np.array(list(self.cohort),np.int64);slots=locate_persons(self.person,ids);n=len(ids)
        if not n:return dict(cohort_size=0,cohort_at_risk=0,cohort_acts=0,cohort_ever_act=0,cohort_first_acts=0,
            cohort_true_sanctions=0,cohort_false_sanctions=0,cohort_removed_true=0,cohort_removed_false=0,cohort_retired=0,
            cohort_dependency_share=None,cohort_request_rate=None,cohort_first_act_risk=0,cohort_exchange_acts=0,cohort_debt_share=None)
        dependent=self.creditor_exposure
        true_s=set(map(int,resolved['true_sanctioned_ids']));false_s=set(map(int,resolved['false_sanctioned_ids']))
        true_exit=set(map(int,resolved['true_exit_ids']));false_exit=set(map(int,resolved['false_exit_ids']))
        first=0;present=slots>=0
        first_risk=int(sum(slot>=0 and self.cohort[int(pid)]['first_act'] is None for pid,slot in zip(ids,slots)))
        for pid,slot in zip(ids,slots):
            r=self.cohort[int(pid)]
            if slot>=0:
                r['exposure_years']+=1
                for key,flag in [('first_act',act[slot]),('first_filing',file[slot]),('first_true_filing',true_filing[slot]),('first_false_filing',false_filing[slot]),('first_dependency',dependent[slot]>0),('first_owed_obligation',self.debt_exposure[slot]>0)]:
                    if flag and r[key] is None:
                        r[key]=self.tick
                        if key=='first_act':first+=1;r['first_act_received_illicit']=bool(received[slot]>0)
                if received[slot]>0:r['ever_received_illicit']=True
                if employment_exit[slot]:r['employment_exit']=self.tick;r['exit_true_case']=int(pid) in true_exit
                if retired[slot]:r['retirement']=self.tick
            if int(pid) in true_s and r['first_true_sanction'] is None:r['first_true_sanction']=self.tick
            if int(pid) in false_s and r['first_false_sanction'] is None:r['first_false_sanction']=self.tick
        cohort_rows=list(self.cohort.values());alive=slots[present]
        return dict(cohort_size=n,cohort_at_risk=int(present.sum()),cohort_acts=int(act[alive].sum()),
            cohort_ever_act=sum(r['first_act'] is not None for r in cohort_rows),cohort_first_acts=first,
            cohort_first_act_risk=first_risk,cohort_exchange_acts=int((act[alive]&(received[alive]>0)).sum()),
            cohort_true_sanctions=sum(r['first_true_sanction'] is not None for r in cohort_rows),
            cohort_false_sanctions=sum(r['first_false_sanction'] is not None for r in cohort_rows),
            cohort_removed_true=sum(r['employment_exit'] is not None and r['exit_true_case'] for r in cohort_rows),
            cohort_removed_false=sum(r['employment_exit'] is not None and not r['exit_true_case'] for r in cohort_rows),
            cohort_retired=sum(r['retirement'] is not None for r in cohort_rows),
            cohort_dependency_share=float((dependent[alive]>0).mean()) if len(alive) else None,
            cohort_debt_share=float((self.debt_exposure[alive]>0).mean()) if len(alive) else None,
            cohort_request_rate=float(self.incoming[alive].mean()) if len(alive) else None)

    def finish_tilly(self,act,receipts,output,file,true_filing,false_filing,resolved,employment_exit,retired,pol,draw,year):
        p=self.p;O=self.O;G=p.organizations
        slots=locate_persons(self.person,self.creditor);valid=(slots>=0)&(self.creditor!=self.person)
        safe=np.maximum(slots,0);before=self.debt.copy()
        can_pay=valid&act&act[safe]&pol['obligations']
        paid=np.minimum(self.debt,receipts*p.settlement_fraction)*can_pay
        self.debt-=paid;self.balance['illicit']=float(paid.sum())
        received=np.bincount(safe[valid],weights=paid[valid],minlength=O)
        net=receipts-paid+received
        assert np.isclose(net.sum(),receipts.sum(),rtol=1e-10,atol=1e-8)
        self.paid_support=paid/(.1+before)
        self.support_to=np.where(paid>0,self.creditor,-1)
        self.receipts=.7*self.receipts+.3*net
        supply=p.protection_supply*paid/(.1+before)
        same=(paid<=0)|(self.shield_to==self.creditor)
        self.shield*=same
        self.shield_to=np.where(paid>0,self.creditor,self.shield_to)
        self.shield=np.clip(.8*self.shield+.2*supply,0,.95) if pol['protection_exchange'] else np.zeros(O)
        self.shield_to[self.shield<=0]=-1
        self.creditor[self.debt<=1e-12]=-1
        load=np.bincount(self.org,weights=self.request,minlength=G)/self.size
        org_output=np.bincount(self.org,weights=output,minlength=G)/self.size
        org_filing=np.bincount(self.org,weights=file,minlength=G)/self.size
        signal=org_output-2*org_filing
        routine=self.closure.copy()
        if pol['adapt']:
            target=logistic(-1+2*p.closure_response*load+.5*routine)
            routine=(1-p.adaptation)*routine+p.adaptation*target
        if pol['emulate']:
            other=draw['model_org'];copy=(signal[other]>signal)&(draw['emulate']<p.emulation)
            routine=np.where(copy,self.closure[other],routine)
        self.closure=np.clip(routine,0,1) if pol['access'] else np.zeros(G)
        metrics=dict(mean_obligation=float(self.debt.mean()),assistance_share=float(self.assisted.mean()),
            dependent_share=float((self.debt>0).mean()),mean_closure=float(self.closure.mean()),
            resource_allocated=float(self.allocation.sum()),resource_diverted=float(receipts.sum()),
            resource_delivered=float(self.last_contract['delivered'].sum()),illicit_transferred=float(paid.sum()),
            net_private_receipts=float(net.sum()),mean_exchange_shield=float(self.shield.mean()),
            requests_per_official=float(self.request.mean()),appointment_debt_writeoff=self.appointment_writeoff)
        self.appointment_writeoff=0.
        metrics.update(self.track_cohort(act,file,true_filing,false_filing,resolved,employment_exit,retired,year,received))
        for rank in range(5):
            ix=self.rank==rank
            metrics[f'rank{rank}_misconduct']=float(act[ix].mean())
            metrics[f'rank{rank}_extraction_per_official']=float(receipts[ix].mean())
            metrics[f'rank{rank}_extraction_per_resource']=float(receipts[ix].sum()/self.allocation[ix].sum())
            metrics[f'rank{rank}_requests_per_official']=float(self.incoming[ix].mean())
        self.last_tilly=dict(paid=paid,received=received,net=net,creditor_slots=slots,act=act.copy(),before=before)
        return metrics

    def remap_tilly(self,source,fresh,old_person,pol):
        safe=np.maximum(source,0);departed=np.ones(self.O,bool);departed[source[~fresh]]=False
        self.balance['writeoff']+=float(self.debt[departed].sum())
        for name in ['debt','creditor','shield','paid_support','support_to','shield_to']:
            x=getattr(self,name)[safe].copy();x[fresh]=-1 if name in ('creditor','support_to','shield_to') else 0.;setattr(self,name,x)
        gone=(self.debt>0)&~np.isin(self.creditor,self.person)
        self.balance['writeoff']+=float(self.debt[gone].sum());self.debt[gone]=0.;self.creditor[gone]=-1
        unsupported=~np.isin(self.shield_to,self.person);self.shield[unsupported]=0.;self.shield_to[unsupported]=-1

    def final_tilly_accounting(self):
        b=self.balance;closing=float(self.debt.sum())
        residual=b['opening']+b['created']-b['lawful']-b['illicit']-b['writeoff']-closing
        if not np.isclose(residual,0.,atol=1e-7):raise AssertionError(('Obligation balance',b,closing,residual))
        return dict(obligation_opening=b['opening'],obligation_created=b['created'],obligation_lawful=b['lawful'],
            obligation_illicit=b['illicit'],obligation_writeoff=b['writeoff'],obligation_closing=closing,obligation_residual=float(residual))
