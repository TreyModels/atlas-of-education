from accounted import Settings,run
from pathlib import Path
import csv,statistics
rows=[]
for lever,values in [('maintenance_factor',(.2,.35,.6,1.)),('military_share',(.04,.08,.16))]:
 for value in values:
  for drought in (False,True):
   for seed in range(40):
    s=Settings(regime='maintenance_only',drought=drought,seed=seed,**{lever:value})
    h=run(s);last=h[-1]
    rows.append(dict(lever=lever,value=value,drought=drought,seed=seed,state_population=last['state_population'],total_population=last['total_population'],canal_condition=last['canal_condition'],shortfall_kg=sum(x['shortfall_kg'] for x in h)))
with (Path(__file__).parent/'sensitivity.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for lever,values in [('maintenance_factor',(.2,.35,.6,1.)),('military_share',(.04,.08,.16))]:
 for value in values:
  sub=[x for x in rows if x['lever']==lever and x['value']==value and x['drought']]
  print(lever,value,'drought median state',round(statistics.median(x['state_population'] for x in sub)), 'shortfall',round(statistics.median(x['shortfall_kg'] for x in sub)))
