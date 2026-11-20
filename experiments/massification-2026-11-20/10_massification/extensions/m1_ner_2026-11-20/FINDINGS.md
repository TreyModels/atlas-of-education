# FINDINGS — M1-NER (EXP-3): construct equivalence of the cohort-flow NER analogue

**Worker MN, 2026-11-20 (Asia/Shanghai).**
**LABEL: SYNTHETIC / DERIVED (test objects) · OBSERVED-REFERENCE-ONLY (HKG/PHL series).**
**No causal or direction claim. No HKG transfer was run. No HKG, portability, capacity-timing, or
phase-verdict claim is made. Nothing here is evidence about any country.**

---

## 1. Answer in one paragraph

**No — under the frozen H1 bars, the model's cohort-flow NER analogue is not construct-equivalent to
the predeclared stock-style NER reconstruction.** Both H1 conditions fail. In the declared
`SYN00_PHL_LIKE / primary` window, the stock and flow analogues differ by up to **2.685 pp** in the
85–95 band (7 of 15 band years exceed the 2.0 pp bar), and the implied first-sustained 5-year
crossings differ by **3 years at the 90 threshold** (flow 2007 vs stock 2010) and **2 years at the 95
threshold** (flow 2016 vs stock 2018). **H1 = NOT ADMISSIBLE.** The declared expected sign does hold —
in every band expansion year the flow leads the stock (mean stock−flow = **−1.75 pp**) — but the
magnitude of the lead is 2–3 years at the crossings, exactly the direction that could make a crossing
look earlier than a stock measure would. The direct consequence for the HKG gate is in §8: SR-1 is
**not** cleared at the construct level, so an HKG diagnostic transfer may not use this object as-is.

---

## 2. What was tested

| item | value |
|---|---|
| test object | v1.2.1 NER panel (`synthetic_panel_v1_2_ner.csv`), **SYNTHETIC / DERIVED** |
| flow analogue | `flow = 100 × admitted_official / cohort` = the panel's `ner` column |
| stock analogue | `stock = 100 × mean over the last dur years of admitted_official / cohort` (mean of per-year ratios, including year t) |
| durations | factory's declared `DVEC` = (6, 3, 3, 4) for (primary, lower_secondary, upper_secondary, tertiary); primary `dur = 6` |
| verdict series | **`SYN00_PHL_LIKE / primary`, years 1970–2025** — declared in the predeclaration before any stock or difference was computed |
| band | every year 1975–2025 with `85.0 ≤ flow ≤ 95.0` (inclusive); 1970–1974 excluded only because the 6-year stock window is incomplete |
| Condition B bar | `|stock − flow| ≤ 2.0 pp` in **every** band year |
| Condition C bar | first-sustained (5 consecutive years ≥ threshold) crossing years differ by **≤ 1 y** at thresholds **90** and **95** |
| overall rule | `ADMISSIBLE` iff Conditions B and C both hold |
| reference series | HKG observed NER/ANER 1971–1996 and PHL observed NER 1976–2017, computed separately, **REFERENCE-ONLY** |

The test is a **measurement / construct** test. It does not re-score any v1.2 check, does not re-fit,
does not add a parameter, and does not use the observed HKG or PHL series in the H1 decision.

---

## 3. Condition B — band agreement: **NOT MET**

15 band years have a complete 6-year stock window. Seven of them exceed 2.0 pp.

| year | flow | stock | stock − flow (pp) | \|diff\| | 2.0 pp bar |
|---:|---:|---:|---:|---:|---|
| 2001 | 85.138 | 82.453 | −2.685 | 2.685 | **NOT MET** |
| 2002 | 86.048 | 83.505 | −2.543 | 2.543 | **NOT MET** |
| 2003 | 86.945 | 84.540 | −2.405 | 2.405 | **NOT MET** |
| 2004 | 87.801 | 85.531 | −2.270 | 2.270 | **NOT MET** |
| 2005 | 88.643 | 86.457 | −2.187 | 2.187 | **NOT MET** |
| 2006 | 89.440 | 87.336 | −2.104 | 2.104 | **NOT MET** |
| 2007 | 90.067 | 88.157 | −1.910 | 1.910 | MET |
| 2008 | 90.536 | 88.905 | −1.631 | 1.631 | MET |
| 2009 | 90.873 | 89.560 | −1.313 | 1.313 | MET |
| 2010 | 91.126 | 90.114 | −1.012 | 1.012 | MET |
| 2011 | 91.445 | 90.581 | −0.864 | 0.864 | MET |
| 2012 | 91.861 | 90.985 | −0.876 | 0.876 | MET |
| 2013 | 92.415 | 91.376 | −1.039 | 1.039 | MET |
| 2014 | 93.206 | 91.821 | −1.385 | 1.385 | MET |
| 2015 | 94.473 | 92.421 | −2.052 | 2.052 | **NOT MET** |

