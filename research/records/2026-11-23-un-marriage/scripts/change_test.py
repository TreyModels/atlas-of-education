#!/usr/bin/env python3
"""Kill-or-explain test for the positive "later female marriage age -> smaller
future fertility fall" coefficient.

Three tests:
  A. First difference on both sides: change in births per woman over a real
     survey window 8-13 years long regressed on the change in women's mean age
     at marriage over the SAME window (decade effects; country effects where a
     country contributes more than one window).  If the positive level effect
     were a genuine timing effect, this should be positive too.
  B. Level estimator where the predictor is the CHANGE in marriage age over the
     previous 8-13 years (does past marriage-age change predict future fertility
     change once country trends are in?).
  C. The level estimator with an added straight-line trend for each region on top
     of the country trends, to absorb common development paths.
  D. Raw level pattern: pooled cross-country correlation and a decade-FE
     cross-section regression of fertility on marriage age.
"""
import json
import numpy as np
from edge_marriage import S, build_rows, fit, dm, CTRL

meta = json.load(open("/root/work/data/meta.json"))
REG = {i: (m.get("region") or "").strip() for i, m in meta.items()}
EDGES = ["smam_f", "smam_gap", "nevermar_f_4549"]


# ---------- A. first difference on both sides ----------
def windows(name):
    byc = {}
    for (i, t), v in S[name].items():
        byc.setdefault(i, []).append((t, v))
    out = []
    for i, lst in byc.items():
        lst.sort()
        for k, (t1, v1) in enumerate(lst):
            cand = [(abs(t2 - t1 - 10), t2, v2) for t2, v2 in lst[k + 1:]
                    if 8 <= t2 - t1 <= 13]
            if cand:
                _, t2, v2 = min(cand)
                out.append([i, t1, t2, v2 - v1])
    return out


def fit_delta(xname, yname="fertility", country_fe=False):
    rows = []
    X = S[xname]
    for i, t1, t2, dx in windows(xname):
        if (i, t1) not in S[yname] or (i, t2) not in S[yname]:
            continue
        rows.append([i, t1, S[yname][(i, t2)] - S[yname][(i, t1)], dx])
    if len(rows) < 150:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    Y = np.array([r[2] for r in rows], float)
    D = np.array([r[3] for r in rows], float)
    cols = [D]
    if country_fe:
        # one column per country except the first (all rows of a country have
        # the same country dummy; with decade demeaning this is identified)
        for j in range(1, len(ui)):
            cols.append((gi == j).astype(float))
    Xm = np.column_stack([np.ones(len(Y))] + cols)
    Xm = np.column_stack([dm(Xm[:, k], gy) for k in range(Xm.shape[1])])
    Ym = dm(Y, gy)
    b = np.linalg.lstsq(Xm.T @ Xm, Xm.T @ Ym, rcond=None)[0]
    u = Ym - Xm @ b
    XtX = Xm.T @ Xm
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = Xm[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return dict(b=float(b[1]), se=float(np.sqrt(max(Vb[1, 1], 0))),
                n=len(Y), nc=len(ui))


# ---------- C. country trends + region trends ----------
def fit_region_trends(xname, yname="fertility"):
    rows = build_rows(xname, yname, "grid10")
    cnt = {}
    for r in rows:
        cnt[r[0]] = cnt.get(r[0], 0) + 1
    rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    regs = sorted({REG.get(i, "") for i in iso})
    ri = np.array([regs.index(REG.get(i, "")) for i in iso])
    yv = np.array([r[2] for r in rows], float)
    cols = [np.array([r[4] for r in rows], float),
            np.array([r[3] for r in rows], float),
            np.array([r[5] for r in rows], float),
            np.array([r[6] for r in rows], float)]
    for j in range(len(ui)):
        cols.append(((gi == j) * yr).astype(float))
    for j in range(len(regs)):
        cols.append(((ri == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(yv, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return dict(b=float(b[1]), se=float(np.sqrt(max(Vb[1, 1], 0))),
                n=len(yv), nc=len(ui))


# ---------- D. raw level pattern ----------
def raw_level():
    keys = sorted(set(S["smam_f"]) & set(S["fertility"]))
    X = np.array([S["smam_f"][k] for k in keys])
    Y = np.array([S["fertility"][k] for k in keys])
    gy = np.array([(k[1] // 10) * 10 for k in keys])
    # cross-section, decade fixed effects
    cols = [np.ones(len(Y)), X]
    for d in sorted(set(gy))[1:]:
        cols.append((gy == d).astype(float))
    Xm = np.column_stack(cols)
    b = np.linalg.lstsq(Xm.T @ Xm, Xm.T @ Y, rcond=None)[0]
    u = Y - Xm @ b
    XtX = Xm.T @ Xm
    Vb = np.linalg.pinv(XtX) @ (Xm.T @ (Xm * (u ** 2)[:, None]) / len(Y)) @ np.linalg.pinv(XtX)
    # decade means
    means = {}
    for d in sorted(set(gy)):
        m = gy == d
        means[int(d)] = (float(X[m].mean()), float(Y[m].mean()), int(m.sum()))
    return dict(pooled_corr=float(np.corrcoef(X, Y)[0, 1]),
                decade_fe_b=float(b[1]), decade_fe_se=float(np.sqrt(max(Vb[1, 1], 0))),
                n=len(Y), decade_means=means)


if __name__ == "__main__":
    out = {}
    for x in EDGES:
        out[f"delta_{x}"] = fit_delta(x, country_fe=False)
        out[f"delta_{x}_country_fe"] = fit_delta(x, country_fe=True)
        out[f"region_trends_{x}"] = fit_region_trends(x)
    out["raw_level"] = raw_level()
    json.dump(out, open("/root/work/undata/results_change_test.json", "w"), indent=1)
    for k, v in out.items():
        if k == "raw_level":
            print(f"{k}: pooled corr={v['pooled_corr']:+.3f}; decade-FE slope "
                  f"{v['decade_fe_b']:+.4f} (se {v['decade_fe_se']:.4f}), n={v['n']}")
            for d, (mx, my, n) in v["decade_means"].items():
                print(f"    {d}s: mean marriage age {mx:.1f} yrs, mean births per woman {my:.2f} (n={n})")
        elif v:
            print(f"{k:34s} b={v['b']:+.4f} se={v['se']:.4f} n={v['n']} countries={v['nc']}")
        else:
            print(f"{k}: not estimable")
