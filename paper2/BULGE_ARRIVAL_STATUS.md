# BULGE ARRIVAL — status report (event study, falsifier, auditor-number verification)

**Branch:** `research/bulge-arrival-2026-11-25` (additive, no push). **Record:** `paper2/`.
**Date:** 25 November 2026. **Author:** `paper2-outliner`. **Pre-registration:** `PREREGISTRATION_BULGE_ARRIVAL.md`
(written and written down before any estimation).
**No estimation was run.** No server/GPU was used, no power/shutdown command was issued, no series was invented.

---

## A. `t*` sourcing — summary

| item | count | notes |
|---|---|---|
| E8 countries | 8 | MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA |
| `t_abolition` sourced | **8 / 8** | `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` @ `research/e6e8-sequencing-2026-11-25` @ `2d19da7…` (blob `85d09f86…`, identical at `9a0fd69…`) |
| `L_primary` sourced | **0 / 8** | no education-structure / primary-duration file in any ref |
| `t*` sourced | **0 / 8** | therefore excluded from the main specification by the pre-registered rule |
| auditor candidates checked | 5 of 8 | UGA 2004, MWI 2002, TZA 2008, KEN 2011, GHA 2011 — all **UNSOURCED, not adopted** (ETH/LSO/MOZ not supplied) |

Full table in `PREREGISTRATION_BULGE_ARRIVAL.md` §3–4.

---

## B. Macro event study centred on `t*` — **NOT-ESTIMABLE**

**Machinery exists and is reusable (located, not rebuilt).**
`research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py` @
`research/e6e8-sequencing-2026-11-25` @ `bd782be4d15c834f054b1ecc650e54565f6b292f`:
- `att_cs(...)` line 67 — Callaway–Sant'Anna ATT(g,t), universal base `g−1`, not-yet-treated controls, event-time
  aggregation;
- `twfe_event(...)` line 123 — TWFE event study (comparison only);
- `boot_rep(...)` line 152 — country-cluster bootstrap;
- `load_wdi_outcome` line 38 / `load_fee_dates` line 49 / `build_panel` line 54 — the WDI/UIS pipeline.
The pre-registered estimand is exactly what this file already computes, with `g = t*` instead of `g = t_abolition`.

**Why it cannot be run.** Two independent blockers:
1. **`t*` is UNSOURCED for all 8 countries** (`L_primary` missing) — there is no treatment date to centre the event
   study on.
2. **The outcome series do not exist in the repo.** Tree-scan across every `refs/heads` and `refs/remotes` tip
   found **no committed series** for:
   - final-grade (or overall) **primary repetition** — WDI `SE.PRM.REPT.ZS` / UIS repetition-by-grade: **none**;
   - **primary→secondary transition / progression** — WDI `SE.PRM.PRSL.ZS`: **none**; UIS transition rate: **none**;
   - **exam-gate queuing** — no cross-country annual series exists in standard sources, and no national exam data
     in repo;
   - the E8 **raw outcome inputs** (`SE.PRM.ENRR`, `SE.SEC.ENRR` WDI zips) are also absent from the record, and
     `scripts/download_data.sh` (cited by `REPORT.md` §5) does not exist at `bd782be`.

**Pre-trend test / placebo / leave-one-out: cannot be computed** — they are properties of an estimate, and no
estimate exists. Reporting them as "flat"/"~0" would be fabrication. Registered consequence: **NOT-ESTIMABLE**.

**Re-entry:** commit a year-varying `L_primary` source, at least one repetition series and one transition series
with annual SSA coverage ~1990–2016, and the raw E8 outcome inputs + a download script (all hashed). The
pre-registration then executes unchanged.

---

## C. Step-3 falsifier (capacity-expanded vs rationed) — **NOT-ESTIMABLE**

**Estimand was specified before looking** (`PREREGISTRATION_BULGE_ARRIVAL.md` §6): the stratum difference
`Delta = ATT_S1(e) − ATT_S2(e)`, split by whether secondary seat capacity expanded ahead of `t*` or stayed
rationed, with a pre-declared sign/consistency rule.

