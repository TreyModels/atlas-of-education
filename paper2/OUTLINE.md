# Paper #2 — "Massification Before Industrialization" — evidence-annotated outline

Working outline for drafting, 25 Nov 2026. Compiler: `paper2-outliner`. This is an **outline + evidence
packet**, not a draft and not new empirical work. Every number below was either read from the committed file
named, or recomputed from that file in this session (recomputations are marked *recomputed*).

**One-line honest framing for the paper.** On pre-1990 structural-change series, the schooling take-off is the
larger strict ordering against the demand take-off, but demand-first is neither eliminated nor cleanly ordered,
and the orderings are threshold- and series-sensitive; separately, fee abolition in eight sub-Saharan African
countries with page-located dates is followed by large primary-enrolment gains in a staggered-adoption event
study. The paper is an **ordering / association** paper, not a causal one.

---

## 0. Scope, ref convention, and what this paper may not contain

**Ref convention.** Repo clone: `/Users/treymenefee/neon-boot/repos/atlas` (clean clone, `--filter=blob:none`).
Its `main` working tree was found empty (1,108 staged deletions left by another process) and was **not touched**;
all evidence was read with `git show <commit>:<path>` plumbing. Branch names below are the `origin/<name>` refs of
that clone; commits are full-anchored SHAs (abbreviated in text, full in `CLAIMS.csv`).

**Evidence base = the two auditor-cleared pillars only.**
- **E6** — pre-1990 demand-timing record: `research/records/2026-11-25-e6e8-sequencing/` @
  `research/e6e8-sequencing-2026-11-25`
  (results at `2d19da7`, errata at `bd782be`).
- **E8** — fee-abolition event study with dates verified to page/box locators: same record, plus the
  independent source-verification record `research/records/2026-11-25-codex-source-verification/fee_dates.csv` @
  `research/codex-source-verification-2026-11-25` (`9a0fd69`; file introduced at `bfb8c6f`; blob
  `85d09f86…` identical at both).
- **Shared provenance / errata**: the E6/E8 record's `ERRATUM.md` (`bd782be`) and `PRE_REGISTRATION.md`
  (`a2a116d`); data-tier and input-hash tables in the same record.

**Explicitly out of scope** (they belong to other, non-cleared records and must not be imported as evidence):
Paper M's horse race and supply/demand decomposition (`supply-demand @ 963e5e5`), the historical case typology
(`historical-sequence @ ab658c7` — all dates UNVERIFIED literature standard), the agricultural-floor model
(`subsistence @ 41f6429`), scaling/credential/care sections, the N1 sequencing paper (`paper-sequencing-novel @
62c27a3`), and **any simulation or illustrative output**. This paper cites none of them as evidence.

**Hard language rules.** No "effect of", "caused", "drives", "led to". Permitted: "is followed by", "consistent
with", "the ordering is", "the association is". Simulation results are never cited as empirical evidence.

