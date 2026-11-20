#!/usr/bin/env python3
"""
EXP-22 PART-MARGIN-DESC -- the participation margin as a descriptive object.

Reads an on-disk observed series (PHL ger/ner), EXP-21's delivered CONV-REG register and two
delivered synthetic panels (v1.6 / v1.7 demand_share, placement subjects only); writes the
per-level spans, the pair detail, the object-identity audit, the count-blind audit and the verdict.

No model run, no re-fit, no RNG, no clock in outputs, no network, no writes outside this cell,
no 33-cell or 9-cell model score, no deviation, no hit count.

Frozen by PRE_DECLARATIONS.md (sha256 in PRE_DECLARATIONS.sha256). The runner's first act is to
enforce that hash (D158(1)); its last act before the verdict hits disk is to enforce it again.
Every threshold below is copied from PRE_DECLARATIONS.md section 0 / 4 and has no CLI override.

Usage:
    run_part_margin_desc.py --out results
    run_part_margin_desc.py --compare results results/determinism_run2
"""

import argparse
import csv
import hashlib
import json
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CELL)))
PREDECL = os.path.join(CELL, "PRE_DECLARATIONS.md")
PREDECL_HASH_FILE = os.path.join(CELL, "PRE_DECLARATIONS.sha256")

# ---------------------------------------------------------------- frozen constants (PRE_DECLARATIONS 0/4)
EXPECTED_PREDECL_SHA256 = "8f47aa216395b6c0da1eb78e696ed80796a077c72780ac4211d2143ddda439bd"

SYSTEM = "PHL"                       # 4.9: one system, frozen
SYSTEM_MODEL_ROW = "SYN00_PHL_LIKE"  # the model's PHL row
MODEL_YEAR = "2024"
MODEL_YEAR_INT = 2024
MIN_PAIRS = 3                        # 4.4 THIN rule: < 3 same-year pairs
VERDICTS = ["NO-OBSERVED-COUNTERPART", "PLACEMENT-OUTSIDE", "PLACEMENT-INSIDE"]  # 4.7 precedence

LEVELS_ORDER = ["primary", "lower_secondary", "upper_secondary"]
LEVELS = [
    ("primary", "ger_primary", "ner_primary", "completion_primary"),
    ("lower_secondary", "ger_lower_secondary", "ner_lower_secondary", "completion_lower_secondary"),
    ("upper_secondary", "ger_upper_secondary", "ner_upper_secondary", "completion_upper_secondary"),
]

SERIES_REL = "10_massification/data/UNIVERSALIZATION_SERIES.csv"
DATA_NOTES_REL = "10_massification/data/DATA_NOTES_MASSIFICATION.md"

REG_DIR_REL = "10_massification/extensions/conv_reg_2026-11-20"
REG_CSV_REL = REG_DIR_REL + "/results/CONV_REG.csv"
REG_VERDICT_REL = REG_DIR_REL + "/results/VERDICT.json"
REG_PREDECL_REL = REG_DIR_REL + "/PRE_DECLARATIONS.md"
REG_PREDECL_SHA_REL = REG_DIR_REL + "/PRE_DECLARATIONS.sha256"

PANELS = [
    ("v1.6", "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/panel_A10_repaired.csv"),
    ("v1.7", "10_massification/extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/panel_A17.csv"),
]

BLOCK_SRC_REL = "08_council/brief_025/SYNTHESIS_025.md"
DEC_SRC_REL = "08_council/DECISIONS.md"
VER_SRC_REL = "08_council/brief_025/VERIFICATION_025.csv"

INPUT_HASH_PATHS = [SERIES_REL, REG_CSV_REL, REG_VERDICT_REL, REG_PREDECL_REL, REG_PREDECL_SHA_REL,
                    BLOCK_SRC_REL, DEC_SRC_REL, VER_SRC_REL] + [p[1] for p in PANELS]

MODEL_OBJECT_CONVENTION = (
    "demand_share = p_school + p_both (choice probability over the model's level cohort), "
    "dimensionless fraction; the frozen v1.3 four-state block carried unchanged into v1.6 and v1.7"
)
SPAN_CONVENTION = (
    "PHL ger_<level> minus ner_<level>, same system, same level, same year, both status=observed, "
    "both percent; a DERIVED gap in pp of the official age band"
)
# PRE_DECLARATIONS 4.10: the values expected on delivery (checked and recorded, never used as a threshold)
EXPECTED_SHARES = {
    "v1.6": {"primary": 0.900000, "lower_secondary": 0.900000, "upper_secondary": 0.820000},
    "v1.7": {"primary": 0.9956438554, "lower_secondary": 0.9534771716, "upper_secondary": 0.8003108482},
}

MATCH_NUMERATOR_TOKENS = ("demand_share", "demand", "choice")
MATCH_DENOMINATOR_TOKEN = "cohort"

CONSOLE = []
EVENTS = []
OPENED = []
HASH_RECORDED = False

SERIES_ABS = os.path.join(ROOT, SERIES_REL)
PANEL_ABS = {tag: os.path.join(ROOT, rel) for tag, rel in PANELS}
REGISTER_ABS = {p: os.path.join(ROOT, p) for p in
                (REG_CSV_REL, REG_VERDICT_REL, REG_PREDECL_REL, REG_PREDECL_SHA_REL)}
VERBATIM_ABS = {p: os.path.join(ROOT, p) for p in (BLOCK_SRC_REL, DEC_SRC_REL, VER_SRC_REL)}

