"""Corrected, standalone Phase B1 audit.

SIMULATION ONLY. Implements the preregistered B1 estimand with explicit child deaths,
within-mother contrasts, missing values for unsupported units, feature-specific gate,
and an upstream-independent s=0 null. No causal or empirical interpretation is intended.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, sys, time
from pathlib import Path
import numpy as np

WORLDS = ("P", "S", "C", "R")
PARAMS = {"P": (0.42, 0.06, 0.10, 1.8), "S": (0.34, 0.08, 0.08, 1.6),
          "C": (0.30, 0.10, 0.06, 1.5), "R": (0.38, 0.05, 0.09, 1.7)}
# Upstream model theta_w(s=1): (poverty, push, tutoring, diversification).
SCHOOL_WEIGHTS = {"P": (2.0,0.3,1.3,0.03), "S": (0.6,0.55,1.9,0.05),
                  "C": (0.5,0.4,1.8,0.25), "R": (0.7,0.3,1.6,0.18)}
NULL = tuple(float(np.mean([PARAMS[w][i] for w in WORLDS])) for i in range(4))
WOMEN, AGES = 4000, 25
MIN_EVENTS_PER_SIDE, MIN_MOTHERS = 5, 5


def advance_interval_death_flag(deaths, births, death_since_birth):
    """Return completed interval exposures and the flag carried to the next step."""
    with_deaths = np.asarray(death_since_birth, dtype=bool) | np.asarray(deaths, dtype=bool)
    births = np.asarray(births, dtype=bool)
    completed_exposed = births & with_deaths
    return completed_exposed, with_deaths & ~births


def next_year_recency(deaths, recency):
    """Update the counter after this year's births, for use beginning next year."""
    return np.where(np.asarray(deaths, dtype=bool), 2, np.maximum(np.asarray(recency)-1, 0))


def seed_registry(keys):
    """Assign collision-free 32-bit model seeds from SHA-256 namespaced keys."""
    result={}; used=set()
    for key in sorted(set(tuple(k) for k in keys)):
        nonce=0
        while True:
            payload="phaseb-v1|"+"|".join(map(str,key))+f"|{nonce}"
            value=int.from_bytes(hashlib.sha256(payload.encode()).digest()[:4],"big")
            if value not in used: break
            nonce+=1
        used.add(value); result[key]=value
    if len(result) != len(used): raise AssertionError("seed registry collision")
    return result


