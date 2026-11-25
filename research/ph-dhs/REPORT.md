# Philippines DHS — attendance and the credential-floor test (25 Nov 2026)

Pre-registered in `PRE_REGISTRATION.md`; script `quintile_profile.py`; tables in `results/`.
Raw microdata are not committed (DHS terms); derived tables + hashes are.

## Coverage

| wave | PR file | attendance (`HV121`) | wealth quintile (`HV270`) | used |
|---|---|---|---|---|
| 2003 | PHPR41 (SAS) | yes (0/1) | yes | **yes** |
| 2008 | PHPR52 (SAS) | **all NotAppl** in the release | yes | no |
| 2013 | PHPR62 (Stata) | **all missing** in the release | yes | no |
| 2017 | PHPR71 (SAS) | yes (0/2) | yes | **yes** |
| 2022 | PHPR82 (Stata) | yes (0/2) | yes | **yes** |

1993 and 1998 PR recodes have no `HV121`/`HV122` and no `HV270`/`HV271`; they carry `HV106–HV109`
(completion) and separate WI files (`WHHID`, `WLTHINDF`, `WLTHIND5`), so they can support a later
**completion-by-quintile** check but not the attendance test. The 1993 INDEPTH file is a special subsample
and is excluded.

## Credential-floor statistic (ages 14–17)

| wave | attendance | Q1 | Q2 | Q3 | Q4 | Q5 | **bottom-40 share of non-attenders** |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2003 | 71.2% | 55.7 | 64.6 | 73.5 | 79.6 | 80.3 | **52.4%** |
| 2017 | 87.3% | 74.8 | 84.6 | 88.9 | 93.9 | 95.8 | **68.1%** |
| 2022 | 92.8% | 85.8 | 92.4 | 94.1 | 96.1 | 97.2 | **66.5%** |

Model predictions: human capital ≈ **65%**, relational floor ≈ **98%**.

**Reading:** the relational floor is rejected (66–68% is nowhere near 98%). The 2017/2022 values sit on
the **human-capital prediction (65%)**; 2003 is below it. As attendance rises toward universal, the
remaining non-attenders become *more* bottom-concentrated (52% → 66–68%), which is the pattern a
human-capital/positional model predicts, not a fixed relational floor.

**Cross-country contrast with Cambodia** (same test): Cambodia's bottom-40 share is **47.5–51.6%** across
2005–2021–22, i.e. *less* bottom-concentrated than human capital predicts; the Philippines is **52–68%**,
i.e. close to human capital. Neither is anywhere near the relational floor's 98%.

## Secondary: attendance by age group (national, both sexes)

| wave | 6–11 | 12–14 | 15–17 |
|---|---:|---:|---:|
| 2003 | 92.2% | 88.4% | 66.7% |
| 2017 | 97.9% | 95.8% | 85.7% |
| 2022 | 95.1% | 95.8% | 91.8% |

(The 2022 6–11 value is slightly below 2017; not investigated here.)

## Caveats

- `HV121` coding differs by release (2003 uses 0/1; 2017/2022 use 0/2); attendance is `HV121 ∈ {1,2}`.
- 2008/2013 cannot be used: the PR release marks `HV121` NotAppl/all-missing even though the reports have
  attendance tables; the variable may live in another recode. Do not substitute the final-report table
  without recording the source.
- The model's "exits" (credential non-completion) are not exactly "non-attenders at 14–17"; the mapping
  must be fixed in the credential-floor code before the formal test.
- The 1993/1998 waves need the WI merge and a completion-based (not attendance) test.
- Weighted `HV005/1e6`; Taylor SE with PSU/strata; unweighted n in the CSVs.
