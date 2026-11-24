# AMENDMENT 01 — pre-estimation data-availability facts

**Committed before any estimate was computed** (nothing in `results/` exists at this commit; the only prior
commits are the pre-registration `88073d0` and the raw pull). Appended to, not editing,
[`PRE_REGISTRATION.md`](PRE_REGISTRATION.md), per its §5 "Deviations" rule. Discovered while building the panel
from the cached raw pull; no outcome was inspected before this amendment.

## A1.1 Rate/median indicators publish no denominators in the API

`FE_FRTY_W_MNC` (completed fertility) and `PR_DESL_W_WNM` (want no more) are published **with**
`DenominatorUnweighted` / `DenominatorWeighted`. The rate and median indicators —
`FE_FRTR_W_TFR`, `FE_FRTR_W_GFR`, `PR_WTFR_W_WFR`, `FE_AAFB_W_M25` — are published **without** any denominator
(vérified on the cache: 1,419 education rows for TFR, **0** with a denominator; same for GFR / wanted TFR;
median age at first birth likewise). The pre-registration's cell rule ("`DenominatorUnweighted ≥ 20`") therefore
cannot apply to them.

**Fixed rule (now binding):**

1. Indicators **with** denominators enter the **weighted** models exactly as pre-registered (weight = women in
   cell), plus unweighted analogues.
2. Indicators **without** denominators enter the **unweighted** models only (each published cell is already a
   survey-weighted DHS estimate; the cell contributes one observation, no invented weight).
3. **No denominator is constructed, proxied or imputed.** The absence is reported.
4. For the Q2a window contrast (`A` cumulative births vs `B` period TFR) the primary ratio uses **unweighted
   models for both** indicators so the two coefficients are on the same weighting basis; the weighted-A /
   unweighted-B version is reported as a sensitivity and labelled as such.

## A1.2 `PR_DESL_W_WNM` is published crossed with a second dimension

The "women who want no more children" indicator is published at the intersection of education **and number of
living children** (8 categories). The API exposes that second dimension in `ByVariableId` / `ByVariableLabel`
(`1000` = the "Total" by-variable, i.e. the education main effect; `189000…189006` = living children 0…6+),
which the first pull did not request. The first cache therefore held 8 rows per education label (the panel
builder would have silently collapsed them), and the first re-pull over-corrected and dropped the main-effect
rows. Fixed by re-pulling this one indicator with `ByVariableId,ByVariableLabel` and keeping
`ByVariableId == 1000` for both the education cells and the national total. The national-total pull
(no `breakdown`) likewise returns 8 rows per survey for this indicator and is filtered the same way. If the
subset is still not clean, **indicator D is dropped** and the fact is stated in the report — it is a
descriptive preference measure in no decision rule, and no proxy is substituted.

## A1.3 National-vs-cell consistency check corrected

The pre-registration proposed re-aggregating education cells with cell denominators and comparing to the
published national total within 1%. Unweighted denominators are **not** population-proportional (DHS
stratification and urban oversampling), so the check uses the published **weighted** denominators where the
indicator has them. The check is reported as a diagnostic distribution (median and maximum absolute difference),
not a pass/fail gate — it is a data-quality screen, not a decision rule. For indicators without denominators
the check is not computable and is skipped (reported).

## A1.4 Nothing else changes

The indicator set, the panel rules (education levels, one row per survey × education, no imputation), the
models M0–M5, the contrasts, the decision rules D1–D7, the cohort proxy, the heterogeneity families and the
ecological-limits statement are unchanged. All numbers remain **OBSERVED / ECOLOGICAL**.
