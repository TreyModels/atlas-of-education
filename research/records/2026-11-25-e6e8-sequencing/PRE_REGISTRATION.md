# PRE-REGISTRATION — E6 + E8 + N3 (Sonnet Step 2)

Branch `research/e6e8-sequencing-2026-11-25`; record `research/records/2026-11-25-e6e8-sequencing/`.
Written and committed **before any analysis run** (first commit on the branch). Author `un-data`, 25 Nov 2026.
Box: `ssh autodl3` (32-core host, job uses 8 workers maximum). Server repo `/root/work/repo`.

## Purpose and frame

The sequencing paper's demand-timing test used series whose employment/wage coverage begins in 1991; Codex
F02/F12 established that the "7%" demand-first figure is a **series-start artefact** and called for
(a) removal of the inference, (b) exact original input hashes, and (c) a rebuild on pre-1990 series in common
windows. E8 rebuilds the fee-abolition event study with primary-source-verified dates and a
staggered-adoption-robust estimator. N3 replaces the take-off dating boundary rule with smoothing windows and a
left-truncated survival version. Framing throughout: descriptive/"consistent with"; no causal claim.

## E6 — demand timing on pre-1990 series

**Data (each series labelled OBSERVED / RECONSTRUCTED / IMPUTED in every table).**
1. GGDC 10-Sector Database (release 10sd_2023): employment share by sector, 1950+ for ~40-42 countries —
   **OBSERVED** (harmonised, RECONSTRUCTED for missing intermediates per GGDC documentation; label per series).
   Demand proxy D1 = non-agricultural employment share = 1 − agriculture employment share.
2. Penn World Table 10.01: `labsh` (labour share), `emp`, `rgdpna`, `pop` for controls/scale; 1950+ —
   **OBSERVED**.
3. WDI: urbanisation (SP.URB.TOTL.IN.ZS, 1960+), industry value added share (NV.IND.TOTL.ZS, 1960+),
   agricultural value added share (NV.AGR.TOTL.ZS, 1960+, median start later — selection reported),
   agricultural employment share (SL.AGR.EMPL.ZS, starts 1991 — used only as a labelled sensitivity, never as
   the pre-1990 test) — **OBSERVED** where published, model-based where WDI says modelled (label).

**Demand take-off rule (pre-registered).** For a demand series s at year t, onset = first year y in the window
with s(y+10) − s(y) ≥ +3.0 percentage points (D1 and industry share) or, for urbanisation, the same +3.0 pp rule;
annual data; a date equal to the first observable year is **left-censored**. No hindsight smoothing beyond a
3-year centred mean (robustness: 5-year).

**Schooling take-off rule.** As in the pre-registered sequencing code: first year y in the window with
mean years of schooling(y+10) − (y) ≥ +1.0 (5-year grid; robustness 0.5/1.5), from the committed long-run panel;
first grid year = left-censored.

**Comparison.** For each demand proxy, classify countries: both_exact (forward = demand before schooling,
reverse = schooling before demand), schooling_censored (forward), demand_censored (reverse_or_tie or
undetermined), both_censored (undetermined). **Report the full classification table per proxy and per window**,
plus the set of countries selected in, their first/last observable years, and the median lead.
**Decision rule:** if demand precedes schooling in more than one third of identifiable countries, Paper 1's
supply-led framing is softened to "schooling and structural change move together"; if fewer than 15%, the claim
is restated with the new numbers. In between: ambiguous, report bounds. **We do not re-derive or defend the 7%
figure, and treat F02/F12 as established.**

**Common windows.** Primary 1960–2010 (all series overlapping); robustness 1965–2010 and 1970–2015; demand
series restricted to years where that proxy is observed, schooling to shared years; selection counts reported.

## E8 — fee-abolition event study

