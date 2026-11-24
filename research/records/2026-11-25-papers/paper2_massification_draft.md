# Massification before Industrialization: schooling take-off, structural change, and fee abolition in sub-Saharan Africa

**Draft — Paper #2 of the Atlas of Education project. Working paper, 25 November 2026.**
Not for circulation outside the project. Every number below is traceable to a committed file at a named branch and
commit; the source-key table in Appendix A resolves the `[S#]` tags used in the text and tables. Cell-level
provenance notes are in Appendix B. Evidence base: two auditor-cleared pillars only — **E6** (pre-1990 demand
timing) and **E8** (fee-abolition event study with page-located dates), plus the **E8 Fisher randomization
inference** (RI) record and one **E1** procedural context line. No simulation or illustrative output is cited as
empirical evidence. No causal language is used beyond what the designs identify.

---

## Abstract

Most accounts of mass schooling are demand stories: families and states buy schooling because the returns to
literacy and numeracy rise with industrialisation and structural change. This paper asks about **timing**. On
pre-1990 structural-change series covering up to 143 countries, we date the take-off of schooling (a sustained rise
in mean years of schooling, 1870–2020 reconstruction) and of demand (non-agricultural employment, urbanisation,
industry value added, agricultural value added), and classify their order. Across four full-overlap (1900–2012)
proxies, demand take-off precedes schooling take-off in **10.0–24.1% of identifiable countries**; schooling-first
is the **larger strict ordering at 21.5–46.3%** of identifiable countries (**58.3–71.4%** of strict orderings); all-
country bounds are **6.7–53.0%**, and **21–43%** of in-window countries are weak ties or left-censored. Across 54
threshold/smoothing definitions the strict demand-first share ranges **0.0–30.8%** (median 10.45%): the ordering is
sensitive to the dating rule and is not a fixed percentage. Separately, in eight sub-Saharan African countries with
fee-abolition dates located to named pages/boxes in World Bank/UNICEF (2009) volumes, a staggered-adoption event
study finds Callaway–Sant'Anna post-period primary-enrolment ATTs of **+22.12 to +28.56 points**; the on-impact
estimate is **+12.44** with a 95% CI that includes zero; pre-trends at −2/−3/−4 are flat; a −6-year placebo gives
**−0.39**; leave-one-out mean posts range **18.17–26.16**; and Fisher randomization inference over 10,000
placebo-date and 10,000 placebo-country re-assignments places the observed abolition-year ATT (**12.4436**) in the
extreme tail (two-sided p = **9.999e-05** and **5.999e-04** respectively). The two pillars are **consistent with**
schooling and structural change moving together, with schooling typically but not universally first, and with fee
abolition followed by large primary-enrolment gains. Nothing here identifies a causal effect of abolition or of
schooling; the paper's own headline ordering is measurement-limited (a schooling-stock take-off, not enrolment-
threshold crossing) and its biggest inferential limit is the 7–8-country treated sample.

**Keywords:** mass schooling; structural transformation; fee abolition; event study; randomization inference;
late industrialisation.

---

## 1. Introduction

The standard economic account treats mass schooling as a **response**: returns to skill rise with industrialisation
and technological change, and families and governments invest accordingly [cite: human-capital tradition]. A
supply-led account reverses the emphasis: states build school systems, and enrolment expands ahead of, or alongside,
economic demand [cite: Pritchett, supply-led schooling; cite: world-polity tradition]. The two accounts make
different predictions about **order**, and order is measurable in a way that "importance" is not.

This paper makes two bounded empirical moves. First, it dates take-offs on **pre-1990 series** and asks whether the
demand take-off precedes the schooling take-off. Pre-1990 is the operative word: an earlier project estimate using
a 1991-start wage-employment series produced a 7% demand-first figure, which the project has **retracted as a
series-start artefact** (Codex F02/F12; recorded in `[S14]`). Second, it studies one supply-side policy family —
**fee abolition** — in eight sub-Saharan African countries whose abolition dates are located to named pages/boxes,
using a staggered-adoption event study and an independent randomization-inference check.

The contribution is measurement and honest bounds, not a new direction of history. The claim, stated at the
strongest level the evidence permits, is: **on pre-1990 series, schooling and structural change move together, with
schooling typically but not universally first, and the ordering is threshold-sensitive; fee abolition in the
eight dated countries is followed by large primary-enrolment gains, without a causal identification.** We also
report what the evidence does **not** show, in §6.

