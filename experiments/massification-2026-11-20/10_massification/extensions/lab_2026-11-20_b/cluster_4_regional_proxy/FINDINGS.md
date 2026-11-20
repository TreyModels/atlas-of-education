# Cluster 4 — Regional Post-Secondary Proxy (X10/X11/X12)

**BINDING LIMITATION (applies to all sections and every row of every results file):** regional tertiary enrolment is NOT observed on disk; there is no PHL regional tertiary GER/participation series. All cells use regional attainment/inequality proxies and national tertiary GER as CONTEXT ONLY. No causal or policy-effect claim. The cohort comparison is descriptive.

## X10 — Regional convergence in mean years of schooling

- Spearman rho of dMYS vs MYS_initial across 17 regions: **-0.443627** (n=17; from `results/X10_convergence.csv` summary row and `results/CLUSTER_RESULTS.csv`).
- Regions with dMYS > 0: **17/17**.
- Verdict per frozen threshold (CONVERGENCE if rho<0 AND >=12/17 improving): **SUPPORTED**.
- Sex aggregation: mean of the two sex rows per region/cohort (n_sex_rows_mys = 4 per region in the CSV). Largest gain: CAR dMYS = 2.095; smallest gain: NCR dMYS = 0.505 (from X10_convergence.csv). Descriptive only; no causal or direction claim.

## X11 — Regional education inequality vs national tertiary expansion (CONTEXT ONLY)

- Regions with dGini <= -0.02: **17/17** (from `results/X11_gini.csv`).
- Spearman rho of dGini vs Gini_initial: **-0.621524** (n=17).
- National PHL ger_tertiary, CONTEXT ONLY (not regressed, no causal read): 1971 = **16.33575057983398**, 2024 = **47.41349962** (from `results/CLUSTER_RESULTS.csv` note column).
- Verdict per frozen threshold (EQUALIZING if >=10/17 regions fall >=0.02 AND rho<0): **SUPPORTED**.
- Largest dGini decline: ARMM -0.095; smallest: NCR -0.03 (from X11_gini.csv). Descriptive only.

## X12 — Gradient by initial attainment (whose schooling grew more)

- Quartile cut-offs on MYS_initial (from `results/X12_gradient.csv` summary row): Q1 [7.050000, 9.160000]; Q2 [9.160000, 9.390000]; Q3 [9.390000, 9.820000]; Q4 [9.820000, 12.010000].
- Median dMYS: Q1 = **1.340000**, Q4 = **1.220000**.
- Ratio Q1/Q4 = **1.098361** > 1.0 → verdict per frozen threshold: **SUPPORTED** (PRO-POOR GRADIENT).
- Q1 membership: ARMM, Central Visayas, MIMAROPA, Eastern Visayas, Zamboanga Peninsula. Q4 membership: Central Luzon, Ilocos Region, CALABARZON, NCR. Full 17-region table with quartile bounds is in `results/X12_gradient.csv`; each row carries the binding-limitation note. Descriptive only.

## Reproducibility

- Code: `code/run.py` (sha256 51b529e819de343358c809d0273e87512a8d21c82d7863ea3bc6129ee2e81f9e), deterministic, absolute paths, seed: none needed (no RNG).
- Re-run confirmed byte-identical results CSVs:
  - `results/CLUSTER_RESULTS.csv` 29ecf871ed0cc3519ba1e3dad466cbce6e5c74c6d7d48d1268c8c8a688350ad3
  - `results/X10_convergence.csv` c3c44ed2674074b62679a74e0e3fc824120060ac5346ec0c7dbdfc03fe0da2e0
  - `results/X11_gini.csv` d5e407260ac55e6d819bff2c491ffb12ccaff20963309029d266d9cd21b97feb
  - `results/X12_gradient.csv` 6909611c660ecdcbb5d4705d36f8ca6aa05764954e2582d8267fbd5aed6ac99e
- Full details in `RUN_MANIFEST.json`. All numbers quoted above exist verbatim in the results CSVs.
