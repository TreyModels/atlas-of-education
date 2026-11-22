# Protocol v6_phl: Pre-Registered Philippine Demand-and-Capacity Experiment

**Date written:** 2026-11-22 (before any `v6_phl` parameter is fitted).  
**Status of test:** Retrospective and inspected, not blind (post-1995 Philippine observations were inspected in v1–v5).  
**Preserved baseline:** `PROTOCOL_v5.md` and `outputs/PHL/v5/` remain untouched and authoritative for v5. This experiment writes exclusively to `outputs/PHL/v6_phl/`.  
**Scope:** Philippines only. Cambodia, Hong Kong, tutoring, China, and Atlas Worlds release are strictly out of scope.

## 1. Research question

Does a small, sign-constrained nested sequence of Philippine demand specifications—with (a) split basic vs. tertiary private-sector income slopes (`nu_basic`, `nu_ter`) to address v5's 19–38 pp private-share errors, and (b) a bounded saturating positional pull—beat naive persistence (`6.600142`), linear trend (`11.793765`), v5 `R0` (`14.229522`), and v5 `R2` (`7.458470`) on the exact same held-out post-1995 GER observations without relying on negative human-capital signs or bound-hugging artefacts?

## 2. Training and held-out observations (identical to v5 for apples-to-apples comparison)

All rows are built by `masseng.calibrate5.build_rows(Country('PHL'))` and verified via `masseng.readiness5.check_country('PHL')`:
- **Training (`n = 121`):** 1971–1995 WDI enrolment series (`ger_primary`, `ger_secondary`, `ger_tertiary`, `ner_primary`, `priv_primary`), 1985 tertiary private share (`79.0%`), declared APIS 2019 richest/poorest participation ratios (`gradlr_*`, carried over from v3/v5), and verified FIES 2003 & 2006 household education spending shares (national, bottom 30%, top 70%).
- **Held-out test (`n = 164`):** post-1995 WDI enrolment (`ger_primary`, `ger_secondary`, `ger_tertiary`, `ner_primary`, `ner_secondary`), post-1995 private shares (`priv_primary`, `priv_secondary`, `priv_lower_secondary`, `priv_upper_secondary`, `priv_tertiary`), FIES 2012 national spending share (`4.1%`), PIDS NTA household shares (1991–2010), CHED tertiary headcount index (2016–2020, 2016 = 1; **original PDF verification remains open**), and DepEd Grade 10→11 transition (`93.3%`, reference year 2018).
- **Excluded:** Unverified FIES 2023 row remains excluded.

## 3. Fixed inputs and declared sources

- **Demography & macro:** WDI `SP.POP.TOTL`, `SP.DYN.CBRT.IN`, `SH.DYN.MORT`, `NY.GDP.PCAP.KD`, `SI.POV.GINI`, `SE.XPD.TOTL.GD.ZS`, `SE.PRM.AGES`, `SE.PRM.DURS`, `SE.SEC.DURS`.
- **Drivers (`countries/PHL/drivers_v5.json`):** `premium_secondary` and `premium_tertiary` (log points; combines methods and interpolates 1995–2013—declared comparability limitation).
- **Costs & policies (`countries/PHL/config.json` `v5` block):** Declared direct cost schedule (`direct_costs_share_of_gdppc`), forgone earnings (`forgone_earnings_share_of_gdppc`), dated policy events (1989 RA 6655, 1990 ESC/GASTPE, 2017 SHS vouchers, 2018 RA 10931), 2009 4Ps transfers, `household_consumption_share_of_gdp = 0.72`, `max_defer_age = 25`.
- **Fixed bookkeeping parameters (not fitted, not tuned):** `h_def = 0.20`, `late = 0.15`, `rep_prim = 0.04`, `rep_sec = 0.02`, and half-saturation constant `s0_sat = 0.25` (declared our modelling adaptation, not attributed to any external source).

## 4. Candidate specifications, substantive dials, and bounds

Every specification separates **3–5 substantive behavioural dials** from **declared level/sector intercepts and scaling (`a_prim`, `a_sec`, `a_sec_entry`, `a_ter`, `a_ter_entry`, `mu_basic`, `mu_ter`, `nu_basic`, `nu_ter`, `c_scale`)**.

