# Paper #2 — "Massification Before Industrialization" — outline + evidence packet + bulge-arrival lane

**Compiled:** 25 November 2026 by `paper2-outliner` (delegated lane; Lead: `lead`).
**Repo used:** `/Users/treymenefee/neon-boot/repos/atlas` — clean clone, `--filter=blob:none`. Its `main`
working tree was found empty (1,108 staged deletions left by another process) and was **not touched**; all
evidence was read with `git show <commit>:<path>` plumbing and its committed blobs.

## Files

| file | what it is |
|---|---|
| `OUTLINE.md` | Section-by-section outline for Paper #2 (E6 + E8 pillars). Each section: claim, exact evidence file @ branch @ commit, the figure/table it needs, and the known weakness. Includes a figure/table manifest and a scope note separating Paper #2 from Paper M / Paper N1. |
| `CLAIMS.csv` | 44 claims. Columns: `claim_id, one_line_claim, evidence_path, branch, commit, verification_status, caveats`. Every row points at a file that was confirmed to exist with `git cat-file -e <commit>:<path>` and was read; 37 VERIFIED, 3 NEEDS-RECHECK, 4 UNSUPPORTED (see below). |
| `GAPS.md` | What must be re-verified before the paper can be quoted, and what would need new data. Includes the quotation-ban table (5 stale prose ranges), fee-date primary-source gap, E8 raw-input gap, GGDC vintage mismatch, the two framing gaps (enrolment thresholds; manufacturing), pre-1900 limits, bulge-arrival data gaps, and a sign-off checklist. |
| `PREREGISTRATION_BULGE_ARRIVAL.md` | Pre-registration for the auditor's "Bulge Arrival" macro test: `t* = t_abolition + L_primary`; sourcing rule; registered `t*` table; estimand; estimator reuse; pre-trend/placebo/LOO checks; step-3 falsifier; data gate. Written **before** any estimation. |
| `BULGE_ARRIVAL_STATUS.md` | Status of the bulge lane: `t*` sourced/unsourced counts, event-study verdict (**NOT-ESTIMABLE**), falsifier verdict (**NOT-ESTIMABLE**), exact missing series, and the verification of the three auditor-quoted numbers. |

## Verification summary

- **CLAIMS.csv: 44 rows — 37 VERIFIED, 3 NEEDS-RECHECK, 4 UNSUPPORTED.**
- VERIFIED = the number was read from, and (for the core E6/E8 statistics) independently recomputed from, the
  committed output file at the named commit.
- NEEDS-RECHECK = file exists and supports the record, but either the strict primary-source standard is not met
  (fee dates), the raw inputs are not committed (E8 outcome data), or a vintage mismatch must be reconciled
  (GGDC 2014 vs prereg 2023).
- UNSUPPORTED = no committed file supports the claim: the title-level "secondary/tertiary enrolment threshold"
  framing (C14), the auditor's "E6 76–90% / 20–40 yrs" composite (C40), the bulge `t*` table (C43), and the bulge
  event study/falsifier on current data (C44).

## Key commits referenced

| branch (`origin/…` in the clone) | commit | role |
|---|---|---|
| `research/e6e8-sequencing-2026-11-25` | `2d19da7cfea0c007eced8e3b114a6eea35ddbaea` | E6/E8/N3 results, fee dates, input hashes |
| `research/e6e8-sequencing-2026-11-25` | `bd782be4d15c834f054b1ecc650e54565f6b292f` | ERRATUM + erratum-check outputs (head) |
| `research/e6e8-sequencing-2026-11-25` | `a2a116df0fe481419dabd4b0c2ad70e6289c9600` | E6/E8/N3 pre-registration |
| `research/codex-source-verification-2026-11-25` | `9a0fd69a51625818494379d37974f1eb0aeeb2c6` | independent fee-date verification (verified head) |
| `research/codex-source-verification-2026-11-25` | `bfb8c6f205c2ec7fc1cae2c649664e5a3b5a3a9a` | commit that introduced `fee_dates.csv` (identical blob) |
| `research/paper-massification-2026-11-25` | `fb9f4190a4cf9e0fb5e1ca5f00d28c11ab857a1b` | Paper M cross-check: `revision_verification.json` 41/41 |
| `research/e1-multiverse-1200-2026-11-25` | `6a452a45a5aa172ca996ffae93292beb8270a2ad` | E1 `summary_by_R.json` (auditor "0/0/0/32") |

## Reading order

1. `OUTLINE.md` §0 (scope + title risk) → §5–§9 (the two pillars) → §11 (errata ledger).
2. `CLAIMS.csv` filtered to `VERIFIED` for drafting numbers; filtered to `UNSUPPORTED` for what to avoid.
3. `GAPS.md` §1 (quotation bans) before writing a single number.
4. `PREREGISTRATION_BULGE_ARRIVAL.md` → `BULGE_ARRIVAL_STATUS.md` for the added lane.
