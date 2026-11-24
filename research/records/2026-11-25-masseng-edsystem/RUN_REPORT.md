# RUN REPORT — full-system behavioural prototype + multiverse of equation choices (eduengine)

**SIMULATION ONLY — toy `eduengine` worlds; every parameter is illustrative; no causal or empirical
claims. The centre of gravity is the full massification system (household affordability, state/school
supply and funding, learning/quality, limited-place gates at all levels, credential→jobs,
rural/urban), with tutoring kept as one declared module. Missing mechanisms (migration, rural–urban
sorting, remittances) are stated, not invented.**

Server run: `/root/work/edsystem/research/records/2026-11-25-masseng-edsystem/`, 1,440 runs
(144 combinations × 10 seeds), **304.1 s at 12 workers**, no Mac compute. Branch
`research/masseng-edsystem-2026-11-25`.

---

## 1. What was built (and where each piece lives in `engine/eduengine/`)

The engine already contains the four connected pieces; this prototype wires them explicitly and
varies their equation/mechanism choices:

| Piece | Engine location | What it does in this prototype |
|---|---|---|
| Family affordability incl. **forgone child earnings** | `core.step` / `anchored_choice` / `need_frac`: yearly cash = income − subsistence + borrow·income + CCT; required = fees + `need_frac(income)·child_wage(age)`; children who cannot pay exit (liquidity) | 3 affordability choices: **cash-only** (borrow=0, constant replacement share), **credit** (borrow=.20, constant), **credit + poverty-line need** (borrow=.30, logistic replacement share) |
| Learning / quality | `modules/schools.py` (public quality via pay, monitoring, budget, PTR), `modules/schools.py` (private entry), `modules/tutoring.py` (tutoring gain) | 3 supply/learning configurations: **public only**, **+private**, **+private+tutoring** |
| Limited-place gates at levels | `core` gates + `anchored_choice`: bar vs quota (planned seats share), pass probabilities, cash first | **bar** vs **quota** at the four level transitions |
| Credential → labour outcomes | `modules/labour.py`: **QueueLabour** (credential floors, queueing) vs **CompetitiveLabour** (skill premium/returns) | both labour regimes, existing credential floors |
| Rural/urban | `core`: rural distance cost beyond primary; `urban_share` | **low** vs **high** rural penalty/urban share |
| Tutoring (one module) | `modules/tutoring.py`: MNL none/own/other/firm, gate-prep demand, access | present only in the `+private+tutoring` learning arm; declared as one module, not the centre |

Multiverse: 3 affordability × 2 supply/funding (fixed budget vs fiscal tax-share loop) × 3
learning/supply configurations × 2 gates × 2 labour regimes × 2 rural structures = **144
combinations × 10 seeds = 1,440 runs**. N=400 children/cohort, T=70 years, cohorts measured from
year 35; base world `formal_loop`. All axes are **equation/mechanism choices**, not calibrated
parameters.

---

## 2. Observed vs assumed (using the task-41 data-readiness map)

| Module | Observed data that exist (task-41) | What this prototype assumes | Status |
|---|---|---|---|
| Household demand/affordability | DHS IR gated; DHS API aggregates; LSMS irregular — no fees/forgone-earnings panel; **no public harmonised income×schooling data** | `need_frac` shape, child-wage profile, borrowing share, income distribution | **Assumed; not identified by public data** (task-41 top gap 1) |
| State/school supply & funding | UIS/EdStats PTR, teachers, private share, ~200 countries 1970–2023 | public budget per child vs fiscal loop (edu share, tax base), teacher pay/monitoring, private entry | **Partly usable** (ratios as covariates; capacity latent, no invented target) |
| Learning/quality | PISA/TIMSS/PIRLS/SACMEQ/PASEC/LLECE anchors; no annual grade-level learning series | CES-like learning response to quality/tutoring/home/ability; assessment scale not matched | **Anchors only; grade profile assumed** (gap 2) |
| Gates | EdStats completion/transition proxies, 1970–2022; no exam-pass/quota rules | bar vs quota seats, pass probabilities, no exam-score data | **Proxy only; mechanism assumed** (gap 3) |
| Jobs/credentials | ILOSTAT wages by education (~150 ctry 1990–2023); STEP gated; repo credential-floor record; E6/GGDC+PWT employment shares | queue with credential floors vs competitive skill premium; no credential-requirement series | **Returns proxy only** (gap 5) |
| Rural/urban & migration | WDI urban share 1960–2023; UN migrant stock (cross-border) 1990–2020; DHS residence | rural distance cost + urban income share; **no migration/sorting/remittances** | **Level only; flows absent** (gap 4) |
| Macro/development | WDI GDP/growth 1950–2023; GGDC/PWT E6 (post-1990 demand limit); WID/SWIID | fiscal loop (tax, education share) and income growth absent (static incomes) | **Usable covariates; not coupled here** |

