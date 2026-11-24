"""E1-structured synthetic matrix: 7 links x 15 groupings x 3 specs x 4 literature worlds."""
import json, os, sys, time, itertools
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); REC=os.path.dirname(HERE); RES=os.path.join(REC,"results")
sys.path.insert(0,HERE)
import model
N_COUNTRIES=72; YEARS=25; SEED_BASE=20270101
RANGES=dict(sigma_y=(0.35,0.75),sigma_a=(0.12,0.30),mu_y=(-0.20,0.30),mu_a=(0.85,1.20),
            w_child=(0.05,0.35),shadow_cost=(0.15,0.50),f_pub_pre=(0.05,0.30),y_sub0=(0.65,1.05))
LINKS=("cl_observed","study_work","work_only","hidden_work","tutoring","mean_learn","mean_income")
SPECS=("S1_10y_decFE","S2_5y_binFE","S3_levels_country_year_FE")

def country_nuisances():
    rng=np.random.default_rng(20261124)
    return [{k:float(rng.uniform(*v)) for k,v in RANGES.items()} for _ in range(N_COUNTRIES)]

def country_links(world, c, nu):
    res=model.run_unit(world,1,SEED_BASE+100*c,years=YEARS,**nu)
    s=res["state"]; out={}
    out["cl_observed"]=np.isin(s,(1,2)).mean(1).astype(float)
    out["study_work"]=(s==1).mean(1).astype(float)
    out["work_only"]=(s==2).mean(1).astype(float)
    out["hidden_work"]=(s==3).mean(1).astype(float)
    out["tutoring"]=res["tutor"].mean(1).astype(float)
    out["mean_learn"]=res["learn"].mean(1).astype(float)
    out["mean_income"]=res["y_hh"].mean(1).astype(float)
    out["ger"]=(s<=1).mean(1).astype(float)
    return out

def rows_for(link_series, ger_series, spec, countries):
    rows=[]
    for c in countries:
        y=link_series[c]; g=ger_series[c]
        if spec=="S1_10y_decFE":
            for t in range(10,YEARS):
                dec=1 if t<15 else (2 if t<20 else 3)
                rows.append((c,dec,y[t]-y[t-10],g[t]-g[t-10]))
        elif spec=="S2_5y_binFE":
            for t in range(5,YEARS):
                b=1+(t-5)//5
                rows.append((c,b,y[t]-y[t-5],g[t]-g[t-5]))
        else:
            for t in range(YEARS):
                rows.append((c,t,y[t],g[t]))
    return np.array(rows,dtype=float)

def design(rows,spec,ncountry=72):
    C=rows[:,0].astype(int); F=rows[:,1].astype(int); y=rows[:,2]; x=rows[:,3]
    if spec=="S3_levels_country_year_FE":
        cols=[x]
        for c in sorted(np.unique(C).tolist()): cols.append((C==c).astype(float))
        for t in range(1,YEARS): cols.append((F==t).astype(float))
        return np.column_stack(cols), C, y
    cols=[np.ones(len(rows)),x]
    if spec=="S1_10y_decFE":
        cols += [(F==2).astype(float),(F==3).astype(float)]
    elif spec=="S2_5y_binFE":
        for b in range(2,5): cols.append((F==b).astype(float))
    return np.column_stack(cols), C, y

def ols_cluster(y,X,G):
    n,k=X.shape; beta,*_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    XtXi=np.linalg.inv(X.T@X); meat=np.zeros((k,k))
    for g in np.unique(G):
        m=G==g; s=X[m].T@e[m]; meat+=np.outer(s,s)
    Gc=len(np.unique(G)); V=XtXi@meat@XtXi*(Gc/(Gc-1))*((n-1)/(n-k))
    return beta,V

