# LEMMA LEDGER — mechanical consistency audit (Paper C / programme claims)

**Owner:** qa-verifier · **date:** 2026-11-25 ~21:30 · **mode:** host-only
**Artefacts audited:** `verification/lean/Atlas/Claims.lean` + `Atlas/{Definitions,Identities,PlackettLuce}.lean` (commit `4d42101`), `docs/audit/LEMMA_LEDGER.md` (sha `f8be23a7…`), `docs/audit/LEMMA_LEDGER.csv` (sha `da956fc1…`, 130 rows), `docs/audit/LEMMA_LEDGER_BASELINE.json`, frozen baseline `results/audit/paper_claims.csv` (sha **`f2ce655e…c655a40`**, **130 rows**).
**Verdict: PASS — SIGNED OFF for mechanical ledger consistency (R1–R7 all PASS).** This certifies the claim→declaration mapping, not the truth of empirical claims nor engine numerics.

## 1. Frozen baseline and ledger (this is the pinned pair)

| item | value |
|---|---|
| baseline | `results/audit/paper_claims.csv` — sha256 `f2ce655eb232a97f3ef5338334c8ed2f2dad953b328ab6a80fe066823c655a40`, **130 rows**, 130 unique ids |
| baseline record | `docs/audit/LEMMA_LEDGER_BASELINE.json` — rows 130, declared 18, not_yet 112, missing_from_ledger [] |
| ledger CSV | `docs/audit/LEMMA_LEDGER.csv` — sha256 `da956fc1e1d3a3ff18c31c98cf30f8dcd5d5c8817fab2ed55b2f0f55f5617df5`, **130 rows** |
| ledger MD | `docs/audit/LEMMA_LEDGER.md` — sha256 `f8be23a7da854d6b52489e63c7c765be5ccb7ed7c025c2640ccae9639d875c33` |
| declared / explicit NOT-YET | **18 declared** (A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04) + **112 explicit `NOT-YET-LEMMATISED`** = 130 |
| X-28 / X-29 / D-05 / D-06 | all present (previously the ledger lagged by 1–3 rows; regeneration at `4d42101` closes it) |
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
| R1 | claim ids non-empty, unique | **PASS** — 130 claims, 130 unique, no duplicates |
| R2 | exactly one ledger row per claim AND (≥1 existing Lean declaration group OR explicit not-yet entry) | **PASS** — 18 declared + 112 explicit not-yet, 0 missing/multi |
| R3 | no silent `sorry` (code only; comments/docstrings stripped) | **PASS** — **0 code `sorry` tokens**; the only textual "sorry" is prose at `Claims.lean:18` (docstring), correctly ignored |
| R4 | ledger ids == claims ids | **PASS** — missing = [], orphans = [] |
| R5 | no duplicate ledger rows / declaration names | **PASS** — 130 unique ledger ids; 61 Lean declaration names, none duplicated |
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
