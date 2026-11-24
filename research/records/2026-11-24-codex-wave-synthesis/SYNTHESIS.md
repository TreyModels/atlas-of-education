# Codex wave — synthesis (24 November 2026)

**Status:** the Codex wave is closed. Nine branch heads are verified; this record is the seam document for the
next session: what the wave **established**, what it did **not** establish, what was **retracted**, and what the
forward programme is. It contains no new analysis and no new data.

**Rules applied here.** Every headline number below was **recomputed from a committed source file** (see §6) before
being quoted. Numbers that could not be recomputed are labelled **UNVERIFIED** with the reason, even where a branch
REPORT states them. Simulation is marked as simulation throughout; nothing in the synthetic runs is evidence about
history. "Effective fertility" is surviving children per woman and is **never** called TFR; TFR is births per woman.
No causal language is used: the one checked event study (E8) is stated as "consistent with", and the observational
associations are stated as associations.

**Source of record:** `HANDOFF.md` @ `51f9f02` and `research/records/2026-11-24-handoff/codex_wave_ledger.md` on
`research/handoff-2026-11-24`; the nine branch heads in §1.

---

## 1. The nine verified heads

| Item | Branch | Head | Record directory |
|---|---|---|---|
| Q1 mechanisms (synthetic known-truth pilot + GPU gate) | `research/q1-mechanisms-2026-11-25` | `9b0cabe` | `research/records/2026-11-25-q1-mechanisms/` |
| Q2 country pathways (pair benchmark, audit, cases; erratum on `f71b789`) | `research/q2-pathways-2026-11-25` | `9a4f586` | `research/records/2026-11-25-q2-pathways/` |
| Q3 multiverse calibration + full BH/BY | `research/q3-multiverse-calibration-2026-11-25` | `db7814d` | `research/records/2026-11-25-q3-calibration/` |
| E1 multiverse at R = 1,200 (erratum on `7e6f7b5`) | `research/e1-multiverse-1200-2026-11-25` | `6a452a4` | `research/records/2026-11-25-e1-multiverse/` |
| E6/E8 sequencing repairs (demand timing, fee event study, N3; errata on `2d19da7`) | `research/e6e8-sequencing-2026-11-25` | `bd782be` | `research/records/2026-11-25-e6e8-sequencing/` |
| E11 fertility audit (EFR vs TFR, placebo ladder) | `research/e11-fertility-audit-2026-11-25` | `e926575` | `research/records/2026-11-25-e11-fertility-audit/` |
| Source verification (fee dates, demand series, prior art; metadata erratum on `9a0fd69`) | `research/codex-source-verification-2026-11-25` | `ea6bc61` | `research/records/2026-11-25-codex-source-verification/` |
| Methods paper (multiverse) | `research/methods-multiverse-paper-2026-11-23` | `d7e8f9f` | `research/records/2026-11-23-multiverse-paper/` |
| Paper F (fertility; rounding correction applied; erratum commits `4f8a61c` + `23928e0`; data unchanged) | `research/paper-fertility-2026-11-25` | `23928e0` | `research/records/2026-11-25-paper-fertility/` |

Q3's substantive verification was at `075c8c3`; `db7814d` is a documentation-only addendum (the 1,200-draw
cross-reference paragraph) and is the final head. Paper F's assembled draft (with the E11 text changes) is now at
`23928e0`; the −0.227 rounding correction is **applied**, and the rebuilt draft prints −0.227 (0 × −0.228).
Verification status per item is from the ledger @ `51f9f02`, not re-audited here; the **numbers** are
recomputed in §6. **Record heads advanced after the consolidated errata pass (task-12), each an additive erratum
commit with data unchanged: Q2 `f71b789 → 9a4f586`; E1 `7e6f7b5 → 6a452a4`; E6/E8 `59d31d7 → bd782be`; source
verification `9a0fd69 → ea6bc61`; Paper F `ec899cc → 4f8a61c → 23928e0` (draft correction applied; erratum commits
`4f8a61c` + `23928e0`; data unchanged).** The corrections are folded into §2.1(d),
§2.3, §2.4, the §3 erratum list, and the §6 R1/R4/R5/R6/R7/R10 rows; none changes a recomputed headline number.

---

## 2. What the wave established

### 2.1 About the world, under the committed estimator (association, not identification)

**(a) The macro wall — only 5 of 272 links travel across all groupings. RECOMPUTED.**
The grouping multiverse re-partitions 217 countries into 50 real groupings across 8 families and re-estimates the
same 272-link within-country lead-lag matrix inside every group, against 400–1,200 random re-partitions of identical
sizes. Five links are `robust everywhere`; the other 267 fall under the remaining verdicts (group-specific, beats-random-without-a-clear-group, or no better than random). The
methods paper reports 5 robust / 76 group-specific / 161 no better than random (**76 and 161 are UNVERIFIED here —
they are reported counts in prose, not recomputed by this synthesis**; the 5 is recomputed in §6 row R1).
The substantive reading is narrow and must stay narrow: *under this estimator, on this panel, the typical
within-country link does not transport across country typologies.* It is a transportability description, not a
causal finding, and "no better than random" means "not detectable at this resolution", not "no effect".