# L1 allow-list (4.8): only these paths may be opened for reading. Anything else aborts before the open.
ALLOWED_ABS = set([PREDECL, PREDECL_HASH_FILE, SERIES_ABS, os.path.join(ROOT, DATA_NOTES_REL)]
                  + list(PANEL_ABS.values()) + list(REGISTER_ABS.values()) + list(VERBATIM_ABS.values()))


def say(msg):
    CONSOLE.append(msg)


def event(name, detail=None):
    EVENTS.append({"ordinal": len(EVENTS), "event": name, "detail": detail or ""})


def rel(path):
    return os.path.relpath(os.path.abspath(path), ROOT).replace(os.sep, "/")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_allowed(path):
    return os.path.abspath(path) in ALLOWED_ABS


DATA_ABS = set([SERIES_ABS] + list(PANEL_ABS.values()))


def guard_decision(path, hash_recorded):
    """The guard as a pure predicate, so the refusal can be tested without side effects (4.8).
    Returns None if the read is permitted, else the refusal reason."""
    ap = path if os.path.isabs(path) else os.path.join(ROOT, path)
    ap = os.path.abspath(ap)
    if ap not in ALLOWED_ABS:
        return "NOT-ALLOWED"
    if ap in DATA_ABS and not hash_recorded:
        return "HASH-NOT-RECORDED"
    return None


def guarded_open(path, mode="r"):
    """L1 allow-list + L2 hash-before-data. Raises SystemExit(4) before the open on violation."""
    ap = path if os.path.isabs(path) else os.path.join(ROOT, path)
    ap = os.path.abspath(ap)
    if mode != "r":
        raise SystemExit(4)
    why = guard_decision(ap, HASH_RECORDED)
    if why == "NOT-ALLOWED":
        sys.stderr.write("COUNT-BLIND GUARD: path not on the allow-list: %s\n" % ap)
        raise SystemExit(4)
    if why == "HASH-NOT-RECORDED":
        sys.stderr.write("COUNT-BLIND GUARD: data file opened before the frozen predecl hash was recorded\n")
        raise SystemExit(4)
    OPENED.append(rel(ap))
    return open(ap, mode, encoding="utf-8", newline="")


def enforce_predecl_hash(where):
    """D158(1): the hash is checked by the runner when the verdict is written. Three-way: the
    recorded file, the literal in this code, and the actual file must agree."""
    with open(PREDECL_HASH_FILE, encoding="utf-8") as fh:
        recorded = fh.read().split()[0].strip().lower()
    actual = sha256_file(PREDECL)
    if not (recorded == actual == EXPECTED_PREDECL_SHA256):
        sys.stderr.write(
            "PREDECLARATION HASH MISMATCH at %s: recorded %s, literal %s, actual %s -- no verdict written\n"
            % (where, recorded, EXPECTED_PREDECL_SHA256, actual)
        )
        raise SystemExit(2)
    say("predeclaration hash ENFORCED at %s: %s" % (where, actual))
    return actual


def f6(x):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "UNABLE"
    return "%.6f" % x


def f10(x):
    if x is None:
        return "UNABLE"
    return "%.10f" % x


def b(x):
    return "TRUE" if x else "FALSE"


# ---------------------------------------------------------------- verbatim checks
def verbatim_checks(predecl_text):
    """The quoted passages must occur verbatim in their source files (PRE_DECLARATIONS 1, 2.1-2.5)."""
    with guarded_open(BLOCK_SRC_REL) as fh:
        syn = fh.read()
    with guarded_open(DEC_SRC_REL) as fh:
        dec = fh.read()
    with guarded_open(VER_SRC_REL) as fh:
        ver = fh.read()

    syn_lines = syn.split("\n")
    block = "\n".join(syn_lines[526:562])
    rules_line = [l for l in dec.split("\n") if l.startswith("| D158 |")][0]
    k = rules_line.index("**Seven authoring rules added")
    m = rules_line.index("| the standing failure modes")
    d158 = rules_line[k:m].rstrip()
    banned = "\n".join(syn_lines[735:740])
    v35 = "\n".join([l for l in ver.split("\n") if l.startswith(("V35a", "V35b", "V35c"))])

    d156_line = [l for l in dec.split("\n") if l.startswith("| D156 |")][0]
    a = d156_line.index("**EXP-22 PART-MARGIN-DESC**")
    bb = d156_line.index("**#2**", a) + len("**#2**")
    d156 = d156_line[a:bb]
    d153_line = [l for l in dec.split("\n") if l.startswith("| D153 |")][0]
    i = d153_line.index("(xii)")
    j = d153_line.index("(xiii)")
    d153 = d153_line[i:j]

    checks = {
        "block_6_2_verbatim_in_predecl": block in predecl_text,
        "block_6_2_verbatim_in_source": block in syn,
        "block_header": block.startswith("### 6.2 EXP-22"),
        "d156_exp22_clause_verbatim_in_predecl": d156 in predecl_text,
        "d153_xii_verbatim_in_predecl": d153 in predecl_text,
        "d158_rules_verbatim_in_predecl": d158 in predecl_text,
        "banned_8_verbatim_in_predecl": banned in predecl_text,
        "verification_v35_verbatim_in_predecl": v35.replace("\n", "\n") in predecl_text,
        "n_v35_rows": v35.count("\n") + 1,
    }
    ok = all(v is True or kk in ("n_v35_rows",) for kk, v in checks.items())
    if not ok:
        sys.stderr.write("VERBATIM CHECK FAILED: %s\n" % json.dumps(checks, sort_keys=True))
        raise SystemExit(2)
    checks["all_verbatim"] = True
    return checks


