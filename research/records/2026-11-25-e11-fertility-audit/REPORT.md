# REPORT — E11 change-on-change placebo ladder + Q2 construct reconciliation

**Status:** complete. Pre-registration committed before any script or run (`d2c7558`); runs completed on `ssh autodl3`
on 25 Nov 2026; scripts and results committed. **Nothing in this record is causal evidence.** No paper may call
effective fertility "TFR" or vice versa.

**Branch:** `research/e11-fertility-audit-2026-11-25` (base `origin/research/assessment-and-next-experiments-2026-11-24`).
**Record:** `research/records/2026-11-25-e11-fertility-audit/`.
**Environment:** autodl3, 8-core box; venv `/root/work/e11/.venv` (NumPy 2.2.6, pandas 2.3.3, statsmodels 0.15.0) —
the box's conda NumPy was broken (`~umpy.libs`, missing libopenblas); failure recorded in §6, not hidden.
**Runtime:** Q1 2 s; E11 9 s (single-threaded BLAS). Re-running both scripts produced **byte-identical**
outputs (`Q1_IDENTICAL`, `E11_IDENTICAL`).

---

## 1. Construct reconciliation (Q2 / Codex F01–F03): two different things, not one series with a gap

### 1.1 Definitions, quoted from the committed sources

- **`effective_fertility`** — from the transition record's script header: "children per woman expected to survive
  to childbearing age, 1751–2023 (Malani & Jacob / OWID)". It is a **surviving-children** measure; the pre-1950
  part is **reconstructed**.
- **`tfr_observed_1950plus`** — from the OWID metadata: "the total fertility rate summarizes the total number of
  births a woman would have if she experienced the birth rates seen in women of each age group in one particular
  year across her childbearing years"; unit "live births per woman" (UN WPP 2024; 1950–2023). It is a **births**
  measure.
- **`tfr_implied_derived`** — effective fertility ÷ an approximate survival factor; a derived reconstruction,
  never used here.

These are different constructs. `tfr_observed_1950plus` = births; `effective_fertility` = births × survival to
childbearing. They answer different questions: **birth behaviour** versus **realised surviving family size**.

### 1.2 The numbers (5-year grid, 1950–2020, both outcomes non-missing)

| Statistic | Value | Source |
|---|---|---|
| Overlapping country-years (both outcomes) | **2,955 rows / 197 countries** | `results/q1_construct_audit.json:descriptive.n_overlap_rows` |
| Median absolute difference (TFR − EFR) | **0.3042** | `descriptive.median_abs_diff` |
| Maximum absolute difference | **4.2677** | `descriptive.max_abs_diff` |
| Mean TFR/EFR ratio | **1.1749** | `descriptive.mean_ratio_tfr_over_efr` |
| Correlation, levels | **0.9378** | `descriptive.corr_levels` |
| Correlation, ten-year changes (n = 2,758) | **0.9387** | `descriptive.corr_changes` |
| AFG 1950 | EFR **3.3991** vs TFR **7.248** | `descriptive.afg_1950` |
| Coverage | EFR 3,196 rows; TFR 2,955 rows; both 2,955; 197 countries each | `descriptive.coverage` |

Codex F03 reported 14,578 overlapping country-years on the annual panel with median |difference| 0.2835 and
maximum 4.4897. Our 5-year-grid figures (2,955 rows; 0.3042; 4.2677) are consistent with that; the row count
differs because this audit uses the 5-year grid required by the ladders. **The two series are highly correlated
in levels but are not the same variable**, and their changes are not interchangeable.

### 1.3 Both outcomes on the same matched sample (the point of Q2)

Level ladder, per-SD coefficients (clustered SE), country + year FE, controls income and urbanisation,
**identical rows for both outcomes** (n = 1,417; 109 countries; 1950–2010):

| outcome | S(t−10) | S(t) | S(t+10) | lead/lag (S(t+10) ÷ S(t)) |
|---|---|---|---|---|
| effective fertility (surviving children) | −1.0209 (0.1989) | −0.5966 (0.1653) | −0.3229 (0.1924) | **0.541** |
| observed TFR (births) | −0.2999 (0.2173) | −0.5378 (0.1879) | −0.8364 (0.1997) | **1.555** |

