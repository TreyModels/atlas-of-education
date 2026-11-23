"""ABC-PMC on the GPU near-port engine: same prior, same targets, same protocol as the CPU fit, so the
two engines can be compared.  This is NOT the published model (see results/PORT_NOTES.md); it is the
second engine for the engine-dependence test.
usage: fit_gpu.py A|B OUT.json [--rounds 4000,3000,3000,3000] [--keep 500] [--timecap 1800]
"""
import json, os, sys, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model as M
import dosecore as dc
from engine import GPUDose, targets_array, distances, make_spec

ap = argparse.ArgumentParser()
ap.add_argument("scen"); ap.add_argument("out")
ap.add_argument("--rounds", default="4000,3000,3000,3000"); ap.add_argument("--keep", type=int, default=500)
ap.add_argument("--seed", type=int, default=1); ap.add_argument("--nW", type=int, default=12)
ap.add_argument("--timecap", type=int, default=1800); ap.add_argument("--batch", type=int, default=8)
ap.add_argument("--panel", default="data/panel.json")
a = ap.parse_args()
SCEN = 0 if a.scen == "A" else 1
PAN = json.load(open(a.panel)); FIT = PAN["FIT"]
FGRID = [-1.2, 0., 1.2]; RIDGE = .1
D_ = len(M.PN)
B = a.batch; NRUN = B * len(FIT) * len(FGRID)
ENG = GPUDose(nW=a.nW, seed=a.seed, max_runs=NRUN, tmax=2012)


def evaluate(U, seeds, t0, ntot, tag):
    """U: [n,D] parameter matrix.  Returns mean distance per draw and the chosen country effect."""
    n = U.shape[0]; P = M.LO + U * (M.HI - M.LO)
    Dm = np.full(n, np.nan); FB = np.zeros((n, len(FIT)))
    done = 0
    for i0 in range(0, n, B):
        idx = list(range(i0, min(i0 + B, n)))
        pad = idx + [idx[-1]] * (B - len(idx))
        specs = []
        for j, di in enumerate(pad):
            for k, iso in enumerate(FIT):
                pc = PAN["countries"][iso]
                ds0 = j * len(FIT) * len(FGRID) + k * len(FGRID)
                prep = dc.prepare(pc, P[di], SCEN, 1000 + int(seeds[di]) % 100000, ds0)   # once per draw x country
                for fi, f in enumerate(FGRID):
                    specs.append(dict(prep=prep, P=P[di], fc=f, gap=pc["age_gap"]))
        ENG.load(specs)
        acc = ENG.run(SCEN)
        S = targets_array(acc)
        d = differences(S, P, pad)
        for j, di in enumerate(idx):
            sl = slice(j * len(FIT) * len(FGRID), (j + 1) * len(FIT) * len(FGRID))
            dd = d[sl].reshape(len(FIT), len(FGRID)) + RIDGE * np.square(np.array(FGRID))[None, :]
            best = np.argmin(dd, axis=1)
            Dm[di] = float(np.mean(dd[np.arange(len(FIT)), best])); FB[di] = np.array(FGRID)[best]
        done += len(idx)
        if done % (B * 20) == 0:
            print("  %s: %d/%d draws, %.0fs, %.2f draws/s" % (tag, done, n, time.time() - t0, done / (time.time() - t0)), flush=True)
    return Dm, FB


def differences(S, P, pad):
    """standardised squared error per run, same grouping as model.distance"""
    out = np.zeros(len(pad) * len(FIT) * len(FGRID))
    for j, di in enumerate(pad):
        for k, iso in enumerate(FIT):
            pc = PAN["countries"][iso]
            for fi in range(len(FGRID)):
                r = j * len(FIT) * len(FGRID) + k * len(FGRID) + fi
                z = []
                for g, key in (("tfr", "tfr"), ("asfr1519", "asfr1519"), ("smam", "smam"), ("m18", "m18")):
                    for y, v in pc[key].items():
                        y = int(y)
                        if y > 2012: continue
                        s = S[g][y][r]
                        if s is None or np.isnan(s): continue
                        z.append(((s - v) / dc.SD[{"tfr": "tfr", "asfr1519": "asfr", "smam": "smam", "m18": "m18"}[g]]) ** 2)
                out[r] = float(np.mean(z)) if z else np.nan
    return out


def logit(x): x = np.clip(x, 1e-6, 1 - 1e-6); return np.log(x / (1 - x))
def expit(z): return 1 / (1 + np.exp(-z))


if __name__ == "__main__":
    rng = np.random.default_rng(a.seed); sizes = [int(s) for s in a.rounds.split(",")]
    t0 = time.time(); hist = []; pop = None
    for r, n in enumerate(sizes):
        if time.time() - t0 > a.timecap:
            print("time cap before round", r, flush=True); break
        if pop is None:
            U = rng.random((n, D_)); logw = np.zeros(n)
        else:
            Uo, Wo = pop["u"], pop["w"]; Z = logit(Uo)
            cov = 2 * np.cov(Z.T, aweights=Wo) + 1e-6 * np.eye(D_); L = np.linalg.cholesky(cov)
            idx = rng.choice(len(Wo), n, p=Wo); U = expit(Z[idx] + rng.normal(size=(n, D_)) @ L.T)
            Zi = logit(U); invC = np.linalg.inv(cov); ldet = np.linalg.slogdet(cov)[1]; dens = np.zeros(n)
            for j0 in range(0, n, 500):
                dz = Zi[j0:j0 + 500, None, :] - Z[None, :, :]
                m = np.einsum("nki,ij,nkj->nk", dz, invC, dz); dens[j0:j0 + 500] = (Wo[None, :] * np.exp(-.5 * m)).sum(1)
            jac = (U * (1 - U)).prod(1); logw = -np.log(dens / (np.exp(.5 * ldet) * jac) + 1e-300)
        seeds = rng.integers(1, 10**7, n)
        Dm, FB = evaluate(U, seeds, t0, n, "round%d" % r)
        keep = np.argsort(Dm)[:a.keep]; w = np.exp(logw[keep] - logw[keep].max()); w /= w.sum()
        pop = dict(u=U[keep], w=w, D=Dm[keep], f=FB[keep], seed=seeds[keep])
        hist.append(dict(round=r, n=int(n), eps=float(Dm[keep].max()), best=float(Dm.min()),
                         median_kept=float(np.median(Dm[keep])), elapsed=time.time() - t0))
        print("ROUND %d done: %s" % (r, hist[-1]), flush=True)
        json.dump(dict(scen=a.scen, names=M.PN, lo=M.LO.tolist(), hi=M.HI.tolist(), u=pop["u"].tolist(),
                       w=pop["w"].tolist(), D=pop["D"].tolist(), f=pop["f"].tolist(), seed=pop["seed"].tolist(),
                       fit=FIT, hist=hist, engine="gpu-near-port", nW=a.nW, fgrid=FGRID, synthetic=False),
                  open(a.out, "w"))
    print("done %.0fs" % (time.time() - t0), flush=True)
