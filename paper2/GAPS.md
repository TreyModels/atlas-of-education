# GAPS.md — what must be re-verified, and what needs new data, before Paper #2 can be quoted

Compiler: `paper2-outliner`, 25 Nov 2026. Every gap below names the file/commit that establishes it (or the absence
it records). Repo clone: `/Users/treymenefee/neon-boot/repos/atlas`; branch names are `origin/<name>` there.
"Paper #2" = *Massification Before Industrialization*, the two-pillar paper (E6 + E8) outlined in `OUTLINE.md`.

**Bottom line.** The two pillars' *numbers* are reproducible from committed output files and were partly
recomputed in this session. Three things are not yet quotable: (1) four stale prose ranges that must never be
copied; (2) the strict primary-source status of the 8 fee dates; (3) the raw-input chain for E8 (and the GGDC
vintage). Separately, the paper's **title-level claims** — "massification" as enrolment-threshold crossing and
"industrialization" as manufacturing — are not measured by E6 as run, and the pre-1900 classic cases cannot be
tested on these data at all.

---

## 1. Quotation bans — stale numbers that must never appear (highest priority)

These were found by the record's own prose-vs-data audit and are preserved in `ERRATUM.md` @
`research/e6e8-sequencing-2026-11-25` / `bd782be4d15c834f054b1ecc650e54565f6b292f`. A reviewer who finds one
stale range loses trust in all: treat this as a hard checklist.

| id | banned quote | where it appears | reproducible replacement |
|---|---|---|---|
| G1.1 | "18–33% strict schooling-first" | `REPORT.md` line 53 | **21.5–46.3%** of identifiable countries; **58.3–71.4%** of strict orderings |
| G1.2 | "majority strict ordering" (schooling-first) | `REPORT.md` §1 | "**larger** strict ordering" — it is a majority only among strict orderings, never of identifiable countries (max 46.3%) |
| G1.3 | "weak forward-or-tie 56–84%" | `REPORT.md` §3 | **56.67–88.46%** of identifiable countries; **50.00–82.14%** of all countries |
| G1.4 | "25–30 control countries per event" (main table) | `REPORT.md` §2 | **28–30** for verified-8; 25–30 is the all-12 sensitivity |
| G1.5 | "mean post 18–29 points" | `REPORT.md` §2 | **12.3–26.2** across ±1-year and LOO checks; placebo **−0.39**; verified-8 post mean **25.26** |

Recomputed in-session from `e6_summary.csv`, `n3_table.csv`, `e8_event_SE.PRM.ENRR_verified8.csv`,
`e8_sensitivity.csv`: all five replacements reproduce. The banned values do not.

**Status: BLOCKING for any external quote.** Fix: cite the replacements in `CLAIMS.csv` C08/C12/C26/C35/C36.

---

## 2. Fee dates — "primary-verified" needs a stricter standard

**What is actually verified.** Each of the 8 dates (MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003,
MOZ 2004, GHA 2005) is quoted at a named page/box in one of two 2009 World Bank/UNICEF volumes, with the quote
committed in `research/records/2026-11-25-codex-source-verification/README.md` @ `9a0fd69…`, and the machine-readable
table in `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` (blob `85d09f86…`, byte-identical at
`bfb8c6f`, `9a0fd69` and `fb9f419`).

**What is not verified.** No ministry decree, *arrêté*, Education Act, or gazette was retrieved for any of the
eight; the two 2009 volumes are authoritative **compilations**, not the primary instruments. The project's label
"primary-verified" should be read as "page-located in an authoritative compilation".

