# Recompute, 23 Nov 2026: results that used `gdppc_log.json` (and a few other flaws)

Server: AutoDL, all runs in `/root/work/recompute/`. Every output here was produced by the script of the same name in `scripts/`.
`results/old_levels/` = rerun on the original data (control reproduced); `results/new_true_log/` = same script, `gdppc_log` replaced by `ln(value)`.
Paths in the scripts were edited to read `./data`; nothing else was changed unless stated.

## 1. The bug is confirmed
`data/gdppc_log.json` (14,074 rows) holds GDP per head in constant US dollars, not logs: min 122.7, median 3,761, max 247,170, no value <= 0
(`AFE 2024 = 1432.5`). A true log is 4.8 to 12.4. Every script that entered it as a control or variable put income in dollars,
so a coefficient on it was per dollar (the "0.0000" and "+95.5" cells) and it worked as a very poor control for proportional income gaps.

**Affected (income used as control or variable, logged in name only):** full_matrix_trends, spec_curve_final (control), decompose, lead_test,
exp2_battery, boppart_test, bayes_fertility, farms, foodprice, group_trends, group_matrices3, five_groupings, cluster_countries,
massification_analysis, mc_big (country-resample table), and the figures/tables built from them (make_figures, side, battery/battery2, run2/run2b, exp1: Tier D or inputs missing, not rerun).

**Not affected:** exp1b (uses only ter and wage_emp), the luck test headline (lsc vs fertility), absorption_decomposition (income is not in that chain),
the entire 22 Nov panel branch (`sweep.py` applies `np.log` to `NY.GDP.PCAP.KD`; its `tight`, `final`, `bayes`, `sweep` outputs reproduce, see 6).
**Coded for levels on purpose (name was wrong, numbers right):** ag_trends, replacement ($5,000 thresholds), cohort_model / cohort_huge (`ly/y0` ratio),
input_prices_controlled (takes the log itself). Re-running these on logs would be wrong; they are marked and were not rerun on logs.
Could not rerun (inputs not on the server: `water`, `beds`, `roads_paved` .gz): bundle, state_bundle, impute, roads_marriage.

## 2. Old and new numbers

