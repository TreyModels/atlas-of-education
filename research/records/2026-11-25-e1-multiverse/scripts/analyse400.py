#!/usr/bin/env python3
"""Empirical-inference analysis of the grouping multiverse at 400 random draws.

Same real groupings, same estimator, same family-balanced "share significant with the
same sign" yardstick as research/records/2026-11-23-grouping-multiverse/scripts/analyse.py.
What changes: the null is the empirical distribution of 400 random re-partitions instead
of a normal approximation to 74.

Outputs: edge_table400.csv, halves.csv, null_shares_TR.csv.gz, summary400.txt, headline.json.
"""
import sys, os, pickle, csv, gzip, json, warnings
import numpy as np
from collections import defaultdict
from scipy.stats import norm, poisson, spearmanr, binom

warnings.filterwarnings("ignore")

PKL, SURV, OLDTAB, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
OLD_PKL = os.environ.get("GM_OLD", "/root/work/groups/out/final75.pkl")
D = pickle.load(open(PKL, "rb"))
meta, specs, res = D["meta"], D["specs"], D["res"]
IDS = sorted(r for r in res if r != 0)
R = len(IDS)
NE = len(specs); NP = NE // 2
ALPHA = 0.05
FLOOR = 1.0 / (R + 1)
SCH = {"lsc", "sec", "ter", "prm_cmp", "gpi_sec", "gpi_ter"}

# ---------------- flatten cells ----------------
cells = []
for gi, g in enumerate(meta):
    for l, t, m in g["groups"]:
        cells.append((gi, g["family"], t, l, len(m)))
gidx = np.array([c[0] for c in cells]); fam = np.array([c[1] for c in cells])
tags = np.array([c[2] for c in cells])
fams = sorted(set(fam))
G_of_fam = {f: sorted({c[0] for c in cells if c[1] == f}) for f in fams}
tag_names = sorted(set(tags))
tag_cells = np.array([np.where(tags == t)[0] for t in tag_names], dtype=object)

pb, pse, pn, pnc, _ = res[0]["pooled"]
pz = pb / pse
sref = np.sign(pb)
full = res[0]["full"]


def sigmat(z):
    return np.where(np.isfinite(z), ((np.abs(z) > 1.96) & (np.sign(z) == sref)).astype(float), np.nan)


def both(z):
    s = sigmat(z); b = np.full_like(s, np.nan)
    b[:, 0::2] = np.where(np.isnan(s[:, 0::2]) | np.isnan(s[:, 1::2]), np.nan,
                          s[:, 0::2] * s[:, 1::2])
    b[:, 1::2] = b[:, 0::2]
    return b


def shares(S):
    per_g = np.full((len(meta), S.shape[1]), np.nan)
    for gi in range(len(meta)):
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


Zr = res[0]["z"]
Tr_sig, Fr_sig, _ = shares(sigmat(Zr))
Tr_both, _, _ = shares(both(Zr))
Sr = sigmat(Zr)
nullT = np.array([shares(sigmat(res[r]["z"]))[0] for r in IDS], dtype=np.float64)
nullB = np.array([shares(both(res[r]["z"]))[0] for r in IDS], dtype=np.float64)

Qr = np.where(np.isfinite(res[0]["Qp"]), (res[0]["Qp"] < 0.05).astype(float), np.nan)
flr = np.where(np.isfinite(res[0]["Qp"]), res[0]["flip"].astype(float), np.nan)
QR, QRf = rate(Qr); FR, FRf = rate(flr)
nQ = np.array([rate(np.where(np.isfinite(res[r]["Qp"]), (res[r]["Qp"] < 0.05).astype(float), np.nan))[0] for r in IDS])
nF = np.array([rate(np.where(np.isfinite(res[r]["Qp"]), res[r]["flip"].astype(float), np.nan))[0] for r in IDS])


# ---------------- p-values ----------------
def emp_p(real, null, side):
    fin = np.isfinite(null)
    valid = fin.sum(0)
    if side == "up":
        cnt = np.nansum(np.where(fin, null >= real, 0), 0)
    else:
        cnt = np.nansum(np.where(fin, null <= real, 0), 0)
    return (1 + cnt) / (1 + valid)


def emp_p_lib(real, null, side):
    """liberal convention: p = count/R, exactly 0 when no random draw reaches the real value."""
    fin = np.isfinite(null); valid = fin.sum(0)
    if side == "up":
        cnt = np.nansum(np.where(fin, null >= real, 0), 0)
    else:
        cnt = np.nansum(np.where(fin, null <= real, 0), 0)
    with np.errstate(all="ignore"):
        return np.where(valid > 0, cnt / np.maximum(valid, 1), np.nan)


def norm_p(real, null, side):
    mu = np.nanmean(null, 0); sd = np.nanstd(null, 0, ddof=1)
    with np.errstate(all="ignore"):
        z = (real - mu) / np.where(sd > 0, sd, np.nan)
    emp = emp_p(real, null, side)
    if side == "up":
        return np.where(np.isfinite(z), np.maximum(norm.sf(z), 1e-12), emp)
    return np.where(np.isfinite(z), np.maximum(norm.cdf(z), 1e-12), emp)


def bh(p):
    p = np.array(p, float); n = np.isfinite(p).sum(); out = np.full_like(p, np.nan)
    idx = np.where(np.isfinite(p))[0]; o = idx[np.argsort(p[idx])]
    q = p[o] * n / np.arange(1, n + 1); q = np.minimum.accumulate(q[::-1])[::-1]
    out[o] = np.minimum(q, 1); return out


def bh_parity(p_all):
    q = np.full(NE, np.nan)
    for s in (0, 1):
        q[s::2] = bh(p_all[s::2])
    return q


J = np.arange(1, NE, 2)
n272, n136 = NP, NP // 2
bh_min_p = {"BH272": ALPHA / n272, "BH136": ALPHA / n136}
need_draws = {"BH272": int(np.ceil(n272 / ALPHA)), "BH136": int(np.ceil(n136 / ALPHA))}

# --- reproduce the old 74-draw normal-approximation analysis from the same draws ---
idx74 = [i for i, r in enumerate(IDS) if r <= 73 or r == 75]  # the earlier run's replicate set
nullT74 = nullT[idx74]
p_up74 = norm_p(Tr_sig, nullT74, "up"); p_dn74 = norm_p(Tr_sig, nullT74, "dn")
p_upB74 = norm_p(Tr_both, nullT74, "up"); p_F74 = norm_p(FR, nF[idx74], "up"); p_Q74 = norm_p(QR, nQ[idx74], "up")
q_up74 = bh_parity(p_up74); q_dn74 = bh_parity(p_dn74); q_upB74 = bh_parity(p_upB74)
q_F74 = bh_parity(p_F74); q_Q74 = bh_parity(p_Q74)

