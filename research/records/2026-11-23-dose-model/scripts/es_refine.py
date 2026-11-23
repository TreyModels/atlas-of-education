"""Local (1+4) evolution-strategy refinement of the best ABC particles, in logit space; writes a population file
usable as --init for fit_abc.py. usage: es_refine.py SCEN fit.json out.json [chains] [gens]"""
import sys, json, numpy as np
sys.argv_ = sys.argv; scen, fin, fout = sys.argv[1:4]; nch = int(sys.argv[4]) if len(sys.argv) > 4 else 20; gens = int(sys.argv[5]) if len(sys.argv) > 5 else 50
sys.argv = ["x", scen, "/dev/null"]
import fit_abc as F
from multiprocessing import Pool
def logit(x): x = np.clip(x, 1e-4, 1 - 1e-4); return np.log(x / (1 - x))
def expit(z): return 1 / (1 + np.exp(-z))
def chain(args):
    u0, seed = args; rng = np.random.default_rng(seed); z = logit(u0); best = F.evaluate((expit(z), int(seed)))[0]; sig = .35
    for g in range(gens):
        imp = False
        for _ in range(4):
            zn = z + sig * rng.normal(size=z.shape); d = F.evaluate((expit(zn), int(rng.integers(1, 10**7))))[0]
            if d < best: best, z, imp = d, zn, True
        sig *= 1.1 if imp else .93
    d, Dc, fb = F.evaluate((expit(z), int(seed)))
    return expit(z), d, Dc, fb, int(seed)
if __name__ == "__main__":
    fit = json.load(open(fin)); idx = np.argsort(fit["D"])[:nch]
    with Pool(nch) as p: res = p.map(chain, [(np.array(fit["u"][i]), 100 + k) for k, i in enumerate(idx)])
    json.dump(dict(u=[r[0].tolist() for r in res], D=[r[1] for r in res], Dc=[r[2] for r in res], f=[r[3] for r in res], seed=[r[4] for r in res]), open(fout, "w"))
    print("ES done", sorted(r[1] for r in res)[:5], flush=True)
