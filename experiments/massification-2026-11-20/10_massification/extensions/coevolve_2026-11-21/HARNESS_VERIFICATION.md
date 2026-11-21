# HARNESS VERIFICATION — COEVOLUTION v0

**`SIMULATED`.** Independent verification of the delivered COEVOLUTION v0 artefacts. The harness
reads only the frozen contract (`PRE_DECLARATIONS.md`, sha256
`7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d`), `PARAMETERS.csv`, the simulator
source (read, not executed) and the delivered `results/` tables. **The simulator was not re-run.** No
parameter, threshold or seed was changed; no delivered file was modified (additions only).

- Harness code: `harness/code/` (`common.py`, `verify_a…f*.py`, `report_numbers.py`, `run_all.py`)
- Harness outputs: `harness/out/` (tables + `verification_results.json`), hashes in `harness/SHA256SUMS.txt`
- Reproduce: `"<python>" harness/code/run_all.py` (24.6 s, no model execution)
- Environment: Python 3.11.17, pandas 3.1.1, numpy 2.4.6 (only for reading; the verification itself is pure Python)
- Totals: **21 checks PASS, 0 FAIL, 11 descriptive** (`harness/out/verification_results.json`)

Every number below is either `SIMULATED` (model output) or `DERIVED` (arithmetic on `SIMULATED`
pupil records). No observed series is used, so no `OBSERVED` label appears.

---

## 1. Result summary

| # | Item | Check | Result |
|---|---|---|---|
| A1 | Report card A, algebra | 8,640 aggregate cells: NER = in-band/band, GER = all-ages/band, OOS = band − in-band − higher, denominators = band width × location cohort size, 0 ≤ NER ≤ 1, GER ≥ NER, counts bounded | **PASS** (0 violations; max round-trip error 4.8e-11) |
| A2 | Report card A, exact from pupils | 2,304 cohort-table values (5 completion-by-age shares, entered secondary, early leaving, mean years) recomputed from `panel_*.csv` | **PASS** (0 disagreements; max abs diff 3.3e-10) |
| A3 | Report card A, families | 180 family means and gains recomputed from `panel_*.csv` | **PASS** (0 disagreements; max abs diff 5.0e-10) |
| A4 | NER/GER per cell from pupil-years | 8,496 cells recomputed from the declared 1-in-32 sample | **PASS-CONSISTENCY** (r = 0.965, mean abs diff 0.039, 98.9 % within 3σ, 99.8 % within 4σ) — exactness **not testable** (see §7) |
| A5 | Enrolment totals | 720 year-totals: total enrolment vs 32 × sampled pupil-years | **PASS** (mean ratio 31.96, 0/720 outside 4σ) |
| A6 | Gate accounting | 9,840 gate values (admitted ≤ min(qualified, places), turned away = qualified − admitted, applicants ≥ qualified, declared place counts) + admission structure in 10,204 admitted pupils | **PASS** (0 disagreements) |
| B1 | Coexistence arithmetic | 6,480 values in `coexistence_*.csv` | **PASS** (0 violations) |
| B2 | Decisive test, cells | 288 district × cohort cells re-evaluated with the declared thresholds; verdict recomputed | **PASS** (0 verdict mismatches; COEXISTENT) |
| B3 | Early leaving from pupils | 288 cohort values vs `cohorts_*.csv` | **PASS** (max abs diff 5.0e-11) |
| C1–C4 | Counterfactual gains / argmax / correlations / verdict | 12 gain values, 3 correlations, rule re-applied | **PASS** (exact; SAME-RESPONSE re-derived) |
| D1–D3 | Spillback table and DiD | 12 rows reproduced; DiD recomputed under four control definitions | **PASS** (exact; NO-SPILLBACK under all four) |
| E1–E5 | Degrees-outrun-jobs mechanism | graduate share, implied rule, attainment, code path | **DEFECT-CONFIRMED** (`ARM-NOT-TESTING-GLUT`) |
| F1–F2 | Hashes | 62 manifest files + frozen predeclaration hash | **PASS** (0 mismatches) |
| F3 | `RUNS.json` metrics | 264 headline metrics recomputed from the tables | **PASS** (0 disagreements) |
| F4 | D0-INPUT-SEATS | verdict/stages/read audit | **PASS** (13 reads, all allowed) |
| F5 | Labels / suite shape | 51 CSVs labelled, no wall-clock, 24 runs, 17.93 s | **PASS** |
| F6 | Closed records | `git status` in the programme root | **PASS** (0 tracked files modified; only the two new untracked extension dirs) |
| F7 | Determinism | delivered evidence only | **ACCEPTED-EVIDENCE** (not re-run) |

