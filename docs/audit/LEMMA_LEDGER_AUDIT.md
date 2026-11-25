# LEMMA LEDGER — mechanical consistency audit (Paper C / programme claims)

**Owner:** qa-verifier · **date:** 2026-11-25 ~21:10 · **mode:** host-only
**Artefacts audited:** `verification/lean/Atlas/Claims.lean` (330 lines, landed 20:56), `docs/audit/LEMMA_LEDGER.md` (203 lines), `docs/audit/LEMMA_LEDGER.csv` (126 rows), `docs/audit/LEAN_VERIFICATION_SCOPE.md`, baseline `results/audit/paper_claims.csv`.
**Verdict: NOT SIGNED OFF — 2 mechanical defects (stale ledger row; D-04 status/declaration inconsistency). No silent `sorry`; the two-tier structure is otherwise correct.**

## 1. Baseline re-hash (the file moves — always pin before auditing)

| snapshot | rows | sha256 | note |
|---|---|---|---|
| initial QA pin (~20:50) | 118 | `f3480b4d…31c` | before Paper C/D rows landed |
| at ledger generation | 126 | (ledger row count 126) | 18 declared + 108 explicit NOT-YET |
| **current audit baseline (~21:10)** | **127** | **`b50c9f36a0f34c42852ae8f76585d45734f204d699937d22b1b357db6dad892a`** | **X-28 added (CONTRADICTED runner-defect class), CSV line 128** |
| ledger CSV | 126 | `2278f7d49439eb25e74aa716c8de42b416fc4135cd3315d12d242b050e80694c` | one row short of baseline |

## 2. Mechanical checks (`docs/audit/lemma_audit.py`)

Run (re-hashes the baseline every time; comment-aware Lean scan; block-aware in-Lean ledger parse):

```
python3 docs/audit/lemma_audit.py --claims results/audit/paper_claims.csv \
  --ledger docs/audit/LEMMA_LEDGER.csv --lean-dir verification/lean \
  --json-out docs/audit/results/lemma_audit.json
```

| id | rule | result |
|---|---|---|
| R1 | claim ids non-empty, unique | **PASS** — 127 claims, 127 unique, no duplicates |
| R2 | exactly one ledger row per claim AND (≥1 existing Lean declaration group OR explicit not-yet entry) | **FAIL** — 18 declared + 108 explicit not-yet; **X-28 has no ledger row** (`rows not exactly one=[('X-28', 0)]`) |
| R3 | no silent `sorry` (code only, comments/docstrings stripped; each sorry needs a ledger reason) | **PASS** — **0 code `sorry`** occurrences; the only textual "sorry" is prose in `Claims.lean:18` ("no `sorry`s…"), correctly ignored |
| R4 | ledger ids == claims ids (orphans/missing reported) | **FAIL** — `claims missing from ledger=['X-28']`; orphans = none |
| R5 | no duplicate ledger rows / declaration names | **PASS** — 126 ledger rows, 126 unique ids; 60 Lean declaration names, none duplicated |
| R6 | in-Lean `claimLedger` agrees with CSV (ids, `leanDecl`, status) | **PASS** — 18/18 declared rows present in `Claims.lean` block and identical (e.g. `A-34`, `B-41` 3-declaration group, `D-04`) |
| R7 | declared row must not carry `notYetLemmatised` status | **FAIL** — `D-04` |

## 3. Defects (file:line)

| id | severity | finding |
|---|---|---|
| **L1** | **blocking (stale ledger)** | `docs/audit/LEMMA_LEDGER.csv` (126 rows) and `.md` (line 15 "108 of the 126 baseline rows") predate the **X-28** row now present in `results/audit/paper_claims.csv:128` (PROGRAMME, CONTRADICTED, runner-defect class). Mechanical consequence: R2/R4 fail; this is a **staleness gap, not a silent omission in Lean** (the 126 covered rows are all mapped). The generator `verification/lean/tools/gen_lemma_ledger.py:1-12` still hard-codes the old "118 rows / remaining 100" counts → it will reproduce staleness unless updated and re-run. Fix: regenerate ledger/CSV from the 127-row baseline (include X-28 as explicit NOT-YET), refresh the generator docstring counts, commit, then rerun the audit. |
| **L2** | **medium (internal inconsistency)** | `docs/audit/LEMMA_LEDGER.csv:119` (and `Claims.lean:327`) lists **D-04** with `lean_declaration = D04_attribution` **and** status `notYetLemmatised` ("citation/attribution risk is not a mathematical proposition"). A row cannot be both declared and not-yet-lemmatised. Fix: either status `hypothesis`/`specified` with the note (declaration is an `EmpiricalClaim` record, not a theorem) or drop `D04_attribution` and leave the not-yet entry. R7 will then pass. |
| **L3** | **informational (CI hygiene)** | `Claims.lean:18` contains the word "sorry" in a docstring; a naive `grep sorry` reports a false positive. The audit strips comments/docstrings and confirms **0 code sorries**; the CI `sorry` scan should be comment-aware (or exclude `/- … -/` and `--`), and the build log + `#print axioms` evidence should be attached to the ledger. |
| **L4** | **informational (build evidence)** | Independent `lake build` was attempted from `verification/lean`; Lean 4.36.0 toolchain was still downloading from `releases.lean-lang.org` at audit time (`~/.elan/toolchains` only contains the lock), so **the build was not independently confirmed here**. `verification/lean/ci/lean_verify.sh` exists; attach its `lake build` + `#print axioms` output before sign-off. The consistency checks above do not depend on the build. |

## 4. What is already correct

* Two-tier mapping is real: **18 Lead-scoped claims** (A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04) have Lean declarations; **108 remaining rows are individually listed as explicit `NOT-YET-LEMMATISED`** — no silent omissions among the 126 covered rows.
* **No silent `sorry`**: zero code sorries; unproved content is encoded as `EmpiricalClaim`/`SpecClaim` records (`Claims.lean:64-84`), matching the declared "no sorry" policy.
* In-Lean `claimLedger` (18 records, `Claims.lean:287-329`) agrees with the CSV/ledger on ids, declarations and statuses (R6 PASS); no duplicate declarations (R5 PASS); ids unique (R1 PASS).
* The audit re-hashes the baseline on every run, so future row additions cannot silently pass (as X-28 demonstrates).

## 5. Verdict and re-audit condition

**TASK B is NOT signed off.** Required before sign-off:
1. L1: regenerate `LEMMA_LEDGER.md` + `.csv` from the current 127-row `paper_claims.csv` (include X-28 as explicit NOT-YET; update `gen_lemma_ledger.py` docstring/counts); commit.
2. L2: resolve D-04 status vs declaration.
3. Attach L4 build evidence (`lake build`, comment-aware sorry scan, `#print axioms`).
Then rerun the command in §2; expected R1–R7 all PASS (two-tier: 18 declared + 109 explicit not-yet = 127). Nothing is asserted about claims' truth or the engine here — this is a mechanical ledger-consistency audit only.
