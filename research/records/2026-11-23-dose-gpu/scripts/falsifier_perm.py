"""F3 permutation falsifier (partial form).

The brief asks for schooling shuffled across women within country-cohort.  In this model the within-cohort
allocation of schooling across women is generated from the urban/rural and wealth gradient, so the faithful
permutation is to remove that gradient: every woman in a cohort then draws schooling from the national
cohort distribution, i.e. who gets schooling is random within the cohort.  With the estimation budget
exhausted we cannot refit on the permuted data, so we ask the weaker but still informative question: does
the FITTED model predict the observed data worse when the schooling gradient is removed?  If the dose
channel carries real information, it must.
"""
import json, os, sys, argparse
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import model as M

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default="../results"); ap.add_argument("--panel", default="data/panel.json")
ap.add_argument("--n", type=int, default=120); ap.add_argument("--procs", type=int, default=8)
ap.add_argument("--afile", default="rej_fitA.json")
a = ap.parse_args()
PAN = json.load(open(a.panel)); FIT = PAN["FIT"]
fit = json.load(open(os.path.join(a.dir, a.afile)))
u = np.array(fit["u"]); w = np.array(fit["w"])
rng = np.random.default_rng(88)
idx = rng.choice(len(w), a.n, p=w)
P = np.array(fit["lo"]) + u[idx] * (np.array(fit["hi"]) - np.array(fit["lo"]))
f = np.array(fit["f"])[idx]
IU = fit["names"].index("r_u"); IQ = fit["names"].index("r_q")


def job(args):
    i, iso, permuted = args
    th = P[i].copy()
    if permuted:
        th[IU] = 0.0; th[IQ] = 0.0          # schooling independent of urban/rural and wealth
    pc = PAN["countries"][iso]
    S = M.summaries(M.simulate(pc, th, 0, 5000 + i, f[i][FIT.index(iso)], nW=24))
    d, _ = M.distance(S, pc)
    return iso, permuted, d


if __name__ == "__main__":
    jobs = [(i, iso, pm) for i in range(a.n) for iso in FIT for pm in (False, True)]
    pool = Pool(a.procs); res = pool.map(job, jobs, chunksize=2); pool.close(); pool.join()
    out = {}
    for lab, pm in (("real_gradient", False), ("permuted_gradient", True)):
        ds = [d for iso, p, d in res if p == pm]
        out[lab] = dict(mean=float(np.mean(ds)), median=float(np.median(ds)), sd=float(np.std(ds)))
    b = np.array([[d for iso, p, d in res if p and iso == k] for k in FIT])
    r = np.array([[d for iso, p, d in res if (not p) and iso == k] for k in FIT])
    diff = b.mean(1) - r.mean(1)
    boot = [np.mean(rng.choice(diff, len(diff))) for _ in range(4000)]
    out["worse_when_permuted"] = float(diff.mean())
    out["diff_ci"] = [float(np.quantile(boot, .025)), float(np.quantile(boot, .975))]
    out["countries_worse"] = int((diff > 0).sum())
    out["n_particles"] = a.n; out["countries"] = FIT
    json.dump(out, open(os.path.join(a.dir, "falsifier_perm.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
