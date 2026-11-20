# STATE_CAPACITY_NOTES — a three-dimension state-capacity measure for the anchor and portability cases

`data-hunter`, 2026-11-20. `STATE_CAPACITY.csv`: **1,799 rows**, one row per dimension × indicator × country × year, with source, definition and `status` ∈ {observed, policy_fact, check, unable}. **Observed values only; no imputation.** Blocked routes are recorded as `unable` rows or in the sections below.

## Dimension 1 — Fiscal capacity (611 rows)
| Indicator | Source | Coverage | Status |
|---|---|---|---|
| Education spending % GDP | WDI `SE.XPD.TOTL.GD.ZS` | six countries, 1995–2024 | observed |
| Education spending % total government expenditure | WDI `SE.XPD.TOTL.GB.ZS` | six countries, 1995–2024 | observed |
| Education spending % GDP / % budget (UIS cross-check) | UIS `XGDP.FSGOV`, `XGOVEXP.IMF` | six countries, 1970s–2025 (sparse) | observed — **different vintage from WDI; do not average** |
| Government spending per student, constant PPP$ | UIS `XUNIT.PPPCONST.1/.2T3.FSGOV.FFNTR` | PHL 2008 (588/591 PPP$), CHN 2024 (4,035/5,312), HKG 2025 (13,905/16,080), KOR 2023 (15,249/20,642), KHM 2014 (212), JPN 1998 (7,841) | observed — very sparse, latest year differs by country |
| General government revenue, tax revenue, fiscal balance, revenue volatility | WDI `GC.*` | — | **UNABLE / DATA BLOCKED** — `api.worldbank.org` returned HTTP 000 on 3 attempts during this window; retry next batch. Volatility would be derived, not observed. |

Latest fiscal values (WDI): education spending %GDP — PHL 3.93 (2024), KHM 2.0 (UIS), HKG 3.6, CHN 4.0, KOR 4.6, JPN 3.0; %budget — PHL 16.5, KHM ~10.7 (UIS), HKG 15.1, CHN 12.2, KOR ~15, JPN ~10 (last obs 1998). The **per-student PPP$ spread (KHM ~212 at 2014 vs KOR 15,249 at 2023, HKG 13,905) is the single most informative fiscal-capacity number for the model**: it is two orders of magnitude.

## Dimension 2 — Delivery capacity (509 rows)
| Indicator | Coverage | Status |
|---|---|---|
| Teacher counts, primary and secondary (headcount) | six countries, 1990s–2024 | observed (WDI) |
| Pupil-teacher ratios, primary and secondary | six countries, 1995–2024 | observed (WDI; ILO/UNESCO modelled in places) |
| PHL high-school PTR 37 (2000–11) → 27 (2014) → 24 (2017) | PHL | observed (PIDS 2025 ch.4) |
| PHL classroom-student ratios: elementary 1:39 (2010) → 1:32 (2021); JHS 1:54 → 1:44 | PHL | observed (PIDS DPS 2025-10, citing NEDA 2017/2023) |
| PHL classroom backlog 110,954 rooms (SY2019-20); +10,000 rooms/year needed; 9,225 schools below standards; 28,508 structurally unsafe classrooms | PHL | observed (PIDS 2025 ch.5, DepEd figures) |
| PHL congestion 2021: 90% of NCR Northern Manila public elementary students in schools ≥1:50; 76.8% S Manila; 60.1% E Manila; 66.0% Rizal; 57.7% Cavite | PHL subnational | observed (PIDS DPS 2025-10) |
| PHL teacher hiring 2012–16: ~200,000 kindergarten/elementary + ~40,000 SHS | PHL | `check` (approximate, PIDS text) |
| Number of schools by year; classroom construction completed by year; SHS capacity 2016–18; HEI openings | — | **DATA BLOCKED/UNABLE**: deped.gov.ph 403, DPWH 403, DepEd datasets page 403, Wayback 429, CHED 403; BEPER 2019 not retrievable (routes in WEB_BASELINE_NOTES.md) |

## Dimension 3 — Enforcement capacity (679 rows)
| Indicator | Source | Status |
|---|---|---|
| Years of compulsory primary+secondary education **guaranteed in law** (annual) | UIS `YEARS.FC.COMP.1T3` | observed (de jure). Latest: PHL **12** (changed from 6 — the K-12 legal step is in the series), CHN 9, HKG 9, KOR 9, JPN 9, **KHM 0** (no compulsory years reported) |
| Years of free primary+secondary education **guaranteed in law** | UIS `YEARS.FC.FREE.1T3` | observed: PHL 12, HKG 12, KOR 12, CHN 9, JPN 9, KHM 9 |
| Compulsory/free pre-primary years | UIS `YEARS.FC.COMP.02` / `.FREE.02` | observed: JPN free 3, KOR free 3, PHL compulsory+free 1, others 0 |
| Compulsory-education and reform policy events | `POLICY_TIMELINE.csv` | 18 `policy_fact` rows (JPN 1886/1947; KOR 1953/1985; HKG 1971/1978/2008/2012; CHN 1986; PHL 1987/2013/2016/2017/2008; KHM 1996); many **not primary-verified this pass** |
| Attendance enforcement / inspection / sanctions | — | **UNABLE**: no public enforcement or inspection series retrieved |
| 4Ps conditional-transfer coverage/compliance | — | **UNABLE**: DSWD data not retrieved (date only, in POLICY_TIMELINE) |
| WGI government effectiveness `GE.EST`, rule of law `RL.EST`, control of corruption `CC.EST` | World Bank WGI (public) | **DATA BLOCKED**: `api.worldbank.org` HTTP 000 on 3 attempts 14:20–14:25; public and should be retried — do not proxy with anything |

## Three traps
1. **De jure ≠ de facto.** The UIS `YEARS.FC.*` series is what the law guarantees, not what is enforced. PHL guaranteeing 12 compulsory years while 110,954 classrooms are missing is exactly the gap the model should represent as separate fiscal/delivery vs legal dimensions — do not collapse them into one index without declaring weights.
2. **Per-student PPP$ denominators differ** (initial government funding, per student, excludes household spending — Cambodia's private tutoring is a large part of real unit cost).
3. **Vintage mixing**: WDI and UIS education-spending shares differ (PHL 3.93 vs 3.45); government revenue/tax data when pulled must come from the same vintage as the spending series.

## Mapping to the model (plug points)
- `fiscal_capacity` → the state's ability to fund `places`/teachers (supply-push parameter bounds; fiscal constraint on the pipeline).
- `delivery_capacity` → conversion of spending into classrooms/teachers; the PHL PTR 37→24 and classroom-ratio series date the capacity build; congestion share is the subnational capacity gradient.
- `enforcement_capacity` → de jure compulsory/free years date the legal floor; WGI (when retrieved) is the governance proxy; attendance/sanctions remain unobserved, so enforcement strength must be a declared assumption.

## Awaiting user approval (nothing sent)
- PSA FIES/APIS/LFS microdata (PH); WB Enterprise Surveys credential/skills module. Both are **AWAITING USER APPROVAL** — no agency contacted.
