#!/usr/bin/env python3
"""Descriptive key contrasts from the unified DHS estimate table (EXPLORATORY).

No causal interpretation: these are within-wave differences of weighted domain means
with design-based SEs.  Groups are independent domains, so SE(diff) = sqrt(se1^2+se2^2).
BH q-values are computed within each experiment family (pre-declared: all country-waves
of that experiment).
"""
import sys
from pathlib import Path
import numpy as np
from math import erf, sqrt as msqrt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "runs" / "2026-11-25_final" / "estimates_final.csv"
outdir = src.parent
d = pd.read_csv(src)
d = d[d["suppressed"] != True] if "suppressed" in d.columns else d

SPEC = {  # experiment: (group_a, group_b, label)
    "E1": ("5", "1", "Q5minusQ1_attendance"),
    "E2": ("1", "0", "urban_minus_rural"),
    "E3": ("1", "2", "male_minus_female"),
    "E4": ("12+", "0-5", "schooling12plus_minus_0to5"),
    "E5": ("12+", "0-5", "schooling12plus_minus_0to5"),
    "E6": ("1", "0", "urban_minus_rural"),
    "E7": ("12+", "0-5", "schooling12plus_minus_0to5"),
    "E8": ("12+", "0-5", "schooling12plus_minus_0to5"),
}
rows = []
for _, cell in d.groupby(["experiment", "country", "wave"]).__iter__() if False else []:
    pass
for (exp, country, wave), g in d.groupby(["experiment", "country", "wave"]):
    if exp not in SPEC:
        continue
    ga, gb, label = SPEC[exp]
    a = g[g["group"].astype(str) == ga]
    b = g[g["group"].astype(str) == gb]
    if len(a) != 1 or len(b) != 1:
        continue
    a, b = a.iloc[0], b.iloc[0]
    est = float(a["estimate"]) - float(b["estimate"])
    se = float(np.sqrt(float(a["se"]) ** 2 + float(b["se"]) ** 2))
    rows.append({"experiment": exp, "country": country, "wave": wave, "contrast": label,
                 "group_a": ga, "group_b": gb, "diff": est, "se": se,
                 "lo95": est - 1.96 * se, "hi95": est + 1.96 * se,
                 "z": est / se if se > 0 else np.nan,
                 "n_a": a.get("n_unweighted"), "n_b": b.get("n_unweighted"),
                 "evidence": "descriptive within-wave difference of weighted domain means",
                 "causal_claim": False})
c = pd.DataFrame(rows)
if len(c):
    c["p_normal"] = 1 - np.vectorize(lambda z: erf(abs(z) / msqrt(2)))(c["z"].astype(float))
    for exp, idx in c.groupby("experiment").groups.items():
        p = c.loc[idx, "p_normal"].astype(float)
        order = p.sort_values().index
        m = len(p)
        q = (p.loc[order].to_numpy() * m / np.arange(1, m + 1)).clip(max=1.0)
        q = np.minimum.accumulate(q[::-1])[::-1]
        c.loc[order, "q_bh_by_experiment"] = q
    c.to_csv(outdir / "contrasts_final.csv", index=False)
    print(f"wrote {len(c)} contrasts -> {outdir/'contrasts_final.csv'}")
    print(c.groupby("experiment").size().to_string())
    print("\nlargest |diff| (descriptive):")
    print(c.reindex(c["diff"].abs().sort_values(ascending=False).index)[["experiment", "country", "wave", "contrast", "diff", "se", "q_bh_by_experiment"]].head(10).to_string(index=False))
else:
    print("no contrasts computed")
