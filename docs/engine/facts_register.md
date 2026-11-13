# Facts register: what each engine is tuned to and what it is tested on

TODO §2 P1, 5 November 2026. This register was built by reading the code, not the documentation. It covers every number an engine is scored against. Each fact has one role:

- **Calibration**: parameters were chosen to fit it. Matching it is not evidence.
- **Test**: it played no part in choosing parameters. Matching it is evidence. It must also have been unseen when the method was fixed, or the register says otherwise.
- **Diagnostic**: shown for context, with no pass/fail standard.
- **Input**: it drives the model from outside. Its accuracy matters, but the model is not scored on it.

Each mechanism is labelled as one of:

- **built in**: the result follows from how the mechanism is coded.
- **emergent**: the result comes out of interactions the code does not state.
- **tuned**: the result depends on a fitted value.

## China graduate labour market (`engine/firms/`)

| Fact | Source | Role | Where | Status, 5 Nov 2026 |
|---|---|---|---|---|
| Youth (16–24) unemployment, 2018–22, old NBS method (60 months) | NBS | **Calibration** | `calibrate_china.py` early window; `forecast_strict.py`; `wage_anchor.py`; `tilly_strict.py` | Fits within 1.35–1.5 pts |
| Youth unemployment, Jan 2025–Sep 2026, new method, verified (19 months) | NBS | **Test** for the Dec 2024 protocol (`forecast_2024`, `seasonal_2024`) | as named | spread11 0.77 vs naive 0.89 (duration+spread11 0.71). The test-period errors had been seen before the variants were chosen. |
| Youth unemployment, Oct 2026 onwards | NBS | **Blind test**: forecast frozen 5 Nov 2026 | `blind_forecast.py` | Pending |
| Youth unemployment, 2023 H1, old method (6 months) | NBS | **Test** | strict scripts | Fails in every specification: 5.9–6.8 pts against naive 2.5 (two-type, wage-anchored, Tilly) |
| Youth unemployment, Dec 2023–Sep 2026, new method, verified months | NBS | **Test** in strict scripts; **calibration** in the `full` window and `tilly_fit.py` | as named | Strict, 32 months: two-type 5.54, Tilly 5.49–5.84, naive 1.61. The `full`-window error of 1.27 and the Tilly whole-record error are fit statistics, **not** evidence: under the strict protocol the Tilly model scores 5.5–5.8. |
| Graduate postings, H1 2025, −22% y/y | Caixin, citing job boards | **Test** (never fitted) | `vg_check` | Fails: model +2% |
| MyCOS starting wage relative to urban average wage, classes 2019–21 | MyCOS; NBS | **Calibration** (wage speed; joint fit) | `wage_anchor.py` | Matched only with graduate demand shrinking ~7%/yr |
| Same, classes 2022–23 | MyCOS; NBS | **Test** | `wage_anchor.py` | Joint fit overshoots by 6–8 log points |
| Overall urban unemployment | NBS | **Input** (backs out the demand index) | `model.demand_index` | Leak through the youth series closed in strict scripts |
| Graduating-class scale, births, tertiary entrants, property investment | MoE; NBS | **Input** | `data_china.py` | Every value verified 6 Nov 2026 (lane A1, `docs/china_input_verification.md`): graduates 2008–2026, urban series 2018–2026, tertiary entrants 2006–24 and property 2018–25 all `v`; births are `d` — reconstructed from NBS yearbook tables (birth rate × mean of adjacent year-end populations), not published annual counts. One adjacent correction applied in the same batch: urban 2023-01 5.6 → 5.5. |
| Labour force ≈ 33m, graduates ≈ ⅓ of it (2018–19) | Zhang Dandan; China Academy | **Calibration** (sets `psi_g`, `psi_n` by hand) | `model.DEFAULTS` | Assumed, not fitted |
| CES elasticity 5 | Card & Lemieux range | **Calibration** (imported) | `sigma_A` | Profiled at 2.5–∞ in `--full` |
| Tilly fixed values: secure posts 10% of entry, 40% hoarded, 20% outsider wedge, 50% insiders | none | **Assumption** | `tilly_fit.FIXED` | No data behind them. TODO §5 lists identification work. |

**Mechanisms (China)**

