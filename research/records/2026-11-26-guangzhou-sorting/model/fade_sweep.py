import sys,json,numpy as np;sys.path.insert(0,'/home/claude/sig')
import gz_v3 as m, run_v31 as r
mid={k:(a+b)/2 for k,(a,b) in r.R.items()}
out=[]
for va in (0.1,0.4):
  for dc in np.round(np.linspace(0,0.9,10),2):
    rows=[r.metrics(m.run(n=40000,seed=s,**{**mid,'HS_TEACH_SD':mid['TEACH_SD'],'DECAY':float(dc),'SCHOOL_VA':va})) for s in range(4)]
    a={k:float(np.mean([x[k] for x in rows])) for k in ('EO_local','EO_equal_zk','EO_uncond','HUKOU_ratio')}
    a.update(DECAY=float(dc),SCHOOL_VA=va); out.append(a)
    print(f"VA {va} fade {dc:.1f}: equal talent {a['EO_local']:.2f}  equal zhongkao {a['EO_equal_zk']:.2f}  unconditional {a['EO_uncond']:.2f}  hukou {a['HUKOU_ratio']:.2f}",flush=True)
json.dump(out,open('/home/claude/sig/fade_results.json','w'),indent=1)
