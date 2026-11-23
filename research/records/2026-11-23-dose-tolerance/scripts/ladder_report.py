"""Tolerance ladder: does tightening the ABC tolerance narrow the dose-model intervals?

Reads the equal-weight rejection-ABC result files (one per tolerance) and prints/writes:
  * accepted count, acceptance rate, effective sample size (= accepted, by construction)
  * the distance distribution of accepted draws, so a reader can see whether a tight tolerance leaves a
    tiny, selected set
  * posterior median and 90% interval for the five reported strengths, and the posterior spread as a
    fraction of the prior spread
usage: ladder_report.py --dir ../results --files rej_A_eps20.json rej_A_eps10.json rej_A_eps05.json
"""
import json, os, sys, argparse
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("--dir", default="../results")
ap.add_argument("--files", nargs="+", required=True)
ap.add_argument("--labels", nargs="+", default=None)
ap.add_argument("--out", default="ladder.json")
a = ap.parse_args()
REPORT = [("th_k", "kin-support loss per full dose"), ("th_f", "downward money flow"),
          ("kappa", "cohort deepening"), ("gam", "career delay"), ("lam_s", "marriage-market pickiness")]


def wq(x, w, q):
    i = np.argsort(x); c = np.cumsum(w[i]) / w.sum(); return float(np.interp(q, c, x[i]))


rows = []
for k, f in enumerate(a.files):
    p = os.path.join(a.dir, f)
    if not os.path.exists(p): print("missing", p); continue
    d = json.load(open(p))
    u = np.array(d["u"]); w = np.array(d["w"]); lo = np.array(d["lo"]); hi = np.array(d["hi"])
    th = lo + u * (hi - lo); D = np.array(d["D"])
    row = dict(label=(a.labels[k] if a.labels else f), file=f, eps=d.get("eps"),
               drawn=d.get("n_drawn"), accepted=int(len(D)), ess=float(1 / np.sum(w ** 2)),
               acceptance=float(len(D) / max(d.get("n_drawn", len(D)), 1)),
               dist=dict(min=float(D.min()), q25=float(np.quantile(D, .25)), median=float(np.median(D)),
                         q75=float(np.quantile(D, .75)), max=float(D.max())))
    row["params"] = {}
    for n, pretty in REPORT:
        i = d["names"].index(n); sd = float(np.sqrt((w * (th[:, i] - (w * th[:, i]).sum()) ** 2).sum()))
        prior_sd = (hi[i] - lo[i]) / np.sqrt(12)
        row["params"][n] = dict(pretty=pretty, q05=wq(th[:, i], w, .05), q50=wq(th[:, i], w, .5),
                                q95=wq(th[:, i], w, .95), spread=sd / prior_sd,
                                width=(wq(th[:, i], w, .95) - wq(th[:, i], w, .05)),
                                prior_width=float(hi[i] - lo[i]))
    rows.append(row)
json.dump(rows, open(os.path.join(a.dir, a.out), "w"), indent=1)
print("| tolerance | draws drawn | accepted | acceptance | accepted-distance median [min, max] |")
print("|---|---|---|---|---|")
for r in rows:
    print("| %s | %s | %d | %.1f%% | %.2f [%.2f, %.2f] |" % (r["label"], r["drawn"], r["accepted"],
          100 * r["acceptance"], r["dist"]["median"], r["dist"]["min"], r["dist"]["max"]))
print()
print("| strength | " + " | ".join(r["label"] + " median [90%] (spread/prior)" for r in rows) + " |")
print("|---|" + "---|" * len(rows))
for n, pretty in REPORT:
    cells = []
    for r in rows:
        q = r["params"][n]
        cells.append("%.2f [%.2f, %.2f] (%.2f)" % (q["q50"], q["q05"], q["q95"], q["spread"]))
    print("| %s | %s |" % (pretty, " | ".join(cells)))
