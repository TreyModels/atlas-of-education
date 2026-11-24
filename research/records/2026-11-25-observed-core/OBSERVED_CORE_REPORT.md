# OBSERVED-CORE FULL-SYSTEM MODEL — report (task-42)

**Branch:** `research/observed-core-2026-11-25` (from `origin/research/full-system-data-2026-11-25` @ `34fd7c9`).
**Record:** `research/records/2026-11-25-observed-core/`.
**Status:** observational reduced-form model, run and evaluated. **No causal claims.** Everything labelled
"association" is an association. Pre-registration `1f438c6`, Amendments 01–04 (`050198c`, `7d08105`, `55cd2fa`,
`302cb43`) were committed before the full run; the code and data hashes are in `results/RUN_LOG.txt`.

**Headline.** The observed core can be built honestly from public data and it reproduces the broad
cross-country development–schooling gradient, but it is **not a validated forecaster**: under genuine
out-of-period (future-year) splits it never beats simply carrying forward the last observed value
(0% of cells), and its 5-year cross-country gains are small (3–6% lower RMSE than persistence, only for
primary GER, primary completion and primary PTR). The binding gap remains the one task-41 identified:
there is no public household demand/affordability data, so the demand block is declared, not estimated.

---

## 1. What is observed and what is assumed

| block | status here | evidence |
|---|---|---|
| **State/school supply** | **observed proxies**: pupil–teacher ratios (primary, lower secondary), teacher counts, education spending (% GDP and per student), private-enrolment share | 17 WDI/EdStats series, 1970–2023, up to 213 countries, no imputation |
| **Attainment/transitions** | **observed proxies**: gross enrolment ratios, primary completion, lower-secondary completion | completion is EdStats model-based, not exam pass; GER can exceed 100 |
| **Macro / structural change** | **observed**: GDP per capita, urban share, agriculture employment share, population | ILO agriculture share is *modelled*; urban share is a level, not migration |
| **Household demand / affordability** | **declared assumption, not fitted** | child-employment series (the only public demand-margin proxy) covers 100 countries, 1994–2016, 281 country-year values — the "full" demand specification is **not estimable** (0 cells) |
| **Learning / quality** | **not modelled, not fitted** | no comparable annual grade-level learning series; assessment anchors not used |
| **Gates / admissions** | **not modelled, not fitted** | completion/transition are proxies, cannot separate capacity rationing from exam screening |
| **Jobs / credentials** | **not modelled, not fitted** | wage premia are not returns; no credential-requirement series |
| **Migration** | **not modelled, not fitted** | urban share only; no rural–urban flows |
| **Borrowing / forgone earnings** | **not modelled, not fitted** | no household credit or fee data |

This matches the task-41 data map: only macro and supply blocks can be used without inventing a target. No
parameter in this record is estimated for learning, gates, jobs, migration or borrowing, and no observed
target is manufactured for them.

## 2. Data (OBSERVED tier; retrieval provenance)

- Source: public World Bank API (`api.worldbank.org/v2`), retrieved by `scripts/fetch_wdi.py`; retrieval
  timestamp, per-indicator API URL, raw-download `sha256` and tidy-file `sha256` are in `data/MANIFEST.json`.
- 17 series, 1970–2023, aggregates excluded (World Bank `region != "Aggregates"`); 94,506 country-year-value
  rows, 218 country codes with any data.
- Coverage (countries / years): primary GER 209 / 1970–2023; secondary GER 208; primary completion 198;
  lower-secondary completion 197; primary PTR 206 / 1970–2019; lower-secondary PTR 180 / 1981–2019;
  primary teachers 208; education spending % GDP 203; per-student primary 172 / **1995–2018**; per-student
  secondary 167 / 1995–2018; private primary share 206; private secondary share 196 / 1998–2023;
  children in employment 100 / 1994–2016; agriculture employment 187 / 1991–2023; urban share 217;
  GDP pc 213; population 217.
- **No imputation, no interpolation, no back-casting.** Missing cells reduce the estimation sample row-wise
  and are counted. Eleven series stop before 2023 (PTR to 2019, per-student spending to 2018), which is why
  the 2011–2023 time block is thinner than it looks.

