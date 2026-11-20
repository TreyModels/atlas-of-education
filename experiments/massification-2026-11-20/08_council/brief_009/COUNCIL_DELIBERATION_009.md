> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# COUNCIL DELIBERATION 009 — assumption-space mapping

**Panel (AI composites):** PAGE (model space), PATRINOS (economics; steel-man), BRAY (shadow education, mandatory).
**Input:** `brief_009/BRIEF.md`; deliverables `SYNTHETIC_PARAMS.csv` (49 rows), `SCENARIO_FAMILIES.md` (7 families),
`PREDICTION_REGISTER.csv` (74 rows: 70 target rows + 4 direction-only complexity rows),
`WHAT_WOULD_COUNT_AS_SUPPORT.md`, `DATA_FIRST_LINK.md`; sources `02_lit/ECON_LIT.md`, `ECON_TARGETS.csv`,
`SHADOW_TARGETS.csv`, `04_data/econ_round2/PARAMETER_MAP.csv`, `09_relations/{RELATION_CANDIDATES.csv (30),
MODEL_PLUG_MAP.md, COUNTRY_TYPOLOGY.md}`, loop-2–5 cells. `04_data/complexity/` **PENDING** (raw ECI files exist in
`09_relations/raw/`).

## Agreed

1. **The space is mapped as joint bundles, not knobs.** Seven families (6 coherent + F7 negative-growth arm per Lead):
   F1 HC/formalization, F2 credential rationing, F3 informal coping/teacher-sold, F4 strong-state administered,
   F5 migration option, F6 compressed returns/saturation, F7 negative growth (R13 = −1.035, se 0.240).
2. **Predictions are predeclared and direction+band, never fitted.** HK 0.85 is excluded as the loop-2 calibration;
   no target is used for fitting; the register carries its hash and a predeclaration timestamp.
3. **Three predeclared impossibilities:** (i) no family reproduces KOR 86.0/75.4/66.4 — the one-margin stage engine
   plus monotone stakes cannot invert it (R23's two-margin fact is the missing structure); (ii) no family reproduces
   KHM 68.4/41.3 simultaneously (ratio 1.66; closest F3 = 58/45); (iii) no single family fits all four countries —
   consistency can only be country-type contingent.
4. **Support is possibility, not evidence.** The read-out rules (§2 of `WHAT_WOULD_COUNT_AS_SUPPORT.md`) are
   predeclared; the strongest predicted outcome is "possibly consistent, country-type contingent" (F2 inside HKG's
   three stages; F3 inside PHL all-basic and KHM primary). No stop rule from brief 008 is reopened.
5. **Complexity is an axis, not a validation.** ECI/COI enters as a third country-type axis (P46–P49 assumed;
   CX-01…CX-04 direction-only), can condition the family map, and cannot be scored inside/outside or used as
   synthetic validation — it is endogenous to education and correlated with income/capacity.
6. **Data-first collapse ranking:** #1 credential requirement share in hiring (P17 — the only employer-side parameter,
   separates 4 of 7 families); #2 education→formal-job elasticity (P18, confronted with R13); #3 country Mincer
   returns table (P13/P14, cheap annex extraction).

## Disagreements preserved

**D1. PATRINOS vs PAGE — F2's HKG fit is a convenient prediction.**
PATRINOS: F2 (terminal-gate credential rationing, commercial provision) was constructed so that its central band sits
inside the HKG 2003 gradient (34/48/72 vs 35.1/46.6/70.3); a prediction that was built to pass is weak evidence.
PAGE: it is legitimate as a *predeclared* prediction — the family was specified before the register, and the value of
the exercise is that F2, F5 and F6 make *different* predictions elsewhere (KOR, provider mix); if F2 passes HKG and
also predicts the rest, the map is informative. *Resolution:* report F2's HKG outcome as "predeclared, but
family-designed for the HKG type; not evidence", and rely on the cross-family contrasts, not the single pass.

**D2. BRAY vs PATRINOS — KHM grade-9 miss.**
BRAY: no family is predicted inside KHM 68.4, which is the strongest empirical shadow moment in the set; the map may
be underspecified (teacher-sold supply plus gate stakes at Grade 9). PATRINOS: that is a legitimate impossibility
finding — a one-margin structural model cannot hit both KHM 68.4 and 41.3; do not tune to fix it. *Resolution:*
record as a predeclared impossibility, not a tuning target; if the runner produces it, report a structural finding.

**D3. All — complexity amendment.**
The axis is added before finalisation, but data are PENDING; the register rows CX-01…CX-04 are direction-only and
unscoreable. If ECI data remains absent, the runner runs the six-family map unchanged and marks the complexity rows
unscoreable; no ECI imputation is permitted.

## Read-out

The runner consumes `PREDICTION_REGISTER.csv` (sha256 `93cbc563…f5f170b`); the original 70-row hash `82c24773…bc4241`
is retained as the first predeclaration. Any post-run change is an amendment with a new timestamp. The exercise can
at most produce a **country-type-contingent possibility** result; it cannot validate any family, reopen incidence, or
attribute a causal role to complexity.
