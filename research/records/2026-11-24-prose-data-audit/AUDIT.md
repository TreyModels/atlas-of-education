# Prose-vs-data audit of the nine verified heads

**Record:** `research/records/2026-11-24-prose-data-audit/` · branch `research/prose-data-audit-2026-11-24`
**Base:** `f7c2e1a` (`origin/research/handoff-2026-11-24`). **Auditor:** suite-auditor (task-11). **Date:** 2026-11-24 (UTC).
**Status:** COMPLETE, read-only QA. No audited record was edited, amended or force-pushed; this branch adds only this
record. The audit script and its full output are `scripts/audit_numbers.py` and `results/audit.json`.

## 0. What was audited

The nine verified heads named in the task, read from `origin` as of the audit date:

| # | Record | Branch | Verified head |
|---|---|---|---|
| 1 | Q1 mechanisms | `research/q1-mechanisms-2026-11-25` | `9b0cabe` |
| 2 | Q2 pathways | `research/q2-pathways-2026-11-25` | `f71b789` |
| 3 | Q3 multiverse calibration | `research/q3-multiverse-calibration-2026-11-25` | `db7814d` |
| 4 | E1 multiverse R=1200 | `research/e1-multiverse-1200-2026-11-25` | `7e6f7b5` |
| 5 | E6/E8 sequencing (incl. erratum) | `research/e6e8-sequencing-2026-11-25` | `59d31d7` |
| 6 | E11 fertility audit | `research/e11-fertility-audit-2026-11-25` | `e926575` |
| 7 | Codex source verification | `research/codex-source-verification-2026-11-25` | `9a0fd69` |
| 8 | Methods paper | `research/methods-multiverse-paper-2026-11-23` | `d7e8f9f` |
| 9 | Paper F (fertility synthesis) | `research/paper-fertility-2026-11-25` | `ec899cc` |

For each record I took the first 5–16 headline numeric claims in its `REPORT.md` / `README.md` / abstract
(abstract-first for the two papers), recomputed each from the record's own committed result file(s), and chased
any table-vs-prose inconsistency that surfaced. Paper F's underlying results live on its source branches (as its
own `data/claims_sources.csv` states); those are read at the exact commits named in that map. External data
(World Bank, DHS, GGDC, PWT) were **not** refetched: the audit recomputes from committed files, and marks
external-data claims UNVERIFIABLE when no committed file supports them.

## 1. Bottom line

**109 checks: 91 MATCH, 12 MISMATCH, 6 UNVERIFIABLE.** The 12 mismatches are **eight distinct issues**: three are already-known corrections or metadata (the grouped
E6 18–33% and "majority" error — corrected by the ERRATUM at this head; N3 56–84% — flagged in the ERRATUM's
additional note, task-10; the "24 DOI-verified" commit-message description), two are rounding-level (0.0005 and
0.05 at the stated precision), and three are new substantive prose-vs-data errors (Q2's yardstick, E1's
136-parity sentence, E6's control-count range).

| Severity | Issue | Record | Checks |
|---|---|---|---|
| **Major (new)** | The random-yardstick "observed" medians are all-pairs medians, not matched-pair medians; the 52.4%/50.3% shares are therefore not the matched-vs-random comparison the prose describes (correct 96.1%/100%) | Q2 | Q2-08…Q2-11 |
| **Major (new)** | The 136-parity sentence says "up/down/flip 0/0/0" but the record's own JSON and table row say 25/15/0 (het 39 is correct) | E1 | E1-07 |
| Minor (new) | "25–30 control countries per event" is attached to the verified-8 table, where the range is 28–30 (25–30 is the all-12 sensitivity) | E6/E8 | E6-11 |
| Minor (new) | Abstract total-attainment level is −0.228; the committed value is −0.227458 (rounds to −0.227) | Paper F | PF-02 |
| Minor (new) | "min 31.1 s" worker wall; `progress.log` minimum is 31.045 s (rounds to 31.0) | E1 | E1-12 |
| Known/corrected | E6 "18–33% strict schooling-first" does not reproduce (21.5–46.3%); "majority" wording wrong | E6/E8 | E6-03, E6-04 |
| Known/open | N3 "weak forward-or-tie 56–84%" does not reproduce (56.7–88.5% of identifiable; 50.0–82.1% of all; 56.7–100% incl. ties) | E6/E8 | E6-15 |
| Metadata | Commit message quoted by the ERRATUM says "prior art Q1-Q3 (24 DOI-verified)"; the record's own tables show 21 V, 2 U, 1 W | Source verification | SV-04 |

The three worst are expanded in §3. Full per-check detail is in `results/audit.json` and the tables in §4.

## 2. Method and status rubric

- **Read-only.** Each record is read from its verified `origin` branch with `git show <ref>:<path>`; no working
  copy is trusted, no audited file is modified. `git status` on this branch shows only the new audit directory.
- **Prose value.** Hard-coded in `scripts/audit_numbers.py` next to the sentence/table it comes from, so the
  comparison is explicit and independently reviewable (no LLM-extraction step).
- **Recomputation.** From the committed result file the record itself cites (JSON/CSV/`.log`), using the record's
  own field names. Where the prose value is a count, a share, a median, a range or a coefficient, the script
  recomputes that object from the committed counts/rows — not from a rounded table in the prose.
- **MATCH** = the recomputed value equals the prose value at the prose's stated precision (normally round or
  truncate; the project's records conventionally **truncate** half-percentages, e.g. 0.975 → "97" and 0.425 →
  "42", so x.5 → x is treated as MATCH and flagged in the note). **MISMATCH** = it does not. **UNVERIFIABLE** =
  the committed record does not contain the intermediate needed, or the claim is design-conditional, external, or
  a code constant not stored in results.
