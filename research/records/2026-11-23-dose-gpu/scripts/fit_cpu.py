"""ABC-PMC on the ORIGINAL published numba model (the exact model), multiprocess on the allotted cores.
Time-capped: writes results after every round, so a partial campaign is always usable.
usage: fit_cpu.py A|B OUT.json [--rounds 15000,10000,10000] [--keep 500] [--procs 6] [--timecap 5400]
"""
import json, os, sys, time, argparse, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root holds model.py
from multiprocessing import Pool
import model as M

ap = argparse.ArgumentParser(); ap.add_argument("scen"); ap.add_argument("out")
ap.add_argument("--rounds", default="15000,10000,10000"); ap.add_argument("--keep", type=int, default=500)
ap.add_argument("--procs", type=int, default=6); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--nW", type=int, default=12); ap.add_argument("--timecap", type=int, default=5400)
ap.add_argument("--panel", default="data/panel.json"); ap.add_argument("--init")
a = ap.parse_args()
SCEN = 0 if a.scen == "A" else 1
PAN = json.load(open(a.panel)); FIT = PAN["FIT"]
FGRID = [-1.2, 0., 1.2]; RIDGE = .1
D_ = len(M.PN)

def evaluate(job):
    u, seed = job
    P = M.LO + u * (M.HI - M.LO); Dc, fb = [], []
    for k, iso in enumerate(FIT):
        pc = PAN["countries"][iso]; best = (1e9, 0.)
        for f, out in zip(FGRID, M.simulate_many(pc, P, SCEN, seed * 100 + k, FGRID, nW=a.nW)):
            S = M.summaries(out); d, _ = M.distance(S, pc); d = d + RIDGE * f * f
            if np.isnan(d): d = 1e6
            if d < best[0]: best = (d, f)
        Dc.append(best[0]); fb.append(best[1])
    return float(np.mean(Dc)), Dc, fb

def logit(x): x = np.clip(x, 1e-6, 1 - 1e-6); return np.log(x / (1 - x))
def expit(z): return 1 / (1 + np.exp(-z))

if __name__ == "__main__":
    rng = np.random.default_rng(a.seed); sizes = [int(s) for s in a.rounds.split(",")]
    t0 = time.time(); pool = Pool(a.procs); hist = []; pop = None
    for r, n in enumerate(sizes):
        if time.time() - t0 > a.timecap:
            print("time cap hit before round", r, flush=True); break
        if pop is None:
            U = rng.random((n, D_)); logw = np.zeros(n)
        else:
            Uo, Wo = pop["u"], pop["w"]; Z = logit(Uo); mu = (Wo[:, None] * Z).sum(0)
            cov = 2 * np.cov(Z.T, aweights=Wo) + 1e-6 * np.eye(D_); L = np.linalg.cholesky(cov)
            idx = rng.choice(len(Wo), n, p=Wo); U = expit(Z[idx] + rng.normal(size=(n, D_)) @ L.T)
            Zi = logit(U); invC = np.linalg.inv(cov); ldet = np.linalg.slogdet(cov)[1]; dens = np.zeros(n)
            for j0 in range(0, n, 500):
                dz = Zi[j0:j0 + 500, None, :] - Z[None, :, :]
                m = np.einsum("nki,ij,nkj->nk", dz, invC, dz); dens[j0:j0 + 500] = (Wo[None, :] * np.exp(-.5 * m)).sum(1)
            jac = (U * (1 - U)).prod(1); logw = -np.log(dens / (np.exp(.5 * ldet) * jac) + 1e-300)
        seeds = rng.integers(1, 10**7, n)
        res = []
        for i, x in enumerate(pool.imap_unordered(evaluate, list(zip(U, seeds)), chunksize=4)):
            res.append(x)
            if (i + 1) % 500 == 0:
                print("  round %d: %d/%d draws, %.0fs elapsed, %.2f draws/s" % (r, i + 1, n, time.time() - t0, (i + 1) / (time.time() - t0)), flush=True)
        D = np.array([x[0] for x in res]); Dc = np.array([x[1] for x in res]); fb = np.array([x[2] for x in res])
        keep = np.argsort(D)[:a.keep]; w = np.exp(logw[keep] - logw[keep].max()); w /= w.sum()
        pop = dict(u=U[keep], w=w, D=D[keep], Dc=Dc[keep], f=fb[keep], seed=seeds[keep])
        eps = float(D[keep].max())
        hist.append(dict(round=r, n=int(n), eps=eps, best=float(D.min()), median_kept=float(np.median(D[keep])), elapsed=time.time() - t0))
        print(hist[-1], flush=True)
        print("ROUND %d complete: n=%d best=%.4f eps(keep max)=%.4f elapsed=%.0fs rate=%.2f draws/s" % (
            r, n, hist[-1]["best"], eps, hist[-1]["elapsed"], n / max(hist[-1]["elapsed"], 1e-9)), flush=True)
        json.dump(dict(scen=a.scen, names=M.PN, lo=M.LO.tolist(), hi=M.HI.tolist(), u=pop["u"].tolist(), w=pop["w"].tolist(),
                       D=pop["D"].tolist(), Dc=pop["Dc"].tolist(), f=pop["f"].tolist(), seed=pop["seed"].tolist(),
                       fit=FIT, hist=hist, engine="original-numba", nW=a.nW, synthetic=False), open(a.out, "w"))
    print("done %.0fs" % (time.time() - t0), flush=True)
