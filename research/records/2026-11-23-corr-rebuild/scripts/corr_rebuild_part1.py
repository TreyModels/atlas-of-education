#!/usr/bin/env python3
"""Task 15: rebuild the schooling-fertility correlation at the right level.

Pre-registered in research/records/2026-11-23-corr-rebuild/PRE_REGISTRATION.md
(commit c077672, written before any code). This script implements exactly that
design: levels vs decade changes, transportability of the level relation,
cohort/lagged female attainment with thresholds, and the specification curve.

Data (all annual country-year; no interpolation):
  /root/work/data : fertility (TFR), lower-secondary completion, secondary
                    enrolment, tertiary enrolment, primary completion, gender
                    parity indices, income (LEGISLATED check: file holds levels,
                    natural log taken here), urbanisation, meta.json (regions)
  /root/work/corr_rebuild/raw : OWID mean years of schooling (total, 1870-2020),
                    mean years of schooling by sex (1990-2023), adjusted gender
                    parity index (25+, 1970-2024), cohort fertility (33 countries)
  /root/work/transition/raw/mean-years-of-schooling.csv (copied in)
"""
import csv, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = "/root/work/data"
RAW = "/root/work/corr_rebuild/raw"
OUT = "/root/work/corr_rebuild/out"
FIG = "/root/work/corr_rebuild/figures"
os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)

META = json.load(open(os.path.join(DATA, "meta.json")))
REGION = {i: (m.get("region") or "").strip() for i, m in META.items()}
INCOME = {i: (m.get("income") or "").strip() for i, m in META.items()}
PANEL = {i for i in REGION if len(i) == 3 and REGION[i] != "Aggregates"}


def load_json(name):
    d = {(r[0], int(r[1])): float(r[2]) for r in
         json.load(open(os.path.join(DATA, name + ".json"))) if r[2] is not None}
    return {k: v for k, v in d.items() if k[0] in PANEL}


def load_csv(path, value_col=None):
    rows = list(csv.DictReader(open(path)))
    cols = [c for c in rows[0] if c not in ("entity", "code", "year")]
    c = value_col or cols[0]
    d = {}
    for r in rows:
        try:
            iso, y, v = r["code"], int(float(r["year"])), r[c]
            if iso and len(iso) == 3 and iso in PANEL and v not in (None, ""):
                d[(iso, y)] = float(v)
        except (TypeError, ValueError, KeyError):
            pass
    return d


TFR = load_json("fertility")
INC = {k: float(np.log(max(v, 1.0))) for k, v in load_json("gdppc_log").items()}
URB = load_json("urban")
MEAS = {"prm_cmp": load_json("prm_cmp"), "sec": load_json("sec"),
        "lsc": load_json("lsc"), "ter": load_json("ter"),
        "gpi_sec": load_json("gpi_sec"), "gpi_ter": load_json("gpi_ter")}
MYS_TOT = load_csv(os.path.join(RAW, "mean-years-of-schooling.csv"))
MYS_F = load_csv(os.path.join(RAW, "average-years-of-schooling-males-vs-females.csv"), "mys__sex_female")
MYS_M = load_csv(os.path.join(RAW, "average-years-of-schooling-males-vs-females.csv"), "mys__sex_male")
GPI_ADJ = load_csv(os.path.join(RAW, "gender-ratios-for-mean-years-of-schooling.csv"))
COHORT = load_csv(os.path.join(RAW, "cohort-fertility-rate.csv"), "ccf__birth_order_total")
MEAS.update({"mys_total": MYS_TOT, "mys_female": MYS_F, "mys_male": MYS_M, "gpi_adj": GPI_ADJ})

ATTAIN = {"mys_total", "mys_female", "mys_male", "gpi_adj"}   # years-scale measures
NAMES = {"prm_cmp": "primary completion (%)", "sec": "secondary enrolment (%)",
         "lsc": "lower-secondary completion (%)", "ter": "tertiary enrolment (%)",
         "gpi_sec": "gender parity index, secondary", "gpi_ter": "gender parity index, tertiary",
         "mys_total": "mean years of schooling, total", "mys_female": "mean years of schooling, women",
         "mys_male": "mean years of schooling, men", "gpi_adj": "adjusted gender parity index (25+)"}


def fit(yv, cols, clusters):
    """OLS with country-clustered SEs. cols = list of arrays; first is the regressor."""
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


def dummies(values, drop_first=True):
    vals = sorted(set(values))
    cols = []
    for v in vals[1 if drop_first else 0:]:
        cols.append(np.array([1.0 if x == v else 0.0 for x in values]))
    return cols


