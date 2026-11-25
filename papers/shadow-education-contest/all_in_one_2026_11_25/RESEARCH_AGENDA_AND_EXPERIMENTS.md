# Atlas of Education — Research Agenda & Next Experiments (2026-11-25)

## Four-Paper Portfolio Architecture

1. **Paper #1 (Flagship Methods-Meets-Substance): "Zero Universal Laws, 32 Regimes"**
   - *Target venues:* Nature Human Behaviour, PNAS, World Development, Sociological Methods & Research.
   - *Core evidence:* 172.6M panel regressions (`corr-battery` 57.3M + `E1` 115.3M, BY `0/0/0/32`); `Q3` 87% minority-effect leakage; `E11` construct flip (`0.541` vs `1.555`); `observed-core` 0% win rate vs persistence across 94,506 WDI rows; `F10` construct divergence (`n=14,578`, median `|Δ|=0.284`); corrected DHS `C_vs_B = -0.1962` and `higher × cohort = +0.1804 (p=0.030)`. Positive contrast: `E8` (`+12.44 / +25.26 pp`, Fisher RI `p=0.0001`) + Exp 5 (`-78.6% to -80.5%` RMSE vs persistence).

2. **Paper #2 (Empirical Anchor): "Massification Before Industrialization"**
   - *Target venues:* Economics of Education Review, Comparative Education Review, Journal of Development Economics.
   - *Core evidence:* `E6` (1900–2012 GGDC/WDI: demand-first only 10–24%; PHL schooling 1945 vs industry 1964 / urban 1989) + `E8` (8 SSA fee abolitions, `+22–29 pp`, 20k Fisher RI `p=0.0001`, no gender gap `D=-3.94 [-8.72, +0.29]`) + Exp 5 out-of-sample mechanistic shock validation (`4.68–5.13 pp` RMSE vs `23.93 pp` persistence).

3. **Paper A & Paper B (Two-Paper Shadow Education Sequence for Prof. Mark Bray & Prof. Bjørn Nordtveit)**
   - **Paper A (General Mechanism):** *When Fee Abolition Meets Rationed Gates: Shadow Education, Strategic Contests, and Micro-Identifiability in Massifying Education Systems* — establishes the general `bar` vs `quota` vs Tullock `contest` mechanism (`H2 = +0.1086`, `p=1.9e-11`; inverted-U peak `+0.2573` at `vac0=0.25`), exit migration (`q1 never` −72 to −74 pp, `gate_fail` +10.39 pp under tight quota), the exact 2-micro-moment Jacobian rank theorem (`5/7 -> 6/7 -> 7/7`, `cond = 43.81`), and the honest WDI `$t^*$` null.
   - **Paper B (IRL Comparative Study — Hong Kong & South Korea):** *Why Tutoring Taxes Backfire and Expanding Elite Seats Fuels the Arms Race* — adapts vertical-tier `contest` (`fail='track'`) to HKDSE (`S=0.23`) and South Korea CSAT (`S12=0.12`), proves mathematically why +50% taxes backfire on BOTH spend (`+4.8% / +7.4%`) and equity, why expanding hyper-tight seats fuels the arms race via the `P(1-P)` hump (`+5.9% / +22.3%` KR, reproducing the 2024 +2,000 medical-seat shock), and why only Wage Compression (`ΔV ↓`) paired with Caps or Seats reaches the Win-Win Zone.

4. **Meta-Science Short Paper:** *Silent Failures in an AI-Assisted Social-Science Pipeline* (`research/meta-science-silent-failures-2026-11-25`) — commit-by-commit forensic record of 10 branches passing `returncode == 0` while hiding verdict-flipping estimator bugs caught by pre-registered adversarial audit.

---

## Queued Next Experiments (All Local M1 CPU — Zero Paid Server Needed)

### Exp 7 (~15s on M1): Paper B Combined Win-Win Policy Arms (`CF4a` & `CF4b`)
- Add `CF4a` (Wage Compression `ΔV −50%` + Effort Cap `−50%`) and `CF4b` (Wage Compression `ΔV −50%` + Large Seat Expansion `HK S=0.50 / KR S12=0.40`) across 30 matched seeds for HK and Korea.
- Verify quantitatively that combined levers enter the Win-Win Zone (Spend Index `< 80` AND Elite Q5 Share below baseline).

### Exp 2 (Local CPU, after free LSMS download): World Bank LSMS-ISA Household Tutoring Check
- Countries: Malawi, Ethiopia, Uganda, Tanzania (`https://microdata.worldbank.org/index.php/catalog/lsms`).
- Compare household tutoring/exam-prep expenditure in national exam-transition grades vs. grade − 1 across consumption quintiles (`Q5` vs. `Q1`) and within-grade school-quality strata (supplying the exact 2 micro-moments required by Exp 4's Jacobian rank theorem).

### Exp 6 (Overnight M1): `E1` / `Q3` Finite-Sample Wild-Cluster Permutation Null (`B = 2,000`)
- Run Rademacher wild-cluster bootstrap + country-block permutations over `E1` / `Q3` panel matrices to armor Paper #1's `0/0/0/32` and `87%` leakage findings against asymptotic-SE referee critiques.

### Exp 8 (~15s on M1): South Korea Elementary Enrichment / Childcare Floor
- Add a fixed non-exam elementary floor in Grades 1–6 to test whether the combined model matches Korea's inverted age curve (~86% elementary > ~75% middle > ~67% high school) while keeping Grade-12 CSAT policy rankings invariant.
