#!/usr/bin/env python3
"""
WT1-WT5 predeclared test battery (brief 019, D98-D101, D89 standing order).

Deterministic. No RNG, no bootstrap (seed = null). Reads on-disk data only; writes only
RESULTS.csv / DETAIL.csv / run_info.json into the directory given by --outdir.

Thresholds, falsifiers, qualifying rules and verdict words are FROZEN in PRE_DECLARATIONS.md
(sha256 recorded in RUN_MANIFEST.json) and are implemented here verbatim. Mechanical readings
M1-M16 of that file are cited by id in comments.

Verdict vocabulary (closed): SUPPORTED | NOT SUPPORTED | DATA LIMITED | DESIGN-ONLY | HELD.
A WT PASS is a descriptive footprint, NOT validation of the paper.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------
# paths
# ----------------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
WTDIR = HERE.parent
ROOT = WTDIR.parents[2]          # .../massification-2026-11-20

IN_PANEL = ROOT / "09_relations/data/panel_wdi_long.csv"
IN_UNIV = ROOT / "10_massification/data/UNIVERSALIZATION_SERIES.csv"
IN_ECI = ROOT / "09_relations/data/economic_complexity_panel_30ctys.csv"
IN_SHADOW_GRAD = ROOT / "09_relations/data/shadow_gradients.csv"
IN_SHADOW_TARGETS = ROOT / "04_data/TARGETS_SHADOW.csv"

INPUTS = [IN_PANEL, IN_UNIV, IN_ECI, IN_SHADOW_GRAD, IN_SHADOW_TARGETS]

# frozen parameters (M4, M5, M6, M8, M9, M12, M13)
MIN_OBS = 15
RUN_MIN_LEN = 2
RUN_MIN_DEPTH = 3.0
WT1_RATIO_MAX = 0.50
WT2_WINDOW = (1995, 2024)
WT2_DECOUPLED_SHARE = 0.50
WT2_REVERSAL_SHARE_MAX = 1.0 / 3.0
WT3_WINDOW = (1995, 2024)
WT3_MIN_COUNTRIES = 5
WT3_RHO_MIN = 0.40
WT4_US_PEAK = 76.432953          # PHL upper-secondary completion peak, 2017 (on disk)
WT4_US_PEAK_YEAR = 2017
WT4_DROP = 5.0
WT4_RECOVER = 2.0
WT4_RUN_YEARS = 3
WT4_TER_ANCHOR = 38.344741       # PHL tertiary GER 2016 (on disk)
WT4_TER_RECOVER_LEVEL = 50.0
WT4_TER_RECOVER_YEAR = 2025

VERDICTS = ("SUPPORTED", "NOT SUPPORTED", "DATA LIMITED", "DESIGN-ONLY", "HELD")


# ----------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------
def f6(x) -> str:
    """fixed 6-dp formatting for determinism; empty for missing."""
    if x is None:
        return ""
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return ""
    return f"{float(x):.6f}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def series(df: pd.DataFrame, iso3: str, indicator: str):
    s = df[(df.iso3 == iso3) & (df.indicator == indicator)][["year", "value"]].dropna()
    s = s.sort_values("year", kind="mergesort")
    return s.year.to_numpy(dtype=int), s.value.to_numpy(dtype=float)


def rank_avg(x) -> np.ndarray:
    """average ranks, deterministic (mergesort + tie blocks)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(n, dtype=float)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and x[order[j + 1]] == x[order[i]]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def spearman(a, b) -> float:
    ra, rb = rank_avg(a), rank_avg(b)
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def partial_spearman(x, y, z) -> float:
    """M12: rho_xy.z on Spearman rank correlations."""
    rxy, rxz, ryz = spearman(x, y), spearman(x, z), spearman(y, z)
    den = (1.0 - rxz ** 2) * (1.0 - ryz ** 2)
    if den <= 0:
        return float("nan")
    return float((rxy - rxz * ryz) / math.sqrt(den))


def runs_of(years, vals):
    """M3/M4: maximal same-sign blocks of >=RUN_MIN_LEN consecutive deltas whose cumulative
    delta clears +/-RUN_MIN_DEPTH. Returns (runs, subthreshold_blocks)."""
    d = np.diff(np.asarray(vals, dtype=float))
    n = len(d)
    runs, subs = [], []
    i = 0
    while i < n:
        if d[i] == 0.0:
            i += 1
            continue
        sign = 1 if d[i] > 0 else -1
        j = i
        while j + 1 < n and d[j + 1] != 0.0 and (1 if d[j + 1] > 0 else -1) == sign:
            j += 1
        length = j - i + 1
        cum = float(np.sum(d[i:j + 1]))
        rec = dict(start_year=int(years[i]), end_year=int(years[j + 1]),
                   n_deltas=int(length), cum=cum, sign=sign)
        if length >= RUN_MIN_LEN and ((sign > 0 and cum >= RUN_MIN_DEPTH) or
                                      (sign < 0 and cum <= -RUN_MIN_DEPTH)):
            runs.append(rec)
        else:
            subs.append(rec)
        i = j + 1
    return runs, subs


def med(vals) -> float:
    if len(vals) == 0:
        return float("nan")
    return float(np.median(np.asarray(vals, dtype=float)))


