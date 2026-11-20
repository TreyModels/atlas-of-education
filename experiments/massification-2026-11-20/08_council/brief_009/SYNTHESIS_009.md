> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# SYNTHESIS 009 — synthetic scenario families and prediction register (for `lead`)

**What this is.** An **assumption-space map**: 49 assumed parameters, 7 scenario families, and a 74-row predeclared
prediction register for the runner. **It is possibility analysis, never evidence**; the brief-008 identification
limits stand, and no stop rule is reopened by anything here.

| File | Content | sha256 |
|---|---|---|
| `SYNTHETIC_PARAMS.csv` | 49 parameters (P01–P49), values-by-family, literature basis or "assumed", relation ids (R01–R24, ECI-PENDING), identification grade, observable implication, reopening data | `84e6f649…78cdd4` |
| `SCENARIO_FAMILIES.md` | 7 families (6 bundles + F7 negative-growth arm), live/dormant relations, predicted stage profiles, predeclared impossibilities, complexity axis | — |
| `PREDICTION_REGISTER.csv` | 70 family × target rows + 4 direction-only complexity rows; predicted band/direction/inside; predeclared timestamp | **`93cbc563…f5f170b`** (original 70-row: `82c24773…bc4241` retained) |
| `WHAT_WOULD_COUNT_AS_SUPPORT.md` | support / possibly-consistent / impossible criteria; 4a complexity caveat; reporting rules | — |
| `DATA_FIRST_LINK.md` | collapse-power ranking; #1 credential requirement share | — |

**The seven families (one line each).** F1 HC/formalization (schooling creates jobs; returns real); F2 credential
rationing (fixed slots, gates by credential); F3 informal coping/teacher-sold (weak state, teachers sell the
curriculum); F4 strong-state administered (public hiring, administered credentials); F5 migration option (foreign
demand prices the credential); F6 compressed returns/saturation (positional defence as returns fall); F7
negative-growth arm (R13: tertiary GER t−15 → growth −1.035, se 0.240 — the model's `eps_ec>0` prior is run against
this, not assumed).

**Predicted shadow profiles (central band, %; predeclared).**

| Family | KOR all | HKG S1-3 / S4-5 / S6-7 | KHM G9 / primary | PHL all-basic | Predicted register hits |
|---|---|---|---|---|---|
| F1 | 38 | 30 / 36 / 44 | 38 / 30 | 36 | none |
| **F2** | 44 | **34 / 48 / 72** | 45 / 30 | 42 | **HKG all 3 stages; PHL (boundary)** |
| **F3** | 36 | 32 / 38 / 46 | 58 / **45** | **44** | **KHM primary; PHL** |
| F4 | 42 | 36 / 44 / 58 | 44 / 32 | 40 | none |
| **F5** | 46 | 38 / 52 / 72 | 46 / 32 | **44** | **HKG S6-7; PHL** |
| **F6** | 64 (KOR high only) | 40 / 52 / 72 | 50 / 36 | **46** | **KOR high; HKG S6-7; PHL** |
| F7 | 40 | 36 / 46 / 64 | 44 / 34 | 40 | partial only |

**Predeclared impossibilities.** (1) No family reproduces the KOR falling profile (86.0/75.4/66.4); the one-margin
stage engine plus monotone stakes cannot invert it — R23 requires a second (intensive) margin, so a pass here would be
a structural finding. (2) No family reproduces KHM grade 9 (68.4) and KHM primary (41.3) simultaneously (ratio 1.66;
closest F3 = 58/45). (3) No single family fits all four countries; consistency can only be **country-type contingent**.

**Support criteria (predeclared).** Support = a family inside ≥2 targets in ≥2 countries with no target used for
fitting; "possibly consistent" = one family inside HKG's gradient (predicted F2), one inside PHL/KHM rows (predicted
F3), and none inside KOR — i.e. country-type contingency. Impossible = a pattern no coherent family can produce, or one
produced only by setting a parameter to the target. A predicted-outside family landing inside means the mapping was
wrong or its parameters are outside plausibility bands — reported, not quietly accepted. Support is **not** validation.

**Complexity amendment (Lead, before finalisation).** ECI/COI added as a third country-type axis (low/high complexity
alongside state capacity): P46 (ECI level), P47 (+0.40 formal-job creation), P48 (+0.60 complex-job share), P49
(+0.30 pp upper-stage tutoring per 1 sd) — all **assumed**, with Hidalgo & Hausmann (2009) sign expectations; register
rows CX-01…CX-04 are **direction-only** (higher ECI → higher senior take-up, +5–10 pp; higher formal/complex share;
basic near-null; typology conditioning). **Data PENDING:** `04_data/complexity/` absent at finalisation; raw ECI
dictionary/rankings exist in `09_relations/raw/`; data-hunter pull and scout complexity relations in flight. If absent
at runner start, run the six-family map unchanged and mark CX rows unscoreable — no ECI imputation.

**Data-first link (answer).** If one assumed parameter is measured, measure **credential requirement share in hiring
(P17)** — the only employer-side parameter, it separates 4 of 7 families (F2/F6/F7 from F1/F3) and currently has no
empirical requirement schedule. Second: education→formal-job elasticity (P18), confronted with R13. Third: country
Mincer returns table (P13/P14; extract WPS8402 annex). Routes/costs in `DATA_FIRST_LINK.md`.

**Runner hand-off.** Consume `PREDICTION_REGISTER.csv` (74 rows; hash anchored); do not fit to any target; HK 0.85 is
excluded as calibration; report per-family inside/inside-partial/outside; treat the three impossibilities as
hypotheses about the model class, not as validation opportunities. Files: `08_council/brief_009/`.