**(b) Effective fertility and TFR are different constructs, and they flip the schooling lead/lag. RECOMPUTED.**
`effective_fertility` is expected surviving children per woman (reconstructed pre-1950); `tfr_observed_1950plus` is
births per woman (UN WPP 2024). On the matched 5-year grid (n = 2,955 country-years, 197 countries) the median
absolute difference is **0.3042** and the maximum **4.2677** (AFG 1950: 3.399 surviving children vs 7.248 births).
In the level ladder (country + year FE, controls, identical rows), the schooling terms' **lead/lag ratio is 0.541
for effective fertility** (lag-dominant) and **1.555 for TFR** (future-dominant). Neither series corrects the other;
the divergence is what different constructs produce, not a data mystery. Consequence: no paper may call effective
fertility "TFR", and any claim that pits one against the other must name the construct.

**(c) The 68.75% "schooling before fertility" figure was a tie-counting artefact; strict ordering is 37.5%.
RECOMPUTED.**
From the subsistence-v2 event table @ `ce66cfc` (annotated at `8caaeac`), the three-event sample is 64 countries:
**24/64 = 37.5% strict schooling-first** (bootstrap 95% CI **26.6–50.0%**), **20/64 = 31.25% simultaneous**, and
**20/64 = 31.25% fertility-first**. The retracted 68.75% is the sum of the 24 strict cases and the 20 ties
(44/64); it treats simultaneity as schooling-first. The all-with-both-dates sample (81 countries) gives 35.8%
strict. The two orderings (release-vs-schooling and schooling-vs-fertility) are separate and must never be merged.

**(d) On pre-1990 series, demand-first is a minority ordering; the honest framing is "schooling and structural
change move together". RECOMPUTED.**
E6 rebuilds the demand-ordering test on pre-1990 observed series, replacing the retracted 7% figure (§3). In the
primary 1900–2012 full-overlap window, the demand take-off precedes the schooling take-off in **10.0%** of
identifiable countries on GGDC non-agricultural employment (2/20), **15.4%** on urbanisation (10/65), **24.1%** on
industry value added (13/54) and **18.8%** on agricultural value added (9/48). Bounds over all in-window countries
are **6.7–53.0%**; weak ties or left-censored demand onsets are **21.1–43.3%** of in-window countries. Strict
**schooling-first** is the larger strict ordering in all four proxies — **21.5–46.3% of identifiable countries**,
against 10.0–24.1% demand-first, and **58.3–71.4% of strict orderings** — but it is not a majority of identifiable
countries; the remainder are weak ties or undetermined. (The branch's earlier strict-schooling-first prose range did
not reproduce; the E6/E8 record erratum (Issue A at `59d31d7`; record head `bd782be`, data unchanged) corrects it to
these recomputed values.) The
preregistered 1960–2010 window selects against pre-1960 demand take-offs
and is reported as robustness, not as the primary test. The defensible sentence is: **schooling and structural
change move together, with schooling typically but not universally first; demand-first is neither eliminated nor
cleanly distinguished from censoring.**

### 2.2 About the method used to make those claims (synthetic / arithmetic, not history)

**(e) The two standard model-selection criteria fail the wave's zero-signal control. RECOMPUTED.**
Q1 is **synthetic throughout**: three known-truth worlds (direct schooling effect, common-development selection,
joint choice) with distinct kernels, fitted by closed-form Gaussian MLE rivals. On the preregistered zero-signal
control (strength 0), a valid discriminator must be at chance (~33%). It is not: raw held-out MSE picks the most
flexible kernel R3 in **97.5%** of W1 reps and **97.5%** of W2 reps (the REPORT rounds this to "97 per cent"), and
BIC picks the most parsimonious R1 in **100%** of every world. A model winner from either criterion is therefore a
complexity artefact, not mechanism evidence. This is a statement about the estimator, **not about any real-world
mechanism**.

**(f) "Robust everywhere" is a share rule, not a homogeneity certificate: it mislabels 87% of minority-effect
worlds. RECOMPUTED.**
Q3 calibrates the verdict rule on a known-truth simulator (150 countries, 50 periods, 400 groupings, 400 replicate
seeds per regime). The rule controls the null well (false positive 4.25% [2.7–6.7]; uniform strong effect false
negative 2.5%; shared-trend false positive 5.0%). But when the effect lives in only one third of countries it calls
the link robust in **87.0%** of replicates (48.25% strict ROBUST+H + 38.75% ROBUST-but-GROUP, i.e. 348/400
replicates) while localising the planted group only **42.0%** of the time. The failure gets worse with N, not
better. "Robust everywhere" is a descriptive significance-share label; it is not evidence of a homogeneous effect.
This is a calibration of the **rule** (8 groupings, 1 link per replicate), not of the real 50-grouping pipeline —
labelled simulation, not history.

