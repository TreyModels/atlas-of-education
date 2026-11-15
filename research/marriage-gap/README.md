# Why do unmarried Chinese women say they want marriage less than men do? A small-model test

*A worked example of building a small model with the six-rule gate. Every model number below is written into this file by `make_readme.py` from `results/*.json`; nothing is typed by hand. Re-run `python3 experiments.py && python3 make_readme.py` to regenerate. Tests: `python3 test_model.py`.*

## Puzzle

The Institute for Family Studies chart "Big marriage aspiration gap in China" (IFS-Wheatley Survey of Family Culture 2026) shows the percent of unmarried adults aged 18-34 who would like to get married someday, women / men: Egypt 83/95, Israel 85/92, United Kingdom 83/86, Ireland 88/78, United States 83/77, Korea 66/78, China 48/77, Japan 51/53. In mainland China 48% of women and 77% of men say yes, a gap of 29 points. Japan, with similarly low numbers, shows no gap. The gap is the puzzle: do Chinese women want marriage less, or is something about who is left unmarried making it look that way?

## Fact check

**Main doubt first.** The 48% for Chinese women comes from an online opt-in panel of 1,047 Chinese respondents, more educated than China as a whole, and the cell it is based on (unmarried women 18-34) is smaller still and unreported. The chart marks the China gap as significant at 95%, but the sample is not random, so that significance covers sampling noise only, not who joins an online panel. I have not seen the question wording, so I do not know whether "undecided" people were counted as not wanting to marry.

Short version of the rest (full table with a URL for every figure and a read-in-source / not-found label for each: `FACT_CHECK.md`):

- Survey: online opt-in panel (Lucid/Cint), 1,047 mainland Chinese respondents in all, fielded August 2026, weighted to UN margins. The question wording and the size of the unmarried 18-34 cells were not found.
- Independent surveys: The independent sources agree that Chinese women are less keen than men in some surveys (Youth League, Beijing), but not in Blair and Madigan. None reports a 48% versus 77% split. The chart's number is at the low end of what the independent sources would suggest for women and cannot be confirmed.
- Sex ratio at birth, UN WPP 2024, average over the 1992-2008 birth cohorts (those aged 18-34 in 2026): China 115.9, South Korea 112.1, Japan 105.4 boys per 100 girls. Only the UN series was read for China and Japan; Korea was partly cross-checked.
- Share of 30-34 year olds who had ever married in China, 2022, about 81.6% (a news report of a yearbook figure; used only to set the speed of marriage).

## Two rival explanations

- **DIVERGENCE.** Women in China really want marriage less than men do, for reasons such as family duties after marriage and risk. The sex ratio plays no part.
- **SELECTION.** Men and women want marriage equally. But the unmarried are not a random sample: where men outnumber women, women who want to marry are matched and leave the unmarried pool, while men who want to marry stay in it. Among the unmarried, the share of women who want marriage falls and the share of men stays high, with no difference in underlying preference.

## The observation that separates them

Decided before the model was built, and written down in `experiments.py`: **the age profile of the gap.** Selection acts only after people start to leave the pool, so it predicts a gap near zero among the youngest unmarried (18-22) that widens with age. Divergence predicts a gap that is already present at 18-22. Anything that shows the share wanting marriage by sex and single year of age separates them; a single country-wide pair of numbers, like the chart, cannot.

## The model in plain words

Everyone in one birth cohort is the same age and cohorts are the same size. Each year, unmarried people who want marriage meet; marriages happen at a fixed rate; people who do not want marriage never marry. Nobody dies, moves or divorces. Four parameters:

- **r**: the number of men per woman in each cohort (selection takes it from the sex ratio at birth; divergence sets it to 1).
- **p_m**: the share of men who want to marry, fixed for each person for life.
- **p_w**: the share of women who want to marry, fixed for life. SELECTION sets p_w = p_m.
- **m**: each year, the number of marriages is m times the smaller of the two groups (men or women who want marriage and are still unmarried) in a matched pair of cohorts. A larger m means marriage happens faster.
- Fixed, not fitted: men and women of the same age are matched (the main model); marriage is possible from age 20; ages 18-34 are reported. A robustness run has men marrying women two years younger.
- Output: among unmarried 18-34 year olds, the share who want to marry, by sex, overall and by age band. The overall figure is age-standardised in a simple way (each single age gets equal weight), because the chart is age-standardised; the unweighted pooled version is also stored in the JSON files and is smaller.
- m is pinned by one real figure: the share ever married by age 30-34 (pooled over both sexes) should be the census-style figure above. The window treated as realistic is 75% to 88%.

## Results

