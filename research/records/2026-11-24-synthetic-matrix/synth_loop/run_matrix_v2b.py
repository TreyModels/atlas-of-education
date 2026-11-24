import os
os.environ.update({"OMP_NUM_THREADS":"1","MKL_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1"})
import json, sys, time, math, multiprocessing as mp, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); REC=os.path.dirname(HERE); RES=os.path.join(REC,"results"); sys.path.insert(0,HERE)
import model
model.LITERATURE["Rm"]=dict(model.LITERATURE["R"], div=0.02)
model.DELTAS["Rm"]={k:model.LITERATURE["Rm"][k]-model.THETA0[k] for k in model.THETA0}
model.WORLD_FIXED["Rm"]=dict(model.WORLD_FIXED["R"])
WORLDS=("P","S","C","R","Rm"); LINKS=("cl","sw","wo","hw","tut","learn","inc")
NH=100_000; NC=512; T=25; BLOCKS=tuple(range(10)); SEED0=20261124
CACHE=os.path.join(REC,"cache_v2b"); CELLD=os.path.join(REC,"cells_v2b")
os.makedirs(CACHE,exist_ok=True); os.makedirs(CELLD,exist_ok=True); os.makedirs(RES,exist_ok=True)
RANGES=dict(sigma_y=(0.25,0.95),sigma_a=(0.08,0.45),mu_y=(-0.4,0.5),mu_a=(0.7,1.5),w_child=(0.02,0.5),shadow_cost=(0.1,0.7),f_pub_pre=(0.0,0.45),y_sub0=(0.55,1.25))
TYPES=[(0.45,0.18,-0.10,0.95,0.10,0.25,0.12,0.75),(0.65,0.25,0.10,1.05,0.20,0.35,0.20,0.85),(0.35,0.15,-0.20,0.90,0.05,0.20,0.08,0.70),(0.75,0.30,0.20,1.10,0.30,0.45,0.30,0.95),(0.55,0.22,0.00,1.00,0.15,0.30,0.15,0.80),(0.50,0.20,0.05,1.02,0.10,0.40,0.25,0.90),(0.60,0.28,-0.05,1.08,0.25,0.28,0.10,0.75),(0.40,0.16,0.15,0.92,0.08,0.22,0.05,0.65)]
def nuis_all():
    rng=np.random.default_rng(SEED0); out=[]
    for c in range(NC):
        base=dict(zip(RANGES,TYPES[c%8])); out.append({k:float(np.clip(base[k]+rng.normal(0,0.05),*RANGES[k])) for k in RANGES})
    return out
NUIS=nuis_all()
def series_task(args):
    w,c0,c1,k=args; out={}
    for c in range(c0,c1):
        res=model.run_unit(w,1,20270101+100*c,n=NH,years=T,**NUIS[c]); s=res["state"]
        out[c]={"cl":np.isin(s,(1,2)).mean(1),"sw":(s==1).mean(1),"wo":(s==2).mean(1),"hw":(s==3).mean(1),"tut":res["tutor"].mean(1),"learn":res["learn"].mean(1),"inc":res["y_hh"].mean(1),"ger":(s<=1).mean(1)}
    p=os.path.join(CACHE,f"{w}_{k}.npz"); np.savez(p,**{f"{c}_{L}":out[c][L] for c in out for L in out[c]})
    return p
_G={}
def init_cells(cache_list):
    import glob
    for p in glob.glob(os.path.join(CACHE,"*.npz")):
        w=os.path.basename(p).split("_")[0]; z=np.load(p)
        for k in z.files:
            c,L=k.split("_"); _G.setdefault(w,{}).setdefault(L,{})[int(c)]=z[k]
