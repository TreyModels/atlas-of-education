"""Phase A run: calibration -> H1 macro wall -> H4 static tie-breakers -> ABC identifiability pre-audit."""
import json, os, sys, time, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REC = os.path.dirname(HERE); RES = os.path.join(REC, "results")
sys.path.insert(0, HERE)
import model, calibrate, macro, tiebreak

def jable(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, dict): return {k: jable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jable(v) for v in o]
    return o

def main():
    os.makedirs(RES, exist_ok=True); t0 = time.time(); slog = []
    cal = {"m_star": calibrate.M_STAR.tolist(), "tolerance": calibrate.TOL, "cells": {}}
    nuis = {}
    for w in model.WORLDS:
        c = calibrate.calibrate(w, 1, calibrate.M_STAR, slog, n_candidates=300)
        cal["cells"][w] = c; nuis[w] = c["chosen"]["nuisance"]
    c0 = calibrate.calibrate(None, 0, calibrate.M_STAR, slog, n_candidates=300)
    cal["cells"]["s0"] = c0; nuis["s0"] = c0["chosen"]["nuisance"]
    cal["all_matched"] = all(cal["cells"][w]["matched"] for w in model.WORLDS)
    json.dump(jable(cal), open(os.path.join(RES, "calibration.json"), "w"), indent=1)
    for w in model.WORLDS:
        print(w, "matched", cal["cells"][w]["matched"], "maxres", round(cal["cells"][w]["chosen"]["max_abs_residual"], 3))
    ident = {"max_abs_diff": 0.0}
    for k in (0, 1, 2):
        rs = [model.run_unit(w, 0, tiebreak.SEED_K(k), **nuis["s0"]) for w in model.WORLDS]
        d = max(float(np.max(np.abs(rs[0][key].astype(float) - rs[i][key].astype(float)))) for i in (1, 2, 3) for key in rs[0])
        ident["max_abs_diff"] = max(ident["max_abs_diff"], d)
    ident["passed"] = ident["max_abs_diff"] == 0.0
    print("[identity] s=0 identical:", ident["passed"], ident["max_abs_diff"])
    h1 = macro.run_h1(slog); h1["identity_check"] = ident
    json.dump(jable(h1), open(os.path.join(RES, "h1_macro_wall.json"), "w"), indent=1)
    print("[H1]", {w: round(v["beta"], 3) for w, v in h1["slopes"].items()}, "p", h1["joint_interaction"]["p"], h1["verdict_code"])
    cu = tiebreak.build_block(tiebreak.CAL_BLOCK, nuis, seed_log=slog)
    hu = tiebreak.build_block(tiebreak.HELDOUT_BLOCK, nuis, seed_log=slog)
    ru = tiebreak.build_block(tiebreak.REPL_BLOCK, nuis, seed_log=slog)
    def s0(block):
        out = []
        for k in block:
            b = tiebreak.build_unit("P", 0, tiebreak.SEED_K(k), nuis["s0"])
            for w in model.WORLDS:
                u = dict(b); u["world"] = w; out.append(u)
        return out
    h4 = tiebreak.run_h4(cu, hu, ru, {"calibration": s0(tiebreak.CAL_BLOCK), "heldout": s0(tiebreak.HELDOUT_BLOCK)}, nuis, slog)
    h4["identity_check"] = ident; h4["macro_matching"] = {w: {"matched": cal["cells"][w]["matched"], "max_abs_residual": cal["cells"][w]["chosen"]["max_abs_residual"]} for w in model.WORLDS}
    json.dump(jable(h4), open(os.path.join(RES, "h4_tiebreakers.json"), "w"), indent=1)
    for k, v in h4["tiebreakers"].items(): print("[H4]", k, "acc", round(v["heldout"]["accuracy"], 3), "R2", round(v["admissibility"]["max_r2"], 3), "rejected", v["admissibility"]["rejected"])
    print("[H4] verdict:", h4["verdict"])
    # ---- ABC pre-audit ----
    import urllib.request
    E8 = ["MWI","ETH","UGA","LSO","TZA","KEN","MOZ","GHA"]; url = f"https://api.worldbank.org/v2/country/{';'.join(E8)}/indicator/SL.TLF.0714.ZS?format=json&per_page=5000&date=1990:2023"
    try:
        d = json.load(urllib.request.urlopen(url, timeout=30)); vals = [x["value"] for x in d[1] if x["value"] is not None]
        cl_target = float(np.mean(vals) / 100.0)
    except Exception as e:
        cl_target = 0.314; print("WDI pull failed, using design constant:", e)
    targets = np.array([0.80, cl_target, 0.70]); abc_nuis = {"sigma_y": 0.55, "sigma_a": 0.20, "mu_y": 0.0, "mu_a": 1.0, "f_pub_pre": 0.0, "y_sub0": 0.85, "w_child": 0.15, "shadow_cost": 0.32}
    rng = np.random.default_rng(12345); rows = []
    for i in range(5000):
        theta = {"w_pov": float(rng.uniform(0, 3)), "w_push": float(rng.uniform(0, 3)), "w_tutor": float(rng.uniform(0, 3)), "div": float(rng.uniform(0, 0.35))}
        model.THETA0 = dict(theta); model.DELTAS = {w: {k: 0.0 for k in theta} for w in model.WORLDS}
        res = model.run_unit(None, 0, 777 + i, n=50_000, years=1, **abc_nuis)
        s = res["state"][0]; ger = float(np.mean(s <= 1)); cl = float(np.mean(np.isin(s, (1, 2))))
        sw = float(np.mean(s == 1) / cl) if cl > 0 else 0.0
        mom = np.array([ger, cl, sw]); dist = float(np.sqrt(np.sum((mom - targets) ** 2)))
        rows.append({"draw": i, **theta, "ger": ger, "cl": cl, "sw": sw, "dist": dist})
    rows.sort(key=lambda r: r["dist"]); acc = rows[:500]
    priors = {"w_pov": (0, 3), "w_push": (0, 3), "w_tutor": (0, 3), "div": (0, 0.35)}
    ident_tab = {}
    for p, (lo, hi) in priors.items():
        v = np.array([r[p] for r in acc]); q05, q50, q95 = np.percentile(v, [5, 50, 95]); ratio = float((q95 - q05) / (hi - lo))
        ident_tab[p] = {"q05": float(q05), "median": float(q50), "q95": float(q95), "width_ratio": ratio, "identified": bool(ratio <= 0.80)}
    abc = {"method": "equal-weight rejection ABC, 5000 draws, top 10% accepted (500)", "targets": {"ger": 0.80, "cl_children_in_employment": cl_target, "study_work_share_of_employed": 0.70}, "construct_notes": ["children in employment != child labour", "model cl is a share of children; WDI SL.TLF.0714.ZS is the children-in-employment share", "study+work share is a share of employed children (WDI SW.ZS)"], "logged_nuisances": abc_nuis, "identifiability": ident_tab, "n_accepted": len(acc), "label": "SIMULATION-pre-audit"}
    json.dump(jable(abc), open(os.path.join(RES, "abc_preaudit.json"), "w"), indent=1)
    for p, v in ident_tab.items(): print("[ABC]", p, "width_ratio", round(v["width_ratio"], 3), "identified", v["identified"])
    man = {"task": "task-18 Phase A", "commit_base": subprocess.run(["git", "-C", REC, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(), "started_local": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "wall_s": round(time.time() - t0, 1), "backend": model.BACKEND, "batch_layout": model.LAYOUT, "worlds": list(model.WORLDS), "theta0": model.THETA0, "literature": model.LITERATURE, "seed_blocks": {"calibration": [tiebreak.SEED_K(0), tiebreak.SEED_K(19)], "heldout": [tiebreak.SEED_K(20), tiebreak.SEED_K(79)], "replication": [tiebreak.SEED_K(80), tiebreak.SEED_K(139)]}, "python": sys.executable, "label": "SIMULATION", "verdicts": {"H1": h1["verdict_code"], "H4": h4["verdict_code"], "ABC_pre_audit": {k: v["identified"] for k, v in ident_tab.items()}}}
    json.dump(jable(man), open(os.path.join(RES, "run_manifest.json"), "w"), indent=1)
    print("[done]", man["wall_s"], "s")
if __name__ == "__main__": main()
