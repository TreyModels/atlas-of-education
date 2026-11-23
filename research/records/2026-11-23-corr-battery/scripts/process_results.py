#!/usr/bin/env python3
"""Post-process the task-21 battery: turn checkpoint arrays into the compact
results table, transportability comparison, bootstrap summary, placebo
comparison and two figures. Run after battery.py finishes.

Inputs : /root/work/corr_battery/out/checkpoint_final.pkl
Outputs: /root/work/corr_battery/out/results_summary.json
         /root/work/corr_battery/out/pair_table.csv
         /root/work/corr_battery/out/transport.csv
         /root/work/corr_battery/figures/fig_battery_levels_vs_changes.png
         /root/work/corr_battery/figures/fig_transportability.png
"""
import csv, json, os, pickle
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/root/work/corr_battery/out"
FIG = "/root/work/corr_battery/figures"
os.makedirs(FIG, exist_ok=True)

ALLM = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp", "gdppc_log",
        "urban", "tax", "agri_va", "emp_agri", "flfp", "life_exp", "u5mr",
        "gpi_sec", "gpi_ter", "fertility", "mys_total", "mys_female"]
PAIRS = [(y, x) for y in ALLM for x in ALLM if y != x]
LAGS = [0, 5, 10, 15, 20, 25]
FE_LEVEL = ["dec", "dec_reg", "country", "country_trend"]
FE_CHANGE = ["country", "country_trend", "dec_reg"]
CTRLS = ["none", "income", "inc_urb"]
SAMPLES = ["all", "p1960_1990", "p1990_2024"] + [f"region" for r in range(7)] + \
          [f"income" for g in range(4)] + [f"decade" for d in range(7)] + \
          [f"regxinc" for r in range(7) for g in range(4)]
BOOT_CELL = (1, 2, 0)

with open(os.path.join(OUT, "checkpoint_final.pkl"), "rb") as f:
    ck = pickle.load(f)
res = ck["res"]
meta = dict(regs=ck["regs"], elapsed=ck["elapsed"], done=ck["done"])
print("checkpoint:", meta)

summary = dict(counts=meta, pairs={})

