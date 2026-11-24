# Pre-Registration: Unified Fee-Free / Child-Labor / Shadow-Education GPU Suite

**Commit this file BEFORE running `run_all.sh` or inspecting any output.**

## 1. Hypotheses & Pre-Declarations
- **H1 (Macro Wall):** Standard 10-year FE regressions on synthetic country aggregates (`d_GER`, `d_cl_total`) will not separate `DGP_POVERTY`, `DGP_SCHOOL_PUSH`, and `DGP_CROWDING_TUTOR` (cross-DGP macro slope overlap > 75%).
- **H2 (Nordtveit Backfire):** Under `DGP_SCHOOL_PUSH` and `DGP_MIXED`, `Arm 3 (binary_ban)` increases `hidden_work` relative to `Arm 1 (tuition_only)`, whereas `Arm 2 (protective_capacity)` reduces both `work_only` and `hidden_work` while compressing `tutoring`.
- **H3 (Bray Crowding Surge):** Under `DGP_CROWDING_TUTOR` and `DGP_MIXED`, `Arm 1 (tuition_only)` raises `ger` while diluting `q_pub` and increasing `tutoring` share among upper-income households.
- **H4 (Micro Tie-Breaker):** At least one micro distribution (`enrolled_work_hrs_p90`, `hidden_to_sw_ratio`, `tutor_income_elast`) separates the 3 single-mechanism DGPs with >80% out-of-seed accuracy, while dropping to ~33% (chance) under `strength = 0` (`Q1` zero-signal control).

## 2. Identifiability & Reporting Rules (Binding)
1. **Batch-size pinning:** Fix `N = 250,000` (simulation) and `N_abc = 50,000` per country (ABC) because Philox keys depend on agent index; report exact `N` in `REPORT.md`.
2. **Rejection ABC only:** Equal-weight top-10% acceptance (`500 / 5,000` draws). No importance-weighted particle filters.
3. **0.80 Prior-Width Gate:** Any parameter with `(q95 - q05) / (prior_max - prior_min) > 0.80` is declared **UNIDENTIFIED**.
4. **Descriptive language:** Empirical `EXP-4` (`E8` + ILO/UCW) uses `"consistent with"`, never causal claims, and flags sparse survey-year coverage.
