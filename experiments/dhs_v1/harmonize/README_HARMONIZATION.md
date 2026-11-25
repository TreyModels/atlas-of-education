# DHS harmonization — verified adapters, availability matrix, aggregate layer (data-team deliverable)

Owner: data team (`engine-tutoring`) · worktree `/Users/treymenefee/neon-boot/wt5/dhs8` · branch
`research/dhs-eight-experiments-2026-11-25`. Binding schema/engine: `experiments/dhs_v1/README.md` +
`experiments.R` (untested by the attachment author; no validation claim is made for that script).
**Raw restricted microdata stays local (`~/neon-boot/pulled/dhs`, 2.8 GB) and the row-level normalized files stay
local (`~/neon-boot/dhs-normalized`); only non-disclosive metadata/aggregates are committed here.**
R for validation: `/Users/treymenefee/neon-boot/r-env/bin/Rscript` — R 4.5.3, `survey` 4.5 (recorded in every
validate run). Python: `/Users/treymenefee/neon-boot/venv/bin/python` (pandas 2.3.3, pyreadstat 1.3.8).

## 1. Dedupe inventory (reuse; do not rebuild)

| prior artifact | path @ branch/commit | what it is | verdict |
|---|---|---|---|
| KH PR ingest + attendance aggregates | `wt3/dhs/research/cambodia-dhs/` (ingest_cambodia_dhs.py, REPORT.md, results/attendance_*.csv) @ `2d651e5`, branch `research/cambodia-dhs-2026-11-25` | KH PR attendance by age/sex/residence/region; benchmarked KH 2021-22 NAR | **REUSE** — reference recodes + benchmark; our KH numbers reproduce theirs (74.7 / 73.2 / 76.1) |
| ID/DH quintile attendance profile | `wt3/iddhs/research/id-dhs/quintile_profile.py` @ `206bbde`, branch `research/id-dhs-2026-11-25` | ID PR attendance 14–17 by wealth | **REUSE** recode logic; our adapter supersedes the file-specific extract |
| PH/VN credential-floor extracts | `wt3/{phdhs,vndhs}/research/{ph-dhs,vn-dhs}/` @ `206bbde` | bottom-40 share of non-attenders etc. | **REUSE** as prior descriptive choices; not re-run here |
| DHS IR pipeline + acquisition record | `wt2/dhs` @ `fc9b7f7` (AMENDMENT_03, EXECUTION_READY, target inventory) | metadata/targets only, no microdata | **REUSE** metadata; its IR variable list matches our verified recodes |
| DHS API ecological panel + corrected branch | `wt2/dhseco` @ `792dba1`, `research/dhs-api-ecological-2026-11-24` + `dhs-corrected-2026-11-25` | country-year PUBLIC DHS-API aggregates (`panel_edu2_*.csv`) | **REUSE** as the macro-link source (M6); ecological only, not causal |
| Bulge micro-DHS feasibility | `research/bulge-micro-dhs-2026-11-25` @ `230521b` | DHS fertility target inventory; bulge NOT-ESTIMABLE | **REUSE** as absent-data ledger; do not cite as estimation |
| eight-experiment starter | `experiments/dhs_v1/` (this worktree) | README + experiments.R + attachment | **USE** (binding, untested) |
| `research/dhs-eco-gfr-uncomputed` claims | archive branch | GFR never estimated / retracted | **DUPLICATE-DO-NOT-USE** |

No prior artifact contains the E1–E8 design. No branch/worktree was modified.

## 2. Verified raw-data inventory (non-disclosive metadata; full detail in `availability_matrix.csv`)

Local recodes found (DTA and SAS7BDAT): ID PR 1991/1994/1997/2002-03/2007/2012/2017 + HH 1987; KH PR+IR
2000/2005/2010/2014/2021-22 (**SAS only**); PH PR 1993/1998/2003/2008/2013/2017/2022 + IR 2022; VN PR
1997/2002/2005ais. **Correction to the preliminary matrix:** the `WI` files (`IDWI3A`, `PHWI31/3A`, `VNWI31/41`)
are **wealth-index files** (`whhid`, `wlthindf`, `wlthind5`), **not woman recodes** — so E4/E5/E7/E8 exist only
for **KH (5 waves) + PH 2022**, not for ID/VN/PH-1993/98. `catalog.json` records per-file path, sha256, bytes,
format, rows; `adapter_manifest.json` records input sha256, rows, weight variable and per-column non-missing counts.

## 3. Harmonization rules (documented; verified per wave)

* **Weights (never mixed):** PR/person rows use the household weight `hv005/1e6`; woman recode rows use the
  individual-woman weight `v005/1e6`. `record_type` says which design applies.
* **Design:** real `stratum = hv022` (PR) / `v022` (IR) and `psu = hv021` / `v021`, written as strings; PSU is
  unique *within* stratum by construction (repeated (stratum,psu) rows are repeated persons, which is expected).
