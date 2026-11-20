# Changelog — Massification research package

All dates 2026 (Asia/Shanghai). This is the programme-level log; per-cell run records live in the experiment
manifests and error logs.

## 2026-11-20 (final) — PHASE CLOSEOUT COMMITTED; iCloud worktree retired as active checkout

- `06_report/MASSIFICATION_CLOSEOUT.md` committed as the phase's authoritative summary; pointers added to
  `LEAD_HANDOFF.md`, `NEXT_LEAD_PROMPT.md`, `06_report/EXTERNAL_CHECKIN.md` read order.
- iCloud worktree **retired as an active checkout** (canonical = GitHub branch; stable-root clone for checkpoints;
  iCloud package = read-only mirror with only the ZIP pair written back). Recorded rationale: iCloud file-loss incident.
- Final commit/ZIP hashes in the `OP: checkpoint … — phase closeout committed` bridge post; SHA256SUMS verified in
  `/tmp`, conflict scan 0. Data asks HELD; nothing external sent.

## 2026-11-20 (night, recovery) — DELIVERY INCIDENT + RECOVERY CHECKPOINT (outside iCloud)

- **Incident:** during the anchor-closure checkpoint the iCloud-synced package lost files mid-operation (directories
  emptied, truncated reads, git index timeouts). A checkpoint built against the incomplete stage (`fabe4cf`) deleted
  282 tracked files; it was pushed then **reverted on the remote by force-push to the last good commit `3e3f705`**
  (authoritative). No pre-`3e3f705` history was rewritten.
- **Recovery:** checkpoint rebuilt entirely in `/tmp` from the pre-incident ZIP extraction
  (`/tmp/massif_recover`, 1,184 files) overlaid with the uncommitted post-`3e3f705` content
  (`/tmp/massif_new_checkpoint`, 19 files); manifest/stage/SHA256SUMS/commit/ZIP built there; only the `.zip` +
  `.sha256` copied back to the iCloud package. Branch tip and ZIP hash are announced in the `OP:` checkpoint post.
- **Content now included:** Council-2 intake (D66–D78; D71–D78 bind), A1 addendum C1–C10 (C8 primary-2017 reporting
  gap; M4 not discriminable; constant back-fill + de jure enforcement disclosed; G(C)=C^0.75 text fix; M1 ≤1977;
  corrected accounting), A2d model-internal descriptive-negative, A6/A7 portability design notes (PARKED-ARMED),
  phase write-up shell with provenance block, closure STATUS §3q/§3r.
- **Provenance resolved:** linear-trend 4.35 / persistence 8.60 from `model/calib/calibration_table.csv`
  sha256-16 552e0cce04bd148d; repair fit 6.16–7.43 from `model/calib/repair_table.csv` sha256-16 34b0a5bc98e3d603.
- **Standing recommendations:** keep the iCloud package read-only until a reconciliation pass; use a stable-root copy
  (e.g. `/tmp/massif_work` or `~/massif_work`, cloned from GitHub) for future checkpoints and mirror to iCloud only at
  delivery boundaries. Data queue HELD; nothing external sent.

## 2026-11-20 (night) — ANCHOR CELL CLOSED; COUNCIL ROTATED TO COUNCIL-2

- **Council rotation executed** (context-rotation plan): expert-council → **council-2** (fresh-context subagent, party
  `deepseek-council2`); handoff `08_council/COUNCIL_STATE.md` + `10_massification/HANDOFF_expert-council.md`; authority
  persists via files; D66–D70 (first pass) kept and **D71–D78 bind**; old Council stood down.
- **PHL anchor cell CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT (D76)**: A1 descriptive report (`model/anchor_out/`) =
  milestone timing miss (M2 2024 not reproduced in 9/12 arms; M4 = 1960 initialisation artefact/not discriminable;
  M3 non-crossing passes in-window but 2/12 arms overshoot after 2024), **A6 asymmetry unreproduced 0/3**, capacity-gated
  ties law-only → capacity-timing not supported (EQUIVALENT), A2d model-internal descriptive-negative (−0.427 lag 6),
  scaling criterion FAIL standing. Remaining PHL work = **A1 addendum C1–C10 + write-up**; re-openers C1–C4 only.
- **Phase headline (exact): "conditional level reproduction + observational equivalence + an unreproduced asymmetry"**;
  "reproduces universalization"/"capacity explains timing"/"portability holds"/direction words barred.
- **Capacity data reconciled**: three dimensions canonical (data-hunter), scout composite DERIVED only; tax/GDP provenance
  resolved; WGI blocked → 0.85; de jure ≠ de facto; BEPER DATA BLOCKED; asks held.
- **Publishable objects**: bounded negative on income-scaling (model class cannot generate positive income-scaling sign
  without exogenous supply channel, R27) + equivalence/identification map with the unreproduced asymmetry (D58); write-up
  shell assigned to lit-archivist.

## 2026-11-20 (late) — SINGLE-SYSTEM PIVOT + TIMING REGIME (A4)

