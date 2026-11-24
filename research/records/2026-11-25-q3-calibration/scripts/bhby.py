#!/usr/bin/env python3
"""Q3 job 2: validate the real 272-link empirical p-values, then recompute BH and BY from the
FULL sorted p-value vector for each of the four strict-tier families (up, down, sign-flip,
heterogeneity). No floor-count inference. Codex fdr_check.py is run unmodified on the same
complete families as an independent implementation.

Inputs (committed in inputs/):
  edge_table400.csv      grouping-multiverse-400 @ 1152cec, results/edge_table400.csv
  null_shares_TR.csv.gz  grouping-multiverse-400 @ 1152cec, results/null_shares_TR.csv.gz
  dependence_analysis.json  methods-multiverse-paper-2026-11-23, results/dependence_analysis.json
  fdr_check.py           codex-handoff-run-2026-11-24, unmodified
"""
import json, os, subprocess, sys
import numpy as np
import pandas as pd
from scipy.stats import kstest, f_oneway, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
INP = os.path.join(REC, "inputs")
OUT = os.path.join(REC, "results")
Q = 0.05


def step_up(p, q=Q, by=False):
    p = np.asarray(p, float)
    m = len(p)
    H = sum(1.0 / i for i in range(1, m + 1)) if by else 1.0
    order = np.argsort(p, kind="stable")
    th = q * np.arange(1, m + 1) / (m * H)
    ok = p[order] <= th
    keep = np.zeros(m, bool)
    if ok.any():
        keep[order[: np.nonzero(ok)[0].max() + 1]] = True
    return keep


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [float(max(0, c - h)), float(min(1, c + h))]


