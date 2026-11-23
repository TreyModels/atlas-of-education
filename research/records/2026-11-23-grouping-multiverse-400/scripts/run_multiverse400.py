#!/usr/bin/env python3
"""Grouping multiverse: real groupings + 400 random-partition replicates.

Same estimator, same real groupings, same random-partition rule as
research/records/2026-11-23-grouping-multiverse/scripts/run_multiverse.py.
Changes: R=400 replicates (seeds 1000+r, so replicate r is exactly the draw the
74-replicate run would have used), per-worker BLAS/OpenMP threading capped at 1
(16 workers -> 16 threads total, the allotted share), per-replicate wall times
saved for the runtime report, and a resume-free final pickle.

The real-grouping pass (r=0) is deterministic and is kept as the whole-sample
reference; replicate r=1..400 are random re-partitions with the nesting rule
(different cuts of one measure share one random ordering, see gm_core.random_version).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, pickle, time, numpy as np
from multiprocessing import Pool
from scipy.stats import chi2
import gm_core as g

R = int(os.environ.get("GM_R", "400"))
NPROC = int(os.environ.get("GM_NPROC", "16"))
OUT = os.environ.get("GM_OUT", "out/final400.pkl")
G = g.make_groupings()


def run_groups(members_per_grouping, keep_full):
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
    meta = [dict(name=gg["name"], family=gg["family"], ordinal=gg["ordinal"],
                 groups=[(l, t, [g.ISOS[i] for i in m]) for l, t, m in gg["groups"]]) for gg in G]
    print(f"{len(G)} groupings, {sum(len(x['groups']) for x in G)} cells, {g.NE} edge-specs, "
          f"R={R} replicates, {NPROC} workers", flush=True)
    t0 = time.time(); res = {}
    with Pool(NPROC) as p:
        for r, out in p.imap_unordered(job, range(R + 1)):
            res[r] = out
            n = len(res)
            if n % 50 == 0:
                pickle.dump(dict(meta=meta, specs=g.SPECS, res=res,
                                 total_fits=sum(o["fits"] for o in res.values()) + res[0]["pooled"][4],
                                 runtime=round(time.time() - t0, 3)),
                            open(OUT + ".partial", "wb"))
            if r == 0 or n % 20 == 0:
                el = time.time() - t0
                eta = el / n * (R + 1 - n) if n < R + 1 else 0.0
                print(f"done {n}/{R+1}  {el:.0f}s  fits so far {sum(o['fits'] for o in res.values())}  "
                      f"eta {eta:.0f}s", flush=True)
    runtime = time.time() - t0
    total = sum(o["fits"] for o in res.values()) + res[0]["pooled"][4]
    walls = np.array([o["wall"] for k, o in res.items() if k > 0])
    print(f"TOTAL REGRESSIONS {total}  wall {runtime:.0f}s  "
          f"per-replicate mean {walls.mean():.2f}s min {walls.min():.2f}s max {walls.max():.2f}s", flush=True)
    pickle.dump(dict(meta=meta, specs=g.SPECS, res=res, total_fits=total,
                     runtime=round(runtime, 3), nproc=NPROC, R=R), open(OUT, "wb"))
    print("saved", OUT, flush=True)