# ----------------------------------------------------------------------------------
# WT1 - asymmetric adjustment (rise-runs vs fall-runs)
# ----------------------------------------------------------------------------------
WT1_INDICATORS = ["SE.PRM.CMPT.ZS", "SE.SEC.CUAT.UP.ZS", "SE.SEC.CMPT.LO.ZS",
                  "SE.TER.ENRR", "SE.ADT.LITR.ZS"]


def wt1(panel, univ, detail):
    candidates = []   # (unit_id, iso3, country, indicator, source, years, vals)
    for ind in WT1_INDICATORS:
        for iso3, g in panel[panel.indicator == ind].groupby("iso3", sort=True):
            g = g.dropna(subset=["value"]).sort_values("year", kind="mergesort")
            candidates.append(dict(unit=f"WDI:{iso3}:{ind}", iso3=iso3,
                                   country=g.country.iloc[0], indicator=ind, source="IN1",
                                   years=g.year.to_numpy(int), vals=g.value.to_numpy(float)))

    # M2: PHL detail series from IN2, admitted only if not duplicates of an IN1 series
    phl = univ[(univ.status == "observed")]
    for ind in ["completion_primary", "completion_upper_secondary",
                "completion_lower_secondary", "ger_tertiary"]:
        g = phl[(phl.iso3 == "PHL") & (phl.indicator == ind)].dropna(subset=["value"])
        g = g.sort_values("year", kind="mergesort")
        if g.empty:
            continue
        years, vals = g.year.to_numpy(int), g.value.to_numpy(float)
        dup, dup_max = False, float("nan")
        for c in candidates:
            if c["iso3"] != "PHL":
                continue
            common = np.intersect1d(c["years"], years)
            if len(common) == 0:
                continue
            if len(common) >= 0.9 * min(len(c["years"]), len(years)):
                a = pd.Series(c["vals"], index=c["years"]).loc[common].to_numpy(float)
                b = pd.Series(vals, index=years).loc[common].to_numpy(float)
                m = float(np.max(np.abs(a - b)))
                if m <= 1e-6:
                    dup, dup_max = True, m
                    break
        if dup:
            detail.append(("WT1", f"IN2:PHL:{ind}", "PHL", ind, "duplicate_of_in1", len(years), "",
                           "", "DERIVED", f"excluded M2 duplicate (max|diff|={dup_max:.2e})"))
            continue
        candidates.append(dict(unit=f"IN2:PHL:{ind}", iso3="PHL", country="Philippines",
                               indicator=ind, source="IN2", years=years, vals=vals))

    qual, excluded = [], []
    for c in candidates:
        if len(c["years"]) >= MIN_OBS:
            qual.append(c)
        else:
            excluded.append(c)

    rise, fall, sub_n = [], [], 0
    for c in qual:
        r, s = runs_of(c["years"], c["vals"])
        sub_n += len(s)
        rises = [x for x in r if x["sign"] > 0]
        falls = [x for x in r if x["sign"] < 0]
        rise += [(c["unit"], x) for x in rises]
        fall += [(c["unit"], x) for x in falls]
        detail.append(("WT1", c["unit"], c["iso3"], c["indicator"], "n_obs", len(c["years"]),
                       f"{c['years'].min()}-{c['years'].max()}", "", "OBSERVED", c["source"]))
        detail.append(("WT1", c["unit"], c["iso3"], c["indicator"], "rise_runs", len(c["years"]),
                       f"{c['years'].min()}-{c['years'].max()}", f6(float(len(rises))), "DERIVED", ""))
        detail.append(("WT1", c["unit"], c["iso3"], c["indicator"], "fall_runs", len(c["years"]),
                       f"{c['years'].min()}-{c['years'].max()}", f6(float(len(falls))), "DERIVED", ""))
        for x in rises:
            detail.append(("WT1", c["unit"], c["iso3"], c["indicator"], "rise_run", len(c["years"]),
                           f"{x['start_year']}-{x['end_year']}", f6(x["cum"]), "DERIVED",
                           f"{x['n_deltas']} deltas"))
        for x in falls:
            detail.append(("WT1", c["unit"], c["iso3"], c["indicator"], "fall_run", len(c["years"]),
                           f"{x['start_year']}-{x['end_year']}", f6(x["cum"]), "DERIVED",
                           f"{x['n_deltas']} deltas"))

    for c in excluded:
        detail.append(("WT1", c["unit"], c["iso3"], c["indicator"], "excluded_n_lt_15",
                       len(c["years"]), f"{c['years'].min()}-{c['years'].max()}", "", "OBSERVED",
                       "fails M1 n>=15"))

    n_countries = len({c["iso3"] for c in qual})
    n_rise, n_fall = len(rise), len(fall)
    rise_depth = [abs(x[1]["cum"]) for x in rise]
    fall_depth = [abs(x[1]["cum"]) for x in fall]

    if n_rise == 0:
        row = ("WT1", "ratio of fall-runs to rise-runs (and of median run depths)", "", "0.5 (both)",
               "DATA LIMITED", 0, n_countries, "DERIVED",
               f"n_qualifying_series=0; n_rise_runs=0", "M5: no rise-runs, ratio unformable")
        return row, f"qualifying series = 0 of {len(candidates)} candidates", None

    ratio_count = n_fall / n_rise
    if n_fall == 0:
        ratio_depth = 0.0
        depth_note = "no fall-runs (degenerate: maximally asymmetric)"
    else:
        ratio_depth = med(fall_depth) / med(rise_depth) if med(rise_depth) > 0 else float("nan")
        depth_note = ""

    ok = (ratio_count <= WT1_RATIO_MAX) and (ratio_depth <= WT1_RATIO_MAX)
    verdict = "SUPPORTED" if ok else "NOT SUPPORTED"
    if not (ratio_count == ratio_count) or not (ratio_depth == ratio_depth):
        verdict = "DATA LIMITED"

    fails = []
    if ratio_count > WT1_RATIO_MAX:
        fails.append(f"count_ratio {f6(ratio_count)} > {f6(WT1_RATIO_MAX)}")
    if not (ratio_depth <= WT1_RATIO_MAX):
        fails.append(f"depth_ratio {f6(ratio_depth)} > {f6(WT1_RATIO_MAX)}")
    comps = (f"n_qualifying_series={len(qual)}; n_rise_runs={n_rise}; n_fall_runs={n_fall}; "
             f"ratio_count={f6(ratio_count)}; median_rise_depth_pp={f6(med(rise_depth))}; "
             f"median_fall_depth_pp={f6(med(fall_depth))}; ratio_depth={f6(ratio_depth)}; "
             f"sub_threshold_blocks={sub_n}; "
             f"binding_leg={'none' if not fails else '; '.join(fails)}"
             + (f"; note={depth_note}" if depth_note else ""))
    row = ("WT1", "fall-runs / rise-runs, and median|fall depth| / median|rise depth|", f6(ratio_count),
           "0.5 (both)", verdict, len(qual), n_countries, "DERIVED", comps,
           "descriptive episode-count asymmetry only; expansion-era panel (M5, block caveat)")
    summary = (f"series={len(qual)} ({n_countries} countries); rise={n_rise} fall={n_fall} "
               f"ratio_count={f6(ratio_count)} ratio_depth={f6(ratio_depth)}")
    return row, summary, (ratio_count, ratio_depth, n_rise, n_fall, med(rise_depth), med(fall_depth))


