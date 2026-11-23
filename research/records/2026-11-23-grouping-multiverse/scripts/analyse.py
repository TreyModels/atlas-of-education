#!/usr/bin/env python3
"""Turn the multiverse pickle into edge tables, tag tables and a text summary."""
import sys, pickle, csv, gzip, numpy as np
from collections import defaultdict

PKL, OUTDIR, SURV = sys.argv[1], sys.argv[2], sys.argv[3]
D = pickle.load(open(PKL, "rb"))
meta, specs, res = D["meta"], D["specs"], D["res"]
R = len(res) - 1
NE = len(specs)
SCH = {"lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter"}

# flatten cells
cells = []   # (grouping idx, family, tag, label, nmembers)
for gi, g in enumerate(meta):
    for l, t, m in g["groups"]:
        cells.append((gi, g["family"], t, l, len(m)))
gidx = np.array([c[0] for c in cells]); fam = np.array([c[1] for c in cells]); tags = np.array([c[2] for c in cells])
fams = sorted(set(fam))
G_of_fam = {f: sorted({c[0] for c in cells if c[1] == f}) for f in fams}

pb, pse, pn, pnc, _ = res[0]["pooled"]
pz = pb / pse
sref = np.sign(pb)
full = res[0]["full"]  # list per cell of (b,se,n,nc)

def sigmat(z):  # cells x NE, nan where not estimable
    out = np.where(np.isfinite(z), ((np.abs(z) > 1.96) & (np.sign(z) == sref)).astype(float), np.nan)
    return out

def both(z):    # FE and TR both sig same sign as pooled TR sign... use each spec's own pooled sign
    s = sigmat(z)
    b = np.full_like(s, np.nan)
    b[:, 0::2] = np.where(np.isnan(s[:, 0::2]) | np.isnan(s[:, 1::2]), np.nan, s[:, 0::2] * s[:, 1::2])
    b[:, 1::2] = b[:, 0::2]
    return b

def shares(S):
    """family-balanced share, plus per-family shares. S: cells x NE"""
    per_g = np.full((len(meta), S.shape[1]), np.nan)
    for gi in range(len(meta)):
        m = gidx == gi
        with np.errstate(all="ignore"):
            per_g[gi] = np.nanmean(S[m], 0) if m.any() else np.nan
    per_f = np.full((len(fams), S.shape[1]), np.nan)
    for k, f in enumerate(fams):
        with np.errstate(all="ignore"):
            per_f[k] = np.nanmean(per_g[G_of_fam[f]], 0)
    with np.errstate(all="ignore"):
        T = np.nanmean(per_f, 0)
    return T, per_f, per_g

import warnings; warnings.filterwarnings("ignore")
Zr = res[0]["z"]
Tr_sig, Fr_sig, _ = shares(sigmat(Zr))
Tr_both, _, _ = shares(both(Zr))
nullT = np.array([shares(sigmat(res[r]["z"]))[0] for r in range(1, R + 1)])
nullF = np.array([shares(sigmat(res[r]["z"]))[1] for r in range(1, R + 1)])
nullB = np.array([shares(both(res[r]["z"]))[0] for r in range(1, R + 1)])

from scipy.stats import norm
def _z(real, null):
    mu = np.nanmean(null, 0); sd = np.nanstd(null, 0, ddof=1)
    return (real - mu) / np.where(sd > 0, sd, np.nan), sd
def pup(real, null):
    """one-sided p that real >= null. Normal approximation to the null (R is small relative to the
    number of tests); falls back to the empirical rank p where the null has no spread."""
    z, sd = _z(real, null)
    emp = (1 + (null >= real - 1e-12).sum(0)) / (R + 1)
    return np.where(np.isfinite(z), np.maximum(norm.sf(z), 1e-12), emp)
def pdn(real, null):
    z, sd = _z(real, null)
    emp = (1 + (null <= real + 1e-12).sum(0)) / (R + 1)
    return np.where(np.isfinite(z), np.maximum(norm.cdf(z), 1e-12), emp)
def bh(p):
    p = np.array(p, float); n = np.isfinite(p).sum(); out = np.full_like(p, np.nan)
    idx = np.where(np.isfinite(p))[0]; o = idx[np.argsort(p[idx])]
    q = p[o] * n / (np.arange(1, n + 1)); q = np.minimum.accumulate(q[::-1])[::-1]
    out[o] = np.minimum(q, 1); return out

