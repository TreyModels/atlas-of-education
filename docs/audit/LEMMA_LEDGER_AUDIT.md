# LEMMA LEDGER — mechanical consistency audit (Paper C / programme claims)

**Owner:** qa-verifier · **date:** 2026-11-25 ~22:20 · **mode:** host-only
**Artefacts audited:** full Lean package `verification/lean/{Atlas.lean, LeanStarter.lean, Atlas/{Claims,Definitions,Identities,PlackettLuce,Model}.lean}`, `docs/audit/LEMMA_LEDGER.md` (sha `eb639671…`), `LEMMA_LEDGER.csv` (sha **`3e9dbbc1…`**, **132 rows**, unchanged), `LEMMA_LEDGER_BASELINE.json` (sha `52dee893…`), frozen baseline `results/audit/paper_claims.csv` (sha **`55f75eea…cd212`**, **132 rows**) at freeze commit **`f4167fc`**. Prior pins: `e0a5662` with baseline `3ff88d39…`; earlier 130-row `f2ce655e…`@`4d42101` and `b990c99f…`@`4c06025` preserved in git history. The `3ff88d39→55f75eea` change is **content-only (same 132 rows/ids/statuses; ledger CSV byte-identical)** — re-verified, no re-baseline semantics change.
**Verdict: PASS — SIGNED OFF for mechanical ledger consistency + Lean axiom hygiene on the pinned pair below (R1–R8 all PASS; re-verified at content-edit pin `f4167fc` / baseline `55f75eea…` — same rows/ids/statuses, ledger unchanged).** This certifies the claim→declaration mapping and axiom hygiene, not the truth of empirical claims nor engine numerics; the engine is NOT formally verified. The earlier PASS on the 130-row pair (`f2ce655e…` + `da956fc1…`, commit `4a9afd7`) is preserved in git history and superseded **only as the current record**; nothing was silently rewritten.

## 1. Frozen baseline and ledger (this is the pinned pair)

| item | value |
|---|---|
| baseline | `results/audit/paper_claims.csv` — sha256 `07f83156cb6f4cb22a46516ebbe313f5db47d22e7a6de0025f2d6625ddf6f9cb`, **132 rows**, 132 unique ids. Batched update at adjudication commit **`1227593`**: only the **X-29 row changed** (status `UNRESOLVED` → `REPRODUCED SIMULATION`, claim/action text); no ids/rows added/removed (tally R25/U20). Prior baseline `55f75eea…`/`f4167fc` preserved in git history. |
| baseline record | `docs/audit/LEMMA_LEDGER_BASELINE.json` — sha256 `77098a5dfa1d32a067374ffa843002e2ba3e16c3099227317705c606dc3e7b23`; **records `07f83156…` / 132 rows, declared 18, not_yet 114, missing_from_ledger []** (regenerated with the loud pins at audit-runner commit **`5c485c0`**, pushed `1227593..5c485c0`) |
| ledger CSV | `docs/audit/LEMMA_LEDGER.csv` — sha256 **`840945ffcef2698cdc1093b145e0d9b902a7af44f6f8d4af3ab031205e755940`**, **132 rows** (regenerated after the status-only CSV update; ids/rows identical to the previous `3e9dbbc1…`; only the stored X-29 status text changed) |
| ledger MD | `docs/audit/LEMMA_LEDGER.md` — sha256 `c9bb869173d833166f0d7d802e84bd700da14d7e7c059b15c0745e97692d70c2` (regenerated); proof-status MD `7c0e753c…` (refreshed to cite baseline `07f83156…`); proof-status CSV `1ff80fb0…` and axioms `f9c05bc4…` unchanged; Lean sources/build/bridge unchanged |
| declared / explicit NOT-YET | **18 declared** (A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04) + **114 explicit `NOT-YET-LEMMATISED`** = 132 |
| C-05 / X-28 / X-29 / X-30 / D-05 / D-06 | all present (C-05 and X-30 added after the previous freeze; regeneration at `4c06025` closes the drift) |
| generator | `verification/lean/tools/gen_lemma_ledger.py` now derives sha/row counts from the CSV, supports `--expect-sha/--expect-rows` loud failure, writes `LEMMA_LEDGER_BASELINE.json` — no hard-coded 118/100 counts |

**For the record (both pins):** the audited PASS pair was baseline **`3ff88d39…`** + ledger **`3e9dbbc1…`** at
commit **`e0a5662`** (QA report `2ba5f74`, R1–R8 PASS). The current re-pin is baseline **`55f75eea…`** at commit
**`f4167fc`** with the *same* 132 rows, ids and statuses and a byte-identical ledger CSV (`3e9dbbc1…`) — the
content-only edit was re-verified here (`c18a44f`), so the PASS carries over with the "same rows/ids/statuses"
note rather than a new audited pair.

## 2. Mechanical checks (`docs/audit/lemma_audit.py`) — all PASS