# ----------------------------------------------------------------------------------
# WT2 - credential decoupling (tertiary GER vs formal-non-agricultural share)
# ----------------------------------------------------------------------------------
def wt2(panel, detail):
    y0, y1 = WT2_WINDOW
    countries = sorted(panel.iso3.unique())
    qual, rows = [], []
    for iso3 in countries:
        ty, tv = series(panel, iso3, "SE.TER.ENRR")
        ay, av = series(panel, iso3, "SL.AGR.EMPL.ZS")
        ok = (len(ty) >= MIN_OBS and len(ay) >= MIN_OBS and
              y0 in set(ty) and y1 in set(ty) and y0 in set(ay) and y1 in set(ay))
        if not ok:
            miss = []
            if len(ty) < MIN_OBS:
                miss.append("ter_n<15")
            if len(ay) < MIN_OBS:
                miss.append("agr_n<15")
            if y0 not in set(ty) or y1 not in set(ty):
                miss.append("ter_endpoint")
            if y0 not in set(ay) or y1 not in set(ay):
                miss.append("agr_endpoint")
            detail.append(("WT2", f"CTY:{iso3}", iso3, "SE.TER.ENRR+SL.AGR.EMPL.ZS",
                           "excluded", len(ty), "", "", "OBSERVED", ",".join(miss)))
            continue
        ter0 = float(tv[list(ty).index(y0)])
        ter1 = float(tv[list(ty).index(y1)])
        agr0 = float(av[list(ay).index(y0)])
        agr1 = float(av[list(ay).index(y1)])

        d_cred = 100.0 * (ter1 / ter0 - 1.0)                 # percent growth (M6, verbatim)
        d_dest = (100.0 - agr1) - (100.0 - agr0)             # pp change (M6, verbatim)
        d_cred_pp = ter1 - ter0                              # M7 diagnostic, not used for verdict
        decoupled = (d_cred > 0) and (d_dest < d_cred)       # M6, verbatim

        rev, rev_info = reversal_flag(ty, tv, y0, y1)
        qual.append(dict(iso3=iso3, d_cred=d_cred, d_dest=d_dest, d_cred_pp=d_cred_pp,
                         decoupled=decoupled, reversal=rev))
        detail.append(("WT2", f"CTY:{iso3}", iso3, "SE.TER.ENRR+SL.AGR.EMPL.ZS", "D_cred_pct_growth",
                       int(len(ty)), f"{y0}-{y1}", f6(d_cred), "DERIVED",
                       f"ter {f6(ter0)} -> {f6(ter1)}"))
        detail.append(("WT2", f"CTY:{iso3}", iso3, "SL.AGR.EMPL.ZS", "D_dest_pp_change",
                       int(len(ay)), f"{y0}-{y1}", f6(d_dest), "DERIVED",
                       f"formal-non-agric {f6(100.0 - agr0)} -> {f6(100.0 - agr1)}"))
        detail.append(("WT2", f"CTY:{iso3}", iso3, "SE.TER.ENRR", "D_cred_pp_change_DIAGNOSTIC",
                       int(len(ty)), f"{y0}-{y1}", f6(d_cred_pp), "DERIVED",
                       "M7 unit diagnostic only; NOT used for the verdict"))
        detail.append(("WT2", f"CTY:{iso3}", iso3, "SE.TER.ENRR", "decoupled_flag",
                       int(len(ty)), f"{y0}-{y1}", "1" if decoupled else "0", "DERIVED", M6_TXT))
        detail.append(("WT2", f"CTY:{iso3}", iso3, "SE.TER.ENRR", "reversal_flag",
                       int(len(ty)), f"{y0}-{y1}", "1" if rev else "0", "DERIVED", rev_info))

    n_qual = len(qual)
    if n_qual == 0:
        row = ("WT2", "share of qualifying countries where the credential is decoupled from its destination",
               "", ">= 0.50", "DATA LIMITED", 0, 0, "DERIVED", "n_qualifying=0", "M6")
        return row, "no qualifying country", None

    n_dec = sum(1 for q in qual if q["decoupled"])
    dec = [q for q in qual if q["decoupled"]]
    n_rev = sum(1 for q in dec if q["reversal"])
    share_dec = n_dec / n_qual
    share_rev = (n_rev / n_dec) if n_dec else float("nan")

    ok = (share_dec >= WT2_DECOUPLED_SHARE) and (n_dec > 0) and (share_rev <= WT2_REVERSAL_SHARE_MAX)
    verdict = "SUPPORTED" if ok else "NOT SUPPORTED"
    fails = []
    if share_dec < WT2_DECOUPLED_SHARE:
        fails.append(f"decoupled_share {f6(share_dec)} < {f6(WT2_DECOUPLED_SHARE)}")
    if not (share_rev <= WT2_REVERSAL_SHARE_MAX):
        fails.append(f"reversal_share {f6(share_rev)} > {f6(WT2_REVERSAL_SHARE_MAX)}")
    comps = (f"n_qualifying={n_qual}; n_decoupled={n_dec}; share_decoupled={f6(share_dec)}; "
             f"n_decoupled_with_reversal={n_rev}; share_reversal_among_decoupled={f6(share_rev)}; "
             f"thresholds=0.50 decoupled / 0.333333 reversal; "
             f"binding_leg={'none' if not fails else '; '.join(fails)}")
    row = ("WT2", "share of qualifying countries where tertiary GER grows while the formal-non-agricultural "
                  "destination grows more slowly, with no >=5pp sustained tertiary reversal",
           f6(share_dec), ">= 0.50 and reversal <= 1/3", verdict, n_qual, n_qual, "DERIVED", comps,
           "M7 caveat: literal criterion compares % growth (D_cred) with a pp change (D_dest) -> easily satisfied; "
           "no direction/causal claim; wage-premium version HELD (C3 not reopened)")
    summary = (f"qualifying={n_qual}; decoupled={n_dec} ({f6(share_dec)}); reversal among decoupled={n_rev}")
    return row, summary, (n_qual, n_dec, share_dec, n_rev, share_rev)


