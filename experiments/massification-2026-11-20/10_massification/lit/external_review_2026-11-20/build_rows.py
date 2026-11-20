#!/usr/bin/env python3
"""Assemble the external literature claim table from the three research workstreams.

Reads (whichever exist):
  rows_A_schooling_complexity.csv   (strands a + b + b2: schooling/cognitive skills/growth, ECI, education->complexity)
  rows_B_absorption_credential.csv  (strands c + d: thresholds/dual economy, educated unemployment/credential queue)
  rows_C_projections.csv            (strand e: existing projection models)

Writes:
  EXTERNAL_LITERATURE_ROWS.csv      one normalised row per checkable claim
  EXTERNAL_LITERATURE_CITE_INDEX.csv one row per unique source (authors+year+title) with URL and verification status

No number or citation is invented here: rows are passed through, only column names are normalised.
Floats/hashes are not involved; output is a deterministic function of the inputs (no timestamps).
"""
from __future__ import annotations

import csv
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent

INPUTS = [
    ("rows_A_schooling_complexity.csv", "A"),
    ("rows_A2_education_to_complexity.csv", "A2"),
    ("rows_B_absorption_credential.csv", "B"),
    ("rows_C_projections.csv", "C"),
]

UNIFIED = ["row_id", "strand", "claim", "status_or_model", "direction_or_magnitude",
           "magnitude_verbatim", "source_authors", "source_year", "source_title", "venue",
           "url", "doi", "verification_status", "notes", "workstream"]


def norm(row: dict, workstream: str) -> dict:
    g = lambda *keys: next((row.get(k, "") for k in keys if k in row), "")
    return {
        "row_id": row.get("row_id", ""),
        "strand": row.get("strand", ""),
        "claim": row.get("claim", ""),
        "status_or_model": g("what_is_established_or_contested", "model_or_dataset"),
        "direction_or_magnitude": g("direction_or_sign", "method"),
        "magnitude_verbatim": g("reported_magnitude_verbatim", "outputs"),
        "source_authors": row.get("source_authors", ""),
        "source_year": row.get("source_year", ""),
        "source_title": row.get("source_title", ""),
        "venue": row.get("venue", ""),
        "url": row.get("url", ""),
        "doi": row.get("doi", ""),
        "verification_status": row.get("verification_status", ""),
        "notes": g("notes", "reusability"),
        "workstream": workstream,
    }


def main():
    out = []
    present = []
    for fn, ws in INPUTS:
        p = HERE / fn
        if not p.exists():
            print(f"  MISSING (workstream {ws}): {fn}")
            continue
        present.append(fn)
        with open(p, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                out.append(norm(row, ws))
    outpath = HERE / "EXTERNAL_LITERATURE_ROWS.csv"
    with open(outpath, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=UNIFIED)
        w.writeheader()
        for r in out:
            w.writerow(r)
    # citation index: unique (authors, year, title) with url + best verification status
    rank = {"VERIFIED-FULLTEXT": 4, "VERIFIED": 3, "VERIFIED-ABSTRACT": 2,
            "VERIFIED-METADATA": 1, "VERIFIED-FROM-DISK": 3, "UNVERIFIED": 0, "": 0}
    idx = {}
    for r in out:
        key = (r["source_authors"], r["source_year"], r["source_title"])
        cur = idx.setdefault(key, {"source_authors": r["source_authors"], "source_year": r["source_year"],
                                   "source_title": r["source_title"], "urls": set(), "indicators": [],
                                   "verification_status": r["verification_status"]})
        if r["url"]:
            cur["urls"].add(r["url"])
        cur["indicators"].append(r["row_id"])
        if rank.get(r["verification_status"], 0) > rank.get(cur["verification_status"], 0):
            cur["verification_status"] = r["verification_status"]
    cidx = HERE / "EXTERNAL_LITERATURE_CITE_INDEX.csv"
    with open(cidx, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["source_authors", "source_year", "source_title",
                                           "verification_status", "urls", "indicator_rows"])
        w.writeheader()
        for key in sorted(idx):
            v = idx[key]
            w.writerow({**{k: v[k] for k in ("source_authors", "source_year", "source_title",
                                            "verification_status")},
                        "urls": " | ".join(sorted(v["urls"])),
                        "indicator_rows": " ".join(v["indicators"])})
    print(f"wrote {outpath.name}: {len(out)} rows from {len(present)} workstream files")
    print("verification_status:", dict(Counter(r["verification_status"] for r in out)))
    print(f"wrote {cidx.name}: {len(idx)} unique sources")


if __name__ == "__main__":
    main()
