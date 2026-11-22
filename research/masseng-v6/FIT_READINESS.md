# v5 fit readiness and corrections

## Corrections made before the first fit

- **PHL relational driver:** the configuration pointed to absent `occ_credential_share`, which silently produced a zero series. It now uses the verified `formal_share` proxy, as the protocol permits. Short occupation series with classification breaks are not spliced.
- **KHM wage premiums:** converted the reported 30% tertiary and 21% secondary premiums to log points as `ln(1.30) = 0.262364` and `ln(1.21) = 0.190620`. These are not `0.30` and `0.21`.
- **PHL targets:** registered the already sourced 2003/2006 FIES training rows, NTA household shares, CHED totals and Grade 10→11 transition. CHED totals are normalised to the verified 2016 base. The unverified 2023 FIES row is recorded but excluded.
- **Transition timing:** the 93.3% figure pairs Grade 10 in SY2016–17 with Grade 11 in SY2017–18, so its model reference year is **2018**. It is not shifted to the first senior-high cohort to make prediction easier.
- **KHM targets:** registered the sourced 2019/20 household education spending share as a 2019 test row and the DHS 2010 quintile attendance gradients as training rows.
- **Preflight:** fitting now checks mapped-driver existence, verification, units, non-empty training/test sets, finite predictions, and required FIES training targets. It fails instead of silently substituting missing inputs.

## Preflight result

| Country | Training | Test | Diagnostic | Status |
|---|---:|---:|---:|---|
| PHL | 121 | 164 | 5 | Ready with declared warnings |
| KHM | 60 | 50 | 16 | Ready |

Philippine warnings: the college premium combines methods and interpolation across 1995–2013 is a comparability limitation; the relational term uses wage/salary employment rather than a spliced occupation measure.

All **34 tests passed** after these corrections. The first fit is run only after the corrected 2018 transition target passes preflight. Any later protocol change must be a dated amendment. Post-1995 enrolment remains test-only; unverified rows are excluded.
