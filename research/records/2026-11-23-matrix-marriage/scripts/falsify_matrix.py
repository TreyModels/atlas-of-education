#!/usr/bin/env python3
"""Falsifiers for the 20-measure matrix.

(a) circular-shift permutation within country (the only permutation used here;
    the year-shuffle is anti-conservative and is NOT used) for the marriage-
    involving links that look interesting (|t|>1.96 with country trends, plus the
    three marriage -> fertility links always);
(b) drop the UN model-based "Estimate" rows and recompute every marriage-
    involving link at both trend settings;
(c) change-on-change version for any marriage -> fertility link that looks
    interesting: change in births per woman over a real 8-13-year survey window
    on the change in the marriage measure over the same window, country
    effects + decade effects + clustered errors.

Income is logged in the shared loader (edge_marriage.py), per the session rule.
Writes out/falsify_matrix.json.
"""
import csv, json, os
import numpy as np
from edge_marriage import S, build_rows, fit

# Session rule: the income file holds GDP per head in LEVELS despite its name.
# Log it at load, before any fit, so every link uses a logged income control.
S["gdppc_log"] = {k: float(np.log(max(v, 1.0))) for k, v in S["gdppc_log"].items()}

RNG = np.random.default_rng(20261125)
MARRIAGE = ["smam_f", "nevermar_f_4549", "smam_gap"]
PANEL17 = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp",
           "gdppc_log", "urban", "tax", "agri_va", "emp_agri", "flfp",
           "life_exp", "u5mr", "gpi_sec", "gpi_ter", "fertility"]
M = json.load(open("out/matrix20.json"))
NPERM = 60


def circ_shift(name):
    byc = {}
    for (i, t), v in S[name].items():
        byc.setdefault(i, []).append((t, v))
    out = {}
    for i, lst in sorted(byc.items()):
        lst.sort()
        vals = [v for _, v in lst]
        if len(vals) > 1:
            k = int(RNG.integers(1, len(vals)))
            vals = list(np.roll(np.array(vals), k))
        for (t, _), v in zip(lst, vals):
            out[(i, t)] = float(v)
    return out


def perm_test(x, y, nperm=NPERM):
    mode = "survey10" if y in MARRIAGE else "grid10"
    base = fit(build_rows(x, y, mode), True, x, y)
    if base is None or base["se"] == 0:
        return None
    target = y if y in MARRIAGE else x
    obs = abs(base["b"])
    null = []
    for _ in range(nperm):
        old = S[target]
        S[target] = circ_shift(target)
        try:
            r = fit(build_rows(x, y, mode), True, x, y)
        finally:
            S[target] = old
        if r is not None:
            null.append(abs(r["b"]))
    null = np.array(null)
    return dict(b=base["b"], se=base["se"], p_circ=float((null >= obs).mean()),
                null_q95=float(np.percentile(null, 95)), draws=len(null),
                target_shifted=target)


# ---------------- (b) drop UN model-based rows ------------------------------
def census_survey_series():
    """Return {name: {(iso3, year): value}} keeping only non-Estimate rows."""
    import extract_un as X
    not_est = lambda p: bool(str(p or "").strip()) and "estimat" not in str(p).lower()

    def iso(code):
        try:
            return X.NUM2ISO.get(int(float(code)))
        except (TypeError, ValueError):
            return None

    out = {k: {} for k in MARRIAGE}
    fem, male = {}, {}
    for idx, r in X.rows_from((X.WMD, "SMAM"), 3):
        if not r or not r[idx["Country or area"]]:
            continue
        i, sex = iso(r[idx["ISO code"]]), str(r[idx["Sex"]]).strip()
        v, proc = X.num(r[idx["DataValue"]]), r[idx["DataProcess"]]
        yr = X.midyear(r[idx["YearStart"]], r[idx["YearEnd"]])
        if i is None or v is None or yr is None or not not_est(proc):
            continue
        if sex in ("Women", "Female"):
            fem.setdefault((i, yr), v)
            out["smam_f"].setdefault((i, yr), v)
        elif sex in ("Men", "Male"):
            male.setdefault((i, yr), v)
    for k in fem:
        if k in male:
            out["smam_gap"][k] = fem[k] - male[k]
    for idx, r in X.rows_from((X.WMD, "EVER_MARRIED"), 3):
        if not r or not r[idx["Country or area"]]:
            continue
        if str(r[idx["AgeGroup"]]).strip() != "[45-49]":
            continue
        if str(r[idx["Sex"]]).strip() not in ("Women", "Female"):
            continue
        i = iso(r[idx["ISO code"]])
        e, proc = X.num(r[idx["DataValue"]]), r[idx["DataProcess"]]
        yr = X.midyear(r[idx["YearStart"]], r[idx["YearEnd"]])
        if i is None or e is None or yr is None or not not_est(proc):
            continue
        out["nevermar_f_4549"].setdefault((i, yr), 100.0 - e)
    return out