| Result | Old | New (true log) | Plain-words conclusion |
|---|---|---|---|
| Matrix with country trends (job 1) | 126 edges sig. with country FE; 45 with trends; 25 both (19.8%) | 127; 42; 24 (18.9%) | Same: most edges die under trends. Survivor list changes at the margin (gdppc_log -> urban, fertility -> gdppc_log now appear). |
| Electricity -> lower-secondary, matrix | FE +0.333 (SE .083); trends +0.052 (SE .098), n=1,343 | FE +0.348 (.084); trends +0.067 (.111) | Unchanged: real with country effects, not separable from a country trend. |
| Spec curve, wage jobs -> tertiary (script says 1,536; 1,408 estimable) | median -0.00; 5-95% -0.040..+1.371; sig+ 27.9%; LOCO +0.83..+1.22, 203/203 positive; base +1.133 (+-0.378) | median +0.014; -0.016..+1.323; sig+ 24.9%; LOCO +0.69..+1.18, 203/203; base +1.083 (+-0.458) | Unchanged: fragile, holds in about a quarter of specifications. |
| Same curve plus country-trend specs (2,304 defined, new script) | sig+ 18.6%; trend specs 0.0% sig+ | sig+ 16.6%; trend specs 0.0% sig+ | The wage->tertiary signal does not survive a country trend in any specification. |
| Luck test, headline | 0 of 20,000; observed 11.97%, null max 4.57% | identical (variable is lsc, not income) | Unchanged on its own terms. |
| Luck test with a harder null (other country's lsc series, same years; `luck_v2.py`) | n/a | null median 1.06%, 99th pct 6.89%, max 13.12%; **6 of 20,000** reach 11.97% | Weaker than quoted but still not chance (p ~ 0.0003). The time-shift null was easy, as REVIEW said. "Survives 40% measurement noise" should be dropped (its yardstick, 2.2%, was the easy null). |
| Luck test, country resample, income "top three" | 0.0% | 1.8% | Lsc and child mortality still the two leaders (99.8%). |
| exp1b chain vs common cause | obs +1.425; common-cause 0 of 1,200 reach it | identical output | Unchanged (conditional on the most favourable specification). |
| Bayesian model averaging, fertility fall (bayes_fertility) | inclusion: higher ed 1.00, labour force 0.99, income 0.26 | higher ed **0.45**, labour force 0.86, income **0.97**; electricity, lsc, child mortality 1.00 in both; higher-ed coefficient -0.033 -> -0.023 | **Changes.** With real log income, income is in the model and higher education is a coin flip. The old "higher ed is a robust predictor of the fertility fall" does not hold. |
| Absorption decomposition (tertiary -> secondary) | +0.106 -> +0.035 with cities | identical lines; only the reverse-direction income row changes (+95.5 -> +0.003) | Unchanged. |
| Lead/lag, lsc/sec/ter | lsc +0.333, sec +0.418, ter -0.183 | +0.348, +0.362, -0.253 | Unchanged; all still flagged PRE-TREND. New: electricity -> tax placebo now significant (+0.055 +-0.027). |
| Driver battery vs noise band (exp2) | income +0.97 +-0.81, "indistinguishable from trend" | income +2.07 +-0.74, "outside both" | Income moves from noise to signal. Note the simulated bands moved by +-0.2 between two runs of identical code: that simulation is unseeded. |
| Boppart test (investment price -> farm share) | +0.098 (+-.18) FE; -0.068 trends | +0.072 (+-.20); -0.061 | Unchanged: null. |
| Farms, food prices | farm-output share +income&cities +0.0081; food price x farm share -0.668 | +0.0105; -0.664 | Unchanged in sign and significance. |
| massification_analysis | income explains 0.7% (n=9,272); "more income -> fall begins earlier" r=-0.16 (n=60) | 2.7%; r=-0.38 | Income now matters more; direction story unchanged. |
| Clusters, five groupings, group trends | | 118 / 48 / 105 changed lines | Exploratory Tier B; values changed, not re-interpreted. See `results/*/`. |
| Input prices (ag_trends = original ratio, now with true log income) | farm exit +0.0239 (trends +0.0056); wage jobs -0.0140 (trends -0.0004) | farm exit +0.0119 (+0.0061); wage jobs -0.0035 n.s. (+0.0004) | As job 3 found: wage-jobs effect is an income effect; farm exit halves. |

## 3. Electricity +16.05 (tight/results.json)
**Where +16.05 comes from.** `research/records/2026-11-22-massification-panel/results/tight/results.json`, key `within["electricity->lsc"]`, produced by `scripts/tight_tests.py` (panel-branch script; WDI data via `sweep.py fetch`): split-panel-jackknife country-FE regression of the 10-year change in lower-secondary completion on electricity access standardised to one SD, controlling own starting level and decade dummies, n=471, one specification. It contains no income variable, and the panel branch logs income correctly, so this number is **not touched by the gdppc_log bug**. Because X is per SD (SD = 33.0 points), +16.05 means about +0.49 points of completion per point of electrification over ten years, not "+16 points".

Rerun on freshly fetched data (`tight_pair.py`, same code, PYTHONHASHSEED=0), both ways:
| | b_xy | 90% CI | b_yx | n |
|---|---|---|---|---|
| Original (outcome in its own units) | **+16.048** (old file: +16.048) | +12.17, +21.73 (old +11.77, +20.96: bootstrap seed differs) | +1.478 (old +1.478) | 471 |
| A2 (outcome standardised, fixes the b_xy minus b_yx unit mismatch, apex-v1.2 a21bbe6) | +1.215 SD per SD | +0.92, +1.65 | +0.155 | 471 |
The point estimate reproduces to three decimals; the A2 version is the same number rescaled by the SD of the outcome change (13.2), and the lead over the reverse direction still excludes zero. Same for electricity -> sec (+15.38 / A2 +1.26), wage_emp -> ter (+21.96 / +1.81) and urban -> lsc.

**Through the specification curve (never done before; `spec_curve_generic.py`, X = electricity, Y = 10-year change in lsc, 2,304 specifications: 4 lags x 32 control subsets x 3 fixed-effect types x 3 samples x 2 transforms; 2,208 estimable):**
| slice | old data | true-log data |
|---|---|---|
| all specs: median / sig+ / sig- | +0.004 / 25.4% / 5.1% | +0.004 / 24.2% / 5.1% |
| level outcome, country FE: median b / sig+ | +0.279 / 66.3% | +0.272 / 63.3% |
| level outcome, country+decade FE | +0.278 / 67.1% | +0.272 / 64.7% |
| level outcome, **country trends** | +0.051 / 4.3% sig+, 8.7% sig- | same |
| log outcome (any FE) | about 0, 5 to 8% sig+ | same |
| leave-one-country-out (base spec) | +0.333 (+-0.083); +0.300..+0.384; 197/197 positive | +0.348 (+-0.084); +0.310..+0.397; 197/197 |
Reading: the association with country effects survives lags, control sets (income, cities, paid jobs, tertiary, child mortality) and samples in about two thirds of level specifications, and no single country drives it. It does not survive a country-specific linear trend (4% significant, as many significant negatives as positives), and it is zero in log terms. That is the same fork as the wage result but with a much stronger "FE" arm: **Tier B stays, with the sentence "real with country effects, indistinguishable from a country trend; not shown to be zero (power check, job 2)"**. The pooled median of about 0 in the first row is a unit artefact (level and log specs are mixed), so do not quote it as "median zero".

**BMA**: the panel branch's `bayes.py` rerun reproduces its findings file exactly (deterministic; see 6). Electricity's inclusion probability for lower-secondary is **0.92 within-country (0.25 pooled)**, not 1.00; the 1.00 values are for secondary GER (within-country 1.00) and tertiary 0.96. STATUS's "posterior inclusion probability of 1.00" for electricity -> lsc is a misquote; with the corrected 0.92 the within-country evidence is still strong but it is again a fixed-effects statement.

## 4. Other bugs found while doing this
- **Spec-curve label:** script prints "specifications: 1536" but only 1,408 are estimable; headline now reports estimable of defined.
- **Spec-curve median mixes units:** level specs are in points, log specs in log points; pooled median (about 0) is partly scale. STATUS's "0.00 under a log transform" is a scale artefact, not a null. `spec_curve_generic.py` reports median and share significant per transform (t-statistics are unit-free). Wage->tertiary, level, country FE: median +0.82, 45% significant; electricity -> lsc, level, country FE: median +0.27, 63% significant. The collapse comes from country trends, not from the log.
- **tight_tests unit mismatch** (b_xy in outcome units vs b_yx in X units, so their difference was meaningless): already fixed on apex-v1.2 (commit a21bbe6); rerun both ways below. Seeds used Python `hash()` (salted per process): not reproducible; fixed with PYTHONHASHSEED=0.
- exp2 simulation unseeded (see above).
- Missing inputs make four pack scripts unrunnable here (listed in 1). Not recomputed: matching_model claims (REVIEW item 5), CES recovery (job 6 already redone).

## 5. Boppart, Kiernan, Krusell and Malmberg (2023) set-up, and a matched input-price test
**What they did (from the paper's text, NBER w31101, sections 2 and 4).** Four agricultural inputs: labour (human-capital adjusted), capital, land, intermediates
(fertiliser, pesticides and other outside-sector goods). Prices: wage from the PWT labour share times output per worker; capital priced by the PWT investment
price; **intermediates priced from BACI bilateral trade unit values of selected fertilisers and pesticides** (country-specific; they note no macro price series exists after the 1985 FAO set);
land from micro rental data. Quantities: FAO capital stock, UN/FAO intermediate-input use. Everything is a **2005 cross-section**; countries are ordered by log real GDP per worker (a "development index").
Elasticities come from the first-order conditions in exact log-linear form (log quantity ratio on log price ratio), nest by nest, set to match the two extremes of the sample (poorest and richest), not by regression.
Estimates: capital-labour in agriculture **sigma1 = 1.90** (Herrendorf et al. 2015: 1.58; non-agriculture 0.98); the other two nests 0.66 and 1.75 (the paper's own nesting description and its text disagree on which of land or intermediates is which; I read 0.66 as land versus the capital-labour nest and 1.75 as intermediates).
They state that micro studies find much lower elasticities and that their function is a reduced form. The paper has no panel, no fertility outcome and no farm-exit regression: its mechanism is that falling capital and intermediate prices relative to wages pull labour out of farming.

**Like-for-like check of our CES 0.43** (`input_prices_boppart.py`, Part 1; our capital and intermediate quantities are USDA ERS per worker, price of capital is PWT `pli`, intermediate price is the world Pink Sheet fertiliser index, which has no cross-country variation):
- 2005 cross-section, slope of log(K/L) on log(w/Pk): **+1.36 (+-0.22)**; poorest-vs-richest-decile arc elasticity **1.57** (quantity x549 against price x55). Intermediates M/L on w/Px: +1.48 (+-0.25), arc **1.64**. These sit right next to their 1.90 and 1.75.
- Annual levels, country and year effects (our CES design): K/L +0.41 (+-0.16); this reproduces the 0.43. Ten-year changes with country and year effects: K/L +0.12, M/L +0.41.
- So 0.43 is not a different answer to their question. It is the within-country, time-series elasticity; their 1.9 is the long-run development gradient across countries. The same data give 1.4 to 1.6 across countries and 0.1 to 0.4 within countries. Labelling 0.43 as "the" structural elasticity and contrasting it with Boppart was a category error in both directions; it cannot refute their calibration. Their own reading, that micro estimates are lower, fits.

**Input-price test redone to their set-up** (Part 2, true-log income, level, 10-year change and change x exposure all controlled; 95% half-widths):
- Exposure = baseline farm share, world fertiliser price change: farm share +0.0117 (+-0.0081), with country trends +0.0071 (+-0.0049); paid-job share -0.0023 (+-0.0051), trends -0.0011 (+-0.0034); births +0.0001 (+-0.0008). Same picture as the earlier income-controlled rebuild: farm exit weak but positive (price up, farm share down more slowly), paid jobs and births zero.
- Relative price d log(Px/w) (their object, wage instead of GDP per head): farm share +0.0149 (+-0.0105), trends +0.0042 (+-0.0052, not significant); paid jobs -0.0035 (+-0.0077); births +0.0012 (+-0.0009).
- Exposure = baseline log intermediates per worker (their mechanism, farms that buy more inputs): farm share -0.0177 (+-0.0430) n.s.; paid jobs n.s.; **births +0.0094 (+-0.0045), trends +0.0059 (+-0.0032)**: the one cell that is significant in both. Births rise when the fertiliser price rises, more where farms use more purchased inputs. It is one of 36 cells with a hand-picked exposure; treat as a lead, not a finding.
- What cannot be done: BACI prices are not available here, so there is no country-specific intermediate price. With a global price, income and the price-times-exposure variable are close to collinear in the within dimension, so "disappears when income is controlled" is partly built in; in their model income (the development index) is a sufficient statistic. The honest reading: our data cannot distinguish a price effect from an income effect on farm exit or paid jobs; births show no response through the farm-share channel.


## 6. Panel branch checks
`bayes.py` (panel branch) rerun on freshly fetched WDI data reproduces `results/bayes/findings.txt` line for line (only runtime and a note line differ): the panel pipeline is deterministic and its `gdppc_log` is a true log (median 8.24, range 4.98 to 11.86 after `sweep.build`). Its income inclusion probabilities (lsc within 0.66; sec within 0.12; ter within 0.05) therefore stand. The full 380-pair `tight_tests.py` run finished afterwards (`results/tight_full_panel_orig.txt`, `tight_full_panel_a2fix.txt`): 78 of 380 pairs show a within-country lead as originally coded (77 in the 22 Nov file; bootstrap seeds differ), 79 with the A2 unit fix. The unit mismatch therefore changes almost nothing; the weakness of these leads is the single specification and the trend test, not the units.