def simulate_b1(world: str, seed: int, ger_post: float, *, cl_post: float = 0.0,
                null: bool = False, women: int = WOMEN) -> dict:
    """Return B1 as mother-weighted paired difference; None if unsupported.

    Each mother's birth intervals are assigned exposure if at least one living child
    dies after the preceding birth and before the next birth. Death counts are simulated
    at child level. The two interval means are computed within mother before aggregation.
    """
    if world not in WORLDS: raise ValueError(f"unknown world: {world}")
    lam0, beta, mort, rho = NULL if null else PARAMS[world]
    rng = np.random.default_rng(int(seed))
    p8 = float(np.clip(ger_post, 0.0, 0.9)); p12 = float(np.clip(0.3*p8, 0.0, 1.0-p8))
    edu = rng.choice((0, 8, 12), size=women, p=(1-p8-p12, p8, p12))
    education_factor = np.exp(-beta*edu/8.0)
    mortality = np.minimum(mort*np.exp(-0.3*edu/8.0), 1.0)
    living = np.zeros(women, dtype=int); parity = np.zeros(women, dtype=int)
    last_birth = np.full(women, -1, dtype=int); recent_death = np.zeros(women, dtype=int)
    death_since_birth = np.zeros(women, dtype=bool)
    first_birth_age = np.full(women, np.nan)
    # store interval outcomes per mother, separately by exposure status
    exposed = [[] for _ in range(women)]; unexposed = [[] for _ in range(women)]
    for t in range(AGES):
        # Deaths occur among children born before this year's birth opportunity.
        deaths = rng.binomial(living, mortality)
        living -= deaths
        completed_exposed, death_since_birth = advance_interval_death_flag(
            deaths > 0, np.zeros(women, dtype=bool), death_since_birth)
        # Birth hazard at t uses only death history known before t. Deaths at t
        # affect hazards at t+1 and t+2, not the same-year birth opportunity.
        hazard = lam0*education_factor*(1.0-0.10*parity)*np.where(recent_death > 0, rho, 1.0)
        birth = rng.random(women) < np.clip(hazard, 0.0, 0.95)
        completed_exposed, death_since_birth = advance_interval_death_flag(
            np.zeros(women, dtype=bool), birth, death_since_birth)
        idx = np.flatnonzero(birth & (last_birth >= 0))
        for i in idx:
            interval = t-int(last_birth[i])
            (exposed[i] if completed_exposed[i] else unexposed[i]).append(float(interval))
        first_birth_age = np.where(birth & np.isnan(first_birth_age), 15+t, first_birth_age)
        recent_death = next_year_recency(deaths > 0, recent_death)
        last_birth[birth] = t; parity += birth.astype(int); living += birth.astype(int)
    contrasts = []
    exposed_n = unexposed_n = 0
    supported_mothers = 0
    for a, b in zip(exposed, unexposed):
        exposed_n += len(a); unexposed_n += len(b)
        if len(a) and len(b):
            contrasts.append(float(np.mean(a)-np.mean(b)))
            supported_mothers += 1
    valid = (exposed_n >= MIN_EVENTS_PER_SIDE and unexposed_n >= MIN_EVENTS_PER_SIDE
             and supported_mothers >= MIN_MOTHERS)
    low, high = edu <= 8, edu == 12
    den_low, den_high = int(np.sum(parity[low] >= 1)), int(np.sum(parity[high] >= 1))
    ppr_low = float(np.sum(parity[low] >= 2)/den_low) if den_low else None
    ppr_high = float(np.sum(parity[high] >= 2)/den_high) if den_high else None
    b2 = (ppr_low-ppr_high) if ppr_low is not None and ppr_high is not None else None
    n_first_low, n_first_high = int(np.sum(np.isfinite(first_birth_age[low]))), int(np.sum(np.isfinite(first_birth_age[high])))
    mean_first_low = float(np.nanmean(first_birth_age[low])) if n_first_low else None
    mean_first_high = float(np.nanmean(first_birth_age[high])) if n_first_high else None
    b3 = (mean_first_high-mean_first_low) if mean_first_low is not None and mean_first_high is not None else None
    return {"B1": float(np.mean(contrasts)) if valid else None,
            "n_exposed_intervals": exposed_n, "n_unexposed_intervals": unexposed_n,
            "n_mothers_with_both": supported_mothers, "estimable": bool(valid),
            "B2": float(b2) if b2 is not None else None,
            "B2_n_parity1_low": den_low, "B2_n_parity1_high": den_high,
            "B2_missing_reason": None if b2 is not None else "PPR undefined in at least one education group (no parity-1 denominator)",
            "B3": float(b3) if b3 is not None else None,
            "B3_n_first_birth_low": n_first_low, "B3_n_first_birth_high": n_first_high,
            "B3_missing_reason": None if b3 is not None else "no observed first births in at least one education group",
            "ger_post": float(ger_post), "cl_post": float(cl_post),
            "missing_reason": None if valid else "insufficient within-mother exposed/unexposed interval support"}


