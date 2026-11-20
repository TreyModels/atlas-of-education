# Y3 — Capacity floor-not-ceiling observed check (6 systems, descriptive)

**Verdict: `NOT SUPPORTED`.** The floor condition was met at the boundary, but the ceiling condition was not,
so under the predeclared conjunction the descriptive claim "capacity (here: PTR improvement) tracks the floor,
not the ceiling" is **not separable** in these six systems and is reported as UNABLE/not separable per the
declared falsifier. It is not rescued, respecified or re-run.

- Predeclaration: `10_massification/extensions/lab_2026-11-20_c/PRE_DECLARATIONS.md`,
  sha256 `8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1` (frozen; no threshold changed).
- ΔPTR-improvement = secondary PTR (`SE.SEC.ENRL.TC.ZS`) earliest observed ≥1995 minus latest observed ≤2024;
  positive = improvement. All six systems have the series in `panel_wdi_long.csv`; where an overlap with
  `JOBS_AND_MARKETS_PANEL.csv` `SE.SEC.ENRL.TC.ZS` exist, the overlapping values are identical, and
  ΔPTR from the jobs panel is identical for all six systems (`abs_diff_vs_panel` = 0.0), so the source choice
  changes nothing. No imputation anywhere.

## Correlations

| pair | rho | n | component met |
|---|---|---|---|
| ΔPTR-improvement vs **floor** (latest completion_primary, fallback SE.PRM.CMPT.ZS) | 0.5 | 5 | True (positive, `|rho| >= 0.50`, at the boundary) |
| ΔPTR-improvement vs **ceiling** (latest completion_upper_secondary, fallback ger_tertiary) | 0.6 | 6 | False (`|rho| >= 0.50`) |

Predeclared rule (verbatim): SUPPORTED only if ρ(ΔPTR-improvement, floor) is POSITIVE with `|rho| >= 0.50`
AND `|rho(ΔPTR-improvement, ceiling)| < 0.50` (or sign-inconsistent); falsifier → UNABLE/not separable
otherwise.

- floor: ρ = 0.5 — positive and exactly at the 0.50 bar. Met, but only at the boundary, on n = 5.
- ceiling: ρ = 0.6 — magnitude at or above the 0.50 bar → **condition 2 failed**. No ceiling sign was
  predicted in the predeclaration, so the "sign-inconsistent" escape cannot be invoked; that reading is
  recorded in `results/Y3_correlations.csv`.
- Conjunction: `NOT SUPPORTED` (not separable), i.e. the falsifier fires.

## Every system's values

| system | ΔPTR-improvement | floor (source) | ceiling (source) |
|---|---|---|---|
| CHN | 1.8148600000000012 | 99.19 (completion_primary, 2020) | 87.52 (completion_upper_secondary, 2020) |
| HKG | 8.90912 | 91.6803149606299 (SE.PRM.CMPT.ZS, 2024) | 120.0897903442383 (ger_tertiary, 2024) |
| JPN | 0.32211000000000034 | UNABLE (no completion_primary, no SE.PRM.CMPT.ZS on disk) | 65.2245864868164 (ger_tertiary, 2024) |
| KHM | -11.74569 | 84.6092529296875 (completion_primary, 2023) | 27.87285614013672 (completion_upper_secondary, 2023) |
| KOR | 11.334249999999999 | 100.0 (completion_primary, 2012) | 99.4581527709961 (completion_upper_secondary, 2023) |
| PHL | 12.32215 | 98.30461883544922 (completion_primary, 2024) | 75.02525329589844 (completion_upper_secondary, 2024) |

PTR coverage (observations inside 1995–2024, first→last year): CHN 20 (1995→2018), HKG 19 (1996→2018),
JPN 4 (2014→2017), KHM 8 (1998→2007), KOR 23 (1995→2017), PHL 16 (1995→2017). Full detail and per-cell
coverage flags are in `results/Y3_country_detail.csv`.

## Caveats and scope

- **SMALL-N WARNING: n = 6 systems at most** — n = 5 for the floor pair (JPN floor UNABLE) and n = 6 for the
  ceiling pair; the two ρ are therefore computed on different point sets. A six-point Spearman takes only a
  few discrete values and one system swings it. The floor result (0.5) sits exactly on the 0.50 bar, and the
  floor values are compressed (84.6092529296875 for KHM, 91.6803149606299–100.0 for the other four), so the
  rank correlation is carried almost entirely by KHM being the only low-floor, negative-improvement system.
- **Knife-edge, disclosed (`results/Y3_leave_one_out.csv`):** dropping one system at a time gives floor ρ of
  0.0 (excluding KHM), 0.4 (HKG), 0.4 (KOR), 0.5 (JPN), 0.8 (CHN), 0.8 (PHL), and ceiling ρ of 0.3 (JPN),
  0.3 (KHM), 0.6 (CHN), 0.7 (HKG), 0.7 (KOR), 0.9 (PHL). Both predeclared conditions hold simultaneously only
  in the variant that drops JPN — the one system whose floor is UNABLE. The declared run uses n = 6 for the
  ceiling pair (JPN has a ceiling), so the reported verdict stays `NOT SUPPORTED`; the leave-one-out table is
  disclosure of fragility, **not** a re-specification and **not** a second verdict.
- **Measure fallbacks (recorded per country, never imputed):** floor for HKG uses `SE.PRM.CMPT.ZS`; ceiling
  for HKG and JPN uses `ger_tertiary`, a gross enrolment ratio rather than a completion rate. Mixing a
  completion rate with a GER across points is a real limitation of this check and is one reason a 6-point
  ρ should not be read as more than a description.
- **Provenance limits:** KOR's floor comes from a single observed year (2012); CHN's floor and ceiling come
  from 2020; the PTR series for CHN and HKG stop in 2018 and for KHM in 2007, so "latest observed ≤2024" is
  not 2024 for all systems. Values are bounded at ≤2024 to respect the declared data window.
- **Descriptive label:** every row is `observed`. No causal or direction claim is made, no "capacity explains
  timing" claim, no policy-effect claim. C1–C4 are not reopened; the phase stays CLOSED at
  PARTIAL/DESCRIPTIVE/EQUIVALENT.
- Does not reopen C4 (annual observed capacity/enforcement): uses only the already-ruled partial PTR/teacher
  path (D53/R26).

## Files

`code/run.py` → `results/Y3_country_detail.csv` (all six systems, every value, source and year),
`results/Y3_correlations.csv` (both ρ, n, component flags, excluded systems),
`results/Y3_ptr_source_sensitivity.csv` (panel vs jobs PTR), `results/Y3_leave_one_out.csv`
(per-system exclusion stability), `results/CLUSTER_RESULTS.csv`.
`RUN_MANIFEST.json` carries input/code hashes and the reproducibility note.