**Dates.** The 12 from the massification-panel record: MWI 1994, ETH 1995, UGA 1997, LSO 2000, CMR 2000,
TZA 2001, ZMB 2002, KEN 2003, RWA 2003, MOZ 2004, BDI 2005, GHA 2005. Verify each against primary sources
(World Bank/UNICEF 2009 *Abolishing School Fees in Africa*; SFAI country notes; ministry decrees/Education Acts)
and resolve the documented conflicts by giving **both dates** with a preferred date and a source/page:
Cameroon 1999/2000; Ghana 1997/2005; Ethiopia 1994/1995; Tanzania 2001/2003; Malawi 1994/1995; Mozambique
2004/2005. Store `data/fee_dates.csv` (country, preferred year, alternative year, source, page/URL, conflict
note). Preferred-year choice rule: primary-source administrative date of national fee abolition; if sources
disagree on the administrative act vs rollout, prefer the act and record the rollout.

**Estimator (pre-registered).** Outcome: WDI primary GER (SE.PRM.ENRR), annual; second outcome lower-secondary
GER — WDI does not publish lower-secondary GER annually, so use UNESCO UIS lower-secondary GER if retrievable,
else WDI secondary GER (SE.SEC.ENRR) as a **proxy labelled as such**. Sample: Sub-Saharan African countries,
1990–2015; treated = the 12 cohorts; controls = never-treated SSA countries.
Main estimator: **Callaway–Sant'Anna with a universal base period g−1 and not-yet-treated controls**
(never-treated allowed when no not-yet-treated exists), ATT(g,t) for t = g−5..g+6, aggregated to event time by
cohort shares; country-cluster bootstrap (500) CIs. Comparison: TWFE event study (country and year FE, binned
endpoints) on the same sample. Pre-trends: ATT(g,g−2), ATT(g,g−3) and a joint test; reported before the
post-treatment table.
**Sensitivity:** every date ±1 year (preferred-year shifts, one at a time); leave-one-country-out; placebo
dates 6 years earlier for the pre-period. **Decision rule:** the first-stage claim of a large positive primary
GER effect with no pre-trend is kept only if it survives the CS estimator and ±1-year shifts; otherwise it is
reported as not robust.

## N3 — threshold smoothing and left-truncated survival dating

**Data.** Schooling: committed long-run panel (mean years of schooling). Release/demand: GGDC non-agricultural
employment share (E6 download) where available; WDI agricultural employment/VA only as labelled sensitivity.
**Dating variants (all pre-registered):**
1. q1 rule: 5-year grid, unsmoothed, Δ_s ∈ {0.5, 1.0, 1.5}; release Δ_r ∈ {2, 3, 5} pp/10y.
2. Smoothed: centred moving average windows 3, 5, 7 years applied to both series before the same threshold rule.
3. **Left-truncated survival dating:** discrete-time take-off model for schooling: hazard h(t) = P(take-off in
   year t | no take-off before t), estimated on the country-year panel with (a) countries whose take-off is
   observed, (b) left-truncated countries (first observed year already above the threshold interval) contributing
   only from their first observed year, (c) right-censored countries at the last observable year. Use a
   Kaplan–Meier-style non-parametric estimate with interval-censored first observation (take-off interval
   [first_year − 10, first_year]) and report median take-off year. Compare its implied event dates with the
   q1 dates; forward share computed from survival-dated schooling onset vs release onset from GGDC.
4. Table: forward share (identified), bounds (all), n identifiable, n undetermined, median lead — across all
   smoothing × threshold × dating definitions.
**Recommendation to Paper 1's abstract:** state the forward share as an interval with its selection and threshold
definitions (e.g., "X% among identifiable countries, bounds Y–Z% across all countries at threshold T; sensitive
to smoothing = ..."), and **never a bare percentage**. If the forward share falls below 75% in any definition
with ≥20 identifiable countries, the abstract must say threshold-sensitive.

## Outputs and discipline

`REPORT.md` + `data/` tables (`e6_classification.csv`, `e6_inputs_and_hashes.csv`, `fee_dates.csv`,
`e8_att_gt.csv`, `e8_event_study.csv`, `n3_table.csv`), scripts, and a claims→source map. Every table labels
series OBSERVED/RECONSTRUCTED/IMPUTED. Exact input hashes (sha256) recorded in `data/input_hashes.csv`; downloads
kept out of git if large, with URLs and hashes committed. No secrets; box credentials never committed.
Any deviation is listed in the report's deviations section with the reason.
