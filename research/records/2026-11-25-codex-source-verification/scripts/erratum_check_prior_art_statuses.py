#!/usr/bin/env python3
"""Erratum check — metadata: the 9a0fd69 commit message says "24 DOI-verified";
the record's own Job-3 prior-art tables mark 21 V / 2 U / 1 W.

The commit message cannot be edited without rewriting history, so the correct tallies are recorded in
ERRATUM.md and pointed at from README.md. This script parses the three Job-3 tables in README.md and
recounts the status column (V = DOI verified, W = working-paper version, U = no DOI / book / pre-DOI).

Writes `results/erratum_check_prior_art.json`.

Run (standard library only):  python3 scripts/erratum_check_prior_art_statuses.py
"""
import json
import re

README = "README.md"
lines = open(README, encoding="utf-8").read().split("\n")

tables = {"Q1": [], "Q2": [], "Q3": []}
current = None
for ln in lines:
    m = re.match(r"^### (Q[123]) — ", ln)
    if m:
        current = m.group(1)
        continue
    if ln.startswith("## ") and current is not None and not ln.startswith("### "):
        current = None
    if current and ln.strip().startswith("|"):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 4 and not set(cells[0]) <= set("-: ") and cells[0] != "#":
            tables[current].append(cells[3])  # Status column

counts = {"V": 0, "W": 0, "U": 0}
per_table = {}
for q, statuses in tables.items():
    c = {"V": 0, "W": 0, "U": 0, "n": len(statuses)}
    for s in statuses:
        for k in ("V", "W", "U"):
            if s.startswith(k):
                c[k] += 1
                counts[k] += 1
                break
    per_table[q] = c

out = {
    "question": ("Does the 9a0fd69 commit-message description 'prior art Q1-Q3 (24 DOI-verified)' match "
                 "the record's Job-3 tables?"),
    "answer": ("NO — the tables contain 24 prior-art works, of which 21 are V (DOI verified), 2 are U "
               "(books/no DOI) and 1 is W (working-paper version whose published DOI is not verified). "
               "The commit message cannot be edited without rewriting history; this metadata erratum "
               "records the correct description."),
    "source": "README.md, Job 3 tables (Q1/Q2/Q3, 8 works each)",
    "per_table": per_table,
    "totals": counts,
    "n_works": sum(counts.values()),
    "correct_description": ("24 prior-art works checked; 21 DOIs verified (V), 2 works without DOI (U), "
                            "1 working-paper version with the published DOI unverified (W)."),
    "repo_hint": "git show -s --format=%B 9a0fd69",
    "reproduction": "python3 scripts/erratum_check_prior_art_statuses.py (this record; stdlib only)",
    "audit_reference": ("research/prose-data-audit-2026-11-24 @ ff390fe, "
                        "research/records/2026-11-24-prose-data-audit/AUDIT.md check SV-04"),
}
json.dump(out, open("results/erratum_check_prior_art.json", "w"), indent=1)
print(json.dumps(out, indent=1))
