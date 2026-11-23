# Added controls: child mortality and women's work, 23 Nov 2026

Server box2 (`ssh autodl2`), `/root/work/controls`; scripts in `scripts/`, results in `results/`. **Panel: the
observed data** `/root/work/data` (migrated copy under `/root/autodl-tmp/migrated/`; not the gap-filled panel, so
every number here is directly comparable with the reference
matrix and with the earlier session; the controls are also the two least complete series, so gap-filling would
not rescue them). Estimator = `2026-11-23-handoff-run/scripts/full_matrix_trends.py`: 17 measures, ten-year
changes, country effects, decade effects, errors clustered by country, with and without a straight-line
country trend. **Income is logged** here; the handoff copy itself used income in levels (the known bug) and
that version gives 126/45/25, so it is not used.
**Baseline check:** with the log fix the estimator reproduces the recompute reference exactly — **127 links
significant with country effects, 42 with trends, 24 in both**. All comparisons below are against those.

## The mediator rule, applied to all 272 links
A control is a **mediator** of link x -> y when it lies on a two-step causal path x -> control -> y. Plausible
one-step causal links among the 17 measures were written down once (in `scripts/controls_matrix.py`, plain
to read) and the rule was applied programmatically; the full table is `results/mediator_table.csv`.
- **Child mortality** is a mediator for 28 links and is the treatment or outcome for 32 more, so it is usable
  for **212**. The excluded links are exactly the ones where schooling or income leads to life expectancy or
  fertility through child survival (e.g. `lsc->life_exp`, `gdppc_log->fertility`, `urban->fertility`).
- **Women's work** is a mediator for 42 links and is the treatment or outcome for 32 more, so it is usable for
  **198**. It is excluded for every `schooling -> fertility` link and every `schooling/income/urbanisation ->
  income/life expectancy/child mortality` link — e.g. **all six schooling -> fertility links are NOT tested
  with either added control**, which is the rule the task demanded (never control for a variable on the causal
  path when testing schooling -> fertility).
- Both controls are usable together for **172 links**.

## Tests designed to kill this exercise
1. **Sample composition vs control effect (the one that matters most).** Of the rule-allowed tests, verdict
   changes vs baseline: with country effects 51 of 212 for child mortality, 37 of 198 for women's work and 59
   of 172 for both; with country trends 8, 34 and 28. Adding a control also changes the
   sample: child mortality is observed for ~73% of country-years, women's work for only ~40%. For every one
   of the 217 cells whose verdict changed, the baseline was **re-estimated on exactly the rows the control
   used**. Result: **120 changes are pure sample composition** (the baseline verdict already flips on the
   smaller, different set of countries), **94 are genuine control effects** (of which 79 are real estimate
   moves and 15 are only precision losses), 3 are both. By control: **child mortality 53 control-effect
   changes vs 6 sample changes; women's work only 8 control-effect vs 63 sample changes.** Women's work is
   therefore mostly a sample-selection device in this panel, not a test of the effect.
2. **Negative control — deliberately control a mediator.** The rule bites and the estimator notices:
   life expectancy -> fertility controlling child mortality (its mediator) moves **-0.049 (0.007) ->
   +0.013 (0.007)**, from significant negative to zero/sign flip; income -> fertility controlling women's work
   **+0.133 (0.060) -> +0.022 (0.065)**, i.e. collapses; lower-secondary -> child mortality controlling women's
   work **+0.183 (0.059) -> +0.047 (0.045)**, a 74% shrink; secondary -> child mortality 88%. These are exactly
   the cells the rule excludes; the collapse proves a mediator control would have manufactured a null.
3. **Leave-one-control-out.** In the country-effects version, **114 of 172** links give the same verdict with
   child mortality only, women's work only and both; 46 differ between the two single-control versions. With
   country trends it is 143 of 172. So the verdict often depends on *which* control is added — another reason
   not to read "survives a control" as "is causal".
4. **Collinearity.** With country effects, child mortality VIF median 1.37 (max 4.4); women's work median 1.04
   (max 1.1) — fine. **With country trends child mortality becomes collinear with life expectancy: VIF median
   8.0, max 33.0**, and indeed the three sign flips are all `life_exp -> ...` cells under the "both" controls.
   Those flips are an artefact of two near-identical life-table series; do not report them as findings.