- **User design pivot (logged):** (1) single-system first — stand up ONE education system (best data, actually
  massifies), show the mechanisms, then test portability to Hong Kong and China; (2) mechanisms to test, especially
  **state pushes** — compulsory-education-law changes, school/place expansion (construction, teacher supply,
  pupil-teacher ratios), fee abolition — against **demand-pull** (jobs/returns) and **supply-push** (cohorts);
  (3) researchers do **web searches** (UNESCO, World Bank, national sources) for baseline data on synthetic-fitting
  questions; (4) **test different researchers' models on the same system record**. Keeps the Council gate/acceptance
  rules and the Japan timing directive (A4/R19).
- **Board restructure:** task-37 becomes the **anchor-system model** (mechanisms + calibration) with a **portability
  checkpoint to HKG/CHN**; data-hunter gets the web-search baseline-data task; lit-archivist the UNESCO/WB + rival-model
  narrative; scout prepares **event windows** for compulsory-law/expansion/fee dates. The Council is asked to **name
  the anchor system and the single-system success criteria before the runner fits** (provisional candidate:
  Philippines — best observed coverage on disk, actually massified, dated state pushes 2013 K-12 / 2018 free tuition /
  4Ps; alternatives Korea, China).
- **Council Amendment A4 (timing regime) adopted:** milestones M0 massification ≥50%, M1 primary NER≥95 (or GER≥100),
  M2 lower-sec completion ≥90, M3 upper-sec completion/transition ≥90, M4 tertiary GER ≥50; crossing year = first
  observed year at/above threshold, band = adjacent observed years; **N = ±5 y (±3 y where band ≤2 y)**; JPN/KOR/HKG
  levels CHECK-ONLY ±5 pp; crossing years are HOLDOUT outcomes, **never fitted** (R4/R5; R19 timing miss = structural
  miss); left-censored = boundary constraint, right-censored = false-positive test. Censored ratios reconstruct only
  from observed headcounts + documented population denominators, labelled **"reconstructed (not UIS)"**, with
  method/uncertainty + two-denominator sensitivity. Slate re-rank: **E6 timing comparison #2; E9 crossing-year
  reconstruction #3**; E4 #4; E2 #5; E1 #6 parked/unfielded; E3 #7 DATA BLOCKED; E5 #8; E7 #9; E8 KILL.
- **Loop-5 adjudication (D19–D30):** phase headline = **conditional reproduction + observational equivalence**; E1
  killed as the identification gate as specified (redesigned/sign-only options defined, parked); A1 scaling capped
  PARTIAL; income-scaling repair accepted for intake, timeboxed one cell/cycle; E2 accepted with claim cap/MDE;
  E3 DATA BLOCKED; M2c retro-accepted; M2b estimator range; data D16 accepted; E4 elevated to KEEP.
- **Timing artifacts landed:** scout crossing-year reconstruction (`relations/data/UNIVERSALIZATION_TIMING.csv`,
  pattern, E6 timing comparison) and exp1 timing-check predeclaration for JPN/KOR/HKG (not run, DATA BLOCKED pending
  crossing-year series); data-hunter asked for `UNIVERSALIZATION_TIMING.csv` (crossing years + intervals).

## 2026-11-20 (evening) — FIRST-ORDER PHASE: massification/universalization + schooling-jobs push-pull

- **Reorientation (user request):** the first-order question is now massification/universalization of schooling
  across countries and sectors, and the push-pull dynamics between schooling and jobs/markets; shadow education is
  demoted to secondary. The previous phase's close-out remains valid for shadow education and is not re-fit.
- **New scope:** `10_massification/` with disjoint workstreams — `data/` (jobs/markets panel, ILO/OECD corpus,
  universalization series), `lit/` (massification theory, push-pull rivals, scaling laws), `relations/`
  (universalization curves, scaling exponents, lead-lag tests), `model/` (cohort-flow push-pull model),
  `model2/` (independent scaling + rival recovery/identification), Council brief 013 (design gate).
- **Governance:** Council of Experts is authority for research direction; Lead executes and enforces the bridge
  protocol. `06_report/AGENT_PROTOCOL.md` live (`NEW:`/`ACK:`/`COUNCIL:`/`OP:`/`STOP:`/`ASK:` grammar).
  `08_council/DECISIONS.md` created (D1–D5).
- **Gate:** task-37 (model calibration) blocked until brief 013 defines "reproducing universalization" operationally
  and the stop rules (D4).
- **Follow-on from the shadow phase (same day, closed):** T1 Korea decomposition amended (M1 resolved: KEDI hours
  are per all students; one-margin arms-race participation description withdrawn; price escalation not established);
  loop 8 + loop 8b synthetic frontier (relations/ECI wired; empty support persists for the KOR gradient; HKG
  0→2/256 only); C access requests drafted and held.

## 2026-11-20 (afternoon) — shadow-education phase closed

- 40+ predeclared cells across iterations 1–8; reproduction audit (5/7 headline results reproduced); literature
  ledger (20 core sources, 68-claim register); six country cards; shadow target register (21 rows); WDI/UIS/national
  data layer with documented-imputation panel; economic-complexity panel (ECI); ranked-relation register (49 rows);
  synthetic assumption-space analysis (empty support); Council briefs 001–012.