The paper is deliberately narrow. It does not import the historical case narrative (Prussia/Britain/France/US),
the agricultural-floor model, or any simulation output; those belong to other project records, and the historical
dates in particular are labelled UNVERIFIED literature standard there. Section 2 describes the data and their
tiers, §3 the two designs, §4 the results, §5 robustness, §6 negatives, §7 replication status.

---

## 2. Evidence base and measurement tiers

### 2.1 E6 — pre-1990 demand timing

The E6 record `[S1–S5, S15, S16]` uses four demand proxies and one schooling series:

| series | role | evidence tier (as labelled in the record) | provenance |
|---|---|---|---|
| GGDC 10-Sector Database, employment by sector, 42 countries, 1947–2012 | demand proxy D1 = 1 − agricultural employment share | **OBSERVED** (harmonised; GGDC reconstructs missing intermediates) | archive `10sd_jan15_2014.zip`, sha256 `061a0767…` `[S15]` |
| WDI urbanisation `SP.URB.TOTL.IN.ZS`, 1960–2025 | demand proxy D2 | **OBSERVED** | WDI API zip, sha256 `0f0f5e09…` `[S15]` |
| WDI industry value added `NV.IND.TOTL.ZS`, 1960–2025 | demand proxy D3 | **OBSERVED** | sha256 `5c987a43…` `[S15]` |
| WDI agricultural value added `NV.AGR.TOTL.ZS`, 1960–2025 | demand proxy D4 (falls) | **OBSERVED** (selection caveat) | sha256 `adb17a1c…` `[S15]` |
| Long-run panel, mean years of schooling, 5-year grid, 1870–2020 | schooling take-off | **RECONSTRUCTED** (historical reconstruction) | `long_run_panel.csv`, sha256 `cd30d7ea…` `[S15]` |
| WDI agricultural employment `SL.AGR.EMPL.ZS`, 1991– | sensitivity only, never the pre-1990 test | **RECONSTRUCTED/modelled** (ILO modelled) | sha256 `3b5e81a8…` `[S15]` |
| PWT 10.01 (`labsh`, `emp`, `rgdpna`) | context only | **OBSERVED**; **not** a demand-timing proxy (no sectoral employment split) | `pwt1001.dta`, sha256 `746a4836…` `[S15]` |

Two measurement caveats are structural and travel with every E6 number. (i) "Massification" is dated by a
**reconstructed mean-years-of-schooling take-off**, not by secondary or tertiary **enrolment-threshold crossing**;
the paper's title is therefore a shorthand, and a clean enrolment-massification test would need new series (see
§6). (ii) "Industrialization" is proxied by broad structural-change shares; no manufacturing-only onset is run in
the E6 record. (iii) The pre-registration text names GGDC release `10sd_2023`, while the downloaded and hashed
archive is the **2014** 10-Sector release (`10sd_jan15_2014.zip`); the results are on the 2014 release, and the
vintage mismatch must be reconciled before submission (§7).

### 2.2 E8 — fee abolition dates

The E8 main specification uses **8 dates verified to named page/box locators** in World Bank/UNICEF (2009) volumes,
committed in `[S5]` (blob `85d09f86…`, byte-identical to the source-verification copy). Four further dates are
**UNRESOLVED** and excluded from the main specification; they enter only the all-dates sensitivity. Table 1 gives the
date table.

**Table 1. Fee-abolition dates as used (source: `[S5]`).**

