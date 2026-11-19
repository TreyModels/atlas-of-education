"""Economic anchors with explicit vintage and scope. No imputation of early history."""
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parent
class Evidence:
    def __init__(self,use=True):
        self.use=use
        d=pd.read_csv(P/'data/verified_observations.csv')
        self.land=d[d.variable=='land_revenue'].set_index('year').value.to_dict()
        self.fin=d[d.variable=='rmb_loans_to_real_economy_increment'].set_index('year').value.to_dict()
        self.records=d
    def flows(self,year):
        if not self.use:return [1.,1.,1.,1.,1.]
        # Before the first verified observation the factor is a declared normalized assumption.
        land=self.land.get(year,self.land[max(self.land)] if year>max(self.land) else self.land[min(self.land)])
        fin=self.fin.get(year,self.fin[max(self.fin)] if year>max(self.fin) else self.fin[min(self.fin)])
        # 2026 is an approved central budget, not observed actual procurement expenditure.
        defense=1.909561/1.784665 if year>=2026 else 1.
        return [defense,land/self.land[min(self.land)],fin/self.fin[min(self.fin)],1.,1.]
