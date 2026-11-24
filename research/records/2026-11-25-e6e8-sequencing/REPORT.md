# E6 + E8 + N3 — sequencing repairs: REPORT

Branch `research/e6e8-sequencing-2026-11-25`; record `research/records/2026-11-25-e6e8-sequencing/`.
Pre-registration: `PRE_REGISTRATION.md`, commit **a2a116d**, pushed **before any analysis run**. Author `un-data`,
25 Nov 2026. Box `autodl3`; scripts in `scripts/`, tables in `results/`, input hashes in
`results/e6_inputs_and_hashes.csv`. Framing is descriptive throughout: "consistent with", never causal. The 7%
demand figure is **not re-derived and not defended** (Codex F02/F12: the 1991 series start manufactures it).

## 0. What was run, and what is labelled what

| series | role | label |
|---|---|---|
| GGDC 10-Sector Database (10sd_jan15_2014), employment by sector, 42 countries, 1947–2012 | demand proxy D1 = non-agricultural employment share (1 − AGR/SUM) | **OBSERVED** (harmonised; GGDC reconstruction for missing intermediates noted by GGDC) |
| WDI urbanisation (SP.URB.TOTL.IN.ZS), 1960–2025 | demand proxy D2 | **OBSERVED** |
| WDI industry value added share (NV.IND.TOTL.ZS), 1960–2025 | demand proxy D3 | **OBSERVED** |
| WDI agricultural value added share (NV.AGR.TOTL.ZS), 1960–2025 (median start later — selection reported) | demand proxy D4 (falls) | **OBSERVED** (selection caveat) |
| WDI agricultural employment share (SL.AGR.EMPL.ZS), 1991– | sensitivity only, never the pre-1990 test | **RECONSTRUCTED/modelled** (ILO modelled) |
| Long-run panel mean years of schooling (5-year grid, 1870–2020) | schooling take-off | **RECONSTRUCTED** (historical reconstruction) |
| PWT 10.01 (`labsh`, `emp`, `rgdpna`, 1950–2019) | context/labour share, income controls | **OBSERVED** — **not** used as a demand-timing proxy: PWT has no sectoral employment split, so it cannot date a structural take-off; stated rather than forced |
| WDI primary GER (SE.PRM.ENRR); WDI secondary GER (SE.SEC.ENRR) | E8 outcomes | **OBSERVED**; secondary GER is a **proxy** for the requested lower-secondary GER (WDI publishes no annual lower-secondary GER; no UIS annual series was retrieved in-session) |
| Fee dates | E8 treatment | 8 **VERIFIED** (novelty-review, task-49); 4 **UNRESOLVED**, excluded from main, sensitivity only |

## 1. E6 — demand timing on pre-1990 series

**Design.** Demand take-off = first year y in the series with s(y+10) − s(y) ≥ +3.0 pp (D1–D3; D4 uses ≤ −3.0 pp
because it falls); schooling take-off = first 5-year-grid year with schooling(y+10) − (y) ≥ +1.0. Onsets are
searched over each series' **full observed range**; a take-off equal to a series' first observable year is
left-censored and is classified as **demand-first, weakly** (a weak inequality, never called reverse — Codex
F14 discipline). Primary comparison uses the full overlap (1900–2012) because a 1960 start selects against
demand take-offs that happen before 1960; the pre-registered 1960–2010 window is reported as robustness with its
selection. This ordering is a **documented deviation** from the pre-registration (which named 1960–2010 primary)
made because the diagnostic showed the window itself selects.

**Results (demand-first share among identifiable countries; bounds over all countries).**

| proxy | sample (in-window / all with both series) | demand-first | schooling-first | weak tie (forward_or_tie) | undetermined | demand-first share among identifiable | bounds (all) |
|---|---|---|---|---|---|---|---|
| GGDC non-ag employment, 1900–2012 | 30 / 37 | 2 | 5 | 13 | 10 | **10.0%** | 6.7–40.0% |
| WDI urbanisation, 1900–2012 | 101 / 143 | 10 | 14 | 41 | 36 | **15.4%** | 9.9–45.5% |
| WDI industry VA share, 1900–2012 | 76 / 143 | 13 | 25 | 16 | 22 | **24.1%** | 17.1–46.1% |
| WDI agricultural VA share (falling), 1900–2012 | 83 / 143 | 9 | 21 | 18 | 35 | **18.8%** | 10.8–53.0% |
| GGDC non-ag employment, 1960–2010 (pre-registered window) | 9 / 37 | 1 | 3 | 3 | 2 | 14.3% | 11.1–33.3% |
| WDI urbanisation, 1960–2010 | 65 / 143 | 10 | 7 | 41 | 7 | 17.2% | 15.4–26.2% |
| WDI industry VA, 1960–2010 | 54 / 143 | 13 | 13 | 16 | 12 | 31.0% | 24.1–46.3% |
| WDI agricultural VA, 1960–2010 | 58 / 143 | 9 | 15 | 18 | 16 | 21.4% | 15.5–43.1% |

