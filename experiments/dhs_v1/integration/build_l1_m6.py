#!/usr/bin/env python3
"""L1 → M6 linkage prototype (non-disclosive aggregates only).

L1 = `harmonize/_out/aggregate_layer.csv` — survey-wave domain estimates with
design-based SEs (household microdata already reduced to aggregates; NOT included).
M6 = public DHS API indicator panels from the prior M6 record
(`~/neon-boot/wt2/dhseco/research/records/2026-11-24-dhs-api-ecological/data/
panel_edu{2,4}_FE_*.csv`) — public country-year aggregates, ecological only.

The prototype attaches same-year and 5-year-lagged contextual indicators to each
L1 cell, preserving source file+sha256, survey, year, education stratum, unit and
missingness. It is EXPLORATORY: contemporaneous/lagged context attached to a
descriptive survey mean is not an exposure, and no causal claim is made. Country-
level covariates must not be treated as household-level measurements (ecological
fallacy guard); the effective N for cross-country statements is the number of
countries (4 here), not the number of cells.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]        # .../experiments/dhs_v1
L1 = ROOT / "harmonize" / "_out" / "aggregate_layer.csv"
M6_DIR = Path.home() / "neon-boot" / "wt2" / "dhseco" / "research" / "records" / "2026-11-24-dhs-api-ecological" / "data"
OUT = ROOT / "integration"
COUNTRIES = ["KH", "ID", "PH", "VN"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wave_year(w) -> int | None:
    m = re.search(r"(19|20)\d{2}", str(w))
    return int(m.group(0)) if m else None


def load_l1() -> pd.DataFrame:
    d = pd.read_csv(L1)
    d["year"] = d["wave"].map(wave_year)
    d = d[d["country"].isin(COUNTRIES)].copy()
    if "suppressed" in d.columns:
        d = d[d["suppressed"].astype(str).str.lower().isin(["false", "0", "no"])]
    return d


def load_m6() -> tuple[pd.DataFrame, dict]:
    panels, meta = [], {}
    for p in sorted(M6_DIR.glob("panel_edu*_*.csv")):
        if p.name.endswith(".csv") is False:
            continue
        x = pd.read_csv(p)
        if "country" not in x.columns:
            continue
        x = x[x["country"].isin(COUNTRIES)].copy()
        if x.empty:
            continue
        x["source_panel"] = p.name
        x["source_sha256"] = sha256(p)
        panels.append(x)
        meta[p.name] = {"sha256": sha256(p), "rows_4countries": int(len(x)),
                        "years": [int(x["year"].min()), int(x["year"].max())]}
    return (pd.concat(panels, ignore_index=True) if panels else pd.DataFrame()), meta


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    l1 = load_l1()
    m6, m6meta = load_m6()
    if l1.empty:
        raise SystemExit("no L1 rows")
    rows, gaps = [], []
    for _, cell in l1.iterrows():
        if pd.isna(cell["year"]):
            continue
        for lag, tag in ((0, "same_year"), (5, "lag5y")):
            target = int(cell["year"]) - lag
            hit = m6[(m6["country"] == cell["country"]) & (m6["year"] == target)]
            if hit.empty:
                gaps.append({"country": cell["country"], "wave": cell["wave"],
                             "experiment": cell["experiment"], "lag": tag,
                             "requested_year": target})
                continue
            for _, m in hit.iterrows():
                rows.append({
                    "experiment": cell["experiment"], "country": cell["country"],
                    "wave": cell["wave"], "survey_year": int(cell["year"]),
                    "outcome": cell.get("outcome"), "group_var": cell.get("group_var"),
                    "group": cell.get("group"), "estimate": cell.get("estimate"),
                    "se": cell.get("se"), "n_complete": cell.get("n_complete"),
                    "indicator": m.get("indicator"), "indicator_edu": m.get("edu"),
                    "indicator_edu_level": m.get("edu_level"),
                    "indicator_value": m.get("value"), "indicator_year": int(m["year"]),
                    "indicator_survey": m.get("survey"), "lag": tag,
                    "lag_years": lag, "source_panel": m.get("source_panel"),
                    "source_sha256": m.get("source_sha256"),
                    "unit": "indicator value as published by DHS API (indicator-specific; see catalogue)",
                    "evidence_class": "exploratory_descriptive_context",
                    "causal_claim": False,
                    "ecological_caution": True,
                })
    proto = pd.DataFrame(rows)
    proto.to_csv(OUT / "prototype_l1_m6.csv", index=False)
    pd.DataFrame(gaps).to_csv(OUT / "prototype_missing_links.csv", index=False)

    # coverage summary
    cov = (proto.groupby(["country", "lag"])
           .agg(cells=("experiment", "size"), experiments=("experiment", "nunique"),
                indicators=("indicator", "nunique")).reset_index()) if not proto.empty else pd.DataFrame()
    cov.to_csv(OUT / "prototype_coverage.csv", index=False)
    manifest = {
        "prototype_version": "l1-m6-v0.1",
        "created_by": "deepseek-dhs (lead)",
        "inputs": {"l1": {"path": str(L1), "sha256": sha256(L1), "rows": int(len(l1))},
                   "m6": m6meta},
        "counts": {"prototype_rows": int(len(proto)), "missing_links": int(len(gaps)),
                   "countries": COUNTRIES, "effective_n_countries": len(COUNTRIES)},
        "rules": {
            "join": "country (ISO2) + indicator year; same_year = survey start year, lag5y = start year - 5",
            "lag_policy": "lagged context attached only as context; no exposure claim; timing recorded per row",
            "inference_guard": "country-level covariates are not household measurements (ecological fallacy); effective N = 4 countries for cross-country statements",
            "disclosure": "L1 rows are aggregates; household microdata never included",
            "evidence_label": "exploratory descriptive; no causal interpretation",
        },
        "m6_restriction": "public DHS API aggregates only; M1/M3 country-year matrices are not local and are declared out of scope for this prototype",
        "subnational": "BLOCKED (survey regions + displaced GPS; no defensible subnational macro source)",
    }
    (OUT / "prototype_manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"[l1-m6] {len(l1)} L1 cells -> {len(proto)} prototype rows; "
          f"{len(gaps)} missing links; coverage:\n{cov.to_string(index=False) if not cov.empty else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
