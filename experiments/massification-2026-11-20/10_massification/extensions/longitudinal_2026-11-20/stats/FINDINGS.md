**Short answer, in plain words.** Using the 30 countries on disk and the years 1995-2024, we asked the user's question in four different ways: across countries, within countries year by year, over five-year blocks, and over long differences. The headline is that **the literacy-versus-schooling-years horse race is not reproducible as a within-country finding in these data**: in the annual within-country panel the adult-literacy coefficient is 0.45 standardized units (95% CI -0.43 to 1.32) and the schooling-years proxy is 0.87 (-1.50 to 3.24). Verdict H1: **PARTIAL**. The verdict is PARTIAL rather than a clean null because the five-year-block panel tells a different story: there literacy is positive and significant at 1.52 (0.54 to 2.50) while the schooling-years proxy turns negative at -1.59 (-2.24 to -0.94) - the direction the 2015 exercise expected, but only at the lower frequency. That does not mean literacy is irrelevant; with only 127 annual observations across 23 countries, the literacy series is measured in scattered survey years, so a null here is a statement about what these data can resolve, not about what literacy does. For economic complexity (ECI), the same panel gives a standardized coefficient of -0.58 (-1.63 to 0.47); verdict H2: **NOT SUPPORTED**. For the 'has the economy kickstarted?' idea, ECI terciles give literacy slopes of 0.022 (low), 0.370 (mid) and -0.014 (high) growth points per literacy point, a high-minus-low difference of -0.036 (bootstrap 95% CI -0.647 to 1.642); verdict H3: **NOT SUPPORTED**. Nothing below is causal, nothing below claims a direction (growth pushing education or education pushing growth), and nothing below is a claim about Africa.

---

## 1. What was asked, and what was frozen before any run

The user's 2015 UIS/Excel experience: *years of schooling did not seem to move with GDP growth, but literacy did*. The question restated here: in a longitudinal panel, does literacy co-move with GDP growth where years of schooling does not, and does economic complexity (ECI) gate that association, with a threshold below which the economy has not "kickstarted"?

Everything in this directory implements `PRE_DECLARATIONS.md` (sha256 `bff1c3ec39cdd76d984e04038cafac6124073714642e2794c0fc87eba7270d91`) exactly: specifications S1-S8, the four robustness variants, hypotheses H1-H4 with their frozen thresholds, the declared `MYS_proxy`, the verdict vocabulary, listwise deletion with no imputation. No threshold was changed after seeing a number.

**Declared derived proxy** (`derived`, used only as the years-of-schooling side of the horse race):

```
MYS_proxy = 6 + 6*(SE.SEC.CUAT.LO.ZS/100) + 3*(SE.SEC.CUAT.UP.ZS/100) + 4*(SE.TER.CUAT.BA.ZS/100)
```

It is an attainment-based approximation, **not** a measured mean years of schooling. It assumes 6 years of primary for everyone, adds 6 for at-least-lower-secondary, 3 for at-least-upper-secondary and 4 for tertiary attainment. Cells are used only where all three components are observed (193 of 895 country-years in the window).

**All coefficients reported in this file are standardized** (outcome and each regressor divided by its pooled sample SD over the estimation sample), so literacy and `MYS_proxy` are directly comparable: a coefficient is the change in growth, in units of its own pooled SD, per one pooled SD of the regressor. The raw (unstandardized) coefficients are in the per-specification CSVs (`coef_raw`) and are quoted where the units matter (H3 tercile slopes, in growth percentage points per literacy percentage point).

## 2. Headline verdicts (predeclared thresholds, computed by `code/run.py`)

| Hypothesis | Verdict | What decided it |
|---|---|---|
| **H1** literacy moves, schooling years does not | **PARTIAL** | S2 literacy CI includes 0 but S3 (5-year blocks) literacy is significant -> not a stable within-country association. |
| **H2** ECI matters | **NOT SUPPORTED** | ECI is not positive-significant in S2 or S3, so the frozen threshold (positive with CI excluding 0 in BOTH) fails; its S3 coefficient is significantly NEGATIVE. |
| **H3** ECI gates the association | **NOT SUPPORTED** | high and low tercile slopes do not share a sign. |
| **H4** what moves together | **SUPPORTED** | 45 of 45 pairs have n>=20; 17 reach |r|>=0.4 with permutation p<0.05; 17 also pass the sign-stability checks. |