Construct caveats carried from task-41 and repeated wherever a result is read: GER ≠ net attendance ≠
completion; completion is model-based, not exam pass; PTR is a headcount ratio, not effective teacher supply;
children in employment ≠ child labour; urban share ≠ migration; wage premia ≠ returns.

## 3. The model (exact equations fitted)

For each outcome `y` and horizon `h`, one linear equation is estimated on the country-year panel:

```
y_it = a + Σ_k b_k x_kit−h + (fixed effects) + e_it
```

with six outcomes: primary GER, secondary GER, primary completion, lower-secondary completion, primary PTR,
lower-secondary PTR; and two horizons: h = 1 (annual one-step) and h = 5 (one five-year step).

Predictor sets (nested, pre-declared):

- **Base:** `y_it−h`, `ln GDPpc_it−h`.
- **Supply:** Base + education spending (% GDP) + per-student spending at the matching level.
- **Full:** Supply + urban share + children in employment + agriculture employment share + matching-level
  enrolment lag. **The Full set is not estimable** — see §5.

Three transforms are run per cell: level; log (outcome strictly positive in training); logit of outcome/100
(share outcomes). Predictions are back-transformed and clipped to the indicator's admissible range
(enrolment 0–150, completion/PTR 0–100). Estimation is OLS with fixed effects: LOO/region folds use
year, decade or region×decade FE (unseen country intercepts are unavailable); time blocks use country FE,
country+region FE, country+linear trend, or country+region-specific trends (identified for future years).
Country-clustered standard errors are used for the association estimates only.

## 4. Evaluation design (pre-declared; see PRE_REGISTRATION.md and Amendments 01–04)

- **Leave-country-out:** 5 folds from a fixed seeded permutation (`seed 20261125`), all years of a country
  held out together.
- **Leave-region-out (robustness):** 6 World Bank regions.
- **Time blocks:** h=1: train ≤2000 → test 2001–2012; train ≤2010 → test 2011–2023. h=5: single steps
  2000→2005 and 2010→2015 (predictors strictly in the training period).
- **Benchmarks:** persistence (value at t−h), country trend (time blocks), region trend (LOO folds; global
  pooled trend fallback), pooled mean.
- **PASS rule (pre-declared):** skill vs persistence > 0 in ≥60% of LOO folds, pooled skill vs persistence
  ≥ 0.05, pooled skill vs trend ≥ 0; outcome×horizon verdict PASS if ≥50% of specification cells meet it,
  WEAK 20–50%, FAIL <20% (Amendment 03). **The pre-declared verdict uses LOO folds only**; time-block and
  region results are reported as robustness and are not used to select a verdict.

## 5. Results

### 5.1 Pre-declared verdicts (LOO folds)

6,048 specification cells attempted; **3,528 ok, 2,520 skipped (2,472 too-small samples, 48 transform not
applicable), 0 silently dropped.** Verdicts: **3 PASS, 9 WEAK, 0 FAIL**.

| outcome | horizon | verdict | share of LOO cells beating persistence | median skill vs persistence | median skill vs trend |
|---|---|---|---|---|---|
| primary GER | 1 | WEAK | 0.30 | −0.752 | 0.910 |
| primary GER | 5 | **PASS** | 0.51 | +0.057 | 0.630 |
| secondary GER | 1 | WEAK | 0.35 | −3.837 | 0.792 |
| secondary GER | 5 | WEAK | 0.34 | −0.370 | 0.665 |
| primary completion | 1 | WEAK | 0.27 | −0.322 | 0.823 |
| primary completion | 5 | **PASS** | 0.45 | −0.031 | 0.614 |
| lower-sec completion | 1 | WEAK | 0.33 | −1.022 | 0.829 |
| lower-sec completion | 5 | WEAK | 0.45 | −0.058 | 0.731 |
| primary PTR | 1 | WEAK | 0.29 | −0.491 | 0.940 |
| primary PTR | 5 | **PASS** | 0.61 | +0.060 | 0.796 |
| lower-sec PTR | 1 | WEAK | 0.26 | −0.923 | 0.877 |
| lower-sec PTR | 5 | WEAK | 0.41 | −0.056 | 0.666 |

