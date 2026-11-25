# LEMMA LEDGER — mechanical consistency audit (Paper C / programme claims)

**Owner:** qa-verifier · **date:** 2026-11-25 ~21:10 · **mode:** host-only
**Artefacts audited:** `verification/lean/Atlas/Claims.lean` (330 lines, landed 20:56), `docs/audit/LEMMA_LEDGER.md` (203 lines), `docs/audit/LEMMA_LEDGER.csv` (126 rows), `docs/audit/LEAN_VERIFICATION_SCOPE.md`, baseline `results/audit/paper_claims.csv`.
**Verdict: NOT SIGNED OFF — 1 blocking defect (ledger lag: 3 newly committed claims X-29/D-05/D-06 not yet mapped) + build evidence pending. No silent `sorry`; two-tier structure, id uniqueness and in-Lean/CSV agreement are correct.**

## 1. Baseline re-hash (the file moves — always pin before auditing)

| snapshot | rows | sha256 | ledger state |
|---|---|---|---|
| initial QA pin (~20:50) | 118 | `f3480b4d…31c` | ledger not yet landed |
| at first ledger audit (~21:05) | 126 | — | ledger 126 rows (X-28 absent; D-04 status inconsistent) |
| after ledger regeneration (~21:06) | 127 | — | ledger 127 rows (X-28 included; D-04 fixed to `hypothesis`) |
| **current audit baseline (~21:14)** | **130** | **`23ecde418dded6d316fe44bc11e1d9b62f9dcf25085db10fa3bd1c5f2d6ec8f5`** | ledger 127 rows → **3 rows behind** (X-29, D-05, D-06) |
| ledger CSV at audit | 127 | `a3a95bba20e11329392bb8cbe9722136877b3da7759510893ecdca192807f19a` | regenerated 21:06; D-04 `hypothesis`; X-28 present |

## 2. Mechanical checks (`docs/audit/lemma_audit.py`)

Run (re-hashes the baseline every time; comment-aware Lean scan; block-aware in-Lean ledger parse):

```
python3 docs/audit/lemma_audit.py --claims results/audit/paper_claims.csv \
  --ledger docs/audit/LEMMA_LEDGER.csv --lean-dir verification/lean \
  --json-out docs/audit/results/lemma_audit.json
```

| id | rule | result (latest run) |
|---|---|---|
| R1 | claim ids non-empty, unique | **PASS** — 130 claims, 130 unique |
| R2 | exactly one ledger row per claim AND (≥1 existing Lean declaration group OR explicit not-yet entry) | **FAIL** — 18 declared + 109 explicit not-yet; **X-29, D-05, D-06 have no ledger row** |
| R3 | no silent `sorry` (code only, comments/docstrings stripped) | **PASS** — **0 code `sorry`**; only prose "sorry" at `Claims.lean:18` |
| R4 | ledger ids == claims ids | **FAIL** — missing `['X-29','D-05','D-06']`, orphans none |
| R5 | no duplicate ledger rows / declaration names | **PASS** — 127 unique ledger ids; 60 Lean declarations, none duplicated |
| R6 | in-Lean `claimLedger` agrees with CSV | **PASS** — 18/18 declared rows present and identical |
| R7 | declared row must not be `notYetLemmatised` | **PASS** — D-04 fixed to `hypothesis` (`LEMMA_LEDGER.csv` D-04 row; note: "declared as an empirical hypothesis record, never a theorem") |

## 3. Defects (file:line)

| id | severity | finding |
|---|---|---|
| **L1** | **blocking (ledger lag, live race)** | Claims baseline advanced to **130 rows** while `LEMMA_LEDGER.csv/.md` were regenerated at 127: **X-29** (gate diagnostic gap; `verify` row in baseline), **D-05**, **D-06** are absent from the ledger → R2/R4 fail. This is not a silent omission in Lean; it is a regeneration-lag race (several claims landed while the ledger was being rebuilt). The generator `verification/lean/tools/gen_lemma_ledger.py:1-12` still hard-codes old "118 rows / remaining 100" counts and must be updated/re-run **after the claims file freezes**. |
| **L2** | resolved | D-04 was declared (`D04_attribution`) with status `notYetLemmatised` in the 21:05 ledger; the 21:06 regeneration sets it to `hypothesis` with note "declared as an empirical hypothesis record, never a theorem" → R7 now passes. |
| **L3** | informational (CI hygiene) | `Claims.lean:18` prose contains "sorry"; a naive grep false-positives. Audit strips comments and confirms **0 code sorries**; make the CI scan comment-aware. |
| **L4** | informational (build evidence) | Independent `lake build` not confirmed (Lean 4.36.0 toolchain download incomplete; only lock in `~/.elan/toolchains`). Attach `verification/lean/ci/lean_verify.sh` output (`lake build`, `#print axioms`) before sign-off. |

## 4. What is already correct

* Two-tier mapping is real: **18 Lead-scoped claims** (A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04) have Lean declarations; **109 remaining rows are individually listed as explicit `NOT-YET-LEMMATISED`** — no silent omissions among the 127 covered rows (X-28 now included; D-04 status fixed).
* **No silent `sorry`**: zero code sorries; unproved content is encoded as `EmpiricalClaim`/`SpecClaim` records (`Claims.lean:64-84`), matching the declared "no sorry" policy.
* In-Lean `claimLedger` (18 records, `Claims.lean:287-329`) agrees with the CSV/ledger on ids, declarations and statuses (R6 PASS); no duplicate declarations (R5 PASS); ids unique (R1 PASS).
* The audit re-hashes the baseline on every run, so future row additions cannot silently pass (as X-28 demonstrates).

## 5. Verdict and re-audit condition

**TASK B is NOT signed off.** Required before sign-off:
1. L1: regenerate `LEMMA_LEDGER.md` + `.csv` from the current 127-row `paper_claims.csv` (include X-28 as explicit NOT-YET; update `gen_lemma_ledger.py` docstring/counts); commit.
2. L2: resolve D-04 status vs declaration.
3. Attach L4 build evidence (`lake build`, comment-aware sorry scan, `#print axioms`).
Then rerun the command in §2; expected R1–R7 all PASS (two-tier: 18 declared + 109 explicit not-yet = 127). Nothing is asserted about claims' truth or the engine here — this is a mechanical ledger-consistency audit only.
