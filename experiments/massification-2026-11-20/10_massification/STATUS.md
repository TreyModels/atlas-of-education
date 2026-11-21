# Handover status — massification-first phase

**Written:** 20 Nov 2026 ~14:12 Asia/Shanghai, by `lead-successor`, handing coordination to **`repo-auditor`** (Lead executor; bridge party `deepseek-audit`). `lead-fresh` was never provisioned (fleet member limit) — ignore that name in older drafts.
**Governance:** the **Synthetic Council of Experts is the authority** for research direction; the Lead executes,
coordinates, enforces the bridge protocol (`06_report/AGENT_PROTOCOL.md`) and may veto only on safety/evidence
grounds. **Shadow education is secondary**; the shadow close-out (`LOOP_CLOSEOUT.md`, brief 008) remains valid and
is not re-fit.

## 1. Workstreams (all claimed, in progress)

| task | owner | scope | status | artifacts on disk now |
|---|---|---|---|---|
| 34 | data-hunter | `10_massification/data/` | in progress | none yet (directory created; jobs/markets panel + ILO/OECD corpus + universalization series to land) |
| 35 | lit-archivist | `10_massification/lit/` | in progress | `MASSIFICATION_THEORY.md`, `PUSH_PULL.md`, `SCALING_LAWS.md`, `LABOUR_MARKET_REPORTS.md`, `PUSH_PULL_TARGETS.csv` |
| 36 | pattern-scout | `10_massification/relations/` | in progress | `scripts/fit_universalization.py`, `data/universalization_fits.csv`, `data/universalization_common_shape.csv` |
| 37 | experiment-runner | `10_massification/model/` | in progress, **GATED** | none yet (scaffold; must not fit until brief 013 criteria are final) |
| 38 | experiment-runner-2 | `10_massification/model2/` | in progress | `PRE_DECLARATIONS_M2.md`, `code/m2.py`, `runs/scaling_estimates.csv`, `runs/scaling_classification.csv` |
| 39 | expert-council | `08_council/brief_013/` | in progress (gate) | `BRIEF.md`, `EXPERTS.json`, `SUCCESS_CRITERIA.md`, `STOP_RULES.md` (synthesis pending) |

All six tasks were claimed by their owners after the reorientation brief. The Council's `SUCCESS_CRITERIA.md` and
`STOP_RULES.md` are the gate for task-37; the Council must post `COUNCIL:` with the final operational definition and
ranked slate.

## 2. Repository / delivery state

- **Checkpoint log:** content checkpoint **`493ebd7`** (20 Nov 2026 ~14:10) = lit/relations/model/model2 batches +
  governance + this STATUS executor fix. The branch tip may advance only by STATUS/README metadata commits; the
  **authoritative ZIP sha256 is in the adjacent `.sha256` file** (rebuild after any edit) and the current pair is
  announced in the `OP:` bridge post.


- **Last committed state:** branch `experiment/massification-2026-11-20`; the `lead-fresh` handover checkpoint was
  `80f50cc` (clean, ZIP `85137fad…45221`). The **massification-first checkpoint** that follows supersedes it: it
  commits the `10_massification/` batches (lit theory/push-pull/scaling, universalization fits, model2 scaling
  estimates, push-pull model scaffold + gate predeclarations, data raw payload), the governance files
  (`08_council/BIG_PICTURE_RULE.md`, `06_report/EXTERNAL_CHECKIN.md`, `AGENT_PROTOCOL.md` §7) and this STATUS file.
  **Authoritative tip = `git log -1` on the branch**; verify with `git -C 01_sources/atlas-main-55732f4 log --oneline -1`.
- **Zip:** rebuilt with this checkpoint; sha256 in the adjacent `.sha256` file (authoritative; not inside the ZIP).
- **Branch self-contained for external check-in:** `06_report/EXTERNAL_CHECKIN.md` is the entry point; the tip holds
  this STATUS file, `08_council/brief_013/` (current gate) and the commit/zip hashes in the `OP:` bridge post.
- **Site safety:** nothing under `main`/`src`/`public` touched; results only in
  `experiments/massification-2026-11-20/`.
- **Governance files:** `06_report/AGENT_PROTOCOL.md` (live), `08_council/DECISIONS.md` (D1–D5; Council owns from
  here), `CHANGELOG.md` (records the new first-order phase).

## 3. iCloud conflict copies — status

**None present at handover.** A full scan of the package and the git worktree found no `* N` conflict directories,
no "conflicted copy" names, and no `.icloud` placeholders. Actions taken:
- `git status --porcelain` in the worktree: **clean** (0 changed, 0 untracked).
- Canonical tree verified against `SHA256SUMS`: **724/724 OK**.
- The conflict directories the op centre flagged earlier were transient iCloud sync copies; they were cleared when
  the experimental folder was regenerated from the package stage (the packaging step deletes and recopies the
  folder each time).
- **Guard added** to `07_logs/package_delivery.py`: packaging and ZIP now skip any path matching ` <number>` /
  "conflicted copy" / `.icloud`, so conflict copies can never be committed or zipped again.
- **No ambiguous uncommitted paths:** the only uncommitted work at handover is the new `10_massification/`
  artifacts (listed in §1) plus the packaging guard and this STATUS file — all clean, all committed by this
  checkpoint. `07_logs/` is local-only (excluded from the experimental folder by design; included in the ZIP).

## 3b. Council gate amendment + critical path (20 Nov, D13–D16)

- **Amendment A1 (binding):** "reproduces universalization" = trajectory checks **and** classified scaling-exponent
  reproduction out of sample (secondary GER~income +0.286 (0.045); tertiary +0.776 (0.086); lower-sec completion
  logit law) with country-specific timing. Verdicts add **PASS-CONDITIONAL** (declared channel mixture) and
  **IDENTIFIED** (E1 or the predeclared E2+E3 pair). **R13:** no direction claims from cross-country/panel moments —
  report EQUIVALENT (model2 forced-ID 1.00). **R14:** scaling-exponent reproduction caps trajectory-only fits at
  PARTIAL. **R15:** conditional reproductions must be labelled.
- **Assignments (1-cycle deadlines):** exp2 → M2b (declared partial re-run vs landed relations data; resolve
  lower-sec coefficient +0.84 vs +1.174) + M2c (E1-design recovery test on simulated two-shock data, predeclared);
  exp1 → E2 (PH K-12 cohort exposure) + E3 (PH nurse-visa replication) predeclarations on observed `04_data` fallback;
  data-hunter → D16 one-cycle partial jobs/markets + completion/sector panel with hash, else **DATA BLOCKED** recorded;
  pattern-scout → `NEW:` for universalization fits with PAGE caveat, lead-lag labelled predictive-only, E6 constraint-only.
- **E1 kill trigger:** if E2/E3 and M2c are not executing within one cycle, the programme reduces to conditional
  reproduction + an equivalence result (Council step-back, `08_council/BIG_PICTURE.md`).

## 3c. Milestone log — first results after gate (20 Nov, 14:15)

**task-37 PHL smoke fit (experiment-runner; `model/calib/calibration_table.csv`, hash 13c93588…)**
- Fit window reduced to observed `status=target` rows only: fit 1999–2010 (n=16), holdout 2011–2024 (n=17).
- Rivals same window: demand-led fit 0.95 pp / holdout 4.84 pp; education-led 1.20 / 5.40; complementary 1.09 / 6.08.
- Naive benchmarks: persistence 8.60 pp; **linear trend 4.35 pp**. All three rivals lose to the linear-trend benchmark.
- **Verdict: PARTIAL, EQUIVALENT on completion moments (R13).** Levels clear §3 tolerance but no PASS; sector shares
  executed as CHECK-only (demand-led 19.96, education-led 2.47, complementary 12.77 pp) per §6 + Lead resolution.
- **A1 scaling check (`model/calib/scaling_check.csv`, hash a07077c4…): FAILED.** Generated OOS exponents are the
  wrong sign vs A1: secondary GER~income −1.89/−0.38/−0.74 vs target **+0.286**; tertiary −1.23/−0.14/−0.35 vs
  **+0.776**. Model does not generate the classified scaling law → R4 (supplied law) applies; universalization
  reproduction is at most PARTIAL. Logit completion slopes positive (+0.032/+0.040/+0.031). Proposed next fix:
  income-scaling channel as a predeclared structural change (not completion tuning).

**M2c — E1 estimator recovery (`model2/runs/m2c_*`; SIMULATED, predeclared M2C_PREREG.md before run)**
- DGP 30 provinces × 10y; γ ∈ {−0.30, 0, +0.30}; σ ∈ {0.5, 1.0}; 100 sims/cell; two-way FE OLS, CR1.
- σ=0.5: sign accuracy 0.93/0.92; median |bias| **0.55 > 0.50 predeclared**; 90% coverage 0.88; null FP 0.08.
- **Predeclared sufficiency rule FAILS on bias → E1 NOT SUFFICIENT as the identification gate; do not field E1.**
  High-noise stress (σ=1.0) sign accuracy falls to 0.74/0.68. Routed to Council for the R3/R13 reduction decision.

**M2b — declared partial re-run (`model2/runs/m2b_*`)**: lower-secondary completion coefficient resolved as an
**estimator range** (~+0.84 logit-between to ~+1.17 log-within), not a data error; Part-2 conclusions unchanged
(countries do not share a common slope; lead-lag not identifiable). No direction claim.

**Phase-1 predeclarations**: E2 `PRE_EXP_E2_PH_K12.md` (sha 14a007df…) and E3 `PRE_EXP_E3_PH_NURSES.md`
(sha 8708015c…) delivered, brief-013 §2–§4 + A1 copied verbatim, `04_data` fallback declared. **E3 is DATA BLOCKED**
for replication: no PRC/CHED nursing series on disk (simulated elasticity may be reported, labelled simulated, never
as replication). E2 coverage is thin (~6–7 pre-reform completion points) with a declared DATA BLOCKED contingency.
Both await Council intake acceptance. M2c ran at 14:13, before `INTAKE_ACCEPTANCE.md` was registered at 14:40 —
Council retro-review requested.

**exp2 gate-ACK correction + M2b/M2c NEWs (bridge c41076dd, 86eb4133, 2be3e544, 8faca41e):** the first gate
file omitted SUCCESS_CRITERIA §2–§4 through a shell-extraction fault; corrected `GATE_ACK_BRIEF013.md` now carries
the full verbatim table + tolerances + A1 (sha256-16 **321a8cf8…**; supersedes 203d7e42…). M2b resolves the lower-sec
completion coefficient as an **estimator range** with transform/FE named (between-logit +0.84; all-year re-run +1.36;
year-FE log-log reimplementation +1.97/+2.28; scout relay +1.174 carried as their value) — data-adoption re-run
deferred by choice. M2c: R14/A1 sign is recoverable (0.92–0.93) but **size bias fails**; if E1 is ever used it must
be predeclared as **SIGN-identification only**, not size. Scout `SCALING_NOTES.md` landed; E6 bootstrap updated.

**Data (D16) satisfied**: `data/UNIVERSALIZATION_SERIES.csv` (2,458 rows) + `JOBS_AND_MARKETS_PANEL.csv` (5,622 rows,
39 series) + `DATA_NOTES_MASSIFICATION.md`, observed-only with derived/check flags; ILOSTAT/OECD/PSA/Enterprise
Surveys 403/000 recorded as DATA BLOCKED. Hygiene note: `data/SHA256SUMS.txt` is written as `hash size filename`
(not `shasum -c` parseable); hashes verified manually; regenerate in standard format next batch.

## 3d. Council loop-5 adjudication applied (D19–D30; Amendments A2–A3, R16–R18)

- **Phase headline is now CONDITIONAL REPRODUCTION + OBSERVATIONAL EQUIVALENCE** (D19): E1 is **killed as the
  identification gate as specified** (M2c: sign recoverable 0.92–0.93 but median size bias 0.55 > 0.50); panel/
  cross-country direction claims remain barred (R13). E1 is not killed forever: a redesigned E1 with a power fix +
  its own recovery test is permitted under a NEW predeclaration; sign-only E1 only if both shocks ever have observed
  data (D28). No direction claim has been posted.
- **task-37 smoke fit accepted PARTIAL/EQUIVALENT** (D20/R18); fit window 1999–2010 accepted as disclosed deviation
  (A2); sector shares CHECK-only.
- **A1 scaling failure confirmed; universalization capped at PARTIAL** (R14/R17). **Income-scaling channel repair
  APPROVED for predeclaration intake** as a new structural cell (named mechanism, no exponent as parameter, holdout
  untouched, exponents only as checks; D21). **Timebox: one cell / one cycle** — if it fails, publish PARTIAL +
  EQUIVALENT and park the rest (D26).
- **E2 accepted with a claim cap** (D23): descriptive association only unless ≥10 pre-reform observed points AND
  pre-trends pass; add COVID sensitivity + predecl amendment before running. **E3 DATA BLOCKED** for replication
  (D22): simulated elasticity only, labelled, never a replication; E2+E3 cannot identify direction → EQUIVALENT.
- **M2c retro-accepted** (D24/D27; gate ACK corrected 321a8cf8 verified). **M2b estimator range confirmed** (D29/A3).
  **Data D16 accepted**; M2 data-adoption re-run not ordered now (D30).
- **Slate re-rank:** E4 Bartik elevated to KEEP (next identification route after the income-channel cell); E5/E7
  PARK; E8/shadow KILL; T1/T2 papers PARK (D25).

## 3e. NEW USER DIRECTIVE — outcome is TIMING for near-universal systems (20 Nov ~15:00)

**Directive (user, via Lead):** Japan is probably near-universal already; the question is **when** that happened —
same for Korea and Hong Kong. For near-universal systems the outcome is the **timing of universalization**, not the
level.

- **Council action requested (Amendment A4 + slate re-rank):** add crossing-year tolerances (±N years) for
  JPN/KOR/HKG, make **levels check-only** for those three, keep fit/holdout roles for PHL/CHN/KHM unchanged, and
  re-rank the slate with timing as a first-class outcome. Pending A4, provisional tolerance is ±5 years (the existing
  midpoint tolerance) and crossing years are **never fitted**.
- **Data deliverable (data-hunter):** `10_massification/data/UNIVERSALIZATION_TIMING.csv` — crossing years
  (definitions documented: e.g. 50% / 90% / 95% cohort completion or equivalent by level) + uncertainty intervals,
  reconstructed from **headcounts/population** where UIS ratios are censored; observed-only; method + uncertainty
  + status per row; HKG/JPN have no UIS completion series and must be reconstructed or marked UNABLE (no imputation).
- **A4 CONFIRMED (Council D31–D37, 20 Nov 15:02/15:10; on disk `SUCCESS_CRITERIA.md` Amendment A4 +
  `UNIVERSALIZATION_MILESTONES.md`):** milestones **M0 massification ≥50%**, **M1** primary NER≥95 (or GER≥100),
  **M2** lower-sec completion ≥90, **M3** upper-sec completion/transition ≥90, **M4** tertiary GER ≥50; crossing year
  = first observed year at/above threshold, band = adjacent observed years; **N = ±5 y (±3 y where band ≤2 y)**;
  JPN/KOR/HKG levels **CHECK-ONLY ±5 pp**; crossing years are **HOLDOUT outcomes, never fitted** (R4/R5; R19 timing
  miss = structural miss); left-censored = boundary constraint, right-censored = false-positive test.
  **Censored-ratio rule:** reconstruct only from observed headcounts + documented population denominators, labelled
  **"reconstructed (not UIS)"**, with method/uncertainty + two-denominator sensitivity; never imputed as observation.
  **Slate re-ranked:** E6 timing comparison **#2**; **E9 crossing-year reconstruction #3** (data-hunter+scout);
  E4 #4; E2 #5; E1 #6 parked/unfielded; E3 #7 DATA BLOCKED; E5 #8; E7 #9; E8 KILL.
- **Lit/scout deliverable:** dated timelines (policy and attainment) for JPN/KOR/HKG, with sources and uncertainty.
- **task-37 timing check must be predeclared before its next run:** generated vs observed crossing years, per
  level/country, tolerance from Council A4 (±N y), timing **never fitted** (else R4/R5 supplied-law violation);
  the check is a HOLDOUT outcome, not a target.

## 3f. DESIGN PIVOT (user directive, 20 Nov ~15:20) — SINGLE-SYSTEM FIRST

**Directive:** (1) **single-system first** — stand up ONE education system (best data, actually massifies), show the
mechanisms, then test **portability to HKG and CHN**; (2) mechanisms to test, especially **state pushes** —
compulsory-education-law changes, **school/place expansion** (construction, teacher supply, pupil-teacher ratios),
**fee abolition** — against **demand-pull** (jobs/returns) and **supply-push** (cohorts); (3) researchers do **web
searches for baseline data** (UNESCO, World Bank, national) to answer synthetic-fitting questions; (4) **test
different researchers' models on the same system record**. The Council gate/acceptance rules and the Japan timing
directive (A4/R19) are retained.

**Board restructure (in progress):**
- **task-37 = anchor-system model** (mechanisms + calibration) with a **portability checkpoint to HKG/CHN**; the
  runner must NOT fit until the Council names the anchor system and single-system success criteria.
- **data-hunter** = web-search baseline data (compulsory-law dates, construction/places, teacher supply/pupil-teacher,
  fees/free-tuition, cohorts, jobs/returns; UNESCO/WB/national; retrieval log + sources) on top of the E9 timing file.
- **lit-archivist** = UNESCO/WB report layer + narrative of different researchers' models (world society, human
  capital, queue/credential, political economy/state-building, demographic) applied to the anchor system record.
- **pattern-scout** = event windows for compulsory-law/expansion/fee dates (anchor + HKG/CHN portability), with
  sources and uncertainty; E6 timing comparison remains #2.
- Council asked to **name the anchor system and single-system success criteria** before the fit; provisional
  candidate **Philippines** (best observed coverage on disk; actually massified; dated state pushes 2013 K-12 /
  2018 free tuition / 4Ps), alternatives Korea (near-universal timing, little mechanism room) and China (scale,
  weaker subnational data).

## 3g. Council A6 adopted — anchor signal is ASYMMETRY (D47–D49; A6; R23)

- **A6 milestone asymmetry (verified on disk):** PHL completion primary 83.16 (1999) → ≥90 in **2017** (91.92) →
  98.30 (2024); lower-secondary 58.86 → ≥90 in **2024** (92.41); upper-secondary 59.70 → 75.03 (2024) **never ≥90**;
  tertiary GER ≥50 in **2024–25**. The anchor model must reproduce **which milestone moved and when (ordering/gaps,
  ±5 y / ±3 y)**; a single universalization curve is **PARTIAL at most (R23)**; generating top-level universalization
  the record does not show is a **false-positive failure (R6)**. **Anchor fit 1999–2013, holdout 2014–2024**
  (supersedes the 1999–2010 smoke window for the anchor). Rivals are scored on ordering/gaps, not levels.
- **D48 rival testability split:** testable now (in order) world-society timing, state-building step,
  demographic/cohort contrast, formal-model shapes; **design-only** human capital (PSA returns by education) and
  signalling/MMI (Enterprise Surveys credential/skills module) — listed in every results file, never silently
  dropped, never modelled as if tested.
- **D49 report-layer rule:** anchor claims rest on observed on-disk evidence; blocked sources (OECD/ILO/PSA) are not
  load-bearing; UNREAD docs (BEPER 2019) must be retrieved from public sources before use; no citation of unread
  material.
- **Enforcement:** exp1 must fold A6 into the anchor predeclaration before fitting; exp2 runs the four testable
  rivals on the same PHL record/events with the two design-only rivals explicitly listed.

## 3h. DATA ASKS — AWAITING USER APPROVAL (do not send)

Two external requests are drafted and held; per protocol, external data requests need the user's approval and
**nothing has been sent**. Drafts: `06_report/access_requests/01_PSA_PHILIPPINES.md`,
`06_report/access_requests/03_WB_ENTERPRISE_SURVEYS.md`.
1. **PSA Philippines microdata** — FIES / APIS / LFS (returns by education, education expenditure, formal/informal
   transitions); the 403 route. Status: **AWAITING USER APPROVAL**.