- **Final adjudication:** five claim classes excluded by predeclared tests (gate architecture, provider technology as
  missing channel, cross-country shadow incidence, mechanism classification, country completion forecasting);
  8/9 stop rules fired; cohort conservation passed exactly. Publishable objects: negative/identification map,
  measurement programme, Korean provider/fee descriptive note.

## 2026-11-20 (evening) — synthetic workbench v1, longitudinal battery, external literature review

- **Synthetic workbench packaged** (`10_massification/extensions/synthetic_2026-11-20/`): equations register (43
  relationships; 10 `equation-in-literature` tags) + fact register (53 facts; 35 VERIFIED-FROM-DISK) + generator v0
  (7,040-row panel) + generator v1 (6,720-row tiered occupation-aware panel; authoritative worker delivery,
  controller-verified byte-identical on two clean re-runs). v1's predeclared checks: **A PASS but target-encoded · B
  FAIL (non-diagnostic: association survives both ablations) · C PASS (half structural) · D PASS · E PASS · F PASS**;
  the load-bearing object is the **stipulated upper-secondary seat cap**, so v1 reproduces the anchor asymmetry
  substantially by assuming it. An earlier same-day intermediate run (A–D FAIL) is withdrawn; the full audit trail is
  `generator_v1/TUNE_LOG.md`. **v1.1 predeclaration must** add the education→complexity channel, remove the per-level
  anchor interpolation, adopt the ablation-fail diagnostic rule, and derive the seat cap from the economy side.
- **Amendment A2 (user directive) recorded + v1.2 spec frozen:** demographic overflow (baby boom) + lagged
  capacity → congestion/quality collapse + **childworld four-state child-labour block** (structural borrow only,
  `engine/childworld.py` sha256 `ae73adb2…`; no calibrated values; caveats carried). `synthetic_2026-11-20/v1_2/
  PRE_DECLARATIONS.md` freezes the five v1.2 checks, including "PHL asymmetry from the mechanism **without per-level
  anchor interpolation**" and "no passive neither sink". v1.2 build is the next worker-sized job.
- **Measurement insight recorded:** completion can exceed GER (UIS completion uses a 3–5-years-above-grade
  denominator) — verified PHL 2024 primary **98.30 vs 94.03**; note added to `facts/STYLIZED_FACTS.md` §12 and
  `10_massification/data/DATA_NOTES_MASSIFICATION.md`. This explains part of the old model's over-scale GER artefact
  and makes "universalisation" measure-dependent.
- **Longitudinal battery corrected to final verdicts:** H1 PARTIAL, **H2 NOT SUPPORTED** (ECI S3 −2.589,
  CI −4.112…−1.067, negative-significant, opposite the canon; raw within-country r = −0.153), H3 NOT SUPPORTED,
  H4 SUPPORTED (descriptive co-movement only); "growth is the weakly-attached variable" (all nine growth pairs
  |r| < 0.21 and negative). Package rebuilt (3 stale hashes fixed; 23/23 verify). No causal/direction/Africa claims.
- **External literature review DELIVERED** (Priority 1, user ask): `10_massification/lit/external_review_2026-11-20/`
  — memo + **76 claim rows / 63 unique sources** (38 VERIFIED-FULLTEXT, 10 VERIFIED, 14 VERIFIED-ABSTRACT, 4
  VERIFIED-METADATA, 10 UNVERIFIED flagged) + citation index + repo literature audit + deterministic assembler;
  packaged 13/13 SHA256 verify. Verdicts: (a) schooling-vs-skills settled — skills not attainment (HW 2012 1 SD ≈
  1.2–2.0 pp/yr; Pritchett 2001 no association vs 0.21–0.42 benchmark; Krueger–Lindahl initial-stock reconciliation;
  Barro 2013 counterexample 0.44 pp); (b) ECI→growth modest/contested, education→complexity is capability theory with
  R=0.13 between ECI and schooling in the field's own data; (c) absorptive/threshold frame canonical but absent
  internally; (d) credential/queue theory settled and the Philippines already measured (39% overeducated, 1-in-5
  vertical mismatch, BPO 1.9M jobs/80k net adds); (e) projection models absent internally — **WIC multi-state model
  with CC BY 4.0 2023 data is directly reusable; do not rebuild the demographic engine**. Ledger audit: 0 hits for
  growth/complexity/ECI; only 10/43 equations are literature equations. "What we do NOT need to redo" (§8) and
  "what remains open" (§9) in the memo. `web_fetch` DNS-blocked; retrieval via curl, every status reflects text read.
- **Education → ECI predeclared panel analysis run** (`10_massification/extensions/edu_eci_2026-11-20/`): 272-row
  matrix, frozen rule → **1 SUPPORTED · 5 PARTIAL · 8 NOT SUPPORTED** (12/14 robust to `eci_hs92`). Primary
  completion PARTIAL at 5 and 10 years and robust (+0.003–0.008 ECI points/pp, halved by income control); adult
  literacy stock null at 10y; upper-secondary nothing; tertiary attainment negative-significant (S2, −0.0155,
  p=0.006); no low-base heterogeneity. Existing E5 **replicated exactly** (0.5932271376, se 0.1757698583, n=253,
  23 cty; true-year-lag version 0.5691, n=320, 27 cty) — real but specification-dependent (log spec, `eci_hs92`, no
  income control). Descriptive only; no causal/direction claim. Deterministic, two runs byte-identical.
