# DATA AVAILABILITY — DHS individual recode (IR) waves + LSMS-ISA tutoring expenditure items

**Scope:** the micro leg of the "Bulge Arrival" test (Paper #2), as requested 2026-11-25. This file inventories
**what data actually exist in the holdings** (Mac repo/worktrees + AutoDL box) before any modelling. Every
missing item is recorded as a finding — **no proxy was substituted** and no value was invented.

**Holdings checked (read-only):**
- Repo clone `~/neon-boot/repos/atlas` (partial clone, all refs) and the working worktrees.
- Box `autodl-container-a8f742b5ee-292349c5`: `/root/work` scanned; **no `.dta` and no `.zip` larger than 1 MB
  anywhere**, `/root/work/dhs_ir` does not exist, only small aggregate JSON/CSV/log artefacts (largest files are
  two edsystem multiverse JSONs, unrelated).
- Committed API-cell record: `research/records/2026-11-24-dhs-api-ecological/data/`.

---

## 1. DHS IR waves for the 8 E8 fee-abolition countries

**Verdict: 0 waves present. All are targets only.**

The repo contains **no DHS microdata** (`git ls-files` → 0 `.dta`; DHS Terms forbid redistribution, so none is
committed by design). The box contains none either. What exists is the **public DHS file inventory target list**
(`research/records/2026-11-24-dhs-acquisition/data/dhs_ir_inventory_targets.csv`, 92 files / 14 countries =
public API metadata, committed 2026-11-24), which names the files to obtain — it is not the files.

E8 target IR waves (**67 rows = 48 standard-DHS + 13 MIS + 6 AIS**, independently recounted from the committed CSV), extracted with a `held_on_box_or_repo = NO` column:
[`data/dhs_ir_target_waves_e8.csv`](data/dhs_ir_target_waves_e8.csv).

| Country | t_abolition (sourced) | standard-DHS IR target waves (file names) | held? |
|---|---|---|---|
| MWI | 1994 | 1992 `MWIR22DT.ZIP`; 2000 `MWIR41DT.ZIP`; 2004 `MWIR4EDT.ZIP`; 2010 `MWIR61DT.ZIP`; 2015 `MWIR7ADT.ZIP`; 2024 `MWIR81DT.zip` | **NO** (6) |
| ETH | 1995 | 2000 `ETIR41DT.ZIP`; 2005 `ETIR51dt.zip`; 2011 `ETIR61DT.ZIP`; 2016 `ETIR71DT.ZIP`; 2019 `ETIR81DT.ZIP`; 2024 `ETIR8ADT.zip` | **NO** (6) |
| UGA | 1997 | 1988 `UGIR01DT.ZIP`; 1995 `UGIR33DT.ZIP`; 2000 `UGIR41DT.ZIP`; 2006 `UGIR52DT.ZIP`; 2011 `UGIR61DT.ZIP`; 2016 `UGIR7BDT.ZIP` | **NO** (6) |
| LSO | 2000 | 2004 `LSIR41DT.ZIP`; 2009 `LSIR61DT.ZIP`; 2014 `LSIR71DT.ZIP`; 2023 `LSIR81DT.ZIP` | **NO** (4) |
| TZA | 2001 | 1992 `TZIR21DT.ZIP`; 1996 `TZIR3ADT.ZIP`; 1999 `TZIR41DT.ZIP`; 2004 `TZIR4IDT.ZIP`; 2010 `TZIR63DT.ZIP`; 2015 `TZIR7BDT.ZIP`; 2022 `TZIR82DT.ZIP` | **NO** (7) |
| KEN | 2003 | 1989 `KEIR03DT.ZIP`; 1993 `KEIR33DT.ZIP`; 1998 `KEIR3ADT.ZIP`; 2003 `KEIR42DT.ZIP`; 2008 `KEIR52DT.ZIP`; 2014 `KEIR72DT.ZIP`; 2022 `KEIR8CDT.ZIP`; 2025 `KEIR91DT.zip` | **NO** (8) |
| MOZ | 2004 | 1997 `MZIR31DT.ZIP`; 2003 `MZIR41DT.ZIP`; 2011 `MZIR62DT.ZIP`; 2022 `MZIR82DT.zip` | **NO** (4) |
| GHA | 2005 | 1988 `GHIR02DT.ZIP`; 1993 `GHIR31DT.ZIP`; 1998 `GHIR41DT.ZIP`; 2003 `GHIR4BDT.ZIP`; 2008 `GHIR5ADT.ZIP`; 2014 `GHIR72DT.ZIP`; 2022 `GHIR8CDT.ZIP` | **NO** (7) |

`t_abolition` is sourced 8/8: `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` @
`research/e6e8-sequencing-2026-11-25` @ `2d19da7` (blob `85d09f86…`), quoted in the Paper-#2 packet
(`~/neon-boot/paper2/`, C43).

**Access status (why nothing is held):** DHS downloads are gated, country-approved, per registered user.
`research/records/2026-11-24-dhs-acquisition/application/STATUS_LOG.md`: the 9-country Asia request is
**"received and pending"**; the **Africa-11 request (which contains all 8 E8 countries) is "not yet submitted"**.
No DHS credentials or microdata are in the repo.

### Variables the test would need, and whether DHS IR has them (if acquired)

| Need | DHS IR variable | Availability | Note |
|---|---|---|---|
| Birth year / 5-year birth cohort | `v011` (CMC of respondent's birth) + `v008` (CMC of interview) | **present in every IR**; derivable exactly | cohort = 5·floor(floor(v011/12)/5) |
| Interviewee age | `v012` | present | consistency check vs v008−v011 |
| **Secondary-entry outcome** | **no direct school-entry date/age variable exists in the DHS IR** | **partial**: `v106` (attained level, 0–3: none/primary/secondary/higher), `v107` (highest year), `v133` (years of schooling), `v149` (education categories) | the observable is **attained/attended secondary**, not the *date of entry* into secondary; any "entry" claim must be phrased as attainment/transition at the cohort level and logged as a definitional limit |
| Wealth quintile (Q5−Q1 gap) | `v190` | present in modern IR; may be missing/NaN in some older rounds → listwise handling (see the IR amendment) | must check per wave before pooling |
| Survey design | `v021` (PSU), `v022` (strata), `v005` (weight / 1e6) | present | design-corrected SEs |
| Fertility outcomes (if used) | `v201`, `v206`, `v207` | present | O1 births, O2 surviving |

**No proxy used:** a "bulge arrival" date cannot be faked from attained education, and no rounding of attainment
into a pseudo entry-year is proposed.

### Aggregate API alternative — considered and rejected

The committed DHS-API record (`2026-11-24-dhs-api-ecological`) publishes **education × survey cells**; the DHS
API also exposes some single background characteristics (e.g. `ED_EDUC_W_SEH` has `Age (5-year groups)` and
`Wealth quintile` categories; `FE_FRTY_W_MNC` has `Wealth quintile`/`Residence`/`Region`). These are **separate
margins, not the joint age × wealth × attainment distribution**, and the committed record holds no wealth-quintile
breakdown. They therefore **cannot** yield the pre-registered Q5−Q1 wealth gap in secondary attainment by birth
cohort. Aggregate cells are not a substitute for IR microdata here; using them would change the estimand
(ecological, not individual).

---

## 2. LSMS-ISA tutoring / extra-classes / exam-prep out-of-pocket expenditure items

**Verdict: NOT VERIFIABLE from holdings — 0 LSMS-ISA files and 0 questionnaires in the repo or on the box;
item existence is UNVERIFIED, and no proxy was used.**

| Country | LSMS-ISA panel (candidate waves to verify at acquisition) | held? | tutoring/extra-classes/exam-prep item |
|---|---|---|---|
| MWI | IHS3 2010/11, IHS4 2016/17, IHS5 2019/20 (candidate set) | **NO** | **UNVERIFIED** |
| ETH | ESS 2011/12, 2013/14, 2015/16, 2018/19 (candidate set) | **NO** | **UNVERIFIED** |
| UGA | UNPS 2009/10, 2010/11, 2011/12, 2013/14, 2015/16, 2018/19 (candidate set) | **NO** | **UNVERIFIED** |
| TZA | NPS 2008/09, 2010/11, 2012/13, 2014/15, 2019/20 (candidate set) | **NO** | **UNVERIFIED** |

Wave lists above are the **standard LSMS-ISA sets to be confirmed against the World Bank Microdata Library
catalogue at download** — they are not asserted as held or as final.

What must be inspected per wave, in the education module of the household questionnaire (exact item names are
**wave-specific** and must be read from each questionnaire, not assumed):

1. school **fees / tuition** paid (out-of-pocket);
2. **extra tuition / coaching / private lessons / holiday classes** — the tutoring item the test needs;
3. **examination / exam-registration fees**;
4. uniforms, books/stationery, transport, boarding (to separate the tutoring item from other school costs);
5. the recall period and whether the item is per-child or per-household (needed for a household-level spend
   outcome).

**Where to obtain (and by whom):** World Bank Microdata Library, LSMS-ISA studies for MWI/ETH/UGA/TZA —
questionnaires + data, free but registration/terms acceptance required. **Request by: Trey (holder of the
registered account)**; an agent cannot accept the terms. After download, commit (i) the hashed questionnaire
PDFs/excerpts, (ii) the exact variable names/section locators, (iii) the tidy spending extract, and re-check
this file. If an item is absent in a wave, that is reported as **missing**, not proxied by another school cost.

---

## 3. Other series the bulge test needs (cross-reference, not re-scanned here)

From the Paper-#2 packet (`~/neon-boot/paper2/BULGE_ARRIVAL_STATUS.md`, C43–C44): `L_primary` is **0/8 sourced**
(no education-structure file in any ref — independently re-checked here: no `primary_length`/`L_primary`/
education-duration file in the checked-out trees), so `t* = t_abolition + L_primary` is **0/8**; and no committed
series exist for primary repetition, primary→secondary transition, exam-gate queuing or secondary seat capacity.

---

## 4. Bottom line

- **DHS IR micro leg:** **NOT-ESTIMABLE** — **0/48** required standard-DHS E8 IR waves held (target set is
  48 DHS + 13 MIS + 6 AIS = 67 rows; none present; access request not submitted), and even when acquired the IR has no direct secondary-**entry** variable (attainment
  proxy only).
- **`t*`:** **NOT-ESTIMABLE** — `L_primary` 0/8; no in-repo source, and no web/assumed duration is substituted.
- **LSMS-ISA tutoring spend:** **NOT-ESTIMABLE / item existence UNVERIFIED** — no LSMS-ISA data or
  questionnaires in holdings; exact items must be read from each wave's questionnaire after download.
- **No proxy, interpolation or synthetic series was used.** No modelling was run for this leg.
