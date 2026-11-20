> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# SCENARIO_FAMILIES — the assumption space for shadow education

**This is assumption-space mapping, not evidence about any country.** Every parameter is a declared assumption
(`SYNTHETIC_PARAMS.csv`); literature values carry citations from `02_lit/ECON_LIT.md`, `ECON_TARGETS.csv`, and the
pattern-scout register `09_relations/RELATION_CANDIDATES.csv` (R01–R24). The runner consumes
`PREDICTION_REGISTER.csv` (7 families × 10 targets, 70 predeclared rows, sha256 in `SYNTHESIS_009.md`).

**Typology switch (scout, COUNTRY_TYPOLOGY.md):** four conditional relations — spending→secondary (R01), private
provision→secondary (R09), tax→spending (R12), teacher supply→primary (R10) — are one condition: *is the state the
binding constraint on school places?* Each family carries `capacity_binding` (P33). Thresholds: GDP pc US$1,706
(2015 const), tax/GDP 13.1%, 1990 secondary GER 47.3%, urban 40.2%.

**The seven families** (6 coherent bundles + 1 named arm requested by the Lead for the negative education→growth
finding, R13 = −1.035, se 0.240):

| Family | One line | capacity_binding | Live relations | Dormant relations |
|---|---|---|---|---|
| **F1 HC_FORMALIZATION** | Schooling creates formal jobs; returns are real | no | R04 (income→tertiary), R13 as positive prior | R01/R02/R09/R10 |
| **F2 CREDENTIAL_RATIONING** | Formal slots are fixed; credentials gate access | yes | R01, R09, R21, R22 | R13 positive |
| **F3 INFORMAL_COPING_TEACHER_SOLD** | Weak state; teachers sell the curriculum | yes | R01, R09, R10, R24 | R04 strong |
| **F4 STRONG_STATE_ADMINISTERED** | State funds and administers credentials | yes | R01, R12, R10 | R04 |
| **F5 MIGRATION_OPTION** | Foreign demand prices the credential | no | R04, R21, R28 | R01/R09 |
| **F6 COMPRESSED_RETURNS_SATURATION** | Returns compress; position defended | no | R04 (saturated), R21, R22, R23 | R01/R09/R10 |
| **F7 NEGATIVE_GROWTH_ARM** | Education→growth is negative (R13) | yes | R13 (negative), R01, R21 | R13 positive |

## Family bundles (key values; full list in `SYNTHETIC_PARAMS.csv`)

| Parameter (id) | F1 | F2 | F3 | F4 | F5 | F6 | F7 |
|---|---|---|---|---|---|---|---|
| r_school P13 (%/yr; WPS8402 8.8 world, 8.7 EAP) | 8.8 | 8.8 | 7.5 | 6.0 | 8.5 | 5.0 | 7.0 |
| tertiary/secondary premium P14 | 1.42 | 1.60 | 1.25 | 1.20 | 1.45 | 1.55 | 1.40 |
| education→formal-job elasticity P18 (not observable) | 0.50 | 0.05 | 0.10 | 0.35 | 0.10 | 0.05 | −0.20 |
| credential requirement share P17 (not observable) | 0.25 | 0.65 | 0.20 | 0.50 | 0.55 | 0.60 | 0.60 |
| formal/informal gap P15 (log pts; not observable) | 0.30 | 0.50 | 0.20 | 0.35 | 0.40 | 0.45 | 0.45 |
| transition hazard P19 (not observable) | 0.08 | 0.02 | 0.03 | 0.05 | 0.04 | 0.02 | 0.02 |
| public-sector share P20 (proxy only) | 0.15 | 0.18 | 0.10 | 0.30 | 0.12 | 0.18 | 0.18 |
| teacher-tutor capacity P9 | 0.10 | 0.15 | 0.60 | 0.20 | 0.15 | 0.10 | 0.15 |
| income elasticity of tutoring P11 (KOR-derived 1.33) | 0.8 | 1.0 | 1.2 | 0.9 | 1.1 | 1.3 | 1.0 |
| income→tertiary R04 0.848 (Asia 1.075) | live | live | weak | live | live | live | live |
| spending→secondary R01 0.111 (Asia 0.189) | off | 0.111 | 0.132 | 0.111 | off | off | 0.111 |
| spending→primary R02 0.021 (null) | off | off | off | off | off | off | off |
| fertility→completion R07 −0.189 | global | global | global | global | global | global | global |
| place premium P25 (Clemens 3.99) | 1.0 | 1.0 | 1.0 | 1.0 | 4.0 | 1.0 | 1.0 |
| nurses/migrant P26 (Abarcar 9) | 0 | 0 | 0 | 0 | 9 | 0 | 0 |
| two-margin (hours×participation) P44 (KOR fact) | no | no | no | no | no | yes | no |

