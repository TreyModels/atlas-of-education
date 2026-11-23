# Lead–lag matrix on the gap-filled panel, 23 Nov 2026
Server `/root/work/impute`; scripts in `scripts/`, results in `results/`. Panel `/root/work/data_imputed`
(217 countries x 74 years, 1950–2023: 20 draws `m01`–`m20`, `mean/`, `flags/`); observed data `/root/work/data`.
Estimator = recompute-branch matrix: each of 17 measures against every other (272 ordered pairs), the ten-year
change of the outcome regressed on the cause's starting level, own starting level, logged income, urbanisation,
country effects, decade effects, errors clustered by country; a second version adds a country trend. Income is
logged (the file holds levels). Threshold |t|>1.96.

## Is the existing run sound? Yes — verified by full rerun
The 16:07 `matrix_results.json` is sound: server scripts byte-identical to the branch, panel written (15:39)
before the matrix ran (16:07), and my from-scratch rerun (`matrix_ext.py`) reproduces its observed and imputed
estimates **exactly** (max difference 0.00e+00), so I use it after verifying it. **Baseline:** recompute-branch
matrix with true-log income — **127 links significant with country effects, 42 with trends, 24 survive both**;
my observed arm reproduces 127/42/24 exactly. The two other counts this session are implementation, not data:
handoff-run 126/45/25 used income in levels (the `gdppc_log` bug); grouping-multiverse 127/43/26 partials the
country trend once per country. **No sign flips at all** in the 61 changes.
## What the gap-filling adds, and how good it is
Coverage (share of 16,058 country-year cells; `results/coverage.csv`): education observed 26–38%, model-filled
18–35%, missing 28–52%; income/urbanisation observed 69–87%, long-run source 14–17%; fertility, life expectancy,
child mortality observed 73–86%, long-run source 14–18%; the other six measures are copied unchanged. Education
series gain 2.5–4.5x rows (median schooling link 2,266 -> 5,530; links with no schooling 4,305 -> 4,218).
Backcast validation (`validation_*.json`): error 10–25% of a standard deviation one year out, 20–45% at 6–10
years, 30–60% at 11–15; 90% intervals cover 89–94% within a validated 3–15 year horizon.
## Tests designed to kill "gap-filling is harmless"
1. **Observed cells only:** 129/44 significant vs 127/42 reference; only 8 of 544 verdicts differ, because the
   reference files carry a few 2024 endpoints the 1950–2023 panel cannot use. Masking itself changes nothing.
2. **The 20 imputations vs their standard errors.** "Lambda" = share of a link's uncertainty that comes from
   the 20 imputations disagreeing with each other rather than from sampling. Median 0.14, 90th percentile 0.59,
   max 0.94; 76/544 cells exceed 0.5. **Fourteen education cells exceed 0.8 — imputation artefacts, not results:**
   sec->lsc .94, sec->ter .94, tax->lsc .93, sec->gpi_ter .91, tax->gpi_ter .91, lsc->sec .91, lsc->gpi_ter .88,
   sec->fertility (trend) .87, sec->gpi_ter (trend) .82, gpi_ter->ter .82, gpi_ter->lsc .81, sec->u5mr .81,
   tax->gpi_sec .81, sec->lsc (trend) .81. Six of the 61 changed cells are in this class (tagged UNRELIABLE).
   Median 17 of 20 single imputations give the same verdict; 17 of the 61 are significant in all 20, 4 in none.
3. **Wrong-country permutation null (the real negative control):** one fixed random re-matching of the 217
   countries (no fixed points); the cause becomes the **same-year value of the matched other country**, outcome
   and controls stay own-country, same 544 cells. Share significant: observed **21.7%** with country effects,
   **8.5%** with trends; imputed panels 22.4–24.6% and 6.2–7.4%. So the estimator is nowhere near a clean 5%
   null — the excess is common global co-movement no control removes — and this matrix cannot certify causal
   links. What it can test is manufacture: **gap-filling does not raise the null rate** (+1.4 points with
   country effects, −1.5 with trends, i.e. noise), so the schooling fill does not create link-shaped association
   the observed data did not already have. The pre-registered negative-control link (another country's child
   mortality -> own schooling change) is null observed (-0.011, SE 0.021) and borderline in some imputed panels
   (-0.030, SE 0.014, ~4x rows): the imputed estimate sits inside the observed interval, so it is a power change,
   and with a 22% placebo false-positive rate it certifies nothing. The future-cause placebo (cause 20 years
   AFTER the outcome) is **not a usable null**: 39.0% significant in both panels.