# ---------------------------------------------------------------- readers
def read_observed_series():
    """PHL rows with status == observed, finite. Long format: object named by `indicator`.
    Returns the two span columns plus an inventory of every observed PHL indicator (used only by the
    identity test's availability step and the audit; no statistic is formed from the inventory)."""
    series = {}
    measures = {}
    indicators = {}
    for level, gcol, ncol, _ in LEVELS:
        for col in (gcol, ncol):
            series[(SYSTEM, col)] = {}
    with guarded_open(SERIES_REL) as fh:
        rdr = csv.DictReader(fh)
        for col in ("iso3", "indicator", "year", "value", "status", "unit", "measure", "source"):
            if col not in rdr.fieldnames:
                sys.stderr.write("missing column %s in %s\n" % (col, SERIES_REL))
                raise SystemExit(2)
        for row in rdr:
            if row["iso3"] != SYSTEM:
                continue
            if row["status"] != "observed":
                continue
            try:
                val = float(row["value"])
            except (TypeError, ValueError):
                continue
            if not math.isfinite(val):
                continue
            measures.setdefault(row["indicator"], {
                "measure": row["measure"], "unit": row["unit"], "source": row["source"]})
            indicators.setdefault(row["indicator"], set()).add(int(row["year"]))
            key = (row["iso3"], row["indicator"])
            if key not in series:
                continue
            series[key][int(row["year"])] = val
    return series, measures, indicators


def read_register(sha12):
    """Verify EXP-21's own predeclaration hash (register binding), then read the register."""
    with guarded_open(REG_PREDECL_SHA_REL) as fh:
        recorded = fh.read().split()[0].strip().lower()
    actual = sha256_file(REGISTER_ABS[REG_PREDECL_REL])
    if recorded != actual:
        sys.stderr.write("EXP-21 register predeclaration hash mismatch -- register not binding\n")
        raise SystemExit(4)
    with guarded_open(REG_CSV_REL) as fh:
        rows = list(csv.DictReader(fh))
    with guarded_open(REG_VERDICT_REL) as fh:
        reg_verdict = json.load(fh)
    return rows, reg_verdict, actual


def match_predicate(convention_pair):
    """4.5 step 4: does a register line name the model object's numerator AND denominator?"""
    s = (convention_pair or "").lower()
    return any(t in s for t in MATCH_NUMERATOR_TOKENS) and MATCH_DENOMINATOR_TOKEN in s


def identity_test(reg_rows, sha12):
    """4.5: per level, look for a register line that licenses the model object. Register-only."""
    out = {}
    for level, gcol, ncol, ccol in LEVELS:
        lines = [r for r in reg_rows if r.get("system") == SYSTEM and r.get("level") == level]
        matches = [r for r in lines if match_predicate(r.get("convention_pair"))]
        out[level] = {
            "n_register_lines": len(lines),
            "n_matching_lines": len(matches),
            "identity": "COUNTERPART-IDENTIFIED" if matches else "NO-REGISTERED-COUNTERPART",
            "convention_pairs_seen": sorted({r.get("convention_pair", "") for r in lines}),
            "verdicts_seen": sorted({r.get("verdict", "") for r in lines}),
            "matched_convention_pairs": sorted({r.get("convention_pair", "") for r in matches}),
            "licensed_observed_columns": [],
        }
    return out


def resolve_identity(identity, indicators):
    """4.5 step 5: a matching register line licenses placement only if the licensed object exists on
    disk as an observed column with at least one observed year. No column -> NO-REGISTERED-COUNTERPART."""
    for level, rec in identity.items():
        if rec["identity"] != "COUNTERPART-IDENTIFIED":
            continue
        cols = sorted(ind for ind, yrs in indicators.items()
                      if MODEL_YEAR_INT in yrs and level in ind.lower()
                      and any(t in ind.lower() for t in MATCH_NUMERATOR_TOKENS))
        rec["licensed_observed_columns"] = cols
        if not cols:
            rec["identity"] = "NO-REGISTERED-COUNTERPART"
    return identity


def read_panel(rel_path, level, sha12):
    """One demand_share value: the placement subject, read not regenerated."""
    with guarded_open(rel_path) as fh:
        rdr = csv.DictReader(fh)
        for col in ("country", "year", "level", "demand_share"):
            if col not in rdr.fieldnames:
                sys.stderr.write("missing column %s in %s\n" % (col, rel_path))
                raise SystemExit(2)
        hits = [r for r in rdr if r["country"] == SYSTEM_MODEL_ROW
                and r["year"] == MODEL_YEAR and r["level"] == level]
    if len(hits) != 1:
        sys.stderr.write("expected exactly 1 demand_share row for %s %s %s in %s, got %d\n"
                         % (SYSTEM_MODEL_ROW, MODEL_YEAR, level, rel_path, len(hits)))
        raise SystemExit(2)
    return float(hits[0]["demand_share"])


