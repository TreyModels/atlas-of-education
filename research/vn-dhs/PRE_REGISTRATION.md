# Pre-registration — Vietnam DHS/AIS completion by wealth quintile (credential-floor test)

**Date:** 25 Nov 2026. **Status:** pre-registered before the VN outcome was computed.
**Purpose:** the credential-floor model's Vietnam margin is **upper-secondary completion at age 19**, not
attendance. The VN PR recodes carry no `HV121` attendance, so this test uses education completion by wealth
quintile and compares it with the model's predictions (exits from the bottom 40%: human capital ≈48%,
relational ≈53%) and with the external profiles already in the note (Young Lives 2013: 80.5% top vs 25.1%
bottom quintile; MICS 2014 upper-secondary quintile enrolment 40/67/74/85/93%). Descriptive only.

## Data
- VN DHS 1997 (VNPR31), VN DHS 2002 (VNPR41), VN 2005 AIS (VNPR53); all Stata `.DTA`.
- Wealth: 1997/2002 WI files (`VNWI31`, `VNWI41`: `whhid`, `wlthind5`); 2005 AIS PR has `HV270`.
- The PR recodes have `HV106` (highest level) and `HV109` (highest level completed) but **no `HV121`/`HV122`**
  attendance; the 2005 AIS is an HIV survey, so its education/wealth variables are used as available.
- Raw microdata not committed; derived tables + hashes only.

## Measurement (fixed before computation)
- `HV109` labels: 0 none, 1 incomplete primary, 2 complete primary, 3 incomplete secondary,
  4 complete secondary, 5 higher, 8 don't know.
- **Completed secondary** = `HV109 ∈ {4,5}`. **Non-completer** = `HV109 ∈ {0..3}`; `8` excluded.
- Cohorts: ages **20–24** and **25–29** (completed by the survey; the model's age-19 margin is matched by
  post-19 cohorts).
- Wealth quintile: `wlthind5` (1997/2002, merged to PR `HHID` by normalised whitespace) or `HV270` (2005).
- Weights `HV005/1e6`; weighted percentages; unweighted n; no imputation.

## Decision rule
Report completion by quintile and the **share of non-completers from the bottom two quintiles**. Compare with
the model's 48% (human capital) and 53% (relational) predictions and with the Young Lives/MICS gradients. If
the observed bottom-40 share is near 48–53%, the DHS does not separate the two structures on this margin; if it
is far from both, say so. Do not tune the mapping to rescue a structure.

## Outputs
`results/vn_completion_by_quintile.csv`, `results/catalog.json`, `REPORT.md`.