5. **Power — where a verdict did not change, could a meaningful change have been seen?** The exact standard
   error of "how much the estimate would move if the control were dropped" is computed for every link. The
   median smallest detectable change is **37% of the baseline estimate** (child mortality, country effects),
   17% (child mortality, trends), 14% (women's work, country effects), 18% (women's work, trends). Of the
   unchanged links, **117 of 161** (child mortality, FE) and **56 of 161** (women's work, FE) could hide a 20%
   change at this sample size. A blank "no change" cell is not evidence of no effect.

## (1) Fertility
- **Schooling -> fertility cannot be tested with these controls** by the rule (both are mediators); that is
  the correct answer, not a null. What can be shown is that breaking the rule destroys results — see the
  negative control above.
- **Fertility -> schooling is robust to both controls.** Fertility -> lower secondary: **-4.79 (1.29),
  n=1,932 -> -4.08 (1.25), n=1,894** with child mortality and **-6.26 (1.37), n=1,479** with women's work;
  with country trends -3.41 (0.96) -> -3.05 (0.98) / -7.69 (1.89). Fertility -> secondary: -4.43 (0.85) ->
  -2.96 (0.82) / -5.28 (1.10). Fertility -> primary completion: -2.98 (1.18) -> -2.02 (1.01) / -3.00 (1.44).
  Every one stays significant; magnitudes are similar or larger. **This conclusion is strengthened.**
- **Child mortality -> fertility is robust to women's work with country effects** (+0.008 (0.001) ->
  +0.006 (0.001), n 8,569 -> 4,378), but its country-trend version loses significance on the women's-work
  sample. The loss is sample composition (the baseline is already null on those rows), not the control.
- **Life expectancy -> fertility**: child mortality is its mediator, so the rule forbids the control; the
  violation flips it (above). With women's work (allowed) it stays significant: -0.049 (0.007) -> -0.036
  (0.008). Its trend version loses significance on the smaller sample (sample composition).
- **Income -> fertility** is a mediator case (through women's work and child mortality); controlling either
  kills it (+0.133 -> +0.022 with women's work), which is why the rule excludes it. Nothing here weakens the
  earlier finding; it shows the finding is a total association whose channel is these mediators.

## (2) Massification
- **The main massification finding is unchanged and strengthened.** Electricity -> lower secondary:
  **+0.348 (0.084), n=1,414 -> +0.299 (0.085), n=1,378** with child mortality and **+0.349 (0.082),
  n=1,351** with women's work; still significant with country effects and still null with country trends
  (+0.067 (0.111) -> +0.062 / +0.082). Electricity -> secondary +0.362 (0.082) -> +0.300 (0.086) /
  +0.350 (0.084). The extra controls do not explain the electricity-schooling association.
- **Income and urbanisation -> schooling** are similar: income -> secondary **+5.97 (2.36)** survives child
  mortality (+5.33) and grows with women's work (+7.55); urbanisation -> secondary +0.78 (0.17) -> +0.58
  (0.17) / +0.80 (0.15). Their country-trend versions are fragile: income -> secondary +4.52 (2.04) becomes
  3.89 (2.02, not significant) with child mortality — a genuine control effect; the women's-work version loses
  significance only because the smaller sample's baseline is already null (sample composition).
- **The internal schooling ladder** (primary -> secondary, lower secondary -> secondary) survives child
  mortality with country effects (e.g. lower secondary -> secondary +0.125 (0.058) -> +0.183 (0.053)) but
  loses significance on the women's-work sample; that loss is sample composition, not the control.
- **Women's work itself does not rescue or destroy any education-driver linkage in a way that survives the
  sample-change check**: of its 71 verdict changes, 63 are sample composition and only 2 are estimate moves
  (both tiny). So "control for women's work and the schooling effect survives" is mainly a statement that the
  surviving sample is different, not that the effect is robust.

## What changes for the earlier conclusions
- **Unchanged/strengthened:** electricity -> schooling (country effects only), income/urbanisation ->
  schooling (country effects), fertility -> schooling, child mortality -> fertility, life expectancy ->
  fertility (with the caveats above).
- **Weakened:** income -> secondary with country trends (child mortality absorbs it); the internal
  schooling-ladder results on the women's-work sample (sample composition).
- **Not evidence either way:** all "no change" cells are power-limited to a median 14–37% change; the three
  sign flips are collinearity artefacts of child mortality with life expectancy under country trends.

## Files
`scripts/`: `controls_matrix.py` (all 272 links x 2 trend specs x 4 control variants + mediator table +
power constants), `common_sample.py` (same-row baseline re-estimation), `controls_analysis.py` (tables,
decomposition, power, collinearity). `results/`: `variant_table.csv` (every link x variant: estimate, SE, n,
countries, verdict, change, MDC, VIF), `changed_verdicts.csv` (all 217 changed cells), `changed_origin.csv`
(sample-composition vs control-effect classification), `mediator_table.csv` (the rule applied to all 272
links), `summary.txt`, and the raw `controls_results.json` / `common_sample.json`. Provisional: any cell where
the added control is collinear (child mortality with country trends) or where the sample falls sharply
(women's work) is not a clean test; the sample-vs-control decomposition is the honest reading.
