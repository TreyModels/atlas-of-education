#!/usr/bin/env python3
"""Task 15, part 2: transportability of the level relation, the pre-registered
specification curve, placebos, the income rival, and the figures.

Design frozen in PRE_REGISTRATION.md (commit c077672, before any code).
Part 1 (levels vs changes, lags, thresholds, cohort) is corr_rebuild_part1.py.
"""
import csv, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import corr_rebuild_part1 as P

OUT = "/root/work/corr_rebuild/out"
FIG = "/root/work/corr_rebuild/figures"
os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)
TFR, MEAS, INC, URB, REGION, INCOME = P.TFR, P.MEAS, P.INC, P.URB, P.REGION, P.INCOME
PANEL, COHORT = P.PANEL, P.COHORT


def fit(yv, cols, clusters):
    X = np.column_stack([np.ones(len(yv))] + cols)
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ yv, rcond=None)[0]
    u = yv - X @ b
    meat = np.zeros_like(XtX)
    for c in np.unique(clusters):
        m = clusters == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return b, float(np.sqrt(max(Vb[1, 1], 0)))


def dummies(vals):
    u = sorted(set(vals))
    return [np.array([1.0 if v == x else 0.0 for v in vals]) for x in u[1:]]


def tstat(b, se):
    return b / se if se > 0 else float("nan")