**Binding number:** maximum |stock − flow| = **2.685005 pp at 2001** (stock 82.452834, flow
85.137839). Seven violating years: **2001, 2002, 2003, 2004, 2005, 2006, 2015**. Condition B is
**NOT MET**.

Two in-band years, 1970 (flow 94.745) and 1971 (flow 87.823), are excluded because a 6-year stock
window does not exist before 1975. This exclusion was declared before the run (predeclaration §4.1);
it is **not** a result-dependent exclusion. It is a real limitation of applying a 6-year stock
reconstruction at the panel's left edge.

Note that in **all 15** band years the difference is negative: the stock reconstruction sits **below**
the flow. The band test fails on **magnitude**, not on the sign of the declared expected bias.

---

## 4. Condition C — crossing agreement: **NOT MET**

Crossing rule: first year of five consecutive years at or above the threshold.

| threshold | flow first-sustained | stock first-sustained | difference | ≤ 1 y bar |
|---:|---:|---:|---:|---|
| 90 | 2007 | 2010 | **3 y** | **NOT MET** |
| 95 | 2016 | 2018 | **2 y** | **NOT MET** |

- At 90, the flow series is non-monotone: it is already at 94.745 in 1970 (so `first-at-or-above` is
  1970) but falls away and only becomes **sustained** in 2007. The stock analogue first reaches 90 in
  2010 and is sustained from 2010. The predeclared sustained rule is used, so the 1970 spike is not
  treated as a crossing.
- At 95, flow is first-at and first-sustained in 2016; stock reaches 95 and is sustained in 2018.

**Binding numbers:** **3 y** (90) and **2 y** (95). Condition C is **NOT MET** at both thresholds.

The size of the lag is not noise. A backward 6-year mean of a rising annual series lags the annual
series by roughly half the window — `(6 − 1) / 2 = 2.5` years on a linear ramp — and the observed
2–3 year differences are of that order. The flow object and the stock reconstruction therefore record
the crossing at different times as an arithmetic property of averaging, not because of a few outlying
years.

---

## 5. Overall H1 and the declared expected sign

| condition | bar | result |
|---|---|---|
| B — band agreement | ≤ 2.0 pp every band year | **NOT MET** (max 2.685 pp; 7/15 years) |
| C — crossing agreement | ≤ 1 y at 90 and 95 | **NOT MET** (3 y and 2 y) |
| **H1 overall** | B **and** C | **NOT ADMISSIBLE** |

**Expected sign (descriptive).** In all **15/15** band expansion years the flow is at or above the
stock (`stock − flow ≤ 0`); the mean difference over those years is **−1.75 pp**, and there are **no**
counter-sign years. This is exactly the sign the Council declared: during expansion the cohort-flow
analogue leads the stock reconstruction, so a crossing read off the flow is earlier than a crossing
read off the stock. The observed 2–3 year crossing lead is the quantified size of that bias in this
series. It is reported as a measurement result; no direction or causal claim is made.

The expected sign is **not** one of the two numeric falsifiers. The verdict is set by Conditions B
and C, both of which fail.

---

## 6. Panel-wide sensitivity (descriptive only, not verdict-bearing)

The same band rule was applied to **all 30 synthetic countries × 4 levels** (582 complete-window band
series-years), purely to check that the anchor is not an outlier:

| statistic | value |
|---|---|
| panel-wide max \|stock − flow\| | **6.740 pp** (`SYN04 / primary`, 2008) |
| band series-years over 2.0 pp | **141 / 582** |
| series with at least one violating band year | **44 / 120** |
| at 90: series with both crossings defined and within 1 y | **4 / 30** |
| at 90: series with both crossings defined and ≥ 2 y apart | **26 / 30** |
| at 95: series with both crossings defined and within 1 y | **2 / 20** |
| at 95: series with both crossings defined and ≥ 2 y apart | **18 / 20** |

The anchor is therefore **not** selectively bad: the failure is systematic across the panel, and the
verdict does not depend on choosing `SYN00_PHL_LIKE`. (Many series have no crossing at all at 90/95;
those are counted separately in `M1_NER_RESULTS.csv` and are not treated as agreements.)

---

## 7. Observed references — **REFERENCE-ONLY, NOT VALIDATION**

These are descriptions of the on-disk observed series. They were **not** compared with the synthetic
stock or flow series, were **not** used to set the synthetic series or thresholds, and are **not**
evidence for or against the model.

| series | window | observations | first-sustained ≥ 90 | first-sustained ≥ 95 |
|---|---|---:|---:|---:|
| HKG `ner_primary` | 1971–1996 | 17 (1971–1985, 1995–1996) | **1974** | **1979** |
| HKG `aner_primary` | 1971–1996 | 17 | **1974** | **1979** |
| PHL `ner_primary` | 1976–2017 | 30 (sparse) | **1981** | **none_by_2025** |

