"""Plain ABC rejection: draw from the prior, simulate, keep every draw within a FIXED distance tolerance.
Equal weights, so the effective sample size equals the number of accepted draws by construction.  This is
the weight-free fallback used because the ABC-PMC importance weights collapsed (see README).
usage: reject_abc.py A|B OUT.json [--eps 14.5] [--n 4000] [--procs 6]
"""
import json, os, sys, time, argparse
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import model as M

ap = argparse.ArgumentParser()
ap.add_argument("scen"); ap.add_argument("out")
ap.add_argument("--eps", type=float, required=True); ap.add_argument("--n", type=int, default=4000)
ap.add_argument("--procs", type=int, default=6); ap.add_argument("--seed", type=int, default=5)
ap.add_argument("--nW", type=int, default=12); ap.add_argument("--timecap", type=int, default=2400)
ap.add_argument("--panel", default="data/panel.json")
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


if __name__ == "__main__":
    rng = np.random.default_rng(a.seed); t0 = time.time()
    U = rng.random((a.n, D_)); pool = Pool(a.procs)
    res, acc = [], []
    for i, x in enumerate(pool.imap_unordered(evaluate, [(U[j], int(rng.integers(1, 10**7))) for j in range(a.n)], chunksize=4)):
        res.append((i, x))
        if (i + 1) % 250 == 0:
            print("  %d/%d draws, %d accepted (%.1f%%), %.0fs, %.2f draws/s" % (
                i + 1, a.n, len(acc), 100 * len(acc) / (i + 1), time.time() - t0, (i + 1) / (time.time() - t0)), flush=True)
        if time.time() - t0 > a.timecap: print("time cap", flush=True); break
    pool.close(); pool.join()
    idx = [j for j, _ in res]; dist = np.array([x[0] for _, x in res]); Dc = np.array([x[1] for _, x in res]); fb = np.array([x[2] for _, x in res])
    keep = dist <= a.eps
    out = dict(scen=a.scen, names=M.PN, lo=M.LO.tolist(), hi=M.HI.tolist(), engine="original-numba-rejection",
               u=U[idx][keep].tolist(), w=(np.ones(keep.sum()) / max(keep.sum(), 1)).tolist(),
               D=dist[keep].tolist(), Dc=Dc[keep].tolist(), f=fb[keep].tolist(), eps=a.eps,
               n_drawn=int(len(dist)), n_accepted=int(keep.sum()), acceptance=float(keep.mean()),
               hist=[dict(drawn=int(len(dist)), accepted=int(keep.sum()), eps=a.eps, elapsed=time.time() - t0)])
    json.dump(out, open(a.out, "w"))
    print("DONE drawn=%d accepted=%d (%.1f%%) ESS=%d wrote %s" % (len(dist), keep.sum(), 100 * keep.mean(), keep.sum(), a.out), flush=True)
