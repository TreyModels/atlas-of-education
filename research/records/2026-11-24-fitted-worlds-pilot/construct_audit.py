#!/usr/bin/env python3
"""STAGE 1 construct/feasibility audit for the fitted-worlds pilot.

Reads ONLY data already committed in this repository (this worktree; and committed files on
other branches via `git show`). No model/fitting compute: this is an inventory and coverage
audit. Emits stage1_audit.json and prints a summary; the human-readable report
STAGE1_CONSTRUCT_AUDIT.md interprets it.

Pre-registration: research/records/2026-11-24-fitted-worlds-pilot/
                 PRE_REGISTRATION_fitted_worlds_pilot.md (commit before this code).
"""
import argparse
import csv
import gzip
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC = HERE  # this script lives at the record root (stage1 output goes beside it)
OUTDIR = os.path.join(REC, "stage1")
WDI_BRANCH = "origin/research/massification-panel-2026-11-22"
WDI_PREFIX = "research/records/2026-11-22-massification-panel/sources/wdi_sweep/"
DHS_BRANCH = "origin/research/dhs-api-ecological-2026-11-24"
DHS_PREFIX = "research/records/2026-11-24-dhs-api-ecological/data/"
DHSA_BRANCH = "origin/research/dhs-acquisition-2026-11-24"
DHSA_PREFIX = "research/records/2026-11-24-dhs-acquisition/data/"
E1_BRANCH = "origin/research/e1-multiverse-1200-2026-11-25"
E1_PREFIX = "research/records/2026-11-25-e1-multiverse/"

# Series the audit needs from the massification-panel WDI sweep (committed, same repo).
WDI_SERIES = ["child_work.json", "pre_ger.json.gz", "prm_ner.json", "sec_ner.json",
              "lsc.json", "test_scores.json", "hci.json", "gdppc_log.json.gz",
              "fertility.json.gz", "repeat_prm.json", "prm_cmp.json.gz"]


def git_show(repo, rev_path):
    p = subprocess.run(["git", "-C", repo, "show", rev_path],
                       capture_output=True)
    if p.returncode != 0:
        raise FileNotFoundError(f"git show {rev_path}: {p.stderr.decode()[:300]}")
    return p.stdout


def load_wdi(repo, filename):
    raw = git_show(repo, WDI_BRANCH + ":" + WDI_PREFIX + filename)
    if filename.endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw)


