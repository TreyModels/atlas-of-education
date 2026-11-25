# Eight DHS descriptive experiments — report

**Programme:** Atlas of Education · DHS window 2026-11-25 · branch `research/dhs-eight-experiments-2026-11-25`
**Party:** `deepseek-dhs` · **Authorising assignment:** Bridge `366086d3-1bfc-4465-8a7c-86519848db1f`
**Status:** executed on real DHS microdata. Exploratory and descriptive only.

---

## 0. What this is, and what it is not

These are **eight within-wave descriptive domain means with design-based standard errors**.
They are **not** causal estimates. In particular:

- birth before 20 and union before 20 are **not** effects of schooling;
- wealth quintiles are a **relative asset index**, not income or expenditure;
- current household size is **not** kin support, and is not a household's kin network;
- comparisons across waves are **not** a panel: each survey is its own cross-section with
  its own sample, and no person is linked across waves.

The starter (`experiments.R`, v1) was **untested** and is superseded by `engine/experiments_v2.R`.
Nothing in this report claims the starter was validated.

---

## 1. Data, access, and what was left out

Real DHS microdata already on the machine under `/Users/treymenefee/neon-boot/pulled/dhs`
(4 countries, 35 recode files). Raw and unit-level data stayed **local**; this repo contains
only design-based aggregates.

| Country | Person recodes (PR) | Individual-woman recodes (IR) | Verdict |
|---|---|---|---|
| Cambodia | 2000, 2005, 2010, 2014, 2021-22 (`.SAS7BDAT`) | same 5 waves | full E1–E8 |
| Indonesia | 2017 (`.DTA`) usable; 1991/1994/1997 lack attendance & wealth | **none** (1997 "WI" file is a 3-column wealth stub) | E1–E3, E6 only |
| Philippines | 2003, 2017, 2022 | 2022 only | E1–E3, E6 all; E4–E8 2022 only |
| Vietnam | 1997, 2002, 2005 — **no attendance variable** | **none** (`WI` = wealth stubs) | **all 8 BLOCKED** |

Three genuine data traps were found and are documented rather than papered over:

1. **`WI` is not "women's individual".** `VNWI31FL`, `VNWI41FL`, `IDWI3AFL`, `PHWI31FL`,
   `PHWI3AFL` contain exactly three columns (`whhid`, `wlthindf`, `wlthind5`) — they are
   **wealth-index** files. No women's recode exists locally for Vietnam, Indonesia, or
   Philippines 1993/1998. Those cells are BLOCKED, not estimated.
2. **Philippines 2003 has no variance stratum.** `HV022` is wholly missing; only `HV023`
   (design domain, 17 regions) exists. Using `HV023` would substitute a coarser
   stratification for the one DHS uses for its own standard errors, so PH2003 is
   **excluded from design-based estimation** and reported as BLOCKED.
3. **Vietnam has no school-attendance item** in any local recode, so E1–E3 and E6 cannot be
   formed (education *level* is not attendance).

### 1.1 Blocked experiments (documented, not fabricated)

| Experiment | Blocked for | Reason |
|---|---|---|
| E1 | Vietnam; Cambodia 2000 | no attendance; KH2000 PR has no `HV270` wealth |
| E2, E3 | Vietnam | no attendance item |
| E4, E5, E7, E8 | Indonesia, Vietnam, Philippines 1993/1998/2003/2008/2013/2017 | no individual-woman recode available locally |
| E6 | Vietnam | no attendance item |
| all | Philippines 2003 | no variance stratum |

---

## 2. Adapter decisions, with the evidence for each

Every non-obvious recode is asserted at runtime in `harmonize/harmonize.py`; a failed
assertion invalidates the file rather than producing a number.

### 2.1 The attendance code is wave-specific — proven, not assumed

`HV121` does **not** use one coding scheme across waves. Frequencies (`*.FRQ`) show
Cambodia 2000 with three categories (0 No, 1 Currently attending, 2 Attended at some time)
while 2005–2021-22 expose only two (0 No, 2 "Attended at some time"). Read literally,
code 2 would mean *ever* attended — which would make adult attendance ~20–26%, absurd.

