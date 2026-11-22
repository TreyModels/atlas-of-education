import battery as B, numpy as np
V,F=B.V,B.F
CAND=B.CAND
def rows(c):
    out=[]
    for (i,t),v in F.items():
        if (i,t+10) in F and (i,t) in V[c]:
            out.append((i,t,F[(i,t+10)]-v,V[c][(i,t)]))
    return out
print("="*74)
print("A. ONE AT A TIME, country against itself, NO starting-level control")
print("   (% of the fall in births explained)")
print("="*74)
r=[]
for c in CAND:
    w=rows(c)
    if len(w)<300: continue
    y=np.array([x[2] for x in w]); x=np.array([x[3] for x in w])
    iso=[x2[0] for x2 in w]; yr=[x2[1] for x2 in w]
    def dm(v,g):
        m={}
        for a,b in zip(v,g): m.setdefault(b,[]).append(a)
        mu={k:np.mean(z) for k,z in m.items()}
        return np.array([a-mu[b] for a,b in zip(v,g)])
    xw=dm(dm(x,iso),yr); yw=dm(dm(y,iso),yr)
    s = 0 if xw.std()==0 else np.corrcoef(xw,yw)[0,1]
    r.append((c,s*s*100,len(w)))
for c,s2,n in sorted(r,key=lambda z:-z[1]):
    print(f"  {B.NAME[c]:32s} {s2:5.1f}%   (n={n})")
print()
print("="*74)
print("B. WHEN did the fall start, and what predicted starting early?")
print("   (no level control anywhere — pure timing)")
print("="*74)
def onset(iso,thr=5.0):
    ys=sorted(y for (i,y) in F if i==iso)
    for y in ys:
        if F[(iso,y)]<thr: return y
    return None
st=[(iso,onset(iso)) for iso in {i for (i,y) in F}]
st=[(i,y) for i,y in st if y and 1950<=y<=2020]
print(f"  {len(st)} countries fell below 5 children/woman")
for c in ["ter","sec","lsc","gpi_ter","flfp","wage_emp","urban","gdppc_log","u5mr","electricity","lit_adult"]:
    xs,yy=[],[]
    for iso,yy0 in st:
        v,yr=B.V[c],None
        for d in range(0,11):
            if (iso,yy0-20-d) in v: yr=yy0-20-d; break
        if yr is None: continue
        xs.append(v[(iso,yr)]); yy.append(yy0)
    if len(xs)<25: continue
    cr=np.corrcoef(xs,yy)[0,1]
    print(f"  higher {B.NAME[c]:30s} 20yrs before onset -> onset {'earlier' if cr<0 else 'LATER  '} (r={cr:+.2f}, n={len(xs)})")