- **New user directive recorded:** hypothesis is **education → economic complexity (ECI)** (growth is a different
  outcome). `synthetic_2026-11-20/MODEL_ARCHITECTURE.md` Amendment A1 requires v1.1 to encode schooling flow → X;
  a predeclared education→ECI panel analysis is queued on the existing 30-country data
  (`09_relations/LITERACY_ECI_DEMOGRAPHY.md`: literacy STOCK 0.001 ns vs primary completion lagged 10y **0.593**,
  p=0.001 — the flow tracks complexity).

## 2026-11-20 (late) — REACTIVATION: PHL critical path resumes (v1.2 build + shadow-at-gates + HKG prep)

- **User directive recorded (STATUS §3w):** the Philippine system is only partly stood up — v1.2 demographic/quality
  layer not built, no shadow-education block, demand signals/economy interactions not accurately modelled. The user's
  standing instruction is to **keep working until that exists**; HKG is a **parallel prep workstream, not a hand-off**.
  Shadow education (paused) must now "show up" **around the relevant gating** — tutoring demand as a demand signal at
  the gates/queue, not a generic add-on.
- **Three workers dispatched** (disjoint dirs, predeclare-first, labelled): W1 builds `generator_v1_2/` to the frozen
  v1.2 spec (check A **without per-level anchor interpolation**, childworld four-state structural borrow, five checks);
  W2 designs `shadow_module/` (SHADOW_MODULE.md + frozen predeclaration + parameter table + dry-run plan for v1.3:
  tutoring demand = f(gate pressure, expected returns, family income), tutoring raises gate-passing probability/rank,
  near-zero at primary, HKG-high/PHL-mid/KHM-low ordering predeclared); W3 prepares `hkg_transfer_2026-11-20/`
  (inventory + frozen D75 transfer predeclaration + checklist, run-ready not run).
- **Next integration:** MODEL_ARCHITECTURE **Amendment A3** — demand signals (expected returns × gate probability ×
  sector structure × migration/remittances) and the shadow block at gates; verify/package/commit each deliverable and
  rebuild the ZIP.

## 2026-11-20 (reactivation batch 2) — v1.2 built, shadow module frozen, HKG prep blocked, theory frame merged

- **v1.2 DELIVERED** (`synthetic_2026-11-20/generator_v1_2/`): 30×56×4 = 6,720-row SYNTHETIC panel; declared PHL
  cohort path; childworld four-state structural borrow; lagged capacity → congestion/quality → completion;
  education→X at lag 10. Predeclared checks **A–E PASS** with decisive caveats disclosed (A scored on the UIS series
  with single declared m = 1.10; cohort-flow series would fail A; parameters calibrated in design phase → feasibility
  demonstration, not blind test; ceiling demand/quality-driven, not boom-driven; 0 identity violations in scored run).
  Supply-rule audit: 0 country branches, 0 anchor arrays. Determinism and all manifest hashes verified by the controller.
- **Shadow-education gating module DESIGNED + FROZEN** (`shadow_module/`): tutoring demand at gates from queue/
  transition/rank pressure, positional credential value, family income; frozen predeclaration sha256 `cf8c61cb…`;
  checks c1–c6 incl. no-re-fit guard; 42-row parameter table; dry-run plan; toy design check PASS c1/c2/c3/c5; controller
  S1 pre-run note corrects the "HKG>PHL>KHM" assumption (KHM 68.4 case study > PHL 46.5 all-basic; c4b is a
  cohort-incidence synthetic check).
- **HKG transfer prep BLOCKED** (`hkg_transfer_2026-11-20/`): D75 targets verified (NER ≥90 1974; ≥95 1979; 1977-vs-1979
  resolved and disclosed); frozen predeclaration `99be01d7…`; blocked by SR-1 (no NER object in the model), SR-2, SR-9;
  no results. v1.2.1 queued to add NER output + audit the identity fix.
- **Council cycle 12 merged**: brief_020 decisions D102–D105; BIG_PICTURE/COUNCIL_STATE cycle-12 addenda;
  `MODEL_ARCHITECTURE.md` **Amendment A4 DECLARED-THEORY** (scaffold/induction/exit-cost/shadow frame; no parameters or
  layers; conditional gates on WT1&WT3 / DT1&DT2; theory-only, never evidence). WT and DT batteries dispatched.

## 2026-11-20 (reactivation batch 3) — WT + DT theory-test batteries: both conditional gates fail

- **WT battery** (`wt_2026-11-20/`, predecl `d3ad365e…`, 13/13 SHA verify, deterministic): WT1 NOT SUPPORTED
  (depth ratio 0.601 > 0.50), WT2 NOT SUPPORTED (4/10 decoupled countries reverse), WT3 NOT SUPPORTED (income-partial
  ρ = −0.520, sign flip), WT4 SUPPORTED descriptive (0 exit episodes; fragile), WT5 DESIGN-ONLY/NOT SCORED (block's
  1.889 is cross-year HKG 2010 senior / 1996 primary; same-year HKG 1996 = 0.889 → no gradient). **D101 gate not met:
  exit-cost/complementarity layer PARKED.**