**(g) "BY certifies zero" is a draw-budget statement, not a universal property. RECOMPUTED.**
The empirical p-value floor is 1/(R+1). The dependence-robust Benjamini–Yekutieli procedure certifies, at R = 400,
**0/0/0/0** (up/down/sign-flip/heterogeneity — 272 links each), and still **0** for all four at R = 800. At
R = 1,200 the heterogeneity family alone crosses the step-up line and BY certifies **32 heterogeneity links**
(first BY rank 29), while up/down/sign-flip stay at 0. Nominal Benjamini–Hochberg over the same 272-link families
certifies **35/19/15/53** at R = 400 and **41/23/20/53** at R = 1,200; the effective-tests sensitivity gives 44 up
links at m_eff ≈ 157. The 400-draw range is 0 (BY) / 35 (nominal) / 44 (anti-conservative sensitivity) — a range,
not a confidence interval. "400 draws can certify nothing" was wrong; "BY certifies zero" is only true at the tested
lower budgets.

### 2.3 The one checked event study (design-conditional, not identification)

**(h) Fee abolition: post-period primary-enrolment effects are positive and pre-trends are flat at −2/−3/−4.
NOT RECOMPUTED (committed field only).**
E8 uses 8 fee-abolition dates verified against primary/authoritative sources by the source-verification record (4
further dates — CMR, ZMB, RWA, BDI — are unresolved and excluded from the main specification); the branch's working
note cited `bfb8c6f`, and the E6/E8 record erratum (Issue B at `59d31d7`; head `bd782be`, data unchanged) records
that `bfb8c6f` is an ancestor of the verified source-verification head `9a0fd69` (now `ea6bc61`, metadata erratum
only) and the `fee_dates.csv` is sha256-identical at both (`1a08d465…`) — provenance only, no date change;
Callaway–Sant'Anna
with not-yet-treated controls on the SSA sample, WDI primary GER. The on-impact ATT is **+12.44** (95% CI −2.36 to
27.24); from +1 onward the effects are positive and significant (e.g. +1: 23.82 [2.05, 45.60]; +6: 25.92 [8.64,
43.20]); the placebo-date check is −0.39 and the leave-one-out mean post range 18.17–26.16. The −2/−3/−4
pre-trends are flat; the earliest horizon (−5, only 6 cohorts) is imprecise. **These event ATT values are verified
at source but were not independently recomputed here** (see §7). The correct sentence is "**consistent with** a
fee-abolition effect on primary GER at the enrolment margin", not an identified effect; the small treated
sample and the sensitive on-impact estimate are part of the claim. The secondary-GER proxy shows no clear effect
and is not a null.

### 2.4 Descriptive only (not evidence for any mechanism)

Q2's pair benchmark is a **descriptive** path comparison, explicitly not a causal design. Its central honest null
survives, but with corrected magnitudes (Q2 erratum §A @ `9a4f586`): the committed "observed" medians 0.82 / 0.7715
were computed over **all 5,460 unordered pairs**, while the random draws use 52 pairs. The **matched-pair** medians
are **0.620 years (schooling) / 0.2375 (TFR)**; against those, the shares of random draws whose median is at least as
large are **96.1% / 100.0%**. Matched 1980-similar pairs are therefore **less** divergent in 1990–2010 outcomes than
random pairing — not "equally" or "not unusually" divergent. The direction of the honest null is unchanged (matching
did not produce more divergence than random pairing); the old all-pairs 0.82 / 0.77 versus random 0.825 / 0.773
comparison and its 52.4% / 50.3% shares must not be quoted. The primary pair set also remains matching-dependent
(overlap 21.2% with Manhattan, 28.8% with Mahalanobis/2-opt — **UNVERIFIED**, committed-field only, §7). The
pair-benchmark counts (105 baseline-complete / 52 pairs / 1 unpaired / 52 with both outcomes) are **RECOMPUTED**
(§6 R7); the corrected yardstick is **RECOMPUTED-AT-ERRATUM** (§6 R10). No claim about similar starts causing
divergent paths is supportable, and none is made.

---

## 3. What was retracted or corrected (must never reappear)

1. **The "7%" labour-demand figure is retracted.** It was an artefact of the 1991+ start of the wage/paid-employment
   series (the original test binned 1991-start series against a 1990 baseline), and the source-verification record confirms **no
   pre-1990 wage-employment series exists** in the standard public sources checked (WDI/ILO modelled series begin
   1991). It is not evidence against a demand mechanism. E6 replaced it with the pre-1990 sector-employment,
   urbanisation and value-added series in §2.1(d); a 1991+ wage-employment comparison may be reported only with its
   data-start caveat and never as a pre-1990 ordering.
