# Y1 — Ceiling-residual candidate-account screen (descriptive)

**Verdict: `NOT SUPPORTED`.** Both predeclared conditions failed, so the opportunity-cost account is
discarded from the D63 candidate list under this screen. This is a *screen outcome*, not evidence against
any mechanism: `SUPPORTED` here would only ever have meant "the candidate account survives".

- Predeclaration: `10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md`,
  sha256 `8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1` (frozen; no threshold changed).
- Estimator (declared): country-level last-3-observed means inside 2000–2024; Spearman on country cells;
  rank-partial = Pearson of rank residuals after regressing each rank series on the rank of the control
  `NY.GDP.PCAP.PP.CD`. No imputation, no RNG. Verified against the algebraic partial-Spearman identity.

## 30-country screen (n = 30, countries = 30)

| candidate | indicator | rho_raw | rho_partial_income | n |
|---|---|---|---|---|
| agri_share (opportunity cost) | SL.AGR.EMPL.ZS | -0.7179087875417131 | -0.10538277771148254 | 30 |
| youth_unemp | SL.UEM.1524.ZS | 0.05717463848720801 | 0.24600234433273743 | 30 |
| wage_share (returns/demand) | SL.EMP.WORK.ZS | 0.7370411568409344 | 0.13230467040639488 | 30 |

Predeclared rule (verbatim): a candidate note only if `rho_partial(ceiling, agri) <= -0.40` AND
`rho_partial(ceiling, youth_unemp) <= -0.40`; falsifier → UNABLE/discard if either `|rho| < 0.40` or the sign
is positive.

- agri-share: ρ = -0.10538277771148254 — magnitude below the 0.40 bar → **condition 1 failed**.
- youth-unemployment: ρ = 0.24600234433273743 — positive sign → **condition 2 failed**.
- wage-share: ρ = 0.13230467040639488 — reported only, no threshold attached, not adjudicated.

Reading: the *raw* rank association of the tertiary ceiling with the agricultural employment share is
-0.7179087875417131, and with the formal wage-share 0.7370411568409344. Nearly all of that raw association
is absorbed by the income rank control — after the declared rank-partial, neither survives. That is exactly
the outcome the screen was designed to detect, and it is reported as such, not rescued.

## Six-system check (descriptive)

| ceiling variable | candidate | rho | n | countries |
|---|---|---|---|---|
| completion_upper_secondary | agri | -0.8 | 4 | CHN;KHM;KOR;PHL |
| completion_upper_secondary | wage_share | 0.8 | 4 | CHN;KHM;KOR;PHL |
| ger_tertiary | agri | -0.7142857142857143 | 6 | CHN;HKG;JPN;KHM;KOR;PHL |
| ger_tertiary | wage_share | 0.7142857142857143 | 6 | CHN;HKG;JPN;KHM;KOR;PHL |

These six-system figures are raw (no income control) and are **not** adjudicated against the Y1 threshold;
they are reported because the predeclaration asks for them. They point the other way from the 30-country
income-partial screen, on n = 4 and n = 6 points. The contradiction is left standing: at that n a single
system materially moves ρ, and the six-system cells come from a different file, window and measure mix
(completion rate vs gross enrolment ratio).

## Caveats and scope

- **Small-n caveat:** the 30-country screen has n = 30, so no small-n caveat applies there. The six-system
  check has n = 4 (completion_upper_secondary) and n = 6 (ger_tertiary) and is **descriptive only**.
- **Descriptive label:** every row is `derived` (country-level last-3 means and rank statistics computed from
  observed series); no cell is imputed; no series was substituted.
- **No causal or direction claim is made.** No mechanism is asserted, no push/pull direction, no
  policy-effect claim. The screen answers only "does this candidate account survive the predeclared
  threshold", and it does not.
- **Closed claims untouched:** C1–C4 are not reopened; the phase stays CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT.
- Terminal values were bounded at ≤2024 to respect the declared data window; the year used is recorded
  per system in `results/Y1_six_system.csv`.

## Files

`code/run.py` → `results/Y1_country_panel.csv` (all 30 country rows, every series' last-3 mean, years used
and observation counts), `results/Y1_correlations.csv` (raw + partial ρ per candidate, with the threshold
text and component flag), `results/Y1_six_system.csv`, `results/Y1_six_correlations.csv`,
`results/CLUSTER_RESULTS.csv`. `RUN_MANIFEST.json` carries input/code hashes and the reproducibility note.