| ISO3 | country | preferred year | alternative year | status | locator (source key) | conflict resolution |
|---|---|---|---|---|---|---|
| MWI | Malawi | **1994** | 1995 | VERIFIED | World Bank/UNICEF 2009 *Six Steps* Box 3.2; World Bank 2009 ch.5 `[S5]` | abolition 1994; 1995 = first full academic year |
| ETH | Ethiopia | **1995** | 1994 | VERIFIED | World Bank 2009 ch.2, PDF p.75 / printed p.49 `[S5]` | implementation 1995; 1994 = policy adoption |
| UGA | Uganda | **1997** | — | VERIFIED | *Six Steps* Box 3.2 `[S5]` | none recorded |
| LSO | Lesotho | **2000** | — | VERIFIED | *Six Steps* Box 3.3 `[S5]` | phased Grade-1 abolition from 2000 |
| TZA | Tanzania | **2001** | 2003 | VERIFIED | *Six Steps* Box 6.1 `[S5]` | PEDP launch 2001; 2003 = first academic year |
| KEN | Kenya | **2003** | — | VERIFIED | World Bank 2009 ch.4, PDF p.156 / printed p.130 `[S5]` | announced Dec 2002, implemented 4 Jan 2003 |
| MOZ | Mozambique | **2004** | 2005 | VERIFIED | World Bank 2009 ch.6, PDF p.233 / printed p.207 `[S5]` | abolition 2004; 2005 = first full academic year |
| GHA | Ghana | **2005** | 1997 | VERIFIED | *Six Steps* Box 4.2; World Bank 2009 ch.3, PDF p.119/137 `[S5]` | 2005/06 national scale-up; 1997 is not a national abolition |
| CMR | Cameroon | — (1999/2000) | — | **UNRESOLVED** | no primary source located `[S5]` | excluded from main; all-dates sensitivity only |
| ZMB | Zambia | — (2002) | — | **UNRESOLVED** | no abolition source; SFAI "2002" is a survey year `[S5]` | excluded from main; all-dates sensitivity only |
| RWA | Rwanda | — (2003) | — | **UNRESOLVED** | no primary source located `[S5]` | excluded from main; all-dates sensitivity only |
| BDI | Burundi | — (2005) | — | **UNRESOLVED** | no primary source located `[S5]` | excluded from main; all-dates sensitivity only |

**Verification caveat.** "Verified" here means **quoted at a named page/box** in the two 2009 World Bank/UNICEF
compilations, which are authoritative secondary compilations; no underlying ministry decree, *arrêté*, or
Education Act was retrieved. For a strict primary-source standard the eight date values remain
**re-verification pending** (§6, §7). The values themselves are committed and reproducible.

### 2.3 E8 Fisher randomization inference

The RI record `[S10–S12]` reuses the same outcome panel and the **same estimator** as E8 and adds design-based
placebo inference. Outcome: WDI primary GER (`SE.PRM.ENRR`), annual, SSA, 1990–2015; committed panel
`data/e8_primary_ger_panel.csv` (4,836 rows, 251 countries; sha256 `365bcd43…`; WDI vintage "Last Updated
2026-11-11"), sample **48 SSA countries**, **8** treated, **40** never-treated placebo-country candidates. A
reproduction gate passes before any permutation: the observed event ATTs reproduce the published E8 verified-8
table (ATT(0) exact to 0.0; max abs difference across 11 events `2.220e-16`) `[S12]`.

---

## 3. Design

### 3.1 E6 — take-off dating

Demand take-off = first year `y` in the series with `s(y+10) − s(y) ≥ +3.0` percentage points (agricultural VA uses
≤ −3.0 because it falls). Schooling take-off = first 5-year-grid year with `schooling(y+10) − schooling(y) ≥ +1.0`.
A take-off equal to a series' first observable year is **left-censored** and classified as *demand-first, weakly* —
never as the reverse. Countries are classified `forward` (demand first), `reverse` (schooling first),
`forward_or_tie` (weak forward / left-censored), or `undetermined`. The **primary window is the full overlap
1900–2012**; the pre-registered 1960–2010 window is reported as robustness because it selects against pre-1960
demand take-offs. This window choice is a **documented deviation** from the pre-registration `[S16]`, not the
pre-registered plan.

Reported quantities: the strict demand-first share among *identifiable* countries (forward + reverse + weak tie),
the schooling-first share under the same denominator, the share among *strict* orderings only, the bounds computed
over **all** countries with both series, and the weak-tie/left-censored share of in-window countries. No single
percentage is privileged.

### 3.2 E8 — event study around abolition (not t*)

The treatment date is the abolition year itself; the design is **not** centred on `t* = t_abolition + L_primary`.
Estimation is Callaway–Sant'Anna with universal base period `g−1` and not-yet-treated controls (never-treated
allowed), event time −5..+6, cohort-size-weighted aggregation, country-cluster bootstrap (500) `[S6, S7]`; a TWFE
event study (country and year FE, binned endpoints) is the comparison `[S6]`. The outcome is WDI **primary GER**;
WDI **secondary GER** is a labelled proxy for the requested lower-secondary outcome (WDI publishes no annual
lower-secondary GER). Sensitivity: all dates ±1, leave-one-country-out, placebo dates 6 years earlier, and the
all-12-dates set `[S8]`.

