"""Explicitly separated training drivers and forecast/conditional input paths."""
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parent
class Evidence:
    def __init__(self,use=False):
        if use:raise ValueError('Use an explicit LandDriver with a declared information set')
    def flows(self,year):return [1.,1.,1.,1.,1.]

class LandDriver:
    def __init__(self,records,mode='strict',cutoff=2019):
        if mode not in ('strict','conditional'):raise ValueError(mode)
        self.mode=mode;self.cutoff=cutoff
        data=records.copy()
        if mode=='strict':data=data[data.year<=cutoff]
        self.land=data.set_index('year').value.to_dict();self.first=min(self.land);self.last=max(self.land)
        self.anchor=self.land[self.first]
    def flows(self,year):
        # Before observed history, declare a fixed normalized baseline.
        value=self.land.get(year,self.land[self.last] if year>self.last else self.land[self.first])
        return [1.,value/self.anchor,1.,1.,1.]
