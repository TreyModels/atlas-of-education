#!/usr/bin/env python3
"""Erratum check C — does the REPORT's "weak forward-or-tie share ranges 56-84%" reproduce?

Reads the committed `results/n3_table.csv` (N3 threshold/smoothing/survival sweep, 54 definitions)
and recomputes the weak forward-or-tie quantities under the plausible denominators. Writes
`results/erratum_check_n3.json`.

Columns in `results/n3_table.csv`:
  n                 countries in the definition
  forward           demand take-off first (strict)
  forward_or_tie    weak forward ordering (demand at or before schooling, weak inequality)
  reverse           schooling take-off first (strict)
  undetermined      no ordering inside the window
  forward_share_incl_ties   (forward + forward_or_tie) / identifiable, already as a percentage

So the candidate "weak forward-or-tie share" quantities are:
  A. forward_or_tie / identifiable   (identifiable = n - undetermined)
  B. forward_or_tie / n
  C. forward_share_incl_ties        ((forward + forward_or_tie) / identifiable)
  D. (forward + forward_or_tie) / n

Erratum context: REPORT.md §3 says "the weak forward-or-tie share ranges 56-84%". This script shows
none of A-D spans 56-84 (with either denominator's exact endpoints), and no subset (q1-only,
non-survival) reproduces the endpoints either.

Run: python3 scripts/erratum_check_n3_prose.py   (stdlib only)
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HERE)
tab = list(csv.DictReader(open(os.path.join(REC, "results", "n3_table.csv"))))

assert len(tab) == 54, f"expected 54 definitions, got {len(tab)}"


def quantities(rows):
    out = []
    for r in rows:
        n = int(r["n"])
        und = int(r["undetermined"])
        ident = n - und
        fwd = int(r["forward"])
        tie = int(r["forward_or_tie"])
        out.append(dict(
            definition=r["definition"],
            n=n, identifiable=ident,
            tie_over_identifiable=100.0 * tie / ident,
            tie_over_n=100.0 * tie / n,
            incl_ties=float(r["forward_share_incl_ties"]),
            fwd_plus_tie_over_identifiable=100.0 * (fwd + tie) / ident,
            fwd_plus_tie_over_n=100.0 * (fwd + tie) / n,
        ))
    return out


def summarise(rows):
    q = quantities(rows)
    keys = ["tie_over_identifiable", "tie_over_n", "incl_ties",
            "fwd_plus_tie_over_identifiable", "fwd_plus_tie_over_n"]
    summary = {}
    for k in keys:
        vals = [x[k] for x in q]
        lo = min(vals)
        hi = max(vals)
        summary[k] = dict(
            min=round(lo, 4), max=round(hi, 4),
            min_definition=next(x["definition"] for x in q if x[k] == lo),
            max_definition=next(x["definition"] for x in q if x[k] == hi),
            includes_both_56_and_84=bool(lo <= 56.0 and hi >= 84.0
                                        and lo >= 55.0 and hi <= 85.0),
        )
    return summary


out = dict(
    question='Does "(the weak forward-or-tie share ranges 56-84%)" reproduce from results/n3_table.csv?',
    answer="NO — no denominator (or subset) gives endpoints 56 and 84.",
    source="results/n3_table.csv (54 definitions; all have n>=20)",
    n_definitions=len(tab),
    all_definitions=summarise(tab),
    q1_only=summarise([r for r in tab if r["definition"].startswith("q1")]),
    non_survival=summarise([r for r in tab if not r["definition"].startswith("survival")]),
    conclusion=(
        "The reproducible quantities are: weak tie share of identifiable countries 56.67-88.46%; "
        "of all n 50.00-82.14%; forward_share_incl_ties 56.70-100.00%; (forward+forward_or_tie)/identifiable "
        "56.67-100.00%; (forward+forward_or_tie)/n 50.00-92.86%. None spans 56-84, and restricting to "
        "q1-only or non-survival definitions does not change this. The REPORT's 56-84% line is a stale or "
        "hand-rounded range; it should be replaced by one of the reproducible quantities with its "
        "denominator stated."
    ),
    reproduces="scripts/erratum_check_n3_prose.py (this record, task-10).",
)

json.dump(out, open(os.path.join(REC, "results", "erratum_check_n3.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
