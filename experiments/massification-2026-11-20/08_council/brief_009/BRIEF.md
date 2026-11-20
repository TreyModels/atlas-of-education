> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# BRIEF 009 — SYNTHETIC SCENARIO FAMILIES AND PREDICTION REGISTER (iteration 6)

- **sent by / date:** lead, 2026-11-20 ~13:36 Asia/Shanghai (task-25; assumption-space mapping).
- **purpose:** specify the assumed-parameter scenarios, their predicted shadow-education profiles, and a predeclared
  family × target prediction register for the runner. **Possibility analysis; explicitly not evidence.**
- **inputs:** brief 008 (identification limits established); `06_report/LOOP_CLOSEOUT.md`;
  `02_lit/ECON_LIT.md` + `ECON_TARGETS.csv`; `02_lit/SHADOW_TARGETS.csv`; `04_data/econ_round2/PARAMETER_MAP.csv`
  (28 quantities; 10 not observable); `09_relations/{RELATION_CANDIDATES.csv (30 rows), DATA_PATTERNS.md,
  MODEL_PLUG_MAP.md, COUNTRY_TYPOLOGY.md}` (pattern-scout, landed before writing); loop-2–5 cells.

## 1. Literature-grounded ranges used (from ECON_LIT / ECON_TARGETS / pattern-scout)

- Returns: 8.8%/yr world, 8.7 EAP (Psacharopoulos & Patrinos 2018, WPS8402); country Mincer table not extracted.
- Migration: place premium 3.99 (3.71–4.36; Clemens, Montenegro & Pritchett 2008); 9 nurses licensed per migrant
  (Abarcar & Theoharides 2024).
- Fees/participation: KOR 434/553k won per month; 78.5% all-level participation; HKG 2003 35.1/46.6/70.3 (Bray &
  Kwok 2003); KHM case 60.5/26.4 urban/rural, fees 500–1,000 Riel/session; teacher salary US$44/mo vs US$80–100 with
  tutoring (Brehm & Silova WP39); Nepal teacher-tutoring (Jayachandran 2014).
- Panel relations (pattern-scout, 30-country FE panel, correlational unless noted): **R01** spending→secondary GER
  0.111 (Asia 0.189; low-GER 0.132; non-Asia 0.010 ns); **R02** spending→primary 0.021 = saturated null; **R04**
  income→tertiary 0.848 (Asia 1.075; non-Asia 0.281 ns); **R05** income→secondary 0.154; **R07** fertility→primary
  completion −0.189 (plausibly causal); **R09** private share→secondary 0.075 (low-tax 0.102 vs high-tax −0.065);
  **R10** teacher supply→primary 0.528 low-income vs 0.192 ns; **R13** education→growth **negative**: tertiary GER
  t−15 −1.035 (se 0.240); **R21** gate proximity→tutoring; **R22** income elasticity of tutoring spend 1.33;
  **R23** Korea two margins (participation 86→75→66 while spend/student +23%); **R24** urban→tutoring gradients.
- Typology (scout): one flag — *is the state the binding constraint on school places?* — switches R01/R09/R12/R10;
  thresholds: GDP pc US$1,706, tax/GDP 13.1%, 1990 secondary GER 47.3%, urban 40.2%.

## 2. Deliverables (on disk in this directory)

| file | content |
|---|---|
| `SYNTHETIC_PARAMS.csv` | 45 assumed parameters (P01–P45), each with model role, family values, units, literature basis/citation, relation id, identification grade, observable implication, reopening data |
| `SCENARIO_FAMILIES.md` | 7 families: 6 coherent bundles + 1 named negative-growth arm (R13); bundles, live/dormant relations, predicted stage profiles, predeclared impossibilities |
| `PREDICTION_REGISTER.csv` | 70 predeclared rows (7 families × 10 literature targets), predicted direction/band/inside-outside, timestamp, hash |
| `WHAT_WOULD_COUNT_AS_SUPPORT.md` | predeclared support / possibly-consistent / impossible criteria and reporting rules |
| `DATA_FIRST_LINK.md` | rank of assumed parameters by collapse power; #1 = credential requirement share (P17) |

## 3. Predeclaration anchors

- `PREDICTION_REGISTER.csv` sha256 (amended, complexity rows appended): `93cbc563958daf86be2b7d36fd941d8234ebfdd5d30980411da2ca6fcf5f170b` (original 70-row hash `82c24773d93462c46c6e842cf8fe755b69225383450c764c89cf52fa1fbc4241` retained as the first predeclaration).
- `SYNTHETIC_PARAMS.csv` sha256 (amended, P46–P49 complexity rows appended): `84e6f64959e5820101437ccfb9c8bf037a4f3a514fc00e24fc05fe0d4a78cdd4`.
- Declared 2026-11-20T13:52+08:00, before any runner-2 synthetic run. No target was used for fitting; HK 0.85 is
  excluded as the loop-2 calibration moment.

## 3b. Economic complexity (Lead amendment, before finalisation)

- **Data status: PENDING.** `04_data/complexity/` is absent; ECI raw files (dictionary, growth-projection rankings,
  dataverse metadata) exist under `09_relations/raw/`; data-hunter is pulling ECI/COI, pattern-scout is adding
  complexity relations. Until they land, complexity is a **design-intent axis only**.
- **Added as a country-type axis** (low vs high complexity, alongside state capacity) in `SCENARIO_FAMILIES.md`.
- **Added as assumed parameters** P46 (ECI level), P47 (complexity→formal-job creation, +0.40), P48 (complexity→
  complex-job share, +0.60), P49 (complexity→upper-stage tutoring, +0.30 pp per 1 sd ECI), all labelled assumed, with
  Hidalgo & Hausmann (2009) sign expectations and relation id `ECI-PENDING`.
- **Added as direction-only register rows** CX-01…CX-04 (senior take-up +, formal/complex share +, basic null,
  typology conditioning). They are not target-based predictions and cannot be scored as inside/outside.
- **Rule:** complexity is a country-level index, not a mechanism; it may condition relations, never serve as
  synthetic validation (see `WHAT_WOULD_COUNT_AS_SUPPORT.md` §4a).

## 4. Rules

No fabrication; every assumed value is labelled assumed; literature values carry citations; this is a possibility
analysis, never a validation; absent layers (e.g., country Mincer tables) marked "not available"; no stop-rule is
reopened by synthetic support (brief 008 stands).
