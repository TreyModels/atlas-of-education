# AFRICA-11 EXTENSION — the ecological schooling→fertility replication restricted to the 11 African countries

> **25 Nov 2026 SUPERSESSION (read before quoting any number below).** This file describes the run at
> `fe762b9`. `CORRECTED_RUN_2026-11-25.md` supersedes the key numbers: the **D4** wanted-vs-actual gap is
> now **−0.1962 (0.0495)** (its point estimate moved because the full construct×schooling interaction set
> replaced the single-secondary interaction), and the **bootstrap CIs** widen (full-sample Q2a 2-group
> 0.958 [0.906, 1.019]; Africa-11 2-group ratio 1.0698 [0.9987, 1.1403] — **now includes 1.0**, so that
> verdict moves to indeterminate). The two changes are separable: multiplicities move CIs only; the
> interaction set moves D4. Both are **provisional** pending Neon's diff. Numbers below that disagree are
> pre-correction values, not current claims.


**Task:** task-36 part 1. **Branch:** `research/dhs-api-ecological-2026-11-24`. **Status:** complete.
**Scope:** the 11 African countries of the acquisition panel — **MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA, BEN,
NAM, SWZ** (the 8 verified E8 countries + 3 comparators), using the **already-pulled public-API panels** and the
same pre-registered construct split and caveats as the full analysis.
**Labels:** every number is **OBSERVED (published DHS cells) / ECOLOGICAL**, a country×survey×education cell, not
a woman. **No causal language. Not a substitute for the individual Recode test.**
**Computation:** new box (`ssh -p 45973`, `/root/work/dhs-api/`), 8 workers, 13 s wall; **nothing on the Mac**.
The estimates use the **corrected** FE parameterisation (see [`BUGFIX_FE_PARAMETERISATION.md`](BUGFIX_FE_PARAMETERISATION.md)).

> **Coverage tier:** under [`../2026-11-24-dhs-acquisition/AMENDMENT_02_ACCESS_COVERAGE.md`](../2026-11-24-dhs-acquisition/AMENDMENT_02_ACCESS_COVERAGE.md)
> this is the **T1 coverage-restricted** sample (11 African countries only; the 3 Asian benchmarks are absent).
> It is **not** the pre-registered 14-country main test, and the pre-registered D1 (which compares the full
> sample to the prior record) is **not applied** here. The full-sample corrected numbers remain in
> [`REPORT.md`](REPORT.md).

---

## 1. Coverage of the restricted sample

| Panel | cells | surveys | countries | note |
|---|---|---|---|---|
| Completed fertility (women 40–49), 4-level education | 176 | 44 | 11 | ETH/GH/KE/UG dominate; BJ/SZ have a single round each |
| Completed fertility, 2-group education | 144 | 72 | 11 | the coverage-maximising panel |
| Period TFR 15–49, 4-level | 244 | 61 | 11 | |
| Period TFR, 2-group | 148 | 74 | 11 | |
| Wanted TFR, 4-level | 228 | 57 | 11 | desired-fertility limb |
| Survey-level construct panel (CEB/deaths/TFR) | — | 74 | 11 | 1988–2025 |

Structural gaps that travel with every number below: **Eswatini has one DHS round (2006)** — it cannot support
cohort-vs-round separation and appears only in the pooled/descriptive cells; **Ethiopia's first round is 2000**
and **Lesotho's first is 2004**, so neither has a pre-1995/pre-2000 round on DHS; the 4-level completed-fertility
panel has only **44 survey-rounds**, so its within-survey estimates are thinner than the 2-group ones.

---

## 2. Q1 — the association in the 11 African countries

Completed fertility (women 40–49, mean children ever born), education vs **no education**; survey weights = women
in the cell; cluster-robust SEs by country. Corrected estimator.

### 2.1 M1 (country×survey FE), 4-level panel — 176 cells, 44 surveys

| Education | children | SE | per-SD | unweighted |
|---|---|---|---|---|
| Primary | **−0.707** | 0.158 | −0.41 | −0.621 (0.135) |
| Secondary | **−2.163** | 0.179 | −1.29 | −2.152 (0.248) |
| Higher | **−3.198** | 0.135 | −1.99 | −3.234 (0.159) |

Monotone in education; all CIs exclude 0. The gradient in the African-11 is **steeper** than in the full
87-country sample (secondary −1.58 there), which is expected: the full sample includes lower-fertility Asian and
Latin American countries where the secondary-vs-none gap is smaller.

### 2.2 Specification ladder (weighted; country FE + period FE vs within-survey vs trends)

| Model | Primary | Secondary | Higher |
|---|---|---|---|
| M0 country FE + 5-yr period FE | −0.714 (0.159) | −2.176 (0.177) | −3.208 (0.134) |
| **M1 country×survey FE** | −0.707 (0.158) | −2.163 (0.179) | −3.198 (0.135) |
| M5 + country-specific trends | −0.708 (0.158) | −2.163 (0.179) | −3.198 (0.135) |
| 2-group, M1 (`secondary+ vs none/primary`), 72 surveys | — | **−1.974** (0.123) | — |

