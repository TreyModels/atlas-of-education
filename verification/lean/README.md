# Lean verification prototype — `atlasVerification`

Host-only formal-QA prototype for the Atlas programme. **Lean proves the reference mathematics and the
accounting/inventory identities; the Python engine is differential-tested against Lean witnesses; numerical
results remain reproducible-artifact evidence.** See [`docs/audit/LEAN_VERIFICATION_SCOPE.md`](../../../docs/audit/LEAN_VERIFICATION_SCOPE.md)
for the tier table, resource measurements and the honest limits, and
[`docs/audit/LEMMA_LEDGER.md`](../../../docs/audit/LEMMA_LEDGER.md) for the claim-by-claim ledger.

## Build (Lean core only; no Mathlib)

```bash
# toolchain is pinned in lean-toolchain (leanprover/lean4:v4.36.0)
# with elan:  elan default leanprover/lean4:v4.36.0
cd verification/lean
lake build          # 16 jobs, ~2 s cold (Lean 4.36.0); compiles Atlas.Definitions / Identities / PlackettLuce / Claims
```

## Policy (binding)

- **No `sorry`.** CI fails on any `sorry` token. Claims that cannot be theorems are encoded as
  `EmpiricalClaim`/`SpecClaim` records (statements + artifact hashes + status), never asserted.
- **Axiom audit.** `ci/lean_verify.sh` runs `#print axioms` on the proved theorems; a `sorryAx` or unexpected
  axiom fails the run. Empirical statements about the world are hypotheses, not axioms claimed as facts.
- **No engine claims.** Nothing here says the Python engine is verified.

## Layout

| path | contents |
|---|---|
| `Atlas/Definitions.lean` | model objects (`Cohort`, `Gate`, `seatCount`, `Budget`, `TaxLedger`, `PrepStock`, `PLWeights`, `EqState`, `classicalDemand`) with units/domains documented |
| `Atlas/Identities.lean` | proved identities: budget ledger, tax revenue bound, prep-stock closed form |
| `Atlas/PlackettLuce.lean` | proved finite PL (n=2): `ΣP = min(seats, candidates)` in integer-scaled encoding; `decide` checks |
| `LeanStarter.lean` | Luna starter Nat gap/capacity/time lemmas (compiled with 4 documented fixes) |
| `Atlas/Model.lean` | Codex staged-plan model: A/R/gap, capacity, accounting, tie-rule rank, conditional invariants + counterexamples |
| `Atlas/Claims.lean` | the lemma ledger in Lean: 18 Lead-scoped claim declarations + `EmpiricalClaim`/`SpecClaim` records + omission lemmas M1–M5 + D-02 `¬` counterexample |
| `ci/lean_verify.sh` | local CI: build, `sorry` scan, axiom audit |
| `bridge/lean_witness.lean` | executable Lean witness (JSON on stdout) for the differential tests |
| `bridge/fixtures.json` | Python-fixture expected values (exact integers/rationals) |
| `bridge/differential_test.py` | runs the Lean witness, compares with fixtures, writes a hashed result JSON |
| `tools/gen_proof_status.py` | proof-status table + automatic `#print axioms` for all theorems |
| `tools/gen_lemma_ledger.py` | regenerates `docs/audit/LEMMA_LEDGER.md` from `results/audit/paper_claims.csv` + this project's claim map |

## Measured verification status (2026-11-25)

- `ci/lean_verify.sh` → **PASS**: build 16 jobs; **0 sorry tokens** (comment-aware scan); axiom audit 33 theorem
  lines, only allowed axioms (`propext`/none); 18/18 claim ids present. Log: `docs/audit/results/LEAN_VERIFY_host.log`.
- `bridge/differential_test.py` → **PASS 22/22** exact fixtures (incl. Luna starter + Codex-model parity values). Result: `docs/audit/results/LEAN_DIFFERENTIAL_BRIDGE.json`.
- Ledger: 18 declared + 112 explicit not-yet = **130 rows**, re-baselined to claims baseline sha256
  `b990c99f4bf666786ad1f87a91cdf4eb1f2a831a51f245d770c7ccdb41ff6f24` (132 rows)
  (`docs/audit/LEMMA_LEDGER_BASELINE.json`).

## Quick verification

```bash
cd verification/lean
./ci/lean_verify.sh
PYTHONPATH=../../engine python3 bridge/differential_test.py   # needs no engine import for exact fixtures
```