Verdict vocabulary: `SUPPORTED` / `NOT SUPPORTED` / `PARTIAL` / `DATA LIMITED` / `UNABLE`, plus `NULL` in the specification rows of `results/RESULTS.csv`, where `NULL` means *no predeclared threshold applies to this descriptive cell* and **is not a null result**.

## 3. H1 - the 2015 horse race, re-run longitudinally

Standardized coefficients, literacy versus `MYS_proxy` (95% CI in brackets; CR1 clustered by country):

| Specification | literacy | `MYS_proxy` (derived) | ECI | n | clusters |
|---|---|---|---|---|---|
| S1 cross-section (1995-2024 means) | 0.273 [-0.088, 0.634] | -0.285 [-1.122, 0.552] | -0.025 [-0.537, 0.486] | 25 | 25 |
| S2 annual, country+year FE | 0.447 [-0.426, 1.320] | 0.871 [-1.502, 3.243] | -0.581 [-1.632, 0.469] | 127 | 23 |
| S3 5-year blocks, country FE | 1.520 [0.540, 2.500] | -1.591 [-2.242, -0.940] | -2.589 [-4.112, -1.067] | 62 | 25 |
| S4 long differences (2015-24 minus 1995-2004) | DATA LIMITED | DATA LIMITED | DATA LIMITED | 5 | 5 |

S4 is `DATA LIMITED` by the predeclared minimum (n >= 20 observations and >= 8 clusters for a FE slope): only **5 countries** (CHN;LKA;MNG;MYS;SGP) have literacy, MYS_proxy, ECI and growth observed in *both* the 1995-2004 and the 2015-2024 windows. No workaround was substituted: the cell is reported as unestimable rather than redefined.

Adjudication against the frozen H1 rule (S2 is the declared test bed): S2 literacy CI includes 0 but S3 (5-year blocks) literacy is significant -> not a stable within-country association.

Reading, in the predeclaration's own words: the result is a statement about what these data can and cannot resolve, i.e. *with these data*, whether literacy moves with growth and the schooling-years proxy does not. It says nothing about whether literacy matters in a causal sense.

## 4. H2 and H3 - does economic complexity move with growth, and does it gate the link?

**H2 (NOT SUPPORTED).** ECI standardized beta = -0.581 [-1.632, 0.469] in S2 (n=127, 23 clusters) and -2.589 [-4.112, -1.067] in S3 (n=62, 25 clusters). ECI is not positive-significant in S2 or S3, so the frozen threshold (positive with CI excluding 0 in BOTH) fails; its S3 coefficient is significantly NEGATIVE. Note that ECI enters a regression that also contains the derived `MYS_proxy` and urban share.

**H3, the "has the economy kickstarted?" threshold.** Terciles are formed on within-country-demeaned ECI, so a country is classified by whether its complexity is high or low *for that country*, not by whether it is rich. Literacy slopes are raw growth percentage points per literacy percentage point, estimated with country FE inside each tercile and standardized on the pooled S2 scale so the three cells are comparable.

| ECI tercile (within-country) | literacy slope | n | countries |
|---|---|---|---|
| low | 0.0220 (std 0.088, CI [-1.412, 1.588]) | 43 | 18 |
| mid | 0.3696 (std 1.477, CI [-1.318, 4.272]) | 42 | 17 |
| high | -0.0144 (std -0.058, CI [-1.308, 1.193]) | 42 | 18 |

High minus low literacy slope = **-0.0365** raw growth points per literacy point (std -0.146), cluster bootstrap over countries 95% percentile CI [-0.6468, 1.6417] with 992/1000 estimable draws (seed 20261726). The predeclared threshold requires the high slope to exceed the low slope by at least 50% of the low magnitude, with the same sign and a CI excluding zero. Observed relative difference: -1.65x the low slope. Verdict: **NOT SUPPORTED**.

