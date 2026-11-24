# PRE-REGISTRATION — exploratory receipt-drift audit of the 25 Nov handoff

**Record:** `research/records/2026-11-25-meta-science/` (follow-up to the confirmatory record at `01f9e45`)
**Branch:** `research/meta-science-silent-failures-2026-11-25`
**Status: EXPLORATORY / POST-HOC.** This audit was prompted by the sixth finding of the confirmatory essay
(claim coalescence around the non-existent "eq03 TWFE transpose" receipt). The question and the documents were
chosen **after** that finding, so this is hypothesis-generating, not confirmatory. It does not edit
`ARTICLE.md` or `RECEIPTS.csv`, makes no inferential claim about rates beyond the audited documents, and uses
host-only git reads (no server, no power actions).

## 1. Question

How widespread is receipt drift in the two 25 Nov handoff documents? Specifically:

- **C1.** Do the branch/head rows in `MIGRATION_2026-11-25.md` @ `354f7c0` and the four fix rows in
  `NEON_FREE_FIXES_2026-11-25.md` @ `6f68776` name receipts that exist, and does the claimed fix match the
  actual diff?
- **C2.** Does each "Neon item N fixed by X"-style claim resolve to a commit that touches the named code, and
  do the item numbers stay consistent between the documents?
- **C3.** What additional COALESCED / WRONG-COMMIT / MISSING receipts exist beyond the eq03 case?

## 2. Documents under audit (pinned commits; time-indexed)

| doc | commit | committer time | facts used |
|---|---|---|---|
| `MIGRATION_2026-11-25.md` | `354f7c0` | 2026-11-25T00:17:31+08:00 | §Heads (origin) table lines 15–34; papers line 36; quarantine items 1–6 lines 48–63; "All committed work is pushed" line 10 |
| `NEON_FREE_FIXES_2026-11-25.md` | `6f68776` | 2026-11-25T00:46:47+08:00 | table rows lines 9–12; local-only branch lines 26–30; key results lines 34–51; "Still open" lines 55–63 |

Both documents are audit **targets**, not audit evidence. Later commits (`d532478`, branch tips moving) are
noted but do not retroactively change whether a head claim was true when published.

## 3. Definitions (fixed before the audit)

**Receipt**: a branch name, commit SHA, file path, symbol, or PR/paper SHA that a claim cites as the thing that
shows the claim.

**Status categories** (mutually exclusive; one per audited claim):

- **VERIFIED** — every cited receipt exists in the reachable repository (remote or local refs) and the claimed
  content matches the actual diff/content. For a *head* claim: the cited SHA is the branch tip as of the
  document commit's committer time (see §4), or the branch advanced only after that time.
- **COALESCED** — the cited receipt(s) exist but the claim merges two or more distinct objects, versions,
  fixes, or numbers, so no single cited receipt shows the whole claim (including re-numbering that makes
  "item N" ambiguous between the two documents).
- **WRONG-COMMIT** — the cited receipt exists but the claimed content is not in it, or the cited head was not
  the branch tip at the document's committer time (a stale head), or the claim names a commit that does not
  carry the named fix.
- **MISSING** — the cited branch/commit/file/symbol does not exist in the reachable repository; for a
  claim explicitly labelled "local only", missing **from this repository** counts here and the evidence records
  where the cited path points.

**Counting rule.** A claim with several assertions gets sub-rows (e.g. `N-B3.1a`) so each status refers to one
assertion. The headline count is over sub-rows, not over nominal claims.

## 4. Time-indexed head rule

A handoff's "head" is a statement about a moment. For each head claim:

1. Resolve the branch to its current tip (`origin/<branch>` first, else local ref).
2. Walk the branch's first-parent chain from the tip and take the newest commit whose **committer time** is
   `<=` the document's committer time; that is the branch tip "as of publication".
3. Exact equality with the cited SHA → VERIFIED. A later commit that existed before publication → WRONG-COMMIT
   (stale head). A branch that advanced only after publication → VERIFIED, with the current tip recorded as a
   note (branches moving is not drift).
4. Clock caveat: all times are local (+08:00); ties within a few seconds are reported as such, not decided
   silently.

