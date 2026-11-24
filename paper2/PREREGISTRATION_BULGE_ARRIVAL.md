# PRE-REGISTRATION — Bulge Arrival macro test (`t*` event study)

**Branch:** `research/bulge-arrival-2026-11-25` (additive; no push). **Record:** `paper2/` on that branch.
**Date:** 25 November 2026. **Author:** `paper2-outliner` (delegated lane; Lead: `lead`).
**Status: written BEFORE any estimation. No estimation was run for this record** (see §7: the data gate fails).

This is a pre-registration, not a results note. It fixes the `t*` definition, the sourcing rule, the estimand, the
estimator, the pre-trend/placebo/leave-one-out checks, and the falsifier **before** any number is computed. It also
records, up front, which inputs are **not available in-repo**, so the main specification is empty by rule rather
than by hindsight.

Language rule: **association only.** Permitted: "is followed by", "the estimate at event time e is". Forbidden:
"effect of abolition", "caused", "drives", "led to". Failures and nulls are reported, never dropped.

---

## 1. Purpose

The E8 fee-abolition event study centres on the **abolition year** `t_abolition`. The "bulge arrival" hypothesis
centres instead on the year the first post-abolition cohort reaches the **end of the primary cycle**:
`t* = t_abolition + L_primary`, where `L_primary` is the length of the primary cycle in years in that country at
that time. The question is descriptive: **at `t*`, does the final-grade primary bulge show up as repetition /
exam-gate queuing, and does the primary→secondary transition fall** (rationing the bulge at the next gate)?

This test reuses the E6/E8 evidence base (same 8 countries, same verified abolition dates, same estimator family)
and adds no new country sample.

---

## 2. Sourcing rule (binding)

Every input to `t*` must be traceable to a **real repo file at a named branch + commit**.

- `t_abolition` — sourced from `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` @
  `research/e6e8-sequencing-2026-11-25` (`2d19da7…`), column `preferred_year`, rows `status=VERIFIED`. (Blob
  `85d09f86…`, byte-identical to `research/records/2026-11-25-codex-source-verification/fee_dates.csv` @
  `9a0fd69…`.)
- `L_primary` — must come from a repo file that states primary-cycle length for that country/year. **If no such
  file exists, the input is `UNSOURCED` and the country is excluded from the main specification — the value is not
  estimated, inferred, or borrowed from the auditor.**
- No invented series, no invented `t*`, no "standard 6–8 years" fill-in. Auditor-supplied candidates are recorded
  only as *unadopted candidates* (§4).

---

## 3. The `t*` table as registered (main specification)

`t*` is registered as **UNSOURCED** for every country because `L_primary` has no in-repo source. The
`t_abolition` half is sourced for all eight. No row enters the main specification.

| # | ISO3 | country | t_abolition (sourced) | source file @ branch @ commit | L_primary | L_primary source | t* | main-spec status |
|---|---|---|---|---|---|---|---|---|
| 1 | MWI | Malawi | **1994** | `…/2026-11-25-e6e8-sequencing/data/fee_dates.csv` @ `research/e6e8-sequencing-2026-11-25` @ `2d19da7…` | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |
| 2 | ETH | Ethiopia | **1995** | same | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |
| 3 | UGA | Uganda | **1997** | same | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |
| 4 | LSO | Lesotho | **2000** | same | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |
| 5 | TZA | Tanzania | **2001** | same | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |
| 6 | KEN | Kenya | **2003** | same | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |
| 7 | MOZ | Mozambique | **2004** | same | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |
| 8 | GHA | Ghana | **2005** | same | **UNSOURCED** | none in repo | **UNSOURCED** | EXCLUDED |

Sourced `t_abolition`: **8 / 8**. Sourced `L_primary`: **0 / 8**. Sourced `t*`: **0 / 8**. Excluded from main
specification: **8 / 8**.

**Search performed for `L_primary` (negative result recorded):** all branch trees were scanned by path for
education-structure / primary-duration / compulsory-years / ISCED-mapping files. The only education-structure file
is `public/reference/east-asia-schools/source/systems.json` (a Hong-Kong/East-Asia city model with stage lags, no
sub-Saharan primary-cycle lengths). No repo file gives `L_primary` for MWI/ETH/UGA/LSO/TZA/KEN/MOZ/GHA.

---

## 4. Auditor candidates — recorded, NOT adopted

These were supplied as candidates to check, not to copy. They are **not** used for `t*` and do not enter any
specification until each `L_primary` is sourced to a repo file.

| ISO3 | auditor candidate | arithmetic | status |
|---|---|---|---|
| UGA | 7-year primary | 1997 + 7 = 2004 | UNSOURCED — not adopted |
| MWI | 8-year primary | 1994 + 8 = 2002 | UNSOURCED — not adopted |
| TZA | 7-year primary | 2001 + 7 = 2008 | UNSOURCED — not adopted |
| KEN | 8-year primary | 2003 + 8 = 2011 | UNSOURCED — not adopted |
| GHA | 6-year primary | 2005 + 6 = 2011 | UNSOURCED — not adopted |
| ETH, LSO, MOZ | (not supplied) | — | UNSOURCED — cannot check |