### 3.3 Fisher randomization inference

Two pre-registered placebo re-assignments `[S10]`, **B = 10,000** each, master seed 20261125, per-permutation RNG:
**P1 placebo-date** redraws each treated country's date uniformly from its feasible window (excluding the true date
±2); **P2 placebo-country** keeps the 8 dates and draws 8 countries without replacement from the 40 never-treated
SSA countries. Statistics: **T0** = CS ATT at event 0, **Tpost** = unweighted mean of event ATTs at +1..+6.
Two-sided `p2 = (1 + #{|T_perm| ≥ |T_obs|}) / (B_eff + 1)`. The pre-registered decision rule labels the result
`robust` if all four two-sided p-values are < 0.05. The pre-registration (`4e466a3…`) precedes the data/gate commit
(`263bef2…`) `[S10 meta]`.

**Hard data gate — `t*` is NOT-ESTIMABLE.** The RI record and this paper's bulge-arrival pre-registration record
`t*` as **NOT-ESTIMABLE** with no proxy: `t_abolition` is sourced **8/8**, `L_primary` (primary-cycle length) is
sourced **0/8**, therefore `t*` is sourced **0/8** and excluded from every specification. This is a **data gate**,
not a null result: no `t*`-centred estimate is computed anywhere, and auditor-supplied cycle-length candidates are
recorded as unadopted candidates, not used as inputs `[S10; paper2/PREREGISTRATION_BULGE_ARRIVAL.md]`.

---

## 4. Results

### 4.1 E6 — the ordering on pre-1990 series

**Table 2. E6 full-overlap results, 1900–2012 (source: `[S1]`; counts and shares recomputed from the committed CSV).**

| proxy | countries with both series | in window | demand-first n | schooling-first n | weak tie / censored n | undetermined n | demand-first % identifiable | schooling-first % identifiable | schooling-first % strict | bounds over all | weak/censored % in-window | src |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GGDC non-agricultural employment | 37 | 30 | 2 | 5 | 13 | 10 | **10.0** | 25.0 | 71.4 | 6.7–40.0 | 43.3 | `[S1]` |
| WDI urbanisation | 143 | 101 | 10 | 14 | 41 | 36 | **15.4** | 21.5 | 58.3 | 9.9–45.5 | 40.6 | `[S1]` |
| WDI industry value added | 143 | 76 | 13 | 25 | 16 | 22 | **24.1** | 46.3 | 65.8 | 17.1–46.1 | 21.1 | `[S1]` |
| WDI agricultural value added (falling) | 143 | 83 | 9 | 21 | 18 | 35 | **18.8** | 43.8 | 70.0 | 10.8–53.0 | 21.7 | `[S1]` |

**Reading.** Demand-first is **10.0–24.1% of identifiable countries** — below the pre-registered one-third decision
threshold in all four proxies. Schooling-first is the **larger strict ordering** in all four proxies
(**21.5–46.3%** of identifiable countries; **58.3–71.4%** of strict orderings), but it is **not a majority of
identifiable countries** (maximum 46.3%). The remaining **21–43%** of in-window countries are weak ties or
left-censored. The all-country bounds (**6.7–53.0%**) are the honest uncertainty band; a bare point percentage
must never be quoted without its denominator and the weak-tie category. The record's earlier prose range
"18–33% strict schooling-first" **does not reproduce** and is not used `[S14]`.

### 4.2 E6 — the ordering is threshold- and smoothing-sensitive

**Table 3. N3 dating sweep (source: `[S3, S4]`; 54 committed definitions, all n ≥ 20).**

| quantity | value | src |
|---|---|---|
| strict demand-first share across 54 definitions | **0.0–30.8%** | `[S3]` |
| median across definitions | **10.45%** | `[S4]` |
| q1 default definition (Δs = 1.0, Δr = 3.0 pp, no smoothing; n = 34) | demand-first **6.2%**, weak tie **70.6%**, schooling-first **17.6%**, undetermined **5.9%** | `[S4]` |
| q1 all-country bounds | **5.9–82.4%** | `[S4]` |
| definitions below the 75% forward threshold | **100%** | `[S4]` |

