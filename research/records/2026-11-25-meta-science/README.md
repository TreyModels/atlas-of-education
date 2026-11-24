# 2026-11-25 — Meta-science: five silent failures, forensically reconstructed

**Task:** task-4 (meta-science worker), branch `research/meta-science-silent-failures-2026-11-25`,
base `origin/main` @ `55732f4`. **Status:** complete for the four deliverables below; additive record.

## What this record is

A methods/forensics essay about **this repository's own silent failures**: five defects that did not crash
anything, produced plausible numbers, and passed the checks that were in place. For each defect the record shows
the defective line *before* the fix, the mechanism that kept it silent, the audit step that caught it, the fix,
the regression guard, and the generalisable lesson. It also documents one suggested receipt that does not exist
(the "eq03 TWFE transpose" commit), one record that does not reconcile (the Africa-11 interval), and one latent
control-flow hazard (gate-kind dispatch).

The corpus is the commit history; every quoted commit, path and line is in `RECEIPTS.csv` and was verified with
`git show` before it was quoted. Derived statements are labelled *recomputation* or *inference*. Retractions are
preserved as they were published; nothing in the source history was rewritten.

## Files

| file | what it is |
|---|---|
| `OUTLINE.md` | the plan: five bugs, the per-bug schema, the receipt-verification protocol, article structure. Committed first and alone (`5b93a41`). |
| `ARTICLE.md` | the essay (~4,300 words excluding code fences; 4,581 total). Five cases, taxonomy T1–T5, what caught them, the claim-coalescence finding, the latent case, limits. |
| `RECEIPTS.csv` | 38 rows: `receipt_id, bug, commit, file, hunk_or_line, claim`. Full 40-char SHAs. |
| `GUARDS_CHECKLIST.md` | short, operational checklist; each item tied to the case that motivates it. |
| `README.md` | this file. |

## The five bugs (one line each)

1. **DHS cluster-bootstrap multiplicities** — `r["country"] in samp` kept each resampled country at most once;
   intervals too narrow; a resampling fix that cannot move a point estimate. Fixed at `3faeff3` (and again,
   independently, at `93b882a`); record corrected at `9e063bf` / `22de735`.
2. **Transposed TWFE design matrix** (equation suite eq09) — `np.tile` for unit dummies and `np.repeat` for time
   dummies in a row-major array; also 2SLS SE from fitted-D residuals. Fixed at `0a91afb`; results re-recorded
   only at `d575bfe`. The suggested "eq03 TWFE transpose" commit **does not exist**: eq03's actual fix is
   `aefade0` (a 2-D (ρ, ω) CES grid), and the transpose was eq09.
3. **`pinv` masking rank deficiency** (full-system screen) — `pinv` produced finite estimates and tiny SEs for
   non-identified contrasts; `all([])` passed empty strata; a zero-variance outcome was "supported". Fixed at
   `22c4bb8`; supported set 49 → 45; guards in `test_full_system.py` + new `test_guards.py`.
4. **`e.kids['reason']` vs `e.exits`** (exit decomposition) — the engine compacts exits out of the roster, so the
   driver read all `-1` and reported liquidity = choice = never = 0 and `started_share = 1.0` in every run. The
   original "engine overwrites reason" blame was **wrong and retracted** (`4679ddb`, erratum `3afac25`); fixed
   properly at `747be44` (partial) and `219747a` (`aggregate_exits` + `test_exit_reason.py`).
5. **`returncode == 0` hiding `PASS=False`** (`run_all.py`) — the runner used the process exit code as the
   verdict; three scripts failed their own decision rules while the runner reported `failures = []`. Fixed at
   `93a351e`; re-recorded verdicts show `RULE_FAIL` with `returncode = 0`.

## How to verify