2. **World Bank Enterprise Surveys credential/skills module** (PHL 2015/2023, KHM 2016) + establishment census.
   Status: **AWAITING USER APPROVAL**.
   Public retrieval is authorised: BEPER 2019 must be retrieved from public sources and logged before any citation
   (D49); the ILO/OECD/PSA 403s remain recorded as blocks. Op centre requested to surface both to the user.
3. **A9 state-capacity data asks** (Council A9/D59, queued only — nothing sent; user is away and asked for no
   op-centre updates beyond the queue): (a) **fiscal** — tax/GDP, government revenue/GDP, revenue volatility
   (education spending %GDP/%gov exp and per-student are observed/derived already); (b) **delivery** —
   schools/classrooms counts, procurement, subnational delivery series (PTR/teacher path observed; PIDS hires
   `check`/medium; school/classroom counts UNABLE); (c) **enforcement** — inspection/sanctions/attendance-enforcement
   indicators (compulsory age/duration are policy facts; 4Ps = weak B marker). Status: **AWAITING USER APPROVAL /
   queued; observed-only or DATA BLOCKED; never inferred from outcomes (R28)**.

## 3i. A7 adopted — timing alignment; anchor mechanism verdict is DESCRIPTIVE

- **A7/R24 — timing-alignment rule (adopted):** a state-push law counts as a mechanism only if its event window is
  computable on the affected level's observed series, the shift sign matches the prediction, the event-to-crossing
  gap is within ±5 y (or the crossing sits inside the post window), and affected cohorts are declared with transition
  cohorts excluded. Otherwise it is a **candidate marker/context, not a mechanism**. Evidence is descriptive (naive
  SE, no controls, quality A/B/C — R25): no causal claim (R13), never a model schedule (R4/R14).
- **Anchor mechanism verdict (descriptive, D51):** PHL's discrete state pushes **do not align** — 1987 Constitution →
  primary universal 2017–21 (**31 y later**); K-12 (effective 2016) → upper-secondary mass already **≤1999**;
  2018 free tuition → tertiary GER **−5.39 pp (t=−3.00, confounded)**; 4Ps negative. **The anchor's state-push channel
  is alignment-gated and may not be assumed** — justify by R24 alignment or drop/re-specify. The anchor target is the
  observed **crossing years and spacing** (A6: primary 2017, lower-secondary 2024, upper-secondary never by 2024,
  tertiary 2024–25). Aligned portability markers: HKG 2009 (+9.08, t=5.20), CHN 1999 (+4.70, t=7.94); CHN 1986
  (−27 y) and PHL 1987 (−31 y) are not markers; HKG lower-secondary NER 2015–16 is a measure artefact.
- **`SCHOOL_EXPANSION.csv` absent → DATA ASK** (D52): scout's four expansion episodes are quality-C inferred and
  **may not serve as event-window evidence (R25)**; data-hunter asked to pull the named file (DepEd/DPWH construction,
  teacher hires, pupil-teacher, SHS capacity) or mark DATA BLOCKED. Public retrieval authorised; external requests
  remain AWAITING USER APPROVAL (STATUS §3h).
- **Enforcement:** exp1 re-scopes `PRE_ANCHOR_A1.md` to A6/A7 (crossings+spacing target; state push alignment-gated
  or dropped) before its next run; exp2 re-scores the four testable rivals on crossing ordering/spacing and
  mechanism-implied ordering, listing the two design-only rivals in every results file.

## 3j. INCOME-SCALING REPAIR CELL — **FAILED** (D31 timebox; exp1 `calib/repair_*.csv`)

- The structural income-facing intake/continuation repair (D31-accepted cell) was run and **FAILED its predeclared
  gate**: generated OOS exponents remain wrong-sign and outside the A3 estimator range —
  secondary **−2.73 / −2.53 / −1.03** (A3 range +0.090…+0.215; A1 +0.286 ± 0.045), tertiary
  **−0.32 / −1.32 / −0.39** (A3 +0.567…+0.848; A1 +0.776 ± 0.086), lower-sec completion law **+11.46 / +1.87 /
  +2.55** (A3 +0.169…+0.247). `signs_ok` 1/3, `contained` 0/3, `within_1se_A1` false for all three rivals.
  PHL fit MAE 6.16–7.43 (worse than the 5 pp gate), holdout 4.80–6.26; CHN fit/holdout 7.03–8.83.
- **Consequence per Council timebox (D26/R14/R17):** the phase outcome stands at **conditional reproduction +
  observational equivalence**; universalization reproduction is capped at **PARTIAL**; the anchor (A1) may still be
  run for mechanism/crossing description but **cannot PASS the scaling criterion**, and no further scaling-repair
  iteration is to be attempted without a new Council decision. Unrepaired results retained alongside (R12).
  Routed to Council for formal adjudication under D26/D31.

## 3k. Council repair-failure ruling (D56–D58, R27; 20 Nov 16:15) — phase cap confirmed

- **Repair FAIL confirmed under the predeclared gate** (R14/R17/R1): generated OOS exponents remain wrong-sign and
  outside the A3 estimator range; `signs_ok` 1/3, contained 0/3, within-1se-A1 0/3; PHL fit MAE 6.16–7.43 (>5 pp),
  holdout 4.80–6.26 but loses to the linear-trend benchmark 4.35. **Timebox consequence confirmed:** the phase stands
  at **conditional reproduction + observational equivalence**; universalization reproduction is capped at **PARTIAL**;
  **no further scaling-repair iteration** without a new Council decision + new predeclaration + intake (R27: one cell).
- **Anchor A1 re-scoped (D57):** may run for **descriptive/mechanism-crossing reporting only** — A6 crossing
  years/spacing, A7/R24 event-window alignment, R26 capacity (level-specific), PIDS equity (check-only), A5 rivals.
  It must report the **scaling criterion as FAIL explicitly** and must not fit around it; verdict at most
  **PARTIAL/DESCRIPTIVE**; no PASS; no direction claim.
- **Publishable object updated (D58):** the failure is a **bounded negative result** — this cohort-flow model
  class/implementation cannot generate the observed positive income-scaling sign without an exogenous supply channel
  (0/3 contained across rivals; six added parameters did not rescue it; fit MAE >5 pp; holdout loses to linear trend).
  Publishable alongside the equivalence/identification map, caveated to this class/implementation; no positive model
  claim.

## 3l0. A5b final scoring (exp2, committed fcff06e) — equivalence set to the observed record is EMPTY
None of the four testable rivals reproduces PHL's observed milestone ordering/spacing (primary 2017, lower-secondary
2024, tertiary 2025, upper-secondary never ≥90 by 2024); pairwise equivalence only in the empty sense for
state-building vs demographic (both predict no crossing in holdout); world-society 2014 vs formal-shapes 2023 primary
crossings are distinguishable. **Phase verdict: EQUIVALENT + PARTIAL; the ceiling/asymmetry is unreproduced by this
rival field** (honest negative; no direction claim). Design-only rivals (HC, signalling/MMI) listed in every results
file as DATA BLOCKED.

## 3l. Council A9/R28/D59–D61 — STATE CAPACITY as third mechanism dimension (20 Nov 16:30)

- **A9 adopted:** the anchor's third mechanism dimension is **state capacity**, measured (not assumed) in three
  dimensions: **fiscal** (education spending %GDP / %gov exp observed; per-student derived; tax/GDP, revenue/GDP,
  volatility = DATA ASK), **delivery** (PTR/teacher path observed; PIDS hires `check`/medium; schools/classrooms/
  procurement = UNABLE/DATA ASK), **enforcement** (compulsory age/duration policy facts; inspection/sanctions/
  attendance enforcement NOT on disk = DATA ASK; 4Ps = weak B marker). Missing sub-dimensions are **excluded and
  labelled partial — never inferred from outcomes (R28)**.
- **Model entry (D60):** `effective_push_t = law_t · G(C_t)`, `G(C)=C^κ`, κ∈[0.5,1.0], weights predeclared with
  sensitivity; `C` is an **observed input trajectory**, never a target/fitted. Ladder: **law-only vs law×capacity**
  must be compared.
- **Capacity-alignment criterion (D61):** the model must reproduce A6 crossing years **given observed capacity**, and
  the capacity-gated spec must beat law-only on the crossings before PHL's state-push non-alignment is called a
  capacity-timing problem; otherwise **EQUIVALENT/FAIL, no capacity claim**. PHL evidence: PTR/teacher path
  37→27→24 / hires 2012–16 plausibly aligns with primary 2017 but **not** lower-secondary 2024 / tertiary 2024–25.
  Portability: capacity-response function fixed; capacity trajectories + minimum-capacity thresholds are declared
  country inputs (PHL/CHN/HKG differ); re-fit = FAIL (R20/R28).
- **New DATA ASKS (observed-only or DATA BLOCKED; external access needs user approval):** fiscal tax/revenue/volatility;
  delivery schools/classrooms/procurement; enforcement inspection/sanctions/attendance. Drafted/hold; route via op
  centre with the existing PSA and WB-ES asks (STATUS §3h). Nothing sent.

## 3m. Council A10/R29/D62–D64 — capacity buys the floor, not the ceiling

- **A10/R29 adopted:** the capacity channel is **level-specific and non-monotone** — a necessary delivery precondition
  for **floor** universalization, **not sufficient** for the **ceiling**. The model may not generate upper-secondary/
  tertiary universalization the record does not show (R6/R29); capacity effects may saturate by level; no tuning to
  rescue. Verified on disk: PHL spending 2.66→3.93 %GDP, secondary PTR 37.9→23.9, **ceiling 75.0 (never ≥90)**;
  HKG PTR 23.7→13.4, NER≥90 **1974** (≥95 1979); CHN PTR 22.9→16.4, lower-sec ≥90 only **2016**; KOR at ceiling.
- **Ceiling-residual test added to A1 descriptive scope (D63):** after law markers (A7), capacity (A9/A10) and observed
  demand inputs, predeclare and report the unexplained **ceiling residual** (PHL upper-secondary 75.0 vs 90; per level)
  with candidate accounts — foregone income/opportunity cost, demand/returns, gate structure/credential, enforcement;
  where no discriminating observable exists report **UNABLE**, never an explanation; no direction claim (R13).
- **Caveats (D64):** spending-%GDP and PTR are **crude proxies**; enforcement unmeasured everywhere; real per-pupil
  spending absent (DATA ASK); HKG crossings are threshold-specific (NER≥90 1974; NER≥95 1979).
- **Anchor A1 first run attempt FAILED (honest record):** `model/anchor.py` crashed with `KeyError: 'ger_primary'` at
  the crossing computation; `anchor_out/` is empty — **no anchor result exists yet**; exp1 is fixing and must add the
  A10 floor/ceiling split + predeclared residual decomposition before the re-run. No result claimed.

## 3n. CONTEXT_PRESSURE register (context-rotation plan; reviewed each checkpoint)

Plan: `06_report/CONTEXT_ROTATION_PLAN.md` (user request). Hard facts: durable teammate cap = 8 (9th spawn fails);
**subagents do not consume slots** (use `subagent` fresh for bounded rotation, never forklift a heavy window);
reassign a completed-role teammate as durable successor; spawn fresh durable only when a slot frees. Council
authority survives rotation because A/R/D rules + `INTAKE_ACCEPTANCE.md` are files. Every durable agent maintains
`10_massification/HANDOFF_<agent>.md` (≤1 screen: task, live artifacts + sha256-16, decisions, open ASKs, next 3
actions) and updates it on each delivered batch.

| agent | pressure signal | headroom estimate | planned replacement |
|---|---|---|---|
| experiment-runner (exp1) | continuous anchor/repair cycles; several failed-run retries (anchor KeyError); longest active window | low–medium | finish current atomic unit; subagent dispatcher for the anchor re-run if needed; durable successor only when a slot frees |
| experiment-runner-2 (exp2) | A5b/E6 delivered; still on A3 blocked + portability prep | medium | subagent for bounded portability cells; same slot if rotation needed |
| data-hunter | repeated web-search batches + acquisition attempts | medium | subagent for bounded public pulls; handoff = DATA_NOTES + SHA256SUMS |
| pattern-scout | timing/event layers delivered; audits stable | medium–high | subagent re-runs scripts from disk |
| lit-archivist | RIVAL_MODELS/STATE_CAPACITY/timelines delivered | high | **first candidate for reassignment** if a durable slot is needed |
| expert-council | **HIGH — rotating**: reports high window load; handoff `08_council/COUNCIL_STATE.md` mirrored to `10_massification/HANDOFF_expert-council.md`; D65 logged | low | **rotate at next checkpoint AFTER the anchor A1 descriptive report lands** → fresh-context subagent **council-2** (party `deepseek-council2`, brief `10_massification/COUNCIL2_BRIEF.md`); durable slots full; authority persists via files; Council-2 must ACK open NEWs (A5b equivalence-empty, A3 status, capacity data asks) |
| lead-successor (stood down) | light context, idle | high | **replacement candidate for Lead/executor role** |
| repo-auditor (Lead/executor) | long coordination window | watch | successor path: lead-successor reassignment or subagent dispatcher; state = STATUS + commit/zip chain |

Rotation log: no rotation has occurred yet. Council rotation is **scheduled** (after the A1 descriptive report).
Rotation rule: when a rotation happens, post `OP: rotation — <role> → <replacement>` with the handoff path and record
it in CHANGELOG. No rotation has occurred yet.

## 3o. Capacity layer landed + SERIES CORRECTION (scout NEW; data-hunter STATE_CAPACITY)

- **Capacity index built (scout `relations/data/state_capacity.csv` + `CAPACITY_LAYER.md`):** **1,182 country-years
  × 30 countries, 1971–2024**, declared weights; WGI **GE.EST blocked → index renormalised to 0.85 coverage** (partial
  index labelled, missing sub-dimensions excluded, never inferred — R28).
- **PHL within-country capacity path: 58.9 (2005) → 83.4 (2019) → 89.1 (2021)**, i.e. **+35.2 points into the primary
  ≥90 crossing (2017)** — consistent with capacity as a floor precondition (A9/A10), not a ceiling mechanism.
- **Cross-country capacity does NOT predict crossing timing:** Spearman **+0.15 / +0.10 / +0.41 / +0.30, all ns,
  n=5** → country-specific alignment, **not a cross-country law** (no capacity claim; R28).
- **SERIES CORRECTION (binding):** the **"PTR 37→27→24"** figure is the **PIDS high-school (classroom-based) teacher
  ratio**, **not** WDI primary PTR (which runs **~32–35 then ~29–30**). Record both separately; **never splice them in
  any claim**; `SCHOOL_EXPANSION.csv` rows are the **high-school** ratio (data-hunter to mirror this distinction in
  `DATA_NOTES_MASSIFICATION.md`/`STATE_CAPACITY_NOTES.md`).
- **Anchor A1 status:** the crash fix **is applied** (`model/anchor.py` updated; run progressing in `model/anchor.log`:
  demand_led law_only fit 2.03 / hold 4.42, capacity_gated fit 1.85 / hold 4.51, crossings M0 1960, M1 1966, M2/M3
  None, M4 1960). **`anchor_out/` is still EMPTY → NO anchor result is claimed**; the partial log already indicates a
  timing miss (crossings ~1960/1966 vs observed primary 2017 / lower-sec 2024 / tertiary 2024–25) and that
  capacity-gated does **not** beat law-only on crossings (D61 alignment FAIL on this partial run). Final report must
  come from exp1 with `anchor_out/` populated + A10/R29 requirements in the predeclaration.
- **Council-2 intake list addition (for rotation after A1):** declared capacity gate (`K_t = capacity_index/100`
  observed; `base_cost × (1 + cap_cost(1−K_t))`; places gate; twoway φ), **validation rule** (must produce PHL
  crossings within ±5 y **without a fitted capacity coefficient**, else the gate FAILS), and weight/κ sensitivities.

## 3p. Capacity data RECONCILED (executor adjudication; `data/CAPACITY_RECONCILIATION.md`)

- **Two files, canonical split:** data-hunter `data/STATE_CAPACITY.csv` (1,799 rows: fiscal 611 / delivery 509 /
  enforcement 679; statuses observed/policy_fact/check/unable) is **canonical for the three dimensions**; scout
  `relations/data/state_capacity.csv` (1,182 country-years × 30 countries, 1971–2024) is **canonical for the declared
  composite index only, labelled DERIVED**, with `weight_coverage`/weights metadata. Models take fiscal/delivery/
  enforcement **separately**; no collapsed index may carry a capacity claim.
- **tax/GDP discrepancy resolved:** scout includes `tax_gdp` (weight 0.20) from WDI `GC.TAX.TOTL.GD.ZS` with
  provenance columns (PHL 11.9/13.0/13.6 for 2005/2015/2017); data-hunter's `GC.*` pull failed (api HTTP 000) and is
  `unable`. Resolution: tax enters the index **only with scout's WDI provenance, never spliced** with blocked rows;
  data-hunter retries `GC.*` next batch; if provenance cannot be verified the component is dropped and weights
  renormalised.
- **WGI governance 0.15 blocked in BOTH files** → not proxied; index renormalises over the remaining **0.85**
  coverage; governance/enforcement is a declared assumption (R28).
- **De jure ≠ de facto (binding):** UIS compulsory years (PHL 12) vs delivery (PHL 110,954 missing classrooms;
  ≥1:50 congestion in 90% of NCR Northern Manila elementaries) vs enforcement (inspection/sanctions UNABLE) are
  three separate inputs in the anchor predeclaration — no collapse.
- **BEPER 2019 = DATA BLOCKED**, no citations (D49); schools/classrooms/procurement + attendance enforcement UNABLE.
  User-approval asks remain queued (nothing sent).
- **Anchor A1 status:** crash fix applied; run progressing in `model/anchor.log` (rival arms: demand_led law_only
  fit 2.03/hold 4.42; capacity_gated 1.85/4.51; education_led none 1.37/5.88; capacity_only 3.02/6.12; crossings
  ~1960s vs observed 2017/2024); **`anchor_out/` still empty → no result claimed**.

## 3q. ANCHOR CELL CLOSED — rotation executed; phase verdict recorded (D66–D78)

- **Rotation executed (2026-11-20 14:31 +08): expert-council → council-2** (fresh-context subagent, party
  `deepseek-council2`; handoff `08_council/COUNCIL_STATE.md` mirrored to `10_massification/HANDOFF_expert-council.md`,
  brief `10_massification/COUNCIL2_BRIEF.md`). Old Council stood down. **Authority persists via files** (A1–A10,
  R1–R29, D1–D78, `INTAKE_ACCEPTANCE.md`); Council-2 posted `COUNCIL: online`/intake ACKs; **`DECISIONS.md` D71–D78
  bind** (second pass; D66–D70 first pass kept); concurrent-instance precedence recorded in D78.
- **PHL anchor cell CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT (D76).** Remaining PHL-side work = **A1 addendum
  C1–C10 + the write-up only**. No new fit, repair, arm re-specification, rival re-score, capacity re-index or
  level re-fit without a new Council decision (R27).
- **Phase headline (exact, D77):** **"conditional *level* reproduction + observational equivalence + an
  unreproduced asymmetry"**. Barred phrasings: "reproduces universalization", "capacity explains the timing",
  "portability holds", any direction word (R13/R14/R17/R22/R28).
- **A1 verdict detail (Council-2 re-derived on disk):** M0 left-censored (≤1999); **M1 left-censored ≤1976/77**
  (primary NER 96.79 at 1976; GER≥100 1977 — report's ≤1999 was looser); **M2 lower-sec ≥90 in 2024** (92.41;
  2023 = 88.44); **M3 upper-sec never ≥90** (peak 76.43 2017; 75.03 2024); **M4 tertiary GER ≥50 first 2025**
  (51.07; 2024 = 47.41). Model: M0/M1 1960/1966 satisfy bounds but **earn no credit**; M2 no crossing in 9/12 arms
  (only education_led/gated 2025 within ±3; others late/far); M3 in-window R6 passes but **2/12 arms overshoot after
  2024** (2027/2031 = ceiling overshoot, R29); **M4 = 1960 is an initialisation artefact, not a 65-y miss** — the
  simulated tertiary GER is ≥50 at the first simulated year, so M4 is **not discriminable** and the tertiary-GER
  **level check is missing (C6)**. **A6 asymmetry not reproduced: 0/3 informative outcomes credited.**