2. **Effective fertility is not TFR.** See §2.1(b). The old cross-series comparisons that treated them as one series
   (including "the EFR/TFR gap is a data problem") are withdrawn; the gap is the construct difference.
3. **68.75% / 69% schooling-before-fertility is withdrawn.** See §2.1(c). Use 37.5% strict (24/64, CI 26.6–50.0)
   with 31.25% simultaneous and 31.25% fertility-first, or the all-81 figure 35.8%, and never merge it with the
   release-vs-schooling ordering.
4. **"Robust everywhere" as a homogeneity certificate is withdrawn.** See §2.2(f). It is a share rule.
5. **"BY certifies zero" as a universal claim is withdrawn.** See §2.2(g). It is true at 400 and 800 draws and false
   for the heterogeneity family at 1,200.
6. **"400 draws can certify nothing" was already retracted before this wave.** Nominal BH certifies a floor cluster
   (35 up links at 400; 41 at 1,200). The dependence-robust reading remains a separate, conditional statement.
7. **"The level relation is a development gradient, not an identified schooling effect" was too strong**
   (Codex F11; Paper F, F11 text at `ec899cc`, record head `23928e0`). The paper now says: the level association is consistent with (i) a common
   development gradient, (ii) anticipation/quantity-quality, and (iii) a schooling effect with a long lag, and this
   design **cannot distinguish them**. "Causal claim rejected" is not a claim the project is entitled to make.
8. **The supply-led framing of massification was softened** (E6/E8, Paper M revision branch). The defensible
   ordering statement is §2.1(d), not "supply-led is established".

**Record errata (25 Nov 2026, consolidated task-12).** Each is an additive erratum commit; data unchanged, and none
changes a recomputed headline number above. Pinned to the errata heads:

- **Q2 yardstick** (`9a4f586`): matched-pair medians **0.620 / 0.2375** and shares **96.1% / 100.0%** replace the
  all-pairs 0.82 / 0.7715 comparison — matched pairs are *less* divergent than random pairing (see §2.4, §6 R10).
- **E1 136-parity** (`6a452a4`): under the committed 136-parity convention at R = 1,200, BY certifies up **25** /
  down **15** / sign-flip **0** / heterogeneity **39**, not up/down/flip 0/0/0; the conservative-family statement
  (BY 0 at 400; 32 heterogeneity links at 1,200) is unchanged.
- **E6/E8 controls** (`bd782be`, Issue D): the verified-8 E8 event table has **28–30** control countries per event;
  25–30 belongs to the all-12 sensitivity.
- **E6/E8 mean-post** (`bd782be`, Issue D): no mean-post quantity spans 18–29; the reproducible statement is mean
  post **12.3–26.2** across the ±1-year and leave-one-out checks, against **−0.39** under the placebo (verified-8 CS
  post mean 25.26).
- **N3 weak-tie range** (`bd782be`, Issue C): the "56–84%" line does not reproduce; weak tie is **56.7–88.5%** of
  identifiable countries (50.0–82.1% of all countries), or `forward_share_incl_ties` 56.7–100.0% with the
  denominator stated.
- **Source-verification metadata** (`ea6bc61`): 24 prior-art works checked = **21 V (DOI verified) / 2 U (no DOI) /
  1 W (working-paper version)**; the `9a0fd69` commit message's "24 DOI-verified" is a metadata overstatement, not a
  status change.
- **Paper F rounding** (`4f8a61c` erratum; **APPLIED** at `23928e0`): the total-attainment level coefficient is
  **−0.227458**, which prints as **−0.227** (3 occurrences in the rebuilt draft; 0 × −0.228); four source
  occurrences were corrected and the draft rebuilt. Data unchanged; substance unchanged (ERRATUM §B).

---

## 4. What the wave did NOT establish

- **No identified causal schooling → fertility effect at the aggregate level.** The level association is robust and
  negative, but it survives neither a future-schooling placebo nor a change-on-change placebo in a way that
  identifies schooling; the E11 change ladder returns "does not discriminate" between a common development
  gradient, anticipation/quantity-quality, and a long-lag schooling effect. Nothing here is an effect size for a
  policy lever.
- **No mechanism winner.** Q1's rivals are observationally equivalent on the aggregate observables by construction,
  and its selection criteria are degenerate; E11 cannot separate the three candidate mechanisms; the multiverse is a
  transportability test, not an identification strategy. The three worlds remain observationally equivalent at the
  aggregate level, and the pilot does not claim equivalence beyond its shared-mean construction.
- **No claim that demand is ruled out.** The retraction of the 7% figure means the opposite: pre-1990 demand
  indicators are available, demand-first is a real 10–24% minority ordering, and 21–43% of countries are weak
  ties/censored. Demand is neither established nor excluded.
- **No claim that schooling is a "dose" whose size is known.** The dose model does not beat development-only out of
  sample and its strengths are prior-wide; that is a statement about one model with poor fit, not about Caldwell or
  the wealth-flows thesis.