Utility for level $L$, decile $d$, year $y$:
$$U_{L,d,y} = \alpha_L + b_h p_{L,y} + b_p g(S_{L,y-1}) + \eta \ln(\text{GDPpc}_y / \text{GDPpc}_{1990}) + \eta_x \ln(I_{d,y} / \bar{I}_y) - \kappa \exp(-\lambda g(S_{L,y-1})) \ln(1 + \text{burden}_{L,s,d,y}),$$
with pre-registered bounded saturating positional pull (our modelling adaptation):
$$g(S_{L,y-1}) = \frac{S_{L,y-1}}{S_{L,y-1} + 0.25} \in [0, 1).$$

Private-sector preference splits basic (`primary`, `secondary`, `upper_secondary`) from `tertiary`:
$$v^{\text{priv}}_{L,d,y} = v^{\text{base}}_{L,d,y} + \begin{cases} \mu_{\text{basic}} + \nu_{\text{basic}}(\ln \text{GDPpc}_y/\text{GDPpc}_{1990} + \ln(I_{d,y}/\bar{I}_y)), & L \neq \text{tertiary} \\ \mu_{\text{ter}} + \nu_{\text{ter}}(\ln \text{GDPpc}_y/\text{GDPpc}_{1990} + \ln(I_{d,y}/\bar{I}_y)), & L = \text{tertiary}. \end{cases}$$

### Nested model sequence (6 runs: constrained and unconstrained pairs where signs are tested)

| Spec | Mechanism | Substantive behavioural dials (count) | Sign bounds on substantive dials |
|---|---|---|---|
| `P0` | Income + cost benchmark | `eta`, `eta_x`, `kappa` (3) | `eta in [0, 6]`, `eta_x in [0, 4]`, `kappa in [0, 40]` |
| `P1_con` | Human-capital returns + cost (constrained) | `b_h`, `eta_x`, `kappa` (3) | `b_h in [0, 12]`, `eta_x in [0, 4]`, `kappa in [0, 40]` |
| `P1_unc` | Human-capital returns + cost (unconstrained) | `b_h`, `eta_x`, `kappa` (3) | `b_h in [-6, 12]`, `eta_x in [0, 4]`, `kappa in [0, 40]` |
| `P2_con` | Bounded positional + returns + cost (constrained) | `b_h`, `b_p`, `eta_x`, `kappa` (4) | `b_h in [0, 12]`, `b_p in [0, 12]`, `eta_x in [0, 4]`, `kappa in [0, 40]` |
| `P2_unc` | Bounded positional + returns + cost (unconstrained) | `b_h`, `b_p`, `eta_x`, `kappa` (4) | `b_h in [-6, 12]`, `b_p in [-6, 12]`, `eta_x in [0, 4]`, `kappa in [0, 40]` |
| `P3_con` | Bounded positional + saturation-dependent cost (constrained) | `b_h`, `b_p`, `eta_x`, `kappa`, `lam` (5) | `b_h in [0, 12]`, `b_p in [0, 12]`, `eta_x in [0, 4]`, `kappa in [0, 40]`, `lam in [0, 12]` |

RRA (Breen–Goldthorpe) is **not** included because empirical completion probabilities and class status-payoff inputs are absent in the Philippine dataset and will not be invented.

Level/sector intercept bounds (shared across all specs): `a_prim, a_sec, a_ter in [-4, 16]`, `a_sec_entry in [-10, 14]`, `a_ter_entry in [-12, 12]`, `mu_basic in [-10, 6]`, `mu_ter in [-8, 8]`, `nu_basic, nu_ter in [-6, 8]`, `c_scale in [0.05, 8]`.

## 5. Supply-capacity rule (no manufactured capacity series)

Documented 1950–2024 historical Philippine physical seat capacities are not available in this repository. Therefore:
- All empirical fits (`P0`–`P3_con`) run without manufactured seat caps.
- One separate **illustrative** declared-capacity diagnostic is run on the winning specification using the conserved two-sector allocator, explicitly reporting **qualified people (Q)**, **latent applicants (L)**, **effective applicants (E)**, **admitted students (R)**, and **accessible unfilled places**. This diagnostic is labelled **illustrative, not calibrated**.

## 6. Benchmarks, separating observations, selection & stopping rules