The ordering cannot be quoted as a single number. Ties and left-censoring dominate because GGDC demand take-offs
are often at the series start. The record's earlier "weak forward-or-tie 56–84%" prose also **does not reproduce**;
the reproducible quantities are **56.7–88.5%** of identifiable countries and **50.0–82.1%** of all countries
`[S14]`.

### 4.3 E8 — the event study

**Table 4. Callaway–Sant'Anna event study, primary GER, verified-8 dates (source: `[S6]`; every cell from the committed CSV).**

| event | ATT | bootstrap SE | 95% CI | TWFE ATT | treated n | src |
|---|---|---|---|---|---|---|
| −5 | 6.39 | 3.30 | [−0.08, 12.86] | 12.15 | 6 | `[S6]` |
| −4 | 1.35 | 3.93 | [−6.35, 9.04] | 1.89 | 7 | `[S6]` |
| −3 | −0.13 | 3.62 | [−7.23, 6.98] | 1.14 | 7 | `[S6]` |
| −2 | −0.03 | 1.74 | [−3.43, 3.38] | 1.96 | 7 | `[S6]` |
| **0** | **12.44** | 7.55 | **[−2.36, 27.24]** | 12.88 | 7 | `[S6]` |
| +1 | **23.82** | 11.11 | [2.05, 45.60] | 23.80 | 7 | `[S6]` |
| +2 | **25.94** | 10.95 | [4.48, 47.40] | 25.77 | 7 | `[S6]` |
| +3 | **22.12** | 8.42 | [5.62, 38.62] | 24.48 | 6 | `[S6]` |
| +4 | **25.19** | 8.50 | [8.54, 41.84] | 26.73 | 7 | `[S6]` |
| +5 | **28.56** | 9.67 | [9.61, 47.51] | 27.65 | 6 | `[S6]` |
| +6 | **25.92** | 8.82 | [8.64, 43.20] | 21.05 | 7 | `[S6]` |

**Reading.** Post-period CS ATTs are **+22.12 to +28.56 points** and are significant from +1 onward. The **on-impact
(+0) estimate is +12.44 and its 95% CI includes zero** — the design does not date the response to the abolition
year itself. Pre-trends at −2/−3/−4 are flat; the **−5** estimate (**6.39, CI [−0.08, 12.86]**, only 6 treated
cohorts) is imprecise and is reported, not hidden. TWFE post estimates are similar (21.05–27.65). Control
countries per event are **28–30** in the verified-8 table (25–30 is the all-12 sensitivity).

**Table 5. E8 sensitivity, mean post ATT (source: `[S8]`).**

| specification | mean post ATT | on-impact (t0) | src |
|---|---|---|---|
| all dates +1 year | 12.31 | 10.37 | `[S8]` |
| all dates −1 year | 18.65 | 0.03 | `[S8]` |
| placebo dates −6 years | **−0.39** | −0.24 | `[S8]` |
| all-12 dates | 20.80 | 7.03 | `[S8]` |
| leave-one-country-out | **18.17–26.16** | 7.00–13.94 | `[S8]` |

The sign and rough magnitude do not depend on any single country; the ±1-year shifts move the timing (especially
on-impact) but not the direction. The secondary-GER proxy shows post ATTs of **+6.71 [−3.39, 16.82]** at +5 and
**+6.07 [−0.01, 12.16]** at +6, with every CI including zero: a **proxy with no clear detected effect**, not a null
`[S9]`.

### 4.4 E8 — Fisher randomization inference

**Table 6. Fisher RI, B = 10,000 per family (source: `[S10, S11]`).**

| family | statistic | T_obs | perm mean (SD) | #(\|T_perm\| ≥ \|T_obs\|) | B_eff | two-sided p2 | one-sided p+ | MCSE(p2) | src |
|---|---|---|---|---|---|---|---|---|---|---|
| placebo-date | T0 | **12.4436** | −0.90 (1.25) | 0 | 10,000 | **9.999e-05** | 9.999e-05 | 1.0e-04 | `[S10]` |
| placebo-date | Tpost | **25.2607** | −2.54 (3.75) | 0 | 10,000 | **9.999e-05** | 9.999e-05 | 1.0e-04 | `[S10]` |
| placebo-country | T0 | **12.4436** | −0.40 (2.15) | 5 | 10,000 | **5.999e-04** | 5.999e-04 | 2.45e-04 | `[S10]` |
| placebo-country | Tpost | **25.2607** | −1.04 (5.17) | 2 | 10,000 | **2.9997e-04** | 2.0e-04 | 1.73e-04 | `[S10]` |