def coverage(rows):
    rows = [r for r in rows if r and len(r) >= 3 and r[2] is not None]
    iso = sorted({r[0] for r in rows})
    years = sorted({int(r[1]) for r in rows if str(r[1]).isdigit()})
    per = {}
    for r in rows:
        per.setdefault(r[0], []).append(int(r[1]))
    counts = sorted(len(v) for v in per.values())
    return {"rows": len(rows), "countries": len(iso), "years": [years[0], years[-1]] if years else None,
            "year_values": years, "obs_per_country_median": counts[len(counts) // 2] if counts else 0,
            "obs_per_country_min": counts[0] if counts else 0,
            "obs_per_country_max": counts[-1] if counts else 0}


def wdi_obs(repo, filename):
    d = load_wdi(repo, filename)
    return {(r[0], int(r[1])): float(r[2]) for r in d if r and len(r) >= 3 and r[2] is not None}


def overlap(a, b, max_gap=2):
    """Country-years matched between two {（iso,year): value} series within max_gap years."""
    by_iso_a, by_iso_b = {}, {}
    for (i, y) in a:
        by_iso_a.setdefault(i, []).append(y)
    for (i, y) in b:
        by_iso_b.setdefault(i, []).append(y)
    pairs, countries = 0, set()
    for i in set(by_iso_a) & set(by_iso_b):
        for ya in by_iso_a[i]:
            if any(abs(ya - yb) <= max_gap for yb in by_iso_b[i]):
                pairs += 1
                countries.add(i)
    return {"pairs_within_gap": pairs, "countries": len(countries), "max_gap_years": max_gap}


def read_text(repo, local_rel, git_ref):
    p = os.path.join(repo, local_rel)
    if os.path.exists(p):
        return open(p, "rb").read()
    return git_show(repo, git_ref)


def read_csv_text(repo, rev_path):
    raw = git_show(repo, rev_path).decode("utf-8", "replace")
    return list(csv.DictReader(io.StringIO(raw)))


def read_local_csv(path):
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def parse_int(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.getcwd(), help="git repo/worktree to read committed data from")
    args = ap.parse_args()
    repo = args.repo
    os.makedirs(OUTDIR, exist_ok=True)
    out = {"label": "STAGE 1 CONSTRUCT/FEASIBILITY AUDIT — inventory only, no fitting",
           "prereg": "research/records/2026-11-24-fitted-worlds-pilot/PRE_REGISTRATION_fitted_worlds_pilot.md",
           "repo": repo, "sources": {}, "mapping": [], "joint_coverage": {}, "verdict": {}}

    # ---------------- D1 WDI/UIS/ILO sweep ----------------
    meta = json.loads(git_show(repo, WDI_BRANCH + ":" + WDI_PREFIX + "meta.json"))
    aggregates = {iso for iso, m in meta.items() if str(m.get("region", "")).strip() == "Aggregates"}
    d1 = {}
    obs = {}
    for f in WDI_SERIES:
        try:
            rows = load_wdi(repo, f)
        except FileNotFoundError:
            d1[f] = {"status": "missing from cache"}
            continue
        rows_nat = [r for r in rows if r and len(r) >= 3 and r[2] is not None and r[0] not in aggregates]
        cov = coverage(rows_nat)
        d1[f] = {"coverage_national": cov,
                 "rows_including_aggregates": coverage(rows)["rows"]}
        obs[f] = {(r[0], int(r[1])): float(r[2]) for r in rows_nat}
    out["sources"]["D1_wdi_sweep"] = {"branch": WDI_BRANCH, "path": WDI_PREFIX,
                                      "series": d1, "n_aggregate_codes": len(aggregates)}

    # overlap facts needed by the fitted-worlds question (child work x schooling/learning)
    jc = {}
    if "child_work.json" in obs:
        cw = obs["child_work.json"]
        for other in ("pre_ger.json.gz", "prm_ner.json", "sec_ner.json", "lsc.json",
                      "test_scores.json", "hci.json", "gdppc_log.json.gz"):
            if other in obs:
                jc[f"child_work x {other}"] = overlap(cw, obs[other], max_gap=2)
    out["joint_coverage"]["child_work_overlaps"] = jc
    if "pre_ger.json.gz" in obs and "test_scores.json" in obs:
        out["joint_coverage"]["pre_ger x test_scores"] = overlap(obs["pre_ger.json.gz"],
                                                                 obs["test_scores.json"], max_gap=2)

    # ---------------- D2 asia_school_work cross-section ----------------
    try:
        a = json.loads(read_text(repo, "engine/data/asia_school_work.json",
                                 E1_BRANCH + ":engine/data/asia_school_work.json"))
        ctry = a["countries"]
        oos = [v for v in ctry.values() if v.get("oos_lower") is not None]
        cl = [v for v in ctry.values() if v.get("child_labour") is not None]
        years_oos = sorted({v["oos_year"] for v in ctry.values() if v.get("oos_year")})
        years_cl = sorted({v["cl_year"] for v in ctry.values() if v.get("cl_year")})
        both = [k for k, v in ctry.items() if v.get("oos_lower") is not None and v.get("child_labour") is not None]
        out["sources"]["D2_asia_school_work"] = {
            "path": "engine/data/asia_school_work.json", "n_countries": len(ctry),
            "n_with_oos_lower": len(oos), "n_with_child_labour": len(cl),
            "n_with_both": len(both), "oos_years": [years_oos[0], years_oos[-1]],
            "cl_years": [years_cl[0], years_cl[-1]],
            "definition_note": a.get("_about", "")[:400],
            "composition_test_countries": sum(1 for v in ctry.values() if "composition" in v)}
    except FileNotFoundError:
        out["sources"]["D2_asia_school_work"] = {"status": "file not in this tree"}

    # ---------------- D3 shadow education (tutoring) ----------------
    d3 = {}
    for f in ("shadow_incidence_round2.csv", "shadow_fees_round2.csv"):
        rel = ("experiments/massification-2026-11-20/04_data/shadow_round2/data/" + f)
        try:
            raw = read_text(repo, rel, "origin/experiment/massification-2026-11-20:" + rel)
        except FileNotFoundError:
            d3[f] = {"status": "missing"}
            continue
        rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", "replace"))))
        cols = list(rows[0].keys()) if rows else []
        ctry_col = next((c for c in cols if "countr" in c.lower()), None)
        year_col = next((c for c in cols if "year" in c.lower()), None)
        countries = sorted({r[ctry_col] for r in rows if ctry_col and r.get(ctry_col)}) if ctry_col else []
        years = sorted({r[year_col] for r in rows if year_col and r.get(year_col)}) if year_col else []
        d3[f] = {"rows": len(rows), "columns": cols[:12], "countries_or_sites": len(countries),
                 "country_list_sample": countries[:8], "years_sample": years[:10],
                 "national_panel": False}
    out["sources"]["D3_shadow_education"] = d3

    # ---------------- D4 E1 (derived only) ----------------
    e1_files = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", E1_BRANCH],
                              capture_output=True, text=True).stdout.splitlines()
    e1 = [f for f in e1_files if f.startswith(E1_PREFIX)]
    raw_like = [f for f in e1 if re.search(r"\.(pkl|parquet|dta|npz)$|/data/.*\.(json|csv)(\.gz)?$", f)]
    # variables from gm_core.py
    vars_list = []
    gm = [f for f in e1 if f.endswith("scripts/gm_core.py")]
    if gm:
        src = git_show(repo, E1_BRANCH + ":" + gm[0]).decode()
        m = re.search(r"VARS\s*=\s*\[(.*?)\]", src, re.S)
        if m:
            vars_list = re.findall(r'"([^"]+)"', m.group(1))
    out["sources"]["D4_e1"] = {
        "branch": E1_BRANCH, "record_files": len(e1), "raw_panel_files": raw_like,
        "raw_panel_committed": bool(raw_like), "variables_17": vars_list,
        "note": "E1 record commits derived link statistics only; the raw WDI panel is not in the "
                "repo (per E1 REPORT it lived at /root/work/data on a different host). No re-pull allowed."}

    # ---------------- D5 Q2 long-run panel ----------------
    q2_rel = "research/records/2026-11-25-q2-pathways/data/long_run_panel.csv"
    try:
        raw_q2 = read_text(repo, q2_rel,
                           "origin/research/q2-pathways-2026-11-25:" + q2_rel)
        rows = list(csv.DictReader(io.StringIO(raw_q2.decode("utf-8", "replace"))))
        cols = list(rows[0].keys())
        iso = {r["iso3"] for r in rows}
        yrs = sorted({parse_int(r["year"]) for r in rows if parse_int(r["year"]) is not None})
        var_cov = {}
        for c in cols:
            vals = [r for r in rows if r.get(c, "") not in ("", None)]
            vc = sorted({parse_int(r["year"]) for r in vals if parse_int(r["year"]) is not None})
            vcso = {r["iso3"] for r in vals}
            var_cov[c] = {"non_empty_rows": len(vals), "countries": len(vcso),
                          "years": [vc[0], vc[-1]] if vc else None}
        out["sources"]["D5_q2_panel"] = {"path": q2_rel, "rows": len(rows), "countries": len(iso),
                                         "years": [yrs[0], yrs[-1]], "variables": var_cov}
    except FileNotFoundError:
        out["sources"]["D5_q2_panel"] = {"status": "file not in this tree"}

    # ---------------- D6/D7 DHS API cache ----------------
    d6 = {}
    try:
        cat = json.loads(git_show(repo, DHS_BRANCH + ":" + DHS_PREFIX + "indicator_catalogue.json"))
        d6["indicator_catalogue_size"] = len(cat)
    except FileNotFoundError:
        d6["indicator_catalogue_size"] = None
    for f in ("panel_edu2_FE_AAFB_W_M25.csv", "panel_edu2_FE_FRTY_W_MNC.csv",
              "panel_edu2_FE_FRTR_W_TFR.csv", "panel_survey.csv"):
        try:
            rows = read_csv_text(repo, DHS_BRANCH + ":" + DHS_PREFIX + f)
        except FileNotFoundError:
            d6[f] = {"status": "missing"}
            continue
        ctry = {r.get("country") for r in rows if r.get("country")}
        yrs = sorted({parse_int(r.get("year")) for r in rows if parse_int(r.get("year")) is not None})
        edu = sorted({r.get("edu") for r in rows if r.get("edu")}) if rows and "edu" in rows[0] else []
        d6[f] = {"rows": len(rows), "countries": len(ctry),
                 "years": [yrs[0], yrs[-1]] if yrs else None, "edu_categories": edu[:8],
                 "indicators": sorted({r.get("indicator") for r in rows if r.get("indicator")})[:6]}
    out["sources"]["D6_dhs_api_cache"] = {"branch": DHS_BRANCH, "path": DHS_PREFIX, "panels": d6}
    try:
        rows = read_csv_text(repo, DHSA_BRANCH + ":" + DHSA_PREFIX + "ceb_education_cells.csv")
        ctry = {r.get("country") for r in rows if r.get("country")}
        yrs = sorted({parse_int(r.get("survey_year")) for r in rows if parse_int(r.get("survey_year")) is not None})
        out["sources"]["D7_dhs_ceb_education_cells"] = {
            "rows": len(rows), "countries": len(ctry), "years": [yrs[0], yrs[-1]] if yrs else None,
            "education_categories": sorted({r.get("education") for r in rows if r.get("education")}),
            "definition_column": "mean_ceb_40_49 (published DHS API cells; women 40-49)"}
    except FileNotFoundError:
        out["sources"]["D7_dhs_ceb_education_cells"] = {"status": "missing"}

    # ---------------- D8 Philippines HE enrolment ----------------
    ph_rel = "docs/engine/comparative_cases/philippines_enrolment.json"
    try:
        d = json.loads(read_text(repo, ph_rel, E1_BRANCH + ":" + ph_rel))
        out["sources"]["D8_philippines_he"] = {
            "source": d.get("source"), "unit": d.get("unit"), "coverage": d.get("coverage"),
            "n_observations": len(d.get("observations", []))}
    except FileNotFoundError:
        out["sources"]["D8_philippines_he"] = {"status": "file not in this tree"}

    # ---------------- model observables (for the mapping table) ----------------
    model_py = os.path.join(repo, "research", "records", "2026-11-24-synthetic-corrected", "model.py")
    model_obs = {}
    if os.path.exists(model_py):
        spec = importlib.util.spec_from_file_location("m", model_py)
        # do not import (would need numpy + port backend); parse statistically instead
        src = open(model_py).read()
        model_obs = {"has_age_or_grade_variable": bool(re.search(r"\bage\b|\bgrade\b", src)),
                     "n_households_default": 10_000, "years": 25,
                     "states": "0 school only; 1 school+work; 2 visible work; 3 hidden work",
                     "source": "research/records/2026-11-24-synthetic-corrected/model.py (unmodified kernel)"}
    out["model_observables"] = model_obs

    # ---------------- static mapping table (declared classifications) ----------------
    # status: compatible / partial / unmatched  (judged against the prereg Stage-1 rule)
    mapping = [
        {"output": "ger", "definition": "share of households with a child in school (model states 0,1); "
                                        "no age band, no grade, no repetition, one child per household",
         "candidates": "D1 pre_ger (primary GER, 248 codes incl. aggregates, 1970-2022); D1 prm_ner/sec_ner "
                       "(net enrolment, 236/227 countries, 1970-2019); D1 lsc (lower-secondary completion); "
                       "D5 mean years of schooling; D6 DHS women's education",
         "age_unit_definition_period": "GENERAL/PARTIAL: gross enrolment ratio (pupils of any age / official-age "
                                       "population, can exceed 100%) vs a household participation share; net "
                                       "enrolment is age-specific (model has no age); completion/attainment is a "
                                       "stock, not participation; calendar vs synthetic time",
         "status": "partial", "reason": "no age/grade structure in the model; gross-vs-net and "
                                         "participation-vs-attainment mismatch cannot be removed without an invented mapping"},
        {"output": "cl", "definition": "share of households in observed child employment (states 1+2)",
         "candidates": "D1 child_work (ILO/UCW children 7-14 in employment; 100 countries; 1994-2016; sparse); "
                       "D2 child_labour (ILO/UNICEF, children 5-17; 21-country cross-section, years differ)",
         "age_unit_definition_period": "PARTIAL: employment definition broadly matches, but the model has no age "
                                       "band while observed series are 7-14 or 5-17; child-weighted vs "
                                       "household-weighted; ILO modelled/administrative estimates; sparse irregular panel",
         "status": "partial", "reason": "age band and unit differ; observations are sparse and irregular (not a "
                                         "change panel); no joint panel with the other states"},
        {"output": "sw", "definition": "study-and-work share (state 1)",
         "candidates": "UCW publishes study-and-work shares, but the committed cache (D1 child_work.json) holds "
                       "only the total employment series; no work-only/study-and-work split is committed",
         "age_unit_definition_period": "NO COMMITTED SERIES", "status": "unmatched",
         "reason": "observed decomposition not present in the repo"},
        {"output": "wo", "definition": "visible-work-only share (state 2)",
         "candidates": "same as sw: work-only share is not in the committed cache",
         "age_unit_definition_period": "NO COMMITTED SERIES", "status": "unmatched",
         "reason": "observed decomposition not present in the repo"},
        {"output": "hw", "definition": "hidden work (state 3); unobserved by construction",
         "candidates": "none: surveys do not observe hidden/unpaid non-employment activity as this model defines it",
         "age_unit_definition_period": "NO OBSERVED COUNTERPART", "status": "unmatched",
         "reason": "not measurable with the repo's observed data"},
        {"output": "tut", "definition": "share of households using tutoring",
         "candidates": "D3 shadow-education incidence/fees (hand-collected; 38+20 rows; several case studies, "
                       "not national; definitions and years differ)",
         "age_unit_definition_period": "PARTIAL/UNMATCHED: no harmonised country-year panel; case-study "
                                        "definitions; tutoring 'participation' differs across sources",
         "status": "unmatched",
         "reason": "no comparable panel; using it would invent a national tutoring target"},
        {"output": "learn", "definition": "mean learning in model grade-equivalents (model-internal scale)",
         "candidates": "D1 test_scores (WDI harmonized test scores 0-625, 172 countries, 2010-2020); D1 hci "
                       "(learning index 0-1); D5 schooling attainment",
         "age_unit_definition_period": "UNIT MISMATCH: model grade-equivalents have no empirical scale "
                                       "mapping to test-score points or HCI units; observed period only 2010-2020",
         "status": "partial", "reason": "unit/scale cannot be mapped without an invented calibration; no "
                                         "period overlap with a documented model episode"},
        {"output": "inc", "definition": "mean household income in model units (arbitrary logarithmic scale)",
         "candidates": "D1 gdppc_log (257 countries, 1960-2024); D5 Maddison GDP pc",
         "age_unit_definition_period": "UNIT MISMATCH: country GDP per capita in dollars vs household mean in "
                                       "arbitrary model units; household vs country; only scale-free shapes could "
                                       "be compared by inventing a normalisation",
         "status": "unmatched", "reason": "no level/unit link; would require an invented scaling target"},
        {"output": "B1", "definition": "within-mother post-death birth-spacing contrast",
         "candidates": "none: no birth-interval microdata in the repo (DHS API publishes no such cell; microdata "
                       "acquisition forbidden)",
         "age_unit_definition_period": "NO OBSERVED COUNTERPART", "status": "unmatched",
         "reason": "requires microdata that the pilot may not acquire"},
        {"output": "B2", "definition": "parity-progression gradient by education",
         "candidates": "D6/D7 mean CEB by education (published DHS API cells; women 40-49); not a parity-progression ratio",
         "age_unit_definition_period": "PARTIAL: related fertility-education gradient but different construct "
                                        "(mean CEB vs PPR), different age band, survey vintages",
         "status": "unmatched", "reason": "parity progression is not published; mean CEB is a different quantity"},
        {"output": "B3", "definition": "age-at-first-birth gradient by education",
         "candidates": "D6 FE_AAFB_W_M25 (median age at first birth by education; published DHS cells)",
         "age_unit_definition_period": "PARTIAL: years vs years, but median vs mean, women 25+ vs model women "
                                        "15-40, education categories differ",
         "status": "partial", "reason": "estimator/category mismatch; only usable as a declared approximation"},
    ]
    out["mapping"] = mapping
    n_compat = sum(1 for m in mapping if m["status"] == "compatible")
    n_partial = sum(1 for m in mapping if m["status"] == "partial")
    n_unmatched = sum(1 for m in mapping if m["status"] == "unmatched")
    out["mapping_summary"] = {"compatible": n_compat, "partial": n_partial, "unmatched": n_unmatched,
                              "total_outputs": len(mapping)}

    # ---------------- declared Stage-1 decision rule ----------------
    cw_overlap = jc.get("child_work x pre_ger.json.gz", {})
    cw_lsc = jc.get("child_work x lsc.json", {})
    reasons = []
    if n_compat < 2:
        reasons.append(f"only {n_compat} of {len(mapping)} model outputs are fully measurement-compatible "
                       f"(rule requires >=2); {n_partial} are partial and {n_unmatched} unmatched")
    # joint moment: only child_work (total employment, sparse) overlaps schooling series
    reasons.append(f"the only cross-output observed overlap is child_work x primary GER "
                   f"({cw_overlap.get('countries',0)} countries, {cw_overlap.get('pairs_within_gap',0)} "
                   f"country-years within {cw_overlap.get('max_gap_years',2)} years); the school/work "
                   f"decomposition that distinguishes the four worlds (study-and-work, work-only, hidden work) "
                   f"is not in the committed data")
    reasons.append("the model has no age or grade structure, so age-specific observed constructs "
                   "(7-14 child labour, primary/secondary enrolment) cannot be matched without an invented age rule")
    reasons.append("no frozen training/validation split can reach 20 training + 10 independent validation "
                   "countries on a compatible joint moment")
    out["verdict"] = {
        "code": "insufficient_evidence",
        "text": "Stage 1 FAILS: the constructs do not line up. The fitted-worlds question is not answerable "
                "with the observed series committed to this repository without inventing targets or age/unit/"
                "scale mappings. Per the pre-registration, the pilot stops before any fitting, synthetic "
                "recovery, ABC or server draw.",
        "reasons": reasons,
        "stage1_passed": False,
        "stage2_launched": False,
        "server_run": False,
        "box_status_checked": True,
    }
    out["what_would_be_needed"] = [
        "an age/grade-structured model output (or a declared, testable age-aggregation rule) so that UCW "
        "7-14 child-labour states and primary/secondary enrolment can be matched to model states",
        "the UCW study-and-work and work-only shares (not only total child employment) as a harmonised "
        "country-year panel, so the school/work decomposition that separates the worlds is observed",
        "a learning scale anchor (e.g. an explicit model-to-test-score mapping validated out of sample)",
        "a harmonised cross-country tutoring/shadow-education panel (the current data are case studies)",
        "DHS microdata (IR/BH files) for B1 birth-interval contrasts, which this pilot may not acquire",
        "harmonised data vintages/periods across constructs so a frozen train/validation split is possible",
    ]
    json.dump(out, open(os.path.join(OUTDIR, "stage1_audit.json"), "w"), indent=1)
    print(json.dumps({"mapping_summary": out["mapping_summary"],
                      "child_work_overlaps": jc,
                      "verdict": out["verdict"]["code"],
                      "reasons": reasons}, indent=1))
    return out


if __name__ == "__main__":
    main()