**Exact missing series (why it cannot run):**
- no committed **secondary seat capacity / intake / PTR** series for the SSA sample (UIS intake rate, secondary
  PTR, or enrolment-capacity ratio: **none** in any ref);
- therefore the S1/S2 split cannot be constructed for treated countries **or** for non-abolition SSA controls;
- and the outcome side inherits the same missing repetition/transition series as §B.

**Verdict: NOT-ESTIMABLE.** No substitute proxy was used and no stratum was assigned by hand.

---

## D. Auditor-quoted numbers — checked against the repo (do not trust)

| # | auditor quote | source checked | recomputed from committed file | verdict |
|---|---|---|---|---|
| D1 | "**E6: massification 20–40 yrs before industrialisation in 76–90% of countries**" | `e6_summary.csv`/`.json` @ `2d19da7` | demand-first **10.0–24.1%** of identifiable countries; schooling-first **21.5–46.3%** identifiable / **58.3–71.4%** of strict orderings; leads are mostly single-digit years | **DOES NOT REPRODUCE in E6 (UNSUPPORTED).** The components of the quote trace to *other, non-cleared* records: **95.3% (61/64) with median 26 y** is the N1 schooling-vs-agricultural-release ordering (`paper-sequencing-novel` @ `62c27a3`), and **76%** is the supply-vs-schooling fair sample (`supply-demand` @ `963e5e5`). Neither is a "massification before industrialisation in 76–90%" figure. **Do not carry it into Paper #2.** |
| D2 | "**E8: +22–29 pp primary GER**" | `e8_event_SE.PRM.ENRR_verified8.csv` @ `2d19da7` | CS post ATTs: +23.82, +25.94, +22.12, +25.19, +28.56, +25.92 → **+22.12 to +28.56** | **REPRODUCES** as the post-period CS range (with T0 +12.44, CI `[-2.36, 27.24]` including zero, and sensitivity means 12.31–26.16). Quote only with those caveats. |
| D3 | "**E1 finds 0/0/0/32**" | `summary_by_R.json` @ `6a452a4…` (`research/e1-multiverse-1200-2026-11-25`) | conservative-family `certified_BY` at **R=1200**: up 0, down 0, flip 0, het **32** → **0/0/0/32**. At **R≤800: 0/0/0/0**. Under the **136-parity** convention: **25/15/0/39** | **REPRODUCES, but only as the conservative-family count at R=1200.** E1's own `ERRATUM.md` §A says the 136-parity "0/0/0" prose is wrong. Quote the convention and the draw budget explicitly, or the number is misleading. |

**Cross-cutting finding.** Of the three auditor numbers, one (E6 76–90%) is a **conflation across records** and must
not be used; one (E8 +22–29) is **right but needs its on-impact and sensitivity caveats**; one (E1 0/0/0/32) is
**right under one convention at one draw budget** and wrong/partial under the other. This reinforces the general
rule: quote only numbers that carry their file, field, denominator and convention.

---

## E. What was NOT done (explicit)

- No estimation of any kind was run for the bulge test (pre-registration gate failed first).
- No `t*` value, `L_primary` value, or outcome series was invented, interpolated, or borrowed from the auditor.
- No simulation output is cited anywhere in this record.
- The repo clone's working tree was not modified; there is no push.
- No server/GPU, no power or shutdown command.

---

## F. Three things the Lead should know (risk summary)

1. **The `t*` table cannot be populated from the repo as it stands** — the blocker is `L_primary` (education-system
   duration), which is a one-file data gap that a UNESCO/ISCED mapping could close. Until then the auditor's
   candidates must stay unadopted.
2. **The bulge *outcomes* are the harder blocker** — repetition, transition, exam-gate and seat-capacity series are
   absent from the repo and several are absent from standard cross-country sources in annual form. This test needs
   a data-acquisition task, not a compute task.
3. **The auditor's E6 quote is not an E6 number** — if it appears in any draft or briefing, it will be indefensible
   against the committed E6 files.