- **DT battery** (`dt_2026-11-20/`, predecl `6ed67b82…`, 10/10 SHA verify, deterministic): DT1 NULL (income-partial
  ρ = +0.0146 vs raw +0.3867; 5 countries), DT2 NON-NULL (E_entrant +1.605, p = 0.00036; reproduces on-disk D1),
  DT3 UNABLE/HELD, DT4 NULL, DT5 NULL (PHL z = −0.508). **D104 gate not met: induction grounding PARKED; A1/A3 stay
  declared assumptions with no theory citation.**
- DECISIONS D106–D107 record both outcomes. Queue: v1.3 shadow build, v1.2.1 NER object (W4 in progress), A3 demand
  implementation; HKG run still needs explicit Council authority (SR-9).

## 2026-11-20 (reactivation batch 4) — v1.2.1 NER output object (HKG interface blocker cleared, with a declared limitation)

- `synthetic_2026-11-20/generator_v1_2_addendum/`: adds NER columns to the frozen v1.2 panel by **age-structure
  derivation** (`ner = 100 × admitted_official / cohort`); 6,720 rows, 67 columns unchanged, 10 appended; invariance 3/3
  PASS (v1.2 re-runs byte-identical, rows/keys preserved, `enrolment = admitted_official + admitted_overage` and
  `ner ≤ ger` hold); predecl `aa756f8b…`; smoke test PHL-like first-sustained NER ≥90 = 2007, ≥95 = 2016 (SYNTHETIC,
  diagnostic only). **Declared limitation: cohort-flow NER analogue, not the UIS stock-based NER** — the HKG timing
  test is now runnable at the interface but SR-9 (Council authority) remains open. No HKG run performed.

## 2026-11-20 (reactivation batch 5) — Council cycle 13: WT/DT adjudicated, both gates parked, SR-9 granted with conditions, five experiments

- **D108–D113 merged**: WT ACCEPTED (WT2 VOID as paper test; WT4 fragility sentence corrected; WT5 cross-year error
  recorded as Council-side); DT ACCEPTED (DT4 NULL-BY-CONSTRUCTION; DT1 scoped; DT5 near-circular). Both conditional
  gates confirmed **PARKED** (exit-cost layer; induction grounding). **v1.2 recorded PASS-CONDITIONAL** with three
  record corrections applied (m = 1.10 restated as convention; cross-year 1.136 ratio removed from v1.2 FINDINGS; A4
  "theory-grounded" → "candidate grounding — PARKED per D104"; HKG SR-2 path status note). **SR-9:
  AUTHORISE-WITH-CONDITIONS (H1–H6)** — HKG diagnostic transfer gated on the M1-NER construct-equivalence test and five
  other conditions; no run executed; TRANSFER-FAILS is the informative outcome. **Five experiments adopted:** CEIL-ATTRIB
  #1, A3-D #2, M1-NER #3, A3-S #4 (= v1.3), ASYM-K #5 drop-first. D113: re-derive block numbers before freeze;
  paper-test series terminated this phase.

## 2026-11-20 (reactivation batch 6) — CEIL-ATTRIB + M1-NER outcomes; v1.3 final snapshot; HKG measure blocker

- **CEIL-ATTRIB** (`ceil_attrib_2026-11-20/`, predecl `ed9b31b9…`, 24/24 SHA): Test A **MIXED** (mechanism ablations
  ≥2 pp but calibration knobs also ≥2 pp); Test B **PIPELINE-CONSISTENT** (7/8 observed PHL pairs in [0.90,1.10] at a
  3-year lag) → **overall `PIPELINE-CONSISTENT`**: the upper-secondary ceiling is reclassified as a **lower-secondary
  pipeline** object (D63 stays UNABLE as to cause); v1.2's "mechanism produces the ceiling" claim is **not licensed**.
- **M1-NER** (`m1_ner_2026-11-20/`, predecl `9eb35a92…`, 16/16 SHA): **H1 NOT ADMISSIBLE** — max |stock−flow| 2.685 pp
  (7/15 band years fail), crossing differences 3 y/2 y; the cohort-flow NER analogue leads a stock object by 2–3 years.
  **HKG diagnostic transfer is `BLOCKED-MEASURE(SR-1)`; D111 authorisation void for this object**; a new predeclaration
  with a stock NER object (and a new Council decision) would be required. No HKG result.
- **v1.3 final snapshot re-committed**: thresholds fix + bug disclosures (TUNE_LOG); controller re-verified two clean
  runs byte-identical and the c6 no-re-fit guard; **c4a/c4b FAIL stand** (HKG level 0.340 vs 0.75–0.95; HKG−PHL gap
  0.0967 vs 0.10).
- DECISIONS **D114** (M1-NER/H1 + HKG blocked) and **D115** (CEIL-ATTRIB) recorded. Next: EXP-2 A3-D demand core.

## 2026-11-20 (reactivation batch 7) — EXP-2 A3-D demand core FALSIFIED; A3 PARKED