The prototype is therefore a **constrained full-system model**: observed macro/supply blocks could
discipline it, but demand, learning, gates and jobs remain declared assumptions; the household
affordability block is the binding data gap.

---

## 3. Results (seed-level: mean and 90 % range across 10 seeds; no causal reading)

### 3.1 What moves attainment / inequality at which stage (pre-declared η²)

| outcome | largest axis (η²) | second | third |
|---|---|---|---|
| primary completion | **affordability .69** | jobs .15 | rural .05 |
| lower completion | **gates .70** | rural .06 | jobs .04 |
| upper completion | **gates .69** | rural .05 | jobs .04 |
| tertiary completion | **affordability .41** | gates .35 | rural .10 |
| public quality `q_pub` | **supply .42** | jobs .26 | learning .03 |
| formal share / edu share GDP | **jobs .96** | — | — |
| wealth parity (lower) | **rural .51** | affordability .26 | jobs .10 |
| wealth completion gap, upper | **gates .66** | affordability .09 | rural .09 |
| wealth completion gap, tertiary | **gates .77** | learning .04 | rural .02 |
| tutoring at gate-adjacent grades | **gates .89** | rural .07 | — |
| marginal value of learning | **learning .61** | jobs .09 | supply .08 |

Reading: **gates dominate lower/upper attainment and the wealth completion gaps; affordability
dominates primary and tertiary completion and the poverty gap; jobs dominate formal-share/education
spending; rural structure dominates wealth parity; supply/funding moves public quality but not
attainment; learning configuration moves the value of learning and quality slightly; tutoring is
gate-driven.**

### 3.2 Gates (bar vs quota), 10-seed means [90 % range]

| outcome | bar | quota |
|---|---|---|
| lower completion | **.720** [.592,.849] | **.550** [.549,.550] |
| upper completion | **.609** [.493,.746] | **.449** [.446,.450] |
| tertiary completion | **.411** [.273,.562] | **.313** [.248,.386] |
| tutoring rate (tutoring arm) | **.273** [.214,.320] | **.499** [.413,.564] |
| gate-adjacent tutoring | .320 [.250,.372] | .604 [.522,.677] |
| skill premium (competitive arm) | **1.59** [1.28,2.01] | **1.91** [1.69,2.16] |
| wealth parity, lower | .180 [.047,.387] | .165 [.052,.343] |
| lower completion, quintile 1 / 5 | **.174 / .966** | **.121 / .767** |

Who is pushed out: the bar gate is a **screen**: lower-secondary completion rises from .174 (poorest
quintile) to .966 (richest). The quota gate lowers completion for everyone (especially the middle:
q2 .617→.453, q3 .891→.672) and narrows the absolute top–bottom gap (.792→.646), while wealth
parity moves only .180→.165. Tutoring rises under quota for every quintile (q1 .068→.235, q2 .164→
.457, q5 .405→.578), and its mass shifts from tertiary (.145→.078) to lower/primary (.209→.267,
.426→.445). This is a seat-rationing/tutoring-demand reallocation in the toy model, not evidence
about real quotas.

### 3.3 Affordability (cash-only vs credit), 10-seed means [90 % range]