M6_TXT = "M6: decoupled iff D_cred>0 and D_dest<D_cred"


def reversal_flag(ty, tv, y0, y1):
    """M8: distinct >=5pp peak-to-trough fall held for >=3 consecutive observed years."""
    ys = [(int(y), float(v)) for y, v in zip(ty, tv) if y0 <= y <= y1]
    for i in range(len(ys)):
        peak = max(v for _, v in ys[:i + 1])
        thr = peak - 5.0
        if ys[i][1] > thr:
            continue
        run = 0
        j = i
        while j < len(ys) and ys[j][1] <= thr:
            run += 1
            j += 1
        if run >= 3:
            return True, (f"peak {f6(peak)} -> {f6(ys[i][1])} at {ys[i][0]}; "
                          f"{run} consecutive observed years below {f6(thr)}")
    return False, "no >=5pp reversal sustained >=3 observed years"


# ----------------------------------------------------------------------------------
# WT3 - complementarity -> persistence, income-partial Spearman
# ----------------------------------------------------------------------------------
def wt3(panel, eci, detail):
    y0, y1 = WT3_WINDOW
    countries = sorted(panel.iso3.unique())
    recs = []
    for iso3 in countries:
        cy, cv = series(panel, iso3, "SE.SEC.CUAT.UP.ZS")
        win = [(int(y), float(v)) for y, v in zip(cy, cv) if y0 <= y <= y1]
        ay, av = series(panel, iso3, "SL.AGR.EMPL.ZS")
        awin = [(int(y), float(v)) for y, v in zip(ay, av) if y0 <= y <= y1]
        gy, gv = series(panel, iso3, "NY.GDP.PCAP.KD")
        g2015 = [float(v) for y, v in zip(gy, gv) if int(y) == 2015]
        e = eci[(eci.iso3 == iso3) & eci.eci_sitc.notna()]
        ewin = e[(e.year >= y0) & (e.year <= y1)]

        if len(win) < MIN_OBS or len(awin) < 5 or len(g2015) != 1 or len(ewin) < 5:
            why = []
            if len(win) < MIN_OBS:
                why.append(f"M9 cuat_n_in_window={len(win)}<15")
            if len(awin) < 5:
                why.append("agr_missing")
            if len(g2015) != 1:
                why.append("gdp2015_missing")
            if len(ewin) < 5:
                why.append("eci_missing")
            detail.append(("WT3", f"CTY:{iso3}", iso3, "SE.SEC.CUAT.UP.ZS", "excluded",
                           len(win), f"{y0}-{y1}", "", "OBSERVED", ";".join(why)))
            continue

        wy = np.array([x[0] for x in win], dtype=float)
        wv = np.array([x[1] for x in win], dtype=float)
        p1 = float(np.max(wv))                                   # M10 P1 saturation ceiling
        # M10 P2: reversal count on the OLS-linear-detrended series
        b, a = np.polyfit(wy, wv, 1)
        resid = wv - (a + b * wy)
        dres = np.diff(resid)
        p2 = int(np.sum(dres <= -3.0))
        p2_raw = int(np.sum(np.diff(wv) <= -3.0))
        c1 = float(np.median(ewin.eci_sitc.to_numpy(float)))     # M11 C1
        c2 = float(np.median([100.0 - v for _, v in awin]))      # M11 C2
        inc = math.log(float(g2015[0]))                          # M12 income

        recs.append(dict(iso3=iso3, p1=p1, p2=p2, p2_raw=p2_raw, c1=c1, c2=c2, inc=inc,
                         n_win=len(win)))
        detail.append(("WT3", f"CTY:{iso3}", iso3, "SE.SEC.CUAT.UP.ZS", "P1_saturation_ceiling",
                       len(win), f"{y0}-{y1}", f6(p1), "DERIVED", "M10 max 1995-2024"))
        detail.append(("WT3", f"CTY:{iso3}", iso3, "SE.SEC.CUAT.UP.ZS", "P2_reversal_count_detrended",
                       len(win), f"{y0}-{y1}", f6(float(p2)), "DERIVED",
                       "M10 delta<=-3.0pp on OLS-detrended series"))
        detail.append(("WT3", f"CTY:{iso3}", iso3, "SE.SEC.CUAT.UP.ZS", "P2_reversal_count_raw_DIAGNOSTIC",
                       len(win), f"{y0}-{y1}", f6(float(p2_raw)), "DERIVED",
                       "raw (non-detrended) delta<=-3.0pp; sensitivity only"))
        detail.append(("WT3", f"CTY:{iso3}", iso3, "eci_sitc", "C1_median_eci",
                       len(ewin), f"{y0}-{y1}", f6(c1), "DERIVED", "M11"))
        detail.append(("WT3", f"CTY:{iso3}", iso3, "SL.AGR.EMPL.ZS", "C2_median_formal_nonagric_share",
                       len(awin), f"{y0}-{y1}", f6(c2), "DERIVED", "M11"))
        detail.append(("WT3", f"CTY:{iso3}", iso3, "NY.GDP.PCAP.KD", "income_log_gdp_pc_2015",
                       "", "2015", f6(inc), "DERIVED", "M12 control"))

    n = len(recs)
    if n < WT3_MIN_COUNTRIES:
        row = ("WT3", "income-partial Spearman rho(persistence, complementarity | log income)", "",
               ">= +0.40", "DATA LIMITED", n, n, "DERIVED", f"n_qualifying={n}<{WT3_MIN_COUNTRIES}",
               "M9")
        return row, f"only {n} qualifying countries", None

    p1 = np.array([r["p1"] for r in recs])
    p2 = np.array([r["p2"] for r in recs], dtype=float)
    c1 = np.array([r["c1"] for r in recs])
    c2 = np.array([r["c2"] for r in recs])
    inc = np.array([r["inc"] for r in recs])

    combos = {}
    for pname, pv in (("P1", p1), ("P2", p2)):
        for cname, cv in (("C1", c1), ("C2", c2)):
            raw = spearman(pv, cv)
            part = partial_spearman(pv, cv, inc)
            combos[(pname, cname)] = dict(raw=raw, partial=part)
            detail.append(("WT3", f"COMBO:{pname}x{cname}", "ALL", f"{pname}x{cname}",
                           "spearman_raw", n, f"{y0}-{y1}", f6(raw), "DERIVED", "M12"))
            detail.append(("WT3", f"COMBO:{pname}x{cname}", "ALL", f"{pname}x{cname}",
                           "spearman_partial_on_log_income", n, f"{y0}-{y1}", f6(part), "DERIVED",
                           "M12"))

    pr = combos[("P1", "C1")]          # M12 predeclared primary
    raw, part = pr["raw"], pr["partial"]
    sign_ok = (part == part) and (part > 0) and (np.sign(part) == np.sign(raw))
    ok = (part == part) and (part >= WT3_RHO_MIN) and sign_ok
    verdict = "SUPPORTED" if ok else "NOT SUPPORTED"
    if part != part:
        verdict = "DATA LIMITED"
    others = "; ".join(f"{k[0]}x{k[1]} raw={f6(v['raw'])} partial={f6(v['partial'])}"
                       for k, v in sorted(combos.items()) if k != ("P1", "C1"))
    comps = (f"primary=P1x C1; raw_spearman={f6(raw)}; income_partial_spearman={f6(part)}; "
             f"threshold=+0.40; sign_retained={int(bool(sign_ok))}; n={n}; "
             f"robustness[{others}]")
    row = ("WT3", "income-partial Spearman rho between upper-secondary attainment saturation ceiling "
                  "and median ECI", f6(part), ">= +0.40 with sign retained", verdict, n, n, "DERIVED",
           comps, "cross-sectional descriptive association, n small, income-confounded proxy; "
                  "never a law; no direction claim (R13)")
    summary = f"n={n}; raw rho={f6(raw)}; partial rho={f6(part)}"
    return row, summary, (n, raw, part, combos)