```bash
cd /Users/treymenefee/neon-boot/wt3/meta

# every receipt resolves (spot-check a few)
git cat-file -t 3faeff3 0a91afb 22c4bb8 219747a 93a351e

# the before/after pair for case 2
git show 0a91afb^:research/records/2026-11-25-equation-suite/scripts/eq09_identification.py | sed -n '27,35p'
git show 0a91afb:research/records/2026-11-25-equation-suite/scripts/eq09_identification.py  | sed -n '27,40p'

# the supported-row change for case 3 (49 -> 45)
git show 22c4bb8^:research/records/2026-11-25-edsystem-tests/full_system_tests.json | grep -c '"supported": true'
git show 22c4bb8:research/records/2026-11-25-edsystem-tests/full_system_tests.json  | grep -c '"supported": true'

# the retraction for case 4
git show 4679ddb:research/records/2026-11-25-masseng-edsystem/RUN_REPORT.md | sed -n '175,214p'
git show 3afac25:research/records/2026-11-25-suite-audit/ERRATUM_FS-12.md

# the non-existent eq03 transpose commit
git log --all --oneline -- '*eq03*'      # 5 commits, none transposes anything
git log --all -S'np.tile' -- research/records/2026-11-25-equation-suite   # eq09 only
```

The full row-by-row mapping is `RECEIPTS.csv`.

## Recomputations performed (not receipts)

Run on the host with the repository's own code/seeds where possible; these confirm mechanisms, they are not new
estimates:

- **Bootstrap multiplicity fraction.** `G·(1−(1−1/G)^G)` distinct countries expected; at `G` = 65, 80 the
  discarded share is ≈36.5–36.6 % (asymptotic 36.79 %), consistent with the record's "~36.8 %". Verified
  arithmetically and by simulating the exact sampling line.
- **TWFE old-vs-new bias.** Both dummy variants on the suite's own `did_world` with seed `20261125`, 60 reps,
  `N=40, T=20`: old `twfe_mean / twfe_bias / null_twfe_mean` = `0.785 / −0.499 / −0.023`; new = `0.138 / −1.146 /
  0.003`, matching the committed before/after JSONs.
- **`test_guards.py`** from `22c4bb8`, host run: `ALL PASS` (numpy only). Against the pre-fix module it exits
  non-zero (missing guard API), so it cannot silently pass either.
- **`test_exit_reason.py`** from `219747a` against the local engine (`N=80, T=40`): `ALL PASS`; against the
  pre-fix driver it exits non-zero (missing `aggregate_exits`).

## Reported honestly, not smoothed

- **No eq03 TWFE-transpose commit exists.** The suggested receipt was probably produced by coalescing the
  handoff's quarantine bundle (`MIGRATION_2026-11-25.md` @ `354f7c0`:57–59) into a per-script citation. This is
  documented in `ARTICLE.md` §8 as a sixth meta-finding (T5 provenance/retraction drift).
- **The Africa-11 interval does not reconcile across implementations.** The record's headline interval
  `[0.9987, 1.1403]` (which includes 1.0) comes from `corrected_reduction.py`; the same run's `estimate.py`
  bootstrap wrote `[1.0011, 1.1403]` (which excludes 1.0). Both files are named; the verdict flip is
  implementation-dependent at the boundary.
- **Guard gaps.** No committed regression test exists for case 1 (bootstrap multiplicities), case 2 (TWFE
  indexing) or case 5 (beyond the re-recorded output contract). These gaps are stated in the article rather than
  presented as covered.
- **Latent hazard.** The gate dispatch treats any non-`'bar'` kind as a quota (`engine/eduengine/core.py`
  @ `origin/main`:164, 369–371). It is verified in code but no run is known to have used an unknown kind; it is
  labelled latent, not a sixth occurred bug.

## Scope and limits

Five-case convenience sample from one repository, written by a participant in the same programme. No base rate,
no causal claim about why the defects were introduced, no claim that the mapping generalises beyond this corpus.
Statements about mechanisms are statements about code. The source history is untouched; this record is purely
additive on its branch.

## Provenance

- Branch: `research/meta-science-silent-failures-2026-11-25`, base `origin/main` @ `55732f4`.
- `OUTLINE.md` commit: `5b93a41`.
- All receipts are pinned to commits, not branch tips (branches move; the equation-suite and DHS branches were
  still being committed to while this record was written).
