# REGRESSION_INVENTORY — the massification programme's statistical-relation artefacts

**Audit date:** 2026-11-20 · **Auditor:** evidence auditor (subagent) · **Base:** `experiments/massification-2026-11-20`
**Write scope:** `10_massification/extensions/audit_2026-11-20/a_regressions/` only. **No experiment was run, no claim changed.**
**Machine-readable companion:** [`REGRESSION_INVENTORY.csv`](REGRESSION_INVENTORY.csv) — 85 rows, one per artefact, with full sha256.

---

## 0. What was done, and what was not

**Done.** Every `.md` note and every `data/*.csv` in `10_massification/relations/`; every result CSV and note in `09_relations/`
(including `scripts/` to establish data inputs); the E1–E10, X1–X15, Y1–Y5 batteries (FINDINGS + result CSVs, not re-run); the
`04_data`/`data` series the relation files actually cite; and the two model-layer scaling files that supply the A1/A3 targets.
Files were opened read-only, hashed, and their numbers checked against the narrative that quotes them.

**Not done (deliberately).** Nothing was re-estimated. Where a published number could not be reproduced from the file it claims to
come from, I recorded the discrepancy and recomputed **only** the arithmetic that a file's own components imply (flagged as
"auditor recomputation" below). No model was run; no CSV was edited; no claim was reworded in place.

**Vocabulary.** `status`: **observed** (measured series), **derived** (computed/fitted from observed series), **check** (a robustness
or verification statistic), **modelled** (simulated or model-generated). `evidence_role`: **load-bearing** (a closed-phase verdict
quotes or depends on it), **descriptive-only**, **DATA BLOCKED**, **superseded**.

## 1. Counts

| | n |
|---|---|
| Artefacts inventoried | **85** |
| by status | derived **62**, observed **14**, check **6**, modelled **3** |
| by role | descriptive-only **57**, load-bearing **22**, DATA BLOCKED **4**, superseded **2** |
| by group | relations layer A01–A21 (21), `09_relations` B01–B27 (27), cited inputs C01–C07 (7), lab batteries D01–D30 (30) |
| files cited that do not exist at the documented path | **1** (the GMR observed series — see FLAG-01) |
| empty/unreadable files | **1** (`relations/logs_e6.txt`, 0 bytes) |

---

## 2. The data spine, and the one break that matters

Every universalization artefact in the programme sits on the same spine:

```
data/gmr_observed_6countries_1970_2024.csv   (4,635 rows, 6 countries, 32 indicators, 1970-2026)   <- observed
        +-> universalization_fits.csv, common_shape*.csv, e6_*.csv, UNIVERSALIZATION_TIMING.csv
        +-> event_windows.csv, capacity_alignment.csv, capacity_crosscountry.csv
        +-> 09_relations/event_windows_gmr.csv, Y4_AUDIT.csv
09_relations/data/panel_wdi_wide.csv          (1,950 rows x 65 cols, 30 countries, 1970-2024)     <- observed
        +-> scaling_laws.csv, push_pull_tests.csv, state_capacity.csv, panel_results.csv,
            panel_heterogeneity.csv, complexity_*, eci_*, literacy_*, E1/E5/E10, X1-X9, Y1-Y3
10_massification/data/UNIVERSALIZATION_SERIES.csv (2,458 rows) + JOBS_AND_MARKETS_PANEL.csv (5,622)
        +-> timing layer, E1/E6/E7/E8, X3, Y3, Y4, Y5
```

**The GMR file is real and its numbers verify.** Spot-checked against the A6/D77 signature: PHL primary completion 83.16 (1999) →
87.45 (2013) → **91.92 (2017)** → 98.30 (2024); lower-secondary 88.44 (2023) → **92.41 (2024)**; upper-secondary 76.43 (2017 peak) →
75.03 (2024), never ≥90; tertiary GER 47.41 (2024) → **51.07 (2025)**; primary NER 96.79 (1976). The closed phase's observed
signature is **confirmed from source** (`data/gmr_observed_6countries_1970_2024.csv`).

---

## 3. Group A — `10_massification/relations/`