# ---------------- Grid A ----------------
A = res["A"]
# columns: pair, rel, fe_i, ctrl_i, lag_i, sample_i, b, se, n, nc
if len(A):
    pair = A[:, 0].astype(int); rel = A[:, 1].astype(int)
    fe = A[:, 2].astype(int); ci = A[:, 3].astype(int)
    lag = A[:, 4].astype(int); si = A[:, 5].astype(int)
    b = A[:, 6]; se = A[:, 7]; n = A[:, 8]; nc = A[:, 9]
    t = b / np.where(se > 0, se, np.nan)

    def shares(mask):
        if not mask.any():
            return dict(n=0)
        bb = b[mask]; tt = t[mask]
        neg = bb < 0
        return dict(n=int(mask.sum()),
                    share_negative=float(neg.mean()),
                    share_negative_significant=float((neg & (tt < -1.96)).mean()),
                    share_positive_significant=float(((bb > 0) & (tt > 1.96)).mean()),
                    median_b=float(np.median(bb)))

    # pre-registered "baseline" cells: fe dec/dec_reg for levels; country/country_trend for changes;
    # controls inc_urb; lags all; samples all + two periods
    base_mask = ((si <= 2) & (ci == 2))
    lev_base = base_mask & (rel == 0) & (fe <= 1)
    chg_base = base_mask & (rel == 1) & (fe <= 1)
    summary["grid_a"] = dict(
        levels=shares(lev_base), changes=shares(chg_base),
        levels_all=shares(rel == 0), changes_all=shares(rel == 1))
    # real-group transportability analogue: within each real grouping sample the
    # pair-level relation is one "group x pair" estimate (regions 7, incomes 4,
    # decades 7; lag 0, income+urban controls)
    real_masks = []
    region_idx = list(range(3, 10)); income_idx = list(range(10, 14)); decade_idx = list(range(14, 21))
    for si_ in region_idx + income_idx + decade_idx:
        real_masks.append((rel == 0) & (fe == 0) & (ci == 2) & (lag == 0) & (si == si_))
    real_levels = np.zeros(len(b), dtype=bool)
    for mm in real_masks:
        real_levels |= mm
    real_masks = []
    for si_ in region_idx + income_idx + decade_idx:
        real_masks.append((rel == 1) & (fe == 0) & (ci == 2) & (lag == 0) & (si == si_))
    real_changes = np.zeros(len(b), dtype=bool)
    for mm in real_masks:
        real_changes |= mm
    summary["real_groups"] = dict(levels=shares(real_levels), changes=shares(real_changes))

    # headline coefficients per pair: levels dec_reg/inc_urb/lag0/all ; changes country_trend/inc_urb/lag0/all
    def pick(relm, fem, lagm):
        m = (rel == relm) & (fe == fem) & (ci == 2) & (lag == lagm) & (si == 0)
        return m
    ml = pick(0, 1, 0)   # levels: dec_reg
    mc = pick(1, 1, 0)   # changes: country_trend
    bl = {int(pair[i]): (float(b[i]), float(se[i]), int(n[i]), int(nc[i]))
          for i in np.where(ml)[0]}
    bc = {int(pair[i]): (float(b[i]), float(se[i]), int(n[i]), int(nc[i]))
          for i in np.where(mc)[0]}
    for p, (y, x) in enumerate(PAIRS):
        m = pair == p
        summary["pairs"][f"{y}->{x}"] = dict(
            level=bl.get(p), change=bc.get(p),
            level_specs=shares(m & (rel == 0)),
            change_specs=shares(m & (rel == 1)))

    # placebo comparison: same cells as the pre-registered levels baseline
    plt.figure(figsize=(6.5, 5.5))
    for relm, color, lab in ((0, "#1f77b4", "levels"), (1, "#d62728", "decade changes")):
        mm = (rel == relm) & (ci == 2) & (si == 0) & (lag == 0) & (fe <= 1)
        plt.scatter(b[mm], t[mm], s=6, alpha=0.4, color=color, label=lab)
    plt.axhline(0, color="k", lw=0.8); plt.axhline(-1.96, color="0.5", lw=0.6, ls="--")
    plt.axhline(1.96, color="0.5", lw=0.6, ls="--")
    plt.xlabel("coefficient"); plt.ylabel("t statistic")
    plt.title("Every pair, headline specs (levels vs decade changes)")
    plt.legend(fontsize=8, frameon=False); plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_battery_levels_vs_changes.png"), dpi=170)
    plt.close()