This is the closest thing in the battery to the user's "the economy has not kickstarted" intuition, and the honest reading is in the verdict: the point estimates are ordered as the intuition predicts only if they are, the CI is wide, and the sample of countries behind each tercile cell is 13-16. It is not an Africa claim: only five of the 30 countries are African (EGY, KEN, MAR, NGA, ZAF) and no country-level reading is made here.

## 5. S5 interaction and S7 reverse check

S5 adds literacy x ECI and MYS x ECI to the S2 model: literacy x ECI = -0.832 [-6.420, 4.755], MYS x ECI = -0.742 [-3.695, 2.211] (n=127, 23 clusters). This is descriptive; the predeclared H3 test is the tercile split above, not this interaction term.

S7 is a **symmetry check only**: 5-year changes in the education series are placed on growth lagged five years, with the same FE. It is recorded here so that a reader can see the association is symmetric-looking in both orderings, which is precisely why nothing in this battery is a direction claim:

| outcome (5-year change) | growth(t-5) std beta | n | clusters |
|---|---|---|---|
| delta_lit | -0.093 [-0.320, 0.133] | 131 | 23 |
| delta_MYS | -0.059 [-0.219, 0.100] | 89 | 15 |
| delta_eci | 0.085 [-0.070, 0.240] | 745 | 30 |

The audits' corrected push-pull orientation (income growth -> tertiary GER is the correctly-oriented association; education -> growth is null) is recorded in the predeclaration and in this battery's design, but **it is not a direction result here** (R13). No sentence in this file should be read as "education pushes growth" or "growth pulls education".

## 6. H4 - what actually moves together (S8)

The full 45-pair within-country matrix is `results/S8_comovement.csv` (45 pairs, 1000 within-country permutations per pair, seed 20261928). 45 pairs have n >= 20; 17 reach |r| >= 0.4 with permutation p < 0.05; 17 also survive the sign-stability checks across adult/youth literacy and across the two attainment levels tested.

| pair | within-country r | n | countries | permutation p | stable |
|---|---|---|---|---|---|
| cuat_up ~ MYS | 0.920 | 193 | 27 | 0.0010 | yes |
| lit ~ lit_youth | 0.909 | 274 | 28 | 0.0010 | yes |
| cuat_ba ~ MYS | 0.830 | 193 | 27 | 0.0010 | yes |
| cuat_up ~ cuat_ba | 0.684 | 207 | 27 | 0.0010 | yes |
| lsec_cmpt ~ urban | 0.674 | 516 | 28 | 0.0010 | yes |
| prm_cmpt ~ lsec_cmpt | 0.652 | 459 | 28 | 0.0010 | yes |
| cuat_up ~ urban | 0.590 | 418 | 30 | 0.0010 | yes |
| lit ~ lsec_cmpt | 0.589 | 189 | 26 | 0.0010 | yes |
| lit_youth ~ prm_cmpt | 0.585 | 205 | 27 | 0.0010 | yes |
| prm_cmpt ~ urban | 0.545 | 520 | 28 | 0.0010 | yes |
| lit_youth ~ lsec_cmpt | 0.535 | 216 | 27 | 0.0010 | yes |
| lit ~ prm_cmpt | 0.528 | 178 | 26 | 0.0010 | yes |
| lit ~ urban | 0.518 | 274 | 28 | 0.0010 | yes |
| lit ~ cuat_up | 0.517 | 222 | 27 | 0.0010 | yes |
| MYS ~ urban | 0.499 | 193 | 27 | 0.0010 | yes |
| lit_youth ~ urban | 0.468 | 314 | 28 | 0.0010 | yes |
| lit ~ MYS | 0.432 | 127 | 23 | 0.0010 | yes |

**The five strongest co-movements** (|r| >= 0.4, permutation p < 0.05, n >= 20): cuat_up~MYS (r=+0.920, n=193, p=0.0010); lit~lit_youth (r=+0.909, n=274, p=0.0010); cuat_ba~MYS (r=+0.830, n=193, p=0.0010); cuat_up~cuat_ba (r=+0.684, n=207, p=0.0010); lsec_cmpt~urban (r=+0.674, n=516, p=0.0010).