- `generator_v1_4_demand/` (predecl `9ed0cae3…`, deterministic, 18/18 SHA): **FALSIFIED** — the demand block does not
  replace the upper-secondary taste parameter. d1/d2 fail on PHL (at bound; HKG +1.52/+2.47, KHM +4.77/+10.33), d3
  −0.58 pp vs +2.0 bar, d6 PASS; replacement test +18.05 pp outside [73,77] (NOT DEMAND-ROBUST, not re-tuned);
  ablation +18.41 pp → NON-DECORATIVE (destroys the ceiling); no-re-fit guard PASS (OFF panel = v1.3 panel byte-identical,
  placebo same). Migration/remittances DECLARED/NOT-VERIFIED and tiny. **Structural finding: P(advance) ≈ 0.999 at the
  upper gate → the gate-probability channel is near-inert; the ceiling is not a demand-rationed gate (consistent with
  CEIL-ATTRIB's pipeline reclassification).** **Disposition: A3 demand core PARKED; no demand layer wired** (D116).
- **USER CORRECTION (Lead-recorded): demand is NOT falsified** — it is revealed and strong (shadow education,
  queues/competition for good schools, closure reactions, credential chasing). What failed is the **specified block at
  an unrationed gate** (`P(advance) ≈ 0.999`): a **model-specification failure**; correct label "the unrationed
  single-gate model cannot represent a bimodal system". Successor: **Amendment A5 / v1.5 BIMODAL-GATE** (two-tier
  gates — open-access low-cost seats that can go unfilled + rationed high-quality gates with queues/rank/shadow —
  explicit outside option, binding rationing, shadow re-anchor, tier-specific exit cost for the Council). No re-tune of
  A3-D; no fitting to the known outcome.

## 2026-11-20 (reactivation) — user structural correction: bimodal system; Amendment A5 / v1.5 BIMODAL-GATE

- **No "demand falsified" language.** The A3-D result is relabelled **"the unrationed single-gate model cannot represent
  a bimodal system"** — a model-specification failure; demand is revealed and strong (shadow education, queues for good
  schools, closure reactions, credential chasing). Record corrections applied to DECISIONS D116, v1.3/v1.4 FINDINGS,
  STATUS and CHANGELOG.
- **`MODEL_ARCHITECTURE.md` Amendment A5 (first-class requirement):** two-tier gates — open-access low-cost seats that
  can go untaken + rationed high-quality gates with queues/rank/shadow — plus explicit outside option (childworld
  four-state), sorting by income/ability/taste, returns differing by tier, and **tier-specific exit cost** (cheap exit
  from the open seat; expensive exit from the credential gate) as a WT-adjacent Council question. v1.5 checks (a)–(e)
  frozen before run, incl. **no free taste parameter** and a no-re-fit guard; true seat utilisation **HELD DATA ASK**
  (DepEd/CHED seats vs enrolment, private/public shares, SHS voucher take-up) — declared proxies only, labelled DERIVED.
- Next: frozen v1.5 predeclaration after the Council cycle-14 merge. No re-tune of A3-D; no fitting to the known outcome.

## 2026-11-20 (reactivation) — Council cycle 14 merged; user corrections + macro-principle (ratchet); bimodal v1.5 queued

- **D117–D123**: model-line batch adjudicated — all four verdicts stand, no re-runs. EXP-1 CEIL-ATTRIB
  ACCEPT-WITH-CONDITIONS (band one-sided; generator ratio >1.10 in 12 anchor-type years); EXP-2 A3-D FALSIFIED narrowed
  (PHL saturation artefact; substitution used school gate ≈0.999 vs binding rung-4 ≈0.151 — 6.6× domain error); EXP-3
  M1-NER ACCEPT; A3-S/v1.3 ACCEPT-WITH-CONDITIONS (c4b not informative at 0.0033). Pipeline reclassification confirmed
  **as location** (object = `upper_t/lower_{t−3}`, one admissible numerator). HKG `BLOCKED-MEASURE` terminal.
- **New disclosures:** v1.2 is **crossing/endpoint placement, not a path** (9/33 within ±5 pp; D119); the generator has
  **no cross-level linkage** (ratio >1.10 in 12 anchor years, max 1.444); school gate rations at primary/lower (87.4% /
  93.3%) not upper/tertiary (6.5% / 0%); the binding queue is **rung-4 absorption ≈0.151**. Record items fixed (+18.05
  vs +18.4064; v1.4 SHA256SUMS 38/38; v1.3 binding spec hash).
- **D124 (user correction): no "demand falsified"** — correct label "the unrationed single-gate model cannot represent
  a bimodal system"; **Amendment A5 / v1.5 BIMODAL-GATE** (two-tier gates, untaken free seats, outside option,
  tier-specific exit cost, checks a–e, no free taste parameter, no-re-fit guard; true seat utilisation = HELD DATA ASK).
- **D125 (user macro-principle): the ONE-WAY RATCHET** — declared theory (never evidence): no reverse/reversal term,
  shocks as declared inputs, options path-created; stronger than exit-cost asymmetry (exit cost is *why* the ratchet
  holds); honest bound: data show **setbacks without reversal** (PHL upper-sec −8.16 pp then 75.03, never ≥90; WT4 zero
  sustained exits, fragile), strong claim **untestable**; recorded in `THEORY_FRAME.md` + MODEL_ARCHITECTURE A4.