## Predicted shadow-education profiles (central band, %; predeclared)

| Family | KOR all | HKG S1–3 / S4–5 / S6–7 | KHM G9 / primary | PHL all-basic | Expected register hits |
|---|---|---|---|---|---|
| F1 | 38 (30–46) | 30 / 36 / 44 | 38 / 30 | 36 | none inside |
| **F2** | 44 (32–56) | **34 / 48 / 72** | 45 / 30 | **42** | **HKG all three stages; PHL all-basic (boundary)** |
| **F3** | 36 (28–44) | 32 / 38 / 46 | 58 / **45** | **44** | **KHM primary; PHL all-basic** |
| F4 | 42 (34–50) | 36 / 44 / 58 | 44 / 32 | 40 | none inside |
| **F5** | 46 (38–54) | 38 / 52 / **72** | 46 / 32 | **44** | **HKG S6–7; PHL** |
| **F6** | **64** (56–72; KOR high only) | 40 / 52 / **72** | 50 / 36 | **46** | **KOR high; HKG S6–7; PHL** |
| F7 | 40 (32–48) | 36 / 46 / 64 | 44 / 34 | 40 | partial only (HKG S6–7 64 vs 65.3–75.3; PHL 40 vs 42–49.9) |

**Predeclared impossibilities (see `WHAT_WOULD_COUNT_AS_SUPPORT.md`):**
1. **No family reproduces the KOR four-stage falling profile** (86.0 / 75.4 / 66.4). All families predict flat or
   rising profiles; the model's stage engine plus a monotone stakes vector cannot invert it. F6 hits only the KOR
   high-school row (64). This is consistent with loop-5 E1's failure and with R23's two-margin requirement.
2. **No family reproduces KHM grade 9 (68.4) and KHM primary (41.3) simultaneously** (ratio 1.66); F3 predicts
   58/45 (ratio 1.29), the closest.
3. **A single family inside all four countries' profiles is predicted impossible**; consistency can only be
   country-type contingent (different families for rich vs poor presets), which is a finding about the assumption
   space, not about the world.

**Coherence notes.** F2's HKG fit is a *predeclared prediction*, not a result: terminal-gate rationing with commercial
provision is exactly the HKG 2003 configuration; if the runner's F2 lands inside all three HKG rows, that is the one
family-level "possibly consistent" outcome. F3 is the only family with teacher-sold supply and is predicted to fit
the PHL 2010 aggregate and KHM primary but to miss KHM's grade-9 rate. F5 and F6 intentionally share the HKG
senior-secondary prediction (convergent implications — the runner cannot distinguish them on shadow data; they differ
on provider mix and returns). F7 exists to stop the model's `eps_ec > 0` prior from being assumed: with R13 =
−1.035, the positive-growth arm must be run and reported, not retained by default.


## Economic complexity axis (ECI/COI) — Lead amendment

**Data status: PENDING.** `04_data/complexity/` absent at finalisation; ECI raw dictionary/rankings exist in
`09_relations/raw/`; data-hunter pull and pattern-scout complexity relations are in flight. Nothing below is scored as
a result; the axis is design intent.

**Why an axis.** Hidalgo & Hausmann (2009) imply that more complex economies have more formal, high-skill production
and higher returns to high-level credentials. If that is a real driver, it should shift the shadow profile toward
upper-secondary/tertiary gates and away from basic-stage, teacher-sold tutoring, and it should raise the formal/
complex-job share. It is **confounded with income and state capacity** (the typology thresholds), so it enters as a
third axis, not a standalone mechanism.

| Complexity type | Family mapping (assumed) | Predicted shadow profile | Predicted shift if complexity is a real driver |
|---|---|---|---|
| **High ECI, capacity not binding** | F1, F6 (and F2 partly) | senior/terminal-gate heavy, commercial, income-elastic | +5–10 pp senior take-up per 1 sd ECI; +formal/complex-job share; basic near-null |
| **High ECI, capacity binding** | F2, F4 | terminal-gate rationing; commercial + state-administered gates | senior/board uptake; credential requirement high |
| **Low ECI, capacity binding** | F3, F7 | basic/teacher-sold; low senior provision; urban–rural gap | basic-stage tutor (saturation-side), teacher-sold supply; senior flat |
| **Low ECI, capacity not binding** | (not mapped in this set — flagged as an empty cell) | — | — |

**Directions (predeclared, from HH reasoning; assumed, not estimated):** complexity ↑ → formal/complex-job creation
(P47, sign +), complex-job share ↑ (P48, +), upper-stage tutoring demand ↑ (P49, +0.30 pp per 1 sd), basic-stage
tutoring ~null (CX-03). **These are direction-only predictions**; they cannot be scored as inside/outside a target
band and cannot convert a synthetic fit into evidence (see `WHAT_WOULD_COUNT_AS_SUPPORT.md` §4a).