| outcome | cash-only | credit (constant) | credit (poverty-line need) |
|---|---|---|---|
| primary completion | **.797** [.746,.852] | **.929** [.865,.977] | **.910** [.831,.968] |
| lower completion | .615 [.549,.755] | .650 [.550,.848] | .640 [.550,.838] |
| tertiary completion | **.296** [.245,.392] | **.362** [.283,.497] | **.428** [.340,.569] |
| wealth parity, lower | **.103** [.047,.171] | **.231** [.093,.397] | **.183** [.044,.358] |
| lower completion, q1 / q5 | .091 / .889 | .195 / .849 | .157 / .862 |
| skill premium (competitive) | 1.95 [1.61,2.17] | 1.73 [1.37,1.99] | 1.57 [1.27,1.78] |

Borrowing/credit access is the largest single lever on primary completion and on the poorest
quintile's lower completion (.091→.195), and it raises tertiary completion .296→.428 under the
poverty-line need equation. Household affordability, not tutoring, is the demand-side driver in this
prototype.

### 3.4 Jobs / credentials (queue floors vs competitive)

| outcome | queue floors | competitive |
|---|---|---|
| formal share of GDP | **.293** [.275,.331] | **.627** [.556,.707] |
| wealth parity, lower | **.141** [.044,.302] | **.204** [.063,.393] |
| lower / upper / tertiary completion | .616 / .511 / .359 | .654 / .547 / .365 |
| skill premium | (queue module does not report this) | 1.59–1.91 across gates |

The credential→labour regime is the dominant determinant of the formal-share/education-spending
block (η² .96) and shifts wealth parity and completion, but the engine's queue/competitive forms are
stylised; observed ILOSTAT premia are not used as targets (returns proxy only).

### 3.5 Rural/urban structure (low vs high penalty)

| outcome | low penalty | high penalty |
|---|---|---|
| lower completion | **.660** [.550,.849] | **.610** [.549,.769] |
| upper completion | **.551** [.449,.746] | **.507** [.446,.659] |
| tertiary completion | **.388** [.277,.562] | **.335** [.248,.476] |
| tutoring rate | **.420** [.257,.564] | **.351** [.214,.489] |
| wealth parity, lower | **.245** [.124,.393] | **.100** [.043,.180] |
| skill premium (competitive) | 1.67 [1.28,2.02] | 1.83 [1.42,2.16] |

Rural distance/urban-share structure is the largest determinant of the wealth parity index and a
material determinant of attainment at every level. **No migration, sorting or remittance channel is
modelled**; the real rural–urban process would move both the distributions and the gaps, so these
numbers are structural assumptions, not estimates.

### 3.6 Supply/funding and learning configuration

- Supply: fiscal loop vs fixed budget changes **public quality** (1.12 vs 0.99; η² .42) and
  education spending (edu_gdp only exists in fiscal arms) but completion differences are small
  (.639 vs .631 lower; .534 vs .524 upper) and **supply is not identifiable from attainment** (range
  overlap 1.00 for all completion outcomes).
- Learning configuration: public-only → +private → +private+tutoring raises lower completion
  .622→.633→.651, upper .513→.526→.548, tertiary .347→.360→.379; the value of learning moves most
  (η² .61) and q_pub only slightly (1.03→1.07). Tutoring appears only in the third arm (rate .386),
  by design.

### 3.7 Tutoring module (one module, not the centre)

- Tutoring rate by gates: bar .273 vs quota .499; gate-adjacent grades .320 vs .604; the
  gate-adjacent **mass share** rises only .230→.250, so most of the increase is broader gate-prep
  pressure, not a single grade.
- Level shares of tutoring: bar primary .426, lower .209, upper .220, tertiary .145; quota primary
  .445, lower .267, upper .211, tertiary .078 → quota reallocates prep from tertiary to
  lower/primary.
- Who buys prep: bar [q1 .068, q2 .164, q3 .239, q4 .308, q5 .405]; quota [.235,.457,.518,.537,
  .578]. Tutoring is pro-rich in both, but quota raises participation at every quintile (largest at
  q2 +.29) and slightly compresses the q5−q1 gap (.337→.344).