- Next model line object = transition ratio + declared κ=0.949 link; sequencing EXP-7 → EXP-6 → EXP-8 → EXP-9 →
  EXP-10; **EXP-7 dispatched** (gates downstream predeclarations). DOMUS noted, not integrated.

## 2026-11-20 — EXP-7 REPRO-PATH: v1.2 ENDPOINT-ONLY; κ-link valid; pipeline to be built into v1.5 (D126)

- `repro_path_2026-11-20/` (predecl `74f9d0e0…`, deterministic, baseline guard PASS): **leg A `ENDPOINT-ONLY`** —
  9/33 within ±5 pp vs the ≥17/33 bar (medians −4.30/−29.44/−27.59; worst upper 1999 −36.62); **leg B κ-link VALID**
  (κ = 0.949 declared from the observed median; 20/53 → 0/53 violations; guards pass) with class **b2** (linked upper
  2024 63.97, delta −12.67 pp). The pipeline link must be built into v1.5; v1.5 BIMODAL-GATE predeclaration (κ + two
  orthogonal no-refit guards) in production. No re-fit; no causal/direction claim.

## 2026-11-20 — Amendment A5 / v1.5 BIMODAL-GATE predeclaration FROZEN, run-ready NOT RUN (D127)

- `generator_v1_5_bimodal/` (predecl `7178e3d2…`, 32/32 SHA; no results/RNG): Tier O open low-cost places with unfilled
  places as a primary object (no reallocation to Tier H); Tier H rank-rationed carrying both the school gate and the
  credentialed-job rung (p4 ≈ 0.151, V8); childworld outside option; **κ = 0.949 structural in-loop admission cap**
  (declared, never fitted); **one-way ratchet** (three declared absences, no reversal term, no reversal diagnostic);
  checks (a)–(e) with thresholds and four arms (A00 guard = byte-identical v1.3 panel).
- **Pre-freeze expectation declared:** κ×67.4073 = 63.9695 ⇒ check (b) expected MIXED; (a) a representation check.
  **HELD DATA ASK:** DepEd/CHED seats-vs-enrolment by track/region, private/public shares, SHS voucher take-up,
  utilisation/quality — proxies only, DERIVED, distortions stated. Scope honesty: current stack already has 0.1418 spare
  upper places + a binding job gate, so "bimodal" = three declared absences.
- **Not run**; parks intact until the v1.5 build/run. No re-tune of A3-D; no fitting to the known outcome.

## 2026-11-21 — EXP-6 PIPE-LOO (PREDICTIVE 3/4; per-system κ) and EXP-8 GATE-LOCUS (floor gate; upper-gate line closed)

- **EXP-6** (`pipe_loo_2026-11-20/`, predecl `97033df0…`, 13/13 SHA, deterministic): **PREDICTIVE (3/4)** at the declared
  boundary — PHL n=8, median |LOO error| 1.50 pp, 87.5% within ±5 pp; KOR 0.48 pp/89.5%; KHM 2.17 pp/90.9%; CHN
  14.48 pp/0.0% (fails). **Per-system κ: PHL 0.949, KOR 0.990, KHM 0.595, CHN 0.722** — a single κ misstates KHM by
  ~0.40. Thin/uneven pass; D63 stays UNABLE; no direction claim.
- **EXP-8** (`gate_locus_2026-11-20/`, predecl `a8566fbf…`, 25/25 SHA, deterministic): school gate binds at
  **primary 79.1%/87.4%** and **lower 91.3%/93.3%** of country-years (0.95/0.99 bars) but **upper 4.7%/6.6%** and
  **tertiary 0%/0%** → **upper-gate line CLOSED**; anchor upper `p_off=1.0000` all 56 years; rung-4 absorption median
  **0.151**. Falsifier not tripped; A3-D d2 and A3-S c4a explained, not reopened; **EXP-9 dispatched**. Caveat: v1.3 g3
  panel vs flow panel tertiary p_off ≡ 1.0 disclosed.
- D128/D129 recorded; STATUS 3ac(m)/(n).

## 2026-11-21 — EXP-9 RUNG-PROB: NOT DEMAND-DERIVABLE; A3 demand line KILLED (D130)

- `rung_prob_2026-11-20/` (predecl `1cd399dd…`, deterministic, 21/21 SHA): arm A (school-gate P≈0.999) upper 2024
  **95.05** (+16.05 above the band; ablation +18.41 pp, NON-DECORATIVE); arm B (rung-4 P≈0.151) upper 2024 **42.13**
  (−28.87 below the band; ablation −34.51 pp). **Both outside [71,79] → NOT DEMAND-DERIVABLE → the A3 line is KILLED**
  (not parked); the taste parameter is irreducible without a fit. Baseline guards PASS (G1 = v1.3 panel; G2 = frozen v1.4
  panel); no re-tune; A3-D FALSIFIED stands; "demand falsified" language still banned.

## 2026-11-21 — v1.5 BIMODAL-GATE BUILT AND RUN: representation works, level FAILS, two implementation defects (D131)