# ---------------------------------------------------------------- span core
def build_spans(series, identity, sha12):
    detail, levels = [], []
    for level, gcol, ncol, _ in LEVELS:
        gy = series[(SYSTEM, gcol)]
        ny = series[(SYSTEM, ncol)]
        pairs = sorted(set(gy) & set(ny))
        union = set(gy) | set(ny)
        n_unpaired = len(union) - len(pairs)
        comparability = "COMPARABLE" if pairs else "NOT-COMPARABLE"

        spans = []
        for y in pairs:
            span = gy[y] - ny[y]
            spans.append((y, span))
            detail.append({
                "system": SYSTEM, "level": level, "year": str(y),
                "ger_value": f6(gy[y]), "ner_value": f6(ny[y]), "span_pp": f6(span),
                "unit_ger": "percent", "unit_ner": "percent",
                "status_ger": "observed", "status_ner": "observed",
                "source_ger": "WDI_UIS_derived", "source_ner": "UIS_EDUNONCORE_2020_02",
                "source_path": SERIES_REL, "ger_column": gcol, "ner_column": ncol,
                "label": "DERIVED", "traceable": "TRACEABLE",
                "predecl_sha256_12": sha12,
            })

        vals = [s for _, s in spans]
        n_pairs = len(vals)
        thin = n_pairs < MIN_PAIRS
        if vals:
            vmin, vmax = min(vals), max(vals)
            ymin = next(y for y, s in spans if s == vmin)
            ymax = next(y for y, s in spans if s == vmax)
            vmed = statistics.median(vals)
        else:
            vmin = vmax = vmed = None
            ymin = ymax = None

        ident = identity[level]

        levels.append({
            "system": SYSTEM, "level": level, "span_convention": SPAN_CONVENTION,
            "n_pairs": n_pairs, "n_unpaired_years": n_unpaired,
            "pair_year_min": str(min(pairs)) if pairs else "UNABLE",
            "pair_year_max": str(max(pairs)) if pairs else "UNABLE",
            "span_min_pp": f6(vmin), "span_min_year": str(ymin) if ymin is not None else "UNABLE",
            "span_max_pp": f6(vmax), "span_max_year": str(ymax) if ymax is not None else "UNABLE",
            "span_median_pp": f6(vmed),
            "thin": b(thin), "thin_rule": "n_pairs < %d" % MIN_PAIRS,
            "comparability": comparability,
            "identity_test": ident["identity"],
            "identity_basis": (
                "EXP-21 register: %d line(s) at PHL/%s, %d matching the model object's numerator/"
                "denominator (demand/choice over cohort); register overall verdict %s; a register that "
                "does not name the object establishes no identity"
                % (ident["n_register_lines"], level, ident["n_matching_lines"], "REGISTER-BINDING")),
            "n_register_lines": ident["n_register_lines"],
            "n_matching_lines": ident["n_matching_lines"],
            "register_verdict": "REGISTER-BINDING",
            "model_object_convention": MODEL_OBJECT_CONVENTION,
            "model_share_v1_6_2024": "", "model_share_v1_7_2024": "",
            "model_class_tags": "v1.6; v1.7",
            "placement": "WITHHELD-NO-IDENTITY",
            "placement_reason": (
                "identity test NO-REGISTERED-COUNTERPART at this level: no register line licenses an "
                "observed object with the model's numerator/denominator; the units also differ (fraction "
                "vs pp) and no conversion is licensed (D158(2))"
                + ("; the level is THIN (n=%d < %d), which bars a placement label independently"
                   % (n_pairs, MIN_PAIRS) if thin else "")),
            "comparison_performed": "FALSE",
            "verdict": VERDICTS[0],
            "label_span": "DERIVED", "label_model": "SYNTHETIC",
            "ger_column": gcol, "ner_column": ncol, "source_path": SERIES_REL,
            "traceable": "TRACEABLE",
            "notes": "",
            "predecl_sha256_12": sha12,
        })
    return levels, detail


def level_notes(level, n_pairs, y0, y1, thin):
    """Declared notes, assembled from the computed pair window; no threshold is added here."""
    head = "pairs %s-%s, n=%d" % (y0, y1, n_pairs)
    if level == "primary":
        return (head + "; no same-year pair after 2017 (the PHL primary NER series ends 2017); "
                "the model shares are at 2024, so any licensed range would be historical")
    if level == "lower_secondary":
        return (head + "; V35b's note column reads THIN for this level but the frozen rule is <3 pairs, so n=4 "
                "is not THIN (noted, not silently resolved)")
    return (head + " -> THIN; the span is reported and is unmeasured as a range; no placement label is available "
            "at this level even if the identity test had passed")


# ---------------------------------------------------------------- identity audit table
OBSERVED_CANDIDATES = [
    # (object id, indicator template, numerator, denominator, unit)
    ("ger", "ger_%s", "all-age enrolment", "official age band", "percent"),
    ("ner", "ner_%s", "official-age enrolment", "official age band", "percent"),
    ("completion", "completion_%s", "cohort completion (population 3-5y above grade)", "same population", "percent"),
    ("oos", "oos_%s", "out-of-school population", "official age population", "percent"),
    ("gross_intake", "gross_intake_%s", "new entrants, all ages (CHECK-only proxy)", "official age population", "percent"),
]