# --- 400-draw empirical inference ---
p_up = emp_p(Tr_sig, nullT, "up"); p_dn = emp_p(Tr_sig, nullT, "dn")
p_upB = emp_p(Tr_both, nullB, "up")
p_Q = emp_p(QR, nQ, "up"); p_F = emp_p(FR, nF, "up")
q_up272 = bh(p_up[J]); q_dn272 = bh(p_dn[J]); q_upB272 = bh(p_upB[J])
q_F272 = bh(p_F[J]); q_Q272 = bh(p_Q[J])
q_up136 = bh_parity(p_up); q_dn136 = bh_parity(p_dn); q_upB136 = bh_parity(p_upB); q_F136 = bh_parity(p_F)
q_Q136 = bh_parity(p_Q)

# same 400 draws but normal approximation (isolates approximation vs draw count)
p_up_n400 = norm_p(Tr_sig, nullT, "up"); p_dn_n400 = norm_p(Tr_sig, nullT, "dn")
p_F_n400 = norm_p(FR, nF, "up"); p_upB_n400 = norm_p(Tr_both, nullB, "up")
q_up_n400_272 = bh(p_up_n400[J]); q_up_n400_136 = bh_parity(p_up_n400)
q_upB_n400_272 = bh(p_upB_n400[J])
q_dn_n400_272 = bh(p_dn_n400[J]); q_F_n400_272 = bh(p_F_n400[J])

# --- TIER 2 main inference: smoothed null fitted to the 400 random draws ---
from scipy.stats import t as tdist
p_t400 = np.full(NE, np.nan); t_df = np.full(NE, np.nan); t_scale = np.full(NE, np.nan)
for jt in J:
    x = nullT[:, jt]; x = x[np.isfinite(x)]
    if len(x) > 30 and np.nanstd(x) > 0:
        try:
            df_, loc_, sc_ = tdist.fit(x)
            if np.isfinite(df_) and np.isfinite(sc_) and sc_ > 0:
                t_df[jt] = df_; t_scale[jt] = sc_
                p_t400[jt] = tdist.sf((Tr_sig[jt] - loc_) / sc_, df_)
        except Exception:
            pass
q_t400_272 = bh(p_t400[J]); q_t400_136 = bh_parity(p_t400)
q_norm400_272 = q_up_n400_272; q_norm400_136 = q_up_n400_136
sig_norm400_272 = q_norm400_272 < 0.05; sig_t400_272 = q_t400_272 < 0.05
sig_norm400_136 = q_norm400_136[J] < 0.05; sig_t400_136 = q_t400_136[J] < 0.05
tier2 = dict(normal_272=int(np.nansum(sig_norm400_272)), t_272=int(np.nansum(sig_t400_272)),
             normal_136=int(np.nansum(sig_norm400_136)), t_136=int(np.nansum(sig_t400_136)),
             agree_272=int(np.nansum(sig_norm400_272 & sig_t400_272)),
             disagree_272=int(np.nansum(sig_norm400_272 ^ sig_t400_272)),
             median_df=float(np.nanmedian(t_df[J])), median_scale=float(np.nanmedian(t_scale[J])))
# does the normal fit describe the 400-draw null well? compare its 95% interval with the empirical one
_muJ = np.nanmean(nullT[:, J], 0); _sdJ = np.nanstd(nullT[:, J], 0, ddof=1)
_loJ = np.nanpercentile(nullT[:, J], 2.5, axis=0); _hiJ = np.nanpercentile(nullT[:, J], 97.5, axis=0)
_gap = np.abs((_muJ - 1.96 * _sdJ) - _loJ); _gap2 = np.abs((_muJ + 1.96 * _sdJ) - _hiJ)
tier2["median_normal_vs_empirical_95_gap"] = float(np.nanmedian(np.maximum(_gap, _gap2)))

# --- sensitivity: liberal p convention (count/R, zero allowed) ---
p_up_lib = emp_p_lib(Tr_sig, nullT, "up"); p_dn_lib = emp_p_lib(Tr_sig, nullT, "dn")
p_F_lib = emp_p_lib(FR, nF, "up"); p_upB_lib = emp_p_lib(Tr_both, nullB, "up")
q_up_lib272 = bh(p_up_lib[J]); q_dn_lib272 = bh(p_dn_lib[J])
q_F_lib272 = bh(p_F_lib[J]); q_upB_lib272 = bh(p_upB_lib[J])
cert_lib_up = int(np.nansum(q_up_lib272 < 0.05)); cert_lib_dn = int(np.nansum(q_dn_lib272 < 0.05))
cert_lib_F = int(np.nansum(q_F_lib272 < 0.05)); cert_lib_upB = int(np.nansum(q_upB_lib272 < 0.05))

# --- nested-draw curve: what a bigger run would do, using the same nested draws ---
curve = []
for k in (50, 100, 200, 300, 400):
    if k > R:
        continue
    idx = list(range(k))
    pk = emp_p(Tr_sig, nullT[idx], "up"); pkd = emp_p(Tr_sig, nullT[idx], "dn")
    pkf = emp_p(FR, nF[idx], "up"); pkb = emp_p(Tr_both, nullB[idx], "up")
    pk_lib = emp_p_lib(Tr_sig, nullT[idx], "up")
    mm = np.isfinite(pk[J]) & np.isfinite(p_up[J])
    curve.append(dict(draws=k, floor=1 / (k + 1),
                      ceiling_up=int(np.nansum(pk[J] <= 1 / (k + 1) + 1e-15)),
                      ceiling_dn=int(np.nansum(pkd[J] <= 1 / (k + 1) + 1e-15)),
                      ceiling_flip=int(np.nansum(pkf[J] <= 1 / (k + 1) + 1e-15)),
                      certified_up_strict=int(np.nansum(bh(pk[J]) < 0.05)),
                      certified_up_liberal=int(np.nansum(bh(pk_lib[J]) < 0.05)),
                      rank_corr_with_400=float(spearmanr(pk[J][mm], p_up[J][mm]).correlation)))