| Mechanism | Label | Note |
|---|---|---|
| Old/new NBS definition gap (searching students) | built in | An observation rule, not a finding |
| Graduate surge → unemployment, through wage rigidity | built in + tuned | Its size depends on `lam_g`, which the 2018–22 data cannot identify (`forecast_strict.md`) |
| Downgrading / graduates crowding out non-graduates | emergent | Has a tier-2 property test |
| Waiting outside the labour force lowers the official rate | built in + tuned | `tilly_fit` "no waiting" counterfactual: +12.2 pts on the current results/tilly_fit.json (the +22.8 of an earlier run is not reproduced). Holding the Tilly parameters fixed, the measured rise is +5.1 with waiting and +12.2 without; the broad measure with waiting is +9.5. Fitted on pre-2023 data only, the waiting pool drains after 2022 (1.1m → 0.6m), so the mechanism does not produce persistence (`tilly_strict.md`). |
| Hoarding and emulation | built in | Contribute ≈ 0 to the rise in `tilly_fit` |

## Cambodia child labour (`web/camchild.js`)

| Fact | Source | Role | Status |
|---|---|---|---|
| Out-of-school rates 2024: primary 3.7%, lower secondary 17.6%, upper secondary 48.9% | UNESCO UIS | **Calibration**: six school-value constants (`vPrim`, `vLow`, `vUp` × two regions) tuned to three national targets | Within 2.5 pts (a `test_camchild.cjs` check of the calibration itself, not evidence) |
| Phnom Penh/countryside split of those rates | none | **Assumption** | Three of the six constants are free. The rural lower-secondary value (5.66 vs 2.16 in Phnom Penh) is the "unexplained boost". |
| Child labour ≈ 10.7% | Cambodia Child Labour Survey 2012 | **Test** (not fitted) | Fails: model ≈ 14%. The survey is 12 years older than the calibration year, so the test is weak in both directions. |
| Countryside child labour > Phnom Penh | stylised | **Test**, weak | Passes. A sign check only. |
| Policy directions (cash, Thai route, ban, floor, protection) | none | **Built in** (code checks) | The ban's effect on rural migration is the one emergent result, and the test labels it so |
| Robustness of policy effects to the calibration ridge | `camchild_ridge.md` | **Diagnostic** | Cash, ban, floor and protection are robust in sign. The Thai closure and the garment boom have no established sign. Child labour stays at about 14% in every variant. |
| UIS 2024 vs Census 2019 out-of-school, lower secondary | UIS; NIS | **Unresolved observation equation** | 17.6% vs about 8.4%, a factor-of-two disagreement |
| Nordtveit protection magnitudes | none | **Placeholder** | To be set by Bjørn |

## Atlas household-and-school engine (`engine/eduengine/`, `history_match.py`)

This is the best-governed engine. Its protocol (`tune_protocol.json`) was recorded before the search. Targets run to 2015 (training), and post-2015 rows are evaluation only. Seeds are split between training and evaluation. `test_validation.py` enforces that test rows and unverified or stylised rows cannot affect selection.

| Fact | Role |
|---|---|
| UIS completion, primary/lower/upper, ≤2015 (Cambodia, Philippines, China) | **Calibration** |
| UIS completion >2015 | **Test**, with a caveat. The protocol says these were inspected before the search, so it is a temporal holdout, not a blind one. |
| Tutoring shares, private shares | **Diagnostic** where `unverified`/`stylised`; otherwise test |
| China youth unemployment 12% (2019) / 19% (2023) | **Diagnostic** (stylised) |

## Planning Lab and public-data regressions

The Planning Lab tools implement published formulas. Their 30 tests check identities and limiting cases (built in). Nothing is calibrated, so there are no facts to separate. The cross-country regressions in `analysis/public_data/` are **diagnostic**.

## Rules from here

1. A fact moves from test to calibration only with a dated entry in this file. It never moves the other way.
2. A headline number states whether it is a fit statistic or a test. The run report's "whole-record error 1.27" is a fit statistic.
3. Before a new test is scored, its method and benchmark are written down: Dec 2022 cutoff, prespecified input rules, and the naive benchmark. The strict China scripts follow this rule. The Cambodia world needs the same treatment, with a 2019 baseline scored against later data.
