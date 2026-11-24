import json, os, sys, time, subprocess
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); REC=os.path.dirname(HERE); RES=os.path.join(REC,"results"); sys.path.insert(0,HERE)
import model, fertility
countries=72
PHASE_A=os.path.join(REC,"..","2026-11-24-synthetic-loop","results","calibration.json")
cal=json.load(open(PHASE_A)); NUIS={w:cal["cells"][w]["chosen"]["nuisance"] for w in model.WORLDS}; NUIS["s0"]=cal["cells"]["s0"]["chosen"]["nuisance"]
def jable(o):
    if isinstance(o,(np.floating,)): return float(o)
    if isinstance(o,(np.integer,)): return int(o)
    if isinstance(o,np.ndarray): return o.tolist()
    if isinstance(o,dict): return {k:jable(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [jable(v) for v in o]
    return o
SEED_K=lambda k: 20261125+100*int(k)
def unit(world,s,seed):
    nuis=NUIS["s0"] if s==0 else NUIS[world]
    res=model.run_unit(world if s==1 else "P", 0 if s==0 else 1, seed, **nuis)
    ys=model.year_stats(res); return fertility.simulate(world,s,seed,float(ys["ger"][15:].mean()),float(ys["cl_observed"][15:].mean()))
def block(block_seeds,s=1):
    out=[]
    for k in block_seeds:
        seed=SEED_K(k)
        for w in model.WORLDS:
            if s==0:
                u=unit(w,0,seed)  # identical across labels at s=0
            else: u=unit(w,1,seed)
            out.append({"world":w,"seed":seed,**u})
    return out
CAL=list(range(0,20)); HELD=list(range(20,80)); REPL=list(range(80,140))
def features(units,keys=("B1","B2","B3")):
    X=np.array([[u[k] for k in keys] for u in units],float); y=np.array([u["world"] for u in units]); return X,y
def classify(tr,te):
    Xtr,ytr=features(tr); Xte,yte=features(te); mu,sd=Xtr.mean(0),Xtr.std(0); sd[sd==0]=1
    Ztr,Zte=(Xtr-mu)/sd,(Xte-mu)/sd; W=list(model.WORLDS); cents={w:Ztr[ytr==w].mean(0) for w in W}
    pred=np.array(W)[np.argmin(np.column_stack([np.linalg.norm(Zte-cents[w],axis=1) for w in W]),axis=1)]
    acc=float(np.mean(pred==yte)); p=float(__import__("scipy.stats",fromlist=["binomtest"]).binomtest(int((pred==yte).sum()),len(yte),1/len(W),alternative="greater").pvalue)
    return {"accuracy":acc,"binom_p":p,"n":int(len(yte)),"per_world_recall":{w:float(np.mean(pred[yte==w]==w)) for w in W}}
def adm(tr):
    X,y=features(tr); A=np.column_stack([np.ones(len(X)),[list(r.values())[0] for r in [{"x":1}]]*0]) if False else None
    W=[model.theta_of(u["world"],1) for u in tr]; W=np.array([[w["w_pov"],w["w_push"],w["w_tutor"],w["div"]] for w in W])
    A=np.column_stack([np.ones(len(X)),W,np.array([[u["ger_post"],u["cl_post"]] for u in tr])])
    r2s=[]
    for j in range(X.shape[1]):
        yv=X[:,j]; beta,*_=np.linalg.lstsq(A,yv,rcond=None); resid=yv-A@beta; sst=np.sum((yv-yv.mean())**2)
        r2s.append(float(1-np.sum(resid**2)/sst) if sst>0 else 0.0)
    return {"r2_per_component":r2s,"max_r2":max(r2s),"rejected":bool(max(r2s)>0.90)}
def holm(ps):
    order=np.argsort(ps); m=len(ps); adj=np.empty(m); run=0.0
    for rank,i in enumerate(order):
        val=(m-rank)*ps[i]; run=max(run,val); adj[i]=min(1.0,run)
    return adj
def main():
    countries=72
    os.makedirs(RES,exist_ok=True); t0=time.time()
    cu,hu,ru=block(CAL),block(HELD),block(REPL); s0c,s0h=block(CAL,0),block(HELD,0)
    res={}
    names=["B1","B2","B3"]; ps=[]
    for keys in names:
        tr=[{**u,"_v":u[keys]} for u in cu]; te=[{**u,"_v":u[keys]} for u in hu]; rp=[{**u,"_v":u[keys]} for u in ru]
        # single-feature classifier: patch features via temporary key
        def cl(tr_,te_):
            Xtr=np.array([[u["_v"]] for u in tr_]); Xte=np.array([[u["_v"]] for u in te_]); ytr=np.array([u["world"] for u in tr_]); yte=np.array([u["world"] for u in te_])
            mu,sd=Xtr.mean(0),Xtr.std(0); sd[sd==0]=1; Ztr,Zte=(Xtr-mu)/sd,(Xte-mu)/sd; W=list(model.WORLDS)
            cents={w:Ztr[ytr==w].mean(0) for w in W}; pred=np.array(W)[np.argmin(np.column_stack([np.linalg.norm(Zte-cents[w],axis=1) for w in W]),axis=1)]
            import math
            k=int((pred==yte).sum()); n=len(yte); p0=1/len(W)
            pv=sum(math.comb(n,i)*p0**i*(1-p0)**(n-i) for i in range(k,n+1))
            return {"accuracy":float(np.mean(pred==yte)),"binomial_p":float(pv),"n":n}
        res[keys]={"admissibility":adm(tr),"heldout":cl(tr,te),"replication":cl(tr,rp),"s0_control":cl([{**u,"world":w,"_v":u[keys]} for u in s0c for w in model.WORLDS],[{**u,"world":w,"_v":u[keys]} for u in s0h for w in model.WORLDS])}
        ps.append(res[keys]["heldout"]["binomial_p"])
    adj=holm(np.array(ps)); n=len(model.WORLDS); band=[1/n-1.96*np.sqrt((1/n)*(1-1/n)/240), 1/n+1.96*np.sqrt((1/n)*(1-1/n)/240)]
    seps=[]
    for k,p in zip(names,adj):
        r=res[k]; r["holm_adjusted_p"]=float(p); r["beats_chance"]=bool(r["heldout"]["accuracy"]>band[1] and p<0.05 and not r["admissibility"]["rejected"])
        if r["beats_chance"]: seps.append(k)
    eligible=[k for k in names if not res[k]["admissibility"]["rejected"]]
    if not eligible: verdict=("cannot_test","cannot test (F3): all dynamic observables rejected by the admissibility gate")
    elif seps: verdict=("separates",f"separates (dynamic observables: {seps})")
    else: verdict=("cannot_separate","cannot separate (no dynamic observable beats chance after Holm)")
    countries=72
    rr=np.random.default_rng(20261124)
    RR=dict(sigma_y=(0.35,0.75),sigma_a=(0.12,0.30),mu_y=(-0.2,0.3),mu_a=(0.85,1.2),w_child=(0.05,0.35),shadow_cost=(0.15,0.5),f_pub_pre=(0.05,0.30),y_sub0=(0.65,1.05))
    nus=[{k:float(rr.uniform(*v)) for k,v in RR.items()} for _ in range(countries)]
    panels={}
    for w in model.WORLDS:
        rows=[]
        for c in range(countries):
            ys=model.year_stats(model.run_unit(w,1,20270101+100*c,**nus[c]))
            rows.append({t:{"dger":float(ys["ger"][t]-ys["ger"][t-10]) if t>=10 else None,"dcl":float(ys["cl_observed"][t]-ys["cl_observed"][t-10]) if t>=10 else None} for t in range(25)})
        panels[w]=rows
    countries=len(panels[model.WORLDS[0]])
    base=[panels[model.WORLDS[0]][c][t]["dger"] for c in range(countries) for t in range(10,25) if panels[model.WORLDS[0]][c][t]["dger"] is not None]
    med=np.median([np.mean([panels[model.WORLDS[0]][c][t]["dger"] for t in range(10,25)]) for c in range(countries)])
    strata={"low_expansion":[c for c in range(countries) if np.mean([panels[model.WORLDS[0]][c][t]["dger"] for t in range(10,25)])<=med],"high_expansion":[c for c in range(countries) if np.mean([panels[model.WORLDS[0]][c][t]["dger"] for t in range(10,25)])>med]}
    def slope(w,idx):
        R=[]
        for c in idx:
            for t in range(10,25):
                d=panels[w][c][t]
                if d["dger"] is None: continue
                R.append((1 if t<15 else (2 if t<20 else 3),d["dcl"],d["dger"]))
        A=np.array(R); X=np.column_stack([np.ones(len(A)),A[:,2],(A[:,0]==2).astype(float),(A[:,0]==3).astype(float)]); beta,*_=np.linalg.lstsq(X,A[:,1],rcond=None); return float(beta[1])
    strata_res={}
    for name,idx in strata.items():
        sl={w:slope(w,idx) for w in model.WORLDS}; vals=list(sl.values()); strata_res[name]={"slopes":sl,"spread":float(max(vals)-min(vals)),"separated":bool((max(vals)-min(vals))>0.05)}
    out={"dynamic_tiebreakers":res,"chance_band_95":band,"holm":{k:float(v) for k,v in zip(names,adj)},"verdict":{"code":verdict[0],"text":verdict[1]},"fertility_strata":strata_res,"note":"SIMULATION; B1=death-spacing, B2=PPR gradient, B3=age-at-first-birth gradient; fertility layer is a declared minimal approximation, not the full dose ABM","label":"SIMULATION"}
    json.dump(jable(out),open(os.path.join(RES,"phaseb_results.json"),"w"),indent=1)
    man={"task":"task-20","commit_base":subprocess.run(["git","-C",REC,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),"wall_s":round(time.time()-t0,1),"backend":model.BACKEND,"batch_layout":model.LAYOUT,"women_per_unit":fertility.WOMEN,"n_units":{"calibration":len(cu),"heldout":len(hu),"replication":len(ru)},"label":"SIMULATION","verdicts":{"dynamic":verdict[0],"fertility_strata":{k:{"spread":v["spread"],"separated":v["separated"]} for k,v in strata_res.items()}}}
    json.dump(jable(man),open(os.path.join(RES,"run_manifest.json"),"w"),indent=1)
    print("VERDICT",verdict); print("DYNAMIC",{k:{"acc":round(res[k]["heldout"]["accuracy"],3),"R2":round(res[k]["admissibility"]["max_r2"],3),"rejected":res[k]["admissibility"]["rejected"]} for k in names}); print("STRATA",{k:v["spread"] for k,v in strata_res.items()}); print("wall",man["wall_s"])
if __name__=="__main__": main()
