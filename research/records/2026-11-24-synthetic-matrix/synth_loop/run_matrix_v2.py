import os
os.environ.update({"OMP_NUM_THREADS":"1","MKL_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1"})
import json, sys, time, multiprocessing as mp, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); REC=os.path.dirname(HERE); RES=os.path.join(REC,"results"); sys.path.insert(0,HERE)
import model
model.LITERATURE["Rm"]=dict(model.LITERATURE["R"], div=0.02); model.DELTAS["Rm"]={k:model.LITERATURE["Rm"][k]-model.THETA0[k] for k in model.THETA0}; model.WORLD_FIXED["Rm"]=dict(model.WORLD_FIXED["R"])
WORLDS=("P","S","C","R","Rm"); N=256; YEARS=25; SEED=20261124
TYPES=[(0.45,0.18,-0.10,0.95,0.10,0.25,0.12,0.75),(0.65,0.25,0.10,1.05,0.20,0.35,0.20,0.85),(0.35,0.15,-0.20,0.90,0.05,0.20,0.08,0.70),(0.75,0.30,0.20,1.10,0.30,0.45,0.30,0.95),(0.55,0.22,0.00,1.00,0.15,0.30,0.15,0.80),(0.50,0.20,0.05,1.02,0.10,0.40,0.25,0.90),(0.60,0.28,-0.05,1.08,0.25,0.28,0.10,0.75),(0.40,0.16,0.15,0.92,0.08,0.22,0.05,0.65)]
RANGES=dict(sigma_y=(0.25,0.95),sigma_a=(0.08,0.45),mu_y=(-0.4,0.5),mu_a=(0.7,1.5),w_child=(0.02,0.5),shadow_cost=(0.1,0.7),f_pub_pre=(0.0,0.45),y_sub0=(0.55,1.25))
def make_nuis():
    rng=np.random.default_rng(SEED); out=[]
    for c in range(N):
        base=dict(zip(RANGES, TYPES[c%8])); d={k: float(np.clip(base[k]+rng.normal(0,0.05), *RANGES[k])) for k in RANGES}; out.append(d)
    return out
NUIS=make_nuis()
def links(res):
    s=res["state"]; y={"cl":np.isin(s,(1,2)).mean(1),"sw":(s==1).mean(1),"wo":(s==2).mean(1),"hw":(s==3).mean(1),"tut":res["tutor"].mean(1),"learn":res["learn"].mean(1),"inc":res["y_hh"].mean(1),"ger":(s<=1).mean(1)}; return {k:v.astype(float) for k,v in y.items()}
def series_chunk(args):
    w,cs=args; out={}
    for c in cs:
        out[c]=links(model.run_unit(w,1,20270101+100*c,years=YEARS,**NUIS[c]))
    return w,out
SERIES={}
def add_measure(series, sig, rng):
    return {L: v*np.exp(rng.normal(0,sig,size=v.shape)) for L,v in series.items()}