The FE choice does not move the result; the 2-group coverage-maximising panel gives −1.97 (SE 0.12). The pipeline-
density interaction (M2) is positive in direction for higher education (+0.24 (0.11), p=0.035) and null for
secondary (+0.11 (0.18), p=0.54) — with 11 countries and three interactions this is **exploratory**, not a
supported heterogeneity claim.

### 2.3 Heterogeneity inside the 11

- **Per survey** (72 surveys with both 2-group cells): **98.6% negative**, only **MW 1992** non-negative (+0.5);
  median **−2.00** (IQR −2.33 to −1.70), range −4.5 to +0.5.
- **Per country** (10 countries with ≥2 surveys; SWZ has 1): all **10 negative**; BH at q=0.05 rejects all 10.
  Gradient sizes: ET −3.40 (0.21), BJ −2.56 (0.17), TZ −2.11 (0.07), MW −2.03 (0.15), MZ −1.96 (0.06),
  NM −1.97 (0.07), KE −1.87 (0.07), UG −1.75 (0.12), GH −1.71 (0.05), LS −1.27 (0.06).
- **Cross-country spread is real**: Lesotho's gradient is less than half Ethiopia's. The pooled coefficient hides
  this; the minority is *not* in sign (10/10 negative) but in magnitude.

---

## 3. Q2a — period TFR vs cumulative completed fertility (the window contrast)

Both births-based; standardised within outcome; unweighted for both (rate indicators publish no denominators);
country-cluster bootstrap, 500 draws, seed 20261124.

| Contrast (11 African) | standardised ratio β(period TFR) / β(cumulative CEB40) | 95% CI | verdict (D3 rule) |
|---|---|---|---|
| 4-level, secondary vs none | **1.178** | [1.027, 1.356] | **same sign, materially different magnitude** |
| 2-group, secondary+ vs none/primary | **1.070** | [1.011, 1.135] | **same sign, materially different magnitude** (by 7 %) |

Raw-unit gradients: cumulative CEB40 secondary **−2.163** (0.179) vs period TFR secondary **−1.630** (0.075) on
the 4-level panels (different samples/standardisations; the standardised ratio is the pre-registered comparison).

**Reading:** in the African-11 the *period* TFR gradient is **larger in standardised magnitude** than the
cumulative completed-fertility gradient, by roughly 7–18 %. This is the opposite direction from the full sample,
where the two were indistinguishable (ratio 1.003 [0.932, 1.077]). The difference must be stated plainly: the
window contrast is **not uniform across regions**; in these 11 countries the period measure gives a somewhat
steeper schooling gradient than the completed-fertility measure. It remains a *magnitude* difference, not a sign
change.

---

## 4. Q2b — the construct contrast in the 11

### 4.1 Births period vs cumulative (cell level) — null

Stacked standardised model, country×survey FE, construct × secondary interaction, cluster by country:
**−0.0795 (SE 0.088, p=0.37)**. The two births-based measures are not distinguishable in this restricted sample
(full sample: +0.016, p=0.70).

### 4.2 Wanted vs actual TFR — direction right, not distinguishable

**−0.0196 (SE 0.0256, p=0.44)** for the secondary × construct interaction (actual − wanted). The full-sample
result (−0.0775, p=0.0004) *[pre-interaction-set; corrected **−0.1962 (0.0495)** in `CORRECTED_RUN_2026-11-25.md`]* — that the schooling gradient is weaker in **wanted** than in **actual** fertility —
**does not replicate with precision in the 11-country subset**; the sign is the same but the CI includes 0. In the
separate standardised models: actual TFR secondary −1.630 (0.075) vs wanted TFR −1.576 (0.087), a gap of ~0.05 SD
vs ~0.21 SD in the full sample.

### 4.3 Surviving children vs period TFR (survey level) — different series

74 surveys, 11 countries, 1988–2025:

| statistic | 11 African | full 87-country sample (for comparison) |
|---|---|---|
| corr(Surviving₄₀, TFR) | **0.754** (Spearman 0.719) | 0.822 |
| corr(CEB₄₀, TFR) | **0.868** | 0.899 |
| median \|TFR − Surviving₄₀\| | **0.533** | 0.631 |
| max \|TFR − Surviving₄₀\| | **1.829** | 2.681 |
| median \|TFR − CEB₄₀\| | **0.860** | 1.009 |
| mean ratio TFR / Surviving₄₀ | **1.008** | 0.942 |
| within-country changes (n = 10): corr(ΔSurviving, ΔTFR) | **0.426** | 0.321 |
| within-country changes: corr(ΔCEB, ΔTFR) | **0.689** | 0.509 |
| median Δ gap (ΔSurviving − ΔTFR) | **+0.774** | +0.435 |

