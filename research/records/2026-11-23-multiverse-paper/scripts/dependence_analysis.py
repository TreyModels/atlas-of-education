#!/usr/bin/env python3
"""Dependence analysis for the resolution rule.

Reads the committed 400-draw random-share matrix (null_shares_TR.csv.gz, 400 draws x 272 links,
family-balanced shares) and the 400-draw edge table (real family-balanced shares), and reports:
  (1) the dependence of the 272 tests: correlation matrix, mean |r|, sign split;
  (2) the effective number of independent tests (Li & Ji 2005), and PCs-for-90%-variance;
  (3) BH step-up certification counts under M = 272 (baseline), M = M_eff (adjusted), and a
      sensitivity grid over M;
  (4) the draws needed for a lone link and for a cluster of j under each M;
  (5) a dependence-aware permutation null for the certified count: each random draw is treated
      as pseudo-real and compared with the other 399 draws (leave-one-out), giving a null
      distribution of how many links BH certifies when there is no real grouping at all.
Inputs are committed to this branch (2026-11-23-grouping-multiverse-400 merged into it).
"""
import csv, gzip, json, itertools
import numpy as np

BASE = "../2026-11-23-grouping-multiverse-400/results"
R = 400
ALPHA = 0.05

# ---- load null matrix -------------------------------------------------------
with gzip.open(f"{BASE}/null_shares_TR.csv.gz", "rt") as f:
    rd = csv.reader(f)
    header = next(rd)
    links = header[1:]
    X = np.array([[float(v) for v in row[1:]] for row in rd], dtype=float)
assert X.shape == (R, len(links)), X.shape
M = len(links)

# ---- load real shares -------------------------------------------------------
real = {}
with open(f"{BASE}/edge_table400.csv") as f:
    for r in csv.DictReader(f):
        real[f"{r['x']}->{r['y']}"] = float(r["share_TR"])
missing = [l for l in links if l not in real]
assert not missing, missing
r_real = np.array([real[l] for l in links])

# ---- dependence -------------------------------------------------------------
C = np.corrcoef(X, rowvar=False)
off = C[~np.eye(M, dtype=bool)]
eig = np.linalg.eigvalsh(C)
eig = np.clip(eig, 0, None)
m_eff_li_ji = float(eig.sum() ** 2 / (eig ** 2).sum())  # Li & Ji (2005) equivalent
cum = np.cumsum(np.sort(eig)[::-1]) / eig.sum()
pcs90 = int(np.searchsorted(cum, 0.90) + 1)
dep = dict(
    n_links=M, n_draws=R,
    mean_offdiag_r=float(off.mean()),
    mean_abs_offdiag_r=float(np.abs(off).mean()),
    median_offdiag_r=float(np.median(off)),
    frac_positive=float((off > 0).mean()),
    frac_negative=float((off < 0).mean()),
    max_abs_r=float(np.abs(off).max()),
    m_eff_li_ji=round(m_eff_li_ji, 2),
    pcs_for_90pct_variance=pcs90,
)

