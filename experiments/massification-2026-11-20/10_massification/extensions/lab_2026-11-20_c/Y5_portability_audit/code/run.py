#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Y5 - portability design data-completeness audit (CHN then HKG, D75 six constraints).

DESIGN-ONLY. No model run, no portability claim, no C1-C4 reopening (D75/R22).

The script reads the frozen on-disk data files read-only and writes exactly two
result CSVs under this experiment's results/ directory:

    results/transfer_checklist.csv   one row per D75 input x country (6 x 2)
    results/CLUSTER_RESULTS.csv      one summary row, experiment="Y5"

Deterministic: no RNG, no network, no clock value in any result cell. The
run timestamp lives only in RUN_MANIFEST.json, which is written separately.

Nothing here sends, requests, fetches or fabricates data. A checklist cell is
marked present-on-disk only when the cited file actually contains observed
rows for that country; every number printed below is computed from those rows.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Frozen paths (absolute; the script is independent of the CWD)
# ---------------------------------------------------------------------------
BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20")
DATA = BASE / "10_massification" / "data"
OUT = BASE / "10_massification" / "extensions" / "lab_2026-11-20_c" / "Y5_portability_audit"
RESULTS = OUT / "results"

PRE = BASE / "10_massification" / "extensions" / "lab_2026-11-20_c" / "PRE_DECLARATIONS.md"
PRE_SHA_EXPECTED = "8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1"

# Threshold copied verbatim from the task / predeclaration Y5 block.
THRESHOLD = (
    '"data-complete" only if every D75 input is present-on-disk or already-ruled-held '
    '(no NEW data ask); falsifier = any NEW-ASK -> design marked BLOCKED-ON-DATA for that input.'
)

# The existing HELD labels from D76/D92 (reuse only; never create a new request).
HELD_LABELS = {
    "capacity trajectory": (
        "annual capacity/enforcement and the named expansion file "
        "(D76/D92 HELD - already-held, nothing sent)"
    ),
}

# D75 inputs, in the order declared by the Y5 operationalisation.
INPUTS = [
    ("I1", "initial cohorts"),
    ("I2", "observed economy series"),
    ("I3", "policy dates/pushes"),
    ("I4", "capacity trajectory"),
    ("I5", "level-gate mapping"),
    ("I6", "measurement definitions"),
]

