> **SYNTHETIC EXERCISE — DESIGN DOCUMENT.** Council design decision, not evidence. Numbers are design parameters,
> not estimates.

# ANCHOR SYSTEM — stand up ONE education system first (user design pivot)

**User directive, 20 Nov 2026; Council decision D38.** Build and show the mechanisms on one system, then test
portability to Hong Kong and China. E1-class two-shock identification is secondary until the anchor works.

## A. Anchor choice: **PHILIPPINES (PHL)**

**Decision: PHL is the anchor.** Data-sufficiency argument:

| Requirement | PHL evidence |
|---|---|
| Long observed enrolment series | GMR/UIS observed GER 1971–2024 (~50 yearly points) on disk (`04_data/data/gmr_observed_6countries_1970_2024.csv`) |
| Completion series | Observed `status=target` completion rows 1999–2024 (12 distinct years, `04_data/TARGETS_FLOW.csv`); thin but observed-only |
| Jobs/markets side | `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` (5,622 rows, 39 series) + `ECONOMY_SERIES.csv` (GDP, sector shares, remittances 1995–2024) |
| Dated **state pushes** | K-12 extension **RA 10533 (2013)**; free SHS (2016) and free tertiary (2018); earlier compulsory primary (Act 74 / 1935 Constitution lineage); school/teacher expansion |
| **Demand pull** | US nurse visa expansion (Abarcar & Theoharides 2024); BPO/IT services growth; remittance inflows |
| **Supply push** | HEI expansion, teacher supply, educated-cohort growth |
| Existing scaffolding | country card (`02_lit/COUNTRY_CARDS/PHL.md`), prior loop-2–5 cells, shadow-phase PH case |
| Weaknesses (declared) | completion pre-1999 missing; PSA microdata blocked; 2013+ events fall inside the holdout window |

**Why not the others:** CHN has the richest state-push battery (1986 Compulsory Education Law; 1999 expansion; 2006
rural fee abolition) and a long GER series, but completion/microdata are thinner → **portability target #1**. HKG has
no UIS completion and a near-universal system → **portability target #2 (timing regime)**. KOR/JPN are near-universal
(timing only; sparse completion) → checks. The anchor must be a system that *massifies within the observed window* and
has jobs/markets data: PHL.

## B. Single-system success criteria (in addition to brief-013 §2–§4 + A1–A4)

1. **Trajectory** (existing): levels (5 pp in-sample; 8 pp out and beat persistence + linear trend), shape corr
   0.6/0.5, cohort conservation exact, false-positive test.
2. **Scaling laws** (A1/A3): generated OOS exponents within the estimator range (secondary +0.286; tertiary +0.776;
   lower-sec completion law) with correct sign.
3. **Milestone timing** (A4/R19): M0 massification crossing ≥50% and M2/M3 universalization crossings within ±5 y
   (±3 y narrow band); primary is near-universal → timing/boundary regime.
4. **Mechanism event reproduction** (new, A5): for each predeclared exogenous event (state push, demand pull), the
   model conditional on that event must generate the observed break: pre-trend clean, break sign and magnitude inside
   the predeclared band, placebo cohorts/fields/regions null. A model that reproduces the trajectory but not the
   event breaks has not "shown the mechanisms".
5. **Rival comparison** (new): at least three fair rivals fit on the same PHL record with the same events; the
   anchor model must beat them on the predeclared event-break estimand and on out-of-sample trajectory, or the honest
   result is equivalence.
6. **No-fitted-events rule:** policy dates and demand-shock dates are **exogenous inputs** (R12/R4); their effects
   may not be calibrated to the outcome.

## C. Mechanism test menu (single system; what would show each)

| Mechanism | PHL test | Signature that would show it | What would refute it |
|---|---|---|---|
| **State push — compulsory/cycle** | K-12 2013 (SHS 2016–17) cohort exposure | break in upper-secondary completion for exposed cohorts; JHS-holder definition shift; pre-trend clean; placebo pre-2013 cohorts null | no break, or break only in treated definition arithmetically |
| **State push — fee abolition** | free SHS 2016; free tertiary 2018 | intake/completion rise concentrated in liquidity-constrained (Q1–Q2); no equivalent rise for unaffected levels; remittance-rich households less responsive | uniform rise across income (demand trend) or no differential |
| **State push — places/teachers** | school construction, teacher supply expansion (DPWH/DepEd series; web search) | capacity leads intake (places/teacher stock → enrolment with declared lag); unmet demand before, absorbed after | no lead relation; capacity follows enrolment |
| **Demand pull — foreign** | US nurse visa expansion (2005–06) | nursing enrolment/licensure response; field-specific; placebo fields null | no field-specific response (E3 DATA BLOCKED for replication; simulated only) |
| **Demand pull — domestic sectoral** | BPO/IT regional growth; remittances | regional transition/enrolment response to demand exposure; placebo sectors null | no regional exposure gradient |
| **Supply push — educated cohorts** | HEI/teacher expansion; education→jobs | schooling expansion leads formal jobs (positive) vs absorbed in informality/queue (R13 negative/zero) | if education→jobs coefficient is ~0/negative, "supply push" is a queue, not job creation |
| **Rival models** | HC (Becker/Mincer), world culture (Meyer/Schofer), labour queue (Thurow/Collins), state-building (Paglayan), sectoral demand (Lewis/Kuznets) | each fitted on the same PHL pre-2013 record with the same exogenous events; predict 2013–2024 and event breaks out of sample | a rival that matches the same moments equally = EQUIVALENT (R3) |

## D. Portability protocol (to HKG then CHN; CHN first where massification is in-window)

**What must transfer (fixed, no re-fit):** the structural/behavioural core — household demand and liquidity rules,
schooling production/progression, state-capacity response functions, provider response, cohort accounting, and the
**parameter values estimated on PHL**.

**What may be re-set (country inputs, declared and dated):** initial cohort structure; observed income, urbanisation,
sector-share, remittance series; **policy-event dates and implementation capacity** (CHN 1986 compulsory law; 1999
expansion; 2006 rural fee abolition — HKG 1971 free primary, 1978 free junior secondary, 2012 HKDSE as structural
context); institutional level/gate mapping; measurement definitions of completion/enrolment.

**Success:** portability PASS if, with no behavioural re-fit and only the declared re-sets, the transferred model
reproduces the country's milestones (M0–M4) and trajectory within §3 tolerances and reproduces the country's
predeclared state-push/demand breaks. **FAIL** if it needs behavioural re-fitting, extra free parameters, or target
fitting — report which parameter had to move (R20). HKG is a timing/ceiling test (near-universal; levels check-only).

## E. Removed/held

E1-class two-shock identification is **secondary** until the anchor works (user directive); E1 stays parked. Rival
model comparison is the substitute for causal direction until the anchor is shown. Shadow education remains closed.