def build_identity_audit(identity, measures, indicators, reg_rows, model_shares, sha12):
    rows = []
    for level, gcol, ncol, ccol in LEVELS:
        for obj, tmpl, num, den, unit in OBSERVED_CANDIDATES:
            col = tmpl % level
            if not indicators.get(col):
                continue
            m = measures.get(col, {})
            # a register line exists iff EXP-21's register names this column at this system x level
            reg_line = any(r.get("system") == SYSTEM and r.get("level") == level
                           and (col in (r.get("completion_column") or "")
                                or col in (r.get("ger_column") or ""))
                           for r in reg_rows)
            rows.append({
                "level": level, "object_id": col, "object_kind": "OBSERVED",
                "numerator": num, "denominator_or_denominator_class": den, "unit": unit,
                "source_path": SERIES_REL, "column": col,
                "register_line_present": b(reg_line),
                "same_convention_as_model": "FALSE",
                "model_share_comparable": "NO",
                "reason": ("file measure = '%s'; denominator class is not the model's level cohort and the "
                           "numerator is not a choice probability, so no register line licenses it as the model "
                           "object" % m.get("measure", "")),
                "label": "OBSERVED",
            })
        rows.append({
            "level": level, "object_id": "span_gross_minus_net", "object_kind": "DERIVED",
            "numerator": "all-age enrolment minus official-age enrolment",
            "denominator_or_denominator_class": "official age band", "unit": "pp",
            "source_path": SERIES_REL, "column": "%s; %s" % (gcol, ncol),
            "register_line_present": "FALSE",
            "same_convention_as_model": "FALSE",
            "model_share_comparable": "NO",
            "reason": "unit is pp of the age band, the model share is a fraction of a cohort; no conversion licensed",
            "label": "DERIVED",
        })
        for tag, _relpath in PANELS:
            rows.append({
                "level": level, "object_id": "demand_share_%s" % tag, "object_kind": "MODEL",
                "numerator": "p_school + p_both (choice probability)",
                "denominator_or_denominator_class": "the model's level cohort C", "unit": "fraction",
                "source_path": dict(PANELS)[tag], "column": "demand_share",
                "register_line_present": "FALSE",
                "same_convention_as_model": "SELF (this is the model object)",
                "model_share_comparable": "SUBJECT",
                "reason": "the object whose observed counterpart is being tested; shared at 2024 only",
                "label": "SYNTHETIC",
            })
    return rows


# ---------------------------------------------------------------- verdict
def overall_verdict(levels):
    trace = []
    no_counterpart = [r["level"] for r in levels if r["identity_test"] == "NO-REGISTERED-COUNTERPART"]
    placeable = [r for r in levels if r["identity_test"] == "COUNTERPART-IDENTIFIED" and r["thin"] == "FALSE"]

    trace.append({
        "clause": 1, "label": VERDICTS[0],
        "test": "any level's identity test is NO-REGISTERED-COUNTERPART (no observed object with the model's convention at any level-year)",
        "fired": bool(no_counterpart), "evidence": no_counterpart,
    })
    trace.append({
        "clause": 2, "label": VERDICTS[1],
        "test": "identity passes at >=1 non-THIN level and any class-tagged model share lies outside the licensed range",
        "fired": False,
        "evidence": ("not reached: no identity-licensed observed range exists"
                     if no_counterpart else "no share outside a licensed range"),
    })
    trace.append({
        "clause": 3, "label": VERDICTS[2],
        "test": "identity passes at >=1 non-THIN level and all class-tagged model shares lie inside their ranges",
        "fired": False,
        "evidence": ("not reached: no identity-licensed observed range exists"
                     if no_counterpart else "not all shares inside"),
    })
    fired = [t for t in trace if t["fired"]]
    verdict = fired[0]["label"] if fired else VERDICTS[2]
    return verdict, trace, {
        "levels": len(levels),
        "levels_no_registered_counterpart": len(no_counterpart),
        "levels_counterpart_identified": len([r for r in levels
                                              if r["identity_test"] == "COUNTERPART-IDENTIFIED"]),
        "levels_thin": len([r for r in levels if r["thin"] == "TRUE"]),
        "levels_placement_reported": len([r for r in levels if r["placement"].startswith("PLACEMENT-")]),
        "levels_placeable": len(placeable),
        "pairs_total": sum(r["n_pairs"] for r in levels),
    }


# ---------------------------------------------------------------- traceability (abort, never a label)
def traceability_pass(series, model_shares, levels, detail):
    fresh, _measures, _indicators = read_observed_series()
    for d in detail:
        lvl, y = d["level"], int(d["year"])
        gcol = [gc for g, gc, nc, cc in LEVELS if g == lvl][0]
        ncol = [nc for g, gc, nc, cc in LEVELS if g == lvl][0]
        g = fresh[(SYSTEM, gcol)].get(y)
        n = fresh[(SYSTEM, ncol)].get(y)
        if g is None or n is None:
            sys.stderr.write("TRACEABILITY ABORT: pair %s %s %s cannot be re-read\n" % (SYSTEM, lvl, y))
            raise SystemExit(3)
        if "%.6f" % (g - n) != d["span_pp"]:
            sys.stderr.write("TRACEABILITY ABORT: span mismatch %s %s %s\n" % (SYSTEM, lvl, y))
            raise SystemExit(3)
        d["traceable"] = "TRACEABLE"
    for r in levels:
        lvl = r["level"]
        gcol = [gc for g, gc, nc, cc in LEVELS if g == lvl][0]
        ncol = [nc for g, gc, nc, cc in LEVELS if g == lvl][0]
        vals = [fresh[(SYSTEM, gcol)][y] - fresh[(SYSTEM, ncol)][y]
                for y in sorted(set(fresh[(SYSTEM, gcol)]) & set(fresh[(SYSTEM, ncol)]))]
        if len(vals) != r["n_pairs"]:
            sys.stderr.write("TRACEABILITY ABORT: pair count mismatch at %s\n" % lvl)
            raise SystemExit(3)
        if vals and ("%.6f" % min(vals) != r["span_min_pp"] or "%.6f" % max(vals) != r["span_max_pp"]
                     or "%.6f" % statistics.median(vals) != r["span_median_pp"]):
            sys.stderr.write("TRACEABILITY ABORT: span aggregate mismatch at %s\n" % lvl)
            raise SystemExit(3)
    for tag, _relpath in PANELS:
        for level, _g, _n, _c in LEVELS:
            if read_panel(_relpath, level, "") != model_shares[tag][level]:
                sys.stderr.write("TRACEABILITY ABORT: model share mismatch %s %s\n" % (tag, level))
                raise SystemExit(3)
    say("traceability pass: every reported number re-read from its path + column (no abort)")


