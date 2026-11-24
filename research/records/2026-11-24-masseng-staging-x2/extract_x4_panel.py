#!/usr/bin/env python3
"""Deterministic extraction of the X4 aggregate panel from COMMITTED data only.

Source: origin/research/massification-panel-2026-11-22 (commit 7d25322e…) →
research/records/2026-11-22-massification-panel/sources/wdi_sweep/{prm_ner.json,
wage_emp.json.gz, emp_agri.json.gz, lsc.json, sec_ner.json, meta.json}.

Reads via `git show` (no network, no new pulls, no imputation). Values matched with a maximum
±2-year tolerance (declared). National countries only (meta region ≠ "Aggregates", 3-letter ISO3).
Writes x4_input/x4_panel.csv and x4_input/provenance.json. This is data assembly, not
model/statistical compute; the X4 analysis runs separately on region-42.
"""
import csv
import gzip
import hashlib
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "x4_input")
BRANCH = "origin/research/massification-panel-2026-11-22"
COMMIT = "7d25322e9997b60a88cb2c143c880e1cc174c569"
PREFIX = "research/records/2026-11-22-massification-panel/sources/wdi_sweep/"
FILES = {"edu": "prm_ner.json", "job": "wage_emp.json.gz", "job_alt": "emp_agri.json.gz",
         "out": "lsc.json", "out_alt": "sec_ner.json"}
TOL = 2
YEARS = {"edu": [1991, 1995, 1998, 2004, 2005], "job": [1991, 1995, 1998, 2004, 2005],
         "job_alt": [1991, 1995, 1998, 2004, 2005], "out": [1991, 2004, 2005, 2018, 2019],
         "out_alt": [2004, 2018]}


def blob(name):
    p = subprocess.run(["git", "-C", REPO, "show", f"{BRANCH}:{PREFIX}{name}"], capture_output=True)
    if p.returncode != 0:
        raise FileNotFoundError(f"{name}: {p.stderr.decode()[:200]}")
    return p.stdout


def load(name):
    raw = blob(name)
    if name.endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def main():
    os.makedirs(OUT, exist_ok=True)
    meta = json.loads(blob("meta.json"))
    national = {i for i, m in meta.items()
                if str(m.get("region", "")).strip() != "Aggregates" and len(i) == 3}
    raw_hashes = {f: sha(blob(f)) for f in FILES.values()}
    series = {}
    for key, f in FILES.items():
        rows = load(f)
        series[key] = {(r[0], int(r[1])): float(r[2]) for r in rows
                       if len(r) >= 3 and r[2] is not None and r[0] in national}

    def get(key, iso, year):
        for dy in (0, 1, -1, 2, -2):
            v = series[key].get((iso, year + dy))
            if v is not None:
                return v, year + dy
        return None, None

    isos = sorted({k[0] for k in series["out"]})
    rows = []
    matched_counts = {}
    for iso in isos:
        row = {"iso3": iso}
        for key, years in YEARS.items():
            for y in years:
                v, y_used = get(key, iso, y)
                row[f"{key}_{y}"] = "" if v is None else v
                row[f"{key}_{y}_year_used"] = "" if y_used is None else y_used
        rows.append(row)
    with open(os.path.join(OUT, "x4_panel.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    prov = {"label": "X4 aggregate panel extracted from committed data only; no simulation",
            "source_branch": BRANCH, "source_commit": COMMIT, "source_prefix": PREFIX,
            "source_file_sha256": raw_hashes, "national_filter": "meta region != 'Aggregates' and len(iso3)==3",
            "tolerance_years": TOL, "years_requested": YEARS, "n_national_countries": len(isos),
            "n_rows_written": len(rows), "rows_with_primary_outcome_2004_2018":
                sum(1 for r in rows if r["out_2004"] != "" and r["out_2018"] != ""),
            "extraction_script_sha256": sha(open(os.path.abspath(__file__), "rb").read()),
            "note": "values matched at ±2 years; year_used columns record the actual year; "
                    "no imputation; missing values left blank"}
    with open(os.path.join(OUT, "provenance.json"), "w") as f:
        json.dump(prov, f, indent=1)
    print(json.dumps({"n_countries": len(isos), "n_rows": len(rows),
                      "complete_primary_outcome": prov["rows_with_primary_outcome_2004_2018"],
                      "out": OUT}, indent=1))


if __name__ == "__main__":
    main()
