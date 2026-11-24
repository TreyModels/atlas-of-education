# Formalized Research Methodology: Breaking the Macro Regression Wall

## The Problem: Why 172 Million Regressions Still Say "Everything Is Development"
Across `E1` (`115.3M` regressions), `corr-battery` (`57.3M`), and `Q2` (`52` matched pairs), aggregate country panels hit an **observational-equivalence wall**:
1. Only `5/272` within-country links travel across all country groupings (`E1`), while `"robust everywhere"` still leaks `87%` of minority-effect worlds (`Q3`).
2. `MSE` (`97%`) and `BIC` (`100%`) fail zero-signal mechanism controls (`Q1`), rewarding model flexibility or parsimony rather than causal truth.
3. `effective_fertility` vs. `TFR` flip lead/lag behavior (`0.541` vs. `1.555`) on identical rows (`E11`).

Stopping at *"everything is development"* is scientifically incomplete. Instead, we use **forward micro-simulation on GPU** to map *where* distinct micro mechanisms collapse into identical macro correlations—and *which* micro-level observables break the tie.

## The Four-Step Pipeline

### Step 1 — Map the Macro Wall (Done)
Use the 50-typology multiverse (`E1`), matched-pair sensitivity (`Q2`), and construct audits (`E11`) to establish which aggregate correlations are non-separable.

### Step 2 — Formalize Competing Micro Mechanisms From Literature
Translate rival theories into explicit household/teacher behavioral rules:
- **Basu–Van (1998) & Baland–Robinson (2000):** Subsistence threshold $Y_{\text{sub}}$ and credit-constraint corner ($L_c = 1$ when $Y_h < Y_{\text{sub}}$ or borrowing is blocked).
- **Nordtveit (2010a, 2010b):** 4-state continuum (`school_only`, `study_and_work`, `visible_work_only`, `hidden_work`), hidden direct school costs $H_{\text{hidden}}$ (uniforms, exam birth certs), and school hostility/stigma $\psi$. Binary bans on `study_and_work` without closing $Y_{\text{sub}} - Y_h$ push survival-constrained youth into `hidden_work`.
- **Bray (2016, 2018), Jayachandran (2014), & Dang–Rogers (2008):** Endogenous shadow tutoring $T_i$ driven by public classroom crowding $Q_{\text{pub}}(\text{GER})$ and/or teacher effort diversion $\beta_{\text{div}}$.
- **Pritchett (2013):** Flat cohort learning profile $\alpha(g)$ under centralized enrollment surges, which simultaneously drives dropout at the bottom (low return vs. $H_{\text{hidden}} + \psi$) and tutoring flight at the top.

### Step 3 — GPU Forward Simulation & Macro-Wall Verification (`EXP-1` + `EXP-2`)
Simulate `N = 250,000` households per country-arm across `T = 25` years (`F_pub -> 0` shock at `t = 10`) under four true micro DGPs (`DGP_POVERTY`, `DGP_SCHOOL_PUSH`, `DGP_CROWDING_TUTOR`, `DGP_MIXED`).
1. **Macro-wall check:** Run standard 10-year country+decade FE regressions on the synthetic macro panel to test whether distinct micro DGPs produce indistinguishable aggregate slopes.
2. **Micro tie-breaker:** Score which *micro-level* statistics (e.g., 90th-percentile work hours among enrolled children, `hidden_work / study_and_work` ratio, tutoring income elasticity, learning-per-grade slope) cleanly separate the DGPs—**passing `Q1`'s zero-signal control** (`strength = 0` must yield chance accuracy).

### Step 4 — Rejection-ABC Calibration & Identifiability Gate on Public Data (`EXP-3` + `EXP-4`)
Fit the GPU kernel via **equal-weight rejection ABC** (`5,000` prior draws, top `10%` accepted) against public World Bank WDI / ILO-UCW targets (`cl_total`, `cl_work_only`, `cl_study_work`, `cl_agri`, `prm_enr`, `prm_cmp`, `sec_enr`) for the 8 verified `E8` SSA countries + SEA benchmarks (`KHM, PHL, VNM, BEN, NAM, SWZ`).
- **Hard Identifiability Gate:** Any parameter whose 90% posterior width exceeds `0.80` of its prior width is reported as **UNIDENTIFIED**, never interpreted.