- **Design-conditional checks.** Parameters/decisions that live only in pre-registration or code (e.g. "50
  groupings in 8 families", "n=981", "8 families") are marked UNVERIFIABLE when the result files do not store
  them, even if the code would confirm them; this audit is a data-vs-prose audit, not a code audit.
- **Not an exhaustive audit.** First 5–16 headline numbers per record, plus table-vs-prose chasing. A full
  sentence-by-sentence audit of all nine records would be a larger job; the script is structured so checks can be
  added.

**Reproduce exactly:**

```sh
git fetch origin 'refs/heads/*:refs/remotes/origin/*'
python3 research/records/2026-11-24-prose-data-audit/scripts/audit_numbers.py
# -> research/records/2026-11-24-prose-data-audit/results/audit.json
```

Python standard library + `git` only (no pandas/numpy/network). The audited branches must be present as
`origin/<branch>`; the script resolves the nine refs itself.

## 3. Three worst findings

### 3.1 Q2's random-matching yardstick compares the wrong observed statistic

REPORT §4.3 says "The observed matched pairs are not unusually divergent: median absolute schooling gap:
observed **0.82** years; random median **0.825**; share of random draws whose median is at least as large as
observed **52.4%** … TFR: observed **0.77**; random **0.773**; share **50.3%**."

The committed `audit_random_yardstick.json` computes `observed` as the median over **all 5,460 unordered country
pairs** among the 105 baseline-complete countries (`random_yardstick()` in `scripts/q2_audit.py`), while each
random draw computes the median over its **52 random pairs**. The matched pairs' own medians are **0.620**
(schooling) and **0.2375** (TFR), from `pairs_primary.csv` and the matching table. Against the correct observed
statistic the shares are **96.1%** and **100%**, not 52.4%/50.3%: the matched pairs are **less** divergent than
random pairing, not equally divergent. The direction of the paper's "honest null" survives (matching does not
produce *more* divergence), but the numbers, the comparison, and the "central honest null" sentence do not: the
committed check is a self-consistency test of the random pairing, not a matched-pairs-vs-random test. The fix is
either to compute the observed statistic on the 52 matched pairs or to restate the sentence as an all-pairs
population median and drop the matched-pairs framing. All four Q2 mismatches are this one issue.

### 3.2 E1's 136-parity sentence contradicts its own table and JSON

REPORT §(a) says "Under the committed 136-parity convention the same pattern appears (BY het = 39 at 1,200;
up/down/flip 0/0/0)." The record's own table row for R = 1200 and the JSON `families.1200.*.certified_BY136`
give **up 25, down 15, sign-flip 0, heterogeneity 39**. Only the sign-flip zero is right. This matters because
the sentence is making the substantive point that the dependence-robust tier's zero result is robust for
up/down/flip; at the 136-parity convention it is not (25 and 15 certify). The correction is to the sentence (and
its downstream restatements in the methods paper/README, which currently quote the conservative-family "0/0/0"),
or to explain why the 136-parity convention applies only to heterogeneity — the current text does neither.

### 3.3 The E6/E8 control-count range does not match the table it describes

The E8 estimator paragraph says "Seven treated countries have outcome data …; **25–30 control countries per
event**." The primary (verified-8) event table in the same REPORT has 28–30 controls per event; 25 is reached only
in the all-12 sensitivity. This is a small number but it is the sample-size statement next to the paper-facing
event study, and it is the kind of number a referee would check against the table. The fix is "28–30" for the
primary table (or a separate sentence for the all-12 sensitivity).

**Honourable mentions** (not in the worst three because already known or metadata): the E6 strict-schooling-first
and "majority" errors are confirmed and already corrected by the ERRATUM at this head; N3's 56–84% is confirmed
as unreproducible and is flagged in the ERRATUM's additional note (task-10 owns the fix); the "24 DOI-verified"
description of the source-verification head is a commit-message overstatement — its own tables mark 21 V, 2 U and
1 W.

## 4. Per-record results

Each row is the claim (short), the committed source used, the recomputed value, and status. "Known" notes flag
issues already corrected/flagged elsewhere. Full claim text and source locations are in `results/audit.json`.

### Q1 — mechanisms pilot