- Tutoring is **not** a major determinant of attainment in this prototype (η² ≈ 0 for completion;
  gates and affordability dominate).

### 3.8 Push-out decomposition — engine limitation, stated

The prototype tried to split exits into liquidity vs choice vs never-started by wealth quintile and
rural/urban. The engine's final state records **no liquidity exits** in these configurations: the
`reason` code is overwritten for children who stop after a liquidity exit (engine code path in
`core.step`), so the decomposition reads 0/0/0 and is **not usable**. We therefore report
gate screening directly: lower completion by quintile (.174→.966 under bar; .121→.767 under quota)
and wealth parity/wealth gaps above. Fixing the engine's exit-reason bookkeeping would be needed
before any "who is pushed out by liquidity vs choice" statement; we did not modify the engine.

### 3.9 PHL coupling attempt (construct-limited, not calibration)

Committed PHL UIS/WDI lower-secondary completion (`lsc`): 1990 64.8 %, 1998 65.6 %, 2004 77.3 %,
2014 76.1 %, 2022 97.4 %, 2024 84.8 % (series in `phl_lsc.json`). Simulated lower completion across
the multiverse: **mean .635, 90 % range [.550, .833]**. The simulated distribution overlaps the
earlier observed PHL range but not the latest points; because the engine's completion is a toy
share, `lsc` is a reconstruct/model-based series, and the engine has no migration/sorting/fees data,
this is **a level check on one variable, not a calibration or validation**.

---

## 4. What is not identifiable

Pre-declared rule: an axis is not distinguished by an outcome when variant 5–95 % ranges overlap
≥80 %. Result (selected):
- **Supply/funding vs attainment: not identified** (overlap 1.00 for primary/lower/upper; .? for
  tertiary) — fixed budget and fiscal loop produce indistinguishable attainment in this design.
- **Learning configuration vs attainment**: not identified for primary (overlap 1.00); matters for
  `mpl_primary` (η² .61) but not for completion levels.
- **q_pub**: affordability, learning, gates, rural not identified (supply/jobs do move it).
- **Tutoring rate/gate mass**: affordability, supply, learning, jobs not identified; only gates
  move it strongly.
- **Formal share/edu_gdp**: supply/gates/rural not identified; jobs dominates.
- **Liquidity vs choice exits: not identifiable** in this engine version (bookkeeping issue above). **Withdrawn 25 Nov:** it was the driver read bug, not the engine (see correction above and `4679ddb` §3.8).
- More fundamentally (task-41): **household demand/affordability, learning grade profiles, exam/quota
  rules, migration flows and credential requirements are not identified by available public data**;
  any target for them here would be invented.

## 5. What is observed vs assumed (short form)

Observed/usable today: UIS/EdStats enrolment, completion and PTR; ILO-UCW children-in-employment
(construct-correct: employment, not labour); GGDC/PWT+E6 structural-change/employment shares
(post-1990 demand limitation); DHS API aggregates (ecological only); WDI GDP/growth; Barro-Lee
attainment (reconstructed). Assumed here: demand/affordability parameters (forgone-earnings profile,
borrowing, need shape), learning production and grade profile, gate rules/seat shares, credential
floors/skill premium, rural costs, private/tutoring supply; none is calibrated to a country.

## 6. Cost, files, hashes

- 1,440 runs, 304.1 s at 12 workers on the shared 15-core-quota server; no Mac compute; no jobs left
  of ours; server remains up (not shut down).
- `results_multiverse.json` sha256 **`004173aa…`**; `summary_multiverse.json` sha256 **`549958e2…`**;
  driver **`932fc973…`**; `run_multiverse.log`, `run_meta.txt`, `phl_lsc.json` committed.
- Pre-registration committed before code/runs: `PRE_REGISTRATION_masseng_edsystem.md`.
- Branch `research/masseng-edsystem-2026-11-25`.