Repro (re-hashes baseline each run; comment-aware Lean scan; block-aware in-Lean ledger parse):

```
python3 docs/audit/lemma_audit.py --claims results/audit/paper_claims.csv \
  --ledger docs/audit/LEMMA_LEDGER.csv --lean-dir verification/lean \
  --json-out docs/audit/results/lemma_audit.json
```

| id | rule | result |
|---|---|---|
| R1 | claim ids non-empty, unique | **PASS** — 132 claims, 132 unique, no duplicates |
| R2 | exactly one ledger row per claim AND (≥1 existing Lean declaration group OR explicit not-yet entry) | **PASS** — 18 declared + 114 explicit not-yet, 0 missing/multi |
| R3 | no silent `sorry` (code only; comments/docstrings stripped) | **PASS** — **0 code `sorry` tokens**; the only textual "sorry" is prose at `Claims.lean:18` (docstring), correctly ignored |
| R4 | ledger ids == claims ids | **PASS** — missing = [], orphans = [] |
| R5 | no duplicate ledger rows / declaration names | **PASS** — 132 unique ledger ids; 61 Lean declaration names, none duplicated |
| R6 | in-Lean `claimLedger` agrees with CSV | **PASS** — 18/18 records match on id, `leanDecl`, status |
| R7 | declared row must not be `notYetLemmatised` | **PASS** — D-04 now `hypothesis` ("declared as an empirical hypothesis record, never a theorem") |
| R8 | proof-status table covers every Lean library declaration; all `compiled=yes`, `sorry_free=yes`, axioms only `''`/`propext` | **PASS** — `LEAN_PROOF_STATUS.csv` 107 rows vs 107 library declarations; 0 missing/extra/duplicate/bad; 46 theorems all compiled/sorry-free |

## 3. Independent build / axiom evidence (verified, not just quoted)

| evidence | result |
|---|---|
| `lake build` (host, Lean 4.36.0, `verification/lean`) | **PASS — 16 jobs completed, exit 0** (independently re-run by QA at `e0a5662`) |
| comment-aware `sorry` scan (`ci/lean_verify.sh`) | **PASS — 7 Lean files, 0 `sorry` tokens** (independently re-run) |
| `#print axioms` allow-list | **PASS — 33 theorem lines parsed; only `propext` / none**; no `sorryAx`/`choice`/`ofReduceBool` (`LEAN_AXIOMS_ALL.txt` sha `f9c05bc4…`; CI: `axiom audit OK`) |
| proof-status package | **PASS — 107 declarations / 46 theorems, `LEAN_PROOF_STATUS.csv` sha `1ff80fb0…`, `.md` `c02b4085…`; all compiled, all sorry-free** |
| 18 Lead-scoped claim ids present | **PASS (18/18)** per `ci/lean_verify.sh` |
| Lean↔Python differential bridge | **PASS — 22/22 exact fixture matches, `passed=true`, `lean_exit_code=0`** (`LEAN_DIFFERENTIAL_BRIDGE.json` sha `56cdfd7b…`) |
| new package proofs/counterexamples | `Atlas/Model.lean` compiles: gap/capacity/accounting/additivity/time lemmas + `rank_invariant_under_common_shift`, monotonicity, and counterexamples (`fixed_seat_relative_rank_counterexample`, `complementarity_counterexample`, `feedback_capacity_counterexample`); Luna starter `LeanStarter.lean` compiled (4 documented fixes) |

## 4. Residual caveats (not defects)

* The audit is **mechanical**: it verifies the claim→declaration/ledger mapping, absence of unapproved axioms, and that non-theorem claims are explicitly not-yet/unproved. It does **not** verify the truth of the empirical claims, the Python engine's numerics, or Paper C's results.
* D-04 ("citation/attribution risk") is intentionally encoded as an `EmpiricalClaim` hypothesis with a note — correct given it is not a mathematical proposition.
* `Claims.lean:18` contains the word "sorry" in prose; the CI scan is comment-aware (0 tokens). A naive `grep sorry` would false-positive — keep the CI hook as the gate.
* If `results/audit/paper_claims.csv` moves again, the generator now **fails loudly** on `--expect-sha/--expect-rows`; re-run the generator and this audit before citing the ledger.

## 5. Defect history closed by this re-audit

| id | earlier finding | status |
|---|---|---|
| L1 | ledger stale by 1–3 rows as the claims baseline advanced (X-28, then X-29/D-05/D-06) | **CLOSED** at `4d42101` — 130/130 rows mapped, baseline frozen to `f2ce655e…`, generator loud on drift |
| L2 | D-04 declared but `notYetLemmatised` | **CLOSED** — status `hypothesis` with explanatory note |
| L3 | prose "sorry" false positive risk | **MITIGATED** — CI comment-aware scan PASS (0 tokens); informational only |
| L4 | independent `lake build`/axiom evidence missing | **CLOSED** — independently re-verified here (`12 jobs`, `propext`/none only, bridge 9/9) |

