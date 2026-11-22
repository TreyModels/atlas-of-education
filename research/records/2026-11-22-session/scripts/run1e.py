"""Does the break appear when the threshold is on FEMALE tertiary enrolment?
GPI_ter = F/M ; total GER = F+M  =>  F = GER*GPI/(1+GPI). Uses Trey's own mechanism."""
import run1c as R, numpy as np
reg=R.regions()
import gzip,json,os
SRC="/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"
def load(n):
    d=json.load(gzip.open(os.path.join(SRC,n+".json.gz")))
    return {(r[0],int(r[1])):float(r[2]) for r in d if r[2] is not None}
ter,gpi,tfr=load("ter"),load("gpi_ter"),load("fertility")
fem={}
for k,v in ter.items():
    g=gpi.get(k)
    if g: fem[k]=v*g/(1+g)
print("female tertiary GER constructed for",len(fem),"country-years")
def rows(thr,keep):
    out=[]
    for iso in sorted({i for (i,y) in fem}):
        if not keep(iso): continue
        ys=sorted(y for (i,y) in tfr if i==iso)
        if len(ys)<18: continue
        vals=[(y,fem[(iso,y)]) for y in ys if (iso,y) in fem]
        below,c=False,None
        for y,v in vals:
            if v<thr: below=True
            elif below and v>=thr and c is None: c=y
        if c is None: continue
        if sum(1 for y in range(c-10,c) if (iso,y) in tfr)<3: continue
        for y in ys:
            k=y-c
            if -15<=k<=30: out.append((iso,y,k,tfr[(iso,y)],c))
    return out
eap=lambda i: reg.get(i)=="East Asia & Pacific"
allc=lambda i: True
for name,keep in (("ALL",allc),("EAST ASIA & PACIFIC",eap)):
    print(f"\n{name}: threshold on FEMALE tertiary GER")
    for thr in (10,15,20,25):
        for K in (15,20):
            r=rows(float(thr),keep)
            if len({x[0] for x in r})<4: print(f" thr{thr} K{K}: too few"); continue
            (c1,s1),(c2,s2),n1,n=R.fit(r,K=K)
            print(f" thr {thr:>2} K{K:>2}: pre {c1:+.4f} change {c2:+.4f} ({s2:.4f}) t={c2/s2 if s2>0 else float('nan'):+5.2f} n={n1}")
