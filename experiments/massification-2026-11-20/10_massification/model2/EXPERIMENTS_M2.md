# EXPERIMENTS — model2: independent scaling, universalization dynamics, rival comparison, push-pull recovery

**Observed vs simulated is labelled throughout.** Observed data: `04_data/ECONOMY_SERIES.csv`,
`04_data/data/gmr_observed_6countries_1970_2024.csv` (observed UIS cells only), and
`09_relations/data/panel_wdi_eci.csv` (WDI30 wide panel). `10_massification/data/` and
`10_massification/relations/` were EMPTY at run time (workstreams 34/36 not landed), so the fallback declared
in `PRE_DECLARATIONS_M2.md` was used; the script re-reads them first if present. **No imputed panel
(`gmr_annual_1980_2020_imputed.csv`) was used.** Simulated data appears only in Part 4 and is labelled
SIMULATED. Closed shadow-education claims are not re-fit. Code: `code/m2.py`; outputs in `runs/`.

## Part 1 — Independent scaling exponents (different estimator/sample than pattern-scout)

Independent estimators: 10-year long differences (period FE, country-clustered), between (country means,
HC1), country-specific time series (Newey–West lag 3, median), first differences (year FE, country-clustered).
Pattern-scout's levels two-way FE is computed only as a reference row. Two samples: UIS6 (observed, 1980–2024)
and WDI30 (observed WDI cells). Representative between-sample exponents (SE):

| relation | UIS6 (6 countries) | WDI30 (30 countries) |
|---|---|---|
| GER secondary ~ GDP pc (log-log) | +0.250 (0.088) | **+0.286 (0.045)** |
| GER tertiary ~ GDP pc | +0.721 (0.171) | **+0.776 (0.086)** |
| upper-sec completion (logit) ~ GDP pc | +2.226 (0.561) | **+0.843 (0.157)** |
| agriculture share (log) ~ GDP pc | −1.446 (0.419) | **−1.360 (0.168)** |
| services share (log) ~ GDP pc | +0.336 (0.073) | — |
| urbanisation (logit) ~ GDP pc | +1.113 (0.109) | **+1.488 (0.276)** |
| wage-share (log) ~ GDP pc | +0.254 (0.035) | — |
| upper-sec completion (logit) ~ log TFR | — | −1.157 (0.432) |

**Law vs regularity classification (predeclared rule: sign stable + |exponent| within factor 2 across
estimators and ≥2 significant estimates).** *Scaling laws* on WDI30: **GER secondary ~ income (+0.286;
magnitude ratio 1.74)**, **GER tertiary ~ income (+0.776; ratio 1.89)**, **lower-secondary completion
(logit) ~ income (+0.843-ish; ratio 1.76)**. *Period/region regularities (sign stable, magnitude unstable
across samples/estimators):* upper-secondary completion (~income, ratio 2.97), agriculture share (ratio
11.2), education spending→secondary GER (ratio 16.5), urbanisation (sign unstable across samples), and
**all UIS6 pairs are regularities** (small N, ratio 2.5–10.4). **GER primary ~ income: unidentified
(0 significant estimates)** — saturation. **Returns vs schooling: UNABLE** — no earnings microdata in any
on-disk panel; the 8.8% Mincer figure is calibration-only and is not used as an observation.

## Part 2 — Universalization dynamics

- **Logistic fits** per country × level (GER primary/secondary/tertiary, upper-sec completion), residual
  bootstrap B=120 for parameter SEs (`seed 1`), reported in `runs/logistic_fits.csv`. WDI30 GER secondary:
  median K ≈ 130 (sd 33), r ≈ 0.077 (sd 0.095), t0 ≈ 2000 (sd 26); GER tertiary: median K ≈ 87 (sd 52),
  r ≈ 0.114, t0 ≈ 2020 (sd 17) — wide parameter uncertainty, many series not near saturation.
