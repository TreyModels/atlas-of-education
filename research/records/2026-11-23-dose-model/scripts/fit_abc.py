"""ABC-PMC (population Monte Carlo ABC) fit of the dose model to the fit countries.
usage: fit_abc.py SCEN(A|B) OUT.json [--truth truth.json] [--rounds 8000,5000,5000,5000] [--keep 500] [--procs 24] [--seed 1]
Country-specific 'family-system strength' f_c is profiled out on a grid for every parameter draw."""
import json, sys, time, argparse, numpy as np
from multiprocessing import Pool
import model as M

ap = argparse.ArgumentParser(); ap.add_argument("scen"); ap.add_argument("out")
ap.add_argument("--truth"); ap.add_argument("--rounds", default="8000,5000,5000,5000"); ap.add_argument("--keep", type=int, default=500)
ap.add_argument("--procs", type=int, default=24); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--nW", type=int, default=12)
ap.add_argument("--panel", default="data/panel.json"); ap.add_argument("--init")
args = ap.parse_args()
SCEN = 0 if args.scen == "A" else 1
PAN = json.load(open(args.panel)); FIT = PAN["FIT"]
FGRID = [-1.2, 0., 1.2]; RIDGE = .1
D_ = len(M.PN)
if SCEN == 1: ACTIVE = np.array([n != "kappa" for n in M.PN])   # kappa has no role in B: keep it but flag
else: ACTIVE = np.ones(D_, bool)

def make_synthetic(tr):
    """Replace targets by simulated 'observations' from known parameters."""
    P = np.array(tr["theta"]); sc = 0 if tr["scen"] == "A" else 1; rng = np.random.default_rng(tr["seed"])
    for iso in FIT:
        pc = PAN["countries"][iso]; out = M.simulate(pc, P, sc, int(rng.integers(1e9)), tr["f"][iso], nW=40)
        S = M.summaries(out)
        for g, key, sd in (("tfr", "tfr", .10), ("asfr", "asfr1519", .004), ("smam", "smam", .4), ("m18", "m18", .015)):
            pc[key] = {y: float(S[g][int(y)] + rng.normal(0, sd)) for y in pc[key] if not np.isnan(S[g].get(int(y), np.nan))}
if args.truth: make_synthetic(json.load(open(args.truth)))

def evaluate(job):
    u, seed = job
    P = M.LO + u * (M.HI - M.LO); Dc, fb = [], []
    for k, iso in enumerate(FIT):
        pc = PAN["countries"][iso]; best = (1e9, 0.)
        for f, out in zip(FGRID, M.simulate_many(pc, P, SCEN, seed * 100 + k, FGRID, nW=args.nW)):
            S = M.summaries(out)
            d, _ = M.distance(S, pc); d = d + RIDGE * f * f
            if np.isnan(d): d = 1e6
            if d < best[0]: best = (d, f)
        Dc.append(best[0]); fb.append(best[1])
    return float(np.mean(Dc)), Dc, fb

def logit(x): x = np.clip(x, 1e-6, 1 - 1e-6); return np.log(x / (1 - x))
def expit(z): return 1 / (1 + np.exp(-z))

if __name__ == "__main__":
    rng = np.random.default_rng(args.seed); sizes = [int(s) for s in args.rounds.split(",")]
    t0 = time.time(); pool = Pool(args.procs); hist = []
    pop = None
    if args.init:
        z = json.load(open(args.init)); pop = dict(u=np.array(z['u']), w=np.ones(len(z['u'])) / len(z['u']))
    for r, n in enumerate(sizes):
        if pop is None or (args.init and r == 0 and False): U = rng.random((n, D_)); logw_prop = np.zeros(n)
        else:
            Uo, Wo = pop["u"], pop["w"]; Z = logit(Uo); mu = (Wo[:, None] * Z).sum(0)
            cov = 2 * np.cov(Z.T, aweights=Wo) + 1e-6 * np.eye(D_); L = np.linalg.cholesky(cov)
            idx = rng.choice(len(Wo), n, p=Wo); Zn = Z[idx] + rng.normal(size=(n, D_)) @ L.T; U = expit(Zn)
            # importance weight 1/sum_j w_j K(u|u_j) with K Gaussian in logit space (Jacobian cancels across draws up to u(1-u) factor)
            Zi = logit(U); invC = np.linalg.inv(cov); ldet = np.linalg.slogdet(cov)[1]
            dens = np.zeros(n)
            for j0 in range(0, n, 500):
                dz = Zi[j0:j0 + 500, None, :] - Z[None, :, :]
                m = np.einsum("nki,ij,nkj->nk", dz, invC, dz); dens[j0:j0 + 500] = (Wo[None, :] * np.exp(-.5 * m)).sum(1)
            jac = (U * (1 - U)).prod(1)           # u-space density = logit-space density / prod(u(1-u))
            logw_prop = -np.log(dens / (np.exp(.5 * ldet) * jac) + 1e-300)
        seeds = rng.integers(1, 10**7, n)
        res = pool.map(evaluate, list(zip(U, seeds)), chunksize=8)
        D = np.array([x[0] for x in res]); Dc = np.array([x[1] for x in res]); fb = np.array([x[2] for x in res])
        keep = np.argsort(D)[:args.keep]; w = np.exp(logw_prop[keep] - logw_prop[keep].max()); w /= w.sum()
        pop = dict(u=U[keep], w=w, D=D[keep], Dc=Dc[keep], f=fb[keep], seed=seeds[keep])
        eps = float(D[keep].max())
        hist.append(dict(round=r, n=n, eps=eps, best=float(D.min()), median_kept=float(np.median(D[keep])), elapsed=time.time() - t0))
        print(hist[-1], flush=True)
        json.dump(dict(scen=args.scen, names=M.PN, lo=M.LO.tolist(), hi=M.HI.tolist(), u=pop["u"].tolist(), w=pop["w"].tolist(), D=pop["D"].tolist(),
                       Dc=pop["Dc"].tolist(), f=pop["f"].tolist(), seed=pop["seed"].tolist(), fit=FIT, hist=hist, synthetic=bool(args.truth)), open(args.out, "w"))