The pairs that dominate are the ones where the two series are measurement-adjacent (adult with youth literacy, primary with lower-secondary completion, upper-secondary with tertiary attainment, and `MYS_proxy` with the attainment levels it is built from). That is a finding about the data rather than about economies: the education series move together far more reliably than any of them moves with growth. Nothing here is a direction claim and no pair is interpreted causally.

**What moves with growth, specifically.** None of the nine growth pairs reaches |r| >= 0.4: growth~lit (r=-0.091, n=274, p=0.068); growth~lit_youth (r=-0.079, n=314, p=0.094); growth~prm_cmpt (r=-0.006, n=520, p=0.877); growth~lsec_cmpt (r=-0.029, n=516, p=0.519); growth~cuat_up (r=-0.132, n=418, p=0.013); growth~cuat_ba (r=-0.191, n=225, p=0.014); growth~MYS (r=-0.203, n=193, p=0.014); growth~eci (r=-0.153, n=895, p=0.001); growth~urban (r=-0.089, n=895, p=0.002). The largest is growth~MYS at r=-0.203, so within countries the growth side of the horse race is weak for *every* education series tested, and ECI's within-country growth correlation is negative and significant at the conventional level. That is consistent with the negative ECI coefficient in S3 and is the reason H2 is read as NOT SUPPORTED rather than reversed.

## 7. Robustness (all four predeclared variants, no extra ones)

| variant | spec | literacy | `MYS_proxy` | ECI | n | clusters |
|---|---|---|---|---|---|---|
| ECI HS92 instead of SITC | S2 | 0.507 [-0.323, 1.337] | 0.810 [-1.476, 3.096] | -0.962 [-2.290, 0.366] | 127 | 23 |
| ECI HS92 instead of SITC | S3 | 1.599 [0.817, 2.382] | -1.359 [-1.967, -0.752] | -2.968 [-5.298, -0.637] | 62 | 25 |
| exclude HKG and SGP (city-states) | S2 | 0.468 [-0.349, 1.284] | 0.817 [-1.287, 2.920] | -0.633 [-1.699, 0.433] | 115 | 22 |
| exclude HKG and SGP (city-states) | S3 | 1.512 [0.519, 2.506] | -1.483 [-2.122, -0.844] | -2.438 [-3.939, -0.938] | 59 | 24 |
| exclude 2020-2021 (COVID) | S2 | 0.482 [-0.602, 1.565] | 0.963 [-2.653, 4.578] | -0.975 [-1.892, -0.058] | 111 | 22 |
| exclude 2020-2021 (COVID) | S3 | 1.466 [0.375, 2.556] | -0.978 [-1.824, -0.132] | -2.461 [-4.803, -0.119] | 55 | 24 |
| youth literacy instead of adult literacy | S2 | 0.373 [-0.059, 0.805] | 0.520 [-1.411, 2.451] | -0.548 [-1.557, 0.462] | 134 | 24 |
| youth literacy instead of adult literacy | S3 | 0.309 [-1.042, 1.661] | -1.191 [-2.060, -0.322] | -2.281 [-4.045, -0.517] | 62 | 25 |

The four variants were fixed in advance; none was added after looking at the baseline. They are reported in full in `results/ROBUSTNESS.csv`, including cells that lose significance.

## 8. Honest limits (read before quoting any number)