* **Attendance / current school (E1–E3, E6):** `hv110` ("member still in school", 1=yes/0=no/9=DK) is the
  unambiguous household-schedule item where present and is preferred. Where `hv110` is absent, `hv121` is used
  with the **empirically verified per-wave coding**: recodes where code 1 appears use `hv121==1` as current;
  recodes with codes {0,2} use `hv121==2` as current ("attended at some time" code is then 0/absent). Evidence
  table is in `value_codes.json` + `availability_matrix.csv`; e.g. ID 2017: `hv110==1` count equals `hv121==2`
  count exactly (48,423) and the 10–14 age profile is 96 % current, so `hv121==2` is current attendance there.
  Missing/not-asked → **NA**, never "no". PH 2008 and PH 2013 have `hv121` labelled "na - …" and no `hv110` in
  the recode → **attendance BLOCKED** for those waves.
* **`school_years`:** `hv108` (PR) / `v133` (IR), 0–25 accepted; 97=inconsistent, 98=DK, other → NA.
  Education groups for E4–E8 are the README/experiments.R bands: `0-5`, `6-11`, `12+`.
* **`wealth`:** `hv270` (PR) / `v190` (IR), values 1–5; anything else → NA.
* **`children_ever_born`:** `v201` (0–25; 0 is a genuine zero).
* **`age_first_birth`:** `v212` (IR); **`age_first_union`:** `v511` (IR) — note the common confusion: `v525` is
  age at first *sex*, not union; `v511` is age at first union/cohabitation. Numeric ages only; 96/97/98 special
  codes and 0 → NA; a **99 is treated as known-never only where the codebook defines it as never**, otherwise NA.
  `early_birth = age_first_birth<20`, `early_union = age_first_union<20` (NA preserved).
* **`household_size`:** `hv009` (PR) / `v136` (IR), 1–60.
* **E6 (binding decision D-01):** the woman recodes have **no current-school attendance item** — verified from
  the codebooks/FRQ/DCT: `v716`/`v717` are occupation, `v731` is employment status, no school-attendance
  variable exists. E6 is therefore built from **PR person rows, females aged 20–24, `currently_in_school =
  hv121/hv110`, person weight `hv005`** and is labelled `person_sex2` (a documented deviation from the
  `record_type='woman'` spec; no IR sensitivity extract is possible).

## 4. Verified E1–E8 availability (country × wave; full CSV `availability_E1_E8.csv`)

| country | waves | E1 (attendance × wealth) | E2 (× residence) | E3 (× sex) | E4–E8 (women) |
|---|---|---|---|---|---|
| KH | 2000 | BLOCKED (wealth absent) | FEASIBLE | FEASIBLE | **FEASIBLE all 5 waves** (true IR) |
| KH | 2005/2010/2014/2021-22 | **FEASIBLE (5 groups)** | FEASIBLE | FEASIBLE | FEASIBLE |
| ID | 1991/1994/1997 | BLOCKED (wealth absent) | FEASIBLE | FEASIBLE | BLOCKED (no woman recode) |
| ID | 2002-03/2007/2012/2017 | **FEASIBLE (5 groups)** | FEASIBLE | FEASIBLE | BLOCKED (no woman recode) |
| PH | 1993/1998 | BLOCKED (wealth absent) | FEASIBLE | FEASIBLE | BLOCKED (WI is wealth index) |
| PH | 2003 | **FEASIBLE (5 groups)** | FEASIBLE | FEASIBLE | BLOCKED |
| PH | 2008/2013 | BLOCKED (attendance "na" in PR) | BLOCKED | BLOCKED | BLOCKED (2013 PR) |
| PH | 2017/2022 | **FEASIBLE (5 groups)** | FEASIBLE | FEASIBLE | PH **2022 IR only** |
| VN | 1997/2002 | BLOCKED (wealth absent) | FEASIBLE | FEASIBLE | BLOCKED (WI is wealth index) |
| VN | 2005ais | **FEASIBLE (5 groups)** | FEASIBLE | FEASIBLE | BLOCKED |

All cells carry n (unweighted complete) and design summaries in `coverage_missingness.csv`; aggregate estimates
(incl. suppressed cells) are in `aggregate_layer.csv`. E4–E8 samples: KH 2000–2021-22 (n ≈ 3.2k–4.3k per wave
per outcome/domain) and PH 2022 (n ≈ 3.1k–4.0k); no other country has a woman recode.

## 5. Aggregate layer + macro join manifest

`aggregate_layer.py` reproduces the eight experiments.R domains E1–E8 as design-based domain means with
Taylor-linearized stratified-cluster SEs (full-design PSU universe, matching `survey::svymean` on a subset
design). Suppression rule: `n_complete >= 50` **and** ≥2 PSUs and ≥2 strata with >1 PSU; otherwise the estimate is
suppressed (n reported). Outputs: `aggregate_layer.csv` (252 estimates), `coverage_missingness.csv` (176 cells),
`join_manifest.json` (country-year keys; **subnational-year links are BLOCKED** because DHS regions/clusters are
survey-specific and GPS is displaced; macro candidates = public DHS-API `panel_edu2_*.csv` (M6) and the declared
but not-local M1/M3 country-year matrices; timing/geography/permission rules recorded).

