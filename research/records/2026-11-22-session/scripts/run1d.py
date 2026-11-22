import run1c as R, numpy as np
reg=R.regions()
eap=lambda i: reg.get(i)=="East Asia & Pacific"
print("EAST ASIA & PACIFIC robustness — hinge change at knot K (negative = steepens)\n")
print(f"{'thr':>4} {'K':>4} {'pre':>8} {'change':>8} {'se':>7} {'t':>6}  n")
for thr in (15,20,25,30):
    for K in (5,10,15,20):
        rows=R.rows_for(float(thr),eap)
        if len({r[0] for r in rows})<4: print(f"{thr:>4} {K:>4}   too few"); continue
        (c1,s1),(c2,s2),ncty,n=R.fit(rows,K=K)
        print(f"{thr:>4} {K:>4} {c1:+8.4f} {c2:+8.4f} {s2:7.4f} {c2/s2 if s2>0 else float('nan'):+6.2f}  {ncty}")
# placebo for EAP
print("\nEAP placebo (crossings moved 10y earlier), thr=20, K=15:")
ter,tfr=R.load("ter"),R.load("fertility")
import copy
orig=R.rows_for
def rf(thr,keep,shift=-10):
    import json
    t,tf=R.load("ter"),R.load("fertility"); out=[]
    for iso in sorted({i for (i,y) in t}):
        if not keep(iso): continue
        ys=sorted(y for (i,y) in tf if i==iso)
        if len(ys)<18: continue
        vals=[(y,t[(iso,y)]) for y in ys if (iso,y) in t]
        below,c=False,None
        for y,v in vals:
            if v<thr: below=True
            elif below and v>=thr and c is None: c=y
        if c is None: continue
        c+=shift
        if sum(1 for y in range(c-10,c) if (iso,y) in tf)<3: continue
        for y in ys:
            k=y-c
            if -15<=k<=30: out.append((iso,y,k,tf[(iso,y)],c))
    return out
(c1,s1),(c2,s2),ncty,n=R.fit(rf(20.0,eap),K=15)
print(f"  pre {c1:+.4f} change {c2:+.4f} ({s2:.4f}) t={c2/s2 if s2>0 else float('nan'):+.2f} n={ncty}")