**Status: NEEDS-RECHECK for a strict primary-source standard.** Fix: retrieve and cite the underlying instrument
for each of the eight (or soften the paper's label and the abstract's wording to "verified to page locators in
World Bank/UNICEF (2009)"). This is a labelling/verification issue, not a claim that the dates are wrong.

**Related:** the 4 unresolved dates (**CMR** 1999/2000, **ZMB** 2002, **RWA** 2003, **BDI** 2005) must stay
UNRESOLVED and excluded from the main specification; the source record's own rule is "do not guess". The paper
must report them, not drop them silently.

---

## 3. Reproducibility of the two pillars — missing raw inputs

### 3.1 E8 outcome data are not committed
- `scripts/e8_fee_event_study.py` reads `data/wdi_SE.PRM.ENRR/` and `data/wdi_SE.SEC.ENRR/` (WDI CSV zips), and
  `data/wdi_SE.PRM.ENRR/Metadata_Country_*.csv` for the region filter.
- The record's `data/` directory contains **only `fee_dates.csv`**. There is **no `SE.PRM.ENRR` or `SE.SEC.ENRR`
  entry in `results/e6_inputs_and_hashes.csv`**.
- `REPORT.md` §5's reproduction recipe calls `bash scripts/download_data.sh`; **that script does not exist in the
  record** (`git cat-file -e …/scripts/download_data.sh` fails at head `bd782be`).

**Status: NEEDS-RECHECK.** Fix: re-pull the WDI outcome zips, commit them (or their sha256 + a committed download
script), and re-run E8 end-to-end; then compare to `results/e8_results.json`. Until then E8 is
"results-verified, pipeline-unreproducible".

### 3.2 GGDC vintage mismatch
- `PRE_REGISTRATION.md` names GGDC release **`10sd_2023`**.
- The downloaded/hashed archive is **`10sd_jan15_2014.zip`** (sha256 `061a0767…`); `REPORT.md` §0 names the 2014
  10-Sector Database.
- **Status: NEEDS-RECHECK.** Fix: state the authoritative vintage (2014 release is what was hashed and run) and
  confirm E6 results are recomputed on that release; if the 2023 successor is wanted, fetch and hash it and re-run.

### 3.3 E6 inputs are external but hashed; two inputs live on other branches
- GGDC zip, PWT 10.01 dta, and the four WDI zips are external downloads with sha256 in
  `results/e6_inputs_and_hashes.csv` — acceptable provenance, but reproduction needs network and exact releases.
- `long_run_panel.csv` (sha256 `cd30d7ea…`) is committed at `research/records/2026-11-24-next-tests/data/` @
  `research/assessment-and-next-experiments-2026-11-24`; `event_dates.csv` at
  `research/records/2026-11-25-paper-sequencing-novel/results/` @ `research/paper-sequencing-novel-2026-11-25`.
  Both paths and hashes check out, but they are cross-branch dependencies the Paper #2 record must cite explicitly.
- **Status: VERIFIED provenance, with a cross-branch dependency note.** Fix: add both paths + commits to App B.

### 3.4 Data vintages / revisions not tested
WDI rewrites history; `SE.PRM.ENRR` revisions after the 24–25 Nov 2026 pull could move the E8 event table. There is
no vintage-robustness check in the E6/E8 record (the E1 record documents exactly this risk for its own panel: a
later WDI pull moved pooled t-stats by up to 3.97e-5). **Status: NEEDS-RECHECK.** Fix: pull a second WDI vintage and
report the event-table delta, or state the vintage in the table note.

---

## 4. Framing gap 1 — "massification" is a schooling-stock take-off, not enrolment-threshold crossing

**What E6 measures.** Schooling take-off = first 5-year-grid year with `mean years of schooling(y+10) − (y) ≥ +1.0`,
from the **reconstructed** long-run panel (`REPORT.md` §1; `PRE_REGISTRATION.md` "Schooling take-off rule"). The
demand side is non-agricultural employment share, urbanisation, industry VA, agricultural VA.

**What the title implies.** That secondary/tertiary **enrolment** crossed mass-education thresholds before
industrialisation. **No committed file dates secondary or tertiary enrolment threshold crossings.** The only
enrolment outcomes in the record are E8's WDI primary GER (and secondary GER as a labelled proxy). See `CLAIMS.csv`
C14 (UNSUPPORTED).

**Status: UNSUPPORTED as framed.** Two acceptable fixes: (a) retitle to the ordering claim (e.g. "Schooling before
structural change…") and keep the mean-years measure; or (b) add a new analysis with long secondary/tertiary GER
series and explicit crossing thresholds — new data, see §6.

---

## 5. Framing gap 2 — "industrialization" is proxied, and manufacturing is never dated

**What E6 measures.** Demand take-off from (i) GGDC **non-agricultural** employment share (= 1 − AGR/SUM), (ii)
urbanisation, (iii) industry VA share (includes mining/utilities/construction), (iv) agricultural VA share. None of
these is a **manufacturing employment share**.

**What would be needed.** The GGDC 10-Sector database does publish manufacturing separately; a manufacturing-only
onset (same +3 pp/10y rule) is a straightforward new analysis on the **same committed input**. Until it is run, the
paper must say "structural change", not "industrialization", in the claims — or run it. See `CLAIMS.csv` C03/C14.

**Status: NEEDS-RECHECK / new analysis.** Fix: add manufacturing-only onset as a robustness row (data already
hashed, so this is a re-analysis, not new data).

---

## 6. Pre-1900 and the classic cases — cannot be tested on these data

The E6 head series start in **1947/1950 (GGDC), 1950 (PWT), 1960 (WDI)**, and the schooling panel in **1870 on a
5-year grid**. Britain's 1870 Education Act vs the industrial revolution, and Prussia's 1763 compulsory-schooling
edict, are therefore outside the measurable range; the project's historical case record
(`research/historical-sequence-2026-11-23` @ `ab658c7`) explicitly labels **every historical date UNVERIFIED
literature standard** and is not one of the two cleared pillars.

**Status: UNSUPPORTED inside Paper #2.** Fix: state the pre-1900 limitation in §12 and do **not** import the
Prussia/Britain/France/US narrative from Paper M; if a historical section is wanted it needs its own source
verification (date-by-date, page references) before it can be quoted.

---

## 7. Bulge-arrival test (added lane) — NOT-ESTIMABLE on current data

The Lead's "Bulge Arrival" macro test needs `t* = t_abolition + L_primary` and outcome series around `t*`. Both
halves are blocked:

1. **`L_primary` (primary-cycle length) has no in-repo source.** Searched every branch tree for
   education-structure / primary-duration files: none. (The only education-structure file is
   `public/reference/east-asia-schools/source/systems.json`, East-Asian city model, no SSA primary lengths.) So all
   8 `t*` values are **UNSOURCED**; the auditor's candidate lengths must not be adopted. See
   `CLAIMS.csv` C43 and `PREREGISTRATION_BULGE_ARRIVAL.md`.
2. **No repetition / exam-gate / transition / seat-capacity series.** Tree scan across all refs finds no
   `SE.PRM.REPT` (repetition), no `SE.PRM.PRSL` (progression to secondary), no UIS repetition-by-grade or
   transition series, and no secondary seat-capacity / intake-ratio series. See `CLAIMS.csv` C44 and
   `BULGE_ARRIVAL_STATUS.md`.

**Status: NOT-ESTIMABLE** (two independent blockers). The Callaway–Sant'Anna machinery is reusable
(`scripts/e8_fee_event_study.py`: `att_cs`, `twfe_event`, `boot_rep` @ `bd782be`), so this becomes runnable the
moment the inputs below exist. This is a data gap, not an analysis gap.

---

## 8. What would need new data (exact series)

For the paper as titled:
1. **Long secondary GER and tertiary GER series** with consistent definitions and pre-1990 coverage (WDI/UIS;
   `SE.SEC.ENRR`, `SE.TER.ENRR`) — to date enrolment-threshold crossings. **NEW DATA.**
2. **Manufacturing employment share**, GGDC 10-Sector — already in the hashed archive; **re-analysis, not new
   data.**
3. **Complete raw E8 inputs** — WDI `SE.PRM.ENRR` + `SE.SEC.ENRR` zips + region metadata + `download_data.sh`;
   **restore/commit** (currently absent).
4. **Primary-cycle length by country and year** (`L_primary`) — UNESCO/ISCED mappings or national education acts;
   **NEW DATA**, with a year-varying source because several SSA systems changed structure (e.g. Kenya's 8-4-4 to
   CBC; Ghana's 6-3-3/6-3-4-4) inside the window. Needed for the bulge test.
5. **Final-grade primary repetition** (WDI `SE.PRM.REPT.ZS` and/or UIS repetition by grade),
   **primary→secondary transition/progression** (WDI `SE.PRM.PRSL.ZS` or UIS transition rate), and
   **secondary seat capacity / intake ratio** (UIS; e.g. intake rate, PTR, or enrolment-capacity series) — **NEW
   DATA**, for the bulge event study and its falsifier.
6. **Exam-gate queuing** — no cross-country annual series exists in the standard sources; would require national
   examination results (candidates/passes/places) for the 8 countries. **NEW DATA, likely manual collection.**
7. **The four unresolved fee dates** — ministry *arrêté*/decree or gazette for CMR, ZMB, RWA, BDI. **NEW
   SOURCES.**
8. **Underlying primary instruments for the 8 verified dates** (see §2). **NEW SOURCES.**
9. **A second WDI vintage** for revision robustness (§3.4). **NEW PULL.**

---

## 9. Sign-off checklist before Paper #2 is quoted externally

| # | item | blocker? | evidence |
|---|---|---|---|
| 1 | No banned stale range appears anywhere (§1) | **yes** | `ERRATUM.md` @ `bd782be`; recomputations |
| 2 | Fee-date label either upgraded to primary instruments or softened (§2) | **yes** | `README.md` @ `9a0fd69` |
| 3 | E8 raw inputs + download script committed and re-run reproduces `e8_results.json` (§3.1) | **yes** | absent from record tree |
| 4 | GGDC vintage stated and reconciled (§3.2) | yes | `e6_inputs_and_hashes.csv` vs `PRE_REGISTRATION.md` |
| 5 | Title/abstract either retitled or two new analyses added (§4–5) | **yes** | no enrolment-threshold or manufacturing-once file |
| 6 | Pre-1900 limitation stated; no Paper M historical narrative imported (§6) | yes | `ab658c7` (UNVERIFIED dates) |
| 7 | DOIs re-verified in this paper's own Crossref pass (§2 of OUTLINE) | no (submission) | `claims-prior-art.md` @ `fb9f419`; `ea6bc61` metadata erratum |
| 8 | Bulge-arrival analysis reported NOT-ESTIMABLE with named missing series (§7) | yes | `BULGE_ARRIVAL_STATUS.md` |

**Not a gap:** the four error-corrected E6/E8 result files are internally consistent. Two independent cross-checks
exist and pass: the record's own `erratum_check*.json` (recomputed here) and Paper M's
`scripts/verify_revision_numbers.py` → `data/revision_verification.json` (41/41 checks, 0 fail) @ `fb9f419…`.