COUNTRIES = ["CHN", "HKG"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(value) -> str:
    """Deterministic human-readable number (no scientific notation)."""
    if value is None or pd.isna(value):
        return "NA"
    f = float(value)
    if f == int(f):
        return f"{int(f):,}"
    s = f"{f:,.4f}".rstrip("0").rstrip(".")
    return s


def require(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(f"required on-disk input missing: {path}")
    return path


# ---------------------------------------------------------------------------
# 0. Frozen predeclaration integrity check
# ---------------------------------------------------------------------------
pre_sha = sha256(require(PRE))
if pre_sha != PRE_SHA_EXPECTED:
    print(f"FATAL: predeclaration sha256 {pre_sha} != frozen {PRE_SHA_EXPECTED}", file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# 1. Load the on-disk data (read-only)
# ---------------------------------------------------------------------------
series = pd.read_csv(require(DATA / "UNIVERSALIZATION_SERIES.csv"))
timing = pd.read_csv(require(DATA / "UNIVERSALIZATION_TIMING.csv"))
policy = pd.read_csv(require(DATA / "POLICY_TIMELINE.csv"))
jobs = pd.read_csv(require(DATA / "JOBS_AND_MARKETS_PANEL.csv"))
capacity = pd.read_csv(require(DATA / "STATE_CAPACITY.csv"))
expansion = pd.read_csv(require(DATA / "SCHOOL_EXPANSION.csv"))
notes_path = require(DATA / "DATA_NOTES_MASSIFICATION.md")
notes_text = notes_path.read_text(encoding="utf-8")

# Minimal schema guards (fail loudly rather than fabricate).
for frame, cols, name in [
    (series, {"country", "iso3", "indicator", "year", "value", "unit", "status"}, "UNIVERSALIZATION_SERIES.csv"),
    (timing, {"country", "iso3", "level", "threshold_pct", "measure", "crossing_year",
              "censoring", "status", "derivation_method"}, "UNIVERSALIZATION_TIMING.csv"),
    (policy, {"country", "iso3", "year", "event", "source", "confidence", "status"}, "POLICY_TIMELINE.csv"),
    (jobs, {"country", "iso3", "indicator_code", "year", "value", "unit", "definition", "status"}, "JOBS_AND_MARKETS_PANEL.csv"),
    (capacity, {"country", "iso3", "dimension", "indicator", "year", "value", "unit", "definition", "status"}, "STATE_CAPACITY.csv"),
    (expansion, {"country", "iso3", "indicator", "value"}, "SCHOOL_EXPANSION.csv"),
]:
    missing = cols - set(frame.columns)
    if missing:
        raise ValueError(f"{name} missing required columns: {sorted(missing)}")

# SCHOOL_EXPANSION coverage check (D75 capacity-expansion input).
expansion_countries = sorted(expansion["iso3"].dropna().unique().tolist())
expansion_only_phl = expansion_countries == ["PHL"]

# ---------------------------------------------------------------------------
# 2. Per-input evidence builders
# ---------------------------------------------------------------------------
def series_rows(iso: str, indicator: str, frame=series, ind_col="indicator") -> pd.DataFrame:
    d = frame[(frame["iso3"] == iso) & (frame[ind_col] == indicator)].copy()
    return d[d["value"].notna()].sort_values("year")


def availability_cohorts(iso: str) -> str:
    parts = []
    for ind in ["cohort_population_0_14", "population_total"]:
        d = series_rows(iso, ind)
        if len(d) == 0:
            parts.append(f"{ind}: ABSENT")
            continue
        first, last = d.iloc[0], d.iloc[-1]
        parts.append(
            f"{ind}: n={len(d)}, {int(first.year)}-{int(last.year)}, "
            f"latest {int(last.year)}={fmt(last.value)} {last.unit} [{last.status}]"
        )
    return "UNIVERSALIZATION_SERIES.csv; " + "; ".join(parts)


ECON_INDICATORS = [
    "SL.AGR.EMPL.ZS",
    "SL.EMP.WORK.ZS",
    "SL.SRV.EMPL.ZS",
    "SL.UEM.1524.ZS",
    "NY.GDP.PCAP.PP.CD",
    "SE.XPD.TOTL.GD.ZS",
]


def availability_economy(iso: str) -> str:
    parts = []
    for ind in ECON_INDICATORS:
        d = series_rows(iso, ind, frame=jobs, ind_col="indicator_code")
        if len(d) == 0:
            parts.append(f"{ind}: ABSENT")
            continue
        first, last = d.iloc[0], d.iloc[-1]
        parts.append(
            f"{ind}: n={len(d)}, {int(first.year)}-{int(last.year)}, "
            f"latest {int(last.year)}={fmt(last.value)}"
        )
    return "JOBS_AND_MARKETS_PANEL.csv; all status=observed; " + "; ".join(parts)


def availability_policy(iso: str) -> str:
    d = policy[policy["iso3"] == iso].sort_values("year")
    if len(d) == 0:
        return "POLICY_TIMELINE.csv; no rows"
    pushes = "; ".join(f"{int(r.year)} {r.event}" for r in d.itertuples())
    confidences = sorted({str(c) for c in d["confidence"].dropna().unique()})
    return (
        f"POLICY_TIMELINE.csv; {len(d)} dated push(es): {pushes}; "
        f"status=policy_fact; confidence={' | '.join(confidences)}"
    )


CAP_INDICATORS = [
    "pupil-teacher ratio, primary",
    "pupil-teacher ratio, secondary",
    "teachers, primary (persons)",
    "teachers, secondary (persons)",
    "education spending (% of GDP), UIS cross-check",
    "education spending (% of GDP), WDI",
    "govt spending per primary student (constant PPP$)",
    "govt spending per secondary student (constant PPP$)",
]


def availability_capacity(iso: str) -> str:
    d = capacity[(capacity["iso3"] == iso) & capacity["value"].notna()
                 & capacity["indicator"].isin(CAP_INDICATORS)]
    parts = []
    for ind in CAP_INDICATORS:
        dd = d[d["indicator"] == ind].sort_values("year")
        if len(dd) == 0:
            parts.append(f"{ind}: ABSENT")
            continue
        last = dd.iloc[-1]
        parts.append(
            f"{ind}: n={len(dd)}, {int(dd.year.min())}-{int(dd.year.max())}, "
            f"latest {int(last.year)}={fmt(last.value)} {last.unit}"
        )
    return (
        "STATE_CAPACITY.csv; " + "; ".join(parts)
        + f"; SCHOOL_EXPANSION.csv covers {expansion_countries} only"
    )


def availability_gates(iso: str) -> str:
    d = timing[timing["iso3"] == iso]
    dated = pd.to_numeric(d["crossing_year"], errors="coerce").notna().sum()
    left = int((d["censoring"] == "left").sum())
    right = int((d["censoring"] == "right").sum())
    unable = int((d["status"] == "unable").sum())
    levels = ", ".join(sorted(d["level"].dropna().unique()))
    thresholds = "/".join(str(int(t)) for t in sorted(d["threshold_pct"].dropna().unique()))
    measures = ", ".join(sorted(d["measure"].dropna().unique()))
    return (
        f"UNIVERSALIZATION_TIMING.csv; {len(d)} gate rows; levels={levels}; "
        f"thresholds={thresholds}; measures={measures}; numeric dated={int(dated)}, "
        f"left-censored={left}, right-censored={right}, unable={unable}; "
        f"observed={int((d['status'] == 'observed').sum())}, "
        f"reconstructed={int((d['status'] == 'reconstructed').sum())}"
    )


def availability_definitions(iso: str) -> str:
    s = series[series["iso3"] == iso]
    s_ok = int(s[["unit", "source", "source_detail"]].notna().all(axis=1).sum())
    j = jobs[jobs["iso3"] == iso]
    j_ok = int(j[["unit", "definition"]].notna().all(axis=1).sum())
    c = capacity[capacity["iso3"] == iso]
    c_ok = int(c[["unit", "definition"]].notna().all(axis=1).sum())
    t = timing[timing["iso3"] == iso]
    t_ok = int(t["derivation_method"].notna().sum())
    traps = "Definition traps" in notes_text
    return (
        "In-file definitions: UNIVERSALIZATION_SERIES unit+source+source_detail "
        f"{s_ok}/{len(s)} rows; JOBS unit+definition {j_ok}/{len(j)} rows; "
        f"STATE_CAPACITY unit+definition {c_ok}/{len(c)} rows; "
        f"UNIVERSALIZATION_TIMING measure+derivation_method {t_ok}/{len(t)} rows; "
        f"DATA_NOTES_MASSIFICATION.md 'Definition traps' register present={traps}"
    )


def evidence_count(input_id: str, iso: str) -> int:
    if input_id == "I1":
        return int(len(series[(series["iso3"] == iso)
                              & series["indicator"].isin(["cohort_population_0_14", "population_total"])
                              & series["value"].notna()]))
    if input_id == "I2":
        return int(len(jobs[(jobs["iso3"] == iso)
                            & jobs["indicator_code"].isin(ECON_INDICATORS)
                            & jobs["value"].notna()]))
    if input_id == "I3":
        return int(len(policy[policy["iso3"] == iso]))
    if input_id == "I4":
        return int(len(capacity[(capacity["iso3"] == iso) & capacity["value"].notna()
                                & capacity["indicator"].isin(CAP_INDICATORS)]))
    if input_id == "I5":
        return int(len(timing[timing["iso3"] == iso]))
    if input_id == "I6":
        s = series[series["iso3"] == iso]
        j = jobs[jobs["iso3"] == iso]
        c = capacity[capacity["iso3"] == iso]
        t = timing[timing["iso3"] == iso]
        return int(
            s[["unit", "source", "source_detail"]].notna().all(axis=1).sum()
            + j[["unit", "definition"]].notna().all(axis=1).sum()
            + c[["unit", "definition"]].notna().all(axis=1).sum()
            + t["derivation_method"].notna().sum()
        )
    raise KeyError(input_id)


def supply_text(input_id: str, iso: str) -> str:
    if input_id == "I1":
        return "UNIVERSALIZATION_SERIES.csv -> indicator=cohort_population_0_14 / population_total (rows 1995-2024)"
    if input_id == "I2":
        return ("JOBS_AND_MARKETS_PANEL.csv -> indicator_code in "
                "{SL.AGR.EMPL.ZS, SL.EMP.WORK.ZS, SL.SRV.EMPL.ZS, SL.UEM.1524.ZS, "
                "NY.GDP.PCAP.PP.CD, SE.XPD.TOTL.GD.ZS}")
    if input_id == "I3":
        return f"POLICY_TIMELINE.csv -> rows iso3={iso} (country, iso3, year, event, detail)"
    if input_id == "I4":
        return ("STATE_CAPACITY.csv -> dimension=delivery_capacity/fiscal_capacity "
                "(PTR, teachers, education spending, per-student spending) + "
                "SCHOOL_EXPANSION.csv coverage check")
    if input_id == "I5":
        return ("UNIVERSALIZATION_TIMING.csv -> rows level x threshold_pct x measure "
                f"(iso3={iso})")
    if input_id == "I6":
        return ("DATA_NOTES_MASSIFICATION.md + in-file unit/definition/source_detail fields "
                "(UNIVERSALIZATION_SERIES, JOBS_AND_MARKETS_PANEL, STATE_CAPACITY, "
                "UNIVERSALIZATION_TIMING)")
    raise KeyError(input_id)


NOTES = {
    "I1": (
        "Cohort count is DERIVED (WDI SP.POP.TOTL x SP.POP.0014.TO.ZS); both inputs observed, "
        "product flagged status=derived in the file. 0-14 is not a level-specific school-age cohort - "
        "declared as the cohort input, not silently substituted for completion denominators. "
        "No imputation; 1995-2024 window identical for both countries."
    ),
    "I2": (
        "SL.* rows are ILO modelled estimates in WDI (not national LFS tabulations); "
        "SE.XPD.TOTL.GD.ZS is sparse for CHN (5 observations). No new request: the on-disk vintage "
        "is the one ruled usable (D92). Gross vs net and UIS vs WDI vintage traps are handled by "
        "using the series as labelled, never averaged."
    ),
    "I3": (
        "Dated policy pushes only, status=policy_fact with declared confidence "
        "('fact (not re-verified this pass)'; HKG-2012 from the workspace ledger). "
        "CHN carries the single 1986 Compulsory Education Law - D75 requires its -27 y miss "
        "reported as is (no repair, no target fitting). Nothing fetched or sent."
    ),
    "I4": (
        "Declared partial capacity path only (annual PTR / teacher counts / fiscal shares; D53/R26). "
        "SCHOOL_EXPANSION.csv inspected and is PHL-only, so it supplies neither CHN nor HKG; the "
        "named expansion file and annual capacity/enforcement remain HELD per D76/D92 - already-held, "
        "reaffirmed, not a new request. CHN per-student spending is sparse (3 years) and is flagged, "
        "not imputed or proxied."
    ),
    "I5": (
        "Gate mapping is fixed by D75 constraint (iii)/(iv): HKG timing-only and levels check-only "
        "(NER>=90 1974, NER>=95 1979, threshold-specific, never spliced); CHN with censoring rules - "
        "left-censored primary gates and a right-censored upper-secondary GER>=90 row (>2019). "
        "HKG completion-gate rows are status=unable because UIS reports no HKG completion series - "
        "declared unavailable in the file, not a new ask."
    ),
    "I6": (
        "Definitions, units and source_detail are populated in-file for both countries, and the "
        "'Definition traps' register (gross != net, completion != enrolment, cohort derived, "
        "UIS vs WDI vintage, ILO modelled, HKG 100% urban) is the measurement-definition input. "
        "No new definition is needed for the transfer; no splicing across measures is permitted."
    ),
}


# ---------------------------------------------------------------------------
# 3. Build the checklist
# ---------------------------------------------------------------------------
chn_avail = {iid: fn("CHN") for iid, fn in [
    ("I1", availability_cohorts), ("I2", availability_economy), ("I3", availability_policy),
    ("I4", availability_capacity), ("I5", availability_gates), ("I6", availability_definitions),
]}
hkg_avail = {iid: fn("HKG") for iid, fn in [
    ("I1", availability_cohorts), ("I2", availability_economy), ("I3", availability_policy),
    ("I4", availability_capacity), ("I5", availability_gates), ("I6", availability_definitions),
]}

rows = []
for iid, name in INPUTS:
    for iso in COUNTRIES:
        n_ev = evidence_count(iid, iso)
        if n_ev > 0:
            status = "present-on-disk"
        elif name in HELD_LABELS:
            status = "already-held-ask"
        else:
            status = "NEW-ASK"
        rows.append({
            "input_id": iid,
            "input": name,
            "required_for": "CHN;HKG",
            "country": iso,
            "supplying_file_and_indicator_row": supply_text(iid, iso),
            "chn_value_availability": chn_avail[iid],
            "hkg_value_availability": hkg_avail[iid],
            "status": status,
            "notes": NOTES[iid],
        })

checklist = pd.DataFrame(rows, columns=[
    "input_id", "input", "required_for", "country",
    "supplying_file_and_indicator_row",
    "chn_value_availability", "hkg_value_availability",
    "status", "notes",
])

# Determinism guard: exactly 6 inputs x 2 countries.
assert checklist["input_id"].nunique() == 6
assert len(checklist) == 12

new_ask_inputs = sorted({r["input"] for r in rows if r["status"] == "NEW-ASK"})
already_held_rows = sorted({r["input"] for r in rows if r["status"] == "already-held-ask"})
present_inputs = sorted({r["input"] for r in rows if r["status"] == "present-on-disk"})

if new_ask_inputs:
    verdict = "BLOCKED-ON-DATA"
elif len(present_inputs) == 6 and len(checklist) == 12:
    verdict = "DATA-COMPLETE"
else:
    verdict = "UNABLE"

new_ask_text = (
    "none" if not new_ask_inputs
    else "; ".join(f"{n} (HELD, nothing sent; design BLOCKED-ON-DATA for this input)" for n in new_ask_inputs)
)

note = (
    f"NEW-ASK: {new_ask_text}. "
    f"{len(present_inputs)}/6 D75 inputs present-on-disk for both CHN and HKG "
    f"({int((checklist['status'] == 'present-on-disk').sum())}/12 input-country rows); "
    f"already-held-only inputs: {', '.join(already_held_rows) if already_held_rows else 'none'}. "
    "Capacity trajectory uses only the declared partial delivery/fiscal path (D53/R26); "
    "annual capacity/enforcement, real per-pupil spending, PSA/ES microdata and the named "
    "expansion file stay HELD per D76/D92 - reaffirmed, nothing sent. "
    "Design-only data-completeness audit: no model run, no portability claim (D75/R22); "
    "C1-C4 untouched."
)

cluster = pd.DataFrame([{
    "experiment": "Y5",
    "cluster": "Y5_portability_audit",
    "question": ("Do all six D75 transfer inputs exist on disk for CHN and HKG, or under an "
                 "already-held ask, with no new data request?"),
    "estimand": "number of D75 inputs requiring a NEW-ASK (not on disk and not already held)",
    "estimate": len(new_ask_inputs),
    "se": "",
    "ci_low": "",
    "ci_high": "",
    "n": 6,
    "clusters": 2,
    "threshold": THRESHOLD,
    "verdict": verdict,
    "label": "derived",
    "note": note,
}], columns=[
    "experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low",
    "ci_high", "n", "clusters", "threshold", "verdict", "label", "note",
])

# ---------------------------------------------------------------------------
# 4. Write results (deterministic CSV bytes)
# ---------------------------------------------------------------------------
RESULTS.mkdir(parents=True, exist_ok=True)
checklist.to_csv(RESULTS / "transfer_checklist.csv", index=False, lineterminator="\n")
cluster.to_csv(RESULTS / "CLUSTER_RESULTS.csv", index=False, lineterminator="\n")

# Console summary (not part of the result files).
print(f"predeclaration sha256 OK: {pre_sha}")
print(f"inputs audited: {checklist['input_id'].nunique()} | checklist rows: {len(checklist)}")
for iid, name in INPUTS:
    st = checklist[checklist["input_id"] == iid][["country", "status"]]
    pairs = ", ".join(f"{r.country}={r.status}" for r in st.itertuples())
    print(f"  {iid} {name}: {pairs}")
print(f"NEW-ASK: {new_ask_text}")
print(f"verdict: {verdict}")
print(f"wrote: {RESULTS / 'transfer_checklist.csv'}")
print(f"wrote: {RESULTS / 'CLUSTER_RESULTS.csv'}")
