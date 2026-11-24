#!/usr/bin/env python3
"""E1 analysis: full BH and BY verdicts for all 272 links, per family, at each R.

Families (as in the committed analysis): up (real significance share >= null), down (<= null),
sign-flip (real flip rate <= null), heterogeneity (real Q rate >= null). Four separate procedures,
each a BH/BY over its own 272-link p-vector (trend specification; FE parity reported as sensitivity).

Reads per-replicate checkpoints written by run_e1.py. Writes:
  results/summary_by_R.json   counts certified under BH and BY at each R, floors, first-certifying ranks
  results/verdict_by_R.csv    per link, per R: empirical p, BH q, BY q, certified flags (four families)
  results/split_halves.json   split-half stability at the largest R
  results/repro400.json       comparison of the R=400 analysis with the committed headline (panel-vintage diff)
"""
import os, sys, json, csv
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gm_core as g

OUT = os.environ.get("GM_OUT", "/root/work/e1/out")
REPS = os.path.join(OUT, "reps")
RES = os.path.join(ROOT, "results")
DATA = os.path.join(ROOT, "data")
os.makedirs(RES, exist_ok=True)
ALPHA = 0.05
RLIST = [20, 74, 400, 800, 1200]

# ---- inspect replicate-derived quantities exactly as analyse400.py ----
G = g.make_groupings()
meta = [dict(name=gg["name"], family=gg["family"], ordinal=gg["ordinal"]) for gg in G]
cells = []
for gi, gg in enumerate(G):
    for l, t, m in gg["groups"]:
        cells.append((gi, gg["family"], t, len(m)))
gidx = np.array([c[0] for c in cells]); fam = np.array([c[1] for c in cells])
fams = sorted(set(fam))
G_of_fam = {f: sorted({c[0] for c in cells if c[1] == f}) for f in fams}
NP = g.NE // 2
J = np.arange(1, g.NE, 2)          # trend-specification indices of the 272 links
SCHOOL = {"lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter"}


def sigmat(z, sref):
    return np.where(np.isfinite(z), ((np.abs(z) > 1.96) & (np.sign(z) == sref)).astype(float), np.nan)


def both(z, sref):
    s = sigmat(z, sref); b = np.full_like(s, np.nan)
    b[:, 0::2] = np.where(np.isnan(s[:, 0::2]) | np.isnan(s[:, 1::2]), np.nan,
                          s[:, 0::2] * s[:, 1::2])
    b[:, 1::2] = b[:, 0::2]
    return b


def shares(S):
    per_g = np.full((len(G), S.shape[1]), np.nan)
    for gi in range(len(G)):
        m = gidx == gi
        if m.any():
            per_g[gi] = np.nanmean(S[m], 0)
    per_f = np.full((len(fams), S.shape[1]), np.nan)
    for k, f in enumerate(fams):
        per_f[k] = np.nanmean(per_g[G_of_fam[f]], 0)
    return np.nanmean(per_f, 0), per_f, per_g


def rate(arr):
    pf = np.array([np.nanmean(arr[G_of_fam[f]], 0) for f in fams])
    return np.nanmean(pf, 0), pf


def emp_p(real, null, side):
    fin = np.isfinite(null); valid = fin.sum(0)
    if side == "up":
        cnt = np.nansum(np.where(fin, null >= real, 0), 0)
    else:
        cnt = np.nansum(np.where(fin, null <= real, 0), 0)
    return (1 + cnt) / (1 + valid)


def emp_p_lib(real, null, side):
    fin = np.isfinite(null); valid = fin.sum(0)
    cnt = np.nansum(np.where(fin, null >= real, 0) if side == "up"
                    else np.where(fin, null <= real, 0), 0)
    return np.where(valid > 0, cnt / np.maximum(valid, 1), np.nan)