- **No individual-level (micro) result.** DHS Individual Recode is login-gated and was not obtained; the published
  ecological cells are ecological, not individual. The individual test remains the decisive missing measurement.
- **No historical identification from the model.** E6, E8, N3 and the GPU transition runs are
  observed/reconstructed data plus model-conditional statements; none is an event study of schooling on fertility
  with checked pre-trends, and none licenses causal language.

---

## 5. Forward programme (the wave's actual output)

> **Status: needs redesign per the 24 Nov 2026 suite audit — see "Suite audit (24 Nov 2026)" at the end of this section.**

The aggregate regression route is exhausted at this resolution. The next programme is measurement, not more
panels:

1. **Micro-simulation with explicit simulation/history labels.** Run the GPU suite (`research/records/2026-11-24-gpu-suite/`)
   on the Apple Silicon port, then check whether the four DGPs collapse to identical macro slopes (the wall) and
   whether any **micro tie-breaker** separates them. Every output is labelled *simulation*; a model winner is not an
   established cause and a counterfactual is model-conditional. Equivalence and timing gates come first (`exp1`/`exp3`
   fixed-seed equivalence; only scale if acceptable).
2. **Micro tie-breakers as observables.** Identify measurements that separate the mechanisms *within* the same
   aggregate distribution — the wave's own conclusion is that "only different measurements or interventions can"
   (Q1), so the tie-breaker design is the bridge from the multiverse to identification.
3. **DHS individual microdata.** The biggest available upgrade: individual-level schooling → children-ever-born,
   cohort comparisons, and the effective-fertility/TFR construct split as the first real micro test. This is an
   access-path job (files are login-gated), not a scraper.
4. **Keep the two orderings separate** (release-vs-schooling vs schooling-vs-fertility) and keep the
   EFR-vs-TFR construct labels in every table. Keep the draw-budget/dependence caveats attached to every "robust"
   or "BY" statement.

### Suite audit (24 Nov 2026)

**The forward programme above needs redesign per audit: the shipped suite cannot test its own pre-registered hypotheses.** The audited payload (`research/records/2026-11-24-gpu-suite/` @ `51f9f02`) does not implement H1 or H4. `exp2` is a logistic classifier on pre/post means — there is no macro fixed-effects regression, no country dimension and no cross-DGP overlap statistic, so H1's ">75% macro-slope overlap" is undefined. `strength` appears only inside a docstring, so H4's zero-signal control cannot execute; the four "micro signatures" are transforms of the same state mix, so exp2's classifier recovery is **construction-implied and is not evidence**. `exp4` raises `IndexError` on its first World Bank API call, and WDI `SL.TLF.0714.ZS` is "Children in employment", **not** child labour, so the series cannot carry a child-labour claim. Any exp2/exp3 output, including the PORT-PRODUCTION run, inherits these defects.

The **ten claims in AUDIT §9 must not be published** in their current form: the macro wall demonstrated; binary bans backfire; protective capacity reduces child labour while fees-only does not; a micro tie-breaker passes the Q1 zero-signal control; rejection-ABC calibrates and identifies; fee abolition reduces child employment; learning-per-grade slope tested; faithful DGP mapping to Basu–Van / Baland–Robinson / Nordtveit / Bray / Jayachandran / Dang–Rogers / Pritchett; hidden work measured; the mixed DGP as a mixed-mechanism world. The honest labels are "simulation", "reduced form" and "consistent with" — nothing stronger.

The **Apple Silicon work is portability only**: the port reproduces the CuPy subset and the `sim_step` kernel bit-identically (NumPy vs MLX) and its full run is labelled **PORT-PRODUCTION, not research results** (`research/apple-silicon-gpu-2026-11-24`, port complete at `fd933d9`; branch head `be42c4d`). It does not repair the inferential objects.

Therefore the **"macro wall" and the "micro tie-breaker" remain UNTESTED by simulation.** In progress is a **strength-separable, macro-moment-matched redesign with a survey measurement layer**, pre-registered as design only (no run) at `research/records/2026-11-24-suite-tiebreakers/PRE_REGISTRATION.md` @ `e526c94` on `research/suite-tiebreakers-2026-11-24`: worlds `θ_w(s) = θ_0 + s·Δ_w` that are identical at `s = 0`; per-world nuisance search to a common macro vector `M*`; measured-variable tie-breakers with sampling, non-response, heaping, reference-period and under-reporting layers; algebraic-equivalence and label-permutation placebos; out-of-seed, out-of-parameter-region and mixture-world validation. Audit source: `research/records/2026-11-24-suite-lit-review/AUDIT.md` @ `4649cae` on `research/suite-lit-review-2026-11-24`. Until the redesign runs and passes its pre-registered controls, no suite output may be cited as evidence for the wall or for a tie-breaker.

---

## 6. Recomputation log (every headline number above)