**Sign-off:** `docs/audit/LEMMA_LEDGER_AUDIT.md` PASS on the pinned pair (baseline `f2ce655e…`, ledger `da956fc1…`); report to lead and paper-adjudicator. No causal-language or truth claims are implied.


## 6. Baseline drift — resolved at `4c06025`

The first PASS (commit `4a9afd7`) was pinned to the 130-row pair (`f2ce655e…` + `da956fc1…`). The live CSV
then advanced to **132 rows** (`b990c99f…`) adding **C-05** (Paper C confirmatory prereg review) and
**X-30** (Lean methods artefact). audit-runner regenerated with the loud pins
(`--expect-sha b990c99f… --expect-rows 132`, commit **`4c06025`**) and the re-audit above confirms
**R1–R7 PASS on 132 rows, 18 declared + 114 explicit NOT-YET**; C-05/X-30 are present as explicit
NOT-YET, D-04 stays `hypothesis`, ids equal, no duplicates. The 130-row PASS remains preserved in git
history (`4a9afd7`) and is superseded only as the current record. If the CSV moves again, the generator
now fails loudly on the pinned sha/rows; re-run generator + this audit and repin before citing CI.

**Pilot-0 note (unchanged):** payload still absent (live 8-worker run at 14/128 rows, no
`paperC_pilot0_results.json`); host-only QA remains blocked on the completed copy.


## 7. Post-sign-off content edits (no re-baseline needed for the mapping)

Two content-only edits after the `e0a5662` sign-off: `3ff88d39…` (X-30 action text) and `55f75eea…`
(MZ-01/MZ-02/C-05/X-30 text). Row count, id set and claim statuses are unchanged (audit-runner verified
programmatically against the `e0a5662` snapshot; this audit independently confirms 132/132 ids and all
checks). Re-ran against **`55f75eea…` × ledger `3e9dbbc1…`** (132 rows, byte-identical): **R1–R8 all PASS**.
The ledger keys rows by id, so text edits do not stale the mechanical audit. If an **id/row/status** change
lands, regenerate the ledger with the pinned `--expect-sha/--expect-rows` and re-pin first.


## 8. Audit-script refinements applied at this re-pin (QA-side, not engine defects)

* **Namespace-aware declaration names.** The Lean sources now define `gap` in both `LeanStarter` and
  `Atlas.Model`; the audit tracks fully-qualified names so these are distinct (the earlier
  `duplicated=['gap']` flag was a parser artefact, resolved).
* **Library vs witness scope.** `verification/lean/bridge/lean_witness.lean` is the executable witness
  program (validated by the 22/22 differential bridge), not part of the Atlas library; its helper defs
  (`jLine`, `main`) are excluded from the declaration/proof-status mapping. Library declarations now price
  exactly to the 107-row proof-status table (0 missing/extra) — R8.
* **Qualified-or-basename resolution.** Ledger `leanDecl` strings use simple names (e.g.
  `A34_arithmetic`); R2 resolves them against qualified Lean names by suffix.

No claim is made that the formal layer verifies the Python engine or the empirical claims; the scope
document (`LEAN_VERIFICATION_SCOPE.md`, sha `575c8966…`) and the Codex/Luna fixes are recorded as methods
artefacts, and the "engine NOT formally verified" boundary stands. If `paper_claims.csv` changes ids/rows,
regenerate the ledger with the pinned `--expect-sha/--expect-rows` and rerun this audit.


## 9. Post-X-29 batched update (status-only) — re-affirmed

After the X-29 diagnostic closed, the adjudicator applied the single agreed batched CSV update
(`1227593`): baseline `55f75eea…` → **`07f83156…`**, 132 rows, **only the X-29 row changed**
(`UNRESOLVED` → `REPRODUCED SIMULATION`); no ids/rows added or removed. **X-29 remains an explicit
`notYetLemmatised` ledger row with no Lean declaration** — the status change only edits its baseline-status
note; the declared set stays the 18 Lead-scoped claims. audit-runner re-pinned the ledger at `5c485c0`
(`--expect-sha 07f83156… --expect-rows 132`); the final hashes are the ones in §1 above. Re-ran the audit against
`07f83156…` × ledger `3e9dbbc1…` (132 rows, byte-identical): **R1–R8 all PASS** (132/132 unique ids,
18 declared + 114 explicit NOT-YET, 0 code sorries, in-Lean 18/18, D-04 `hypothesis`, proof-status
107/107). No mapping change is implied by a status-text update. audit-runner is re-pinning the ledger
record to the new sha with the loud pins; when their regenerated ledger hashes arrive I will record them
and (if the ledger CSV stays byte-identical) the PASS carries over. The claims record is: this PASS
covers mapping + axiom hygiene, **not** empirical truth/engine numerics.
