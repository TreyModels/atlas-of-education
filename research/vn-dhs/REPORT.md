# Vietnam DHS/AIS — secondary completion by wealth quintile (25 Nov 2026)

Pre-registered in `PRE_REGISTRATION.md`; script `completion_profile.py`; tables in `results/`.
Raw microdata are not committed (DHS terms); derived tables + hashes are.

## Coverage / measurement

| wave | PR | attendance (`HV121`) | education completion | wealth |
|---|---|---|---|---|
| 1997 | VNPR31 (Stata) | **absent** | `HV106`/`HV109` | WI `wlthind5` merged on `HHID` |
| 2002 | VNPR41 (Stata) | **absent** | `HV106`/`HV109` | WI `wlthind5` merged on `HHID` |
| 2005 AIS | VNPR53 (Stata) | **absent** | `HV106`/`HV109` | `HV270` in PR |

The model’s Vietnam margin is **upper-secondary completion at 19**, so this is the native outcome: completed
secondary = `HV109 ∈ {4,5}`; cohorts 20–24 and 25–29 (post-19). `HV121` attendance does not exist in these
VN recodes, unlike Cambodia/Philippines, so no attendance test is possible here.

## Completion by wealth quintile

| wave | cohort | completed secondary | Q1 | Q2 | Q3 | Q4 | Q5 | **bottom-40 share of non-completers** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1997 | 20–24 | 16.5% | 1.4 | 5.7 | 9.0 | 20.5 | 46.1 | **47.3%** |
| 1997 | 25–29 | 22.6% | 4.7 | 12.6 | 20.4 | 29.1 | 46.2 | **49.3%** |
| 2002 | 20–24 | 27.7% | 4.8 | 11.7 | 18.6 | 36.4 | 63.4 | **51.5%** |
| 2002 | 25–29 | 21.2% | 1.5 | 5.5 | 12.8 | 19.3 | 58.6 | **50.6%** |
| 2005 AIS | 20–24 | 33.5% | 6.6 | 17.8 | 29.0 | 48.0 | 64.6 | **50.5%** |
| 2005 AIS | 25–29 | 21.1% | 4.9 | 8.3 | 16.0 | 22.5 | 53.4 | **47.1%** |

## Reading

- **The gradient is very steep**: Q1 completion is 1–7% against Q5 46–65%. This is consistent with the
  external profiles already in the relational-floor note (Young Lives 2013: 80.5% top vs 25.1% bottom;
  MICS 2014 upper-secondary 40/67/74/85/93%).
- **The bottom-40 share of non-completers (47–52%) sits between the model’s human-capital (48%) and
  relational (53%) predictions.** This summary statistic therefore does **not** separate the two structures
  for Vietnam — exactly the caution in the note that Vietnam is the one country where the data already push
  against the relational floor on the full profile rather than on a single bottom-40 number.
- **The full five-quintile profile must go into the credential-floor ABC**; the single statistic is not
  decisive. Levels rise across cohorts (16.5% → 27.7% → 33.5% completed secondary at 20–24), but the
  bottom-40 share is stable at ~47–52%.

## Caveats

- 2005 is an **AIS (HIV) survey**, not a full DHS; its education/wealth variables are usable but its sample
  design differs. The 1997/2002 waves are full DHS.
- 1997/2002 wealth comes from the separate WI file merged on normalised `HHID`; the 2005 PR carries `HV270`.
- `HV109` categories: 0 none, 1 incomplete primary, 2 complete primary, 3 incomplete secondary,
  4 complete secondary, 5 higher, 8 don’t know (excluded). “Completed secondary” = 4–5.
- Cohorts 20–24/25–29 approximate the model’s age-19 margin; DHS education is household-reported.
- No attendance variable exists in these VN recodes; this is a completion test by construction.
- Weighted `HV005/1e6`; unweighted n in the CSV.
