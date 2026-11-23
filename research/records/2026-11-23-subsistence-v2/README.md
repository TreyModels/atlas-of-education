# Subsistence model v2: calibration repair and cohort sequencing, 23 Nov 2026

Branch `research/subsistence-v2-2026-11-23`. Pre-registration was the **first commit** (`62730fc`), before any
v2 data pull, code or estimate. Task-22 baseline: `research/subsistence-2026-11-23` @ `41f6429`.
Box2 `/root/work/subsistence_v2`. All numbers below are from the scripts and files listed at the end.

## 1. Calibration repair (pre-registered C1-C3)
v1 failed in two places: agricultural employment fell too fast (8.1% in 2020 vs 19.4% data) and population
grew too fast (index 4.4 vs 2.9). The repair hypothesis was that both are partly one problem: labour release
was tied too tightly to mechanisation and the absorbing wage sector was not explicit. v2 adds a **wage-sector
job stock with its own creation rate plus a schooling/credential queue**, calibrates agricultural TFP growth
and the food-demand income elasticity instead of imposing them, and lets a mortality-timing shift fit the
demographic path. **Five free parameters (GATE satisfied)**, all calibrated jointly on 1950-2020 stylised-
country medians; N0 and kappa are calibrated from endpoints (not free), sigma = 1.5 is estimated in task-22:

| parameter | value | label |
|---|---|---|
| queue weight in schooling | 4.87 | calibrated |
| wage-job creation rate (per 5 yr) | 0.021 | calibrated |
| agricultural TFP growth (per 5 yr) | 0.045 | calibrated |
| food income elasticity | 0.409 | calibrated |
| mortality timing shift | +28.8 years | calibrated |
| sigma (substitution elasticity) | 1.5 | estimated (task-22) |
| desired surviving children at zero schooling | 3.18 | calibrated (endpoints) |
| schooling effect on desired fertility | 0.124 | calibrated (endpoints) |

**Repair check (model vs data, 1960 = 1; v1 value in brackets):**

| year | ag employment share | TFR | schooling years | population index |
|---|---|---|---|---|
| 1960 | 39.3% vs 30.6% | 4.40 vs 6.01 | 2.99 vs 3.12 | 1.00 vs 1.00 |
| 2000 | 24.9% vs 30.3% | 2.72 vs 2.71 | 5.77 vs 7.92 | 1.33 vs 2.24 |
| 2020 | **17.6% vs 19.4%** (v1 8.1) | **2.35 vs 2.06** (v1 2.19) | 7.53 vs 9.57 (v1 8.2) | **1.58 vs 2.92** (v1 4.4) |

Verdict against the pre-registered tolerance: **the agricultural-share repair succeeded** (1.8 points from the
data, inside the 5-point tolerance), **the population repair failed in the other direction** (1.34 below the
data, outside the 0.5 tolerance; v1 was 1.5 above). TFR and schooling fits improved or held. The population
path is now too slow because the fitted mortality shift delays the mortality decline.

**Parameter recovery test:** re-simulating from known parameters and re-fitting all five series recovers
agricultural TFP growth and the food elasticity exactly, the job creation rate approximately, but **not** the
queue weight or the mortality shift (errors 2.50 and 2.54). So the repaired model is a demonstration with
2 of 5 parameters well identified; the queue and demography channels are weakly identified and no structural
claim should rest on their point values.

**Counterfactuals (2020, baseline first):**

| scenario | ag share | schooling | TFR | population index |
|---|---|---|---|---|
| baseline | 17.6% | 7.5 yrs | 2.35 | 1.58 |
| freeze mechanisation after 1960 | **39.9%** | **0.2 yrs** | 3.29 | 2.19 |
| freeze schooling pipeline after 1960 | 18.0% | **3.0 yrs** | **2.94** | 1.90 |
| freeze mortality decline (1800 level) | 18.4% | 7.2 yrs | **3.96** | **0.39** |

Reading: freezing mechanisation keeps the floor in agriculture and starves the schooling pipeline; freezing
the pipeline leaves released labour unabsorbed and fertility higher; **freezing the mortality decline removes
the population explosion altogether** — the model's implicit first mover is the mortality decline. The
pipeline is what turns released labour into schooling and lower fertility.