All inputs were extracted with `git show <head>:<path>` from the branch heads in §1; the script is
`scripts/recompute_headlines.py` and its full output is `results/recompute.json`. "Match" means the recomputed
value equals the branch record's committed value.

| # | Number | Recommended from (file @ commit) | Recomputed | Match |
|---|---|---|---|---|
| R1 | 5 of 272 links robust in every grouping | `results/verdict_by_R.csv` @ E1 `6a452a4` (erratum on `7e6f7b5`; data unchanged) (`robust_everywhere_Rmax`) | **5** | yes |
| R2 | MSE picks flexible kernel 97.5% (W1, W2) / BIC picks parsimonious R1 100% | `results/pilot_recovery_bic.json` @ Q1 `9b0cabe` (`zero_signal_control.0.0`) | **0.975 / 0.975 / 1.00 all worlds** | yes (REPORT says "97") |
| R3 | Minority-effect worlds labelled robust 87.0%; planted group flagged 42.0%; null FP 4.25% | `results/calibration.json` @ Q3 `db7814d` (`main.B.counts`, `main.C.counts`) | **348/400 = 0.870; 168/400 = 0.420; 17/400 = 0.0425** | yes |
| R4 | BH 35/19/15/53 at R=400 and BY 0; BH 41/23/20/53 and BY het 32 at R=1200; BY 0 at R≤800 | `results/verdict_by_R.csv` @ E1 `6a452a4` (erratum on `7e6f7b5`; data unchanged); cross-check `results/families_for_fdr_check.csv` + `fdr_check_output.csv` @ Q3 `db7814d` | **35/19/15/53 and 0; 41/23/20/53 and 32; 0 at 400/800**; recomputed BH/BY from the four sorted 272-link p-vectors also gives 35/19/15/53, BY 0, m_eff=157 → 44 up | yes |
| R5 | EFR vs TFR: lead/lag 0.541 vs 1.555; median abs diff 0.3042, max 4.2677 | `results/q1_construct_audit.json` @ E11 `e926575`; panel sha256 `cd30d7ea…` @ Q2 `9a4f586` (erratum on `f71b789`; data unchanged) (`data/long_run_panel.csv`) | **0.5412 / 1.5552; 0.3042 / 4.2677 on 2,955 country-years, 197 countries**; AFG 1950 3.3991 vs 7.248 | yes |
| R6 | E6 demand-first 10.0/15.4/24.1/18.8%; strict schooling-first 21.5–46.3% (58.3–71.4% of strict orderings); bounds 6.7–53.0%; ties/censoring 21–43% | `results/e6_classification.csv` @ E6/E8 `bd782be` (record head advanced to `bd782be` — errata only; data unchanged; on top of `59d31d7`/`2d19da7`) | **10.0 (2/20), 15.4 (10/65), 24.1 (13/54), 18.8 (9/48); strict schooling-first 25.0 (5/20), 21.5 (14/65), 46.3 (25/54), 43.8 (21/48) → 21.5–46.3%; 71.4/58.3/65.8/70.0% of strict orderings (58.3–71.4%); bounds 6.7–40.0 / 9.9–45.5 / 17.1–46.1 / 10.8–53.0 (overall 6.7–53.0); ties 43.3/40.6/21.1/21.7%** | yes |
| R7 | Q2 pair benchmark 105 baseline-complete / 52 pairs / 1 unpaired / 52 with both outcomes | `results/smoke/pairs.csv` + `pairs_metadata.json` @ Q2 `9a4f586` (record head advanced to `9a4f586` — erratum only; data unchanged; on top of `f71b789`) | **52 pairs; 104 distinct paired + 1 unpaired = 105; 52 with both schooling changes; 52 with both TFR changes** | yes |
| R8 | 68.75% was a tie artefact; strict 37.5% = 24/64, CI 26.6–50.0 | `results/event_dates.csv` @ subsistence-v2 `ce66cfc` (annotated `8caaeac`) | **24/64 = 37.5%, ties 20/64 = 31.25%, fertility-first 20/64 = 31.25%; bootstrap CI 26.56–50.0; 68.75 = 44/64 = strict + ties** | yes |
| R9 | Q1 GPU gate: repeat 8.9e-16; layout diff 1.9074; pin nW=12 seed 7 | `results/engine_check.json` @ Q1 `9b0cabe` | **UNVERIFIED — not recomputed** (needs the T4 box and a synthetic panel; numbers are committed fields and were not re-run in this synthesis) | n/a |
| R10 | Q2 random yardstick: matched-pair medians 0.620 / 0.2375; shares of random draws at least as large = 96.1% / 100.0% | `results/audit/pairs_primary.csv` (matched medians) + `results/audit/erratum_check_q2_yardstick.json` (shares) @ Q2 `9a4f586` (record head advanced to `9a4f586` — erratum only; data unchanged); recomputed in this record's `results/recompute.json` (`Q2_yardstick`) | **0.6200 / 0.2375 (matched medians, independently re-derived); 961/1,000 and 1,000/1,000 (committed erratum check); random-draw medians 0.825 / 0.7728** | yes (**RECOMPUTED-AT-ERRATUM**) |

