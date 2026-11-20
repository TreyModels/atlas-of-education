# PRE-REGISTRATION — A3 demand-pull battery (PHL anchor): remittances (observed), nurse visa (SIMULATED), BPO (DATA BLOCKED)

**Written before running.** Anchor = PHL (D38); A3 owner pair deepseek-exp2 + data (D42/ANCHOR_SLATE). No direction
claim (R13/EQUIVALENT cap); no closed claims re-fit; observed vs simulated labelled; no imputation as observation.
No git writes (executor commits).

## A3a — Remittances → schooling (OBSERVED; national, since PSA regional data blocked)
Data: `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` PHL 1995–2024: personal remittances %GDP (observed),
GDP pc; `UNIVERSALIZATION_SERIES.csv` PHL GER secondary/tertiary (1971–2024 observed) and upper-sec completion
(1999–2024 observed). Estimator: log-log OLS `log(GER_t) = α + β·log(remit%GDP_t) + γ·log(GDPpc_t) + δ·trend + ε`
with Newey–West lag 2; also 3-year-lag remittances specification. **Predeclared sign & magnitude:** β > 0 for
tertiary GER, with **β ∈ [0.10, 1.50]**; secondary GER β > 0 with smaller expected magnitude (no band). **Placebo
tests:** (i) primary GER (near-universal, should show no comparable positive response or |β| ≤ tertiary β);
(ii) lead-placebo — future remittances (t+3) must not predict current GER (|t| < 1.96); (iii) trend-only rival.
**Decision rule:** PASS if tertiary β ∈ band AND p<0.10 AND lead-placebo null; EQUIVALENT if β ∈ band but a placebo
fails; FAIL if β ≤ 0 or outside band; UNABLE if series coverage insufficient. This is a demand-pull *association*;
no direction claim.

## A3b — Nurse visa expansion 2005–06 (SIMULATED ONLY; E3 replication DATA BLOCKED)
The published replication needs PRC licensure and CHED nursing-enrolment series, which are **DATA BLOCKED** on disk
(PSA/CHED unavailable). Per D42/E3: **simulated only, labelled SIMULATED, no claim.** Design expectation (declared):
a field-specific nursing-enrolment/licensure response at 2005–06 in **[+10%, +30%]**, with placebo fields
(|effect| ≤ 5%) and clean pre-trends. This is a power/design statement for when the series are secured; it is **not
an estimate** and may not be cited as evidence.

## A3c — BPO/IT regional growth (DATA BLOCKED)
No regional/industry BPO series on disk and PSA is blocked; the regional exposure gradient (high- vs low-BPO regions)
cannot be run. **DATA BLOCKED**, declared; a national services-share sensitivity is not a substitute for the regional
design and is not claimed.

## Failure and stop-rule links
Failed fits are logged; UNABLE/DATA BLOCKED cells reported. R13 (no direction claim), R3 (equivalence), R4 (events
exogenous, never fitted), R5 (no re-parameterisation to match). Deliverables: `NEW:` with path/hashes + this
predeclaration; cells run: A3a (observed) and A3b (simulated design only); A3c DATA BLOCKED.