Note for the eventual sourcing pass: several SSA systems changed structure inside the window (e.g. Kenya moved from
8-4-4 toward CBC; Ghana's 6-3-3/6-3-4-4 reform), so `L_primary` should be **year-varying**, not a single constant per
country. A constant would itself be a modelling assumption and must be declared if ever used.

---

## 5. Estimand (registered before estimation)

**Primary outcome family at `t*`** (in priority order; each must be a committed, annual, country-level series):
1. **Final-grade primary repetition** — repetition rate in the last primary grade (preferred), or overall primary
   repetition rate as a labelled fallback.
2. **Primary→secondary transition** — progression/transition rate to secondary (a fall is the rationing signature).
3. **Exam-gate queuing** — candidates vs places at the primary/secondary gate (no standard cross-country annual
   series exists; see §7).

**Estimand.** For outcome `Y` and `t*` as registered,
`ATT(e) = E[ Y_i(t*+e) − Y_i(t*−1) | cohort i ] − E[ Y_c(t*+e) − Y_c(t*−1) | not-yet / never treated c ]`,
for event times `e ∈ {−5,…,+6}`, aggregated over cohorts with cohort-size weights. This is the **Callaway–Sant'Anna
attribution with universal base period `g−1` and not-yet-treated controls**, exactly the estimand already implemented
in the E8 record.

**Estimator (reuse, do not rebuild).** `research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py`
@ `research/e6e8-sequencing-2026-11-25` @ `bd782be…`:
- `att_cs(...)` — line 67 (CS ATT(g,t) + event-time aggregation),
- `twfe_event(...)` — line 123 (TWFE event study, country+year FE, comparison only),
- `boot_rep(...)` — line 152 (country-cluster bootstrap),
- data loaders `load_wdi_outcome` line 38, `load_fee_dates` line 49, `build_panel` line 54.
The UIS/WDI pipeline is the same file's WDI-CSV loader; no new estimator is written.

**Checks, all mandatory and all reported:**
- pre-trends at `e = −2, −3, −4` (and `−5` with its treated-`n` disclosed);
- placebo: `t*` shifted **6 years earlier** — the mean post estimate must be ≈0 for the result to be read;
- leave-one-country-out mean post range;
- **all nulls reported**, including event times with CIs spanning zero and any outcome for which the sign is
  unstable;
- the on-impact (`e=0`) estimate reported separately, never folded into the post mean.

**Decision rule (registered).** If pre-trends are flat at −2/−3/−4 and the placebo is ≈0, report "consistent with a
bulge arriving at `t*`"; otherwise report "not distinguishable from a pre-existing trend". No language stronger than
"consistent with".

---

## 6. Step-3 falsifier (registered before estimation)

**Question.** Does the bulge outcome at `t*` depend on whether **secondary seat capacity expanded ahead of `t*`** or
**stayed rationed**?

**Design.** Split the E8 countries into two pre-declared strata:
- **S1 expanded** — a committed secondary-capacity series shows capacity growth above its pre-abolition trend in the
  window `[t_abolition, t*]`;
- **S2 rationed** — capacity growth at or below the pre-abolition trend in that window.
Non-abolition SSA controls are assigned to the same strata by the same rule, applied at the matched `t*` of the
treated country they are compared with (or at the median treated `t*` for the pooled comparison — fixed here as the
median, so the choice is not made after seeing results).

**Estimand (falsifier).** `Delta = ATT_S1(e) − ATT_S2(e)` for the same outcome family and event times as §5. A
negative `Delta` on the transition outcome (bulge absorbed where capacity expanded; rationed where it did not) is the
falsifier's predicted direction. The threshold is: the difference is read only if the **same sign holds at every one
of e = +1,…,+4** and the bootstrap 95% CI for the post mean excludes zero; otherwise report "indistinguishable".

**Capacity measure.** Must be a committed, annual secondary-capacity or intake series (e.g. UIS intake rate,
secondary PTR, or an enrolment/capacity ratio). **If no such series is committed, the falsifier is
`NOT-ESTIMABLE`** and the exact missing series are named (§7).

---

## 7. Data gate (run BEFORE estimation) — registered outcome: **FAIL**

The gate was applied on 25 Nov 2026 by scanning every ref tree in the clone (`git ls-tree -r` across all
`refs/heads` and `refs/remotes`) for the required series. Result:

| required input | status | exact missing series / file |
|---|---|---|
| `L_primary` per country-year | **MISSING** | no education-structure/primary-duration file in any ref |
| final-grade primary repetition | **MISSING** | `SE.PRM.REPT.ZS` (WDI) and UIS repetition-by-grade: not committed anywhere |
| primary→secondary transition | **MISSING** | `SE.PRM.PRSL.ZS` (WDI "progression to secondary") / UIS transition rate: not committed anywhere |
| exam-gate queuing | **MISSING** | no cross-country annual series exists in the standard sources; national exam data not in repo |
| secondary seat capacity / intake | **MISSING** | no UIS intake/PTR/capacity series for the SSA sample; no `SE.SEC.*` capacity file in any ref |
| WDI outcome CSVs for E8 (`SE.PRM.ENRR`, `SE.SEC.ENRR`) | **MISSING from record** | E8's own raw outcome zips are absent from the record; `scripts/download_data.sh` referenced by `REPORT.md` §5 does not exist at `bd782be` |

**Registered consequence.** Because the gate fails, the main specification and the falsifier are **NOT-ESTIMABLE**;
**no estimation was run**. This is the pre-registered outcome, not a post-hoc excuse: the gate rule was fixed before
looking for data. See `BULGE_ARRIVAL_STATUS.md` for the status report and the exact re-entry conditions.

**Re-entry conditions (all required).** Commit (a) a year-varying `L_primary` source with country/year coverage for
the 8; (b) at least one repetition and one transition series with annual SSA coverage around 1990–2016; (c) a
secondary-capacity/intake series; (d) the raw E8 outcome inputs and a download script, hashed. Then this
pre-registration can be executed unchanged.

---

## 8. Relation to Paper #2

This test is an **extension**, not a pillar. Paper #2's evidence base remains E6 and E8 only (see `OUTLINE.md`). If
the bulge test later becomes estimable, it would enter Paper #2 as a labelled secondary analysis with the same
association-only language, and it must not be blended into the E8 abolition event study's post-period estimates.
