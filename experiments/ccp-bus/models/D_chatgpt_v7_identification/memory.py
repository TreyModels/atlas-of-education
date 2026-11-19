"""Original social-trap mechanisms expressed in the audited V6 identity kernel."""
from dataclasses import replace
import numpy as np

FAMILIES=('current_incentives','social_trap','bus')
def configure(p,family):
    if family not in FAMILIES:raise ValueError(family)
    return replace(p,family=family,request_rate=0.,obligation_pressure=0.,request_pressure=0.,resource_attraction=0.,
        adaptation=0.,emulation=0.,protection_supply=0.,exchange_promotion=0.,entry_bias=0.,
        concealment_cost=0.,coordination=0.,productive_patronage=False,protection=0.,report_suppression=0.,
        network_weight=0.,performance_weight=0.,peer=0. if family=='current_incentives' else p.peer,
        report_capture=0. if family=='current_incentives' else p.report_capture,
        informality=.7 if family=='bus' else 0.,memory=.6 if family=='bus' else 0.,
        rewiring=.15 if family=='bus' else 0.,empirical_flows=False)

class MemoryMixin:
    def prepare_memory(self,policy):
        # Private local knowledge is an explicit assumption, as in the original kernel.
        contact=self.state[self.dst].mean(axis=1)
        organization=np.bincount(self.org,weights=self.state,minlength=self.p.organizations)/self.size
        self.memory_peer=.5*contact+.5*organization[self.org]
        cap=policy['capacity']*(.5+self.e)
        if self.p.family=='current_incentives':
            self.expected_detection=np.full(self.O,min(.95,.85*cap))
            return np.zeros(self.O)
        # A fixed investigative resource is spread over locally perceived wrongdoing.
        congestion=np.minimum(1.,cap/np.maximum(self.memory_peer,1/self.O))
        self.expected_detection=np.clip(self.e*(1-self.p.report_capture*self.memory_peer)*congestion,0,.95)
        return self.memory_peer