# --- nominal (uncorrected) evidence and its family-level test ---
n_nom_up = int(np.nansum(p_up[J] <= 0.05)); n_nom_dn = int(np.nansum(p_dn[J] <= 0.05))
n_nom_F = int(np.nansum(p_F[J] <= 0.05))
binom_p_up = float(binom.sf(n_nom_up - 1, NP, 0.05)); binom_p_F = float(binom.sf(n_nom_F - 1, NP, 0.05))
n_norm400_05 = int(np.nansum(p_up_n400[J] <= 0.05))
ci = dict(null_share_bin_se_median=float(np.nanmedian(np.abs(p_up[J] * 0 + np.array([np.nanmean(nullT[:, j]) for j in J]) * (1 - np.array([np.nanmean(nullT[:, j]) for j in J])) / R) ** 0.5)) if False else None,
          ceiling_upper95=3.0 / R,
          worst_bin_se=float(np.sqrt(0.25 / R)))

# ---------------- tag-level ("where it holds") ----------------
# FE real tag means (only used for the old "FE points the same way" check)
tag_FE = ([], [], [])
obs_fe = np.empty((len(tag_names), NP)); sh_fe = np.empty((len(tag_names), NP)); nn_fe = np.empty((len(tag_names), NP))
for ti in range(len(tag_names)):
    z = Zr[tag_cells[ti]][:, 0::2]
    with np.errstate(all="ignore"):
        obs_fe[ti] = np.nanmean((z * sref[0::2]), 0)
        sh_fe[ti] = np.nanmean(np.where(np.isfinite(z), (np.abs(z) > 1.96) & (np.sign(z) == sref[0::2]), np.nan), 0)
        nn_fe[ti] = np.isfinite(z).sum(0)
tag_FE = (obs_fe, sh_fe, nn_fe)

# TR tag means: observed + the 400 random-draw tag means; smoothed-null (tier 2) p-values
obs = np.empty((len(tag_names), NP)); sh = np.empty((len(tag_names), NP)); nn = np.empty((len(tag_names), NP))
for ti in range(len(tag_names)):
    z = Zr[tag_cells[ti]][:, 1::2]
    with np.errstate(all="ignore"):
        obs[ti] = np.nanmean((z * sref[1::2]), 0)
        sh[ti] = np.nanmean(np.where(np.isfinite(z), (np.abs(z) > 1.96) & (np.sign(z) == sref[1::2]), np.nan), 0)
        nn[ti] = np.isfinite(z).sum(0)
nullmu = np.empty((len(tag_names), R, NP))
for r_i, r in enumerate(IDS):
    zz = res[r]["z"]
    for ti in range(len(tag_names)):
        with np.errstate(all="ignore"):
            nullmu[ti, r_i] = np.nanmean(zz[tag_cells[ti]][:, 1::2] * sref[1::2], 0)
mu_n = np.nanmean(nullmu, 1); sd_n = np.nanstd(nullmu, 1, ddof=1)
with np.errstate(all="ignore"):
    zsc = (obs - mu_n) / np.where(sd_n > 0, sd_n, np.nan)
    pu = np.where(np.isfinite(zsc), np.maximum(norm.sf(zsc), 1e-12), np.nan)
    pd = np.where(np.isfinite(zsc), np.maximum(norm.cdf(zsc), 1e-12), np.nan)
tag_obs = (obs, sh, nn)
tag_q = (bh(pu.ravel()).reshape(pu.shape), bh(pd.ravel()).reshape(pd.shape))
tag_ceil = (pu <= FLOOR + 1e-15, pd <= FLOOR + 1e-15)   # tier 3 descriptive
del nullmu

# ---------------- old committed table ----------------
old = {}
with open(OLDTAB) as f:
    for row in csv.DictReader(f):
        old[(row["x"], row["y"])] = row
surv = set()
for line in open(SURV):
    w = line.split()
    if len(w) >= 2:
        surv.add((w[0], w[1]))