| id | path (under `10_massification/relations/`) | estimates | status | role |
|---|---|---|---|---|
| A01 | `data/UNIVERSALIZATION_TIMING.csv` | crossing years + bands + censoring, 63 rows | derived | **load-bearing** |
| A02 | `data/universalization_timing_summary.md` | human-readable A01, 30 rows | derived | **load-bearing** |
| A03 | `data/UNIVERSALIZATION_TIMING_PATTERN.csv` | ordering/spacing per country, 6 rows | derived | descriptive |
| A04 | `data/universalization_fits.csv` | 634 logistic/Gompertz fits, 194 series, 68 identified | derived | **load-bearing** |
| A05 | `data/universalization_fits_supplement.csv` | in-school (100−OOS) curves, 13 rows | derived | descriptive |
| A06 | `data/universalization_common_shape.csv` | common-slope F, 4 indicators | check | descriptive |
| A07 | `data/universalization_common_shape_bootstrap.csv` | residual bootstrap p | check | descriptive |
| A08 | `data/universalization_common_shape_jackknife.csv` | leave-one-country-out F | check | descriptive |
| A09 | `data/universalization_refit_verification.csv` | provenance re-fit, 5 rows | check | descriptive |
| A10 | `data/e6_shape_comparison.csv` | 4 functional forms × 12 series, holdout | check | **load-bearing** |
| A11 | `data/e6_timing_comparison.csv` | predicted vs observed crossing, 36 rows | check | **load-bearing** |
| A12 | `data/scaling_laws.csv` | 15 relations × within/between exponents | derived | **load-bearing** |
| A13 | `data/push_pull_tests.csv` | 13 Granger-style panel tests, EQUIVALENT-labelled | derived | **load-bearing** |
| A14 | `data/event_windows.csv` | 20 policy events, 7 computed / 3 inferred / 10 UNABLE | derived | **load-bearing** |
| A15 | `data/capacity_alignment.csv` | capacity before/at/after each crossing, 24 rows | derived | **load-bearing** |
| A16 | `data/capacity_crosscountry.csv` | Spearman capacity vs crossing year, 4 rows × n=5 | derived | **load-bearing** |
| A17 | `data/capacity_leadlag.csv` | 5-year-difference correlations, 12 rows | derived | descriptive |
| A18 | `data/state_capacity.csv` | 1,182 country-years, declared-weight composite | derived | **load-bearing** |
| A19 | `SCALING_NOTES.md` | method + caveats + constraint list | derived | descriptive |
| A20 | `EVENT_WINDOWS.md` | 20 event narrative, PHL/HKG/CHN verdicts | derived | **load-bearing** |
| A21 | `CAPACITY_LAYER.md` | index construction + PHL alignment + model gate | derived | **load-bearing** |

### A01 / A02 — the crossing vector (load-bearing, sound, one rendering defect)
The A6/D77 observed signature is in A01 and reproduces from source. Two problems, both cosmetic-to-moderate:
- A02's `flags` column renders as the literal string `<Flags(allows_duplicate_labels=True)>` (a pandas repr leaked into the markdown), so
  the flags are unreadable in the one file a reader is most likely to open.
- A02 prints `not_crossed_by_last_obs` rows as `2024–?` / `2023–?`, which reads like proximity. PHL upper-secondary ≥90 is **75.03** in
  2024 and KHM upper-secondary is **27.87** (2023): these are not near-crossings, and the notation should not imply they are.

### A04 — 634 fits, 68 identified (load-bearing as a check reference)
PHL secondary GER K=92.3 (se 2.4), r=0.0525 (0.0051), t0=1971.9 (0.9), R²=0.96; KOR secondary NER r=0.1414; CHN tertiary
K=125.6, r=0.1267, t0=2020.1, R²=0.995. The file is honest about non-identification (320 rows `not_identified`). One structural
ambiguity: **246 of 634 rows carry NaN `fit_status`** because only full-sample rows were classified, so a naive groupby on
`fit_status` silently drops the entire 1980–2010 fit sample. Negative R² values (e.g. −2.86, −2.31) are printed for series that are
already at ceiling — correct, but a reader who filters on `r2 > 0.9` will keep the wrong rows.

### A06 / A07 / A08 — the "no common shape" claim is not supportable as written
Three files, three answers, all on the same four-to-six nonlinear fits:

| file | secondary GER | tertiary GER | verdict it prints |
|---|---|---|---|
| A06 asymptotic F | F=4.210, p=0.0030 | F=60.941, p<0.001 | reject |
| A07 bootstrap (reps=**3** / **24**) | p_bootstrap=1.000 | p_bootstrap=0.125 | **not** rejected |
| A08 jackknife | F_all=**0.236**, p=0.9178 | F_all=**0.303**, p=0.9110 | **not** robust |

A08's `F_all` is 18× (secondary) and 200× (tertiary) smaller than A06's F **on the same data**, so it is not a jackknife of A06 —
the restricted-fit routine differs. A07 has 3 and 24 replications (script default 50) and one row with `boot_reps=0` "bootstrap
failed"; a p of 1.000 on 3 reps carries no information. Net: the only defensible statement is **"no rejection is established"**, and
A19's "rejection is provisional" is still too strong. Nothing downstream depends on this (the model was not asked to share a slope),
so it is a labelling problem, not a verdict problem.

### A12 / A13 — scaling laws and push-pull (load-bearing; A13's hypothesis labels are inverted)
A12 gives secondary GER←GDPpc **0.090 (0.124) ns within / 0.215 (0.035) between**; tertiary **0.848 (0.172) / 0.567 (0.082)**;
lower-sec completion 0.247/0.169; primary completion←TFR −0.189/−0.122; ag share −0.120 ns/−0.990.

**A13 is the most serious labelling defect in the regression layer** (FLAG-00). `push_pull.py` calls `granger(df, y, x)` where the
model is `y_t ~ own lags + x lags`, and the tuple supplies `y = dependent`, `x = driver`. So the estimated model runs from
**driver → dependent**, and the CSV's `dependent`/`driver` columns are correct — but the `hypothesis` text says the *opposite*,
and every row is consistently reversed. Correctly oriented, the file says:

| in the file | actually estimated | result |
|---|---|---|
| P1 "GDP-pc growth → secondary-GER growth" | **secondary GER → GDP-pc** | F=1.727, p=0.125 (null) |
| P2 "GDP-pc growth → tertiary-GER growth" | **tertiary GER → GDP-pc** | F=0.648, p=0.663 (null) |
| P3 "GDP-pc growth → completion growth" | **completion → GDP-pc** | F=1.516, p=0.181 (null) |
| P5 "tertiary-GER growth → GDP-pc growth" | **GDP-pc → tertiary GER** | **F=6.522, p<0.001, sum +0.205** |
| P6 "completion growth → GDP-pc growth" | **GDP-pc → completion** | F=3.514, p=0.004, sum **−0.667** |
| P9 "wage-share growth → secondary-GER growth" | **secondary GER → wage share** | **F=4.108, p=0.001, sum +0.050** |
| P10 "secondary-GER growth → wage-share change" | wage share → secondary GER | F=1.881, p=0.094 |

`SCALING_NOTES.md` §3 and `MASSIFICATION_CLOSEOUT.md` §2/§3 quote the **labels**, so their push-pull sentence is reversed on both
halves: the reported "income-pull is not supported" actually refers to the education→growth direction (which *is* null), and the
strongest relation in the file — **income growth → tertiary enrolment, F=6.52, p<0.001** — is the one the note calls
"tertiary-GER → GDP growth, consistent with either ordering". The "education→growth −0.667" constraint is really
**income→completion −0.667**. The saved conclusion is unaffected (A13 still cannot identify direction, and the EQUIVALENT label and
`direction_claim = none` are correct), but **any use of these numbers as moments must use the corrected orientation**, and the
phase's descriptive push-pull sentence should be re-stated.

The inconsistency: A12's between-exponents (0.215 / 0.567) are **not** the exponents the A1 gate used (0.286 / 0.776, from
`model2/runs/scaling_estimates.csv` C02). Two "between" estimates for the same pair, same panel, differ by a third. The generated
model exponents are **wrong-signed** (−2.73…−0.39), so the FAIL is robust to which target is used — but the *magnitude* criterion is
not a single object, and the A3 "range" (+0.090…+0.215) is just A12's within and between columns.

### A14 / A20 — event windows (load-bearing for the descriptive mechanism verdict, D51)
Of 20 rows, **7 computed, 3 inferred, 10 UNABLE**. Of the 7 computed, only two are significant: HKG 2009 free senior secondary
**+9.08 pp (se 1.75, t=5.20)** and CHN 1999 HE expansion **+4.70 (0.59, t=7.94)**. PHL: 2018 free tuition **−5.39 (1.80, t=−3.00)**,
K-12 composition **+0.42 (0.83, t=0.50)**, 1987 Constitution **−0.22 (1.54, t=−0.15)**, 4Ps **−2.49 (1.96, t=−1.27)**. The
"state pushes do not align" verdict rests on these four PHL nulls plus the 31-year gap — defensible as descriptive, and correctly
capped by R24/R25, but it is a **null-with-naive-SE** result, not a measured absence. Note also that the same PHL 2018 event is
−5.39 pp here, **−8.40 %** in `09_relations/data/event_windows.csv`, and **−28.87 %** in `event_windows_gmr.csv`: three
estimates of one event, differing by a factor of 3.4, driven by data source and transform (see FLAG-06).

### A15 / A16 / A21 — the capacity layer: the two headline numbers do not reproduce
This is the most consequential finding in the audit.

**(i) The cross-country "null" is not in the data.** A21 §3, STATUS §3o and `MASSIFICATION_CLOSEOUT.md` §2 all report *"Spearman
+0.15 / +0.10 / +0.41 / +0.30, all ns, n=5"*. **Those four numbers appear in no file on disk.** A16 contains:

| level | rho | p |
|---|---|---|
| primary universal | **+0.872** | 0.054 |
| lower-secondary universal | **+0.900** | **0.037** |
| upper-secondary mass | +0.103 | 0.870 |
| tertiary mass | **+0.800** | 0.104 |

Recomputed by me from `state_capacity.csv` + `UNIVERSALIZATION_TIMING.csv` using A16's own documented pipeline: identical
(+0.872/+0.900/+0.103/+0.800). So the file is internally consistent and the **narrative is not**. Moreover the result is a
one-country artefact: Japan enters at `capacity_within` **20.0** against 46.5–61.1 for the other four (its within-country
normalisation is distorted by a 0.30 coverage collapse), and it dominates a 5-point rank correlation. Neither "+0.15, all ns"
nor "+0.90, p=0.037" can carry the sentence *"capacity does not predict crossing timing"*.

