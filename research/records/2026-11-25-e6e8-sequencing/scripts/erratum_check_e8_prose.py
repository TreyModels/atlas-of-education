#!/usr/bin/env python3
"""Erratum check D — E8 prose ranges vs results/e8_results.json.

D.1  REPORT §2 Estimator says "25-30 control countries per event" next to the verified-8 table.
     The verified-8 event table has 28-30 controls; 25 is reached only in the all-12 sensitivity.
D.2  REPORT §2 Decision-rule assessment says "(mean post 18-29 points against ~0 under placebo)".
     The reproducible mean-post quantities are: verified-8 mean of CS post ATTs (+1..+6) = 25.26;
     sensitivity mean_att_post all+1 12.31, all-1 18.65, all12 20.80, leave-one-out 18.17-26.16,
     placebo -0.39. No quantity spans 18-29.

Writes `results/erratum_check_e8_prose.json`.
Run (standard library only):  python3 scripts/erratum_check_e8_prose.py
"""
import json

OUT = "results/erratum_check_e8_prose.json"
e8 = json.load(open("results/e8_results.json"))

verified = e8["results"]["SE.PRM.ENRR_verified8"]["event_table"]
all12 = e8["results"]["SE.PRM.ENRR_all12"]["event_table"]
controls_v8 = [r["n_controls"] for r in verified]
controls_12 = [r["n_controls"] for r in all12]
post_att = [r["att"] for r in verified if r["event"] in (1, 2, 3, 4, 5, 6)]
mean_post_v8 = sum(post_att) / len(post_att)

sens = {s["spec"]: round(s["mean_att_post"], 2) for s in e8["sensitivity"]}
loo = [s["mean_att_post"] for s in e8["sensitivity"] if s["spec"].startswith("drop-")]

out = {
    "issue_D1_controls": {
        "original_sentence": ("Seven treated countries have outcome data (one verified country lacks GER "
                              "coverage); 25-30 control countries per event."),
        "source": "results/e8_results.json SE.PRM.ENRR_verified8.event_table / SE.PRM.ENRR_all12.event_table, n_controls",
        "recomputed": {
            "verified8_n_controls_min": int(min(controls_v8)),
            "verified8_n_controls_max": int(max(controls_v8)),
            "all12_n_controls_min": int(min(controls_12)),
            "all12_n_controls_max": int(max(controls_12)),
        },
        "prose_claim": {"min": 25, "max": 30},
        "verdict": ("MISMATCH for the verified-8 table: actual 28-30; 25-30 is the all-12 sensitivity. "
                    "Recommended: '28-30 controls per event' for the main table, with 25-30 noted for the "
                    "all-12 sensitivity."),
    },
    "issue_D2_mean_post": {
        "original_sentence": ("(mean post 18-29 points against ~0 under placebo)"),
        "source": "results/e8_results.json event_table + sensitivity",
        "recomputed": {
            "verified8_mean_post_att_+1_to_+6": round(mean_post_v8, 2),
            "sensitivity_mean_att_post": sens,
            "leave_one_out_range": [round(min(loo), 2), round(max(loo), 2)],
            "placebo_mean_att_post": sens["placebo-6"],
        },
        "prose_claim": {"min": 18, "max": 29},
        "verdict": ("MISMATCH: no mean-post quantity spans 18-29. Reproducible range across the +-1-year and "
                    "leave-one-out checks is 12.31-26.16; recommended replacement: 'mean post 12.3-26.2 across "
                    "the +-1-year and leave-one-out checks, against -0.39 under the placebo'."),
    },
    "issue_D3_metadata": {
        "note": ("E6/E8 ERRATUM §B quotes the 9a0fd69 commit message, which says 'prior art Q1-Q3 "
                 "(24 DOI-verified)'. The source-verification record's own tables mark 21 V / 2 U / 1 W; that "
                 "record now carries a metadata erratum (head ea6bc61). No E6/E8 data change."),
    },
    "reproduction": "python3 scripts/erratum_check_e8_prose.py (this record; stdlib only)",
    "audit_reference": ("research/prose-data-audit-2026-11-24 @ ff390fe, "
                        "research/records/2026-11-24-prose-data-audit/AUDIT.md checks E6-11 and E8 decision-rule"),
}
assert out["issue_D1_controls"]["recomputed"]["verified8_n_controls_min"] == 28
assert out["issue_D1_controls"]["recomputed"]["verified8_n_controls_max"] == 30
assert out["issue_D1_controls"]["recomputed"]["all12_n_controls_min"] == 25
assert out["issue_D1_controls"]["recomputed"]["all12_n_controls_max"] == 30
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(out, indent=1))