# ----------------------------------------------------------------------------------
# WT4 - PHL ceiling: zero exit episodes
# ----------------------------------------------------------------------------------
def wt4(univ, detail):
    phl = univ[(univ.iso3 == "PHL") & (univ.status == "observed")]

    uy, uv = _univ_series(phl, "completion_upper_secondary")
    ty, tv = _univ_series(phl, "ger_tertiary")
    py, pv = _univ_series(phl, "completion_primary")
    ly, lv = _univ_series(phl, "completion_lower_secondary")

    for ys, vs, nm in ((uy, uv, "completion_upper_secondary"), (ty, tv, "ger_tertiary"),
                       (py, pv, "completion_primary"), (ly, lv, "completion_lower_secondary")):
        for y, v in zip(ys, vs):
            detail.append(("WT4", f"PHL:{nm}", "PHL", nm, "observed_value", len(ys), str(int(y)),
                           f6(float(v)), "OBSERVED", "IN2 status=observed"))

    peak = WT4_US_PEAK
    thr = peak - WT4_DROP
    rec = peak - WT4_RECOVER
    us_episodes = []
    i = 0
    ys_list = [(int(y), float(v)) for y, v in zip(uy, uv)]
    years_after = [(y, v) for y, v in ys_list if y > WT4_US_PEAK_YEAR]
    while i < len(years_after):
        y, v = years_after[i]
        if v < thr:
            j = i
            while j + 1 < len(years_after) and years_after[j + 1][1] < thr:
                j += 1
            runlen = j - i + 1
            recovered_by_2024 = max([x[1] for x in ys_list if x[0] == 2024] or [float("nan")]) >= rec
            calendar_span = years_after[j][0] - years_after[i][0] + 1
            if runlen >= WT4_RUN_YEARS and not recovered_by_2024:
                us_episodes.append((y, runlen, calendar_span))
            detail.append(("WT4", f"PHL:completion_upper_secondary", "PHL",
                           "completion_upper_secondary", "below_threshold_block", runlen,
                           f"{y}-{years_after[j][0]}", f6(years_after[j][1]), "DERIVED",
                           f"threshold {f6(thr)}; observed_years={runlen}; calendar_span={calendar_span}; "
                           f"recovered_by_2024={int(bool(recovered_by_2024))}"))
            i = j + 1
        else:
            i += 1

    ter_thr = WT4_TER_ANCHOR - WT4_DROP
    ter_blocks = []
    tys = [(int(y), float(v)) for y, v in zip(ty, tv)]
    after16 = [(y, v) for y, v in tys if y > 2016]
    i = 0
    while i < len(after16):
        y, v = after16[i]
        if v < ter_thr:
            j = i
            while j + 1 < len(after16) and after16[j + 1][1] < ter_thr:
                j += 1
            ter_blocks.append((y, j - i + 1))
            detail.append(("WT4", "PHL:ger_tertiary", "PHL", "ger_tertiary", "below_threshold_block",
                           j - i + 1, f"{y}-{after16[j][0]}", f6(after16[j][1]), "DERIVED",
                           f"threshold {f6(ter_thr)} (2016 anchor {f6(WT4_TER_ANCHOR)} - 5pp); "
                           f"recovered_to_50_by_2025={int(max(v for yy, v in tys if yy <= 2025) >= 50.0)}"))
            i = j + 1
        else:
            i += 1

    max_by_2025 = max(v for yy, v in tys if yy <= WT4_TER_RECOVER_YEAR)
    ter_recovered = max_by_2025 >= WT4_TER_RECOVER_LEVEL
    ter_episodes = [(y, rl) for (y, rl) in ter_blocks if rl >= WT4_RUN_YEARS and not ter_recovered]
    dip_2018 = dict(tys)[2018] - dict(tys)[2016]

    n_ep = len(us_episodes) + len(ter_episodes)
    ok = (len(us_episodes) == 0) and ter_recovered
    verdict = "SUPPORTED" if ok else "NOT SUPPORTED"

    us_2024 = max(v for yy, v in ys_list if yy == 2024)
    comps = (f"upper_sec_peak={f6(peak)}@{WT4_US_PEAK_YEAR}; upper_sec_threshold={f6(thr)}; "
             f"recovery_band={f6(rec)}; upper_sec_exit_episodes={len(us_episodes)}; "
             f"upper_sec_min_below_band={f6(min(v for yy, v in years_after))}@{min(years_after, key=lambda x: x[1])[0]}; "
             f"upper_sec_2024={f6(us_2024)}; ter_anchor_2016={f6(WT4_TER_ANCHOR)}; "
             f"ter_threshold={f6(ter_thr)}; ter_below_blocks={len(ter_blocks)}; "
             f"ter_2018_dip={f6(dip_2018)}; ter_max_to_2025={f6(max_by_2025)}; "
             f"ter_recovered_to_50_by_2025={int(bool(ter_recovered))}; ter_exit_episodes={len(ter_episodes)}; "
             f"upper_sec_max_drawdown_pp={f6(peak - min(v for yy, v in years_after))}; "
             f"ter_below_block_years={','.join(f'{y}+{rl}' for y, rl in ter_blocks)}")
    row = ("WT4", "count of PHL exit episodes (upper-secondary completion and tertiary GER)", f6(float(n_ep)),
           "0 episodes (and tertiary recovered >=50 by 2025)", verdict, 2, 1, "OBSERVED", comps,
           "descriptive confirmation of a known non-response; the discriminating (queue) version remains C3/HELD; "
           "no direction claim")
    summary = (f"upper_sec_episodes={len(us_episodes)}; ter_below_block={ter_blocks}; "
               f"ter_recovered={int(bool(ter_recovered))}")
    return row, summary, (len(us_episodes), len(ter_episodes), ter_recovered, dip_2018, us_2024)


