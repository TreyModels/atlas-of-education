# COEVOLUTION v0 — core verdicts (`SIMULATED`)

Every number below is `SIMULATED`. No observed series was read or fitted. No causal or direction claim is licensed. This is the model core's own summary; the phase report is `FINDINGS.md`.

Predeclaration sha256 `7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d` (verified; the code refuses to run otherwise).

## Declared suite

- 8 arms x 3 paired seeds = 24 runs; seeds 20261121, 20261122, 20261123.
- Runtime 17.9 s (limit 120 s).

## Verdicts

- **D0**: `PASS`
- **ENDOGENEITY**: `OK`
- **COEXISTENCE**: `COEXISTENT`
- **COEXISTENCE_primary_seed**: `COEXISTENT`
- **DIFFERENT-FAMILIES**: `SAME-RESPONSE`
- **SPILLBACK**: `NO-SPILLBACK`
- **NER-CEILING**: `OK`
- **DETERMINISM**: `BYTE-IDENTICAL`

## Baseline coexistence cells (§8.2; district x cohort entry year)

| threshold | value |
|---|---|
| (a) unused accessible ordinary places >= 10% of offers | mean 0.259 (min 0.230) |
| (b) early leaving >= 5% of secondary entrants | mean 0.171 (range 0.126-0.227) |
| (c) qualified applicants per selective place >= 1.20, turned away > 0 | mean 5.31 |
| (d) gate hours per applicant >= 2x catch-up hours per non-selective pupil | mean 4.72 |
| (d) gate-tutoring households >= 20% of selective applicants | mean 0.203 |

## Counterfactual gains (mean years completed, by family type, vs baseline)

| arm | town nonpoor | town poor | village nonpoor | village poor |
|---|---|---|---|---|
| travel_cut | +0.047 | -0.106 | +0.057 | +0.110 |
| ordinary_expansion | +0.072 | -0.098 | +0.086 | +0.183 |
| selective_expansion | +0.021 | +0.005 | -0.021 | +0.030 |

Argmax family type: `{'travel_cut': ['village', 1], 'ordinary_expansion': ['village', 1], 'selective_expansion': ['village', 1]}`.
Pairwise correlations: `{'travel_cut_vs_ordinary_expansion': 0.991, 'travel_cut_vs_selective_expansion': 0.261, 'ordinary_expansion_vs_selective_expansion': 0.333}`.

## Spillback (§9)

- Difference-in-differences (treated village, younger minus older, net of control): [5.14, 0.66, -6.39] pp.
- Verdict `NO-SPILLBACK` (criterion: every seed >= 5 pp).

## Failures reported as failures (no rescue, no tuning)

- `SAME-RESPONSE`: the three one-change arms share the same argmax family type and two of the three 4-type gain vectors correlate above the declared 0.95.
- `NO-SPILLBACK`: the treated-village younger-cohort primary-persistence gain does not clear 5 pp in every paired seed.

