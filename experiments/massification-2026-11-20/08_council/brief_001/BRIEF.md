> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# RESULTS BRIEF 001 — reproduction + literature audit (provisional)

- **sent by / date:** lead, 2026-11-20 ~12:35 Asia/Shanghai
- **purpose:** decide whether the October paper's mechanism results are (a) reproduced, (b) imposed by the
  equations or discovered, and (c) novel enough to defend against Yoo 2003 / Kang 2026 / Ghaffarzadegan-Xue-Larson 2017.
- **what this informs:** the go/no-go framing of the final report for Trey; whether the remaining ~30 min of
  compute should go to new mechanism arms or to adversarial robustness.
- **provisional or final?** PROVISIONAL — the new experiment suite is still running; a second brief will follow.
- **follow-up cycle expected?** yes (brief 002 on the new experiment suite).

## 1. Artifacts

| artifact | path (relative to workspace root) | sha256 | commit | command | seed(s) | N | runtime | status |
|---|---|---|---|---|---|---|---|---|
| Claim register (68 rows) | `02_lit/CLAIM_REGISTER.csv` | `42e58d7b…55899` | n/a | manual extraction | — | — | — | completed |
| Model cards (7 deep, 13 secondary) | `02_lit/MODEL_CARDS.md` | `c5d504e6…c595` | n/a | — | — | — | — | completed |
| June-vs-October comparison | `02_lit/MANUSCRIPT_COMPARISON.md` | `82718a54…1d53` | n/a | — | — | — | — | completed |
| Model inventory (10 engines) | `03_audit/MODEL_INVENTORY.md` | `db12da75…8e5` | Atlas `55732f4`; massification snapshot git `02cade9` | — | — | — | — | completed |
| Floor/race 6-arm REPRODUCTION | `03_audit/logs/floor_test.log`; `03_audit/runs/massabm/floor_test/` | see log | massification snapshot `02cade9` | `python run.py floor_test --reps 2 --N 6000 --workers 2` | 2 reps | 6000 | 204 s | completed |
| Floor/race 6-arm STORED (manuscript source) | `01_sources/massification_project/results/round8_mechanisms_and_ledger_fix/floor_test/findings.txt` | `—` | same snapshot | `python run.py floor_test` (historical) | 4 reps | 6000 | archived | archived |
| Graduate-supply shock REPRODUCTION | `03_audit/runs/massabm/grad_supply/findings.txt` | `4a0332c1…7562` | `02cade9` | `python run.py grad_supply --reps 6 --N 6000 --workers 2` | 6 reps, paired | 6000 | 54 s | completed |
| Actor knockouts STORED | `01_sources/massification_project/results/round2b_three_actor_model/30_replications/necessity/findings.txt` | `—` | `02cade9` | `python run_triad.py necessity` | 30 reps (stored) | — | archived | archived |
| Gate/tutoring STORED | `01_sources/massification_project/results/round1_philippine_model/gates/findings.txt` | `—` | `02cade9` | `python run.py gates` | archived | — | archived | archived |
| Cohort accounting known-answer test | `/tmp/massrun/runs/kat_cohort.csv` (to be copied into `05_experiments/`) | `—` | new module | new `kat_cohort.py` | deterministic | 200/cohort | <5 s | completed |
| Country data (partial) | `04_data/data/wdi_4countries_long.csv`, `uis_sdg4_4countries_long.csv` | `—` | — | World Bank API + UIS | — | — | — | partial |

## 2. Claims table

| ID | claim (one sentence) | type | unit | estimand / quantity (denominator) | key numbers ± spread, N | where (path:line) | set by hand | falsifier |
|---|---|---|---|---|---|---|---|---|
| C1 | The 6-arm floor/race table reproduces at small reps | simulation | cohort of entrants 1995-2012 | mean diploma completion / formal-job rate / slope | ranked-no-floor 0.771 (0.002); unranked-no-floor 0.733 (0.004); adaptive-floor formal|dip 0.212 vs no-floor 0.351; reps=2, N=6000 | `03_audit/logs/floor_test.log` | floor levels, vacancy path, wage schedules | a rerun at documented reps that reverses the ordering |
| C2 | A floor alone gives persistence + exclusion but NOT intensification; ranking gives intensification | simulation | same | slope of Q3-5 college entry on degree income | unranked slopes +0.221 / +0.027 / +0.650; ranked slopes −0.034 / −0.068 / −0.037 | `03_audit/logs/floor_test.log` | utility spec, risk aversion, cost shapes | negative slope in unranked arms, or positive slope in ranked arms |
| C3 | Graduate-supply shock separates surplus account from competitive market on diploma holders' outcomes | simulation | diploma holders, labour market 2010-30 | Δ absolute income; Δ formal-employment rate | surplus: Δdip income −0.059, Δformal|dip −0.151; competitive: Δdip income +0.285, formal rate undefined | `03_audit/runs/massabm/grad_supply/findings.txt` | fixed vacancies, matching rule, informal cushion | competitive arm also showing a fall, at matched elasticity range |
| C4 | Removing households / employers / state costs 3.45 / 1.49 / 1.19 of 4.29 years | simulation | mean years schooling, years 110-139 | years added by full system over all-removed | 4.29 total; 3.45 / 1.49 / 1.19 | stored `round2b…/necessity/findings.txt` | screening costs/noise, tax rule, horizon | knockout ordering reversing under plausible screening cost |
| C5 | Tutoring clusters at gates where the bar sits among takers | simulation | share of gate takers who tutor | boarding 0.93, apex 0.30, basic 0.05, college 0.35; basic bar −2→+0.5 gives 0.03→0.77 | stored `round1…/gates/findings.txt` | tutoring cost/benefit functions, gate payoff shape | bar sweep that does not move tutoring, or flat shares across gates |
| C6 | Trey's October Prediction 3 ("gate line among its takers") is already derived in Yoo (2003) result 3 | theoretical / literature | — | — | Yoo: T=αe+ε, admit iff F(αe−t*), objective X·F(αe−t*)−βc(e); effort peaks near cutoff; ∂e*/∂t* sign-indeterminate | `02_lit/MODEL_CARDS.md` (Yoo card) | — | showing Yoo's result is not the same object (e.g. quota vs fixed bar changes it) |
| C7 | October silently drops every external empirical number present in June; 33 of 68 registered claims are unresolved | literature | claims | count | 68 claims; 33 verified (27 = model outputs), 33 unresolved/partial, 2 constructs | `02_lit/CLAIM_REGISTER.csv` | — | locating the dropped evidence in a cited source |
| C8 | The Ng & Yip (2020) citation in both drafts is likely Gee (2012) conflated | literature | — | — | printed subtitle matches Gee IPS WP-20 verbatim | `02_lit/SOURCES.json`, `MODEL_CARDS.md` | — | producing an actual Ng & Yip 2020 article whose subtitle matches |
| C9 | Cohort accounting conserves people/money/jobs in a known-answer world | simulation | persons, money, jobs | conservation discrepancy | deterministic 200/cohort, 8-year run | `05_experiments/` (in transit) | — | any conservation residual |

