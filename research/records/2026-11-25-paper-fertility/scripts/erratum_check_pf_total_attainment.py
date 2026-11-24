#!/usr/bin/env python3
"""Erratum check — Paper F total-attainment level coefficient is -0.227458, not -0.228.

The committed source is `research/corr-rebuild-2026-11-23` @ `161b563`,
`research/records/2026-11-23-corr-rebuild/data/results_part1.json`, field `lags.mys_total["0"].b`
(-- and `.se`, `.n`, `.nc`). Paper F's draft/claims map round it to -0.228; the committed value
rounds to -0.227 at three decimals (-0.227458 → -0.227).

Usage:
    # from a checkout with the corr-rebuild commit available:
    git show 161b563:research/records/2026-11-23-corr-rebuild/data/results_part1.json \
        > /tmp/results_part1.json
    python3 scripts/erratum_check_pf_total_attainment.py /tmp/results_part1.json

Writes `data/erratum_check_pf_total_attainment.json`.
"""
import json
import sys

src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/results_part1.json"
d = json.load(open(src))
v = d["lags"]["mys_total"]["0"]
b = float(v["b"])
out = {
    "question": "Does Paper F's -0.228 (0.042) reproduce for the total-attainment level coefficient?",
    "answer": ("NO at the stated 3-dp precision: the committed value is -0.227458..., which rounds to "
               "-0.227 (and truncates to -0.227), not -0.228. A 0.0005 boundary slip."),
    "source": ("research/corr-rebuild-2026-11-23 @ 161b563, "
               "research/records/2026-11-23-corr-rebuild/data/results_part1.json, "
               "field lags.mys_total['0']"),
    "recomputed": {"b": b, "b_round_3dp": round(b, 3), "b_round_4dp": round(b, 4),
                    "se": float(v["se"]), "n": int(v["n"]), "nc": int(v["nc"])},
    "paper_claim": {"b": -0.228, "se": 0.042, "n": 1394, "nc": 144},
    "reproduction": ("git show 161b563:research/records/2026-11-23-corr-rebuild/data/results_part1.json "
                     "> /tmp/results_part1.json && python3 scripts/erratum_check_pf_total_attainment.py "
                     "/tmp/results_part1.json"),
    "audit_reference": ("research/prose-data-audit-2026-11-24 @ ff390fe, "
                        "research/records/2026-11-24-prose-data-audit/AUDIT.md check PF-02"),
    "occurrences_not_changed": [
        "draft/paperF_draft.md line 67 (§1.2)",
        "draft/paperF_draft.md line 468 (Table 1)",
        "draft/paperF_draft.md line 495 (income-rival paragraph)",
        "draft/frame_intro_new.md line 67 (same sentence as the draft)",
        "sections/section1_levels_changes.md line 79 (table) and line 106 (income-rival)",
        "data/claims_sources.csv row A1 'levels coefficient total attainment'",
    ],
}
json.dump(out, open("data/erratum_check_pf_total_attainment.json", "w"), indent=1)
print(json.dumps(out, indent=1))
