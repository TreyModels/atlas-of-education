import json, numpy as np
D="/root/work/data"
def series(name):
    d=json.load(open(f"{D}/{name}.json")); out={}
    for iso,y,v in d:
        if v is None: continue
        try: out.setdefault(iso,{})[int(y)]=float(v)
        except Exception: pass
    return out
F=series("fertility")
ev=[]; starts=[]
for iso,d in F.items():
    if len(d)<35: continue
    ys=sorted(d); v=np.array([d[y] for y in ys])
    best,bt=0.0,None
    for i in range(len(ys)-10):
        if ys[i+10]-ys[i]!=10: continue
        fall=v[i]-v[i+10]
        if fall>best: best,bt=fall,ys[i]
    if bt is not None and best>=1.0: ev.append((iso,bt,best,ys[0],ys[-1]))
print("events:",len(ev))
ey=np.array([e[1] for e in ev]); print("event year: min %d p25 %d median %d p75 %d max %d"%(ey.min(),np.quantile(ey,.25),np.median(ey),np.quantile(ey,.75),ey.max()))
st=np.array([e[3] for e in ev]); print("series start: median %d"%np.median(st))
print("events at start+<20:", int(((ey-st)<20).sum()), "of", len(ev))
print("events with start+20 <= event <= end-10:", int((((ey-st)>=20)&(ey<=np.array([e[4] for e in ev])-10)).sum()))