def main():
    os.makedirs(RES,exist_ok=True); t0=time.time()
    nuis=country_nuisances()
    series={w:{L:{} for L in LINKS+("ger",)} for w in model.WORLDS}
    for w in model.WORLDS:
        for c in range(N_COUNTRIES):
            d=country_links(w,c,nuis[c])
            for L in LINKS+("ger",): series[w][L][c]=d[L]
        print("world",w,"done",round(time.time()-t0,1),"s")
    # groupings
    rng=np.random.default_rng(20261125); groupings={}
    for i in range(12):
        perm=rng.permutation(N_COUNTRIES); groupings[f"rand{i:02d}"]=[sorted(perm[g*18:(g+1)*18].tolist()) for g in range(4)]
    def quartile(key):
        vals=np.array([nuis[c][key] for c in range(N_COUNTRIES)]); order=np.argsort(vals)
        return [sorted(order[g*18:(g+1)*18].tolist()) for g in range(4)]
    for key in ("sigma_y","mu_y","w_child"): groupings[f"q_{key}"]=quartile(key)
    # full sample grouping (for pooled sign reference)
    full=[list(range(N_COUNTRIES))]
    cells=[]; pooled={}
    for w in model.WORLDS:
        for spec in SPECS:
            for L in LINKS:
                rows=rows_for(series[w][L],series[w]["ger"],spec,full[0])
                X,G,y=design(rows,spec); beta,V=ols_cluster(y,X,G)
                pooled[(w,spec,L)]=(float(beta[1]),float(np.sqrt(V[1,1])))
    for gname,groups in groupings.items():
        for spec in SPECS:
            for L in LINKS:
                est={}
                for w in model.WORLDS:
                    betas=[]; ses=[]
                    for grp in groups:
                        rows=rows_for(series[w][L],series[w]["ger"],spec,grp)
                        if len(rows)<30: continue
                        X,G,y=design(rows,spec); beta,V=ols_cluster(y,X,G)
                        betas.append(float(beta[1])); ses.append(float(np.sqrt(V[1,1])))
                    est[w]={"beta":float(np.mean(betas)) if betas else None,"se":float(np.sqrt(np.mean(np.square(ses)))) if ses else None}
                # indistinguishability: all pairwise 95% CI overlap
                ws=[w for w in model.WORLDS if est[w]["beta"] is not None and est[w]["se"] is not None]
                pairs=[(a,b) for a,b in itertools.combinations(ws,2)]
                overlap_all=all(abs(est[a]["beta"]-est[b]["beta"])<=1.96*np.hypot(est[a]["se"],est[b]["se"]) for a,b in pairs)
                cells.append({"grouping":gname,"spec":spec,"link":L,"worlds":est,"indistinguishable":bool(overlap_all),"n_worlds":len(ws)})
    n=len(cells); ind=sum(1 for c in cells if c["indistinguishable"])
    # robust-across-groupings per world: (link,spec) same sign & |t|>1.96 in >=12/15 groupings
    robust={}
    for w in model.WORLDS:
        rob=0; det=[]
        for spec in SPECS:
            for L in LINKS:
                ref=pooled[(w,spec,L)]
                signs=[]
                for gname in groupings:
                    c=next(c for c in cells if c["grouping"]==gname and c["spec"]==spec and c["link"]==L)
                    beta=c["worlds"][w]["beta"]; se=c["worlds"][w]["se"]
                    if beta is not None and se not in (None,0.0):
                        signs.append(np.sign(beta)==np.sign(ref[0]) and abs(beta/se)>1.96)
                    else: signs.append(False)
                is_rob=sum(signs)>=12
                det.append({"spec":spec,"link":L,"groupings_same_sign_sig":int(sum(signs)),"robust":bool(is_rob)})
                rob+=int(is_rob)
        robust[w]={"n_robust":rob,"n_links":len(LINKS)*len(SPECS),"share":rob/(len(LINKS)*len(SPECS)),"detail":det}
    summary={"n_cells":n,"n_indistinguishable":ind,"cross_world_indistinguishable_share":ind/n,
             "wall_decision_rule":"wall demonstrated iff share >= 0.75","wall_verdict":"wall" if ind/n>=0.75 else "separable",
             "robust_across_groupings":robust,
             "comparison":{"E1_robust_travel":"5/272 = 1.8% of links travel across 50 typologies (empirical)",
                           "Q3_minority_mislabel":"87% of minority-effect worlds mislabelled robust everywhere (empirical)",
                           "note":"synthetic robust shares are the structural analogue; Q3 statistic is not directly comparable"},
             "label":"SIMULATION"}
    json.dump(summary,open(os.path.join(RES,"matrix_summary.json"),"w"),indent=1)
    json.dump(cells,open(os.path.join(RES,"matrix_cells.json"),"w"),indent=1)
    man={"task":"task-19","commit_base":__import__("subprocess").run(["git","-C",REC,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
         "started_local":time.strftime("%Y-%m-%dT%H:%M:%S%z"),"wall_s":round(time.time()-t0,1),"backend":model.BACKEND,
         "batch_layout":model.LAYOUT,"n_countries":N_COUNTRIES,"years":YEARS,"links":list(LINKS),"specs":list(SPECS),
         "n_groupings":len(groupings),"seed_base":SEED_BASE,"label":"SIMULATION"}
    json.dump(man,open(os.path.join(RES,"run_manifest.json"),"w"),indent=1)
    print("SUMMARY:",json.dumps({k:summary[k] for k in ("n_cells","n_indistinguishable","cross_world_indistinguishable_share","wall_verdict")},indent=1))
    print("ROBUST:",{w:robust[w]["n_robust"] for w in model.WORLDS},"of",len(LINKS)*len(SPECS))
if __name__=="__main__": main()