---

## 2. Report card A (§7)

### 2.1 What is exactly verifiable, and what is not

`panel_*.csv` holds one row per pupil (14,400 per run = 12 scored cohorts × 1,200) but **no year-by-year
level**. `pupilyear_*.csv` is the **declared 1-in-32 sample** (`pupil_id % 32 == 0`) of
pupil-year rows, not the full table. Per-year NER/GER therefore **cannot be reproduced exactly** from
the delivered files; a pupil's path also contains real non-attending years (about 56 % of pupils have at
least one year between first entry and final exit with no enrolment), so completion years do not pin the
per-year path.

The harness consequently splits the check:

1. **exact** recomputation of everything that *is* a function of the pupil records (cohort completion,
   early leaving, entry, family means) — A2/A3;
2. **exact** algebra of every delivered aggregate cell — A1;
3. **statistical** recomputation of per-cell NER/GER from the sample — A4/A5.

### 2.2 Algebra (A1)

| identity | max error | cells |
|---|---|---|
| NER = enrolled_in_band / pop_official_band | 4.8e-11 | 8,640 |
| GER = enrolled_all_ages / pop_official_band | 4.8e-11 | 8,640 |
| out_of_school = pop − enrolled_in_band − at_higher_level | 0 | 8,640 |
| denominator = (band width) × 320 (town) or 880 (rural), counting only cohorts that exist | 0 | 8,640 |
| 0 ≤ NER ≤ 1; GER ≥ NER; counts bounded | 0 | 8,640 |

`NER ≤ 100 by construction` holds in every cell. **No cell was capped**: `repeaters` (max 937) and
`over_age` (max 797) are carried alongside. `GER` reaches only **0.9068** — the declared property
"GER may exceed 100" is structurally allowed but **never exercised in v0** (see D-9).

### 2.3 Exact recomputation (A2/A3)

| item | values | max abs diff | tolerance | disagreements |
|---|---|---|---|---|
| completion by declared age (5 levels) | 1,440 | 3.3e-10 | 5e-9 | 0 |
| entered secondary / early leaving / mean years | 864 | 3.3e-10 | 5e-9 | 0 |
| family means + gains vs baseline | 180 | 5.0e-10 | 5e-9 | 0 |

The residual 1e-10 is the declared `%.10g` write format, not a computational difference.

### 2.4 NER/GER from the 1-in-32 sample (A4/A5)

| statistic | value |
|---|---|
| cells compared | 8,496 |
| Pearson r (sample vs delivered NER) | 0.9646 |
| mean absolute difference | 0.0387 |
| mean z / sd z | 0.155 / 0.928 |
| within 3σ / 4σ | 98.9 % / 99.8 % |
| worst cell | year 9, tertiary, town: delivered 0.0113, sample 0.100 (n = 50, 5 sampled pupils) |
| total-enrolment ratio (per year, 720 values) | mean 31.96, range 25.6–39.9, 0 outside 4σ |

**Verdict: consistent with the declared sampling design, not an exact reproduction.** The sample is
too small for exact town cells (10 sampled pupils per cohort) and for the sparse tertiary/selective
levels; that is a limit of the delivered files, not evidence of an error in the aggregates. The
aggregates' own algebra (§2.2) and the exact pupil-record items (§2.3) are clean.