Read this table carefully: **at the annual horizon the system is worse than persistence everywhere**
(median skill negative; only 26–35% of cells win), which is unsurprising for slow-moving annual series.
At the 5-year horizon three primary outcomes PASS, but the gains are small (5–6% lower RMSE than
persistence) and two of the three PASS verdicts rest on a minority of specifications (12/24 for primary GER
and primary completion; 15/24 for primary PTR). The robust specifications are the level forms with base or
supply controls; the logit forms and the region-decade FE cells generally do worse.

### 5.2 The harder test: future-year splits

| split | cells ok | median skill vs persistence | share of cells beating persistence |
|---|---|---|---|
| LOO (unseen countries, all years) | 1,424 | −0.176 | 0.38 |
| leave-region-out | 1,716 | −0.277 | 0.34 |
| **future years (time blocks)** | **388** | **−1.015** | **0.003** |

**This is the most important negative result in the record.** When the model is estimated on earlier years
and used for later years — the only split that resembles actually using the model — it is essentially never
better than carrying forward the last observed value (0.3% of 388 cells; median RMSE is about twice
persistence's). The LOO PASS verdicts therefore do **not** transfer to genuine forecasting. The observed
core is a structured description of cross-country associations, not a validated predictive model.

### 5.3 What the data cannot estimate (and why)

- **The demand block.** The only public demand-margin proxy in the pre-registered set, WDI children in
  employment (`SL.TLF.0714.ZS`), has 281 country-year values (100 countries, 1994–2016). Every "Full"
  specification cell is skipped for insufficient sample: **0 of 2,016 Full cells are estimable.** Household
  fees, borrowing and forgone earnings do not exist publicly at all. The demand side of massification is
  therefore not identified — as task-41 predicted.
- **Transmission T3** (child employment → primary GER) could not be estimated at all for the same reason
  (no cell reaches the minimum sample).
- **Learning, gates, jobs/credentials, migration** were never estimated; only declared. Completion and
  transition variables are model-based proxies and cannot separate capacity rationing from exam screening.

### 5.4 Transmission (5- and 10-year long differences; associations only)

Country + decade (baseline) or country + region×decade FE, country-clustered SEs; 4 cells per row
(5y/10y × 2 FE) and up to 2 controls. Full table in `results/transmission.csv`, summary in
`results/analysis_summary.json`.

| id | association | expected sign | median coef (se) | sign as expected | significant at 5% | expected + significant |
|---|---|---|---|---|---|---|
| T1 | Δln GDP pc → Δ primary GER (pp) | + | +9.01 (2.13) | 100% | 100% | **100%** |
| T2 | Δln GDP pc → Δ secondary GER (pp) | + | +8.38 (2.15) | 100% | 100% | **100%** |
| T4 | Δ agriculture employment share → Δ secondary GER | − | −0.32 (0.15) | 100% | 50% | 50% |
| T5 | Δ education spending (% GDP) → Δ primary PTR | − | −0.12 (0.13) | 100% | 12% | 12% |
| T6 | Δ per-student primary spending → Δ primary completion | + | +0.03 (0.12) | 50% | 0% | **0%** |
| T7 | Δ primary completion → Δ agriculture employment share | − | −0.003 (0.016) | 50% | 0% | **0%** |
| T3 | Δ children in employment → Δ primary GER | − | — | — | — | **not estimable (sparse data)** |

Reading: the one robust association is that **GDP-per-capita growth and enrolment/completion growth move
together** (T1/T2: positive in every cell, t≈4, stable across 5- and 10-year differences and both FE
structures; a 10% higher GDP over the period is associated with roughly 0.9 pp higher primary-GER change).
The **structural-change association** (falling agricultural employment ↔ rising secondary enrolment) is
sign-correct in every cell and significant in half (10-year differences: t≈−3.1), so it is reported as
sign-consistent but not robustly precise. **Spending effects are not identified**: education spending →
PTR is sign-correct but only significant in 1 of 8 cells and vanishes at 10 years; per-student spending →
completion and completion → structural change are indistinguishable from zero. None of these is causal.

### 5.5 Specification robustness (what survives the multiverse)

- **Sign of the GDP–enrolment association:** robust (100% of cells, both magnitudes and FE structures).
- **Sign of the structural-change association (T4):** robust in sign, fragile in precision (50% significant).
- **Forecast skill at 5 years for primary GER / PTR:** present in level-form base/supply cells, absent in
  logit and weak-FE cells; small (5–6% RMSE gain).
- **Forecast skill at 1 year:** absent (persistence wins in 65–74% of cells).
- **Forecast skill out of period:** absent (0.3% of cells).
- **Spending/completion/PTR mechanisms:** specification-dependent / not identified.

## 6. Shadow education (small subsection, not modelled)

Shadow education is not modelled here and is not the centre of this record. The panel contains
private-enrolment shares (`SE.PRM.PRIV.ZS`, `SE.SEC.PRIV.ZS`), which are **private schooling**, not private
tutoring; they are not used as a shadow-education target anywhere in this record. The shadow-equation
corner remains the part of the system with the least data (one six-school Cambodian survey), consistent with
task-41; no shadow parameter is estimated or claimed.

## 7. Limitations

- Fixed-effects and long-difference estimates are associations; no identification design, no causal claim,
  no policy recommendation.
- With country FE and lagged outcomes, dynamic panel bias is possible (Nickell-type); the predictive
  evaluation is the discipline used here, and it fails out of period.
- Completion is model-based; GER and PTR are headcount constructs; per-student spending coverage ends in
  2018; children-in-employment coverage is too sparse to estimate a demand block.
- Only 5 LOO folds and 2 country splits were run; fold-to-fold variation is reported through per-fold cells,
  not through a formal uncertainty statement about forecast superiority.
- The trend benchmark is a cross-country trend in LOO folds; it is a weak benchmark (median skill vs trend
  is high), which is why the persistence comparison, not the trend comparison, drives the verdicts.
- Nothing here identifies learning, gates, jobs/credentials, migration or borrowing. Those blocks would need
  data that do not exist publicly (task-41 gaps 1–5).

## 8. Reproduce

Local smoke (no server needed):

```bash
cd research/records/2026-11-25-observed-core
python3 -u scripts/fetch_wdi.py --date 1970:2023 --out data      # ~2 min, public API
python3 -u scripts/observed_core.py --data data --out results_smoke --smoke --workers 1
python3 -u scripts/analyze_results.py
```

Full run (server, key-only SSH; **instance not shut down**):

```bash
ssh -p 45973 root@connect.cqa1.seetacloud.com
mkdir -p /root/work/observed-core && cd /root/work/observed-core
tar xzf observed-core.tgz
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  /root/miniconda3/bin/python -u scripts/observed_core.py --data data --out results --workers 12
```

Actual full run: `/root/miniconda3/bin/python`, numpy version recorded in `results/RUN_LOG.txt`,
**12 workers, 132.3 s wall**, 6,048 cells. Results copied back and committed.

## 9. Files

| file | content |
|---|---|
| `PRE_REGISTRATION.md` | pre-registration + Amendments 01–04 (all committed before the full run) |
| `data/wdi_long.csv`, `data/countries.csv`, `data/MANIFEST.json` | observed panel, country/region list, retrieval + sha256 provenance |
| `scripts/fetch_wdi.py` | public-API data fetch (no credentials) |
| `scripts/observed_core.py` | model, multiverse, splits, benchmarks, transmission |
| `scripts/analyze_results.py` | arithmetic summary of committed results |
| `results/predictive.csv` | every cell: outcome, horizon, split, FE, controls, form, N, RMSE/skill/status |
| `results/transmission.csv` | all association cells with clustered SEs |
| `results/verdicts.csv` | pre-declared PASS/WEAK/FAIL per outcome × horizon |
| `results/analysis_summary.json` | aggregated split/outcome/transmission summary |
| `results/RUN_LOG.txt`, `results/MANIFEST.json` | host, versions, command, wall time, hashes |
| `results_smoke/` | the local smoke run (2 cells) kept for audit |

**Plain-English bottom line.** Build the system from the data that exist; it will describe the
development–schooling gradient well (GDP and enrolment move together; structural change is consistent with
secondary expansion), it will not identify what spending does, and it will not forecast future years better
than assuming nothing changes. The missing demand, learning, gate, jobs and migration blocks are assumptions,
not findings, and they are where the next data work has to go.