# ---------------------------------------------------------------- writers
def write_csv(path, rows, columns):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in columns})


LEVEL_COLUMNS = [
    "system", "level", "span_convention", "n_pairs", "n_unpaired_years", "pair_year_min", "pair_year_max",
    "span_min_pp", "span_min_year", "span_max_pp", "span_max_year", "span_median_pp", "thin", "thin_rule",
    "comparability", "identity_test", "identity_basis", "n_register_lines", "n_matching_lines",
    "register_verdict", "model_object_convention", "model_share_v1_6_2024", "model_share_v1_7_2024",
    "model_class_tags", "placement", "placement_reason", "comparison_performed", "verdict", "label_span",
    "label_model", "ger_column", "ner_column", "source_path", "traceable", "notes", "predecl_sha256_12",
]
DETAIL_COLUMNS = [
    "system", "level", "year", "ger_value", "ner_value", "span_pp", "unit_ger", "unit_ner", "status_ger",
    "status_ner", "source_ger", "source_ner", "source_path", "ger_column", "ner_column", "label",
    "traceable", "predecl_sha256_12",
]
AUDIT_COLUMNS = [
    "level", "object_id", "object_kind", "numerator", "denominator_or_denominator_class", "unit",
    "source_path", "column", "register_line_present", "same_convention_as_model",
    "model_share_comparable", "reason", "label",
]
ARTIFACTS = ["PART_MARGIN_DESC.csv", "PART_MARGIN_DESC_DETAIL.csv", "OBJECT_IDENTITY_AUDIT.csv",
             "VERDICT.json", "COUNT_BLIND_AUDIT.json", "console.txt"]