def ols_r2(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    if len(y) < 3 or np.ptp(y) == 0: return None
    X = np.column_stack((np.ones(len(y)), x))
    fitted = X @ np.linalg.lstsq(X, y, rcond=None)[0]
    return float(1-np.sum((y-fitted)**2)/np.sum((y-y.mean())**2))


def admissibility(units, feature):
    """Feature-specific gate; missing values are excluded separately per feature."""
    rows = [u for u in units if u.get(feature) is not None]
    if len(rows) < 8: return {"feature": feature, "n": len(rows), "r2": None, "rejected": None,
                              "status": "cannot_test_insufficient_complete_units"}
    # Apply the preregistered gate against upstream school-utility weights plus
    # simulated GER and observed child-labor inputs, independently for each feature.
    weights = np.array([SCHOOL_WEIGHTS[u["world"]] for u in rows], float)
    covars = np.array([[u["ger_post"], u["cl_post"]] for u in rows], float)
    predictors = np.column_stack((weights, covars))
    r2 = ols_r2(np.array([u[feature] for u in rows]), predictors)
    return {"feature": feature, "n": len(rows), "r2": r2,
            "rejected": bool(r2 is not None and r2 > 0.90), "threshold": 0.90,
            "status": "tested" if r2 is not None else "cannot_test_constant_feature"}


def _predict(train, test, feature="B1", worlds=WORLDS):
    train = [u for u in train if u.get(feature) is not None]
    test = [u for u in test if u.get(feature) is not None]
    if any(not any(u["world"] == w for u in train) for w in worlds) or not test:
        return train, test, None
    vals = np.array([u[feature] for u in train]); mean, sd = float(vals.mean()), float(vals.std())
    if sd == 0: sd = 1.0
    centers = {w:float(np.mean([(u[feature]-mean)/sd for u in train if u["world"]==w])) for w in worlds}
    pred = [min(worlds, key=lambda w: abs((u[feature]-mean)/sd-centers[w])) for u in test]
    return train, test, pred


def classify(train, test, feature="B1", worlds=WORLDS):
    """One-dimensional nearest-centroid classifier; preserve feature-specific missingness."""
    train, test, pred = _predict(train, test, feature, worlds)
    if pred is None:
        status = "cannot_test_missing_training_class" if test else "cannot_test_no_complete_test_units"
        return {"status":status, "feature":feature, "n":len(test), "accuracy":None}
    correct = sum(p == u["world"] for p,u in zip(pred,test)); n=len(test)
    return {"status":"descriptive_only", "feature":feature, "n":n, "correct":correct, "accuracy":correct/n,
            "per_world_n":{w:sum(u["world"]==w for u in test) for w in worlds},
            "per_world_recall":{w:(sum(p==w and u["world"]==w for p,u in zip(pred,test))/sum(u["world"]==w for u in test)
                                    if any(u["world"]==w for u in test) else None) for w in worlds}}


def blocked_permutation_p(train, test, feature, reps=2000, seed=9147):
    """Permute held-out labels within seed blocks; preserves balanced block design."""
    train, test, pred = _predict(train, test, feature)
    if pred is None: return None
    obs = sum(p == u["world"] for p,u in zip(pred,test)); groups={}
    for i,u in enumerate(test): groups.setdefault(u["seed_index"], []).append(i)
    if any(len(ix) != len(WORLDS) for ix in groups.values()): return None
    rng=np.random.default_rng(seed); ge=0
    labels=np.array([u["world"] for u in test])
    for _ in range(reps):
        perm=labels.copy()
        for ix in groups.values(): perm[ix]=rng.permutation(perm[ix])
        ge += sum(p == y for p,y in zip(pred,perm)) >= obs
    return float((ge+1)/(reps+1))


def holm_adjust(pvalues):
    keys=list(pvalues); ordered=sorted(keys,key=lambda k:pvalues[k]); out={}; running=0.0; m=len(ordered)
    for rank,key in enumerate(ordered):
        running=max(running,(m-rank)*pvalues[key]); out[key]=min(1.0,running)
    return out


def load_upstream(model_path):
    spec=importlib.util.spec_from_file_location("phaseb_upstream_model",model_path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def run_upstream_phase_b(counts=(20,60,60), model_n=10000, women=WOMEN,
                         permutation_reps=2000, model_path=None, calibration_path=None):
    here=Path(__file__).resolve().parent
    model_path=Path(model_path or here/"model.py")
    calibration_path=Path(calibration_path or here.parent/"2026-11-24-synthetic-loop/results/calibration.json")
    if not model_path.exists() or not calibration_path.exists():
        raise FileNotFoundError(f"required upstream model/calibration missing: {model_path}, {calibration_path}")
    model=load_upstream(str(model_path)); calibration=json.loads(calibration_path.read_text())
    nuisance={w:calibration["cells"][w]["chosen"]["nuisance"] for w in WORLDS}
    null_nuisance=calibration["cells"]["s0"]["chosen"]["nuisance"]
    block_ranges={}; cursor=0
    for name,n in zip(("calibration","heldout","replication"),counts):
        block_ranges[name]=range(cursor,cursor+n); cursor += n
    units=[]
    # s=0 upstream unit is generated once per seed and shared by labels as intended;
    # independent fertility histories are still generated for each label below.
    allks=range(cursor)
    splits={k:block for block,rng in block_ranges.items() for k in rng}
    seed_keys=[]
    for k in allks:
        split=splits[k]
        seed_keys.append(("upstream_s0",split,k,"shared"))
        for w in WORLDS:
            seed_keys.extend((("upstream_s1",split,k,w),("fertility_s1",split,k,w),
                              ("fertility_s0",split,k,w)))
    seeds=seed_registry(seed_keys)
    for k in allks:
        split=splits[k]
        res0=model.run_unit("P",0,seeds[("upstream_s0",split,k,"shared")],n=model_n,backend="numpy",**null_nuisance)
        ys0=model.year_stats(res0)
        null_inputs=(float(ys0["ger"][15:].mean()),float(ys0["cl_observed"][15:].mean()))
        for w in WORLDS:
            seed=seeds[("upstream_s1",split,k,w)]
            res=model.run_unit(w,1,seed,n=model_n,backend="numpy",**nuisance[w])
            ys=model.year_stats(res)
            inputs=(float(ys["ger"][15:].mean()),float(ys["cl_observed"][15:].mean()))
            u=simulate_b1(w,seeds[("fertility_s1",split,k,w)],inputs[0],cl_post=inputs[1],women=women)
            units.append({"world":w,"seed_index":k,"block":next(b for b,r in block_ranges.items() if k in r),**u})
            nseed=seeds[("fertility_s0",split,k,w)]
            nu=simulate_b1(w,nseed,null_inputs[0],cl_post=null_inputs[1],null=True,women=women)
            units.append({"world":w,"seed_index":k,"block":next(b for b,r in block_ranges.items() if k in r),
                          "sample":"s0","upstream_s":0,**nu})
    main_units=[u for u in units if u.get("sample") is None]
    null_units=[u for u in units if u.get("sample")=="s0"]
    blocks={name:[u for u in main_units if u["block"]==name] for name in block_ranges}
    null_blocks={name:[u for u in null_units if u["block"]==name] for name in ("calibration","heldout")}
    features=("B1","B2","B3")
    gates={f:admissibility(blocks["calibration"],f) for f in features}
    classifiers={}; raw_p={}
    for f in features:
        classifiers[f]={}
        for block in ("heldout","replication"):
            classifiers[f][block]=classify(blocks["calibration"],blocks[block],f)
            classifiers[f][block]["seed_block_permutation_p"] = blocked_permutation_p(
                blocks["calibration"],blocks[block],f,permutation_reps,seed=9147+features.index(f)+(0 if block=="heldout" else 100))
        raw_p[f]=classifiers[f]["heldout"]["seed_block_permutation_p"]
    holm={f:None for f in features}
    validp={f:p for f,p in raw_p.items() if p is not None}
    holm.update(holm_adjust(validp))
    for f in features:
        classifiers[f]["heldout"]["holm_adjusted_p"] = holm[f]
        classifiers[f]["exploratory_pattern"]=("admissible_separation_pattern" if gates[f].get("rejected") is False and holm[f] is not None and holm[f]<.05
            and classifiers[f]["replication"]["seed_block_permutation_p"] is not None
            and classifiers[f]["replication"]["seed_block_permutation_p"]<.05 else "no_exploratory_separation_pattern")
    null_results={f:{block:classify(null_blocks["calibration"],null_blocks[block],f)
                     for block in ("heldout",)} for f in features}
    return {"label":"SIMULATION ONLY — upstream calibrated model",
      "design":{"n_calibration_per_world":counts[0],"n_heldout_per_world":counts[1],"n_replication_per_world":counts[2],
                "model_households":model_n,"women_per_fertility_unit":women,"worlds":list(WORLDS),
                "heldout_permutation_reps":permutation_reps,"seed_rule":"SHA-256 namespaced (mode, split, k, world) keys, collision-resolved in 32-bit model seed space; s0 uses common null nuisance and one shared upstream seed per split/k; fertility null histories use independent world-specific seeds"},
      "feature_gates":gates,"dynamic_classifiers":classifiers,"s0_independent_null_descriptive":null_results,
      "units":units,"limitations":["Simulation only; not empirical evidence and no causal interpretation.",
        "Each mechanism label uses its own calibration-chosen nuisance vector; classifier separation is conditional on those nuisance values and cannot be attributed uniquely to mechanism labels. A matched-nuisance alternative is not implemented.",
        "Admissibility regresses each feature on the upstream school-utility weight vector plus simulated GER_post and child-labor_post; it is feature-specific and not a proof of causal independence.",
        "The classifier and seed-block permutation analysis are exploratory simulation diagnostics and differ from the original preregistered binomial analysis; do not call these preregistered significance tests.",
        "Held-out permutation p-values retain balanced seed-index blocks and have finite Monte Carlo resolution; they are diagnostics under this model design.",
        "Replication permutation p-values are unadjusted secondary diagnostics; Holm adjustment applies to the three exploratory held-out feature tests only.",
        "s=0 control classifiers are descriptive and are not used to choose thresholds or declare a result.",
        "The birth-history layer remains a minimal approximation, not a full fertility ABM or DHS transport analysis."],
      "upstream":{"model_path":str(model_path),"calibration_path":str(calibration_path),"backend":"numpy","model_layout":model.LAYOUT}}


def run_smoke_design(women=WOMEN):
    """Synthetic input adapter smoke design; not the full upstream model experiment."""
    result = {"label":"SIMULATION ONLY", "design":"independent fertility simulator smoke design",
              "units":[], "limitations":["GER=0.45 and cl_post=0.35 are fixed by construction; no upstream matrix model run.",
              "Classifier accuracy is descriptive under this fixed balanced class design; no p-values or significance claims are reported.",
              "The feature gates use upstream school-utility weights plus GER/cl; with fixed GER/cl in this isolated smoke they are only mechanics checks, not Phase B findings."]}
    # Independent child-history draws per world label are essential here: the null
    # shares fertility parameters and upstream inputs, but does not clone the same
    # simulated women and then relabel those cloned outcomes.
    layout=(("calibration",range(4)),("heldout",range(4,12)),("replication",range(12,20)))
    keys=[("fertility_s0",block,k,w) for block,ks in layout for k in ks for w in WORLDS]
    seeds=seed_registry(keys)
    for block, ks in layout:
        for k in ks:
            for w in WORLDS:
                # Inputs and parameter vector are common; stochastic histories are
                # independent across labels, as in an independently generated null.
                u=simulate_b1(w,seeds[("fertility_s0",block,k,w)],0.45,cl_post=0.35,null=True,women=women)
                result["units"].append({"block":block,"world":w,"seed_index":k,**u})
    for block in ("calibration","heldout","replication"):
        block_units=[u for u in result["units"] if u["block"]==block]
        result[block+"_gates"]={feature:admissibility(block_units,feature) for feature in ("B1","B2","B3")}
    calibration=[u for u in result["units"] if u["block"]=="calibration"]
    heldout=[u for u in result["units"] if u["block"]=="heldout"]
    result["s0_heldout_descriptive"]={feature:classify(calibration,heldout,feature) for feature in ("B1","B2","B3")}
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__); mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--smoke",action="store_true",help="bounded upstream integration smoke")
    mode.add_argument("--full",action="store_true",help="full preregistered sample-size simulation run")
    ap.add_argument("--out",type=Path,default=None)
    ap.add_argument("--counts",default=None,help="comma-separated calibration,heldout,replication counts")
    ap.add_argument("--model-n",type=int,default=None); ap.add_argument("--women",type=int,default=None)
    ap.add_argument("--permutation-reps",type=int,default=2000)
    ap.add_argument("--model-path",default=None); ap.add_argument("--calibration-path",default=None)
    a=ap.parse_args(); t=time.time()
    counts=tuple(map(int,a.counts.split(","))) if a.counts else ((2,3,3) if a.smoke else (20,60,60))
    if len(counts)!=3 or any(n<1 for n in counts): ap.error("--counts must contain three positive integers")
    model_n=a.model_n if a.model_n is not None else (256 if a.smoke else 10000)
    women=a.women if a.women is not None else (200 if a.smoke else WOMEN)
    out=run_upstream_phase_b(counts=counts,model_n=model_n,women=women,
                             permutation_reps=a.permutation_reps,model_path=a.model_path,
                             calibration_path=a.calibration_path)
    out["run_mode"]="bounded_upstream_smoke" if a.smoke else "full_upstream_simulation"
    out["wall_seconds"]=round(time.time()-t,3)
    out_name=("upstream_smoke_" if a.smoke else "upstream_full_")+time.strftime("%Y%m%dT%H%M%SZ",time.gmtime())+".json"
    out_path=a.out or (Path(__file__).parent/out_name)
    if out_path.exists(): ap.error(f"Refusing to overwrite existing output: {out_path}")
    out_path.parent.mkdir(parents=True,exist_ok=True)
    with out_path.open("x") as fh: fh.write(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"path":str(out_path),"label":out["label"],"n_units":len(out["units"]),
                      "dynamic_classifiers":out["dynamic_classifiers"],
                      "s0_descriptive":out["s0_independent_null_descriptive"]},indent=2))

if __name__=="__main__": main()