**Selection alone does not reach the observed gap at realistic values.** With the sex ratio from the data (r = 1.159), a common wish to marry of 90% and marriage speed m = 0.26 (set so that 81.6% have ever married by 30-34), it produces a 20-point gap (51% women vs 71% men) against 29 observed. It gets to 29 points only with a larger sex ratio (fitted r = 1.23 against 1.16 from the data) or with faster marriage and a very high common wish to marry.

### (a) How big a gap can selection alone make?

Sweep of 1680 runs: r from 1.00 to 1.20, a common p from 0.60 to 0.95, m from 0.05 to 1.0. The largest gap anywhere in the sweep is 67 points (r = 1.20, p = 0.95, m = 1.00); it needs everyone who wants marriage to marry almost at once, which no data I have checked supports. Within the ever-married window and r no higher than China's mean (1.16), the largest is 64 points at m = 1.00. 11% of all sweep cells reach the observed 29 points; among cells inside the ever-married window, 29% do. So the sweep alone cannot rule selection out: with r at or below China's, the sweep first reaches 29 points at m = 0.4, p = 0.95 (37 points), where 87.8% have ever married by 30-34, the top of the realistic window. The answer depends on the speed of marriage and on p, neither of which this chart can identify.

At the best-guess values (r = 1.159, p = 0.90, m = 0.26): gap 20 points overall. By age band (men minus women, points): 18-22 1, 23-26 11, 27-30 29, 31-34 44. Measured as a plain pooled share of all unmarried 18-34 year olds instead of age-standardised, the same run gives 6 points. The result is sensitive to this choice, so how the survey standardised its ages matters and was not found.

Robustness, men marrying women two years younger: the best-guess gap becomes 26 points, but part of that comes from men simply staying unmarried longer: with r = 1 and equal preferences the same setting gives 7 points. The fitted selection r under this setting is 1.19.

Gap at the best-guess p and m for several sex ratios (m re-set each time so that ever-married stays at the same figure):

| r | m | gap (points) |
|---|---|---|
| 1.000 | 0.17 | 0 |
| 1.050 | 0.19 | 5 |
| 1.100 | 0.21 | 11 |
| 1.150 | 0.25 | 18 |
| 1.159 | 0.26 | 20 |
| 1.200 | 0.38 | 33 |

### (b) Fit each rival to the China pair

Each rival has three free parameters and three targets (women 48%, men 77%, ever married by 30-34 81.6%). A close fit is therefore guaranteed and is not a test; the question is whether the implied parameters are believable.

| | r | p_m | p_w | m | ever married 30-34, women / men |
|---|---|---|---|---|---|
| SELECTION (p_m = p_w) | 1.23 | 0.92 | 0.92 | 0.31 | 91% / 74% |
| DIVERGENCE (r = 1) | 1.00 | 0.93 | 0.85 | 0.23 | 82% / 82% |
| MIXED (r from data) | 1.16 | 0.92 | 0.90 | 0.28 | 88% / 76% |

- SELECTION needs a sex ratio of 1.23 men per woman at entry. The data give 1.16 (UN WPP, births 1992-2008), so the required ratio is 6% above the birth ratio. Birth ratios are not marriage-market ratios (migration, deaths, the age gap), so this is close enough that selection cannot be dismissed, but it does not fit without stretching the sex ratio. The fitted p of 92% is the same for both sexes.
- DIVERGENCE needs only a 9-point difference in who wants marriage at all (p_m 93% vs p_w 85%), not a halving. In this model even a modest preference difference is magnified in the unmarried pool, because the group that wants marriage less is depleted faster. That is a result about the model: because about 82% of people marry by 30-34 and preferences are fixed here, no more than about 18% of people can be permanent non-wanters. The strong version of divergence, in which nearly half of Chinese women never want marriage, is not compatible with the census-style figure under fixed preferences. It is compatible only if wishes change over time or if the online sample is unrepresentative.
- If m is not tied to the ever-married figure, selection can fit with very different r and p: with m = 0.3 it needs r = 1.25; with m = 0.4 only r = 1.06, but then 94% would have married by 30-34, too many, and with m = 0.2 it needs r = 3.0 and only 38% marry. The ever-married figure is what makes the test informative.

### (c) The age profile of the gap (the observation fixed before building)

Gap, men minus women, in points, among unmarried people in each age band, at each rival's fitted parameters:

| Model (fitted to the China pair) | 18-22 | 23-26 | 27-30 | 31-34 |
|---|---|---|---|---|
| SELECTION | 2 | 17 | 44 | 60 |
| DIVERGENCE | 11 | 24 | 38 | 48 |
| MIXED (r from data) | 5 | 19 | 41 | 57 |

Both rivals predict a gap that grows with age, because people leave the pool as they marry. They differ at the youngest ages: 2 points for selection against 11 for divergence in the 18-22 band (mixed: 5). That is a difference of 10 points. If a survey had about 100 unmarried respondents per sex in that band (an assumption, not a known number), the sampling error of the gap would be about 5 points, so the difference would be about 1.4 standard errors: suggestive, not decisive. By single year of age the profiles are in `results/c_age_profile.json`.