Single-term columns (same sample): EFR on S(t) −1.6083 (0.2087), on S(t+10) −1.2088 (0.2150), on S(t−10)
−1.5773 (0.2116); TFR on S(t) −1.3476 (0.2195), on S(t+10) −1.3588 (0.2138), on S(t−10) −1.0173 (0.2251).

Change ladder, per-SD, country FE, clustered, identical rows (n = 981; 109 countries):

| model | past | current | future |
|---|---|---|---|
| dEFR(t,t+10) on dS terms | −0.2437 (0.0631) | −0.2159 (0.0597) | **−0.1185 (0.0395)** |
| dTFR(t,t+10) on dS terms | −0.1885 (0.0578) | −0.2144 (0.0596) | **−0.1508 (0.0392)** |
| dS(t,t+10) on dEFR terms | −0.0609 (0.0364) | −0.1801 (0.0436) | −0.1344 (0.0368) |
| dS(t,t+10) on dTFR terms | −0.0858 (0.0397) | −0.1858 (0.0453) | −0.1052 (0.0398) |

**Reading:** the "opposite lead/lag patterns" in Sonnet's Q2 are exactly what different constructs produce. In
levels, the surviving-children measure is **lag-dominant** (future term 54% of current) while the births measure
is **future-dominant** (156%); in changes both future terms are present, the births measure somewhat more so.
Neither is a correction of the other, and neither is a "data mystery". The valid statement is: *the level
association between schooling and fertility is consistent with a development gradient, with anticipation/
quantity-quality, and with a schooling effect, and the two fertility outcomes measure different things.*

**Rule for all papers:** effective fertility may never be called "TFR" or "total fertility". If a paper uses
both, it must name the construct in the table ("births per woman" vs "surviving children per woman"). Paper F's
own fertility series is the project's births measure and its label "total fertility rate (births per woman)"
(draft lines 324, 427) is correct; the rule matters where the transition/Q3 materials import
`effective_fertility`.

---

## 2. E11 change-on-change placebo ladder

**Design (pre-registered §3):** 8 schooling indicators; F = project `fertility` (births per woman, TFR-type — not
effective fertility); 5-year grid 1960–2024; controls log income and urbanisation; country-clustered SEs.
Levels: country + decade FE, with and without country-specific linear trends. Changes: country FE, with and
without country trends. FE via Frisch–Waugh–Lovell residualisation (rank-deficiency-safe; coefficient-equivalent
to the full model). Per-SD coefficients.

**Baseline results** (levels = country+decade FE; changes = country FE; per-SD; SE in parentheses; n in CSV):

| indicator | A2 S(t) | A2 S(t+10) | lead/lag | B3 dS past | B3 dS future | lead/lag | C2 future dF |
|---|---|---|---|---|---|---|---|
| mys_total | −0.154 (0.041) | −0.138 (0.038) | 0.90 | −0.051 (0.021) | −0.051 (0.021) | 0.98 | +0.008 (0.021) |
| mys_female | −0.009 (0.018) | −0.086 (0.019) | 9.92* | 0.000 (0.000) | 0.000 (0.000) | NA* | −0.000 (0.000) |
| sec | −0.128 (0.041) | −0.092 (0.037) | 0.71 | −0.042 (0.032) | −0.009 (0.031) | 0.21 | +0.123 (0.895) |
| lsc | −0.014 (0.031) | −0.047 (0.028) | 3.32 | +0.057 (0.033) | −0.054 (0.041) | −0.94 | +2.719 (1.987) |
| prm_cmp | −0.095 (0.033) | −0.018 (0.037) | 0.19 | −0.082 (0.062) | −0.006 (0.046) | 0.07 | −2.052 (1.496) |
| ter | +0.089 (0.027) | −0.051 (0.046) | −0.58 | +0.056 (0.058) | +0.054 (0.059) | 0.97 | +0.527 (0.982) |
| gpi_sec | −0.167 (0.041) | −0.045 (0.027) | 0.27 | +0.019 (0.014) | −0.029 (0.032) | −1.52 | −0.009 (0.011) |
| gpi_ter | −0.073 (0.061) | −0.100 (0.056) | 1.37 | +0.004 (0.055) | −0.014 (0.060) | −3.55 | +0.015 (0.016) |

