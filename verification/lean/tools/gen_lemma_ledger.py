#!/usr/bin/env python3
"""Generate docs/audit/LEMMA_LEDGER.md and docs/audit/LEMMA_LEDGER.csv.

Reads the committed claim baseline `results/audit/paper_claims.csv` (row count and sha256
are derived from the file at generation time; there are no hard-coded counts) and the
Lead-scoped Lean declaration map below, then emits:
  * one row per csv claim: either a Lean declaration (18 Lead-scoped claims) or an explicit
    `NOT-YET-LEMMATISED` entry (all remaining rows) — so the QA mechanical check
    "every row has exactly one declaration or an explicit not-yet entry" is directly runnable;
  * the four-kind table, the sorry ledger, axiom-audit record and the extension plan.

The generator FAILS LOUDLY (exit 2) if `--expect-sha`/`--expect-rows` are given and the
baseline has moved, so a stale ledger cannot be committed silently. It always writes
`docs/audit/LEMMA_LEDGER_BASELINE.json` with the exact baseline sha256 + row count the ledger
was generated against (that is the hash QA should pin).

Usage:  python3 verification/lean/tools/gen_lemma_ledger.py \
            [--out docs/audit/LEMMA_LEDGER.md] [--expect-sha SHA256] [--expect-rows N]
"""
import argparse
import csv
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CSV_PATH = os.path.join(REPO, "results", "audit", "paper_claims.csv")

# Lead-scoped starting rows -> Lean declarations (mirrors Atlas/Claims.lean `claimLedger`).
DECLARED = {
    "A-34": dict(kind="computational", status="computationallyChecked",
                 decl="A34_arithmetic (+ A34_empirical hypothesis)",
                 note="exact milli-pp tolerance check proved; empirical estimate is a data hypothesis"),
    "A-35": dict(kind="empirical", status="hypothesis", decl="A35_empirical",
                 note="CS-style ATT numbers are data, not theorem"),
    "A-36": dict(kind="empirical", status="hypothesis", decl="A36_empirical",
                 note="no-effect evidence (UNRESOLVED)"),
    "A-37": dict(kind="spec", status="specified", decl="A37_spec",
                 note="simulation forecast: specification + differential-test contract"),
    "A-38": dict(kind="computational", status="computationallyChecked", decl="A38_anchor_infeasible",
                 note="infeasibility arithmetic in exact units"),
    "A-39": dict(kind="spec", status="specified", decl="A39_spec",
                 note="rank/nullity exact-matrix computable; SV/conditioning floats are artifact evidence"),
    "B-41": dict(kind="computational", status="computationallyChecked",
                 decl="B41_HK_meets_criterion, B41_KR_TRACKED_meets_criterion, B41_KR_SINGLE_meets_criterion",
                 note="Win-Win accounting criterion proved for cited cells; welfare interpretation unproved"),
    "B-42": dict(kind="computational", status="computationallyChecked",
                 decl="B42_CF4b_fails_spend_HK, B42_CF1b_fails_spend_HK, B42_CF3b_passes_both",
                 note="accounting values falsify the 'only pairing works' reading"),
    "B-43": dict(kind="spec", status="specified", decl="B43_spec",
                 note="provenance/hash-chain correction; not a mathematical proposition"),
    "B-44": dict(kind="spec", status="specified", decl="B44_spec",
                 note="participation deltas accounting; welfare caveat not formalizable from current data"),
    "C-01": dict(kind="empirical", status="hypothesis", decl="C01_empirical",
                 note="provisional anchor, design-only"),
    "C-02": dict(kind="empirical", status="hypothesis", decl="C02_empirical",
                 note="provisional anchor, design-only"),
    "C-03": dict(kind="empirical", status="hypothesis", decl="C03_empirical",
                 note="provisional anchor, design-only"),
    "C-04": dict(kind="spec", status="specified", decl="C04_spec",
                 note="design cells + prereg requirement; no run yet"),
    "D-01": dict(kind="omission", status="proved",
                 decl="classical_demand_ignores_school_supply, ..._positional_seats, ..._withholding, ..._time_budget, ..._supply_form",
                 note="five omission/independence lemmas proved by definitional invariance"),
    "D-02": dict(kind="theoremProved", status="proved", decl="D02_paradox_not_universal",
                 note="contradiction-pattern illustration in a toy encoding; real record is artifact evidence"),
    "D-03": dict(kind="spec", status="specified", decl="D03_spec",
                 note="pre-registerable divergence tests, not results"),
    "D-04": dict(kind="empirical", status="hypothesis", decl="D04_attribution",
                 note="citation/attribution risk is not a mathematical proposition; declared as an empirical hypothesis record, never a theorem"),
}