The decisive test is the age profile of each candidate code. Code 2 has **exactly 0.000
share at ages 25–49** in every wave and peaks at 9–14; "ever attended" cannot be zero among
adults. Therefore **code 2 = currently attending in the current school year**, and the
value label is a DHS recode artefact. Cambodia 2000 and Philippines 2003 use code **1**.

| File | declared code | share at 25–49 | share at 9–14 |
|---|---|---|---|
| KH 2000 | 1 | 0.000 | 0.775 |
| KH 2005 / 2010 / 2014 / 2021-22 | 2 | 0.000 | 0.878 / 0.907 / 0.891 / 0.761 |
| ID 2017 | 2 | 0.000 | 0.970 |
| PH 2017 / 2022 | 2 | 0.000 | 0.969 / 0.967 |

### 2.2 Blank `V212`/`V511` is a **verified never**, not an unknown

The README requires 99 for known never and NA for unknown, and forbids treating an unknown
as "no". In these files the never-states arrive **blank**, not as 99. Blank-to-meaning was
therefore proven rather than assumed:

- `V212` (age at first birth) blank **iff** `V201` (children ever born) = 0 — **0 violations
  in all six IR files** (e.g. 5,622 blank / 5,622 nulliparous in KH 2021-22);
- `V511` (age at first union) blank **iff** `V501` = 0 (never married/in union) — **0
  violations in all six**.

So blank ⇒ 99 (verified never), and nulliparous or never-united women correctly count as
*not* having had a birth/union before 20. Treating them as NA would condition on parity and
badly bias E5/E7. Note Cambodia 2000 labels `V511` "age at first marriage" rather than
"first cohabitation" — a real definitional break across waves.

### 2.3 Other mandatory recodes

- `school_years` = `HV108`/`V133`; values ≥95 are DHS "don't know/inconsistent" and are
  forced to NA. They are **not** years of schooling. (The v1 starter would have binned 98
  as "12+".)
- `wealth` = `HV270`/`V190`, 1–5, survey-specific relative index.
- Design: `weight` = `HV005` (person) / `V005` (woman), **separately per record type**;
  `stratum` = `HV022`/`V022`; `psu` = `HV021`/`V021`.
- Unique ID = stratum–PSU–household–`HVIDX`. `HV003` is the **respondent's** line number,
  not the member line; using it produced 76–82% spurious duplicates before this was caught.
- Every file used has **0 singleton strata** and 0 duplicate IDs within strata.

### 2.4 E6 had to change record type — a starter defect

E6 was specified on **woman** records with outcome `currently_in_school`. No DHS IR/WI file
carries a current-attendance item (searching every IR label for "school"/"attend" returns
only "traditional birth attendant"). E6 was therefore **unrunnable as specified in every
country** and silently produced empty cells. It is implemented on **person** records
restricted to females aged 20–24, which is the only place the observable exists, and is
flagged as a documented deviation.

---

## 3. Validation

**Independent replication against a prior, externally anchored pipeline.** A previously
validated Cambodia attendance series (itself checked against DHS 2021-22 final report
Table 2.12, primary NAR 72.8) was reproduced from scratch. Two independently written
pipelines — Python hand-rolled Taylor linearisation vs R `survey` — agree across all 15
wave × age cells to **max |Δ| = 0.139 pp, 0.21 SE**.

The residual structure is itself informative: agreement is exact against the prior
"attended at any time in the current school year" variant, while the prior's stricter
variant (requiring `HV122 > 0`) differs by up to 5.4 pp **only at ages 6–11** (pre-school /
level-0 records). Within the E1–E3 domain (14–17) the two definitions differ by ≤0.035 pp,
so no conclusion here depends on the choice.

**Synthetic engine tests** — `engine/run_tests.R`, 14 checks, all passing:
SRS mean/SE vs closed form;  stratified-cluster mean and SE vs a hand-written linearisation
(exact to 1e-8); domain mean **and SE** when PSUs lie wholly outside the domain (plus a
demonstration that the naive row-drop analysis differs — the classic trap); domain-lonely
and design-level-lonely PSU handling; 99-as-never vs NA-as-unknown (hand-computable 20/60);
`school_years=98` not binned as 12+; malformed input failing loudly; run determinism.

**Design df** is reported per cell (e.g. 1,903 for Indonesia 2017, 117 strata / 1,247 PSUs
for Philippines 2022). Normal-approximation CIs are used and are approximate.

---