\* mys_female has short coverage (1990–): the lag coefficient is ≈0 and the future/change terms have no usable
variation; it is reported, not dropped, and excluded from the B3 count. Trend variants are in
`results/e11_ladder.csv` (`variant = country_trend_decade`); they are much smaller and noisier for several
indicators (e.g. lsc A2 S(t) +0.055 (0.013), lead +0.043 (0.021)), which is itself a caution that country trends
absorb much of the variation.

**Pre-registered decision (fixed before the run):**
- Levels ladder A2: lead term ≥ 80% of lag term in **4 of 8** indicators; lag ≥ 2× lead in **2 of 8** →
  verdict **"indeterminate"**.
- Change ladder B3: lead term ≥ 80% of lag in **5 of 7** usable indicators; lag ≥ 2× lead in **2 of 7** →
  verdict **"does not discriminate between a common development gradient, anticipation/quantity-quality, and a
  schooling effect"**.

**Interpretation limit (the point):** a future-schooling term as strong as the current term is consistent with
(i) a common development gradient, (ii) anticipation/quantity-quality — parents' fertility at t affects children's
schooling measured at t+10, and (iii) a schooling effect with a long lag. **This design cannot distinguish these
and cannot reject a schooling effect.** The reverse ladder (C) is the anticipation direction, not a test that can
confirm it. The trend-variant instability reinforces the caution.

---

## 3. Required text changes to Paper F (Codex F11)

Draft: `research/records/2026-11-25-paper-fertility/draft/paperF_draft.md` on `fix/fertility-text-2026-11-24`
(1,425 lines). Changes required before submission:

1. **L86 heading.** From: `**The gradient is a development gradient, not an identified schooling effect.**` To:
   `**The association is consistent with a common development gradient, with anticipation/quantity-quality, and with a schooling effect.**`
2. **L88–91.** From: "The pre-registered decision rule therefore fires: the level relation is descriptive.
   Countries with more schooling have fewer births, and the association cannot be read as the effect of changing
   schooling while holding development constant." To: "The pre-registered decision rule fires: the level relation
   cannot be read as the effect of changing schooling. But the placebo does not identify a development gradient
   either. Future schooling at t+10 can move with parents' fertility plans at t (anticipation/quantity-quality),
   and a schooling effect with a long lag predicts the same pattern. The association is consistent with all
   three; this design cannot distinguish them or reject a schooling effect."
3. **L106.** From: "so the descriptive claim survives while the causal one is rejected with evidence." To:
   "so the descriptive claim survives while no mechanism — common development trends, anticipation/
   quantity-quality, or a schooling effect — is identified or rejected."
4. **L590–596 (the placebo conclusion in §4.6).** From: "the level relation is a development-gradient association
   and not an identified schooling effect … it cannot be interpreted as the effect of changing schooling while
   holding development constant." To: "the level relation is not an identified schooling effect, and it is not
   evidence for a pure development gradient either: common development trends, anticipation/quantity-quality, and
   a long-lag schooling effect all predict the same future-schooling pattern."
5. **L601–604.** From: "it is what a development gradient looks like in a cross-section." To: "it is what a
   development gradient — or anticipation, or a long-lag schooling effect — looks like in a cross-section."
6. **L640 / §4.7.** From: "a quantified development-gradient caveat: the level relation is not an identified
   causal effect of schooling." To: "a quantified caveat that the level relation is not an identified causal
   effect; the future-schooling placebo cannot distinguish a development gradient from anticipation or a
   long-lag schooling effect."