**(ii) The PHL "+35.2 points into the crossing" does not reproduce.** A15 reports pre-window 49.5 → 84.7 at the crossing,
change **+35.2**, at `crossing_year_used = 2019`. From A18, the 5-year pre-window mean (2014–18) is **57.2** and 2019 is **83.4** →
**+26.1**; at the A4 first-crossing year **2017** the values are **42.9 → 57.4 (+14.4)**; on the panel-comparable `capacity_index`
the change is **+3.7** (2019) or **+14.1** (2017) — not +35.2 on any reading. Two further problems the note half-acknowledges:
`weight_coverage` falls 1.00 (2005) → 0.90 (2017) → 0.60 (2019–23), so the 2019 value is a differently-composed index; and
`capacity_within` at 2017 is **57.4**, i.e. *below* its 2005 value (58.9), so "capacity rose into the crossing" is true only if the
crossing is dated 2019–21 rather than 2017.

**(iii) The alignment table has empty rows.** KHM (4 rows) and JPN primary/lower/upper carry no capacity values but still carry the
note "censored: uses upper-bound year". A table that prints a censoring note on a row with no data invites the reader to assume a
computed result.

Consequence for the Council: the **A9/A10 "capacity is a floor precondition, not a ceiling driver"** reading rests on (i) the PHL
within-path narrative, which is the +35.2 that does not reproduce, and (ii) a cross-country test whose reported null is not on disk.
The *descriptive* facts survive and are checkable — PHL primary PTR fell 35.1 (2005) → 29.1 (2017), education spending rose
2.33 → 3.96 %GDP, and upper-secondary stayed at 75.0 despite all of it (a genuine counterexample to a *pure* capacity driver in the
sense that capacity rose while the ceiling did not move). But **every quantitative capacity claim in the phase headline needs
re-derivation before reuse.**