def drop_model_rows():
    filt = census_survey_series()
    res = {}
    old = {k: S[k] for k in MARRIAGE}
    try:
        for k in MARRIAGE:
            S[k] = dict(filt[k])
        for x in PANEL17 + MARRIAGE:
            for y in MARRIAGE:
                if x == y:
                    continue
                key = f"{x}->{y}"
                for setting, trend in (("fe", False), ("trend", True)):
                    r = fit(build_rows(x, y, "survey10"), trend, x, y)
                    full = M[key][setting]
                    res.setdefault(key, {})[setting] = dict(
                        full_b=full["b"] if full else None,
                        full_se=full["se"] if full else None,
                        filt_b=r["b"] if r else None,
                        filt_se=r["se"] if r else None,
                        filt_n=r["n"] if r else None,
                        filt_nc=r["nc"] if r else None,
                        same_sign=(None if (full is None or r is None)
                                   else bool(np.sign(full["b"]) == np.sign(r["b"]))),
                        still_sig=(None if (full is None or r is None) else
                                   bool(abs(r["b"] / r["se"]) > 1.96)))
    finally:
        for k, v in old.items():
            S[k] = v
    return res


# ---------------- (c) change-on-change --------------------------------------
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
                out.append((i, t1, t2, v2 - v1))
    return out


def change_on_change(xname, yname="fertility", country_fe=True):
    rows = []
    for i, t1, t2, dx in windows(xname):
        if (i, t1) not in S[yname] or (i, t2) not in S[yname]:
            continue
        rows.append([i, t1, S[yname][(i, t2)] - S[yname][(i, t1)], dx])
    if len(rows) < 100:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    gy = np.array([(r[1] // 10) * 10 for r in rows])
    Y = np.array([r[2] for r in rows], float)
    D = np.array([r[3] for r in rows], float)

    def dm(a, g):
        s = np.bincount(g, weights=a)
        c = np.bincount(g)
        return a - (s / np.maximum(c, 1))[g]
    cols = [D]
    if country_fe:
        for j in range(1, len(ui)):
            cols.append((gi == j).astype(float))
    X = np.column_stack([np.ones(len(Y))] + cols)
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Ym = dm(Y, gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Ym, rcond=None)[0]
    u = Ym - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return dict(b=float(b[1]), se=float(np.sqrt(max(Vb[1, 1], 0))),
                n=len(Y), nc=len(ui), country_fe=country_fe)


if __name__ == "__main__":
    out = {}

    # (a) permutation on interesting marriage links
    interesting = []
    for k, v in M.items():
        if not v["involves_marriage"]:
            continue
        tr = v["trend"]
        if tr is None:
            continue
        if abs(tr["t"]) > 1.96 or tr.get("q", 1) is not None and tr.get("q", 1) < 0.05:
            interesting.append((abs(tr["t"]), k))
    for x, y in [("smam_f", "fertility"), ("nevermar_f_4549", "fertility"),
                 ("smam_gap", "fertility")]:
        k = f"{x}->{y}"
        if k in M and M[k]["trend"] is not None and k not in [i[1] for i in interesting]:
            interesting.append((abs(M[k]["trend"]["t"]), k))
    interesting = sorted(interesting, reverse=True)[:15]
    print(f"interesting marriage links for permutation: {len(interesting)}", flush=True)
    perm = {}
    for _, k in interesting:
        x, y = k.split("->")
        r = perm_test(x, y)
        perm[k] = r
        if r:
            print(f"  {k:28s} b={r['b']:+.4f} se={r['se']:.4f} circ p={r['p_circ']:.3f} "
                  f"(null q95={r['null_q95']:.4f}, {r['draws']} draws)", flush=True)
    out["permutation"] = perm

    # (b) drop model rows
    print("\nrunning drop-model-rows ...", flush=True)
    out["drop_model_rows"] = drop_model_rows()
    changed = [k for k, v in out["drop_model_rows"].items()
               if v["trend"]["same_sign"] is False]
    print(f"  marriage links whose trend-setting sign flips without UN estimates: "
          f"{len(changed)} of {len(out['drop_model_rows'])}")

    # (c) change-on-change for marriage -> fertility
    print("\nrunning change-on-change ...", flush=True)
    cc = {}
    for xname in MARRIAGE:
        for fe in (True, False):
            r = change_on_change(xname, "fertility", country_fe=fe)
            cc[f"{xname}->fertility|country_fe={fe}"] = r
            if r:
                print(f"  {xname:16s} -> fertility (country_fe={fe}): "
                      f"b={r['b']:+.4f} se={r['se']:.4f} n={r['n']} countries={r['nc']}",
                      flush=True)
    out["change_on_change"] = cc

    json.dump(out, open("out/falsify_matrix.json", "w"), indent=1)
    print("\nwrote out/falsify_matrix.json")