# ---- empirical p-values and BH -------------------------------------------------
def bh(p, m):
    p = np.asarray(p, float); out = np.full(len(p), np.nan)
    idx = np.where(np.isfinite(p))[0]
    o = idx[np.argsort(p[idx], kind="stable")]
    q = p[o] * m / np.arange(1, len(o) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out[o] = np.minimum(q, 1.0)
    return out

def count_at_floor(real_vec, null_mat):
    # empirical one-sided p, floor 1/(R+1)
    ge = (null_mat >= real_vec[None, :] - 1e-12).sum(0)
    return (1.0 + ge) / (null_mat.shape[0] + 1.0)

p = count_at_floor(r_real, X)
cert = {}
for m in sorted({272, int(round(m_eff_li_ji)), 150, 100, 50}):
    q = bh(p, m)
    cert[str(m)] = int((q < ALPHA).sum())
# breakdown at the floor: how many links have p == floor and how many are certified
floor = 1.0 / (R + 1)
n_floor = int((np.abs(p - floor) < 1e-12).sum())
q272 = bh(p, 272)
# proper BH step-up rank: largest k with sorted p_(k) <= k*alpha/M
ps = np.sort(p)
ks = np.arange(1, len(ps) + 1)
passing = np.where(ps <= ks * ALPHA / 272)[0]
k_star = int(passing.max() + 1) if len(passing) else 0

# draws needed under M: lone link and clusters
def draws_for(m, j=1):
    return int(np.ceil(m / (ALPHA * j)))
draws = {str(m): {"lone": draws_for(m, 1), "cluster_30": draws_for(m, 30), "cluster_35": draws_for(m, 35)}
         for m in [272, int(round(m_eff_li_ji)), 150, 100]}

# ---- dependence-aware permutation null for the certified count ----------------
# treat each draw as pseudo-real; p from the other 399 draws; BH at 5%
def cert_count_from_p(pvec, m):
    q = bh(pvec, m)
    return int((q < ALPHA).sum())

null_counts_272 = []
null_counts_meff = []
for d in range(R):
    other = np.delete(X, d, axis=0)
    pd_ = (1.0 + (other >= X[d][None, :] - 1e-12).sum(0)) / (other.shape[0] + 1.0)
    null_counts_272.append(cert_count_from_p(pd_, 272))
    null_counts_meff.append(cert_count_from_p(pd_, int(round(m_eff_li_ji))))
null_counts_272 = np.array(null_counts_272)
null_counts_meff = np.array(null_counts_meff)

# ---- Benjamini-Yekutieli (arbitrary dependence) ---------------------------------
H_M = float(np.sum(1.0 / np.arange(1, M + 1)))
alpha = ALPHA
# BY: sort p, largest k with p_(k) <= k*alpha/(M*H_M)
ps = np.sort(p)
ks = np.arange(1, len(ps) + 1)
passing_by = np.where(ps <= ks * alpha / (M * H_M))[0]
certified_by = int(passing_by.max() + 1) if len(passing_by) else 0
by_threshold_rank1 = alpha / (M * H_M)
by_draws = {"lone": int(np.ceil(M * H_M / alpha)),
            "cluster_30": int(np.ceil(M * H_M / (alpha * 30))),
            "cluster_35": int(np.ceil(M * H_M / (alpha * 35)))}
by_info = dict(
    family_size=M,
    family_members="one trends-specification p-value per directed link (272); the committed analysis forms BH over bh(p_up[J]) with J = np.arange(1, NE, 2), NE = 544 specs, i.e. 272 values",
    direction="up; the down, sign-flip and heterogeneity counts in the strict tier are three further separate BH procedures, each over the same 272-link family, not a single joint 122-test family",
    H_M=round(H_M, 4), threshold_rank1=round(by_threshold_rank1, 8),
    certified=certified_by, draws_needed=by_draws,
    min_rank_needed_at_floor=int(np.ceil((1.0/(R+1)) / by_threshold_rank1)),
    n_at_floor=n_floor,
    per_procedure_by_zero=dict(
        up=0, down=0, flip=0, het=0,
        floor_clusters=dict(up=30, down=19, flip=15, het=53),
        note="Each of the four procedures has family size 272, so each needs rank >= 84 at the 400-draw floor; every floor cluster is below 84, so BY certifies zero in every procedure. The down/flip/het null matrices were not saved with the committed record, so these are floor-size deductions, not recomputations."),
    hypothetical_per_direction_68=dict(
        certified=35,
        draws_needed=dict(lone=6533, cluster_30=218, cluster_35=186),
        note="NOT the committed family. A hypothetical 272/4 = 68-link family would give BY=35 and budgets 6,533/218/186, but no 68-link family appears in analyse400.py; this row is recorded only to reconcile the three readings in the audit."),
    note="BY controls FDR under arbitrary dependence; at 400 draws the p floor is above its first-step threshold, so certification requires a floor cluster of at least the stated rank.")

out = dict(
    source_matrix=f"{BASE}/null_shares_TR.csv.gz",
    source_real=f"{BASE}/edge_table400.csv (column share_TR)",
    dependence=dep,
    certification=dict(M_baseline=272, certified_baseline=cert.get("272"), certified_by_M=cert,
                       n_at_floor=n_floor, floor=round(floor, 8), k_star=k_star),
    draws_needed=draws,
    benjamini_yekutieli=by_info,
    permutation_null_of_certified_count=dict(
        M=272, mean=float(null_counts_272.mean()), p95=float(np.percentile(null_counts_272, 95)),
        p99=float(np.percentile(null_counts_272, 99)), max=int(null_counts_272.max()),
        n_ge_35=int((null_counts_272 >= cert.get("272", 0)).sum()),
        M_eff=dict(mean=float(null_counts_meff.mean()), p95=float(np.percentile(null_counts_meff, 95)),
                   max=int(null_counts_meff.max()))),
    notes=("Family-balanced random shares; real share from edge_table400.share_TR. "
           "Li & Ji (2005) effective-tests formula on the correlation matrix of the 272 null-share series. "
           "The permutation null treats each of the 400 draws as pseudo-real and compares it with the other 399."),
)
json.dump(out, open("results/dependence_analysis.json", "w"), indent=1)
print(json.dumps(out, indent=1))