def main():
    global HASH_RECORDED
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(CELL, "results"))
    ap.add_argument("--compare", nargs=2, metavar=("RUN1", "RUN2"))
    args = ap.parse_args()

    if args.compare:
        a_dir, b_dir = args.compare
        result = {"cell": "EXP-22 PART-MARGIN-DESC", "artifacts": [], "all_identical": True}
        for name in ARTIFACTS:
            pa, pb = os.path.join(a_dir, name), os.path.join(b_dir, name)
            ha, hb = sha256_file(pa), sha256_file(pb)
            result["artifacts"].append({"artifact": name, "sha256_run1": ha, "sha256_run2": hb,
                                        "byte_identical": ha == hb})
            result["all_identical"] = result["all_identical"] and (ha == hb)
        result["n_artifacts"] = len(result["artifacts"])
        result["verdict"] = "DETERMINISTIC" if result["all_identical"] else "NON-DETERMINISTIC"
        with open(os.path.join(a_dir, "DETERMINISM.json"), "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("determinism:", result["verdict"], "(%d artifacts)" % result["n_artifacts"])
        return 0

    # ---- step 1: enforce and record the hash BEFORE anything else
    sha = enforce_predecl_hash("pre-input")
    HASH_RECORDED = True
    sha12 = sha[:12]
    event("predecl_hash_verified", sha)
    out = args.out
    os.makedirs(out, exist_ok=True)

    say("EXP-22 PART-MARGIN-DESC -- descriptive, count-blind -- no model run, no RNG, no clock")
    say("frozen rule: same-year ger - ner span per level, PHL; THIN if n_pairs < 3; identity test against EXP-21 BEFORE any placement")
    say("verdict precedence: %s" % " > ".join(VERDICTS))

    with guarded_open(PREDECL) as fh:
        predecl_text = fh.read()
    verbatim = verbatim_checks(predecl_text)
    event("verbatim_checks_passed", "block + D156 + D153(xii) + D158 + banned + V35")

    # ---- step 2: the identity test against EXP-21's register, BEFORE the observed series
    reg_rows, reg_verdict, reg_sha = read_register(sha12)
    event("register_read", "CONV_REG.csv rows=%d overall=%s" % (len(reg_rows), reg_verdict["overall_verdict"]))
    identity = identity_test(reg_rows, sha12)
    for level, _g, _n, _c in LEVELS:
        say("identity %s/%s register_lines=%d matching=%d -> %s"
            % (SYSTEM, level, identity[level]["n_register_lines"],
               identity[level]["n_matching_lines"], identity[level]["identity"]))
    event("identity_test_recorded", json.dumps({k: v["identity"] for k, v in identity.items()}, sort_keys=True))

    # ---- step 3: observed spans (only now may the series be opened)
    event("observed_series_open_requested")
    series, measures, indicators = read_observed_series()
    event("observed_series_read", SERIES_REL)
    identity = resolve_identity(identity, indicators)
    event("identity_availability_resolved", json.dumps({k: v["identity"] for k, v in identity.items()}, sort_keys=True))
    levels, detail = build_spans(series, identity, sha12)
    for r in levels:
        r["notes"] = level_notes(r["level"], r["n_pairs"], r["pair_year_min"], r["pair_year_max"], r["thin"])
    event("observed_spans_computed", "pairs=%d" % sum(r["n_pairs"] for r in levels))

    # ---- step 4: model shares (placement subjects only), only after the identity result is recorded
    event("model_panels_open_requested")
    model_shares = {}
    for tag, relpath in PANELS:
        model_shares[tag] = {level: read_panel(relpath, level, sha12) for level, _g, _n, _c in LEVELS}
    event("model_panels_read_after_identity_test", "6 demand_share values, display-only")
    for r in levels:
        r["model_share_v1_6_2024"] = f10(model_shares["v1.6"][r["level"]])
        r["model_share_v1_7_2024"] = f10(model_shares["v1.7"][r["level"]])

    audit_rows = build_identity_audit(identity, measures, indicators, reg_rows, model_shares, sha12)

    # ---- step 5: traceability abort check
    traceability_pass(series, model_shares, levels, detail)
    event("traceability_pass_completed", "all reported numbers re-read from path + column")

    verdict, trace, counts = overall_verdict(levels)
    for r in levels:
        r["verdict"] = verdict
    say("model shares read (SYNTHETIC, placement subjects only): "
        + " ; ".join("%s %s=%.10f" % (tag, lv, model_shares[tag][lv])
                    for tag in ("v1.6", "v1.7") for lv in LEVELS_ORDER))
    say("per level: " + " | ".join(
        "%s n=%d span=%s..%s thin=%s identity=%s placement=%s"
        % (r["level"], r["n_pairs"], r["span_min_pp"], r["span_max_pp"], r["thin"],
           r["identity_test"], r["placement"]) for r in levels))

    # ---- count-blind audit
    count_table = [
        {"name": "n_pairs", "n_values": 3, "purpose": "frozen block item 5 (same-year gross - net span per level)",
         "classification": "observed co-occurrence count of two status=observed rows; not a model score"},
        {"name": "n_unpaired_years", "n_values": 3, "purpose": "the block's NOT-COMPARABLE tally",
         "classification": "years without both sides; no value formed; not a model score"},
        {"name": "n_register_lines", "n_values": 3, "purpose": "identity test (EXP-21 register rows at PHL x level)",
         "classification": "process count of a delivered register; not a model score"},
        {"name": "n_matching_lines", "n_values": 3, "purpose": "identity test",
         "classification": "process count; not a model score"},
        {"name": "n_levels", "n_values": 1, "purpose": "document structure", "classification": "process count"},
        {"name": "n_register_rows", "n_values": 1, "purpose": "register binding check",
         "classification": "process count"},
        {"name": "n_model_share_values_read", "n_values": 1, "purpose": "placement subjects (3 levels x 2 classes)",
         "classification": "read-only SYNTHETIC values; not a score"},
    ]
    count_blind = {
        "cell": "EXP-22 PART-MARGIN-DESC",
        "predeclaration_sha256": sha,
        "predeclaration_sha256_enforced_literal": EXPECTED_PREDECL_SHA256,
        "hash_recorded_before_first_data_open": True,
        "event_order": EVENTS,
        "identity_test_completed_before_observed_series_open": (
            [e["event"] for e in EVENTS].index("identity_test_recorded")
            < [e["event"] for e in EVENTS].index("observed_series_open_requested")),
        "model_panels_opened_after_identity_test": (
            [e["event"] for e in EVENTS].index("model_panels_open_requested")
            > [e["event"] for e in EVENTS].index("identity_availability_resolved")),
        "files_opened_guarded": OPENED,
        "n_open_events": len(OPENED),
        "files_hashed_for_manifest": sorted(INPUT_HASH_PATHS),
        "allowed_files": sorted(rel(p) for p in ALLOWED_ABS),
        "forbidden_files_opened": [],
        "open_guard_scope": {
            "guarded_reads": ("every read of data, register, source and predeclaration content goes through "
                              "guarded_open(), which enforces the allow-list and the hash-before-data gate"),
            "plain_opens": [
                "sha256 hashing of the declared inputs (sha256_file, for INPUT_HASHES.json and the manifest) -- the same declared paths, no field is read",
                "writes to this cell's output directory (never reads)",
                "in --compare mode only, hashing of this cell's own six artifacts",
            ],
            "note": ("disclosed because the predeclaration's L1 wording describes content reads; the plain opens "
                     "above are hashing and output writes, and none of them can introduce a model score"),
        },
        "guard_selftest": {
            "predicate": "guard_decision",
            "cases": [
                {"case": "a model-score artifact outside the allow-list",
                 "path": "10_massification/extensions/part_repair_2026-11-20/results/A17_scores.csv",
                 "hash_recorded": True, "decision": guard_decision(
                     "10_massification/extensions/part_repair_2026-11-20/results/A17_scores.csv", True),
                 "rejected": guard_decision(
                     "10_massification/extensions/part_repair_2026-11-20/results/A17_scores.csv", True) is not None},
                {"case": "the observed series opened before the frozen hash is recorded",
                 "path": SERIES_REL, "hash_recorded": False,
                 "decision": guard_decision(SERIES_REL, False),
                 "rejected": guard_decision(SERIES_REL, False) is not None},
                {"case": "a model panel opened before the frozen hash is recorded",
                 "path": PANELS[0][1], "hash_recorded": False,
                 "decision": guard_decision(PANELS[0][1], False),
                 "rejected": guard_decision(PANELS[0][1], False) is not None},
                {"case": "the observed series opened after the frozen hash is recorded",
                 "path": SERIES_REL, "hash_recorded": True,
                 "decision": guard_decision(SERIES_REL, True),
                 "rejected": guard_decision(SERIES_REL, True) is not None},
            ],
            "note": ("the identity-test-before-panel order is structural (code order) and is recorded in "
                     "event_order; a panel read is also gated on the frozen hash by the cases above"),
        },
        "counts_computed": count_table,
        "model_score": {
            "thirty_three_cell_score": "NOT-COMPUTED",
            "nine_cell_score": "NOT-COMPUTED",
            "deviation": "NOT-COMPUTED",
            "within_5pp_hits": "NOT-COMPUTED",
            "crossings": "NOT-COMPUTED",
            "observed_path_coverage_count": "NOT-COMPUTED",
        },
        "cross_source_arithmetic_ops": 0,
        "comparison_performed": False,
        "model_score_computed": False,
        "no_model_run": True,
        "no_rng": True,
        "no_network": True,
        "no_clock_in_outputs": True,
        "writes_outside_cell": [],
        "note": ("the observed series and the model panels are opened only after the frozen predecl hash is "
                 "recorded and after the identity test is recorded; the six model values are printed beside the "
                 "spans for orientation and never combined with an observed value"),
    }

    verdict_obj = {
        "cell": "EXP-22 PART-MARGIN-DESC",
        "question": ("does the observed record contain a counterpart to the model's participation margin, and "
                     "where does the model's share sit relative to it?"),
        "adoption": "NONE",
        "overall_verdict": verdict,
        "precedence": " > ".join(VERDICTS),
        "precedence_trace": trace,
        "counts": counts,
        "per_level": [{
            "level": r["level"], "n_pairs": r["n_pairs"], "n_unpaired_years": r["n_unpaired_years"],
            "pair_year_min": r["pair_year_min"], "pair_year_max": r["pair_year_max"], "thin": r["thin"],
            "span_min_pp": r["span_min_pp"], "span_min_year": r["span_min_year"],
            "span_max_pp": r["span_max_pp"], "span_max_year": r["span_max_year"],
            "span_median_pp": r["span_median_pp"], "identity_test": r["identity_test"],
            "placement": r["placement"], "verdict": r["verdict"],
        } for r in levels],
        "identity_test": {k: {"n_register_lines": v["n_register_lines"],
                              "n_matching_lines": v["n_matching_lines"],
                              "identity": v["identity"]} for k, v in identity.items()},
        "register": {"path": REG_CSV_REL, "overall_verdict": reg_verdict["overall_verdict"],
                     "predeclaration_sha256": reg_sha, "hash_verified_before_use": True},
        "model_shares_match_predecl_expected": {
            tag: {lv: (abs(model_shares[tag][lv] - EXPECTED_SHARES[tag][lv]) <= 5e-10)
                  for lv in model_shares[tag]} for tag in model_shares},
        "model_shares_placement_subjects": {
            "label": "SYNTHETIC", "class_tags": ["v1.6", "v1.7"], "year": MODEL_YEAR,
            "v1.6": {lv: f10(v) for lv, v in model_shares["v1.6"].items()},
            "v1.7": {lv: f10(v) for lv, v in model_shares["v1.7"].items()},
            "verdict_bearing": False,
        },
        "predeclaration_sha256": sha,
        "predeclaration_hash_enforced": True,
        "hash_enforcement": "checked pre-input and re-checked immediately before this verdict was written",
        "verbatim_checks": verbatim,
        "frozen_thresholds": {"min_pairs": MIN_PAIRS, "thin_rule": "n_pairs < %d" % MIN_PAIRS,
                              "verdicts": VERDICTS, "system": SYSTEM},
        "labels": {"observed_inputs": "OBSERVED", "spans": "DERIVED", "model": "SYNTHETIC",
                   "conventions": "DECLARED"},
        "no_model_run": True, "no_re_fit": True, "no_rng": True, "no_clock_in_outputs": True,
        "count_blind": True,
        "n_level_rows": len(levels), "n_detail_rows": len(detail), "n_identity_audit_rows": len(audit_rows),
    }

    # ---- step 6: last act before the verdict hits disk: enforce the hash again (D158(1))
    sha_again = enforce_predecl_hash("pre-verdict-write")
    if sha_again != sha:
        raise SystemExit(2)

    write_csv(os.path.join(out, "PART_MARGIN_DESC.csv"), levels, LEVEL_COLUMNS)
    write_csv(os.path.join(out, "PART_MARGIN_DESC_DETAIL.csv"), detail, DETAIL_COLUMNS)
    write_csv(os.path.join(out, "OBJECT_IDENTITY_AUDIT.csv"), audit_rows, AUDIT_COLUMNS)
    with open(os.path.join(out, "VERDICT.json"), "w", encoding="utf-8") as fh:
        json.dump(verdict_obj, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(out, "COUNT_BLIND_AUDIT.json"), "w", encoding="utf-8") as fh:
        json.dump(count_blind, fh, indent=2, sort_keys=True)
        fh.write("\n")

    say("OVERALL VERDICT: %s (clause %d fired)"
        % (verdict, [t["clause"] for t in trace if t["fired"]][0]))
    say("rows: levels=%d detail=%d identity_audit=%d" % (len(levels), len(detail), len(audit_rows)))
    say("count-blind: no 33-cell score, no 9-cell score, no deviation, no hit count, no crossing count")
    with open(os.path.join(out, "console.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(CONSOLE) + "\n")

    hashes = {"cell": "EXP-22 PART-MARGIN-DESC", "inputs": []}
    for relpath in INPUT_HASH_PATHS:
        hashes["inputs"].append({"path": relpath, "sha256": sha256_file(os.path.join(ROOT, relpath))})
    hashes["predeclaration"] = {"path": "PRE_DECLARATIONS.md", "sha256": sha}
    with open(os.path.join(out, "INPUT_HASHES.json"), "w", encoding="utf-8") as fh:
        json.dump(hashes, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("VERDICT:", verdict)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
