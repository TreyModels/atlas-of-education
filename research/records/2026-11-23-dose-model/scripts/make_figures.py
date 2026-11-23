"""Figures from results/analysis.json and the fit files. usage: make_figures.py results_dir"""
import json, sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = sys.argv[1]; A = json.load(open(f"{R}/analysis.json")); fa = json.load(open(f"{R}/fit_A.json")); fb = json.load(open(f"{R}/fit_B.json"))
pan = json.load(open(f"{R}/../data/panel.json"))
def th(fit, name):
    k = fit["names"].index(name); u = np.array(fit["u"])[:, k]; return fit["lo"][k] + u * (fit["hi"][k] - fit["lo"][k]), np.array(fit["w"]), fit["lo"][k], fit["hi"][k]
fig, ax = plt.subplots(1, 4, figsize=(15, 3.2))
for a, (n, lab) in zip(ax, [("th_k", "kin-support loss per full dose"), ("th_f", "wealth-flow reversal per full dose"), ("kappa", "cohort deepening"), ("gam", "career years at full dose")]):
    x, w, lo, hi = th(fa, n); a.hist(x, bins=20, range=(lo, hi), weights=w, color="#3b6ea5", alpha=.8, density=True); a.axhline(1 / (hi - lo), color="k", ls="--", lw=1); a.set_title(lab, fontsize=9)
plt.suptitle("Scenario A posterior (dashed = prior)"); plt.tight_layout(); plt.savefig(f"{R}/fig_posterior.png", dpi=110); plt.close()
H = A["holdout"]["predicted"]; hold = list(H["A"]); fig, ax = plt.subplots(2, 3, figsize=(12, 6))
for a, iso in zip(ax.ravel(), hold):
    ys = sorted(int(y) for y in H["A"][iso]["tfr_path_mean"]); a.plot(ys, [pan["countries"][iso]["tfr"][str(y)] for y in ys], "k-o", label="observed")
    for s, c in (("A", "#c0392b"), ("B", "#2471a3")): a.plot(ys, [H[s][iso]["tfr_path_mean"][str(y)] for y in ys], c + "", color=c, label=s)
    a.set_title(iso); a.set_ylim(0, 7)
ax[0, 0].legend(); plt.suptitle("Held-out countries: TFR, predicted without refitting"); plt.tight_layout(); plt.savefig(f"{R}/fig_holdout_tfr.png", dpi=110); plt.close()
d = A["decomposition"]; fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
for a, key in zip(ax, ["A_fit", "B_fit"]):
    dd = d["results"][key]["decomp"]["1980"]; names = d["dose_groups"] + ["national"]
    q = [dd[n]["quantum"] for n in names]; t = [dd[n]["tempo"] for n in names]
    a.bar(names, q, label="never born (quantum)", color="#8e44ad"); a.bar(names, t, bottom=q, label="postponed past 35 (tempo)", color="#f39c12")
    a.set_title(f"{key[0]}: fall in births per woman, 1940 -> 1980 cohort", fontsize=9); a.tick_params(axis="x", rotation=25, labelsize=7)
ax[0].legend(fontsize=7); plt.tight_layout(); plt.savefig(f"{R}/fig_tempo_quantum.png", dpi=110); plt.close()