# What would prove the unproved-but-declared statements (sorry-ledger analogue; 0 sorries).
WOULD_PROVE = {
    "A-34": "n/a for the Lean part (arithmetic proved). The empirical estimate would require the fresh-WDI panel + estimator formalized or reproduced as a fixture.",
    "A-35": "data + CS estimator formalization (or exact fixture from the artifact); not a theorem of the model.",
    "A-36": "same as A-35; no-effect statement requires the estimator and data.",
    "A-37": "exact-rational re-encoding of the forecast scoring function + engine fixtures; float32 internals stay out of Lean.",
    "A-39": "the exact rational Jacobian matrix as a fixture; rank/nullity provable by `decide`; SV/conditioning floats stay artifact evidence.",
    "B-43": "hash-chain provenance check in Python; not a Lean proposition.",
    "B-44": "welfare interpretation needs learning/access/teacher-workload/student-time data not in the programme; Lean records only the accounting criterion.",
    "C-01": "a formal model of the private-market regime + a fixture showing the engine's own_ban/mode settings; design-only today.",
    "C-02": "formal substitution channel (school-supplied prep S) in the model; Tier-1b extension.",
    "C-03": "formal withholding/rent channel with firm-fee response; model extension + fixtures.",
    "C-04": "pre-registration + executed grid; Lean can formalize the design schema now.",
    "D-03": "pre-registration + executed divergence tests; Lean can formalize the schema now.",
    "D-04": "primary-source citation verification (not a Lean task).",
}