The Q1 pilot is synthetic (three constructed worlds, closed-form MLE rivals, 40 reps per cell). The Q3 calibration
is a simulation of the verdict rule (8 groupings, 1 link per replicate, 400 replicates per regime), not the real
50-grouping / 272-link pipeline. The draw-budget arithmetic is arithmetic on empirical p-values, not a calibrated
test under dependence. R10 is a record-erratum recomputation, scripted in `scripts/recompute_headlines.py` and output to
`results/recompute.json` (`Q2_yardstick`): the matched-pair medians are re-derived from `pairs_primary.csv`, and the
random-draw shares come from the committed erratum check (seed 71201, 1,000 draws).
**None of §2.2 is history.**

---

## 7. UNVERIFIED items (quoted but not recomputed here)

These are deliberately **not** promoted to the established list. Each is either a committed field this synthesis
did not re-derive, or a prose claim with no committed reduction.

- **E8 event-study ATTs** (§2.3): +12.44, 23.82, 25.92, the pre-trend values and the sensitivity range. Reason: the
  CS/TWFE estimates need the served data and bootstrap; only the committed `e8_event_*.csv` / `e8_results.json` were
  inspected, not re-estimated. Treat as committed-field, design-conditional.
- **Q2 matching-sensitivity shares** (21.2 / 28.8 / 61.5%): committed-field only, not recomputed here. The
  **random-yardstick comparison is no longer UNVERIFIED** — it was recomputed at Q2 erratum §A (`9a4f586`) and is
  recorded in §2.4 and §6 R10 (matched-pair medians 0.620 / 0.2375; shares 96.1% / 100.0%).
- **Q3 design-size grid, strength ladder and draw axis** (e.g. b = 0.06 strict power 19.0%, N = 220 minority
  false-robust 55.5%): the main minority/null rates are recomputed in R3, but the grid cells are committed fields,
  not re-simulated.
- **Methods paper counts 76 group-specific / 161 no better than random**, and the robustness/group-localisation
  splits (1 of 5 robust links group-concentrated; 20 of 32 BY heterogeneity links group-concentrated). Reason:
  reported in prose/JSON but not reduced from the committed per-link tables by this synthesis.
- **N3 range 0.0–30.8% (median 10.45%) across 54 definitions** and the q1-default 6.2%/70.6%/17.6%: committed fields
  in `n3_table.csv`/`n3_recommendation.json`; not re-derived. The record's separate "weak forward-or-tie 56–84%"
  line does not reproduce; the E6/E8 erratum §C (record head `bd782be`) gives weak tie **56.7–88.5%** of identifiable
  countries (50.0–82.1% of all countries), or `forward_share_incl_ties` 56.7–100.0% with the denominator stated.
  The 56–84% line must not be quoted.
- **The exact empirical p-values in Q3** cannot be re-derived from the committed null array (rounded to 4
  significant digits; the record documents agreement to about one draw count for 267/272 up and 271/272 down links);
  sign-flip and heterogeneity null draws were not saved. This is the record's own documented limitation, repeated
  here so it is not lost.

---

## 8. File and command map

- This synthesis: `research/records/2026-11-24-codex-wave-synthesis/SYNTHESIS.md`.
- Recompute script: `research/records/2026-11-24-codex-wave-synthesis/scripts/recompute_headlines.py` (extraction
  commands in its docstring; `--sources` points at a directory of `git show` copies).
- Recompute output: `research/records/2026-11-24-codex-wave-synthesis/results/recompute.json`.
- Handoff contract and ledger: `HANDOFF.md` @ `51f9f02`,
  `research/records/2026-11-24-handoff/codex_wave_ledger.md` @ `51f9f02`.
- Forward-programme suite: `research/records/2026-11-24-gpu-suite/` (`METHODOLOGY.md`, `PRE_REGISTRATION.md`,
  `run_all.sh`, exp1/exp3 CuPy, exp2/exp4 CPU pandas) @ `51f9f02`.
- Dashboard: `research/records/2026-11-23-dashboard/README.md` @ `research/dashboard-2026-11-23`; the Codex-wave
  addendum is the new commit on that branch and points here.

Reproduce the recomputation:

```bash
cd research/records/2026-11-24-codex-wave-synthesis
# extract the inputs per the script docstring into $S, then:
python scripts/recompute_headlines.py --sources "$S" --out results/recompute.json
```

No secrets, no branch rewrites, no new analysis in this record.

---


## 9. Full-system multiverse (25 Nov 2026) — toy simulation, not history