The full table (all proxies × windows) is `results/e6_summary.csv`; country-level dates, classification, and
selection are in `results/e6_classification.csv` and `results/e6_selection.csv`. Input hashes are in
`results/e6_inputs_and_hashes.csv` (sha256 for GGDC zip and dta, PWT dta, WDI zips, long-run panel, event dates).

**Reading.** On pre-1990 series, demand take-off precedes schooling take-off in **10–24% of identifiable
countries** (point estimates by proxy), below the pre-registered one-third threshold; **schooling-first is the
majority strict ordering** (18–33% strict schooling-first, with the remainder weak ties or undetermined). But the
weak-forward share is large (21–43% of in-window countries) because demand take-offs are frequently left-censored
at the series' first year: for those countries demand-first cannot be excluded, only weakly ordered. The honest
summary is therefore: **on pre-1990 data the strict ordering favours schooling-first in a majority of
identifiable cases, but demand-first is neither eliminated (10–24%) nor cleanly distinguished from weak ties
(another 21–43%)**; the paper's supply-led framing should be softened to "schooling and structural change move
together, with schooling typically but not universally first." The 7% figure is not used or re-derived.

**CORRECTION (see `ERRATUM.md` §A):** the "18–33% strict schooling-first" clause in the sentence above does not
reproduce from `results/e6_summary.json`; the recomputed range is **21.5–46.3% of identifiable countries**
(58.3–71.4% of strict orderings), and "majority strict ordering" should read "larger strict ordering". The original
sentence is left visible.

## 2. E8 — fee-abolition event study with verified dates

**Dates.** Main specification uses the 8 dates verified by the independent audit (task-49,
`research/codex-source-verification-2026-11-25` @ `bfb8c6f`, file `fee_dates.csv`): MWI 1994, ETH 1995,
UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005. The four unresolved dates (CMR, ZMB, RWA, BDI) are
**excluded from the main specification** and enter only the all-dates sensitivity, flagged. The verified table
with source, page, quote, and conflict resolution is committed at `data/fee_dates.csv`; conflict resolutions:
Ghana→2005 (national scale-up; 1997 is not a national abolition), Ethiopia→1995 (implementation; 1994 = policy
adoption), Tanzania→2001 (PEDP launch), Malawi→1994 (elimination), Mozambique→2004 (abolition),
Cameroon unresolved.

**PROVENANCE NOTE (see `ERRATUM.md` §B):** `fee_dates.csv` is byte-identical (sha256
`1a08d4652371f7a3c79a54725b79c48429a793e3d88252d170715018ddd8e2ab`) between `bfb8c6f` (the fee-date commit cited
above) and the verified branch head `9a0fd69`; the papers cite `9a0fd69`. The same note applies to the citation in
`scripts/e8_fee_event_study.py`. No data changes.

**Estimator.** Callaway–Sant'Anna with universal base period g−1 and not-yet-treated controls (never-treated
allowed), event time −5..+6, cohort-size aggregated, country-cluster bootstrap (500). TWFE event study (country
and year FE, binned endpoints, cluster by country) is the comparison. SSA sample, 1990–2015, WDI primary GER.
Seven treated countries have outcome data (one verified country lacks GER coverage); 25–30 control countries per
event.

**CORRECTION (see `ERRATUM.md` §D.1):** the verified-8 event table this paragraph describes has **28–30** control
countries per event; **25–30** is the all-12 sensitivity range. Original text left visible.

**Primary outcome (WDI primary GER), verified-8 dates.**

| event | CS ATT | boot SE | 95% CI | TWFE ATT | TWFE SE | treated n |
|---|---|---|---|---|---|---|
| −5 | 6.39 | 3.30 | −0.08, 12.86 | 12.15 | 3.65 | 6 |
| −4 | 1.35 | 3.93 | −6.35, 9.04 | 1.89 | 2.62 | 7 |
| −3 | −0.13 | 3.62 | −7.23, 6.98 | 1.14 | 2.38 | 7 |
| −2 | −0.03 | 1.74 | −3.43, 3.38 | 1.96 | 1.47 | 7 |
| 0 | **12.44** | 7.55 | −2.36, 27.24 | 12.88 | 4.76 | 7 |
| +1 | **23.82** | 11.11 | 2.05, 45.60 | 23.80 | 7.11 | 7 |
| +2 | **25.94** | 10.95 | 4.48, 47.40 | 25.77 | 6.83 | 7 |
| +3 | **22.12** | 8.42 | 5.62, 38.62 | 24.48 | 5.28 | 6 |
| +4 | **25.19** | 8.50 | 8.54, 41.84 | 26.73 | 5.54 | 7 |
| +5 | **28.56** | 9.67 | 9.61, 47.51 | 27.65 | 6.09 | 6 |
| +6 | **25.92** | 8.82 | 8.64, 43.20 | 21.05 | 5.22 | 7 |

