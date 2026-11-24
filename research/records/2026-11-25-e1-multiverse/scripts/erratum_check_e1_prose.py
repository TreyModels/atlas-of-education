#!/usr/bin/env python3
"""Erratum check — E1 REPORT prose vs the record's own table/JSON and progress log.

Issue A: the sentence "Under the committed 136-parity convention the same pattern appears (BY het = 39 at
1,200; up/down/flip 0/0/0)" contradicts `results/summary_by_R.json` `families.1200.*.certified_BY136`.
Issue B: the runtime bullet says "min 31.1 s" worker wall; `results/progress.log` minimum is 31.045 s.

Writes `results/erratum_check_prose.json`.

Run (standard library only):  python3 scripts/erratum_check_e1_prose.py
"""
import json
import statistics as st

OUT = "results/erratum_check_prose.json"

summary = json.load(open("results/summary_by_R.json"))
fam = summary["families"]["1200"]
by136 = {proc: fam[proc].get("certified_BY136") for proc in ("up", "down", "flip", "het")}

# progress.log columns: <draw_index> <worker_wall_s> <cumulative_elapsed_s> <completed/expected>
walls = []
for line in open("results/progress.log"):
    parts = line.split()
    if len(parts) >= 2:
        try:
            walls.append(float(parts[1]))
        except ValueError:
            continue

out = {
    "issue_A_136_parity": {
        "original_sentence": ("Under the committed 136-parity convention the same pattern appears "
                              "(BY het = 39 at 1,200; up/down/flip 0/0/0)."),
        "committed_json": "results/summary_by_R.json families.1200.*.certified_BY136",
        "recomputed": by136,
        "prose_claim": {"het": 39, "up": 0, "down": 0, "flip": 0},
        "verdict": "MISMATCH: only the sign-flip zero is right; up=25 and down=15 also certify at 136 parity.",
    },
    "issue_B_runtime": {
        "original_sentence": ("per-draw worker wall mean 37.8 s, median 36.4 s, max 136.2 s (the real pass), "
                              "min 31.1 s (results/progress.log, results/run_meta.txt)"),
        "source": "results/progress.log column 2 (worker wall seconds), 1,201 rows",
        "recomputed": {
            "n": len(walls),
            "mean": round(st.mean(walls), 3),
            "median": round(st.median(walls), 3),
            "min": round(min(walls), 4),
            "max": round(max(walls), 4),
            "min_rounded_1dp": round(min(walls), 1),
            "min_truncated_1dp": int(min(walls) * 10) / 10,
        },
        "prose_claim": {"mean": 37.8, "median": 36.4, "max": 136.2, "min": 31.1},
        "verdict": ("MISMATCH at the stated precision: min is 31.045 s (rounds/truncates to 31.0), "
                    "not 31.1; the other three values reproduce."),
    },
    "reproduction": "python3 scripts/erratum_check_e1_prose.py (this record; stdlib only)",
    "audit_reference": ("research/prose-data-audit-2026-11-24 @ ff390fe, "
                        "research/records/2026-11-24-prose-data-audit/AUDIT.md checks E1-07 and E1-12"),
}
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(out, indent=1))
