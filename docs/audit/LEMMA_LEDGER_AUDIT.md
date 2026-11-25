# LEMMA LEDGER — mechanical consistency audit (Paper C / programme claims)

**Owner:** qa-verifier · **date:** 2026-11-25 · **mode:** host-only
**Status: BLOCKED — Lean artefacts not yet committed.** `verification/lean/Claims.lean` and
`docs/audit/LEMMA_LEDGER.md` are absent from `wt4/auditv2` (branch
`research/contest-audit-v2-2026-11-25`) as of this audit. `audit-runner` reports they will land this
session (host-only Lean install; GitHub-release toolchain mirror) with `verification/lean/Atlas/*.lean`,
`LEAN_VERIFICATION_SCOPE.md`, `grep -n sorry` / `#print axioms` / `lake build` evidence.

## 1. Baseline pinned now (so the audit is reproducible)

| item | value |
|---|---|
| claims file | `results/audit/paper_claims.csv` @ `research/contest-audit-v2-2026-11-25` |
| git blob | `4d7a7a20acad080a7d5632de742d796243da84ff` (`git rev-parse HEAD:results/audit/paper_claims.csv`) |
| sha256 | `f3480b4db57fcf6e9b7499697e3b30ecc09619bf42db65eb73e1d3037886c31c` |
| rows | **118 data rows** (plus header), 118 unique `claim_id`s, no duplicates |
| papers | A 39, B 44, X 27, C 4, D 4 |
| target set (Lead's 18 rows) | A-34…A-39 (6), B-41…B-44 (4), C-01…C-04 (4), D-01…D-04 (4) — **all 18 present** in the baseline |

## 2. Mechanical checks implemented (`docs/audit/lemma_audit.py`)

Run:

```
python3 docs/audit/lemma_audit.py \
  --claims results/audit/paper_claims.csv \
  --lean verification/lean/Claims.lean \
  --ledger docs/audit/LEMMA_LEDGER.md \
  --json-out docs/audit/results/lemma_audit.json
```

| id | rule |
|---|---|
| R1 | every claim id in `paper_claims.csv` is non-empty and unique (duplicates reported) |
| R2 | every claim id has **exactly one** Lean declaration (name contains the id, e.g. `A_34`) **or** an explicit `not-yet-lemmatised` ledger entry; missing/multi-declared ids listed |
| R3 | **no silent `sorry`**: every `sorry` in `Claims.lean` is inside a named declaration that appears in the ledger with a non-empty status/reason, or the claim row is explicitly not-yet-lemmatised with a reason; every sorry line reported |
| R4 | claim-id match: ledger ids ⊆ claims ids (orphans reported) and every claim id is either declared or explicitly not-yet (tiered result) |
| R5 | no duplicate declaration names and no duplicate ledger claim rows |

Expected shape from `audit-runner`: two-tier ledger — **18 specified rows** (A-34…A-39, B-41…B-44,
C-01…C-04, D-01…D-04) plus **100 explicit `NOT-YET-LEMMATISED` rows by id**; unproved statements encoded
as `def … : Prop`, not asserted theorems, so the planned sorry count is 0. The audit will confirm both
tiers and report any id that is neither declared nor explicitly listed.

## 3. Current result (pre-landing)

| check | result |
|---|---|
| R1 claims inventory | **PASS** — 118 rows, 118 unique ids |
| R2 exactly-one-declaration-or-explicit-not-yet | **BLOCKED** — no Lean/ledger files yet; the check will run over all 118 and return a two-tier result (18 specified + 100 not-yet) |
| R3 no silent sorry | **BLOCKED** — no Lean file; validator will list every `sorry` with line + enclosing declaration and require a ledger reason |
| R4 claim-id match | **BLOCKED** — baseline ids pinned above; orphans/mismatches will be listed |
| R5 duplicates | **BLOCKED** — no Lean/ledger files |

**Known risk to check on landing:** the current 118-row baseline contains only papers A/B/X/C/D; if the
Lean scope introduces new ids (e.g. `C-05…`) or renames existing ones, R4 will report ledger/claims
mismatches — those are findings, not silent passes. No `sorry` may be accepted without a ledger reason;
"the build passed" is not evidence of consistency.

**Verdict:** TASK B is **NOT-YET-LEMMATISED / BLOCKED** in the ledger sense — inventory pinned and
mechanical audit ready; final PASS/FAIL pending the `audit-runner` commit (expected this session). No
declaration or sorry status is asserted until the files exist.