**Heads.** Full-system multiverse: `research/masseng-edsystem-2026-11-25` @ `b7108da` (`RUN_REPORT.md`; **1,440 runs** = 144 equation-choice combinations × 10 seeds, 304.1 s at 12 workers; `results_multiverse.json` sha256 `004173aa…`, `summary_multiverse.json` `549958e2…`, driver `932fc973…`; pre-registration `3679f2d`). Statistical tests: `research/edsystem-tests-2026-11-25` @ `aadbbb4` (`MULTIVERSE_TESTS.md`; cluster-robust OLS + seed FE + Holm over 9 outcomes + stratum sign checks). Equation suite: `research/equation-suite-2026-11-25` @ `a7fcfb9` (**10 scripts**, 61.7 s on the 192-core server, 0 runtime failures, **3 pre-declared decision-rule FAILs preserved**).

**What was tested.** `eduengine`'s full massification chain — family affordability incl. forgone earnings → learning/quality → limited-place gates at four transitions → credential→jobs — with rural structure and supply/funding. The multiverse varies **equation/mechanism choices** (3 affordability × 2 supply funding × 3 learning/supply configurations × 2 gates × 2 labour regimes × 2 rural structures), not calibrated parameters. **Toy simulation: every parameter illustrative, no causal or empirical claim, and not a MASSENG v5 output.**

**Findings (toy-model regularities).**
- **Gates dominate lower/upper attainment and the wealth completion gap.** Bar vs quota: lower completion **.720 vs .550**, upper **.609 vs .449**, tertiary .411 vs .313; the bar screens the poorest quintile hardest (lower completion q1 **.174** vs q5 **.966**). Quota lowers completion for everyone (middle quintiles most), narrows the absolute top–bottom gap (.792→.646) but barely moves wealth parity (.180→.165). Quota raises tutoring **.273→.499** (gate-adjacent .320→.604) and **shifts prep away from tertiary** (tertiary share .145→.078). Tests: quota-vs-bar lower completion **−17.0 pp** [−18.4,−15.7], tutoring **+22.6 pp** [21.3,23.9].
- **Affordability dominates primary/tertiary completion and the poverty gap.** Cash-only vs credit: primary **.797 vs .929 / .910**, tertiary **.296 vs .362 / .428**; poorest-quintile lower completion .091→.195; wealth parity .103→.231/.183. Tests: credit vs cash primary **+13.2 pp** [12.6,13.9], tertiary up to **+13.2 pp** (poverty-line need).
- **Jobs regime dominates formal share:** queue-with-credential-floors **.293** vs competitive **.627** (η² .96; tests **+33.4 pp** formal share, Holm-supported).
- **Rural structure dominates wealth parity:** low vs high rural penalty **.245 vs .100** (tests **−14.6 pp**, sign-consistent) and lowers attainment at every level. **No migration, sorting or remittances are modelled.**
- **Supply/funding moves public quality but is not identifiable from attainment:** fiscal loop vs fixed budget moves public quality 1.12 vs 0.99 (tests +0.132 [0.115,0.149]) but completion ranges overlap 1.00 — a statement about this design, not that supply never matters.
- **Learning configuration moves the learning proxy but only slightly completion** (.622→.633→.651 lower across public-only/+private/+private+tutoring; value of learning η² .61).
- **Tutoring is gate-driven and second-order** (η²≈0 for completion; +3.5 pp primary in tests). It is one module, not the system centre.
- **Engine limitation — RETRACTED 25 Nov (driver bug, not engine):** the push-out decomposition (liquidity vs choice vs never-started) was reported unusable because "the engine overwrites the exit reason"; this is **wrong** — `core.step` compacts exits into `e.exits` and the driver read `e.kids['reason']` afterwards. Fix + regression test: `fix/edsystem-exit-reason-2026-11-25` @ `4679ddb` (§3.8). The decomposition is recoverable after the corrected re-run; no liquidity-vs-choice claim until then.

**What not to believe.** Not causal, not empirical, not country-calibrated: do not quote as policy effects or as evidence about real quotas, affordability or jobs regimes. p-values describe regularities of the simulated design only. The full-system engine is toy `eduengine`, not MASSENG v5; migration, rural–urban sorting and remittances are missing (being added). The equation suite's **3 pre-declared FAILs remain FAIL**. Observed vs assumed: UIS/EdStats, ILO-UCW, GGDC/PWT, WDI/Barro-Lee and DHS aggregates are usable; demand, learning profiles, gate rules, credential requirements and migration flows are assumptions (task-41 top gaps). The DHS ecological FE-bug correction is already recorded in the dashboard and handoff (§14); never quote the old biased numbers (`708e34a`).

**Next actions.** (1) Add migration/rural–urban sorting/remittances to `eduengine` and rerun the multiverse. (2) Fix the exit-reason bookkeeping before any liquidity-vs-choice claim. (3) Feed the equation test bench (task-43) with the suite's estimand/identification/benchmark frame. (4) Couple observed covariates where task-41 says usable; do not invent demand/learning/gate/credential targets. (5) DHS: the second African request remains the only route to the individual test.