def level_spec(measure, fe="decade_region", controls=("income", "urban"), lo=1870, hi=2024):
    X_, Y_ = MEAS[measure], TFR
    rows = []
    for (i, t), x in X_.items():
        if t < lo or t > hi or (i, t) not in Y_:
            continue
        if "income" in controls and (i, t) not in INC:
            continue
        if "urban" in controls and (i, t) not in URB:
            continue
        rows.append((i, t, Y_[(i, t)], x,
                     INC.get((i, t)), URB.get((i, t)), REGION.get(i, ""), (t // 10) * 10))
    if len(rows) < 60 or len({r[0] for r in rows}) < 10:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    cl = np.array([ui[v] for v in iso])
    xv = np.array([r[3] for r in rows], float)
    cols = [xv]
    if "income" in controls:
        cols.append(np.array([r[4] for r in rows], float))
    if "urban" in controls:
        cols.append(np.array([r[5] for r in rows], float))
    if fe in ("decade", "decade_region"):
        cols += dummies([r[7] for r in rows])
    if fe == "decade_region":
        cols += dummies([r[6] for r in rows])
    b, se = fit(np.array([r[2] for r in rows], float), cols, cl)
    return dict(b=float(b[1]), se=se, n=len(rows), nc=len(ui))


def change_rows(measure, trends=True, controls=("income", "urban"), lo=1870, hi=2014):
    """Ten-year change in TFR on the starting level of the measure (the matrix)."""
    X_ = MEAS[measure]
    rows = []
    for (i, t), x in X_.items():
        if (i, t) not in TFR or (i, t + 10) not in TFR:
            continue
        if "income" in controls and (i, t) not in INC:
            continue
        if "urban" in controls and (i, t) not in URB:
            continue
        rows.append((i, t, TFR[(i, t + 10)] - TFR[(i, t)], x,
                     INC.get((i, t)), URB.get((i, t))))
    return rows


def change_spec(measure, trends=True, controls=("income", "urban")):
    rows = change_rows(measure, controls=controls)
    if not rows:
        return None
    cnt = {}
    for r in rows:
        cnt[r[0]] = cnt.get(r[0], 0) + 1
    rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 100 or len({r[0] for r in rows}) < 10:
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
    cols = [np.array([r[3] for r in rows], float),
            np.array([r[4] for r in rows], float),
            np.array([r[5] for r in rows], float)]
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
    meat = np.zeros((XtX.shape[0], XtX.shape[0]))
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return dict(b=float(b[1]), se=float(np.sqrt(max(Vb[1, 1], 0))),
                n=len(yv), nc=len(ui))


if __name__ == "__main__":
    RES = {}
    print("=== Analysis 1: levels vs changes, all schooling measures ===")
    RES["levels_vs_changes"] = {}
    for m in MEAS:
        L = level_spec(m, fe="decade_region")
        L0 = level_spec(m, fe="decade")
        C = change_spec(m, trends=False)
        C2 = change_spec(m, trends=True)
        RES["levels_vs_changes"][m] = dict(level_decade_region=L, level_decade=L0,
                                           change_fe=C, change_trends=C2)
        for tag, r in (("LEVEL(dec+reg)", L), ("LEVEL(dec)", L0),
                       ("CHANGE(FE)", C), ("CHANGE(trends)", C2)):
            if r:
                print(f"  {m:10s} {tag:15s} b={r['b']:+.4f} se={r['se']:.4f} "
                      f"t={r['b']/r['se']:+.2f} n={r['n']} countries={r['nc']}")
            else:
                print(f"  {m:10s} {tag:15s} not estimable")

    print("\n=== rival predictor: income in the same level specs ===")
    RES["income_rival"] = {}
    # income as the regressor in the level spec
    def level_spec_income(fe="decade_region"):
        rows = []
        for (i, t), y in TFR.items():
            if (i, t) not in INC or (i, t) not in URB:
                continue
            rows.append((i, t, y, INC[(i, t)], URB[(i, t)], REGION.get(i, ""), (t // 10) * 10))
        rows = rows[:]
        iso = [r[0] for r in rows]
        ui = {v: n for n, v in enumerate(sorted(set(iso)))}
        cl = np.array([ui[v] for v in iso])
        cols = [np.array([r[3] for r in rows], float), np.array([r[4] for r in rows], float)]
        cols += dummies([r[6] for r in rows]) + dummies([r[5] for r in rows])
        b, se = fit(np.array([r[2] for r in rows], float), cols, cl)
        return dict(b=float(b[1]), se=se, n=len(rows), nc=len(ui))
    inc_res = level_spec_income()
    RES["income_rival"]["income_level"] = inc_res
    print(f"  log income -> fertility level: b={inc_res['b']:+.4f} se={inc_res['se']:.4f} "
          f"n={inc_res['n']} countries={inc_res['nc']}")

    print("\n=== Analysis 3: lags, female vs total attainment, thresholds ===")
    RES["lags"] = {}
    for m in ["mys_female", "mys_total", "mys_male", "sec", "lsc", "prm_cmp", "gpi_ter", "gpi_adj"]:
        RES["lags"][m] = {}
        for lag in (0, 10, 15, 20, 25):
            # y = fertility at t+lag, x = measure at t (level spec, decade+region FE)
            Xm = MEAS[m]
            rows = []
            for (i, t), x in Xm.items():
                if (i, t + lag) not in TFR or (i, t) not in INC or (i, t) not in URB:
                    continue
                rows.append((i, t, TFR[(i, t + lag)], x, INC[(i, t)], URB[(i, t)],
                             REGION.get(i, ""), (t // 10) * 10))
            if len(rows) < 60 or len({r[0] for r in rows}) < 10:
                RES["lags"][m][lag] = None
                continue
            iso = [r[0] for r in rows]
            ui = {v: n for n, v in enumerate(sorted(set(iso)))}
            cl = np.array([ui[v] for v in iso])
            cols = [np.array([r[3] for r in rows], float),
                    np.array([r[4] for r in rows], float),
                    np.array([r[5] for r in rows], float)]
            cols += dummies([r[7] for r in rows]) + dummies([r[6] for r in rows])
            b, se = fit(np.array([r[2] for r in rows], float), cols, cl)
            RES["lags"][m][lag] = dict(b=float(b[1]), se=se, n=len(rows), nc=len(ui))
        print("  " + m + ": " + "  ".join(
            f"lag{lag}={v['b']:+.3f}" if v else f"lag{lag}=n/a"
            for lag, v in RES["lags"][m].items()))

    # threshold / spline around 6 and 9 years of schooling, female and total
    print("\n=== threshold/spline (knots 6 and 9 years) ===")
    RES["threshold"] = {}
    for m in ["mys_female", "mys_total"]:
        rows = []
        for (i, t), x in MEAS[m].items():
            if (i, t) not in TFR or (i, t) not in INC or (i, t) not in URB:
                continue
            rows.append((i, t, TFR[(i, t)], x))
            # spline hinges computed below
        if len(rows) < 60:
            continue
        iso = [r[0] for r in rows]
        ui = {v: n for n, v in enumerate(sorted(set(iso)))}
        cl = np.array([ui[v] for v in iso])
        x = np.array([r[3] for r in rows], float)
        hinges = [np.minimum(x, 6.0), np.clip(x - 6.0, 0, 3.0), np.maximum(x - 9.0, 0)]
        cols = hinges + [np.array([INC[(r[0], r[1])] for r in rows], float),
                         np.array([URB[(r[0], r[1])] for r in rows], float)]
        cols += dummies([REGION.get(r[0], "") for r in rows]) + \
            dummies([(r[1] // 10) * 10 for r in rows])
        # three slope coefficients; report each with its own clustered se
        X = np.column_stack([np.ones(len(rows))] + cols)
        XtX = X.T @ X
        yv = np.array([r[2] for r in rows], float)
        b = np.linalg.lstsq(XtX, X.T @ yv, rcond=None)[0]
        u = yv - X @ b
        meat = np.zeros_like(XtX)
        for c in np.unique(cl):
            msk = cl == c
            s = X[msk].T @ u[msk]
            meat += np.outer(s, s)
        Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
        ses = np.sqrt(np.maximum(np.diag(Vb)[1:4], 0))
        RES["threshold"][m] = dict(slope_below6=dict(b=float(b[1]), se=float(ses[0])),
                                   slope_6_9=dict(b=float(b[2]), se=float(ses[1])),
                                   slope_above9=dict(b=float(b[3]), se=float(ses[2])),
                                   n=len(rows), nc=len(ui))
        print(f"  {m}: slope<6y {b[1]:+.3f} (se {ses[0]:.3f}); 6-9y {b[2]:+.3f} "
              f"(se {ses[1]:.3f}); >9y {b[3]:+.3f} (se {ses[2]:.3f}); n={len(rows)}")

    # cohort fertility with total attainment measured when the cohort is 25
    print("\n=== cohort fertility vs attainment measured at cohort age 25 ===")
    RES["cohort"] = {}
    for m in ["mys_total", "mys_female"]:
        rows = []
        for (i, cohort), cf in COHORT.items():
            x = MEAS[m].get((i, cohort + 25))
            if x is None:
                x = MEAS[m].get((i, cohort + 20))
            if x is None:
                continue
            rows.append((i, cohort, cf, x))
        if len(rows) < 40 or len({r[0] for r in rows}) < 8:
            RES["cohort"][m] = None
            continue
        iso = [r[0] for r in rows]
        ui = {v: n for n, v in enumerate(sorted(set(iso)))}
        cl = np.array([ui[v] for v in iso])
        cols = [np.array([r[3] for r in rows], float)] + \
            dummies([(r[1] // 10) * 10 for r in rows])
        b, se = fit(np.array([r[2] for r in rows], float), cols, cl)
        RES["cohort"][m] = dict(b=float(b[1]), se=se, n=len(rows), nc=len(ui))
        print(f"  {m}: b={b[1]:+.4f} se={se:.4f} n={len(rows)} countries={len(ui)}")

    json.dump(RES, open(os.path.join(OUT, "results_part1.json"), "w"), indent=1, default=float)
    print("\nwrote", os.path.join(OUT, "results_part1.json"))
