# Adapters — source, recode, design, and verdict per file

Generated from `~/neon-boot/dhs8_local/manifest.json` (14 adapters, all validations passed).
Raw microdata are DHS restricted: local only, never committed, never sent to the box.

## Person records (PR) — used by E1, E2, E3, E6

| Key | File | weight | stratum | psu | id | attendance code | wealth | verdict |
|---|---|---|---|---|---|---|---|---|
| KH-2000 | `cambodia/2000/KHPR42SD` | HV005 | HV022 | HV021 | HV022-HV021-HV001-HV002-HVIDX | HV121==1 | **absent** (no HV270) | E2,E3,E6 ok; E1 blocked |
| KH-2005 | `cambodia/2005/KHPR51SD` | HV005 | HV022 | HV021 | same | HV121==2 | HV270 | ok |
| KH-2010 | `cambodia/2010/KHPR61SD` | HV005 | HV022 | HV021 | same | HV121==2 | HV270 | ok |
| KH-2014 | `cambodia/2014/KHPR73SD` | HV005 | HV022 | HV021 | same | HV121==2 | HV270 | ok |
| KH-2021-22 | `cambodia/2021-22/KHPR82SD` | HV005 | HV022 | HV021 | same | HV121==2 | HV270 | ok (COVID-affected wave) |
| ID-2017 | `indonesia/2017/IDPR71DT` | hv005 | hv022 | hv021 | same | hv121==2 | hv270 | ok |
| PH-2017 | `philippines/2017/PHPR71SD` | HV005 | HV022 | HV021 | same | HV121==2 | HV270 | ok |
| PH-2022 | `philippines/2022/PHPR82DT` | hv005 | hv022 | hv021 | same | hv121==2 | hv270 | ok |

Not adapted: **PH-2003** (HV022 wholly missing → no variance stratum; excluded, BLOCKED).
Unusable: **ID-2002-03, ID-2007, ID-2012, PH-2008, PH-2013** (`hv121` present but 100% empty);
**VN-1997/2002/2005** (no attendance item at all); **ID-1991/1994/1997** (no hv121, no hv270).

## Woman records (IR) — used by E4, E5, E7, E8

| Key | File | weight | stratum | psu | school years | CEB | first birth | first union | households | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| KH-2000 | `KHIR42SD` | V005 | V022 | V021 | V133 | V201 | V212 | V511 (labelled *first marriage*) | V136 | ok |
| KH-2005 | `KHIR51SD` | V005 | V022 | V021 | V133 | V201 | V212 | V511 | V136 | ok |
| KH-2010 | `KHIR61SD` | V005 | V022 | V021 | V133 | V201 | V212 | V511 | V136 | ok |
| KH-2014 | `KHIR73SD` | V005 | V022 | V021 | V133 | V201 | V212 | V511 | V136 | ok |
| KH-2021-22 | `KHIR82SD` | V005 | V022 | V021 | V133 | V201 | V212 | V511 | V136 | ok |
| PH-2022 | `philippines/2022/PHIR82DT` | v005 | v022 | v021 | v133 | v201 | v212 | v511 | v136 | ok |

Not available for Indonesia or Vietnam: the only local "WI" files (`VNWI31FL`, `VNWI41FL`,
`IDWI3AFL`, `PHWI31FL`, `PHWI3AFL`) have three columns (`whhid`, `wlthindf`, `wlthind5`)
and are **wealth-index** files, not women's recodes.

## Runtime assertions (in `harmonize/harmonize.py`)

1. **Attendance code** — the declared HV121 code must have <2% share at ages 25–49 *and*
   >50% at ages 9–14. Observed: 0.000 at 25–49 and 0.76–0.97 at 9–14 for every file.
2. **Never semantics** — blank `V212` must equal `V201==0` and blank `V511` must equal
   `V501==0`, with **zero violations**. Observed: 0 violations in all six IR files.
3. **Design integrity** — stratum and PSU non-missing; unique ID within stratum
   (0 duplicates); singleton strata counted and reported, never silently "fixed".
4. Any failed assertion → the adapter is marked `INVALID` and no CSV is written.