KIND_LABEL = {
    "definition": "1 definition",
    "theoremProved": "2 theorem",
    "computational": "3 computational",
    "omission": "4 omission/independence",
    "empirical": "empirical (hypothesis)",
    "spec": "spec (differential contract)",
}


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def short(s, n=110):
    s = esc(s)
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "docs", "audit", "LEMMA_LEDGER.md"))
    ap.add_argument("--csv-out", default=os.path.join(REPO, "docs", "audit", "LEMMA_LEDGER.csv"))
    ap.add_argument("--axioms", default="", help="optional #print axioms output file")
    ap.add_argument("--expect-sha", default="", help="fail loudly unless the claims CSV has this sha256")
    ap.add_argument("--expect-rows", type=int, default=0, help="fail loudly unless the claims CSV has this row count")
    ap.add_argument("--baseline-out", default=os.path.join(REPO, "docs", "audit", "LEMMA_LEDGER_BASELINE.json"))
    args = ap.parse_args()

    raw = open(CSV_PATH, "rb").read()
    baseline_sha = hashlib.sha256(raw).hexdigest()
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    if not rows:
        sys.exit("empty paper_claims.csv")
    if args.expect_sha and baseline_sha != args.expect_sha:
        sys.exit(f"FATAL: claims baseline moved: expected sha256 {args.expect_sha}, "
                 f"found {baseline_sha} — refusing to generate a stale ledger")
    if args.expect_rows and len(rows) != args.expect_rows:
        sys.exit(f"FATAL: claims baseline moved: expected {args.expect_rows} rows, "
                 f"found {len(rows)} — refusing to generate a stale ledger")
    ids = [r["claim_id"] for r in rows]
    missing = [cid for cid in DECLARED if cid not in ids]
    if missing:
        sys.exit(f"Lead-scoped claim ids missing from paper_claims.csv: {missing}")

    declared = [r for r in rows if r["claim_id"] in DECLARED]
    not_yet = [r for r in rows if r["claim_id"] not in DECLARED]

    kind_counts = {}
    status_counts = {}
    for r in declared:
        d = DECLARED[r["claim_id"]]
        kind_counts[d["kind"]] = kind_counts.get(d["kind"], 0) + 1
        status_counts[d["status"]] = status_counts.get(d["status"], 0) + 1

    axioms_note = "not captured in this generation (run `verification/lean/ci/lean_verify.sh`)"
    if args.axioms and os.path.isfile(args.axioms):
        axioms_note = open(args.axioms, encoding="utf-8").read().strip()

    L = []
    L.append("# LEMMA LEDGER — claim-by-claim Lean map (Atlas verification prototype)")
    L.append("")
    L.append("**Owner:** `audit-runner` · **Date:** 2026-11-25 · **Host-only** (no box use)")
    L.append("")
    L.append("**Machine-readable companion:** [`LEMMA_LEDGER.csv`](LEMMA_LEDGER.csv) (one row per `paper_claims.csv` claim).")
    L.append("**Lean source:** [`verification/lean/Atlas/Claims.lean`](../../verification/lean/Atlas/Claims.lean) "
             "(18 Lead-scoped claims, one declaration group each). **Baseline:** "
             "[`results/audit/paper_claims.csv`](../../results/audit/paper_claims.csv) "
             f"({len(rows)} rows, committed).")
    L.append("")
    L.append("**Binding rule:** *Lean proves the reference mathematics and the accounting/inventory identities; the "
             "Python engine is differential-tested against Lean witnesses on fixtures; numerical results remain "
             "reproducible-artifact evidence. This is not \"the engine is verified\".*")
    L.append("")
    L.append("**No silent `sorry`:** this project contains **0 `sorry`s**. Claims that cannot be theorems are "
             "`EmpiricalClaim`/`SpecClaim` records (statement + artifact hashes + status), never asserted. "
             "Unproved ≠ false; empirical ≠ theorem. CI runs `grep sorry` and `#print axioms`.")
    L.append("")
    L.append("## Scope of this ledger generation")
    L.append("")
    L.append(f"- **Declared now:** {len(declared)} Lead-scoped claims — "
             "A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04.")
    L.append(f"- **Explicit NOT-YET-LEMMATISED:** {len(not_yet)} of the {len(rows)} baseline rows "
             "(listed individually below with their ids — no silent omissions).")
    L.append("- Extension plan: next pass adds the remaining rows in paper order; the four-kind schema and "
             "status vocabulary are stable, so adding a row is one declaration + one ledger row.")
    L.append("")
    L.append("## Four statement kinds")
    L.append("")
    L.append("| kind | meaning | Lean encoding | examples |")
    L.append("|---|---|---|---|")
    L.append("| 1 definition | model objects; units/domains stated; no partial functions | `structure`/`def` in "
             "`Atlas/Definitions.lean` | `Cohort`, `Gate`, `seatCount`, `Budget`, `TaxLedger`, `PrepStock`, `EqState` |")
    L.append("| 2 theorem | identities and finite PL math, proved | `theorem` in `Atlas/Identities.lean`, "
             "`Atlas/PlackettLuce.lean` | `budget_ledger_identity`, `prep_recursion_closed_form`, "
             "`pl_top1_sum_eq_denom`, `pl_topK_selected_sum` |")
    L.append("| 3 computational | numeric claims as exact re-encodings, `decide`-checked; or spec + differential contract | "
             "`theorem … := by decide` and `SpecClaim` records in `Atlas/Claims.lean` | `A34_arithmetic`, "
             "`A38_anchor_infeasible`, `B41_*`, `B42_*`, `A37_spec`, `A39_spec` |")
    L.append("| 4 omission/independence | inventory equation invariant to each omitted channel; recorded contradictions as `¬` | "
             "`theorem … := rfl` / `¬` in `Atlas/Claims.lean` | `classical_demand_ignores_school_supply` … `_supply_form`; "
             "`D02_paradox_not_universal` |")
    L.append("")
    L.append("Counts (declared rows): " + ", ".join(
        f"{KIND_LABEL.get(k, k)} = {v}" for k, v in sorted(kind_counts.items())) + ".")
    L.append("Status counts: " + ", ".join(f"`{k}` = {v}" for k, v in sorted(status_counts.items())) + ".")
    L.append("")
    L.append("## Declared claims (18)")
    L.append("")
    L.append("| claim | paper | kind | status | Lean declaration | claim (short) | note |")
    L.append("|---|---|---|---|---|---|---|")
    for r in declared:
        cid = r["claim_id"]
        d = DECLARED[cid]
        L.append(f"| {cid} | {esc(r['paper'])} | {KIND_LABEL.get(d['kind'], d['kind'])} | `{d['status']}` | "
                 f"`{esc(d['decl'])}` | {short(r['claim'])} | {esc(d['note'])} |")
    L.append("")
    L.append("## Not-yet-lemmatised claims (" + str(len(not_yet)) + ")")
    L.append("")
    L.append("These rows have **no Lean declaration yet** by design — explicit entries so the QA check has no "
             "silent gaps. Status: `NOT-YET-LEMMATISED`; paper claims' own evidence status is preserved in the "
             "baseline (`results/audit/paper_claims.csv`).")
    L.append("")
    L.append("| claim | paper | baseline status | claim (short) |")
    L.append("|---|---|---|---|")
    for r in not_yet:
        L.append(f"| {esc(r['claim_id'])} | {esc(r['paper'])} | {esc(r['status'])} | {short(r['claim'], 130)} |")
    L.append("")
    L.append("## Sorry ledger")
    L.append("")
    L.append("**Zero `sorry`s in `verification/lean/`.** For every declared-but-unproved statement, the table below "
             "records *what would prove it* (the \"sorry ledger\" analogue; these are `hypothesis`/`specified` "
             "declarations, not admitted proofs).")
    L.append("")
    L.append("| claim | status | why unproved | what would prove it |")
    L.append("|---|---|---|---|")
    for r in declared:
        cid = r["claim_id"]
        d = DECLARED[cid]
        if d["status"] in ("proved", "computationallyChecked"):
            continue
        L.append(f"| {cid} | `{d['status']}` | "
                 + ("empirical/world statement — not a mathematical theorem" if d["status"] == "hypothesis"
                    else "not a mathematical proposition" if d["status"] == "notYetLemmatised"
                    else "specification only; exact proof requires data/code outside the prototype")
                 + f" | {esc(WOULD_PROVE.get(cid, 'see scope document'))} |")
    L.append("")
    L.append("Claims proved or computationally checked in this prototype: `budget_ledger_identity`, "
             "`tax_revenue_le_base`, `prep_recursion_closed_form`, `pl_top1_sum_eq_denom`, "
             "`pl_top1_sum_eq_min`, `pl_topK_selected_sum`, `A34_arithmetic`, `A38_anchor_infeasible`, "
             "`B41_*` (×3), `B42_*` (×3), `classical_demand_ignores_*` (×5), `D02_paradox_not_universal`.")
    L.append("")
    L.append("## Axiom audit")
    L.append("")
    L.append("`verification/lean/ci/lean_verify.sh` runs `#print axioms` on every proved theorem and fails if "
             "`sorryAx`, `Classical.choice`, `Lean.ofReduceBool` or `Lean.trustCompiler` appear. Last recorded "
             "output:")
    L.append("")
    L.append("```")
    L.append(axioms_note if axioms_note else "(run the CI script to populate)")
    L.append("```")
    L.append("")
    L.append("## CI and extension plan")
    L.append("")
    L.append("1. **Local:** `verification/lean/ci/lean_verify.sh` — build, `sorry` scan, axiom audit, 18/18 claim ids.")
    L.append("2. **GitHub Actions:** `leanprover/lean-action` (toolchain from `lean-toolchain`) + `lake build`; "
             "Tier-2 Mathlib job only with `lake exe cache get`; artifacts: build log, axiom report, ledger.")
    L.append("3. **Ledger consistency gate:** regenerate this file with `tools/gen_lemma_ledger.py`; the QA check "
             "\"every `paper_claims.csv` row has a declaration or an explicit not-yet entry\" is mechanized in "
             "`LEMMA_LEDGER.csv`.")
    L.append("4. **Tier-2:** general-n Plackett–Luce (Mathlib) in CI; **Tier-1b:** expand omission lemmas to a "
             "typed model with explicit parameters; **Tier-3 never theorems** (numerics/DID/bootstrap stay "
             "hashed artifacts).")
    L.append("")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    with open(args.csv_out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["claim_id", "paper", "ledger_kind", "ledger_status", "lean_declaration", "note"])
        for r in rows:
            cid = r["claim_id"]
            if cid in DECLARED:
                d = DECLARED[cid]
                w.writerow([cid, r["paper"], d["kind"], d["status"], d["decl"], d["note"]])
            else:
                w.writerow([cid, r["paper"], "notYetLemmatised", "notYetLemmatised", "",
                            "explicit not-yet-lemmatised entry; baseline status: " + r["status"]])
    # record the exact baseline this ledger was generated against (QA pin)
    baseline_path = args.baseline_out
    os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
    baseline_payload = {
        "schema": 1,
        "path": "results/audit/paper_claims.csv",
        "sha256": baseline_sha,
        "rows": len(rows),
        "declared": len(declared),
        "not_yet_lemmatised": len(not_yet),
        "generated_utc": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
        "missing_from_ledger": [],
    }
    tmp = baseline_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(baseline_payload, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, baseline_path)
    print(f"wrote {args.out} and {args.csv_out}: {len(declared)} declared + {len(not_yet)} not-yet of {len(rows)} rows; baseline sha256 {baseline_sha}")


if __name__ == "__main__":
    main()