## 2. Cohort-level sequencing (pre-registered C4) and the US laboratory (C5)
**C4, country event sequencing.** Pre-registered event rules: release onset = first year after which the
agricultural employment share falls ≥3 points in 10 years; schooling take-off = mean years of schooling rises
≥1.0 year in 10 years; fertility onset = TFR falls ≥1.0 birth in 10 years; common window 1965-2010. 180
countries have data; **64 countries have all three events detected**.
- **release before schooling: 5%** (bootstrap 95%: 0-11%); **schooling before fertility: 69%** (58-80%);
  release before fertility: 6%. Median gap release -> schooling: **-26 years** (-26 to -22).
- So in 61 of 64 countries **schooling take-off precedes agricultural labour release**, i.e. the theory's
  generational ordering (labour release first, schooling second, fertility third) is **not supported** by the
  country event dates. This is the pre-registered falsifier result and it is reported as such.
- Caveats stated up front: these are country-level event dates from period data, not linked cohort histories;
  the common 1965-2010 window and the thresholds were fixed in advance but the schooling series starts in 1870
  and many early expansions are outside the window; the schooling variable is years of schooling for ages
  15-64, which lags cohort attainment. The honest statement is: **the data cannot order a cohort's own
  outcomes, and the country-level ordering they can give contradicts "labour release first"**.

**C5, US laboratory.** OWID long-run US fertility (available 1933-2023 only) and mean years of schooling
(1870+) were pulled; a long-run US agricultural-employment-share series was **not obtainable** (OWID's
share-of-employment series starts in 1991; four other OWID slugs returned 404 and FRED was unreachable), so
documented Historical Statistics/USDA benchmark dates are used and labelled external reference points, not API
data. Detected order: **farm-employment decline 1910 -> schooling take-off 1955 -> fertility decline 1957.**
This is consistent with the theory's ordering for the *twentieth-century* US, but the fertility series cannot
see the nineteenth-century US transition, so the US cannot adjudicate the earlier history. The second early
industrialiser (UK) gap is documented: no long-run farm-employment series was obtainable, so no UK ordering is
claimed.

## (1) Fertility
The repaired model produces the right shape: TFR falls from 4.5 (1950) to 2.35 (2020) against data 6.0 -> 2.06.
It falls because the mortality decline creates the population explosion, and the schooling/pipeline expansion
raises the quantity-quality cost of children. Counterfactuals: with the pipeline frozen TFR stays at 2.94;
without the mortality decline TFR stays at 3.96 and there is no population explosion. The model's fertility
ordering is mortality first, pipeline second — but the event dates above do not let us claim that this is
what happened in most countries, and the population level remains mis-fitted (1.58 vs 2.92). Fertility claims
stay demonstration-level.

## (2) Massification
The v2 schooling path is 3.0 years in 1960 and 7.5 in 2020 against data 3.1 and 9.6 — better behaved than v1
and driven by the explicit queue (without mechanisation schooling collapses to 0.2 years; without the pipeline
it stays at 3.0). But the corrected sequencing result is the important one for massification: **mass schooling
in the 1965-2010 window starts before the large agricultural labour release in 61 of 64 countries**, so the
"pipeline absorbs the released farm labour" story is not the dominant historical ordering in these data. It
may describe later-stage countries and the counterfactual mechanism is still real, but the sequence the theory
needs is not evidenced at the country-event level.

## Honest failures kept
1. Population repair failed (now too slow instead of too fast; pre-registered tolerance missed).
2. Parameter recovery identified 2 of 5 parameters; queue weight and mortality timing are not identified.
3. The pre-registered sequencing falsifier fired: schooling precedes release in 61/64 countries.
4. The US test can only address the twentieth century; the UK/long-run farm-share gap is documented, not filled.

## Files and provenance
`scripts/`: `pull_us_history.py` (OWID/FRED pull, network-bound; raw files on box2), `sequencing.py` (C4/C5),
`model_v2.py` (C1-C3). `results/`: `model_v2_summary.txt`, `model_v2_paths.csv`,
`model_v2_counterfactual.csv`, `model_v2_params.json`, `sequencing.txt`, `sequencing.json`,
`event_dates.csv`; `data/us_history_sources.txt` records which pulls succeeded and which failed.
Data reused from the task-22 box2 paths (WDI extract, transition record, project panel, PWT/USDA series).
Runtime: network pull ~1 minute; sequencing ~3 s; model calibration ~4 s wall on one core — the box was under
the task-21 battery, so the job stayed light. This is a demonstration model, not an estimate of history.