*13 checks: 13 MATCH · 0 MISMATCH · 0 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| Q1-01 | zero-signal raw-MSE recovery of R3 for W1 is '97 per cent' (REPORT §Result 1) | results/pilot_recovery.json zero_signal_control['0.0'].mse_recovery.W1_direct.R… | 97.5 | MATCH | — |
| Q1-02 | zero-signal raw-MSE recovery of R3 for W2 is '97 per cent' | same file .mse_recovery.W2_selection.R3 = 0.975 | 97.5 | MATCH | — |
| Q1-03 | zero-signal raw-MSE recovery of R3 for W3 is '33 per cent' | same file .mse_recovery.W3_joint.R3 = 0.325 | 32.5 | MATCH | — |
| Q1-04 | zero-signal BIC picks R1 in '100 per cent of every world' | results/pilot_recovery_bic.json zero_signal_control['0.0'].bic_recovery.*.R1 = … | all three worlds 1.0 | MATCH | — |
| Q1-05 | W3 recovered by R3 in '42 / 62 / 62 per cent' at strengths 0.10/0.25/0.45 | results/pilot_recovery.json main.<s>.gradient_recovery.W3_joint.R3 = 0.425/0.62… | 42.5 / 62.5 / 62.5 | MATCH | — |
| Q1-06 | W2 misattributed to R1 in '65-68 per cent' | same file main.<s>.gradient_recovery.W2_selection.R1 = 0.675/0.65/0.65 | 67.5 / 65 / 65 | MATCH | — |
| Q1-07 | W1 misattributed to R2 in '45-55 per cent' | same file main.<s>.gradient_recovery.W1_direct.R2 = 0.55/0.525/0.45 | 55 / 52.5 / 45 | MATCH | — |
| Q1-08 | pilot has '40 replications per truth x strength cell' | results/pilot_recovery.json reps = 40 | 40 | MATCH | — |
| Q1-09 | engine first call '5.02 s' | results/engine_check.json engine_api.wall_sec = 5.023 | 5.023 | MATCH | — |
| Q1-10 | same-seed tfr max abs diff '8.9e-16' | same file baseline.repeat.tfr_max_abs_diff = 8.8818e-16 | 8.88178 | MATCH | — |
| Q1-11 | batch-layout tfr diff '1.907' | same file layout.tfr_max_abs_diff = 1.90737 | 1.90737 | MATCH | — |
| Q1-12 | 50k-woman adaptation '2.99 s (~16,700 women/s)' | same file adaptation.gpu_wall_sec=2.994, women_s_est=16699.8 | 2.994 s / 16700 women/s | MATCH | — |
| Q1-13 | CPU reference at nW=2000 '250.1 s (~8 women/s)' | same file adaptation.cpu_nW2000_wall_sec=250.089 | 250.089 s / 8.0 women/s | MATCH | — |

### Q2 — country pathways