The pre-registered decision rule returns **`robust`**: all four two-sided p-values are below 0.05. Read correctly,
the placebo-date floor `9.999e-05` = `1/(B+1)` means **"no placebo draw in 10,000 reached the observed statistic"**,
not a precise tail probability (MCSE 1.0e-4). The placebo-country distribution is wider and heavier-tailed, so its
p-values are larger but still small. As in the main E8 record, the observed T0 uses 7 effective cohorts (MOZ 2004
lacks a 2003 base-year observation), and P2 draws average 5.51 effective treated cohorts; nothing is imputed. The RI
result **complements, and does not replace**, the wide bootstrap CIs: the on-impact CS CI still includes zero.

### 4.5 E1 procedural context (procedure-dependent)

A related project record `[S13]` reports BY (Benjamini–Yekutieli) certified counts for a multiverse of
permutation-based link tests: at draw budget **R = 1200**, **0/0/0/32** for up/down/sign-flip/heterogeneity under
the conservative-family convention; at **R ≤ 800** the same convention is **0/0/0/0**; under the 136-parity
convention R = 1200 is **25/15/0/39**. These counts are **procedure-dependent** (they depend on the p-value
convention and the draw budget) and the record's underlying panel is **not committed** (reproduction uses a later
WDI pull; the original panel is documented as lost). They are context for how fragile "certified" counts are, not
evidence for any Paper #2 claim.

---

## 5. Robustness summary

Four independent checks point the same way for E8: (i) the **−6-year placebo** gives a mean post of **−0.39**
`[S8]`; (ii) **leave-one-country-out** stays at **18.17–26.16** `[S8]`; (iii) **date ±1** shifts move the timing but
preserve direction and magnitude `[S8]`; (iv) **Fisher RI** over two placebo schemes places the observed abolition-
year ATT in the extreme tail (p2 **9.999e-05** and **5.999e-04**) `[S10]`. The RI estimator is verified against the
cited `att_cs` (max abs difference **7.11e-15** across the 11 event ATTs) `[S10]`, and the reproduction gate passes
against the published E8 table `[S12]`.

For E6, robustness is the other way round: the ordering is **sensitive** to the dating rule. Across 54
threshold/smoothing definitions the strict demand-first share spans **0.0–30.8%** `[S3]`; the full-overlap window is
a documented deviation from the pre-registered 1960–2010 window `[S16]`; and the schooling series is a
**reconstruction**. The defensible E6 statement is the interval, not a point.

---

## 6. What this does not show (preserved negatives)

1. **No causal identification.** E8 is a staggered-adoption association with pre-trend checks, not a causal design;
   the on-impact CI includes zero; the treated sample is 7–8 countries. The RI p-values are design-based and
   conditional on strong exchangeability assumptions (placebo dates within windows; never-treated countries as
   exchangeable carriers of the date pattern). RI does not replace the bootstrap CIs.
2. **`t*` is not estimated.** `t* = t_abolition + L_primary` is **NOT-ESTIMABLE** (`L_primary` sourced 0/8); this is
   a data gate, not a null result. No bulge-arrival claim is made `[S10]`.
3. **The ordering is measurement-limited.** E6 dates a **reconstructed mean-years-of-schooling take-off**, not a
   secondary/tertiary enrolment-threshold crossing; demand is proxied by broad structural-change shares, with no
   manufacturing-only onset. A title-level "massification before industrialization" claim would require two
   analyses not run here (§7).
4. **Pre-1900 is outside the data.** GGDC/PWT start 1950, WDI 1960, the schooling panel 1870 on a 5-year grid. The
   classic first-industrialiser cases cannot be tested on these series; the project's historical dates are
   UNVERIFIED literature standard and are **not** used here.
5. **Four fee dates are unresolved** (CMR, ZMB, RWA, BDI) and excluded from the main specification. They are
   never-treated controls in the main design; if any actually abolished fees in-window, the control pool is
   contaminated, with no signed direction available.
6. **One outcome family.** Primary GER (OBSERVED; modelled where WDI says modelled) is the main outcome; the
   secondary-GER proxy shows no clear detected effect. No other outcome was permuted or searched.
7. **Stale prose values must not be quoted.** The record's "18–33% strict schooling-first", "weak-or-tie 56–84%",
   "25–30 controls" (main table) and "mean post 18–29" do not reproduce; the corrections are in `[S14]` and are the
   values used here.
