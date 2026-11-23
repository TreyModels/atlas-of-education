"""One-screen digest of every result file, so the report can be written from numbers rather than memory."""
import json, os, sys
D = sys.argv[1] if len(sys.argv) > 1 else "../results"
def L(f):
    p = os.path.join(D, f)
    return json.load(open(p)) if os.path.exists(p) else None
def q(d, k="q50"): return d[k] if k in d else float("nan")
R = {}
for tag, f in (("A", "cpu_fitA.json"), ("B", "cpu_fitB.json"), ("Arep", "cpu_fitA_rep.json"),
               ("gpuA", "gpu_fitA.json"), ("gpuB", "gpu_fitB.json")):
    fit = L(f)
    if not fit: continue
    import numpy as np
    u = np.array(fit["u"]); w = np.array(fit["w"]); lo, hi = np.array(fit["lo"]), np.array(fit["hi"])
    th = lo + u * (hi - lo)
    def wq(x, qq):
        i = np.argsort(x); c = np.cumsum(w[i]) / w.sum(); return float(np.interp(qq, c, x[i]))
    post = {}
    for k, n in enumerate(fit["names"]):
        m = float((w * th[:, k]).sum()); sd = float(np.sqrt((w * (th[:, k] - m) ** 2).sum()))
        post[n] = dict(q05=wq(th[:, k], .05), q50=wq(th[:, k], .5), q95=wq(th[:, k], .95),
                       ratio=sd / ((hi[k] - lo[k]) / np.sqrt(12)))
    ess = float(1 / np.sum(w ** 2))
    R[tag] = dict(engine=fit.get("engine"), hist=fit["hist"], ess=ess, n=len(w), post=post)
print("=" * 100)
for tag, d in R.items():
    h = d["hist"]
    print(f"[{tag}] engine={d['engine']} rounds={len(h)} draws={sum(x['n'] for x in h)} kept={d['n']} ESS={d['ess']:.0f}")
    print("   best distance by round:", [round(x['best'], 2) for x in h], " tolerance:", [round(x['eps'], 2) for x in h])
    for n in ("th_k", "th_f", "kappa", "gam", "lam_s"):
        p = d["post"][n]; print(f"   {n:6s} med {p['q50']:7.3f}  90% [{p['q05']:6.3f},{p['q95']:6.3f}]  post/prior sd {p['ratio']:.2f}")
an = L("analysis_A.json"); ho = L("analysis_holdout.json"); dc_ = L("analysis_decomp.json")
st = L("analysis_stability.json"); fa = L("falsifiers.json"); bs = L("bench_scale.json")
if ho and "mean_A" in ho.get("holdout", {}):
    h = ho["holdout"]; print("\n[HOLDOUT]", "mean D A %.2f B %.2f diff %+.2f CI [%.2f, %.2f] A better in %d/%d (nhold=%d)" % (
        h["mean_A"], h["mean_B"], h["diff_mean"], h["diff_ci"][0], h["diff_ci"][1], h["A_better"], h["n"], h["nhold"]))
if dc_ and "decomposition" in dc_:
    print("[DECOMP]")
    for k, v in dc_["decomposition"].items():
        print(f"   {k}: quantum {v['quantum_mean']:+.2f} [{v['quantum_q05']:+.2f},{v['quantum_q95']:+.2f}]  tempo {v['tempo_mean']:+.2f} [{v['tempo_q05']:+.2f},{v['tempo_q95']:+.2f}]  never-married change {v['never_married_change']:+.3f}")
if st and "stability_A_two_runs" in st:
    print("[STABILITY]")
    for n, v in st["stability_A_two_runs"].items():
        print(f"   {n:6s} run1 {v['run1']['q50']:.2f} [{v['run1']['q05']:.2f},{v['run1']['q95']:.2f}]  run2 {v['run2']['q50']:.2f} [{v['run2']['q05']:.2f},{v['run2']['q95']:.2f}]  gap {v['median_gap']:+.2f} = {v['gap_over_run1_sd']:+.2f} sd  overlap {v['both_overlap']}")
if fa:
    print("[FALSIFIERS]")
    for k in ("F1_parameter_recovery", "F2_scenario_recovery", "F3_permutation"):
        if k in fa: print("   ", k, json.dumps(fa[k])[:400])
if bs:
    print("[BENCH]")
    for r in bs["results"]:
        print("   ", r)
