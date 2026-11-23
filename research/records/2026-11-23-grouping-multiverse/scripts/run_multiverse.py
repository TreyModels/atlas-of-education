#!/usr/bin/env python3
"""Run real groupings (+ whole-sample reference) and R random-partition replicates in parallel."""
import sys, pickle, time, numpy as np
from multiprocessing import Pool
from scipy.stats import chi2
import gm_core as g

R = int(sys.argv[1]); NPROC = int(sys.argv[2]); OUT = sys.argv[3]
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
    if r == 0:
        parts = [[m for _, _, m in gg["groups"]] for gg in G]
        res = run_groups(parts, True)
        allm = g.mask(np.arange(g.C))
        res["pooled"] = g.fit_cell(allm)
        return r, res
    rng = np.random.default_rng(1000 + r)
    return r, run_groups(g.random_version(G, rng), False)


if __name__ == "__main__":
    meta = [dict(name=gg["name"], family=gg["family"], ordinal=gg["ordinal"],
                 groups=[(l, t, [g.ISOS[i] for i in m]) for l, t, m in gg["groups"]]) for gg in G]
    print(f"{len(G)} groupings, {sum(len(x['groups']) for x in G)} cells, {g.NE} edge-specs", flush=True)
    t0 = time.time(); res = {}
    with Pool(NPROC) as p:
        for r, out in p.imap_unordered(job, range(R + 1)):
            res[r] = out
            if len(res) % 25 == 0:
                pickle.dump(dict(meta=meta, specs=g.SPECS, res=res, total_fits=sum(o['fits'] for o in res.values()) + res[0]['pooled'][4]), open(OUT + '.partial', 'wb'))
            if r == 0 or len(res) % 20 == 0:
                print(f"done {len(res)}/{R+1}  {time.time()-t0:.0f}s  fits so far {sum(o['fits'] for o in res.values())}", flush=True)
    total = sum(o["fits"] for o in res.values()) + res[0]["pooled"][4]
    print("TOTAL REGRESSIONS", total, flush=True)
    pickle.dump(dict(meta=meta, specs=g.SPECS, res=res, total_fits=total), open(OUT, "wb"))
