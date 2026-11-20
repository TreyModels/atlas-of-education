> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# RESULTS BRIEF 006 — STOP-RULE ADJUDICATION (loop 3; loop 4 pending)

- **sent by / date:** lead, 2026-11-20 ~13:21 Asia/Shanghai (re-sent signal; run now).
- **purpose:** adjudicate the predeclared stop-rule event fired by loop 3; define what is withdrawn; rank the
  publishable objects; name the single rescue experiment; sign off withdrawal language in `SUMMARY_FOR_TREY.md` and
  `06_report/RESEARCH_LOOP.md`.
- **what this informs:** iteration-3/4 reporting language and the programme's publishable output.

## 1. Artifacts read (verified this session)

| artifact | path | status |
|---|---|---|
| Loop-3 predeclarations | `05b_experiments/loop3/PRE_DECLARATIONS_L3.md` | present |
| Loop-3 experiments record | `05b_experiments/loop3/EXPERIMENTS_L3.md` | present |
| Loop-3 summary | `05b_experiments/loop3/SUMMARY_L3.csv` | present |
| S1 stage-matched table | `05b_experiments/loop3/runs/s1_table.txt` / `s1_table.csv` | present |
| S2 structural-parameter search | `05b_experiments/loop3/runs/s2_findings.txt` / `s2_search.csv` | present |
| S3 price/entry grid | `05b_experiments/loop3/runs/s3_findings.txt` / `s3_grid.csv` | present |
| Loop-3 error log | `05b_experiments/loop3/ERROR_LOG_L3.md` | present |
| Loop 4 | `05b_experiments/loop4/` | **not on disk at intake — PENDING, marked UNABLE TO ASSESS** |
| Withdrawal texts to sign off | `SUMMARY_FOR_TREY.md` §4b/§6; `06_report/RESEARCH_LOOP.md` §2/§4/§5/§6 | read |

## 2. Verified loop-3 numbers

**S1 — stage-matched shadow check (11 `use_as_model_target=YES` rows + HKG gradient; HK 0.85 excluded as the
calibration target).** Assessable countries = HKG, KHM, PHL; KOR/JPN and the HKG-1996 rows are `UNABLE TO ASSESS`
(no variants / no range).

| country | stage | literature % | model % | miss |
|---|---|---|---|---|
| PHL | all basic | 46.5 [42.0–49.9] | 23.5 | −19.0 to −26.4 |
| PHL | elementary | 23.8 | 17.4 | −6.4 |
| PHL | upper secondary | 28.1 | 39.4 | +11.3 |
| KHM | lower secondary (G9) | 68.4 | 21.3 | −47.1 |
| KHM | primary | 41.3 | 12.8 | −28.5 |
| KHM | primary urban | 60.5 | 19.6 | −40.9 |
| KHM | primary rural | 26.4 | 10.5 | −15.9 |
| HKG | lower secondary | 72 | 30.6 | −41.4 |
| HKG | middle secondary | 82 | 40.2 | −41.8 |
| HKG | senior secondary | 85 | 54.4 | excluded (calibration target) |

Predeclared threshold: ≥2 assessable countries outside range (or any HKG gradient check outside) ⇒ stop. Result:
**outside 3/3; HKG gradient misses 2 ⇒ STOP RULE 1 FIRED.** Direction flipped vs loop 2: loop-2 over-universalised
(0.88–0.89 everywhere), loop-3 under-predicts (except PHL upper, +11.3).

**S2 — structural parameters only (no take-up set directly).** PHL: baseline RMSE 15.2 pp, joint search 11.7 pp →
**no defensible reproduction**; one-parameter effects tiny (best +0.6 pp). KHM: 35.2 → 8.3 pp → **partial**, joint
solution at parameter bounds (pub = 0.0, stake 2.44, inc 2.87). HKG: 41.6 → 0.2 pp with **8 parameters for 2 targets**
→ saturated/weak identification, not evidence. Gate stakes, public-school substitute and credential returns do most
of the work.

**S3 — price/entry grid.** 675-point grid × 3 countries; finite prices and sensible provider counts, but the only
verified fee moments are Korean (434k won/month per student; 553k per participant) and there is **no KOR model
variant** ⇒ **UNABLE TO ASSESS**. Structural note: prices can stay above the floor at part of the grid (entry costs up
to 10×), so loop-2's floor collapse was an under-priced entry-cost block, not an intrinsic result.

## 3. Questions

1. Confirm the stop-rule event; state precisely what is withdrawn (incidence only, or more?).
2. Rank the publishable objects: (a) method + negative/identification map; (b) provider/fee economics on Korea;
   (c) data-first measurement programme; or a combination. Given the data reality — HKG is the only verified
   incidence number (and it is second-hand/caveated), KOR/JPN exist but have no model variants, PHL is one select
   sample, KHM is a two-school case, CHN is unresolved.
3. The single experiment that could still rescue an incidence claim.
4. Sign off or amend the withdrawal language in `SUMMARY_FOR_TREY.md` and `RESEARCH_LOOP.md`.

## 4. Known limitations carried in

- HK 0.85 is the loop-2 calibration moment and is excluded from pass/fail; if counted, loop-3 misses it too (54.4 vs
  85) — report in an appendix, not as a pass.
- S2's HKG "reproduces" is 8 params / 2 targets — do not read as replication.
- KOR/JPN lack model variants; HKG 1996 rows lack a declared range; both marked UNABLE, never counted as outside.
- Loop 4 (KOR variant + fee calibration, recovery/forced-ID, holdout) not yet on disk; if it lands before this panel
  closes it will be reviewed; otherwise PENDING.