# ---------------- per-link table ----------------
table = []
for pi in range(NP):
    x, y, _ = specs[2 * pi]
    jf, jt = 2 * pi, 2 * pi + 1
    oldrow = old.get((x, y), {})
    fam_min = np.nanmin(Fr_sig[:, jt]) if np.isfinite(Fr_sig[:, jt]).any() else np.nan
    nullflip = float(np.nanmean(nF[:, jt]))
    pooled_both = abs(pz[jf]) > 1.96 and abs(pz[jt]) > 1.96 and sref[jf] == sref[jt]
    robust = bool(pooled_both and Tr_sig[jt] >= 0.5 and fam_min >= 0.25
                  and (FR[jt] if np.isfinite(FR[jt]) else 0) <= max(0.1, nullflip + 0.05))
    ge = int(np.nansum(np.where(np.isfinite(nullT[:, jt]), nullT[:, jt] >= Tr_sig[jt], 0)))
    le = int(np.nansum(np.where(np.isfinite(nullT[:, jt]), nullT[:, jt] <= Tr_sig[jt], 0)))
    geF = int(np.nansum(np.where(np.isfinite(nF[:, jt]), nF[:, jt] <= FR[jt], 0)))
    ceil_up = bool(p_up[jt] <= FLOOR + 1e-15); ceil_dn = bool(p_dn[jt] <= FLOOR + 1e-15)
    ceil_upB = bool(p_upB[jt] <= FLOOR + 1e-15); ceil_F = bool(p_F[jt] <= FLOOR + 1e-15)
    no_better = bool(p_up[jt] > 0.05)
    # "where it holds": old non-p criteria + tag mean beating its 400-draw smoothed null (BH 5%)
    up_hits, dn_hits = [], []
    obsT, shT, nnT = tag_obs
    quT, qdT = tag_q
    for ti, t in enumerate(tag_names):
        if nnT[ti, pi] < 1:
            continue
        mu = obsT[ti, pi]
        fe_ok = obs_fe[ti, pi] >= 1  # old rule: FE version points the same way
        if np.isfinite(quT[ti, pi]) and quT[ti, pi] < 0.05 and shT[ti, pi] >= 0.5 \
                and mu >= (2 if nnT[ti, pi] >= 3 else 3) and fe_ok:
            up_hits.append((t, mu))
        elif np.isfinite(qdT[ti, pi]) and qdT[ti, pi] < 0.05 and mu <= -2 and nnT[ti, pi] >= 2:
            dn_hits.append((t, mu))
    if robust:
        verdict = "robust everywhere"
    elif up_hits or dn_hits:
        verdict = "group-specific"
    elif (np.isfinite(q_up_n400_272[pi]) and q_up_n400_272[pi] < 0.05) or \
            (np.isfinite(q_upB_n400_272[pi]) and q_upB_n400_272[pi] < 0.05):
        verdict = "beats random, no clear group"
    elif no_better:
        verdict = "no better than random"
    else:
        verdict = "no better than random"
    table.append(dict(
        x=x, y=y, topic=("fertility" if "fertility" in (x, y) else "massification" if y in SCH else "other"),
        in_base_survivors=(x, y) in surv,
        pooled_FE_t=pz[jf], pooled_TR_t=pz[jt],
        share_TR=Tr_sig[jt], share_FE=Tr_sig[jf], share_both=Tr_both[jt],
        null_TR_mean=float(np.nanmean(nullT[:, jt])), null_TR_p95=float(np.nanpercentile(nullT[:, jt], 95)),
        null_TR_max=float(np.nanmax(nullT[:, jt])), n_draws_ge_real=ge, n_draws_le_real=le,
        null_TR_bin_se=float(np.sqrt(max(np.nanmean(nullT[:, jt]) * (1 - np.nanmean(nullT[:, jt])), 0) / R)),
        emp_p_up_TR=p_up[jt], emp_p_dn_TR=p_dn[jt], emp_p_up_both=p_upB[jt],
        q_up_BH272=q_up272[pi], q_dn_BH272=q_dn272[pi], q_upB_BH272=q_upB272[pi],
        q_up_BH136=q_up136[jt], q_dn_BH136=q_dn136[jt],
        p_up_normal400=p_up_n400[jt], q_up_normal400_BH272=q_up_n400_272[pi],
        q_up_normal400_BH136=q_up_n400_136[jt], q_upB_normal400_BH272=q_upB_n400_272[pi],
        q_dn_normal400_BH272=q_dn_n400_272[pi], q_flip_normal400_BH272=q_F_n400_272[pi],
        beats_random_tier2=bool((np.isfinite(q_up_n400_272[pi]) and q_up_n400_272[pi] < 0.05) or
                                (np.isfinite(q_upB_n400_272[pi]) and q_upB_n400_272[pi] < 0.05)),
        worse_random_tier2=bool(np.isfinite(q_dn_n400_272[pi]) and q_dn_n400_272[pi] < 0.05),
        flips_more_tier2=bool(np.isfinite(q_F_n400_272[pi]) and q_F_n400_272[pi] < 0.05),
        tier2_t_version=bool(np.isfinite(q_t400_272[pi]) and q_t400_272[pi] < 0.05),
        old_q_up_TR=float(oldrow.get("q_beats_null_TR") or "nan"),
        old_q_dn_TR=float(oldrow.get("q_below_null_TR") or "nan"),
        old_q_flip=float(oldrow.get("q_flip") or "nan"),
        old_class=oldrow.get("cls", ""),
        fam_min_TR=fam_min, flip_rate_TR=FR[jt], null_flip_mean=nullflip, n_draws_flip_le_real=geF,
        emp_p_flip_le=p_F[jt], het_Q_rate_TR=QR[jt], null_Q_mean=float(np.nanmean(nQ[:, jt])),
        emp_p_Q_up=p_Q[jt], q_Q_BH136=q_Q136[jt],
        robust_everywhere=robust, ceil_up=ceil_up, ceil_dn=ceil_dn, ceil_up_both=ceil_upB,
        ceil_flip=ceil_F, no_better_up=no_better,
        tags_where_holds=";".join(f"{t}[z={mu:+.1f}]" for t, mu in (up_hits or dn_hits)[:8]),
        n_tags_ceiling_TR=int(np.nansum(tag_ceil[0][:, pi] & (nnT[:, pi] >= 1))),
        tags_opposite=";".join(f"{t}[z={mu:+.1f}]" for t, mu in dn_hits[:4]),
        verdict_400=verdict))

# ---------------- headline counts ----------------
def has(r, k, thr=0.05):
    v = r[k]; return np.isfinite(v) and v < thr


old_beats = [r for r in table if has(r, "old_q_up_TR")]
old_worse = [r for r in table if has(r, "old_q_dn_TR")]
old_flip = [r for r in table if has(r, "old_q_flip")]
old_robust = [r for r in table if r["old_class"] == "a_robust_everywhere"]
new_robust = [r for r in table if r["robust_everywhere"]]
ceil_up = [r for r in table if r["ceil_up"]]; ceil_dn = [r for r in table if r["ceil_dn"]]
ceil_flip = [r for r in table if r["ceil_flip"]]
new_no_better = [r for r in table if r["no_better_up"]]
tier2_beats = [r for r in table if r["beats_random_tier2"]]
tier2_worse = [r for r in table if r["worse_random_tier2"]]
tier2_flips = [r for r in table if r["flips_more_tier2"]]
tier2_t_diff = [r for r in table if r["beats_random_tier2"] != r["tier2_t_version"]]
class_new = defaultdict(int)
for r in table: class_new[r["verdict_400"]] += 1
moved = [r for r in old_beats if not r["ceil_up"]]
moved_hard = [r for r in old_beats if not r["ceil_up"] and r["no_better_up"]]

# TIER 2 movement: old 43 vs smoothed null refitted on 400 draws
old43_mask = np.array([has(r, "old_q_up_TR") for r in table])
old43_idx = np.where(old43_mask)[0]
t2_survive = [i for i in old43_idx if sig_norm400_272[i]]
t2_died = [i for i in old43_idx if not sig_norm400_272[i]]
t2_new = [i for i in range(NP) if (not old43_mask[i]) and sig_norm400_272[i]]
t2_survive_t = [i for i in old43_idx if sig_t400_272[i]]
t2_died_t = [i for i in old43_idx if not sig_t400_272[i]]
t2_new_t = [i for i in range(NP) if (not old43_mask[i]) and sig_t400_272[i]]
old74_norm_sig = np.array([has(r, "old_q_up_TR") for r in table])
movement = dict(normal=dict(survive=len(t2_survive), died=len(t2_died), new=len(t2_new),
                            survive_names=[(table[i]["x"], table[i]["y"]) for i in t2_survive],
                            died_names=[(table[i]["x"], table[i]["y"]) for i in t2_died],
                            new_names=[(table[i]["x"], table[i]["y"]) for i in t2_new]),
                t=dict(survive=len(t2_survive_t), died=len(t2_died_t), new=len(t2_new_t),
                       died_names=[(table[i]["x"], table[i]["y"]) for i in t2_died_t],
                       new_names=[(table[i]["x"], table[i]["y"]) for i in t2_new_t]))