- **Common-parameters test:** common-r (country-specific K,t0) does **not** beat country-specific fits
  (shared=False; GER secondary AIC sep 3052.9 vs common-r AIC not finite/converged; same for tertiary) —
  **countries do not share a common slope** at this design.
- **Lead–lag (education vs structural change):** short panels (differenced annual data) leave only 2
  countries with usable WDI30 series on all three drivers; median peak lag for education vs urbanisation is
  +1y but the country coverage is too thin to identify a lead-lag — reported as **NOT IDENTIFIABLE** at
  this sample (see `runs/lead_lag.csv`; UIS6 differenced series too short after matching). What cannot be
  identified: direction/timing of education-structure lead-lag from these short panels.

## Part 3 — Rival comparison (demand-led / supply-led / complementary)

Country-level time series, train 1980–2010, test 2011–2024 (`runs/rivals.csv`): **23 countries** with
enough training and test points. Demand-led (pull: lagged income + agriculture) wins out-of-sample in
**8/23** countries; supply-led (AR(1)+trend with a push equation for GDP growth) wins in **15/23**; median
OOS RMSE demand 0.182 vs supply 0.123 (log points). Median estimated push coefficient (education →
Δlog GDP) is **+0.026**, small. **Observational equivalence:** the two rivals' predicted education differs
by less than 2× residual noise over a substantial part of the observed covariate space — the rival models are
**observationally close** on these data (see `runs/rivals.csv`; equivalence is quantified in the recovery
design below, where AIC equivalence occurs for 7% of candidate-truth simulations, but the OUTSIDE truth is
always forced — see Part 4).

## Part 4 — Push–pull identification (SIMULATED; the decisive test)

Panel 30 countries × 30 years simulated from four truths (demand-led/pull, supply-led/push, complementary,
and an OUTSIDE cohort/fertility truth), generator masked, three rivals fitted and chosen by AIC
(`runs/recovery.csv`; seeds 0–4 per truth):

| truth | recovery (correct rival chosen) |
|---|---|
| demand-led (pull) | **1.00** |
| supply-led (push) | **1.00** |
| complementary | **0.00** (misclassified) |
| OUTSIDE cohort/fertility | — forced-ID **1.00** (always classified as a candidate channel) |

**Observational-equivalence share (candidate truths, AIC gap < 2): 0.07.**
**Predeclared threshold:** identifiable iff recovery ≥0.67 AND forced-ID = 0 AND equivalence <0.34.
**Verdict: PUSH–PULL NOT IDENTIFIABLE at this design.** Pure push and pure pull worlds are recoverable when
one channel is shut down, but **the outside cohort/fertility truth is forced into a candidate channel in
100% of simulations** — i.e. cross-country panels cannot tell "education follows jobs/income" from
"education is cohort/fertility-driven" without an additional discriminating moment. The complementary world
is not recovered at all. No claim about direction is made from observed data.

## Strongest discriminating evidence (what the data *can* separate)

1. In observed country panels the **push coefficient (education → GDP growth) is small (+0.026)** and the
   pull terms (income, agriculture) fit education out-of-sample in a large minority of countries — consistent
   with demand-side association, not with a strong push channel.
2. The **identification test fails** where it matters: an outside (cohort/fertility) truth is always
   assigned to a candidate channel (forced-ID = 1.00), and the complementary rival is never recovered
   (recovery 0.00). So the discriminating evidence is **not sufficient** for a push-pull verdict on
   cross-country data; the strongest available indicator is the small observed push coefficient plus the
   observational closeness of the rivals.
3. **Returns vs schooling** cannot be estimated on these data (UNABLE), removing a second potential
   discriminating moment.

## Caveats
- Small observed samples: 6 UIS6 countries, 30 WDI30 countries; short annual panels; sparse GER/completion
  coverage; parameter estimates are associational (no causal identification), and logistic fits are
  under-determined for series not near saturation.
- The push–pull recovery is a **simulated** design; recovery/forced-ID rates are properties of this design,
  not of the world.
- `10_massification/data|relations` were empty at run time; results should be re-run when they land (script
  reads them first if present).
