> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# BRIEF 008 — FINAL LOOP ADJUDICATION AND CLOSE-OUT

- **sent by / date:** lead, 2026-11-20 ~13:36 Asia/Shanghai (task-24).
- **purpose:** decide whether the programme's identification limits are *established*; audit every predeclared stop
  rule; name the final publishable object(s); set the data-first programme; draft close-out language.
- **status:** final brief of the programme.

## 1. Evidence read (on disk, this session)

`05b_experiments/loop5/runs/{E1,E1b,E4}/findings.txt`; `05b_experiments/loop5/{PRE_DECLARATIONS_L5.md,
EXPERIMENTS_L5.md, SUMMARY_L5.csv, ERROR_LOG_L5.md}`; `05_experiments/loop5/{LOOP5_STATUS.md, E2/findings.txt,
E3/findings.txt}`; `05b_experiments/loop4/runs/{U1,U1b,U2,U3}`; `05b_experiments/loop3/runs/{s1_table,s2_findings,
s3_findings}`; `05_experiments/loop2/{CALIBRATION_TABLE.csv, findings_ledger.txt, balance_checks.csv}`;
`04_data/econ_round2/PARAMETER_MAP.csv` (28 quantities) + `WBSOURCE_NOTES.md` + six WB snapshots;
`09_relations/` (panel WDI data + fetch/build scripts only — **RELATION_CANDIDATES.csv, DATA_PATTERNS.md,
MODEL_PLUG_MAP.md absent → relation layer PENDING/partial**); `08_council/brief_003..007`;
`06_report/RESEARCH_LOOP.md` §5.

## 2. Loop-5 results (verified cells)

| cell | evidence | verdict |
|---|---|---|
| **E1 gate-architecture gradient** | `05b/loop5/runs/E1/findings.txt`: policy-dated KOR=gate-each-transition model 27.3/25.0/24.4 vs observed 86.0/75.4/66.4 (misses −58.7/−50.4/−42.0); HKG=terminal-only 14.4/19.7/46.7 vs 35.1/46.6/70.3 (−20.7/−26.9/−23.6) | **FAIL all six; gate-position story dropped, not re-fitted** |
| **E1b KOR no-fit** | stage fee multipliers fitted (0.852/1.104/1.363 → 11.5/14.9/18.4% by construction); participation 27.8/24.6/23.3 vs 86.0/75.4/66.4; provider commercial share 41.4% (<50% check); overall checks 13.5 vs 13.8% (pass), 14.2 vs 10.8% (fail) | **FAIL; the stop-rule stands permanently** |
| **E4 income gradient** | demand-consistent top/bottom spend ratio 2.14 vs observed 3.67; predeclared band [1.84, 5.51]; monotone; mechanical income identity 8.55 (diagnostic only) | **PASS (weak)** — one behavioural regular, not identification |
| **E2 provider technology/fee** | T1 spend mix: hagwon 47.7 vs 73.7 (−26.0 pp), small group 17.3 vs 6.7, others pass ⇒ FAIL; 3/36 quality parameterisations pass; T2 HKG mass-lecture gap −55.3 pp at declared prior but 33/36 grid cells pass ⇒ not identified; T3 HKG fee/income 3.56% (inside 1.1–5.0%) ⇒ PASS; cost-plus: observed fees 1.5–4.2× teacher-time+amortised-entry cost | **FAILS thresholds; not the missing channel; cannot price itself (rents/brand carry fees)** |
| **E3 Japan density** | required elasticity: density 0.226 (band 0.1–0.6) PASS; income 2.05 (band ≤1.0) FAIL; gate-stakes 5.29 (band ≤2.0) FAIL; n=2 endpoints, full 47-prefecture table absent ⇒ T5 not computable | **density "not rejected", not identified** |

**Cumulative prior cells:** C1 no-ID + forced-ID (0.30–0.50); C2 supplied attainment/one-way jobs; loop-2 freeze-both
(job side 3–4% generated); U1 fee pass/ordering fail; U1b HKG OOS fail; U2 recovery 0.50/forced-ID 0.30; U3 PH
holdout fail (14.68 vs naive 5.70), KHM pass (1.84); loop-3 S1 3/3 outside; S2 no structural reproduction (PH 11.7
pp); S3 UNABLE.

## 3. Parameter map (04_data/econ_round2/PARAMETER_MAP.csv)

28 model quantities: **8 observable** (shadow incidence uneven, completion partial, sector/status employment,
education spending, PTR, cohort/age, urbanisation, GDP/inflation), **10 NOT observable** (formal-job creation
elasticity to schooling, wage premium by education, Mincer returns, formal/informal transitions, public-sector
employment share, transition-to-tertiary/repetition/dropout, LFPR by education, credential requirement in hiring,
formal wage premium, nurse deployment), the remainder proxy/partial (remittances, provider fees not entry costs,
credential stock, teacher pay, per-student spend, contributing family workers, school counts).

## 4. Questions for the panel (task-24, 1–6)

1. Has the programme **established its identification limits**? Enumerate excluded and possible.
2. **Stop-rule audit:** every predeclared rule, fired or not, with the evidence cell; confirm or reject the
   "two iterations without identification gain ⇒ stop" rule.
3. **Final publishable object(s)**, ranked, with evidence and referee asks.
4. **Data-first programme**, ranked, with cost/access route, that would reopen each closed claim.
5. **Close-out language** for `06_report/LOOP_CLOSEOUT.md`.
6. **Record any dissent.**

## 5. Rules

On-disk evidence only; untraceable numbers `UNABLE TO ASSESS`; no fabrication; each verdict cites the cell/file.
`09_relations` marked PENDING/partial (panel data present; candidate relations absent) — cite as "new data/relations
needed", never invent an id.
