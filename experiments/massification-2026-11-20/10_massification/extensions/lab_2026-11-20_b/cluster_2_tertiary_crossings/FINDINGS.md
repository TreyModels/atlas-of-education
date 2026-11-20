# Cluster 2 — Tertiary Crossing Structure (X4, X5, X6)

All numbers below are quoted from the results CSVs in `results/` of this directory
(`X4_crossing_typicality.csv`, `X5_package_contrast.csv`, `X6_spacing_structure.csv`,
`CLUSTER_RESULTS.csv`). Crossing years are band midpoints / band_latest / last_obs_year taken
directly from `UNIVERSALIZATION_TIMING.csv` (GER rows) — they are never fitted or interpolated
from outcomes. Structure values are observed panel values (exact year or interpolation within the
1995–2024 observed panel range; no extrapolation). No causal or directional claims are made;
these are descriptive cross-sectional contrasts in a very small sample (n ≤ 6 systems:
Cambodia, China, Hong Kong SAR, Japan, Philippines, Republic of Korea).

**Censoring summary.** Left-censored milestones used at band_latest: Japan tertiary-15 (1971),
tertiary-50 is dated (band 1999–2013, midpoint 2006); Japan secondary-50 (2013) and secondary-90
(2013); Korea tertiary-15/tertiary-50/secondary-50/secondary-90 (2000 each); Hong Kong
secondary-50 (2001); Philippines tertiary-15 (1971). Right-censored (excluded from medians):
Cambodia tertiary-50 (last_obs 2025) and Cambodia secondary-90 (last_obs 2024). Structure values
are missing for crossings before 1995 (Philippines/China secondary-50, Japan/Korea/Hong Kong/
Philippines tertiary-15 at 1971–2000 in some cases) because the structure panel starts in 1995.

## X4 — Structure typicality at tertiary vs secondary crossings

Verdict (CLUSTER_RESULTS.csv): **NOT SUPPORTED / NOT SUPPORTED** (tertiary set / secondary set).

- Milestone set "tertiary 15 + tertiary 50": inside-IQR counts LGDP=3/5, URBAN=3/5, SVCS=3/5
  (n_with_values=5 per variable; crossings before 1995 and the right-censored Cambodia
  tertiary-50 at 2025 have no structure value). Threshold requires >=4/6 inside IQR on >=2 of 3
  variables; max inside count is 3/5 → NOT SUPPORTED.
  - Medians (Q1–Q3): LGDP 9.864586 (9.588081–10.433259); URBAN 79.579961 (59.540096–87.146090);
    SVCS 60.480267 (43.139615–67.887147).
- Milestone set "secondary 50 + secondary 90": inside-IQR counts LGDP=2/6, URBAN=2/6, SVCS=2/6
  (n_with_values=6 per variable). Max inside count 2/6 → NOT SUPPORTED.
  - Medians (Q1–Q3): LGDP 9.511488 (9.112449–10.410906); URBAN 67.100142 (50.245980–88.258735);
    SVCS 59.122575 (42.492350–68.313633).

## X5 — Same package or different package? (tertiary-50 vs secondary-90)

Verdict (CLUSTER_RESULTS.csv): **DATA LIMITED** — dated crossings per set fall below the frozen
minimum of 4 (dated n tertiary50=4, secondary90=3 in the note column of CLUSTER_RESULTS.csv;
right-censored Cambodia excluded, left-censored Japan-secondary-90 and Korea excluded).

Per-variable table still reported (CONTRAST rows of X5_package_contrast.csv):

| variable | median tertiary_50 | median secondary_90 | diff_or_Q3 (median diff) | pooled_IQR_width | absdiff_over_IQR | flag |
|---|---|---|---|---|---|---|
| LGDP | 10.433259 | 9.158391 | 1.274869 | 1.395515 | 0.913547 | different |
| URBAN | 87.146090 | 54.620322 | 32.525768 | 40.936257 | 0.794547 | different |
| SVCS | 67.887147 | 57.764883 | 10.122264 | 34.152958 | 0.296380 | same |

Mapping of verdict labels: the two-sided question maps "same-dominant (>=2 of 3 variables with
|diff| <= 0.50*pooled IQR)" → SAME PACKAGE and "different-dominant (>=2 of 3 with > 0.50)" →
DIFFERENT PACKAGE, replacing SUPPORTED/NOT SUPPORTED; mixed patterns → PARTIAL; below the n>=4
minimum per set → DATA LIMITED (what happened here). Directional sign consistency cannot be
adjudicated at this n and is not claimed.

## X6 — Secondary→tertiary spacing vs structure

Verdict (CLUSTER_RESULTS.csv): **UNABLE** (n=3 < 4).

Countries with both crossings dated (X6_spacing_structure.csv): Hong Kong SAR gap −4.000000
(tertiary-50 2007.5 minus secondary-90 2011.5; secondary-50 was left-censored so secondary-90 was
substituted — disclosed), Philippines gap 48.000000 (2024.5 − 1976.5), China gap 44.000000
(2016.5 − 1972.5). Excluded: Japan (no dated secondary milestone — secondary-50 and substituted
secondary-90 both left-censored), Cambodia and Republic of Korea (tertiary-50 censored:
right-censored 2025 and left-censored 2000 respectively). Structure values at the secondary
crossing exist only for Hong Kong (2001/2011.5) and Korea-excluded cases within the 1995–2024
panel window, so Spearman rho could not be computed for LGDP, URBAN, or SVCS (rho columns blank;
per-variable n recorded as 0 in the rho rows).

## Caveats

- Extremely small n (<= 6 systems); every verdict is fragile to one country's censoring or one
  missing structure year.
- Left-censored crossings (true crossing at or before band_latest) bias crossing years upward;
  right-censored crossings were excluded from medians rather than imputed.
- Structure variables exist only 1995–2024; crossings before 1995 have no structure value and
  were never extrapolated.
- Crossing years are descriptive band-derived dates, never fitted; nothing here supports causal
  or directional interpretation.