## 4. Results

Sign convention for contrasts: the difference is **group A − group B** as named, computed
with `svycontrast` on the joint design so that the covariance between domain means is
carried. Holm adjustment is within each experiment × country family of waves.

Coverage: **53 of 64 country-wave-experiment cells estimated**, 9 BLOCKED, 1 insufficient,
2 with domain-lonely PSUs noted.

### E1 — Adolescent attendance by wealth quintile (persons 14–17)

| Country | Wave | Q1 | Q5 | Q1−Q5 | SE | Holm p |
|---|---|---|---|---|---|---|
| Indonesia | 2017 | 73.2 | 92.4 | −0.192 | 0.015 | <0.001 |
| Cambodia | 2005 | 53.5 | 75.9 | −0.224 | 0.025 | <0.001 |
| Cambodia | 2010 | — | — | −0.393 | 0.026 | <0.001 |
| Cambodia | 2014 | — | — | −0.362 | 0.028 | <0.001 |
| Cambodia | 2021-22 | — | — | −0.250 | 0.032 | <0.001 |
| Philippines | 2017 | — | — | −0.210 | 0.015 | <0.001 |
| Philippines | 2022 | — | — | −0.114 | 0.013 | <0.001 |

Monotone in every wave. The gradient is **widest in Cambodia 2010–2014 and narrows
substantially by 2021-22**; the Philippines 2022 gradient is the narrowest measured.
*Competing explanations:* (i) equalisation of access as enrolment saturated; (ii) the
wealth index is wave-specific, so quintile boundaries are not comparable across waves and
"narrowing" may be partly an index artefact; (iii) Cambodia 2021-22 is COVID-distorted
(the same wave's primary NAR fell to 72.8 against a 2019 census household figure near 90%),
so the narrowing there is not a clean trend. These are not separable with these data.

### E2 — Attendance by residence (persons 14–17)

Rural minus urban: Cambodia −0.113 (2000), −0.058 (2005), −0.162 (2010), −0.171 (2014),
−0.048 (2021-22); Indonesia −0.052 (2017); Philippines −0.015 (2017, **null**, p=0.20) and
−0.022 (2022). The rural gap is small and, outside Cambodia's 2010/2014 peak, close to
noise. *Interpretation limit:* residence is a coarse proxy and urban/rural definitions are
not harmonised across countries.

### E3 — Attendance by sex (persons 14–17)

Male minus female: Cambodia **+0.235** (2000) → +0.112 (2005) → +0.083 (2010) → +0.019
(2014, **null**) → **−0.055** (2021-22); Philippines −0.071 (2017), −0.035 (2022);
Indonesia −0.024 (2017). This is a **sign reversal** in Cambodia across two decades: a large
male advantage in 2000 becomes a modest female advantage by 2021-22, with the crossing near
2014. *Competing explanations:* (i) genuine convergence in girls' schooling; (ii) the
composition of who remains in the 14–17 population changed (migration, child work);
(iii) questionnaire change. The reversal is large enough (23 pp in 2000) that (iii) alone is
unlikely, but this design cannot adjudicate (i) vs (ii).

### E4 — Children ever born, women 40–49, by years of schooling

| Country | Wave | 0–5 yrs | 12+ yrs | gap | SE | Holm p |
|---|---|---|---|---|---|---|
| Cambodia | 2000 | 5.51 | 2.60 | +2.913 | 0.613 | <0.001 |
| Cambodia | 2005 | 5.08 | 1.84 | +3.235 | 0.270 | <0.001 |
| Cambodia | 2010 | 4.36 | 2.11 | +2.251 | 0.152 | <0.001 |
| Cambodia | 2014 | 4.11 | 2.42 | +1.688 | 0.139 | <0.001 |
| Cambodia | 2021-22 | 3.06 | 2.25 | +0.808 | 0.126 | <0.001 |
| Philippines | 2022 | 4.75 | 2.32 | +2.433 | 0.150 | <0.001 |

Completed-cohort fertility fell in **both** groups, and the **education gap narrowed by 2.4
children** in Cambodia over 21 years (3.2 → 0.8). The 2000 and 2005 endpoints rest on small
12+-year cells (n = 25 and n = 33), so the size of the narrowing is less certain than its
direction; the 2010→2021-22 part of the series is estimated on groups of 391–1,011 and is
the more reliable segment. *Competing explanations:* (i) fertility
transition compressed all groups toward replacement; (ii) the 0–5-year group in 2021-22 is a
different, more selected population than in 2000 (schooling expanded, so "under 6 years"
became a smaller and more disadvantaged residual); (iii) differential mortality/survival of
high-parity women. (ii) is the most serious threat: the 0–5 group's **share** of the cohort
falls over time, so the narrowing is partly compositional. E4 is **duplicative** of prior
work in this repo (see §6).

### E5 — Birth before age 20, women 25–34, by years of schooling

Gap (0–5 minus 12+): Cambodia +0.317 (2000), +0.181 (2005), +0.235 (2010), +0.256 (2014),
+0.255 (2021-22); Philippines +0.405 (2022). Levels: 0–5 years ≈ 0.28–0.33 throughout;
12+ years 0.143 (2005) falling to 0.021 (2021-22), and 0.108 in the Philippines. The
2000 value for 12+ years (0.0148, SE 0.0147, n = 80 but CV ≈ 1.00) is effectively a single
early birth and should be treated as uninformative rather than as a low rate.
*Critical caveat:* schooling is measured at the survey and may be **completed after** the
birth, so this is not a temporal ordering and certainly not a causal effect. The non-monotone
12+ series (0.143 in 2005, 0.015 in 2000) is a warning that the cell is small and the
classification unstable.

### E6 — Current school participation, women 20–24, by residence

Rural minus urban: Indonesia −0.098 (2017); Cambodia −0.036 (2000), −0.063 (2005), −0.187
(2010), −0.173 (2014), −0.134 (2021-22); Philippines −0.046 (2017, p=0.03) and +0.030 (2022,
**null**, p=0.15). Participation at 20–24 is low everywhere and the rural penalty is
clearly negative except in the Philippines 2022. *Caveat:* the 20–24 window mixes tertiary
participation with late secondary completion, and institution types are not distinguished.

### E7 — Union before age 20, women 25–34, by years of schooling

Gap: Cambodia +0.390 (2000), +0.260 (2005), +0.319 (2010), +0.382 (2014), +0.394 (2021-22);
Philippines +0.550 (2022). Levels: 0–5 years 0.47–0.53 (Cambodia), 0.68 (Philippines);
12+ years 0.076–0.273. Unlike E4, this gap **does not narrow** — it is stable or widening
in Cambodia. The 12+ series falls (0.136 → 0.076) while the low-education series is flat
near 0.5. *Competing explanations:* (i) schooling delays union; (ii) early union truncates
schooling — direction is not identified here, and the two are observationally equivalent in
a cross-section. Cambodia 2000 measures first **marriage**, later waves first **union**, so
the 2000 level is not strictly comparable.

### E8 — Current household size, women 40–49, by years of schooling

**Essentially null in Cambodia**: gaps +0.726 (2000, p=0.25), +0.323 (2005, p=0.42), +0.369
(2010, p=0.16), +0.150 (2014, p=0.45), −0.096 (2021-22, p=0.65); all Holm-adjusted p = 1.00.
Household size falls for everyone (6.31→4.62 in the 0–5 group; 5.58→4.72 in 12+), but the
**education differential is not distinguishable from zero**. In the Philippines 2022 the gap
is real: 5.77 vs 4.80, +0.972 (p<0.001). This is a genuine **negative result** for the
Cambodian case and should not be reported as a schooling effect elsewhere.

---

## 5. Missingness, coverage, reliability

- Analysable n per cell (whole domain): 2,056 (smallest, KH 2000 E6) to 15,052
  (ID 2017 E1–E3).
- Loss between eligible and analysable is small: ≤1.5% in every cell except KH 2000 E6
  (2,118 → 2,056, 2.9%) and KH 2000 E4/E8 (3,245 → 3,232).
- **Group-level cells are not all large.** The smallest is **n = 25** (Cambodia 2000,
  12+ years, E4 and E8; 22 PSUs), then n = 33 (Cambodia 2005, 12+ years). Almost nobody
  aged 40–49 in Cambodia in 2000 had 12+ years of schooling, so that group is a thin
  residual — not a rounding detail. **One cell is flagged for high CV**: E5 Cambodia 2000,
  12+ years, estimate 0.0148 with SE 0.0147 (CV ≈ 1.00), i.e. approximately one woman;
  that level and the corresponding 2000 gap must not be read as a rate. No cell was
  flagged for n < 25 or for fewer than 10 PSUs, and design df is ≥ 245 everywhere.
- Two E6 cells carry **domain-lonely PSUs** (stratum with one PSU contributing to the
  domain: KH 2005 → 2, KH 2000 → 11). These are reported, not silently adjusted. Under
  domain estimation via `subset()`, zero-weight PSUs remain in the design and contribute
  zero to the linearised total, which is the correct treatment; the flag exists so the
  reader can see where a stratum contributes a single PSU.
- Design-level singleton strata: **none** in any file used (verified per file).
- Item missingness that matters: `HV121` missing on 0–559 records per PR file; `HV108`
  don't-know codes 0–367 per file; `V133` 0–66. All excluded, not imputed.

## 6. Dedupe — duplicate vs genuinely new

| Prior work | Relation to this run |
|---|---|
| `research/cambodia-dhs` (attendance by wave/sex/residence, quintile profile) | **Duplicate estimand** for E2/E3 on Cambodia; our numbers reproduce it to 0.21 SE. Used here as the *validation target*, not as a new finding. |
| `research/records/2026-11-24-dhs-acquisition/data/ceb_education_cells.csv` (CEB women 40–49 by education level, 14 countries incl. KH, PH2022) | **E4 is substantially duplicative.** Prior gives 5.4 / 4.4 / 3.2 / 2.3 by level for PH2022; we give 4.75 / 3.39 / 2.32 by years. Different cut, same domain, same direction. New contribution is design-based SEs/CIs and years-of-schooling bands — not a new substantive result. |
| `research/dhs-api-ecological`, `dhs-corrected`, `dhs-eco-gfr-uncomputed` | Different unit of analysis (ecological/API aggregates, not microdata). Not duplicated; not comparable. |
| `research/bulge-micro-dhs` | Different question. |
| **E1, E5, E6, E7, E8** | **Genuinely new** in this repo: no prior design-based estimates for the wealth gradient at 14–17, early birth, young-adult participation, early union, or household size. |

## 7. Limitations

1. **Descriptive only.** No causal claim; no temporal ordering is established for E5/E7.
2. **Wealth quintiles are wave-specific** relative indices; a "Q1 vs Q5" gap is not a
   money metric and quintile cut-points move between waves.
3. **Repeated cross-sections are never combined**; each cell is its own universe, and no
   person is linked across waves.
4. **Multiple testing**: Holm within experiment × country. Across 55 contrasts, treating
   each as an independent discovery would be wrong, and the adjusted values are the ones
   quoted.
5. **Normal-approximation CIs** are approximate; no bootstrap or replication variance was
   computed.
6. **Suppression**: no cell in this run is disclosive (all are large domains and coarse
   age-education-residence groups), but only aggregates are published.
7. **One wave is COVID-distorted** (Cambodia 2021-22); it is flagged where used.
8. **Education is measured at the survey**, so E5/E7 cannot order schooling against early
   birth/union.
9. **The `HV121` definition** is "attended at any time during the current school year",
   which at ages 6–11 differs from a "level>0" definition by up to 5.4 pp. Immaterial at
   14–17.

## 8. Reproducing

```
harmonize/harmonize.py                      # local only -> ~/neon-boot/dhs8_local/normalized
engine/experiments_v2.R  normalized_all.csv runs/2026-11-25_all
engine/contrasts.R       normalized_all.csv runs/2026-11-25_all
engine/summarise.py      runs/2026-11-25_all # -> SUMMARY.md, hashes.txt
engine/run_tests.R                          # 12 synthetic checks
engine/validate_benchmarks.R                # real-data benchmark replication
```

Environment: R 4.4.3 + `survey` 4.5.0 (conda-forge, `~/neon-boot/renv`), Python 3.10 with
pandas 2.3.3 / pyreadstat 1.3.8. The R + `survey` 4.1-1 pairing is also installed on the
authorised compute box (R 4.1.2); the box was **not** used for microdata because DHS
restricted data must stay local.

All hashes are in `runs/2026-11-25_all/hashes.txt`. Unit-level normalized CSVs are
**local-only and not committed**.