4. **The mean-imputation trap — say it loudly.** Proper pooling over 20 draws gives 127/45. Treating the `mean/`
   panel as data gives **158 country-effect and 80 trend-significant links**: it manufactures ~30 extra
   "findings" by ignoring imputation uncertainty. Never use `mean/` for inference.
## (1) Fertility
All links keep their sign. The two observed-data survivors still survive both ways: child mortality -> fertility
**+0.008 (SE 0.001), n=8,567 -> +0.006 (0.000), n=11,225**, and life expectancy -> fertility **-0.049 (0.007),
n=9,268 -> -0.054 (0.005), n=11,744**. But the extra rows are the UN WPP splice and both sides are WPP
life-table outputs, so the *strengthening* is partly mechanical — they were already robust before gap-filling.
- Fertility -> schooling all survive: lower secondary **-4.79 (1.29), n=1,932 -> -6.23 (0.99), n=7,298**;
  secondary **-4.43 (0.85) -> -4.56 (0.98), n=8,909**; primary completion **-2.98 (1.18) -> -3.02 (1.08),
  n=5,493**; fertility -> income -0.065 -> -0.064.
- **"Births now strongly predict child mortality" (-0.56 -> -3.70) is not a discovery:** zero
  between-imputation spread because both sides are filled from the same UN WPP source (coverage-driven,
  mechanically entangled). Same for life expectancy <-> child mortality.
- **Urbanisation -> fertility (trends) is a precision gain, not a new effect:** -0.014 (0.007, n.s.) ->
  -0.017 (0.006, significant); the estimate moved by 0.003, under half its original SE. Fertility -> primary
  completion loses its trend version (-2.73 -> -1.99), gender parity -> fertility gains one (-0.31 -> -0.25),
  fertility -> tertiary parity gains one (-0.024 -> -0.048). All marginal; listed below.
## (2) Massification
- **The main conclusions are unchanged.** Electricity -> lower secondary **+0.348 (0.084), n=1,414 -> +0.383
  (0.102), n=3,584**; -> secondary +0.362 -> +0.341; -> primary +0.345 -> +0.423 — still significant with
  country effects, still dead under country trends. Income -> secondary +5.97 -> +5.81; urbanisation ->
  secondary +0.78 -> +0.74 (survives both). The extra rows keep the same estimates: counting, not new effects.
- **What genuinely weakens:** paid jobs -> tertiary **+1.083 (0.458, n=1,874) -> +0.503 (0.318, n=3,765)**,
  losing significance with lambda 0.04 — a real estimate change once missing tertiary data are included, and
  it reinforces the earlier warning that wage -> tertiary was fragile. Gender parity in tertiary ->
  lower/secondary/tertiary lose significance with lambda 0.76–0.82: **unreliable imputation, not evidence the
  ladder is absent.** The schooling ladder is mechanically entangled by construction and is tagged MECHANICAL.
- **Of the 18 new trend survivors, most are not new knowledge:** 6 are precision gains (estimate essentially
  unchanged), 4 are coverage-driven from the macro splice, 2 are the mechanically entangled WPP pair; the
  remaining 6 moved materially (fertility->gpi_ter, parity->secondary, life_exp->lsc, life_exp->prm_cmp,
  primary->secondary, u5mr->lsc). Seven old survivors drop: sec->ter, sec->agri_va, ter->lsc, ter->prm_cmp,
  gpi_ter->lsc, fertility->prm_cmp, income->secondary. "35 survivors" is not 35 robust findings.

## Every changed verdict (55 links; observed -> imputed, estimate (SE), rows)
Tags: precision = estimate moved < half its original SE, only certainty changed; coverage = reproduced with
education left as observed, i.e. added long-run macro rows (between-imputation spread ~0); moved = estimate
genuinely moved; UNRELIABLE = lambda >= 0.8; MECHANICAL = definitionally entangled. Every changed cell is here;
full columns in `results/changed_verdicts.csv`.