p_up = pup(Tr_sig, nullT); p_dn = pdn(Tr_sig, nullT)
p_upB = pup(Tr_both, nullB)
q_up = np.full(NE, np.nan); q_dn = np.full(NE, np.nan); q_upB = np.full(NE, np.nan)
for s in (0, 1):
    q_up[s::2] = bh(p_up[s::2]); q_dn[s::2] = bh(p_dn[s::2]); q_upB[s::2] = bh(p_upB[s::2])

# heterogeneity
def rate(arr):  # groupings x NE -> family balanced share
    with np.errstate(all="ignore"):
        pf = np.array([np.nanmean(arr[G_of_fam[f]], 0) for f in fams])
        return np.nanmean(pf, 0), pf
Qr = np.where(np.isfinite(res[0]["Qp"]), (res[0]["Qp"] < 0.05).astype(float), np.nan)
flr = np.where(np.isfinite(res[0]["Qp"]), res[0]["flip"].astype(float), np.nan)
QR, QRf = rate(Qr); FR, FRf = rate(flr)
nQ = np.array([rate(np.where(np.isfinite(res[r]["Qp"]), (res[r]["Qp"] < 0.05).astype(float), np.nan))[0] for r in range(1, R + 1)])
nF = []; nFf = []
for r in range(1, R + 1):
    a, b_ = rate(np.where(np.isfinite(res[r]["Qp"]), res[r]["flip"].astype(float), np.nan)); nF.append(a); nFf.append(b_)
nF = np.array(nF); nFf = np.array(nFf)
p_Q = pup(QR, nQ); p_F = pup(FR, nF)
q_Q = np.full(NE, np.nan); q_F = np.full(NE, np.nan)
for s in (0, 1):
    q_Q[s::2] = bh(p_Q[s::2]); q_F[s::2] = bh(p_F[s::2])

# tags
tag_names = sorted(set(tags))
rows_tag = []
tag_hits = defaultdict(list)   # (edge spec j) -> list of (tag, stat...)
TagStat = {}
def tagstat(z, mask):
    sz = z[mask] * sref
    with np.errstate(all="ignore"):
        return np.nanmean(sz, 0), np.nanmean(np.where(np.isfinite(z[mask]), (np.abs(z[mask]) > 1.96) & (np.sign(z[mask]) == sref), np.nan), 0), np.isfinite(z[mask]).sum(0)
tag_p_up = {}; tag_p_dn = {}; tag_obs = {}
for t in tag_names:
    m = tags == t
    mu, sh, nn = tagstat(Zr, m)
    nul = np.array([tagstat(res[r]["z"], m)[0] for r in range(1, R + 1)])
    tag_obs[t] = (mu, sh, nn)
    tag_p_up[t] = pup(mu, nul); tag_p_dn[t] = pdn(mu, nul)