Pre-trends: e=−2 −0.03 [−3.43, 3.38]; e=−3 −0.13 [−7.23, 6.98]; e=−4 1.35 [−6.35, 9.04]; e=−5 6.39
[−0.08, 12.86] on only 6 treated cohorts (weak evidence of a pre-trend at the earliest horizon; the −2/−3/−4
horizons are flat). Post-treatment: large positive effects, significant from +1 onward, with the on-impact (+0)
estimate positive but CI spanning zero.

**Sensitivity (mean post ATT, primary outcome, verified dates).** All dates +1: 12.31 (t0 10.37); all dates −1:
18.65 (t0 0.03); placebo dates −6 years: **−0.39** (t0 −0.24); all-12-dates set: 20.80 (t0 7.03); leave-one-out
range **18.17–26.16** (t0 7.00–13.94) — the sign and rough magnitude do not depend on any single country. The
±1-year shifts move the timing (on-impact estimate especially) but not the direction or the large post-period
effects.

**Secondary GER proxy (requested lower-secondary outcome; WDI secondary GER).** Post-period ATTs rise to
6.71 [−3.39, 16.82] at +5 and 6.07 [−0.01, 12.16] at +6; pre-trends flat; CIs include zero. Reported as a
**proxy with no clear detected effect**, not as a null.

**Decision-rule assessment.** The pre-registered first-stage claim (large positive primary GER effect with no
pre-trend) **survives the CS estimator and the ±1-year/leave-one-out checks in direction and rough magnitude**
(mean post 18–29 points against ~0 under placebo), with two honest caveats: the on-impact estimate is sensitive to
date shifts, and the treated sample is small (7–8) so CIs are wide and the +0 horizon includes zero. No causal
language is used: the finding is "consistent with" a fee-abolition effect on primary GER.

**CORRECTION (see `ERRATUM.md` §D.2):** "mean post 18–29 points" does not reproduce; the reproducible values are
12.31 / 18.65 / 20.80 / leave-one-out 18.17–26.16 / placebo −0.39, i.e. **12.3–26.2 across the ±1-year and
leave-one-out checks, against −0.39 under the placebo**. Original text left visible.

## 3. N3 — threshold smoothing, left-truncated survival dating, and the abstract rule

**Design.** Schooling threshold Δ_s ∈ {0.5, 1.0, 1.5} (5-year grid); demand threshold Δ_r ∈ {2, 3, 5} pp/10y;
demand smoothing windows 3, 5, 7 years (centred moving average); schooling is on a 5-year grid, so 3/5/7-year
windows collapse to the same points — stated, not faked. Dating variants: q1 unsmoothed; smoothed demand;
left-truncated survival dating of schooling onset (observed onset, or for left-censored countries the empirical
median observed onset conditional on onset ≤ first observable year; lower/upper bounds of the censoring interval
give the range). Ties remain weak inequalities.

**Result (`results/n3_table.csv`, 54 definitions; all have ≥20 countries).** The **demand-first strict share
ranges 0.0–30.8% across definitions, median 10.45%**; the **weak forward-or-tie share ranges 56–84%** (ties and
left-censoring dominate because GGDC demand take-offs are often at the series start). The q1 default
(Δ_s=1.0, Δ_r=3.0, no smoothing, 34 countries): demand-first strict **6.2%**, weak tie **70.6%**, schooling-first
**17.6%**, undetermined 5.9%; bounds over all countries 5.9–82.4%. Left-truncated survival dating changes the
dates but not the qualitative picture (table rows `survival-lower/upper`). **Every definition with ≥20
identifiable countries is below the 75% forward threshold** in the pre-registered sense (the share of
definitions below 75% is 100%) — i.e., the ordering is threshold- and series-sensitive and cannot be quoted as a
single percentage.

**CORRECTION (see `ERRATUM.md` §C):** the "56–84%" weak forward-or-tie range in the sentence above does not
reproduce from `results/n3_table.csv`; the reproducible quantities and their denominators are given in §C. The
original sentence is left visible.