def _univ_series(phl, ind):
    g = phl[phl.indicator == ind].dropna(subset=["value"]).sort_values("year", kind="mergesort")
    return g.year.to_numpy(int), g.value.to_numpy(float)


# ----------------------------------------------------------------------------------
# WT5 - shadow gate gradient (DESIGN-ONLY, NOT SCORED)
# ----------------------------------------------------------------------------------
def wt5(grad, targets, detail):
    """M14: tabulation only; NOT SCORED. Reports the block's stated ratios AND the same-year
    reading the disk actually supports (the block's 45 is a 1996 HKG figure, not 2010)."""
    out = {}
    hk = targets[(targets.iso3 == "HKG") & targets.rate_pct.notna()]
    by_year = {}
    for yr in (1996, 2010):
        d = hk[hk.year.astype(str) == str(yr)]
        by_year[yr] = dict(zip(d.stage, d.rate_pct.astype(float)))

    # the block's stated ratio: 85 (2010 senior) / 45 (1996 primary) = 1.89 -> CROSS-YEAR
    r_block = by_year[2010]["senior secondary"] / by_year[1996]["primary"]
    # same-year readings that the disk can actually support
    r_1996 = by_year[1996]["senior secondary"] / by_year[1996]["primary"]
    r_2010 = by_year[2010]["senior secondary"] / by_year[2010]["lower secondary"]
    # HKG 2003 stage gradient (same survey, same schools)
    hk03 = grad[(grad.country == "HKG") & (grad.year == 2003) & (grad.dimension == "stage")]
    g03 = dict(zip(hk03.level, hk03.value_pct.astype(float)))
    r_2003 = g03["S6-7"] / g03["S1-3"]
    # KOR 2023: participation falls at the gate, per-student spend rises
    k = grad[(grad.country == "KOR") & (grad.year == 2023)]
    part = dict(zip(k[k.dimension == "level-participation"].level,
                    k[k.dimension == "level-participation"].value_pct.astype(float)))
    spend = dict(zip(k[k.dimension == "level-spend"].level,
                     k[k.dimension == "level-spend"].value_pct.astype(float)))
    spend_ratio = spend["high"] / spend["elementary"]
    part_delta = part["high"] - part["elementary"]

    out.update(r_block=r_block, r_1996=r_1996, r_2010=r_2010, r_2003=r_2003,
               spend_ratio=spend_ratio, part=part, spend=spend, part_delta=part_delta,
               by_year=by_year)

    detail.append(("WT5", "HKG:2010_senior/1996_primary", "HKG", "shadow participation",
                   "gate_ratio_CROSSYEAR_as_block_states", 2, "1996,2010", f6(r_block), "OBSERVED",
                   f"85 (2010 senior) / 45 (1996 primary) = the block's 1.89; years differ"))
    detail.append(("WT5", "HKG:1996_same_survey", "HKG", "shadow participation",
                   "gate_ratio_senior_over_primary", 2, "1996", f6(r_1996), "OBSERVED",
                   f"40/45 same telephone survey (HKFYG 1996): senior LOWER than primary"))
    detail.append(("WT5", "HKG:2010_same_survey", "HKG", "shadow participation",
                   "gate_ratio_senior_over_lower_secondary", 2, "2010", f6(r_2010), "OBSERVED",
                   "85/72; no primary row exists for 2010 on disk"))
    detail.append(("WT5", "HKG:2003_stage_gradient", "HKG", "shadow participation",
                   "gate_ratio_S6-7_over_S1-3", 3, "2003", f6(r_2003), "OBSERVED",
                   "Bray & Kwok (2003) same survey, same schools; near-circular re-tabulation"))
    detail.append(("WT5", "KOR:2023", "KOR", "shadow participation",
                   "participation_delta_elementary_to_high", 2, "2023", f6(part_delta), "OBSERVED",
                   f"elementary {f6(part['elementary'])} -> high {f6(part['high'])}"))
    detail.append(("WT5", "KOR:2023", "KOR", "shadow spend", "spend_ratio_high_over_elementary",
                   2, "2023", f6(spend_ratio), "OBSERVED",
                   f"per student {f6(spend['elementary'])} -> {f6(spend['high'])} thousand KRW/month"))

    held = targets[targets.status == "unresolved"]
    for _, r in held.iterrows():
        detail.append(("WT5", f"HELD:{r.iso3}", r.iso3, "shadow participation", "HELD", "", "",
                       "", "HELD", f"no verified participation rate on disk: {r.notes}"))

    comps = (f"block_ratio_crossyear={f6(r_block)} (85@2010/45@1996); "
             f"same_year_1996={f6(r_1996)} (40/45); same_year_2010={f6(r_2010)} (85/72); "
             f"HKG2003_S6-7_over_S1-3={f6(r_2003)} (70.3/35.1); "
             f"KOR2023_participation {f6(part['elementary'])}->{f6(part['high'])}; "
             f"KOR2023_spend_ratio={f6(spend_ratio)}; "
             f"surveys_with_BOTH_primary_and_senior_same_year=1 (HKG 1996); "
             f"PHL/KHM/CHN/JPN=HELD")
    row = ("WT5", "senior-secondary shadow rate / primary shadow rate (design-only tabulation)", f6(r_block),
           ">= 1.50 (design-only)", "DESIGN-ONLY", 2, 1, "OBSERVED", comps,
           "NOT SCORED. The block's 1.89 is CROSS-YEAR (2010 senior / 1996 primary); the only same-year "
           "primary-vs-senior pair on disk is HKG 1996 = 0.889, i.e. no gate gradient. Near-circular "
           "re-tabulation (Bray & Kwok 2003); the real shadow test is the v1.3/W2 module (d5).")
    summary = (f"block cross-year={f6(r_block)}; same-year 1996={f6(r_1996)}; 2010 senior/lower="
               f"{f6(r_2010)}; 2003={f6(r_2003)}; KOR spend ratio={f6(spend_ratio)}")
    return row, summary, out


