> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# BRIEF 007 — COUNTRY-EVIDENCE-DRIVEN EXPERIMENT SLATE (iteration 5)

- **sent by / date:** lead, 2026-11-20 ~13:27 Asia/Shanghai (task-18; role change from results audit to experiment
  design).
- **purpose:** read the country evidence and propose what to run next — a slate of 6–8 experiments for iteration 5,
  each changing a structural model variable, with data requirement, arms, estimand, threshold, cost, and type.
- **informs:** iteration-5 workstreams and the paper's next-round framing.

## 1. Artifacts read (on disk, this session)

`02_lit/COUNTRY_CARDS/{PHL,KHM,HKG,CHN,KOR,JPN}.md`; `02_lit/SHADOW_TARGETS.csv` (21 rows, 11 YES);
`02_lit/MODEL_CARDS.md` (Yoo/other model cards, read in earlier cycles); `04_data/TARGETS_SHADOW.csv`,
`TARGETS_FLOW.csv`, `ECONOMY_SERIES.csv` (4,031 rows, 1995–2024), `TARGETS_README.md`;
`04_data/shadow_round2/SHADOW_DATA.md` + `data/shadow_incidence_round2.csv` (38 rows) +
`data/shadow_fees_round2.csv` (20 rows); `05_experiments/loop2/{CALIBRATION_TABLE.csv, findings_ledger.txt,
freeze_both.csv, balance_checks.csv}`; `05b_experiments/loop2/` (two-way module, brief 005); `05b_experiments/loop3/`
(S1–S3, stop rule); `05b_experiments/loop4/{PRE_DECLARATIONS_L4.md, runs/U1, runs/U1b, runs/U2, runs/U3}`;
`06_report/RESEARCH_LOOP.md`.

**PENDING layer:** `09_relations/` exists but is **empty at intake** (RELATION_CANDIDATES.csv, DATA_PATTERNS.md,
MODEL_PLUG_MAP.md not yet written). Each proposed experiment below carries a **relation slot: PENDING
(09_relations)** and a design-intent type (causal / plausibly-causal / correlational); the slate will be re-ranked
when the relation layer lands. No relation id is invented.

## 2. New country evidence (verified)

- **Korea — HIGH, official.** MODS/KEDI 2023: participation by level **86.0 elementary / 75.4 middle / 66.4 high**
  (all 78.5); hours 7.5/7.4/6.7 (all 7.3 h/wk); monthly spend per student 398/449/491k won (all 434k), per participant
  462/596/740k (all 553k); provider spend mix hagwon 241 / 1:1 37 / group 22 / internet 16 (thousand won, general
  subjects); income gradient 183k (<3m won) vs 671k (≥8m won); purposes makeup 49.6%, advance 24.0%, next-level prep
  14.2%. Fees reach official tables; **2011 "90%" not traceable** and stays an assumption.
- **Hong Kong — 2003 anchor, MEDIUM-HIGH.** Bray & Kwok 2003 (6-school quota sample, n=630, 1998/99): S1-3 **35.1**,
  S4-5 **46.6**, S6-7 **70.3**, all **48.8**; commercial mass-lecture classes 72.4% (S6-7) and 33.0% (S4-5);
  multi-provider 12.3/29.4/19.8; fees: 28.1% pay >HK$1,000/month, 8.5% >HK$2,000, fees 1.1–5.0% of household income;
  modal 6–10 h/month. 1996/2010 surveys stay LOW (authors: "not statistically robust"); 2010 senior 85% remains the
  single calibration moment.
- **Japan — HIGH for grade 6 (prefecture table), MEDIUM for 2007 national.** Grade-6 juku mean **41.8%**, prefecture
  range **22.1 (Akita) – 57.9 (Tokyo)**; 2007 national primary 26%, lower-secondary 53%; grades 1–4 math 15.0%.
  Fees **unresolved** (MEXT/e-Stat blocked in this environment).
- **China — MEDIUM 2014, LOW post-2021.** 29.8% of primary+lower-secondary students received tutoring in 2014
  (Liu & Bray 2020, ERIC abstract); post-Double-Reduction ">80% did not attend off-campus subject tutoring" (China
  Education Daily 2022-03-03, headline only; **not a rate**). No provider split; CFPS/CEPS credentialed.
- **Cambodia — case study only.** One district, six schools, 444 students: grade-6 **60.5% urban / 26.4% rural**;
  grade-9 Khmer 52% urban / 39% rural (after excluding NGO-funded); dominant provider **Rien Kuo** (government
  teachers teaching their own students in school buildings); fees 500–1,000 Riel/session (US$0.13–0.25).
- **Philippines — incidence BLOCKED.** PSA 403 on every path; data.gov.ph no CKAN API; PIDS JS-only; no APIS/FIES/LFS
  tutoring item. One 2010 select-sample survey (46.5% all basic) remains MEDIUM for the aggregate only. Cohort/economy
  targets exist: UIS 2024 completion primary 98.3 / lower-sec 92.4 / upper-sec 75.0; out-of-school 12.8%.
- **Cohort/economy and calibration artifacts now exist** (`05_experiments/loop2`): fit/hold MAE table (e.g. PH
  tertiary held-out 16.5 pp), balance checks pass exactly (B1/B2/B3 = 0), but the ledger's long-run path collapses
  (PH upper-sec 0.741→0.431 and degree 0.184→0.000 at +40y; KHM similar) — an anomaly, not a finding.

## 3. Loop-4 results that constrain iteration 5 (read from disk)

| cell | result |
|---|---|
| U1 KOR fee test | fee block **PASS** (per-participant 13.5% inside 10.5–18.5%; per-student 10.6% inside 9.5–16%); **by-level participation ordering FAILS** (model E71.9<M78.9<H88.0 rising; official falls 86.0>75.4>66.4); provider mix: commercial 82.9% of demand vs observed hagwon 55.5% of spend; hours UNABLE (no hours object) |
| U1b HKG OOS | **FAIL**: monotone shape holds (Spearman 1.0) but levels off by +16.8/+12.1 pp at S1-3/S4-5; provider ordering inverted (model commercial S6-7 22.3% vs S4-5 100.0%; observed 72.4% vs 33.0%); fee/income 5.19% outside 1.1–5.0% |
| U2 recovery/forced-ID | **NEGATIVE**: recovery 0.50 (<0.67), forced-ID 0.30 (placebo) / 0.50 (no placebo) — no mechanism claim from the module |
| U3 holdout | **PH FAIL** (held-out MAE 14.68 vs naive 5.70); **KHM PASS** (1.84 vs naive 6.80) |
| U4 verdict | not yet on disk — PENDING |

## 4. Questions for the panel (1–5 from task-18)

1. What does each country profile actually support (evidence / assumption / calibration vs check vs demonstration)?
2. Propose 6–8 iteration-5 experiments, each with country/stage, model variable changed, economic mechanism in words,
   exact data series (or "new data needed"), arms, estimand, decision threshold, cost, and type.
3. Rank by identification value and feasibility.
4. Data-first list the profiles imply but data cannot support yet.
5. The ONE experiment if only one were possible.

## 5. Rules carried in

Use only on-disk artifacts; mark absent layers `UNABLE TO ASSESS`; every data need cites a series or says "not
available"; no fabricated numbers; relation layer PENDING (09_relations) — cite the slot, not an invented id. The
scout's country typology (when it lands) supplies the "only in certain types of countries" dimension.