def rows(link, ger, spec, cs, sig, rngseed):
    rng=np.random.default_rng(rngseed); rr=[]
    for c in cs:
        y=link[c]; g=ger[c]
        if sig>0: y=add_measure({0:y},sig,rng)[0]; g=add_measure({0:g},sig,rng)[0]
        if spec=="S1": 
            for t in range(10,YEARS): rr.append((c,1 if t<15 else (2 if t<20 else 3),y[t]-y[t-10],g[t]-g[t-10],0))
        elif spec=="S2":
            for t in range(5,YEARS): rr.append((c,1+(t-5)//5,y[t]-y[t-5],g[t]-g[t-5],0))
        elif spec=="S3":
            for t in range(YEARS): rr.append((c,t,y[t],g[t],0))
        else:
            for t in range(10,YEARS): rr.append((c,1 if t<15 else (2 if t<20 else 3),y[t]-y[t-10],g[t]-g[t-10],0))
    return np.array(rr,float)
def ols(y,X,G):
    n,k=X.shape; beta,*_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta; XtXi=np.linalg.inv(X.T@X); meat=np.zeros((k,k))
    for g in np.unique(G):
        m=G==g; s=X[m].T@e[m]; meat+=np.outer(s,s)
    V=XtXi@meat@XtXi*(len(np.unique(G))/(len(np.unique(G))-1))*((n-1)/(n-k)); return beta,V
def cell_task(args):
    gname,groups,spec,dose,bidx=args; out=[]
    for L in ("cl","sw","wo","hw","tut","learn","inc"):
        est={}
        for w in WORLDS:
            betas=[]; ses=[]
            for gi,grp in enumerate(groups):
                A=rows(SERIES[w][L],SERIES[w]["ger"],spec,grp,dose,(SEED+hash((gname,spec,dose,bidx,w,L,gi))%100000))
                if len(A)<30: continue
                C=A[:,0].astype(int); F=A[:,1].astype(int); yv=A[:,2]; x=A[:,3]
                cols=[np.ones(len(A)),x]
                if spec in ("S1","S4"): cols+=[(F==2).astype(float),(F==3).astype(float)]
                elif spec=="S2": cols+=[(F==b).astype(float) for b in (2,3,4)]
                else:
                    for c in sorted(set(C.tolist())): cols.append((C==c).astype(float))
                    for t in range(1,YEARS): cols.append((F==t).astype(float))
                X=np.column_stack(cols); beta,V=ols(yv,X,C); betas.append(float(beta[1])); ses.append(float(np.sqrt(V[1,1])))
            est[w]=(float(np.mean(betas)) if betas else None, float(np.sqrt(np.mean(np.square(ses)))) if ses else None)
        ws=[w for w in WORLDS if est[w][0] is not None and est[w][1] is not None]
        ind=all(abs(est[a][0]-est[b][0])<=1.96*np.hypot(est[a][1],est[b][1]) for i,a in enumerate(ws) for b in ws[i+1:]) if len(ws)>1 else False
        out.append({"grouping":gname,"spec":spec,"dose":dose,"block":bidx,"link":L,"est":est,"indistinguishable":bool(ind)})
    return out
def main():
    t0=time.time(); os.makedirs(RES,exist_ok=True); nw=min(96,mp.cpu_count()); print("nproc",mp.cpu_count(),"workers",nw,flush=True)
    rng=np.random.default_rng(SEED)
    groupings={}
    for i in range(32):
        p=rng.permutation(N); groupings[f"r{i:02d}"]=[sorted(p[g*64:(g+1)*64].tolist()) for g in range(4)]
    for ti in range(4):
        idx=[c for c in range(N) if c%8==ti]
        for half in range(2): groupings[f"t{ti}_{half}"]=[sorted(idx[:16]),sorted(idx[16:])]
    RAW={}
    for w in WORLDS:
        for c0 in range(0,N,16):
            _,out=series_chunk((w,list(range(c0,min(c0+16,N)))))
            RAW.setdefault(w,{}).update(out)
    for w in WORLDS:
        SERIES[w]={L:{c:RAW[w][c][L] for c in RAW[w]} for L in ("cl","sw","wo","hw","tut","learn","inc","ger")}
    print("series done",round(time.time()-t0,1),"s",flush=True)
    tasks=[(gn,groups,spec,dose,bidx) for gn,groups in groupings.items() for spec in ("S1","S2","S3","S4") for dose in (0.0,0.05,0.10) for bidx in (1,2)]
    cells=[]
    with mp.Pool(nw) as pool:
        for out in pool.imap_unordered(cell_task,tasks,chunksize=1): cells.extend(out)
    n=len(cells); ind=sum(1 for c in cells if c["indistinguishable"])
    by_dose={f"{d}": [c for c in cells if c["dose"]==d] for d in (0.0,0.05,0.10)}
    ladder={k:{"n":len(v),"share":sum(1 for c in v if c["indistinguishable"])/len(v) if v else None} for k,v in by_dose.items()}
    robust={}
    for w in WORLDS:
        cnt=0; tot=0
        for L in ("cl","sw","wo","hw","tut","learn","inc"):
            for spec in ("S1","S2","S3","S4"):
                for dose in (0.0,0.05,0.10):
                    same=[c for c in cells if c["link"]==L and c["spec"]==spec and c["dose"]==dose]
                    ref=np.mean([c["est"][w][0] for c in same if c["est"][w][0] is not None])
                    ok=sum(1 for c in same if c["est"][w][0] is not None and np.sign(c["est"][w][0])==np.sign(ref) and abs(c["est"][w][0]/max(c["est"][w][1],1e-9))>1.96)
                    cnt+=int(ok>=0.8*len(same)); tot+=1
        robust[w]={"n_robust":cnt,"n_links":tot,"share":cnt/tot if tot else None}
    summ={"design":{"n_countries":N,"worlds":list(WORLDS),"links":7,"groupings":len(groupings),"specs":4,"doses":[0.0,0.05,0.10],"blocks":[1,2]},"n_cells":n,"n_indistinguishable":ind,"cross_world_indistinguishable_share":ind/n,"wall_rule":0.75,"wall_verdict":"wall" if ind/n>=0.75 else "separable","dose_ladder":ladder,"robust_across_groupings":robust,"label":"SIMULATION","workers":nw,"nproc":mp.cpu_count()}
    json.dump(summ,open(os.path.join(RES,"matrix_v2_summary.json"),"w"),indent=1); json.dump(cells,open(os.path.join(RES,"matrix_v2_cells.json"),"w"),indent=1)
    json.dump({"wall_s":round(time.time()-t0,1),"nproc":mp.cpu_count(),"workers":nw,"numpy":np.__version__,"python":sys.version.split()[0],"seed":SEED,"label":"SIMULATION"},open(os.path.join(RES,"run_manifest_v2.json"),"w"),indent=1)
    print("SUMMARY",json.dumps({k:summ[k] for k in ("n_cells","n_indistinguishable","cross_world_indistinguishable_share","wall_verdict")})); print("LADDER",ladder); print("ROBUST",{w:robust[w]["n_robust"] for w in WORLDS}); print("wall",round(time.time()-t0,1))
if __name__=="__main__": main()