## 5. Claim universe (enumerated before any status is recorded)

### MIGRATION @354f7c0

- **M-A1.1 … M-A1.20** — the 20 branch/head rows, lines 15–34, in order.
- **M-A2.1 … M-A2.3** — papers `a22f3c4`, `5a56864`, `2bcb7d7`, line 36 ("plus negatives branches; older heads
  unchanged" — audited only to the three named SHAs).
- **M-A3.1 … M-A3.6** — quarantine items 1–6, lines 48–63: does each named code object/file exist at the
  branch head that the same document lists for that workstream, and does the description match the code?
- **M-A4.1** — line 10: "All committed work is pushed; nothing is only on the Mac" (tested for the twenty
  enumerated heads only).

### NEON_FREE_FIXES @6f68776

- **N-B1.1 … N-B1.4** — the four fix-table rows, lines 9–12: branch exists, cited head is the tip at
  publication, the claimed fix is in the branch/diff, the named test exists and passes (`ALL PASS` checked from
  the test file's own exit semantics where it can be run host-side; otherwise "test file exists" only).
- **N-B2.1** — lines 26–30: "Not pushed, local only: `fix/equation-suite-2026-11-25` (in `~/neon-boot/wt/eq`)"
  and "the math fixes are not done".
- **N-B3.1a/b/c** — lines 34–38: DHS numbers; "point estimates unchanged"; "now includes 1.0".
- **N-B3.2** — lines 39–41: eduengine driver spot-check percentages.
- **N-B3.3** — lines 42–46: edsystem-tests 49→45, the four dropped rows, 17/45 and 6/45, deviation file.
- **N-B3.4** — lines 47–51: test-bench numbers, Q1 permutation PASS, data manifest "all verify".
- **N-B4.1** — lines 3–5 + 55–63: "four of Neon's quarantine items are fixed" and the item-number mapping
  between the two documents (C2).

## 6. Protocol per claim

1. `git rev-parse` / `git cat-file -t` the cited SHA; `git rev-parse origin/<branch>` (else local) for branches.
2. Reachability: `git merge-base --is-ancestor <sha> <branch-tip>`.
3. Content: `git show --stat <sha>` and `git show <sha> -- <named path>` (or `git show <sha>:<path>` +
   `sed -n` for documents); quote the hunk/line in the evidence field.
4. Numbers: grep the quoted value in the file at the cited commit; for the data-manifest claim, recompute
   `sha256` of the committed files and compare with `data/MANIFEST.sha256`.
5. Symbols: `git grep -l '<symbol>' <sha> -- <dir>` for named code objects (e.g. `_record`, `stacked`).
6. Each row records: `claim, cited_receipt, verified_commit, status, evidence` (CSV columns fixed).
7. No claim is called drift unless the git evidence is quoted; judgement calls (e.g. sequencing ambiguity) are
   labelled in the evidence text.

## 7. Outputs

- `results/receipt_audit.csv` — one row per audited sub-claim.
- `FOLLOWUP_RECEIPT_AUDIT.md` — methods, results table by document, findings (C3), limitations, and the honest
  note that this was post-hoc.
- Counts: N VERIFIED / M COALESCED / K WRONG-COMMIT / J MISSING, over sub-rows.

## 8. Out of scope (stated before the audit)

- No audit of the server, box logs, or provenance narratives (read-only host git only).
- No audit of `HANDOFF.md`/`HANDOFF.txt`, the research records on each branch, or the "What is trustworthy"
  section of MIGRATION (not a branch/head claim).
- The claimed local-only worktree `~/neon-boot/wt/eq` points into a **different Git repository**; per the
  no-touch rule for `~/massification_live` I will not inspect that repository's refs, only record the pointer.
- No edit to `ARTICLE.md` or `RECEIPTS.csv`; no causal language; no server power actions.

## 9. Honesty note

Because the audit question was generated by the confirmatory essay's own finding, any elevated drift count
here cannot be read as a base rate. It is a targeted check of two documents, and its result may be negative
(i.e. receipts mostly verify). That outcome will be reported as plainly as a positive one.