## 3. Rivals the results are claimed to have beaten

- **rival 1 — competitive CES skill market** (human-capital + imperfect substitution). Made comparable in C3:
  same households, same tuition shock, same vacancy/informational environment; differs only in wage formation.
  It wins if diploma holders' absolute income falls there too, at a matched elasticity range.
- **rival 2 — Yoo (2003) fixed-cutoff / quota model.** Comparable in C5/C6: same threshold logic, same
  effort cost. It wins (i.e. absorbs the contribution) if Trey's gate-clustering is a restatement of Yoo's
  effort-near-cutoff result and adds no new mechanism.
- **rival 3 — Ghaffarzadegan–Xue–Larson (2017) workforce pipeline.** Comparable on the nurse/professional
  supply failure (C4 and the October paper's own 0.25-vs-9 nurse result): same pipeline, provider capacity and
  top-down displacement. It wins if it explains Trey's own documented failure better than Trey's model does.
- **how a rival could win:** see each row; the crucial unrun cell is a *matched-elasticity* competitive market
  and a *Yoo-style analytic* derivation of the gate result.

## 4. Questions to the Council (≤6)

1. Which of C1–C5 are **imposed by the equations** rather than discovered? In particular: does "intensification
   requires ranking" follow mechanically from the specified utility/ranking rule? Does C5 require the particular
   tutoring cost/benefit functions?
2. Given C6 (Yoo already has effort-near-cutoff), what is the strongest **defensible novel claim** in October —
   the relational floor as a *level/eligibility* object, the three-actor convergence, or the compression
   technology? Is that enough for a paper, or is it a synthesis?
3. Is C3 a fair beat of the competitive market, or is it rigged by fixed vacancies + no formal sector in the
   rival? What would a fair matched-elasticity cell look like?
4. Given C7/C8, what is the **minimum external evidence** (from the country data ledger) that would move the
   mechanism claims from SIMULATION-ONLY to CONDITIONALLY SUPPORTED?
5. With ~30 minutes of compute left, what is the single **highest-value experiment**: a new mechanism arm
   (China school-support substitution), an adversarial robustness cell (matched-elasticity rival; equation
   knockout), or a recovery/identification test?
6. How visible should the citation problems (C6–C8) be in a report handed to Trey and, potentially, to Bjørn?

## 5. Known limitations and failures

- The floor/race rerun used reps=2 (stored = 4; manuscript reports 4) — ordering is stable, slopes differ by up
  to 0.07 (unranked no-floor +0.221 vs stored +0.151), likely small-rep noise. Not yet re-run at 4 reps.
- The audit's triad necessity rerun was still executing when this brief was written; C4 is **stored + in-flight**.
- All external numbers in the manuscripts remain `unresolved` until the data ledger lands.
- `05_experiments` suite is still running; no new-mechanism result is available yet.
- The iCloud copy of the 16 Nov venv was evicted; a fresh local venv (numpy 2.4.6 / scipy 1.17.1 / pandas
  3.1.1) was used. pandas 3.1.1 differs from the 16 Nov campaign's 2.3.3.

## 6. Out of scope / do not read

- Anything under `fleet.nosync/` (the user's live working tree) and `00_handoff/papers/` beyond the two papers.
- Do not re-derive model equations from memory; use `02_lit/MODEL_CARDS.md` and `01_sources/`.

## 7. Budget

- **deadline:** ~20 minutes.
- **Council output wanted:** reviews + deliberation + synthesis (default).
- **max words in the reply:** 900 for the synthesis; up to 500 per expert.