### 2.5 Baseline portrait (3-seed mean)

| item | value |
|---|---|
| cohort completion, primary | 0.5409 |
| cohort completion, lower secondary | 0.2130 |
| cohort completion, upper secondary | 0.1150 |
| cohort completion, tertiary | 0.0043 |
| mean years completed | 5.091 |
| entered lower secondary | 0.257 (derived: `A_transitions_derived.csv`) |
| early leaving (entered lower secondary, did not complete it) | 0.1715 |

Rural–urban (baseline, by declared age):

| item | town | village |
|---|---|---|
| primary completion by 14 | 0.572 | 0.426 |
| lower secondary by 18 | 0.345 | 0.158 |
| upper secondary by 20 | 0.240 | 0.069 |
| tertiary by 26 | 0.013 | 0.001 |
| mean years completed | 6.321 | 4.644 |

Tertiary GER uses the declared five-year band **18–22** immediately after the official secondary
leaving age 17 (`PARAMETERS.csv: age_band_tertiary`), verified. Post-secondary non-tertiary is a
**separate level row** (`post_secondary_non_tertiary`, band 18–19), verified.

### 2.6 Report-card-A definitional findings (recorded, not rescued)

- **D-7 upper secondary is split into two reporting levels.** The model tabulates `upper_secondary`
  and `upper_selective` as separate levels with the same 16–17 band and **no combined row**, although
  §3/§7 name one upper-secondary level with the elite track as a track of it. Magnitude in v0 is small
  (selective = 1.3 % of the upper-secondary NER on average), but the combined NER is not delivered.
- **D-8 "out-of-school" is "out of level L"**, as the declaration literally defines it: a 12-year-old
  still in primary is counted out of school for lower secondary. In the sample, **7.8 %** of the
  lower-secondary OOS count is children still enrolled in primary. The column must not be read as the
  conventional UIS out-of-school rate.
- **D-9 GER > 100 untested.** Maximum GER is 0.9068 (primary). The model never reaches universal
  enrolment, so the "may exceed 100" clause and the repeater-driven inflation it is meant to display
  are never exercised.
- **D-10 truncated age bands.** 624 of 8,640 cells (26 per run) are at the edge of the cohort frame
  (entries −11…23): at t = 0 no child is 18–22, at t = 1 only 18-year-olds exist, and at t = 29 no
  child is 6–11. Ratios there are computed on a partial band (definitionally correct, not comparable to
  later years). `ner_primary_final_year` in `RUNS.json` is `NaN` for this reason.
- **D-11 two different "selective applicant" counts.** Criterion (c) uses the gate-log
  `selective_applicants`; criterion (d)'s household share divides by the tutoring-log
  `lower_final_applicants`. In year 0 of the baseline these are 128 and 152. Both are delivered
  columns, but the same words denote different populations.

---

## 3. The decisive test (§8.2)

### 3.1 Four criteria, declared thresholds

| criterion | declared threshold | baseline cells passing (of 36) | mean of cell values (min–max) |
|---|---|---|---|
| (a) unused accessible ordinary places | ≥ 10 % of offers | 36 | 0.268 (0.251–0.284) |
| (b) early leaving | ≥ 5 % of secondary entrants | 36 | 0.172 (0.126–0.227) |
| (c) qualified applicants per selective place, turned away > 0 | ≥ 1.20 | 36 | 6.06 (4.89–7.00) |
| (d) gate hours per applicant ≥ 2 × catch-up hours per non-selective pupil | ≥ 2.0 | 36 | 5.01 (1.71–28.98) |
| (d) gate-tutoring households ≥ 20 % of selective applicants | ≥ 0.20 | **32** | 0.224 (0.121–0.287) |