def bh_vec(p, m=None):
    p = np.asarray(p, float); m = int(np.isfinite(p).sum()) if m is None else m
    out = np.full_like(p, np.nan)
    idx = np.where(np.isfinite(p))[0]
    if len(idx) == 0:
        return out
    o = idx[np.argsort(p[idx])]
    q = p[o] * len(idx) / np.arange(1, len(idx) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out[o] = np.minimum(q, 1)
    return out


def by_vec(p, m=272):
    H = np.sum(1.0 / np.arange(1, m + 1))
    p = np.asarray(p, float)
    out = np.full_like(p, np.nan)
    idx = np.where(np.isfinite(p))[0]
    if len(idx) == 0:
        return out
    o = idx[np.argsort(p[idx])]
    q = p[o] * m * H / np.arange(1, len(idx) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out[o] = np.minimum(q, 1)
    return out


def first_rank(p, proc):
    p = np.sort(np.asarray(p, float)[np.isfinite(p)])
    if len(p) == 0:
        return None
    if proc == "BH":
        line = np.arange(1, len(p) + 1) * ALPHA / 272
    else:
        H = np.sum(1.0 / np.arange(1, 273)); line = np.arange(1, len(p) + 1) * ALPHA / (272 * H)
    ok = np.where(p <= line)[0]
    return int(ok[0] + 1) if len(ok) else None


# ---- load real pass and replicates ----
z0 = np.load(os.path.join(REPS, "r0000.npz"))
Zr = z0["z"]; pooled_b = z0["pooled_b"]; pooled_se = z0["pooled_se"]
sref = np.sign(pooled_b)
Tr_sig, Fr_sig, _ = shares(sigmat(Zr, sref))
Tr_both = shares(both(Zr, sref))[0]
Qr = np.where(np.isfinite(z0["Qp"]), (z0["Qp"] < 0.05).astype(float), np.nan)
flr = np.where(np.isfinite(z0["Qp"]), z0["flip"].astype(float), np.nan)
QR, QRf = rate(Qr); FR, FRf = rate(flr)
pz = pooled_b / pooled_se

avail = sorted(int(f[1:5]) for f in os.listdir(REPS) if f.startswith("r") and f.endswith(".npz") and f != "r0000.npz")
Rmax = max(avail) if avail else 0
print("available draws:", Rmax, flush=True)
use = [r for r in avail]
zts = []; qps = []; flps = []
for r in use:
    d = np.load(os.path.join(REPS, f"r{r:04d}.npz"))
    zts.append(d["z"]); qps.append(d["Qp"]); flps.append(d["flip"])
nullT = np.array([shares(sigmat(z, sref))[0] for z in zts], float)
nullB = np.array([shares(both(z, sref))[0] for z in zts], float)
nQ = np.array([rate(np.where(np.isfinite(q), (q < 0.05).astype(float), np.nan))[0] for q in qps])
nF = np.array([rate(np.where(np.isfinite(q), f.astype(float), np.nan))[0] for q, f in zip(qps, flps)])


def analysis(subset, label):
    idx = np.asarray(subset)
    nt = nullT[idx]; nb = nullB[idx]; nq = nQ[idx]; nf = nF[idx]
    R = len(idx)
    out = dict(R=R, floor=float(1.0 / (R + 1)), label=label, families={})
    pset = {}
    for proc, side in (("up", "up"), ("down", "dn"), ("flip", "dn"), ("het", "up")):
        data = {"up": (Tr_sig, nt), "down": (Tr_sig, nt), "flip": (FR, nf), "het": (QR, nq)}[proc]
        real, null = data
        p = emp_p(real, null, side)
        p_lib = emp_p_lib(real, null, side)
        q_bh = bh_vec(p[J]); q_by = by_vec(p[J])
        q_bh_lib = bh_vec(p_lib[J]); q_by_lib = by_vec(p_lib[J])
        pset[proc] = p
        out["families"][proc] = dict(
            certified_BH=int(np.nansum(q_bh < ALPHA)),
            certified_BY=int(np.nansum(q_by < ALPHA)),
            certified_BH_liberal=int(np.nansum(q_bh_lib < ALPHA)),
            certified_BY_liberal=int(np.nansum(q_by_lib < ALPHA)),
            n_floor=int(np.nansum(p[J] <= 1.0 / (R + 1) + 1e-15)),
            rank_floor=int(np.nansum(p[J] <= 1.0 / (R + 1) + 1e-15)),
            first_rank_BH=first_rank(p[J], "BH"), first_rank_BY=first_rank(p[J], "BY"),
            p=p[J], q_bh=q_bh, q_by=q_by)
    # parity-136 sensitivity for BH/BY
    for proc in ("up", "down", "flip", "het"):
        p = pset[proc]
        q136_bh = np.full(g.NE, np.nan); q136_by = np.full(g.NE, np.nan)
        for s in (0, 1):
            q136_bh[s::2] = bh_vec(p[s::2], 136)
            q136_by[s::2] = by_vec(p[s::2], 136)
        out["families"][proc]["certified_BH136"] = int(np.nansum(q136_bh[J] < ALPHA))
        out["families"][proc]["certified_BY136"] = int(np.nansum(q136_by[J] < ALPHA))
    return out, pset


# ---- R ladder ----
ladder = {}
psets = {}
for R in RLIST:
    if Rmax >= R:
        out, ps = analysis(list(range(0, R)), f"R{R}")
        ladder[R] = out; psets[R] = ps

# robust-everywhere recomputed at largest R (unchanged rule)
fam_min = np.nanmin(Fr_sig, 0)
nullflip = np.nanmean(nF, 0)
pooled_both = (np.abs(pz[0::2]) > 1.96) & (np.abs(pz[1::2]) > 1.96) & (sref[0::2] == sref[1::2])
robust = pooled_both & (Tr_sig[J] >= 0.5) & (fam_min[J] >= 0.25) & \
         (np.where(np.isfinite(FR[J]), FR[J], 0) <= np.maximum(0.1, nullflip[J] + 0.05))
robust_idx = np.where(robust)[0]

# ---- verdict_by_R.csv ----
rows = []
for pi in range(NP):
    x, y, _ = g.SPECS[2 * pi]
    row = dict(x=x, y=y)
    for R in sorted(ladder):
        for proc in ("up", "down", "flip", "het"):
            p = ladder[R]["families"][proc]["p"]
            qb = ladder[R]["families"][proc]["q_bh"]
            qy = ladder[R]["families"][proc]["q_by"]
            row[f"p_{proc}_R{R}"] = float(p[pi]) if np.isfinite(p[pi]) else ""
            row[f"qBH_{proc}_R{R}"] = float(qb[pi]) if np.isfinite(qb[pi]) else ""
            row[f"qBY_{proc}_R{R}"] = float(qy[pi]) if np.isfinite(qy[pi]) else ""
            row[f"certBY_{proc}_R{R}"] = int(np.isfinite(qy[pi]) and qy[pi] < ALPHA)
            row[f"certBH_{proc}_R{R}"] = int(np.isfinite(qb[pi]) and qb[pi] < ALPHA)
    row["robust_everywhere_Rmax"] = int(robust[pi])
    rows.append(row)
fields = list(rows[0].keys())
with open(os.path.join(RES, "verdict_by_R.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)

# ---- summary json ----
summary = dict(available_R=Rmax, expected_R=1200, floors={R: ladder[R]["floor"] for R in ladder},
               families={R: {proc: {k: v for k, v in ladder[R]["families"][proc].items()
                                    if k not in ("p", "q_bh", "q_by")}
                              for proc in ladder[R]["families"]} for R in ladder},
               robust_everywhere_count=int(robust.sum()),
               robust_everywhere=[(g.SPECS[2 * i][0], g.SPECS[2 * i][1]) for i in robust_idx],
               interpretation={})
# does the BY-certified set change with R?
by_sets = {}
for proc in ("up", "down", "flip", "het"):
    by_sets[proc] = {R: set(np.where(ladder[R]["families"][proc]["q_by"] < ALPHA)[0])
                     for R in ladder}
summary["BY_tier_changes"] = {}
for proc in ("up", "down", "flip", "het"):
    Rs = sorted(ladder)
    summary["BY_tier_changes"][proc] = {
        f"{a}->{b}": dict(gained=len(by_sets[proc][b] - by_sets[proc][a]),
                          lost=len(by_sets[proc][a] - by_sets[proc][b]),
                          n_at_{b}=len(by_sets[proc][b]))
        for a, b in zip(Rs[:-1], Rs[1:])}
json.dump(summary, open(os.path.join(RES, "summary_by_R.json"), "w"), indent=1, default=float)

# ---- split halves at largest R ----
split = dict(R=Rmax)
if Rmax >= 20:
    half = Rmax // 2
    a, _ = analysis(list(range(0, half)), "halfA")
    b, _ = analysis(list(range(half, Rmax)), "halfB")
    # recompute empirical p within each half for rank correlation
    pa = np.full(g.NE, np.nan); pb = np.full(g.NE, np.nan)
    for proc, side in (("up", "up"), ("down", "dn"), ("flip", "dn"), ("het", "up")):
        real, null = {"up": (Tr_sig, None), "down": (Tr_sig, None), "flip": (FR, None),
                      "het": (QR, None)}[proc]
    pa = emp_p(Tr_sig, nullT[:half], "up"); pb = emp_p(Tr_sig, nullT[half:], "up")
    rho = float(spearmanr(pa[J], pb[J]).correlation)
    split["up_p_rank_correlation"] = rho
    agree = {}
    for proc in ("up", "down", "flip", "het"):
        sa = a["families"][proc]; sb = b["families"][proc]
        # certified sets within each half; note q vectors aligned to 272 order
        ca = np.where(sa["q_by"] < ALPHA)[0]; cb = np.where(sb["q_by"] < ALPHA)[0]
        both_ = len(set(ca) & set(cb)); one = len(set(ca) ^ set(cb))
        agree[proc] = dict(certified_A=len(ca), certified_B=len(cb),
                           certified_both=both_, certified_one_half=one,
                           jaccard=float(len(set(ca) & set(cb)) / max(1, len(set(ca) | set(cb)))),
                           BH_A=sa["certified_BH"], BH_B=sb["certified_BH"])
    split["family_agreement"] = agree
json.dump(split, open(os.path.join(RES, "split_halves.json"), "w"), indent=1, default=float)

# ---- reproduction comparison at R=400 (panel-vintage) ----
repro = {"available": Rmax >= 400}
if Rmax >= 400:
    import csv as _csv
    comm = {}
    with open(os.path.join(DATA, "edge_table400.csv")) as fh:
        for row in _csv.DictReader(fh):
            comm[(row["x"], row["y"])] = row
    share_diff = []
    p_comm = []; p_ours = []
    for pi in range(NP):
        x, y, _ = g.SPECS[2 * pi]
        r0 = comm.get((x, y))
        if r0 is None:
            continue
        share_diff.append(abs(Tr_sig[J][pi] - float(r0["share_TR"])))
    head = json.load(open(os.path.join(DATA, "headline400.json")))
    ours = {proc: ladder[400]["families"][proc]["certified_BH"]
            for proc in ("up", "down", "flip", "het")}
    repro.update(dict(
        max_abs_share_TR_diff=float(np.nanmax(share_diff)),
        median_abs_share_TR_diff=float(np.nanmedian(share_diff)),
        certified_BH_ours=ours,
        certified_BH_committed={k: head["new_counts"].get("certified_" + {"up": "up_BH272",
                                "down": "dn_BH272", "flip": "flip", "het": "het_Q"}[k]) for k in ours},
        robust_ours=int(summary["robust_everywhere_count"]),
        robust_committed=int(head["new_counts"]["robust"]),
    ))
json.dump(repro, open(os.path.join(RES, "repro400.json"), "w"), indent=1, default=float)
print(json.dumps({k: summary[k] for k in ("available_R", "robust_everywhere_count")}, indent=1))
print("families:", json.dumps({R: {p: (ladder[R]["families"][p]["certified_BH"],
                                          ladder[R]["families"][p]["certified_BY"])
                                    for p in ladder[R]["families"]} for R in ladder}, indent=1))
print("split halves:", json.dumps(split.get("family_agreement", {}), indent=1))
print("repro:", json.dumps(repro, indent=1, default=float))