| area | link | country effects | country trends |
|---|---|---|---|
| fert | fertility -> gpi_ter | — | gained: -0.024(0.03) n2171 -> -0.048(0.02) n7862 [moved] |
| fert | fertility -> prm_cmp | — | lost: -2.732(1.26) n2566 -> -1.985(1.46) n5484 [coverage] |
| fert | fertility -> u5mr | gained: -0.556(1.77) n8569 -> -3.699(1.53) n11225 [coverage,MECHANICAL] | gained: -0.828(1.84) n8567 -> -3.198(1.58) n11225 [coverage,MECHANICAL] |
| fert | fertility -> wage_emp | gained: -0.560(0.32) n4326 -> -0.655(0.32) n4370 [precision] | — |
| fert | gpi_sec -> fertility | — | gained: -0.308(0.16) n4887 -> -0.245(0.11) n7102 [precision] |
| fert | urban -> fertility | — | gained: -0.014(0.01) n9270 -> -0.017(0.01) n11744 [precision] |
| mass | agri_va -> gpi_sec | gained: -0.003(0.00) n2688 -> -0.003(0.00) n4855 [precision] | — |
| mass | agri_va -> gpi_ter | gained: -0.002(0.00) n2041 -> -0.003(0.00) n5716 [precision] | — |
| mass | electricity -> gpi_ter | — | lost: -0.002(0.00) n1515 -> -0.001(0.00) n3650 [moved] |
| mass | emp_agri -> gpi_sec | lost: -0.003(0.00) n1841 -> -0.003(0.00) n3173 [precision] | — |
| mass | emp_agri -> gpi_ter | lost: -0.006(0.00) n1645 -> -0.002(0.00) n3871 [moved] | — |
| mass | emp_agri -> prm_cmp | — | lost: +0.617(0.23) n1745 -> +0.366(0.21) n3199 [moved] |
| mass | gdppc_log -> gpi_sec | gained: -0.033(0.02) n3290 -> -0.044(0.02) n6297 [moved] | — |
| mass | gdppc_log -> sec | — | lost: +4.515(2.03) n3390 -> +3.928(2.20) n8908 [precision] |
| mass | gdppc_log -> ter | gained: +4.121(2.40) n2857 -> +5.544(2.46) n7248 [moved] | — |
| mass | gpi_sec -> agri_va | — | lost: -3.924(1.94) n3991 -> -1.874(1.69) n5499 [moved] |
| mass | gpi_sec -> flfp | gained: -4.797(2.58) n2878 -> -3.681(1.76) n3880 [precision] | — |
| mass | gpi_sec -> gpi_ter | — | gained: +0.065(0.09) n1733 -> +0.095(0.04) n5901 [precision] |
| mass | gpi_sec -> sec | — | gained: +1.258(2.56) n2944 -> +5.573(2.79) n6435 [moved] |
| mass | gpi_ter -> lsc | lost: +14.036(4.99) n1335 -> +10.095(6.11) n6608 [UNRELIABLE] | lost: +7.088(3.18) n1272 -> +4.512(4.96) n6605 [moved] |
| mass | gpi_ter -> sec | lost: +10.684(3.14) n2146 -> +5.831(4.61) n7814 [moved] | — |
| mass | gpi_ter -> ter | lost: +18.445(4.25) n2385 -> +9.525(5.10) n7042 [UNRELIABLE] | — |
| mass | gpi_ter -> u5mr | gained: +9.481(4.91) n3125 -> +13.318(5.33) n7763 [coverage] | — |
| mass | life_exp -> lsc | — | gained: +0.052(0.22) n1873 -> +0.470(0.22) n7298 [moved] |
| mass | life_exp -> prm_cmp | — | gained: +0.280(0.29) n2566 -> +0.457(0.20) n5484 [moved] |
| mass | life_exp -> ter | — | lost: -0.518(0.20) n2811 -> -0.116(0.09) n7248 [moved] |
| mass | lsc -> sec | lost: +0.125(0.06) n1943 -> +0.098(0.07) n7280 [UNRELIABLE,MECHANICAL] | — |
| mass | prm_cmp -> sec | — | gained: +0.017(0.04) n2351 -> +0.069(0.03) n5719 [moved] |
| mass | prm_cmp -> u5mr | gained: +0.140(0.08) n3485 -> +0.107(0.05) n5655 [precision] | lost: +0.150(0.07) n3473 -> +0.062(0.03) n5647 [moved] |
| mass | prm_cmp -> urban | lost: +0.033(0.01) n3561 -> +0.009(0.01) n5766 [moved] | — |
| mass | sec -> agri_va | lost: +0.039(0.02) n3851 -> +0.017(0.02) n6285 [moved] | lost: +0.057(0.02) n3824 -> +0.019(0.02) n6282 [moved] |
| mass | sec -> gpi_ter | lost: +0.002(0.00) n1935 -> +0.000(0.00) n7750 [UNRELIABLE] | — |
| mass | sec -> life_exp | gained: -0.007(0.01) n4548 -> -0.011(0.01) n8969 [precision] | — |
| mass | sec -> ter | lost: +0.228(0.06) n2456 -> +0.104(0.10) n7126 [UNRELIABLE,MECHANICAL] | lost: +0.099(0.05) n2419 -> +0.011(0.03) n7125 [moved,MECHANICAL] |
| mass | sec -> u5mr | — | gained: +0.093(0.06) n4407 -> +0.091(0.04) n8697 [precision] |
| mass | tax -> gpi_sec | lost: -0.002(0.00) n1773 -> -0.000(0.00) n2710 [UNRELIABLE] | — |
| mass | ter -> agri_va | — | lost: +0.032(0.01) n3278 -> +0.021(0.01) n5764 [moved] |
| mass | ter -> flfp | gained: +0.039(0.02) n2434 -> +0.031(0.01) n4185 [precision] | — |
| mass | ter -> life_exp | gained: -0.017(0.01) n3854 -> -0.019(0.01) n7423 [precision] | — |
| mass | ter -> lsc | lost: -0.090(0.04) n1465 -> -0.028(0.07) n6355 [moved,MECHANICAL] | lost: -0.155(0.06) n1403 -> -0.116(0.09) n6355 [moved,MECHANICAL] |
| mass | ter -> prm_cmp | — | lost: -0.108(0.05) n1887 -> -0.094(0.07) n5125 [precision] |
| mass | ter -> urban | — | lost: -0.034(0.01) n3818 -> -0.012(0.01) n7419 [coverage] |
| mass | u5mr -> gpi_sec | — | gained: -0.001(0.00) n3203 -> -0.001(0.00) n6167 [coverage] |
| mass | u5mr -> lsc | — | gained: -0.062(0.05) n1840 -> -0.085(0.03) n7156 [moved] |
| mass | u5mr -> prm_cmp | — | gained: -0.090(0.05) n2520 -> -0.113(0.03) n5388 [precision] |
| mass | urban -> gpi_ter | — | gained: +0.005(0.01) n2171 -> +0.006(0.00) n7862 [precision] |
| mass | wage_emp -> ter | lost: +1.083(0.46) n1874 -> +0.503(0.32) n3765 [moved] | — |
| other | agri_va -> u5mr | gained: +0.284(0.18) n6583 -> +0.415(0.20) n6558 [coverage] | — |
| other | emp_agri -> gdppc_log | lost: -0.008(0.00) n4305 -> -0.005(0.00) n4175 [coverage] | — |
| other | gdppc_log -> life_exp | gained: -0.427(0.30) n9270 -> -0.677(0.27) n11744 [coverage] | — |
| other | life_exp -> u5mr | — | gained: +0.739(0.38) n8565 -> +1.154(0.43) n11225 [coverage,MECHANICAL] |
| other | life_exp -> urban | — | gained: +0.032(0.05) n9268 -> +0.100(0.05) n11744 [coverage] |
| other | u5mr -> gdppc_log | — | gained: -0.001(0.00) n8543 -> -0.002(0.00) n11207 [coverage] |
| other | urban -> flfp | — | lost: +0.122(0.05) n4499 -> +0.100(0.05) n4550 [precision] |
| other | wage_emp -> gdppc_log | — | gained: -0.004(0.00) n4303 -> -0.005(0.00) n4175 [coverage] |

## Files and provisos
`scripts/`: `matrix_ext.py`, `matrix_decomp.py` (education-only vs macro-only), `null_placebo.py` (wrong-country
permutation), `analyse_ext.py`. `results/`: `all_links.csv` (all 544 cells: estimate, SE, n, countries, verdicts,
observed vs imputed), `changed_verdicts.csv` (61 cells with labels, per-imputation range, leave-one-out
stability), `summary.txt`, `coverage.csv`, `placebo.csv`, `matrix_ext.json`, `matrix_decomp.json`,
`null_placebo.json`, `validation_*.json`, `prior_matrix_results_1607.json`. Provisional: UNRELIABLE cells must
not be quoted; mechanically entangled links are not discoveries; precision/coverage changes are statements
about rows. Both nulls show a large common-trend component: association map, not causal map.