How much of the gap does each mechanism carry? Mixed model, r from data, p_m and p_w both fitted (points):

| Total | Selection only (equal preferences, r from data) | Preferences only (fitted p_m, p_w, r = 1) | Interaction |
|---|---|---|---|
| 29 | 22 | 13 | -6 |

The mixed fit has a preference difference of 3 points (p_m 92%, p_w 90%). The two mechanisms do not add up: each alone gives a smaller or similar gap, and together they overlap. The split is a property of this particular model and should not be read as a measurement.

### (d) Cross-country consistency check (weak: three points)

With each country's sex ratio and a common p, and the China-calibrated m, selection predicts these gaps (points); chart in the last column. The chart's Korea gap is not significant, and the Japan gap has no significance label in the data we were given.

| common p | China (r = 1.159) | Korea (r = 1.121) | Japan (r = 1.054) |
|---|---|---|---|
| 0.6 | 10 | 8 | 4 |
| 0.75 | 14 | 12 | 6 |
| 0.9 | 20 | 17 | 11 |
| chart | 29 | 12 | 2 |

Ordering predicted at p = 0.9: China > Korea > Japan; chart: China > Korea > Japan. The ordering matches. But the size is off: Japan is over-predicted at high p (11 against 2), and Japan's own numbers imply a low common p, which is not common. A variant that sets p to each country's own chart average (which uses the outcome, so favours selection) gives China 10, Korea 11, Japan 3, where the ordering is Korea > China > Japan. With three points and free p this is a consistency check, not a test. Divergence makes no cross-country prediction without a story about why preferences differ. Countries where women exceed men on the chart (Ireland, the United States) are not explained by either mechanism here; their sex ratios were not checked.

## Verdict so far

The chart cannot tell the two explanations apart, because a single gap among the unmarried is produced by both. At the sex ratio the data give, selection by itself makes about 20 of the 29 points and needs a sex ratio about 6% higher than the birth data to make all of it, so a mixture, or selection plus a modestly higher effective sex ratio, is as consistent with the numbers as either pure story. The size of the preference difference that divergence needs (9 points) is much smaller than the headline suggests, so the chart does not show that Chinese women want marriage much less than men; it shows that the unmarried women are less keen, which is partly arithmetic. The headline number itself comes from a non-random online sample of 1,047 Chinese respondents, with other surveys giving different values for women. The next step is data on marriage intention by sex and single year of age, not more modelling of this chart.

## What data would settle it

A survey, or a survey wave, with: marriage intention by sex in single years of age (or at least 18-20, 21-23, and so on) and enough respondents in each cell, say several hundred per sex in the youngest band; ideally the same people followed for several years, so we can see who with a given stated wish marries (which would test the fixed-wish assumption), and the local sex ratio of each respondent. I have not verified that any specific survey has these. Candidates to check: the China Family Panel Studies, the Chinese General Social Survey, the Renmin University surveys of unmarried people, and the micro data of the IFS-Wheatley survey itself (to see the unmarried 18-34 cell sizes, the question wording and the age weighting). Marriage registration counts by sex and age are a separate check on how fast marriage happens (m).

## Limits

- Preferences are fixed for life. If people's wish to marry changes with age or experience, the ever-married figure no longer limits how many women can be non-wanters at a given moment, and the fixed-wish divergence fit is too restrictive.
- No deaths, migration, divorce or remarriage. The survey's 'not currently married' includes divorced people; the model's unmarried are never-married only.
- Marriages are one-to-one between the same age (main model) and the speed m is one number for everyone and every age. Real search is more complicated, including class and region matching, which can make local sex ratios much more extreme than the national one.
- The sex ratio at birth is used as the sex ratio of the pool. UN WPP values are smoothed and national series can differ (Korea: two sources differed by about 2 per 100 in some years).
- The ever-married anchor is one figure from a news report of a yearbook table, for both sexes, for 2022, and the window of 'realistic' values is my choice.
- The survey is an online opt-in sample; its weighting, question wording and cell sizes were not found. Significance in the chart covers sampling noise only.
- The age-standardisation here (equal weights across single years) is an assumption; a different standardisation changes the overall gap noticeably (see (a)).
- Both rivals fit the China pair exactly with three free parameters and three targets, so the fits cannot favour either. Only the age profile and independent data can.
- This is a model of a mechanism, not an estimate of how much of the real gap each mechanism explains.

## Files

`model.py` (the model), `experiments.py` (all experiments), `data_inputs.py` (sourced inputs), `FACT_CHECK.md` (sources), `results/*.json`, `make_readme.py` (this file's generator), `test_model.py`.
