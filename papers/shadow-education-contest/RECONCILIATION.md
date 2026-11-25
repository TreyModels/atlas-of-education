# Reconciliation — claimed Paper A/B numbers vs committed Atlas records

**Purpose.** The bridge handoff asks to commit "verified" numbers. Several of those claims have no committed
code/data in this repository, and some conflict with committed records. This file separates the three tiers:
**COMMITTED** (citable), **AUTHOR-REPORTED** (not yet verifiable here), **CONFLICT** (must not be cited as is).

## Committed reference values (citable)

| result | value | evidence |
|---|---|---|
| E8 CS ATT at abolition | 12.44362392207772; 95% CI [−2.3558, 27.2431]; SE 7.5507 | `research/e6e8-sequencing-2026-11-25` @ `bd782be`, `results/e8_event_SE.PRM.ENRR_verified8.csv` |
| E8 post ATTs (+1…+6) | 23.8244, 25.9429, 22.1208, 25.1932, 28.5608, 25.9224; mean 25.2607 | same |
| E8 Fisher RI | p_date 9.999e−05; p_country 5.999e−04 (T0), 2.9997e−04 (Tpost); B = 10,000 × 2 | `research/e8-fisher-ri-2026-11-25` @ `fb8b67e` |
| Gender split | D = −3.94395, paired 95% CI [−8.7178, +0.2946] | `research/gender-split-e6e8-2026-11-25` @ `b4eb680` |
| E6 ordering | demand-first 10.0–24.1%; schooling-first 21.5–46.3% (strict 58.3–71.4%) | `research/e6e8-sequencing-2026-11-25` @ `bd782be`; dossier line 115: auditor "76–90%" does **not** reproduce |
| Equifinality (SIMULATION) | within-gate 176 observed vs null 190.52 (p = 0.838); total pairs 319,600 = 159,600 within + 160,000 cross | `research/equifinality-phase-2026-11-25` @ `ab415f2` |
| Contest gate in committed engine | **NOT-IMPLEMENTED**: only `bar`/`quota`; unknown kind silently becomes quota | `…equifinality-phase/PRE_REGISTRATION.md` @ `078cc13`; `engine/eduengine/core.py`:164, 369–371 |
| `t*` bulge | **NOT-ESTIMABLE**: `L_primary` sourced 0/8 in-repo; no proxy | `research/bulge-arrival-2026-11-25` @ `1b91a71` |

## Paper A claims — status

| claim | tier | issue |
|---|---|---|
| Exp 5 on-impact predicted +11.60/+13.48 vs empirical +12.44 | AUTHOR-REPORTED | the empirical +12.44 **matches** the committed E8 value; the simulated predictions have no committed run |
| Exp 1 `t*` live-WDI, 7,290 obs, 2,500 permutations | AUTHOR-REPORTED | data/code not committed. Committed bulge record says `t*` NOT-ESTIMABLE in-repo (0/8). A live WDI `SE.PRM.DURS` pull could legitimately make it estimable, but the series, hashes, sample, and runner must be committed before the null result can be cited |
| Exp 3 Tullock `contest`, 1,640 runs, H2 +0.1086 (p = 1.9e−11) | **CONFLICT** | committed engine has no `contest` kind; committed phase prereg/report records NOT-IMPLEMENTED. The patch, runner, seeds, and results JSON are not in this deposit |
| Exp 4 identifiability (rank 5/7, cond 1.09e13 → 7/7, 43.81) | **CONFLICT / QUARANTINED** | no committed code/results; the shadow-equations review branch is quarantined (`264c059`) and must not be cited |
| E6 "76–90% schooling-first" (appears in an earlier Paper A draft) | **CONFLICT** | the committed record shows this auditor figure does not reproduce; E6 is 10.0–24.1% demand-first, 21.5–46.3% schooling-first |
| Earlier Paper A draft Table 1 event column (+1 22.12, +2 24.18, +3 25.60, +6 28.56; on-impact CI [+7.12, +17.76]) | **CONFLICT** | does not match the committed verified-8 table above (e.g. committed +1 = 23.8244; on-impact CI [−2.3558, 27.2431]). If this is the Paper A being deposited, the empirical table must be corrected to the committed values |

## Paper B claims — status

| item | status |
|---|---|
| 14 arms, 420 runs, 30 matched seeds, HK/Korea calibration | **AUTHOR-REPORTED**; `run_hk_korea_comparative.py` and `hk_korea_comparative.json` not received |
| Four embedded charts | extracted and checked against the handoff numbers: **all four match** (calibration, counterfactual spend, seat expansion, trade-off frontier) |
| Headline counterfactuals (tax +50% raises spend; seat expansion raises participation/spend; wage compression is the win-win route) | **AUTHOR-REPORTED**; simulation, uncalibrated beyond the stated benchmarks; no committed run |

## Verdict rule for future citation

- Empirics: cite only the COMMITTED values above.
- Phase/equifinality: cite `ab415f2`; it is descriptive and **not** evidence beyond chance.
- Contest gate, live-WDI `t*`, identifiability, calibration, and Paper B's run: **cannot be cited as verified**
  until the missing artifacts are committed with code, data, seeds, and hashes.
- Paper A must correct the empirical table if the earlier draft is the deposited version.