**Known title risk.** "Massification" in the evidence is dated by a **reconstructed mean-years-of-schooling
take-off**, not by secondary/tertiary enrolment threshold crossings, and "industrialization" is proxied by
**non-agricultural employment / urbanisation / value-added shares**, not manufacturing. The title therefore
over-promises relative to E6 as run. Options: (a) retitle to the ordering claim ("Schooling before structural
change…"); (b) keep the title and add a §3/§12 paragraph that states both measurement substitutions — and add the
two analyses listed in `GAPS.md` §4–5. This is a Lead/user decision, flagged, not silently resolved.

---

## 1. Introduction — the demand-led default and the timing prediction

**Claim.** The human-capital account predicts that labour-market demand turns on before school systems expand;
the institutionalist/world-polity account predicts the reverse is possible. The paper tests the **order** of
documented take-offs, not the direction of a correlation and not a causal mechanism.

**Evidence.** No new data for §1. Framing constraints from the E6/E8 `PRE_REGISTRATION.md` (purpose and frame;
"descriptive/'consistent with'; no causal claim") @ `a2a116d`; the retraction of the 7% figure is recorded in the
record's `REPORT.md` §0 and in `ERRATUM.md` (`bd782be`) — the 1991-start wage-employment series manufactures it
(Codex F02/F12).

**Figure/table.** None (text only).

**Known weakness.** The demand-led prediction is stated at the level of theory; the paper cannot adjudicate
between mechanisms, only orderings. Do not let the introduction promise a test of "why".

---

## 2. Prior art and the contribution

**Claim.** The ordering pattern is not new in direction (Sandberg 1979; world-polity school; economic-history
case narratives); the contribution claimed here is **systematic measurement with pre-registered definitions**,
not precedence.

**Evidence.** `research/records/2026-11-25-codex-source-verification/README.md` @ `9a0fd69`, Job 3 tables
(Q1 list of eight works with DOI status); `research/records/2026-11-25-paper-massification/claims-prior-art.md`
@ `fb9f419` (seven claim groups, "new vs replicated" column). Both are *records about* references, not the
references themselves.

**Figure/table.** Table: prior-art map (claim → closest works → DOI status → what remains).

**Known weakness.** DOI statuses were verified by that record, not re-verified here; the source-verification
record's own commit message says "24 DOI-verified" while its tables mark **21 V / 2 U / 1 W**, and that record
now carries a metadata erratum (`ea6bc61`). Treat all DOIs as **NEEDS-RECHECK** before submission.

---

## 3. Data and measurement — three evidence tiers

**Claim.** Every series is labelled OBSERVED / RECONSTRUCTED / IMPUTED, and the labels travel with every table.

**Evidence.** `REPORT.md` §0 and `results/e6_inputs_and_hashes.csv` @ `2d19da7`:
- GGDC 10-Sector Database, employment by sector, 42 countries, 1947–2012 — **OBSERVED** (harmonised;
  GGDC reconstructs missing intermediates). Actual downloaded file `10sd_jan15_2014.zip`, sha256 `061a0767…`,
  extracted dta sha256 `7447311a…`.
- WDI urbanisation `SP.URB.TOTL.IN.ZS` (1960+), industry VA `NV.IND.TOTL.ZS` (1960+), agricultural VA
  `NV.AGR.TOTL.ZS` (1960+) — **OBSERVED**; WDI agricultural employment `SL.AGR.EMPL.ZS` starts 1991 — labelled
  **RECONSTRUCTED/modelled** and used only as sensitivity.
- Long-run panel mean years of schooling (5-year grid, 1870–2020), `long_run_panel.csv` sha256 `cd30d7ea…`,
  committed at `research/records/2026-11-24-next-tests/data/long_run_panel.csv` —
  **RECONSTRUCTED** (historical reconstruction).
- PWT 10.01 (`pwt1001.dta`, sha256 `746a4836…`) — **OBSERVED**, used for context only; **no sectoral employment
  split**, so it cannot date a structural take-off (stated, not forced).
- E8 outcome: WDI primary GER `SE.PRM.ENRR` — **OBSERVED**; WDI secondary GER `SE.SEC.ENRR` — labelled **proxy**
  for the requested lower-secondary GER (WDI publishes no annual lower-secondary GER).

**Figure/table.** Table 1 (data-tier/provenance table: series, label, source URL, sha256, coverage). Must be in
the main text, not appendix, because the reconstructed schooling series is the single largest interpretive risk.

**Known weakness.** (i) The schooling series is a reconstruction; E6's ordering is only as good as it. (ii) The
raw GGDC/PWT/WDI zips are **not committed** — only URLs + sha256 (acceptable, but reproduction needs network and
the exact release). (iii) The pre-registration names GGDC release `10sd_2023` while the downloaded and hashed zip
is the **2014** release (`10sd_jan15_2014.zip`) — a vintage mismatch to reconcile before quoting (§0 of REPORT
already names 2014; prereg does not). (iv) E8's outcome WDI files are **not in the input-hash table at all**
(see §8 and `GAPS.md` §3).

---

## 4. Strategy — take-off dating (E6) and treatment timing (E8)

**Claim (E6).** Demand take-off = first year `y` in the series with `s(y+10) − s(y) ≥ +3.0 pp` (agricultural VA
uses `≤ −3.0` because it falls); schooling take-off = first 5-year-grid year with `schooling(y+10) − schooling(y)
≥ +1.0`. A take-off equal to a series' first observable year is **left-censored** and classified as *demand-first,
weakly*; it is never called reverse. Primary comparison window **1900–2012** (full overlap) — a documented
deviation from the pre-registered 1960–2010, made because the 1960 window selects against pre-1960 demand
take-offs.

**Claim (E8).** Staggered-adoption event study: Callaway–Sant'Anna with universal base `g−1` and not-yet-treated
controls (never-treated allowed), event time −5..+6, cohort-size-aggregated, country-cluster bootstrap (500);
TWFE event study (country + year FE, binned endpoints, cluster by country) as comparison. Pre-trends at −2/−3.
Sensitivity: dates ±1, leave-one-country-out, placebo dates 6 years earlier, all-12 set.

**Evidence.** `PRE_REGISTRATION.md` @ `a2a116d` (definitions/windows/thresholds fixed before analysis);
`scripts/e6_demand_timing.py` and `scripts/e8_fee_event_study.py` @ `bd782be`; the estimator code is in the record
(`att_cs`, `twfe_event`, `boot_rep` in `e8_fee_event_study.py`, lines ~80–190) — reusable machinery for the bulge
test, see `PREREGISTRATION_BULGE_ARRIVAL.md`.

**Figure/table.** Table: definitions, windows, thresholds, and the documented deviation, with the pre-registered
alternative.

**Known weakness.** The window deviation is post-hoc and must be presented as a deviation, not as the plan.
Threshold choices are defended only by the N3 sweep (§6), which shows they matter.

---

## 5. E6 results — the ordering on pre-1990 series

**Claim.** On the full-overlap window, demand take-off precedes schooling take-off in **10.0–24.1% of
identifiable countries** (by proxy): GGDC non-agricultural employment **10.0% (2/20 identifiable; 30 in-window)**;
urbanisation **15.4% (10/65)**; industry VA **24.1% (13/54)**; agricultural VA **18.8% (9/48)**. All four are
below the pre-registered one-third threshold. Over **all** countries with both series the bounds are
**6.7–53.0%**. Another **21–43% of in-window countries** are weak ties or left-censored.

**Evidence.** `results/e6_summary.csv` and `results/e6_summary.json` @ `2d19da7` (rows `window=1900-2012`);
country-level dates and classification in `results/e6_classification.csv`; selection in `e6_selection.csv`.
*Recomputed in-session from `e6_summary.csv`:* demand-first 10.00–24.07%; bounds min 6.7, max 53.0;
weak/in-window 21.05–43.33% — all match the file.

**Figure/table.** **Fig 1** — demand-first share by proxy, 4 points with identifiable `n` labels and all-country
bound whiskers (source: `e6_summary.csv`). **Fig 2** — composition per proxy (forward / reverse / weak tie /
undetermined), stacked bars (source: `e6_classification.csv`). **Table 2** — the four full-overlap rows with
`n_all`, `n_in_window`, counts, and both denominators.

**Known weakness.** The "identifiable" denominator excludes undetermined countries; the gap between 10–24%
(identifiable) and 6.7–53.0% (bounds over all) is the honest uncertainty, and reviewers will attack whichever
denominator the abstract uses. Never quote a bare percentage without the denominator and the weak-tie category.

---

## 6. Robustness — thresholds, smoothing, and left-censoring (N3)

**Claim.** The ordering is **threshold- and smoothing-sensitive** and cannot be quoted as a single number.
Across **54 committed definitions** (all with `n ≥ 20`), the strict demand-first share ranges **0.0–30.8%,
median 10.45%**. The q1 default (Δ_s = 1.0, Δ_r = 3.0 pp, no smoothing, n = 34) gives **6.2% demand-first /
70.6% weak tie / 17.6% schooling-first / 5.9% undetermined**, all-country bounds **5.9–82.4%**. Left-truncated
survival dating changes the dates but not the qualitative picture.

**Evidence.** `results/n3_table.csv`, `results/n3_recommendation.json` @ `2d19da7`; `scripts/n3_threshold_survival.py`
@ `bd782be`. *Recomputed in-session:* 54 definitions; strict range 0.0–30.8, median 10.45; q1 row exactly
6.2/81.2/5.9/82.4 as committed.

**Figure/table.** **Fig 3** — 54 definitions sorted by strict demand-first share, q1 default annotated, threshold
and smoothing shown. **Table 3** — q1 default row + range summary + the "100% of definitions below the 75%
forward threshold" statement.

**Known weakness.** The 3/5/7-year schooling smoothing windows collapse on the 5-year grid (documented, not
faked). Ties dominate. The record's own prose range "weak forward-or-tie 56–84%" **does not reproduce** — the
reproducible quantities are **56.67–88.46% of identifiable countries** and **50.00–82.14% of all countries**
(ERRATUM §C). Use the corrected wording.

---

## 7. What the ordering does and does not establish (country variation)

**Claim.** The pattern is heterogeneous and the paper should show it: schooling-first is the **larger strict
ordering in all four proxies — 21.5–46.3% of identifiable countries against 10.0–24.1% demand-first, and
58.3–71.4% of strict orderings** — but it is **not a majority of identifiable countries** (maximum 46.3%). It is
a majority only among strict orderings. The remainder is weak ties or undetermined.

**Evidence.** ERRATUM §A and `results/erratum_check.json` @ `bd782be`; recomputed in-session from
`e6_summary.csv` (school-first/identifiable 21.54–46.30; strict 58.33–71.43). Named country examples from
`e6_classification.csv` (full-overlap, GGDC proxy; *read, not recomputed*): **CHN** schooling onset 1930 vs
demand onset 1962; **PHL** 1945 vs 1972; **BOL** demand 1958 vs schooling 1965; **IND** demand 1976 vs schooling
1980. These are illustration rows, not a case sample.

**Figure/table.** **Table 4** — 6–8 illustrative countries with both onset years, the classification label, and
the `series_first_year` flag (so left-censored cases are visible). Optional small map/heat strip.

**Known weakness.** Country examples are selected from a reconstructed schooling series and a 42-country GGDC
panel; they illustrate, they do not generalise. **Do not** carry Paper M's Prussia/Britain/France/US narrative
here: those dates are UNVERIFIED literature standard and come from a different, non-cleared record.

---

## 8. E8 design — eight page-located fee-abolition dates

**Claim.** Main specification uses the **8 dates verified to named page/box/quotes** in two 2009 World
Bank/UNICEF volumes: **MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005**. Four
dates (**CMR, ZMB, RWA, BDI**) are **UNRESOLVED** and excluded from the main specification, entering only the
all-12 sensitivity. Conflict resolutions: Ghana→2005 (national scale-up; 1997 is not a national abolition),
Ethiopia→1995 (implementation; 1994 = policy adoption), Tanzania→2001 (PEDP launch), Malawi→1994 (elimination),
Mozambique→2004 (abolition), Cameroon unresolved.

**Evidence.** `data/fee_dates.csv` @ `2d19da7` (blob `85d09f86…`; byte-identical to the source-verification copy at
`9a0fd69` and to the paper copy at `fb9f419`); `README.md` Job 1 @ `9a0fd69` (quote + page/box locators for every
row). *Recomputed in-session:* 12 rows, 8 VERIFIED / 4 UNRESOLVED; preferred years exactly as listed.

**Figure/table.** **Table 5** — the date-provenance table: country, preferred year, alternative year, status,
source + page/box, quote locator, conflict-resolution note. This table is the paper's single most checkable asset.

**Known weakness.** "Primary-verified" is the project's label; in strict terms each date is **quoted in a 2009
World Bank/UNICEF compilation at a named page/box**, and no underlying ministry decree, *arrêté*, or Education Act
was retrieved. For a strict primary-source standard, all eight are **NEEDS-RECHECK** (see `GAPS.md` §2). The four
unresolved countries must not be quietly dropped — report them and say why.

---

## 9. E8 results — the event study

**Claim (primary outcome, WDI primary GER, verified-8).** CS post-period ATTs (points): **+1: 23.82
[2.05, 45.60]; +2: 25.94 [4.48, 47.40]; +3: 22.12 [5.62, 38.62]; +4: 25.19 [8.54, 41.84]; +5: 28.56
[9.61, 47.51]; +6: 25.92 [8.64, 43.20]** — i.e. roughly **+22 to +29 points**. The **on-impact (+0) estimate is
+12.44 [−2.36, 27.24] and its CI includes zero**. Pre-trends at **−2/+−3/−4 are flat** (−0.03 [−3.43, 3.38];
−0.13 [−7.23, 6.98]; 1.35 [−6.35, 9.04]); the **−5** estimate is **6.39 [−0.08, 12.86] on only 6 treated
cohorts** — weak evidence of a pre-trend at the earliest horizon, reported, not hidden. TWFE post estimates are
similar (21.05–27.65). **Placebo (−6 years): −0.39.** Leave-one-out mean-post: **18.17–26.16**. All-12-dates:
**20.80**; all dates +1: **12.31**; all dates −1: **18.65**. Control countries per event: **28–30** for the
verified-8 table (25–30 is the all-12 sensitivity). Seven treated countries have outcome data (one verified
country lacks primary-GER coverage), 6 at the −5/+3/+5 horizons.

**Claim (secondary GER proxy).** Post ATTs **+6.71 [−3.39, 16.82] at +5** and **+6.07 [−0.01, 12.16] at +6**;
pre-trends flat; **every CI includes zero** — report as a **proxy with no clear detected effect**, not as a null.

**Evidence.** `results/e8_results.json`, `results/e8_event_SE.PRM.ENRR_verified8.csv`,
`results/e8_event_SE.SEC.ENRR_verified8.csv`, `results/e8_sensitivity.csv`, `results/e8_att_gt_SE.PRM.ENRR_verified8.csv`
@ `2d19da7`; cross-checked by `scripts/verify_revision_numbers.py` → `data/revision_verification.json` (41/41
checks) @ `fb9f419`. *Recomputed in-session from the committed CSVs:* post range 22.12–28.56; on-impact CI
spans zero; −2/−3/−4 flat; −5 as stated; placebo −0.39; LOO 18.17–26.16; n_controls 28–30; secondary CIs include
zero — all match.

**Figure/table.** **Fig 4** — event-study plot, CS ATT ± 95% CI with TWFE overlay, verified-8, primary GER.
**Fig 5** — sensitivity dot plot (all+1, all−1, all-12, LOO range, placebo). **Table 6** — full event table.
**Fig 6 (optional)** — secondary-GER proxy event study, clearly labelled "proxy; CIs include zero".

**Known weakness.** 7–8 treated countries; wide CIs; on-impact zero; earliest pre-trend imprecise; **no causal
identification**. The paper must use "is followed by", "consistent with a supply-side expansion", never "effect
of abolition". The record's own stale ranges ("mean post 18–29", "25–30 controls") **do not reproduce** — use
12.3–26.2 and 28–30 (ERRATUM §D).

---

## 10. Joint synthesis — what the two pillars together support

**Claim.** The two cleared pillars support one bounded statement: **schooling and structural change move
together, with schooling typically — but not universally, and not cleanly — first on pre-1990 series**, and one
supply-side policy family (fee abolition) is followed by large primary-enrolment gains in the eight dated SSA
cases. Neither pillar identifies a mechanism or a causal direction.

**Evidence.** Synthesis only of §5–§9 numbers; no new file. Suggested wording is in the E6/E8 record's
`REPORT.md` §3 recommendation and ERRATUM §A corrected wording. The `e8` "consistent with" language is the
strongest permitted claim.

**Figure/table.** **Fig 7 (optional, conceptual)** — a two-panel "what each pillar can and cannot say" diagram;
must be labelled schematic (not data).

**Known weakness.** The temptation to merge E6's demand-ordering with the N1 schooling-vs-fertility ordering.
**The two orderings must never be merged** (Council/Codex F14; ERRATUM §E "Effect on the papers"). This paper
reports only the E6 ordering.

---

## 11. Known negatives and errata ledger (must survive editing)

**Claim.** The paper must carry a short, explicit "what we know is false or unresolved" box. At minimum:

1. **The 7% labour-demand figure is retracted** — a 1991-start series artefact (Codex F02/F12); not re-derived,
   not defended, not used.
2. **"18–33% strict schooling-first" does not reproduce** from `e6_summary.json`; the reproducible range is
   **21.5–46.3% of identifiable countries** (58.3–71.4% of strict orderings), and "majority" must read "larger
   strict ordering" (ERRATUM §A).
3. **"56–84% weak forward-or-tie" does not reproduce**; use **56.67–88.46% of identifiable countries**
   (50.00–82.14% of all countries) (ERRATUM §C).
4. **"25–30 control countries"** is the all-12 sensitivity; the verified-8 table has **28–30** (ERRATUM §D.1).
5. **"Mean post 18–29 points" does not reproduce**; the reproducible range is **12.3–26.2** across ±1-year and
   LOO checks, against **−0.39** under the placebo; verified-8 post mean is 25.26 (ERRATUM §D.2).
6. **Four fee dates unresolved** (CMR, ZMB, RWA, BDI); excluded from main, flagged in sensitivity.
7. **No pre-1900 data** for the classic cases; the E6 head series start 1947/1950/1960 and the schooling panel
   1870 — a "before industrialization" claim about Britain/Prussia cannot be tested on these series.
8. **PWT has no sectoral employment split** — it cannot date a structural take-off.
9. **−5 pre-trend imprecise** (6 cohorts) and **on-impact CI includes zero** in E8.

**Evidence.** `ERRATUM.md` and `results/erratum_check*.json` @ `bd782be`; `REPORT.md` §0 @ `2d19da7`.
*Recomputed:* at least the 21.5–46.3 / 56.67–88.46 / 12.3–26.2 quantities were checked against the committed
files in-session.

**Figure/table.** **Table 7 (errata ledger)** — number, where it appeared, what reproduces, what to quote instead.

**Known weakness.** Prose errata multiply; a reviewer who finds one stale range loses trust in all. Keep the
ledger in the main text, not buried.

---

## 12. Limitations and referee objections

**Claim.** Pre-empt the four strongest objections: (i) the schooling series is reconstructed; (ii) the take-off
thresholds and window are choices, and the ordering is sensitive to them; (iii) the E8 treated sample is 7–8
countries with wide CIs and a zero on-impact estimate; (iv) "industrialization" is proxied, and "massification"
is a schooling-stock take-off, not enrolment massification.

**Evidence.** `REPORT.md` §4 "Deviations, limits, and what cannot be said" @ `2d19da7`; `GAPS.md` here.

**Figure/table.** None.

**Known weakness.** Several of these are not fixable inside the current data (see `GAPS.md` §4–6); say so.

---

## 13. Conclusion

**Claim.** Restate the bounded finding and the two-pillar structure; no new number; explicitly list the two
analyses that would change the verdict (manufacturing-only onset; secondary/tertiary enrolment-threshold
crossings).

**Evidence.** Synthesis only.

**Figure/table.** None.

**Known weakness.** Do not let the conclusion's rhythm imply causation.

---

## Appendices

- **App A — Evidence labels and data tiers** (from `REPORT.md` §0; includes the PWT non-use and the 2014/2023
  GGDC vintage mismatch).
- **App B — Reproduction and provenance** (`scripts/`, input hashes, the missing `download_data.sh` and missing
  E8 outcome files — see `GAPS.md` §3).
- **App C — Data gaps** (copy of `GAPS.md` §4–6).

---

## Figure/table manifest (what drafting must produce)

| id | name | data file | commit | status |
|---|---|---|---|---|
| Fig 1 | demand-first share by proxy + bounds | `e6_summary.csv` | `2d19da7` | data ready |
| Fig 2 | classification composition per proxy | `e6_classification.csv` | `2d19da7` | data ready |
| Fig 3 | N3 54-definition threshold sweep | `n3_table.csv` | `2d19da7` | data ready |
| Fig 4 | E8 event study, primary GER, verified-8 | `e8_event_SE.PRM.ENRR_verified8.csv` | `2d19da7` | data ready |
| Fig 5 | E8 sensitivity dot plot | `e8_sensitivity.csv` | `2d19da7` | data ready |
| Fig 6 | E8 secondary-GER proxy (optional) | `e8_event_SE.SEC.ENRR_verified8.csv` | `2d19da7` | data ready, label proxy |
| Table 1 | data-tier/provenance | `e6_inputs_and_hashes.csv` | `2d19da7` | needs E8 outcome rows added (missing) |
| Table 2 | E6 full-overlap summary | `e6_summary.csv` | `2d19da7` | data ready |
| Table 3 | N3 q1 default + ranges | `n3_table.csv`, `n3_recommendation.json` | `2d19da7` | data ready |
| Table 4 | illustrative countries | `e6_classification.csv` | `2d19da7` | data ready |
| Table 5 | fee-date provenance (8+4) | `fee_dates.csv` | `2d19da7` / `9a0fd69` | data ready |
| Table 6 | E8 full event table | `e8_results.json` | `2d19da7` | data ready |
| Table 7 | errata ledger | `ERRATUM.md`, `erratum_check*.json` | `bd782be` | data ready |

No figure in this paper may use simulated or illustrative model output; all seven panels are from committed
observed/reconstructed data files above.
