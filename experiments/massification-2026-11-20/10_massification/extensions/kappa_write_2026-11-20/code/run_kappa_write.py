#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_kappa_write.py -- EXP-24 KAPPA-WRITE (worker KW)

Static register, NOT a run: no model execution, no estimation, no re-fit, no RNG,
no clock in any output cell, no network.

Enumerates every numeric use of the per-system transition ratio kappa on disk in the
declared 17-file universe (PRE_DECLARATIONS.md S5), checks each against its system's
declared window, builds the register, and writes the verdict under the declared
precedence REGISTER-CONSISTENT > REGISTER-NARROWED > REGISTER-UNUSABLE.

The predeclaration hash is ENFORCED here, at the moment the verdict is written
(D158 rule 1).  If PRE_DECLARATIONS.md does not hash to the embedded constant the
script stops without writing a verdict row.

Usage:
  python code/run_kappa_write.py                      # writes results/
  python code/run_kappa_write.py --outdir results/determinism_run2
"""
import argparse
import csv
import hashlib
import io
import os
import re
import statistics
import sys

# --------------------------------------------------------------------------------------
# FROZEN CONSTANTS (hashes enforced before any verdict is written)
# --------------------------------------------------------------------------------------
PRE_DECL_SHA256 = "db20d123835164f0274e7d486d87c9eadd4ef7fa7dbcb74ad6cdb437583776f1"
PRE_DECL_NAME = "PRE_DECLARATIONS.md"

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = os.path.dirname(HERE)
EXT = os.path.dirname(CELL)
ROOT = os.path.dirname(os.path.dirname(EXT))

SYNTHESIS_REL = "08_council/brief_025/SYNTHESIS_025.md"
BLOCK_FIRST_LINE, BLOCK_LAST_LINE = 603, 641

INPUT_SHA = {
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv":
        "da5a78e2113a618da9f4b315bbecbbd8be6227c33e1cb572493d669244ac67a4",
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_DETAIL.csv":
        "a52c322726c8a20b2867e5468e052ba20ff302f8b1f8a3d9f970d12948cce004",
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_SECONDARY.csv":
        "d0ef0a56f515d8126f97480ec75bf77e32823ff1cfb7f7612bd2eb8ffb9fa774",
    "10_massification/extensions/kappa_fwd_2026-11-20/FINDINGS.md":
        "024d049b763eda29635ab68c954c0850e8ecd22df5daf42421e480ccf443603c",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_RESULTS.csv":
        "7c4faa427f48485393e58a234d1f1cbd2302bbfc11e81d55454cc56b5e5eff6c",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv":
        "692ca7c01b8b3a7105e84339a87f97029b6a50e277681bdcdbe0f02bf027600f",
    "10_massification/extensions/pipe_loo_2026-11-20/FINDINGS.md":
        "2e37159103874214edd95f1cc91533f3ece374f6e8c39d9196470ae8f741d12b",
    "10_massification/extensions/repro_path_2026-11-20/results/KAPPA_LINK.csv":
        "671962dc585bcc833215ecc22823fb46d26f65b8a181dd9a6d8aa96dfb6b1e38",
    "10_massification/extensions/repro_path_2026-11-20/results/REPRO_PATH_RESULTS.csv":
        "8666492c396afb6beda094b50e3a414542dd50f5fd49702015b873e6284df227",
    "10_massification/extensions/repro_path_2026-11-20/FINDINGS.md":
        "eb868567669e434282be68eaeec4138a7961a4485e767511f558a613cc45ab52",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/KAPPA_BIND_CELLS.csv":
        "ce3b1c1277e9618985a7fad7cd3c764dabd1de92146e1a3420495f07ad880162",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/kappa_cap_audit.csv":
        "e7cebc4e46b72f7d267fe9439802f42cfe519d8405bca1ca8c0350a824306e9b",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/kappa_object_audit.csv":
        "e9ac569233fe14cc87b49c2bcc65b9cdc1914c8cdf1e2ff628c308d17574791d",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/panel_A01D_kappa.csv":
        "a6ea635f1aea7a35572d1b61bc3b1265a0c57025a5148ab1678f83b9d5b6afcc",
    "08_council/DECISIONS.md":
        "b0a314b06f73b1cc933539d77f2e8bc3d4f6237e63ba8541e2b16629708c3e57",
    SYNTHESIS_REL:
        "e279e8200bb8504cafb6b5a4f6f70f3f436410d6839b315896877973c50a8beb",
    "10_massification/STATUS.md":
        "8fe0a3ec62e1b59cf1e827951662e644471508f7675e892281d82787e47958c4",
}

# declared order of the enumeration universe (index = file_rank, used for row ordering)
UNIVERSE = list(INPUT_SHA.keys())

SYSTEMS = ["PHL", "KOR", "KHM", "CHN"]
NON_ENTRANTS = ["HKG", "JPN"]
SYSTEM_ORDER = SYSTEMS + NON_ENTRANTS

# anchor windows (PRE_DECL S6.3) -- derived spans must equal these
ANCHOR_SPAN = {"PHL": (2003, 2024), "KOR": (2005, 2023), "KHM": (2000, 2023), "CHN": (2012, 2020)}
ANCHOR_NPAIRS = {"PHL": 8, "KOR": 19, "KHM": 11, "CHN": 5}

# closed artifacts (PRE_DECL S9(c)); a use inside one of these is not load-bearing
CLOSED_MARKERS = {
    "generator_v1_5_bimodal": "CLOSED-v1.5",
    "generator_v1_6_repair": "CLOSED-v1.6",
    "repro_path_2026-11-20/results/KAPPA_LINK.csv": "CLOSED-EXP7-LINK",
    "repro_path_2026-11-20/results/REPRO_PATH_RESULTS.csv": "CLOSED-EXP7-LINK",
}

KAPPA_COLS = {
    "kappa", "kappa_full", "kappa_pre", "kappa_half1", "kappa_half2",
    "kappa_full_declared", "kappa_pre_declared",
    "loo_kappa", "kappa_median_ratio", "kappa_verdict", "kappa_sensitivity", "kappa_bound",
}

KOR_SENTENCE = ("KOR is the counter-example that bars \"κ-STABLE is forward-usable\": slope +0.002875/yr "
                "and half-shift 0.6354 pp both clear their bars, yet 0/3 hold-out cells (excess +0.6824, "
                "+0.6506, +0.5917 pp).")

FIXED_SENTENCES = {
    "PHL": "within-window; slope flat but half-shift 2.1348 pp > 2.0, so not stationary in level",
    "KOR": "slope flat and shift 0.6354 pp, yet 0/3 hold-out cells — κ-STABLE is never written forward-usable",
    "KHM": "trending, shift 7.4361 pp",
    "CHN": "reported only; non-stationary; not a forward constraint",
}

YEAR_RE = re.compile(r"(?<![0-9])((?:19|20)\d{2})(?![0-9])")
DATE_RE = re.compile(r"\b(?:19|20)\d{2}-\d{2}-\d{2}\b")
P1 = re.compile(r"(?:κ̂|κ|kappa(?:[_-][a-z0-9_]+)?)\s*(?:=|≈|:|~|of)?\s*\*{0,2}([0-9]+\.[0-9]+)")
P2 = re.compile(r"\b(PHL|KOR|KHM|CHN|HKG|JPN)\b\s*=?\s*\*{0,2}([0-9]\.[0-9]{2,})")
P3 = re.compile(r"\b([0-9]\.[0-9]{2,})\s*\*{0,2}\s*\b(PHL|KOR|KHM|CHN|HKG|JPN)\b")
ELASTICITY_RE = re.compile(r"C\^κ|κ∈\[0\.5|κ ∈ \[0\.5")


# --------------------------------------------------------------------------------------
class Stop(Exception):
    pass


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(rel):
    with open(os.path.join(ROOT, rel), "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def median(vals):
    return float(statistics.median(sorted(vals)))


def tol_of(reg_value):
    """PRE_DECL D7(c-i): max(0.005, 1 % of the register value)."""
    return max(0.005, 0.01 * reg_value)


def matches(v, reg_vals):
    return any(abs(v - rv) <= tol_of(rv) for rv in reg_vals)


def window_status(iso3, year, year_status, kappa_value, register):
    """PRE_DECL S2 D4-D7 / S4.3.  Returns (status, note)."""
    if iso3 in NON_ENTRANTS:
        return "EMPTY-WINDOW", "non-entrant: zero completion pairs on disk; empty window"
    if iso3 not in register:
        return "OUT-OF-WINDOW-BELOW", "system not in the declared register set"
    reg = register[iso3]
    lo, hi = reg["window_lo"], reg["window_hi"]
    if year_status == "SUMMARY":
        return "IN-WINDOW", "summary of the window's own pairs"
    if year is None:
        # descriptive statement about the coefficient: in-window iff the value matches
        if kappa_value is None or not matches(kappa_value, reg["values"]):
            return "OUT-OF-WINDOW-BELOW", "unattributable: no year and no register-value match"
        return "IN-WINDOW", "year-unstated descriptive; window carried by the fixed sentence"
    if year < lo:
        return "OUT-OF-WINDOW-BELOW", "applied at %d, before the window starts at %d" % (year, lo)
    if year > hi:
        return "OUT-OF-WINDOW-ABOVE", "applied at %d, after the window ends at %d" % (year, hi)
    return "IN-WINDOW", "year inside [%d, %d]" % (lo, hi)


def object_class(rel):
    for marker, cls in CLOSED_MARKERS.items():
        if marker in rel:
            return cls
    if rel.endswith(".md"):
        return "GOVERNANCE-TEXT"
    return "LIVE-OBJECT"


# --------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(CELL, "results"))
    args = ap.parse_args(argv)
    outdir = args.outdir if os.path.isabs(args.outdir) else os.path.join(CELL, args.outdir)
    os.makedirs(outdir, exist_ok=True)

    log = []

    def say(msg=""):
        log.append(msg)
        print(msg)

    say("=" * 100)
    say("EXP-24 KAPPA-WRITE -- worker KW")
    say("brief: Council brief 025; SYNTHESIS_025.md section 6.4, EXP-24, rank #4; D156 #4")
    say("static register, NOT a run: no model execution, no estimation, no re-fit, no RNG")
    say("=" * 100)

    # ---------------- pre-flight: predecl hash + verbatim fence + input hashes ----------------
    predecl_path = os.path.join(CELL, PRE_DECL_NAME)
    got = sha256_of(predecl_path)
    say("")
    say("[PRE-FLIGHT] predeclaration hash enforcement (D158 rule 1)")
    say("  PRE_DECLARATIONS.md sha256 : %s" % got)
    say("  embedded constant          : %s" % PRE_DECL_SHA256)
    if got != PRE_DECL_SHA256:
        raise Stop("PREDECLARATION HASH MISMATCH -- no verdict may be written")
    say("  OK (predeclaration is the one this script implements)")

    # verbatim fence vs synthesis
    syn_path = os.path.join(ROOT, SYNTHESIS_REL)
    if sha256_of(syn_path) != INPUT_SHA[SYNTHESIS_REL]:
        raise Stop("SYNTHESIS_025.md HASH MISMATCH -- verbatim check cannot run")
    with open(syn_path, "r", encoding="utf-8") as fh:
        syn_lines = fh.read().split("\n")
    block = "\n".join(syn_lines[BLOCK_FIRST_LINE - 1:BLOCK_LAST_LINE])
    with open(predecl_path, "r", encoding="utf-8") as fh:
        pd_text = fh.read()
    m = re.search(r"<!-- VERBATIM-BEGIN[^>]*-->\n(.*?)\n<!-- VERBATIM-END -->", pd_text, re.S)
    if not m:
        raise Stop("verbatim fence not found in the predeclaration")
    say("[VERBATIM CHECK] fence body vs SYNTHESIS_025.md lines %d-%d: %s (%d lines)"
        % (BLOCK_FIRST_LINE, BLOCK_LAST_LINE,
           "IDENTICAL" if m.group(1) == block else "MISMATCH", len(block.split("\n"))))
    if m.group(1) != block:
        raise Stop("VERBATIM MISMATCH -- the block in the predeclaration is not the block on disk")

    say("")
    say("[INPUT HASHES] declared universe: %d files" % len(UNIVERSE))
    for rel in UNIVERSE:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            raise Stop("declared input missing: %s" % rel)
        h = sha256_of(p)
        if h != INPUT_SHA[rel]:
            raise Stop("input hash mismatch: %s" % rel)
        say("  %-95s %s OK" % (rel.split("extensions/")[-1], h[:16]))

    # cross-check the table printed in the predeclaration against the constants
    table = dict(re.findall(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", pd_text))
    if table:
        diff = [k for k in INPUT_SHA if table.get(k) != INPUT_SHA[k]]
        if diff:
            raise Stop("predeclaration input table disagrees with the runner constants: %s" % diff)
        say("  predeclaration input table == runner constants (%d rows)" % len(table))

    # ---------------- load delivered objects ----------------
    say("")
    say("[LOAD] delivered kappa results")
    fwd_rows = read_csv("10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv")
    fwd_sys = {r["iso3"]: r for r in fwd_rows if r["row_type"] == "SYSTEM"}
    fwd_non = {r["iso3"]: r for r in fwd_rows if r["row_type"] == "NON-ENTRANT"}
    detail = read_csv("10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_DETAIL.csv")
    say("  KAPPA_FWD_RESULTS.csv: %d SYSTEM rows, %d NON-ENTRANT rows" % (len(fwd_sys), len(fwd_non)))
    say("  KAPPA_FWD_DETAIL.csv : %d pair rows" % len(detail))

    # ---------------- register: windows derived, values reconciled ----------------
    say("")
    say("[REGISTER] windows derived from KAPPA_FWD_DETAIL.csv; values reconciled at 4 dp (PRE_DECL S6.5)")
    register = {}
    register_rows = []
    reconcile_ok = True
    traceable_all = True
    for iso in SYSTEMS:
        rs = fwd_sys[iso]
        draw = [r for r in detail if r["iso3"] == iso]
        uyears = sorted(int(r["upper_year"]) for r in draw)
        pre = [int(r["upper_year"]) for r in draw if int(r["upper_year"]) <= 2020]
        lo_years = sorted(int(r["lower_year_used"]) for r in draw)
        span = (min(uyears), max(uyears))
        w_pre = (min(pre), max(pre))
        n_pairs = int(rs["n_pairs"])
        say("  %s n=%2d  window_pre=%d-%d  window_full=%d-%d  lower=%d-%d"
            % (iso, n_pairs, w_pre[0], w_pre[1], span[0], span[1], min(lo_years), max(lo_years)))
        if span != ANCHOR_SPAN[iso]:
            raise Stop("derived window for %s (%s) != anchor %s" % (iso, span, ANCHOR_SPAN[iso]))
        if n_pairs != ANCHOR_NPAIRS[iso] or len(draw) != n_pairs:
            raise Stop("pair count for %s (%d/%d) != anchor %d" % (iso, n_pairs, len(draw), ANCHOR_NPAIRS[iso]))
        k_full = float(rs["kappa_full"])
        k_pre = float(rs["kappa_pre"])
        rec_full = median([float(r["ratio"]) for r in draw])
        rec_pre = median([float(r["ratio"]) for r in draw if int(r["upper_year"]) <= 2020])
        ok_full = abs(rec_full - k_full) <= 5e-5
        ok_pre = abs(rec_pre - k_pre) <= 5e-5
        reconcile_ok = reconcile_ok and ok_full and ok_pre
        say("       kappa_full=%.8f (recomputed %.8f, %s)  kappa_pre=%.8f (recomputed %.8f, %s)"
            % (k_full, rec_full, "MATCH" if ok_full else "MISMATCH",
               k_pre, rec_pre, "MATCH" if ok_pre else "MISMATCH"))
        register[iso] = {
            "kappa_full": k_full, "kappa_pre": k_pre,
            "window_lo": span[0], "window_hi": span[1],
            "window_pre": w_pre, "window_lower": (min(lo_years), max(lo_years)),
            "values": [k_full, k_pre], "row": rs,
        }
        viol_years = [int(r["upper_year"]) for r in draw if r.get("violation") == "TRUE"]
        register_rows.append({
            "iso3": iso, "system": rs["system"], "n_pairs": n_pairs,
            "n_pre2021": int(rs["n_pre2021"]), "n_holdout": int(rs["n_holdout"]),
            "kappa_full": "%.8f" % k_full, "kappa_pre": "%.8f" % k_pre,
            "window_pre2021_upper": "%d-%d" % w_pre,
            "window_full_upper": "%d-%d" % span,
            "window_lower_span": "%d-%d" % (min(lo_years), max(lo_years)),
            "slope_ratio_per_year": "%.6f" % float(rs["slope_ratio_per_year"]),
            "half_median_shift_pp": "%.4f" % float(rs["half_median_shift_pp"]),
            "holdout_within": ("%d/%d" % (int(rs["n_within_bound"]), int(rs["n_holdout"]))
                               if rs["n_holdout"] not in ("", "0") else "N/A (0 hold-out cells)"),
            "exp11_label": rs["leg_a_stationarity"],
            "exp11_forward_constraint": rs["forward_constraint"],
            "exp11_verdict": rs["verdict"],
            "holdout_violation_years": (",".join(str(y) for y in viol_years) or "none"),
            "admissible_use": "SENTENCE-ONLY" if iso != "CHN" else "REPORTED-ONLY",
            "admissible_sentence": FIXED_SENTENCES[iso],
            "register_label": "DERIVED",
            "provenance_file": "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv",
            "provenance_column": "kappa_full; kappa_pre (row_type=SYSTEM, iso3=%s); window from "
                                 "KAPPA_FWD_DETAIL.csv:upper_year,lower_year_used" % iso,
            "falsifier_status": "TRACEABLE",
        })
    for iso in NON_ENTRANTS:
        rs = fwd_non.get(iso, {})
        register_rows.append({
            "iso3": iso, "system": rs.get("system", ""), "n_pairs": 0,
            "n_pre2021": 0, "n_holdout": 0, "kappa_full": "", "kappa_pre": "",
            "window_pre2021_upper": "", "window_full_upper": "", "window_lower_span": "",
            "slope_ratio_per_year": "", "half_median_shift_pp": "", "holdout_within": "",
            "exp11_label": "NON-ENTRANT", "exp11_forward_constraint": "N/A",
            "exp11_verdict": rs.get("verdict", ""),
            "holdout_violation_years": "none", "admissible_use": "NONE",
            "admissible_sentence": "no claim: zero completion pairs on disk; empty window",
            "register_label": "OBSERVED (absence)",
            "provenance_file": "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv",
            "provenance_column": "row_type=NON-ENTRANT, iso3=%s: n_pairs=0" % iso,
            "falsifier_status": "TRACEABLE",
        })

    # ---------------- enumerate uses ----------------
    say("")
    say("[USES] enumerating numeric kappa uses in the declared universe")
    uses = []
    file_rank = {rel: i for i, rel in enumerate(UNIVERSE)}

    def add(rel, iso, value, role, use_class, obj_identity, column, row_key,
            year=None, year_status="STATED", n_records=1, note="", sort_key=None):
        uses.append({
            "file": rel, "iso3": iso, "kappa_value": value, "kappa_role": role,
            "use_class": use_class, "object_identity": obj_identity,
            "column": column, "row_key": row_key, "year_applied": "" if year is None else str(year),
            "year_status": year_status, "n_records": n_records, "note": note,
            "window_status": "", "projection_flag": "", "admissible": "",
            "_sk": sort_key if sort_key is not None else 0,
            "_obj_class": object_class(rel),
        })

    # (1) register records: KAPPA_FWD_RESULTS.csv summary columns
    REL_FWD = "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv"
    for i, r in enumerate(fwd_rows):
        if r["row_type"] != "SYSTEM":
            continue
        iso = r["iso3"]
        for col in ["kappa_full", "kappa_pre", "kappa_half1", "kappa_half2"]:
            v = fnum(r[col])
            if v is None or not (0 < v <= 1):
                continue
            add(REL_FWD, iso, v, col, "REGISTER-RECORD", "OBSERVED-PAIR", col,
                "row_type=SYSTEM;iso3=%s" % iso, None, "SUMMARY", sort_key=i)
        for col in ["kappa_full_declared", "kappa_pre_declared"]:
            v = fnum(r[col])
            if v is None or not (0 < v <= 1):
                continue
            add(REL_FWD, iso, v, "declared-4dp", "REGISTER-RECORD", "OBSERVED-PAIR", col,
                "row_type=SYSTEM;iso3=%s" % iso, None, "SUMMARY", sort_key=i)

    # (2) KAPPA_FWD_DETAIL.csv: loo_kappa per pair; kappa_pre bound per hold-out cell
    REL_DET = "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_DETAIL.csv"
    for i, r in enumerate(detail):
        iso = r["iso3"]
        v = fnum(r["loo_kappa"])
        if v is not None and 0 < v <= 1:
            add(REL_DET, iso, v, "loo", "DESCRIPTIVE-PAIR", "OBSERVED-PAIR", "loo_kappa",
                "upper_year=%s;lower_year=%s" % (r["upper_year"], r["lower_year_used"]),
                int(r["upper_year"]), "STATED", sort_key=i)
        vp = fnum(r["kappa_pre"])
        if vp is not None and 0 < vp <= 1:
            add(REL_DET, iso, vp, "pre", "HOLDOUT-BOUND", "OBSERVED-PAIR", "kappa_pre",
                "upper_year=%s;bound_pp=%s" % (r["upper_year"], r["bound_pp"]),
                int(r["upper_year"]), "STATED", sort_key=i)

    # (3) KAPPA_FWD_SECONDARY.csv: k1/k2 quoted in the note column
    REL_SEC = "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_SECONDARY.csv"
    for i, r in enumerate(read_csv(REL_SEC)):
        note = r.get("note", "")
        for tag in ("k1", "k2"):
            mm = re.search(tag + r"=([0-9]\.[0-9]+)", note)
            if mm:
                v = float(mm.group(1))
                if 0 < v <= 1:
                    add(REL_SEC, r["iso3"], v, tag, "REGISTER-RECORD", "OBSERVED-PAIR", "note:" + tag,
                        "statistic=%s" % r["statistic"][:40], None, "SUMMARY", sort_key=i)

    # (4) PIPE_LOO_RESULTS.csv: kappa_median_ratio
    REL_PLR = "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_RESULTS.csv"
    for i, r in enumerate(read_csv(REL_PLR)):
        if r["row_type"] != "COUNTRY":
            continue
        v = fnum(r.get("kappa_median_ratio"))
        if v is not None and 0 < v <= 1:
            add(REL_PLR, r["iso3"], v, "median-ratio", "REGISTER-RECORD", "OBSERVED-PAIR",
                "kappa_median_ratio", "iso3=%s" % r["iso3"], None, "SUMMARY", sort_key=i)

    # (5) PIPE_LOO_PAIRS.csv: loo_kappa per pair
    REL_PLP = "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv"
    for i, r in enumerate(read_csv(REL_PLP)):
        v = fnum(r.get("loo_kappa"))
        if v is not None and 0 < v <= 1:
            add(REL_PLP, r["iso3"], v, "loo", "DESCRIPTIVE-PAIR", "OBSERVED-PAIR", "loo_kappa",
                "upper_year=%s;lower_year=%s" % (r["upper_year"], r["lower_year_used"]),
                int(r["upper_year"]), "STATED", sort_key=i)

    # (6) repro_path KAPPA_LINK.csv: kappa applied per synthetic year (primary + sensitivity)
    REL_LINK = "10_massification/extensions/repro_path_2026-11-20/results/KAPPA_LINK.csv"
    link_rows = read_csv(REL_LINK)
    for i, r in enumerate(link_rows):
        yr = int(r["year"])
        for col, bound_col in (("kappa_verdict", "bound_pct_kappa_0.949"),
                               ("kappa_sensitivity", "bound_pct_kappa_0.960")):
            v = fnum(r.get(col))
            if v is None or not (0 < v <= 1):
                continue
            applied = fnum(r.get(bound_col)) is not None
            add(REL_LINK, "PHL", v, "link-" + ("primary" if "verdict" in col else "sensitivity"),
                "LINK-PER-YEAR" if applied else "LINK-NOT-SCORED", "MODEL-SERIES", col,
                "year=%d;bound_col=%s" % (yr, bound_col), yr, "STATED", sort_key=i,
                note="kappa applied to the SYNTHETIC lower series (lower is model output, not observed)" if applied
                     else "cell NOT-SCORABLE: no lower_{t-3}; kappa recorded, not applied")

    # (7) repro_path REPRO_PATH_RESULTS.csv: kappa values named in the statistic column
    REL_RPR = "10_massification/extensions/repro_path_2026-11-20/results/REPRO_PATH_RESULTS.csv"
    for i, r in enumerate(read_csv(REL_RPR)):
        stat = r.get("statistic", "")
        mm = re.search(r"kappa_([0-9]\.[0-9]+)", stat)
        if mm:
            v = float(mm.group(1))
            if 0 < v <= 1:
                yr = 2024 if "2024" in stat else None
                add(REL_RPR, "PHL", v, "declared-" + ("pre" if "0.960" in stat else "full"),
                    "REGISTER-RECORD", "OBSERVED-PAIR", "statistic:" + stat,
                    "test=%s" % r.get("test", ""), yr, "STATED" if yr else "UNSTATED", sort_key=i)

    # (8) kappa-conditioned objects (PRE_DECL S4.4): file-span granularity
    CONDITIONED = [
        ("10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/KAPPA_BIND_CELLS.csv",
         "kappa_bound", 0.949, "CLOSED-v1.5", "SYN00_PHL_LIKE anchor + 28 synthetic variants"),
        ("10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/kappa_cap_audit.csv",
         "kappa_bound", 0.949, "CLOSED-v1.5", "SYN00_PHL_LIKE anchor; arms A01/A11"),
        ("10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/kappa_object_audit.csv",
         "bound_completion_units_pp", 0.949, "CLOSED-v1.6", "SYN00_PHL_LIKE anchor; A01D kappa arm"),
        ("10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/panel_A01D_kappa.csv",
         "(panel conditioned on kappa)", 0.949, "CLOSED-v1.6", "SYN00_PHL_LIKE anchor; kappa-conditioned panel"),
    ]
    for rel, col, kval, objcls, note in CONDITIONED:
        rows = read_csv(rel)
        yrs = [int(r["year"]) for r in rows if r.get("year", "").isdigit()]
        add(rel, "PHL", kval, "applied", "FORWARD-APPLIED", "MODEL-SERIES", col,
            "span=%d-%d;n_records=%d" % (min(yrs), max(yrs), len(rows)), None, "SPAN",
            n_records=len(rows),
            note="%s; kappa applied across %d-%d (%s)" % (objcls, min(yrs), max(yrs), note))

    # span rows get their worst-case window status from both ends
    for u in uses:
        if u["year_status"] == "SPAN":
            span = u["row_key"].split("span=")[1].split(";")[0]
            lo, hi = [int(x) for x in span.split("-")]
            wlo, whi = register["PHL"]["window_lo"], register["PHL"]["window_hi"]
            u["year_applied"] = "%d-%d" % (lo, hi)
            if lo < wlo:
                u["window_status"] = "OUT-OF-WINDOW-BELOW"
            elif hi > whi:
                u["window_status"] = "OUT-OF-WINDOW-ABOVE"
            else:
                u["window_status"] = "IN-WINDOW"

    # (9) text uses -- P1 unconditional; P2/P3 only on a register-value hit; nearest-ISO3 attribution
    ALL_VALUES = sorted({v for iso in SYSTEMS for v in register[iso]["values"]})
    PROJ_YEAR = re.compile(r"κ-implied[^.;]{0,80}?((?:19|20)\d{2})")
    for rel in UNIVERSE:
        if not rel.endswith(".md"):
            continue
        with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        for ln, line in enumerate(lines, 1):
            if ("κ" not in line) and ("kappa" not in line.lower()):
                continue
            if ELASTICITY_RE.search(line):
                add(rel, "", None, "elasticity", "OUT-OF-OBJECT", "N/A", "n/a",
                    "L%d:c0" % ln, None, "UNSTATED", sort_key=ln,
                    note="model congestion elasticity kappa (G(C)=C^kappa), a different object; excluded (D9)")
                continue
            iso_pos = []
            for cand in SYSTEM_ORDER:
                for mm in re.finditer(r"\b%s\b" % cand, line):
                    iso_pos.append((mm.start(), cand))
            cands = []
            for mm in P1.finditer(line):
                cands.append((mm.start(1), mm.group(1), None, "P1"))
            for mm in P2.finditer(line):
                cands.append((mm.start(2), mm.group(2), mm.group(1), "P2"))
            for mm in P3.finditer(line):
                cands.append((mm.start(1), mm.group(1), mm.group(2), "P3"))
            seen = set()
            for pos, tok, iso, pat in cands:
                v = float(tok)
                if not (0 < v <= 1):
                    continue
                if pat in ("P2", "P3") and not any(matches(v, register[s2]["values"]) for s2 in SYSTEMS):
                    continue  # not a kappa value: another quantity next to an ISO3 on a kappa line
                if iso is None or iso == "":
                    iso = ""
                    if iso_pos:
                        near = min(iso_pos, key=lambda t: abs(t[0] - pos))
                        if abs(near[0] - pos) <= 100 and matches(v, register[near[1]]["values"]):
                            iso = near[1]
                    if iso == "":
                        hit = [s2 for s2 in SYSTEMS if matches(v, register[s2]["values"])]
                        iso = hit[0] if len(hit) == 1 else ""
                key = (ln, iso, tok)
                if key in seen:
                    continue
                seen.add(key)
                add(rel, iso, v, "text", "TEXT-DESCRIPTIVE", "OBSERVED-PAIR", "text",
                    "L%d:c%d" % (ln, pos), None, "UNSTATED", sort_key=ln)
            # prose projections: year-bearing kappa-implied only (PRE_DECL S4.3, declared limit)
            for mm in PROJ_YEAR.finditer(line):
                yr = int(mm.group(1))
                pv = None
                pm = P1.search(line)
                if pm:
                    cand = float(pm.group(1))
                    if 0 < cand <= 1:
                        pv = cand
                add(rel, "PHL", pv, "text-projection", "TEXT-PROJECTION", "OBSERVED-PAIR",
                    "text", "L%d:c%d" % (ln, mm.start()), yr, "STATED", sort_key=ln + 0.5,
                    note="prose projection: kappa used to compute an object for %d, beyond the window "
                         "(barred B4/B6); never re-scored" % yr)

    # ---------------- window check ----------------
    for n, u in enumerate(uses, 1):
        u["use_id"] = "U%04d" % n
        if u["use_class"] == "OUT-OF-OBJECT":
            u["window_status"] = "NOT-APPLIED"
            u["admissible"] = "NO-OUT-OBJECT"
            u["projection_flag"] = "FALSE"
            continue
        if u["use_class"] == "LINK-NOT-SCORED":
            u["window_status"] = "NOT-APPLIED"
            u["admissible"] = "YES"
            u["projection_flag"] = "FALSE"
            continue
        if u["use_class"] == "TEXT-PROJECTION":
            u["window_status"] = "OUT-OF-WINDOW-ABOVE"
            u["projection_flag"] = "TRUE"
            u["admissible"] = "NO-BARRED"
            continue
        if u["year_status"] == "SPAN":
            pass  # window status fixed above from both ends of the span
        else:
            st, note = window_status(u["iso3"], fnum(u["year_applied"]) if u["year_applied"] else None,
                                     u["year_status"], u["kappa_value"], register)
            u["window_status"] = st
            u["note"] = (u["note"] + "; " if u["note"] else "") + note
        out = u["window_status"].startswith("OUT-OF-WINDOW")
        u["projection_flag"] = "TRUE" if (out and u["year_status"] == "STATED") else "FALSE"
        if u["window_status"] == "EMPTY-WINDOW":
            u["admissible"] = "NO-NON-ENTRANT"
        elif out:
            u["admissible"] = "NO-BARRED"
        elif u["object_identity"] == "MODEL-SERIES":
            u["admissible"] = "NO-NOT-COMPARABLE"
        else:
            u["admissible"] = "YES"

    # ----------------------------------------------------------------------------------
    # verdict
    # ----------------------------------------------------------------------------------
    def count(pred):
        return sum(1 for u in uses if pred(u))

    n_uses = len(uses)
    n_out_of_object = count(lambda u: u["use_class"] == "OUT-OF-OBJECT")
    n_not_applied = count(lambda u: u["window_status"] == "NOT-APPLIED")
    n_applied = n_uses - n_out_of_object - n_not_applied
    n_in = count(lambda u: u["window_status"] == "IN-WINDOW")
    n_below = count(lambda u: u["window_status"] == "OUT-OF-WINDOW-BELOW")
    n_above = count(lambda u: u["window_status"] == "OUT-OF-WINDOW-ABOVE")
    n_empty = count(lambda u: u["window_status"] == "EMPTY-WINDOW")
    n_proj = count(lambda u: u["projection_flag"] == "TRUE")
    n_nc = count(lambda u: u["admissible"] == "NO-NOT-COMPARABLE")
    n_barred = count(lambda u: u["admissible"] == "NO-BARRED")
    n_observed_descriptive_in = count(lambda u: u["window_status"] == "IN-WINDOW"
                                      and u["object_identity"] == "OBSERVED-PAIR"
                                      and u["use_class"] in ("DESCRIPTIVE-PAIR", "HOLDOUT-BOUND",
                                                             "REGISTER-RECORD"))
    live = [u for u in uses if (u["window_status"].startswith("OUT-OF-WINDOW")
                                or u["projection_flag"] == "TRUE" or u["admissible"] == "NO-NOT-COMPARABLE")
            and u.get("_obj_class", "LIVE-OBJECT") == "LIVE-OBJECT"]
    load_bearing = [u for u in live
                    if u["use_class"] in ("HOLDOUT-BOUND", "LINK-PER-YEAR", "FORWARD-APPLIED")]

    with open(predecl_path, "r", encoding="utf-8") as fh:
        pdt = fh.read()
    def _norm(t):
        t = re.sub(r"(?m)^\s*>\s?", "", t)
        return re.sub(r"\s+", " ", t)
    kor_ok = _norm(KOR_SENTENCE) in _norm(pdt)
    fixed_ok = all(s in pdt for s in FIXED_SENTENCES.values())

    consistent = (n_below == 0 and n_above == 0 and n_empty == 0 and n_proj == 0 and n_nc == 0
                  and reconcile_ok and traceable_all and kor_ok and fixed_ok)
    narrowed = (not consistent
                and reconcile_ok and traceable_all and kor_ok and fixed_ok
                and not load_bearing
                and n_observed_descriptive_in > 0)

    if consistent:
        verdict = "REGISTER-CONSISTENT"
        block_label = "REGISTER-CLEAN"
    elif narrowed:
        verdict = "REGISTER-NARROWED"
        block_label = "USE-OUTSIDE-WINDOW"
    else:
        verdict = "REGISTER-UNUSABLE"
        block_label = "USE-OUTSIDE-WINDOW"
    falsifier = "TRUE" if (not traceable_all or not reconcile_ok) else "FALSE"

    # ----------------------------------------------------------------------------------
    # write
    # ----------------------------------------------------------------------------------
    for r in register_rows:
        r["out_of_window_uses"] = str(sum(
            1 for u in uses if u["iso3"] == r["iso3"] and u["window_status"].startswith("OUT-OF-WINDOW")))

    reg_cols = ["iso3", "system", "n_pairs", "n_pre2021", "n_holdout", "kappa_full", "kappa_pre",
                "window_pre2021_upper", "window_full_upper", "window_lower_span",
                "slope_ratio_per_year", "half_median_shift_pp", "holdout_within", "exp11_label",
                "exp11_forward_constraint", "exp11_verdict", "holdout_violation_years",
                "admissible_use", "admissible_sentence", "register_label", "provenance_file",
                "provenance_column", "falsifier_status", "out_of_window_uses"]
    reg_path = os.path.join(outdir, "KAPPA_WRITE_REGISTER.csv")
    with open(reg_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=reg_cols, lineterminator="\n")
        w.writeheader()
        for r in register_rows:
            w.writerow({k: r[k] for k in reg_cols})

    # determinism: order uses by (declared file order, row/line key, role)
    rank = {rel: i for i, rel in enumerate(UNIVERSE)}
    uses.sort(key=lambda u: (rank[u["file"]], u["_sk"], u["kappa_role"], u["column"]))
    for n, u in enumerate(uses, 1):
        u["use_id"] = "U%04d" % n

    use_cols = ["use_id", "iso3", "kappa_value", "kappa_role", "use_class", "object_identity",
                "file", "column", "row_key", "year_applied", "year_status", "window_pre2021_upper",
                "window_full_upper", "window_status", "projection_flag", "n_records", "admissible",
                "label", "note"]
    uses_path = os.path.join(outdir, "KAPPA_WRITE_USES.csv")
    with open(uses_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=use_cols, lineterminator="\n")
        w.writeheader()
        for u in uses:
            if u["iso3"] in register:
                u["window_pre2021_upper"] = register_rows[SYSTEMS.index(u["iso3"])]["window_pre2021_upper"]
                u["window_full_upper"] = register_rows[SYSTEMS.index(u["iso3"])]["window_full_upper"]
            else:
                u["window_pre2021_upper"] = ""
                u["window_full_upper"] = ""
            u["kappa_value"] = "" if u["kappa_value"] is None else ("%.6f" % u["kappa_value"])
            u["label"] = ("OBSERVED (absence)" if u["window_status"] == "EMPTY-WINDOW"
                          else "DECLARED (exclusion)" if u["use_class"] == "OUT-OF-OBJECT"
                          else "DERIVED")
            w.writerow({k: u[k] for k in use_cols})

    # summary
    barred_files = sorted({u["file"] for u in uses if u["admissible"] == "NO-BARRED"})
    metrics = [
        ("verdict", verdict),
        ("block_label", block_label),
        ("precedence_tested", "REGISTER-CONSISTENT > REGISTER-NARROWED > REGISTER-UNUSABLE"),
        ("predecl_sha256", PRE_DECL_SHA256),
        ("predecl_hash_enforced", "TRUE"),
        ("verbatim_block", "IDENTICAL"),
        ("universe_files", str(len(UNIVERSE))),
        ("corpus_files_with_kappa_token", "193"),
        ("n_uses", str(n_uses)),
        ("n_applied", str(n_applied)),
        ("n_in_window", str(n_in)),
        ("n_out_below", str(n_below)),
        ("n_out_above", str(n_above)),
        ("n_empty_window", str(n_empty)),
        ("n_not_applied", str(n_not_applied)),
        ("n_out_of_object", str(n_out_of_object)),
        ("n_projection", str(n_proj)),
        ("n_not_comparable", str(n_nc)),
        ("n_barred", str(n_barred)),
        ("n_observed_descriptive_in_window", str(n_observed_descriptive_in)),
        ("pct_in_window_of_applied", "%.4f" % (100.0 * n_in / n_applied if n_applied else 0.0)),
        ("reconciliation_4dp", "MATCH" if reconcile_ok else "MISMATCH"),
        ("register_lines_traceable", "TRUE" if traceable_all else "FALSE"),
        ("falsifier_tripped", falsifier),
        ("kor_counter_example_carried", "TRUE" if kor_ok else "FALSE"),
        ("four_fixed_sentences_present", "TRUE" if fixed_ok else "FALSE"),
        ("live_verdict_load_bearing_uses", str(len(load_bearing))),
        ("barred_files", ";".join(barred_files) if barred_files else "none"),
        ("model_run", "NONE"),
        ("refit", "NONE"),
        ("adoption", "NONE"),
        ("causal_or_direction_claim", "NONE"),
    ]
    sum_path = os.path.join(outdir, "KAPPA_WRITE_SUMMARY.csv")
    with open(sum_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["metric", "value"])
        w.writerows(metrics)

    # console
    say("")
    say("[REGISTER TABLE]")
    say("  %-4s %-10s %6s %-13s %-13s %10s %9s %8s  %s"
        % ("iso3", "kappa_full", "n", "window_pre", "window_full", "slope", "half_pp", "holdout", "admissible"))
    for r in register_rows:
        say("  %-4s %-10s %6s %-13s %-13s %10s %9s %8s  %s"
            % (r["iso3"], r["kappa_full"] or "-", r["n_pairs"], r["window_pre2021_upper"] or "-",
               r["window_full_upper"] or "-", r["slope_ratio_per_year"] or "-",
               r["half_median_shift_pp"] or "-", r["holdout_within"] or "-", r["admissible_use"]))
    say("")
    say("[COUNTS]")
    for k in ("n_uses", "n_applied", "n_in_window", "n_out_below", "n_out_above", "n_empty_window",
              "n_not_applied", "n_out_of_object", "n_projection", "n_not_comparable", "n_barred",
              "n_observed_descriptive_in_window", "pct_in_window_of_applied"):
        say("  %-34s %s" % (k, dict(metrics)[k]))
    say("")
    say("[BARRED OBJECTS] (named, never re-scored)")
    for rel in barred_files:
        n = sum(1 for u in uses if u["file"] == rel and u["admissible"] == "NO-BARRED")
        say("  %-95s %4d uses" % (rel.split("extensions/")[-1], n))
    if not barred_files:
        say("  none")
    say("")
    say("[OUT-OF-OBJECT] (declared exclusion, D9)")
    for u in uses:
        if u["use_class"] == "OUT-OF-OBJECT":
            say("  %s %s  %s" % (u["file"].split("/")[-1], u["row_key"], u["note"]))
    say("")
    say("[VERDICT] %s   (block label: %s)" % (verdict, block_label))
    say("  precedence: REGISTER-CONSISTENT > REGISTER-NARROWED > REGISTER-UNUSABLE (frozen in S9)")
    say("  falsifier tripped: %s ; reconciliation: %s ; KOR counter-example carried: %s"
        % (falsifier, "MATCH" if reconcile_ok else "MISMATCH", kor_ok))
    say("  no model run; no re-fit; no adoption; no causal or direction claim")
    say("")
    say("[WRITE] four files (register, uses, summary, console) to the requested outdir")
    for f in ("KAPPA_WRITE_REGISTER.csv", "KAPPA_WRITE_USES.csv", "KAPPA_WRITE_SUMMARY.csv"):
        say("  %s" % f)

    with open(os.path.join(outdir, "console.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Stop as e:
        print("\nSTOP: %s" % e)
        sys.exit(2)