- **Benchmarks:** Naive persistence (`6.600142`), linear trend (`11.793765`), preserved v5 `R0` (`14.229522`), preserved v5 `R2` (`7.458470`), and `P0`.
- **Primary selection rule:** Lowest held-out mean RMSE across all registered post-1995 observations of the three GER series (`ger_primary`, `ger_secondary`, `ger_tertiary`).
- **Private-share repair diagnostic:** Compare held-out RMSE on `priv_primary`, `priv_secondary`, `priv_tertiary`, `priv_lower_secondary`, `priv_upper_secondary` against v5 `R2`.
- **Separating observations:**
  1. `tertiary_2013_2024`: paired tertiary GER in 2013 (`31.870%`) and 2024 (`47.413%`) as college premium falls (`0.88` to `0.59`).
  2. `recession_secondary`: observed 1998 secondary GER.
  3. `grade10_to_grade11_2018`: DepEd Grade 10→11 transition (`93.3%`, reference year 2018).
  4. `ched_k12_recovery`: CHED tertiary headcount index 2016–2020 (provisional; original PDF unverified).
  - A mechanism is called supported on a separating observation **only if** its specification beats every registered rival on that observation **and** satisfies the overall selection rule.
- **Stopping rule:** If no structural model beats naive persistence (`6.600142`), report that result prominently, keep status **`not calibrated`**, do not add countries, tutoring, or extra feedback loops to rescue it, and document the measurements needed for a stronger test.

## 7. Recovery and boundary-censoring rules

- Run **20 synthetic replicates** on the selected winning specification using the exact v5 Gaussian noise design (`1.0 pp` rates/shares, `0.1 pp` spending shares).
- **Numerical pass rule:** $\ge 80\%$ of replicates within $\pm 25\%$ of a nonzero true parameter.
- **Boundary-censoring rule:** Any parameter resting at a bound in the fitted truth OR hitting a bound in $> 20\%$ of recovery replicates (i.e. $\ge 5/20$) is labelled **`boundary-censored / not cleanly identified`**, even if it satisfies the numerical proximity criterion.
- Synthetic recovery is reported strictly as a software/design diagnostic, never as proof of historical identification.

## Amendments

### A1 — 2026-11-22 13:35 CST (written after P0, P1_con, P1_unc, P2_con, P2_unc training fits were inspected; before any held-out score was computed)

1. **Nesting defect.** P1 and P2 fix `eta = 0`, so P1 is not nested in P0: moving P0→P1 both adds returns (`b_h`) and removes aggregate income growth (`eta`). Two added runs make the clean comparison: `P0h_con` (dials `eta, eta_x, kappa, b_h`; `b_h ≥ 0`) and `P0h_unc` (`b_h ∈ [-6, 12]`). All other bounds as §4. Implemented in `scripts/run_v6_phl_amendA1.py` by registering specs at run time; `engine_v6_phl.py` is not edited.
2. **Status of the added runs.** They are post-inspection additions. They are scored and reported alongside the registered runs, but the **registered winner is chosen only among the six registered specs**. If an A1 run would have won, that is reported separately as an amendment result, not as the pre-registered result.
3. **Optimiser restarts.** Every fit above uses one start. Several dials sit on bounds, so the selected winner gets up to 4 random-start refits (`--multistart`). Report whether any restart reaches lower training cost. Restarts do not change the selection rule.
4. **Benchmark rule recorded.** Persistence carries the last training-window value (≤1995) forward for every held-out year (`calibrate5.benchmarks`). Trend is a linear fit over the training window. Neither uses held-out data.
5. **Separating-test reading.** §6 says "every registered rival". This includes persistence and trend wherever they produce a prediction for the observation, not only the structural specs.
6. **Code lineage.** Package = `MASSENG_v7_lab` (Claude/Kimi masseng lineage: v1–v5 → R0–R5 → v6_phl). It is not the separate ChatGPT `MASSENG_v5_full.zip` in `MASSENG_v6_surplus_motor_CONTEXT_HANDOFF.zip`, which has different code and results.
7. **Run location.** Gemini's local run did not complete P3_con. P3_con, the A1 runs, scoring and recovery were run by Claude in a Linux workspace (Python 3, numpy 2.5.3, scipy 1.18.1) on a snapshot of the same files. Version differences from `requirements-v5.txt` (numpy 2.4.4) are recorded in the hashes file.

