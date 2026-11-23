"""Coverage of the known parameter values by the equal-weight intervals from a synthetic-data recovery fit.
usage: recover_coverage.py results/rec_fitA.json data/truth_A.json
"""
import json, sys
import numpy as np
fit = json.load(open(sys.argv[1])); tr = json.load(open(sys.argv[2]))
u = np.array(fit["u"]); w = np.array(fit["w"]); lo = np.array(fit["lo"]); hi = np.array(fit["hi"])
th = lo + u * (hi - lo); truth = np.array(tr["theta"])
def wq(x, q):
    i = np.argsort(x); c = np.cumsum(w[i]) / w.sum(); return float(np.interp(q, c, x[i]))
print("accepted %d of %d, best error %.2f" % (fit["n_accepted"], fit["n_drawn"], min(fit["D"])))
cov = 0; rows = []
for n in ("th_k", "th_f", "kappa", "gam", "lam_s"):
    k = fit["names"].index(n); q05, q50, q95 = wq(th[:, k], .05), wq(th[:, k], .5), wq(th[:, k], .95)
    ok = q05 <= truth[k] <= q95; cov += ok
    rows.append(dict(name=n, truth=float(truth[k]), q05=q05, q50=q50, q95=q95, covered=bool(ok)))
    print("%-6s truth %.2f  fit %.2f [%.2f, %.2f]  covered %s" % (n, truth[k], q50, q05, q95, ok))
print("coverage %d of 5" % cov)
json.dump(dict(n_accepted=fit["n_accepted"], n_drawn=fit["n_drawn"], best=min(fit["D"]),
               coverage=cov, rows=rows), open(sys.argv[1].replace(".json", "_coverage.json"), "w"), indent=1)