- HKG `ner_primary` first-at-or-above 90 is also 1974; first-at-or-above 95 is 1977 (sustained 1979).
- PHL `ner_primary` first-at-or-above 90 and 95 is 1976, but 1976 is a single-year observation; the
  first **sustained** ≥90 run is 1981 (inside the contiguous 1981–1989 block). No five-consecutive-
  observed-year run at ≥95 exists in the PHL record, so it is reported as `none_by_2025`.
- Missing years are not interpolated. A "5 consecutive years" run must be five consecutive **observed**
  calendar years; block-level crossings are in `M1_NER_REFERENCE.csv`.

The HKG reference crossing years are a property of the observed series only. They do not enter the
synthetic test and must not be read as a check on the model.

---

## 8. What this means for the HKG gate

H1 is the construct-level clearance of **SR-1**. It fails at **both** conditions. Therefore:

1. **SR-1 is not cleared at the construct level.** The cohort-flow analogue is **not** an admissible
   realisation of the stock-style NER target under the frozen bars.
2. An HKG diagnostic transfer that would use this object **must return `BLOCKED-MEASURE(SR-1)`**
   (a terminal state, not a diagnostic result), unless and until a **stock object** is specified in a
   **new predeclaration**. The SR-9 authorisation is void for the current NER object, exactly as the
   H1 row states ("if FAIL → `BLOCKED-MEASURE(SR-1)`, authorisation void").
3. The v1.2.1 object must be labelled a **cohort-flow analogue only** — not the UIS stock NER, and
   not a cleared measure for the HKG target.
4. **No HKG transfer comparison was run here**, and none should be run on this object without the
   measures step above. No statement is made about whether an HKG transfer would hold or fail.

The failure is not a claim that no NER object could ever be admissible. It is a result about **this
declared stock reconstruction and this cohort-flow analogue**: the gap is too large in the band and
the crossing lag is 2–3 years. A different stock object (e.g. one carrying grade progression
explicitly) would be a **new** measurement predeclaration, not a rescue of this one.

---

## 9. Limits and disclosures

1. **One declared stock reconstruction.** The test uses the brief's parameter-free analogue: mean of
   `admitted_official / cohort` over the last `dur` years. It is not the UIS stock measure itself and
   does not model grade progression or repetition. A different stock construction is not tested; the
   verdict applies to the frozen definition.
2. **Left-edge exclusion.** 1970–1971 are in the band but have no complete 6-year stock window, so
   they are excluded as predeclared. If they were included with a truncated stock window, the band
   result could differ; that variant was not predeclared and is not run. This exclusion **cannot
   rescue** the verdict: Condition B already fails at seven complete-window years (and adding years
   can only add violations), and Condition C fails independently at both thresholds.
3. **Non-monotone flow.** The flow series has 11 year-on-year decreases over 1970–2025 and starts at
   94.745 in 1970. The sustained-crossing rule (fixed before the run) is what prevents the 1970 spike
   from being read as a crossing. `first-at-or-above` is reported alongside for transparency.
4. **Synthetic only.** The object is model output. The observed HKG/PHL series are construct
   references only. No external data, no web, no re-fit, no new parameter, no RNG.
5. **Predeclaration note (descriptive; no rule changed).** Predeclaration §8's parenthetical says
   "24 observations each" for HKG. 24 is the size of the **full** observed HKG series (1971–2018); the
   declared **1971–1996** window contains **17** observations each (15 in 1971–1985, 2 in 1995–1996).
   The operative window rule ("1971–1996") was applied exactly as declared; no threshold, window, or
   rule was changed, and the H1 verdict does not depend on this description.
6. **No HKG run.** This experiment deliberately stops at the construct test. It does not execute any
   HKG input assembly, transfer comparison, timing tolerance, or verdict.

---

## 10. Reproducibility

- `code/run_m1_ner.py` is deterministic: no RNG, no clock, no network, no environment-dependent
  output. It verifies the predeclaration and panel sha256 before running and refuses otherwise.
- Two independent runs, `_determinism/run1/` and `_determinism/run2/`, are **byte-identical** to each
  other and to `results/` for all four CSVs (`cmp` clean; `sha256` recorded in `RUN_MANIFEST.json`).
- Binding result hashes: see `RUN_MANIFEST.json`.

| file | content |
|---|---|
| `results/M1_NER_RESULTS.csv` | all test statistics and verdicts |
| `results/M1_NER_COMPARISON.csv` | year-by-year flow vs stock, band only (verdict + sensitivity roles) |
| `results/M1_NER_CROSSINGS.csv` | first-sustained crossings at 90/95 for both analogues, all series |
| `results/M1_NER_REFERENCE.csv` | observed HKG/PHL series and crossings, REFERENCE-ONLY |

**In one line:** *the model's NER object is a cohort-flow analogue that leads a stock reconstruction
by 2–3 years at the crossings and by up to 2.7 pp in the 85–95 band; under the frozen H1 bars that is
**NOT ADMISSIBLE**, so the HKG gate must return `BLOCKED-MEASURE(SR-1)` or adopt a newly predeclared
stock object.*