def rows(L,w,spec,cs,dose,rngseed):
    rng=np.random.default_rng(rngseed); out=[]
    for c in cs:
        y=_G[w][L][c].astype(float); g=_G[w]["ger"][c].astype(float)
        if dose>0: y=y*np.exp(rng.normal(0,dose,y.shape)); g=g*np.exp(rng.normal(0,dose,g.shape))
        for t in range(5,T):
            if spec.startswith("S5"): out.append((c,1+(t-5)//5,y[t]-y[t-5],g[t]-g[t-5]))
            elif t>=10: out.append((c,1 if t<15 else (2 if t<20 else 3),y[t]-y[t-10],g[t]-g[t-10]))
    return np.array(out,float)
def ols(y,X,G):
    n,k=X.shape; b,*_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b; Xi=np.linalg.inv(X.T@X); m=np.zeros((k,k))
    for g in np.unique(G):
        z=G==g; s=X[z].T@e[z]; m+=np.outer(s,s)
    return b,Xi@m@Xi*(len(np.unique(G))/(len(np.unique(G))-1))*((n-1)/(n-k))
def cell_task(args):
    gname,groups,spec,dose,bi=args; outp=os.path.join(CELLD,f"c_{abs(hash((gname,spec,dose,bi)))%10**9}.jsonl"); f=open(outp,"w")
    n=0
    for L in LINKS:
        est={}
        for w in WORLDS:
            bs=[]; ss=[]
            for gi,grp in enumerate(groups):
                A=rows(L,w,spec,grp,dose,SEED0+abs(hash((gname,spec,dose,bi,w,L,gi)))%99999)
                if len(A)<40: continue
                C=A[:,0].astype(int); F=A[:,1].astype(int); cols=[np.ones(len(A)),A[:,3]]
                if spec.startswith("S5"): cols+=[(F==b).astype(float) for b in (2,3,4)]
                else: cols+=[(F==2).astype(float),(F==3).astype(float)]
                b,V=ols(A[:,2],np.column_stack(cols),C); bs.append(float(b[1])); ss.append(float(np.sqrt(max(V[1,1],0))))
            est[w]=(float(np.mean(bs)) if bs else None,float(np.sqrt(np.mean(np.square(ss)))) if ss else None)
        ws=[w for w in WORLDS if est[w][0] is not None and est[w][1] is not None]
        ind=all(abs(est[a][0]-est[b][0])<=1.96*math.hypot(est[a][1],est[b][1]) for i,a in enumerate(ws) for b in ws[i+1:]) if len(ws)>1 else False
        f.write(json.dumps({"g":gname,"spec":spec,"dose":dose,"block":bi,"link":L,"est":{w:list(est[w]) for w in est},"ind":ind})+"\n"); n+=1
    f.close(); return outp
def agg_task(paths):
    n=ind=0; ladder={}; rob={}
    for p in paths:
        for line in open(p):
            r=json.loads(line); n+=1; ind+=int(r["ind"])
            key=f'{r["dose"]}'; ladder.setdefault(key,[0,0]); ladder[key][0]+=int(r["ind"]); ladder[key][1]+=1
            for w,(b,se) in r["est"].items():
                if b is None: continue
                k=(w,r["link"],r["spec"],r["dose"]); rob.setdefault(k,[]).append(np.sign(b))
    return {"n":n,"ind":ind,"ladder":{k:{"share":v[0]/v[1] if v[1] else None,"n":v[1]} for k,v in ladder.items()},"robust_sign":{str(k):[float(np.mean([1 if x>0 else 0 for x in v])),len(v)] for k,v in rob.items()}}
def main():
    t0=time.time(); nw=mp.cpu_count(); print("nproc",nw,"NH",NH,"NC",NC,flush=True)
    chunks=[]
    for w in WORLDS:
        step=64
        for k,c0 in enumerate(range(0,NC,step)): chunks.append((w,c0,min(c0+step,NC),k))
    with mp.Pool(nw) as pool: paths=pool.map(series_task,chunks)
    print("series",len(paths),"files",round(time.time()-t0,1),"s",flush=True)
    rng=np.random.default_rng(SEED0); groupings={}
    for i in range(64):
        p=rng.permutation(NC); groupings[f"r{i:02d}"]=[sorted(p[g*(NC//4):(g+1)*(NC//4)].tolist()) for g in range(4)]
    for ti in range(8):
        idx=[c for c in range(NC) if c%8==ti]; half=len(idx)//2
        for h in range(2): groupings[f"t{ti}_{h}"]=[sorted(idx[:half]),sorted(idx[half:])]
    specs=("S1_10y","S2_5y","S5_5y"); doses=(0.0,0.05,0.10)
    tasks=[(gn,groups,spec,dose,bi) for gn,groups in groupings.items() for spec in specs for dose in doses for bi in BLOCKS]
    with mp.Pool(nw,initializer=init_cells,initargs=(paths,)) as pool:
        cps=pool.map(cell_task,tasks,chunksize=1)
    print("cells",len(cps),"files",round(time.time()-t0,1),"s",flush=True)
    # seed-block dimension handled inside tasks; aggregate with a parallel scan over cell files
    with mp.Pool(nw) as pool:
        parts=pool.map(agg_task,[ [p] for p in cps ])
    n=sum(p["n"] for p in parts); ind=sum(p["ind"] for p in parts); ladder={}
    for p in parts:
        for k,v in p["ladder"].items(): ladder.setdefault(k,[0,0]); ladder[k][0]+=0 if v["share"] is None else round(v["share"]*v["n"]); ladder[k][1]+=v["n"]
    share=ind/n; rngb=np.random.default_rng(7); boot=[]
    for _ in range(400): boot.append(rngb.binomial(n,share)/n)
    lo,hi=np.percentile(boot,[2.5,97.5])
    summary={"design":{"worlds":list(WORLDS),"NH":NH,"NC":NC,"groupings":len(groupings),"specs":list(specs),"doses":list(doses),"blocks":list(BLOCKS),"links":len(LINKS)},"n_cells":n,"n_indistinguishable":ind,"cross_world_indistinguishable_share":share,"ci95":[float(lo),float(hi)],"wall_rule":0.75,"wall_verdict":"wall" if share>=0.75 else "separable","dose_ladder":{k:{"share":(v[0]/v[1] if v[1] else None),"n":v[1]} for k,v in ladder.items()},"label":"SIMULATION","wall_s":round(time.time()-t0,1),"workers":nw,"numpy":np.__version__}
    json.dump(summary,open(os.path.join(RES,"matrix_v2b_summary.json"),"w"),indent=1)
    print("SUMMARY",json.dumps({k:summary[k] for k in ("n_cells","cross_world_indistinguishable_share","ci95","wall_verdict","wall_s")}),flush=True)
if __name__=="__main__": main()