**Recommendation for Paper 1's abstract (demand-ordering claim).** State it as an **interval with selection and
threshold**: e.g. "on pre-1990 demand series, demand take-off precedes schooling take-off in 10–24% of
identifiable countries (bounds 7–53% over all countries), with another 21–43% weak ties/left-censored; the strict
schooling-first share is threshold- and smoothing-sensitive." Do **not** quote the old 7% (retracted,
series-start artefact) or a bare 31/34. For the **separate schooling-vs-fertility ordering** claim, use Paper M's
corrected figures (strict schooling-first 37.5% (24/64, CI 26.6–50.0), simultaneous 31.25%, fertility-first
31.25%; all-81 35.8%) — the two orderings must never be merged (see Council record and Codex F14).

## 4. Deviations, limits, and what cannot be said

1. **E6 primary window** (documented deviation): full overlap 1900–2012 is reported as primary; the
   pre-registered 1960–2010 window is robustness because it selects against pre-1960 demand take-offs.
2. **Demand-censoring classification** adapted: with pre-1990 series, a demand take-off at the first observable
   year means demand-first weakly, not the reverse_or_tie convention that applied to the 1991-start release
   series. Both are labelled; the weak category is reported separately.
3. **PWT** has no sectoral employment split; it is used for context/labour-share only, not as a demand-timing
   proxy. This is stated rather than forced.
4. **N3 schooling smoothing** collapses on the 5-year grid; the 3/5/7-year windows are effectively identical for
   schooling and are documented as such.
5. **E8 lower-secondary GER**: WDI has no annual lower-secondary GER; secondary GER is a labelled proxy. The
   4 unresolved fee dates are excluded from the main specification and included only in the all-dates
   sensitivity.
6. **Sample sizes**: E8 has 7–8 treated countries; the event-0 CI includes zero and the earliest pre-trend
   horizon is imprecise. E6/N3 demand identification is limited by GGDC's 42 countries and by left-censoring.
7. **Box sharing**: the box also ran E1; the E8 bootstrap briefly used the pool before the 2-core notice; all
   runs are complete and no further compute is required for this record.
8. No causal claim is made anywhere; "consistent with" is the strongest language used.

## 5. Reproduction

```
# on autodl3, /root/work/e6e8 (venv: numpy/pandas/scipy)
bash scripts/download_data.sh            # GGDC zip, PWT dta, WDI indicator zips (URLs in e6_inputs_and_hashes.csv)
./venv/bin/python scripts/e6_demand_timing.py
./venv/bin/python scripts/e8_fee_event_study.py
./venv/bin/python scripts/n3_threshold_survival.py
```
Input hashes: `results/e6_inputs_and_hashes.csv` (sha256 for every raw and copied input). Fee dates:
`data/fee_dates.csv` (verified by novelty-review; see its `README.md` and quote locators).

## 6. Claims → source map

| claim | number | source file | field |
|---|---|---|---|
| E6 demand-first share, full overlap, GGDC | 10.0% (2/20 identifiable; 30 in-window) | results/e6_summary.csv | forward_share_identified, proxy=ggdc_nonag_emp, window=1900-2012 |
| E6 demand-first share, full overlap, urban | 15.4% (10/65) | results/e6_summary.csv | same, proxy=urban |
| E6 demand-first share, full overlap, industry VA | 24.1% (13/54) | results/e6_summary.csv | same, proxy=ind_va |
| E6 demand-first share, full overlap, agri VA | 18.8% (9/48) | results/e6_summary.csv | same, proxy=agri_va |
| E6 bounds | 6.7–53.0% across proxies | results/e6_summary.csv | forward_lower_bound_all, forward_upper_bound_all |
| E8 CS post effects | +1 23.82 [2.05,45.60] … +6 25.92 [8.64,43.20] | results/e8_event_SE.PRM.ENRR_verified8.csv | att, ci_lo, ci_hi |
| E8 pre-trends | −2 −0.03 [−3.43,3.38]; −3 −0.13 [−7.23,6.98] | same | event −2/−3 rows |
| E8 placebo | −0.39 mean post | results/e8_sensitivity.csv | spec=placebo-6, mean_att_post |
| E8 leave-one-out | 18.17–26.16 | results/e8_sensitivity.csv | drop-* rows |
| N3 demand-first strict range | 0.0–30.8%, median 10.45% | results/n3_table.csv / n3_recommendation.json | forward_share_identified |
| N3 q1 default | 6.2% strict, 70.6% weak tie, 17.6% schooling-first | results/n3_recommendation.json | q1_default |