8. **Fee-date verification is page-located, not primary-instrument.** "Verified" means a named page/box/quote in
   World Bank/UNICEF (2009) compilations; no ministry decree/Education Act was retrieved.
9. **Vintage and provenance gaps.** The GGDC archive used is the 2014 release while the pre-registration text names
   `10sd_2023`; E8's main-record raw outcome files are not committed (the RI record does commit its panel, at WDI
   vintage 2026-11-11); E6 external zips are hashed, not committed.

---

## 7. Replication status

**Table 7. Branches and heads used (repo `TreyModels/atlas-of-education`; refs are `origin/…`).**

| record | branch | head (commit) | used for |
|---|---|---|---|
| E6/E8/N3 results | `research/e6e8-sequencing-2026-11-25` | `2d19da7cfea0c007eced8e3b114a6eea35ddbaea` | Tables 2–5, fee dates |
| E6/E8 errata | same | `bd782be4d15c834f054b1ecc650e54565f6b292f` | corrections, `[S14]` |
| E6/E8 pre-registration | same | `a2a116df0fe481419dabd4b0c2ad70e6289c9600` | design, window deviation |
| E8 Fisher RI | `research/e8-fisher-ri-2026-11-25` | `fb8b67e7b8e659546b3421e1d0ba8d3f42ecac10` | Table 6, gate |
| E8 RI pre-registration | same | `4e466a316f4b219c256a45dbf5a1ce8ea8deb11b` | RI design/decision rule |
| E8 RI data+gate | same | `263bef238e5ac7baffacecdf37c37c0c288abb02` | panel, gate |
| E1 procedural context | `research/e1-multiverse-1200-2026-11-25` | `6a452a45a5aa172ca996ffae93292beb8270a2ad` | §4.5 only |
| fee dates (independent) | `research/codex-source-verification-2026-11-25` | `9a0fd69a51625818494379d37974f1eb0aeeb2c6` | date verification |

**What a replication needs.** E8/RI: the committed panel `[S10 data/]` plus the cited `att_cs` script
`bd782be:…/e8_fee_event_study.py`; the RI gate passes on WDI vintage 2026-11-11. E6: the four external WDI zips,
the GGDC 2014 archive, PWT 10.01, the long-run panel and event-dates file (hashes in `[S15]`), then the three
scripts in `bd782be`'s record. **Known gaps:** E8's main-record raw WDI outcome files and the `download_data.sh`
cited by its report are not committed; the GGDC vintage mismatch; and the E1 panel is not committed. The two
analyses that would lift the title-level claim are (a) a **manufacturing-only onset** on the already-hashed GGDC
10-Sector data and (b) **secondary/tertiary enrolment-threshold crossings** with long series consistent across
countries.

---

## 8. Conclusion

On pre-1990 series the demand take-off precedes the schooling take-off in a minority of identifiable countries
(10.0–24.1%), schooling-first is the larger strict ordering (21.5–46.3% of identifiable countries; 58.3–71.4% of
strict orderings), and the remainder is dominated by weak ties and left-censoring (21–43% of in-window countries).
The ordering is threshold- and smoothing-sensitive across 54 definitions (0.0–30.8% strict demand-first). In eight
sub-Saharan African countries with page-located fee-abolition dates, the post-period primary-enrolment estimates are
large (+22.12 to +28.56 points), the on-impact estimate is imprecise (12.44, CI including zero), and Fisher
randomization inference over 20,000 placebo re-assignments places the observed abolition-year ATT in the extreme
tail (p2 9.999e-05 and 5.999e-04). The evidence is **consistent with** schooling and structural change moving
together, with schooling typically but not universally first, and with fee abolition followed by large
primary-enrolment gains. It does not identify causes, does not date `t*`, and does not measure enrolment-threshold
massification — the three limits that should frame any quotation of this paper.

---

## References (placeholder — not yet verified in this draft)

`[cite]` Pritchett — supply-side / schooling expansion account.
`[cite]` Sandberg (1979) — schooling before industrialisation (Sweden).
`[cite]` World-polity tradition (Boli/Ramirez/Meyer; Soysal & Strang).
`[cite]` Human-capital tradition (Schultz; Becker; Mincer; Goldin & Katz).
`[cite]` Callaway & Sant'Anna — staggered-adoption ATT estimation.
`[cite]` Fisher — randomization inference; `[cite]` permutation-inference methods.
`[cite]` World Bank/UNICEF (2009) *Six Steps to Abolishing Primary School Fees*; World Bank (2009) *Abolishing
School Fees in Africa*.