**R cross-validation** (KH 2021-22, E1 by wealth, `validate_adapter.R`): schema OK; R survey estimates
0.44662/0.51882/0.56701/0.56921/0.69647 vs Python 0.446623/0.518817/0.567012/0.569209/0.696468 (identical);
R SEs 0.017073/0.020578/0.019536/0.020865/0.027036 vs Python 0.017073/0.020578/0.019536/0.020865/0.027036
(identical after using the full-design PSU universe).

**Lonely/singleton strata audit** (data-team check; QA reported none): files with strata containing a single PSU:
`PH 2008` (19 singleton strata), `VN 1997` (1), `VN 2002` (1), `ID 2007` (1); all other 24 normalized files have
none. `experiments.R` sets `options(survey.lonely.psu='fail')`, so executing VN 1997/2002 E2/E3 (and any cell that
touches those strata) will stop until the design treatment is documented — flag to QA/execution; PH 2008 cells are
already BLOCKED for E1–E3. The aggregate variance uses the full-design PSU universe (so one-PSU strata contribute a zero variance term); the singleton counts above are the explicit audit record — they are not silently dropped.

## 6. Benchmark validation (registry v0.2 in `benchmark_registry_v0.2.csv`)

| id | country/wave | published (public report) | our matched estimate | verdict |
|---|---|---|---|---|
| B001 | KH 2021-22 | primary NAR 72.8 (FR377 Table 2.12) | 74.65 (ages 6–11 current attendance) | +1.85 pp within ±2.5 definitional tolerance |
| B002 | KH 2021-22 | primary NAR M 72.0 / F 73.5 | M 73.23 / F 76.14 | M +1.2 pp OK; F +2.64 pp slightly outside ±2.5 → report definitional gap (any-level vs attending-primary) |
| B003 | KH 2021-22 | secondary NAR 42.0 | 60.18 (ages 12–18 any current attendance) | **not matched** (level-specific vs any-level); direction only |
| B004 | KH 2021-22 | primary NAR urban 75.5 / rural 71.3 | urban 76.93 / rural 73.44 | +1.43/+2.14 pp within ±3.0 |
| B005–B008 | PH/ID/VN, E4–E8 | — | — | **PENDING**: no exact public final-report table value retrieved in this environment; must not substitute prior-run numbers |

Cross-check: our KH 2021-22 extract reproduces the prior validated extraction exactly (74.7; M 73.2 / F 76.1;
urban 79.7 / rural 73.5 in their any-current-year variant), which is independent evidence the adapter recodes are
consistent with the earlier verified pipeline. Public PDFs located: DHS Cambodia 2021-22 Final Report FR377
(nis.gov.kh PDF) and Philippines DHS 2022 Final Report FR381 (dhsprogram.com) — the PENDING rows name the exact
table types still needed.

## 7. Reproduce

```bash
PY=~/neon-boot/venv/bin/python; R=~/neon-boot/r-env/bin/Rscript
cd ~/neon-boot/wt5/dhs8/experiments/dhs_v1
$PY harmonize/inventory_dhs.py                    # metadata/hash inventory -> harmonize/_out/
$PY harmonize/build_normalized.py                 # normalized.csv per country/wave/record -> ~/neon-boot/dhs-normalized
$PY harmonize/aggregate_layer.py                  # aggregates/coverage/benchmarks/join manifest
$PY harmonize/make_availability_matrix.py         # verified E1-E8 matrix
$R  harmonize/validate_adapter.R ~/neon-boot/dhs-normalized/KH/normalized_KH_2021-22_person.csv E1 KH 2021-22
```

## 8. Limitations / open items

1. E4–E8 are limited to **KH (5 waves) + PH 2022** because the other "WI" files are wealth-index files, not
   woman recodes; no data were invented.
2. E6 is a **person-record** operationalisation (females 20–24, PR, person weight), not a woman-recode domain.
3. Public benchmark coverage is strong only for KH (4 comparisons); PH/ID/VN/E4–E8 rows stay PENDING rather than
   using unverifiable numbers.
4. Subnational linkage is BLOCKED (survey-specific regions, displaced GPS); country-year macro linkage uses
   public DHS-API panels and is descriptive/ecological, never causal.
5. Singleton-PSU strata exist in 4 normalized files (see §5) — execution/QA must document the design treatment.
6. `experiments.R` remains an untested starter; this lane only verified adapters/aggregates, not E1–E8 execution.
7. The normalized row-level files and raw microdata are **not** committed and never leave the Mac.