exp_ceiling = NP * FLOOR
pois_up = float(poisson.sf(len(ceil_up) - 1, exp_ceiling)) if ceil_up else 1.0
pois_flip = float(poisson.sf(len(ceil_flip) - 1, exp_ceiling)) if ceil_flip else 1.0
pois_dn = float(poisson.sf(len(ceil_dn) - 1, exp_ceiling)) if ceil_dn else 1.0

cert_up272 = int(np.nansum(q_up272 < 0.05)); cert_up136 = int(np.nansum(q_up136[J] < 0.05))
cert_dn272 = int(np.nansum(q_dn272 < 0.05)); cert_upB272 = int(np.nansum(q_upB272 < 0.05))
cert_F = int(np.nansum(q_F272 < 0.05)); cert_Q = int(np.nansum(q_Q272 < 0.05))
n_floor_up = int(np.nansum(p_up[J] <= FLOOR + 1e-15))
n_floor_dn = int(np.nansum(p_dn[J] <= FLOOR + 1e-15))
n_floor_F = int(np.nansum(p_F[J] <= FLOOR + 1e-15))
n_floor_Q = int(np.nansum(p_Q[J] <= FLOOR + 1e-15))
_sup = np.sort(p_up[J][np.isfinite(p_up[J])])
_pdn = np.sort(p_dn[J][np.isfinite(p_dn[J])])
kstar_up = int(max([k for k in range(1, len(_sup) + 1) if _sup[k - 1] <= k * ALPHA / n272], default=0))
kstar_dn = int(max([k for k in range(1, len(_pdn) + 1) if _pdn[k - 1] <= k * ALPHA / n272], default=0))
kstar_up_thr = kstar_up * ALPHA / n272 if kstar_up else np.nan
p_at_kstar = float(_sup[kstar_up - 1]) if kstar_up else np.nan
# step-up bar as a function of how many links are truly at the ceiling: R+1 >= n/(alpha*j)
draws_cluster = {j: int(np.ceil(n272 / (ALPHA * j))) for j in (1, 5, 10, 14, 20, 30, 35)}
# strict-tier movement against the old beats-random set
strict_survive = [i for i in old43_idx if np.isfinite(q_up272[i]) and q_up272[i] < 0.05]
strict_lost = [i for i in old43_idx if i not in strict_survive]
strict_new = [i for i in range(NP) if (not old43_mask[i]) and np.isfinite(q_up272[i]) and q_up272[i] < 0.05]
try:
    from statsmodels.stats.multitest import multipletests as _mt
    _sm_up = int(_mt(p_up[J], alpha=0.05, method="fdr_bh")[0].sum())
    _sm_dn = int(_mt(p_dn[J], alpha=0.05, method="fdr_bh")[0].sum())
    _sm_F = int(_mt(p_F[J], alpha=0.05, method="fdr_bh")[0].sum())
    statsmodels_check = dict(up=_sm_up, dn=_sm_dn, flip=_sm_F, matches=bool(_sm_up == cert_up272 and _sm_dn == cert_dn272 and _sm_F == cert_F))
except Exception as _e:
    statsmodels_check = dict(error=repr(_e))
cert_normal400 = int(np.nansum(q_up_n400_272 < 0.05))