# ---------------- Grid B transportability ----------------
B = res["B"]
if len(B):
    # columns: part, pair, rel, n_est, n_neg, sum_b  (aggregated per partition x pair x relation)
    part = B[:, 0].astype(np.int64); pairB = B[:, 1].astype(np.int64)
    rel = B[:, 2].astype(np.int64); n_est = B[:, 3]; n_neg = B[:, 4]
    key = part * 2 + rel
    K = int(key.max()) + 1
    tot = np.bincount(key, weights=n_est, minlength=K)
    neg = np.bincount(key, weights=n_neg, minlength=K)
    ok = tot > 0
    is_rel = (np.arange(K) % 2 == 1)
    lev = ok & (~is_rel); chg = ok & is_rel
    levels_shares = (neg[lev] / tot[lev])
    change_shares = (neg[chg] / tot[chg])
    summary["transport"] = dict(
        n_partitions=int(len(np.unique(part))),
        levels_mean=float(np.mean(levels_shares)),
        levels_q05=float(np.percentile(levels_shares, 5)),
        levels_q95=float(np.percentile(levels_shares, 95)),
        change_mean=float(np.mean(change_shares)),
        change_q05=float(np.percentile(change_shares, 5)),
        change_q95=float(np.percentile(change_shares, 95)))
    # per-pair transportability (pooled over all partitions)
    keyp = pairB * 2 + rel
    Kp = int(keyp.max()) + 1
    totp = np.bincount(keyp, weights=n_est, minlength=Kp)
    negp = np.bincount(keyp, weights=n_neg, minlength=Kp)
    transport_pairs = {}
    for k in range(Kp):
        if totp[k] == 0:
            continue
        p_i, r_i = divmod(k, 2)
        transport_pairs.setdefault(str(p_i), {})[str(r_i)] = float(negp[k] / totp[k])
    summary["transport_pairs"] = transport_pairs
    focal = [("fertility", "mys_female"), ("fertility", "mys_total"), ("fertility", "sec"),
             ("fertility", "lsc"), ("fertility", "prm_cmp"), ("fertility", "ter")]
    summary["transport_focal_pairs"] = {
        f"{y}->{x}": transport_pairs.get(str(PAIRS.index((y, x))), {}) for (y, x) in focal}
    with open(os.path.join(OUT, "transport.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["partition", "relation", "n_estimates", "n_negsig", "share"])
        for k in range(K):
            if tot[k] > 0:
                w.writerow([k // 2, k % 2, int(tot[k]), int(neg[k]), neg[k] / tot[k]])
    plt.figure(figsize=(6.5, 4))
    plt.hist(levels_shares, bins=25, alpha=0.75, color="#1f77b4", label="levels")
    plt.hist(change_shares, bins=25, alpha=0.75, color="#d62728", label="decade changes")
    plt.xlabel("share of within-group pair estimates negative & significant")
    plt.ylabel("partitions"); plt.legend(fontsize=8, frameon=False)
    plt.title(f"Transportability over {len(np.unique(part))} random repartitions")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "fig_transportability.png"), dpi=170)
    plt.close()

# ---------------- Grid C bootstrap ----------------
C = res.get("C")
if C is None or not len(C):
    _p = os.path.join(OUT, "final_C.npz")
    if os.path.exists(_p):
        C = np.load(_p)["C"]
        print("loaded bootstrap from final_C.npz", C.shape)
    else:
        C = np.zeros((0, 8))
if len(C):
    # columns: pair, cell, n, mean, sd, q05, q50, q95
    excl = 0; total = 0; rows = []
    for i in range(len(C)):
        p = int(C[i, 0]); n_ = int(C[i, 2]); q05 = C[i, 5]; q95 = C[i, 7]
        total += 1
        if q05 > 0 or q95 < 0:
            excl += 1
        rows.append((p, n_, C[i, 3], C[i, 6], q05, q95))
    summary["bootstrap"] = dict(cells=total, share_ci_excludes_zero=excl / max(total, 1),
                                n_pairs=len({int(x[0]) for x in C}))
    with open(os.path.join(OUT, "bootstrap.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["pair", "draws", "mean", "median", "q05", "q95"])
        w.writerows(rows)

# ---------------- threshold bootstrap ----------------
T = res.get("T")
if T is None or not len(T):
    _p = os.path.join(OUT, "final_T.npz")
    if os.path.exists(_p):
        T = np.load(_p)["T"]
        print("loaded threshold bootstrap from final_T.npz", T.shape)
    else:
        T = np.zeros((0, 6))
if len(T):
    summary["threshold_bootstrap"] = [
        dict(measure=int(r[0]), term=int(r[1]), draws=int(r[2]),
             q05=float(r[3]), q50=float(r[4]), q95=float(r[5])) for r in T]

# ---------------- placebo ----------------
P = res["P"]
if len(P):
    # columns: pair, fe, ctrl, sample, b, se, n, nc
    bb = P[:, 4]; se = P[:, 5]; t = bb / np.where(se > 0, se, np.nan)
    summary["placebo_future"] = dict(
        n=int(len(bb)), share_negative=float((bb < 0).mean()),
        share_negative_significant=float(((bb < 0) & (t < -1.96)).mean()),
        median_b=float(np.median(bb)))
    # focal-pair placebo comparison (schooling -> fertility pairs only)
    focal_pairs = [(y, x) for (y, x) in
                   [("fertility", m) for m in ("mys_female", "mys_total", "sec", "lsc", "prm_cmp", "ter")]]
    fp = np.array([PAIRS.index((y, x)) for (y, x) in focal_pairs])
    pm = np.isin(P[:, 0].astype(int), fp)
    if pm.any():
        bf = P[pm, 4]; sf = P[pm, 5]; tf = bf / np.where(sf > 0, sf, np.nan)
        summary["placebo_focal"] = dict(
            n=int(pm.sum()), share_negative=float((bf < 0).mean()),
            share_negative_significant=float(((bf < 0) & (tf < -1.96)).mean()),
            median_b=float(np.median(bf)))
    # correct-time comparison at the SAME design cells as each placebo row:
    # key = (pair, fe, ctrl, sample) matched to Grid A rows with rel=0, lag=0
    if len(A):
        amap = {}
        for i in np.where((A[:, 1] == 0) & (A[:, 4] == 0))[0]:
            key = (int(A[i, 0]), int(A[i, 2]), int(A[i, 3]), int(A[i, 5]))
            amap[key] = (A[i, 6], A[i, 7])
        pairs_b = []
        for i in range(len(P)):
            key = (int(P[i, 0]), int(P[i, 1]), int(P[i, 2]), int(P[i, 3]))
            if key in amap:
                pairs_b.append(amap[key])
        focal_keys = {(PAIRS.index((y, x)), int(P[i, 1]), int(P[i, 2]), int(P[i, 3]))
                      for i in range(len(P)) for (y, x) in
                      [("fertility", m) for m in ("mys_female", "mys_total", "sec", "lsc",
                                                  "prm_cmp", "ter")]}
        pairs_b_focal = [amap[k] for k in focal_keys if k in amap]
        if pairs_b_focal:
            bf0 = np.array([x[0] for x in pairs_b_focal])
            sf0 = np.array([x[1] for x in pairs_b_focal])
            tf0 = bf0 / np.where(sf0 > 0, sf0, np.nan)
            summary["correct_time_focal"] = dict(
                n=int(len(bf0)), share_negative=float((bf0 < 0).mean()),
                share_negative_significant=float(((bf0 < 0) & (tf0 < -1.96)).mean()),
                median_b=float(np.median(bf0)))
        if pairs_b:
            b0 = np.array([x[0] for x in pairs_b]); s0 = np.array([x[1] for x in pairs_b])
            t0 = b0 / np.where(s0 > 0, s0, np.nan)
            summary["correct_time_same_cells"] = dict(
                n=int(len(b0)), share_negative=float((b0 < 0).mean()),
                share_negative_significant=float(((b0 < 0) & (t0 < -1.96)).mean()),
                median_b=float(np.median(b0)))

# ---------------- pair table ----------------
with open(os.path.join(OUT, "pair_table.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["outcome", "predictor", "level_b", "level_se", "level_n", "level_countries",
                "change_b", "change_se", "change_n", "change_countries",
                "level_share_neg", "level_share_negsig", "change_share_neg", "change_share_negsig",
                "transport_level_share", "transport_change_share"])
    for k, v in summary["pairs"].items():
        y, x = k.split("->")
        lv = v["level"] if v["level"] else ("", "", "", "")
        ch = v["change"] if v["change"] else ("", "", "", "")
        ls = v["level_specs"]; cs = v["change_specs"]
        tp = summary.get("transport_pairs", {}).get(str(PAIRS.index((y, x))), {})
        w.writerow([y, x, *lv, *ch,
                    round(ls.get("share_negative", np.nan), 3),
                    round(ls.get("share_negative_significant", np.nan), 3),
                    round(cs.get("share_negative", np.nan), 3),
                    round(cs.get("share_negative_significant", np.nan), 3),
                    round(tp.get("0", np.nan), 3), round(tp.get("1", np.nan), 3)])

json.dump(summary, open(os.path.join(OUT, "results_summary.json"), "w"), indent=1, default=float)
print("wrote results_summary.json, pair_table.csv, transport.csv, bootstrap.csv and figures")
print(json.dumps({k: summary.get(k) for k in ("grid_a", "transport", "bootstrap", "placebo_future",
                                              "correct_time_same_cells")}, indent=1, default=float)[:3000])