The construct gap is **smaller** in the African-11 than in the full sample (median 0.53 vs 0.63 children) but
still material, and the surviving-children series tracks TFR changes less well than the cumulative births series
(0.43 vs 0.69). As pre-declared: these are **different constructs** (surviving family size vs period births); the
gap is not an error and neither series corrects the other. **No surviving-children-by-education gradient exists**
in the public API (education breakdown not published for `FE_CEBA_W_MND`), and none is constructed.

---

## 5. Cohort proxy — steepening, not attenuation (diverges from the full sample)

Repeated cross-sections; cohort proxy = survey year − 44.5; country FE + cohort-bin FE; education × cohort
(per decade, centred):

| interaction (11 African) | children per decade | SE | 95% CI |
|---|---|---|---|
| primary × cohort | **−0.278** | 0.112 | [−0.497, −0.059] |
| secondary × cohort | **−0.186** | 0.076 | [−0.335, −0.037] |
| higher × cohort | +0.016 | 0.082 | [−0.145, +0.177] |

**The interaction is negative and distinguishable from zero for primary and secondary** — the schooling gradient
is *steeper* in later cohorts in these 11 countries. That **contradicts** both the prior ecological attenuation
(+0.26 (0.13), `research/dhs-micro-2026-11-23 @ 31ded00`) and the corrected full-sample attenuation
(2-group +0.244, p=0.016). It is a genuine regional divergence and must not be averaged away. Caveats: the cohort
proxy is built from survey years, not followed women; "secondary" expands from an elite to a mass category over
these decades, which can move the gradient in either direction; and the 4-level African panel has only 44 surveys.
The individual microdata would be needed to separate composition from a change in the individual association.

---

## 6. What the 11-country extension does and does not show

**Does show (OBSERVED / ECOLOGICAL):**
1. The negative schooling–completed-fertility association is present in **every one of the 11 countries** and in
   **98.6 % of 72 African survey-rounds**; median per-survey gradient −2.00 children (secondary+ vs none/primary).
2. It survives country FE, period FE and country trends; the FE choice changes nothing material.
3. The period-vs-cumulative **window contrast is materially larger here** (ratio 1.07–1.18, CI excluding 1) than in
   the full sample (1.003) — a regional difference in how the measure's window matters.
4. The wanted-vs-actual gap is directionally present but **not statistically distinguishable** in this restricted
   sample; it does not replicate the full-sample precision.
5. The cohort interaction is **negative (steepening)** for primary and secondary — opposite to the full-sample
   attenuation. This is the most interesting divergence and the strongest argument for the individual test.
6. The surviving-children and period-TFR series remain **different** (median gap 0.53 children, change correlation
   0.43 vs 0.69 for cumulative births).

**Does not show:** anything causal; anything individual-level; anything about surviving children by education;
the pre-registered 14-country main test (T1 coverage restriction); D1 (not applicable to the subset).

---

## 7. Reproduction

- Panels: committed `data/panel_edu*_<IND>.csv` (public-API pull, no microdata).
- Command (new box, corrected estimator):
  `cd /root/work/dhs-api && DHS_WORKERS=8 /root/miniconda3/bin/python -u scripts/estimate.py \
   --countries MWI,ETH,UGA,LSO,TZA,KEN,MOZ,GHA,BEN,NAM,SWZ --outdir results/africa11`
  — **13 s wall**, load average ≈ 19–25 on the shared box (8 workers, 15-CPU container quota).
- Independent cross-check: `scripts/corrected_reduction.py` reproduces the point estimates exactly (Q1 M1
  −0.7070/−2.1627/−3.1977; ratio 4-level 1.177998; A-vs-B −0.07948) and validates against the prior record
  (max |Δ| 0.0036). Logs: `results/server_box2/`.
- Outputs: `results/africa11/{results.json, model_table.csv, heterogeneity_*.csv, heterogeneity_bh.json,
  survey_construct.csv}`; cross-check `results/corrected/corrected_results.json`.

## 8. Honest caveats (repeated because they matter)

- **Ecological**: a published country×survey×education cell, not a woman. Composition (wealth, residence,
  community, cohort) cannot be separated from education in these data — the API never crosses education with
  wealth or residence.
- **Category meaning drifts** across rounds (massification); a stable coefficient is not a stable individual effect.
- **Thin cells**: 4-level completed fertility has 44 surveys and some countries contribute a single round;
  Eswatini one round; Ethiopia/Lesotho post-1995/2000 only.
- **Construct naming**: O1/Ceb is cumulative **births**, O2 is **surviving children**, only TFR/wanted TFR are
  rates. Nothing here is a TFR except the TFR.
- **The individual test remains the tie-breaker** and remains blocked on DHS access
  (`../2026-11-24-dhs-acquisition/application/NEXT_ACTION_2026-11-24.md`).
