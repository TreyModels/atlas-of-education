> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# RESULTS BRIEF 005 — ITERATION-2 PARTIAL RESULTS (country cards, targets, two-way + shadow module)

- **sent by / date:** lead, 2026-11-20 ~13:14 Asia/Shanghai (explicit SIGNAL; partial set accepted by instruction).
- **purpose:** review the iteration-2 artifacts that are on disk; mark the runner-1 layer pending; judge shadow
  incidence, cohort-flow consistency, two-way identification/imposition, and run the **restatement test**; supply
  amendments + next 3 experiments.
- **what this informs:** iteration-2 reporting language and whether any iteration-2 result may be cited.

## 1. Artifacts ON DISK (verified this session)

| artifact | path | status |
|---|---|---|
| Country cards (6) | `02_lit/COUNTRY_CARDS/{PHL,KHM,HKG,CHN,KOR,JPN}.md` | present; sourced/dated, with NOT FOUND / NOT VERIFIED flags |
| Shadow target register | `02_lit/SHADOW_TARGETS.csv` | 21 rows; **11** rows `use_as_model_target=YES` (not 6) |
| Target sets | `04_data/TARGETS_SHADOW.csv`, `04_data/TARGETS_FLOW.csv` | present; shadow = HK rows + unresolved PH/KHM/CHN; flow = mostly unresolved/proxy |
| Loop-2 module (batch B) | `05b_experiments/loop2/{EXPERIMENTS_L2.md, SUMMARY_L2.csv, PRE_DECLARATIONS_L2.md, ERROR_LOG_L2.md, code/twoway.py, runs/L2, runs/L2_uncalibrated}` | present; 150/150 trajectories, 0 failures; uncalibrated sensitivity present |
| Brief 004 | `08_council/brief_004/` | design review, accepted by Lead |

## 2. Artifacts PENDING (marked UNABLE TO ASSESS, not inferred)

- `05_experiments/loop2/` — runner-1 country configs, `CALIBRATION_TABLE.csv`, **longitudinal cohort ledger**. Still running.
- Recovery with truths outside the candidate set and forced-ID rate (Amendment L2-4) — **not run**.
- 1980–2010 fit / 2011–2024 holdout on PH and KHM observed completion (Amendment L2-5) — **not run**.
- KOR and JPN: country cards exist, but no loop-2 simulation run exists for them.

## 3. Claims to judge (from the Lead's signal; verified against files where possible)

| ID | claim | verified numbers in artifacts |
|---|---|---|
| G1 | Freeze-both: job path is schedule-like | frozen-schooling complex vacancies PH 71.0→130.9, HK 172.8→235.8, KHM 32.3→80.0; endogenous schooling adds +4.5/+6.5/+3.1 jobs (~3–4%) (`EXPERIMENTS_L2` §2) |
| G2 | Freeze-economy: attainment still rises (residual shadow channel) | +0.028/+0.022/+0.024 (frozen) vs +0.067/+0.118/+0.077 (live) → residual ≈20–40% (`EXPERIMENTS_L2` §2) |
| G3 | Direction: HK demand-led only | HK Ec_dir +0.0983 (2sd 0.0138); PH ed/ec ≈ −0.0008/−0.0004; KHM +0.0008/−0.0119 → neither (`EXPERIMENTS_L2` §1) |
| G4 | Provider entry/teacher-tutor dominance | teacher share 76/86/97%; endogenous vs fixed-supply take-up PH 0.884 vs 0.219, HK 0.865 vs 0.327, KHM 0.887 vs 0.258 (**54–67 pp**, not the 46–66 pp in the signal); prices at floor 0.30/0.55/0.13; provider counts +5–90× (§3) |
| G5 | One-moment fit cannot pin cross-country shadow | HK fitted to 0.85 → PH 0.884 / KHM 0.887 with no verified target; uncalibrated HK 0.581 (−26.9 pp) (§4) |
| G6 | Biggest data misses | KHM formal share +14.0 pp; KHM university-attainment proxy +17.5 pp; PH completion −8.9 pp; KHM completion +9.9 pp; positional response null in all countries (§5–6) |
| G7 | Missing layer | runner-1 calibration table + cohort ledger; recovery; holdout (see §2) |

## 4. Questions

1. Does shadow education appear where the literature says — by stage, provider and country? (Targets: `SHADOW_TARGETS.csv`; country cards.)
2. Are cohort flows internally consistent, and can anything be said before the runner-1 ledger lands?
3. Is the two-way economy feedback identified or imposed (freeze-both)?
4. **Restatement test:** were any of the literature shadow rates coded as parameters? For each target, generated vs set.
5. Sign-off or amendment list; next 3 experiments with arms / estimand / threshold / cost.

## 5. Known limitations

- Partial set: runner-1 loop2 (configs, calibration table, cohort ledger) absent; recovery and holdout not run.
- Uncalibrated sensitivity run is a declared variant, not a validation.
- All loop-2 numbers are stylized model output, not country estimates; GMR/CLFS observed cells only where cited.
- Price/entry block overshoots (prices at floor/ceiling); entry parameters uncalibrated.
- `SHADOW_TARGETS.csv` has 11 `YES` rows: KOR 78.5, KOR elem 90, JPN G6 41.8, HKG 85, KHM 68.4/41.3/60.5/26.4, PHL 46.5/23.8/28.1.