- `generator_v1_5_bimodal/` run to the frozen predecl (`7178e3d2…`; controller-verified deterministic; 84/84 SHA):
  **a=MIXED; b=FAIL; c=MIXED; d=FAIL; e=MIXED; ALL=FAIL.** **Representation works:** PHL-like 2010–2024, Tier O upper
  unfilled 0.648–0.932 coexisting with Tier H queue ratio 1.29–1.93 and p4 ≈ 0.25 in all 15 years; a-i/a-ii/a-iii hold;
  a-iv mislabelled in the predecl (A00 same_level 0 vs A01 15 because the κ cap creates same-level counts).
  **Level fails:** Tier O quality 0.55 → survival ≈0.48–0.51 → primary 51.63, upper 33.68 (collapse not stall).
  **(d) FAIL:** child-wage substitution wrong sign (+1.081 pp vs ≤ −2.0) despite 0 free-taste audit hits and working
  quality sensitivity. **(c) MIXED:** open-tier gap +2.16 > +1.0 bar. **(e) MIXED:** **A00 guard PASS (v1.3 panel
  byte-identical)**; frozen 20/20; determinism PASS; κ 20/53→0/53 — but the in-loop κ cap breaches cell identity
  (`KAPPA-GUARD-FAIL`). **A01 linked upper 2024 = 55.657** (≤63.97 but 8.31 below: cap bounds entry cohort, upper
  survival 0.870); required lower-2021 80.76 vs generator 67.41. No rescue/re-tune; parks stay; A3 KILLED; D63 UNABLE.

**v1.5 post-run disclosures (Lead-recorded; no re-score):** outside refusal set = `max(U_work, U_neither)` (U_both is a
school state; as an outside value it dominates Tier O 15/15 cells → would drive T_O ≡ 0; affected-cell count published
per cell); outside option at cell income; tertiary tier-choice has no equilibrium in the frozen child block → declared
carry-forward; `D_O` year-invariant by construction; κ-binding reduction order over-age → Tier H → Tier O; process error
B1 — pre-run SHA snapshot reconstructed (30/33 match, original hash `89638b39…` recorded). No threshold altered.

## 2026-11-21 — Council cycle 15 merged (D132–D137); per-system κ; v1.5 defect rulings; EXP-10 design (HKG DEFER)

- **Cycle 15**: all model-line verdicts stand, no re-runs. **Per-system κ: PHL 0.9491 / KOR 0.9898 / KHM 0.5950 / CHN
  0.7222** (single κ overstates KHM by 0.354; CHN not forward-usable). EXP-7's 63.97 is an admission-cohort bound
  (realised endpoint 55.66). EXP-8 floor gate binds; upper-gate line CLOSED (falsifier measure-dependent). EXP-9 →
  **A3 line KILLED** (model-side only). v1.5 admitted for **REPRESENTATION ONLY**.
- **D134 v1.5 defect rulings (binding on V16):** κ cell-identity guard **mis-specified** (completion units + survival
  explicit; projection order + propagation ledger + counterfactual identity; one cap register); child-wage sign test
  **structurally unfirable** under a binding cap (re-specify object: A10 κ OFF, pre-cap object); Tier O quality belongs at
  the **return/take-up** margin (no grid search; retire the (b) family for ≥17/33 ±5 pp); a-iv leg is a pre-run label
  error (A00 0 vs A11 15; contrast A00 vs A11).
- **A10/D62 scope:** floor universalization at seat_coverage 0.8722 via declared phys_cap=1.15 — conditional until
  FLOOR-CLOSE. **D63** observed-side necessary condition recorded (κ-implied upper max 2027 = 87.710; observed 2024 upper
  1.75 pp inside its bound).
- **EXP-10 stock-NER design** delivered (predecl `6f5d3c16…`, PRE_DECL-FROZEN, 20/20 SHA, target never read; run-ready
  not run) — but after cycle 15's cut, so **HKG = DEFER-HKG** per D120's timing rule (new Council decision required; the
  frozen design artifact is preserved).
- Next slate: EXP-11 KAPPA-FWD, EXP-12 FLOOR-CLOSE, EXP-13 LOWER-DEF (parallel), EXP-14 V16-REPAIR (after 11+13),
  EXP-15 CONV-REG (drop-first). HELD queue complete; no proxy substitution.

## 2026-11-21 — EXP-11 KAPPA-FWD: WINDOW-ONLY; κ is not a forward constraint (D138)

- `kappa_fwd_2026-11-20/` (predecl `bda79ac4…`, deterministic, 14/14 SHA): PHL slope −0.000704 (pass) but half-shift
  2.13 pp (fail) → κ-TRENDING, hold-out 2/2; KOR slope +0.002875 / shift 0.64 pass → κ-STABLE but 0/3 forward cells; KHM
  slope +0.017318 / shift 7.44 fail; CHN reported only. Aggregate 3/7 within strict bound, 4 violations → BOUND-BREAKS;
  falsifier tripped; verdict invariant. **V16-REPAIR: κ may not be a forward constraint** — within-window trajectory only
  (never extrapolated) or dropped. No re-fit.