### A17 — capacity lead-lag (descriptive; not identified)
12 correlations of 5-year changes, r = −0.719 (KHM lower-sec, n=17) to +0.530 (HKG primary, n=13). No SE, no p, signs flip across
countries at the same lag. It is labelled descriptive in the CSV, but the `reading` column ("capacity change LEADS completion
change") reads as a directional result. It is not one: it is a within-country correlation on 8–19 overlapping 5-year differences.

---

## 4. Group B — `09_relations/`

| id | path (under `09_relations/`) | estimates | status | role |
|---|---|---|---|---|
| B01 | `RELATION_CANDIDATES.csv` | 49 graded relations R01–R49 | derived | **load-bearing** |
| B02 | `data/panel_results.csv` | 66 two-way-FE / FD coefficients, 30 specs | derived | **load-bearing** |
| B03 | `data/panel_heterogeneity.csv` | 110 split-sample coefficients | derived | descriptive |
| B04 | `data/country_typology.csv` | 30 country baselines + split thresholds | observed | descriptive |
| B05 | `data/event_windows.csv` | 6 WDI ITS estimates | derived | descriptive |
| B06 | `data/event_windows_gmr.csv` | 5 GMR ITS estimates | derived | descriptive |
| B07 | `data/shadow_gradients.csv` | 17 observed shadow-education gradients | observed | descriptive |
| B08 | `data/complexity_results.csv` | 14 ECI relations C1–C12 | derived | descriptive |
| B09 | `data/complexity_conditioning.csv` | 14 interaction cells X1–X8 | derived | descriptive |
| B10 | `data/complexity_metric_choice.csv` | ECI variant comparison | derived | descriptive |
| B11 | `data/eci_growth_crosssection.csv` | ECI growth premium, 5 rows | derived | descriptive |
| B12 | `data/eci_literacy_results.csv` | 17 ECI × literacy × GDP tests | derived | descriptive |
| B13 | `data/literacy_cohort_decomposition.csv` | 241 country-periods, entrant/exit decomposition | derived | descriptive |
| B14 | `data/literacy_decomposition_regressions.csv` | 3 rows behind the replacement share | derived | descriptive |
| B15 | `data/literacy_country_examples.csv` | 10 illustrative country rows | derived | descriptive |
| B16 | `data/population_pyramids.csv` | 3-band pyramid + derived 15–24 proxy | observed | descriptive |
| B17 | `data/economic_complexity_panel.csv` | 180 × 27 model-input ECI panel | observed | descriptive |
| B18 | `data/economic_complexity_panel_30ctys.csv` | 895-row 30-country ECI set | observed | descriptive |
| B19 | `data/panel_wdi_wide.csv` | 30-country × 65-col observed panel | observed | **load-bearing** |
| B20 | `data/panel_wdi_long.csv` | 63,570-row long panel | observed | **load-bearing** |
| B21 | `data/panel_wdi_eci.csv` | panel joined to ECI | observed | descriptive |
| B22 | `DATA_PATTERNS.md` | narrative of B02–B07 | derived | **load-bearing** |
| B23 | `COUNTRY_TYPOLOGY.md` | T1–T6 conditional relations | derived | descriptive |
| B24 | `LITERACY_ECI_DEMOGRAPHY.md` | 17 tests + cohort decomposition | derived | descriptive |
| B25 | `LITERATURE_ELASTICITIES.md` | verified literature priors | observed | **DATA BLOCKED** |
| B26 | `MODEL_PLUG_MAP.md` | relation → parameter map | derived | descriptive |
| B27 | `STATUS.md` | completeness claims | derived | descriptive |

### B02 — the two sign constraints the model is judged on (load-bearing, verifies)
Tertiary GER←GDPpc **0.848 (0.172)**; GDP growth←tertiary GER (t−15) **−1.035 (0.240)**; fertility→primary completion
**−0.189 (0.044)**, holding in every split; spending→secondary 0.152 (0.110) ns with FD 0.014. The PTR row is a genuine sign
conflict (**+0.385 levels vs −1.243 first differences**) and the file says so — it is correctly excluded from parameters.

### B05 / B06 / B22 — event windows: three magnitudes for one event
PHL 2018 free tuition: **−8.40 %** (B05, WDI), **−28.87 %** (B06, GMR), **−5.39 pp** (A14, levels). Same event, same design family,
different data and transform. Each is separately defensible; the programme should quote one and say which. B22 also claims
**"19 event-window estimates"** while the two files hold **6 + 5 = 11** rows.

### B07 — shadow-education gradients (observed, descriptive)
HKG gate gradient 35.1 → 46.6 → 70.3 % (**+35.2 pp**, one survey, 6 schools, n=630); KOR income elasticity **1.325** (183 vs 671
thousand won); KOR participation falls 86.0 → 66.4 % while spend rises 398 → 491; JPN Tokyo 57.9 vs Akita 22.1 % (2.62×); KHM
60.5 vs 26.4 % (one district, six schools); CHN 29.8 % (2014) → **<20 %** (2022, newspaper headline, LOW). These are calibration
priors, not estimates — the file's own `note` column says so.

### B12 / B13 / B24 — the honest addendum
ECI tracks the schooling **flow** (completion t−10 **0.593**, se 0.176) but not the adult-literacy **stock** (**0.001**, se 0.005);
literacy does not track GDP within country (**3.91**, se 2.67, ns); the published ECI growth premium does not replicate
(**−0.068**, se 0.067); **62–66 %** of observed adult-literacy gains is cohort replacement. This is the best-executed block in
`09_relations` — it reports its own failures, bounds the exit component instead of estimating it, and explains the negative
residuals as series revision.

### B25 / B01 — what is imported rather than estimated
The register has exactly one plausibly-causal relation (R07 fertility→completion, structural timing) and one **imported** causal
target (R28, 9.0 licensed nurses per additional nurse migrant, Abarcar & Theoharides). R28 is not re-estimated here, and its
replication design (E3, PH nurse visa) is DATA BLOCKED — no PRC/CHED nursing series on disk. R30 (school construction) is
**UNVERIFIED at source** (Duflo 2001 not retrieved). B25 correctly names its gaps rather than filling them: spending→enrolment,
school construction, teacher supply and returns→tutoring have **no verified estimate**.

---

## 5. Group C — cited inputs

| id | path | what it is | status | role |
|---|---|---|---|---|
| C01 | `data/gmr_observed_6countries_1970_2024.csv` | 4,635-row observed UIS/GMR panel, 6 countries, 32 indicators | observed | **load-bearing** |
| C02 | `10_massification/model2/runs/scaling_estimates.csv` | 91 rows, 5 estimators × 10 relations (source of A1 targets) | modelled | **load-bearing** |
| C03 | `10_massification/data/UNIVERSALIZATION_TIMING.csv` | 128-row timing layer (data-hunter) | observed | **load-bearing** |
| C04 | `10_massification/relations/logs_fit.txt` | console log of the common-shape run | derived | superseded |
| C05 | `10_massification/relations/logs_e6.txt` | **empty (0 bytes)** | — | superseded |
| C06 | `10_massification/data/UNIVERSALIZATION_SERIES.csv` | 2,458-row series file | observed | **load-bearing** |
| C07 | `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` | 5,622-row jobs/markets panel | observed | descriptive |

**C03 is the second timing layer, with the same filename as A01 and different content.** A01 (scout, 63 rows, completion/NER,
first-*sustained*) and C03 (data-hunter, 128 rows, GER/NER, first-*at-above*) disagree on the central milestones because they use
different measures and different crossing definitions:

| milestone | A01 (completion/ner) | C03 (ger/ner) |
|---|---|---|
| PHL primary ≥95 | **2017–2021** (completion) | **1971** GER (left-censored), **1976** NER (left-censored) |
| PHL lower-secondary ≥90 | **2023–2024** (completion) | **2014** GER (band 2009–2014) |
| CHN lower-secondary ≥90 | **2014–2016** (completion) | **2006** GER |
| PHL tertiary ≥50 | 2024–2025 | **2025** (agree) |

Both are internally valid; A4 predeclared *which measure* applies to each milestone (M1 NER/GER, M2/M3 completion, M4 GER), so the
mapping was not retrofitted. But nothing on disk disambiguates the two identically-named files, and the consequence is large:
**PHL primary GER was ≥95 in every observed year from 1971 to 2017** (99.54 in 1971; 106.47 in 1990; 103.41 in 2015;
99.37 in 2017) and fell below 95 only in 2018–2024, after K-12 changed the cohort structure (min 88.83 in 2021, 94.03 in 2024).
So "primary universalization in 2017" is a statement about *cohort completion*, not access — and the headline "the 1987 mandate
preceded universal primary by 31 years" contrasts a **completion** crossing with a **participation** law, while participation on the
GER measure had been above the 95 line for 47 years, including the whole period before the law. A6 itself keeps these separate
(M1 primary NER≥95 is reported left-censored at ≤1976/77; the 2017 date is the *completion* ≥90 milestone, F1). The observed
signature is therefore correct; it is the *narrative* that collapses two milestones into one and reads a participation law against a
completion outcome. C03's own notes also record that its reconstructed CHN GER differs from
observed GER by a **median 15.28 pp** — too large to call a validated reconstruction.

---

## 6. Group D — the descriptive batteries (E, X, Y)

Read from FINDINGS/RESULTS and per-experiment CSVs; **not re-run**. Per-experiment detail is in the CSV (D01–D30).

### D01–D10 — battery E (`lab_2026-11-20`)

| id | exp | key estimate | verdict as printed | role |
|---|---|---|---|---|
| D01 | E1 | within slope **+56.07** GER pp/log GDP (se 19.56, n=93, **5 clusters**) | "strong" | descriptive |
| D02 | E2 | max fraction of crossings inside GDP IQR **0.60** (rule 4/6) | not typical | descriptive |
| D03 | E3 | Gini~MYS **−0.055** (1960–64) → **−0.051** (1990–94); 17/17 regions | equalizing | descriptive |
| D04 | E4 | duration ratio 1.10; volatility ratio 0.326 | no clear / smoother | descriptive |
| D05 | E5 | services slope **−0.495** (0.217) but **+1.82** without log GDP | not robust | descriptive |
| D06 | E6 | completion×wage-share r **+0.586** at lag 5 (n=39, 4 systems) | association | descriptive |
| D07 | E7 | delivery Δ **−0.15 SD**, only dimension with coverage | DATA LIMITED | **DATA BLOCKED** |
| D08 | E8 | dPTR on dGER **+0.245** (0.185) | no strain | descriptive |
| D09 | E9 | remittances: −0.046 / −0.0007 / −0.0024, all ns | no association | descriptive |
| D10 | E10 | 30-country slope **+14.74** (CI −1.56…+31.04) vs E1 +56.07 | **does not replicate** | descriptive |

**Label problem:** E1 is printed as "**strong** (≥3 pp per log point)" on 5 clusters, and its own predeclared replication (E10) fails.
"Strong" should read "large and not transferable; driven by CHN/KHM". E10 is the most valuable cell in the battery because it is the
internal falsifier, and the FINDINGS do say so — but the verdict column does not.

### D11–D25 — battery B (`lab_2026-11-20_b`)

Verdicts as predeclared: SUPPORTED 4 (X3, X10, X11, X12), PARTIAL 1 (X9), NOT SUPPORTED 5 (X1, X2, X4, X7, X8), DATA LIMITED 1 (X5),
UNABLE 1 (X6), SIMULATED-THRESHOLD-MISSED 3 (X13–X15), plus 3 Amendment-B1 PARTIALs. Verdict counts match `RESULTS.csv` (18 rows).

- **X3 "queue depth"** is the only absorption cell that "survives", and it is near-mechanical: numerator = lagged attainment stock,
  denominator = wage share (Council relabelled it derived/mechanical). Its +0.366 (CI 0.198…0.534) is real arithmetic, not a queue.
- **X1/X2** are both nulls with CIs spanning zero; the "opposite sign" reading rests on point estimates.
- **X7** prints NOT SUPPORTED but its within CI spans 57 log points (−34.14…+22.86) — uninformative, not evidence of no size effect.
- **X8** has **one** usable duration pair (CHN 13.0 y vs HKG 19.5 y → 0.667, HKG *slower*), with HKG volatility inflated by a series break.
- **X13–X15** are simulated toys; the predeclared run produced an all-censored artefact from a contractive recursion (r=0.08<1), disclosed
  as a Lead predeclaration defect and answered by post-hoc Amendment B1 under unchanged thresholds. Evidential weight zero (D88).
  `rho = 1.000` on four finite cells is a mechanical monotone, not an estimate.

### D26–D30 — battery C (`lab_2026-11-20_c`)

- **Y1** ceiling residual: income-partial rho(ceiling, agri) **−0.105**; rho(ceiling, youth-unemp) **+0.246**; raw −0.718 absorbed by income →
  opportunity-cost account **discarded** under the predeclared rule. The 6-system check points the other way (−0.714) and is left as a
  disclosed tension — correct.
- **Y2** max |partial r| **0.208** (n=700, 30 countries), **0/24** cells reach 0.25, reverse direction −0.057…+0.090 → not detectable. This is
  the cleanest demonstration in the programme that the visible schooling–market co-movement (zero-order 0.49–0.71) is shared trend.
- **Y3** floor rho **+0.50** (n=5), ceiling rho **+0.60** (n=6) → not separable; leave-one-out swings 0.0–0.8 / 0.3–0.9 and both conditions hold
  only when dropping JPN. Correctly reported as not separable — this is the honest weak link in the A10 "floor not ceiling" ruling.
- **Y4** null-model scoring: upper-secondary null year 2011.5 from **one** dated crossing (HKG), 4 false crossings, 2 evidence-backed →
  DISTINGUISHED. **Measure mismatch:** the two evidence-backed values quoted (CHN **79.39**, PHL **66.05**) are observed **GER** finals,
  while the threshold is **completion** ≥90; on completion CHN is **87.52** and PHL **75.03**. The conclusion survives, the cited numbers
  are the wrong series.
- **Y5** data audit: 6/6 D75 inputs present for CHN and HKG (12/12 rows), 0 new asks. Design-only; records that CHN per-student spending has
  3 observations and CHN education spending 5 — thin inputs behind "complete".

---

## 7. Integrity register

| # | severity | artefact | finding | what changes |
|---|---|---|---|---|
| **FLAG-00** | **high** | A13, A19 §3, CLOSEOUT §2/§3 | `push_pull_tests.csv`'s `hypothesis` text is the **reverse** of the model actually estimated (`push_pull.py` regresses `dependent` on lagged `driver`). The note and the closeout quote the labels, so "income-pull not supported" is really the education→growth null, and the file's strongest result (**GDP growth → tertiary GER, F=6.52, p<0.001**) is reported as the reverse. | The no-direction verdict stands (R13), but the descriptive push-pull sentence must be restated and every moment re-oriented. |
| **FLAG-01** | high | C01 vs all scripts/notes | Every relation script and note cites `04_data/data/gmr_observed_6countries_1970_2024.csv`; **that path does not exist** (the file is at `data/gmr_observed_...`). As written, A04–A11, A14, A18, B06, C03 and the timing layer cannot be regenerated. | Reproduction requires a one-line path fix; the numbers themselves verify. |
| **FLAG-02** | **high** | A16 vs A21/STATUS/CLOSEOUT | The cross-country capacity correlations quoted in the phase headline (+0.15/+0.10/+0.41/+0.30, "all ns") **appear in no file**. A16 holds +0.872 (p=.054), +0.900 (p=.037), +0.103, +0.800. | "Capacity does not predict crossing timing" is unsupported as written; the replacement number is itself a one-country artefact (JPN at 20.0). |
| **FLAG-03** | **high** | A15 vs A18 | The PHL "+35.2 points into the primary crossing" does not reproduce: +26.1 at 2019, **+14.4** at the 2017 crossing year, +3.7/+14.1 on the panel-comparable index. | The descriptive "capacity lines up with the crossing" claim weakens substantially and depends on dating the crossing 2019–21. |
| **FLAG-04** | medium | A06/A07/A08 | Three common-shape files return three verdicts; A08's F_all (0.236/0.303) cannot be a jackknife of A06's F (4.21/60.94); A07 has 3 and 24 reps (one row 0). | "No common shape" is not established; report "not established" and drop the rejection language. |
| **FLAG-05** | medium | A01 vs C03 | Two identically-named timing files (63 vs 128 rows) place PHL primary at **2017** vs **1971/1976**, PHL lower-sec at **2024** vs **2014**, CHN lower-sec at **2014–2016** vs **2006** — different measures *and* different crossing definitions, undisclosed at the point of use. | The "31-year lag behind the 1987 Constitution" compares a **completion** crossing with a **participation** law, while primary GER was ≥95 from 1971 to 2017. The observed signature stands (M1 is already left-censored); the *interpretation* is measure-dependent. |
| **FLAG-06** | medium | B05/B06/A14 | One event (PHL 2018 free tuition) has three estimates: −8.40 %, −28.87 %, −5.39 pp. | Quote one, name the source; the sign is robust, the size is not. |
| **FLAG-07** | medium | B22, B27 | "19 event-window estimates" claimed; 11 rows exist (6 + 5). "Every CSV is regenerable" is false as written (FLAG-01). | Completeness claims in the 09 layer overstate by 8 rows and by one broken path. |
| **FLAG-08** | medium | D01 | E1 labelled "strong" on **5 clusters**, with its own replication (E10) failing (+14.7, CI −1.6…+31.0). | The label overstates; E1 should be quoted only with E10. |
| **FLAG-09** | low-medium | A02 | `flags` column renders `<Flags(allows_duplicate_labels=True)>`; `not_crossed_by_last_obs` printed as `2024–?` although the level is 75.03 (PHL) / 27.87 (KHM). | Cosmetic but misleading; fix the rendering. |
| **FLAG-10** | low-medium | A04 | 246/634 rows have NaN `fit_status`; 320 rows `not_identified`. | Any filter on `fit_status` silently drops the 1980–2010 sample. |
| **FLAG-11** | low | D29 | Y4 cites GER finals (CHN 79.39, PHL 66.05) as evidence about a **completion** ≥90 threshold (actual 87.52 / 75.03). | Conclusion unchanged; cited series wrong. |
| **FLAG-12** | low | C05 | `relations/logs_e6.txt` is **0 bytes** — the E6 run has no console evidence on disk. | Recorded as empty, not inferred. |
| **FLAG-13** | low | A20 §6 | Says `SCHOOL_EXPANSION.csv` "was not on disk"; it now exists (27 rows) and is PHL-only. | Superseded in part; the expansion-episode caveat (quality C, not event evidence) still stands. |

**Deliberate non-flags.** The `EQUIVALENT` labelling in A13, the `not_identified` handling in A04/A05, the bounded exit component in
B13, the `DATA LIMITED`/`UNABLE` verdicts in D07/D15/D16, the disclosed Amendment B1, and the `simulated` labels in D23–D25 are all
**correctly and honestly labelled**. The programme's practice of writing its own falsifiers into the result files is unusually good;
the failures above are mostly at the *narrative* layer, where numbers were carried forward from earlier drafts.

---

## 8. What could not be verified

1. **Regeneration.** No artefact was re-run (per instructions) and the broken path (FLAG-01) means most could not be re-run without edits.
2. **`10_massification/lit/UNIVERSALIZATION_TIMING.md`** — a third timing narrative exists; **not read** in this pass, so no claim about it.
3. **Policy dates.** `POLICY_TIMELINE.csv` rows are labelled "fact (not re-verified this pass)" by their own author; no primary legal source was retrieved. Every event-window result inherits this.
4. **Shadow-education sources.** B07's HKG/KOR/JPN/KHM values are single surveys cited to tables I did not retrieve.
5. **Capacity index weights.** `state_capacity.csv` weight sensitivity (0.973/0.955/0.896) is asserted in A21; I did not recompute the alternative weightings.
6. **The A1 anchor outputs** (`model/anchor_out/`) are model results, outside this regression scope, and were not audited.

---

## 9. Files inspected (all hashed in the CSV)

**`10_massification/relations/`** — `SCALING_NOTES.md`, `EVENT_WINDOWS.md`, `CAPACITY_LAYER.md`, `logs_fit.txt`, `logs_e6.txt`;
`data/`: `UNIVERSALIZATION_TIMING.csv`, `UNIVERSALIZATION_TIMING_PATTERN.csv`, `universalization_timing_summary.md`,
`universalization_fits.csv`, `universalization_fits_supplement.csv`, `universalization_common_shape.csv`,
`universalization_common_shape_bootstrap.csv`, `universalization_common_shape_jackknife.csv`,
`universalization_refit_verification.csv`, `e6_shape_comparison.csv`, `e6_timing_comparison.csv`, `scaling_laws.csv`,
`push_pull_tests.csv`, `event_windows.csv`, `capacity_alignment.csv`, `capacity_crosscountry.csv`, `capacity_leadlag.csv`,
`state_capacity.csv`; `scripts/`: `fit_universalization.py`, `e6_shape_bootstrap.py`, `bootstrap_common_shape_fast.py`,
`jackknife_common_shape.py`, `oos_curves_and_verify.py`, `refit_from_datahunter.py`, `scaling_laws.py`, `push_pull.py`,
`event_windows.py`, `state_capacity.py`, `universalization_timing.py`, `universalization_timing_v2.py`.

**`09_relations/`** — `RELATION_CANDIDATES.csv`, `STATUS.md`, `DATA_PATTERNS.md`, `COUNTRY_TYPOLOGY.md`,
`LITERACY_ECI_DEMOGRAPHY.md`, `LITERATURE_ELASTICITIES.md`, `MODEL_PLUG_MAP.md`; `data/`: `panel_results.csv`,
`panel_heterogeneity.csv`, `country_typology.csv`, `event_windows.csv`, `event_windows_gmr.csv`, `shadow_gradients.csv`,
`complexity_results.csv`, `complexity_conditioning.csv`, `complexity_metric_choice.csv`, `eci_growth_crosssection.csv`,
`eci_literacy_results.csv`, `literacy_cohort_decomposition.csv`, `literacy_decomposition_regressions.csv`,
`literacy_country_examples.csv`, `population_pyramids.csv`, `economic_complexity_panel.csv`,
`economic_complexity_panel_30ctys.csv`, `panel_wdi_wide.csv`, `panel_wdi_long.csv`, `panel_wdi_eci.csv`; `scripts/` (to
establish inputs): `analyze_panel.py`, `analyze_hetero_events.py`, `analyze_events_gmr.py`, `analyze_complexity.py`,
`analyze_literacy_eci.py`, `build_panel.py`, `panel_lib.py`.

**Extensions** — `lab_2026-11-20/FINDINGS.md`, `results/SUMMARY.csv`, `results/E1–E10_*.csv`; `lab_2026-11-20_b/FINDINGS.md`,
`RESULTS.csv`, `cluster_*/results/*.csv`; `lab_2026-11-20_c/FINDINGS.md`, `RESULTS.csv`, `Y1–Y5/results/*.csv`.

**Inputs** — `data/gmr_observed_6countries_1970_2024.csv`, `10_massification/data/UNIVERSALIZATION_SERIES.csv`,
`JOBS_AND_MARKETS_PANEL.csv`, `UNIVERSALIZATION_TIMING.csv`, `STATE_CAPACITY.csv`, `SCHOOL_EXPANSION.csv`,
`POLICY_TIMELINE.csv`, `BASELINE_SERIES.csv`, `10_massification/model2/runs/scaling_estimates.csv`,
`scaling_classification.csv`.

**Context (for the verdict, not inventoried)** — `MASSIFICATION_CLOSEOUT.md`, `10_massification/STATUS.md`.
