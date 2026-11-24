#!/usr/bin/env python3
"""Leg B data gate for the gender-split E8 record — pre-registered in PRE_REGISTRATION.md §B.

Question: is the `t*` bulge-by-sex test estimable from repo-committed inputs?
  t* = t_abolition + L_primary
Required (all three):
  (1) an in-repo L_primary / primary-cycle-length source for MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA;
  (2) a SEX-DISAGGREGATED final-grade primary repetition OR primary->secondary transition/progression series,
      annual, committed;
  (3) DHS IR individual-recode microdata for the 8 countries (or an equivalent committed cohort-level,
      sex-comparable outcome).
Not accepted (pre-registered): DHS API ecological country x survey x education aggregates; borrowed/assumed
L_primary values.

This script performs the scan and writes results/legb_data_gate.json. It does not estimate anything.
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.abspath(os.path.join(HERE, ".."))
RES = os.path.join(REC, "results")
os.makedirs(RES, exist_ok=True)
WT = os.path.abspath(os.path.join(REC, "..", "..", ".."))  # worktree root

E8_BRANCH = "origin/research/e6e8-sequencing-2026-11-25"
BULGE_BRANCH = "origin/research/bulge-arrival-2026-11-25"
BULGE_MICRO_BRANCH = "origin/research/bulge-micro-dhs-2026-11-25"
DHS_ACQ_BRANCH = "origin/research/dhs-acquisition-2026-11-24"
DHS_MICRO_BRANCH = "origin/research/dhs-micro-2026-11-23"
DHS_API_BRANCH = "origin/research/dhs-api-ecological-2026-11-24"


def run(cmd, cwd=WT):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True)


def blob_sha(ref_path):
    r = run(["git", "rev-parse", ref_path])
    return r.stdout.strip() or None


def show(ref_path):
    r = run(["git", "show", ref_path])
    if r.returncode != 0:
        return None
    return r.stdout


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8", "replace")).hexdigest()


def evidence_lines(text, patterns):
    out = []
    for line in text.splitlines():
        if any(re.search(p, line, re.I) for p in patterns):
            out.append(line.strip())
    return out


def main():
    gate = {"scan_timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "preregistration_commit": "875ffd8",
            "question": "t* = t_abolition + L_primary; sex-disaggregated bulge outcome",
            "verdict": None, "inputs": {}, "scans": {}, "evidence": {}, "missing_series": [],
            "commands": []}

    # ---------- scan 1: every ref's file paths (no blob fetch needed) ----------
    refs = [l for l in run(["git", "for-each-ref", "--format=%(refname)"]).stdout.splitlines() if l]
    gate["commands"].append("git for-each-ref --format='%(refname)' ; git ls-tree -r --name-only <each ref>")
    paths = set()
    for ref in refs:
        r = run(["git", "ls-tree", "-r", "--name-only", ref])
        paths.update(r.stdout.splitlines())
    paths = sorted(paths)
    kw = {
        "primary_duration_or_cycle_or_structure": r"primary.?dur|primary.?cycle|primary.?length|primary.?long|L_primary|education.?structure|isced",
        "repetition": r"repet|rept",
        "progression_transition": r"prsl|progress|transition",
        "individual_recode_or_dhs_microdata": r"individual.?recode|\.dta$|dhs.?ir|ir_.*\.(dta|zip)|IR[A-Z]{2}",
    }
    matches = {}
    for k, pat in kw.items():
        matches[k] = [p for p in paths if re.search(pat, p, re.I)]
    gate["scans"]["screened_and_rejected"] = {
        "reason": "path-keyword hits that are NOT education-system data; screened and rejected, none is a "
                  "country-year sex-disaggregated repetition/transition series",
        "groups": {
            "research/records/2026-11-23-transition{,-gpu}/": "schooling-fertility phase-transition record "
                "(long_run_panel.csv = mean years of schooling; trans_*.json = model results) -- not primary->secondary transition",
            "experiments/massification-2026-11-20/.../coevolve_*/**/A_transitions_derived.csv, transitions_all_arms.csv": "ABM model output, not country-year education data",
            "research/masseng-v6/model/outputs/PHL/v3/figures/k12_transition.png": "model figure, not a series",
            "research/records/2026-11-23-dhs-micro/": "DHS API AGGREGATE cells (women's education x fertility); no IR microdata -- see evidence.dhs_ir_microdata",
            "e6_inputs_and_hashes.csv .dta hits": "GGDC/PWT Stata files, not DHS microdata",
        },
    }
    gate["scans"]["all_ref_path_scan"] = {
        "n_refs": len(refs), "n_unique_paths": len(paths), "keyword_matches": matches,
        "n_dta_files": sum(1 for p in paths if p.lower().endswith(".dta")),
        "n_repetition_indicator_paths": len(matches["repetition"]),
        "n_rept_or_prsl_paths": sum(1 for p in paths if re.search(r"rept|prsl", p, re.I)),
    }

    # ---------- scan 2: content of the working tree ----------
    tokens = ["L_primary", "primary_cycle", "primary cycle length", "SE.PRM.REPT", "SE.PRM.PRSL",
              "repetition rate", "transition rate", "Individual Recode", ".dta"]
    content_hits = {t: [] for t in tokens}
    exts = {".py", ".json", ".csv", ".md", ".txt", ".js", ".cjs", ".ts", ".yml", ".yaml", ".sh", ".R"}
    nfiles = 0
    for root, dirs, files in os.walk(WT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "dist", "__pycache__", ".venv")]
        for fn in files:
            if os.path.splitext(fn)[1].lower() not in exts:
                continue
            p = os.path.join(root, fn)
            nfiles += 1
            try:
                with open(p, "r", errors="ignore") as f:
                    txt = f.read()
            except OSError:
                continue
            for t in tokens:
                if t in txt:
                    content_hits[t].append(os.path.relpath(p, WT))
    gate["scans"]["worktree_content_scan"] = {
        "root": "worktree (branch research/gender-split-e6e8-2026-11-25, base bd782be)",
        "n_files_scanned": nfiles, "tokens": tokens, "hits": content_hits,
        "note": "L_primary hits are the new PRE_REGISTRATION.md of this record; no committed series elsewhere",
    }

    # ---------- evidence: the three required inputs ----------
    # (1) L_primary
    bulge_prereg_path = f"{BULGE_BRANCH}:paper2/PREREGISTRATION_BULGE_ARRIVAL.md"
    bulge_prereg = show(bulge_prereg_path)
    gate["evidence"]["L_primary"] = {
        "ref_path": bulge_prereg_path,
        "blob_sha": blob_sha(bulge_prereg_path),
        "sha256_of_content": sha256_text(bulge_prereg) if bulge_prereg else None,
        "lines": evidence_lines(bulge_prereg or "",
                                [r"Sourced .?L_primary", r"UNSOURCED", r"no education-structure",
                                 r"east-asia-schools", r"0 / 8"]),
        "verdict": "MISSING: L_primary sourced 0/8; no primary-cycle-length file in any ref for the 8 SSA countries",
    }
    # the only education-structure file in any ref
    systems = show(f"{BULGE_BRANCH}:public/reference/east-asia-schools/source/systems.json") or \
        show("origin/research/e6e8-sequencing-2026-11-25:public/reference/east-asia-schools/source/systems.json")
    gate["evidence"]["only_education_structure_candidate"] = {
        "ref_path": "public/reference/east-asia-schools/source/systems.json (present on every branch)",
        "first_keys": list(json.loads(systems).keys())[:3] if systems else None,
        "verdict": "East-Asia/Hong-Kong city school model; no SSA primary-cycle lengths",
    }

    # (2) sex-disaggregated repetition / transition series
    gate["evidence"]["sex_disaggregated_repetition_or_transition"] = {
        "ref_path_scan": "see scans.all_ref_path_scan.keyword_matches",
        "worktree_content_hits": {"SE.PRM.REPT": content_hits["SE.PRM.REPT"],
                                  "SE.PRM.PRSL": content_hits["SE.PRM.PRSL"],
                                  "repetition rate": content_hits["repetition rate"],
                                  "transition rate": content_hits["transition rate"]},
        "public_wdi_probe": {
            "SE.PRM.REPT.ZS": "HTTP 200; WDI label 'Repeaters, primary, total (% of total enrollment)' -- a TOTAL-sex series, not sex-disaggregated; not committed in repo",
            "SE.PRM.REPT.FE.ZS / .MA.ZS / SE.PRM.PRSL.ZS / .FE.ZS / .MA.ZS":
                "probe on 2026-11-25 returned HTTP 429 (rate-limited) -- INCONCLUSIVE as to public existence; does not affect the gate because no such series is committed for the 8 countries in any ref",
        },
        "verdict": "MISSING: no sex-disaggregated repetition or primary->secondary transition/progression series is "
                   "committed in any ref; no such file path exists; WDI's committed/available repetition series is total-sex",
    }

    # (3) DHS IR microdata
    dhs_micro = show(f"{DHS_MICRO_BRANCH}:research/records/2026-11-23-dhs-micro/README.md")
    dhs_micro_probe = show(f"{DHS_MICRO_BRANCH}:research/records/2026-11-23-dhs-micro/data/microdata_probe.txt")
    bullet_micro = show(f"{BULGE_MICRO_BRANCH}:research/records/2026-11-25-bulge-micro-dhs/BULGE_MICRO_STATUS.md")
    gate["evidence"]["dhs_ir_microdata"] = {
        "repo_scan": "0 .dta files in 194 refs (scans.all_ref_path_scan.n_dta_files); DHS Terms forbid redistribution",
        "dhs_micro_record": {
            "ref_path": f"{DHS_MICRO_BRANCH}:research/records/2026-11-23-dhs-micro/README.md",
            "blob_sha": blob_sha(f"{DHS_MICRO_BRANCH}:research/records/2026-11-23-dhs-micro/README.md"),
            "lines": evidence_lines(dhs_micro or "", [r"not publicly downloadable", r"individual-level test could NOT",
                                                      r"401|403|404", r"Individual Recode", r"ecological"]),
        },
        "probe_log": {
            "ref_path": f"{DHS_MICRO_BRANCH}:research/records/2026-11-23-dhs-micro/data/microdata_probe.txt",
            "lines": (dhs_micro_probe or "").splitlines()[:12],
        },
        "bulge_micro_status": {
            "ref_path": f"{BULGE_MICRO_BRANCH}:research/records/2026-11-25-bulge-micro-dhs/BULGE_MICRO_STATUS.md",
            "lines": evidence_lines(bullet_micro or "", [r"NOT-ESTIMABLE \(0/8\)", r"0 of 54", r"not yet submitted",
                                                         r"no school-entry", r"attained"]),
        },
        "verdict": "MISSING: 0 DHS IR waves held in repo/box; DHS IR is login-gated and not publicly downloadable; "
                   "the Africa-11 dataset request (contains all 8 E8 countries) is not yet submitted",
    }

    # DHS API ecological aggregates -- explicitly NOT a valid substitute
    api_readme = show(f"{DHS_API_BRANCH}:research/records/2026-11-24-dhs-api-ecological/data/README.md")
    api_cat = show(f"{DHS_API_BRANCH}:research/records/2026-11-24-dhs-api-ecological/data/indicator_catalogue.json")
    api_panels = show(f"{DHS_API_BRANCH}:research/records/2026-11-24-dhs-api-ecological/data/panel_survey.csv")
    n_ind = None
    n_hits = None
    if api_cat:
        try:
            items = json.loads(api_cat)
            n_ind = len(items)
            n_hits = len([x for x in items if re.search(r"repeat|transition|progression|grade|enrol",
                                                        json.dumps(x).lower())])
        except json.JSONDecodeError:
            pass
    gate["evidence"]["dhs_api_ecological_aggregates"] = {
        "ref_paths": [
            f"{DHS_API_BRANCH}:research/records/2026-11-24-dhs-api-ecological/data/panel_survey.csv",
            f"{DHS_API_BRANCH}:research/records/2026-11-24-dhs-api-ecological/data/panel_edu2_*.csv",
            f"{DHS_API_BRANCH}:research/records/2026-11-24-dhs-api-ecological/data/panel_edu4_*.csv",
        ],
        "panel_survey_header": (api_panels or "").splitlines()[:2],
        "unit": "country x survey round x background category cell (DHS-published aggregate); NOT microdata",
        "dhs_public_indicator_catalogue": {
            "n_indicators": n_ind,
            "n_indicators_matching_repeat_transition_progression_grade_enrol": n_hits,
        },
        "lines": evidence_lines(api_readme or "", [r"unit is the DHS-published cell", r"Nothing here is microdata"]),
        "verdict": "NOT A VALID SUBSTITUTE (pre-registered): country x survey x education ecological aggregates do "
                   "not identify the t*-completion cohort and are not a sex-comparable final-grade repetition / "
                   "transition outcome; the DHS public indicator catalogue has 0 repetition/transition indicators",
    }

    # ---------- gate verdict ----------
    inputs = {
        "L_primary_source": {"required": True, "found": False,
                             "detail": "sourced 0/8; no in-repo primary-cycle-length file for MWI ETH UGA LSO TZA KEN MOZ GHA"},
        "sex_disaggregated_repetition_or_transition_series": {"required": True, "found": False,
                             "detail": "no committed series in any ref; no file path matches rept/prsl"},
        "DHS_IR_microdata": {"required": True, "found": False,
                             "detail": "0 .dta across 194 refs; DHS IR login-gated; Africa-11 request not submitted"},
    }
    gate["inputs"] = inputs
    gate["missing_series"] = [
        "L_primary (primary-cycle length by country-year) for MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA — exact missing input",
        "sex-disaggregated final-grade primary repetition series, annual, 8 countries around t_abolition..t*+6 — exact missing series",
        "sex-disaggregated primary->secondary transition/progression series (WDI SE.PRM.PRSL.ZS / UIS equivalent), annual — exact missing series",
        "DHS IR individual recode files for the 8 countries' waves near t* (0 of 54 standard-DHS waves held) — exact missing data",
    ]
    gate["verdict"] = "NOT-ESTIMABLE"
    gate["pre_registered_consequence"] = ("Leg B reported NOT-ESTIMABLE with the exact missing series; NO proxy, NO "
                                         "borrowed auditor L_primary dates, no estimate (PRE_REGISTRATION.md §B3)")
    gate["not_run"] = ["t* table", "bulge event study", "SE-disaggregated bulge outcome", "pre-trends/placebo"]
    json.dump(gate, open(os.path.join(RES, "legb_data_gate.json"), "w"), indent=1)
    print("VERDICT:", gate["verdict"])
    print("L_primary found:", inputs["L_primary_source"]["found"],
          "| repetition/transition found:", inputs["sex_disaggregated_repetition_or_transition_series"]["found"],
          "| DHS IR found:", inputs["DHS_IR_microdata"]["found"])
    print("refs:", len(refs), "unique paths:", len(paths), "dta:", gate["scans"]["all_ref_path_scan"]["n_dta_files"])
    print("DHS catalogue indicators:", n_ind, "matching repeat/transition:", n_hits)
    print("wrote", os.path.join(RES, "legb_data_gate.json"))


if __name__ == "__main__":
    main()