1. **Literacy is survey-sparse.** The adult literacy series on disk has 275 country-year rows over 1995-2024 for 28 countries, and only 127 rows across 23 countries survive listwise deletion once literacy, the three attainment components of `MYS_proxy`, ECI and urban share are required together. Many countries contribute 1-5 observations. A coefficient estimated from such a panel is weakly identified; the CIs, not the point estimates, are the finding.
2. **`MYS_proxy` is crude and is not measured years of schooling.** It is an attainment-stock approximation with fixed years-per-level weights (6/3/4). It can be wrong in level and in trend, and it is labelled `derived` everywhere.
3. **30 countries, not a sample of the world.** The on-disk panel is 30 countries chosen upstream; no population weights, no claims of representativeness.
4. **Only five African countries** (EGY, KEN, MAR, NGA, ZAF). Any "Africa" reading is out of scope; a Sub-Saharan extension is a DATA ASK, not a result.
5. **Annual growth is noisy** (weather, commodity prices, crises), which is why S3 averages over 5-year blocks and why S4 long differences were predeclared. S4 could not be estimated at all.
6. **No causal claim and no direction claim.** Every estimate is a conditional association. The reverse specification S7 was run as a symmetry check, and its non-null results are the reason no direction is claimed.
7. S1 is a cross-section of 30 country means with 4 regressors (df about 18): it is the weakest design in the battery and is reported only because the 2015 exercise was cross-sectional.
8. `SL.SRV.EMPL.ZS` (services employment) is sparse (450 rows / 15 countries) and is not used in any specification; it was predeclared as "reported only" and no specification depends on it.

## 9. Reproducibility

One deterministic script: `code/run.py` (seed 20261120; bootstrap draws `default_rng(20261726)`, permutation draws `default_rng(20261928)`; absolute paths; fixed CSV float format). Run twice and compared with `code/verify_repro.py`; the two runs' `results/*.csv` are byte-identical, and the per-file hashes are recorded in `RUN_MANIFEST.json` (`results_files`) and `REPRO_CHECK.json`. `run_utc` differs between runs, of course; it is the only field that does.

Result file hashes (sha256):

| file | sha256 |
|---|---|
| results/RESULTS.csv | `b04cbd32e4fbdd5f1e5726fe86d40e3bbfc05fd5aba7cd3978b9f9428a72171b` |
| results/ROBUSTNESS.csv | `b425566f74176bd375767eca068a444e546cb0a84c5805c9aa5b7983429bbeb3` |
| results/S1_cross_section.csv | `00d293a5bf4faea5d29b0200cbe3c55058d4655a0b0af3e849d6ccb69f04ad89` |
| results/S2_countryFE.csv | `3081aae154c463856702a4d7b302504ac6144699b3c9f0f77f44acbb36bf741e` |
| results/S3_five_year_blocks.csv | `c2e7d807b73bf148463442a3c3045a216c73d1f34432b78f0918da0c20f2d160` |
| results/S4_long_differences.csv | `664b4fd110881203eec3702d192d8f3e0f3f3e790c2bf035351ce83cef8862e2` |
| results/S5_interaction.csv | `a2203d0f0ab30b8aff38fc0ee2f50c52b104923e130267bcda8591ae9c3594b9` |
| results/S6_eci_terciles.csv | `5ec4fd4af49ffe2005fc5bde7926ef07418ad83f2739ac0867c86ac8632168be` |
| results/S7_reverse.csv | `7fa45059aecd7eba5fdd79c17c15da8bfcf5ab22d4f514747d79164b163a7bba` |
| results/S8_comovement.csv | `6ec2e80175452a651ad01baa9ddea2842c5ef60d3f2b648bac9222756dcc164b` |

`predeclarations_sha256` = `bff1c3ec39cdd76d984e04038cafac6124073714642e2794c0fc87eba7270d91` (verified unchanged by `run.py` before it runs). `run_utc` = 2026-11-20T14:01:33+00:00. Python 3.11.17, pandas 3.1.1, numpy 2.4.6.

### How to read `results/RESULTS.csv`

One row per hypothesis (H1-H4) and one row per specification (S1-S8). The `estimate`, `se`, `ci_low`, `ci_high` columns contain the **focal standardized coefficient** for that row; the `note` column carries the companion coefficients (the other side of the horse race, the tercile slopes, the bootstrap CI) so that the comparison is auditable from that file alone. `label` is `derived` when the reported quantity is on a construction (`MYS_proxy`, a long difference, an ECI tercile) and `observed` when it is on a raw series. `verdict` is `NULL` on descriptive specification rows: that means *no predeclared threshold applies*, not that the estimate is null.

Per-specification coefficient tables (all terms, raw and standardized, n and clusters on every row) are in `results/S1_cross_section.csv` ... `results/S8_comovement.csv` and `results/ROBUSTNESS.csv`.