def main():
    os.makedirs(OUT, exist_ok=True)
    edge = pd.read_csv(os.path.join(INP, "edge_table400.csv"))
    null = pd.read_csv(os.path.join(INP, "null_shares_TR.csv.gz"))
    dep = json.load(open(os.path.join(INP, "dependence_analysis.json")))
    links = [f"{r.x}->{r.y}" for r in edge.itertuples()]
    assert len(links) == 272 == len(set(links)), "need 272 unique links"
    colmap = {}
    for c in null.columns:
        if c == "draw":
            continue
        colmap[c] = c
    missing = [l for l in links if l not in colmap]
    if missing:
        raise SystemExit(f"null array missing {len(missing)} links; cannot recompute p-values")
    NMAT = null[links].to_numpy(float)          # 400 draws x 272 links
    R = NMAT.shape[0]
    real = edge["share_TR"].to_numpy(float)
    out = {"inputs": {"edge_sha256_note": "see inputs/SHA256SUMS.txt", "R": int(R), "links": len(links)},
           "families": {}, "validation": {}, "committed": {}}

    def emp_p(nullmat, real, side):
        fin = np.isfinite(nullmat)
        valid = fin.sum(0)
        if side == "up":
            cnt = np.nansum(np.where(fin, nullmat >= real, 0), 0)
        else:
            cnt = np.nansum(np.where(fin, nullmat <= real, 0), 0)
        return (1 + cnt) / (1 + valid)

    # ---------- V1: recomputation of share-based p-values ----------
    p_up_re = emp_p(NMAT, real, "up")
    p_dn_re = emp_p(NMAT, real, "dn")
    p_up_c = edge["emp_p_up_TR"].to_numpy(float)
    p_dn_c = edge["emp_p_dn_TR"].to_numpy(float)
    d_up = float(np.nanmax(np.abs(p_up_re - p_up_c)))
    d_dn = float(np.nanmax(np.abs(p_dn_re - p_dn_c)))
    mism_up = int(np.sum(np.abs(p_up_re - p_up_c) > 1e-12))
    mism_dn = int(np.sum(np.abs(p_dn_re - p_dn_c) > 1e-12))
    tol = 1.0 / (R + 1)
    du = np.abs(p_up_re - p_up_c) / tol
    dd = np.abs(p_dn_re - p_dn_c) / tol
    out["validation"]["V1_p_recompute"] = dict(
        max_abs_diff_up=d_up, max_abs_diff_dn=d_dn, mismatches_up=mism_up, mismatches_dn=mism_dn,
        pass_=bool(d_up < 1e-12 and d_dn < 1e-12),
        note="the committed null array is rounded to 4 significant digits, so exact equality cannot "
             "hold; differences are in units of 1/401 draw counts",
        up_links_matching_within_1_draw=int(np.sum(du <= 1.001)),
        up_links_total=int(len(du)), up_max_draw_diff=float(du.max()),
        dn_links_matching_within_1_draw=int(np.sum(dd <= 1.001)), dn_max_draw_diff=float(dd.max()))

    # ---------- V2: floor, range, completeness ----------
    floor = 1.0 / (R + 1)
    fam_cols = {"up": "emp_p_up_TR", "down": "emp_p_dn_TR",
                "sign_flip": "emp_p_flip_le", "heterogeneity": "emp_p_Q_up"}
    V2 = {}
    for fam, col in fam_cols.items():
        p = edge[col].to_numpy(float)
        V2[fam] = dict(n=len(p), n_nan=int(np.isnan(p).sum()), min=float(np.nanmin(p)),
                       max=float(np.nanmax(p)), n_at_floor=int(np.sum(np.abs(p - floor) <= 1e-5 * floor)),
                       all_in_0_1=bool(np.all((p >= 0) & (p <= 1) & np.isfinite(p))))
    out["validation"]["V2_floor_range"] = V2

    # ---------- V3: marginal uniformity for links not claiming superiority ----------
    V3 = {}
    for fam in ("up", "down"):
        p = edge[fam_cols[fam]].to_numpy(float)
        sub = p[p > 0.05]
        ks = kstest(sub, "uniform")
        V3[fam] = dict(n_sub=len(sub), ks_stat=float(ks.statistic), ks_p=float(ks.pvalue),
                       frac_le_05=float((p <= 0.05).mean()),
                       expected_frac_if_valid=0.05)
    out["validation"]["V3_marginal_uniformity"] = V3

    # ---------- V3b: leave-one-out permutation p-values from the null draws ----------
    # For each draw r and link j, p_rj = (1 + #{s != r: null_s >= null_r}) / R. If the draws are
    # exchangeable, these pseudo p-values are uniform. This is a validity check that does not use
    # the real shares at all.
    loo = np.empty_like(NMAT)
    for r in range(R):
        others = np.delete(NMAT, r, axis=0)
        loo[r] = (1 + (others >= NMAT[r]).sum(0)) / R
    loo_flat = loo.ravel()
    ks_loo = kstest(loo_flat, "uniform")
    out["validation"]["V3b_leave_one_out_null"] = dict(
        n=int(loo_flat.size), ks_stat=float(ks_loo.statistic), ks_p=float(ks_loo.pvalue),
        frac_le_05=float((loo_flat <= 0.05).mean()), expected_frac_if_valid=0.05,
        ci_frac_le_05=wilson(int((loo_flat <= 0.05).sum()), int(loo_flat.size)),
        note="permutation-validity check on the random draws themselves; rounding of the committed "
             "null array creates ties and makes this mildly conservative")

    # ---------- V4: exchangeability of the 400 random draws ----------
    blocks = np.array_split(np.arange(R), 4)
    pvals = []
    for j in range(NMAT.shape[1]):
        col = NMAT[:, j]
        if not np.isfinite(col).all():
            continue
        groups = [col[b] for b in blocks]
        f, pv = f_oneway(*groups)
        if np.isfinite(pv):
            pvals.append(pv)
    pvals = np.array(pvals)
    ks_blocks = kstest(pvals, "uniform")
    draw_mean = NMAT.mean(1)
    rho, rho_p = spearmanr(np.arange(R), draw_mean)
    # block-mean range, descriptive
    bm = np.array([draw_mean[b].mean() for b in blocks])
    out["validation"]["V4_exchangeability"] = dict(
        n_links_tested=int(len(pvals)), frac_block_anova_p_lt_05=float((pvals < 0.05).mean()),
        frac_ci=wilson(int((pvals < 0.05).sum()), len(pvals)), ks_of_anova_p=float(ks_blocks.statistic),
        ks_p=float(ks_blocks.pvalue), spearman_draw_index_vs_mean_share=float(rho),
        spearman_p=float(rho_p), block_means=[float(x) for x in bm])

    # ---------- V5: flip/heterogeneity p-values are committed-p only ----------
    out["validation"]["V3a_real_marginal_descriptive"] = dict(
        up_frac_p_eq_1=float((edge["emp_p_up_TR"].to_numpy(float) >= 1 - 1e-9).mean()),
        note="descriptive only: real links need not be null, and links whose real share is at or below "
             "every random draw get p=1 by construction, so a uniform test on the real p-values is "
             "not a validity test")
    out["validation"]["V5_draw_arrays"] = dict(
        share_p_recomputed=True, flip_p_array_available=False, het_p_array_available=False,
        note="flip and heterogeneity p-values cannot be recomputed from the saved 400-draw array; "
             "they are used as committed and labelled committed-p only")

    # ---------- BH / BY per family, from the FULL sorted vector ----------
    HM = sum(1.0 / i for i in range(1, 273))
    csv_rows = []
    for fam, col in fam_cols.items():
        p = edge[col].to_numpy(float)
        bh = step_up(p, Q, by=False)
        by = step_up(p, Q, by=True)
        # BH with an effective number of tests m_eff (as an approximation, not a procedure)
        m_eff = 157
        order = np.argsort(p, kind="stable")
        th157 = Q * np.arange(1, 273) / m_eff
        ok157 = p[order] <= th157
        bh_meff = 0
        if ok157.any():
            bh_meff = int(np.nonzero(ok157)[0].max() + 1)
        out["families"][fam] = dict(p_col=col, n=int(len(p)), bh=int(bh.sum()), by=int(by.sum()),
                                    bh_at_m_eff_157=int(bh_meff), min_p=float(p.min()),
                                    n_at_floor=int(np.sum(np.abs(p - floor) <= 1e-5 * floor)),
                                    k_star_bh=int(np.nonzero(np.sort(p) <= Q * np.arange(1, 273) / 272)[0].max() + 1)
                                    if (np.sort(p) <= Q * np.arange(1, 273) / 272).any() else 0)
        for i, lk in enumerate(links):
            csv_rows.append(dict(family=fam, link=lk, p=float(p[i])))
    out["BY_harmonic"] = float(HM)

    # ---------- independent check with unmodified Codex fdr_check.py ----------
    csv_in = os.path.join(OUT, "families_for_fdr_check.csv")
    csv_out = os.path.join(OUT, "fdr_check_output.csv")
    pd.DataFrame(csv_rows).to_csv(csv_in, index=False)
    chk = subprocess.run([sys.executable, os.path.join(HERE, "fdr_check.py"), "--input", csv_in,
                          "--output", csv_out], capture_output=True, text=True)
    out["fdr_check"] = dict(returncode=chk.returncode, stdout=chk.stdout.strip(), stderr=chk.stderr.strip())
    if chk.returncode == 0:
        got = pd.read_csv(csv_out)
        comp = {}
        for fam in fam_cols:
            sub = got[got.family == fam]
            own = out["families"][fam]
            comp[fam] = dict(bh_agree=int(sub.bh.sum()) == own["bh"], by_agree=int(sub.by.sum()) == own["by"],
                             bh=int(sub.bh.sum()), by=int(sub.by.sum()))
        out["fdr_check"]["agreement_with_own"] = comp

    # ---------- committed values and the 0/35/44 story ----------
    commit = json.load(open(os.path.join(INP, "dependence_analysis.json")))
    cert = commit["certification"]
    out["committed"] = dict(headline_strict=dict(up=35, down=19, sign_flip=15, heterogeneity=53),
                            by_committed=cert.get("certified_by_M", {}),
                            by_procedure=commit["benjamini_yekutieli"]["certified"],
                            m_eff=cert.get("certified_by_M", {}).get("157"),
                            note="committed up/down/flip/het counts from summary400.txt/headline.json; "
                                 "BY and m_eff from methods dependence_analysis.json")
    recomputed = {fam: out["families"][fam]["bh"] for fam in fam_cols}
    expected = out["committed"]["headline_strict"]
    story_changes = bool(any(recomputed[k] != expected[k] for k in expected)) or \
        bool(out["families"]["up"]["by"] != 0) or \
        bool(out["families"]["up"]["bh_at_m_eff_157"] != 44)
    out["story"] = dict(recomputed_bh=recomputed, committed_bh=expected,
                        by_counts={fam: out["families"][fam]["by"] for fam in fam_cols},
                        bh_m_eff_157={fam: out["families"][fam]["bh_at_m_eff_157"] for fam in fam_cols},
                        story_changes=story_changes,
                        validation_passed=bool(out["validation"]["V1_p_recompute"]["pass_"]
                                               and all(v["all_in_0_1"] for v in V2.values())))
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "bhby.json"), "w"), indent=1, default=float)

    # plain text table
    lines = ["Q3 JOB 2 — validation and full-vector BH/BY", f"R={R} draws, {len(links)} links, q={Q}",
             f"V1 p recompute: NOT exact (committed null array rounded to 4 s.f.); up mismatches {mism_up}/272 "
             f"({out['validation']['V1_p_recompute']['up_links_matching_within_1_draw']} within one draw, max "
             f"{out['validation']['V1_p_recompute']['up_max_draw_diff']:.0f} draws); dn mismatches {mism_dn}/272",
             f"V2 floor counts: " + ", ".join(f"{k} {v['n_at_floor']}" for k, v in V2.items()),
             f"V3 KS uniformity: up stat {V3['up']['ks_stat']:.3f} (p {V3['up']['ks_p']:.3f}), "
             f"frac<=.05 {V3['up']['frac_le_05']:.3f}; down stat {V3['down']['ks_stat']:.3f} "
             f"(p {V3['down']['ks_p']:.3f}), frac<=.05 {V3['down']['frac_le_05']:.3f}",
             f"V3b leave-one-out null calibration: KS {out['validation']['V3b_leave_one_out_null']['ks_stat']:.4f} "
             f"(p {out['validation']['V3b_leave_one_out_null']['ks_p']:.4f}), frac<=.05 "
             f"{out['validation']['V3b_leave_one_out_null']['frac_le_05']:.4f} "
             f"(95% CI {out['validation']['V3b_leave_one_out_null']['ci_frac_le_05'][0]:.4f}-"
             f"{out['validation']['V3b_leave_one_out_null']['ci_frac_le_05'][1]:.4f})",
             f"V4 exchangeability: block-ANOVA p<.05 in {out['validation']['V4_exchangeability']['frac_block_anova_p_lt_05']:.3f} "
             f"of links (95% CI {out['validation']['V4_exchangeability']['frac_ci'][0]:.3f}-"
             f"{out['validation']['V4_exchangeability']['frac_ci'][1]:.3f}); Spearman draw-index vs mean share "
             f"{out['validation']['V4_exchangeability']['spearman_draw_index_vs_mean_share']:.3f}",
             "V5 flip/heterogeneity: no draw arrays — committed-p only",
             "",
             "family               BH(272)  BY(272)  BH(m_eff=157)  min_p        n_floor"]
    for fam in fam_cols:
        f = out["families"][fam]
        lines.append(f"{fam:20s} {f['bh']:7d} {f['by']:8d} {f['bh_at_m_eff_157']:14d} "
                     f"{f['min_p']:.5f}  {f['n_at_floor']:7d}")
    lines += ["", f"fdr_check.py agrees: {out['fdr_check'].get('agreement_with_own')}",
              f"committed counts: {expected}; BY committed {cert.get('certified_by_M')}",
              f"0/35/44 story changes: {story_changes}", ""]
    open(os.path.join(OUT, "bhby.txt"), "w").write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
