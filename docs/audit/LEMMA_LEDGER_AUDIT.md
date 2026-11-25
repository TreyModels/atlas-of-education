# LEMMA LEDGER — mechanical consistency audit (Paper C / programme claims)

**Owner:** qa-verifier · **date:** 2026-11-25 ~21:45 · **mode:** host-only
**Artefacts audited:** `verification/lean/Atlas/Claims.lean` + `Atlas/{Definitions,Identities,PlackettLuce}.lean`, `docs/audit/LEMMA_LEDGER.md` (sha `5e414bc0…`), `docs/audit/LEMMA_LEDGER.csv` (sha `3e9dbbc1…`, **132 rows**), `docs/audit/LEMMA_LEDGER_BASELINE.json` (sha `87c14a6a…`), frozen baseline `results/audit/paper_claims.csv` (sha **`b990c99f…ff6f24`**, **132 rows**) at commit **`4c06025`**.
**Verdict: PASS — SIGNED OFF for mechanical ledger consistency on the pinned 132-row pair below (R1–R7 all PASS).** This certifies the claim→declaration mapping, not the truth of empirical claims nor engine numerics. The earlier PASS on the 130-row pair (`f2ce655e…` + `da956fc1…`, commit `4a9afd7`) is preserved in git history and superseded **only as the current record**; nothing was silently rewritten.

## 1. Frozen baseline and ledger (this is the pinned pair)

| item | value |
|---|---|
| baseline | `results/audit/paper_claims.csv` — sha256 `b990c99f4bf666786ad1f87a91cdf4eb1f2a831a51f245d770c7ccdb41ff6f24`, **132 rows**, 132 unique ids, freeze commit `4c06025` |
| baseline record | `docs/audit/LEMMA_LEDGER_BASELINE.json` — sha256 `87c14a6a…`; rows 132, missing_from_ledger [] |
| ledger CSV | `docs/audit/LEMMA_LEDGER.csv` — sha256 `3e9dbbc188a4309156310bd0696967261e11d0f2243c66c4da53daa4144e1287`, **132 rows** |
| ledger MD | `docs/audit/LEMMA_LEDGER.md` — sha256 `5e414bc09d103c183f541da15a4574c1a03aa336980d4d5969c942c5cf4cde71` |
| declared / explicit NOT-YET | **18 declared** (A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04) + **114 explicit `NOT-YET-LEMMATISED`** = 132 |
| C-05 / X-28 / X-29 / X-30 / D-05 / D-06 | all present (C-05 and X-30 added after the previous freeze; regeneration at `4c06025` closes the drift) |
| generator | `verification/lean/tools/gen_lemma_ledger.py` now derives sha/row counts from the CSV, supports `--expect-sha/--expect-rows` loud failure, writes `LEMMA_LEDGER_BASELINE.json` — no hard-coded 118/100 counts |

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

## 3. Independent build / axiom evidence (verified, not just quoted)

| evidence | result |
|---|---|
| `lake build` (host, Lean 4.36.0, `verification/lean`) | **PASS — 12 jobs completed, exit 0** (independently re-run by QA; `Atlas.Claims` 2.8 s, `Atlas` 173 ms) |
| comment-aware `sorry` scan (`ci/lean_verify.sh`) | **PASS — 5 Lean files, 0 `sorry` tokens** (log `docs/audit/results/LEAN_VERIFY_host.log`) |
| `#print axioms` allow-list | **PASS — 12 theorem lines parsed; only `propext` / none**; no `sorryAx`, no `choice`, no `ofReduceBool` (`docs/audit/results/LEAN_AXIOM_AUDIT.txt`) |
| 18 Lead-scoped claim ids present | **PASS (18/18)** per the same log |
| Lean↔Python differential bridge | **PASS — 9/9 exact fixture matches, `passed=true`, `lean_exit_code=0`** (`docs/audit/results/LEAN_DIFFERENTIAL_BRIDGE.json`) |

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