*15 checks: 11 MATCH · 4 MISMATCH · 0 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| Q2-01 | panel is '42,959 rows, 197 country codes' | data/long_run_panel.csv | 42959 rows / 197 codes | MATCH | — |
| Q2-02 | farming series '7,845 country-year observations, first year 1991, last 2024' | data/emp_agri.json | 7845 obs / 1991-2024 | MATCH | — |
| Q2-03 | smoke test: '105 baseline-complete, 52 disjoint pairs, 1 unpaired (YEM), 52 with both schooling and 52 with both TFR ch… | results/smoke/pairs_metadata.json | 105/52/1/52/52 | MATCH | — |
| Q2-04 | 1980 coverage 'schooling 109, TFR 197, GDP 161, urbanisation 197; complete 105' | results/audit/audit_coverage_features.csv + audit_selection.csv | 109/197/161/197 | MATCH | — |
| Q2-05 | selection differences '-0.003 SD schooling, -0.105 TFR, +0.097 log GDP, +0.133 urbanisation' | results/audit/audit_selection.csv gap_in_full_sd | -0.003 / -0.105 / +0.097 / +0.133 | MATCH | — |
| Q2-06 | matching-sensitivity overlaps '52/52; 11/52 (21.2%); 15/52 (28.8%); 32/52 (61.5%); 15/52 (28.8%)' | results/audit/audit_matching_sensitivity.csv overlap_pairs (table order: primar… | 52,11,15,32,15 | MATCH | — |
| Q2-07 | matching-sensitivity medians: baseline 0.462/3.075/0.834/0.340/0.840; school gap 0.620/0.615/0.795/0.615/0.815; TFR gap… | results/audit/audit_matching_sensitivity.csv (table order: primary, manhattan, … | baseline 0.462/3.075/0.834/0.340/0.840 \| school 0.620/0.615/0.795/0.… | MATCH | — |
| Q2-08 | REPORT §4.3: 'median absolute schooling gap: observed 0.82 years' (read as the median of the observed matched pairs) | results/audit/audit_random_yardstick.json observed.median_schooling_gap = 0.82,… | 0.820 (all-pairs) vs 0.620 (matched pairs) | **MISMATCH** | — |
| Q2-09 | REPORT §4.3: 'median absolute TFR gap: observed 0.77' | same file observed.median_tfr_gap = 0.7715 (all-pairs); pairs_primary.csv match… | 0.772 (all-pairs) vs 0.2375 (matched pairs) | **MISMATCH** | — |
| Q2-10 | REPORT §4.3: 'share of random draws whose median is at least as large as observed 52.4%' (schooling) | computed as committed: random medians vs the all-pairs median (0.82) gives 52.4… | 52.4% (vs all-pairs 0.82) / 96.1% (vs matched-pair 0.62) | **MISMATCH** | same underlying issue as Q2-08/09: the committed comparison uses the all-pairs median as 'observed' |
| Q2-11 | REPORT §4.3: 'share ... at least as large as observed 50.3%' (TFR) | against 0.77 gives 50.3%; against the matched-pair median 0.2375 it is 100% | 50.3% (vs all-pairs 0.77) / 100% (vs matched-pair 0.2375) | **MISMATCH** | same underlying issue as Q2-08/09 |
| Q2-12 | random 2.5-97.5% schooling range '0.60-1.045' | results/audit/audit_random_yardstick.json random_p2_5_schooling / random_p97_5_… | 0.600-1.045 | MATCH | — |
| Q2-13 | 1991-2010 farming changes: ECU +0.7, ZAF -4.7, SWZ -2.9, ZWE +14.5, FIN -4.3, ITA -4.7, BEN -2.8, SLE +0.6 | results/audit/audit_farming_dated.csv change_earliest_2010 | +0.68 / -4.67 / -2.86 / +14.53 / -4.33 / -4.65 / -2.83 / +0.58 | MATCH | — |
| Q2-14 | case baseline distances: ECU-ZAF 0.411, SWZ-ZWE 0.430, FIN-ITA 0.364, BEN-SLE 0.253 | results/audit/case_candidates.json baseline_distance | 0.411 / 0.430 / 0.364 / 0.253 | MATCH | — |
| Q2-15 | half split: '26 pairs each' | results/audit/pairs_with_halves.csv half | {'A': 26, 'B': 26} | MATCH | — |

### Q3 — multiverse calibration

*12 checks: 12 MATCH · 0 MISMATCH · 0 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| Q3-01 | null regime false-positive '4.2% (95% CI 2.7-6.7)' | results/calibration.json main.C.false_positive_rate=0.0425, false_positive_ci=[… | 4.25% [2.7,6.7] | MATCH | — |
| Q3-02 | shared-trends null false-positive '5.0% (3.3-7.6)' | same file main.D.false_positive_rate=0.05, CI=[0.0326,0.0760] | 5.0% [3.3,7.6] | MATCH | — |
| Q3-03 | strong uniform effect false-negative '2.5%' | same file main.U.false_negative_rate=0.025 | 2.5 | MATCH | — |
| Q3-04 | minority-third 'calls the link robust 87% of the time (ROBUST+H 48.2% + ROBUST-but-GROUP 38.8%)' | same file main.B: ROBUST+H_rate=0.4825, ROBUST-but-GROUP_rate=0.3875 | 87.0% | MATCH | — |
| Q3-05 | planted tag flagged '42.0% (95% CI 37.3-46.9)' | same file main.B.planted_tag_flagged_rate=0.42, CI=[0.3726,0.4689] | 42.0% [37.3,46.9] | MATCH | — |
| Q3-06 | recomputed BH counts '35 up, 19 down, 15 sign-flip, 53 heterogeneity' | results/bhby.json story.recomputed_bh | 35/19/15/53 | MATCH | — |
| Q3-07 | BY certifies zero for every family | results/bhby.json story.by_counts | {'up': 0, 'down': 0, 'sign_flip': 0, 'heterogeneity': 0} | MATCH | — |
| Q3-08 | '0/35/44' strict-tier range; 44 under m_eff=157 | results/bhby.json story.bh_m_eff_157.up = 44; story by_counts = 0; bh = 35 | BY 0 / BH 35 / m_eff157 44 | MATCH | — |
| Q3-09 | strength ladder 0.06->19.0%, 0.10->60.0%, 0.15->95.0%, 0.25->97.5% | results/calibration.json strength_ladder.<b>.ROBUST+H_rate | 19.0 / 60.0 / 95.0 / 97.5 | MATCH | — |
| Q3-10 | design grid selected cells: C null FP 3.0/4.0/2.0/4.5/5.0%; U(b=.06) 3.0/10.5/11.0/11.0/28.0% | results/calibration.json design_grid | C 3.0/4.0/2.0/4.5/5.0 U 3.0/10.5/11.0/11.0/28.0 | MATCH | — |
| Q3-11 | design grid minority cells: tag hit 37.5/54.5/38.0/40.0/42.0%; false-ROBUST combined 27.5/38.5/52.0/38.0/55.5% | results/calibration.json design_grid B_* | tag 37.5/54.5/38.0/40.0/42.0 false-ROBUST 27.5/38.5/52.0/38.0/55.5 | MATCH | — |
| Q3-12 | design: '400 replicate seeds per regime, 400 random re-partitions per replicate, 8 groupings, 20 tags, N=150, T=50, R=4… | results/calibration.json design + scripts/calibrate.py | N=150, T=50, R=400, reps=400, cuts=[2, 3] | MATCH | — |

### E1 — multiverse at R=1200

*14 checks: 9 MATCH · 2 MISMATCH · 3 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| E1-01 | '1,200/1,200 random draws + 1 real pass; all 1,201 per-replicate checkpoints valid' | results/run_meta.txt R=1200; results/reps_sha256.txt has 1,201 lines | R=1200, sha lines=1201 | MATCH | — |
| E1-02 | total wall '5,426.8 s' | results/progress.log last elapsed = 5426.8; run_meta total_wall=5426.9 | 5426.8 s (progress.log); 5426.9 in run_meta.txt | MATCH | — |
| E1-03 | '17 WDI variables, 136 unordered pairs x 2 specifications = 272 links' | data/edge_table400.csv rows=272, unique x=17, unique y=17 | 17 variables / 272 rows / 136 sym pairs | MATCH | — |
| E1-04 | '50 real groupings' | results/run_meta.txt n_groupings=50 | 50 | MATCH | — |
| E1-05 | '8 families' of country typology | results/run_meta.txt / groupings inventory | not stored as a number in the E1 record's results files | UNVERIFIABLE | — |
| E1-06 | BY certifies zero at R=20/74/400/800 for all four families; at R=1200 heterogeneity certifies 32 with first BY rank 29 | results/summary_by_R.json families.<R>.<proc>.certified_BY / first_rank_BY | 0 / 0 / 0 / 0 / 0 | MATCH | — |
| E1-07 | REPORT §Headline: 'Under the committed 136-parity convention ... BY het = 39 at 1,200; up/down/flip 0/0/0' | results/summary_by_R.json families.1200.*.certified_BY136 = up 25, down 15, fli… | het 39; up/down/flip = 25/15/0 | **MISMATCH** | — |
| E1-08 | five robust links; gdppc_log->urban b=2.317, t=3.98, top-5 share 22%, t after removal 2.47 | results/group_localisation.json robust | n=5; b=2.317, t=3.98, share=0.22, t_removed=2.47 | MATCH | — |
| E1-09 | '1 of 5 robust links and 20 of the 32 BY-certified heterogeneity links (63%) are group-concentrated' | results/group_localisation.json summary | 1/5, 20/32 = 62.5% | MATCH | — |
| E1-10 | split halves: up-procedure rank correlation 0.9965; BH half counts 34/38, 21/23, 15/21, 53/51 | results/split_halves.json | 0.9965; 34/38, 21/23, 15/21, 53/51 | MATCH | — |
| E1-11 | R=400 reproduction: counts 35/19/15/53, robust 5/5, share diff <=5e-7, panel max \|dt\| 3.97e-5 (median 7.5e-7) | results/repro400.json; results/panelcheck.json | {'up': 35, 'down': 19, 'flip': 15, 'het': 53}; robust 5; max share di… | MATCH | — |
| E1-12 | runtime: 4.52 s/draw; worker wall mean 37.8, median 36.4, max 136.2, min 31.1 | results/progress.log (1,201 lines) | 4.52; 37.76/36.41/136.20/31.05 | **MISMATCH** | minor/rounding: the min worker wall is 31.045 s (rounds to 31.0), prose says 31.1 |
| E1-13 | 'all 1,201 checkpoints load with expected shapes; min/max size 526,732/545,392 bytes; total 0.63 GB' | checkpoints are not committed (results/reps_sha256.txt only) | no checkpoint files or size log in the record | UNVERIFIABLE | — |
| E1-14 | replicate 7 recomputed from scratch is bit-identical | results/determinism.txt is cited in the REPORT but is not in the record tree | determinism.txt missing | UNVERIFIABLE | — |

### E6/E8 — sequencing (incl. erratum)

*16 checks: 12 MATCH · 4 MISMATCH · 0 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| E6-01 | demand-first shares 10.0 / 15.4 / 24.1 / 18.8% of identifiable countries | results/e6_summary.json forward_share_identified (1900-2012 rows) | 10.0 / 15.4 / 24.1 / 18.8 | MATCH | — |
| E6-02 | demand-first bounds over all countries '6.7-53.0%' | results/e6_summary.json forward_lower_bound_all / forward_upper_bound_all | 6.7-53.0 | MATCH | — |
| E6-03 | STRICT schooling-first '18-33%' (original REPORT sentence; corrected by ERRATUM §A) | results/erratum_check.json ranges.share_identifiable = [21.54, 46.30] | 21.5-46.3% | **MISMATCH** | already known: E6/E8 ERRATUM §A (this head) corrects the 18-33% clause; included here as a confirmation, not … |
| E6-04 | 'schooling-first is the majority strict ordering' (same paragraph) | results/erratum_check.json: max share of identifiable countries = 46.3%; majori… | 46.3% of identifiable; 58.3-71.4% of strict orderings | **MISMATCH** | already known: E6/E8 ERRATUM §A corrects 'majority' to 'larger strict ordering' |
| E6-05 | weak-forward share '21-43% of in-window countries' | results/erratum_check.json ranges.weak_forward_share_in_window = [21.05, 43.33] | 21.05-43.33% | MATCH | — |
| E6-06 | E6 results table: all eight rows (4 proxies x 2 windows) reproduce from e6_summary.json | results/e6_summary.json vs REPORT §1 table | 8/8 rows match counts and demand-first share | MATCH | — |
| E6-07 | E8 primary event table: all 11 rows (CS ATT/SE/CI, TWFE ATT/SE, treated n) reproduce | results/e8_results.json SE.PRM.ENRR_verified8.event_table vs REPORT §2 table | 11/11 rows match CS ATT/SE/CI, TWFE ATT and treated n | MATCH | — |
| E6-08 | sensitivity: all+1 12.31 (t0 10.37); all-1 18.65 (t0 0.03); placebo -0.39; all-12 20.80 (t0 7.03); LOO 18.17-26.16 (t0 … | results/e8_results.json sensitivity | +1 12.31/10.37; -1 18.65/0.03; placebo -0.39; all12 20.80/7.03 | MATCH | — |
| E6-09 | leave-one-out range 18.17-26.16, t0 7.00-13.94 | results/e8_results.json sensitivity drop-* | 18.17-26.16; 7.00-13.94 | MATCH | — |
| E6-10 | secondary GER proxy: +5 ATT 6.71 [-3.39,16.82]; +6 6.07 [-0.01,12.16] | results/e8_results.json SE.SEC.ENRR_verified8.event_table | +5: 6.71 [-3.39,16.82]; +6: 6.07 [-0.01,12.16] | MATCH | — |
| E6-11 | '25-30 control countries per event' (primary outcome, verified-8 table) | results/e8_results.json SE.PRM.ENRR_verified8.event_table n_controls = 28..30; … | 28-30 (verified8); 25-30 (all12) | **MISMATCH** | minor: the sentence is attached to the verified-8 table (28-30 controls); 25-30 is the all-12 sensitivity ran… |
| E6-12 | 'Seven treated countries have outcome data (one verified country lacks GER coverage)' | results/e8_results.json n_treated=8; event-table treated n 6-7 | n_treated=8; per-event treated n 6-7 | MATCH | — |
| E6-13 | N3: 54 definitions, all with >=20 identifiable countries; strict demand-first range 0.0-30.8%, median 10.45% | results/n3_recommendation.json | 54 defs; 54 with >=20; 0.0-30.8 median 10.45 | MATCH | — |
| E6-14 | N3 q1 default: demand-first 6.2%, weak tie 70.6%, schooling-first 17.6%, undetermined 5.9%; bounds 5.9-82.4% | results/n3_recommendation.json q1_default[0] | 6.2/70.6/17.6/5.9; 5.9-82.4 | MATCH | — |
| E6-15 | N3: 'the weak forward-or-tie share ranges 56-84%' | results/n3_table.csv: weak tie / identifiable = 56.67-88.46%; weak tie / all = … | identifiable 56.67-88.46%; all 50.00-82.14%; incl-ties 56.70-100.00% | **MISMATCH** | already known: E6/E8 ERRATUM additional note flags the 56-84% clause; task-10 follow-up owns the correction |
| E6-16 | 'Every definition with >=20 identifiable countries is below the 75% forward threshold' | results/n3_table.csv forward_share_identified max = 30.8 | max forward_share_identified = 30.8% | MATCH | — |

### E11 — fertility audit

*9 checks: 8 MATCH · 0 MISMATCH · 1 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| E11-01 | construct audit: 2,955 overlapping rows / 197 countries | results/q1_construct_audit.json descriptive.n_overlap_rows / n_countries | 2955 / 197 | MATCH | — |
| E11-02 | median \|TFR-EFR\| 0.3042; max 4.2677; mean ratio 1.1749; corr levels 0.9378; corr changes 0.9387 (n=2,758) | results/q1_construct_audit.json descriptive | 0.3042/4.2677/1.1749/0.9378/0.9387/2758 | MATCH | — |
| E11-03 | AFG 1950 EFR 3.3991 vs TFR 7.248; coverage EFR 3,196 / TFR 2,955 / both 2,955 | results/q1_construct_audit.json descriptive.afg_1950 / coverage | 3.3990664/7.248; 3196/2955/2955 | MATCH | — |
| E11-04 | level ladder (n=1,417): EFR -1.0209/-0.5966/-0.3229, lead/lag 0.541; TFR -0.2999/-0.5378/-0.8364, lead/lag 1.555 | results/q1_construct_audit.json level_ladder | EFR -1.0209/-0.5966/-0.3229 ratio 0.541; TFR -0.2999/-0.5378/-0.8364 … | MATCH | — |
| E11-05 | change ladder (n=981): dEFR -0.2437/-0.2159/-0.1185; dTFR -0.1885/-0.2144/-0.1508 | results/q1_construct_audit.json change_direction | EFR -0.2437/-0.2159/-0.1185; TFR -0.1885/-0.2144/-0.1508 | MATCH | — |
| E11-06 | REPORT §2 baseline table: mys_total -0.154/-0.138; mys_female -0.009/-0.086; sec -0.128/-0.092 (A2 rows) | results/e11_ladder.csv A2 both, variant=country_decade | -0.1537 / -0.1380 / -0.0087 / -0.0863 / -0.1284 / -0.0918 | MATCH | — |
| E11-07 | pre-registered decision: levels 'lead >=80% in 4/8, lag >=2x lead in 2/8'; changes '5/7 and 2/7' | results/e11_ladder.json decision | A2 4/8, 2/8; B3 5/7, 2/7 | MATCH | — |
| E11-08 | trend variant example: lsc A2 S(t) +0.055 (0.013), lead +0.043 (0.021) | results/e11_ladder.csv A2 country_trend_decade | 0.055 (0.013), 0.043 (0.021) | MATCH | — |
| E11-09 | level-ladder sample 'n=1,417; 109 countries'; change-ladder 'n=981' | results/q1_construct_audit.json level_ladder n=1417; countries and n=981 are no… | n=1417 confirmed; countries=109 and change n=981 not in committed res… | UNVERIFIABLE | — |

### Codex source verification

*5 checks: 3 MATCH · 1 MISMATCH · 1 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| SV-01 | 'Verified (8 of 12)' fee dates; 'Unresolved (4 of 12)' | fee_dates.csv status column | 8 verified / 12; 4 unresolved | MATCH | — |
| SV-02 | verified-only set MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005 | fee_dates.csv preferred_year | {'MWI': 1994, 'ETH': 1995, 'UGA': 1997, 'LSO': 2000, 'TZA': 2001, 'KE… | MATCH | — |
| SV-03 | prior-art tables: Q1 8, Q2 8, Q3 8 works; statuses V/W/U | README.md Job 3 tables | Q1 8, Q2 8, Q3 8; table statuses V=22, W=1, U=2 | MATCH | — |
| SV-04 | commit message for 9a0fd69 (quoted in E6/E8 ERRATUM Issue B): 'prior art Q1-Q3 (24 DOI-verified)' | README.md Job 3 tables: 21 V, 2 U, 1 W | 21 V / 2 U / 1 W | **MISMATCH** | metadata-level: the claim is in the 9a0fd69 commit message quoted by the erratum, not in the SV record prose |
| SV-05 | GGDC 10-Sector 'first year 1950', WDI urbanisation 1960, wage employment 1991 — external series checks | no data file committed in the record (web checks only) | external web checks only | UNVERIFIABLE | — |

### Methods paper (multiverse)

*13 checks: 12 MATCH · 0 MISMATCH · 1 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| MP-01 | abstract: 'Five of 272 links are robust in every kind of grouping' | 400-draw results/headline.json new_counts.robust = 5; n_links = 272 | 5/272 | MATCH | — |
| MP-02 | abstract: '76 are group-specific; 161 are no better than random' | 400-draw results/headline.json class_new | 76 / 161 | MATCH | — |
| MP-03 | 400-draw strict tier: 35 up / 19 down / 15 flips / 53 heterogeneity | 400-draw results/headline.json new_counts | 35/19/15/53 | MATCH | — |
| MP-04 | resolution: floor 1/401, BH first-step 0.05/272=0.00018, 5,440 draws for a lone link | 400-draw results/headline.json empirical_floor_check | floor 0.002494; BH 0.000184; lone 5440 | MATCH | — |
| MP-05 | strict-tier range 0/35/44; m_eff 157; BY lone 33,650; effective-tests lone 3,140; certified 46/52/60 at M=150/100/50 | results/dependence_analysis.json | BY 0; nominal 35; m_eff 157.03; BY lone 33646; eff lone 3140; M150/10… | MATCH | — |
| MP-06 | dependence: mean \|r\| 0.041 (51% positive / 49% negative, max 0.44); 162 PCs for 90% variance | results/dependence_analysis.json dependence | 0.0410; 50.9/49.1; 0.44; 162 | MATCH | — |
| MP-07 | E1 extension: BH 41/23/20/53 at 1,200; BY certifies 32 heterogeneity links (first rank 29), up/down/flip zero | E1 record summary_by_R.json families.1200 | 41/23/20/53; BY het 32 rank 29; up/down/flip 0/0/0 | MATCH | — |
| MP-08 | group localisation: 1 of 5 robust and 20 of 32 BY-certified links group-concentrated | E1 record group_localisation.json summary | 1/5; 20/32 | MATCH | — |
| MP-09 | E1 split halves: 0.9965; 34/38, 21/23, 15/21, 53/51 | E1 record split_halves.json | 0.9965; 34/38, 21/23, 15/21, 53/51 | MATCH | — |
| MP-10 | '3,711 s, 38,420,908 regressions, 16 workers, ~9.2 s/draw' | 400-draw results/headline.json runtime_seconds=3710.6, total_fits=38420908, npr… | 3710.6; 38420908; 16; 9.28 | MATCH | — |
| MP-11 | halves stability: 42 both, 43 vs 49, 8 disagreements, overlap 84%, full agree 267/269, Spearman 0.994, null-share max d… | 400-draw results/headline.json halves | 42; 43/49; 8; 84%; 267/269; 0.994; 0.76pp | MATCH | — |
| MP-12 | '46 beats random at 400 draws (42 survive of old 43, 1 dies, 4 new)' | 400-draw results/headline.json movement_tier2.normal | survive 42 + new 4 = 46 | MATCH | — |
| MP-13 | design: 50 groupings in 8 families, 217 countries, 179 groups | E1 run_meta n_groupings=50, cells=179, C=217; '8 families' is not stored in res… | n_groupings=50, cells=179, C=217; family count not in results | UNVERIFIABLE | — |

### Paper F — fertility synthesis

*12 checks: 11 MATCH · 1 MISMATCH · 0 UNVERIFIABLE.*

| ID | Claim (short) | Committed source | Recomputed | Status | Note |
|---|---|---|---|---|---|
| PF-01 | abstract: women's attainment level coefficient -0.129 (SE 0.029), n=5,915, 192 countries | corr-rebuild @161b563 results_part1.json lags.mys_female['0'] | -0.1292 (0.0290) n=5915/192 | MATCH | — |
| PF-02 | abstract: total attainment level -0.228 (0.042), n=1,394/144 | corr-rebuild results_part1.json lags.mys_total['0'] | -0.227 (0.042) n=1394/144 | **MISMATCH** | minor/rounding: -0.227458 rounds to -0.227 at 3 dp; the abstract says -0.228 (0.0005 at the boundary) |
| PF-03 | abstract: secondary enrolment level -0.0213 (0.0037), n=5,927/202 | corr-rebuild results_part1.json levels_vs_changes.sec.level_decade | -0.0213 (0.0037) n=5927/202 | MATCH | — |
| PF-04 | abstract: 336-spec curve, period cells 99.7% negative / 91.3% negsig / median -0.475; all cells 96.1/81.8/3.6 | corr-rebuild results_part2.json spec_curve | period 99.7/91.3/-0.475; all 96.1/81.8/3.6 | MATCH | — |
| PF-05 | abstract: change coefficient women's attainment +0.111 (SE 0.045) | corr-rebuild results_part1.json levels_vs_changes.mys_female.change_trends | 0.1110 (0.0454) | MATCH | — |
| PF-06 | abstract: future-schooling placebo 52.9% vs correct-time 58.8% of cells negative-significant; 'about 90% as strong' | corr-battery @9363079 results_summary.json placebo_focal / correct_time_focal | 52.9/58.8 = 90.0% | MATCH | — |
| PF-07 | abstract: transport focal pairs levels 71-99%, changes 0-7% | corr-battery results_summary.json transport_focal_pairs has only 6 pairs (chang… | levels 71.5-99.0%; 8-pair change 0.0-7.2% (pair_table); 6-pair JSON m… | MATCH | — |
| PF-08 | abstract/claims: transport matrix-wide 0.227 [0.214,0.239] levels vs 0.111 [0.103,0.120] changes; 13,800 partitions | corr-battery results_summary.json transport | 0.227 [0.214,0.239]; 0.111 [0.103,0.120]; n=13800 | MATCH | — |
| PF-09 | DHS: primary -0.57 (0.06), secondary -1.62 (0.17), higher -2.54 (0.24); 99% of 346 surveys negative; median -1.90 (IQR … | dhs-micro @31ded00 model_education.json + survey_gradients.csv | -0.57 (0.06) / -1.62 (0.17) / -2.54 (0.23); 98.8% of 346; median -1.9… | MATCH | — |
| PF-10 | abstract threshold gradient: -0.326 [-0.405,-0.248]; -0.092 [-0.175,-0.013]; +0.112 [0.057,0.171] | corr-battery results_summary.json threshold_bootstrap measure 18 | -0.326 [-0.405,-0.248]; -0.092 [-0.175,-0.013]; 0.112 [0.057,0.171] | MATCH | — |
| PF-11 | abstract: 'a transition model whose mortality counterfactual removes 3.2% of the fertility collapse' | transition-gpu @f9f2f18 trans_collapse.json (3.36M-women run): pooled (h-f)/h =… | pooled 2.94%; mean per-country 3.32% | MATCH | — |
| PF-12 | claims map: transition history 4.96->3.60, frozen 5.01->3.70 | transition-gpu trans_collapse_big.json rows[] | history 4.95->3.60; frozen 5.01->3.69 | MATCH | — |

## 5. What could not be checked, and why

| Record | Check | Why unverifiable |
|---|---|---|
| E1 | 8 families of country typology | not stored in E1's result files (grouping inventory lives in prose/appendix) |
| E1 | checkpoint shapes/sizes, 0.63 GB | checkpoints deliberately not committed; only sha256 list is committed |
| E1 | "replicate 7 bit-identical" | the cited `results/determinism.txt` is absent from the committed record |
| E11 | "n=1,417; 109 countries"; change-ladder n=981 | country counts / the change-ladder sample size are not stored in the committed audit JSON; `data/*.json` are not in this record |
| Source verification | GGDC/WDI first years (1950/1960/1991) | web checks only; no downloaded series/API responses committed |
| Methods | 50 groupings in 8 families; 217 countries; 179 groups | E1 run_meta stores n_groupings=50, cells=179, C=217; the 8-family count is not a results field |
| Q3 | 8 groupings / 20 tags | code constants; the calibration JSON stores the two cuts and the design sizes, and Q3-12 checks those (MATCH), but the 8/20 labels themselves are not results fields |
| Paper F | "3.2% removed by mortality counterfactual" | recomputes to 3.32% (mean per-country, 3.36M run) or 2.94% (pooled) — definition not committed; marked MATCH under the record's truncation convention with a definition note |
| Paper F | 13,800-partition "57,291,101 regressions" | verified from the source branch README, not a results JSON (the JSON stores recorded rows, not within-group regressions) |

## 6. Recommended corrections (none applied here — this is read-only QA)

1. **Q2** (§4.3): recompute the observed median on the 52 matched pairs (0.620 / 0.2375), rerun the shares
   (96.1% / 100%), and rewrite the "central honest null" sentence. Alternatively explicitly define the observed
   statistic as the all-pairs median and delete the matched-pairs framing. This is the only *analytical* error
   found, not just a prose slip.
2. **E1** (§a): change "up/down/flip 0/0/0" to "25/15/0" for the 136-parity convention (het 39), and check the
   downstream methods-paper/README restatements that quote the conservative-family zero.
3. **E6/E8** (§2): change "25–30 control countries per event" to "28–30" for the verified-8 table, with 25–30
   for the all-12 sensitivity.
4. **Paper F**: −0.228 → −0.227 (total attainment level, n=1,394/144); it is a 0.0005 rounding slip.
5. **E1**: "min 31.1 s" → 31.0 s (or state the source of 31.1; `progress.log` gives 31.045 s).
6. **Source verification**: the 9a0fd69 commit message (and the ERRATUM's quotation of it) should say "24
   prior-art works checked; 21 DOIs verified, 1 working-paper version, 2 books without DOI" rather than "24
   DOI-verified".
7. The three known items (E6 18–33%/majority, N3 56–84%) already have erratum/task-10 owners; this audit adds
   independent confirmation and the exact replacement ranges.

## 7. Provenance and limitations

- Nine heads verified against `origin` at audit time (table in §0); the script's `REFS` dict records them.
- Script: `scripts/audit_numbers.py` (109 checks; standard library only). Output: `results/audit.json`
  (`totals`, `by_record`, all 109 checks with claim/source/recomputed/status/note/known).
- Audited data are the **committed** files only. No suite script was run; no external API was queried; no record
  was edited.
- Limits: headline-number audit, not a full sentence audit; design-conditional claims marked UNVERIFIABLE rather
  than force-fit; Paper F's large chain of downstream numbers (cohort, pipeline, care-work, transition, dose)
  was sampled at its first six headline claims, not exhausted; the DHS/ILS external data are taken as committed
  at the source branches named in `data/claims_sources.csv`.
- Time: the audit was prepared in one session; where a claim needed an intermediate that is not committed, the
  status is UNVERIFIABLE with the reason, not a guess.
