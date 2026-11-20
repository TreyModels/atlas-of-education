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
