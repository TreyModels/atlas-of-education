# PRE-REGISTRATION — A5 rival-model comparison on the same PHL record (no direction claim)

**Written before running.** Anchor = PHL (D38/D39); A5 owners deepseek-exp2 + lit (D42/ANCHOR_SLATE). Rivals fitted
**identically** on the same PHL pre-2013 record and the same observed covariates, then predict 2013–2024 and the
post-2013 event breaks out of sample. **No direction claim (R13/EQUIVALENT);** no closed claims; observed only; no
imputation; no git writes (executor commits). Anchor-vs-rivals comparison is **deferred** until the anchor model
(A1, exp1) lands; this initial cell compares the rivals to each other and reports equivalence, as A5 permits.

## Data and roles
Outcomes: PHL GER_secondary and GER_tertiary (observed 1971–2024; fit ≤2012, holdout ≥2013) and upper-secondary
completion (observed 1999–2024; fit 1999–2012, holdout 2013–2024; thin, declared). Covariates from
`10_massification/data/JOBS_AND_MARKETS_PANEL.csv` (GDP pc, education spending %GDP, primary/secondary teachers,
PTR, services/agriculture shares, remittances) and `UNIVERSALIZATION_SERIES.csv`. Roles: **fit** pre-2013; **holdout**
2013–2024; no series both fit and holdout. No fitted event effects.

## Five reduced-form rivals (same outcome, same fit window; each with its own declared regressors)
1. **HC (Becker/Mincer):** outcome ~ log GDP pc + lagged log GDP pc (returns/income channel).
2. **World culture (Meyer/Schofer):** outcome ~ linear trend + intercept (diffusion/legitimation).
3. **Labour queue (Thurow/Collins):** outcome ~ lagged credential supply proxies (secondary GER, tertiary GER) + trend.
4. **State-building (Paglayan):** outcome ~ education spending %GDP + teacher supply/PTR (shorter window: fit
   1995–2012 where spending observed; UNABLE for 1971–1994).
5. **Sectoral demand (Lewis/Kuznets):** outcome ~ services share + agriculture share + remittances.
Estimator: OLS with HAC (NW lag 2); predictions use **actual observed covariates** in the holdout (declared; not a
forecast exercise). No event dummies in any rival (events are the discriminating dimension that the anchor model will
add later).

## Estimands and predeclared thresholds
- **OOS trajectory:** holdout MAE/RMSE per rival per outcome.
- **Event-break reproduction:** observed change across each predeclared event window (K-12 2013; free SHS 2016;
free tertiary 2018) vs each rival's predicted change over the same window; sign and magnitude error reported.
- **Pre-trends/placebo:** fit-window residual pre-trend and a placebo event window (2005–08, no policy) must not be
materially worse than the real event window; report, do not fit to it.
**Decision rule:** A5 initial reports (i) the rival ranking on OOS MAE and event-break error; (ii) **EQUIVALENT (R3)**
if the best and second-best rivals differ by ≤0.5 pp MAE and ≤0.5 pp event-break error (i.e., the record does not
separate them); (iii) UNABLE per rival where regressors are missing pre-2013. **No anchor claim** is made; the
anchor comparison is deferred to A1.

## Failure/stop-rule links
Failed fits logged; no target as parameter; R3 (equivalence), R13 (no direction), R4/R5 (events exogenous; no
refitting to match). Deliverables: `NEW:` with path/hashes and this predeclaration; all cells including failures.