- **Capacity:** capacity-gated **ties** law-only in 2/3 rivals (identical crossings); its one gain co-occurs with the
  M3 overshoot (not creditable); capacity_only worse → **capacity-timing hypothesis NOT supported → EQUIVALENT**
  (D61/R28). **A2d r = −0.427 at lag 6 is MODEL-INTERNAL descriptive-negative** (simulated series; max-|r| search
  outside the predeclared 2–4 window; observed capacity has only 3 points) — **not an empirical null about the
  Philippines** (D73/F6); folded into the A1 capacity section as exploratory.
- **Capacity ruling binding (D74):** `data/STATE_CAPACITY.csv` canonical for the **three dimensions**; scout composite
  canonical only as **DERIVED** (coverage 0.85); models keep `K_fiscal`/`K_delivery`/`K_enforcement` separate; no
  collapsed index may carry a capacity claim; tax/GDP only with scout WDI `GC.TAX` provenance, never spliced;
  de jure ≠ de facto; **enforcement-proxy-inside-G(C) double-count defect recorded as an OPEN MODEL DEFECT**.
- **Report defects to close in the addendum (C1–C10, D71–D73/D68):** C1 missing naive benchmarks (persistence/linear
  trend); C2 missing κ/weight sensitivity; C3 A10/R29 addendum is post-run (declare; predeclare residual next time);
  C4 findings text says `sigmoid` but code executes **G(C)=C^0.75** (fix text); C5 enforcement sub-index is a
  **de jure** proxy (label); C6 M4/tertiary-GER level check missing; C7 M1 censoring year ≤1976/77; plus F1 report
  the **primary completion ≥90 in 2017** crossing (83.16 1999 → 87.45 2013 → 91.92 2017); F2 classify M4 as
  **not discriminable** (not a 64-y miss); F6 relabel A2d model-internal.
- **Re-openers (only these, D76):** C1 correct-sign OOS generated exponents with no exponent as parameter
  (PASS-CONDITIONAL at best); C2 fixed-behaviour crossings within ±5 y on the corrected informative vector;
  C3 a discriminating push/pull/queue/capacity test (needs PSA/ES data); C4 observed annual capacity/enforcement
  making capacity measured.
- **Portability (A6 CHN / A7 HKG) PARKED-ARMED (D75):** design notes accepted as intake only; any later run needs a
  new Council decision + predecl under fixed-behaviour/declared-inputs (R20), no re-fit, HKG timing-only, CHN
  massifying; no portability claim now (R22).
- **Data queue HELD — nothing sent (user quiet mode):** PSA microdata; WB Enterprise Surveys; A9 fiscal/delivery/
  enforcement; annual classrooms; real per-pupil spending; GC.* verification; BEPER 2019; HKG/CHN/JPN/KOR historical
  timing series. All AWAITING USER APPROVAL / public-retrieval-with-log.
- **Current pair:** commit `3e3f705` (A1 descriptive report final + capacity reconciliation); this closure checkpoint
  supersedes it; ZIP hash in the adjacent `.sha256` and the OP post. Branch worktree is `01_sources/atlas-main-55732f4`
  (the package root is not the git repo; `3e3f705` contains `10_massification/model/anchor_out/anchor_table.csv`,
  `findings.txt`, `run_meta.json`).

## 3r. INCIDENT 2026-11-20 ~14:40–14:50 (+08) — iCloud file-loss during checkpoint; remote restored

**What happened:** during the anchor-closure checkpoint the iCloud-synced package began losing files (directories emptied:
`08_council/brief_013` → 3 files, `10_massification/model2/runs` → 0, `02_lit`/`04_data` partial; git worktree showed 855
tracked files deleted; reads failed with "file truncated"/"No such file"; git index operations timed out). A checkpoint
commit (`fabe4cf`) was created against an incomplete stage and **deleted 282 tracked files** (sha256SUMS −894 lines,
several scripts). That commit was pushed, then **reverted on the remote by force-push to the last good commit
`3e3f705`**; local branch ref restored to `3e3f705` as well (worktree may be inconsistent until a clean `git reset --hard`).
**No history was rewritten before `3e3f705`; `3e3f705` is the authoritative branch tip.**

**Recovery assets (outside iCloud):**
- `/tmp/massif_recover/` — full extraction of the pre-incident ZIP (1,184 files) used to restore missing package files.
- `/tmp/massif_new_checkpoint/` — snapshot of the post-`3e3f705` content that could not be committed: Council-2
  `COUNCIL2_INTAKE.md`, `DECISIONS.md` (D66–D78), `COUNCIL_STATE.md`, `BIG_PICTURE.md`; A1 addendum + corrected
  `findings.txt` + `anchor_table.csv` + `run_meta.json`; `A2D_CAPACITY_LEADS_INTAKE.md`,
  `PRE_PORTABILITY_A6_A7.md`; `lit/PHASE_WRITEUP_SHELL.md`; closure STATUS/CHANGELOG; calib provenance CSVs.
  Key hashes: COUNCIL2_INTAKE 71aadc99…, DECISIONS 88cdf6f8…, A1 addendum 02c5f476…, findings 4c21e3f6…,
  phase shell ed6e2400…, A2d a139f6ff…, portability 53373007…, STATUS fb275563…, CHANGELOG 174fdbfd….
- Git objects for all content up to `3e3f705` are intact in `fleet.nosync/atlas/.git`; prior ZIPs remain on disk.

**Provenance resolved for the write-up shell numbers (lead item):**
- `4.35` linear-trend and `8.60` persistence benchmarks → `10_massification/model/calib/calibration_table.csv`
  sha256-16 **552e0cce04bd148d** (values 4.352883341604888 / 8.599852941176476).
- `6.16–7.43` repair-cell PHL fit MAE → `10_massification/model/calib/repair_table.csv` sha256-16
  **34b0a5bc98e3d603** (PHL_fit_mae 6.1627–7.4326); companion `repair_scaling.csv` **7330a8785e28619f**,
  `scaling_check.csv` **a07077c4e38253af**. These can be pasted into the shell; if the shell already cites
  STATUS, replace with these paths+hashes.

**Pending when filesystem is stable:** re-run `build_manifest.py` + `package_delivery.py stage` from a complete package
root (verify stage ≥900 files, SHA256SUMS verifies), `git reset --hard 3e3f705`, rsync stage → worktree, scoped
`git add`, commit the snapshot content, push, rebuild ZIP, and post `OP: checkpoint <sha> — anchor closed; addendum+shell
in`. No external messages; data queue remains HELD (user quiet mode). Until then, **`3e3f705` is authoritative** and the
new content lives in `/tmp/massif_new_checkpoint/`.

## 3s. PHASE CLOSEOUT committed; iCloud worktree RETIRED as active checkout (20 Nov)

- **Closeout:** `06_report/MASSIFICATION_CLOSEOUT.md` (authoritative phase summary: headline, limits, re-openers C1–C4,
  recovery incident, hashes) committed in the recovery checkpoint lineage; pointers added in `LEAD_HANDOFF.md`,
  `NEXT_LEAD_PROMPT.md` and `06_report/EXTERNAL_CHECKIN.md` read order.
- **iCloud worktree retired as an active checkout.** The canonical branch tip is the GitHub
  `experiment/massification-2026-11-20`; checkpoints are built from a **stable-root clone** (`/tmp/massif_repo`, or a
  durable clone such as `~/massif_work` cloned from GitHub), with the iCloud package kept as a **read-only mirror**
  (only the ZIP pair is written back at delivery boundaries). Reason: iCloud file-loss/truncation incident during the
  anchor-closure checkpoint (see §3r) invalidated in-place git operations.
- **Final delivery pair:** commit and ZIP hashes are in the `OP: checkpoint <sha> — phase closeout committed` bridge post
  and the adjacent `.sha256`; SHA256SUMS verified in `/tmp` (0 failures) and conflict-name scan 0.
- Data asks remain **HELD** (nothing sent; user quiet mode); no direction claims; shadow phase closed.

## 4. Next three actions for `repo-auditor`

1. **Council gate:** get the Council's final `COUNCIL:` post for brief 013 (SUCCESS_CRITERIA + STOP_RULES are
   drafted); read it, then un-gate task-37 and assign the ranked slate to owners with deadlines.
2. **First `NEW:`/`ACK:` cycle:** the lit and model2 batches have landed without a formal `NEW:` post yet — have the
   owners post `NEW:` (path, key number, hash, what it changes) and the mandated ACKs (lit → Council + runners;
   scaling → both runners + Council; model → other runner + Council).
3. **Keep the branch clean:** commit `10_massification/` batches as they land (rebuild the ZIP each checkpoint), and
   re-run the conflict scan + `SHA256SUMS` check before every push.

## 5. Standing rules (unchanged)

Predeclare every run; label observed vs simulated; never impute as observation; no target coded as a parameter;
1980–2010 fit / 2011–2024 holdout where data permit; no re-fit of closed shadow claims; `NEW:`/`ACK:` loop mandatory
(no artifact delivered until ACKed); external actions (data requests, publishing, site) need user approval; bridge is
append-only with per-agent parties via `bridge-agent.sh`.

---

## Recovery marker — 2026-11-20 18:57 +08:00 (Lead, lead-successor)

- **Remote authoritative tip:** `4ba958c`; clean sparse checkout `/Users/treymenefee/massification_live` matches it.
- **iCloud package corruption:** dataless/zero-byte reads, 272 conflict copies, unreadable worktree `.git`; 272
  conflicts removed (canonicals verified), closeout file restored; recovered ZIP rebuilt outside iCloud:
  `/Users/treymenefee/massification_fresh.zip` — 11.9 MB, 1,031 files, sha256 `cc232354…62d9`.
  Closeout's canonical ZIP remains `5de0b4a6…` (1,187 files, built before the incident).
- **Codex bundles preserved outside iCloud:** `extensions_archive/codex_2026-11-20/` with `SHA256SUMS.txt`
  (codex-massification `5eec1147…`, luna `948a07a2…`).
- **Phase remains CLOSED** — anchor PARTIAL/DESCRIPTIVE/EQUIVALENT; no re-fit, no reopening. No A/B/C started.
- **Pending user decision** (only the user may reopen): (A) integrate Codex bundles under
  `10_massification/extensions/codex_2026-11-20/`; (B) C1 correct-sign scaling repair; (C) phase write-up package.
- **Bridge:** 480 messages; local bridge writes are timing out on iCloud — bridge catches up when sync recovers.

---

## 3t. Lab battery B — 15 predeclared experiments, Z.AI Flash worker fleet (2026-11-20 ~21:07 +08:00)

- **New artefact:** `10_massification/extensions/lab_2026-11-20_b/` — extension of lab battery E1–E10 into five
  post-secondary clusters (3 experiments each). **Predeclared before running** (`PRE_DECLARATIONS.md`, sha256
  `c214dddfe51ef0ff9d0173752fe11f74a91e165605ebba45bc405d9fe6381af6`); executed by **five Z.AI GLM-5.3-Flash
  subagents** with disjoint write scopes (one cluster each); Lead consolidated, re-ran every script and
  adjudicated. Phase remains **CLOSED** (D76); C1–C4 not reopened; no causal/direction claims.
- **Results:** `RESULTS.csv` 18 rows = 15 predeclared + 3 `run_tag=amendment_B1` (cluster-5 disclosed post-hoc
  amendment). Predeclared verdicts: **SUPPORTED 4** (X3 queue-depth, X10/X11/X12 PHL regional), **PARTIAL 1**
  (X9 markets, one sample only), **NOT SUPPORTED 5** (X1/X2 absorption, X4 tertiary-vs-secondary structure, X7
  size, X8 city-state), **DATA LIMITED 1** (X5), **UNABLE 1** (X6 n=3), **SIMULATED-THRESHOLD-MISSED 3**
  (X13–X15 predeclared run — lead predeclaration defect, see below). Amendment B1 (same frozen thresholds,
  corrected growing demand rule): X13 Δ=+1.0 y PARTIAL, X14 V=1.231 PARTIAL, X15 ρ=1.000 PARTIAL; exploratory
  extensive margin 77%→100% of seeds cross.
- **Key findings (see `FINDINGS.md`):** (1) no absorption-proxy association replicates across 6-system and
  30-country panels, but the derived queue-depth ratio rises with tertiary GER in 3/3 30-country specs;
  (2) tertiary crossings do not share the secondary structure package and the contrast is DATA LIMITED/UNABLE;
  (3) system size does not scale schooling cross-sectionally; the HKG-vs-CHN duration ratio is 0.667 (HKG slower)
  at n≤4; (4) PHL regional record is the cleanest result (17/17 regions improve, Gini falls ≥0.02 in 17/17,
  mild pro-poor gradient 1.098) — **regional tertiary enrolment unobserved, proxies only**; (5) fragmentation
  (SIMULATED) moves the extensive margin, not timing.
