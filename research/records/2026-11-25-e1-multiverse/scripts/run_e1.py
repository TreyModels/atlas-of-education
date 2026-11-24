#!/usr/bin/env python3
"""E1 resumable runner: real pass + R random-partition replicates, one checkpoint file per replicate.

Identical estimator and seeds to run_multiverse400.py (branch research/grouping-multiverse-400-2026-11-23
@ 1152cec): replicate r uses numpy.random.default_rng(1000+r). The only change is checkpointing and resume.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, time, numpy as np
from multiprocessing import Pool
from scipy.stats import chi2

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gm_core as g

G = g.make_groupings()   # deterministic; workers inherit via fork

R = int(os.environ.get("GM_R", "1200"))
NPROC = int(os.environ.get("GM_NPROC", "8"))
OUT = os.environ.get("GM_OUT", "/root/work/e1/out")
REPS = os.path.join(OUT, "reps")
os.makedirs(REPS, exist_ok=True)
PROGRESS = os.path.join(OUT, "progress.log")


def run_groups(members_per_grouping, keep_full=False):
    z_cells = []; b_all = []; se_all = []; n_fits = 0
    Qp = []; flip = []
    for parts in members_per_grouping:
        bs, ss = [], []
        for m in parts:
            b, se, n, nc, k = g.fit_cell(g.mask(m)); n_fits += k
            bs.append(b); ss.append(se)
            z_cells.append(b / se)
            if keep_full: b_all.append((b, se, n, nc))
        bs = np.array(bs); ss = np.array(ss)
        ok = np.isfinite(bs) & (ss > 0)
        w = np.where(ok, 1 / ss ** 2, 0)
        sw = w.sum(0); bw = (w * np.where(ok, bs, 0)).sum(0) / np.maximum(sw, 1e-300)
        Q = (w * np.where(ok, (bs - bw) ** 2, 0)).sum(0); df = ok.sum(0) - 1
        p = np.where(df >= 1, chi2.sf(Q, np.maximum(df, 1)), np.nan)
        z = bs / ss
        fl = ((np.where(ok, z, 0) > 1.96).any(0) & (np.where(ok, z, 0) < -1.96).any(0))
        Qp.append(p); flip.append(np.where(df >= 1, fl, False))
    return dict(z=np.array(z_cells, dtype=np.float32), Qp=np.array(Qp, dtype=np.float32),
                flip=np.array(flip), fits=n_fits, full=b_all if keep_full else None)


def job(r):
    t = time.time()
    if r == 0:
        parts = [[m for _, _, m in gg["groups"]] for gg in G]
        res = run_groups(parts, True)
        res["pooled"] = g.fit_cell(g.mask(np.arange(g.C)))
    else:
        rng = np.random.default_rng(1000 + r)
        res = run_groups(g.random_version(G, rng), False)
    res["wall"] = round(time.time() - t, 3)
    return r, res


if __name__ == "__main__":
    meta = dict(n_groupings=len(G), cells=sum(len(x["groups"]) for x in G), NE=g.NE, C=g.C,
                R=R, nproc=NPROC)
    print(f"{meta['n_groupings']} groupings, {meta['cells']} cells, {g.NE} edge-specs, R={R}, "
          f"{NPROC} workers", flush=True)
    todo = [r for r in range(R + 1) if not os.path.exists(os.path.join(REPS, f"r{r:04d}.npz"))]
    print(f"checkpoints present: {R + 1 - len(todo)}; todo: {len(todo)}", flush=True)
    t0 = time.time(); done = 0
    with Pool(NPROC) as p:
        for r, res in p.imap_unordered(job, todo):
            path = os.path.join(REPS, f"r{r:04d}.npz")
            if r == 0:
                b, se, n, nc, k = res["pooled"]
                np.savez(path, z=res["z"], Qp=res["Qp"], flip=res["flip"], wall=res["wall"],
                         fits=res["fits"], pooled_b=b, pooled_se=se, pooled_n=n, pooled_nc=nc,
                         pooled_k=k)
            else:
                np.savez(path, z=res["z"], Qp=res["Qp"], flip=res["flip"], wall=res["wall"],
                         fits=res["fits"])
            done += 1
            with open(PROGRESS, "a") as fh:
                fh.write(f"{r}\t{res['wall']}\t{time.time() - t0:.1f}\t{done}/{len(todo)}\n")
            if done % 10 == 0 or done == len(todo):
                print(f"[{done}/{len(todo)}] r={r} wall={res['wall']}s "
                      f"elapsed={time.time() - t0:.0f}s", flush=True)
    json_txt = str(meta) + f"\ntotal_wall={time.time() - t0:.1f}\n"
    open(os.path.join(OUT, "run_meta.txt"), "w").write(json_txt)
    print("DONE", json_txt)