# ---------------- halves stability ----------------
idxA = list(range(0, R // 2)); idxB = list(range(R // 2, R))
nullA, nullB_ = nullT[idxA], nullT[idxB]
pA = emp_p(Tr_sig, nullA, "up"); pB = emp_p(Tr_sig, nullB_, "up")
fA = emp_p(FR, nF[idxA], "up"); fB = emp_p(FR, nF[idxB], "up")
hfloor = 1.0 / (R // 2 + 1)
ceilA = pA[J] <= hfloor + 1e-15; ceilB = pB[J] <= hfloor + 1e-15
noA = pA[J] > 0.05; noB = pB[J] > 0.05
ceilAf = fA[J] <= hfloor + 1e-15; ceilBf = fB[J] <= hfloor + 1e-15
bothC = int((ceilA & ceilB).sum()); oneC = int((ceilA ^ ceilB).sum()); neitherC = int((~ceilA & ~ceilB).sum())
bothF = int((ceilAf & ceilBf).sum()); oneF = int((ceilAf ^ ceilBf).sum())
bothNo = int((noA & noB).sum()); disagreeNo = int((noA ^ noB).sum())
pA_norm = norm_p(Tr_sig, nullA, "up"); pB_norm = norm_p(Tr_sig, nullB_, "up")
qA_norm = bh(pA_norm[J]); qB_norm = bh(pB_norm[J])
sigA_norm = qA_norm < 0.05; sigB_norm = qB_norm < 0.05
sig_full_norm = sig_norm400_272
half_norm = dict(A=int(np.nansum(sigA_norm)), B=int(np.nansum(sigB_norm)),
                 both=int(np.nansum(sigA_norm & sigB_norm)),
                 one=int(np.nansum(sigA_norm ^ sigB_norm)),
                 neither=int(np.nansum(~sigA_norm & ~sigB_norm)),
                 jaccard=float((sigA_norm & sigB_norm).sum() / max((sigA_norm | sigB_norm).sum(), 1)),
                 full_agreeA=int(np.nansum(sigA_norm == sig_full_norm)),
                 full_agreeB=int(np.nansum(sigB_norm == sig_full_norm)))

m = np.isfinite(pA[J]) & np.isfinite(pB[J])
rho = float(spearmanr(pA[J][m], pB[J][m]).correlation) if m.sum() > 3 else np.nan
shareA = np.array([np.nanmean(nullA[:, j]) for j in J]); shareB = np.array([np.nanmean(nullB_[:, j]) for j in J])
m2 = np.isfinite(shareA) & np.isfinite(shareB)
rho_share = float(np.corrcoef(shareA[m2], shareB[m2])[0, 1]) if m2.sum() > 3 else np.nan
maxdiff_share = float(np.nanmax(np.abs(shareA - shareB)))

null74mean = np.array([np.nanmean(nullT74[:, j]) for j in J])
null400mean = np.array([np.nanmean(nullT[:, j]) for j in J])
m3 = np.isfinite(null74mean) & np.isfinite(null400mean)
maxdiff74 = float(np.nanmax(np.abs(null74mean[m3] - null400mean[m3])))

# old-74 reproduction (committed q values are printed to 4 significant digits, so compare
# significance decisions and relative size, not exact equality)
old43 = len(old_beats); q74_43 = int(np.nansum(q_up74[J] < 0.05))
rep_reldiff = [abs(q_up74[2 * pi + 1] - r["old_q_up_TR"]) / max(abs(r["old_q_up_TR"]), 1e-30)
               for pi, r in enumerate(table) if np.isfinite(r["old_q_up_TR"]) and r["old_q_up_TR"] > 0]
rep_relmax = float(np.nanmax(rep_reldiff)) if rep_reldiff else np.nan
flip_signif_old = int(np.nansum(q_F74[J] < 0.05)); flip_signif_new74 = int(np.nansum(q_F74[J] < 0.05))

# ---------------- determinism cross-check against the earlier 74-replicate run ----------------
det = {}
try:
    if OLD_PKL and os.path.exists(OLD_PKL):
        Do = pickle.load(open(OLD_PKL, "rb"))
        common = [r for r in IDS if r in Do["res"]]
        dz = [float(np.nanmax(np.abs(Do["res"][r]["z"] - res[r]["z"]))) for r in common]
        dq = [float(np.nanmax(np.abs(Do["res"][r]["Qp"] - res[r]["Qp"]))) for r in common]
        df = int(sum(int((Do["res"][r]["flip"] != res[r]["flip"]).sum()) for r in common))
        det = dict(common_replicates=len(common), max_abs_diff_z=max(dz), max_abs_diff_Qp=max(dq),
                   flip_mismatches=df, real_pass_z_identical=bool(np.array_equal(Do["res"][0]["z"], res[0]["z"], equal_nan=True)),
                   real_pass_full_identical=bool(all(np.array_equal(np.asarray(Do["res"][0]["full"][c][i]),
                                                                   np.asarray(res[0]["full"][c][i]), equal_nan=True)
                                                     for c in range(len(cells)) for i in range(4))))
except Exception as e:
    det = dict(error=repr(e))

# ---------------- write outputs ----------------
os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, "edge_table400.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(table[0].keys())); w.writeheader()
    for r in table:
        w.writerow({k: (f"{v:.6g}" if isinstance(v, (float, np.floating)) and np.isfinite(v) else
                        ("" if isinstance(v, (float, np.floating)) else v)) for k, v in r.items()})
with gzip.open(os.path.join(OUTDIR, "null_shares_TR.csv.gz"), "wt", newline="") as f:
    w = csv.writer(f)
    w.writerow(["draw"] + [f"{r['x']}->{r['y']}" for r in table])
    for i, rr in enumerate(IDS):
        w.writerow([rr] + [f"{nullT[i, j]:.4g}" for j in J])
with open(os.path.join(OUTDIR, "halves.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["x", "y", "p_up_halfA_200draws", "p_up_halfB_200draws", "p_up_full400",
                "ceiling_halfA", "ceiling_halfB", "ceiling_full400", "no_better_halfA", "no_better_halfB"])
    for pi, r in enumerate(table):
        w.writerow([r["x"], r["y"], f"{pA[J][pi]:.5g}", f"{pB[J][pi]:.5g}", f"{p_up[J][pi]:.5g}",
                    bool(ceilA[pi]), bool(ceilB[pi]), bool(r["ceil_up"]), bool(noA[pi]), bool(noB[pi])])

share_stats = dict(
    median_share_TR=float(np.nanmedian([r["share_TR"] for r in table])),
    median_null_TR=float(np.nanmedian([r["null_TR_mean"] for r in table])),
    mean_share_TR=float(np.nanmean([r["share_TR"] for r in table])),
    mean_null_TR=float(np.nanmean([r["null_TR_mean"] for r in table])),
    frac_real_above_null_mean=float(np.mean([r["share_TR"] > r["null_TR_mean"] for r in table])),
    binom_se_at_50=float(np.sqrt(0.25 / R)), binom_halfwidth95_at_50=float(1.96 * np.sqrt(0.25 / R)),
    binom_se_at_90=float(np.sqrt(0.09 / R)), ceiling_upper95_rule_of_three=float(3.0 / R),
    median_bin_se=float(np.nanmedian([r["null_TR_bin_se"] for r in table])))
head = dict(R=R, floor=FLOOR, n_links=NP, alpha=ALPHA, bh_min_p=bh_min_p, share_summary=share_stats,
            draws_needed_for_BH=need_draws,
            old_counts=dict(beats=len(old_beats), worse=len(old_worse), flip=len(old_flip),
                            robust=len(old_robust), survivors=len(surv)),
            new_counts=dict(certified_up_BH272=cert_up272, certified_up_BH136=cert_up136,
                            certified_dn_BH272=cert_dn272, certified_upB_BH272=cert_upB272,
                            certified_flip=cert_F, certified_het_Q=cert_Q,
                            normal_approx_same_400draws_certified_up=cert_normal400,
                            ceiling_up=len(ceil_up), ceiling_dn=len(ceil_dn),
                            ceiling_flip=len(ceil_flip), no_better_up=len(new_no_better),
                            robust=len(new_robust)),
            expected_ceiling_by_chance=exp_ceiling, poisson_p_up=pois_up,
            poisson_p_flip=pois_flip, poisson_p_dn=pois_dn,
            old_beats_moved_off_ceiling=len(moved), old_beats_to_no_better=len(moved_hard),
            class_new=dict(class_new),
            tier2_retest=dict(beats=len(tier2_beats), worse=len(tier2_worse), flips=len(tier2_flips),
                              t_version_disagrees=len(tier2_t_diff),
                              old_worse_still=int(sum(1 for r in old_worse if r["worse_random_tier2"])),
                              old_flip_still=int(sum(1 for r in old_flip if r["flips_more_tier2"]))),
            halves=dict(both_ceiling=bothC, one_ceiling=oneC, neither=neitherC,
                        both_flip_ceiling=bothF, one_flip_ceiling=oneF,
                        both_no_better=bothNo, disagree_no_better=disagreeNo,
                        normal_fit_halves=half_norm,
                        spearman_p=rho, pearson_null_share=rho_share,
                        max_abs_diff_null_share=maxdiff_share, half_floor=hfloor),
            null_mean_74_vs_400_max_abs_diff=maxdiff74,
            statsmodels_bh_crosscheck=statsmodels_check,
            empirical_floor_check=dict(min_p_up=float(np.nanmin(p_up[J])), min_p_dn=float(np.nanmin(p_dn[J])),
                                       n_at_floor_up=n_floor_up, n_at_floor_dn=n_floor_dn, n_at_floor_flip=n_floor_F,
                                       certified_up=cert_up272, k_star_up=kstar_up, p_at_k_star=p_at_kstar,
                                       k_star_threshold=kstar_up_thr, first_bh_step=bh_min_p["BH272"],
                                       draws_for_lone_link=need_draws["BH272"],
                                       draws_for_cluster={str(k): v for k, v in draws_cluster.items()},
                                       note="BH step-up rejects the floor cluster; a lone link would need 5,440 draws"),
            old74_reproduction=dict(old_significant=old43, reproduced_significant=q74_43,
                                    max_rel_q_diff=rep_relmax),
            tier2_main=tier2, movement_tier2=movement, n_tags=len(tag_names), n_cells=len(cells),
            strict_movement=dict(survive=len(strict_survive), lost=len(strict_lost), new=len(strict_new),
                                 lost_names=[(table[i]["x"], table[i]["y"]) for i in strict_lost],
                                 new_names=[(table[i]["x"], table[i]["y"]) for i in strict_new]),
            determinism_vs_old_run=det,
            runtime_seconds=D.get("runtime"), total_fits=D.get("total_fits"), nproc=D.get("nproc"))
json.dump(head, open(os.path.join(OUTDIR, "headline.json"), "w"), indent=1, default=float)

# ---------------- summary text ----------------
L = []; P = L.append
P("GROUPING MULTIVERSE, 400 RANDOM DRAWS - EMPIRICAL INFERENCE")
P(f"draws {R}; empirical p floor 1/{R+1} = {FLOOR:.5f}; links {NP}; a LONE link needs p <= {bh_min_p['BH272']:.3e} (272 tests) / {bh_min_p['BH136']:.3e} (136) to be certified, i.e. {need_draws['BH272']} / {need_draws['BH136']} draws; "
  f"but BH is a step-up rule, so the {n_floor_up} links tied at the floor are certified at 400 draws")
P(f"strict empirical test, BH<0.05: up {cert_up272} certified (BH272; {cert_up136} under BH136), down {cert_dn272}, both-spec {cert_upB272}, flip {cert_F}, heterogeneity {cert_Q}; {n_floor_up} up are at the resolution ceiling and BH rejects them through its step-up line (k*={kstar_up}, p_(k*)={p_at_kstar:.5f} <= k*alpha/n={kstar_up_thr:.5f})")
P(f"same 400 draws, normal approximation: {cert_normal400} up links certified at BH272 (this is the approximation, not the draws)")
P(f"old 74-draw normal-approx reproduction: {q74_43} significant vs old committed {old43}; max relative q difference {rep_relmax:.2e} (CSV rounding)")
P(f"old committed counts: beats {len(old_beats)}, worse {len(old_worse)}, flip {len(old_flip)}, robust {len(old_robust)} of {len(surv)} survivors")
P(f"at-ceiling links (real above every one of the 400 random draws): up {len(ceil_up)}, down {len(ceil_dn)}, flip {len(ceil_flip)} of {NP}; "
  f"expected by chance {exp_ceiling:.2f}; Poisson p up {pois_up:.3g}, flip {pois_flip:.3g}, down {pois_dn:.3g}")
P(f"strong no-better-than-random (p_up>0.05: more than 20 of 400 draws at least as high): {len(new_no_better)}")
P(f"of the {len(old_beats)} old beats-random links: still above all 400 draws {len(old_beats)-len(moved)}, moved off the ceiling {len(moved)}, of which {len(moved_hard)} now clearly no better than random")
P(f"halves (200+200): ceiling both {bothC}, one {oneC}, neither {neitherC}; flip-ceiling both {bothF}, one {oneF}; "
  f"no-better agreement {bothNo}, disagreement {disagreeNo}; rank corr of p {rho:.3f}; null-share corr {rho_share:.4f}; max share diff {maxdiff_share:.4f}")
P(f"null mean: 74 draws vs 400 draws max abs difference {maxdiff74:.4f}")
P(f"determinism vs old 74-run: {det}")
P(f"runtime {D.get('runtime')} s on {D.get('nproc')} workers, {D.get('total_fits'):,} regressions")
P("")
P("== TIER 1 (strict): empirical p from the 400 draws + BH ==")
P(f"  certified: up {cert_up272}/272 (BH272) and {cert_up136}/272 (BH136 per parity); down {cert_dn272}; both-spec {cert_upB272}; flip {cert_F}")
P(f"  resolution: smallest attainable empirical p = 1/{R+1} = {FLOOR:.5f}; BH line = {bh_min_p['BH272']:.3e} (272) / {bh_min_p['BH136']:.3e} (136)")
P(f"  a single link on its own cannot be certified at 400 draws: even beating all {R} draws gives 1/{R+1} = {FLOOR:.5f}, above the first BH step {bh_min_p['BH272']:.2e}; a lone finding would need {need_draws['BH272']} draws")
P(f"  but BH is a step-up rule: p_(k) <= k*0.05/{NP}. With {n_floor_up} links pinned at the floor the 14th-smallest clears its line "
  f"(14*0.05/{NP}={14*ALPHA/n272:.5f} > {FLOOR:.5f}), so BH rejects the whole floor cluster: k*={kstar_up}, p_(k*)={p_at_kstar:.5f}, and {cert_up272} up links are certified")
P(f"  required draws as a function of the number j of links truly at the ceiling: R+1 >= {NP}/(0.05*j); j=1 -> {draws_cluster[1]}, j=5 -> {draws_cluster[5]}, j=14 -> {draws_cluster[14]}, j=30 -> {draws_cluster[30]} "
  f"(observed cluster {n_floor_up})")
P(f"  BH bookkeeping check: q values are monotone and q >= p; statsmodels multipletests fdr_bh on the same p-values gives {statsmodels_check}")
P(f"  old 43 beats-random under the strict test: {len(strict_survive)} still certified, {len(strict_lost)} not; new (not old beats): {len(strict_new)}")
P("== TIER 2 (main inference): smoothed null fitted to the 400 draws ==")
P(f"  normal fit: {tier2['normal_272']} of 272 links significant (BH272), {tier2['normal_136']} (BH136); "
  f"t fit (median df {tier2['median_df']:.0f}): {tier2['t_272']} / {tier2['t_136']}; normal/t agree on {tier2['agree_272']}, disagree on {tier2['disagree_272']}")
P(f"  old 43 re-tested under the 400-draw normal null: survive {len(t2_survive)}, die {len(t2_died)}, new {len(t2_new)}")
P(f"  old 21 worse-than-random re-tested: {sum(1 for r in old_worse if r['worse_random_tier2'])} of 21 still below their smoothed null; "
  f"old 36 more-sign-flipping: {sum(1 for r in old_flip if r['flips_more_tier2'])} of 36 still more sign-flipping")
P(f"  verdict classes at 400 draws (smoothed null): " + ", ".join(f"{k} {v}" for k, v in sorted(class_new.items())))
P(f"  (t version: survive {len(t2_survive_t)}, die {len(t2_died_t)}, new {len(t2_new_t)})")
P(f"  DIED (old beats-random, now q>=0.05 with the better-estimated null): "
  + (", ".join(f"{table[i]['x']}->{table[i]['y']}" for i in t2_died) if t2_died else "none"))
P(f"  NEW (not old beats-random, now q<0.05): "
  + (", ".join(f"{table[i]['x']}->{table[i]['y']}" for i in t2_new) if t2_new else "none"))
P(f"  halves normal fit: A {half_norm['A']} sig, B {half_norm['B']}, both {half_norm['both']}, one {half_norm['one']}, "
  f"jaccard {half_norm['jaccard']:.2f}; agreement with full400 A {half_norm['full_agreeA']}/272, B {half_norm['full_agreeB']}/272")
P("== TIER 3 (descriptive): above every one of the 400 draws ==")
P(f"  up {len(ceil_up)}/272 (expected by chance {exp_ceiling:.2f}; Poisson p {pois_up:.2g}), down {len(ceil_dn)}, flip {len(ceil_flip)}")
P(f"  nominal p<=0.05 (uncorrected): up {n_nom_up} vs {NP*0.05:.1f} expected (binomial p {binom_p_up:.2g}); flip {n_nom_F} (p {binom_p_F:.2g}); "
  f"same with the 400-draw normal fit: {n_norm400_05}")
P(f"  binomial uncertainty of a share from {R} draws: worst-case 95% half-width {1.96*np.sqrt(0.25/R):.3f}; "
  f"a 0/{R} ceiling means the true chance is below about {3.0/R:.4f} (95%).")
P(f"  share significant with the same sign (family-balanced): real median {share_stats['median_share_TR']:.3f} vs random median {share_stats['median_null_TR']:.3f}; "
  f"real above the random mean for {share_stats['frac_real_above_null_mean']:.1%} of the 272 links; median binomial se {share_stats['median_bin_se']:.3f}")
P("")
P("== old beats-random links (43): status at 400 draws ==")
for r in sorted(old_beats, key=lambda r: -(r["share_TR"] if np.isfinite(r["share_TR"]) else 0)):
    P(f"  {r['x']:11s}->{r['y']:11s} TR t {r['pooled_TR_t']:+5.1f} share {r['share_TR']:.2f} null {r['null_TR_mean']:.2f} "
      f"(p95 {r['null_TR_p95']:.2f}) draws>=real {r['n_draws_ge_real']:3d}/{R} ceil {'Y' if r['ceil_up'] else '-'} "
      f"p_emp {r['emp_p_up_TR']:.4f} p_norm400 {r['p_up_normal400']:.1e} q_old {r['old_q_up_TR']:.1e} -> {r['verdict_400']}")
P("")
P("== old worse-than-random links (21) ==")
for r in sorted(old_worse, key=lambda r: r["share_TR"] if np.isfinite(r["share_TR"]) else 0):
    P(f"  {r['x']:11s}->{r['y']:11s} share {r['share_TR']:.2f} null {r['null_TR_mean']:.2f} draws<=real {r['n_draws_le_real']:3d}/{R} "
      f"p_dn {r['emp_p_dn_TR']:.4f} ceil_dn {'Y' if r['ceil_dn'] else '-'} q_old {r['old_q_dn_TR']:.1e}")
P("")
P("== old more-sign-flipping links (36) ==")
for r in sorted(old_flip, key=lambda r: r["flip_rate_TR"]):
    P(f"  {r['x']:11s}->{r['y']:11s} flip real {r['flip_rate_TR']:.2f} null {r['null_flip_mean']:.2f} draws<=real {r['n_draws_flip_le_real']:3d}/{R} "
      f"p {r['emp_p_flip_le']:.4f} ceilF {'Y' if r['ceil_flip'] else '-'} q_old {r['old_q_flip']:.1e}")
P("")
P("== 24 base-matrix survivors ==")
for r in [r for r in table if r["in_base_survivors"]]:
    P(f"  {r['x']:11s}->{r['y']:11s} share {r['share_TR']:.2f} fam_min {r['fam_min_TR']:.2f} flip {r['flip_rate_TR']:.2f} "
      f"nullflip {r['null_flip_mean']:.2f} robust {'Y' if r['robust_everywhere'] else '-'} old {r['old_class']} -> {r['verdict_400']}")
P("")
P("== new verdict counts ==")
cnt = defaultdict(int)
for r in table: cnt[r["verdict_400"]] += 1
for k in sorted(cnt): P(f"  {k:42s} {cnt[k]}")
P("")
P("== explicit changes of verdict category ==")
for r in table:
    o = r["old_class"]; v = r["verdict_400"]
    if o == "a_robust_everywhere" and not r["robust_everywhere"]:
        P(f"  ROBUST LOST: {r['x']}->{r['y']} (share {r['share_TR']:.2f}, fam_min {r['fam_min_TR']:.2f}, flip {r['flip_rate_TR']:.2f})")
    if o == "b_group_specific" and not v.startswith("group-specific"):
        P(f"  GROUP-SPECIFIC lost: {r['x']}->{r['y']} -> {v}")
    if o == "d_beats_random_no_clear_group" and not v.startswith("beats random"):
        P(f"  BEATS-RANDOM lost: {r['x']}->{r['y']} -> {v}")
    if o == "c_no_better_than_random" and v.startswith("beats random"):
        P(f"  BEATS-RANDOM gained: {r['x']}->{r['y']} (share {r['share_TR']:.2f}, old share-vs-null was not significant)")
    if o == "c_no_better_than_random" and r["robust_everywhere"]:
        P(f"  ROBUST GAINED: {r['x']}->{r['y']}")
open(os.path.join(OUTDIR, "summary400.txt"), "w").write("\n".join(L))
print("\n".join(L[:18]))
print("... wrote", OUTDIR)