All four hold **simultaneously** in **32 of 36** baseline district × cohort cells:
**12/12** for seed 20261121, **10/12** for 20261122 and **10/12** for 20261123. The four failures are
criterion (d)'s household-share leg only (0.121–0.194); the hours-ratio leg passes in every cell.
The declared rule is "at least one cell", so the recomputed verdict is **`COEXISTENT`** — but the
"12/12 cells" phrasing is true only for the primary seed. Note also that the mean household share
(0.203 per-year mean; 0.224 cell mean) sits just above its 0.20 threshold: this leg is **marginal**.

All 288 cells across the 8 arms × 3 seeds were re-evaluated; 175 have all four. The two arms that fail
globally do so on different criteria: `MANDATE-BEFORE-FUNDING` on (b) (early leaving 0.029–0.033, below
5 %) and `SPILLBACK` on (d) (household share ≈ 0.11).

### 3.2 What has two peaks — named, and the three objects kept apart

| object | measurement | two peaks? |
|---|---|---|
| **Years completed** | baseline distribution: **0 years 29.5 %** and **6 years 28.5 %** are the two dominant modes; secondary modes at 10 (9.2 %) and 12 (5.3 %) | **YES — this is the two-peaked object** |
| **Tutoring expenditure** | 95.7 % of pupils buy **zero** gate hours; buyers buy fixed doses of 60 (1,172 pupils) or 120 (665) hours. Catch-up: 43.8 % zero, doses 24/48/72 hours | No — zero-inflated with discrete doses |
| **Applications per selective place** | rises from 3.23 (t = 0) to ≈ 6.5 (t = 18) and then plateaus (5.8–6.3); one prominent local maximum at t = 18 | No — a rise and a plateau, not two peaks |

So the result reports **two peaks in years completed** (a mass that completes nothing and a mass that
completes exactly primary), and **not** two peaks in tutoring expenditure or in applications per place.
These are separate claims and are not combined into a single "bimodality" verdict.

---

## 4. The three one-change counterfactuals (§8.3)

Recomputed from `families_*.csv` alone (seed means of mean years completed, 4 declared family types):

| arm | town nonpoor | town poor | village nonpoor | village poor | argmax | argmax / best other positive |
|---|---|---|---|---|---|---|
| TRAVEL-CUT | +0.0470 | −0.1056 | +0.0571 | +0.1095 | **village poor** | 1.92 |
| ORDINARY-EXPANSION | +0.0720 | −0.0981 | +0.0857 | +0.1827 | **village poor** | 2.13 |
| SELECTIVE-EXPANSION | +0.0208 | +0.0049 | −0.0210 | +0.0301 | **village poor** | 1.44 |

- **Argmax is the same in all three arms → criterion (i) fails.**
- Pairwise correlations: travel vs ordinary **0.9907**, travel vs selective 0.2610, ordinary vs
  selective 0.3334 → the **0.95 correlation falsifier fires**.
- The ratio sub-criterion (ii) is reading-dependent: under the implementation's conservative reading
  (compare only with *positive* other gains) SELECTIVE-EXPANSION fails at 1.44 < 1.5; under the literal
  text (*some* other type, including a negative one) all three pass. The verdict is unaffected because
  (i) and the correlation clause each independently force `SAME-RESPONSE`.
- **Robustness:** per seed, the argmax is *not stable* — travel_cut gives village nonpoor / town poor /
  village poor across the three seeds. The gains are ~0.03–0.18 years, i.e. of the same order as
  seed-to-seed variation. This strengthens, not weakens, the reported failure.

**Verdict `SAME-RESPONSE` correctly applied.** Correction to the core summary's wording: the argmax is
**village *poor*** (`("village", 1)`), not village nonpoor; the gain vectors and the 0.991 correlation
are confirmed exactly.

---

## 5. Spillback (§9)

Delivered table reproduced exactly (12 rows, 0 disagreements). DiD recomputed under four control
definitions, all in pp:

