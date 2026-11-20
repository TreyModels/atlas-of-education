#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-23 D63-BOUNDS -- the D63 residual split as a descriptive bound.

Deterministic. No RNG, no network, no model run, no clock value in any result file.
Reads ONLY the frozen inputs declared in PRE_DECLARATIONS.md S5 and listed in INPUT_SHA256.
Writes ONLY inside this experiment directory (results/ or --outdir).

Implements PRE_DECLARATIONS.md exactly:
  S3   identity     G = P + Q,  P = ln(90/lower_2021),  Q = ln(lower_2021/upper_2024)
                    pipeline_share = P/G,  ratio_share = Q/G,  |(P+Q)-G| <= 1e-12
  S3.1 split verdict UNDETERMINED > (PIPELINE-DOMINANT | RATIO-DOMINANT) > RESIDUAL-SPLIT, THIN rule at n<3
  S4   three bounds B1 required_lower vs record_max_lower; B2 required_ratio vs observed 8-pair range;
                    B3 implied_upper interval at the record max lower vs 90
       bounds map INSIDE (all three) / EDGE (mixed) / OUTSIDE (none), precedence INSIDE > EDGE > OUTSIDE
  S6   reproduction of the Council's stated numbers under the declared rounding rule (BLOCK on failure)
  S7   one declared non-verdict-bearing sensitivity (contemporaneous lower value)
  S8   provenance: one DETAIL row per number, path + column + filter + derivation

Usage:
  python run_d63_bounds.py [--outdir results]
  python run_d63_bounds.py --check-findings      # read-only audit of FINDINGS.md; writes nothing, prints JSON