7. **Construct labelling (all drafts).** Paper F's own fertility measure = births per woman and its label is
   correct (L324, L427). Add, wherever the transition/Q2 material is cited: "effective fertility (surviving
   children per woman) and total fertility (births per woman) are different constructs; they are not
   interchangeable and neither corrects the other." Never write "TFR" for effective fertility.
8. **Cite this record** where the placebo is discussed: the E11 ladder is the change-on-change analogue and
   returns "does not discriminate", so the paper cannot claim the placebo isolates a development gradient.

---

## 4. Audit note: what must soften

- **F11 (Paper F):** "development gradient" as a finding and "causal claim rejected" are too strong → softened as
  in §3. The defensible claim is: the level association is descriptive and is consistent with common development
  trends, anticipation/quantity-quality, and a schooling effect; the design cannot discriminate.
- **F03/Q2:** resolved as construct difference. The two lead/lag patterns are expected; do not describe one as a
  correction of the other. Report both outcomes with construct labels.
- **E11 verdict:** the change-on-change ladder does **not** establish temporal asymmetry in favour of a schooling
  effect, and does not establish a pure development gradient. That is the honest state of the design.

---

## 5. Provenance and traceability

- **Inputs (SHA-256, computed on autodl3):** `long_run_panel.csv` cd30d7ea…3280f2d; `mys_total.csv` 92c03f5c…02376fa;
  `mys_female.csv` aa822843…cbf8a4797. Project JSON series hashes are recorded in the run log on the box
  (`/root/work/e11`); the files are the restored `/root/work/data` panel (fertility.json 98436489…, sec.json
  7013a1d5…, lsc.json 182bdf7b…, prm_cmp.json d665de6e…, ter.json 2129cb8d…, gpi_sec.json 5bc20969…,
  gpi_ter.json d9a69ddf…, gdppc_log.json c4918991…, urban.json d1d3edcb…).
- **Scripts:** `scripts/q1_construct_audit.py`, `scripts/e11_ladder.py`. **Results:** `results/q1_construct_audit.txt/.json`,
  `results/e11_ladder.txt/.json/.csv`.
- **Commands:** `python ../scripts/q1_construct_audit.py /root/work/e11/data` and
  `python ../scripts/e11_ladder.py /root/work/data /root/work/e11/raw` on autodl3, with single-threaded BLAS.
- **Number → field:** construct statistics → `q1_construct_audit.json:descriptive.*`; matched-sample ladders →
  `q1_construct_audit.json:level_ladder.*` and `:change_direction.*`; ladder coefficients → `e11_ladder.csv`
  (`indicator,ladder,step,term,variant,coef,se,ci_lo,ci_hi,n,countries`); decision rule → `e11_ladder.json:decision`.
- **Data tiers:** `long_run_panel.csv` is **reconstructed before 1950** (OWID/Gapminder) and observed TFR after
  1950; project panel is observed; OWID mean-years are observed/reconstructed. No imputation was used.
- **Failures / deviations, recorded:** (i) conda NumPy on the box was broken (`~umpy.libs`, missing libopenblas
  shared object); fixed by a venv (NumPy 2.2.6) — no result depends on the broken install. (ii) First Q1 run
  failed on a wrong `long_run_panel.csv` path; fixed by copying the committed transition panel to
  `/root/work/e11/data` (hash above). (iii) Two script bugs (Series iteration; boolean mask) and one
  rank-deficient FE formula were found and fixed before the reported run; E11 now uses FWL residualisation.
  (iv) The initial formula-FE E11 attempt produced singular-matrix warnings and was discarded, not reported as
  results. (v) `mys_female` has insufficient change variation; reported as NA, not as a null.

---

## 6. Files

`PRE_REGISTRATION.md` (committed first, `d2c7558`); `REPORT.md` (this file); `scripts/q1_construct_audit.py`,
`scripts/e11_ladder.py`; `results/q1_construct_audit.txt`, `results/q1_construct_audit.json`,
`results/e11_ladder.txt`, `results/e11_ladder.json`, `results/e11_ladder.csv`.