| seed | treated village | delivered control | pure villages | excluding treated only | vs baseline arm |
|---|---|---|---|---|---|
| 20261121 | v5 | +5.14 | +6.40 | +5.59 | +3.93 |
| 20261122 | v5 | +0.66 | +1.02 | +0.72 | +1.77 |
| 20261123 | v8 | −6.39 | −6.88 | −6.74 | −6.15 |
| seeds clearing 5 pp | | **1/3** | 1/3 | 1/3 | **0/3** |

**`NO-SPILLBACK` confirmed**, and it is robust: the declared criterion requires **every** paired seed to
clear 5 pp, and the mean is −0.20 pp. Under the literal §9 wording ("relative to the
control-cohort-adjusted baseline", i.e. against the baseline arm) even seed 1 falls to +3.93 pp.

Two implementation defects were found and are recorded, not corrected:

- **D-5 control-group construction.** `_spillback_from_panel` selects controls with
  `panel["village"] != treated_village`, comparing labels `"v5"` / `"town"` with the integer `5`. The
  condition is therefore true for every row: the delivered "control villages" are **the whole district
  including the treated village and the town** (n = 8,400 = 7 cohorts × 1,200, and 6,000 = 5 × 1,200).
  This dilutes the contrast by ≈ 8 % and does not flip the verdict; the pure-village
  recomputation is the one quoted above.
- **D-6 the SPILLBACK arm is not a one-change arm.** It opens one experimental class in the treated
  village at t = 8 **and** switches response (b) on for the whole district. Primary persistence in
  non-treated villages rises from ≈ 0.50–0.52 (baseline) to ≈ 0.59–0.62 (spillback) in both cohort
  groups — a district-wide change, not a one-village treatment. The DiD nets most of that out, so what
  it identifies is the *incremental* effect of one extra class given response (b) on, not the effect of
  "a class with everything else as baseline" as §9 specifies.

---

## 6. DEGREES-OUTRUN-JOBS — design defect `ARM-NOT-TESTING-GLUT`

Measured from the delivered pupil records (years 22–29 are the only years in which the whole 18–22
band lies inside the scored cohort frame):

| item | value |
|---|---|
| declared anchor `g0` | **0.20** |
| model's own graduate share (cred ≥ 3, ages 18–22) | **0.1108–0.1146** |
| arm's rescaled argument `used = g0 + 2(share − g0)` | 0.031–0.048 |
| implied requirement `req = 3 + 0.8(used − g0)` | **2.865–2.879** (baseline 3.0) |
| implied return `1 − 0.45(used − g0)` | **1.068–1.076** (baseline 1.0) |
| attainment change vs baseline | upper secondary +0.0087, tertiary +0.0010, mean years +0.0608 |

Because the model's share never reaches the anchor, `(share − g0)` is negative throughout; the declared
rule therefore **lowers** the employer requirement and **raises** the return as graduates accumulate —
the opposite of a glut. Doubling the deviation pushes the requirement further down. In addition the
requirement move is **inert** (`req` stays inside (2, 3] and credentials are integers, so the
credential-access step mapping is unchanged); the only live channel is the ≈ 7 % uniform credential
premium. The delivered attainment responses are consistent with that premium, not with a glut.

Two further implementation facts: the "doubling" is applied to the argument of the employer rule, not
to any graduate-supply process (the only use of `degrees_double` in the source is `_employer_rule`), and
response (c) is switched on from t = −11 for the whole run, not at the declared year 8. The arm is
therefore a credential-premium arm, and **its result must not be read as evidence about degrees
outrunning jobs**. What a predeclared v0.1 would have to change is listed in
`harness/out/E_summary.json` (`v0_1_requirements`): an anchor taken from the model's own steady state
(or a declared external constant with a sensitivity range), an explicit supply instrument, a
pre-declared expected sign for `req_t`/`return_t`, a pre-outcome manipulation check, and separation of
the response switch from the supply shock. None of that is done here — it is a requirement for a future
frozen predeclaration, not a change to this one.

---

## 7. Verification limits (stated, not hidden)

1. **No full pupil-year table was delivered** (only the declared 1-in-32 sample), so per-cell NER/GER
   are verified statistically (A4), not exactly. A future delivery should include the full pupil-year
   table or a per-year × level × location enrolment count table.
2. **Determinism was not re-run.** `DETERMINISM.json` reports 5 byte-identical artefacts for seed
   20261121, but the two `_det_*` directories are not delivered, so the harness accepts the evidence
   rather than re-deriving it.
3. **The simulator was not executed**, so the D0 source audit is accepted from `D0_CHECK.json` plus a
   read of the source; no independent AST audit was performed by the harness.
4. **`RUNS.json` contains 24 `NaN` literals** (e.g. `ner_primary_final_year`), which is not strict
   RFC-8259 JSON; Python and pandas accept it, other parsers may not.

---

## 8. Defect register (all recorded, none repaired)

| id | what | where it bites | severity |
|---|---|---|---|
| D-1 | `SAME-RESPONSE`: same argmax family type, correlation 0.991 ≥ 0.95 | §8.3 falsifier — reported as a failure | falsifier triggered |
| D-2 | `NO-SPILLBACK`: 1/3 seeds ≥ 5 pp, mean −0.20 pp | §9 falsifier — reported as a failure | falsifier triggered |
| D-3 | `ARM-NOT-TESTING-GLUT`: g0 = 0.20 above the model's own 0.11 share, deviation doubling lowers `req`, raises return | §8.4 degrees arm is not a glut test | design defect |
| D-4 | selective track almost empty: 371–391 admissions per seed over 12 cohorts but only 41–71 pupil-years at the selective level (≈ 6 % of the 38 places × 30 years on offer); 330–370 of the admitted complete upper secondary elsewhere | criterion (c) measures a gate queue whose places are then declined; "competition for a few prestigious places" is not what the model produces | interpretation defect |
| D-5 | spillback control group compares a string label with an integer, so controls = whole district | DiD diluted ≈ 8 %; verdict unchanged | implementation defect |
| D-6 | SPILLBACK arm switches response (b) on district-wide as well as opening one class | DiD identifies a marginal class effect, not §9's one-change contrast | design defect |
| D-7 | upper secondary reported as two levels, no combined row | report card A level taxonomy | reporting defect, small in v0 |
| D-8 | "out-of-school" means "out of level L" (7.8 % of lower-secondary OOS is children in primary) | report card A interpretation | definitional |
| D-9 | GER never exceeds 100 (max 0.907) | the GER > 100 clause is untested | coverage gap |
| D-10 | 624 cells on truncated age bands at the frame edges | early-year tertiary/post-secondary ratios; `NaN` headline metric | reporting artifact |
| D-11 | two different "selective applicant" denominators in criteria (c) and (d) | decisive-test reproducibility | definitional |
| D-12 | `RUNS.json` NaN literals; requirement channel of the degrees arm inert (step function) | downstream parsing; degrees arm interpretation | minor |

---

## 9. Integrity (F)

| item | result |
|---|---|
| frozen predeclaration sha256 | `7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d` — unchanged |
| 62 manifest file hashes (contract, parameters, code, results) | all match |
| `RUNS.json` headline metrics recomputed from tables (264 values) | 0 disagreements |
| D0-INPUT-SEATS | `PASS`, all stages ok, 13 source reads all allowed (no observed data) |
| labels | 51/51 CSVs start `SIMULATED`; 0 date/time strings in results |
| suite shape | 8 arms × 3 seeds = 24 runs, 17.93 s of a 120 s limit |
| closed 2026-11-20 records | `git status`: 0 modified tracked files; only `bridge_tasks_2026-11-21/` and `coevolve_2026-11-21/` untracked |
| determinism | accepted from `DETERMINISM.json` (5 artefacts, seed 20261121), not re-run |