# ----------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=str(WTDIR / "results"))
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(IN_PANEL)
    univ = pd.read_csv(IN_UNIV)
    eci = pd.read_csv(IN_ECI)
    grad = pd.read_csv(IN_SHADOW_GRAD)
    targets = pd.read_csv(IN_SHADOW_TARGETS)

    for df in (panel, univ, eci, grad, targets):
        for c in ("iso3", "indicator"):
            if c in df.columns:
                df[c] = df[c].astype(str).str.strip()

    detail = []
    rows = []

    r, s, _ = wt1(panel, univ, detail)
    rows.append(r)
    print("WT1:", s)
    r, s, _ = wt2(panel, detail)
    rows.append(r)
    print("WT2:", s)
    r, s, _ = wt4(univ, detail)
    rows.append(r)
    print("WT4:", s)
    r, s, _ = wt3(panel, eci, detail)
    rows.append(r)
    print("WT3:", s)
    r, s, _ = wt5(grad, targets, detail)
    rows.append(r)
    print("WT5:", s)

    # HELD rows: named, no numbers (HELD-1, HELD-2)
    rows.append(("WT2.HELD-1",
                 "credential wage-premium series (PSA FIES/LFS; WB Enterprise Surveys)", "", "",
                 "HELD", "", "", "HELD", "",
                 "not on disk; external '39% overeducated / flat graduate wages' facts are cited not measured "
                 "(D49); the C3 wage-premium claim is NOT reopened by this battery"))
    rows.append(("WT5.HELD-2", "PHL/KHM/CHN/JPN shadow participation rates", "", "", "HELD", "", "", "HELD",
                 "", "TARGETS_SHADOW rows are 'unresolved' with empty values; no number is reported or imputed"))

    order = ["WT1", "WT2", "WT3", "WT4", "WT5", "WT2.HELD-1", "WT5.HELD-2"]
    rows = sorted(rows, key=lambda r: order.index(r[0]))
    res = pd.DataFrame(rows, columns=["test_id", "estimand", "statistic", "threshold", "verdict", "n",
                                      "n_countries", "label", "components", "note"])
    for c in ("n", "n_countries"):
        res[c] = res[c].map(lambda v: "" if v == "" or v is None else str(int(v)))
    res["data_basis"] = "OBSERVED-ONLY (no synthetic, no toy)"

    det = pd.DataFrame(detail, columns=["test_id", "unit_id", "iso3", "indicator", "metric", "n_obs",
                                        "year_range", "value", "label", "note"])
    det = det.sort_values(["test_id", "unit_id", "metric", "year_range", "value"],
                          kind="mergesort").reset_index(drop=True)

    res.to_csv(outdir / "RESULTS.csv", index=False, lineterminator="\n")
    det.to_csv(outdir / "DETAIL.csv", index=False, lineterminator="\n")

    info = dict(
        script="code/run_wt.py",
        battery="WT1-WT5 (brief_019 section C; D98-D101, D89)",
        seed=None,
        rng="none - no bootstrap, no Monte Carlo (M15)",
        thresholds=dict(MIN_OBS=MIN_OBS, RUN_MIN_LEN=RUN_MIN_LEN, RUN_MIN_DEPTH=RUN_MIN_DEPTH,
                        WT1_RATIO_MAX=WT1_RATIO_MAX, WT2_WINDOW=list(WT2_WINDOW),
                        WT2_DECOUPLED_SHARE=WT2_DECOUPLED_SHARE,
                        WT2_REVERSAL_SHARE_MAX=WT2_REVERSAL_SHARE_MAX,
                        WT3_WINDOW=list(WT3_WINDOW), WT3_RHO_MIN=WT3_RHO_MIN,
                        WT4_US_PEAK=WT4_US_PEAK, WT4_DROP=WT4_DROP, WT4_RECOVER=WT4_RECOVER,
                        WT4_RUN_YEARS=WT4_RUN_YEARS, WT4_TER_ANCHOR=WT4_TER_ANCHOR,
                        WT4_TER_RECOVER_LEVEL=WT4_TER_RECOVER_LEVEL,
                        WT4_TER_RECOVER_YEAR=WT4_TER_RECOVER_YEAR),
        inputs={str(p.relative_to(ROOT)): sha256(p) for p in INPUTS},
        outputs={n: sha256(outdir / n) for n in ("RESULTS.csv", "DETAIL.csv")},
        verdicts={r[0]: r[4] for r in rows},
    )
    (outdir / "run_info.json").write_text(json.dumps(info, indent=2, sort_keys=True) + "\n",
                                          encoding="utf-8")
    print("wrote", outdir / "RESULTS.csv", outdir / "DETAIL.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
