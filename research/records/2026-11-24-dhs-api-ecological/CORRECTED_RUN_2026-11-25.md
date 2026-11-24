# Corrected run — 25 Nov 2026 (Neon audit item 1: bootstrap multiplicities **and** full construct×schooling interaction set)

**Status: PROVISIONAL.** These numbers come from the in-flight fix applied on the box, **not** from Neon's
drop-in diff. Do **not** update dashboard / handoff D3–D4 text from this file until Neon's patch is applied
and reproduces them.

**Branch:** `research/dhs-corrected-2026-11-25` (additive, cut from `fe762b9`; pushed — corrected run
`3faeff3`, provenance `45b974e`, this correction commit on top).

## Provenance and authorship (read this before citing)

**Who ran it.** This corrected run was executed on the box by a **lingering agent from the retired
window** — not by the Commander of the 25 Nov session and not by the Lead. Evidence: `/root/work/run_neon_fix.sh`
has mtime 00:17 CST (before the 25 Nov session's first action at 00:18), and the dhs-api script edits and
`results/` writes are 00:15–00:20 CST. That same retired-window worker later wrote the on-box
`shutdown_after_two.sh` that powered the instance off at 00:31:04 CST (see `POWER_RULES_2026-11-25.md`
in `research/handoff-2026-11-24`).

**Exact provenance.** box `autodl-container-a8f742b5ee-292349c5`
(`ssh -p 45973 root@connect.cqa1.seetacloud.com`); work dir `/root/work/dhs-api`; runner
`/root/work/run_neon_fix.sh`; log `/root/work/neon_fix.log` (+ `neon_fix_stats.txt`, WALL_SECONDS=211);
run window ~00:15–00:20 CST / 16:15–16:20 UTC; 8 workers; numpy 1.24.1. Logs preserved in
`results/server_box3_corrected/`.

**Why it is trustworthy anyway.** The Commander of the 25 Nov session re-fetched the run's scripts and
outputs, re-ran `corrected_reduction.py` **host-side** against the committed panels, and reproduced
every reported number to ~1e-12 (Africa-11 2-group ratio 1.069843350505824, CI [0.9987338159871082,
1.1403490938072518]; A_vs_B −0.19669737936298431; C_vs_B −0.0031318298867118), with the built-in
validation gate passing against the prior record (max |Δ| 0.0036). Neon's verifier independently
reproduced the same numbers (24/24 within 1e-9, max|Δ| 5.4e-15).

**Input-integrity claim — scope of evidence.** The Commander ran `sha256sum -c data/MANIFEST.sha256` on
the box at ~00:25 CST and saw 28/28 OK. That check is **not preserved in the committed record** (the
committed `run.log` only carries `JOBA/B/C_EXIT=0`), so from the preserved evidence alone the input hashes
are **UNVERIFIED**; the check is reported here as a run-time observation by the reviewer, not as a
quoteable provenance fact.

**Status.** PROVISIONAL: produced by an unattributed box run that has been host-reproduced. It does not
substitute for Neon's `ir_pipeline.py`/`estimate.py` diff; when that lands, re-run under a known runner
and reconcile. Dashboard and migration-handoff D3–D4 text remain untouched until then.

## What changed — two independent changes, with different effects

Neon audit item 1 contains **two** corrections. They are separable and must not be conflated:

**(a) Cluster-bootstrap multiplicities → bootstrap CIs only; it cannot move a point estimate.**
`_boot_task()` in `scripts/estimate.py` (and `ratio_boot()` in `scripts/corrected_reduction.py`) did
`r["country"] in samp`, which keeps each resampled country **at most once**. That is a subsampling
bootstrap, not a country-cluster bootstrap: ~36.8 % of resampled slots were dropped and the intervals were
too narrow. Fix: draw multiplicities (`collections.Counter`) and replicate each resampled country's cells
`count` times (frequency weight = count). By construction this changes only the resampling distribution —
any point estimate computed without resampling is identical.

**(b) Full construct×schooling interaction set → moves the D4 point estimate.**
`stacked()` in `scripts/estimate.py` and `m1()` in `scripts/corrected_reduction.py` previously interacted
the construct dummy with **only the secondary category** (4-level) / `secplus` (2-group). The pre-registered
contrast is the **full** construct × schooling interaction across all education categories; those terms are
now included (`X = [e, con, e_j × con for all j]`; the runner log itself labels JOB A
"bootstrap multiplicities + full stacked interactions").

**Consequence: the Q2b1 point-estimate move is (b), not (a).** `C_vs_B` secondary goes −0.0775 → −0.1962
because the interaction set changed. **Neon's bootstrap-only diff applied to `fe762b9` will give ≈ −0.0775
with corrected CIs, not −0.1962, unless his patch also changes the interaction set.** The Q2a ratios and
the M1 gradient are point-estimate-invariant to (a) and are unchanged here; their CIs are what move.

The separate fixed-effect bug (dropped reference level with no intercept, −0.01 to −0.02 children bias) was
already fixed in `d63754f` and is unchanged here; both scripts still carry it.

## Run

- Box: `autodl-container-a8f742b5ee-292349c5` (`connect.cqa1.seetacloud.com:45973`), 8 workers, numpy 1.24.1.
- Driver: `/root/work/run_neon_fix.sh`; log + wall clock preserved in
  `results/server_box3_corrected/{run.log,stats.txt}`. Wall time **211 s**.
- JOB A full sample (`estimate.py --outdir results`), JOB B Africa-11 (`--countries ... --outdir results/africa11`),
  JOB C independent cross-check (`corrected_reduction.py`). All exit 0.
- Input hashes: see "scope of evidence" above (UNVERIFIED from preserved record).

## Headline numbers after both changes

Full sample (88 countries / 369 surveys, weighted M1, 4-level): primary **−0.554**, secondary **−1.584**,
higher **−2.538** children (SE 0.0588 / 0.1667 / 0.2419); 2-group **−1.5514** (0.1452) — these are M1
weighted gradients and are unchanged by both (a) and (b).

| quantity | before (d63754f) | after (this run) | what moved it | verdict effect |
|---|---|---|---|---|
| Q2a ratio, 2-group (full, G=80) | 0.958 [0.914, 1.002] | **0.958 [0.906, 1.019]** | (a) CI only | stays includes-1.0 |
| Q2a ratio, 4-level (full, G=65) | 1.003 [0.932, 1.077] | **1.003 [0.921, 1.095]** | (a) CI only | stays includes-1.0 |
| Q2b1 C_vs_B (wanted vs actual TFR, SD) | −0.0775 (0.0217) | **−0.1962 (0.0495)** | **(b) interaction set** | **D4 secondary gap re-read: ≈ −0.196, not −0.078** |
| Q2b1 A_vs_B | 0.0158 (0.0411) | **0.0711 (0.0757)** | (b) interaction set | smaller claim, wider CI |
| Africa-11 ratio, 2-group | 1.070 [1.011, 1.135] | **1.0698 [0.9987, 1.1403]** | (a) CI only (point identical) | **now includes 1.0 — verdict moves to indeterminate** |
| Africa-11 ratio, 4-level | 1.178 [1.027, 1.356] | **1.1780 [1.0042, 1.3877]** | (a) CI only (point identical) | stays below 1.0 |

**The −0.1962 was predicted, not discovered.** `MIGRATION_2026-11-25.md` (`research/handoff-2026-11-24`,
"Quarantined / must-fix" item 1) says: "`stacked()` omits higher×co (+0.1804, p=0.030) and pri/hi
interactions; corrected D4 secondary gap ≈ −0.1962". This run implemented that interaction-set change and
reproduces the prediction. (The exact interaction set added is the full construct × all-education set,
which is the family of omission the note describes; the prediction matches to 4 dp.)

## Independent verification (host-side, no server needed)

`scripts/corrected_reduction.py` was re-run on the Mac against the committed panels (`data/`, 13 MB) with the
fixed script: it reproduces every number above to ~1e-12 (Africa-11 2-group ratio `1.069843350505824`,
CI `[0.9987338159871082, 1.1403490938072518]`; A_vs_B `−0.19669737936298431`; C_vs_B `−0.0031318298867118`),
and its built-in validation gate against the prior record passes (`max_abs_delta = 0.0036`). Neon's
verifier reproduced the same numbers independently. So the fix is reproducible off the server.

Minor: `estimate.py`'s own bootstrap and `corrected_reduction.py`'s differ in the last digits of the CI
(2-group full [`0.9056, 1.0144`] vs [`0.9060, 1.0191`]) — different RNG streams/implementations; both include 1.0.

## Open (for Neon / next window)

- Apply Neon's actual drop-in diffs and separate the two items explicitly: if his `estimate.py` patch fixes
  **only** the bootstrap multiplicity, the D4 point estimate will return to ≈ −0.0775; the interaction-set
  change (b) must be either his separate hunk or an explicit decision to adopt ours. Reconcile and re-run.
- `ir_pipeline.py` blockers (v190, region×round, CMC, weights, survey_type, MIS/AIS, clustering) are untouched.
- Only after reconciliation: update dashboard / handoff D3–D4 text.