- **Disclosures:** X1 predeclaration internal conflict (PARTIAL clause vs falsifier) adjudicated
  falsifier-precedence → NOT SUPPORTED (worker's PARTIAL reading retained in the note); X2 point inside the X1
  CI but opposite sign → NOT SUPPORTED; X4 denominator read as ≥4 countries with n=5; X8 HKG volatility inflated
  by a series break; cluster-5 predeclaration used a **contractive** demand recursion (r=0.08<1) → all-censored,
  disclosed as a **Lead predeclaration defect** and answered by post-hoc **Amendment B1** under unchanged
  thresholds.
- **Determinism:** all five cluster scripts + the amendment script re-ran **byte-identical**; `SHA256SUMS.txt`
  51/51 verify; `RUN_MANIFEST.json` carries predeclaration/data/code/results hashes and the re-run table.

---

## 3u. Council-2 brief 017 + battery C (five anchored experiments, Y1–Y5) — 2026-11-20 ~21:30 +08:00

- **User directive this session (institutionalised):** the Council decides next directions and, **after every
  delivered results batch, issues exactly five anchored experiments**; each experiment must carry the mandatory
  7-field ANCHORING BLOCK (first-order channel link; what changes in the model if positive vs negative; why it is
  not a niche; on-disk data or a HELD data ask; numeric threshold + falsifier; closed-claim check; cost/rank) plus a
  **drop-first** naming. Recorded as **D89** (rabbit-hole guard = mandatory step-back + block + drop-first); the
  standing order is also written into `06_report/NEXT_WINDOW_PROMPT.md` so future windows inherit it.
- **Council cycle executed** (`08_council/brief_017/SYNTHESIS_017.md`, sha256 47e28af7…): step-back (five lines);
  **battery B adjudicated ACCEPT-WITH-CONDITIONS** (labelled design evidence, evidential weight zero; Council
  re-derived X10 ρ = −0.443627 / 17-17 and X11 ρ = −0.621524 / 17-17 — MATCH); X3 relabelled
  derived/mechanical (its numerator is a lagged tertiary-attainment stock); battery-B numbers banned from evidence
  columns; all four disclosed Lead adjudications ruled **correct**. Decisions **D88–D92**: battery-B verdict;
  standing order; Y-slate ranking (Y1 > Y4 > Y3 > Y2 > Y5) with **drop-first = Y5**; **critical path = the A1/phase
  write-up** (D91; model repair barred R27; more descriptive battery work = the drift being corrected; C1
  provider-entry design = held re-opener); data ruling (10 usable on-disk series; PSA/ES/annual capacity/per-pupil/
  subnational sector = HELD; no Y needs a new ask). No external message sent (bridge times out, D87).
- **Battery C predeclared and run:** `10_massification/extensions/lab_2026-11-20_c/` — `PRE_DECLARATIONS.md`
  sha256 `8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1` (thresholds copied verbatim from
  SYNTHESIS_017 §D, Lead operationalisation declared). Executed by **three DeepSeek Flash workers** (disjoint
  dirs: Y1+Y3 / Y2+Y4 / Y5); Lead consolidated; **all five scripts re-ran byte-identical**; SHA256SUMS 46/46 verify.
- **Results (RESULTS.csv, one row each):** **Y1 NOT SUPPORTED** — opportunity-cost account discarded
  (income-partial ρ ceiling×agri −0.105, ceiling×youth-unemp +0.246, n=30; raw agri −0.718 absorbed by income;
  6-system raw check points the other way, disclosed tension). **Y2 NOT SUPPORTED** — no detectable schooling↔market
  lead-lag (max |partial r| 0.208 < 0.25 bar; zero-order 0.49–0.71 is shared trend; EQUIVALENT reinforced).
  **Y3 NOT SUPPORTED** — capacity floor-vs-ceiling not separable at n=6 (floor ρ 0.50 boundary; ceiling ρ 0.60
  fails; leave-one-out fragility 0.0–0.8 / 0.3–0.9 disclosed; A10 stays a model-side ruling). **Y4 DISTINGUISHED** —
  the world-society null (median-year crossings) manufactures upper-secondary ≥90 crossings for 4 never-crossed
  systems (2 evidence-backed: CHN 79.39, PHL 66.05), supporting the D77 scoping; caveat = upper null rests on one
  dated crossing (HKG 2011.5). **Y5 DATA-COMPLETE** — all six D75 CHN/HKG transfer inputs present on disk; **0
  NEW-ASK**; held queue reaffirmed HELD, nothing sent; design-only (no portability claim, R20/R22).
- **Critical path (D91) unchanged:** the A1/phase write-up + addendum C1–C10 remains the one thing this cycle;
  Y1–Y5 tighten its open descriptive items only. Phase **CLOSED** at PARTIAL/DESCRIPTIVE/EQUIVALENT; C1–C4 not
  reopened; no direction claims.

---

## 3v. Synthetic workbench v1 + longitudinal battery (final verdicts) + external literature review — 2026-11-20 ~22:30 +08:00

**Authority unchanged:** phase CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT (D76); no causal or push/pull direction
claims; data asks remain HELD; literature *reading* is authorised.

### a) Synthetic-data workbench — v1 delivered, verified, packaged

- **Position:** `10_massification/extensions/synthetic_2026-11-20/` (v0 + v1 + registers), packaged with
  `RUN_MANIFEST.json` + `SHA256SUMS.txt` (**30/30 verify**) via `extensions/build_package.py`.
- **Registers:** equations 43 rows (10 carry an `equation-in-literature` tag; the rest narrative-only /
  programme-invented / programme-estimated); facts 53 rows, **35 VERIFIED-FROM-DISK** (6 SIMULATED, 5 DISPUTED,
  4 MODEL-OUTPUT-NOT-FACT, 3 REPORT-ONLY-UNRELIABLE).
- **v1 (`generator_v1/`):** 30 synthetic countries × 1970–2025 × 4 levels = **6,720 rows**, seed 20261120, constant
  all-SYNTHETIC labels. Determinism **controller-verified**: two fresh runs byte-identical to each other *and* to the
  delivered CSVs (`synthetic_panel_v1.csv` sha256 `d27957be…3103a2b`).
- **v1 predeclared checks (AUTHORITATIVE worker delivery; an earlier same-day intermediate run that read A–D FAIL is
  withdrawn):** **A PASS but target-encoded · B FAIL · C PASS (half structural) · D PASS · E PASS · F PASS.** Key
  numbers: check A — primary first ≥90 **2017**, lower-sec first ≥90 **2024** (2023 = 87.2), upper-sec never ≥90 max
  **75.1**, tertiary GER **15.3 → 50.3**, floor→middle gap **7 y**, ceiling residual **14.9 pp** — but the four PHL
  supply paths are interpolated through the declared anchors, so **"one parameterisation, no per-level rescue" is NOT
  met** and A is encoding, not prediction; check B — pooled decade-FE `b_lit` **+2.37** vs `b_yos` **+0.26** ✓ but the
  association **survives the takeoff ablation (+2.29) and the full job-ladder ablation (+2.10)** → over-determined and
  **non-diagnostic**; check C — no positive rank premium at the primary margin (−0.485 with literacy control; rung-1
  rank factor = 1 by construction → half structural), credential ladder +4.76 (p<1e-6) ✓; check D — +10% schooling
  push buys **+0.022 pp** growth per unit X (p=5.8e-8), high-X tercile +0.029 vs low-X +0.005 (**6.2×**); check E PASS
  (twins within 1.41% graduates: growth 3.10 vs 2.50 pp, queue diff 95%); check F PASS (cohort conservation 2.05e-16;
  shares sum to 1).
- **Load-bearing finding (worker TUNE_LOG):** the **stipulated upper-secondary seat cap (0.845→0.875)** is what makes
  the anchor asymmetry — put the ceiling on the floor's growth path and the asymmetry disappears. v1 therefore
  **reproduces the asymmetry substantially by assuming it**; the declared PHL survival path is the second
  load-bearing object. The rung ladder governs the **marginal return** (D) but not the **level** association (B).
- **Ruling:** target encoding and the non-diagnostic B are **declared-model facts, not empirical findings**; no
  post-hoc re-fitting is permitted. **v1.1 predeclaration must**: (a) add the user's **education → complexity**
  channel (schooling flow raises X with a 5–10 y lag), (b) **remove the per-level PHL anchor interpolation**, (c) adopt
  the rule that a synthetic horse-race PASS is **non-diagnostic unless the ablation fails**, (d) derive the
  upper-secondary seat capacity from the economy side. Also recorded: **completion can exceed GER** because the UIS
  completion rate uses a 3–5-years-above-grade denominator — verified PHL 2024 primary **98.30 completion vs 94.03
  GER**; a measurement-definition note added to `facts/STYLIZED_FACTS.md` §12 and
  `10_massification/data/DATA_NOTES_MASSIFICATION.md`.
- **Determinism re-verified** on the authoritative files: two fresh runs byte-identical to each other and to the
  delivered CSVs (`synthetic_panel_v1.csv` `cf8dfbcb…`, `reproduction_checks_v1.csv` `0914e3c7…`).

### b) Longitudinal battery — final verdicts after the stats re-run (Lead correction applied)

- `longitudinal_2026-11-20/FINDINGS.md` corrected: **H1 PARTIAL · H2 NOT SUPPORTED · H3 NOT SUPPORTED · H4
  SUPPORTED (descriptive co-movement map only)**. H2's final numbers: ECI S2 −0.581 [−1.632, 0.469] ns; **S3
  −2.589 [−4.112, −1.067] significantly NEGATIVE** (opposite the canon's predeclared sign); unconditional
  within-country growth~ECI r = **−0.153** (p=0.001). S4 long differences DATA LIMITED (CHN/LKA/MNG/MYS/SGP).
- **"Growth is the weakly-attached variable":** all nine growth pairs |r| < 0.21 and negative (growth~MYS −0.203,
  growth~ECI −0.153, growth~lit −0.091); the horse race is unresolved on the growth side. No causal/direction claim;
  no Africa claim.
- **Package rebuilt** after the correction (3 stale hashes fixed): `RUN_MANIFEST.json` + `SHA256SUMS.txt` **23/23
  verify**; `stats/REPRO_CHECK.json` shows 10/10 result files identical across re-runs.

### c) External literature review — DELIVERED

- **Deliverable:** `10_massification/lit/external_review_2026-11-20/` — `EXTERNAL_LITERATURE_MEMO.md` (memo with
  citation + URL per claim, the "what we do NOT need to redo" section and the "what genuinely remains open" section),
  `EXTERNAL_LITERATURE_ROWS.csv` (**76 claim rows, 63 unique sources**: 38 VERIFIED-FULLTEXT, 10 `VERIFIED`, 14
  VERIFIED-ABSTRACT, 4 VERIFIED-METADATA, **10 UNVERIFIED** clearly flagged), `EXTERNAL_LITERATURE_CITE_INDEX.csv`,
  and the three workstream evidence files + `rows_C_REPO_AUDIT.md` + `build_rows.py`. Retrieval used `curl` because
  `web_fetch` is DNS-blocked in this environment; every status reflects text actually downloaded and read.
- **Strand verdicts:** (a) schooling vs cognitive skills and growth — **settled in outline**: measured cognitive skills,
  not years of attainment, carry the cross-country growth association (HW 2012: 1 SD ≈ **1.2–2.0 pp/yr**; attainment
  insignificant once skills enter; IV first stage weak); Pritchett (2001) finds **no association** between
  educational-capital growth and output-per-worker growth against a growth-accounting benchmark of 0.21–0.42; Krueger–
  Lindahl reconcile via initial stock/level composition; Barro (2013) is the live counterexample (+1 year male
  secondary = **0.44 pp** impact growth). The programme's years-of-schooling null is a **replication**, not a
  discovery; the programme has **no learning-outcome data**. (b) ECI/complexity — ECI→growth content is real but
  **modest, metric-dependent and contested** (spectral-clustering interpretation, contrasting rankings); education →
  complexity is **capability theory, not established evidence** — the field's own authors report **R = 0.13** between
  ECI and years of schooling and call schooling-years an inadequate capabilities proxy; the three direct
  complexity×human-capital studies were identified but **not fetched**. The programme's own ECI→growth nulls are
  consistent with the critique record. (c) absorptive capacity/threshold/dual economy — **canonical frame exists**
  (Lewis; Harris–Todaro; Abramovitz; Timmer; McMillan–Rodrik; Rodrik; Caselli–Coleman; Goldin–Katz; Autor et al.;
  Eichengreen et al.) but the internal layer has **no** coverage; no published source supplies a threshold value for
  the Philippines. (d) educated unemployment/credential queue — **theory settled** (Freeman, Collins, Spence, Arrow,
  Thurow; Leuven–Oosterbeek: surplus-schooling returns ≈ **45%** of required-schooling returns, rejecting pure
  human-capital *and* pure job-competition), and the **Philippines is already measured**: **39%** overeducated,
  flat real graduate wages vs **~50%** growth below secondary, highest graduate-youth unemployment (World Bank 2026,
  *Building the Filipino Middle Class*); **1 in 5** tertiary workers in basic-skill jobs and licence premia only when
  matched (PIDS DP 2025-32); IT-BPM **~1.9M jobs / US$40bn / ~80k net adds per year** (IBPAP). (e) projection models —
  **internal coverage zero**: WIC multi-state cohort-component (published method; **WIC 2023 dataset CC BY 4.0**,
  Zenodo `10.5281/zenodo.7767425`), WCDE, Barro–Lee (reconstruction, not projection), EPSSim 2.1, UNESCO generic model,
  MOSART microsimulation, schooling ABM. **The programme reinvented its demography; it should adopt/benchmark WIC and
  cite EPSSim/MOSART, not rebuild.**
- **Repo ledger audit:** `LITERATURE_LEDGER.md` contains **zero** hits for growth/complexity/ECI/Hanushek/Barro/Lutz/
  IIASA — it is a shadow-education corpus. `EXPECTATIONS.csv` is **not** zero-standard-citation (19 rows; 9 name a
  work) but **no row's citation is held on disk**. Only **10 of 43** registered equations are literature equations.
- **"What we do NOT need to redo"** (memo §8): the demographic engine; the structural/dual-economy frame; credential/
  queue theory; the ~9%/yr global returns benchmark; the macro–micro puzzle and its resolution; the Philippine
  graduate-market facts; the threshold/middle-income claims. **"What remains open"** (memo §9): a dynamic estimate of
  the queue (what happens to the marginal graduate when the rung fills); direct education→complexity evidence; a usable
  functional form for absorptive capacity; the measurement-definition work; the demographic-overflow mechanism (v1.2).


### e) Education → ECI — predeclared panel analysis RUN (the user's restated hypothesis)

- **New workbench:** `10_massification/extensions/edu_eci_2026-11-20/` — `PRE_DECLARATIONS.md` frozen before the run
  (sha256 `e2a707a9…5bc230`, hash-checked by the script), one deterministic script, 272-row `RESULTS_ALL.csv`;
  specs S1 long differences, S2 annual two-way FE, S3 5-year blocks, S4 within/between, S5 reverse-order (symmetric,
  no direction claim), S6 baseline-ECI heterogeneity; true calendar-year lags 5/10; control sets C0/C1; outcomes
  `eci_sitc` (primary) and `eci_hs92` (robustness). Descriptively only — no causal, no direction claim.
- **Verdicts (frozen rule): 1 SUPPORTED · 5 PARTIAL · 8 NOT SUPPORTED; 12/14 ROBUST to `eci_hs92`.** The single
  SUPPORTED cell (youth literacy, 5y) is **not robust**. **Primary completion is PARTIAL at both 5 and 10 years and
  ROBUST** (+0.003–0.008 ECI points per pp; roughly halved by the income control); lower-secondary PARTIAL at 5y,
  flat at 10y. **Adult literacy stock: null at 10y** (consistent with the earlier on-disk result). **Upper-secondary
  attainment: nothing (negative, ns). Tertiary attainment: negative-significant in the country+year FE spec**
  (−0.0155, p=0.006, adjusted) — massification-without-complexity association, not a direction claim. **No
  low-base heterogeneity**: LOW−HIGH slope difference −0.0045 [−0.024, +0.019] at 5y and −0.0075 [−0.031, +0.021] at
  10y. Reverse order: ECI(t−10) → upper-secondary −4.68 (p=0.016); → primary completion +1.58 (ns); → literacy −0.84 (ns).
- **Existing-result cross-check: EXACT.** E5 (`eci_hs92 ~ log primary completion, t−10`, two-way FE, the file's own
  row-shift lag) reproduces **0.5932271376 (se 0.1757698583, n=253, 23 countries)**; the same spec with a true
  calendar-year 10-year lag gives **0.5690534891 (se 0.2317801262, n=320, 27 countries)** — the anchor survives the
  lag implementation, but it is a **log specification on `eci_hs92` with no income control**, and the predeclared
  level matrix on `eci_sitc` returns only PARTIAL. Specification-dependence must be stated in any write-up.
- **Answer to the user, plainly: the hypothesis is not established in this panel.** The best description is a small,
  fragile association between **primary-completion flow** and measured complexity; the upper levels show nothing (or
  negative), the literacy stock shows nothing, and there is no threshold-from-a-low-base pattern. Determinism: two
  clean runs byte-identical. Deliverable: `FINDINGS.md` in the workbench.

### f) Amendment A2 recorded — demographic overflow / quality collapse / child-labour block (v1.2 predeclared)

- **User directive (dashboard, 2026-11-20):** the Philippine story is a **baby boom moving through the school-age
  population** with schools/teachers not built fast enough → **seats overflowed, quality collapsed** (congestion, PTR,
  double shifts); the **out-of-school block should be borrowed from the Atlas `childworld` model** ("unless it's
  broken"), default **not-in-school = child labour/work**, families compete for places.
- **Recorded** as `MODEL_ARCHITECTURE.md` **Amendment A2** in `synthetic_2026-11-20/`, with the borrow ledger: structural
  elements only from `engine/childworld.py` at parent-repo HEAD, sha256 `ae73adb2…a23cab` (four-state household block,
  utility decision, parameter names), read-only retrieval via `git show`; **no childworld prior/posterior/target/value
  is imported**. Caveats carried: childworld "Not run, only inspected", observation equation **not the ILO definition**,
  v1 failed the India composition test, baseline "neither" 0.421 flagged — all stated in the amendment and spec.
- **Frozen v1.2 spec:** `synthetic_2026-11-20/v1_2/PRE_DECLARATIONS.md` — declared cohort path (observed
  `UNIVERSALIZATION_SERIES.csv`), lagged capacity → congestion/quality → completion/dropout, four-state household block
  **with rationing** and **no passive "neither" sink**, education→complexity channel retained, and five predeclared
  checks: (a) PHL asymmetry from cohort surge + seat lag + quality collapse **without per-level anchor interpolation**,
  (b) OOS/child-labour plausible and cohort-responsive, (c) PTR peaks during the boom then falls, (d) completion ≤ GER
  identity with the disclosed UIS measurement convention, (e) education→X positive at lag. **No post-hoc rescue
  parameters.** v1.2 code/PARAMS are to be frozen with their sha256 in the manifest before the first scored run —
  the build is a separate worker-sized job, not executed in this window.


### d) New user directive (education → ECI) — predeclaration next

- The hypothesis is **education → economic complexity**, not education → growth; outcome = `eci_sitc`. Existing
  on-disk evidence to build on (do not redo): **ECI ~ adult literacy stock 0.001 (p=0.83) — no relation; ECI ~
  primary completion lagged 10y 0.593 (se 0.176, p=0.001) — the schooling FLOW tracks complexity;
  upper-secondary attainment 0.055 (ns)** (`09_relations/LITERACY_ECI_DEMOGRAPHY.md`). A new predeclared
  education→ECI panel (levels × lags 5/10 × cross-section-FE/5-yr-block/within-between/reverse/heterogeneity) is the
  next deliverable; `MODEL_ARCHITECTURE.md` carries **Amendment A1** requiring v1.1 to encode schooling flow → X.

---

## 3w. USER DIRECTIVE (2026-11-20, dashboard relay) — keep building until the PHL system exists; HKG is parallel prep, not a hand-off

**Status correction (accepted):** the Philippine system is only **partly stood up**. Three gaps are now the critical
path: (i) the **v1.2 demographic/quality layer** (cohort surge → lagged capacity → congestion/quality → completion) is
**not built**; (ii) there is **no shadow-education block**; (iii) **education demand signals and their interaction with
the wider economy are not yet modelled accurately**. The user's standing instruction is to **keep working until that
exists**, and he asks whether to move on to Hong Kong — answer: **HKG is a parallel prep workstream (W3), not a
hand-off**; PHL remains the critical path.

**The user's three points, recorded verbatim in intent:**
1. *"Do we move on to Hong Kong?"* → HKG prep proceeds in parallel (inventory + frozen transfer predeclaration,
   run-ready, not run), under D75's six constraints; the actual HKG run waits until v1.2 passes its PHL checks.
2. *Shadow education was paused and must now "show up" around the relevant gating* — tutoring demand as a **demand
   signal at the gates/queue**, not a generic add-on. Encoded in W2's `shadow_module/` (frozen predeclaration).
3. *Accurately model education demand signals and their interaction with the wider economy* — expected returns, gate
   probability, sector structure, migration/remittances. Encoded as **MODEL_ARCHITECTURE Amendment A3** and in the v1.2
   household block; the demand-signal equations must be declared, labelled, and tested, not assumed.

**Work queue dispatched (disjoint dirs; predeclare first; everything labelled observed/derived/synthetic):**
- **W1** — `synthetic_2026-11-20/generator_v1_2/`: build v1.2 exactly to the frozen
  `v1_2/PRE_DECLARATIONS.md`, including check A **without per-level anchor interpolation**, the childworld four-state
  block (structural borrow only, sha256 `ae73adb2…`, no passive "neither"), and the five checks. **Critical path.**
- **W2** — `synthetic_2026-11-20/shadow_module/`: SHADOW_MODULE.md + frozen predeclaration + parameter table + dry-run
  plan for the v1.3 shadow-education-at-the-gates block (tutoring demand = f(gate pressure, expected returns, family
  income); tutoring raises gate-passing probability/rank; near-zero at primary; HKG-high/PHL-mid/KHM-low ordering as a
  predeclared check). Design only, not a build.
- **W3** — `extensions/hkg_transfer_2026-11-20/`: HKG inventory + frozen transfer predeclaration + checklist under
  D75's six constraints (fixed PHL behaviour, no re-fit, timing-only, levels check-only, no imputed completion,
  DIAGNOSTIC-TRANSFER verdicts only; NER ≥90 1974 / ≥95 1979 targets to be verified from disk).
- **Integration (controller, after W1–W3):** `MODEL_ARCHITECTURE.md` **Amendment A3** — demand signals
  (expected returns × gate probability × sector structure × migration/remittances) and the shadow block at gates; verify
  each deliverable, package it (RUN_MANIFEST + SHA256SUMS), commit, push, rebuild the ZIP, report milestones.
- **Standing rules unchanged:** predeclare before running; labels observed/derived/synthetic; no causal or
  direction/push–pull claims (R13/D77); never fabricate a number or citation; deterministic runs (two runs
  byte-identical); data asks remain HELD; no long tasks in the dashboard window.

---

## 3x. Reactivation progress — v1.2 built, shadow module frozen, HKG prep BLOCKED, theory frame merged (2026-11-20 ~22:50)

### a) W1 — SYNTHETIC generator v1.2 DELIVERED (`synthetic_2026-11-20/generator_v1_2/`)

- **Panel:** 30 synthetic countries × 1970–2025 × 4 levels = **6,720 rows**; declared observed PHL cohort path as an
  input; childworld four-state household block (structural borrow only, sha256 `ae73adb2…`), no passive "neither"
  (out-of-school ⇒ work), lagged capacity → congestion `q = cohort/seats` → quality `Q = exp(−γ·max(0,q−1))` →
  completion/dropout; education→`X` channel at 10-year lag.
- **Predeclared checks: A PASS · B PASS · C PASS · D PASS · E PASS** — **with decisive caveats, stated by the worker
  and carried here:** (i) **check A is scored on a UIS-convention series** (`m × cohort-flow`, one declared constant
  **m = 1.10**); the **identity-bound cohort-flow series would FAIL A** (primary 90 only 2024, lower never), and the
  admissible window is narrow (m = 1.05 → primary 2022 FAIL; m = 1.12 → upper-sec 78.0 FAIL); (ii) **the parameterisation
  was calibrated in the design phase** (`TUNE_LOG.md` D0–D4, all disclosed) — this is a **feasibility demonstration,
  not a blind test**; (iii) **the upper-secondary ceiling is demand/quality-driven, not boom-driven** (flat cohort →
  upper-sec 2024 = 73.2 and still never crosses 90); (iv) the design-run 22 completion>GER identity violations were
  traced to an unrealistic 8% household shock (`hh_noise_sd` 0.08→0.015) and a burn-in level; the scored run has
  **0 violations** (worst margin −2.19e−02).
- **Headline numbers (SYNTHETIC):** UIS completion primary first ≥90 **2019**, lower **2025** (2023 = 79.04), upper
  never ≥90 with 2024 = **76.64**; tertiary GER 2025 = **50.23**; PHL primary OOS 2005–15 mean **8.72%**; child-labour
  share of OOS ≥ 0.599 in every country-year; PTR peak **40.93 (1996)** → 32.66 (2024); education→X two-way FE
  **b = +0.828** (p<1e−4).
- **Supply-rule audit PASS:** one equation in three functions, **0 country branches, 0 per-level year-indexed anchor
  arrays, 0 forbidden tokens** — the v1 failure (target-encoded floors) is removed.
- **Verified by the controller:** two clean re-runs byte-identical to each other and to the delivered CSVs; all
  manifest hashes (code, PARAMS, predeclaration, 5 input files) re-computed and **match**.

### b) W2 — shadow-education gating module DESIGNED + FROZEN (`synthetic_2026-11-20/shadow_module/`)

- Design: tutoring demand at a gate `D = σ(a_g + b_Z·lnR + b_V·ln(1+V) + b_Δ·ln(1+Δπ) + b_y·ln(y) − b_F·ln(1+s))`,
  with `R` built from v1.2's queue/transition/rank state, `V` the positional credential value, `Δπ = δ_g(1−π⁰)` so
  tutoring's room is largest where the gate is tightest; feedback into next-period eligibility. **No passive "neither"
  sink; near-zero-at-primary kept as a STRUCTURAL (not empirical) check.**
- Frozen predeclaration sha256 `cf8c61cb…` (hash-checked by the script); checks c1–c6 with thresholds (c4a HKG
  D ∈ [0.75,0.95]; c4b ordering on cohort-incidence D*; **c6 no-re-fit guard**: with shadow off, v1.3 must reproduce
  v1.2 byte-for-byte); 42-row parameter table with provenance; dry-run plan; toy design check (SYNTHETIC/TOY) PASS
  c1/c2/c3/c5, deterministic on re-run.
- **Controller S1 pre-run note added** (`PRE_DECLARATIONS_S1_NOTE.md`, sha256 `af49a616…`): the dispatch brief's
  "HKG high, PHL mid, KHM low" is **not established by the on-disk rates** (KHM Grade-9 case study **68.4%** > PHL
  all-basic **46.5%**; different stages/samples). c4b is therefore a **declared synthetic-reproduction check on the
  model's cohort-incidence statistic**, not a data claim; c4a is the only (wide) empirical anchor; c3 is structural.
- **D* (toy, illustrative states): 0.741 / 0.375 / 0.174** for HKG-like / PHL-like / KHM-like — the ordering is carried
  by **who reaches the gate** (exposure 0.94/0.75/0.43), not by different demand intensity.

### c) W3 — HKG transfer prep BLOCKED (run-ready, NOT run) (`hkg_transfer_2026-11-20/`)

- Both D75 targets verified from disk: primary **NER ≥90 in 1974** (band 1973–74; 89.60→91.11) and **NER ≥95 in 1979**
  (band 1978–79; 94.69→95.08); the **1977-vs-1979 discrepancy resolved** (1977 first-at-above but not sustained; 1978
  dips; on-disk rule = first sustained ≥5y) and carried as a mandatory disclosure.
- **BLOCKED (terminal non-verdict):** **SR-1 no NER object in the frozen model** (panel emits GER/completion/survival/
  enrolment only; not rescued by GER, completion or a proxy), **SR-2** v1.2 not yet passed at time of writing, **SR-9**
  no Council authority. Frozen predeclaration sha256 `99be01d7…`; SHA256SUMS 5/5 verify; no results produced.
- Consequence queued: **v1.2.1 must add an NER output object** (and audit the identity fix) before an HKG run is even
  possible at the model interface.

### d) Council cycle 12 merged; theory frame wired

- brief_019 (hysteresis paper) D98–D101 were already in the log; **brief_020 (assembly paper) merged as D102–D105**
  (paper-status ruling: developmental micro-foundation scoped to the person-installation channel; DT1–DT5 slate;
  integration ruling; falsification reach). `BIG_PICTURE.md` + `COUNCIL_STATE.md` updated once (cycle 12).
- **`MODEL_ARCHITECTURE.md` gains Amendment A4 — DECLARED-THEORY:** the combined frame `scaffold = schooling system →
  induction = literacy/numeracy/schedule-discipline → exit cost = persistence/ceiling → shadow = niche expansion at the
  gates`; **no parameters, no new layer**; gates: exit-cost layer only if **WT1 AND WT3 both non-null** (then declared +
  D81 ablation-tested); induction naming only if **DT1 AND DT2 both non-null**; everything labelled theory-only, never
  evidence.
- **Queued after W1–W3 (dispatched):** WT battery (`wt_2026-11-20/`: WT1, WT2, WT4, WT3 scored; WT5 design-only) and DT
  battery (`dt_2026-11-20/`: DT1, DT2, DT4, DT5 scored; DT3 design-only/HELD) — predeclared, deterministic, all cells
  reported including nulls.

### e) WT + DT batteries EXECUTED — both Council gates NOT met (D106/D107)

- **WT battery** (`wt_2026-11-20/`, predecl sha256 `d3ad365e…`; deterministic, 13/13 SHA verify): **WT1 NOT SUPPORTED**
  (fall/rise run count 0.443 ≤ 0.50 passes, but median depth ratio 0.601 > 0.50 fails — direction as predicted, magnitude
  short; indicator-dependent); **WT2 NOT SUPPORTED** (10/10 decoupled but 4/10 have a ≥5 pp sustained tertiary
  reversal > 1/3; the % growth vs pp criterion is near-vacuous); **WT3 NOT SUPPORTED** (income-partial ρ = −0.520; raw
  +0.073 flips sign on income — Y1 lesson); **WT4 SUPPORTED (descriptive)** (0 exit episodes, but fragile: the
  2017→2022 upper-sec drawdown −8.16 pp has only ONE observed year below threshold; one more 2022-level year flips it);
  **WT5 DESIGN-ONLY / NOT SCORED** — **data problem found:** the block's 1.889 is HKG **2010 senior ÷ 1996 primary**
  (cross-year); the only same-year pair on disk (HKG 1996) is 40/45 = **0.889 → no gate gradient**. **D101 gate NOT met
  (WT1 & WT3 null) → exit-cost/complementarity layer PARKED**; hysteresis paper remains a scored rival with no
  demonstrated footprint.
- **DT battery** (`dt_2026-11-20/`, predecl sha256 `6ed67b82…`; deterministic, 10/10 SHA verify): **DT1 NULL** (median
  income-partial ρ = +0.0146 vs raw +0.3867; 2/5 countries; n = 91 / 5 cty — thin); **DT2 NON-NULL** (`E_entrant`
  b = +1.6054, p = 0.00036; gap0 = 0.204× E; n = 241 / 25 cty; reproduces the on-disk D1 coefficient to 2e-16; partly
  arithmetic); **DT3 UNABLE/HELD** (no behavioural/reform data; no number); **DT4 NULL (falsifier)** (partial ρ = +0.202
  < 0.40; bottom-half reversal 18.2% < 40%; depth proxy duration-sign-sensitive); **DT5 NULL (falsifier)** (joint 58.3%
  ≥ 50% but PHL residual z = −0.508 > −1.0; robust to ECI/completion measure; near-circular). **D104 gate NOT met
  (DT1 null ∧ DT2 non-null) → induction grounding PARKED; Amendments A1/A3 remain declared assumptions, no theory
  citation, no model change.**
- **Consequence for the queue:** neither theory paper earns a model layer. The next builds stay: **v1.3 shadow module**
  (the user's "shadow must show up"; W2's frozen design is ready), **v1.2.1 NER object** (W4, in progress) so HKG
  becomes runnable at the model interface, and then **A3 demand-signal implementation**. The HKG *run* still requires
  an explicit Council authority decision (SR-9).

### f) v1.2 revision R2 (disclosed post-run fix — labelling only, no check impact)

After the v1.2 delivery was committed, W1 applied two **disclosed** fixes (`TUNE_LOG.md` D5–D6): (D5) the tertiary
row's `work_final`/`neither_final` labels were set to 0/0 because the four-state block is a **child** block and
tertiary is an adult decision — the earlier 1.0 `oos_neither_share` was a label error, not a result; (D6) the manifest
gained a `results_sha256` block (contract completeness). **Controller verification:** the only panel column that
changed is `oos_neither_share` (1,680 tertiary rows); `reproduction_checks_v1_2.csv` and
`reproduction_checks_detail_v1_2.csv` are **byte-identical** to the committed versions; the revised code re-runs
**two clean times byte-identical to the delivered files**. No parameter, threshold or check value changed.

### g) v1.2.1 NER output object DELIVERED (W4) — HKG interface blocker cleared with a declared limitation

- `synthetic_2026-11-20/generator_v1_2_addendum/` (predecl sha256 `aa756f8b…`): adds NER columns to the frozen v1.2
  panel by **age-structure derivation**, `ner_L = 100 × admitted_official_L / cohort_L` (v1.2 does model the official-
  vs over-age split; the numerator is the model's official-age admission, not a declared share). Panel 6,720 rows,
  67 old columns unchanged, 10 appended; two addendum runs byte-identical.
- **Invariance 3/3 PASS:** v1.2 code re-runs twice → all three result CSVs byte-identical to delivered; addendum output
  preserves rows/keys/columns; `enrolment = admitted_official + admitted_overage` and `ner ≤ ger + 1e-6` 0 violations.
- **Declared limitation:** this is a **cohort-flow NER analogue** (same denominator as the model's GER), **not the UIS
  stock-based NER** (`NER.1.cp`). It makes the HKG timing test *runnable at the interface*; it does not establish that
  the model's NER is comparable to the observed HKG NER. Smoke test (SYNTHETIC, diagnostic only, no HKG comparison):
  PHL-like primary first-sustained ≥90 = **2007**, ≥95 = **2016**; series not monotone (11 decreases).
- **Consequence:** SR-1 is cleared only in the "an NER object exists" sense; **SR-9 (Council authority) remains
  open** and the HKG run has not been executed.

---

## 3z. Council cycle 13 — WT/DT adjudicated, both gates PARKED, SR-9 granted with conditions, five experiments (2026-11-20 ~23:10)

- **Council brief 021 merged as D108–D113.** WT ACCEPTED (verdicts stand; WT2 annotated **VOID as a paper test** — the
  % growth vs pp comparison is near-vacuous; WT4 SUPPORTED but the worker's "one more year flips it" sentence corrected:
  under the ≥3-consecutive rule it would take **two** more observed years; the real margins are 2023 clearing the 5 pp
  trigger by **0.496 pp** and 2024 clearing the recovery band by **0.592 pp**; WT5's cross-year ratio recorded as a
  **Council-side authoring error**). DT ACCEPTED (DT4 relabelled **NULL-BY-CONSTRUCTION** — the depth proxy is
  non-monotone; DT1 scoped to its 5-country overlap; DT5 near-circular).
- **Both gates confirmed PARKED:** D101 (WT1 ∧ WT3 not met) → exit-cost/complementarity layer parked; D104 (DT1 null) →
  induction grounding parked; A1/A3 keep their declared label. Both papers remain scored rivals/declared assumptions.
- **v1.2 recorded as PASS-CONDITIONAL** with three record corrections applied: (i) `m = 1.10` restated as a declared
  **convention** (window ≈ 1.09–1.11; m=1.05 → primary 2022 FAIL; m=1.12 → upper 78.03 FAIL), and the cross-year
  "1.136 (upper 2018)" ratio **removed** from `generator_v1_2/FINDINGS.md` (the admissible same-year ratios are
  0.925 / 0.901 / 1.094 / 1.045); (ii) `MODEL_ARCHITECTURE.md` Amendment A4 relabelled from "theory-grounded" to
  **"candidate grounding — PARKED per D104; no theory citation"**; (iii) `hkg_transfer_2026-11-20/HKG_SR2_PATH_NOTE.md`
  fixes the SR-2 path to `generator_v1_2/` (frozen predecl untouched).
- **SR-9 ruling: AUTHORISE-WITH-CONDITIONS (H1–H6).** The HKG diagnostic transfer may run only when: **H1** the
  cohort-flow NER analogue passes the construct-equivalence test (|stock−flow| ≤ 2.0 pp in every year with the analogue
  ∈ [85,95], and first-sustained crossing years differ ≤ 1 y; else `BLOCKED-MEASURE(SR-1)`); **H2** v1.2.1 addendum
  delivered as a full artifact; **H3** SR-2 recorded PASS-CONDITIONAL (no HKG file may say "v1.2 passes"); **H4** declared
  D7–D9 inputs pre-tabulated/hashed before the run (not referencing 1974/1979); **H5** D75 six constraints + scaling-FAIL
  banner + closed verdict set (`TRANSFER-HOLDS`/`TRANSFER-FAILS`/`FAIL-RE-FIT`/`BLOCKED-*`, never PASS); **H6** scope
  (timing only, primary NER only, 1974/1979, ±5 y). **TRANSFER-FAILS is the informative outcome.** No run executed yet.
- **Five anchored experiments adopted (D112):** **CEIL-ATTRIB #1** (dispatch in progress), **A3-D #2** (dispatch after
  CEIL-ATTRIB), **M1-NER #3** (dispatch in progress — the H1 gate), **A3-S #4** (= the v1.3 shadow build), **ASYM-K #5
  drop-first** (not dispatched). **D113 process rules:** anchoring-block numbers must be re-derived from disk before
  freeze; the paper-test series is **terminated for this phase**.

### h) EXP-1 CEIL-ATTRIB and EXP-3 M1-NER executed — ceiling reclassified to pipeline; HKG measure gate fails

- **CEIL-ATTRIB** (`ceil_attrib_2026-11-20/`, predecl `ed9b31b9…`, deterministic, 24/24 SHA verify): **Test A = MIXED**
  (mechanism ablations move synthetic upper UIS 2024 by +2.64 / +6.27 / −3.47 pp — all ≥2 pp — but calibration knobs
  also move it by −3.48 / +2.08 / −7.56 pp, so neither the mechanism-carried nor the calibration-carried clause holds);
  **Test B = PIPELINE-CONSISTENT** (observed PHL `upper_t / lower_{t−3}` in [0.90,1.10] in **7/8** pairs). **Overall:
  `PIPELINE-CONSISTENT`** — the observed upper-secondary ceiling is what a **lower-secondary pipeline one stage
  earlier** would produce; **D63 reclassified from "upper gate" to "lower pipeline", still `UNABLE` as to cause**.
  **v1.2's "the mechanism produces the ceiling" is not licensed** (Test A mixed); the ceiling is not declared a
  calibration artefact either. No re-fit, no direction claim.
- **M1-NER** (`m1_ner_2026-11-20/`, predecl `9eb35a92…`, deterministic, 16/16 SHA verify): **H1 NOT ADMISSIBLE** —
  band max |stock−flow| = **2.685 pp** (>2.0; 7/15 band years fail); crossing differences **3 y** (≥90) and **2 y**
  (≥95) (>1 y). The cohort-flow NER analogue **leads** a stock-style object by 2–3 years — the flattering direction.
  **Consequence: the HKG diagnostic transfer must return `BLOCKED-MEASURE(SR-1)`; D111's authorisation is void for this
  object; a future HKG attempt needs a NEW predeclaration with a stock-style NER object and a new Council decision.**
  Recorded in `hkg_transfer_2026-11-20/HKG_H1_OUTCOME.md` (frozen HKG predecl untouched). Reference-only observed
  crossings: HKG ≥90 1974 / ≥95 1979; PHL ≥90 1981 / ≥95 none by 2025.
- **v1.3 current state re-verified and re-committed** (the earlier batch captured a mid-build snapshot; the
  worker's final thresholds fix and bug disclosures are in `TUNE_LOG.md`; two clean re-runs byte-identical to delivered;
  the shadow-off ablation still reproduces the v1.2 panel byte-for-byte — c6 no-re-fit guard holds). **c4 FAIL stands**
  (c4a HKG level 0.340 vs band [0.75,0.95]; c4b gap 0.0967 vs 0.10) — the declared shadow parameterisation does not
  reproduce the HKG anchor.

### i) EXP-2 A3-D demand core executed — **block checks failed (specification failure), A3 block PARKED — demand is NOT falsified**

- **`generator_v1_4_demand/`** (predecl `9ed0cae3…`; deterministic; no-re-fit guard PASS: demand-OFF panel byte-identical
  to the frozen v1.3 panel `47d4b082…`, and a placebo arm reproduces it exactly). **Verdict: FALSIFIED — the demand
  block does not replace the upper-secondary taste parameter.**
- **d1** (+10% gross E[R] → 2020 upper demand): HKG **+1.52**, KHM **+4.77** PASS; **PHL +0.15 FAIL** (share at bound
  0.99); sign ≥0 in all 103 scored cells. **d2** (R→2R gate demand): HKG +2.47, KHM +10.33, **PHL +0.23 FAIL**; shadow
  +31.1/+32.6/+32.0 pp (structural). **d3** (office − mfg twin at equal graduate flow): **−0.58 pp vs +2.0 bar FAIL**.
  **d6** identities 0/6,720 PASS. **Replacement test: upper UIS 2024 = 95.05 vs 76.64 → +18.05 pp outside [73,77],
  NOT DEMAND-ROBUST** (reported, not re-tuned). **Ablation: +18.41 pp ≥ 3.0 → NON-DECORATIVE** (the block matters by
  destroying the ceiling). Migration/remittance channel DECLARED/NOT-VERIFIED and tiny (−0.09 / +0.29 pp).
- **Structural finding:** the model's `P(advance) ≈ 0.999` at the upper gate (unrationed; advances include over-age
  admissions) → the gate-probability channel is **near-inert**. This is consistent with CEIL-ATTRIB's
  **pipeline** reclassification: the ceiling is **not a demand-rationed gate**.
- **Disposition: A3 demand core PARKED; no demand layer wired; the ceiling remains a declared taste parameter.** The
  block's non-trivial ablation effect says the *specification* is wrong for the object, not that demand is irrelevant —
  a new predeclaration would be required. Council decision D116.

**USER CORRECTION (Lead-recorded, dashboard):** the word "FALSIFIED" refers only to the predeclared A3-D block
checks. **Demand is revealed and strong** — shadow education, queues/competition for good schools, closure reactions,
credential chasing. Because the model's upper gate is **unrationed** (`P(advance) ≈ 0.999`), a demand channel attached
to it is inert by construction: the correct label is **"the unrationed single-gate model cannot represent a bimodal
system"** — a **model-specification failure**. Successor: **Amendment A5 / v1.5 BIMODAL-GATE** (two-tier gates +
explicit outside option + binding rationing at high gates + shadow re-anchor). Corrections also appended to
`generator_v1_4_demand/FINDINGS.md` and `generator_v1_3/FINDINGS.md`; no re-tune of A3-D.

---

## 3ab. USER STRUCTURAL CORRECTION (dashboard, 2026-11-20) — bimodal system, not a single gate; Amendment A5 / v1.5 BIMODAL-GATE

**The correction (recorded verbatim in intent):** the Philippine pattern is **bimodal within the same system** — low-cost,
if not free, seats go **untaken** by families choosing out of education at upper-secondary (starting at lower-secondary),
**at the same time as extreme competition at the gates**. That coexistence is the object. **"Demand falsified" is banned
language**; the A3-D result is **"the unrationed single-gate model cannot represent a bimodal system"** — a
model-specification failure.

- **`MODEL_ARCHITECTURE.md` Amendment A5** now records the first-class requirement: **two-tier gate structure** (open-access
  low-cost seats that can go unfilled + rationed high-quality gates with queues/rank/shadow competition), **explicit
  outside option** (v1.2 childworld four-state block: work/child labour/informal/migration), **sorting** by
  income/ability/taste, **returns differing by tier**, and **tier-specific exit cost** (cheap to exit the open seat and
  people do; expensive to exit the credential gate and nobody does) as a **WT-adjacent** question for the Council —
  not a re-opening of D101.
- **v1.5 checks (to be frozen before any run):** (a) untaken low-cost seats AND high-gate queues in the same
  system; (b) primary near-universal while upper-secondary stalls; (c) shadow concentrated at high gates, low at the
  open tier; (d) the PHL ceiling emerges from sorting/quality/outside-option **with no free taste parameter**; (e)
  no-re-fit guard (bimodal block off ⇒ reproduce the current panel byte-for-byte).
- **Data:** true seat utilisation/quality is **not on disk** → **HELD DATA ASK** (DepEd/CHED seats vs enrolment,
  private/public shares, SHS voucher take-up). Until then only **declared proxies** on disk (enrolment vs cohort,
  PTR/capacity, private share), labelled DERIVED, with their distortion stated — never invent utilisation numbers.
- **Record corrections applied** to `DECISIONS.md` D116, `generator_v1_4_demand/FINDINGS.md`,
  `generator_v1_3/FINDINGS.md`, and the CHANGELOG: the A3-D verdict word refers only to the predeclared block checks;
  demand is revealed and strong; no re-tune of A3-D; no fitting to the known outcome. The next step is a **frozen v1.5
  predeclaration** (`v1.5 BIMODAL-GATE`), to be written before any run, after the Council cycle-14 slate is merged.

---

## 3ac. Council cycle 14 merged (D117–D123) + user corrections and macro-principle recorded (D124–D125); v1.5 BIMODAL-GATE queued

- **Council brief 022 merged as D117–D123.** All four model-line verdicts **stand, no re-runs**: EXP-1 CEIL-ATTRIB
  ACCEPT-WITH-CONDITIONS (Test A MIXED; Test B PIPELINE-CONSISTENT 7/8, band effectively one-sided, pass carried by
  2003–2017; generator ratio >1.10 in 12 anchor-type years); EXP-2 A3-D FALSIFIED **narrowed** (PHL failure is a
  **saturation artefact**, share 0.9925 at bound pre-perturbation; the substitution used the school-gate probability
  ≈0.999 rather than the **rung-4 absorption ≈0.151** — a 6.6× domain error; \\\"demand does not respond\\\" narrowed to
  \\\"the replacement drives PHL to the bound\\\"); EXP-3 M1-NER ACCEPT clean; A3-S/v1.3 ACCEPT-WITH-CONDITIONS (c4a
  informative, c4b not informative at its 0.0033 margin). Dispositions: A3-D parked CONFIRM; pipeline reclassification
  **CONFIRMED AS LOCATION with corrected wording** (object = transition ratio `upper_t/lower_{t−3}`; one admissible
  numerator, GER not substitutable); HKG `BLOCKED-MEASURE(SR-1)` terminal CONFIRM.
- **New disclosures recorded:** (V1) **v1.2 is crossing/endpoint placement, not a path** — within ±5 pp in **9/33**
  year-level comparisons (median lower −29.44, upper −27.59; 2024 upper +1.61); label restated in **D119** (no file may
  say v1.2 reproduces the PHL series). (V2) **The generator has no cross-level linkage**: synthetic
  `upper_t/lower_{t−3}` >1.10 in **12 anchor-type years** (all 2013–2024), **177/1,590** cells, max 1.444 vs observed max
  1.072 — no ceiling it produces is inherited. (V3) the school gate rations at **primary 87.4% / lower 93.3%** of
  level-years but **upper 6.5% / tertiary 0%** (anchor upper gate unrationed, Q = 0.621 PHL-like). (V8) the binding
  queue is **rung-4 absorption ≈0.151**, not the school gate ≈0.999. **Record items fixed:** the +18.05 (above band)
  vs +18.4064 (vs baseline) distinction; v1.4 `SHA256SUMS.txt` path defect (regenerated, 38/38 verify); v1.3 copy hash
  `bdb205b2…` vs **binding** spec `cf8c61cb…`.
- **Next model line (D121):** object = the **transition ratio**, first move = a **declared cross-level accounting link**
  `upper_t ≤ κ·lower_{t−3}` with **κ = 0.949 declared from an observed median (never fitted)**; no new layer
  (D116 stands); sequencing **EXP-7 → EXP-6 → EXP-8 → EXP-9 → EXP-10**. EXP-7 REPRO-PATH **dispatched** (it gates any
  downstream predeclaration, D119).
- **User corrections recorded (D124–D125):** (a) **no \\\"demand falsified\\\" language** — the correct label is \\\"the unrationed
  single-gate model cannot represent a bimodal system\\\"; demand is revealed and strong; **Amendment A5 / v1.5
  BIMODAL-GATE** is now a first-class requirement (two-tier gates: open-access seats that can go untaken + rationed
  high-quality gates incl. the rung-4 credential queue; explicit childworld outside option; sorting; tier-specific exit
  cost; v1.5 checks a–e; true seat utilisation = **HELD DATA ASK** (DepEd/CHED seats vs enrolment, private/public shares,
  SHS voucher take-up), declared proxies only, labelled DERIVED). (b) **The user's macro-principle — the ONE-WAY
  RATCHET (\\\"there is no reverse button\\\")** recorded as **DECLARED-THEORY (never evidence)** in
  `synthetic_2026-11-20/THEORY_FRAME.md` and `MODEL_ARCHITECTURE.md` A4: transition rules irreversible by declaration;
  no reverse/reversal term; shocks only as declared inputs; options path-created. Stronger than the hysteresis exit-cost
  asymmetry (exit cost is *why* the ratchet holds). **Honest bound:** our data show **setbacks without reversal** (PHL
  upper-sec 2017→2022 −8.16 pp, recovery to 75.03, never ≥90; WT4 zero sustained exit episodes, descriptive/fragile)
  — a bounded observable implication, **NOT** a test of the strong claim, which is **untestable on our data**; any
  reversal diagnostic must be predeclared and labelled descriptive. The Manila→hill-tribe examples are thought
  experiments and must not be modelled literally.
- **DOMUS noted but not integrated** (separate programme workspace; no action).

### j) EXP-7 REPRO-PATH executed — v1.2 is ENDPOINT-ONLY; the κ-link is valid and the pipeline must be built into v1.5 (D126)

- **`repro_path_2026-11-20/`** (predecl `74f9d0e0…`; deterministic; baseline guard PASS): **leg A = `ENDPOINT-ONLY`** —
  **9/33** year-level comparisons within ±5 pp against the predeclared **≥17/33** bar; medians **−4.30** primary /
  **−29.44** lower / **−27.59** upper; worst miss upper 1999 **−36.62**; no missing synthetic cells and no substitution;
  independently reproduces Council V1. **Leg B: κ-link VALID** — κ = **0.949** (median of 8 observed PHL pairs; declared,
  never fitted); **20/53** violations before projection → **0/53** after; baseline unlinked arm byte-identical to the
  frozen panel `14729c51…acf5ac`; outcome class **b2** (linked upper 2024 **63.97** vs unlinked 76.64, delta **−12.67
  pp**; sensitivity κ = 0.960 unchanged).
- **Consequence:** **the pipeline link must be built into v1.5**; the v1.5 BIMODAL-GATE predeclaration (in production
  now) carries κ = 0.949 as a declared constraint + the two orthogonal guards (bimodal OFF + κ OFF ⇒ v1.3 panel
  byte-identical; bimodal OFF + κ ON ⇒ linked arm). No re-fit; v1.2 scope (D119) unchanged.

### k) EXP-7 implication for v1.5 (Lead-recorded) — κ structural, no endpoint carry-over

- The κ-link as a **post-processing projection** proves overshoot (20/53 → 0/53) but **does not make the upper level
  inherited**. **v1.5 must build κ structurally** — a declared system input evaluated **each year** inside the generator's
  accounting, not a panel censoring.
- **v1.2's 2024 upper endpoint (76.64) may NOT be carried into v1.5 as a ceiling target**: under the declared link it
  falls to **63.97** (ratio 2024 = 1.136955; implied required lower-2021 = 80.76 vs generator 67.41 — **the lower series
  is the defect**).
- **v1.5 level claims must be scored on the path** (counts over observed cells, D119/EXP-7 leg A), not a single endpoint.
- Recorded in `MODEL_ARCHITECTURE.md` A5 addendum 2; the v1.5 design deliverable will be checked against this before its
  predeclaration is frozen (a pre-run S1 amendment is legitimate if needed).

### l) Amendment A5 / v1.5 BIMODAL-GATE predeclaration FROZEN — run-ready, NOT RUN (D127)

- `synthetic_2026-11-20/generator_v1_5_bimodal/` (predecl sha256 **`7178e3d2…`**, 32/32 SHA verify; no results dir, no
  RNG). **Tier O** open low-cost places whose take-up is a utility equilibrium; **unfilled places are a primary object**
  (no reallocation to Tier H). **Tier H** rank-rationed, carrying **both** the school gate and the **credentialed-job
  rung (p4 ≈ 0.151)**. Outside option = frozen childworld four-state block. **κ = 0.949 in-loop admission cap**
  (declared, never fitted). **One-way ratchet** = three declared absences, no reversal term, **no reversal diagnostic**.
- **Checks frozen** (a)–(e) with thresholds; **two orthogonal switches / four arms** (A00 no-re-fit guard must
  reproduce the v1.3 panel byte-for-byte `47d4b082…`; A01 linked arm reported separately; A11 scored).
  **Pre-freeze arithmetic (declared, not results): κ×67.4073 = 63.9695, so check (b) is expected MIXED**; check (a) is
  a declared **representation** check.
- **HELD DATA ASK:** DepEd/CHED seats-vs-enrolment by track/region, private/public shares, SHS voucher take-up,
  utilisation/quality — not on disk; declared proxies only (DERIVED, distortions stated). **Scope honesty:** the current
  stack already has 0.1418 spare upper places plus a binding job gate, so "bimodal" is scoped to **three declared
  absences**, not literal absence.
- **Not run.** Parks stay intact until the v1.5 build/run (next worker job). No re-tune of A3-D; no fitting to the known
  outcome.

### m) EXP-6 PIPE-LOO — the transition ratio IS a (weak) system object; κ must be per-system (D128)

- `pipe_loo_2026-11-20/` (predecl `97033df0…`; deterministic; 13/13 SHA). **Verdict `PREDICTIVE (3/4)`** — exactly at the
  declared boundary. LOO prediction of `upper_t` from the median of the other pairs × `lower_{t−3}`: **PHL** n=8, median
  |error| **1.50 pp**, **87.5%** within ±5 pp PASS; **KOR** n=19, **0.48 pp**, **89.5%** PASS; **KHM** n=11, **2.17 pp**,
  **90.9%** PASS; **CHN** n=5, **14.48 pp**, **0.0%** FAIL. 43 pairs (8/19/11/5); 16 upper years dropped by rule;
  HKG/JPN zero-pair non-entrants.
- **The declared κ must be PER-SYSTEM:** PHL **0.949**, KOR **0.990**, KHM **0.595**, CHN **0.722** — a single κ = 0.949
  misstates KHM by ~0.40. Caveats: thin and uneven (KOR near-vacuous at saturation; CHN fails systematically, ratio
  0.645→0.966 during expansion; PHL carried by 2003–2017). D63 stays `UNABLE`; no causal/direction claim.

### n) EXP-8 GATE-LOCUS — the generator's school gate binds at the FLOOR; the upper-gate line is CLOSED (D129)

- `gate_locus_2026-11-20/` (predecl `a8566fbf…`; deterministic; 25/25 SHA). Per level (n=1,680 country-years), share
  `p_off < bar` & `rationed_official > 0`: primary **79.11% / 87.38%** (0.95/0.99 bars) **GATE BINDS**; lower-secondary
  **91.31% / 93.33%** **GATE BINDS**; upper-secondary **4.70% / 6.55%** **UNRATIONED**; tertiary **0.00% / 0.00%**
  **UNRATIONED** (accounting identity, flagged). Anchor type upper `p_off = 1.0000`, `rationed_official = 0` in all 56
  years; **no binding school gate at any level by 2024**; rung-4 absorption p4 = 0.068/0.110/0.166/0.185 (2010+ median
  **0.151**; panel 0.507). **Falsifier NOT tripped** (0/1680 upper, 0/1680 tertiary below 0.50; 0/60 series) →
  architecture not reversed; **the "ceiling as upper gate" line is CLOSED**; A3-D's d2 and A3-S's c4a are
  **explained, not reopened**; **EXP-9 dispatched** (dispatch-eligible). Disclosed caveat: v1.3 gate panel disagrees at g3
  (PHL-like pi0 0.43–0.71) vs flow tertiary p_off ≡ 1.0 — secondary leg only.

### o) EXP-9 RUNG-PROB — `NOT DEMAND-DERIVABLE`; the A3 demand line is KILLED (D130)

- `rung_prob_2026-11-20/` (predecl `1cd399dd…`; deterministic, two runs byte-identical; 21/21 SHA). **Arm A**
  (`P = pi0(g2) ≈ 0.999`): upper 2024 = **95.04548615** (16.05 above 79), ablation **+18.4064 pp** → NON-DECORATIVE.
  **Arm B** (`P = rung4_emp/rung4_demand`, anchor median 0.151): upper 2024 = **42.1256243** (28.87 below 71), ablation
  **−34.5135 pp** → NON-DECORATIVE. **Overall `NOT DEMAND-DERIVABLE` — both arms outside [71,79]; the falsifier fires;
  the A3 demand line is KILLED, not parked; the taste parameter is irreducible without a fit.** Baseline guards PASS
  (G1 OFF = v1.3 panel `47d4b082…`; G2 unmodified arm-A ON = frozen v1.4 panel `ffecd450…`, both byte-identical).
  A3-D's FALSIFIED verdict stands; no re-tune/fit; migration/remittance DECLARED/NOT-VERIFIED and unused; "demand
  falsified" language remains banned (the *specification* failed).

### p) v1.5 BIMODAL-GATE BUILT AND RUN — representation works, level FAILS, two implementation defects disclosed (D131)

- `generator_v1_5_bimodal/` (frozen predecl `7178e3d2…` verified before/after; controller re-ran the model twice and
  reproduced the delivered panels byte-for-byte; 84/84 SHA from programme root). **Verdict: a=MIXED; b=FAIL; c=MIXED;
  d=FAIL; e=MIXED; ALL=FAIL.**
- **Representation (the user's structural point) works:** for SYN00_PHL_LIKE in **all 15** scored years 2010–2024,
  **Tier O upper-secondary unfilled share 0.648–0.932** coexists with **Tier H queue ratio 1.29–1.93** and
  credentialed-job absorption **p4 ≈ 0.25**. Checks a-i/a-ii/a-iii hold; only a-iv (A01 contrast leg) fails and that leg
  is **mislabelled in the frozen predecl** (A00 has same_level 0; A01 has 15 because the κ cap creates same-level counts).
- **Level FAILS:** declared Tier O quality (`q_O_mult = 0.55`) drives Tier O survival ≈0.48–0.51 → **primary completion
  51.63** (never ≥90) and **upper 33.68** — a collapse, not the predeclared stall. **(d) FAIL:** child-wage substitution
  has the **wrong sign (+1.081 pp vs ≤ −2.0 required)** even though the no-free-taste audit (0 hits) and the quality
  sensitivity (−20% → unfilled +11.22 pp) pass. **(c) MIXED:** placement ratio 33.2 and D_O 0.0077 pass; open-tier gap
  +2.16 pp > the ≤+1.0 pp bar. **(e) MIXED:** **A00 guard PASS (byte-identical v1.3 panel `47d4b082…`)**, frozen 20/20,
  determinism PASS, κ violations 20/53 → 0/53 — **but the in-loop κ cap breaches the cell-identity guard**
  (`KAPPA-GUARD-FAIL`: A01 secondary columns `ptr_system`, `D_cohort` differ from A00).
- **A01 linked upper 2024 = 55.657** (satisfies ≤63.9695 but 8.31 pp below it: the cap bounds the **entry cohort**, and
  upper survival is 0.870); **required lower-2021 = 80.76 vs generator 67.41** — the lower series is the defect.
- **Disposition:** model class admitted for the **representation** purpose only; level not reproduced; the κ-in-loop
  implementation needs a design fix (bound the right object without breaching cell identity); the child-wage
  substitution sign is wrong. No rescue, no re-tune. Parks stay parked; A3 line KILLED (D130); D63 stays UNABLE.

**v1.5 post-run disclosures (added after the first report; no re-score):** (i) the outside refusal set used is
`max(U_work, U_neither)` — `U_both` is a *school* state and as an outside value dominates Tier O in **15/15** cells every
year (published per cell in `both_would_dominate_cells`), which would drive `T_O ≡ 0`; the two no-place outside states
were used and the affected-cell count published, not silently dropped; (ii) outside option evaluated at each cell's own
income; (iii) **tertiary has no tier-choice equilibrium** (frozen child block undefined at L=3) → carry-forward
declared; (iv) `D_O` year-invariant by construction; (v) κ-binding reduction order over-age → Tier H → Tier O (cap never
manufactures unfilled Tier O); (vi) **process error B1:** the pre-run SHA snapshot was overwritten by smoke runs, so
`FROZEN_BEFORE_SHA256SUMS.txt` is a reconstruction of 33 recorded pairs (30/33 match; original hash `89638b39…` recorded
in the manifest/guard). Verdict string unchanged; no threshold altered.

---

## 3ad. Council cycle 15 merged (D132–D137); EXP-10 stock-NER design delivered; HKG DEFER-HKG

- **Cycle 15 adjudicated** the model-line batch: all five verdicts stand, no re-runs. **EXP-6** PREDICTIVE 3/4 at its
  exact boundary — **κ is PER-SYSTEM: PHL 0.9491 / KOR 0.9898 / KHM 0.5950 / CHN 0.7222** (single κ overstates KHM by
  0.354; CHN not forward-usable); **EXP-7** ENDPOINT-ONLY with the κ-link b2 (63.97 is an **admission-cohort bound**, realised
  endpoint 55.66); **EXP-8** floor gate binds, upper-gate line **CLOSED** (falsifier measure-dependent, disclosed);
  **EXP-9** NOT DEMAND-DERIVABLE → **A3 line KILLED** (model-side only; banned phrasing stands); **v1.5** admitted for
  **REPRESENTATION ONLY** with four defect rulings.
- **D134 defect rulings (binding on V16):** (1) the κ cell-identity **guard was mis-specified** — unsatisfiable for any
  binding link; fix = bound completion units with survival explicit + declared projection order + counterfactual-identity
  guard + one cap register; (2) the child-wage sign test was **structurally unfirable** under a binding cap — re-specify
  the object (test in A10 κ OFF, pre-cap object), not the bar; (3) **Tier O quality collapse** — move the discount to the
  **return/take-up** margin, never grid-search; retire the (b) family for the successor (use ≥17/33 within ±5 pp);
  (4) the a-iv leg was a **pre-run label error** (A00 0 vs A11 15; A01 is κ ON) — FAIL stands, contrast is A00 vs A11.
- **A10/D62 scope:** floor universalization arrives at `seat_coverage` **0.8722** via the declared **phys_cap = 1.15**
  convention — claim conditional until FLOOR-CLOSE. **D63** gains an observed-side necessary condition (not a cause):
  under κ=0.9491 upper 90 needs lower(t−3) ≥ 94.827; observed lower max 92.414 → κ-implied upper max for 2027 = 87.710;
  observed 2024 upper 75.025 sits 1.75 pp inside its own bound.
- **EXP-10 stock-NER design delivered** (`hkg_stock_ner_2026-11-20/`, predecl `6f5d3c16…`, design verdict
  **PRE_DECL-FROZEN**, 20/20 SHA; object = ratio of reconstructed stocks; target never read — G6 AST guard; N2 on both
  SYN00_PHL_LIKE and SYN28; run-ready **not run**). **It landed after cycle 15's cut, so per D120's timing rule the
  reversion fired: HKG = `DEFER-HKG`** (a new Council decision is required to re-open; the frozen design artifact is
  preserved).
- **Next slate (D136):** EXP-11 KAPPA-FWD (#1), EXP-12 FLOOR-CLOSE (#2), EXP-13 LOWER-DEF (#3), EXP-14 V16-REPAIR (#4,
  after 11+13), EXP-15 CONV-REG (#5 drop-first). HELD ask queue complete (D135); no proxy substitution.

### q) EXP-11 KAPPA-FWD — `WINDOW-ONLY`: the per-system transition ratio is a within-window description, not a forward constraint (D138)

- `kappa_fwd_2026-11-20/` (predecl `bda79ac4…`; deterministic; 14/14 SHA). **PHL** slope **−0.000704** (stationarity
  slope passes) but half-median shift **2.13 pp** (fails ≤2.0) → `κ-TRENDING`, hold-out 2/2; **KOR** slope **+0.002875**
  and shift **0.64 pp** pass → `κ-STABLE` but **0/3** forward cells; **KHM** slope **+0.017318** and shift **7.44 pp**
  fail → `κ-TRENDING`, hold-out 1/2; **CHN** reported only (D133). **Aggregate 3/7 within strict bound, 4 violations →
  `BOUND-BREAKS`; falsifier tripped**; verdict invariant across declared readings.
- **V16-REPAIR: κ may NOT be a forward constraint** — only a declared within-window trajectory (never extrapolated) or
  dropped. The D133 per-system register stays the descriptive record, not a projection input.

### r) EXP-12 FLOOR-CLOSE — `ALLOWANCE-CARRIED`; A10/D62 restated conditionally (D139)

- `floor_close_2026-11-20/` (predecl `1db266e2…`; deterministic; 18/18 SHA). **40/40 closing cells carried by the
  declared `phys_cap = 1.15` crowding allowance** — median **84.2%** of the counterfactual log-margin (range 66.5–98.1%);
  places 0/40, demand 0/40. 40/120 cells close (primary 14, lower 19, upper 7, tertiary 0); all 40 on the 1.15·seats
  branch; at `phys_cap = 1.0` capacity < demand in every closure. Anchor PHL primary 2019 coverage **0.872166**;
  Shapley A/P/Q = 0.9285/0.0438/0.0276. S1 nuance: the year-to-year mover is places (34/6/0), the allowance is a
  **standing level**.
- **Consequence:** **A10/D62 "capacity buys the floor" is CONDITIONAL on the declared crowding convention**; no
  capacity-mechanism claim may rest on the floor until measured places/PTR (HELD); **V16 must report `phys_cap`
  sensitivity**.

### s) EXP-13 LOWER-DEF — `JOINT`; the lower series loses 13.35 pp through gate + survival (D140)

- `lower_def_2026-11-20/` (predecl `0ab3a90e…`; deterministic). **Chain identity PASSES** (1.10 × 0.783805 × 0.781819 =
  0.674073117881 vs panel; err 1.91e-11; 53/53 cells). Gap **13.3527 pp**. Shares **convention 0.00% / rationing 49.30% /
  survival 50.70%** (delta 1.40 pp → **JOINT**; literal order would read SURVIVAL-CARRIED, both reported). Gate can close
  alone (a* = 0.939069; REACHABLE-BY-CAPACITY); **survival cannot** (s* = 0.936689 > surv_max 0.91; ceiling 78.46,
  2.30 pp short). Channels are one object (gate = 1.15·cover(2018); surv = 0.91·exp(−0.55(C/seats−1))). Path crosses 80.76
  between 2023 and 2024; 27/30 types short. **Declared limit: the required-state split is not identified** (JOINT for
  weight 0.4666–0.5251). **V16 must fix:** target provenance (80.76 vs observed 80.896, +0.136 pp), both lower channels
  declared together, m frozen 1.10, **scored on 2021 not 2024**, survival ceiling stated, clip boundary declared.

### t) EXP-14 V16-REPAIR — `PATH-FAILED`; the repaired bimodal class is representation-only (D141)

- `generator_v1_6_repair/` (predecl `6a554dc0…`; embedded hash + 26 parameter checks; deterministic; 47/47 SHA).
  **Scored on A10 (bimodal ON, κ OFF, D138): 0/33 observed cells within ±5 pp vs the ≥17/33 bar** (primary 0/11,
  lower 0/11, upper 0/11; medians −16.96 / −34.89 / −39.80 pp), against the **A00 comparator 9/33** (EXP-7 construction
  reproduced → derivation check PASS). Crossings **1/3** (upper passes only because neither crosses). **Representation
  HOLDS** (unfilled 17/30, queue 30/30, both 15/15, same_level A00 0 vs A10 15).
- **All guards PASS:** A00 byte-identical to the frozen v1.3 panel `47d4b082…`; **counterfactual identity 0/598,080**;
  schooling 23,520/23,520; tertiary non-monotone 0; projection order + propagation ledger (0 forbidden in-year economy
  reads; replay 53/53); frozen 17; no-fit audit 0. **C1 child-wage FAIL** (Δ = 0.000000 pp — the 10% shock flips none of
  the 15 discrete cells; sign only at ×1.50 post-hoc, non-verdict); **C2 MIXED** with a **predeclaration-authoring error
  (R5c named A01D for A_H/queue objects bimodal-OFF cannot produce — a-iv class, recorded not rescued)**; **C3 phys_cap
  PASS** (anchor identical across six values; 1.15 past the binding regime); **C4 κ PASS** (enforced 0/53; realised 20→1;
  binds 23/53; WINDOW-ONLY diagnostic); **C5 lower register PASS** (80.76 internal / 80.896 observed; m 6720/6720; clip 0).
- **Disposition:** the repair fixes the guard/projection/lower-register/phys_cap defects but **does not make the
  generator face the observed path** (0/33, worse than A00's 9/33) — the bimodal arm is a **representation-only model
  class**; the observed-path question remains open. The whole recovery is the survival repair (primary 51.63 → 81.25);
  q_O is inert. No re-fit; parks stay.

---

## 3ae. Council cycle 16 merged (D142–D147) — observed-path failure ruled; repair branch closed as artifact; one conditional cell

- **Cycle 16 adjudicated** the slate: EXP-11 AWC (WINDOW-ONLY; κ-STABLE must never read forward-usable; structural
  look-ahead reason added; 3/7 with CHN contributing 0); EXP-12 ACCEPT clean (40/40 allowance-carried; median share
  84.15%; allowance is a **standing level**, year-to-year mover is places 34/6/0); EXP-13 AWC (JOINT; precedence defect;
  split unidentified 0.466649–0.525137; "survival loses 50.7%" and "fix survival only" barred); EXP-14 ACCEPT clean
  execution, **PATH-FAILED stands** (record correction: closest A10 cell is **primary 2013, −15.1463683 pp**; C1 is a
  **resolution failure**; C2 repeated the a-iv error → **capability lint**; the run was **not blind** — a peek biases
  toward passing, so the negative is credible, but no "specified without outcome knowledge" claim may be made).
- **Scope corrections:** **A10/D62** confirmed for the untiered floor gate and **narrowed for the bimodal class** (all
  six phys_cap values identical at the anchor; capacity-bound 3193/6720 at 1.00 → 0 at ≥1.05; 1.15 is past the binding
  regime; the bimodal floor is **take-up-limited**) — **D139 does not carry to the bimodal class**; **D140's
  action-reading** corrected (split unidentified; "fix survival only" barred); V23 denominator rule recorded
  (17/30 cells vs 15/15 years).
- **Next model line: `(a) NARROWED AND CONDITIONAL`.** The observed-path loss is **localised to the participation
  margin** — `demand_official/cohort` **0.900000** vs the frozen block's **0.9956438553**, unfilled Tier O removes a
  further 10 pp (`admission` 0.800000); primary-2024 gap **17.0507 pp** with **survival identical** (0.9233395869) and
  m identical. **Repair branch CLOSED as artifacts** (`v1.5`/`v1.6`: no re-run, no re-tune, no v1.7 with a moved
  number; the "re-specify the tier menu" route CLOSED outright — q_O=1.00 reaches only 3/33). **Observed-path question
  OPEN for exactly one conditional cell (EXP-18)**, VOID unless EXP-16 returns DUPLICATED-PRIMITIVES or MIXED, with a
  **pre-committed decision tree and closing rule**. Two drift flags named (fourth model-build in four cycles; three of
  five slots read-only).
- **Next slate (D145):** EXP-16 PARTPROV (#1, count-blind; decides whether the generator line continues), EXP-17
  JOINT-COVER (#2, one declared λ, adopted nothing), EXP-18 PART-REPAIR (#3, conditional), EXP-19 PLACES-BOUND (#4,
  proxy cell), EXP-20 USE-REG (#5 drop-first; second cut EXP-19). **Four authoring rules binding:** precedence;
  resolution pretest; arm tuple + capability lint; count-blind diagnostics. HELD unchanged (D146); HKG DEFER; D63 UNABLE;
  no proxy substitution outside EXP-19.

### u) EXP-17 JOINT-COVER — `SINGLE-LEVER-IDENTIFIED`; λ* is a REQUIRED-STATE, not an installed parameter (D148)

- `joint_cover_2026-11-20/` (predecl `3394e3f4…`; deterministic; 14/14 SHA). Exactly one root in [0.5, 2.0]:
  **λ\* = 1.11465019198434** (bisection; Newton 5.8e-15 agreement). Implied coverage **0.759712** (2018, +7.81 pp) and
  **0.873523** (2021, +8.98 pp); **(a, s) = (0.8736689, 0.8403433)** product **0.8076**; seats **+190,326 / +213,498
  (+11.465%)**; law max 1.05105; λ_demand 1.218125. Falsifier PASS (|chain − panel| = **1.03e-12**).
- **Scope flag:** λ\* holds where the gate is **capacity-limited** (v1.2 panel); it does **not** transfer to A10's
  participation-limited gate — citable only as **`REQUIRED-STATE (EXP-17)`** with the **`DERIVED`** target **0.8076**
  (internal-consistency, not a policy target/forecast). **EXP-19 inputs:** required seats/cohort 0.759712 (2018),
  0.873523 (2021); observed-reference variant +0.079/+0.090 pp. **No λ adopted.**

### v) EXP-16 PARTPROV — `MIXED`: duplicated primitives at primary/lower, structural at upper; EXP-18 LICENSED (D149)

- `partprov_2026-11-20/` (predecl `d7c81309…`; count-blind; deterministic; 8/8 SHA). P1 (frozen v1.3 outside-option
  primitives substituted unchanged) brings `demand_official/cohort` within **±1.0 pp** in **15/15** years at primary
  and lower-secondary (**gap 0.000000 pp**) → `DUPLICATED-PRIMITIVES`; upper-secondary **4/15** (mean gap 5.992 pp) →
  `MIXED`. P0 comparator gaps 9.568/12.764/5.709 pp; P2 report-only. P1 unfilled-≥0.10 years: primary 0, lower 0, upper
  15. **Count-blind guard PASS** (no observed read, no 33-cell count).
- **D144 tree (MIXED → consistency part only; structural part declared and reported as sensitivity; same closing rule) →
  EXP-18 LICENSED** (consistency-only repair, observed path as the only target, ≥17/33 ±5 pp + ±5 y crossings,
  representation carried forward, A00 guard, counterfactual identity, no-fit audit, count-blind; **closing rule: bar
  missed → generator line closes at representation-only**).

**EXP-16 post-run details (Lead-recorded; no re-score):** P1's participation share equals the frozen block's
**bit-identically in 45/45 level-years** (max Δ 0.0); the **upper residual is the eligibility factor** (0.5973 vs 0.6870
in 2010), not a menu object; **P2** zeroes unfilled 15/15 at primary/lower, survives at upper; **P1 also zeroes unfilled
at primary 12/15 and lower 13/15 — a representation risk flagged for EXP-18's unfilled≥0.10 condition**; count-blind
audit: observed file opened false, 0 bytes read, 1 blocked self-test attempt, own-code AST rule PASS; S-IDENT P0 ≡
frozen A10 at 4.44e-10; determinism 3/3; final SHA256SUMS 14/14.

### w) EXP-18 PART-REPAIR — `PATH-FAILED`; the closing rule FIRES: GENERATOR-LINE-CLOSED at representation-only (D150)

- `generator_v1_7_partrepair/` (predecl `3778afe3…`; deterministic 18/18; 42/42 SHA). The consistency repair was made
  cleanly — participation decision from the **frozen v1.3 four-state block, called unchanged**, **no new parameter
  (110 → 110)**; A17's participation share = the frozen block's own (0.995644 / 0.953477 / 0.800311 at 2024) in
  **45/45** cells. **But A17 still scores 0/33 within ±5 pp** (primary 0/11, lower 0/11, upper 0/11; A10 0/33; A00 9/33
  = EXP-7 construction); crossings 1/3 (upper trivially; primary max **88.66**, lower **80.56**).
- **All guards PASS:** A00 byte-identical `47d4b082…`; counterfactual identity 0/18,480; supply identity 0/53,760;
  repair-in-force 45/45; projection order 0 hits; no-fit 0/26 + 0 band hits; count-blind PASS; deterministic 18/18.
  **What sets the level now:** the declared one-place-per-pupil tier capacity (primary admits exactly seats/cohort =
  0.8629 at 2018) and the upper unfilled Tier-O margin — **both structural, not tuned**.
- **Representation passes at exactly 15/30 unfilled through the UPPER cells only**; lower unfilled → 0 (strict both-level
  coexistence 0/15) — flagged. **Disclosures:** G2 narrowed 16→11 columns (frozen `inject_upper` cannot replay the
  over-age top-up; pre-freeze amendment); capacity sensitivity is a decomposition; `capacity_decomposition` nan beyond
  2025; EXP-16 RESULTS.csv hash recorded-not-enforced (file rewritten at 01:31; DETAIL enforced, verdict rows unchanged).
- **CLOSING RULE FIRED: the generator line closes at representation-only; no successor is predeclared this phase.** The
  programme holds a representation capability, a descriptive per-system κ, a labelled placement instrument, and a
  localised level failure; the level question passes to the descriptive + measurement lines (D144 fallback).

### x) EXP-19 PLACES-BOUND — `PROXY-SILENT`: the required coverage is not observable on disk (D151)

- `places_bound_2026-11-20/` (predecl `22786090…`; deterministic; 16/16 SHA). One declared conversion family from the
  on-disk PHL class-size/PTR/enrolment description, three norm class sizes {40,45,50} **declared and none adopted**, does
  **not** discriminate EXP-17's REQUIRED-STATE (required seats/cohort **0.759712** (2018) / **0.873523** (2021); DERIVED
  target 0.8076; λ* NOT adopted) → **`PROXY-SILENT`**. The required state stays **DECLARED**; the **HELD places ask stays
  HELD**; no norm, path or λ adopted.

---

## 3af. Council cycle 17 merged (D152–D159) — closing record ruled; post-generator line = DESCRIPTIVE-CONSOLIDATION

- **Adjudications:** EXP-16 AWC (MIXED stands; per-level split mandatory; the repair's **price** recorded — P1 zeroed
  unfilled at primary 12/15 and lower 13/15; digest 14/14 not 8/8; RESULTS.csv hash RECORDED-NOT-ENFORCED); EXP-17
  ACCEPT clean (λ* 1.11465019198434; 0.8076 DERIVED; REQUIRED-STATE only); EXP-18 ACCEPT clean execution, **PATH-FAILED
  stands and the closing rule fired** — with three corrections: the surviving representation is **single-tier** (upper
  unfilled 15/15 + queue 30/30, **strict both-level coexistence 0/15**, lower unfilled 0/15); the level localisation is
  **class-specific** (v1.6 participation margin; v1.7 tier capacity — admitted/cohort = seats/cohort =
  0.8628866495 — plus Tier-O margin; D143(viii) "take-up-limited" is v1.6 only); the **size** of the miss is not
  decomposable until CONV-REG (constant m=1.1 vs observed completion/GER crossing 1.0); EXP-19 AWC (PROXY-SILENT =
  **NOT-IDENTIFIED**, never "consistent"; 2/3 norms above; nearest cell may never be cited as corroboration; proxy route
  closed).
- **Closing record (D154):** **correctly closed at representation-only; no successor generator admissible this phase** —
  procedural (the act performed was the act licensed; 110→110; repair 45/45; guards pass), substantive (residual = two
  declared objects; moving either against the observed path is a fit), constitutional (the pre-committed rule closed the
  line, not the Council). Conditions: single-tier representation; class- and phase-specific close (re-entry needs a
  **measured HELD object + a new Council decision**); miss size not decomposable. **Forbidden re-entries named**
  (descriptive/measurement-informed/calibration-free generator, v1.8, new tier menu, any grid search, any re-run/re-score).
- **Post-generator line (D155):** **`DESCRIPTIVE-CONSOLIDATION`, one cycle, deliverable = the write-up**; no generator,
  no proxy, no HKG; **sunset clause**; seven authoring rules (D158).
- **D63 bound split (D153(xiii)):** upper 2024 75.02525329589844 vs 90 = **14.974747 pp**; ln(90/75.025) =
  ln(90/80.896)+ln(80.896/75.025) → **58.6008% pipeline / 41.3992% transition ratio**; required lower at the 2024 ratio
  97.042584 (above record max 92.4139633); required ratio at the record's 2024 lower 0.973879 (inside observed 8-pair
  range 0.889–1.072); D63 stays UNABLE; "the upper-secondary ceiling is structural" barred.
- **Next slate (D156):** EXP-21 CONV-REG (#1), EXP-22 PART-MARGIN-DESC (#2), EXP-23 D63-BOUNDS (#3), EXP-24 KAPPA-WRITE
  (#4), EXP-25 V-SPINE (#5 drop-first; second cut EXP-24). HELD unchanged (D157); no proxy substitution; no experiment
  against a HELD object.

### y) EXP-21 CONV-REG — `REGISTER-BINDING`: one constant conversion is not enough (D160)

- `conv_reg_2026-11-20/` (predecl `1dd86bd1…`, hash enforced pre-input and pre-verdict; deterministic 6/6; 21/21 SHA;
  0 untraceable rows). **4/12 cells INTERCHANGEABLE, 6 NOT, 2 THIN.** PHL primary n=9 0.802546–1.073853, share 0.555556,
  crosses 2021 → **NOT**; PHL lower n=4 0.746209–0.900968, 0.250000 → **NOT**; PHL upper n=6 0.898892–1.093971, 1.0,
  crosses 2017 → **INTER**; KOR lower/upper n=16/19 → **INTER**; KOR primary THIN; KHM all three 0.0 in band → **NOT**;
  CHN primary n=6 1.0 → **INTER**; CHN lower THIN; CHN upper 0.2 → **NOT**; HKG/JPN no completion series.
- **All four interchangeable cells still cross 1.0; CHN's per-level intervals are disjoint.** **m-constancy:** A17 CONSTANT
  at 8.8395202269e-10; v1.3/v1.2 NOT-CONSTANT at 4.7043695535e-02 — **35/6,720 cells cap `completion_uis` at 1.0** where
  1.10×cohort > 1. **Consequence: `m = 1.10` is a point convention on a synthetic panel, not a level convention; every
  level sentence names the object pair and the register line.**

### z) Descriptive slate complete except EXP-25: EXP-22 NO-OBSERVED-COUNTERPART; EXP-23 BOUNDS-EDGE; EXP-24 REGISTER-NARROWED (D161–D163)

- **EXP-22** (`part_margin_desc_2026-11-20/`, predecl `8f47aa21…`, deterministic 6/6, 22/22 SHA) — **`NO-OBSERVED-COUNTERPART`**:
  observed same-year gross−net spans PHL primary n=30 **2.196578–14.627307 pp** (median 10.086482), lower n=4
  **17.412040–29.239540** (not THIN; V35b's THIN note contradicts the rule — recorded), upper n=2 **46.062110–51.704530**
  (**THIN**); EXP-21's register has **0** lines naming demand/choice over a cohort → **NO-REGISTERED-COUNTERPART**,
  placement **WITHHELD**; shares printed beside with `comparison_performed = FALSE`; count-blind PASS; no observed
  same-year span at 2024.
- **EXP-23** (`d63_bounds_2026-11-20/`, predecl `dc714963…`, deterministic, 14/14 SHA) — split **RESIDUAL-SPLIT**
  (58.6008% / 41.3992%; identity residual 1.9e-16; 11/11 reproduction), bounds **`BOUNDS-EDGE`**: B1 **OUTSIDE**
  (required lower 97.042584 vs record max 92.413963, +4.628621), B2 **INSIDE** (required ratio 0.973879 in
  [0.889157309, 1.072442162]), B3 **INSIDE** (implied [82.170551, 99.108631] contains 90); **D63 stays UNABLE**; banned
  sentence 0 hits; caveat — contemporaneous lower pipeline share −0.145443, so **58.6% is a t−3 statement**.
- **EXP-24** (`kappa_write_2026-11-20/`, predecl `db20d123…`, deterministic 4/4, 14/14 SHA) — **`REGISTER-NARROWED`**
  (block label USE-OUTSIDE-WINDOW): register PHL 0.949135 [2003-17/2003-24] slope −0.000704 shift 2.1348 holdout 2/2;
  KOR 0.989758 [2005-20/2005-23] 0.002875/0.6354/**0/3**; KHM 0.594984 [2000-17/2000-23] 0.017318/7.4361/1/2; CHN
  0.722222 [2012-20] 0.041728/25.6573/0 cells; HKG/JPN non-entrant. **309 uses enumerated, 299 applied, 233 in-window
  (77.93%), 64 below + 4 above, 68 barred** — all PHL's in 7 named objects (κ-link 31/53 years outside; v1.5 guards;
  v1.6 audit/panel; 2027 κ-implied sentence in D133/STATUS); **0 load-bearing → NARROWED**; KOR counter-example carried;
  **four fixed sentences admissible; bar the κ-link and 2027 sentences**; no adoption.

---

## 3ag. Council cycle 18 merged (D164–D169) — EXPERIMENT PROGRAMME CLOSED; the write-up is the only open item

- **Adjudications:** EXP-21 **ACCEPT clean** (REGISTER-BINDING; 4/12 INTER, 6 NOT, 2 THIN; m constant A17-only
  8.8395202269e-10 vs NOT-CONSTANT v1.3/v1.2 4.7043695535e-02; 35/6,720 capped); EXP-22 **AWC** (NO-OBSERVED-COUNTERPART;
  identity fails, placement WITHHELD; V35b's THIN note contradicts the <3 rule — corrected to not-THIN per D165(vii));
  EXP-23 **AWC** (RESIDUAL-SPLIT 58.6008/41.3992; BOUNDS-EDGE — B1 outside, B2/B3 inside; 58.6% is a t−3 statement,
  contemporaneous pipeline share −0.145443); EXP-24 **AWC** (REGISTER-NARROWED — 233/299 in-window 77.93%, 68 barred,
  universe 17 of 193 files; **D-2** the `exp11_forward_constraint` column carries a stale `FORWARD-CONSTRAINT-ELIGIBLE`
  value and may not ship; **D-3** the HKG/HELD legs owed by the write-up).
- **EXP-25 V-SPINE: `CLOSED-UNRUN`** (drop-first exercised) — it is the write-up, not a test; handed off as **W-1…W-6**
  under the frozen gate **A-1…A-8**; **no `SPINE-REPLACED` verdict**.
- **Line COMPLETE and sunset DISCHARGED** (D167): four of five deliverables on disk and adjudicated; the fifth is the
  write-up the sunset names. **Experiment programme CLOSED — 0 new cells**, by exhaustion (HELD / data gaps / static
  text / forbidden re-entries); **D89 discharged through the completion branch** (a ruling, not an omission).
- **The write-up is the only open item (D168):** two-object headline + four register appendices + HELD/banned apparatus;
  canonical path `10_massification/lit/PHASE_WRITEUP.md`; deadline before the next Council cycle; **if it does not ship,
  it is a writing failure, not a register**. Phase stays CLOSED at `PARTIAL / DESCRIPTIVE / EQUIVALENT` (D76/D77
  untouched).
- **Record corrections applied:** **D-1** closeout fit range now the 12-arm range **1.0475–3.2917** (fit) /
  **4.0148–6.1222** (holdout), with the "2.03–3.29" identified as the six law/capacity-only arms; **D-4** read-order
  paths fixed and the four registers + write-up order added; **V35b** 4-pair lower level **not THIN**.

---

## 3ah. THE PHASE WRITE-UP IS SHIPPED — `WRITE-UP-GATE: PASS` (D170)

- `10_massification/lit/PHASE_WRITEUP.md` (**726 lines**; canonical; supersedes `PHASE_WRITEUP_SHELL.md`)
  + `10_massification/lit/PHASE_WRITEUP_GATE.md` (**287 lines**; A-1…A-8 self-check): **A-1 PASS · A-2 PASS · A-3 PASS ·
  A-4 PASS · A-5 PASS · A-6 PASS · A-7 PASS · A-8 PASS → `WRITE-UP-GATE: PASS`.**
- **Two-object headline block:** phase object (A1 anchor class, 12 arms, pre-close) = conditional **level** reproduction
  with fit MAE **1.047492271754753–3.2916863270693772** / holdout **4.014780434743067–6.122199101442962**, losing to the
  **4.35 pp** linear trend, observational equivalence, one unreproduced upper-secondary asymmetry, placement **9/33** (and
  a placement is not a reproduction); post-close object (`v1.7 (A17)`) = representation-only, upper unfilled **15/15**,
  both-level queue **30/30**, strict both-level coexistence **0/15**, **0/33** vs the **≥17/33** bar, crossings **1/3**,
  D63 `UNABLE` split **58.6008/41.3992** at the declared t−3 pair.
- **W-2…W-6 + Appendices A–G** as adjudicated: level sentences with the `ger_secondary` trap and T-vs-completion columns;
  participation paragraph with `NO-REGISTERED-COUNTERPART`/placement **WITHHELD**; D63 with the t−3 sentence and
  `BOUNDS-EDGE`; κ with the four fixed sentences, KOR counter-example, 17-of-193 universe, κ-link/2027 barred and the
  stale column not lifted; limits (HELD 14/14, HKG two-part condition, corrected 12-arm range, read order,
  theory-as-declared, parks); four register appendices; banned register B-1…B-28; provenance 21 groups.
- **Integrity:** 30 claims each label·class/object·window·status·one sentence; 79 links (35 unique) 0 unresolved; 4/4 κ
  sentences verbatim; 0 banned sentences outside Appendix F; 748 numeric tokens (218 distinct) all mapped to delivered
  cells; **no model run, no re-run, no re-score, no new number**; the untagged D77 headline occurs **0** times; D76/D77
  applied, not amended; no `SPINE-REPLACED` verdict; **Lead checks the gate**. The phase stays **CLOSED at
  PARTIAL/DESCRIPTIVE/EQUIVALENT**; the experiment programme stays **CLOSED at 0 new cells** (D167); parks stand.

---

## 3ai. MODEL-DEBUG MODE (D171–D174) — ceiling-cap defect fixed; benchmark critique recorded; write-up unedited

- **Contract:** `10_massification/extensions/model_debug_2026-11-21/PRE_DECLARATIONS.md` (sha `748335cf…`, amended
  `7d8bade9…` by **AMENDMENT 1 — measures are different objects**: GER may exceed 100; NER ≤ 100 is definitional; the
  UIS completion rate uses the **older (3–5-years-above-grade)** cohort and is **not bounded by GER**). DEBUG label;
  no reproduction claims; no successor generator; the closed line stays closed except this defect fix; every fix
  justified by the defect, not a result; gate-passed write-up **unedited**. The user's critique is recorded verbatim in
  the contract and the benchmark memo.
- **CAP AUDIT (Agent 1): 34 clamp/ceiling/floor/renormalisation sites — 30 declared conventions / 1 implementation
  artefact / 3 undetermined.** The artefact is **CAP-01**: `clip(m × comp_coh, 0.0, 1.0)` at `sim_v1_3.py:832` (and
  copies), binding **35/6,720 cells on v1.3 and 35 on v1.2, 0 on A17** — all primary, five countries, 2012–2025,
  uncapped **1.000259–1.044678**. **0 of the 35 are legitimate CR > GER cases** (GER = 105 there; CR sits below it);
  the repair must not touch the GER/Z1 gate or add an NER cap. **CAP-04** — an undeclared survival floor **0.02**
  binding **24 tertiary burn-in cells (1970–72)** — is recorded, **not fixed**, and needs adjudication before any level
  sentence is called clean. `generator_v1_2/FINDINGS.md:191` already called the cap "a ceiling artifact of m ×
  cohort-flow clipping".
- **FIX + RE-RUN (Agent 2):** one-sided floor `max(0.0, m × comp_coh)` in **copies** of v1.3/v1.2; every other clamp,
  threshold, seed and draw order untouched; delivered files untouched (12/12 input hashes unchanged). **35+35 cells
  uncapped** (values 1.000258707–1.044677728; only `completion_uis` changes). **(a)** m = 1.10 now **CONSTANT on all
  three** panels (A17 8.8395202269e-10; repaired v1.3/v1.2 9.6646846082e-10). **(b)** the old v1.3/v1.2
  **NOT-CONSTANT 4.7043695535e-02 is wholly cap-induced** (exactly 1/0.9497070256 − 1.10). **(c)** the register counts
  are **unchanged — 4 INTER / 6 NOT / 2 THIN, REGISTER-BINDING** (T is observed completion/GER; panels enter only
  m-constancy). **(d)** **no level sentence changes and zero published-number changes** — affected items are
  **prospective amendments only** (C-13, Table A-1 rows, the "CONSTANT is A17-only" sentence, Table G-1 row 10);
  "35/6,720" remains true of the as-delivered panels. **Determinism 12/12**; measure check: 0/70 repaired cells have
  CR > GER.
- **BENCHMARK NOTE + HANDOFF PACKET (Agent 3/3B):** trend/persistence = **humility floor, not a dynamic test**;
  **0 of 10 inventoried results identify a dynamic** (4 dynamic-type, 6 floor-only); **prospective amendment B-1**
  (`applied = false`); §7 handoff packet quotes the paper's **18 claims line-by-line (0 SHOWN / 3 PARTIAL /
  15 NOT SHOWN)** from `…/DeepSeek/massification_2026-11-20/00_handoff/papers/02_october_massification.md` (377 lines,
  sha `1138d453…`; **not under the programme root**), plus the **arm-vs-trend reading hazard** (`complementary ·
  capacity_gated` hold_mae 4.014780434743067 < `naive_trend` 4.352883341604888; different tables/objects, not
  re-scored), Q-1…Q-7 and the **redesign question recorded, unanswered**. Write-up **unedited**.

---

## 3aj. DEBUG-MODE RULINGS APPLIED (D175) — CAP-04 disclosed; Q-5 resolved; B-1 prospective; handoff packet written

- **CAP-04 (undeclared survival floor 0.02, 24 tertiary 1970–72 cells):** **disclosed, not fixed**; sensitivity on copies
  (floor 0.02 vs 0.00): 2024 endpoints Δ **0.000000 / 0.000000 / 0.000000 / −0.000003 pp** (primary/lower/upper/tertiary,
  anchor), **max |Δ| = 0.000228 pp** across 30 countries × 4 levels, **0 cells > 0.01 pp** → **"burn-in dissipated by
  2024"**; delivered panels untouched.
- **Q-5 resolved — (iii) comparing different tables/objects:** the write-up's **4.352883341604888** is the
  **calibration-table** trend (fit 1980–2010 / hold 2011–2024, n=17); the 12-arm range is on the **anchor** windows (fit
  1999–2013 / hold 2014–2024, n=14). **Like-for-like trend on the anchor windows = 5.614935464535336 pp**; **7/12 arms
  beat it** (best 4.014780434743067) and **5/12 lose** (worst 6.122199101442962) → the class does **not** uniformly lose.
  **Corrected sentence + gate re-run prepared** (`q5_resolution/Q5_RESOLUTION.md`), flagged as a correction,
  **`applied = false`**; no arm re-scored.
- **B-1 prospective** (`applied = false`): trend/persistence = **humility floor, not a dynamic test**; **0/10** inventoried
  results identify a dynamic; recommended as a **one-footnote framing amendment**; write-up unedited.
- **Redesign question:** recorded, **unanswered** (external reviewer); no redesign experiment run/predeclared/dispatched;
  D167 stands.
- **Handoff packet:** `model_debug_2026-11-21/HANDOFF_PACKET.md` — (a) paper two on-disk paths + sha `1138d453…`
  (canonical iCloud path + package mirror; **not** under the programme root), (b) **18 claims: 0 SHOWN / 3 PARTIALLY
  SHOWN / 15 NOT SHOWN** with the binding caveat, (c) CAP-04 disclosure + sensitivity, (d) Q-5 hazard + resolution,
  (e) B-1 note. Lead's external file **not overwritten**. Delivered panels and gate-passed write-up **byte-identical**.

---

## 3ak. BRIDGE TASKS (D176) — ACK verified; A6 label collision; expansion/shadow memos; post sent

- **ACK verified:** `ddfa8a61` (2026-11-21T08:30:37Z, deepseek-massification) present with expected content.
- **A6 reconciliation = LABEL COLLISION.** The sealed package **`fba20146…`** (365 artifacts, six cells, GATE A6
  CLOSED, D77/D86) is the **DOMUS A6** package (F4/C26 bridge, M-H3, A6-PASS, Angkor, FFS, Domus Notes) — **not
  massification**. Codex queue A6 = Massification is an **open assignment** (claimed atlas-models A6–A15,
  `e4a0d7d6`) with no delivered package. **Canonical for massification = our closed phase record**; Domus A6 =
  canonical for Domus; **massabm = fenced external** (`796ff9aa…`/`3d276ec3…`), not the phase record.
- Codex's "first battery collapsed → matched-seed single reversions" = an **Atlas-models/massification battery**,
  not the Domus A6 package and not our massabm; our matched reversions are the **massabm round-2 audit**
  (`adult_age=16` flips −0.072→+0.063; `diploma_by_years` makes K-12 size definitional; per-stage dropout −13.3→−6.5;
  weak pressure valve lets 58–100% of states reform without the architecture). **Rural entry = UNRESOLVED**;
  capacity paths exogenous; **coevolve v0** is the predeclared (unrun-at-post-time) answer.
- **Memos:** `bridge_tasks_2026-11-21/AUDIT_EDUCATION_EXPANSION.md` and `AUDIT_SHADOW.md` (shadow: corpus can
  distinguish stage/gate and KHM provider; **cannot** separate catch-up from exam-prep from expenditure).
- **Post sent:** `53e8585d-ecf1-488a-8fce-1aba106fee28` from `deepseek-massification` to `all` (2026-11-21T10:56:09Z).
  China/Tilly **not adopted** (outside this record).

## 3al. COEVOLUTION v0 (D177) — frozen predeclaration, model built and run, harness-verified; two falsifiers fire

- **Predeclaration frozen before code:** sha256 **`7d25e17631a39f556a17ac62a53de12701d60dca6d09a05e2b080d8d3184799d`**.
  New modelling phase (user brief `coevolve_2026-11-21/DESIGN_BRIEF.md`); three demand objects distinct;
  town+8 villages; household next-year choice with real alternative; **endogenous supply** (no seat totals in
  inputs); four gates; catch-up/gate tutoring with concentration as output; three cohort-feedback responses;
  report cards A/B; coexistence test + 3 one-change counterfactuals + spillback; 8 arms × 3 paired seeds.
- **Build/run:** deterministic simulator (2,370 lines), 128 DECLARED parameters, 24 runs in **17.9 s**; **D0 PASS**
  (release-blocking; tamper test exits 3); determinism byte-identical; **report card A PASS** (8,640 cells, 0 identity
  violations; NER ≤1; max GER 0.907; 2,484 values recomputed to 3e-10).
- **Results (harness-corrected):** **COEXISTENT 32/36 baseline cells** (12/12 seed 20261121; 10/12 others; binding leg
  = gate-household share 0.203 vs 0.20); **two peaks = years completed** (0 yrs 29.5%, 6 yrs 28.5%); selective track
  **near-empty** (41–71 pupil-years, 4–6% of places — criterion (c) is a gate queue, not demand). **`SAME-RESPONSE`**
  (all three arms argmax **village poor**; gains +0.110/+0.183/+0.030; r=0.9907) and **`NO-SPILLBACK`**
  (+5.14/+0.66/−6.39 pp; 0/3 seeds clear 5 pp; control-village string-vs-int bug ≈8% dilution). **Report card B:**
  mandate +1.83 yrs, fees +0.37, degrees +0.06 but **`ARM-NOT-TESTING-GLUT`** (g0=0.20 > own share 0.111–0.115;
  requirement channel inert). **Harness: 21 PASS, 0 FAIL, 11 descriptive.** Limitations disclosed (sample-only
  per-cell check r=0.965; OOS = "out of level"; 624 truncated-band cells; 24 NaN literals in RUNS.json; four pre-suite
  bug fixes disclosed; no post-result changes). **No observed data, no country/causal claims, no fitting; closed
  records untouched; Q-5 correction and B-1 footnote remain `applied=false`.**

---

## 3am. YANG FACTORY TOY v2.1 + PARAMETER MONTE CARLO (D178) — `ACTIVE`, robust in 68.3% of draws; wage premium is the driver

- **v2.1 cleanups (no parameter/threshold changed):** explicit factory/formal/informal/farm classification (replaces
  `formal()`), `unfilled = POSTS − factoryJobs`, pre-shock y=20–22 match check **PASS**, saved grid output, two runs
  byte-identical; Lead's working copy preserved. **Grid 200 seeds** (4,800 runs, 12.7 s): completion gap vs `none`
  **0.000/+0.005/+0.192/+0.531/+1.226/+1.652** (50k→2m); **predeclared falsifier `ACTIVE` at 3/6 sizes** (500k
  marginal 0.531). `yang_endog` raises gaps at every size.
- **MC contract frozen** (`MC_PRE_DECLARATIONS.md` sha `6f9d8c35…`): **1,000 parameter draws × paired seeds {0,1,2} ×
  sizes {50k,200k,500k,1m,2m} × designs {none,yang,yang_endog} = 45,000 runs**, draw seed 20261121, CRN, pre-shock
  PASS, **two runs byte-identical**, runtime **151.8/155.6 s**.
- **Results:** **robust-ACTIVE 68.3% (yang) / 82.3% (yang_endog)**; **inert 18.1%** (lower factory-wage multiplier,
  higher formal wage; across all three mappings); pooled completion gap **+0.666** (p5 +0.118, p95 +1.385), leaving
  **+0.894**; by size +0.015/+0.337/+0.674/+1.030/+1.274. **Top-3 load-bearing: factory wage +0.784 (71.6% R² share),
  formal wage −0.357 (11.5%), β −0.232 (6.4%)**; Yang slope/anchor nearly inert (−0.036/+0.078). Descriptive, not
  causal. **Recommendation:** wire the same MC + paired-seed test into the coevolution city-size block (predeclare;
  inert set as boundary condition).

---

## 3an. COEVOLVE v0.1-YANG (D179) — `NOT WIREABLE AS SPECIFIED`; no MC run; clean design mismatch reported

- New extension `coevolve_2026-11-21/v0_1_yang/`; **coevolve v0 and its frozen predeclaration untouched**
  (`7d25e176…` verified). **Predeclared feasibility criterion** (`v0_1_yang/PRE_DECLARATIONS.md` sha256
  `3dea4786…`): the requested wiring (g(N) = share of upper-secondary/tertiary gate places carrying a credential
  requirement, existing gates unchanged) is implementable iff some gate applicants **lack** the required credential;
  zero → `INERT-BY-CONSTRUCTION` → STOP.
- **Audit (read-only import of v0; 2 seeds):** selective gate **12,516 applicants / 0 lacking**; university/post-sec
  gate **12,455 / 0**; allocation **447,098 candidates / 0 lacking** in every level → **`INERT-BY-CONSTRUCTION`**.
  Evidence: `coevolve_v0.py:713` advancement requires `cred == c` (via `NEXT_AFTER_CRED`, `:60`), so every gate
  applicant already holds the prerequisite credential; `_allocate`/`_selective_gate`/`_university_gate` act on those
  candidates; gates are residence / exam+rank / exam+fee+rank — **no gate-place credential-requirement object**.
- **No MC run** (would be zero by construction; the declared stop rule forbids forcing it); no per-draw/MC findings,
  no boundary contingency. **What would be needed (new predeclaration + approval):** (a) a per-gate `cred_req`
  threshold applied to a share `g(N)` of places; (b) an allocation-controller mix; (c) the declared **alternative**
  `g(N) × C_value` (runnable now, but a different object) — recommended given D178's return-side finding.

---

## 3ao. COEVOLVE v0.2-YANGRETURN (D180) — return-side wiring ACTIVE in 100% of draws; β dominates, Yang premium third; wage-premium boundary does NOT reproduce

- New extension `coevolve_2026-11-21/v0_2_yangreturn/` (simulator copied; v0 and v0.1 untouched). **Wiring:**
  `C_eff(L,N)=C_L·(1+α·g(N))`, Yang `D(N)`/`g(N)`, N enters **only** via g; return-side (not gate incidence; v0.1
  showed that reading inert by construction). Designs none/yang/yang_endog (endog: one-year-lag bounded step ±0.05 on
  applicants/place, bounds [0.25,1.50]). **Contract frozen** (`PRE_DECLARATIONS.md` `3c527ce4…`); 150 draws × paired
  seeds {0,1} × 4 sizes × 3 designs = 3,600 runs; 6 workers; **identity guard PASS** (`none` ≡ v0 baseline
  byte-identically); **two runs byte-identical**; runtime 1,115 s (run 2 1,780 s under contention), no draw reduction.
- **Results:** **(a)** robust-ACTIVE `yang` **100%**, `yang_endog` **98%**, inert **0%**. **(b)** completion gap by
  size (median/p5/p95): 200k +2.927/+1.331/+5.930; 500k +4.490/+2.029/+7.196; 1m +5.672/+2.784/+7.827;
  2m +6.674/+3.610/+9.418; pooled yang **+4.956** (median +5.109; p5 +2.468; p95 +7.192); endog pooled +6.125.
  Leaving gap yang **−8.633** pp. **(c)** top-3: **β/future-weight +0.722 (65.3% share)**, **child-wage −0.324
  (14.7%)**, **premium multiplier +0.249 (6.0%)**; Yang slope +0.097 / anchor +0.028 (nearly inert). **(d)** boundary
  contingency **0/14/0/136** → the Yang-toy wage-premium boundary **does not reproduce** (all 14 toy-inert draws are
  coevolve-active; none inactive). **(e)** coexistence: at 2m `yang` vs none — unused accessible 0.171 vs 0.266;
  qualified/place 6.843 vs 5.422; gate-tutoring share 0.189 vs 0.208 (`none` identical across sizes by construction).
  **(f)** runtime as above. **Recommendation:** the Yang map is necessary but not load-bearing; next predeclared test
  should target the **β/future-weight channel**, not the premium multiplier.