def level_rows(measure, lag=0, controls=("income", "urban"), lo=1870, hi=2024):
    rows = []
    X = MEAS[measure]
    for (i, t), x in X.items():
        ty = t + lag
        if ty > hi or (i, ty) not in TFR:
            continue
        if "income" in controls and (i, t) not in INC:
            continue
        if "urban" in controls and (i, t) not in URB:
            continue
        rows.append((i, t, TFR[(i, ty)], x, (INC.get((i, t))), (URB.get((i, t))),
                     REGION.get(i, ""), (t // 10) * 10))
    return rows


def spec_level(measure, lag=0, controls=("income", "urban"), fe="decade_region",
               form="linear", rows=None):
    rows = rows if rows is not None else level_rows(measure, lag, controls)
    if len(rows) < 100 or len({r[0] for r in rows}) < 10:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    cl = np.array([ui[v] for v in iso])
    x = np.array([r[3] for r in rows], float)
    yv = np.array([r[2] for r in rows], float)
    if form == "log":
        cols = [np.log(np.maximum(x, 0) + 1)]
    elif form == "quadratic":
        cols = [x, x ** 2]
    elif form == "spline":
        cols = [np.minimum(x, 6.0), np.clip(x - 6.0, 0, 3.0),
                np.maximum(x - 9.0, 0)]
    else:
        cols = [x]
    if "income" in controls:
        cols.append(np.array([r[4] for r in rows], float))
    if "urban" in controls:
        cols.append(np.array([r[5] for r in rows], float))
    if fe in ("decade", "decade_region"):
        cols += dummies([r[7] for r in rows])
    if fe == "decade_region":
        cols += dummies([r[6] for r in rows])
    b, se = fit(yv, cols, cl)
    return dict(b=float(b[1]), se=se, n=len(rows), nc=len(ui),
                form=form, controls=list(controls), fe=fe, lag=lag, measure=measure)


def spec_cohort(measure, controls=("income", "urban"), fe="decade_region", form="linear"):
    rows = []
    for (i, cohort), cf in COHORT.items():
        x = MEAS[measure].get((i, cohort + 25))
        if x is None:
            x = MEAS[measure].get((i, cohort + 20))
        if x is None:
            continue
        rows.append((i, cohort, cf, x, REGION.get(i, ""), (cohort // 10) * 10))
    if len(rows) < 30 or len({r[0] for r in rows}) < 6:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    cl = np.array([ui[v] for v in iso])
    x = np.array([r[3] for r in rows], float)
    yv = np.array([r[2] for r in rows], float)
    if form == "log":
        cols = [np.log(np.maximum(x, 0) + 1)]
    elif form == "quadratic":
        cols = [x, x ** 2]
    elif form == "spline":
        cols = [np.minimum(x, 6.0), np.clip(x - 6.0, 0, 3.0), np.maximum(x - 9.0, 0)]
    else:
        cols = [x]
    if fe in ("decade", "decade_region"):
        cols += dummies([r[5] for r in rows])
    if fe == "decade_region":
        cols += dummies([r[4] for r in rows])
    b, se = fit(yv, cols, cl)
    return dict(b=float(b[1]), se=se, n=len(rows), nc=len(ui), form=form,
                controls=list(controls), fe=fe, outcome="cohort", measure=measure)


def spec_change(measure, controls=("income", "urban"), trends=True, backwards=False):
    """Decade-change relation (the matrix) for the transportability contrast."""
    rows = []
    for (i, t), x in MEAS[measure].items():
        if backwards:
            if (i, t) not in TFR or (i, t - 10) not in TFR:
                continue
            dy = TFR[(i, t)] - TFR[(i, t - 10)]
        else:
            if (i, t) not in TFR or (i, t + 10) not in TFR:
                continue
            dy = TFR[(i, t + 10)] - TFR[(i, t)]
        if "income" in controls and (i, t) not in INC:
            continue
        if "urban" in controls and (i, t) not in URB:
            continue
        rows.append((i, t, dy, x, INC.get((i, t)), URB.get((i, t)), REGION.get(i, "")))
    if len(rows) < 60:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    yr = np.array([r[1] for r in rows], float)
    gy = ((yr // 10) * 10).astype(int)

    def dm(a, g):
        s = np.bincount(g, weights=a); c = np.bincount(g)
        return a - (s / np.maximum(c, 1))[g]
    yv = np.array([r[2] for r in rows], float)
    cols = [np.array([r[3] for r in rows], float)]
    if "income" in controls:
        cols.append(np.array([r[4] for r in rows], float))
    if "urban" in controls:
        cols.append(np.array([r[5] for r in rows], float))
    if trends:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(yv, gi), gy)
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return dict(b=float(b[1]), se=float(np.sqrt(max(Vb[1, 1], 0))), n=len(rows),
                nc=len(ui))


def group_level(measure, members, controls=("income", "urban"), lag=0, years=None):
    """Level relation inside one grouping (countries in `members`, optional year window)."""
    rows = [r for r in level_rows(measure, lag, controls) if r[0] in members]
    if years is not None:
        rows = [r for r in rows if years[0] <= r[1] < years[1]]
    if len(rows) < 60 or len({r[0] for r in rows}) < 6:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    cl = np.array([ui[v] for v in iso])
    x = np.array([r[3] for r in rows], float)
    yv = np.array([r[2] for r in rows], float)
    cols = [x]
    if "income" in controls:
        cols.append(np.array([r[4] for r in rows], float))
    if "urban" in controls:
        cols.append(np.array([r[5] for r in rows], float))
    cols += dummies([r[7] for r in rows])
    b, se = fit(yv, cols, cl)
    return dict(b=float(b[1]), se=se, n=len(rows), nc=len(ui))


def group_change(measure, members, controls=("income", "urban"), trends=False, years=None):
    sub = {k: v for k, v in MEAS[measure].items()
           if k[0] in members and (years is None or years[0] <= k[1] < years[1])}
    P.MEAS["__tmp__"] = sub
    try:
        r = spec_change("__tmp__", controls=controls, trends=trends)
    finally:
        del P.MEAS["__tmp__"]
    return r


if __name__ == "__main__":
    RES = {}
    measure = "mys_female"
    print("=== Analysis 2: transportability of the level relation ===")
    families = {
        "region": {},
        "income": {},
        "decade": {},
        "region_x_decade": {},
    }
    countries = sorted({i for (i, t) in TFR if i in PANEL})
    YEARS = {}
    for i in countries:
        families["region"].setdefault(REGION.get(i, ""), set()).add(i)
        families["income"].setdefault(INCOME.get(i, ""), set()).add(i)
    for t in range(1960, 2021, 10):
        families["decade"].setdefault(t, set()).update(countries)
        YEARS.setdefault("decade", {})[t] = (t, t + 10)
    for i in countries:
        for t in range(1960, 2021, 10):
            families["region_x_decade"].setdefault((REGION.get(i, ""), t), set()).add(i)
            YEARS.setdefault("region_x_decade", {})[(REGION.get(i, ""), t)] = (t, t + 10)

    RES["transport"] = {}
    for fam, groups in families.items():
        lv, ch = [], []
        for gname, mem in groups.items():
            if len(mem) < 6:
                continue
            yearwin = YEARS.get(fam, {}).get(gname)
            lr = group_level(measure, mem, years=yearwin)
            if lr:
                lv.append(dict(group=str(gname), b=lr["b"], se=lr["se"],
                               n=lr["n"], nc=lr["nc"],
                               neg_sig=bool(lr["b"] < 0 and tstat(lr["b"], lr["se"]) < -1.96)))
            cr = group_change(measure, mem, years=yearwin)
            if cr:
                ch.append(dict(group=str(gname), b=cr["b"], se=cr["se"],
                               n=cr["n"], nc=cr["nc"],
                               neg_sig=bool(cr["b"] < 0 and tstat(cr["b"], cr["se"]) < -1.96)))
        share_l = np.mean([x["neg_sig"] for x in lv]) if lv else None
        share_c = np.mean([x["neg_sig"] for x in ch]) if ch else None
        RES["transport"][fam] = dict(n_groups_level=len(lv), share_level_neg_sig=share_l,
                                     n_groups_change=len(ch), share_change_neg_sig=share_c,
                                     level=lv, change=ch)
        print(f"  {fam:16s} groups={len(lv):3d} level share neg.sig={share_l} "
              f"| change groups={len(ch):3d} share neg.sig={share_c}")

    # random yardstick: 400 random repartitions into 7 groups (region family size)
    rng = np.random.default_rng(20261123)
    k = max(2, len([g for g in families["region"].values() if len(g) >= 6]))
    sizes = [len(g) for g in families["region"].values() if len(g) >= 6]
    level_shares, change_shares = [], []
    for _ in range(400):
        perm = rng.permutation(countries)
        parts, pos = [], 0
        for sz in sizes:
            parts.append(set(perm[pos:pos + sz])); pos += sz
        lv, ch = [], []
        for mem in parts:
            lr = group_level(measure, mem)
            if lr:
                lv.append(lr)
            cr = group_change(measure, mem)
            if cr:
                ch.append(cr)
        if lv:
            level_shares.append(np.mean([x["b"] < 0 and tstat(x["b"], x["se"]) < -1.96 for x in lv]))
        if ch:
            change_shares.append(np.mean([x["b"] < 0 and tstat(x["b"], x["se"]) < -1.96 for x in ch]))
    RES["random_yardstick"] = dict(
        k_groups=k,
        level_mean=float(np.mean(level_shares)), level_q05=float(np.percentile(level_shares, 5)),
        level_q95=float(np.percentile(level_shares, 95)),
        change_mean=(float(np.mean(change_shares)) if change_shares else None),
        change_q05=(float(np.percentile(change_shares, 5)) if change_shares else None),
        change_q95=(float(np.percentile(change_shares, 95)) if change_shares else None),
        draws=len(level_shares))
    print(f"  random repartitions (k={k}, 400 draws): level share neg.sig mean="
          f"{np.mean(level_shares):.2f} [5-95%: {np.percentile(level_shares,5):.2f}-"
          f"{np.percentile(level_shares,95):.2f}]; change mean={np.mean(change_shares):.2f} "
          f"[{np.percentile(change_shares,5):.2f}-{np.percentile(change_shares,95):.2f}]")

    print("\n=== Analysis 4: pre-registered specification curve ===")
    specs = []
    for lag in (0, 10, 15, 20):
        for controls in (("income", "urban"), ("income",), ()):
            for fe in ("decade", "decade_region"):
                for form in ("linear", "log", "quadratic", "spline"):
                    for m in ("mys_female", "mys_total", "lsc"):
                        r = spec_level(m, lag=lag, controls=controls, fe=fe, form=form)
                        if r:
                            r.update(outcome="period", setting="period")
                            specs.append(r)
    for controls in (("income", "urban"), ("income",), ()):
        for fe in ("decade", "decade_region"):
            for form in ("linear", "log", "quadratic", "spline"):
                for m in ("mys_female", "mys_total", "lsc"):
                    r = spec_cohort(m, controls=controls, fe=fe, form=form)
                    if r:
                        r.update(setting="cohort")
                        specs.append(r)

    def summarize(ss, label):
        neg = [s for s in ss if s["b"] < 0]
        negsig = [s for s in neg if tstat(s["b"], s["se"]) < -1.96]
        possig = [s for s in ss if s["b"] > 0 and tstat(s["b"], s["se"]) > 1.96]
        out = dict(n=len(ss), share_negative=len(neg) / len(ss),
                   share_negative_significant=len(negsig) / len(ss),
                   share_positive_significant=len(possig) / len(ss),
                   median_b=float(np.median([s["b"] for s in ss])))
        print(f"  {label}: {out}")
        return out

    RES["spec_curve"] = dict(
        all=summarize(specs, "all 360-ish"),
        period=summarize([s for s in specs if s["setting"] == "period"], "period TFR"),
        cohort=summarize([s for s in specs if s["setting"] == "cohort"], "cohort fertility"),
    )
    with open(os.path.join(OUT, "spec_curve.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["setting", "measure", "outcome", "lag", "controls", "fe", "form",
                    "b", "se", "t", "n", "nc"])
        for s in specs:
            w.writerow([s["setting"], s["measure"], s.get("outcome", ""), s.get("lag", ""),
                        "+".join(s["controls"]) if s["controls"] else "none", s["fe"],
                        s["form"], round(s["b"], 5), round(s["se"], 5),
                        round(tstat(s["b"], s["se"]), 3), s["n"], s["nc"]])

    print("\n=== placebos ===")
    # (a) future schooling: schooling at t+10 predicting fertility at t
    placebo_future = []
    for controls in (("income", "urban"), ("income",)):
        for fe in ("decade", "decade_region"):
            for form in ("linear", "log"):
                for m in ("mys_female", "mys_total", "lsc"):
                    rows = []
                    X = MEAS[m]
                    for (i, t), x in X.items():
                        if (i, t + 10) not in X or (i, t) not in TFR:
                            continue
                        if "income" in controls and (i, t) not in INC:
                            continue
                        if "urban" in controls and (i, t) not in URB:
                            continue
                        rows.append((i, t, TFR[(i, t)], X[(i, t + 10)] if False else x,
                                     INC.get((i, t)), URB.get((i, t)),
                                     REGION.get(i, ""), (t // 10) * 10))
                    # replace x by future schooling
                    rows = [(i, t, y, X[(i, t + 10)], inc, urb, reg, dec)
                            for (i, t, y, _, inc, urb, reg, dec) in rows
                            if (i, t + 10) in X]
                    if len(rows) < 100:
                        continue
                    iso = [r[0] for r in rows]
                    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
                    cl = np.array([ui[v] for v in iso])
                    x = np.array([r[3] for r in rows], float)
                    yv = np.array([r[2] for r in rows], float)
                    cols = [np.log(np.maximum(x, 0) + 1) if form == "log" else x]
                    if "income" in controls:
                        cols.append(np.array([r[4] for r in rows], float))
                    if "urban" in controls:
                        cols.append(np.array([r[5] for r in rows], float))
                    cols += dummies([r[7] for r in rows])
                    if fe == "decade_region":
                        cols += dummies([r[6] for r in rows])
                    b, se = fit(yv, cols, cl)
                    placebo_future.append(dict(b=float(b[1]), se=se, n=len(rows),
                                               measure=m, form=form, fe=fe))
    RES["placebo_future"] = summarize(placebo_future, "future schooling -> current fertility")
    # (b) schooling -> backward ten-year change in fertility
    placebo_back = []
    for controls in (("income", "urban"), ("income",)):
        for trends in (False, True):
            for m in ("mys_female", "mys_total", "lsc"):
                r = spec_change(m, controls=controls, trends=trends, backwards=True)
                if r:
                    placebo_back.append(dict(b=r["b"], se=r["se"], n=r["n"]))
    RES["placebo_backward"] = summarize(placebo_back, "schooling -> backward fertility change")

    print("\n=== income as rival predictor, separately and jointly ===")
    joint = {}
    for m in ("mys_female", "mys_total"):
        rows = level_rows(m, 0)
        iso = [r[0] for r in rows]
        ui = {v: n for n, v in enumerate(sorted(set(iso)))}
        cl = np.array([ui[v] for v in iso])
        x = np.array([r[3] for r in rows], float)
        inc = np.array([r[4] for r in rows], float)
        urb = np.array([r[5] for r in rows], float)
        yv = np.array([r[2] for r in rows], float)
        cols = [x, inc, urb] + dummies([r[7] for r in rows]) + dummies([r[6] for r in rows])
        X = np.column_stack([np.ones(len(yv))] + cols)
        XtX = X.T @ X
        b = np.linalg.lstsq(XtX, X.T @ yv, rcond=None)[0]
        u = yv - X @ b
        meat = np.zeros_like(XtX)
        for c in np.unique(cl):
            msk = cl == c
            s = X[msk].T @ u[msk]
            meat += np.outer(s, s)
        Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
        se = np.sqrt(np.maximum(np.diag(Vb), 0))
        joint[m] = dict(schooling=dict(b=float(b[1]), se=float(se[1])),
                        log_income=dict(b=float(b[2]), se=float(se[2])),
                        n=len(rows), nc=len(ui))
        print(f"  {m}: schooling {b[1]:+.4f} (se {se[1]:.4f}); log income "
              f"{b[2]:+.4f} (se {se[2]:.4f}); n={len(rows)}")
    RES["joint_income"] = joint

    # ---- figures ----
    lvc = json.load(open(os.path.join(OUT, "results_part1.json")))["levels_vs_changes"]
    PLAIN = {"mys_female": "women's mean years", "mys_total": "total mean years",
             "sec": "secondary enrolment", "lsc": "lower-secondary completion",
             "prm_cmp": "primary completion", "ter": "tertiary enrolment",
             "gpi_sec": "parity index, secondary", "gpi_ter": "parity index, tertiary",
             "gpi_adj": "parity index (25+)"}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    groups = [("mys_female", "mys_total", "lsc", "sec", "prm_cmp", "ter"),
              ("gpi_sec", "gpi_ter", "gpi_adj")]
    for ax, ms in zip(axes, groups):
        ys, names, lev, chg = [], [], [], []
        for m in ms:
            L = lvc[m]["level_decade_region"]
            C = lvc[m]["change_trends"]
            if not L or not C:
                continue
            ys.append(len(names)); names.append(PLAIN.get(m, m))
            lev.append((L["b"], 1.96 * L["se"]))
            chg.append((C["b"], 1.96 * C["se"]))
        y = np.arange(len(names))
        ax.errorbar([v[0] for v in lev], y + 0.12, xerr=[v[1] for v in lev],
                    fmt="o", color="#1f77b4", label="levels (decade+region FE)", capsize=3)
        ax.errorbar([v[0] for v in chg], y - 0.12, xerr=[v[1] for v in chg],
                    fmt="s", color="#d62728", label="decade changes (country FE+trends)", capsize=3)
        ax.axvline(0, color="k", lw=0.8)
        ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8)
        ax.set_xlabel("coefficient on fertility")
        ax.legend(fontsize=7, frameon=False, loc="best")
    axes[0].set_title("Attainment and completion measures")
    axes[1].set_title("Gender parity indices")
    fig.suptitle("Schooling -> fertility: levels (blue) vs decade changes (red), 95% CI", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_levels_vs_changes.png"), dpi=170)
    plt.close(fig)

    ss = sorted([s for s in specs if s["setting"] == "period"], key=lambda s: s["b"])
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    for j, s in enumerate(ss):
        t = tstat(s["b"], s["se"])
        color = "#d62728" if (s["b"] < 0 and t < -1.96) else ("#1f77b4" if s["b"] < 0 else "0.55")
        ax.plot([s["b"] - 1.96 * s["se"], s["b"] + 1.96 * s["se"]], [j, j], color=color, lw=0.6)
        ax.plot([s["b"]], [j], "o", color=color, ms=2)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("schooling coefficient on period fertility (per unit of measure)")
    ax.set_ylabel("specification (sorted by coefficient)")
    ax.set_title(f"Specification curve, {len(ss)} period-TFR specs: "
                 f"{RES['spec_curve']['period']['share_negative']:.0%} negative, "
                 f"{RES['spec_curve']['period']['share_negative_significant']:.0%} negative-significant")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_spec_curve.png"), dpi=170)
    plt.close(fig)

    json.dump(RES, open(os.path.join(OUT, "results_part2.json"), "w"), indent=1, default=float)
    print("\nwrote", os.path.join(OUT, "results_part2.json"))