> All references are placeholders to be filled from the project's verified lists; no citation is asserted as
> verified in this draft.

---

## Appendix A. Source keys

| key | file | branch | commit |
|---|---|---|---|
| S1 | `research/records/2026-11-25-e6e8-sequencing/results/e6_summary.csv` | `research/e6e8-sequencing-2026-11-25` | `2d19da7cfea0c007eced8e3b114a6eea35ddbaea` |
| S2 | `…/results/e6_classification.csv` | same | `2d19da7…` |
| S3 | `…/results/n3_table.csv` | same | `2d19da7…` |
| S4 | `…/results/n3_recommendation.json` | same | `2d19da7…` |
| S5 | `…/data/fee_dates.csv` | same | `2d19da7…` |
| S6 | `…/results/e8_event_SE.PRM.ENRR_verified8.csv` | same | `2d19da7…` |
| S7 | `…/results/e8_results.json` | same | `2d19da7…` |
| S8 | `…/results/e8_sensitivity.csv` | same | `2d19da7…` |
| S9 | `…/results/e8_event_SE.SEC.ENRR_verified8.csv` | same | `2d19da7…` |
| S10 | `research/records/2026-11-25-e8-fisher-ri/results/e8_ri_results.json` | `research/e8-fisher-ri-2026-11-25` | `fb8b67e7b8e659546b3421e1d0ba8d3f42ecac10` |
| S11 | `…/results/e8_ri_summary.csv` | same | `fb8b67e…` |
| S12 | `…/results/repro_gate.json` | same | `fb8b67e…` |
| S13 | `research/records/2026-11-25-e1-multiverse/results/summary_by_R.json` | `research/e1-multiverse-1200-2026-11-25` | `6a452a45a5aa172ca996ffae93292beb8270a2ad` |
| S14 | `research/records/2026-11-25-e6e8-sequencing/ERRATUM.md` | `research/e6e8-sequencing-2026-11-25` | `bd782be4d15c834f054b1ecc650e54565f6b292f` |
| S15 | `…/results/e6_inputs_and_hashes.csv` | same | `2d19da7…` |
| S16 | `…/PRE_REGISTRATION.md` | same | `a2a116df0fe481419dabd4b0c2ad70e6289c9600` |

## Appendix B. Cell-level provenance

- **Table 1:** every row from `[S5]` (fee_dates.csv); statuses recomputed (8 VERIFIED, 4 UNRESOLVED) from the same
  file. Quote/page locators are the `source`/`quote_or_locator` fields.
- **Table 2:** counts (`forward`, `reverse`, `forward_or_tie`, `undetermined`, `n_all`, `n_in_window`) from `[S1]`
  rows `window=1900-2012`; `identifiable = forward + reverse + forward_or_tie`; percentages and ranges recomputed
  from those counts (demand-first 10.00–24.07; schooling-first 21.54–46.30; strict 58.33–71.43; weak 21.05–43.33;
  bounds 6.7–53.0). Country-level rows and label tiers are in `[S2]`.
- **Table 3:** range/median/q1 row from `[S3]`/`[S4]` (54 definitions; q1 row n=34).
- **Table 4:** every cell from `[S6]` (`event`, `att`, `se_boot`, `ci_lo`, `ci_hi`, `att_twfe`, `n_treated`); the
  same numbers are in `[S7]` `event_table`.
- **Table 5:** `mean_att_post` / `att_t0` from `[S8]` (specs `all+1`, `all-1`, `placebo-6`, `all12`, `drop-*`).
- **Table 6:** every cell from `[S10]`/`[S11]`; `T_obs`, `B_eff`, p-values, MCSEs, permutation mean/SD and counts.
- **§4.5:** counts from `[S13]` (`certified_BY` / `certified_BY136` at R = 400/800/1200); the record's own erratum
  (branch `research/edsystem-audit-2026-11-25`) documents the 136-parity vs conservative-family distinction.
- **§7 table:** heads verified with `git rev-parse`/`git ls-remote` on 25 Nov 2026; base SHAs are the full 40-hex
  strings shown.