"""
import csv
import hashlib
import json
import math
import os
import re
import sys

# ======================================================================================
# 0. Frozen constants -- hashed before the run; a mismatch is a BLOCK, not a rerun
# ======================================================================================
EXPERIMENT = "EXP-23 D63-BOUNDS"
WORKER = "D63"
BRIEF = "Council brief 025 (D156 #3, rank #3); SYNTHESIS_025.md section 6.3 EXP-23; D153(xiii); D158(1)-(7)"

PREDECL_SHA256 = "dc714963f9c4273ebc36837d50bb98542dba98bf1d66c7b7a3ce076d36efad36"

SERIES = "10_massification/data/UNIVERSALIZATION_SERIES.csv"
SYNTH = "08_council/brief_025/SYNTHESIS_025.md"
DECIS = "08_council/DECISIONS.md"
PAIRS_SRC = "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv"
CONVREG = "10_massification/extensions/conv_reg_2026-11-20/results/CONV_REG.csv"
KAPPA = "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv"
GEN13 = "10_massification/extensions/synthetic_2026-11-20/generator_v1_3/results/synthetic_panel_v1_3.csv"

# role: ARITHMETIC = a number is read from it and enters a result; CITATION-ONLY = named, never used
INPUT_SHA256 = {
    SERIES:  ("85bc869396ebfcb39e3e1a21a31af219e75a07326c738a51d2bfdbe536737ddb", "ARITHMETIC"),
    SYNTH:   ("e279e8200bb8504cafb6b5a4f6f70f3f436410d6839b315896877973c50a8beb", "ARITHMETIC (verbatim source)"),
    DECIS:   ("b0a314b06f73b1cc933539d77f2e8bc3d4f6237e63ba8541e2b16629708c3e57", "ARITHMETIC (verbatim source)"),
    PAIRS_SRC: ("692ca7c01b8b3a7105e84339a87f97029b6a50e277681bdcdbe0f02bf027600f", "ARITHMETIC (8-pair cross-check)"),
    CONVREG: ("", "CITATION-ONLY (object naming)"),
    KAPPA:   ("", "CITATION-ONLY (descriptive / window-only)"),
    GEN13:   ("", "CITATION-ONLY (synthetic context)"),
}

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # experiment dir
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))           # .../massification-2026-11-20

# ---- declared quantities (PRE_DECLARATIONS.md S3, S4) --------------------------------
ISO = "PHL"
UPPER_COL = "completion_upper_secondary"
LOWER_COL = "completion_lower_secondary"
UPPER_YEAR = 2024
LOWER_PAIR_YEAR = 2021          # t - 3, the block's declared one-stage pair
TARGET = 90.0                   # DECLARED-THRESHOLD (D34/A6: 90/90/90 pp crossings)
LAG = 3
TOL_YEARS = 1
EXPECTED_N_PAIRS = 8
IDENTITY_TOL = 1e-12
SPLIT_BAND_LO = 1.0 / 3.0
SPLIT_BAND_HI = 2.0 / 3.0
DECLARED_RANGE_STATED = (0.889, 1.072)      # the block's 3-dp statement of the 8-pair range

CONV = ("UIS completion rate, percent; same file/source/vintage (UIS_SDG4_2026_11), status=observed; "
        "upper vs lower level and year differ by the declared t-3 pairing (D158 rule 2 identity line, "
        "PRE_DECLARATIONS.md S0)")

BANNED = [
    "The model reproduces the PHL level path",
    "the participation margin is duplicated",
    "the repair made the model worse",
    "the upper-secondary ceiling is structural",
    "the ceiling is not structural",
    "the ceiling is reachable",
    "90 was attainable",
    "the proxy is consistent with the required coverage",
    "forward-usable",
    "the representation capability holds at both levels",
    "behaviourally 13-17 pp wrong",
    "behaviourally N pp wrong",
    "demand falsified",
    "v1.2 passes",
    "D63 is resolved",
    "D63 is explained",
    "conditional level reproduction",
]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p):
    return os.path.join(ROOT, p)


# ======================================================================================
# 1. Guards: predeclaration hash + verbatim re-extraction from the frozen sources
# ======================================================================================
def source_63_lines(syn_lines):
    s = next(i for i, l in enumerate(syn_lines) if l.startswith("### 6.3 EXP-23"))
    e = next(i for i, l in enumerate(syn_lines) if l.startswith("### 6.4"))
    while syn_lines[e - 1].strip() == "":
        e -= 1
    return syn_lines[s:e]


def slice_between(text, start, end):
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"[FATAL] anchor not found in source: {start!r}")
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"[FATAL] anchor not found in source: {end!r}")
    return text[i:j + len(end)]


def extract_region(predecl_text, name):
    b = f"<!-- VERBATIM-BEGIN:{name} -->"
    e = f"<!-- VERBATIM-END:{name} -->"
    i = predecl_text.find(b)
    if i < 0:
        raise SystemExit(f"[FATAL] region marker missing: {name}")
    j = predecl_text.find(e, i)
    body = predecl_text[i + len(b):j]
    lines = body.split("\n")
    out = []
    for ln in lines:
        if ln.startswith("> "):
            out.append(ln[2:])
        elif ln == ">":
            out.append("")
        elif ln.strip() == "":
            continue
        else:
            out.append(ln)
    while out and out[0].strip() == "":
        out.pop(0)
    while out and out[-1].strip() == "":
        out.pop()
    return out


def guard_predecl():
    """Hash enforcement at verdict time (D158 rule 1) + verbatim re-extraction (S1, S2, S10.1)."""
    predecl = os.path.join(HERE, "PRE_DECLARATIONS.md")
    got = sha256_of(predecl)
    ok = got == PREDECL_SHA256
    checks = [("predeclaration sha256 (enforced before any computation)", PREDECL_SHA256, got, ok)]

    text = open(predecl, encoding="utf-8").read()
    syn_lines = open(rel(SYNTH), encoding="utf-8").read().split("\n")
    dec_text = open(rel(DECIS), encoding="utf-8").read()
    syn_text = "\n".join(syn_lines)

    regions = {
        "SYNTHESIS_025-6.3": source_63_lines(syn_lines),
        "DECISIONS-D153-xiii": slice_between(dec_text, "(xiii) **D63's residual is split", "**barred**;").split("\n"),
        "DECISIONS-D156-EXP23": slice_between(dec_text, "**EXP-23 D63-BOUNDS** — the D63 residual split",
                                              "D63 stays UNABLE) **#3**").split("\n"),
        "DECISIONS-D158": slice_between(dec_text, "(1) **Hash enforcement at verdict time**",
                                        "in the same sentence as the number.").split("\n"),
        "SYNTHESIS_025-8-banned": slice_between(
            syn_text, "- **Banned sentences (the list #5 carries into the write-up).**",
            '"the upper-secondary ceiling is structural"; "the\n  proxy is consistent with the required coverage"; '
            '"κ ≈ 0.95 is forward-usable"; "the representation capability holds at\n  both levels"; '
            '"the model is behaviourally 13–17 pp wrong"; "demand falsified"; "v1.2 passes".').split("\n"),
    }
    for name, want in regions.items():
        have = extract_region(text, name)
        same = have == want
        checks.append((f"verbatim region {name}", f"{len(want)} source lines", f"{len(have)} lines", same))
        if not same:
            for k in range(max(len(want), len(have))):
                a = want[k] if k < len(want) else "<missing>"
                b = have[k] if k < len(have) else "<missing>"
                if a != b:
                    checks.append((f"  first diff at line {k+1}", a[:120], b[:120], False))
                    break
    return all(c[3] for c in checks), checks


def guard_inputs():
    checks = []
    ok = True
    for path, (want, role) in INPUT_SHA256.items():
        got = sha256_of(rel(path))
        if not want:                       # CITATION-ONLY: hash recorded, not pinned
            checks.append((f"{path} [{role}]", "recorded only (citation-only)", got, True))
        else:
            good = got == want
            ok = ok and good
            checks.append((f"{path} [{role}]", want, got, good))
    return ok, checks


# ======================================================================================
# 2. Load
# ======================================================================================
def load_series():
    upper, lower = {}, {}
    seen = {"upper": {}, "lower": {}}
    nrows = 0
    with open(rel(SERIES), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nrows += 1
            if r["iso3"] != ISO:
                continue
            ind = r["indicator"]
            if ind not in (UPPER_COL, LOWER_COL):
                continue
            y = int(r["year"])
            key = "upper" if ind == UPPER_COL else "lower"
            seen[key][y] = seen[key].get(y, 0) + 1
            if r["status"] != "observed":
                continue
            (upper if key == "upper" else lower)[y] = float(r["value"])
    return upper, lower, nrows, seen


def build_pairs(upper, lower):
    """EXP-1 / PIPE-LOO declared pairing: t-3 exact, else nearest within +/-1 y, ties -> earlier, else drop."""
    pairs = []
    for t in sorted(upper):
        target = t - LAG
        cands = [y for y in lower if abs(y - target) <= TOL_YEARS]
        if not cands:
            continue
        y = min(cands, key=lambda yy: (abs(yy - target), yy))
        pairs.append({
            "upper_year": t, "lower_year": y, "offset": y - target,
            "flag": "EXACT" if y == target else "NEAREST_1Y",
            "upper": upper[t], "lower": lower[y],
        })
    for p in pairs:
        p["ratio"] = p["upper"] / p["lower"]
    return pairs


# ======================================================================================
# 3. Arithmetic per PRE_DECLARATIONS.md S3, S4, S7
# ======================================================================================
def compute(upper, lower, pairs):
    u24 = upper[UPPER_YEAR]
    l21 = lower[LOWER_PAIR_YEAR]
    lmax_year = max(lower, key=lambda y: (lower[y], -y))
    l24 = lower[lmax_year]
    n_lower_obs = len(lower)
    n_upper_obs = len(upper)

    gap_pp = TARGET - u24
    G = math.log(TARGET / u24)
    P = math.log(TARGET / l21)
    Q = math.log(l21 / u24)
    resid = abs((P + Q) - G)
    pipeline_share = P / G
    ratio_share = Q / G

    required_lower = TARGET / (u24 / l21)
    excess = required_lower - l24
    required_ratio = TARGET / l24
    ratios = [p["ratio"] for p in pairs]
    rmin = min(ratios)
    rmax = max(ratios)
    rmin_pair = pairs[ratios.index(rmin)]
    rmax_pair = pairs[ratios.index(rmax)]
    implied_lo = l24 * rmin
    implied_hi = l24 * rmax

    # --- split verdict (S3.1) ---------------------------------------------------------
    thin = len(pairs) < 3
    if pipeline_share > SPLIT_BAND_HI:
        split_verdict = "PIPELINE-DOMINANT" if not thin else "UNDETERMINED"
    elif ratio_share > SPLIT_BAND_HI:
        split_verdict = "RATIO-DOMINANT" if not thin else "UNDETERMINED"
    elif SPLIT_BAND_LO <= pipeline_share <= SPLIT_BAND_HI and SPLIT_BAND_LO <= ratio_share <= SPLIT_BAND_HI:
        split_verdict = "RESIDUAL-SPLIT"
    else:
        split_verdict = "UNDETERMINED"

    # --- three bounds (S4) ------------------------------------------------------------
    b1_out = "INSIDE" if required_lower <= l24 else "OUTSIDE"
    b2_out = "INSIDE" if rmin <= required_ratio <= rmax else "OUTSIDE"
    b3_out = "INSIDE" if implied_lo <= TARGET <= implied_hi else "OUTSIDE"
    outcomes = [b1_out, b2_out, b3_out]
    n_in = outcomes.count("INSIDE")
    if n_in == 3:
        bounds_verdict = "BOUNDS-INSIDE"
    elif n_in == 0:
        bounds_verdict = "BOUNDS-OUTSIDE"
    else:
        bounds_verdict = "BOUNDS-EDGE"

    # --- declared non-verdict-bearing sensitivity (S7) --------------------------------
    P_t = math.log(TARGET / l24)
    Q_t = math.log(l24 / u24)
    sens_resid = abs((P_t + Q_t) - G)

    return dict(u24=u24, l21=l21, l24=l24, lmax_year=lmax_year, n_lower_obs=n_lower_obs,
                n_upper_obs=n_upper_obs, gap_pp=gap_pp, G=G, P=P, Q=Q, resid=resid,
                pipeline_share=pipeline_share, ratio_share=ratio_share,
                required_lower=required_lower, excess=excess, required_ratio=required_ratio,
                rmin=rmin, rmax=rmax, rmin_pair=rmin_pair, rmax_pair=rmax_pair,
                implied_lo=implied_lo, implied_hi=implied_hi,
                b1=b1_out, b2=b2_out, b3=b3_out,
                n_in=n_in, split_verdict=split_verdict, bounds_verdict=bounds_verdict,
                thin=thin, n_pairs=len(pairs),
                P_t=P_t, Q_t=Q_t, sens_pipeline_share=P_t / G, sens_ratio_share=Q_t / G,
                sens_resid=sens_resid, ratio_t=u24 / l24)


# ======================================================================================
# 4. Reproduction of the Council's stated numbers (S6) -- declared rounding rule
# ======================================================================================
def reproduced(stated, got, decimals):
    return abs(got - stated) <= 0.5 * (10.0 ** (-decimals)) + 1e-15


def reproduction_table(c):
    rows = [
        ("R1", "upper_2024", 75.02525329589844, c["u24"], 14),
        ("R2", "lower_2021", 80.89604949951172, c["l21"], 14),
        ("R3", "gap_pp = 90 - upper_2024", 14.974747, c["gap_pp"], 6),
        ("R4", "pipeline_share_pct", 58.6008, 100.0 * c["pipeline_share"], 4),
        ("R5", "ratio_share_pct", 41.3992, 100.0 * c["ratio_share"], 4),
        ("R6", "required_lower", 97.042584, c["required_lower"], 6),
        ("R7", "excess over record max", 4.628621, c["excess"], 6),
        ("R8", "record_max_lower", 92.4139633178711, c["l24"], 13),
        ("R9", "required_ratio", 0.973879, c["required_ratio"], 6),
        ("R10a", "ratio_min (3 dp)", 0.889, c["rmin"], 3),
        ("R10b", "ratio_max (3 dp)", 1.072, c["rmax"], 3),
    ]
    out = []
    for rid, item, stated, got, d in rows:
        out.append(dict(rid=rid, item=item, stated=stated, got=got, decimals=d,
                        diff=got - stated, ok=reproduced(stated, got, d)))
    return out


# ======================================================================================
# 5. Writers
# ======================================================================================
def fnum(x, d=9):
    if x is None:
        return ""
    return f"{x:.{d}f}"


def write_results(path, c, rep, n_pairs_ok):
    cols = ["row_type", "item_id", "item", "value_num", "value_display", "units", "label",
            "comparison", "outcome", "used_in_verdict", "note"]
    rows = []

    def add(rt, iid, item, val, disp, units, label, comp, outcome, used, note):
        rows.append([rt, iid, item, ("" if val is None else repr(val)), disp, units, label,
                     comp, outcome, "TRUE" if used else "FALSE", note])

    add("SPLIT_COMPONENT", "S1", "gap_pp = 90 - upper_2024", c["gap_pp"], fnum(c["gap_pp"], 6), "pp",
        "DERIVED", "90 - 75.02525329589844", "", True,
        "the raw pp gap; the identity below splits the LOG gap")
    add("SPLIT_COMPONENT", "S2", "ln_gap G = ln(90/upper_2024)", c["G"], fnum(c["G"], 12), "log ratio",
        "DERIVED", "ln(90/75.02525329589844)", "", True, "denominator of both shares")
    add("SPLIT_COMPONENT", "S3", "pipeline_log P = ln(90/lower_2021)", c["P"], fnum(c["P"], 12), "log ratio",
        "DERIVED", "ln(90/80.89604949951172)", "", True, "pipeline-level channel, t-3 pair")
    add("SPLIT_COMPONENT", "S4", "ratio_log Q = ln(lower_2021/upper_2024)", c["Q"], fnum(c["Q"], 12),
        "log ratio", "DERIVED", "ln(80.89604949951172/75.02525329589844)", "", True,
        "transition-ratio channel, t-3 pair")
    add("SPLIT_COMPONENT", "S5", "identity_residual |(P+Q)-G|", c["resid"], f"{c['resid']:.3e}",
        "log ratio", "DERIVED", "== 0 by construction, floating point only", "PASS" if c["resid"] <= IDENTITY_TOL else "BLOCK",
        True, f"declared tolerance {IDENTITY_TOL:.0e}")
    add("SPLIT_COMPONENT", "S6", "pipeline_share = P/G", c["pipeline_share"], fnum(c["pipeline_share"], 9),
        "share", "DERIVED", "in [1/3, 2/3] ?", "", True, "0.586008386858443")
    add("SPLIT_COMPONENT", "S7", "ratio_share = Q/G", c["ratio_share"], fnum(c["ratio_share"], 9),
        "share", "DERIVED", "in [1/3, 2/3] ?", "", True, "0.413991613141558")
    add("SPLIT_COMPONENT", "S8", "pipeline_share_pct", 100.0 * c["pipeline_share"],
        fnum(100.0 * c["pipeline_share"], 4), "percent", "DERIVED", "P/G x 100", "", True,
        "the block's 58.6008 %")
    add("SPLIT_COMPONENT", "S9", "ratio_share_pct", 100.0 * c["ratio_share"],
        fnum(100.0 * c["ratio_share"], 4), "percent", "DERIVED", "Q/G x 100", "", True,
        "the block's 41.3992 %")

    add("BOUND_COMPARISON", "B1", "required_lower <= record_max_lower", c["required_lower"],
        fnum(c["required_lower"], 6), "pp", "DERIVED",
        f"{fnum(c['required_lower'], 6)} vs record max {fnum(c['l24'], 6)} (excess {fnum(c['excess'], 6)} pp)",
        c["b1"], True, "lower completion needed at the 2024 ratio, vs the highest lower completion in the record")
    add("BOUND_COMPARISON", "B2", "ratio_min <= required_ratio <= ratio_max", c["required_ratio"],
        fnum(c["required_ratio"], 9), "ratio", "DERIVED",
        f"{fnum(c['required_ratio'], 9)} in [{fnum(c['rmin'], 9)}, {fnum(c['rmax'], 9)}]",
        c["b2"], True, "ratio needed at the record's 2024 lower completion, vs the observed 8-pair range")
    add("BOUND_COMPARISON", "B3", "implied_lo <= 90 <= implied_hi", c["implied_hi"],
        fnum(c["implied_hi"], 6), "pp", "DERIVED",
        f"[{fnum(c['implied_lo'], 6)}, {fnum(c['implied_hi'], 6)}] contains 90", c["b3"], True,
        "upper completion implied by the observed 8-ratio range at the record's highest lower completion")

    add("VERDICT", "V1", "split_verdict", None, c["split_verdict"], "", "DERIVED",
        "pipeline %.9f, ratio %.9f, band [1/3, 2/3]" % (c["pipeline_share"], c["ratio_share"]),
        c["split_verdict"], True,
        "block S6.3 item 5 mapping; THIN rule not binding at n_pairs = %d" % c["n_pairs"])
    add("VERDICT", "V2", "bounds_verdict", None, c["bounds_verdict"], "", "DERIVED",
        "B1 %s / B2 %s / B3 %s -> %d of 3 inside" % (c["b1"], c["b2"], c["b3"], c["n_in"]),
        c["bounds_verdict"], True,
        "precedence BOUNDS-INSIDE > BOUNDS-EDGE > BOUNDS-OUTSIDE; mapping fixed in PRE_DECLARATIONS.md section 4")
    add("VERDICT", "V3", "d63_status", None, "UNABLE as to cause", "", "DECLARED",
        "fixed by the block, D153(vi) and D153(xiii)", "UNABLE", True,
        "no outcome of V1 or V2 changes it")
    add("VERDICT", "V4", "n_pairs", float(c["n_pairs"]), str(c["n_pairs"]), "pairs", "DERIVED",
        "== 8 declared pairs", "PASS" if n_pairs_ok else "BLOCK", True,
        "pair set cross-checked against PIPE_LOO_PAIRS.csv")
    add("VERDICT", "V5", "reproduction_checks_passed", float(sum(1 for r in rep if r["ok"])),
        "%d of %d" % (sum(1 for r in rep if r["ok"]), len(rep)), "checks", "DERIVED",
        "the block's and D153(xiii)'s stated numbers, declared rounding rule",
        "PASS" if all(r["ok"] for r in rep) else "BLOCK", True, "R1-R10b, see DETAIL")

    add("SENSITIVITY_NVB", "X1", "pipeline_share at the contemporaneous lower value", c["sens_pipeline_share"],
        fnum(c["sens_pipeline_share"], 9), "share", "DERIVED",
        "ln(90/lower_2024) / G", "", False,
        "DESCRIPTIVE / NOT-VERDICT-BEARING; declared in PRE_DECLARATIONS.md S7")
    add("SENSITIVITY_NVB", "X2", "ratio_share at the contemporaneous lower value", c["sens_ratio_share"],
        fnum(c["sens_ratio_share"], 9), "share", "DERIVED",
        "ln(lower_2024/upper_2024) / G", "", False, "DESCRIPTIVE / NOT-VERDICT-BEARING")
    add("SENSITIVITY_NVB", "X3", "ratio at the contemporaneous lower value", c["ratio_t"],
        fnum(c["ratio_t"], 9), "ratio", "DERIVED", "upper_2024 / lower_2024", "", False,
        "the observed 2024 same-year ratio; not one of the 8 declared pairs")

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)


def write_detail(path, c, pairs, rep):
    cols = ["number_id", "row_type", "item", "value", "value_display", "units", "label",
            "source_path", "source_column", "source_filter", "derivation", "used_in_verdict",
            "convention", "note"]
    rows = []

    def add(nid, rt, item, val, disp, units, label, path, col, filt, deriv, used, conv, note):
        rows.append([nid, rt, item, ("" if val is None else (repr(val) if isinstance(val, float) else str(val))),
                     disp, units, label, path, col, filt, deriv, "TRUE" if used else "FALSE", conv, note])

    def obs(nid, item, val, disp, year, ind, note):
        add(nid, "OBSERVED_VALUE", item, val, disp, "percent", "OBSERVED", SERIES, "value",
            f"iso3=PHL; indicator={ind}; year={year}; status=observed", "read as-is", True, CONV, note)

    obs("O1", "upper-secondary completion, 2024", c["u24"], fnum(c["u24"], 14), UPPER_YEAR, UPPER_COL,
        "the residual's observed upper value")
    obs("O2", "lower-secondary completion, 2021", c["l21"], fnum(c["l21"], 14), LOWER_PAIR_YEAR, LOWER_COL,
        "the declared t-3 pipeline base")
    obs("O3", "lower-secondary completion, 2024", c["l24"], fnum(c["l24"], 13), c["lmax_year"], LOWER_COL,
        "the record maximum lower completion (also the observed 2024 lower value)")
    add("O4", "DERIVED_VALUE", "record_max_lower", c["l24"], fnum(c["l24"], 13), "percent", "DERIVED",
        SERIES, "value", f"iso3=PHL; indicator={LOWER_COL}; status=observed",
        f"max over the {c['n_lower_obs']} observed lower years; argmax year {c['lmax_year']}", True, CONV, "")
    add("O5", "DERIVED_VALUE", "n_upper_observed_years", float(c["n_upper_obs"]), str(c["n_upper_obs"]), "years",
        "DERIVED", SERIES, "value", f"iso3=PHL; indicator={UPPER_COL}; status=observed", "count of rows", True, CONV, "")
    add("O6", "DERIVED_VALUE", "n_lower_observed_years", float(c["n_lower_obs"]), str(c["n_lower_obs"]), "years",
        "DERIVED", SERIES, "value", f"iso3=PHL; indicator={LOWER_COL}; status=observed", "count of rows", True, CONV, "")

    add("T0", "DERIVED_VALUE", "target level (90 pp)", TARGET, "90", "pp", "DECLARED-THRESHOLD",
        DECIS, "row D34 (M3: upper-sec completion/transition >= 90), 90/90/90 pp",
        "declared crossing bar, not an observed object",
        "DECLARED-THRESHOLD; no observed value is 90", True, "n/a", "not a policy target for this cell")
    add("T1", "DERIVED_VALUE", "split band lower bound", SPLIT_BAND_LO, "0.333333333", "share",
        "DECLARED-THRESHOLD", SYNTH, "section 6.3 item 5", "'both shares lie in [1/3, 2/3]'",
        "1/3", True, "n/a", "the block's split band")
    add("T2", "DERIVED_VALUE", "split band upper bound", SPLIT_BAND_HI, "0.666666667", "share",
        "DECLARED-THRESHOLD", SYNTH, "section 6.3 item 5", "'pipeline_share > 2/3'",
        "2/3", True, "n/a", "the block's dominant threshold")

    add("D1", "DERIVED_VALUE", "gap_pp", c["gap_pp"], fnum(c["gap_pp"], 6), "pp", "DERIVED", SERIES, "value",
        "O1, T0", "90 - upper_2024", True, CONV, "")
    add("D2", "DERIVED_VALUE", "G = ln(90/upper_2024)", c["G"], fnum(c["G"], 12), "log ratio", "DERIVED", SERIES,
        "value", "O1, T0", "math.log(90 / upper_2024)", True, CONV, "")
    add("D3", "DERIVED_VALUE", "P = ln(90/lower_2021)", c["P"], fnum(c["P"], 12), "log ratio", "DERIVED", SERIES,
        "value", "O2, T0", "math.log(90 / lower_2021)", True, CONV, "pipeline-level channel")
    add("D4", "DERIVED_VALUE", "Q = ln(lower_2021/upper_2024)", c["Q"], fnum(c["Q"], 12), "log ratio", "DERIVED",
        SERIES, "value", "O1, O2", "math.log(lower_2021 / upper_2024)", True, CONV, "transition-ratio channel")
    add("D5", "DERIVED_VALUE", "identity_residual", c["resid"], f"{c['resid']:.3e}", "log ratio", "DERIVED",
        SERIES, "value", "O1, O2", "abs((P + Q) - G)", True, CONV, f"declared tolerance {IDENTITY_TOL:.0e}")
    add("D6", "DERIVED_VALUE", "pipeline_share", c["pipeline_share"], fnum(c["pipeline_share"], 9), "share",
        "DERIVED", SERIES, "value", "O1, O2", "P / G", True, CONV, "")
    add("D7", "DERIVED_VALUE", "ratio_share", c["ratio_share"], fnum(c["ratio_share"], 9), "share", "DERIVED",
        SERIES, "value", "O1, O2", "Q / G", True, CONV, "")
    add("D8", "DERIVED_VALUE", "pipeline_share_pct", 100.0 * c["pipeline_share"],
        fnum(100.0 * c["pipeline_share"], 4), "percent", "DERIVED", SERIES, "value", "O1, O2", "100 x P / G",
        True, CONV, "")
    add("D9", "DERIVED_VALUE", "ratio_share_pct", 100.0 * c["ratio_share"],
        fnum(100.0 * c["ratio_share"], 4), "percent", "DERIVED", SERIES, "value", "O1, O2", "100 x Q / G",
        True, CONV, "")
    add("D10", "DERIVED_VALUE", "required_lower", c["required_lower"], fnum(c["required_lower"], 6), "pp",
        "DERIVED", SERIES, "value", "O1, O2, T0", "90 / (upper_2024 / lower_2021)", True, CONV, "B1 input")
    add("D11", "DERIVED_VALUE", "excess over record max", c["excess"], fnum(c["excess"], 6), "pp", "DERIVED",
        SERIES, "value", "O1, O2, O3, T0", "required_lower - record_max_lower", True, CONV, "")
    add("D12", "DERIVED_VALUE", "required_ratio", c["required_ratio"], fnum(c["required_ratio"], 9), "ratio",
        "DERIVED", SERIES, "value", "O3, T0", "90 / lower_2024", True, CONV, "B2 input")
    add("D13", "DERIVED_VALUE", "ratio_min", c["rmin"], fnum(c["rmin"], 12), "ratio", "DERIVED", SERIES, "value",
        "O1, O2 + pair rule", "min over the 8 pairs of upper_t / lower_{t-3}",
        True, CONV, "pair upper %d / lower %d" % (c["rmin_pair"]["upper_year"], c["rmin_pair"]["lower_year"]))
    add("D14", "DERIVED_VALUE", "ratio_max", c["rmax"], fnum(c["rmax"], 12), "ratio", "DERIVED", SERIES, "value",
        "O1, O2 + pair rule", "max over the 8 pairs of upper_t / lower_{t-3}",
        True, CONV, "pair upper %d / lower %d" % (c["rmax_pair"]["upper_year"], c["rmax_pair"]["lower_year"]))
    add("D15", "DERIVED_VALUE", "implied_upper_lo", c["implied_lo"], fnum(c["implied_lo"], 6), "pp", "DERIVED",
        SERIES, "value", "O3, O4 + pair rule", "record_max_lower x ratio_min", True, CONV, "B3 input")
    add("D16", "DERIVED_VALUE", "implied_upper_hi", c["implied_hi"], fnum(c["implied_hi"], 6), "pp", "DERIVED",
        SERIES, "value", "O3, O4 + pair rule", "record_max_lower x ratio_max", True, CONV, "B3 input")
    add("D17", "DERIVED_VALUE", "n_pairs", float(c["n_pairs"]), str(c["n_pairs"]), "pairs", "DERIVED", PAIRS_SRC,
        "upper_year, lower_year", "iso3=PHL", "count of pairs rebuilt under the declared rule", True, CONV, "")
    add("D18", "DERIVED_VALUE", "ratio at the contemporaneous lower value", c["ratio_t"], fnum(c["ratio_t"], 9),
        "ratio", "DERIVED", SERIES, "value", "O1, O3", "upper_2024 / lower_2024", False, CONV,
        "SENSITIVITY / NOT-VERDICT-BEARING")
    add("D19", "DERIVED_VALUE", "pipeline_share at the contemporaneous lower value", c["sens_pipeline_share"],
        fnum(c["sens_pipeline_share"], 9), "share", "DERIVED", SERIES, "value", "O1, O3, T0",
        "ln(90 / lower_2024) / G", False, CONV, "SENSITIVITY / NOT-VERDICT-BEARING; sign flips")
    add("D20", "DERIVED_VALUE", "ratio_share at the contemporaneous lower value", c["sens_ratio_share"],
        fnum(c["sens_ratio_share"], 9), "share", "DERIVED", SERIES, "value", "O1, O3",
        "ln(lower_2024 / upper_2024) / G", False, CONV, "SENSITIVITY / NOT-VERDICT-BEARING")

    for i, p in enumerate(pairs, start=1):
        add(f"P{i}", "PAIR", f"pair upper {p['upper_year']} / lower {p['lower_year']} ({p['flag']}, offset {p['offset']:+d}y)",
            p["ratio"], fnum(p["ratio"], 4), "ratio", "OBSERVED values / DERIVED ratio", SERIES, "value",
            f"iso3=PHL; indicator={UPPER_COL}; year={p['upper_year']}; status=observed AND "
            f"indicator={LOWER_COL}; year={p['lower_year']}; status=observed",
            f"{fnum(p['upper'], 14)} / {fnum(p['lower'], 14)}", True, CONV,
            "cross-checked against PIPE_LOO_PAIRS.csv at 4 dp")

    for r in rep:
        add("R_" + r["rid"], "DERIVED_VALUE", "reproduction: " + r["item"], r["got"], fnum(r["got"], 6),
            "stated units", "DERIVED", DECIS if r["rid"] not in ("R1", "R2", "R8", "R10a", "R10b") else SYNTH,
            "as stated", f"stated {r['stated']} at {r['decimals']} dp",
            f"recomputed - stated = {r['diff']:+.3e}", True, "n/a",
            "reproduced" if r["ok"] else "FAILS the declared rounding rule")

    worst = max(rep, key=lambda r: abs(r["diff"]))
    add("R_MAX", "DERIVED_VALUE", "largest reproduction difference", abs(worst["diff"]),
        fnum(abs(worst["diff"]), 9), "stated units", "DERIVED", DECIS, "as stated",
        f"worst of R1-R10b: {worst['rid']} ({worst['item']})",
        "max over the 11 checks of abs(recomputed - stated)", True, "n/a",
        "smallest headroom of the eleven; still inside the declared rounding rule")

    add("C1", "CITATION_ONLY", "kappa_full (PHL, window-only)", 0.949135, "0.949135", "ratio",
        "DESCRIPTIVE / WINDOW-ONLY", KAPPA, "kappa_full", "iso3=PHL", "read as-is", False,
        "window-only; not used to compute any bound or verdict",
        "cited by the block as a descriptive comparison only (S6.3 item 5)")
    add("C2", "CITATION_ONLY", "generator v1.3 upper 2024 completion_uis", 0.7663908112, "76.63908112",
        "share", "SYNTHETIC", GEN13, "completion_uis",
        "country_id=0; level=upper_secondary; year=2024", "read as-is", False,
        "SYNTHETIC / class v1.3; NO MODEL VALUE ENTERS any bound",
        "cited as context only; no model was run")

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)


# ======================================================================================
# 6. Pair cross-check against the delivered 8-pair file
# ======================================================================================
def crosscheck_pairs(pairs):
    want = {}
    with open(rel(PAIRS_SRC), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["iso3"] != ISO:
                continue
            want[(int(r["upper_year"]), int(r["lower_year_used"]))] = float(r["ratio"])
    have = {(p["upper_year"], p["lower_year"]): p["ratio"] for p in pairs}
    same_set = set(want) == set(have)
    maxdev = max((abs(round(have[k], 4) - round(want[k], 4)) for k in want if k in have), default=0.0)
    return same_set, maxdev, len(want), len(have)


# ======================================================================================
# 7. --check-findings : number register + banned sentences over the prose (writes nothing)
# ======================================================================================
NUM_MASK = [
    # structural markdown numbering (headings, ordered lists) -- not quantities
    (r"(?m)^\s*#{1,6}\s+\d+\.", " "), (r"(?m)^\s*\d+\.\s", " "),
    (r"\bD\d{2,3}\b", " "), (r"\bEXP-\d+\b", " "), (r"§\s?[\d.]+", " "), (r"\bv\d\.\d\b", " "),
    (r"\bR\d+[ab]?\b", " "), (r"\bS\d+\b", " "), (r"\bB\d\b", " "), (r"\bV\d\b", " "),
    (r"\bX\d\b", " "), (r"\bO\d+\b", " "), (r"\bT\d\b", " "), (r"\bP\d\b", " "), (r"\bC\d\b", " "),
    (r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{32,64}\b", " "), (r"\b20\d\d-\d\d-\d\d\b", " "),
    (r"\b\d{1,3}(?:,\d{3})+\b", " "), (r"\b\d+(?:\.\d+)?\s?(?:dp|decimals)\b", " "),
    # cross-references and dates, not quantities
    (r"\brule\s+\w+", " "), (r"\bitem\s+\w+", " "), (r"\b(?:19|20)\d{2}\b", " "),
    (r"\brank\s+#?\d+\b", " "), (r"\bbrief\s+\d+\b", " "), (r"\bSYNTHESIS_\d+\b", " "),
    (r"#\d+", " "),
    (r"\bt\s?[−-]\s?3\b", " "), (r"±\s?\d+(?:\.\d+)?\s?y\b", " "),
    (r"[A-Za-z0-9_]*[dD]63[A-Za-z0-9_]*", " "),
]


def numeric_tokens(text):
    t = text.replace("\u2212", "-").replace("\u2013", "-")
    for pat, rep in NUM_MASK:
        t = re.sub(pat, rep, t)
    return re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])", t)


def detail_values(detail_path):
    vals = []
    with open(detail_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["value"]:
                try:
                    vals.append(float(r["value"]))
                except ValueError:
                    pass
    return vals


def check_findings():
    fin = os.path.join(HERE, "FINDINGS.md")
    det = os.path.join(HERE, "results", "D63_BOUNDS_DETAIL.csv")
    text = open(fin, encoding="utf-8").read()
    vals = detail_values(det)
    toks = numeric_tokens(text)
    unmatched = []
    for tok in toks:
        v = float(tok)
        dec = len(tok.split(".")[1]) if "." in tok else 0
        tol = 0.5 * (10.0 ** (-dec)) + 1e-12
        if not any(abs(v - x) <= tol for x in vals):
            unmatched.append(tok)
    banned_hits = [b for b in BANNED if b.lower() in text.lower()]
    out = dict(n_numbers=len(toks), n_matched=len(toks) - len(unmatched),
               n_unmatched=len(unmatched), unmatched=sorted(set(unmatched)),
               banned_hits=banned_hits, result_files_scanned=[])
    for relp in ("results/D63_BOUNDS_RESULTS.csv", "results/D63_BOUNDS_DETAIL.csv"):
        body = open(os.path.join(HERE, relp), encoding="utf-8").read()
        out["result_files_scanned"].append(relp)
        for b in BANNED:
            if b.lower() in body.lower():
                out["banned_hits"].append(f"{relp}: {b}")
    print(json.dumps(out, ensure_ascii=False))
    return 0 if (not out["unmatched"] and not out["banned_hits"]) else 1


# ======================================================================================
# 8. Main
# ======================================================================================
def main():
    if "--check-findings" in sys.argv:
        return check_findings()

    outdir = "results"
    argv = sys.argv[1:]
    if "--outdir" in argv:
        outdir = argv[argv.index("--outdir") + 1]
    outdir = outdir if os.path.isabs(outdir) else os.path.join(HERE, outdir)
    os.makedirs(outdir, exist_ok=True)

    lines = []

    def say(s=""):
        print(s)
        lines.append(s)

    say("=" * 100)
    say(f"{EXPERIMENT}  |  worker {WORKER}  |  {BRIEF}")
    say(f"predeclaration sha256 : {PREDECL_SHA256}")
    say("=" * 100)

    ok, checks = guard_predecl()
    say("")
    say("[guards] predeclaration hash + verbatim re-extraction, before any computation")
    for name, want, got, good in checks:
        say(f"  {'OK  ' if good else 'FAIL'} {name}")
        if not good:
            say(f"        declared/source {want}")
            say(f"        on-disk         {got}")

    ok2, ichecks = guard_inputs()
    say("")
    say("[guards] frozen inputs (read-only)")
    for name, want, got, good in ichecks:
        say(f"  {'OK  ' if good else 'FAIL'} {name}")
        if want and not good:
            say(f"        declared {want}")
            say(f"        on-disk  {got}")
    if not (ok and ok2):
        say("")
        say("STATUS: BLOCKED (predeclaration hash, verbatim region, or frozen input); not a result")
        with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return 2

    upper, lower, nrows, seen = load_series()
    say("")
    say(f"[data] {SERIES}: {nrows} data rows; PHL observed completion years -- "
        f"upper {len(upper)} {sorted(upper)}, lower {len(lower)} {sorted(lower)}")
    dup = {f"{k}:{y}": n for k in seen for y, n in seen[k].items() if n > 1}
    say(f"       duplicate (iso3, indicator, year) cells on the PHL completion rows: {len(dup)}")

    missing = [k for k in (("upper", UPPER_YEAR), ("lower", LOWER_PAIR_YEAR)) if k[1] not in (upper if k[0] == "upper" else lower)]
    if missing or dup:
        say("")
        say("STATUS: UNDETERMINED -- the block's falsifier fired (2024/2021 pair absent, duplicated or not observed)")
        say("D63 status: UNABLE as to cause (unchanged)")
        with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return 3

    pairs = build_pairs(upper, lower)
    same_set, maxdev, n_want, n_have = crosscheck_pairs(pairs)
    say("")
    say(f"[pairs] rebuilt under the declared rule: n = {len(pairs)} (declared {EXPECTED_N_PAIRS}); "
        f"pair set vs PIPE_LOO_PAIRS.csv: {'MATCH' if same_set else 'MISMATCH'} "
        f"({n_have} vs {n_want}); max 4-dp ratio deviation {maxdev:.4g}")
    for p in pairs:
        say(f"        upper {p['upper_year']} / lower {p['lower_year']} ({p['flag']}, {p['offset']:+d}y)  "
            f"upper {p['upper']:.6f}  lower {p['lower']:.6f}  ratio {p['ratio']:.9f}")
    n_pairs_ok = (len(pairs) == EXPECTED_N_PAIRS) and same_set and maxdev <= 1e-9
    if not n_pairs_ok:
        say("STATUS: BLOCKED-PAIR-SET -- the observed ratio range is not the block's range")
        with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return 4

    c = compute(upper, lower, pairs)

    say("")
    say("[identity] G = ln(90/upper_2024) = ln(90/lower_2021) + ln(lower_2021/upper_2024)")
    say(f"  upper_2024 = {c['u24']!r}   lower_2021 = {c['l21']!r}   lower_2024 = {c['l24']!r} "
        f"(record max lower, year {c['lmax_year']})")
    say(f"  gap_pp                  = {c['gap_pp']:.12f}")
    say(f"  G  = ln(90/u24)         = {c['G']!r}")
    say(f"  P  = ln(90/l21)         = {c['P']!r}")
    say(f"  Q  = ln(l21/u24)        = {c['Q']!r}")
    say(f"  P + Q - G               = {c['resid']:.3e}   (declared tolerance {IDENTITY_TOL:.0e})")
    say(f"  pipeline_share = P/G    = {c['pipeline_share']!r}  ({100*c['pipeline_share']:.4f} %)")
    say(f"  ratio_share    = Q/G    = {c['ratio_share']!r}  ({100*c['ratio_share']:.4f} %)")
    say(f"  SPLIT VERDICT           = {c['split_verdict']}   (band [1/3, 2/3], n_pairs {c['n_pairs']}, thin={c['thin']})")

    say("")
    say("[bounds] three comparisons against the observed record's envelope (no tolerance anywhere)")
    say(f"  B1 required_lower {c['required_lower']!r} vs record_max_lower {c['l24']!r}"
        f"  -> excess {c['excess']:+.12f} pp  -> {c['b1']}")
    say(f"  B2 required_ratio {c['required_ratio']!r} vs observed 8-pair range "
        f"[{c['rmin']!r}, {c['rmax']!r}]  -> {c['b2']}")
    say(f"  B3 implied upper interval at the record max lower "
        f"[{c['implied_lo']!r}, {c['implied_hi']!r}] vs 90  -> {c['b3']}")
    say(f"  outcomes: {c['b1']}/{c['b2']}/{c['b3']}  -> n_inside = {c['n_in']}  -> BOUNDS VERDICT = {c['bounds_verdict']}")

    rep = reproduction_table(c)
    say("")
    say("[reproduction] the block's and D153(xiii)'s stated numbers, declared rounding rule")
    for r in rep:
        say(f"  {'OK  ' if r['ok'] else 'FAIL'} {r['rid']:<5} {r['item']:<38} stated {r['stated']!r:<22} "
            f"recomputed {r['got']!r:<24} diff {r['diff']:+.3e}")
    say(f"  reproduced {sum(1 for r in rep if r['ok'])}/{len(rep)}")

    say("")
    say("[sensitivity] DESCRIPTIVE / NOT-VERDICT-BEARING -- contemporaneous lower value in place of the t-3 pair")
    say(f"  ratio upper_2024/lower_2024 = {c['ratio_t']!r}")
    say(f"  pipeline_share = ln(90/l24)/G = {c['sens_pipeline_share']!r}")
    say(f"  ratio_share    = ln(l24/u24)/G = {c['sens_ratio_share']!r}")
    say(f"  identity residual {c['sens_resid']:.3e}")

    say("")
    say("[verdict]")
    say(f"  split  : {c['split_verdict']}")
    say(f"  bounds : {c['bounds_verdict']}")
    say(f"  D63    : UNABLE as to cause  (fixed; no outcome of this cell changes it)")
    say(f"  model run: NONE.  re-fit: NONE.  adoption: NONE.  the 8-pair range is consumed as a range, not re-tested.")

    if c["resid"] > IDENTITY_TOL:
        say("STATUS: BLOCKED-IDENTITY")
        with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return 5
    if not all(r["ok"] for r in rep):
        say("STATUS: BLOCKED-REPRODUCTION -- reported, not adjusted")
        with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return 6

    write_results(os.path.join(outdir, "D63_BOUNDS_RESULTS.csv"), c, rep, n_pairs_ok)
    write_detail(os.path.join(outdir, "D63_BOUNDS_DETAIL.csv"), c, pairs, rep)
    say("")
    say("wrote D63_BOUNDS_RESULTS.csv")
    say("wrote D63_BOUNDS_DETAIL.csv")
    say("wrote console.txt")
    say("(all three in the --outdir given on the command line; nothing is written outside this experiment directory)")
    with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
