"""Write results/summary.md and results/recovery.json from analysis.json and recovery fits."""
import json, numpy as np
R = "results"; A = json.load(open(f"{R}/analysis.json")); names = ["th_k", "th_f", "kappa", "gam", "lam_s"]
def post(fit):
    u = np.array(fit["u"]); w = np.array(fit["w"]); lo, hi = np.array(fit["lo"]), np.array(fit["hi"]); th = lo + u * (hi - lo)
    def q(k, p):
        x = th[:, k]; i = np.argsort(x); c = np.cumsum(w[i]) / w.sum(); return float(np.interp(p, c, x[i]))
    return {n: (q(fit["names"].index(n), .05), q(fit["names"].index(n), .5), q(fit["names"].index(n), .95)) for n in fit["names"]}, np.array(fit["D"])
rec = {}; L = []
for t in "AB":
    tr = json.load(open(f"data/truth_{t}.json"))
    for s in "AB":
        f = json.load(open(f"{R}/recovery/truth{t}_fit{s}.json")); p, D = post(f)
        rec[f"truth{t}_fit{s}"] = dict(best_D=float(D.min()), median_D=float(np.median(D)), params={n: dict(truth=tr["theta"][f["names"].index(n)], q05=p[n][0], q50=p[n][1], q95=p[n][2]) for n in names})
json.dump(rec, open(f"{R}/recovery.json", "w"), indent=1)
L.append("## Recovery (synthetic data from known parameters)\n\n| data from | fitted as | best distance | parameter: truth [5%, 50%, 95% of fit] |\n|---|---|---|---|")
for k, v in rec.items():
    L.append(f"| {k[5]} | {k[-1]} | {v['best_D']:.2f} | " + "; ".join(f"{n}: {d['truth']:.2f} [{d['q05']:.2f}, {d['q50']:.2f}, {d['q95']:.2f}]" for n, d in v["params"].items() if not (k[-1] == "B" and n == "kappa")) + " |")
L.append("\n## Real-data posterior (final population)\n")
for s in "AB":
    L.append(f"Scenario {s}: best in-sample distance {A['in_sample_D'][s]['best']:.2f}, median {A['in_sample_D'][s]['median']:.2f}\n")
    for n in names:
        d = A["posterior"][s][n]; L.append(f"- {n}: median {d['q50']:.2f}  90% [{d['q05']:.2f}, {d['q95']:.2f}]  posterior/prior sd {d['post_over_prior_sd']:.2f}")
    L.append("")
c = A["holdout_compare"]; L.append(f"## Held-out\nmean D A {c['mean_D_A']:.1f} vs B {c['mean_D_B']:.1f}; diff {c['diff_A_minus_B']:.1f} (95% [{c['boot_q025']:.1f}, {c['boot_q975']:.1f}]); A better in {c['countries_A_better']}/6; ensemble TFR RMSE {c['ensemble_tfr_rmse']}\n")
L.append("| country | D_A | D_B |\n|---|---|---|")
for i, iso in enumerate(c["countries"]): L.append(f"| {iso} | {c['D_A'][i]:.1f} | {c['D_B'][i]:.1f} |")
for s in "AB":
    for lab in ("fit", "holdout"):
        d = A["decomposition"]["results"][f"{s}_{lab}"]["decomp"]["1980"]
        L.append(f"\nDecomposition {s} ({lab} countries), births per woman lost, 1940 -> 1980 cohort: " + "; ".join(f"{k}: quantum {v['quantum']:.2f}, tempo {v['tempo']:.2f}" for k, v in d.items() if k != "national_never_married_change"))
open(f"{R}/summary.md", "w").write("\n".join(L)); print("\n".join(L))