# BH over all tag x edge tests, separately per spec and direction
allq_up = {}; allq_dn = {}
for s in (0, 1):
    P = np.array([tag_p_up[t][s::2] for t in tag_names]); Pd = np.array([tag_p_dn[t][s::2] for t in tag_names])
    ok = np.array([[tag_obs[t][2][s::2][k] >= 1 for k in range(NE // 2)] for t in tag_names])
    P = np.where(ok, P, np.nan); Pd = np.where(ok, Pd, np.nan)
    qu = bh(P.ravel()).reshape(P.shape); qd = bh(Pd.ravel()).reshape(Pd.shape)
    for ti, t in enumerate(tag_names):
        allq_up[(t, s)] = qu[ti]; allq_dn[(t, s)] = qd[ti]

# survivors from base matrix
surv = set()
for line in open(SURV):
    a = line.split()
    if len(a) >= 2: surv.add((a[0], a[1]))

def edge_tags(pi, s, kind):
    """Groups where the link is concentrated. 'up': same sign as the whole-sample link, mean z>=2 (>=3 for a single
    group), >=half of the cells significant, beats the matched random cells (BH q<0.05), and the fixed-effects
    version points the same way. 'dn': opposite sign, mean z<=-2, beats the null in that direction (BH q<0.05)."""
    out = []
    for t in tag_names:
        mu, sh, nn = tag_obs[t]
        j = 2 * pi + s
        if nn[j] < 1: continue
        if kind == "up":
            q = allq_up[(t, s)][pi]
            ok = (np.isfinite(q) and q < 0.05 and sh[j] >= 0.5 and mu[j] >= (2 if nn[j] >= 3 else 3)
                  and (s == 0 or mu[2 * pi] >= 1))
        else:
            q = allq_dn[(t, s)][pi]
            ok = np.isfinite(q) and q < 0.05 and mu[j] <= -2 and nn[j] >= 2
        if ok:
            out.append((t, float(mu[j]), float(sh[j]), int(nn[j])))
    return sorted(out, key=lambda r: -abs(r[1]))

NP = NE // 2
table = []
for pi in range(NP):
    x, y, _ = specs[2 * pi]
    jf, jt = 2 * pi, 2 * pi + 1
    pooled_fe = abs(pz[jf]) > 1.96; pooled_tr = abs(pz[jt]) > 1.96
    pooled_both = pooled_fe and pooled_tr and sref[jf] == sref[jt]
    fam_min = np.nanmin(Fr_sig[:, jt]) if np.isfinite(Fr_sig[:, jt]).any() else np.nan
    up = edge_tags(pi, 1, "up"); dn = edge_tags(pi, 1, "dn")
    upfe = edge_tags(pi, 0, "up")
    flipfam = [f for k, f in enumerate(fams) if np.isfinite(FRf[k, jt]) and FRf[k, jt] > 0
               and FRf[k, jt] > np.nanpercentile(nFf[:, k, jt], 95)]
    if pooled_both and Tr_sig[jt] >= 0.5 and fam_min >= 0.25 and (FR[jt] if np.isfinite(FR[jt]) else 0) <= max(0.1, nF[:, jt].mean() + 0.05):
        cls = "a_robust_everywhere"
    elif up or dn:
        cls = "b_group_specific"
    elif q_up[jt] < 0.05 or q_upB[jt] < 0.05:
        cls = "d_beats_random_no_clear_group"
    else:
        cls = "c_no_better_than_random"
    table.append(dict(x=x, y=y, topic=("fertility" if "fertility" in (x, y) else "massification" if (y in SCH) else "other"),
        in_base_survivors=(x, y) in surv,
        pooled_FE_b=pb[jf], pooled_FE_t=pz[jf], pooled_TR_b=pb[jt], pooled_TR_t=pz[jt],
        share_FE=Tr_sig[jf], share_TR=Tr_sig[jt], share_both=Tr_both[jt],
        null_FE=nullT[:, jf].mean(), null_TR=nullT[:, jt].mean(), null_both=nullB[:, jt].mean(),
        q_beats_null_FE=q_up[jf], q_beats_null_TR=q_up[jt], q_beats_null_both=q_upB[jt],
        q_below_null_TR=q_dn[jt],
        fam_min_TR=fam_min, het_Q_rate_TR=QR[jt], null_Q_rate=nQ[:, jt].mean(), q_het=q_Q[jt],
        flip_rate_TR=FR[jt], null_flip_rate=nF[:, jt].mean(), q_flip=q_F[jt], flip_families=";".join(flipfam),
        tags_where_holds_TR=";".join(f"{t}[z={mu:+.1f},sig={sh:.0%},cells={n}]" for t, mu, sh, n in up[:6]),
        tags_opposite_TR=";".join(f"{t}[z={mu:+.1f},cells={n}]" for t, mu, sh, n in dn[:6]),
        tags_where_holds_FE=";".join(f"{t}[z={mu:+.1f}]" for t, mu, sh, n in upfe[:4]),
        cls=cls))

import os
os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, "edge_table.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(table[0])); w.writeheader()
    for r in table: w.writerow({k: (f"{v:.4g}" if isinstance(v, (float, np.floating)) else v) for k, v in r.items()})
with gzip.open(os.path.join(OUTDIR, "cells_real.csv.gz"), "wt", newline="") as f:
    w = csv.writer(f); w.writerow(["grouping", "family", "group", "tag", "n_countries_in_group", "x", "y", "spec", "b", "se", "rows", "countries"])
    for ci, c in enumerate(cells):
        for j in range(NE):
            b, se, n, nc = full[ci][0][j], full[ci][1][j], full[ci][2][j], full[ci][3][j]
            if np.isfinite(b):
                w.writerow([meta[c[0]]["name"], c[1], c[3], c[2], c[4], specs[j][0], specs[j][1], "trend" if specs[j][2] else "FE", f"{b:.5g}", f"{se:.5g}", n, nc])
with open(os.path.join(OUTDIR, "groupings.csv"), "w") as f:
    w = csv.writer(f); w.writerow(["grouping", "family", "group", "tag", "countries"])
    for g in meta:
        for l, t, m in g["groups"]: w.writerow([g["name"], g["family"], l, t, len(m)])

# ---------- summary ----------
L = []
P = L.append
P(f"Total regressions run: {D['total_fits']:,} (real cells + {R} random-partition replicates + whole-sample reference)")
P(f"Groupings: {len(meta)} in {len(fams)} families ({', '.join(fams)}); cells: {len(cells)}; random partition replicates: {R}")
P(f"Whole sample: significant with FE {int((np.abs(pz[0::2])>1.96).sum())}, with trends {int((np.abs(pz[1::2])>1.96).sum())}, both same sign {sum(1 for r in table if abs(r['pooled_FE_t'])>1.96 and abs(r['pooled_TR_t'])>1.96 and np.sign(r['pooled_FE_b'])==np.sign(r['pooled_TR_b']))} (earlier matrix: 127 / 42 / 24)")
P(f"Edges beating the random-partition null (BH q<0.05, one-sided): FE {int((q_up[0::2]<0.05).sum())}, trends {int((q_up[1::2]<0.05).sum())}, both-specs {int((q_upB[1::2]<0.05).sum())} of {NP}")
P(f"Edges BELOW the null (BH q<0.05): trends {int((q_dn[1::2]<0.05).sum())}")
P(f"Edges whose sign-flip rate beats null (q<0.05): {int((q_F[1::2]<0.05).sum())}; heterogeneity-rate beats null: {int((q_Q[1::2]<0.05).sum())}")
cnt = defaultdict(int)
for r in table: cnt[(r["topic"], r["cls"])] += 1
P("\nClass counts by topic:")
for k in sorted(cnt): P(f"  {k[0]:14s} {k[1]:32s} {cnt[k]}")

def show(topic, clsname, lim=40):
    rows = [r for r in table if r["topic"] == topic and r["cls"] == clsname]
    rows.sort(key=lambda r: -(r["share_TR"] if np.isfinite(r["share_TR"]) else 0))
    for r in rows[:lim]:
        P(f"  {r['x']:11s}->{r['y']:11s} pooled t FE {r['pooled_FE_t']:+5.1f} TR {r['pooled_TR_t']:+5.1f} | share sig FE {r['share_FE']:.2f} TR {r['share_TR']:.2f} (null {r['null_FE']:.2f}/{r['null_TR']:.2f}) qNull TR {r['q_beats_null_TR']:.3f} | base:{'Y' if r['in_base_survivors'] else '-'} flipfam:{r['flip_families'] or '-'}")
        if r["tags_where_holds_TR"]: P(f"        holds in: {r['tags_where_holds_TR']}")
        if r["tags_opposite_TR"]: P(f"        opposite sign in: {r['tags_opposite_TR']}")
for topic in ("fertility", "massification", "other"):
    P(f"\n{'='*30} {topic.upper()} {'='*30}")
    for c in ("a_robust_everywhere", "b_group_specific", "d_beats_random_no_clear_group"):
        P(f"\n-- {c}")
        show(topic, c)
    n = sum(1 for r in table if r["topic"] == topic and r["cls"] == "c_no_better_than_random")
    P(f"\n-- c_no_better_than_random: {n} edges (see edge_table.csv)")
P("\n== Sign flips by family (real rate vs null mean), edges with q_flip<0.05 (trends)")
for pi in range(NP):
    jt = 2 * pi + 1
    if q_F[jt] < 0.05:
        P(f"  {specs[jt][0]}->{specs[jt][1]}: " + "; ".join(f"{f} {FRf[k, jt]:.2f} vs {nFf[:, k, jt].mean():.2f}" for k, f in enumerate(fams) if np.isfinite(FRf[k, jt]) and FRf[k, jt] > 0))
P("\n== Base-matrix survivors (24): where they stand here")
for r in table:
    if r["in_base_survivors"]:
        P(f"  {r['x']:11s}->{r['y']:11s} share TR {r['share_TR']:.2f} null {r['null_TR']:.2f} fam_min {r['fam_min_TR']:.2f} flip {r['flip_rate_TR']:.2f} class {r['cls']}")
open(os.path.join(OUTDIR, "summary.txt"), "w").write("\n".join(L))
print("\n".join(L[:12]))
